# Security

## Scope

wiki-arch is a **local-first** architecture. It runs on your own hardware with your own data. There is no cloud component, no telemetry, and no network service by default.

If you expose the wiki API or MCP server over a network, you are responsible for securing that endpoint.

## Reporting

If you find a vulnerability in the architecture or implementation:

- Open a GitHub issue with `[security]` in the title
- Do not post credentials or personal data in public issues
- Expect a response within 2 weeks (or not — see [CONTRIBUTING.md](CONTRIBUTING.md))

## Best practices

- Keep your wiki directory permissions-restricted (`chmod 600` for sensitive files)
- Do not commit credentials, `.env` files, or private keys to the repo
- If using EventStore persistence, ensure the SQLite database is not world-readable

---

**greyfog-labs** — MIT. Build in the fog. Vanish when done.
