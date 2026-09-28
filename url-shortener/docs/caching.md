# Caching

Redis implements cache-aside:

1. Read the URL from Redis.
2. Hit -> redirect.
3. Miss -> read PostgreSQL.
4. Populate Redis.
5. Redirect.

Additional mechanisms:

- TTL for normal cached links
- short TTL negative entries for nonexistent codes
- per-key rebuild lock to reduce cache stampedes
