"""File-backed transport helpers for IA-Carmine runtime payloads.

HTTP/API calls coordinate work. Large context, prompts, logs and tool payloads
live on disk as addressable artifacts with checksum metadata.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

INLINE_TEXT_MAX_CHARS = 16000
MAX_FILE_WINDOW_CHARS = 16000
TEXT_EVIDENCE_TAIL_CHARS = 4000
SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9_.-]+")


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def safe_name(value: Any, fallback: str = "artifact") -> str:
    text = SAFE_NAME_RE.sub("_", str(value or fallback)).strip("._-")
    return text[:96] or fallback


def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve(strict=False)


def read_text_windows_safe(path: str | Path) -> str:
    raw = Path(path).read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("utf-8", raw, 0, len(raw), "unable to decode file safely")


def read_json_windows_safe(path: str | Path) -> dict[str, Any]:
    data = json.loads(read_text_windows_safe(path))
    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object")
    return data


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_sha256(text: str) -> str:
    return hashlib.sha256(str(text or "").encode("utf-8")).hexdigest()


def artifact_ref(
    path: str | Path,
    repo_root: Path,
    *,
    kind: str,
    ref_id: str = "",
    required: bool = True,
    producer: str = "",
    source: str = "",
    content_type: str = "",
) -> dict[str, Any]:
    artifact_path = resolve_path(repo_root, path)
    exists = artifact_path.is_file()
    return {
        "ref_id": ref_id or safe_name(artifact_path.stem),
        "path": repo_rel(artifact_path, repo_root),
        "kind": kind,
        "required": required,
        "producer": producer,
        "source": source or producer or "unknown",
        "content_type": content_type or _content_type(artifact_path),
        "exists": exists,
        "bytes": artifact_path.stat().st_size if exists else 0,
        "sha256": file_sha256(artifact_path) if exists else "",
    }


def write_text_artifact(
    repo_root: Path,
    output_dir: Path,
    *,
    name: str,
    text: str,
    kind: str,
    producer: str,
    suffix: str = ".txt",
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{safe_name(name)}{suffix}"
    path.write_text(text, encoding="utf-8")
    return artifact_ref(path, repo_root, kind=kind, producer=producer, ref_id=safe_name(name))


def write_large_text_evidence(
    repo_root: Path,
    output_dir: Path,
    *,
    name: str,
    text: str,
    kind: str,
    producer: str,
    suffix: str = ".txt",
    tail_chars: int = TEXT_EVIDENCE_TAIL_CHARS,
) -> dict[str, Any]:
    """Write full text to disk and return JSON-safe evidence metadata.

    Coordination JSON must carry refs, hashes and bounded tails. Full prompt,
    provider response and request bodies remain available through the artifact.
    """
    full_text = str(text or "")
    tail_limit = max(0, int(tail_chars))
    ref = (
        write_text_artifact(
            repo_root,
            output_dir,
            name=name,
            text=full_text,
            kind=kind,
            producer=producer,
            suffix=suffix,
        )
        if full_text
        else {}
    )
    return {
        "ref": ref,
        "chars": len(full_text),
        "sha256": text_sha256(full_text),
        "tail": full_text[-tail_limit:] if tail_limit and full_text else "",
        "tail_chars": min(len(full_text), tail_limit),
        "full_text_in_json": False,
    }


def prefixed_text_evidence_fields(prefix: str, evidence: dict[str, Any]) -> dict[str, Any]:
    """Return JSON coordination fields for a file-backed text artifact."""
    return {
        f"{prefix}_ref": evidence.get("ref") or {},
        f"{prefix}_chars": evidence.get("chars", 0),
        f"{prefix}_sha256": evidence.get("sha256", ""),
        f"{prefix}_tail": evidence.get("tail", ""),
        f"{prefix}_tail_chars": evidence.get("tail_chars", 0),
        f"{prefix}_full_text_in_json": False,
    }


def write_text_evidence_fields(
    repo_root: Path,
    output_dir: Path,
    *,
    prefix: str,
    name: str,
    text: str,
    kind: str,
    producer: str,
    suffix: str = ".txt",
) -> dict[str, Any]:
    """Materialize text and return strict ref/tail fields for runtime JSON."""
    evidence = write_large_text_evidence(
        repo_root,
        output_dir,
        name=name,
        text=text,
        kind=kind,
        producer=producer,
        suffix=suffix,
    )
    fields = prefixed_text_evidence_fields(prefix, evidence)
    fields[f"{prefix}_transport"] = "artifact_ref" if evidence.get("ref") else "empty"
    return fields


def compact_text_fields(
    repo_root: Path,
    output_dir: Path,
    payload: dict[str, Any],
    prefixes: list[str] | tuple[str, ...],
    *,
    name: str,
    producer: str,
    kind_prefix: str = "",
    suffix: str = ".txt",
) -> dict[str, Any]:
    """Replace full text fields with stable ref/hash/tail transport fields.

    This helper is deliberately materialize-first: if a prefix has inline full
    text, the full value is written to disk before the inline field is removed.
    Existing refs are preserved and verified enough to fill stable metadata.
    Tails are kept only as bounded previews/fallbacks.
    """
    compact = dict(payload)
    output_dir.mkdir(parents=True, exist_ok=True)
    for prefix in prefixes:
        inline = compact.pop(prefix, None)
        if isinstance(inline, str) and inline:
            compact.update(
                write_text_evidence_fields(
                    repo_root,
                    output_dir,
                    prefix=prefix,
                    name=f"{name}_{prefix}",
                    text=inline,
                    kind=f"{kind_prefix or name}_{prefix}",
                    producer=producer,
                    suffix=suffix,
                )
            )
            continue

        ref = compact.get(f"{prefix}_ref")
        if isinstance(ref, dict) and str(ref.get("path") or "").strip():
            evidence = read_text_evidence(repo_root, compact, prefix, require_full=True)
            text = str(evidence.get("text") or "")
            if evidence.get("used_ref") and text:
                compact[f"{prefix}_chars"] = len(text)
                compact[f"{prefix}_sha256"] = text_sha256(text)
                tail = text[-TEXT_EVIDENCE_TAIL_CHARS:]
                compact[f"{prefix}_tail"] = tail
                compact[f"{prefix}_tail_chars"] = len(tail)
                compact[f"{prefix}_full_text_in_json"] = False
                compact[f"{prefix}_transport"] = "artifact_ref"
            else:
                compact[f"{prefix}_full_text_in_json"] = False
                compact[f"{prefix}_transport"] = "artifact_ref_unreadable"
                if evidence.get("errors"):
                    compact[f"{prefix}_transport_errors"] = evidence.get("errors")
            continue

        tail = str(compact.get(f"{prefix}_tail") or "")
        compact[f"{prefix}_chars"] = int(compact.get(f"{prefix}_chars") or len(tail))
        compact[f"{prefix}_sha256"] = str(compact.get(f"{prefix}_sha256") or "")
        compact[f"{prefix}_tail"] = tail[-TEXT_EVIDENCE_TAIL_CHARS:] if tail else ""
        compact[f"{prefix}_tail_chars"] = min(len(tail), TEXT_EVIDENCE_TAIL_CHARS)
        compact[f"{prefix}_full_text_in_json"] = False
        compact[f"{prefix}_transport"] = "tail_fallback" if tail else "empty"
    return compact


def text_from_ref_or_tail(repo_root: Path, payload: dict[str, Any], prefix: str) -> str:
    """Load full text from ref, falling back to legacy inline text then tail."""
    return str(read_text_evidence(repo_root, payload, prefix).get("text") or "")


def read_text_evidence(
    repo_root: Path | str | None,
    payload: dict[str, Any],
    prefix: str,
    *,
    require_full: bool = False,
) -> dict[str, Any]:
    """Read ref-backed text evidence with typed fallback metadata.

    Full runtime decisions should use the ref path when present. Tail text is a
    diagnostic fallback only and is flagged so gates can avoid treating it as
    verified full evidence.
    """
    errors: list[str] = []
    warnings: list[str] = []
    root = Path(repo_root or payload.get("repo_root") or ".").resolve(strict=False)
    ref = payload.get(f"{prefix}_ref")
    if isinstance(ref, dict):
        ref_path = str(ref.get("path") or "").strip()
        if ref_path:
            try:
                target = resolve_path(root, ref_path)
                text = read_text_windows_safe(target)
                expected_sha = str(
                    payload.get(f"{prefix}_sha256") or ref.get("sha256") or ""
                ).strip()
                actual_sha = text_sha256(text)
                if expected_sha and actual_sha != expected_sha:
                    errors.append(f"{prefix}_ref_sha256_mismatch:{ref_path}")
                else:
                    return {
                        "text": text,
                        "source": "ref",
                        "ref_path": ref_path,
                        "used_ref": True,
                        "used_legacy_inline": False,
                        "used_tail_fallback": False,
                        "sha256_valid": bool(expected_sha),
                        "full_verified": bool(expected_sha),
                        "errors": errors,
                        "warnings": warnings,
                    }
            except Exception as exc:  # noqa: BLE001 - diagnostic helper.
                errors.append(f"{prefix}_ref_read_failed:{ref_path}:{type(exc).__name__}: {exc}")
        elif require_full:
            errors.append(f"{prefix}_ref_path_missing")
    elif require_full:
        errors.append(f"{prefix}_ref_missing")
    inline = payload.get(prefix)
    if isinstance(inline, str) and inline:
        warnings.append(f"{prefix}_legacy_inline_fallback")
        return {
            "text": inline,
            "source": "legacy_inline",
            "ref_path": "",
            "used_ref": False,
            "used_legacy_inline": True,
            "used_tail_fallback": False,
            "sha256_valid": text_sha256(inline) == str(payload.get(f"{prefix}_sha256") or ""),
            "full_verified": False,
            "errors": errors,
            "warnings": warnings,
        }
    tail = str(payload.get(f"{prefix}_tail") or "")
    if tail:
        warnings.append(f"{prefix}_tail_fallback")
    elif require_full:
        errors.append(f"{prefix}_full_text_unavailable")
    return {
        "text": tail,
        "source": "tail" if tail else "",
        "ref_path": "",
        "used_ref": False,
        "used_legacy_inline": False,
        "used_tail_fallback": bool(tail),
        "sha256_valid": False,
        "full_verified": False,
        "errors": errors,
        "warnings": warnings,
    }


def report_text(
    repo_root: Path | str | None,
    report: dict[str, Any],
    prefixes: list[str] | tuple[str, ...] = ("response_text",),
    *,
    require_full: bool = False,
) -> dict[str, Any]:
    """Read text from a provider/report payload using the canonical order.

    For every prefix the order is ref, legacy inline, then tail. The first
    prefix producing text wins, with fallback metadata preserved for gates.
    """
    collected_errors: list[str] = []
    collected_warnings: list[str] = []
    for prefix in prefixes:
        evidence = read_text_evidence(
            repo_root,
            report,
            prefix,
            require_full=require_full,
        )
        collected_errors.extend(str(item) for item in evidence.get("errors") or [])
        collected_warnings.extend(str(item) for item in evidence.get("warnings") or [])
        if str(evidence.get("text") or ""):
            result = dict(evidence)
            result["prefix"] = prefix
            result["errors"] = collected_errors
            result["warnings"] = collected_warnings
            return result
    return {
        "text": "",
        "prefix": "",
        "source": "",
        "ref_path": "",
        "used_ref": False,
        "used_legacy_inline": False,
        "used_tail_fallback": False,
        "sha256_valid": False,
        "full_verified": False,
        "errors": collected_errors,
        "warnings": collected_warnings,
    }


def write_json_artifact(
    repo_root: Path,
    output_dir: Path,
    *,
    name: str,
    payload: Any,
    kind: str,
    producer: str,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{safe_name(name)}.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return artifact_ref(path, repo_root, kind=kind, producer=producer, ref_id=safe_name(name))


def write_transport_manifest(
    repo_root: Path,
    output_path: Path,
    *,
    job_id: str,
    run_dir: Path,
    refs: list[dict[str, Any]],
    kind: str = "ia_carmine_runtime_payload_manifest",
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema_version": 1,
        "kind": kind,
        "job_id": job_id,
        "run_dir": repo_rel(run_dir, repo_root),
        "repo_root": str(repo_root),
        "created_at": now_iso(),
        "transport_policy": {
            "principle": "http_coordinates_filesystem_transports_mass",
            "http_body": "job_id_payload_file_and_small_control_metadata_only",
            "filesystem": "authoritative_mass_transport",
            "manifest": "stable_structure_and_checksums",
            "report": "execution_verifiability",
        },
        "artifact_refs": refs,
        "artifact_ref_count": len(refs),
    }
    if extra:
        payload.update(extra)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return payload


def should_materialize_inline(value: Any, *, max_chars: int = INLINE_TEXT_MAX_CHARS) -> bool:
    if isinstance(value, str):
        return len(value) > max_chars
    if isinstance(value, (dict, list)):
        try:
            return len(json.dumps(value, ensure_ascii=False, default=str)) > max_chars
        except TypeError:
            return True
    return False


def is_path_inside(child: Path, parent: Path) -> bool:
    try:
        child.resolve(strict=False).relative_to(parent.resolve(strict=False))
        return True
    except ValueError:
        return False


def is_allowed_runtime_artifact_path(repo_root: Path, value: str | Path) -> bool:
    """Return whether a provider-visible file window may read this path.

    The runtime file-window reader is allowed to inspect repository-owned files
    and run artifacts under the repository. Absolute paths outside the checkout
    are rejected instead of becoming a generic local file read primitive.
    """
    return is_path_inside(resolve_path(repo_root, value), repo_root)


def read_text_window_bytes(path: str | Path, *, offset: int, limit: int) -> tuple[str, int, bool]:
    """Read a bounded byte window without loading the whole artifact."""
    target = Path(path)
    start = max(0, int(offset))
    size = target.stat().st_size
    if start >= size:
        return "", start, True
    max_bytes = max(1, min(int(limit), MAX_FILE_WINDOW_CHARS))
    with target.open("rb") as handle:
        handle.seek(start)
        raw = handle.read(max_bytes)
    next_offset = start + len(raw)
    eof = next_offset >= size
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return raw.decode(encoding), next_offset, eof
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace"), next_offset, eof


def validate_runtime_payload_manifest(repo_root: Path, manifest_path: str | Path) -> dict[str, Any]:
    """Validate file-backed manifest refs, checksums and chunk order."""
    errors: list[str] = []
    warnings: list[str] = []
    manifest_file = resolve_path(repo_root, manifest_path)
    try:
        manifest = read_json_windows_safe(manifest_file)
    except Exception as exc:  # noqa: BLE001 - report-only validator helper.
        return {
            "passed": False,
            "errors": [f"manifest_unreadable:{type(exc).__name__}:{exc}"],
            "warnings": [],
        }

    if manifest.get("schema_version") != 1:
        errors.append("manifest_schema_version_not_1")
    if manifest.get("kind") != "ia_carmine_runtime_payload_manifest":
        errors.append("manifest_kind_not_ia_carmine_runtime_payload_manifest")
    job_id = str(manifest.get("job_id") or "").strip()
    if not job_id:
        errors.append("manifest_job_id_missing")
    run_dir_value = str(manifest.get("run_dir") or "").strip()
    if not run_dir_value:
        errors.append("manifest_run_dir_missing")
        run_dir = manifest_file.parent
    else:
        run_dir = resolve_path(repo_root, run_dir_value)
        if not is_path_inside(run_dir, repo_root):
            errors.append("manifest_run_dir_outside_repo")

    refs = manifest.get("artifact_refs")
    if not isinstance(refs, list) or not refs:
        errors.append("manifest_artifact_refs_missing")
        refs = []
    for index, ref in enumerate(refs, start=1):
        if not isinstance(ref, dict):
            errors.append(f"artifact_ref_{index}_not_object")
            continue
        rel_path = str(ref.get("path") or "").strip()
        kind = str(ref.get("kind") or "").strip()
        source = str(ref.get("source") or "").strip()
        expected_bytes = int(ref.get("bytes") or 0)
        expected_sha = str(ref.get("sha256") or "").strip()
        if not rel_path:
            errors.append(f"artifact_ref_{index}_path_missing")
            continue
        raw_path = Path(rel_path)
        if raw_path.is_absolute():
            errors.append(f"artifact_ref_{rel_path}_absolute_path_forbidden")
        if not kind:
            errors.append(f"artifact_ref_{rel_path}_kind_missing")
        if not source or source == "unknown":
            errors.append(f"artifact_ref_{rel_path}_source_missing")
        artifact_path = resolve_path(repo_root, rel_path)
        if not is_path_inside(artifact_path, repo_root):
            errors.append(f"artifact_ref_{rel_path}_outside_repo")
        elif run_dir_value and not is_path_inside(artifact_path, run_dir):
            errors.append(f"artifact_ref_{rel_path}_outside_run_dir")
        if not artifact_path.is_file():
            errors.append(f"artifact_ref_{rel_path}_missing")
            continue
        actual_bytes = artifact_path.stat().st_size
        actual_sha = file_sha256(artifact_path)
        if actual_bytes != expected_bytes:
            errors.append(f"artifact_ref_{rel_path}_bytes_mismatch")
        if actual_sha != expected_sha:
            errors.append(f"artifact_ref_{rel_path}_sha256_mismatch")

    read_order = manifest.get("read_order")
    if read_order is not None and not isinstance(read_order, list):
        errors.append("manifest_read_order_not_list")

    chunk_refs = [
        ref for ref in refs
        if isinstance(ref, dict) and str(ref.get("kind") or "") in {"chunks_manifest", "semantic_chunk_manifest"}
    ]
    for ref in chunk_refs:
        chunk_path = resolve_path(repo_root, str(ref.get("path") or ""))
        try:
            chunk_manifest = read_json_windows_safe(chunk_path)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"chunk_manifest_unreadable:{ref.get('path')}:{type(exc).__name__}:{exc}")
            continue
        chunks = chunk_manifest.get("chunks")
        chunk_order = chunk_manifest.get("read_order")
        if not isinstance(chunks, list) or not chunks:
            errors.append(f"chunk_manifest_{ref.get('path')}_chunks_missing")
            continue
        ids = [str(item.get("chunk_id") or "") for item in chunks if isinstance(item, dict)]
        if not isinstance(chunk_order, list) or [str(item) for item in chunk_order] != ids:
            errors.append(f"chunk_manifest_{ref.get('path')}_read_order_mismatch")
        for chunk in chunks:
            if not isinstance(chunk, dict):
                errors.append(f"chunk_manifest_{ref.get('path')}_chunk_not_object")
                continue
            for key in ("chunk_id", "kind", "path", "source", "bytes", "sha256"):
                if chunk.get(key) in (None, ""):
                    errors.append(f"chunk_{chunk.get('chunk_id') or '?'}_{key}_missing")
            chunk_rel_path = str(chunk.get("path") or "").strip()
            if not chunk_rel_path:
                continue
            if Path(chunk_rel_path).is_absolute():
                errors.append(f"chunk_{chunk.get('chunk_id') or '?'}_absolute_path_forbidden")
            chunk_target = resolve_path(repo_root, chunk_rel_path)
            if not is_path_inside(chunk_target, repo_root):
                errors.append(f"chunk_{chunk.get('chunk_id') or '?'}_outside_repo")
                continue
            if run_dir_value and not is_path_inside(chunk_target, run_dir):
                errors.append(f"chunk_{chunk.get('chunk_id') or '?'}_outside_run_dir")
            if not chunk_target.is_file():
                errors.append(f"chunk_{chunk.get('chunk_id') or '?'}_missing")
                continue
            expected_chunk_bytes = int(chunk.get("bytes") or 0)
            expected_chunk_sha = str(chunk.get("sha256") or "").strip()
            if chunk_target.stat().st_size != expected_chunk_bytes:
                errors.append(f"chunk_{chunk.get('chunk_id') or '?'}_bytes_mismatch")
            if file_sha256(chunk_target) != expected_chunk_sha:
                errors.append(f"chunk_{chunk.get('chunk_id') or '?'}_sha256_mismatch")

    return {"passed": not errors, "errors": errors, "warnings": warnings}


def _content_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return "application/json"
    if suffix in {".md", ".markdown"}:
        return "text/markdown"
    if suffix in {".txt", ".log"}:
        return "text/plain"
    if suffix in {".patch", ".diff"}:
        return "text/x-diff"
    return "application/octet-stream"
