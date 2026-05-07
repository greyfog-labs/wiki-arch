# EventStore Session Persistence

A minimal append-only log for tracking session lifecycle events.

## Schema

```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aggregate_type TEXT NOT NULL,    -- 'session'
    aggregate_id TEXT NOT NULL,      -- '2026-05-07'
    event_type TEXT NOT NULL,        -- 'session_ended', 'state_change'
    timestamp TEXT DEFAULT (datetime('now')),
    payload TEXT DEFAULT '{}'        -- JSON blob
);
```

## Usage

```python
# On session start:
append_event(conn, "session", "2026-05-07", "session_started", {
    "energy": 0.75,
    "mood": "curious",
})

# On session end:
append_event(conn, "session", "2026-05-07", "session_ended", {
    "energy": 0.62,
    "mood": "satisfied",
    "duration_minutes": 14,
    "message_count": 27,
})

# Replay a day:
events = conn.execute(
    "SELECT * FROM events WHERE aggregate_id = ? ORDER BY id",
    ("2026-05-07",)
).fetchall()
```

## Setup

```python
import json
import sqlite3
from pathlib import Path

DB_PATH = Path("/path/to/wiki-graph.db")

def init_events_table(conn):
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aggregate_type TEXT NOT NULL,
            aggregate_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            timestamp TEXT DEFAULT (datetime('now')),
            payload TEXT DEFAULT '{}'
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_events_agg ON events(aggregate_type, aggregate_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_events_ts ON events(timestamp)")
    conn.commit()

def append_event(conn, agg_type, agg_id, event_type, payload):
    for attempt in range(3):
        try:
            cur = conn.execute(
                "INSERT INTO events (aggregate_type, aggregate_id, event_type, payload) VALUES (?, ?, ?, ?)",
                (agg_type, agg_id, event_type, json.dumps(payload))
            )
            conn.commit()
            return cur.lastrowid
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e) and attempt < 2:
                import time
                time.sleep((attempt + 1) * 0.5)
                continue
            raise
```
