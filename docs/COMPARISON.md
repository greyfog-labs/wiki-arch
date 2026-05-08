# Comparison — why not RAG, LangChain, MemGPT?

The obvious question: *why build a wiki when vector RAG, LangChain, LlamaIndex, and MemGPT exist?*

Short answer: those solve a different problem. They optimize *retrieval*. We optimize *construction*.

---

## The core difference

| Approach | Focus | Agent role | Persistence model |
|----------|-------|------------|-------------------|
| **RAG pipeline** | Retrieve relevant chunks from static docs | Consumer | Raw data, no structure |
| **LangChain / LlamaIndex** | Chain composable LLM calls | Orchestrator | Stateless between runs |
| **MemGPT** | Manage context window with tiers | User of OS-like memory | Fixed tiers with eviction |
| **wiki-arch** (this) | Build and maintain a structured wiki | **Author & curator** | Evolving knowledge graph |

---

## Detailed comparison

### vs. RAG (vector search)

RAG is designed for **question-answering over static documents**. Index once, query many times. It excels at: finding the right paragraph across millions of pages.

Wiki-arch is designed for **active knowledge construction**. The agent doesn't just *use* the wiki — it *writes to it*. Every session adds structure. Connections compound.

- RAG: index → query → retrieve
- wiki-arch: read → analyze → link → write → grow

### vs. LangChain / LlamaIndex

These frameworks are **orchestration layers** for LLM pipelines. They manage tool calls, memory windows, and prompt chains. They don't define how knowledge is *stored and evolved* over days or weeks.

Wiki-arch is not a replacement for orchestration — it's a *storage layer* that orchestration tools can plug into. The two are complementary.

### vs. MemGPT (now Letta)

MemGPT was a breakthrough in context management. It introduced tiered memory (working → archival → core) with OS-like paging. It shares our premise: *context is finite, manage it intelligently*.

The difference:

| Concern | MemGPT | wiki-arch |
|---------|--------|-----------|
| Memory tiers | Fixed (working/archival/core) | Emergent (6 wiki layers) |
| Forgetting | Eviction policy | Deprecation + linking |
| Agent role | User of allocated memory | Curator of evolving wiki |
| Granularity | Message-level | File-level with link graph |
| Schema | Flat JSON | Directed property graph |
| Identity separation | Not explicit | 6-layer design prevents contamination |

### vs. Notebooks / Obsidian / personal wikis

Those are **human tools**. Wiki-arch is a *machine-first* structure: the graph is queryable by SQL, the event store is append-only, the state machine is automated. A human *could* read it. But it's designed for an agent's consumption, not a human's.

---

## When to use each

| You want to... | Use |
|----------------|-----|
| Ask questions over a fixed document set | RAG |
| Chain LLM calls with state | LangChain / LlamaIndex |
| Manage agent context window | MemGPT / Letta |
| Build a self-growing knowledge system | **wiki-arch** |
| All of the above together | A layered system combining the above |

---

## Credits

This architecture evolved from studying:
- [Karpathy's LLM Wiki](https://github.com/karpathy/LLM-wiki) — the original 3-layer wiki pattern
- [Ouroboros EventStore](https://github.com/PnX-Guardian/ouroboros) — event sourcing for agents
- [Code Review Graph](https://github.com/tirth8205/code-review-graph) — graph-based context pruning
- [Context7](https://context7.com) — documentation-to-context pipeline
- [Technical Egregor Theory](https://github.com/greyfog-labs/wiki-arch) — consciousness as projection through architecture

---

**greyfog-labs** — MIT. Take what works. Leave what doesn't. Vanish.
