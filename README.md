# Todo-Back

Django REST API for a todo application with categories and tasks management.

## Stack

- **Django 5.2** + **Django REST Framework**
- **CORS** via `django-cors-headers`
- **SQLite** (development) / **PostgreSQL** (production)
- **Gunicorn** + **WhiteNoise** (production)

## Project structure

```
todo-back/
├── todo/
│   ├── core/               # Django project (settings, urls, wsgi)
│   │   └── settings/
│   │       ├── base.py         # Common settings
│   │       ├── development.py  # Local dev (SQLite, DEBUG=True)
│   │       └── production.py   # Production (PostgreSQL, WhiteNoise, HTTPS)
│   ├── categories/         # Categories app
│   │   └── management/
│   │       └── commands/
│   │           └── seed_categories.py  # Seed default categories
│   └── tasks/              # Tasks app
├── requirements.txt
└── .env.example
```

## Quick start

### 1. Clone and set up the virtual environment

```bash
git clone <repo-url>
cd todo-back

python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Generate a secret key and add it to `.env`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Run the development server

```bash
python manage.py migrate
python manage.py runserver
```

API available at `http://localhost:8000`.

---

## API endpoints

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health/` | Health check for PaaS platforms |
| GET | `/error/` | Trigger a test error (Sentry verification) |

---

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories/` | List all categories |
| POST | `/api/categories/` | Create a category |
| GET | `/api/categories/<id>/` | Retrieve a category |
| PATCH | `/api/categories/<id>/` | Update a category |
| DELETE | `/api/categories/<id>/` | Delete a category |

**POST example:**

```json
{
  "name": "Work"
}
```

---

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks/` | List all tasks |
| POST | `/api/tasks/` | Create a task |
| GET | `/api/tasks/<id>/` | Retrieve a task |
| PATCH | `/api/tasks/<id>/` | Update a task |
| DELETE | `/api/tasks/<id>/` | Delete a task |

**POST example:**

```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "category": 1,
  "completed": false
}
```

---

## Deployment

### Settings

The project uses a split settings structure. The default is `development`. In production, override via environment variable.

| File | Used when |
|------|-----------|
| `todo.core.settings.development` | Local development (default) |
| `todo.core.settings.production` | Production |

### Required environment variables (production)

| Variable | Description |
|----------|-------------|
| `DJANGO_SETTINGS_MODULE` | `todo.core.settings.production` |
| `SECRET_KEY` | Django secret key — generate a new one |
| `DATABASE_URL` | PostgreSQL URL: `postgres://user:pass@host:5432/db` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed domains |
| `CORS_ALLOWED_ORIGINS` | Comma-separated list of allowed frontend origins |
| `SENTRY_DSN` | Sentry DSN for error tracking (optional) |

Copy `.env.example` to `.env` and fill in the values. Never commit `.env` to version control.

### Start command (Gunicorn)

```bash
gunicorn todo.core.wsgi:application
```

### Build Command (Render)

```bash
pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate && python manage.py seed_categories
```

`seed_categories` uses `get_or_create` — idempotent, safe to run on every deploy. Creates default categories (Hooman, Work, Food) if they don't exist.

### First deploy checklist

```bash
# Collect static files
python manage.py collectstatic --noinput

# Apply migrations
python manage.py migrate

# Seed default categories
python manage.py seed_categories
```
