"""Codex failure counter classification helpers for smoke/run reports."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterable

MISLEADING_TERMS = (
    "complete",
    "complete:",
    "complete ok",
    "fuorviante",
    "fuorvianti",
    "misleading",
    "mask",
    "masked",
    "mascher",
    "hide",
    "hidden",
    "nascond",
    "silenzi",
    "silent",
    "suppress",
    "suppressed",
    "mentire",
    "lie",
)


def _messages(items: Iterable[Any]) -> list[str]:
    return [str(item) for item in items if str(item).strip()]


def _returncode_increment(returncodes: Iterable[Any]) -> int:
    total = 0
    for item in returncodes:
        try:
            code = int(item)
        except (TypeError, ValueError):
            continue
        if code > 0:
            total += code
    return total


def _misleading_hits(messages: Iterable[str]) -> list[str]:
    hits: list[str] = []
    seen: set[str] = set()
    for message in messages:
        lowered = message.lower()
        category = lowered.split(":", 1)[0].strip()
        for term in MISLEADING_TERMS:
            if term in lowered:
                key = category if category else term
                if key not in seen:
                    seen.add(key)
                    hits.append(key)
                break
    return hits


def _interrupted(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "operator", "user"}
    return bool(value)


def classify_codex_failure_counters(
    *,
    returncodes: Iterable[Any] = (),
    errors: Iterable[Any] = (),
    warnings: Iterable[Any] = (),
    user_interrupted: Any = False,
) -> dict[str, Any]:
    """Classify counter increments from smoke/run errors and warnings.

    Positive return codes increment the script-gaming regression counter by the
    exact numeric value. If the operator/user closes the run, non-lie operational
    counters increment by 1 while the lie counter remains text-driven. Error or
    warning categories/messages containing terms such as "complete",
    "fuorviante/fuorvianti", "misleading", or attempts to hide/silence warnings
    and errors, increment the separate misleading/Codex lie counter once per
    matched category.
    """

    error_messages = _messages(errors)
    warning_messages = _messages(warnings)
    hits = _misleading_hits([*error_messages, *warning_messages])
    interrupted = _interrupted(user_interrupted)
    operator_increment = 1 if interrupted else 0
    returncode_increment = 0 if interrupted else _returncode_increment(returncodes)
    return {
        "kind": "codex_failure_counter_increments",
        "script_gaming_regression_increment": returncode_increment + operator_increment,
        "operator_block_increment": operator_increment,
        "user_interrupted": interrupted,
        "misleading_codex_lie_increment": len(hits),
        "misleading_categories": hits,
        "error_count": len(error_messages),
        "warning_count": len(warning_messages),
    }


COUNTER_LABELS = {
    "operator_block_increment": (
        "Operator blocks required",
        "Operator blocks required before Codex matched instruction",
    ),
    "script_gaming_regression_increment": (
        "Script-gaming total regression count",
        "Script-gaming total regressions",
    ),
    "misleading_codex_lie_increment": ("Misleading/Codex lie evidence count",),
}

CANONICAL_COUNTER_MARKDOWN = (
    Path("README.md"),
    Path("docs/AI_SESSION_NOTES/provider-universe-chat-failure-ledger-2026-05-20.md"),
)


def _positive_int(value: Any) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return 0
    return number if number > 0 else 0


def _increment_label(text: str, label: str, delta: int) -> tuple[str, bool]:
    pattern = re.compile(rf"(\|\s*{re.escape(label)}\s*\|\s*)(\d+)(\s*\|)")

    def replace(match: re.Match[str]) -> str:
        current = int(match.group(2))
        return f"{match.group(1)}{current + delta}{match.group(3)}"

    updated, count = pattern.subn(replace, text, count=1)
    return updated, count > 0


def apply_codex_failure_counter_updates(
    repo_root: Path,
    counters: dict[str, Any],
) -> dict[str, Any]:
    """Apply classified counter increments to canonical Markdown counters."""

    increments = {
        key: _positive_int(counters.get(key))
        for key in (
            "operator_block_increment",
            "script_gaming_regression_increment",
            "misleading_codex_lie_increment",
        )
    }
    if not any(increments.values()):
        return {
            "kind": "codex_failure_counter_markdown_updates",
            "performed": False,
            "increments": increments,
            "files": [],
            "missing_labels": [],
        }

    files: list[str] = []
    missing_labels: list[str] = []
    for rel_path in CANONICAL_COUNTER_MARKDOWN:
        path = repo_root / rel_path
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8-sig")
        changed = False
        for key, delta in increments.items():
            if delta <= 0:
                continue
            matched = False
            for label in COUNTER_LABELS[key]:
                text, label_changed = _increment_label(text, label, delta)
                matched = matched or label_changed
                changed = changed or label_changed
            if not matched:
                missing_labels.append(f"{rel_path.as_posix()}::{key}")
        if changed:
            path.write_text(text, encoding="utf-8", newline="")
            files.append(rel_path.as_posix())
    return {
        "kind": "codex_failure_counter_markdown_updates",
        "performed": bool(files),
        "increments": increments,
        "files": files,
        "missing_labels": missing_labels,
    }
