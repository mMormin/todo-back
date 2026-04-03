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
├── .github/
│   └── workflows/
│       └── ci.yml          # CI pipeline (pytest on push/PR)
├── todo/
│   ├── core/               # Django project (settings, urls, wsgi)
│   │   ├── settings/
│   │   │   ├── base.py         # Common settings
│   │   │   ├── development.py  # Local dev (SQLite, DEBUG=True)
│   │   │   └── production.py   # Production (PostgreSQL, WhiteNoise, HTTPS)
│   │   └── management/
│   │       └── commands/
│   │           └── create_superuser.py  # Create superuser from env vars
│   ├── categories/         # Categories app
│   │   └── management/
│   │       └── commands/
│   │           └── seed_categories.py  # Seed default categories
│   └── tasks/              # Tasks app
│       └── tests.py        # Model + API tests
├── build.sh            # Render build script
├── pytest.ini
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

| Method | Endpoint   | Description                     |
| ------ | ---------- | ------------------------------- |
| GET    | `/health/` | Health check for PaaS platforms |

---

### Categories

| Method | Endpoint                | Description         |
| ------ | ----------------------- | ------------------- |
| GET    | `/api/categories/`      | List all categories |
| POST   | `/api/categories/`      | Create a category   |
| GET    | `/api/categories/<id>/` | Retrieve a category |
| PATCH  | `/api/categories/<id>/` | Update a category   |
| DELETE | `/api/categories/<id>/` | Delete a category   |

**POST example:**

```json
{
  "name": "Work"
}
```

---

### Tasks

| Method | Endpoint           | Description     |
| ------ | ------------------ | --------------- |
| GET    | `/api/tasks/`      | List all tasks  |
| POST   | `/api/tasks/`      | Create a task   |
| GET    | `/api/tasks/<id>/` | Retrieve a task |
| PATCH  | `/api/tasks/<id>/` | Update a task   |
| DELETE | `/api/tasks/<id>/` | Delete a task   |

**POST example:**

```json
{
  "title": "Buy groceries",
  "category": 1,
  "is_completed": false
}
```

---

## Testing

Tests use **pytest** with `pytest-django` and `pytest-xdist` (parallel execution).

### Run all tests

```bash
pytest
```

### Run by marker

```bash
pytest -m model   # model-layer tests only
pytest -m api     # API endpoint tests only
```

### Configuration ([pytest.ini](pytest.ini))

| Option | Value |
| ------ | ----- |
| `DJANGO_SETTINGS_MODULE` | `todo.core.settings.development` |
| `-n auto` | runs tests in parallel across all CPU cores |

### Test files

| File | Coverage |
| ---- | -------- |
| `todo/tasks/tests.py` | Task model + Tasks API endpoints |

### What is tested

**Model (`@pytest.mark.model`)**

- New task defaults to `is_completed = False`
- Setting `is_completed = True` persists after `save()` / `refresh_from_db()`
- Empty title raises `ValidationError` via `full_clean()`
- `__str__` returns title as-is (≤ 50 chars) or truncates with `…` (> 50)
- `created_at` and `updated_at` are auto-populated on creation
- Deleting a category cascades to its tasks

**API (`@pytest.mark.api`)**

- `POST /api/tasks/` creates a task and returns 201
- Empty title on POST or PATCH returns 400 with a `title` error
- `GET /api/tasks/` returns all tasks
- `DELETE /api/tasks/<id>/` returns 204 and removes the task
- `GET /api/tasks/<id>/` returns 200 with correct data
- `GET /api/tasks/99999/` returns 404
- `PATCH /api/tasks/<id>/` marks a task as completed
- `PUT /api/tasks/<id>/` updates the title
- `?category_id=X` filters tasks by category
- Response includes `category_name` as a read-only field
- Leading/trailing whitespace in `title` is stripped on create

---

## CI

GitHub Actions runs the test suite automatically on every push and pull request.

Workflow: [`.github/workflows/ci.yml`](.github/workflows/ci.yml)

```
push / pull_request → install dependencies → pytest
```

---

## Deployment

### Settings

The project uses a split settings structure. The default is `development`. In production, override via environment variable.

| File                             | Used when                   |
| -------------------------------- | --------------------------- |
| `todo.core.settings.development` | Local development (default) |
| `todo.core.settings.production`  | Production                  |

### Required environment variables (production)

| Variable                    | Description                                         |
| --------------------------- | --------------------------------------------------- |
| `DJANGO_SETTINGS_MODULE`    | `todo.core.settings.production`                     |
| `SECRET_KEY`                | Django secret key — generate a new one              |
| `DATABASE_URL`              | PostgreSQL URL: `postgres://user:pass@host:5432/db` |
| `ALLOWED_HOSTS`             | Comma-separated list of allowed domains             |
| `CORS_ALLOWED_ORIGINS`      | Comma-separated list of allowed frontend origins    |
| `DJANGO_SUPERUSER_USERNAME` | Admin username (created on first deploy)            |
| `DJANGO_SUPERUSER_EMAIL`    | Admin email (optional)                              |
| `DJANGO_SUPERUSER_PASSWORD` | Admin password (created on first deploy)            |
| `SENTRY_DSN`                | Sentry DSN for error tracking (optional)            |

Copy `.env.example` to `.env` and fill in the values. Never commit `.env` to version control.

### Start command (Gunicorn)

```bash
gunicorn todo.core.wsgi:application
or
gunicorn todo.core.wsgi:application --bind 0.0.0.0:$PORT
```

> Render specification :  
> `$PORT` is injected by Render at runtime.  
> Without `--bind 0.0.0.0:$PORT`, gunicorn defaults is `127.0.0.1:8000` and the platform cannot reach it.

### Build Command (Render)

```bash
./build.sh
```

`build.sh` runs in order:

1. `pip install -r requirements.txt`
2. `python manage.py migrate`
3. `python manage.py collectstatic --no-input`
4. `python manage.py create_superuser` — creates admin from env vars, skipped if already exists
5. `python manage.py seed_categories` — creates default categories, skipped if already exist

All steps are idempotent — safe to run on every deploy.
