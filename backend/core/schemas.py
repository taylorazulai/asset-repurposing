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


class SlideDeck(BaseModel):
    title: str
    slides: List[Slide]


class PipelineOutput(BaseModel):
    core_context: CoreContext
    executive_brief: ExecutiveBrief | None = None
    social_snippets: List[SocialSnippet] | None = None
    slide_deck: SlideDeck | None = None
    errors: Dict[str, str] = {}
