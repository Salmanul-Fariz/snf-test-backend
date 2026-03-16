# Infra Test API

FastAPI backend for **local infrastructure testing**. Use it to verify server environment, API, database connectivity, and Docker before deploying production applications.

## Features

- **Health checks**: `GET /health`, `GET /db-health`
- **Diagnostics**: `GET /system-info` (app version, DB status, timestamp, hostname)
- **PostgreSQL** with SQLAlchemy and Alembic migrations
- **Docker Compose**: API + Postgres on a shared network; migrations run on API startup
- **Configuration**: `.env` and `.env.example`; dependencies in `pyproject.toml`

## Project structure

```
app/
  main.py           # FastAPI app
  api/              # Routes
  core/             # Config, logging
  database/         # SQLAlchemy session, base
  models/           # ORM models
  schemas/          # Pydantic schemas
  services/         # Business logic
alembic/            # Migrations
tests/
```

## Quick start

### With Docker Compose (recommended)

```bash
# From project root (backend/)
cp .env.example .env   # optional: edit for overrides
docker compose up --build
```

- API: http://localhost:8000  
- Docs: http://localhost:8000/docs  
- Migrations run automatically when the API container starts.

### Local development (API on host, Postgres in Docker)

```bash
cp .env.example .env
# .env already has POSTGRES_HOST=localhost
docker compose up postgres -d
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Ensure PostgreSQL is listening on `localhost:5432` (Docker publishes the port). If `/db-health` fails, check the returned message (e.g. "connection refused" = Postgres not running; "database does not exist" = run `alembic upgrade head` or create the DB).

### Local development (no Docker at all)

1. Install and start PostgreSQL; create database: `createdb infra_test_db` (or match `POSTGRES_*` in `.env`).
2. Copy `.env.example` to `.env`, set `POSTGRES_HOST=localhost` and credentials.
3. Run migrations and the API as in the previous section.

## API endpoints

| Method | Path         | Description                    |
|--------|--------------|--------------------------------|
| GET    | /health      | Liveness; returns `status: OK` |
| GET    | /db-health   | Database connectivity check    |
| GET    | /system-info | App version, DB status, timestamp, hostname |

## Configuration

See `.env.example`. Key variables:

- `APP_NAME`, `APP_VERSION`, `DEBUG`, `LOG_LEVEL`
- `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`

Database URL is built from these; no need to set `DATABASE_URL` unless you override.

## Tests

```bash
pip install -e ".[dev]"
pytest
```

## Dependencies

Managed in **`pyproject.toml`** (no `requirements.txt`). Install with:

```bash
pip install -e .          # runtime
pip install -e ".[dev]"   # with dev/test deps
```
