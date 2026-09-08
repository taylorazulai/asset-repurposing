import openai
from tenacity import (
    AsyncRetrying,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from core.config import settings

client = openai.AsyncOpenAI(
    api_key=settings.EDENAI_API_KEY,
    base_url=settings.EDENAI_BASE_URL,
    timeout=60,
)


def _should_retry(exc: Exception) -> bool:
    """Retry on connection issues, timeouts, 5xx errors, and rate limits (429)."""
    if isinstance(exc, (openai.APIConnectionError, openai.APITimeoutError)):
        return True
    if isinstance(exc, openai.InternalServerError):
        return True
    if isinstance(exc, openai.APIStatusError):
        # Retry 5xx and rate limits; do not retry other 4xx errors.
        return exc.status_code >= 500 or exc.status_code == 429
    return False


async def chat_completion(
    messages: list,
    model: str | None = None,
    temperature: float = 0.7,
) -> str:
    """Send a chat completion request to the EdenAI-compatible endpoint.

    Retries up to 2 additional times on transient errors (connection, timeout,
    5xx, 429) with exponential backoff. Does not retry on other 4xx errors.
    """
    model = model or settings.EDENAI_MODEL

    async for attempt in AsyncRetrying(
        stop=stop_after_attempt(3),  # 1 initial attempt + 2 retries
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception(_should_retry),
        reraise=True,
    ):
        with attempt:
            response = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                response_format={"type": "json_object"},
                timeout=60,
            )
            return response.choices[0].message.content
