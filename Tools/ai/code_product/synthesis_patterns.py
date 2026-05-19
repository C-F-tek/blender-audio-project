"""Content-driven patch synthesis patterns for validated runtime targets."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PatchTransform:
    updated_text: str
    reason: str
    pattern_id: str


def runtime_file_ref_import_block(existing_text: str) -> str:
    sys_import = "" if re.search(r"^import sys$", existing_text, re.MULTILINE) else "import sys\n"
    return sys_import + (
        "from typing import Any\n\n"
        "try:\n"
        "    from Tools.ai.runtime_tool.file_refs import RuntimeConsumer, RuntimeFileRefResolver, RuntimeRefProvenance\n"
        "except ImportError:\n"
        "    repo_root_for_import = Path(__file__).resolve().parents[2]\n"
        "    if str(repo_root_for_import) not in sys.path:\n"
        "        sys.path.insert(0, str(repo_root_for_import))\n"
        "    from Tools.ai.runtime_tool.file_refs import RuntimeConsumer, RuntimeFileRefResolver, RuntimeRefProvenance  # type: ignore\n"
    )


def insert_runtime_file_ref_import(text: str) -> str:
    if "RuntimeFileRefResolver" in text:
        return text
    anchor = "from typing import Any\n"
    if anchor not in text:
        return text
    return text.replace(anchor, runtime_file_ref_import_block(text), 1)


def normalize_repo_path_candidate(rel_path: str, text: str) -> PatchTransform | None:
    if "RuntimeFileRefResolver" in text or "def normalize_repo_path" not in text:
        return None
    pattern = re.compile(
        r"def normalize_repo_path\((?P<params>[^)]*)\) -> (?P<returns>[^\n]+):\n"
        r"(?:    .*\n)+?(?=\n\ndef |\n\nclass |\n\n[A-Z_]+ = |\Z)",
        re.MULTILINE,
    )
    match = pattern.search(text)
    if not match or "from typing import Any\n" not in text:
        return None
    params = match.group("params")
    returns = match.group("returns")
    parts = [part.strip() for part in params.split(",")]
    raw_name = "raw"
    repo_root_name = "repo_root"
    if len(parts) == 1:
        raw_name = parts[0].split(":", 1)[0].split("=", 1)[0].strip() or raw_name
        repo_root_name = "REPO_ROOT"
    elif len(parts) >= 2:
        raw_name = parts[1].split(":", 1)[0].split("=", 1)[0].strip() or raw_name
        repo_root_name = parts[0].split(":", 1)[0].split("=", 1)[0].strip() or repo_root_name
    returns_tuple = "tuple[" in returns or "tuple[" in text[match.start() : match.end()]
    returns_optional_error = "None" in returns or returns_tuple
    if not returns_tuple and repo_root_name == raw_name:
        repo_root_name = "REPO_ROOT"
    success_value = "None" if returns_optional_error else '""'
    if returns_tuple:
        replacement = (
            f"def normalize_repo_path({params}) -> {returns}:\n"
            f"    resolver = RuntimeFileRefResolver({repo_root_name})\n"
            "    ref = resolver.resolve(\n"
            f"        {raw_name},\n"
            "        provenance=RuntimeRefProvenance.TOOL_REQUEST,\n"
            "        consumers=(RuntimeConsumer.LAB, RuntimeConsumer.MATRIX),\n"
            "    )\n"
            "    if not ref.patchable:\n"
            f"        return ref.repo_relative or str({raw_name} or \"\"), ref.reason\n"
            f"    return ref.repo_relative, {success_value}\n"
        )
    else:
        replacement = (
            f"def normalize_repo_path({params}) -> {returns}:\n"
            f"    resolver = RuntimeFileRefResolver({repo_root_name})\n"
            "    ref = resolver.resolve(\n"
            f"        {raw_name},\n"
            "        provenance=RuntimeRefProvenance.TOOL_REQUEST,\n"
            "        consumers=(RuntimeConsumer.BROKER_TOOL,),\n"
            "    )\n"
            f"    fallback = str({raw_name} or \"\").strip().replace(\"\\\\\\\\\", \"/\").lstrip(\"./\")\n"
            "    return ref.repo_relative or fallback\n"
        )
    updated = insert_runtime_file_ref_import(text)
    updated = pattern.sub(replacement, updated, count=1)
    return PatchTransform(
        updated_text=updated,
        reason="replace duplicated textual path normalization with RuntimeFileRefResolver",
        pattern_id="runtime_file_ref_normalize_repo_path",
    )


def candidate_transforms(rel_path: str, text: str, operator_request: str = "") -> list[PatchTransform]:
    transforms: list[PatchTransform] = []
    for builder in (normalize_repo_path_candidate,):
        result = builder(rel_path, text)
        if result and result.updated_text != text:
            transforms.append(result)
    return transforms


def module_line_count() -> int:
    return len(Path(__file__).read_text(encoding="utf-8-sig").splitlines())
