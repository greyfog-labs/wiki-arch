# Quick Start

> Get wiki-arch running from scratch in 5 minutes.

---

## Prerequisites

- Python 3.10+
- A directory of markdown files (your wiki)

## Install

```bash
# Clone
git clone https://github.com/greyfog-labs/wiki-arch.git
cd wiki-arch

# Install dependencies
pip install networkx
```

## Scan your wiki

```bash
# Build the graph from your markdown files
python3 examples/wiki_graph.py /path/to/your/wiki --scan

# Quick stats
python3 examples/wiki_graph.py /path/to/your/wiki --stats

# Find hubs (most linked pages)
python3 examples/wiki_graph.py /path/to/your/wiki --hubs

# Find orphans (unlinked pages)
python3 examples/wiki_graph.py /path/to/your/wiki --orphans
```

## As a library

```python
from wiki_graph import WikiGraph

g = WikiGraph("/path/to/your/wiki")
g.stats()
g.hubs(10)
g.blast_radius("my-page.md")
g.close()
```

## Next steps

- Read [ARCHITECTURE.md](ARCHITECTURE.md) for the full system design
- Read [PHILOSOPHY.md](PHILOSOPHY.md) for why it exists
- Check [ROADMAP.md](../ROADMAP.md) for planned features

---

**greyfog-labs** — MIT. Take it, use it, vanish.
