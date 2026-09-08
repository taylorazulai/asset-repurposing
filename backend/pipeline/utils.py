import json


def parse_json_response(text: str) -> dict:
    """Parse a JSON string returned by an LLM configured with response_format=json_object."""
    return json.loads(text)
