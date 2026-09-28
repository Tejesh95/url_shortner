# Failure Scenarios

## Redis cache failure
Redirect reads fall back to PostgreSQL.

## Redis counter failure
New generated IDs cannot be allocated until Redis recovers or fails over. Existing redirect traffic is unaffected.

## PostgreSQL failure
Warm cached redirects can continue temporarily. Durable misses and writes depend on PostgreSQL recovery.

## Viral link
Immutable `short_code -> original_url` mappings are excellent cache candidates.

## Expiry
Redirect logic checks expiry before redirecting. Cleanup removes old rows and cache keys later.

## Alias race
PostgreSQL UNIQUE(short_code) is the correctness boundary.
