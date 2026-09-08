# Decision: Error-Handling Pattern for the Pipeline DAG

**Date:** 2026-09-07
**Decision:** Use partial-results-with-error-flags for generator failures; fail-fast only for the extraction node.
**Status:** Accepted

## Context

The pipeline has one extraction step followed by three independent generation steps (executive brief, social snippets, slide deck). Each generation step is an LLM call to EdenAI. We need a strategy that gives the user useful output when the system is partially healthy, while preventing meaningless downstream generation if core extraction fails.

## Options Considered

1. **Fail-fast on any failure** — If any generator or the extractor fails, return a 500 and no assets.
   - Pros: Simple, guarantees complete output or nothing.
   - Cons: A single LLM hiccup or provider outage wipes out all assets, giving the user nothing useful and making the system feel brittle.

2. **Partial results with error flags** — Run all generators in parallel; if one fails, capture the error and still return the other successful assets.
   - Pros: Resilient, better UX for a content-repurposing tool, lets users inspect and use partial output while retrying only the failed asset.
   - Cons: Slightly more complex response schema (requires an `errors` field), and the caller must handle optional fields.

3. **Retries with fallback** — Retry each failed generator once or twice before surfacing an error.
   - Pros: Can mask transient failures automatically.
   - Cons: Increases cost and latency; should be added as a second layer after the partial-results pattern is in place, not as the primary strategy.

## Decision

Adopt **partial results with error flags** as the primary error-handling pattern:

- The **extraction node is fail-fast**. If `CoreContext` cannot be extracted, the entire pipeline returns an error because the downstream generators have no shared context to work from.
- The **generation nodes are best-effort**. Each runs independently via `asyncio.gather(..., return_exceptions=True)`. If a generator fails, the error is recorded and the other generators still return their assets.

## Implementation Sketch

```python
class PipelineOutput(BaseModel):
    core_context: CoreContext
    executive_brief: ExecutiveBrief | None = None
    social_snippets: List[SocialSnippet] | None = None
    slide_deck: SlideDeck | None = None
    errors: Dict[str, str] = {}  # node_name -> error message
```

The DAG will:
1. Extract `CoreContext` (raise on failure).
2. Run the three generators concurrently.
3. Build a `PipelineOutput` with successful results and any errors collected per node.
4. Return the response with a 200 status if at least one generator succeeded, or a 500 if all generators failed.

## Consequences

- The frontend must render optional fields and display any error messages to the user.
- The response schema is explicit about what succeeded and what failed.
- Retries and fallbacks can be layered on top later without changing the public API shape.

## References

- `docs/running-doc.md` — Stage 3 will implement this pattern.
- `backend/core/schemas.py` — `PipelineOutput` will be updated to include optional fields and an `errors` map.
