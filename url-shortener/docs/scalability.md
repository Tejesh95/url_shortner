# Scalability

Do not introduce distributed machinery without a capacity reason.

When the workload grows:

1. Put multiple stateless API instances behind a load balancer.
2. Keep a shared Redis layer.
3. Batch Redis counter allocations if write volume increases.
4. Add Redis replicas/cluster.
5. Add PostgreSQL replicas.
6. Shard PostgreSQL by short_code only when one node no longer fits.
7. Add regional caches/edge resolution for global low latency.
