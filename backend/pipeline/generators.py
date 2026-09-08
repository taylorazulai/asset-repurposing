from typing import List

from core.schemas import CoreContext, ExecutiveBrief, SlideDeck, SocialSnippet
from pipeline.llm_client import chat_completion
from pipeline.utils import parse_json_response


EXECUTIVE_BRIEF_ROLE = (
    "You are an expert strategy consultant with 10 years of experience writing "
    "executive briefs at McKinsey-style firms."
)

SOCIAL_SNIPPETS_ROLE = (
    "You are an expert B2B social copywriter with 5 years of experience crafting "
    "LinkedIn and Twitter/X posts for technical and executive audiences."
)

SLIDE_DECK_ROLE = (
    "You are an expert presentation designer with 10 years of experience building "
    "decks for Fortune 500 leadership audiences."
)


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


def _build_system_role(static_role: str, core_context: CoreContext) -> str:
    """Compose a persona-aware system role with a fixed expert fragment and a
    dynamic domain phrase inferred from the extracted core context.

    Gracefully handles empty or missing tone, themes, or audience by falling
    back to generic phrasing so the prompt never renders with blank clauses.
    """
    tone = core_context.tone.strip().lower() or "the provided source material"
    themes = [t.strip() for t in core_context.themes[:3] if t.strip()]
    themes_clause = f" on the themes of {', '.join(themes)}" if themes else ""
    audience = core_context.audience.strip().lower() or "the intended readers"

    domain_phrase = (
        f"You are currently working with {tone} content{themes_clause}, "
        f"targeting an audience of {audience}."
    )
    return f"{static_role} {domain_phrase} Return only valid JSON."


async def generate_executive_brief(core_context: CoreContext) -> ExecutiveBrief:
    """Generate a one-page executive brief from the core context."""
    prompt = EXECUTIVE_BRIEF_PROMPT.format(
        core_context=core_context.model_dump_json(indent=2)
    )
    messages = [
        {
            "role": "system",
            "content": _build_system_role(EXECUTIVE_BRIEF_ROLE, core_context),
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
            "content": _build_system_role(SOCIAL_SNIPPETS_ROLE, core_context),
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
            "content": _build_system_role(SLIDE_DECK_ROLE, core_context),
        },
        {"role": "user", "content": prompt},
    ]
    response = await chat_completion(messages, temperature=0.7)
    data = parse_json_response(response)
    return SlideDeck(**data)
