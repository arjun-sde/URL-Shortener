# FastURL Shortener

Production-style URL shortener built with FastAPI, async SQLAlchemy, PostgreSQL, and Python 3.13.

This project is designed to demonstrate backend engineering fundamentals: clean layering, scalable ID generation, multi-tenant routing, safe concurrent click updates, Dockerized local development, and automated tests.

## Features

- Shorten long URLs into compact base62 codes.
- Public redirect endpoint: `GET /s/{short_code}`.
- Stats endpoint with click count and creation timestamp.
- Snowflake-style 64-bit ID generator for horizontally scaled replicas.
- Per-domain uniqueness for multi-tenant deployments.
- Atomic click increments in the database.
- Docker Compose setup for API + PostgreSQL.
- Pytest coverage for ID generation and service behavior.

## Why Snowflake-Style IDs?

The app generates IDs in the application layer instead of waiting for a database sequence. Each generated ID contains:

- timestamp bits for time ordering,
- a `SNOWFLAKE_MACHINE_ID` for the running replica,
- a per-millisecond sequence for bursts inside one process.

This keeps URL creation fast and HPA-friendly. In Kubernetes, assign every pod a stable unique `SNOWFLAKE_MACHINE_ID` value in the `0-1023` range. If two replicas use the same machine ID at the same millisecond, the database unique constraints still protect correctness, but proper machine ID assignment avoids collisions in normal operation.

## API

### Health

```http
GET /health
```

### Shorten URL

```http
POST /api/v1/urls/shorten
Content-Type: application/json

{
  "original_url": "https://example.com/some/long/path"
}
```

Response:

```json
{
  "short_url": "http://localhost:8000/s/03bY2nQ",
  "short_code": "03bY2nQ"
}
```

### Redirect

```http
GET /s/{short_code}
```

### Stats

```http
GET /api/v1/urls/stats/{short_code}
```

## Local Development

Use Python 3.13.

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn main:app --reload
```

API docs are available at `http://localhost:8000/docs`.

## Docker

```bash
cp .env.example .env
docker compose up --build
```

Apply the schema to the local Postgres database if you are not using migrations yet:

```bash
docker compose exec -T db psql -U postgres -d url_shortener < db_schema.sql
```

## Tests

```bash
pytest
```

## Configuration

| Variable | Purpose | Default |
| --- | --- | --- |
| `DATABASE_URL` | SQLAlchemy async database URL | `postgresql+asyncpg://postgres:postgres@localhost:5432/url_shortener` |
| `BASE_URL` | Public base URL used in returned short links | `http://localhost:8000` |
| `DEFAULT_DOMAIN` | Logical tenant when multi-tenant mode is off | `default` |
| `ENABLE_MULTI_TENANT` | Use incoming host or payload domain as tenant | `false` |
| `SHORT_CODE_MIN_LENGTH` | Minimum base62 code length | `7` |
| `SNOWFLAKE_MACHINE_ID` | Replica ID for distributed ID generation | `1` |
| `SNOWFLAKE_EPOCH_MS` | Custom epoch for generated IDs | `1704067200000` |

## Production Notes

- Put the API behind a reverse proxy or ingress and set `BASE_URL` to the public domain.
- Use a unique `SNOWFLAKE_MACHINE_ID` per replica/pod.
- Keep PostgreSQL unique constraint `UNIQUE(domain, short_code)` enabled.
- Run with multiple Uvicorn/Gunicorn workers only when each process has a safe machine ID strategy.
- Use migrations such as Alembic before production instead of applying raw SQL manually.
- Add rate limiting, abuse detection, and URL safety scanning before exposing a public shortening service.
