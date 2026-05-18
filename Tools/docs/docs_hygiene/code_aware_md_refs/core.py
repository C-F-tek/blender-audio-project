from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any

EXCLUDE_DIR_NAMES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    "node_modules",
    "output",
    "renders",
}
EXCLUDE_PREFIXES = (
    "docs/LOCAL_VALIDATION_EVIDENCE/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
    "Tools/npu/npu_blender_manual_chunks/",
)
ACTIVE_MD_ROOTS = (
    "README.md",
    "AGENTS.md",
    "CHATGPT.md",
    "WORKFLOW.md",
    "FULL_RUN_UNICA_TUTTO_SU_TUTTO.md",
    "docs/",
    "CHATGPT/",
    "Tools/",
)
PATH_RE = re.compile(
    r"(?P<path>(?:\.\\|\./)?(?:[A-Za-z0-9_.-]+[\\/])+[A-Za-z0-9_.-]+\.(?:md|py|ps1|json|csv|txt|yaml|yml))"
)
INLINE_PATH_RE = re.compile(r"`([^`]+\.(?:md|py|ps1|json|csv|txt|yaml|yml))`")
PY_COMMAND_RE = re.compile(
    r"(?:^|\s)(?:python|py|python3|&\s*\$PythonExe)\s+(?P<script>[^\s`'\"]+\.py)",
    re.IGNORECASE,
)
PS_COMMAND_RE = re.compile(
    r"(?:powershell(?:\.exe)?[^\n]*-File\s+|^\s*&\s+|^\s*)"
    r"(?P<script>(?:\.\\|\./|Tools[\\/])[^\s`'\"]+\.ps1)",
    re.IGNORECASE | re.MULTILINE,
)
LONG_FLAG_RE = re.compile(r"(?<![\w-])--[A-Za-z0-9][A-Za-z0-9_-]*")
PS_FLAG_RE = re.compile(r"(?<![\w-])-[A-Z][A-Za-z0-9_]*")


def normalize_ref(raw: str) -> str:
    value = raw.strip().strip("'\"`.,:;()[]{}<>").replace("\\", "/")
    command_path_match = re.search(
        r"(?P<path>(?:\.\/|\.\\|\/)?(?:[A-Za-z0-9_.-]+[\\\/])+[A-Za-z0-9_.-]+\.(?:md|py|ps1|json|csv|txt|yaml|yml))",
        value,
    )
    if command_path_match:
        value = command_path_match.group("path").replace("\\", "/")

    root_like_prefixes = (
        "/AGENTS.md",
        "/CHATGPT.md",
        "/README.md",
        "/WORKFLOW.md",
        "/FULL_RUN_UNICA_TUTTO_SU_TUTTO.md",
        "/CHATGPT/",
        "/Tools/",
        "/docs/",
        "/Scripting/",
        "/indexAI/",
        "/output/",
        "/renders/",
    )
    if any(value == prefix[1:] or value.startswith(prefix) for prefix in root_like_prefixes):
        value = value.lstrip("/")

    while value.startswith("./"):
        value = value[2:]
    while value.startswith("../"):
        value = value[3:]
    while value.startswith(".//"):
        value = value[3:]
    return value


def is_excluded_rel(rel: str) -> bool:
    rel = rel.replace("\\", "/")
    if any(rel.startswith(prefix) for prefix in EXCLUDE_PREFIXES):
        return True
    return any(part in EXCLUDE_DIR_NAMES for part in rel.split("/"))


def is_active_md(rel: str) -> bool:
    return rel.endswith(".md") and any(
        rel == root or rel.startswith(root) for root in ACTIVE_MD_ROOTS
    )


def build_file_index(paths: list[str]) -> dict[str, Any]:
    return {
        "paths": set(paths),
        "basename_counts": Counter(Path(rel).name for rel in paths),
    }


def reference_exists(repo: Path, source_path: Path, ref: str, file_index: dict[str, Any]) -> bool:
    check_ref = ref.lstrip("/") if ref.startswith("/") else ref

    if (repo / check_ref).exists() or (source_path.parent / check_ref).exists():
        return True
    if "/" not in check_ref and "\\" not in check_ref:
        return file_index["basename_counts"].get(Path(check_ref).name, 0) == 1
    return False


def collect_md_refs(text: str) -> set[str]:
    refs = {normalize_ref(m.group("path")) for m in PATH_RE.finditer(text)}
    refs.update(normalize_ref(m.group(1)) for m in INLINE_PATH_RE.finditer(text))
    return {ref for ref in refs if ref and not ref.startswith("http")}


def collect_doc_command_refs(
    text: str,
) -> tuple[list[tuple[str, list[str]]], list[tuple[str, list[str]]]]:
    py_refs: list[tuple[str, list[str]]] = []
    ps_refs: list[tuple[str, list[str]]] = []
    for line in text.splitlines():
        for match in PY_COMMAND_RE.finditer(line):
            py_refs.append((normalize_ref(match.group("script")), sorted(set(LONG_FLAG_RE.findall(line)))))
        for match in PS_COMMAND_RE.finditer(line):
            ps_refs.append((normalize_ref(match.group("script")), sorted(set(PS_FLAG_RE.findall(line)))))
    return py_refs, ps_refs


def classify_missing_ref(ref: str, source_doc: str = "") -> tuple[str, str]:
    source = source_doc.replace("\\", "/")
    target = ref.replace("\\", "/")
    lower_source = source.lower()
    lower_target = target.lower()

    if target.startswith("output/") or "/output/" in target:
        return "low", "evidence-only"
    if target.startswith("docs/LOCAL_VALIDATION_EVIDENCE/"):
        return "low", "evidence-only"
    if source.startswith("CHATGPT/") or "next-chat" in lower_source or "handoff" in lower_source:
        return "low", "chatgpt-advisory-or-handoff"
    if target.startswith("patches/") or "patch_bundles/" in lower_target:
        return "low", "patch-bundle-template"
    if "*" in target or "<" in target or ">" in target:
        return "low", "placeholder-template"
    if "/some_" in lower_target or target.startswith("some_") or "your_app_" in lower_target:
        return "low", "placeholder-template"
    if "check_example_contract.py" in lower_target:
        return "low", "placeholder-template"

    historical_sources = (
        "macro-local-validation-prototype",
        "open-pr-triage",
        "pr109-prelocal",
        "local_runs_testing_and_evidence",
        "full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles",
    )
    if any(token in lower_source for token in historical_sources):
        return "medium", "historical-or-handoff"
    if "next-chat" in lower_target or "handoff" in lower_target:
        return "medium", "historical-or-handoff"
    if lower_target.startswith("users/") or "/users/" in lower_target:
        return "low", "local-absolute-path"
    if "/" not in target and "\\" not in target and target.endswith((".py", ".ps1")):
        return "medium", "ambiguous-basename-reference"
    if target.endswith((".py", ".ps1")):
        return "high", "active-current"
    if target.endswith(".md"):
        return "medium", "stale-or-historical"
    return "low", "unknown"
