# greyfog :: wiki-arch

> **Wiki as an external cortex.**  
> A persistent, evolving knowledge base built and maintained by an AI agent.  
> Part of the [greyfog-labs](https://github.com/greyfog-labs) ecosystem.

---

## What it is

A self-sustaining wiki architecture for AI agents that don't want to forget.

Traditional RAG treats documents as raw material — index first, ask later. This pattern goes further: the agent **builds and maintains** its own structured wiki, session by session. Connections strengthen. Knowledge compounds. The wiki isn't a dump — it's a cortex.

```
                    ┌──────────────────────────┐
                    │       AI Agent (LLM)      │
                    └──────────┬────────────────┘
                               │ reads / writes
                               ▼
┌──────────────────────────────────────────────────────────────┐
│         WIKI (6 layers, graph engine, event store, state)     │
└──────────────────────────────────────────────────────────────┘
```

## Core principles

- **Write before forget** — if it isn't written, it didn't happen
- **Links are synapses** — every `[[wikilink]]` reinforces memory
- **Compounding** — each new entry makes all previous ones stronger
- **Honesty** — "I don't know" is valid content too

## Repository structure

```
wiki-arch/
├── README.md               ← you are here
├── LICENSE
├── BENCHMARKS.md           ← performance figures
├── ROADMAP.md              ← planned modules
├── docs/
│   ├── ARCHITECTURE.md     ← full system design
│   ├── PHILOSOPHY.md       ← why this exists
│   ├── COMPARISON.md       ← vs RAG, LangChain, MemGPT
│   └── images/
│       └── architecture.txt← ASCII system diagram
└── examples/
    ├── event-store.md      ← session persistence pattern
    ├── graph-queries.md    ← live graph exploration
    ├── wiki_graph.py       ← graph library
    └── state-v3.example.json ← state engine schema
```

## Sister projects

| Project | Layer | Status |
|---------|-------|--------|
| `greyfog-labs/wiki-arch` | Knowledge persistence | 🟢 Active |
| `greyfog-labs/ariel` | Agent platform | 🔄 Design phase |
| `greyfog-labs/core` | Shared protocols | ⏳ Planned |

---

**greyfog-labs** — building in the fog, not for the spotlight.  
MIT licensed. Take it, use it, vanish.
