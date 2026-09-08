# Decision: Python Runtime Version for Backend Docker Image

**Date:** 2026-09-07
**Decision:** Pin backend Docker image to `python:3.12-slim`.
**Status:** Accepted

## Context

The initial Dockerfile used `python:3.11-slim` as a conservative default. The local development environment happens to be Python 3.14.7, but that is too new for stable ecosystem compatibility. We needed a production Python version that balances modern features with broad package support.

## Options Considered

1. **Python 3.11** — Proven stable, very wide package support. Slightly older; misses 3.12+ improvements like f-string debugging (`f"{x=}"` was already in 3.8, but 3.12 brings better error messages, `typing` cleanups, and minor performance gains).
2. **Python 3.12** — Good ecosystem maturity by late 2026; most major ML/web packages support it. Modern syntax improvements (e.g., PEP 695 type parameter syntax, improved f-strings) and better error reporting. Good middle ground.
3. **Python 3.13** — Latest stable at the time of this decision. Riskier for some packages; less battle-tested in production Docker images.
4. **Python 3.14** — Matches local environment, but too new and not recommended for production stability.

## Decision

Adopt **Python 3.12** as the pinned Docker runtime. It offers the best balance of modern Python features and proven ecosystem stability for a portfolio project being containerized in 2026.

## Consequences

- Requirements and code should be compatible with Python 3.12+.
- Avoid using features that require Python 3.13+ unless explicitly gated.
- The local virtual environment can remain on the system Python (3.14.7) for development, but CI/CD and Docker builds must use 3.12 to catch compatibility issues.

## References

- `backend/Dockerfile` (line 1)
