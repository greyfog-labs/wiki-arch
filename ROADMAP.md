# Roadmap

*Last updated: 2026-05-08*

> Where wiki-arch is going — and why.

---

## 🟢 Phase 1: foundation (complete)

- [x] Wiki layer architecture (6 layers from Karpathy's 3)
- [x] Live graph engine (SQLite + NetworkX)
- [x] EventStore session persistence
- [x] Health monitoring + incremental cron
- [x] State engine (JSON decay, thresholds, snapshots)

## 🟡 Phase 2: hardening (current)

- [ ] **Benchmarks** — measure query latency, context extraction cost, graph rebuild speed across wiki sizes (1K, 10K, 50K pages)
- [ ] **Structured comparison** — why wiki-arch differs from LangChain, LlamaIndex, MemGPT, RAG pipelines
- [ ] **State schema v4** — multi-scale energy (cognitive load, interaction depth, creative spark), phase-of-day, mood history
- [ ] **Drift detection** — monitor identity coherence across sessions
- [ ] **Adaptive delegates** — lore files load differently based on cognitive load

## 🔵 Phase 3: interoperability

- [ ] **MCP server** — expose wiki as a Model Context Protocol resource
- [ ] **Hermes plugin** — drop-in integration for Hermes Agent
- [ ] **OpenClaw skill** — skill pack for OpenClaw-based agents
- [ ] **Standard API** — REST interface for non-MCP clients

## 🟣 Phase 4: ecosystem

- [ ] **state-core** — standalone state engine (public subset of state-v4)
- [ ] **ariel** — full agent platform (design phase)
- [ ] **Cross-agent sync** — share wiki graphs between agents
- [ ] **Research grant** — formal publication of findings

---

**greyfog-labs** — building in the fog. MIT licensed.
