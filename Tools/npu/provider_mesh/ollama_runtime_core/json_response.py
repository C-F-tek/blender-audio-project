"""Model JSON response parsing compatibility helpers."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from Tools.ai._shared.model_json import (
        ModelJsonParseError,
        parse_model_json_object,
        strip_markdown_json_fence,
    )
except ImportError:
    repo_root = Path(__file__).resolve().parents[3]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from Tools.ai._shared.model_json import (  # type: ignore
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
