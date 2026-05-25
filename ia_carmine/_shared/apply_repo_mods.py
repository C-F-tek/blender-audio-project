#!/usr/bin/env python3
"""
Safe repository patch runner.

Scopo:
- applicare modifiche piccole e verificabili usando un file JSON;
- evitare la riscrittura completa di file grandi;
- rimuovere automaticamente un eventuale BOM UTF-8 iniziale;
- fare backup opzionale dei file modificati;
- stampare numero righe prima/dopo e riepilogo modifiche.

Uso base:
    python -m Tools.repo_patch_runner apply_repo_mods --spec patch_spec.json --dry-run
    python -m Tools.repo_patch_runner apply_repo_mods --spec patch_spec.json --write

Formato JSON minimo:
{
  "version": 1,
  "description": "Fix example",
  "operations": [
    {
      "path": "relative/path/file.py",
      "replacements": [
        {
          "type": "exact",
          "old": "testo vecchio",
          "new": "testo nuovo",
          "count": 1
        }
      ],
      "require_contains_after": ["testo nuovo"],
      "forbid_contains_after": ["testo vecchio"]
    }
  ]
}
"""

from __future__ import annotations

import datetime as _dt
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class PatchError(RuntimeError):
    """Errore controllato durante l'applicazione della patch."""


@dataclass
class FileReport:
    path: Path
    changed: bool
    before_lines: int
    after_lines: int
    replacements_applied: int
    bom_removed: bool


def _count_lines(text: str) -> int:
    if text == "":
        return 0
    return len(text.splitlines())


def _detect_newline(text: str) -> str:
    crlf = text.count("\r\n")
    lf = text.count("\n") - crlf
    return "\r\n" if crlf > lf else "\n"

def _read_text_utf8(path: Path) -> tuple[str, bool]:
    raw = path.read_bytes()
    bom_removed = raw.startswith(b"\xef\xbb\xbf")
    if bom_removed:
        raw = raw[3:]
    try:
        return raw.decode("utf-8"), bom_removed
    except UnicodeDecodeError as exc:
        raise PatchError(f"{path}: file non leggibile come UTF-8: {exc}") from exc


def _write_text_utf8_no_bom(path: Path, text: str) -> None:
    if text.startswith("\ufeff"):
        text = text.lstrip("\ufeff")
    path.write_bytes(text.encode("utf-8"))

def _resolve_repo_root(cli_root: str | None) -> Path:
    if cli_root:
        root = Path(cli_root).expanduser().resolve()
    else:
        root = Path.cwd().resolve()

    if not (root / ".git").exists():
        raise PatchError(f"Root non valida: {root} non contiene .git")
    return root


def _safe_join(root: Path, relative_path: str) -> Path:
    if not relative_path or not isinstance(relative_path, str):
        raise PatchError("Percorso file mancante o non valido")

    rel = Path(relative_path)
    if rel.is_absolute():
        raise PatchError(f"Percorso assoluto non ammesso nello spec: {relative_path}")

    full = (root / rel).resolve()
    try:
        full.relative_to(root)
    except ValueError as exc:
        raise PatchError(f"Percorso fuori dalla root repo non ammesso: {relative_path}") from exc
    return full


def _require_strings(text: str, values: list[str], label: str, path: Path) -> None:
    for value in values:
        if value not in text:
            raise PatchError(f"{path}: validazione fallita: manca {label}: {value!r}")


def _forbid_strings(text: str, values: list[str], label: str, path: Path) -> None:
    for value in values:
        if value in text:
            raise PatchError(f"{path}: validazione fallita: trovato {label}: {value!r}")


def _regex_flags(names: list[str] | None) -> int:
    flags = 0
    for name in names or []:
        key = str(name).upper()
        if key == "MULTILINE":
            flags |= re.MULTILINE
        elif key == "DOTALL":
            flags |= re.DOTALL
        elif key == "IGNORECASE":
            flags |= re.IGNORECASE
        else:
            raise PatchError(f"Flag regex non supportato: {name}")
    return flags


def _apply_exact(text: str, replacement: dict[str, Any], path: Path) -> tuple[str, int]:
    old = replacement.get("old")
    new = replacement.get("new")
    count = int(replacement.get("count", 1))

    if not isinstance(old, str) or not isinstance(new, str):
        raise PatchError(f"{path}: replacement exact richiede old/new stringa")
    if count < 1:
        raise PatchError(f"{path}: count deve essere >= 1")

    found = text.count(old)
    if found < count:
        raise PatchError(
            f"{path}: exact replacement non applicabile: trovate {found}, richieste {count}"
        )

    return text.replace(old, new, count), count


def _apply_regex(text: str, replacement: dict[str, Any], path: Path) -> tuple[str, int]:
    pattern = replacement.get("pattern")
    new = replacement.get("new")
    count = int(replacement.get("count", 1))
    flags = _regex_flags(replacement.get("flags"))

    if not isinstance(pattern, str) or not isinstance(new, str):
        raise PatchError(f"{path}: replacement regex richiede pattern/new stringa")
    if count < 1:
        raise PatchError(f"{path}: count deve essere >= 1")

    compiled = re.compile(pattern, flags)
    matches = compiled.findall(text)
    if len(matches) < count:
        raise PatchError(
            f"{path}: regex replacement non applicabile: match {len(matches)}, richiesti {count}"
        )

    new_text, applied = compiled.subn(new, text, count=count)
    if applied != count:
        raise PatchError(f"{path}: regex replacement applicate {applied}, attese {count}")

    return new_text, applied


def _apply_insert_after(text: str, replacement: dict[str, Any], path: Path) -> tuple[str, int]:
    anchor = replacement.get("anchor")
    insert = replacement.get("insert")
    count = int(replacement.get("count", 1))

    if not isinstance(anchor, str) or not isinstance(insert, str):
        raise PatchError(f"{path}: insert_after richiede anchor/insert stringa")
    if count < 1:
        raise PatchError(f"{path}: count deve essere >= 1")

    found = text.count(anchor)
    if found < count:
        raise PatchError(
            f"{path}: anchor non trovato abbastanza volte: trovate {found}, richieste {count}"
        )

    result = text
    for _ in range(count):
        idx = result.find(anchor)
        if idx < 0:
            raise PatchError(f"{path}: anchor non trovato durante insert_after")
        insert_at = idx + len(anchor)
        result = result[:insert_at] + insert + result[insert_at:]

    return result, count


def _apply_insert_before(text: str, replacement: dict[str, Any], path: Path) -> tuple[str, int]:
    anchor = replacement.get("anchor")
    insert = replacement.get("insert")
    count = int(replacement.get("count", 1))

    if not isinstance(anchor, str) or not isinstance(insert, str):
        raise PatchError(f"{path}: insert_before richiede anchor/insert stringa")
    if count < 1:
        raise PatchError(f"{path}: count deve essere >= 1")

    found = text.count(anchor)
    if found < count:
        raise PatchError(
            f"{path}: anchor non trovato abbastanza volte: trovate {found}, richieste {count}"
        )

    result = text
    offset = 0
    for _ in range(count):
        idx = result.find(anchor, offset)
        if idx < 0:
            raise PatchError(f"{path}: anchor non trovato durante insert_before")
        result = result[:idx] + insert + result[idx:]
        offset = idx + len(insert) + len(anchor)

    return result, count


def _apply_replacements(text: str, op: dict[str, Any], path: Path) -> tuple[str, int]:
    replacements = op.get("replacements", [])
    if not isinstance(replacements, list):
        raise PatchError(f"{path}: replacements deve essere una lista")

    applied_total = 0
    result = text

    for item in replacements:
        if not isinstance(item, dict):
            raise PatchError(f"{path}: replacement non valido: {item!r}")

        kind = item.get("type", "exact")
        if kind == "exact":
            result, applied = _apply_exact(result, item, path)
        elif kind == "regex":
            result, applied = _apply_regex(result, item, path)
        elif kind == "insert_after":
            result, applied = _apply_insert_after(result, item, path)
        elif kind == "insert_before":
            result, applied = _apply_insert_before(result, item, path)
        else:
            raise PatchError(f"{path}: tipo replacement non supportato: {kind}")

        applied_total += applied

    return result, applied_total


def _backup_file(root: Path, path: Path, backup_dir_name: str) -> Path:
    timestamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    rel = path.relative_to(root)
    backup_dir = root / backup_dir_name / timestamp / rel.parent
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / rel.name
    shutil.copy2(path, backup_path)
    return backup_path


def _run_git_diff(root: Path, paths: list[Path]) -> None:
    rel_paths = [str(path.relative_to(root)).replace("\\", "/") for path in paths]
    if not rel_paths:
        return

    try:
        subprocess.run(["git", "diff", "--", *rel_paths], cwd=root, check=False)
    except FileNotFoundError:
        print("[WARN] git non trovato nel PATH: diff saltato", file=sys.stderr)


def apply_spec(
    root: Path, spec: dict[str, Any], *, write: bool, no_backup: bool
) -> list[FileReport]:
    if int(spec.get("version", 1)) != 1:
        raise PatchError("Solo spec version=1 e supportato")

    operations = spec.get("operations")
    if not isinstance(operations, list) or not operations:
        raise PatchError("Lo spec deve contenere operations non vuoto")

    backup_dir_name = str(spec.get("backup_dir", ".repo_patch_backups"))
    reports: list[FileReport] = []

    for op in operations:
        if not isinstance(op, dict):
            raise PatchError(f"Operazione non valida: {op!r}")

        path = _safe_join(root, str(op.get("path", "")))
        if not path.exists():
            raise PatchError(f"File non trovato: {path}")
        if not path.is_file():
            raise PatchError(f"Percorso non file: {path}")

        text, bom_removed = _read_text_utf8(path)
        newline = _detect_newline(text)

        # Normalizza eventuali newlines nei blocchi replacement solo se richiesto.
        normalize_newlines = bool(op.get("normalize_replacement_newlines", True))
        if normalize_newlines:
            for repl in op.get("replacements", []):
                for key in ("old", "new", "anchor", "insert"):
                    if isinstance(repl.get(key), str):
                        repl[key] = repl[key].replace("\r\n", "\n").replace("\n", newline)

        before_lines = _count_lines(text)
        _require_strings(
            text, op.get("require_contains_before", []), "require_contains_before", path
        )
        _forbid_strings(text, op.get("forbid_contains_before", []), "forbid_contains_before", path)

        new_text, replacements_applied = _apply_replacements(text, op, path)

        # Rimuove BOM anche se gia presente nel testo decodificato.
        if new_text.startswith("\ufeff"):
            new_text = new_text.lstrip("\ufeff")
            bom_removed = True

        _require_strings(
            new_text, op.get("require_contains_after", []), "require_contains_after", path
        )
        _forbid_strings(
            new_text, op.get("forbid_contains_after", []), "forbid_contains_after", path
        )

        expected_delta = op.get("expected_line_delta")
        after_lines = _count_lines(new_text)
        if expected_delta is not None:
            delta = after_lines - before_lines
            if delta != int(expected_delta):
                raise PatchError(
                    f"{path}: delta righe inatteso: ottenuto {delta}, atteso {expected_delta}"
                )

        changed = new_text != text
        if changed and write:
            if not no_backup:
                backup_path = _backup_file(root, path, backup_dir_name)
                print(f"[BACKUP] {path.relative_to(root)} -> {backup_path.relative_to(root)}")
            _write_text_utf8_no_bom(path, new_text)

        reports.append(
            FileReport(
                path=path,
                changed=changed,
                before_lines=before_lines,
                after_lines=after_lines,
                replacements_applied=replacements_applied,
                bom_removed=bom_removed,
            )
        )

    return reports


def load_spec(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise PatchError(f"JSON spec non valido: {exc}") from exc

    if not isinstance(data, dict):
        raise PatchError("Lo spec JSON deve essere un oggetto")
    return data
