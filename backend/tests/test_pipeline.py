import json
from typing import Any, Callable, Dict

import pytest
from fastapi.testclient import TestClient

import main
import pipeline.extractors as extractors
import pipeline.generators as generators
from core import schemas
from core.config import settings


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def _make_fake_chat_completion(config: Dict[str, Any] = None) -> Callable:
    """Return an async fake chat_completion function driven by a config dict."""
    config = config or {}

    async def fake_chat_completion(messages, model=None, temperature=0.7) -> str:
        user = messages[-1]["content"]

        if "Core Context fields" in user or "expert document analyst" in user:
            if config.get("extract_fail"):
                raise RuntimeError("extraction failed")
            return json.dumps(
                config.get(
                    "core_context",
                    {
                        "title": "Mock Title",
                        "themes": ["theme1"],
                        "tone": "professional",
                        "audience": "developers",
                        "primary_arguments": ["argument1"],
                    },
                )
            )

        if "executive brief" in user:
            if config.get("executive_brief_fail"):
                raise RuntimeError("executive brief failed")
            return json.dumps(
                config.get(
                    "executive_brief",
                    {
                        "headline": "Mock Headline",
                        "summary": "Mock summary.",
                        "key_points": ["point1"],
                        "call_to_action": "Act now.",
                    },
                )
            )

        if "social media snippets" in user:
            if config.get("social_snippets_fail"):
                raise RuntimeError("social snippets failed")
            return json.dumps(
                config.get(
                    "social_snippets",
                    {
                        "social_snippets": [
                            {
                                "platform": "LinkedIn",
                                "text": "LinkedIn post",
                                "hashtags": ["#AI"],
                            }
                        ]
                    },
                )
            )

        if "slide deck" in user:
            if config.get("slide_deck_fail"):
                raise RuntimeError("slide deck failed")
            return json.dumps(
                config.get(
                    "slide_deck",
                    {
                        "title": "Mock Deck",
                        "slides": [
                            {
                                "title": "Slide 1",
                                "bullets": [
                                    {"text": "bullet1", "sub": ["sub-bullet1"]}
                                ],
                                "speaker_notes": "Notes.",
                            }
                        ],
                    },
                )
            )

        raise RuntimeError(f"Unexpected prompt: {user[:80]}")

    return fake_chat_completion


# ---------------------------------------------------------------------------
# Schema validation tests
# ---------------------------------------------------------------------------

def test_ingest_payload_valid():
    payload = schemas.IngestPayload(source_text="This is a valid source document with enough characters.")
    assert payload.source_text == "This is a valid source document with enough characters."


def test_ingest_payload_empty_rejected():
    with pytest.raises(ValueError):
        schemas.IngestPayload(source_text="")


def test_ingest_payload_too_short_rejected():
    with pytest.raises(ValueError):
        schemas.IngestPayload(source_text="Too short")


def test_core_context_valid():
    ctx = schemas.CoreContext(
        title="Title",
        themes=["t1", "t2"],
        tone="professional",
        audience="devs",
        primary_arguments=["a1"],
        truncated=True,
    )
    assert ctx.truncated is True


def test_social_snippet_valid_platforms():
    schemas.SocialSnippet(platform="LinkedIn", text="Hello", hashtags=[])
    schemas.SocialSnippet(platform="Twitter/X", text="Hello", hashtags=[])


def test_social_snippet_invalid_platform_rejected():
    with pytest.raises(ValueError):
        schemas.SocialSnippet(platform="Facebook", text="Hello", hashtags=[])


def test_executive_brief_valid():
    brief = schemas.ExecutiveBrief(
        headline="H",
        summary="S",
        key_points=["k1"],
        call_to_action="CTA",
    )
    assert brief.headline == "H"


def test_slide_deck_valid():
    deck = schemas.SlideDeck(
        title="Deck",
        slides=[
            schemas.Slide(
                title="Slide 1",
                bullets=[
                    schemas.BulletPoint(text="b1", sub=["s1"]),
                    schemas.BulletPoint(text="b2", sub=[]),
                ],
                speaker_notes="notes",
            )
        ],
    )
    assert len(deck.slides) == 1
    assert deck.slides[0].bullets[0].sub == ["s1"]


def test_slide_bullet_sub_validation():
    with pytest.raises(ValueError):
        schemas.Slide(
            title="Slide 1",
            bullets=[
                schemas.BulletPoint(text="b1", sub=["s1", "s2", "s3", "s4"]),
            ],
            speaker_notes="notes",
        )


def test_pipeline_output_partial_results():
    ctx = schemas.CoreContext(
        title="T",
        themes=["t"],
        tone="t",
        audience="a",
        primary_arguments=["a"],
    )
    brief = schemas.ExecutiveBrief(
        headline="H", summary="S", key_points=["k"], call_to_action="CTA"
    )
    output = schemas.PipelineOutput(
        core_context=ctx,
        executive_brief=brief,
        errors={"social_snippets": "RuntimeError: boom"},
    )
    assert output.executive_brief is not None
    assert output.social_snippets is None
    assert output.errors["social_snippets"] == "RuntimeError: boom"


# ---------------------------------------------------------------------------
# Endpoint tests
# ---------------------------------------------------------------------------

def test_pipeline_happy_path(monkeypatch):
    monkeypatch.setattr(
        extractors, "chat_completion", _make_fake_chat_completion()
    )
    monkeypatch.setattr(
        generators, "chat_completion", _make_fake_chat_completion()
    )

    client = TestClient(main.app)
    response = client.post(
        "/pipeline",
        json={"source_text": "This is a long enough test document for the pipeline."},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["core_context"]["title"] == "Mock Title"
    assert body["executive_brief"] is not None
    assert body["social_snippets"] is not None
    assert body["slide_deck"] is not None
    assert body["errors"] == {}
    assert body["core_context"]["truncated"] is False


def test_pipeline_truncated_source(monkeypatch):
    long_text = "x" * (settings.MAX_SOURCE_CHARS + 50)
    monkeypatch.setattr(
        extractors, "chat_completion", _make_fake_chat_completion()
    )
    monkeypatch.setattr(
        generators, "chat_completion", _make_fake_chat_completion()
    )

    client = TestClient(main.app)
    response = client.post(
        "/pipeline",
        json={"source_text": long_text},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["core_context"]["truncated"] is True


def test_pipeline_single_generator_failure(monkeypatch):
    config = {"executive_brief_fail": True}
    monkeypatch.setattr(
        extractors, "chat_completion", _make_fake_chat_completion(config)
    )
    monkeypatch.setattr(
        generators, "chat_completion", _make_fake_chat_completion(config)
    )

    client = TestClient(main.app)
    response = client.post(
        "/pipeline",
        json={"source_text": "This is a long enough test document for the pipeline."},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["executive_brief"] is None
    assert body["social_snippets"] is not None
    assert body["slide_deck"] is not None
    assert "executive_brief" in body["errors"]


def test_pipeline_all_generators_failure(monkeypatch):
    config = {
        "executive_brief_fail": True,
        "social_snippets_fail": True,
        "slide_deck_fail": True,
    }
    monkeypatch.setattr(
        extractors, "chat_completion", _make_fake_chat_completion(config)
    )
    monkeypatch.setattr(
        generators, "chat_completion", _make_fake_chat_completion(config)
    )

    client = TestClient(main.app)
    response = client.post(
        "/pipeline",
        json={"source_text": "This is a long enough test document for the pipeline."},
    )

    assert response.status_code == 500
    body = response.json()
    assert body["detail"]["message"] == "All asset generators failed"
    assert set(body["detail"]["errors"].keys()) == {
        "executive_brief",
        "social_snippets",
        "slide_deck",
    }


def test_pipeline_extractor_failure(monkeypatch):
    config = {"extract_fail": True}
    monkeypatch.setattr(
        extractors, "chat_completion", _make_fake_chat_completion(config)
    )
    monkeypatch.setattr(
        generators, "chat_completion", _make_fake_chat_completion(config)
    )

    client = TestClient(main.app)
    response = client.post(
        "/pipeline",
        json={"source_text": "This is a long enough test document for the pipeline."},
    )

    assert response.status_code == 500
    body = response.json()
    assert body["detail"]["error"] == "extraction_failed"
    assert "extraction failed" in body["detail"]["detail"]
