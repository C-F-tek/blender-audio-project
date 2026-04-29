from __future__ import annotations

import json
import re
from typing import Any


class JsonParseError(ValueError):
    """Raised when a model response cannot be parsed as JSON."""


def strip_markdown_fence(text: str) -> str:
    stripped = text.strip()
    if not stripped.startswith("```"):
        return stripped
    lines = stripped.splitlines()
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()


def extract_json_candidate(text: str) -> str:
    """Extract the largest likely JSON object/array from a model response."""
    stripped = strip_markdown_fence(text)
    if not stripped:
        return stripped
    if stripped[0] in "[{" and stripped[-1] in "]}":
        return stripped

    starts = [pos for pos in [stripped.find("{"), stripped.find("[")] if pos >= 0]
    if not starts:
        return stripped
    start = min(starts)
    end_obj = stripped.rfind("}")
    end_arr = stripped.rfind("]")
    end = max(end_obj, end_arr)
    if end <= start:
        return stripped[start:]
    return stripped[start : end + 1].strip()


def repair_common_json(text: str) -> str:
    repaired = text.strip()
    repaired = repaired.replace("\ufeff", "")
    repaired = re.sub(r",\s*([}\]])", r"\1", repaired)
    # Remove JavaScript-style comments only when they are on their own line.
    repaired = re.sub(r"(?m)^\s*//.*$", "", repaired)
    return repaired.strip()


def parse_model_json(text: str, *, allow_repair: bool = True) -> Any:
    """Parse JSON returned by an LLM, tolerating fences and minor syntax noise."""
    candidate = extract_json_candidate(text)
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as first_error:
        if not allow_repair:
            raise JsonParseError(str(first_error)) from first_error
        repaired = repair_common_json(candidate)
        try:
            return json.loads(repaired)
        except json.JSONDecodeError as second_error:
            raise JsonParseError(f"Unable to parse model JSON: {second_error}") from second_error


def parse_model_json_object(text: str, *, allow_repair: bool = True) -> dict[str, Any]:
    parsed = parse_model_json(text, allow_repair=allow_repair)
    if not isinstance(parsed, dict):
        raise JsonParseError(f"Expected JSON object, got {type(parsed).__name__}")
    return parsed
