from fastapi import APIRouter, HTTPException

from core.schemas import IngestPayload, PipelineOutput
from pipeline.dag import run_pipeline

router = APIRouter(prefix="/pipeline", tags=["pipeline"])


@router.post("/", response_model=PipelineOutput)
async def pipeline(payload: IngestPayload) -> PipelineOutput:
    """Trigger the asset decomposition pipeline."""
    try:
        result = await run_pipeline(payload.source_text)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={"error": "extraction_failed", "detail": str(exc)},
        ) from exc

    # If every generator failed, surface it as a server error.
    if not any([result.executive_brief, result.social_snippets, result.slide_deck]):
        raise HTTPException(
            status_code=500,
            detail={"message": "All asset generators failed", "errors": result.errors},
        )

    return result
