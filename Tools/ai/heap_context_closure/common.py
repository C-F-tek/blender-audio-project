"""Common IO, path, process, and revision-context helpers."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_REQUEST = (
    "Esegui heap runtime con proposal chunks multi-parte. "
    "Non comprimere tutto nella sola risposta GPU1: salva blocchi par1/par2/par3, "
    "fai review GPU0 dei blocchi non operativi, fai micro-audit NPU se disponibile, "
    "usa debug lab e chiudi con composer finale su file persistenti."
)

REQUIRED_COMPOSER_JSON = "heap_final_proposal_composer.json"
REVISION_CONTEXT_MARKER = "EXTERNAL HEAP REVISION CONTEXT FROM PREVIOUS RUN"


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def resolve_repo_root(value: str) -> Path:
    return Path(value).resolve()


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def resolve_project_python(repo_root: Path, explicit: str = "") -> str:
    if explicit:
        return str(Path(explicit).resolve())
    for candidate in (
        repo_root / ".venv" / "Scripts" / "python.exe",
        repo_root / "venv" / "Scripts" / "python.exe",
        repo_root / ".venv314" / "Scripts" / "python.exe",
    ):
        if candidate.exists():
            return str(candidate.resolve())
    return sys.executable


def resolve_repo_file(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve(strict=False)


def load_operator_request(repo_root: Path, inline_request: str, request_file: str) -> tuple[str, str]:
    if not request_file:
        return inline_request, ""
    path = resolve_repo_file(repo_root, request_file)
    try:
        return path.read_text(encoding="utf-8-sig"), str(path)
    except Exception as exc:
        raise SystemExit(f"cannot read --request-file {path}: {type(exc).__name__}: {exc}") from exc


def run_command(
    command: list[str],
    repo_root: Path,
    timeout_seconds: int | None = None,
) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            cwd=repo_root,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "returncode": -9,
            "stdout_tail": (exc.stdout or "")[-4000:] if isinstance(exc.stdout, str) else "",
            "stderr_tail": (
                ((exc.stderr or "")[-4000:] if isinstance(exc.stderr, str) else "")
                + f"\nTimeoutExpired after {timeout_seconds}s"
            ).strip(),
            "passed": False,
            "timeout": True,
        }
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout_tail": (completed.stdout or "")[-4000:],
        "stderr_tail": (completed.stderr or "")[-4000:],
        "passed": completed.returncode == 0,
        "timeout": False,
    }


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_documents_run_manifest(
    *,
    documents_root: str,
    repo_root: Path,
    run_dir: Path,
    stamp: str,
    request_file: str,
    status: str,
) -> str:
    if not documents_root:
        return ""
    documents_dir = Path(documents_root).expanduser().resolve(strict=False)
    documents_dir.mkdir(parents=True, exist_ok=True)
    manifest = documents_dir / "RUN_IN_PROGRESS.json"
    payload = {
        "schema_version": 1,
        "kind": "operator_documents_run_manifest",
        "stamp": stamp,
        "status": status,
        "repo_root": str(repo_root),
        "run_dir": str(run_dir),
        "request_file": request_file,
        "code_product_expected": str(documents_dir / "CODE_PRODUCT_FULL_PATCH.md"),
        "final_readable_expected": str(documents_dir / "FINAL_READABLE_PRODUCT.md"),
    }
    write_json(manifest, payload)
    return str(manifest)


def is_complete_heap_run_dir(path: Path) -> bool:
    return (
        path.is_dir()
        and path.name.startswith("heap_context_closure_")
        and (path / REQUIRED_COMPOSER_JSON).exists()
    )


def latest_revision_context(repo_root: Path) -> tuple[Path | None, dict[str, Any], str]:
    validation_dir = repo_root / "output" / "validation"
    if not validation_dir.exists():
        return None, {}, "none"
    candidates = sorted(
        [
            run_dir / "external_heap_revision_context.json"
            for run_dir in validation_dir.iterdir()
            if is_complete_heap_run_dir(run_dir)
            and (run_dir / "external_heap_revision_context.json").exists()
        ],
        key=lambda path: path.stat().st_mtime if path.exists() else 0,
        reverse=True,
    )
    if not candidates:
        return None, {}, "none"
    path = candidates[0].resolve()
    return path, load_json(path), "latest_complete_heap_context_closure_with_composer_json"


def resolve_revision_context(repo_root: Path, value: str) -> tuple[Path | None, dict[str, Any], str]:
    mode = str(value or "auto_latest").strip()
    if not mode or mode.lower() in {"off", "none", "false", "0"}:
        return None, {}, "off"
    if mode == "auto_latest":
        return latest_revision_context(repo_root)
    path = Path(mode)
    if not path.is_absolute():
        path = repo_root / path
    path = path.resolve()
    return path, load_json(path), "explicit_revision_context"
