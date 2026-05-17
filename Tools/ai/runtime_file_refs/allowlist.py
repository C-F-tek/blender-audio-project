"""Allowlist and classification rules for runtime file references."""

from __future__ import annotations

import subprocess
from functools import lru_cache
from pathlib import Path

from .models import RuntimeRefKind, RuntimeRefStatus

VALIDATION_PREFIXES = ("Tools/validation/",)
OUTPUT_PREFIXES = ("output/", "docs/LOCAL_VALIDATION_EVIDENCE/")
DENY_PREFIXES = (
    ".git/",
    ".venv/",
    ".claude/",
    "indexAI/",
    "output/",
    "renders/",
)
DENY_SUFFIXES = (
    ".bak",
    ".bak2",
    ".db",
    ".log",
    ".pyc",
    ".pyd",
    ".pyo",
    ".sqlite",
    ".sqlite-shm",
    ".sqlite-wal",
    ".tmp",
    ".zip",
)
RUNTIME_DENY_TOKENS = ("blender", "ffmpeg", "ollama", "openvino", "provider_probe")

SOURCE_SUFFIXES = (".py", ".ps1", ".json", ".yml", ".yaml", ".toml")
DOC_SUFFIXES = (".md", ".txt")
ASSET_SUFFIXES = (
    ".blend",
    ".bmp",
    ".csv",
    ".exr",
    ".flac",
    ".gif",
    ".hdr",
    ".jpeg",
    ".jpg",
    ".lnk",
    ".mov",
    ".mp3",
    ".mp4",
    ".png",
    ".svg",
    ".tsv",
    ".wav",
    ".webp",
)


def normalize_ref_text(raw: str) -> str:
    text = str(raw or "").strip().strip("`'\"")
    text = text.replace("\\", "/").lstrip("./")
    while "//" in text:
        text = text.replace("//", "/")
    return text


def repo_relative(repo_root: Path, raw: str) -> tuple[str, str]:
    text = normalize_ref_text(raw)
    if not text:
        return "", "path is empty"
    path = Path(text)
    if not path.is_absolute():
        path = repo_root / path
    resolved_root = repo_root.resolve(strict=False)
    resolved_path = path.resolve(strict=False)
    try:
        return resolved_path.relative_to(resolved_root).as_posix(), ""
    except ValueError:
        return text, "path escapes repository root"


def classify_kind(rel: str) -> RuntimeRefKind:
    lower = rel.lower()
    suffix = Path(rel).suffix.lower()
    if lower.startswith(OUTPUT_PREFIXES):
        return RuntimeRefKind.OUTPUT_ARTIFACT
    if suffix in ASSET_SUFFIXES:
        return RuntimeRefKind.ASSET
    if lower.startswith(("config/", ".github/")):
        return RuntimeRefKind.CONFIG
    if lower.startswith(("docs/", "chatgpt/")):
        return RuntimeRefKind.DOCS
    if lower.startswith("tools/validation/"):
        return RuntimeRefKind.TEST
    if suffix in SOURCE_SUFFIXES:
        return RuntimeRefKind.SOURCE
    if suffix in DOC_SUFFIXES:
        return RuntimeRefKind.DOCS
    return RuntimeRefKind.UNKNOWN


@lru_cache(maxsize=4096)
def git_ignored(repo_root: str, rel: str) -> tuple[bool, str]:
    root = Path(repo_root)
    if not (root / ".git").exists():
        return False, "git metadata missing; filesystem fallback"
    completed = subprocess.run(
        ["git", "check-ignore", "-q", "--", rel],
        cwd=root,
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if completed.returncode == 0:
        return True, "path is ignored by git"
    return False, "path is not git-ignored"


def classify_status(repo_root: Path, rel: str, *, validation_ref: bool = False) -> tuple[RuntimeRefStatus, str]:
    lower = rel.lower()
    if not rel:
        return RuntimeRefStatus.MISSING, "path is empty"
    if lower.startswith(tuple(prefix.lower() for prefix in OUTPUT_PREFIXES)):
        return RuntimeRefStatus.OUTPUT_ONLY, "output artifact refs are not source targets"
    if lower.startswith(tuple(prefix.lower() for prefix in DENY_PREFIXES)):
        return RuntimeRefStatus.REJECTED_NON_ALLOWLISTED, "path prefix is forbidden"
    if lower.endswith(DENY_SUFFIXES):
        return RuntimeRefStatus.UNSAFE, "runtime database refs are not patch targets"
    if validation_ref:
        if not lower.endswith(".py") or not lower.startswith(tuple(prefix.lower() for prefix in VALIDATION_PREFIXES)):
            return RuntimeRefStatus.REJECTED_NON_ALLOWLISTED, "validation refs must be Python scripts under Tools/validation"
        if any(token in lower for token in RUNTIME_DENY_TOKENS):
            return RuntimeRefStatus.UNSAFE, "validation script targets provider/application runtime"
        return RuntimeRefStatus.VALIDATION_ONLY, "validation command refs are not target files"
    path = repo_root / rel
    if not path.exists():
        return RuntimeRefStatus.MISSING, "path does not exist"
    if not path.is_file():
        return RuntimeRefStatus.REJECTED_NON_ALLOWLISTED, "path is not a file"
    ignored, reason = git_ignored(str(repo_root.resolve(strict=False)), rel)
    if ignored:
        return RuntimeRefStatus.REJECTED_NON_ALLOWLISTED, reason
    return RuntimeRefStatus.VERIFIED, "resolved against local filesystem"
