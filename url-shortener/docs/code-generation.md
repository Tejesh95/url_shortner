# Code Generation

## Rejected approaches

### Prefix/suffix
Not unique.

### Truncated hashes
Collisions are possible, so collision checking and retries are required.

### Counter + Base62
The production baseline:

```text
Redis INCR
    ↓
integer ID
    ↓
Base62
    ↓
short_code
```

The counter is atomic. Base62 produces compact URL-safe strings.

Sequential codes are enumerable. A future hardened mode can apply a keyed permutation/format-preserving encryption before Base62 encoding.
