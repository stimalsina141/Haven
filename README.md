# Haven — Anonymous Peer Support Platform

Full-stack web application enabling users to share personal experiences anonymously while receiving peer support. Built with Django, featuring secure authentication, randomized content visibility, and privacy-preserving architecture.

## Key Features
- Anonymous posting with UUID-based username generation
- Secure user authentication (Django auth: PBKDF2 password hashing, CSRF protection)
- Randomized feed algorithm for equitable content visibility
- Category-based filtering (Celebration, Struggle, Decision Help, Grief)
- Responsive design with Django templates

## Tech Stack
- **Backend:** Python, Django 6.0.5
- **Database:** SQLite (development)
- **Frontend:** HTML, CSS, JavaScript (Django templates)

## Architecture
Modular app structure following Django’s MVT pattern:
- `users` app: authentication and user management
- `posts` app: content creation, display, and filtering

## Local Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install django==6.0.5
python manage.py migrate
python manage.py runserver
```

Open: http://127.0.0.1:8000/

## Notes
- `db.sqlite3` is local-only (don’t commit it).
