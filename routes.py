from flask import request, render_template, flash, redirect, url_for
from urllib.parse import urlparse
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from app import app, db
from models import User, Post
from forms import RegistrationForm, LoginForm, DestinationForm


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create the user object
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        # Add and commit inside try/except to catch unique constraint errors
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Username or email already exists. Please choose a different one.')
            return redirect(url_for('register'))

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).all()

    form = DestinationForm()
    if request.method == 'POST' and form.validate():
        new_destination = Post(
            city=form.city.data,
            country=form.country.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(new_destination)
        db.session.commit()
        flash('Destination added successfully!')
        return redirect(url_for('user', username=user.username))
    elif request.method == 'POST':
        flash(form.errors)

    return render_template('user.html', user=user, posts=posts, form=form)


@app.route('/')
def index():
    posts = Post.query.join(User).\
        filter(User.id == Post.user_id).\
        order_by(Post.timestamp.desc()).all()
    return render_template('landing.html', posts=posts)


@app.route('/post/<int:post_id>/edit', methods=['POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.user_id != current_user.id:
        flash('You can only edit your own posts!')
        return redirect(url_for('index'))
    
    new_description = request.form.get('description')
    if new_description:
        post.description = new_description
        db.session.commit() 
        flash('Your post has been updated!')
    
    return redirect(url_for('user', username=current_user.username))


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    # Example: Deleting records
    post = Post.query.get_or_404(post_id)
    
    if post.user_id != current_user.id:
        flash('You can only delete your own posts!')
        return redirect(url_for('index'))
    
    db.session.delete(post)  
    db.session.commit()      
    flash('Your post has been deleted!')
    
    return redirect(url_for('user', username=current_user.username))


@app.route('/search')
def search_posts():
    query = request.args.get('query', '')
    country = request.args.get('country', '')
    
    posts_query = Post.query
    
    if query:
        posts_query = posts_query.filter(
            (Post.description.ilike(f'%{query}%')) | 
            (Post.city.ilike(f'%{query}%'))           
        )
    
    if country:
        posts_query = posts_query.filter(Post.country.ilike(f'%{country}%'))
    
    posts = posts_query.order_by(Post.timestamp.desc()).all()
    
    return render_template('landing.html', posts=posts, query=query, country=country)



