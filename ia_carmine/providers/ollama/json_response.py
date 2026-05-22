"""Model JSON response parsing helpers for Ollama provider outputs."""

from __future__ import annotations

import json

from ia_carmine._shared.model_json import (
    ModelJsonParseError,
    parse_model_json_object,
    strip_markdown_json_fence,
)


def strip_json_fence(text: str) -> str:
    return strip_markdown_json_fence(text)


def parse_json_response(text: str) -> dict:
    try:
        return parse_model_json_object(text)
    except ModelJsonParseError as exc:
        raise json.JSONDecodeError(str(exc), text, 0) from exc
