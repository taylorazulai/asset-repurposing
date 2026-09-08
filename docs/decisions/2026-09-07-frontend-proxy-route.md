# Decision: Frontend Proxy Route for Backend Calls

**Date:** 2026-09-07
**Status:** Accepted

## Context

The Next.js frontend needs to call the FastAPI backend's `POST /pipeline` endpoint. The initial implementation used a public environment variable (`NEXT_PUBLIC_BACKEND_URL`) so the browser could send requests directly to the backend. This worked for local development but created two problems for portable deployment:

1. **Browser-side backend URL exposure** — In a containerized environment, the browser cannot reach the backend service by its internal Docker hostname (`backend`). The URL must be resolvable from the user's machine, forcing either host-network mode or a public backend address.
2. **Production hardening** — Keeping the backend URL in the browser bundle leaks internal network topology and makes it harder to place the backend behind a private VPC or internal service mesh.

## Decision

Introduce a Next.js Route Handler at `frontend/app/api/pipeline/route.ts` that proxies `POST /api/pipeline` → backend `POST /pipeline`. The frontend's `lib/api.ts` now posts to the relative path `/api/pipeline`, and the backend URL is resolved server-side from the server-only environment variable `BACKEND_URL`.

Defaults:
- Docker Compose: `http://backend:8000` (internal Docker networking).
- Local dev without Docker: `http://localhost:8000`.

`NEXT_PUBLIC_BACKEND_URL` is removed from:
- `frontend/.env.example`
- `docker-compose.yml`
- `frontend/next.config.js`

## Consequences

**Positive:**
- The backend can live on an internal Docker network, unreachable from the browser.
- The frontend bundle no longer depends on a public backend URL, making Cloud Run / Kubernetes / reverse-proxy deployments simpler.
- The proxy is tiny and can be extended later (e.g., auth headers, rate limiting, logging).

**Negative:**
- One extra server hop per pipeline request (negligible for a portfolio demo).
- Adds one small file to maintain.

## Alternatives Considered

- **Keep `NEXT_PUBLIC_BACKEND_URL`**: Rejected because it blocks internal-only backend networking in containerized deployments.
- **Use Next.js rewrite rules**: A rewrite would also work, but a Route Handler gives explicit control over headers, error pass-through, and future middleware.

## Implementation

- `frontend/app/api/pipeline/route.ts` — proxy implementation.
- `frontend/lib/api.ts` — calls `/api/pipeline` instead of `${NEXT_PUBLIC_BACKEND_URL}/pipeline`.
- `frontend/.env.example` — now documents `BACKEND_URL` as a server-only variable.
- `docker-compose.yml` — sets `BACKEND_URL=http://backend:8000` for the frontend service.
- `README.md` — updated to describe the proxy pattern and local-dev configuration.
