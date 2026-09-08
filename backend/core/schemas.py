from pydantic import BaseModel, Field
from typing import Dict, List, Literal


class IngestPayload(BaseModel):
    source_text: str = Field(
        ...,
        min_length=20,
        description="Raw source document text to decompose into derivative assets.",
    )


class CoreContext(BaseModel):
    title: str = Field(..., description="Document title or headline theme.")
    themes: List[str] = Field(..., description="Key themes extracted from the document.")
    tone: str = Field(..., description="Detected brand tone and voice.")
    audience: str = Field(..., description="Target audience description.")
    primary_arguments: List[str] = Field(
        ..., description="Main arguments or takeaways from the document."
    )
    truncated: bool = Field(
        default=False,
        description="Whether the source text was truncated before extraction.",
    )


class ExecutiveBrief(BaseModel):
    headline: str
    summary: str
    key_points: List[str]
    call_to_action: str


class SocialSnippet(BaseModel):
    platform: Literal["LinkedIn", "Twitter/X"]
    text: str
    hashtags: List[str] = []


class Slide(BaseModel):
    title: str
    bullets: List[str]
    speaker_notes: str


class SlideDeck(BaseModel):
    title: str
    slides: List[Slide]


class PipelineOutput(BaseModel):
    core_context: CoreContext
    executive_brief: ExecutiveBrief | None = None
    social_snippets: List[SocialSnippet] | None = None
    slide_deck: SlideDeck | None = None
    errors: Dict[str, str] = {}
