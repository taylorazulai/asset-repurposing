# Asset Repurposing Pipeline

An automated DAG pipeline that decomposes a single canonical source document into structured derivative assets (executive briefs, social snippets, and slide decks) while maintaining consistent brand voice and strict schema enforcement.

## Stack

- **Backend:** Python 3.12+, FastAPI, Pydantic
- **Frontend:** Next.js 16 (App Router, satisfies the 14+ requirement), TypeScript, Tailwind CSS
- **Orchestration:** Native Python `asyncio`
- **LLM Provider:** EdenAI OpenAI-compatible API (`https://api.edenai.run/v3`)
- **Default Model:** `google/gemini-3.8-flash`
- **Deployment:** Docker + Docker Compose (local), Cloud Run-ready

> **Frontend pinned to Next.js 16.3.4 (App Router) via `docs/decisions/2026-09-07-frontend-dependency-versions.md` to satisfy `npm audit` while staying within the "Next.js 14+" constraint and remaining React 18-compatible.**

## Project Structure

```text
asset-repurposing/
├── backend/          # FastAPI service
├── frontend/         # Next.js dashboard
├── docs/             # Planning docs
├── docker-compose.yml
└── README.md
```

## Quick Start

### 1. Clone and configure

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
# Edit backend/.env and add your EDENAI_API_KEY
# Edit frontend/.env.local if your backend is not on http://localhost:8000
```

### 2. Run with Docker Compose

```bash
docker-compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API docs: http://localhost:8000/docs

### 3. Run backend locally (dev)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 4. Run frontend locally (dev)

```bash
cd frontend
npm install
npm run dev
```

## Usage

Upload or paste source text into the frontend dashboard, or call the backend directly:

```bash
curl -X POST http://localhost:8000/pipeline \
  -H "Content-Type: application/json" \
  -d '{"source_text": "Your long source document here..."}'
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `EDENAI_API_KEY` | — | Your EdenAI API key |
| `EDENAI_BASE_URL` | `https://api.edenai.run/v3` | EdenAI OpenAI-compatible base URL |
| `EDENAI_MODEL` | `google/gemini-3.8-flash` | Default chat model |
| `MAX_SOURCE_CHARS` | `20000` | Maximum source characters sent to the extraction prompt |
| `CORS_ORIGINS` | `http://localhost:3000` | Comma-separated list of origins allowed by the backend CORS middleware |

### Frontend Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_BACKEND_URL` | `http://localhost:8000` | Base URL for the FastAPI backend |

## Frontend Build

```bash
cd frontend
npm install
npm run build
npm start
```

## License

MIT
