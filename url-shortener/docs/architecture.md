# Architecture

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

The application tier is stateless. PostgreSQL owns durable URL mappings. Redis handles the shared ID counter and fast read caching.

## Write path

```text
POST /api/v1/urls
   |
   +-- validate
   |
   +-- custom alias?
   |      |
   |      +-- PostgreSQL INSERT + UNIQUE(short_code)
   |
   +-- generated
          |
          +-- Redis INCR
          +-- Base62
          +-- PostgreSQL INSERT
```

## Read path

```text
GET /{short_code}
   |
   +-- Redis
   |     |
   |     +-- hit -> 302
   |
   +-- PostgreSQL
          |
          +-- missing -> 404
          +-- expired -> 410
          +-- valid -> cache + 302
```
