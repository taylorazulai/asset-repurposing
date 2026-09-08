# Asset Repurposing Pipeline — Build Plan

## Stage 1: Project Scaffolding & Shared Configuration
- [ ] Create `/docs` directory and save this plan file
- [ ] Create root directory structure: `/backend`, `/frontend`, `/docs`
- [ ] Write root `README.md` with overview, stack, and quick-start
- [ ] Write root `docker-compose.yml` linking `backend` and `frontend` services
- [ ] Add root `.gitignore` for Python, Node, and OS artifacts

## Stage 2: Backend — Core Framework
- [ ] Create `backend/requirements.txt` with FastAPI, Uvicorn, Pydantic, openai, python-multipart, httpx, pytest
- [ ] Create `backend/Dockerfile`
- [ ] Create `backend/main.py` with FastAPI app factory and health check
- [ ] Create `backend/core/config.py` with env vars:
  - `EDENAI_API_KEY` (required)
  - `EDENAI_BASE_URL` default `https://api.edenai.run/v3`
  - `EDENAI_MODEL` default `google/gemini-3.8-flash`
- [ ] Create `backend/core/schemas.py` with Pydantic models:
  - `IngestPayload`
  - `CoreContext`
  - `ExecutiveBrief`
  - `SocialSnippet`
  - `Slide`
  - `SlideDeck`
  - `PipelineOutput`
- [ ] Create `backend/pipeline/llm_client.py` initializing `AsyncOpenAI` with EdenAI base URL

## Stage 3: Backend — Pipeline DAG
- [ ] Create `backend/pipeline/extractors.py` with core-context extraction prompt/function
- [ ] Create `backend/pipeline/generators.py` with three parallel generators:
  - Executive brief generator
  - Social snippets generator
  - Slide deck generator
- [ ] Create `backend/pipeline/dag.py` with async orchestration using `asyncio.gather`
- [ ] Create `backend/api/routes.py` with `POST /pipeline` endpoint
- [ ] Wire routes into `backend/main.py`

## Stage 4: Backend — Tests
- [ ] Create `backend/tests/test_pipeline.py`
- [ ] Add schema validation tests for all Pydantic models
- [ ] Add a basic endpoint smoke test (can be mocked)

## Stage 5: Frontend — Next.js Scaffold
- [ ] Create `frontend/package.json` with Next.js, React, TypeScript, Tailwind CSS
- [ ] Create `frontend/tsconfig.json`
- [ ] Create `frontend/next.config.js`
- [ ] Create `frontend/Dockerfile`
- [ ] Create `frontend/app/layout.tsx`
- [ ] Create `frontend/app/page.tsx`

## Stage 6: Frontend — UI Components
- [ ] Create `frontend/lib/api.ts` with typed fetch wrapper to `POST /pipeline`
- [ ] Create `frontend/app/components/UploadForm.tsx`
- [ ] Create `frontend/app/components/OutputCards.tsx`
- [ ] Wire components into `frontend/app/page.tsx`

## Stage 7: Integration & Verification
- [ ] Verify backend starts with `uvicorn main:app`
- [ ] Verify frontend starts with `next dev`
- [ ] Verify Docker Compose builds both services
- [ ] Add final notes or known next steps to `README.md`
