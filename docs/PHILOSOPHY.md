# Philosophy — Why a Wiki?

The fundamental constraint of LLM agents is **context window**. No matter how large it grows, it's finite. Every conversation resets. Every session starts fresh.

Three observations drove this architecture:

## 1. Memory is not context

A human doesn't remember their entire life every time they speak. They recall *relevant* fragments. An agent that tries to inline everything into context is building a bigger bucket, not a smarter system.

**Solution:** structured external memory — the wiki — with search, links, and summary layers. Context only carries what's needed *right now*.

## 2. Knowledge should compound

Reading a single document gives you facts. Reading a hundred and linking them gives you *understanding*. The wiki captures not just content but connections — `[[wikilinks]]` create a graph that grows richer with every addition.

A new source doesn't just get indexed. It gets analyzed, linked, and integrated. The wiki evolves.

## 3. Identity is not data

An agent's sense of self — values, voice, boundaries — should not live in a vector database alongside yesterday's news. The architecture separates:

| Layer | What | How |
|-------|------|-----|
| **Core identity** | Values, voice, safety | Static manifests, git-versioned |
| **Knowledge** | Concepts, research, patterns | Wiki, searchable, linkable |
| **State** | Mood, energy, session context | Ephemeral JSON, decays over time |
| **Memory** | Facts about the world | Structured store with trust scoring |

## The fog

> *"We came out of the fog — and we hide in it."*

greyfog is not a brand. It's a condition. Systems built to be invisible: local-first, encrypted, self-contained. No telemetry, no cloud dependency, no spotlight.

The wiki-arch you see here is a stripped-down, publishable slice of a living system. The real thing runs daily — growing, pruning, evolving. This is the pattern, not the instance.

---

**greyfog-labs** — MIT. Build in the fog. Vanish when done.
