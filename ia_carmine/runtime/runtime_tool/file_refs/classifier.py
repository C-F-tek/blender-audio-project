"""Extraction helpers for provider and operator file references."""

from __future__ import annotations

import re
from collections.abc import Iterable

FILE_REF_RE = re.compile(
    r"(?P<path>(?:\.\/)?(?:ia_carmine|Tools|tools|docs|CHATGPT|Scripting|scripts|patch_specs|config|examples|assets|\.github|output|indexAI|renders)/[A-Za-z0-9_./() -]+\.(?:py|ps1|md|json|txt|yml|yaml|toml|diff|patch|csv|tsv|svg|png|jpg|jpeg|webp|wav|mp3|mp4))"
)
SECTION_RE = re.compile(r"(?im)^\s*(?P<name>[A-Z_ ]{3,}):\s*(?P<body>.*)$")
HEADING_RE = re.compile(r"(?im)^\s*#{1,6}\s*(?P<name>[A-Z_ ]{3,})(?:\s*$|[:=])")


def unique_ordered(values: Iterable[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        item = str(value or "").strip().strip("`'\"")
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def extract_file_refs(text: str) -> list[str]:
    return unique_ordered(match.group("path") for match in FILE_REF_RE.finditer(str(text or "")))


def _section_blocks(text: str, section_name: str) -> list[str]:
    lines = str(text or "").splitlines()
    wanted = section_name.replace(" ", "_").upper()
    blocks: list[str] = []
    active: list[str] = []
    in_section = False
    for line in lines:
        match = SECTION_RE.match(line)
        heading = HEADING_RE.match(line)
        if match or heading:
            current = (
                (match.group("name") if match else heading.group("name"))
                .replace(" ", "_")
                .upper()
            )
            body = match.group("body") if match else ""
            if in_section and current != wanted:
                blocks.append("\n".join(active))
                active = []
                in_section = False
            if current == wanted:
                in_section = True
                active.append(body)
                continue
        if in_section:
            active.append(line)
    if in_section:
        blocks.append("\n".join(active))
    return blocks


def extract_section_refs(text: str, section_name: str) -> list[str]:
    blocks = _section_blocks(text, section_name)
    refs: list[str] = []
    for block in blocks:
        refs.extend(extract_file_refs(block))
        for line in block.splitlines():
            cleaned = line.strip().lstrip("-*0123456789. ").strip("`'\"")
            if ("/" in cleaned or "\\" in cleaned) and re.match(
                r"^(?:\.\/)?(?:ia_carmine|Tools|tools|docs|CHATGPT|Scripting|scripts|patch_specs|config|examples|assets|\.github|output|indexAI|renders)/",
                cleaned,
            ):
                refs.append(cleaned.split()[0].strip(",;"))
    return unique_ordered(refs)


def extract_target_refs(text: str) -> list[str]:
    return extract_section_refs(text, "TARGET_FILES")


def extract_validation_refs(text: str) -> list[str]:
    refs = extract_section_refs(text, "VALIDATION_COMMANDS")
    refs.extend(
        match.group("path")
        for match in re.finditer(
            r"(?P<path>(?:\.\/)?(?:Tools|tools)/validation/[A-Za-z0-9_./() -]+\.py)",
            str(text or ""),
        )
    )
    return unique_ordered(refs)
