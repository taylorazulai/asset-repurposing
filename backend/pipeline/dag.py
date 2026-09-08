import asyncio
from typing import Dict

from core.schemas import CoreContext, PipelineOutput
from pipeline.extractors import extract_core_context
from pipeline.generators import (
    generate_executive_brief,
    generate_social_snippets,
    generate_slide_deck,
)


async def run_pipeline(source_text: str) -> PipelineOutput:
    """Run the full DAG: extract core context, then generate assets in parallel."""
    core_context: CoreContext = await extract_core_context(source_text)

    coroutines = {
        "executive_brief": generate_executive_brief(core_context),
        "social_snippets": generate_social_snippets(core_context),
        "slide_deck": generate_slide_deck(core_context),
    }

    results = await asyncio.gather(*coroutines.values(), return_exceptions=True)

    kwargs: Dict = {
        "core_context": core_context,
        "errors": {},
    }

    for name, result in zip(coroutines.keys(), results):
        if isinstance(result, Exception):
            kwargs["errors"][name] = f"{type(result).__name__}: {result}"
        else:
            kwargs[name] = result

    return PipelineOutput(**kwargs)
