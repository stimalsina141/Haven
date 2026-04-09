# Haven (Django)

A Django project with apps:
- `posts`
- `users`

## Requirements
- Python 3.x
- pip
- (Recommended) virtual environment

## Setup (Mac/Linux)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run migrations
```bash
python manage.py migrate
```

## Start the server
```bash
python manage.py runserver
```

Then open:
- http://127.0.0.1:8000/

## Notes
- `db.sqlite3` is ignored (local only).
