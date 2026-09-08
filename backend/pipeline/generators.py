from typing import List

from core.schemas import CoreContext, ExecutiveBrief, SlideDeck, SocialSnippet
from pipeline.llm_client import chat_completion
from pipeline.utils import parse_json_response


EXECUTIVE_BRIEF_PROMPT = """Using the following Core Context, generate a one-page executive brief.
Return ONLY valid JSON matching this exact schema:
{{
  "headline": "...",
  "summary": "...",
  "key_points": ["...", "..."],
  "call_to_action": "..."
}}

Core context:
{core_context}
"""


SOCIAL_SNIPPETS_PROMPT = """Using the following Core Context, generate social media snippets for LinkedIn and Twitter/X.
Return ONLY valid JSON matching this exact schema:
{{
  "social_snippets": [
    {{"platform": "LinkedIn", "text": "...", "hashtags": ["...", "..."]}},
    {{"platform": "Twitter/X", "text": "...", "hashtags": ["...", "..."]}}
  ]
}}

Respect each platform's character style and length norms (LinkedIn ~1300 chars, Twitter/X ~280 chars).

Core context:
{core_context}
"""


SLIDE_DECK_PROMPT = """Using the following Core Context, generate a slide deck outline with a title slide and 4-6 content slides.
Return ONLY valid JSON matching this exact schema:
{{
  "title": "...",
  "slides": [
    {{"title": "...", "bullets": ["...", "..."], "speaker_notes": "..."}},
    ...
  ]
}}

Core context:
{core_context}
"""


async def generate_executive_brief(core_context: CoreContext) -> ExecutiveBrief:
    """Generate a one-page executive brief from the core context."""
    prompt = EXECUTIVE_BRIEF_PROMPT.format(
        core_context=core_context.model_dump_json(indent=2)
    )
    messages = [
        {
            "role": "system",
            "content": "You are a marketing strategist that returns only valid JSON.",
        },
        {"role": "user", "content": prompt},
    ]
    response = await chat_completion(messages, temperature=0.7)
    data = parse_json_response(response)
    return ExecutiveBrief(**data)


async def generate_social_snippets(core_context: CoreContext) -> List[SocialSnippet]:
    """Generate platform-specific social snippets from the core context."""
    prompt = SOCIAL_SNIPPETS_PROMPT.format(
        core_context=core_context.model_dump_json(indent=2)
    )
    messages = [
        {
            "role": "system",
            "content": "You are a social media copywriter that returns only valid JSON.",
        },
        {"role": "user", "content": prompt},
    ]
    response = await chat_completion(messages, temperature=0.8)
    data = parse_json_response(response)
    return [SocialSnippet(**item) for item in data["social_snippets"]]


async def generate_slide_deck(core_context: CoreContext) -> SlideDeck:
    """Generate a slide deck outline from the core context."""
    prompt = SLIDE_DECK_PROMPT.format(
        core_context=core_context.model_dump_json(indent=2)
    )
    messages = [
        {
            "role": "system",
            "content": "You are a presentation designer that returns only valid JSON.",
        },
        {"role": "user", "content": prompt},
    ]
    response = await chat_completion(messages, temperature=0.7)
    data = parse_json_response(response)
    return SlideDeck(**data)
