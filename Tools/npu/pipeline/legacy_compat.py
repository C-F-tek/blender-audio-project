from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

JsonReader = Callable[[str | Path], dict[str, Any]]
OptionalJsonReader = Callable[[str | Path | None], dict[str, Any]]
JsonWriter = Callable[[str | Path, dict[str, Any]], None]
TextReader = Callable[[str | Path], str]


def compare_json_readers(
    path: str | Path, legacy_reader: JsonReader, new_reader: JsonReader
) -> dict[str, Any]:
    """Compare two JSON object readers on the same path without side effects."""

    legacy_value = legacy_reader(path)
    new_value = new_reader(path)
    return {
        "ok": legacy_value == new_value,
        "legacy_type": type(legacy_value).__name__,
        "new_type": type(new_value).__name__,
        "legacy_keys": sorted(legacy_value.keys()) if isinstance(legacy_value, dict) else [],
        "new_keys": sorted(new_value.keys()) if isinstance(new_value, dict) else [],
    }


def compare_optional_json_readers(
    path: str | Path | None,
    legacy_reader: OptionalJsonReader,
    new_reader: OptionalJsonReader,
) -> dict[str, Any]:
    """Compare two optional JSON object readers on the same path."""

    legacy_value = legacy_reader(path)
    new_value = new_reader(path)
    return {
        "ok": legacy_value == new_value,
        "legacy_type": type(legacy_value).__name__,
        "new_type": type(new_value).__name__,
    }


def compare_text_readers(
    path: str | Path, legacy_reader: TextReader, new_reader: TextReader
) -> dict[str, Any]:
    """Compare two text readers on the same path."""

    legacy_value = legacy_reader(path)
    new_value = new_reader(path)
    return {
        "ok": legacy_value == new_value,
        "legacy_chars": len(legacy_value),
        "new_chars": len(new_value),
    }
