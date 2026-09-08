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

---

# Asset Repurposing Pipeline — Next Steps

> **Status:** Project portfolio-ready as of 2026-09-08. This document kicks off
> the next iteration and carries forward the open items declared in the public
> README.

## Inherited from Public README

These items are inherited verbatim from the public README's "Known Limits &
Next Steps" section and remain open:

- **Cloud Run deployment** — Dockerfiles are Cloud Run-shaped but not
  actively deployed. Push containers to Google Artifact Registry and deploy
  with the same `BACKEND_URL` plumbing.
- **Frontend tests** — add a Jest or Playwright suite covering the happy
  path and the three error branches (`network`, `extraction_failed`,
  `all_generators_failed`).
- **Retry-specific tests** — fail-then-succeed unit tests around the
  `tenacity`-wrapped LLM client (currently the only retry coverage is
  `tenacity`'s own upstream tests).
- **Authentication** — out of scope. The pipeline is deterministic and stateless.
- **Longer documents** — sources beyond `MAX_SOURCE_CHARS` are truncated
  before extraction. Future work could chunk and merge very large documents.

The remainder of this doc layers on **two new stages** with specific
 deliverables driven by the maintainer (Taylor).

---

## Stage 8: UX & Prompt Polish

**Goal:** Tighten the user-facing feel of the app and sharpen the prompt
personas so the LLM "writes like a pro, not like a generic assistant."

### Deliverable F1 — Frontend max-character gate (mirror backend cap)

**What:** The frontend currently enforces a 50-character *minimum* in
`UploadForm.tsx` but no enforced *maximum*. The backend silently truncates
sources beyond `MAX_SOURCE_CHARS` (currently defaulted to 20000). After
this stage, the system has a user-visible, hard maximum of `50000` characters
on both the frontend and backend.

**Why 50,000:** Still within a small-budget token envelope (~12–13k tokens
for most encodings), and large enough to cover the example document currently
linked in the live demo (the Perplexity D&D Handbook) without truncating.
This means the truncation banner in the demo eventually becomes unnecessary
for that benchmark doc.

**Tasks:**

1. `backend/.env.example` — set `MAX_SOURCE_CHARS=50000` as the new default.
2. `backend/core/config.py` — update the Pydantic-Settings default.
3. `frontend/.env.example` — add a comment block noting the matching cap
   (the proxy already forwards `source_text` verbatim; if the input is
   over the cap, the backend truncates silently with a warning log).
4. `frontend/app/components/UploadForm.tsx`:
   - Add a live character counter beneath the textarea
     (e.g., *"1,234 / 50,000 characters"*).
   - Disable the submit button when input exceeds `50000`.
   - Show an inline hint ("Source is too long — please trim to under
     50,000 characters") when over the cap.
   - Cap the value `MAX_FRONTEND_SOURCE_CHARS = 50000` as a constant in
     the component (or `lib/constants.ts` if multiple consumers need it).
5. Update root `README.md` and the live demo's truncation caption:
   footnote the new default and confirm the example doc no longer hits
   the cap.

**Verification:**

- `pytest -v` — 14 tests still pass after the config default change.
- `npm run build` — clean.
- Manual: paste a 60,000-char source — frontend blocks submit, backend
  would still truncate if hit directly via `curl`.

### Deliverable F2 — Distinct CSS palette

**What:** Replace the Tailwind defaults with a manuscript / publication feel.

**Color map:**

| Element | Color | Notes |
|---------|-------|-------|
| Page background | Vanilla cream | `#F8F4E9` or `#FBF6E9` |
| Body font | Black | `#1A1A1A` |
| Headings (h1, h2, h3) | Dark emerald | `#065F46` (Tailwind `emerald-800`) |
| Subscripts, italics, captions | Grey | `#6B7280` (Tailwind `gray-500`) |
| Truncation warning | Dark red text on light red bg | text `#B91C1C`, bg `#FEE2E2` |

**Tasks:**

1. Update `frontend/styles/globals.css` to declare the palette as CSS
   custom properties in `:root`:

   ```css
   :root {
     --color-bg:        #FBF6E9;  /* vanilla cream */
     --color-text:      #1A1A1A;  /* near-black */
     --color-heading:   #065F46;  /* emerald-800 */
     --color-muted:     #6B7280;  /* gray-500 */
     --color-warn-text: #B91C1C;  /* red-700 */
     --color-warn-bg:   #FEE2E2;  /* red-100 */
   }
   ```

2. Update `frontend/tailwind.config.cjs` to extend the theme with these
   custom utilities:

   ```js
   theme: {
     extend: {
       colors: {
         cream:    '#FBF6E9',
         heading:  '#065F46',
         muted:    '#6B7280',
         warnText: '#B91C1C',
         warnBg:   '#FEE2E2',
       },
     },
   }
   ```

3. Update components:
   - `<body>` in `app/layout.tsx` → `bg-cream text-[#1A1A1A]`.
   - All `<h1>`/`<h2>`/`<h3>` → `text-heading`.
   - Footnote / disclaimer subtitles → `text-muted italic`.
4. Create `frontend/app/components/TruncationBanner.tsx`:
   - Tailwind: `bg-warnBg text-warnText border border-warnText rounded p-3`.
   - Optional icon (warning triangle or similar).
5. Wire `TruncationBanner.tsx` into `OutputCards.tsx` so it renders at
   the top of the asset column whenever `core_context.truncated === true`.

**Verification:**

- WCAG contrast spot-check (the red-on-light-red pairing comes out to
  ~7.5:1 on `#B91C1C` against `#FEE2E2` — passes AA. Maintain this and
  don't downgrade).
- `npm run build` clean.
- Visual smoke test: load the D&D Handbook document, screenshot the
  rendered output, confirm colors match the table above.
- Replace the public demo screenshot (`local-source-truncated-and-executive-brief.png`)
  with an updated one showing the new palette.

### Deliverable F3 — Persona-prefixed system roles (dynamic domain)

**What:** All four system prompts currently use generic roles
("You are a marketing strategist that returns only valid JSON."). After
this stage, each node anchors a specific expert persona, AND the system
role dynamically incorporates the domain inferred by the extractor
(`core_context.tone`, `themes`, and `audience`) so the LLM voice matches
the actual source material.

**Persona map** (role is fixed per node; domain is dynamic):

| Node | Fixed role fragment |
|------|---------------------|
| Extraction | You are an expert content strategist with 8 years of experience analyzing long-form marketing and editorial assets. |
| Executive brief | You are an expert strategy consultant with 10 years of experience writing executive briefs at McKinsey-style firms. |
| Social snippets | You are an expert B2B social copywriter with 5 years of experience crafting LinkedIn and Twitter/X posts for technical and executive audiences. |
| Slide deck | You are an expert presentation designer with 10 years of experience building decks for Fortune 500 leadership audiences. |

Each is composed with the extracted domain at runtime. Implementation
sketch:

```python
# inside each generator, after core_context is in scope
domain_phrase = (
    f"You are currently working with {core_context.tone.strip().lower()} "
    f"content on the themes of {', '.join(core_context.themes[:3])}, "
    f"targeting an audience of {core_context.audience.lower()}."
)
system_role = f"{static_role_fragment} {domain_phrase}"
messages = [
    {"role": "system", "content": system_role},
    {"role": "user",   "content": prompt},
]
```

**Tasks:**

1. `backend/pipeline/extractors.py` — rebuild the messages array with a
   static role fragment + a domain-injection step (extractor's domain
   comes from `payload.source_text` directly, but it can self-bootstrap
   using its own instruction: "first infer the core context's tone and
   themes, then adopt a domain-expert persona accordingly").
2. `backend/pipeline/generators.py` — refactor each generator's prompt
   construction to take a `CoreContext` (already does) and build the
   persona-aware system role as shown above. Keep temperature settings
   per generator as they are now (0.3 / 0.7 / 0.8 / 0.7).
3. Update the existing 14 tests' mock fixture (`_make_fake_chat_completion`)
   if needed — the messages payload will now include the dynamic system
   role string, but the tests only branch on user-prompt content, so the
   fixture should still pass without changes.
4. Create `docs/decisions/2026-09-08-persona-driven-prompts.md` (new ADR)
   with rationale: "Let the LLM voice match the actual content
   domain rather than producing generic marketing copy."

**Verification:**

- `pytest -v` — 14 tests still pass.
- Live `POST /pipeline` against a casual gaming audience document
  (e.g., a mobile-game press release) — confirm the executive brief and
  social snippets now have voice shifted toward that domain, vs. the
  default McKinsey-style tone you'd get for a B2B whitepaper.
- Confirm `messages[0].content` (system role) reflects the dynamic
  domain in any test-debug snippet.

---

## Stage 9: Schema & Slide Deck Refinement

**Goal:** The current slide deck output is a flat list of 3 bullets per
slide. Real professional slide decks have hierarchy: main points with
0–3 sub-bullets, plus cleaner section/agenda/recap slides.

### Deliverable F4 — Tiered bullet hierarchy (Option C: two-level explicit)

**What:** Replace `bullets: List[str]` on the `Slide` schema with a
two-level explicit structure: each "main bullet" carries 0–3 supporting
sub-bullets. No deeper nesting (most professional decks don't go beyond
two levels of indentation visually).

**Schema changes:**

```python
# backend/core/schemas.py

from pydantic import BaseModel, Field
from typing import List

class BulletPoint(BaseModel):
    text: str = Field(..., description="The main bullet headline.")
    sub: List[str] = Field(
        default_factory=list,
        max_length=3,
        description="0-3 supporting sub-bullets that elaborate on the main point.",
    )

class Slide(BaseModel):
    title: str = Field(..., description="Slide title or section header.")
    bullets: List[BulletPoint] = Field(
        ..., description="2-4 main bullets; each may have 0-3 sub-bullets."
    )
    speaker_notes: str = Field(..., description="30-60 second talk track per slide.")
```

**TypeScript mirror** (`frontend/lib/types.ts`):

```ts
export interface BulletPoint {
  text: string;
  sub: string[];             // 0-3 items
}

export interface Slide {
  title: string;
  bullets: BulletPoint[];
  speaker_notes: string;
}
```

**Prompt rewrite** (`backend/pipeline/generators.py:SLIDE_DECK_PROMPT`):

```text
You are an expert presentation designer with 10 years of experience
building decks for Fortune 500 leadership audiences.

Generate a professional slide deck suitable for a senior leadership audience.
Include:
- a title slide,
- an agenda slide,
- 3-5 content slides,
- a recap / key-takeaways slide.

Each content slide should have 2-4 main bullets. Each main bullet may have
0-3 sub-bullets — only when the source material naturally elaborates
hierarchically. Avoid filler. Each slide's speaker_notes should be a
30-60 second talk track.

Return ONLY valid JSON matching this exact schema:
{
  "title": "...",
  "slides": [
    {
      "title": "...",
      "bullets": [
        {"text": "Main bullet", "sub": ["supporting point", "supporting point"]},
        {"text": "Main bullet", "sub": []},
        ...
      ],
      "speaker_notes": "..."
    },
    ...
  ]
}

Core context:
{core_context}
```

**Tasks:**

1. Update `backend/core/schemas.py` with the new `BulletPoint` model
   and update `Slide.bullets` to `List[BulletPoint]`.
2. Update `frontend/lib/types.ts` to mirror exactly. Add
   `// Mirrors backend/core/schemas.py:BulletPoint` and
   `// Mirrors ...:Slide` comments.
3. Update `backend/pipeline/generators.py:SLIDE_DECK_PROMPT` per the
   text above.
4. Update `frontend/app/components/OutputCards.tsx` to render the
   nested structure visually: each main bullet as a top-level `<li>`
   with its sub-bullets as nested `<ul>` / `<li>` items, plus the
   existing copy buttons per bullet.
5. Update existing test fixtures:
   - `tests/test_pipeline.py:test_slide_deck_valid` — change the fixture
     to use the new shape (`{"text": "...", "sub": ["..."]}`).
   - `_make_fake_chat_completion`'s slide-deck branch — return a
     `BulletPoint`-shaped JSON.
6. Add a new test: `test_slide_bullet_sub_validation` confirming
   that more than 3 sub-bullets is rejected.

**Verification:**

- `pytest -v` — should report 15 passing tests (14 existing + the new
  sub-bullet-validation test).
- `npm run build` — clean.
- Live `POST /pipeline` against the D&D Handbook: confirm at least one
  content slide now has main bullets with 1-2 sub-bullets (natural
  hierarchy in the source material).
- Update the public demo screenshot for slide deck
  (`local-asset-slide-deck-bullets-with-speaker-notes.png` →
  `local-asset-slide-deck-tiered-bullets-with-speaker-notes.png`) so
  the portfolio reflects the new shape.

### Closeout Checklist for Stage 9

Before reporting Stage 9 complete, the agent should provide:

- [ ] Full text of `frontend/app/components/UploadForm.tsx`
  (showing the new char counter + submit disable logic).
- [ ] Full text of `frontend/styles/globals.css` and
  `frontend/tailwind.config.cjs`.
- [ ] Full text of `frontend/app/components/TruncationBanner.tsx` (new).
- [ ] Full text of `backend/core/schemas.py` (showing `BulletPoint`).
- [ ] Full text of `backend/pipeline/generators.py` and `extractors.py`
  (with persona-prompt refactor).
- [ ] New ADR: `docs/decisions/2026-09-08-persona-driven-prompts.md`.
- [ ] `npm run build` clean.
- [ ] `pytest -v` — 15+ tests passing.
- [ ] Live `POST /pipeline` against the D&D Handbook, confirming:
  - [ ] Frontend character counter shows a non-truncating count for that
    document.
  - [ ] System-role message contains the dynamic domain phrase derived
    from the extracted `core_context`.
  - [ ] At least one slide now has tiered bullets in the live response.
- [ ] Updated public demo screenshots in `screenshots/`.
- [ ] Root `README.md` Known Limits & Next Steps section updated:
  bump `MAX_SOURCE_CHARS=50000` and remove the "longer documents"
  caveat (or scope it down to >50000 chars).

---

## Out of Scope for This Iteration

(Carried forward from public README's Known Limits, deferred to a
separate deploy or test-coverage iteration.)

- Authentication.
- Cloud Run deployment.
- Jest / Playwright frontend tests.
- Retry-specific fail-then-succeed tests.
- Document chunking & merging for sources >50,000 characters (deferred
  entirely; current truncation-and-warn behavior is intentional).
