#!/usr/bin/env python3
"""Filesystem primitives for controlled patch bundles."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class LoadedText:
    path: Path
    text_lf: str
    newline: str
    had_bom: bool


def normalize_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def detect_newline(raw: bytes) -> str:
    return "\r\n" if b"\r\n" in raw else "\n"


def load_text(path: Path) -> LoadedText:
    raw = path.read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    return LoadedText(
        path=path,
        text_lf=normalize_lf(text),
        newline=detect_newline(raw),
        had_bom=had_bom,
    )


def write_text_preserved(loaded: LoadedText, text_lf: str) -> None:
    normalized = text_lf.rstrip("\n") + "\n"
    text = normalized.replace("\n", loaded.newline)
    payload = text.encode("utf-8-sig" if loaded.had_bom else "utf-8")
    loaded.path.write_bytes(payload)


def backup_file(repo_root: Path, target: Path, *, namespace: str = "patchkit_backups") -> Path:
    backup_dir = repo_root / "output" / "validation" / namespace
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = backup_dir / f"{target.name}.{stamp}.bak"
    shutil.copy2(target, backup)
    return backup


def repo_path(repo_root: Path, raw: str) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else repo_root / path


def rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()
