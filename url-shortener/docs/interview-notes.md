# Interview Notes

## Why PostgreSQL?
Simple key lookup, durable storage, transactional writes, and a unique constraint that directly enforces alias correctness.

## Why Redis?
Atomic shared counter plus low-latency cache.

## Why Base62?
Compact representation of integer IDs using 62 URL-safe symbols.

## Why 302?
Every click reaches the service, preserving control over expiry and future management.

## Why no sharding initially?
The initial storage and request estimates fit a single PostgreSQL instance.

## Why UNIQUE for aliases?
Check-then-insert has a race condition; the database constraint is atomic.

## Main bottleneck?
Reads. The initial workload is approximately 1000 reads per write.
