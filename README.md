# flask-docker-compose

A small Flask app for tracking stores (name, address, city), backed by PostgreSQL and run with Docker Compose.

## Stack

- Python 3.12, Flask 3.0.3
- PostgreSQL 16 (`psycopg2-binary`)
- Docker Compose

## Quick start

```sh
docker compose up --build
```

Then open <http://localhost:5000>.

Use the form on the page to add a store; stores are listed newest first.

To stop the app:

```sh
docker compose down        # keep data
docker compose down -v     # also delete the pgdata volume
```

## How it works

- `db` runs Postgres with a healthcheck (`pg_isready`); `web` waits until it is healthy.
- On startup, `app.py` creates the `stores` table if it doesn't exist, retrying up to 10 times (2s apart) if the database isn't reachable yet.
- Data persists in the `pgdata` named volume.

### Schema

| Column       | Type          | Notes                  |
|--------------|---------------|------------------------|
| `id`         | `SERIAL`      | Primary key            |
| `name`       | `TEXT`        | Required               |
| `address`    | `TEXT`        |                        |
| `city`       | `TEXT`        |                        |
| `created_at` | `TIMESTAMPTZ` | Defaults to `NOW()`    |

### Routes

| Method | Path | Description                          |
|--------|------|--------------------------------------|
| GET    | `/`  | List all stores and show the add form |
| POST   | `/`  | Add a store (`name` required), then redirect to `/` |

## Configuration

| Variable       | Description                  | Default in `docker-compose.yml`                          |
|----------------|------------------------------|----------------------------------------------------------|
| `DATABASE_URL` | Postgres connection string (required) | `postgresql://postgres:postgres@db:5432/storesdb` |

The Postgres credentials in `docker-compose.yml` are for local development only. Change them before deploying anywhere real.

## Project layout

```
.
├── app.py               # Flask app and DB access
├── templates/
│   └── index.html       # Store list and form
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Notes

The app runs with `python app.py` (Flask's development server). Use a production WSGI server such as gunicorn if you deploy it.
