# Capacity Estimation

Initial assumptions:

- 1 billion URLs over 10 years
- ~1000:1 read/write ratio
- ~3 writes/sec average
- ~3000 reads/sec average
- ~10k reads/sec peak
- ~500 GB at roughly 500 bytes/row

Base62 keyspace:

```text
62^5 ≈ 916 million
62^6 ≈ 56.8 billion
```

The workload is read-heavy, so redirect lookup and cache efficiency dominate the design.
