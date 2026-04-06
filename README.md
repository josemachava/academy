# Django Auth

A Django authentication app with email/password login and full user registration.

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optional — admin panel
python manage.py runserver
```

Then open http://127.0.0.1:8000/

## Routes

| URL           | View       | Description                      |
|---------------|------------|----------------------------------|
| `/`           | login      | Sign in with email & password    |
| `/signup/`    | signup     | Register with name, email & pw   |
| `/logout/`    | logout     | Signs out and redirects to login |
| `/dashboard/` | dashboard  | Protected page (login required)  |
| `/admin/`     | admin      | Django admin panel               |

## Features

- Custom `User` model using email as the login identifier
- Sign up with first name, surname, email, password, repeat password
- Password strength indicator on signup
- "Remember me" toggle (session expires on browser close if unchecked)
- Flash messages on login, signup, and logout
- `@login_required` protection on the dashboard
- SQLite by default — swap `DATABASES` in `settings.py` for PostgreSQL
