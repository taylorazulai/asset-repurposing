import logging

from core.config import settings
from core.schemas import CoreContext
from pipeline.llm_client import chat_completion
from pipeline.utils import parse_json_response

logger = logging.getLogger(__name__)

EXTRACTION_PROMPT = """You are an expert document analyst. Read the source document below and extract the following Core Context fields as a JSON object:

- title: a concise title or headline theme (string)
- themes: a list of key themes (3-7 items)
- tone: the detected brand tone and voice (e.g., professional, conversational, technical, playful)
- audience: the target audience description
- primary_arguments: the main arguments or takeaways (3-5 items)

Return ONLY valid JSON matching this exact schema:
{{
  "title": "...",
  "themes": ["...", "..."],
  "tone": "...",
  "audience": "...",
  "primary_arguments": ["...", "..."]
}}

Source document:
{source_text}
"""


async def extract_core_context(source_text: str) -> CoreContext:
    """Extract the Core Context Entity from the source document."""
    truncated = len(source_text) > settings.MAX_SOURCE_CHARS
    if truncated:
        logger.warning(
            "Source text truncated from %d to %d characters for extraction.",
            len(source_text),
            settings.MAX_SOURCE_CHARS,
        )

    prompt = EXTRACTION_PROMPT.format(source_text=source_text[: settings.MAX_SOURCE_CHARS])
    messages = [
        {
            "role": "system",
            "content": "You are a helpful document analyst that returns only valid JSON.",
        },
        {"role": "user", "content": prompt},
    ]
    response = await chat_completion(messages, temperature=0.3)
    data = parse_json_response(response)
    return CoreContext(**data, truncated=truncated)
