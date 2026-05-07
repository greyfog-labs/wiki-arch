# Graph Query Examples

Once your wiki is scanned into the graph, you can ask structural questions.

## Setup

```python
from wiki_graph import WikiGraph

g = WikiGraph("/path/to/your/wiki")
```

## Hubs — Most Connected Pages

```python
>>> g.hubs(5)

[
  {"id": "concepts/external-cortex.md", "name": "External Cortex", "total_links": 24},
  {"id": "index.md",                    "name": "INDEX.md",        "total_links": 21},
  {"id": "concepts/llm-wiki-pattern.md","name": "LLM Wiki Pattern","total_links": 18},
  {"id": "self/lucy-and-ariel.md",      "name": "Lucy and Ariel",  "total_links": 15},
  {"id": "meta/decisions.md",           "name": "Decisions",       "total_links": 13},
]
```

## Blast Radius

```python
>>> g.blast_radius("concepts/my-experiment.md")

{
  "page": "concepts/my-experiment.md",
  "incoming": ["index.md", "research/patterns.md"],
  "outgoing": ["concepts/core-idea.md", "entities/tool-x.md", "lore/setting-y.md"]
}
```

If you remove `my-experiment.md`, those 2 pages lose a link, and you lose notes about 3 concepts.

## Orphans

```python
>>> g.orphans()[:5]

["brainstorms/old-note.md", "projects/abandoned.md", "scratch/unlinked.md"]
```

Pages nobody links to. Either new, abandoned, or disconnected.

## Stats

```python
>>> g.stats()

{
  "nodes": 134,
  "edges": 349,
  "orphans": 23,
  "density": 1.96
}
```

## CLI

```bash
# All of the above from the command line:
python3 wiki_graph.py --hubs
python3 wiki_graph.py --blast concepts/foo.md
python3 wiki_graph.py --orphans
python3 wiki_graph.py --stats

# Full refresh:
python3 wiki_graph.py --full
```
