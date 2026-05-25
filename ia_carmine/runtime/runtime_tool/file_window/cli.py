"""Read a bounded window from a file-backed runtime artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ia_carmine._shared.file_backed_transport import (
    MAX_FILE_WINDOW_CHARS,
    artifact_ref,
    is_allowed_runtime_artifact_path,
    read_text_window_bytes,
    resolve_path,
)


def render_markdown(report: dict[str, object]) -> str:
    return "\n".join(
        [
            "# Runtime Artifact File Window",
            "",
            f"- Passed: `{report.get('passed')}`",
            f"- Path: `{report.get('path')}`",
            f"- Offset: `{report.get('offset')}`",
            f"- Limit: `{report.get('limit')}`",
            f"- Next offset: `{report.get('next_offset')}`",
            f"- EOF: `{report.get('eof')}`",
            "",
            "## Errors",
            "",
            *[f"- {item}" for item in report.get("errors", [])],
        ]
    ).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--path", default="")
    parser.add_argument("--ref-id", default="")
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--limit", type=int, default=16000)
    parser.add_argument("--startup-manifest", default="")
    parser.add_argument("--strict-startup-refs", action="store_true")
    parser.add_argument("--request-args-file", default="")
    parser.add_argument("--output", default="output/validation/runtime_file_window.json")
    parser.add_argument("--markdown-output", default="output/validation/runtime_file_window.md")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    request_args = _read_request_args(repo_root, args.request_args_file)
    argument_normalized_from = (
        request_args.get("argument_normalized_from")
        if isinstance(request_args.get("argument_normalized_from"), dict)
        else {}
    )
    ref_id = str(args.ref_id or request_args.get("ref_id") or "").strip()
    raw_path = str(args.path or request_args.get("path") or "").strip()
    startup_manifest = str(args.startup_manifest or request_args.get("startup_manifest") or "").strip()
    source_broker_request_id = str(request_args.get("source_broker_request_id") or "").strip()
    source_report_ref = str(request_args.get("source_report_ref") or "").strip()
    strict_startup_refs = bool(
        args.strict_startup_refs or _truthy(request_args.get("strict_startup_refs"))
    )
    startup_refs = _startup_file_window_refs(
        repo_root,
        startup_manifest,
        source_broker_request_id=source_broker_request_id,
        source_report_ref=source_report_ref,
    )
    if ref_id and not raw_path:
        raw_path = startup_refs["by_ref_id"].get(ref_id, "")
        argument_normalized_from = dict(argument_normalized_from)
        argument_normalized_from["ref_id"] = "path"
    target = resolve_path(repo_root, raw_path) if raw_path else repo_root
    errors: list[str] = []
    text = ""
    offset = max(0, int(args.offset))
    limit = int(args.limit)
    next_offset = offset
    eof = True
    path_allowed = bool(raw_path and is_allowed_runtime_artifact_path(repo_root, raw_path))
    startup_ref_allowed = _ref_or_path_in_startup_refs(
        repo_root, ref_id, raw_path, startup_refs
    )
    if not raw_path:
        errors.append("runtime_file_window_path_or_ref_id_required")
        search_error = startup_refs.get("search_ref_error") if isinstance(startup_refs, dict) else ""
        if strict_startup_refs and search_error:
            errors.append(str(search_error))
    elif strict_startup_refs and not startup_ref_allowed:
        errors.append("runtime_file_window_path_not_in_startup_refs")
        search_error = startup_refs.get("search_ref_error") if isinstance(startup_refs, dict) else ""
        if search_error:
            errors.append(str(search_error))
    elif not path_allowed:
        errors.append("runtime_file_window_path_outside_repo_root")
    elif limit <= 0:
        errors.append("runtime_file_window_limit_must_be_positive")
    elif limit > MAX_FILE_WINDOW_CHARS:
        errors.append(f"runtime_file_window_limit_exceeds_max:{MAX_FILE_WINDOW_CHARS}")
    elif not target.is_file():
        errors.append(f"file not found: {args.path}")
    else:
        text, next_offset, eof = read_text_window_bytes(target, offset=offset, limit=limit)
    ref = (
        artifact_ref(target, repo_root, kind="runtime_file_window_source", required=True)
        if path_allowed
        else {
            "ref_id": "rejected_runtime_file_window_source",
            "path": raw_path,
            "kind": "runtime_file_window_source",
            "required": True,
            "producer": "runtime_file_window",
            "source": "rejected_outside_repo_root",
            "content_type": "",
            "exists": False,
            "bytes": 0,
            "sha256": "",
        }
    )
    report = {
        "schema_version": 1,
        "kind": "runtime_file_window",
        "repo_root": str(repo_root),
        "passed": not errors,
        "path": ref.get("path"),
        "requested_path": raw_path,
        "ref_id": ref_id,
        "startup_manifest": startup_manifest,
        "source_broker_request_id": source_broker_request_id,
        "source_report_ref": source_report_ref,
        "strict_startup_refs": strict_startup_refs,
        "startup_ref_allowed": startup_ref_allowed,
        "argument_normalized_from": argument_normalized_from,
        "source_ref": ref,
        "offset": offset,
        "offset_units": "bytes",
        "limit": limit,
        "max_limit": MAX_FILE_WINDOW_CHARS,
        "next_offset": next_offset,
        "eof": eof,
        "text": text,
        "text_chars": len(text),
        "errors": errors,
        "warnings": [],
        "source_writes_performed": False,
        "patch_application_performed": False,
        "provider_execution_performed": False,
        "git_write_performed": False,
    }
    output = resolve_path(repo_root, args.output)
    markdown = resolve_path(repo_root, args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "output": str(output)}, indent=2))
    return 0 if report["passed"] else 2


def _read_request_args(repo_root: Path, value: str) -> dict[str, object]:
    if not str(value or "").strip():
        return {}
    path = resolve_path(repo_root, value)
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _truthy(value: object) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "y", "on"}


def _startup_file_window_refs(
    repo_root: Path,
    startup_manifest: str,
    *,
    source_broker_request_id: str = "",
    source_report_ref: str = "",
) -> dict[str, object]:
    by_ref_id: dict[str, str] = {}
    by_path: dict[str, str] = {}
    search_ref_error = ""
    if not startup_manifest:
        return {"by_ref_id": by_ref_id, "by_path": by_path, "search_ref_error": search_ref_error}
    path = resolve_path(repo_root, startup_manifest)
    try:
        manifest = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        manifest = {}
    if _is_search_report(manifest):
        search_ref_error = _search_report_binding_error(
            repo_root,
            path,
            manifest,
            source_broker_request_id=source_broker_request_id,
            source_report_ref=source_report_ref,
        )
        if not search_ref_error:
            _collect_search_window_refs(repo_root, manifest, by_ref_id)
    else:
        _collect_startup_refs(repo_root, manifest, by_ref_id, by_path)
    return {"by_ref_id": by_ref_id, "by_path": by_path, "search_ref_error": search_ref_error}


def _is_search_report(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    kind = str(value.get("kind") or "")
    return kind in {
        "repo_search_rg",
        "repo_search_git_grep",
        "repo_find_fd",
        "repo_json_query_jq",
    }


def _search_report_binding_error(
    repo_root: Path,
    manifest_path: Path,
    manifest: dict[str, object],
    *,
    source_broker_request_id: str,
    source_report_ref: str,
) -> str:
    manifest_request_id = str(
        manifest.get("source_broker_request_id")
        or manifest.get("broker_request_id")
        or manifest.get("request_id")
        or ""
    ).strip()
    producer = str(manifest.get("producer") or "").strip()
    broker_authorized = manifest.get("broker_authorized") is True
    if (
        not manifest_request_id
        or not source_broker_request_id
        or not source_report_ref
        or not producer
        or not broker_authorized
    ):
        return "runtime_file_window_search_manifest_not_broker_authorized"
    if manifest_request_id != source_broker_request_id:
        return "runtime_file_window_search_ref_invalid_broker_request"
    expected = _repo_relative(repo_root, source_report_ref)
    actual = _repo_relative(repo_root, str(manifest_path))
    if expected != actual:
        return "runtime_file_window_search_ref_invalid_source_report_ref"
    embedded_ref = str(
        manifest.get("source_report_ref") or manifest.get("tool_report_ref") or ""
    ).strip()
    if embedded_ref and _repo_relative(repo_root, embedded_ref) != actual:
        return "runtime_file_window_search_ref_invalid_source_report_ref"
    return ""


def _collect_search_window_refs(
    repo_root: Path,
    manifest: dict[str, object],
    by_ref_id: dict[str, str],
) -> None:
    refs = manifest.get("runtime_file_window_authorized_refs")
    refs = refs if isinstance(refs, list) else []
    for item in refs:
        if not isinstance(item, dict):
            continue
        if str(item.get("kind") or "") != "runtime_file_window_search_ref":
            continue
        ref_id = str(item.get("ref_id") or "").strip()
        raw_path = str(item.get("path") or "").strip()
        item_request_id = str(item.get("source_broker_request_id") or "").strip()
        manifest_request_id = str(
            manifest.get("source_broker_request_id")
            or manifest.get("broker_request_id")
            or manifest.get("request_id")
            or ""
        ).strip()
        if not item_request_id or not manifest_request_id or item_request_id != manifest_request_id:
            continue
        if ref_id and raw_path:
            by_ref_id.setdefault(ref_id, raw_path)


def _collect_startup_refs(
    repo_root: Path,
    value: object,
    by_ref_id: dict[str, str],
    by_path: dict[str, str],
    key_hint: str = "",
) -> None:
    if isinstance(value, dict):
        raw_path = str(value.get("path") or "").strip()
        ref_id = str(value.get("ref_id") or key_hint or "").strip()
        if raw_path:
            _add_startup_ref_path(repo_root, raw_path, by_path)
            if ref_id:
                by_ref_id.setdefault(ref_id, raw_path)
        for key, item in value.items():
            if key in {"path", "ref_id"}:
                continue
            _collect_startup_refs(repo_root, item, by_ref_id, by_path, str(key))
        return
    if isinstance(value, list):
        for item in value:
            _collect_startup_refs(repo_root, item, by_ref_id, by_path, key_hint)
        return
    if isinstance(value, str) and _looks_like_repo_path(value):
        _add_startup_ref_path(repo_root, value, by_path)
        if key_hint:
            by_ref_id.setdefault(key_hint, value)


def _looks_like_repo_path(value: str) -> bool:
    text = value.replace("\\", "/").strip()
    return bool(
        text
        and not text.startswith(("http://", "https://"))
        and ("/" in text or text.endswith((".json", ".md", ".py", ".txt", ".toml", ".yaml", ".yml")))
    )


def _add_startup_ref_path(repo_root: Path, raw_path: str, by_path: dict[str, str]) -> None:
    normalized = _repo_relative(repo_root, raw_path)
    if normalized:
        by_path.setdefault(normalized, raw_path)


def _ref_or_path_in_startup_refs(
    repo_root: Path,
    ref_id: str,
    raw_path: str,
    startup_refs: dict[str, object],
) -> bool:
    if not raw_path:
        return False
    by_ref_id = (
        startup_refs.get("by_ref_id")
        if isinstance(startup_refs.get("by_ref_id"), dict)
        else {}
    )
    if ref_id:
        ref_path = str(by_ref_id.get(ref_id) or "")
        return bool(ref_path and _repo_relative(repo_root, ref_path) == _repo_relative(repo_root, raw_path))
    by_path = startup_refs.get("by_path") if isinstance(startup_refs.get("by_path"), dict) else {}
    return _repo_relative(repo_root, raw_path) in by_path


def _repo_relative(repo_root: Path, raw_path: str) -> str:
    try:
        path = Path(str(raw_path))
        if not path.is_absolute():
            path = repo_root / path
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except Exception:
        return str(raw_path or "").replace("\\", "/").lstrip("./")


if __name__ == "__main__":
    raise SystemExit(main())
