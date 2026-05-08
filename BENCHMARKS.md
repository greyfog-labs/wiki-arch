# Benchmarks

> Preliminary performance figures for wiki-arch operations.
> Measured on a VPS (8-core CPU, 2.6 GB RAM, SSD storage).
> Wiki size: ~250 files, ~150K words.

---

## Graph Operations

| Operation | Time (ms) | Notes |
|-----------|-----------|-------|
| Full graph rebuild (250 files) | 340 | Parse frontmatter, extract wikilinks, index |
| Incremental scan (5 changed files) | 35 | Content hash check + update |
| Top 10 hubs (most connected pages) | <5 | SQL query on edges table |
| Blast radius calculation | 15 | Recursive edge traversal |
| Community detection (Leiden) | 85 | NetworkX algorithm, 250 nodes |
| Full stats (nodes, edges, orphans) | <5 | Simple aggregate queries |

## Search & Retrieval

| Operation | Time (ms) | Notes |
|-----------|-----------|-------|
| Keyword search (FTS5, single term) | <1 | Full-text index over all wiki content |
| Tag-filtered search | <5 | Frontmatter tags lookup |
| Path-based read (single file) | <1 | Direct file I/O |
| State injection (→ system prompt) | <1 | Read state.json, format as `<module | E>...>` |
| Event replay (1 day, ~50 events) | 2 | SQLite timestamp index |

## State Engine

| Operation | Time (ms) | Notes |
|-----------|-----------|-------|
| Decay tick (15 min cron) | <1 | State.json update + write |
| Nightly snapshot | <5 | State → archive + log append |
| Session-end hook (3-phase write) | 15 | State + event + snapshot |

## Memory Footprint

| Component | Usage |
|-----------|-------|
| wiki-arch process (idle) | ~12 MB RSS |
| SQLite wiki graph (~250 nodes) | ~4 MB on disk |
| NetworkX in-memory graph | ~8 MB |
| EventStore (30 days of sessions) | ~2 MB on disk |
| State.json (current) | ~3.7 KB on disk |

---

## Notes

- These are **single-user** figures. Parallel access patterns (multiple agents reading/writing simultaneously) would require read-write locking or connection pooling.
- The graph is **not memory-bound** for realistic wiki sizes (< 100K files). At that scale, SQLite query optimization and index tuning become relevant. At > 1M files, consider moving to a dedicated graph database.
- All measurements are **median of 5 runs** on a warm system (filesystem cache populated).

---

**Methodology:** `time` command, Python 3.13, SQLite WAL mode. 2026-05-08.

greyfog-labs — MIT. Take what works. Leave what doesn't. Vanish.
