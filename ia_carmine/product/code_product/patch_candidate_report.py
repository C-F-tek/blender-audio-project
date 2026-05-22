"""Patch candidate report semantics shared by broker, matrix and final product."""

from __future__ import annotations

from typing import Any


def passed_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [item for item in candidates if isinstance(item, dict) and item.get("passed") is True]


def failed_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [item for item in candidates if isinstance(item, dict) and item.get("passed") is not True]


def candidate_report_passed(candidates: list[dict[str, Any]]) -> bool:
    return bool(passed_candidates(candidates))


def report_level_errors(candidates: list[dict[str, Any]]) -> list[str]:
    if candidate_report_passed(candidates):
        return []
    errors: list[str] = []
    for item in failed_candidates(candidates):
        for error in item.get("errors") or []:
            text = str(error or "").strip()
            if text:
                errors.append(text)
    return errors


def report_level_warnings(candidates: list[dict[str, Any]]) -> list[str]:
    warnings: list[str] = []
    if failed_candidates(candidates) and candidate_report_passed(candidates):
        warnings.append("some patch candidates failed validation and were kept as rejected evidence")
    return warnings
