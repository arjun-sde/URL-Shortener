# Fast URL Shortener

Production-ready FastAPI + PostgreSQL URL shortener.

## Quickstart (Docker)
1. Copy `.env.example` → `.env` and set values.
2. `docker-compose up --build`
3. API docs: `http://localhost:8000/docs`

## Endpoints
- `POST /api/v1/urls/shorten` — shorten a URL.
- `GET /s/{code}` — redirect to original URL.
- `GET /api/v1/urls/stats/{code}` — stats for short code.

## Notes
- Uses async SQLAlchemy + asyncpg.
- Hashids for deterministic short codes derived from DB id.
- Multi-tenant by domain (toggle with `ENABLE_MULTI_TENANT`).

