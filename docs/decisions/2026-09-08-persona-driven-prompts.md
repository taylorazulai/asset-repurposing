# Decision: Persona-Driven System Prompts

**Date:** 2026-09-08
**Status:** Accepted

## Context

The initial pipeline prompts used a single generic system role — e.g., "You are a helpful document analyst that returns only valid JSON." — for every node. This produced competent but bland, marketing-generic copy regardless of the source material's actual domain. A gaming handbook, a mobile-app press release, and a B2B whitepaper all came back sounding like the same consultant wrote them.

## Decision

Anchor each LLM node to a specific expert persona and dynamically inject a domain phrase derived from the extracted `CoreContext` (`tone`, `themes`, and `audience`).

**Fixed persona fragments:**

| Node | Persona |
|------|-----------|
| Extraction | Expert content strategist with 8 years analyzing long-form marketing and editorial assets. |
| Executive brief | Expert strategy consultant with 10 years writing executive briefs at McKinsey-style firms. |
| Social snippets | Expert B2B social copywriter with 5 years crafting LinkedIn and Twitter/X posts for technical and executive audiences. |
| Slide deck | Expert presentation designer with 10 years building decks for Fortune 500 leadership audiences. |

**Dynamic domain phrase:**

```python
f"You are currently working with {tone} content on the themes of {themes}, targeting an audience of {audience}."
```

The final system message is composed as: `{fixed persona} {dynamic domain phrase} Return only valid JSON.`

## Consequences

**Positive:**
- LLM output voice adapts to the actual content domain instead of defaulting to generic marketing prose.
- Personas are explicit and reproducible, making prompt behavior easier to reason about and tune.
- The dynamic phrase is derived from structured schema fields, so it is deterministic for a given input.

**Negative:**
- Slightly more tokens per request due to the persona and domain phrase.
- If the extractor misidentifies tone or audience, the downstream generators inherit the error.

## Implementation

- `backend/pipeline/extractors.py` — uses the content strategist persona and asks the model to infer tone/themes/audience first, then adopt the appropriate domain-expert stance.
- `backend/pipeline/generators.py` — each generator calls `_build_system_role(static_role, core_context)` to compose its persona-aware system message.
- `docs/decisions/2026-09-08-persona-driven-prompts.md` — this ADR.
