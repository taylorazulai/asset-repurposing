# Stage 5 & 6 Instructions
## Core Constraints (Apply to Both Stages)
1. Schema mirroring is non-negotiable
  - Create frontend/lib/types.ts that contains a TypeScript interface for every backend Pydantic model. The interfaces must mirror field names, types, and optionality exactly.
  - Add an inline comment on each interface, e.g.:
    ```ts
    // Mirrors backend/core/schemas.py:CoreContext
    export interface CoreContext {
     title: string;
      themes: string[];
      tone: string;
      audience: string;
      primary_arguments: string[];
     truncated: boolean;
    }``` 
  - Do not invent field names that don't exist on the backend. If the UI wants a derived field, derive it (e.g., a displayTitle from title), but don't rename.
  - For Pydantic Literal["LinkedIn", "Twitter/X"], use a TS union: type SocialPlatform = "LinkedIn" | "Twitter/X".
2. CORS must be explicit
  - Confirm the backend's CORS config in backend/main.py allows exactly http://localhost:3000 (or whatever the frontend's dev port is).
  - Reject allow_origins=["*" unless you also allow_credentials=False — but that's brittle. Use an explicit list.
3. Components should be composable, not monolithic
  - UploadForm.tsx — handles input only: text area, file upload (optional), submit button. Emits typed events upward.
  - OutputCards.tsx — receives PipelineOutput props, renders each asset as a separate card only if it's non-null. Also renders a per-asset error badge if output.errors[assetKey] is set.
  - The page (page.tsx) glues them together: holds state, calls lib/api.ts, passes data down.
4. Error UI must handle the three failure shapes
  - Network failure (backend unreachable): show a top-level error banner with the HTTP status.
  - Extractor failure (error === "extraction_failed"): show a clear "Source analysis failed — try a different document" message.
  - All-generators failure (message === "All asset generators failed"): show a generic "Generation failed across all channels" with the error map beneath.
  - Partial failure: render the successful assets normally, and show a per-asset error badge inline (yellow/red banner above the missing card).
5. Typed fetch wrapper
  - frontend/lib/api.ts should POST /pipeline with { source_text: string }, get back a PipelineOutput, and return it typed.
  - All API calls go through this wrapper. No raw fetch() calls in components.
  - Use NEXT_PUBLIC_BACKEND_URL env var (default http://localhost:8000) so it works under docker-compose.

## Stage 5: Next.js Scaffold — Deliverables
1. frontend/package.json with pinned, modern versions: Next.js 14+ (App Router), React 18, TypeScript ≥5, Tailwind CSS 3+, plus @types/node, @types/react.
2. frontend/tsconfig.json configured for Next.js (use the published next defaults via npx create-next-app as reference, but reproduce the config inline — don't ship the agent's "create-next-app added these magically" output).
3. frontend/next.config.js with NEXT_PUBLIC_BACKEND_URL exposed and standalone output mode for Cloud Run deployment readiness.
4. frontend/Dockerfile (multi-stage Node build → standalone runner) and frontend/.dockerignore.
5. frontend/app/layout.tsx with proper metadata (title: "Asset Repurposing Pipeline").
6. frontend/app/page.tsx as the entry route — initially a placeholder that the Stage 6 components will populate.
7. frontend/tailwind.config.cjs and frontend/postcss.config.js for Tailwind.
8. frontend/styles/globals.css with Tailwind directives.
9. frontend/lib/types.ts containing TS mirrors of every backend Pydantic model.

## Stage 6: UI Components — Deliverables
1. frontend/lib/api.ts — typed pipelineRequest(sourceText: string): Promise<PipelineOutput> wrapper. Handles errors in a single place.
2. frontend/app/components/UploadForm.tsx — controlled text area with submit button, file upload (optional, .txt and .md only). Min 50 chars to submit.
3. frontend/app/components/OutputCards.tsx — renders 3 conditional cards (executive brief, social snippets, slide deck). Each card:
  - Renders only when its asset is non-null in PipelineOutput.
  - Shows an inline error badge when output.errors[assetKey] exists.
  - Has a "Copy" button for text fields (using navigator.clipboard).
4. frontend/app/components/ErrorBanner.tsx — for top-level errors (network, extractor, all-fail).
5. frontend/app/page.tsx — composes the above:
  - State: loading, response: PipelineOutput | null, error: ApiError | null.
  - Calls api.pipelineRequest() on form submit.
  - Defensive: do not block the UI during loading — surface a spinner or disable the submit button only, leaving previous outputs visible (good UX for retries).

## Verification Checklist Before Reporting Stage 6 Complete
Provide answers to:
- List of all frontend files created with their paths.
frontend/package.json dependencies and pinned versions.
- Confirm CORS config in backend/main.py (paste the exact middleware block).
- Sample TS interface for PipelineOutput from frontend/lib/types.ts.
- Confirm npx next build runs cleanly without TS errors (or describe if you can't verify in this environment).
- Confirm Docker build for frontend works end-to-end (or note Stage 7 dependency).

## What's STILL Deferred (Don't Touch Yet)
- Live EdenAI integration with real API key — Stage 7.
- Production deployment to Cloud Run — final docs pass after Stage 7.
- Frontend tests (Jest/Playwright) — out of portfolio MVP scope unless you flag separately.
- Authentication / user accounts — explicitly out of scope per AGENTS.md (deterministic transformation DAG, not a multi-tenant SaaS).
