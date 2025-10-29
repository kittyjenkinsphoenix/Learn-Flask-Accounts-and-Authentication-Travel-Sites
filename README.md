# Learn-Flask-Accounts-and-Authentication-Travel-Sites

A small Flask web application that demonstrates user accounts, authentication, and posting simple travel destinations. Users can register, sign in, create/delete/edit short destination posts (city, country, description), and search posts.

This repository is intended as a learning project and includes examples of:

- Flask application structure
- Flask-WTF forms and validation
- Flask-Login for session management
- Flask-SQLAlchemy models and database usage (SQLite)

Contents
- `app.py` — application factory / main app runner
- `routes.py` — view functions (login, register, post CRUD, search)
- `models.py` — SQLAlchemy models: `User` and `Post`
- `forms.py` — WTForms definitions (RegistrationForm, LoginForm, DestinationForm)
- `create_db.py` — helper script to create the SQLite database
- `my_database.db` — the SQLite database (created at runtime)
- `templates/` — Jinja2 templates for pages (base, landing, login, register, user)

Requirements

You can use the system Python or a virtual environment. The project uses these packages:

- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- email_validator (used by WTForms Email validator)

Quick setup (Windows / PowerShell)

1. Create and activate a virtual environment (optional but recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

2. Install dependencies:

```powershell
pip install flask flask-sqlalchemy flask-login flask-wtf email-validator
```

3. Initialize the database (creates `my_database.db`):

```powershell
python create_db.py
```

4. Run the app:

```powershell
python app.py
```

Open a browser and visit http://127.0.0.1:5000. Useful URLs:

- `/register` — create a new account
- `/login` — sign in
- `/` — landing page (shows posts)
- `/user/<username>` — view a user's page and create destinations (login required to post)

Notes about common issues

- IntegrityError on registration: If you see "UNIQUE constraint failed: user.username" it means a username (or email) already exists. Use a different username or delete `my_database.db` to start over.
- email validation: WTForms' `Email()` validator requires `email_validator` (installed above). If you see an exception about `email_validator`, install that package.
- Circular imports: `app`, `models`, and `routes` are wired so `db` is initialized before importing routes/models. If you restructure files, follow the same order (create app and db first, then import views and models).

Developer tips

- To reset the database during development, stop the server, delete `my_database.db`, then run `python create_db.py`.
- To show validation and flash messages, edit `templates/register.html` and `templates/base.html` to render `get_flashed_messages()` and display `form.errors` inline.
- To run in production use a WSGI server (e.g., Gunicorn) and do not use `app.run(debug=True)`.

Testing the registration flow

1. Go to `/register` and create a new user. The form will validate uniqueness of username and email.
2. After registering, go to `/login` to sign in.
3. Once logged in, visit `/user/<your-username>` to add a destination post.

Where to look next in the code

- `routes.py` — examples of add/update/delete operations using `db.session.add/commit`, and handling `IntegrityError` on registration.
- `models.py` — password hashing helpers and relationships (User.posts -> Post.author).

License

This project includes the included LICENSE file. Use it as a learning resource.

If you'd like, I can also:

- Add a `requirements.txt` listing pinned versions
- Improve the README with a screenshot or example data
- Add inline form error display in the templates

Tell me which of those you'd like next and I'll implement it.
