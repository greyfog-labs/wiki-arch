"""wiki_graph.py — surf your wiki as a graph.

Usage:
    from wiki_graph import WikiGraph
    g = WikiGraph("/path/to/wiki")

    # Top connected pages
    g.hubs(limit=10)

    # What breaks if a page is removed?
    g.blast_radius("concepts/my-idea.md")

    # Find isolated pages
    g.orphans()

    # Community clusters
    g.communities()
"""

import re
import sqlite3
from pathlib import Path
from collections import defaultdict

LINK_RE = re.compile(r'\[\[([^\]|]+)(?:\|[^]]+)?\]\]')
TAG_RE = re.compile(r'^tags:\s*\[(.+)\]', re.MULTILINE)
H1_RE = re.compile(r'^#\s+(.+)$', re.MULTILINE)
FM_RE = re.compile(r'^---\s*\n(.+?)\n---', re.DOTALL)


class WikiGraph:
    """A queryable graph over a directory of markdown files."""

    def __init__(self, wiki_path: str, db_path: str = None):
        self.wiki_dir = Path(wiki_path)
        self.db_path = Path(db_path or self.wiki_dir / "ops/wiki-graph.db")
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row

    def hubs(self, limit: int = 10) -> list[dict]:
        """Most connected pages (incoming + outgoing links)."""
        rows = self.conn.execute("""
            SELECT n.id, n.name, n.tags,
                   COALESCE(ci.cnt, 0) + COALESCE(co.cnt, 0) AS total_links
            FROM nodes n
            LEFT JOIN (SELECT target AS id, COUNT(*) AS cnt FROM edges GROUP BY target) ci USING (id)
            LEFT JOIN (SELECT source AS id, COUNT(*) AS cnt FROM edges WHERE kind = 'WIKILINKS_TO' GROUP BY source) co USING (id)
            ORDER BY total_links DESC
            LIMIT ?
        """, (limit,)).fetchall()
        return [dict(r) for r in rows]

    def blast_radius(self, page_path: str) -> dict:
        """What pages link to this one, and what does it link to?"""
        incoming = self.conn.execute("""
            SELECT source FROM edges WHERE target = ? AND kind = 'WIKILINKS_TO'
        """, (page_path,)).fetchall()
        outgoing = self.conn.execute("""
            SELECT target FROM edges WHERE source = ? AND kind = 'WIKILINKS_TO'
        """, (page_path,)).fetchall()
        return {
            "page": page_path,
            "incoming": [r["source"] for r in incoming],
            "outgoing": [r["target"] for r in outgoing],
        }

    def orphans(self) -> list[str]:
        """Pages with no incoming links."""
        rows = self.conn.execute("""
            SELECT id FROM nodes WHERE kind = 'WikiPage'
            EXCEPT
            SELECT target FROM edges WHERE kind = 'WIKILINKS_TO'
        """).fetchall()
        return [r["id"] for r in rows]

    def stats(self) -> dict:
        """Full graph statistics."""
        nodes = self.conn.execute("SELECT COUNT(*) AS c FROM nodes").fetchone()["c"]
        edges = self.conn.execute("SELECT COUNT(*) AS c FROM edges").fetchone()["c"]
        orphans_count = len(self.orphans())
        return {
            "nodes": nodes,
            "edges": edges,
            "orphans": orphans_count,
            "density": round(edges / max(nodes * (nodes - 1), 1) * 100, 2) if nodes > 1 else 0,
        }

    def close(self):
        self.conn.close()
