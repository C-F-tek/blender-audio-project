from __future__ import annotations

from .capsules import json_capsules, text_capsules
from .cli import main
from .core import (
    DEFAULT_MAX_CAPSULE_CHARS,
    DEFAULT_MAX_PACKET_CHARS,
    capsule,
    compact,
    keywords,
    now_iso,
    read_json,
    read_text,
    rel,
    sha,
    slugify,
)
from .discovery import build_capsules, discover
from .packet import build_packet, score, write_md

__all__ = [
    "DEFAULT_MAX_CAPSULE_CHARS",
    "DEFAULT_MAX_PACKET_CHARS",
    "build_capsules",
    "build_packet",
    "capsule",
    "compact",
    "discover",
    "json_capsules",
    "keywords",
    "main",
    "now_iso",
    "read_json",
    "read_text",
    "rel",
    "score",
    "sha",
    "slugify",
    "text_capsules",
    "write_md",
]
