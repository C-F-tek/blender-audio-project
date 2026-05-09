#!/usr/bin/env python3
"""Anchor and text-operation helpers for controlled patch bundles."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TextChange:
    changed: bool
    text: str
    reason: str = ""


def require_absent(text: str, marker: str) -> bool:
    return marker not in text


def insert_before_marker(text: str, marker: str, content: str, *, idempotency_marker: str = "") -> TextChange:
    if idempotency_marker and idempotency_marker in text:
        return TextChange(False, text, "idempotency marker already present")
    index = text.find(marker)
    if index < 0:
        raise ValueError(f"marker not found: {marker}")
    replacement = content.strip("\n") + "\n"
    return TextChange(True, text[:index] + replacement + text[index:], "insert_before_marker")


def insert_after_marker(text: str, marker: str, content: str, *, idempotency_marker: str = "") -> TextChange:
    if idempotency_marker and idempotency_marker in text:
        return TextChange(False, text, "idempotency marker already present")
    index = text.find(marker)
    if index < 0:
        raise ValueError(f"marker not found: {marker}")
    insert_at = index + len(marker)
    replacement = "\n" + content.strip("\n")
    return TextChange(True, text[:insert_at] + replacement + text[insert_at:], "insert_after_marker")


def replace_once(text: str, old: str, new: str) -> TextChange:
    count = text.count(old)
    if count != 1:
        raise ValueError(f"replace_once expected 1 match, found {count}")
    return TextChange(True, text.replace(old, new, 1), "replace_once")


def append_once(text: str, content: str, *, idempotency_marker: str = "") -> TextChange:
    if idempotency_marker and idempotency_marker in text:
        return TextChange(False, text, "idempotency marker already present")
    return TextChange(True, text.rstrip("\n") + "\n\n" + content.strip("\n") + "\n", "append_once")
