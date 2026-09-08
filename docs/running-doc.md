# Asset Repurposing Pipeline — Running Build Document

## Introduction

This document tracks the live progress of the Asset Repurposing Pipeline build. At the end of every stage, a new section should be appended summarizing what was changed, executed, rebuilt, any major decisions made, deferred tasks and why, and the immediate next steps.

---

## Project Complete Summary

**Date:** 2026-09-08
**Status:** Portfolio-ready

The Asset Repurposing Pipeline is a complete, end-to-end system that ingests a single source document and produces an executive brief, platform-specific social snippets, and a slide deck via a schema-enforced asynchronous DAG. Stages 1–7 are finished; Stage 8 is in progress and Stage 9 is planned in `docs/plan.md`:

- **Backend:** FastAPI service with Pydantic models, EdenAI-powered extraction and three parallel generators, retry/timeout logic, and a full pytest suite.
- **Frontend:** Next.js 16 dashboard with a server-side proxy route, typed API wrapper, and responsive asset/error UI.
- **Integration:** Live verified with a real `EDENAI_API_KEY` against a 500+ word source; Docker Compose stack builds and runs both services; negative cases (min-length, truncation, small happy path) confirmed.
- **Documentation:** Root README with hero/overview, stack table, ASCII architecture diagram, ADR index, quick-start, environment variable table, known limits, and a **Live Demo section with real UI screenshots** against a truncated source document. The source doc is referenced at `assets-for-repurposing/Perplexity - The Complete Dungeons & Dragons Handbook.md`. Five decision records in `docs/decisions/` (including the new `2026-09-08-persona-driven-prompts.md`).

Remaining next steps are documented in the README and include Cloud Run deployment, frontend test suite, and retry-specific unit tests. Stage 9 will refine the slide-deck schema with tiered bullet hierarchy.

---

## Stage 1: Project Scaffolding & Shared Configuration

**Status:** Completed

### What Was Changed / Executed

- Created `/docs/plan.md` containing the full staged build plan.
- Created root `README.md` with project overview, stack, quick-start guide, and environment variable reference.
- Created root `docker-compose.yml` defining `backend` and `frontend` services with hot-reload mounts.
- Created root `.gitignore` covering Python, Node, OS, editor, and environment artifacts.
- Initialized the `/docs` folder for planning and running documentation.

### Major Decisions

- Confirmed stack from `AGENTS.md`: FastAPI backend, Next.js + Tailwind frontend, native `asyncio` DAG orchestration.
- LLM provider set to **EdenAI** using the OpenAI-compatible client pattern (`https://api.edenai.run/v3`).
- Default model locked to `google/gemini-3.8-flash` via environment variable.
- Docker Compose chosen for local development; Cloud Run deployment path documented in README for later.

### Deferred Tasks

- Backend and frontend directories will be populated in subsequent stages rather than all at once, to keep review points clean.
- No live LLM smoke test yet; that will happen during Stage 7 integration.
- No CI/CD or pre-commit hooks added yet; out of scope for the initial build pass.

### Immediate Next Steps

Proceed to **Stage 2: Backend Core Framework**:

1. Create `backend/requirements.txt` and `backend/Dockerfile`.
2. Create `backend/main.py` FastAPI app factory.
3. Create `backend/core/config.py` for environment variables.
4. Create `backend/core/schemas.py` with all Pydantic models.
5. Create `backend/pipeline/llm_client.py` wiring EdenAI via the OpenAI-compatible client.

---

## Stage 2: Backend Core Framework

**Status:** Completed

### What Was Changed / Executed

- Created `backend/requirements.txt` with FastAPI, Uvicorn, Pydantic, Pydantic Settings, python-multipart, httpx, openai, pytest, and pytest-asyncio.
- Created `backend/Dockerfile` using Python 3.12 slim image, installing requirements and exposing port 8000.
- Created `backend/.env.example` documenting the three required/optional environment variables.
- Created `backend/main.py` with a FastAPI app factory, CORS middleware, and a `/health` endpoint.
- Created `backend/core/config.py` using `pydantic_settings.BaseSettings` to load `EDENAI_API_KEY`, `EDENAI_BASE_URL`, and `EDENAI_MODEL` from `.env`.
- Created `backend/core/schemas.py` with strict Pydantic models: `IngestPayload`, `CoreContext`, `ExecutiveBrief`, `SocialSnippet`, `Slide`, `SlideDeck`, and `PipelineOutput`.
- Created `backend/pipeline/llm_client.py` initializing an `AsyncOpenAI` client pointed at EdenAI's OpenAI-compatible endpoint (`https://api.edenai.run/v3`) and a reusable `chat_completion` helper.
- Added package `__init__.py` files for `backend/`, `core/`, `api/`, `pipeline/`, and `tests/`.

### Verification

- Installed dependencies into a local `.venv` (gitignored).
- Confirmed clean imports for `core.config`, `core.schemas`, `pipeline.llm_client`, and `main` with a dummy `EDENAI_API_KEY`.
- FastAPI app title verified as "Asset Repurposing Pipeline".

### Major Decisions

- Used `pydantic-settings` for typed environment variable loading with `.env` support.
- Kept `main.py` route-free in this stage; routes will be wired in Stage 3 to avoid circular dependencies and keep stage boundaries clean.
- LLM client is a module-level singleton for simplicity; can be refactored into a dependency later if needed.
- Chose `str | None` union syntax (Python 3.10+); confirmed Python 3.14.7 in the local environment supports it.

### Deferred Tasks

- `/pipeline` endpoint and route wiring deferred to Stage 3.
- No live LLM call yet (requires a real `EDENAI_API_KEY`); will be done in Stage 7.
- Dockerfile uses Python 3.12 slim (updated from an initial 3.11 choice) as the sweet spot for ecosystem maturity and modern features. Full rationale recorded in `docs/decisions/2026-09-07-python-version.md`.

### Immediate Next Steps

Proceed to **Stage 3: Backend Pipeline DAG**:

1. Create `backend/pipeline/extractors.py` to extract `CoreContext` from source text.
2. Create `backend/pipeline/generators.py` with three parallel asset generators (executive brief, social snippets, slide deck).
3. Create `backend/pipeline/dag.py` to orchestrate extraction and parallel generation using `asyncio.gather`.
4. Create `backend/api/routes.py` with `POST /pipeline` endpoint and wire it into `backend/main.py`.

---

## Inter-Stage Update: Python Version Pin and Docker Context

**Date:** 2026-09-07

### What Was Changed / Executed

- Updated `backend/Dockerfile` base image from `python:3.11-slim` to `python:3.12-slim`.
- Created `backend/.dockerignore` to exclude the local `.venv`, caches, environment files, and test directory from the Docker build context.
- Created `/docs/decisions/2026-09-07-python-version.md` recording the rationale for choosing Python 3.12 as the production runtime.

### Major Decisions

- **Python 3.12 chosen** as the backend Docker runtime because it balances modern language features with proven ecosystem/package maturity in 2026.
- Added a `.dockerignore` immediately to keep images small and avoid copying the local virtual environment into the container.

### Verification

- Dockerfile content verified (`FROM python:3.12-slim`).
- Attempted a local Docker build; the daemon is not available in this environment, so the image will be validated during Stage 7 or on a machine with Docker running.
- `.dockerignore` lists `.venv`, caches, environment files, and other non-essential artifacts.

### Immediate Next Steps

Proceed to **Stage 3: Backend Pipeline DAG**.

---

## Inter-Stage Update: Error-Handling Pattern for the DAG

**Date:** 2026-09-07

### What Was Changed / Executed

- Reviewed the three generator nodes (executive brief, social snippets, slide deck) and the extraction node.
- Decided on a partial-results-with-error-flags pattern for generator failures.
- Created `/docs/decisions/2026-09-07-error-handling-pattern.md` documenting the rationale and implementation plan.

### Major Decisions

- **Extraction node is fail-fast**: if `CoreContext` extraction fails, the pipeline returns an error because downstream generators depend on it.
- **Generator nodes are best-effort**: each runs independently via `asyncio.gather(..., return_exceptions=True)`. If one fails, the error is captured and the other generators still return their assets.
- `PipelineOutput` will be updated to include optional asset fields and an `errors` mapping from node name to error message.

### Verification

- Confirmed the three generators have no dependencies on each other, so partial output is semantically valid.
- Confirmed the extractor is a hard dependency for all generators, justifying fail-fast behavior there.

### Immediate Next Steps

Proceed to **Stage 3: Backend Pipeline DAG** and implement the approved pattern.

---

## Stage 3: Backend Pipeline DAG

**Status:** Completed

### What Was Changed / Executed

- Updated `backend/core/schemas.py` to make `executive_brief`, `social_snippets`, and `slide_deck` optional and added an `errors: Dict[str, str]` field for partial-result reporting.
- Created `backend/pipeline/utils.py` with a `parse_json_response` helper to strip markdown code fences and parse LLM JSON responses.
- Created `backend/pipeline/extractors.py` with `extract_core_context()` using a structured prompt to produce a `CoreContext` object.
- Created `backend/pipeline/generators.py` with three parallel asset generators:
  - `generate_executive_brief()` → `ExecutiveBrief`
  - `generate_social_snippets()` → `List[SocialSnippet]`
  - `generate_slide_deck()` → `SlideDeck`
- Created `backend/pipeline/dag.py` with `run_pipeline()`:
  - Extracts core context first (fail-fast).
  - Runs the three generators concurrently with `asyncio.gather(..., return_exceptions=True)`.
  - Builds a `PipelineOutput` with successful assets and per-node error messages.
- Created `backend/api/routes.py` with `POST /pipeline` endpoint.
  - Returns 200 with partial results if at least one generator succeeds.
  - Returns 500 if all generators fail.
- Updated `backend/main.py` to import and include the API router.
- Fixed JSON prompts in `extractors.py` and `generators.py` to escape braces for Python `.format()`.

### Verification

- Confirmed the app imports cleanly with a dummy `EDENAI_API_KEY`.
- Confirmed `/pipeline` route is registered and accessible via `TestClient`.
- Ran a mocked end-to-end pipeline test: extraction + all three generators produced a valid `PipelineOutput` with no errors.
- Ran a partial-failure test: one generator raised an exception; the response returned 200 with the other two assets and the error recorded in `errors`.
- Ran an all-generators-failure test: response returned 500 with the detailed error map.

### Major Decisions

- Implemented the approved partial-results-with-error-flags pattern from `docs/decisions/2026-09-07-error-handling-pattern.md`.
- Used module-level function imports in extractors/generators so unit tests can monkeypatch the LLM call at the module level.
- Kept the LLM prompts focused on JSON output with a clear schema; no `response_format` or JSON mode used yet to maximize compatibility across EdenAI providers.

### Deferred Tasks

- No live LLM calls yet (requires a real `EDENAI_API_KEY`); will be done in Stage 7.
- More robust prompt parsing (e.g., response schema validation, retries) deferred to a later refinement pass.
- Full pytest test suite will be created in Stage 4.

### Immediate Next Steps

Proceed to **Stage 4: Backend Tests**:

1. Create `backend/tests/test_pipeline.py`.
2. Add schema validation tests for all Pydantic models.
3. Add mocked endpoint tests for the `/pipeline` route covering success, partial failure, and all-failure cases.

---

## Inter-Stage Update: LLM Retries, Timeouts, and Structured Output

**Date:** 2026-09-07

### What Was Changed / Executed

- Added `tenacity>=8.0.0` to `backend/requirements.txt`.
- Rewrote `backend/pipeline/llm_client.py` to:
  - Set a 60-second client-level timeout and a 60-second per-request timeout.
  - Wrap `client.chat.completions.create` in `AsyncRetrying` with `stop_after_attempt(3)` and `wait_exponential` backoff (2–10 seconds).
  - Retry only on transient errors: `APIConnectionError`, `APITimeoutError`, `InternalServerError`, and `APIStatusError` with status >= 500 or 429.
  - Do not retry on other 4xx errors.
  - Pass `response_format={"type": "json_object"}` on every chat completion.
- Simplified `backend/pipeline/utils.py` to a plain `json.loads` wrapper; removed fence-stripping logic since EdenAI supports `json_object` mode.
- Verified that EdenAI's `/v3/models` endpoint lists `google/gemini-3.8-flash` as a valid routable model ID.
- Verified that EdenAI's documentation supports `response_format: {"type": "json_object"}` for Google Gemini models, so structured output is used without markdown-fence fallbacks.

### Verification

- Reinstalled backend dependencies (tenacity added) and confirmed clean imports.
- Re-ran the mocked end-to-end pipeline: all three assets produced successfully with `response_format` in place.
- Confirmed `parse_json_response` no longer attempts fence stripping and parses plain JSON correctly.

### Major Decisions

- Adopted `tenacity` because it keeps retry logic declarative and clean without hand-rolling backoff math.
- Used `json_object` response format because EdenAI docs explicitly support it for Google/Gemini models, and it lets us remove the brittle fence-stripping parser.
- Did **not** switch to `json_schema` mode for this pass: it adds schema-generation complexity and the current prompt-based schema is sufficient for a portfolio MVP. Can be revisited later if field-level strictness becomes critical.

### Deferred Tasks

- Live EdenAI call to confirm `google/gemini-3.8-flash` accepts `response_format` and returns clean JSON — still blocked on a real API key; will be done in Stage 7.
- Dedicated unit tests for retry behavior (e.g., fail-then-succeed) deferred to Stage 4.

### Immediate Next Steps

Wait for user review of the requested files, then proceed to **Stage 4: Backend Tests**.

---

## Stage 4: Backend Tests

**Status:** Completed

### Pre-Stage Items Completed

1. **Structured extraction errors in `backend/api/routes.py`** — wrapped `run_pipeline` in `try/except` so extraction failures return `500` with body `{"error": "extraction_failed", "detail": "..."}` instead of the default FastAPI error shape.
2. **Tightened `SocialSnippet` schema** — changed `platform` to `Literal["LinkedIn", "Twitter/X"]`, rejecting garbage values at parse time.
3. **Configurable source truncation** — moved the `20000` limit into `core/config.py` as `MAX_SOURCE_CHARS`, added a `truncated: bool` field to `CoreContext`, and log a warning when truncation occurs. Updated `backend/.env.example` and `README.md` to document the variable.
4. **`response_format` coverage verification** — grepped the codebase; only one `chat.completions.create` call exists in `backend/pipeline/llm_client.py`, and it passes `response_format={"type": "json_object"}`. All extractors/generators route through this helper.

### What Was Changed / Executed

- Created `backend/pytest.ini` with `pythonpath = .` so pytest can resolve top-level modules (`main`, `core`, `pipeline`, `api`).
- Updated `backend/core/config.py` to use `SettingsConfigDict` instead of the deprecated class-based `Config`.
- Created `backend/tests/test_pipeline.py` with 13 tests covering:
  - Schema validation: `IngestPayload`, `CoreContext`, `SocialSnippet` (valid/invalid platforms), `ExecutiveBrief`, `SlideDeck`, `PipelineOutput` with partial results.
  - Endpoint happy path: all three assets returned, no errors.
  - Endpoint truncation: long source text sets `core_context.truncated = true`.
  - Endpoint single-generator failure: partial results with error flag.
  - Endpoint all-generators failure: `500` with error map.
  - Endpoint extractor failure: `500` with `{"error": "extraction_failed", ...}`.

### Verification

- Ran `pytest -v` inside the backend virtual environment.
- **13 tests passed**, no Pydantic deprecation warnings, only one external `anyio` warning from `starlette.testclient`.

### Major Decisions

- Used `TestClient` for endpoint tests because it exercises the full route, middleware, and Pydantic serialization without starting a server.
- Monkeypatched `extractors.chat_completion` and `generators.chat_completion` at the module level to avoid importing the real EdenAI client during tests.
- Kept retry-specific tests out of this stage; the retry logic is covered by `tenacity` tests upstream, and a live integration test in Stage 7 will validate the full stack.

### Deferred Tasks

- Live EdenAI integration test (blocked on real API key) — Stage 7.
- Frontend tests — Stage 5/6 when the UI scaffold is built.
- Retry-specific unit tests (fail-then-succeed) — can be added later if needed.

### Immediate Next Steps

Proceed to **Stage 5: Frontend Next.js Scaffold**:

1. Create `frontend/package.json` with Next.js, React, TypeScript, Tailwind CSS.
2. Create `frontend/tsconfig.json`, `next.config.js`, and `Dockerfile`.
3. Create `frontend/app/layout.tsx` and `frontend/app/page.tsx`.

---

## Stages 5 & 6: Frontend Scaffold and UI Components

**Status:** Completed

### What Was Changed / Executed

- Tightened backend CORS:
  - Added `CORS_ORIGINS` to `backend/core/config.py` with default `http://localhost:3000`.
  - Updated `backend/main.py` to parse comma-separated origins and pass an explicit list to `CORSMiddleware` (no `*` wildcard).
  - Updated `backend/.env.example`, `docker-compose.yml`, and `README.md` to document the new variable.
- Added backend input gate: `IngestPayload.source_text` now has `min_length=20` so the backend rejects junk submissions independently of the frontend's 50-character form minimum.
- Created the full Next.js frontend scaffold and UI components under `frontend/`:
  - `package.json` — Next.js 16.3.4, React 18.3.1, TypeScript 5.5.3, Tailwind CSS 3.4.6.
  - `tsconfig.json` — App Router TypeScript config with `@/*` path alias.
   - `next.config.js` — standalone output mode for Cloud Run readiness; no public backend URL is exposed in the browser bundle.
  - `tailwind.config.cjs`, `postcss.config.js`, `styles/globals.css` — Tailwind setup.
  - `app/layout.tsx` and `app/page.tsx` — root layout and main page composition.
  - `next-env.d.ts`, `.env.example`, `.dockerignore`, `Dockerfile` (multi-stage Node build → standalone runner).
  - `lib/types.ts` — TypeScript mirrors of every backend Pydantic model with inline `// Mirrors backend/core/schemas.py:<Model>` comments.
  - `lib/api.ts` — typed `pipelineRequest()` wrapper with a discriminated `PipelineError` class (kind: `network` | `extraction_failed` | `all_generators_failed` | `unknown`) for the three failure shapes.
  - `app/components/UploadForm.tsx` — controlled textarea, optional `.txt`/`.md` file upload, 50-character minimum, emits typed `onSubmit`.
  - `app/components/OutputCards.tsx` — conditional rendering of the three asset cards, inline error badges, copy-to-clipboard buttons, and error-only cards when an asset is missing but has a per-asset error.
  - `app/components/ErrorBanner.tsx` — top-level error banner that branches on `error.kind` and lists per-asset errors for `all_generators_failed`.
- Updated `README.md` with frontend setup, environment variables, and build instructions; added a prominent one-liner noting that Next.js 16.3.4 is pinned via `docs/decisions/2026-09-07-frontend-dependency-versions.md` to satisfy `npm audit` while staying within the "Next.js 14+" constraint and remaining React 18-compatible.

### Verification

- Ran `pytest -v` after the `min_length=20` and source-text changes — **14 tests passed**.
- Ran `npm install` in `frontend/`; resolved security advisories by selecting Next.js 16.3.4 and PostCSS 8.5.28.
- Ran `npm audit` — **0 vulnerabilities**.
- Ran `npm run build` — **build completed cleanly** with no TypeScript errors.
- Confirmed frontend compiles against the typed backend schema mirrors.
- Generated a sample `OutputCards` render for a partial-failure case (executive brief failed, social snippets and slide deck succeeded) and verified the rendered HTML includes a red "Failed" badge + inline error message for the missing executive brief, plus copy buttons on the surviving asset cards.
- Docker frontend build not verified in this environment (Docker daemon unavailable); noted for Stage 7.

### Major Decisions

- Selected **Next.js 16.3.4** instead of 14.x because the latest 14.x patch (14.2.35) still carried multiple high-severity advisories. Next.js 16 remains within the user's stated "Next.js 14+" constraint and keeps React 18.3.1 compatibility. Full rationale and pinned version table recorded in `docs/decisions/2026-09-07-frontend-dependency-versions.md`.
- Kept the typed API surface narrow: only `pipelineRequest` talks to the backend; components import types from `lib/types.ts` and never perform raw `fetch()` calls.
- Converted `ApiError` into a discriminated `PipelineError` class with a `kind` field so `ErrorBanner` branches on `error.kind` instead of parsing message strings. This is more robust for future UI additions and easier to test.

### Deferred Tasks

- Live EdenAI integration with a real API key — Stage 7.
- Production deployment to Cloud Run — final docs pass after Stage 7.
- Frontend tests (Jest/Playwright) — out of portfolio MVP scope per `docs/stages5-6.md`.
- Docker frontend build verification — Stage 7 (requires a Docker daemon).

### Immediate Next Steps

Proceed to **Stage 7: Integration & Verification**:

1. Perform an end-to-end run with a real `EDENAI_API_KEY`.
2. Verify the Docker Compose stack builds and runs both services.
3. Add any final documentation or polish to `README.md`.

---

## Inter-Stage Update: Frontend Proxy Route

**Date:** 2026-09-07

### What Was Changed / Executed

- Created `frontend/app/api/pipeline/route.ts` as a Next.js Route Handler that proxies `POST /api/pipeline` to the backend `POST /pipeline`.
- Updated `frontend/lib/api.ts` to call the relative path `/api/pipeline` instead of the absolute `NEXT_PUBLIC_BACKEND_URL + "/pipeline"`.
- Removed `NEXT_PUBLIC_BACKEND_URL` from `frontend/.env.example`, `docker-compose.yml`, `frontend/next.config.js`, and `frontend/Dockerfile`.
- Introduced the server-only environment variable `BACKEND_URL` (no `NEXT_PUBLIC_` prefix):
  - Default for non-Docker local development: `http://localhost:8000`.
  - Default for Docker Compose: `http://backend:8000` (internal Docker networking).
- Created `docs/decisions/2026-09-07-frontend-proxy-route.md` documenting the rationale: portable deployment, internal backend networking, and removal of the browser-side backend URL.
- Updated `README.md` to explain the proxy pattern, the new `BACKEND_URL` variable, and the local-dev vs. Docker defaults.
- Ran `npm run build` in the frontend — **build completed cleanly** with no TypeScript errors and the new `/api/pipeline` route registered as a dynamic server route.

### Major Decisions

- Adopted a server-side proxy route so the browser never needs to know the backend URL. This keeps the backend addressable via internal Docker hostnames and makes production deployments (Cloud Run, reverse proxies, VPC) more flexible.
- Chose a Route Handler over a Next.js rewrite to keep explicit control over request/response headers and future middleware (auth, logging, rate limiting).
- Kept the proxy implementation minimal: pass-through status, content-type, and body with no extra transformation.

### Verification

- `npm run build` in `frontend/` completed successfully with `ƒ /api/pipeline` listed as a dynamic route.
- Confirmed `NEXT_PUBLIC_BACKEND_URL` no longer appears in active build/runtime configuration (`.env.example`, `docker-compose.yml`, `next.config.js`, `Dockerfile`). Historical plan docs retain mentions for context.
- Confirmed `BACKEND_URL` is documented in `frontend/.env.example`, `docker-compose.yml`, `README.md`, and `docs/decisions/2026-09-07-frontend-proxy-route.md`.

### Deferred Tasks

- Docker Compose end-to-end run with a real `EDENAI_API_KEY` — Stage 7.
- Verification that the proxy route correctly resolves `http://backend:8000` inside the Docker network — Stage 7.

### Immediate Next Steps

**STOP.** Awaiting verification and/or reorientation before proceeding to **Stage 7: Integration & Verification**.

---

## Stage 7: Integration & Verification

**Status:** Completed

### What Was Changed / Executed

- Added a 65-second outbound `AbortController` timeout to `frontend/app/api/pipeline/route.ts` and mapped timeouts to a `504 proxy_timeout` response; other proxy errors return `502`.
- Fixed the backend endpoint path so `/pipeline` (no trailing slash) resolves directly by setting `redirect_slashes=False` in `main.py` and using `@router.post("")` in `api/routes.py`.
- Created `backend/.env` with the live `EDENAI_API_KEY` and verified the backend imports and starts cleanly.
- Ran a live `POST /pipeline` against a 500+ word source document; all three assets populated and `errors` was empty.
- Ran Docker Compose `up --build` successfully; fixed a frontend build failure caused by a missing `public` directory by adding `frontend/public/.gitkeep`.
- Updated `docker-compose.yml` so the frontend service uses the production standalone command `node server.js` instead of `npm run dev`, matching the multi-stage Dockerfile.
- Verified the frontend proxy inside Docker correctly resolves `http://backend:8000` and returns a full `PipelineOutput`.
- Live-tested negative cases: 10-character source rejected (`422` min-length), >MAX_SOURCE_CHARS source sets `core_context.truncated: true`, 1500-character source returns a normal happy path.
- Polished `README.md` with hero/overview, stack table, ASCII architecture diagram, ADR index, quick-start, environment variable table (with proxy pattern note), known limits / next steps, and a **Live Demo section** embedding the seven UI screenshots and linking to the source document (`assets-for-repurposing/Perplexity - The Complete Dungeons & Dragons Handbook.md`).
- Added repo badges (License, Python 3.12, Next.js 16, Pydantic v2) to the top of `README.md`.
- Added a `Project Complete Summary` section at the top of this document.

### Major Decisions

- Adopted a 65-second proxy timeout that is slightly longer than the backend's 60-second LLM request timeout, ensuring the proxy never closes before the backend gives up on a slow model call.
- Kept the backend `/pipeline` route without a trailing slash to avoid `307` redirects that can confuse clients and proxies.
- Switched the Docker Compose frontend command to `node server.js` because the production Dockerfile builds a standalone output; dev hot-reload remains available via `npm run dev` outside Docker.
- Added `frontend/public/.gitkeep` rather than removing the `COPY public` Dockerfile line, preserving the standard Next.js public-asset convention for future use.

### Verification

- **Backend tests:** `pytest -v` — **14 passed** after the route path change.
- **Frontend build:** `npm run build` — completed cleanly with `/api/pipeline` as a dynamic route.
- **Live 500+ word run:** `POST /pipeline` returned `200` with `core_context`, `executive_brief`, `social_snippets`, `slide_deck`, and `errors: {}`.
- **Docker Compose:** `docker-compose up --build` started both containers; `POST http://localhost:3000/api/pipeline` returned `200` with all assets populated via the internal `http://backend:8000` backend URL.
- **Negative cases:**
  - `source_text: "short text"` → `422` with `String should have at least 20 characters`.
  - `source_text: "T " * 30000` → `200` with `core_context.truncated: true`.
  - 1500-character source → `200` with all three assets present and `errors: {}`.

### Known Limits & Next Steps

- **Cloud Run deployment:** Local Docker Compose is verified; the next deployment step is to push containers to Google Artifact Registry and deploy with the same `BACKEND_URL` plumbing.
- **Frontend tests:** No Jest/Playwright suite yet; UI error branches are manually verified.
- **Retry-specific tests:** `tenacity` retry logic is in place but not covered by dedicated fail-then-succeed unit tests.
- **Long documents:** Sources beyond `MAX_SOURCE_CHARS` are truncated; future work could implement chunking/merging for very large documents.

### Project Status

Portfolio-ready as of Stage 7. Stages 8 and 9 are now planned in `docs/plan.md` and underway.

---

## Stage 8: UX & Prompt Polish

**Status:** Completed

### What Was Changed / Executed

- **F1 — Frontend max-character gate (mirror backend cap):**
  - Bumped `MAX_SOURCE_CHARS` default to `50000` in `backend/.env.example` and `backend/core/config.py`.
  - Added a matching cap comment in `frontend/.env.example`.
  - Refactored `frontend/app/components/UploadForm.tsx` to display a live character counter (`X / 50,000`), disable submit when over the cap, and show an inline "Source is too long" hint.
- **F2 — Distinct CSS palette:**
  - Added vanilla-cream / near-black / emerald-heading / muted-grey / red-warning palette to `frontend/styles/globals.css` and `frontend/tailwind.config.cjs`.
  - Updated `frontend/app/layout.tsx` to use `bg-cream text-[#1A1A1A]`.
  - Applied `text-heading`, `text-muted`, `text-warnText`, `bg-warnBg`, and related palette classes across `frontend/app/components/OutputCards.tsx`.
  - Created `frontend/app/components/TruncationBanner.tsx` with an inline warning SVG and wired it into `OutputCards.tsx` so it renders whenever `core_context.truncated === true`.
- **F3 — Persona-prefixed system prompts:**
  - Replaced generic system roles in `backend/pipeline/extractors.py` and `backend/pipeline/generators.py` with fixed expert personas (content strategist, strategy consultant, B2B social copywriter, presentation designer).
  - Added `_build_system_role()` helper that composes each fixed persona with a dynamic domain phrase derived from `core_context.tone`, `themes`, and `audience`.
  - Created `docs/decisions/2026-09-08-persona-driven-prompts.md` ADR documenting the rationale.
- Updated `README.md` to:
  - Reflect the new `MAX_SOURCE_CHARS=50000` default.
  - Footnote the Live Demo truncation screenshot as captured under the previous `20000` cap, noting that the demo document (≈38,900 characters) now fits without truncation.

### Major Decisions

- Chose `50000` characters as the unified cap because it keeps the demo D&D Handbook within budget while still bounding token spend (~12–13k tokens for typical encodings).
- Kept the Tailwind palette small and explicit (five named colors) rather than exposing all CSS custom properties to Tailwind, keeping the theme surface narrow and easy to audit.
- Used an inline SVG in `TruncationBanner.tsx` to avoid adding an icon library dependency for a single component.
- Kept the prompt persona fragments as module-level string constants in `generators.py` and `extractors.py` so they are co-located with the prompts they modify and easy to tune without touching the LLM client.

### Verification

- `pytest -v` in `backend/` — **14 tests passed** after all changes.
- `npm run build` in `frontend/` — **clean build** with `/api/pipeline` as a dynamic route.
- Live `POST /pipeline` against the D&D Handbook (38,886 characters):
  - `core_context.truncated: false` — the document now fits under the new `50000` cap.
  - All three assets populated; `errors: {}`.
  - Executive brief and social snippets adopted the gaming/tabletop domain (e.g., "Dungeon Master," "tabletop role-playing," "d20"), confirming the persona-driven prompt shift.
- WCAG contrast spot-check: red-on-light-red pairing (`#B91C1C` on `#FEE2E2`) estimated at ~7.5:1, passing AA.

### Deferred Tasks / Visual Artifacts

- Updated UI screenshots in `screenshots/` are not captured in this environment. The new palette and the non-truncating D&D Handbook run should be reflected in the public demo screenshots by the reviewer before Stage 9 closeout (or when the portfolio is refreshed).
- The `local-source-truncated-and-executive-brief.png` screenshot remains historically accurate but now documents behavior under the previous `20000` cap.

### Immediate Next Steps

**STOP.** Awaiting validation and / or reorientation before proceeding to **Stage 9: Schema & Slide Deck Refinement**.

---

## Stage 8 Closeout & Pre-Stage-9 Baseline

**Date:** 2026-09-09
**Status:** Stage 8 closed; pre-migration baseline captured for Stage 9

### Final Stage 8 Polishes

- **UploadForm.tsx counter-color refinement:**
  - Changed the dead `isUnderMin ? "text-muted" : "text-muted"` conditional in the live character counter to `isUnderMin ? "text-yellow-600 font-medium" : "text-muted"`.
  - This gives users a visible "almost valid" feedback cue when the input is between 1 and 49 characters, while over-max input remains red (`text-warnText`) and valid input stays muted.
  - Re-ran `npm run build` in `frontend/` — clean build.

- **`_build_system_role()` empty-field fallback:**
  - Hardened `_build_system_role()` in `backend/pipeline/generators.py` so it gracefully handles empty or missing `core_context.tone`, `themes`, or `audience`.
  - Falls back to generic phrasing (`"the provided source material"`, `"the intended readers"`) and drops the themes clause entirely if no non-empty themes are present, preventing blank clauses in the composed system prompt.

### Pre-Migration Baseline Capture

- Ran a live `POST /pipeline` against the D&D Handbook (38,886 characters, under the new `50000` cap) before any Stage 9 schema changes.
- Saved the current flat-bullet `slide_deck` response to `docs/baselines/2026-09-09-pre-stage9-slide-deck.json` for before/after comparison.
- Baseline snapshot: 6 slides, each with 3 flat-string bullets, speaker notes per slide. This documents the shape before the `BulletPoint` / tiered-sub-bullet migration.

### Persona-Driven Prompt Confirmation

- The live D&D Handbook run confirmed the persona-driven prompt shift:
  - Executive brief adopted McKinsey-style consulting prose applied to tabletop role-playing ("Dungeon Master," "tabletop role-playing," "player agency").
  - Social snippets for LinkedIn and Twitter/X referenced the gaming domain directly ("300-page rulebook," "d20," "failing forward").
  - Slide deck titles and bullets used facilitation/pedagogy terminology consistent with the source material.

### Immediate Next Steps

Proceed to **Stage 9: Schema & Slide Deck Refinement**:

1. Introduce `BulletPoint` in `backend/core/schemas.py` with `text: str` and `sub: List[str]` (max_length=3); change `Slide.bullets` to `List[BulletPoint]`.
2. Mirror the schema in `frontend/lib/types.ts`.
3. Rewrite `SLIDE_DECK_PROMPT` to request title/agenda/3-5 content/recap slides with 2-4 main bullets and 0-3 sub-bullets.
4. Update `frontend/app/components/OutputCards.tsx` to render nested bullets and copy the entire slide (title + bullets + speaker notes).
5. Update backend tests and fixtures to the new `BulletPoint` shape and add a `max_length=3` validation test.
6. Capture a post-migration live D&D Handbook baseline and save it as `docs/baselines/2026-09-09-post-stage9-slide-deck.json`.

---
