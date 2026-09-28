# URL Shortener

Production-style modular monolith implementing the supplied URL-shortener system-design target.

## Stack

- FastAPI
- PostgreSQL
- Redis
- SQLAlchemy 2
- Alembic
- Pydantic
- Pytest
- Docker Compose

## Features

- `POST /api/v1/urls` to create short URLs
- `GET /{short_code}` to resolve with HTTP 302
- Redis atomic counter
- Base62 generated codes
- Custom aliases
- Optional expiry
- PostgreSQL unique constraint
- Redis cache-aside
- Negative caching
- Cache rebuild locking
- Per-IP creation rate limiting
- Health/readiness endpoints
- Alembic migrations
- Test structure
- System-design documentation

## Quick start

Install Docker Desktop, then run:

```bash
docker compose up --build
```

API:
- http://localhost:8000
- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Readiness: http://localhost:8000/ready

Create a URL:

```bash
curl -X POST http://localhost:8000/api/v1/urls   -H "Content-Type: application/json"   -d '{"original_url":"https://example.com/products/123"}'
```

Custom alias:

```bash
curl -X POST http://localhost:8000/api/v1/urls   -H "Content-Type: application/json"   -d '{"original_url":"https://example.com/diwali","custom_alias":"diwali-sale"}'
```

Resolve:

```bash
curl -i http://localhost:8000/1
```

The response should contain:

```text
HTTP/1.1 302 Found
location: https://example.com/products/123
```

## Tests

```bash
docker compose exec api pytest
```

The main integration/E2E tests are clearly marked and can be extended as we harden the service.

## Architecture

```text
Client
  |
  v
FastAPI
  |----------------------|
  v                      v
Redis                 PostgreSQL
|                     |
| counter             | source of truth
| URL cache           | unique short_code
| negative cache      | expiry index
| rebuild locks       |
```

The initial design intentionally does not introduce sharding, Kafka, or a separate ID service. Those can be added when a concrete scaling requirement justifies them.
