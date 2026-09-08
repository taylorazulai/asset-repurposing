# AGENTS.md: Asset Decomposition & Repurposing Pipeline

## 1. Project Purpose
The goal of this project is to build an automated Directed Acyclic Graph (DAG) pipeline that takes a single canonical source document (e.g., a technical whitepaper, product manual, or audio transcript) and decomposes it into structured derivative assets. 

This serves as a high-impact portfolio piece demonstrating the ability to unlock multi-channel marketing and content velocity without multiplying creative overhead. The system proves expertise in strict schema enforcement, state management, long-context handling, and maintaining consistent brand voice across multiple parallel downstream outputs.

## 2. Technical Architecture & Tech Stack

This architecture is optimized for rapid prototyping, seamless agentic development workflows (Cursor, KiloCode CLI, Kiro CLI, Opencode), and easy containerized deployment.

*   **Backend / API Layer:** Python with FastAPI. Chosen for native Pydantic support, making structured LLM outputs and schema enforcement trivial.
*   **Frontend / UI:** Next.js (TypeScript/React) for a clean, interactive client-facing dashboard to upload assets and view generated outputs.
*   **Orchestration / DAG:** Native Python `asyncio` or a lightweight framework like LangGraph for managing the directed acyclic flow of data. For visual workflow integration, n8n can be optionally layered to trigger the pipeline via webhooks.
*   **LLM Provider:** OpenAI / Anthropic via API, utilizing native tool-calling / JSON mode functionality.
*   **Deployment & Infrastructure:** Dockerized backend and frontend, designed to be spun up via `docker-compose` locally and deployed serverless on Google Cloud Run. Database state can be managed via PostgreSQL or Firestore for tracking job statuses.

## 3. Pipeline Flow (The DAG)

The system operates strictly unidirectionally to ensure predictable execution:

1.  **Ingestion Node:** Receives the raw input text/markdown via the FastAPI endpoint.
2.  **Extraction Node:** Analyzes the master document and extracts the "Core Context Entity" (key themes, tone, primary arguments, target audience) into a strict JSON object.
3.  **Parallel Generation Nodes:** The core context is passed simultaneously to multiple downstream worker functions:
    *   *Node A (Executive Brief):* Generates a 1-page structured summary.
    *   *Node B (Social Snippets):* Generates platform-specific copy (LinkedIn, Twitter/X) matching character limits.
    *   *Node C (Slide Outline):* Generates a JSON array representing presentation slides (Title, Bullets, Speaker Notes).
4.  **Aggregation Node:** Collects all parallel outputs, validates them against their respective Pydantic models, and returns the final payload to the client.

## 4. Proposed Directory Structure

```text
/portfolio-4b-pipeline
│
├── /backend                 # FastAPI Service (Python)
│   ├── /api
│   │   └── routes.py        # Pipeline trigger endpoints
│   ├── /core
│   │   ├── config.py        # Environment variables & setup
│   │   └── schemas.py       # Pydantic models for strict output validation
│   ├── /pipeline
│   │   ├── dag.py           # Orchestration logic (asyncio/LangGraph)
│   │   ├── extractors.py    # Core context extraction prompts
│   │   └── generators.py    # Parallel asset generation logic
│   ├── Dockerfile           # Backend containerization
│   └── requirements.txt
│
├── /frontend                # Next.js UI (TypeScript)
│   ├── /app
│   │   ├── page.tsx         # Main dashboard UI
│   │   └── /components      # Upload forms, output display cards
│   ├── /lib
│   │   └── api.ts           # Fetch wrappers for FastAPI backend
│   ├── Dockerfile           # Frontend containerization
│   └── package.json
│
├── docker-compose.yml       # Local dev orchestration
└── README.md
```

## 5. Agentic Coding Instructions (For Cursor/KiloCode)

When generating code for this repository, the coding agent must adhere to the following rules:
1.  **Strict Typing:** Use Pydantic `BaseModel` for all LLM outputs in the backend. In the frontend, map these exactly to TypeScript interfaces.
2.  **No Hallucinated Tooling:** Stick to the specified stack. Do not introduce heavy vector databases (Weaviate, ChromaDB) or web scrapers (Firecrawl, Tavily) into this specific project, as this is a deterministic transformation DAG, not an autonomous research agent or RAG system.
3.  **Concurrency:** Ensure the generation nodes in the pipeline run asynchronously in parallel to minimize total pipeline execution time.
4.  **Collaboration Context:** When generating review comments or documentation for handoffs, format them cleanly for review by workflow mentors or collaborators (e.g., Nick Puruczky).
