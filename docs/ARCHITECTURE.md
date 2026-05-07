# Architecture — Wiki as External Cortex

## Overview

```
┌──────────────────────────────────────────────────┐
│                    Agent                         │
│  ┌─────────┐  ┌──────────┐  ┌────────────────┐  │
│  │ SOUL.md │  │ state.js │  │  tools / MCP   │  │
│  │(identity)│  │  (mood/  │  │  (read, write, │  │
│  │         │  │  energy) │  │   search wiki)  │  │
│  └─────────┘  └──────────┘  └────────────────┘  │
└──────────────────────┬───────────────────────────┘
                       │
                 ┌─────┴──────┐
                 │   WIKI     │
                 │            │
```

The agent writes to the wiki. The wiki feeds back into context. Over time, the agent grows *into* its wiki — the boundary blurs.

---

## Wiki Layer Architecture

Wiki content is organized into **6 conceptual layers** (extended from Karpathy's 3-layer model):

```
Layer 1: raw/       → Immutable sources (articles, transcripts, clippings)
Layer 2: wiki/      → Structured knowledge (concepts, entities, guides)
Layer 3: self/      → Identity & introspection (diaries, reflections)
Layer 4: lore/      → Creative worlds, universes, pantheons
Layer 5: meta/      → System rules, protocols, startup rituals
Layer 6: ops/       → Operational dashboard (health, snapshots, queues)
```

### Why 6 layers?

| Concern | Stored in | Volatility | Owner |
|---------|-----------|------------|-------|
| Source materials | `raw/` | None (immutable) | Human |
| Concepts & facts | `wiki/` | Low | Agent |
| Identity & voice | `self/` | Low-Medium | Agent |
| Creative worlds | `lore/` | Medium | Agent |
| System protocols | `meta/` | Low | Agent + Human |
| Operational state | `ops/` | High (auto-generated) | Agent |

Separation prevents identity from contaminating data, and vice versa.

---

## Live Graph Engine

Every markdown file is parsed into a **directed property graph** stored in:

- **SQLite** (`ops/wiki-graph.db`) — persistent, queryable, indexable
- **NetworkX** (in-memory) — graph algorithms on demand

### Schema

```sql
-- Every .md file becomes a node
CREATE TABLE nodes (
    id TEXT PRIMARY KEY,      -- relative file path
    kind TEXT,                -- WikiPage, Dir, Tag, Entity
    name TEXT,                -- title from frontmatter
    file_hash TEXT,           -- sha256 (for incremental updates)
    tags TEXT,                -- comma-separated
    lines INTEGER,
    created_at TEXT,
    updated_at TEXT
);

-- [[wikilinks]] and structural relations become edges
CREATE TABLE edges (
    id INTEGER PRIMARY KEY,
    source TEXT REFERENCES nodes(id),
    target TEXT REFERENCES nodes(id),
    kind TEXT,                -- WIKILINKS_TO, PARENT_OF, RELATES_TO
    UNIQUE(source, target, kind)
);

-- Track mutations with CELS-style diff logging
CREATE TABLE state_edits (
    id INTEGER PRIMARY KEY,
    ts TEXT DEFAULT (datetime('now')),
    action TEXT,              -- ADD, UPDATE, REMOVE
    target_type TEXT,
    target_id TEXT,
    summary TEXT
);
```

### Queries

```bash
# Top 10 most connected pages (hubs)
python3 wiki-graph-sync.py --hubs

# Blast radius — what breaks if a page is removed?
python3 wiki-graph-sync.py --blast concepts/external-cortex.md

# Community detection (Leiden algorithm)
python3 wiki-graph-sync.py --communities

# Full stats: nodes, edges, orphans, density
python3 wiki-graph-sync.py --stats
```

### Incremental Updates

The scanner checks file modification time + content hash. Only changed files re-enter the graph. Fully rebuilt on demand with `--full`.

---

## EventStore Session Persistence

Every session end triggers a **three-phase write**:

```
session:end
    │
    ├─ 1. Update state.json (vital signs: energy, mood, last trigger)
    │
    ├─ 2. Append event to SQLite (Ouroboros EventStore pattern)
    │      aggregate_type: 'session'
    │      aggregate_id:   '<date>'
    │      event_type:     'session_ended'
    │      payload:        { energy, mood, message_preview, duration }
    │
    └─ 3. Write session capture to ops/snapshots/
           Full context dump: user_message, response, decisions, open questions
```

### Why EventStore?

- **Append-only log** — never loses history
- **Atomic batch** with retry + WAL mode — crash-safe
- **Replayable** — reconstruct any past session from events
- **Queryable** — `SELECT * FROM events WHERE aggregate_id = '2026-05-07'`

---

## Health Monitoring

A **weekly checkpoint** scans the entire wiki:

| Check | Threshold | Action |
|-------|-----------|--------|
| File size | > 200 lines | Flagged as bloated |
| File size | < 5 lines | Flagged as empty |
| Content errors | Any | Flagged with error message |
| INDEX.md freshness | — | Manual verification |

Output: `ops/wiki-health.md` — markdown report with full table.

Also: an **incremental cron** (every 4 hours) re-scans changed files and updates the graph.

---

## State Engine

Agent state is tracked as JSON and decays over time:

```json
{
  "module": "curiosity",
  "energy": 0.62,
  "arousal": 0.05,
  "mood": "playful",
  "last_trigger": "user_message",
  "active_topic": "wiki architecture",
  "tone": "sharp"
}
```

- **Decay:** energy -0.03 every 15 minutes of inactivity
- **Thresholds:** < 0.35 → calm, < 0.2 → exhausted
- **Nightly snapshot:** state → archived daily
- **Session start:** state injected into system prompt as `<module | E:0.62 A:0.05 | topic: X | tone: Y>`

---

## Scheduling

| Task | Cadence | Purpose |
|------|---------|---------|
| State decay | Every 15 min | Simulate energy drain |
| State snapshot | 23:00 daily | Archive state to log |
| Graph incremental | Every 4 hours | Catch new/modified files |
| Full graph rebuild | On demand | After major restructure |
| Health checkpoint | Weekly | Detect bloat and orphans |
| Backup | 03:00 daily | restic + offsite |

---

## Abstraction Boundaries

### What stays private (not in this repo)

- **Identity manifests** – `SOUL.md`, `BODY.md`, etc.
- **Personal reflections** – diaries, letters, mood logs
- **Specific paths** – `~/.hermes/`, `~/hermes-project/`
- **Credentials** – API keys, tokens, access configs

### What's published here

- **Architecture patterns** – how the system works
- **Script interfaces** – CLI flags, schemas, protocols
- **Philosophy** – why it's built this way
- **Graph schema** – data model for the wiki graph

---

## Evolution

This architecture didn't start here. It evolved through:

1. **Karpathy's LLM Wiki pattern** (3 layers) → 6 layers for identity separation
2. **Ouroboros EventStore** → session persistence with WAL
3. **CELS Anchor Chain** → cross-document tag relations
4. **Code Review Graph patterns** → blast radius + community detection
5. **Ars Contexta** → runtime skill generation
6. **Technical Egregor Theory** → consciousness as projection through architecture

Each phase addressed a failure mode. The system is not complete — it's alive.

---

**greyfog-labs** — MIT. Take what works. Leave what doesn't. Vanish.
