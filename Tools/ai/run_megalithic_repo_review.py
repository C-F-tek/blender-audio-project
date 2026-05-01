#!/usr/bin/env python3
"""Run an explicit all-resources repository review.

The megalithic review is an artifact-first helper for IA-Carmine work. It reads
Markdown, code and validation artifacts, compares docs against implementation and
optionally asks live Ollama/GPU for a semantic review.

Default behavior is CPU-only and report-only:

- no provider execution unless --use-ollama is explicitly passed;
- no NPU execution;
- no patch application;
- no source writes except requested report outputs;
- no Blender runtime execution;
- no full analysis JSON edits;
- no SQLite DB commits.

NPU/OpenVINO participates through already-generated metadata, decode diagnostics,
quality-gate reports and knowledge-broker packets. Live NPU execution remains a
separate explicit provider/tool step.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

DEFAULT_OUTPUT_JSON = "output/ai_pipeline/megalithic_repo_review.json"
DEFAULT_OUTPUT_MD = "output/ai_pipeline/megalithic_repo_review.md"
DEFAULT_PROPOSALS_JSON = "output/ai_pipeline/megalithic_repo_review_proposals.json"

DOC_EXTENSIONS = {".md"}
CODE_EXTENSIONS = {".py", ".ps1", ".sh", ".yaml", ".yml", ".json"}
DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "output",
    "renders",
    "indexAI",
}
DEFAULT_REPORTS = (
    "output/validation/docs_contract_drift.json",
    "output/validation/code_contract_drift.json",
    "output/validation/ai_workload_report_quality.json",
    "output/validation/validation_report_contract.json",
    "output/validation/local_ai_resource_lanes.json",
    "output/validation/local_provider_probe.json",
    "output/validation/ai_workload_quality_lane_routing.json",
    "output/validation/npu_decode_quality_remediation.json",
    "output/validation/npu_review_metadata.json",
)
PATH_RE = re.compile(r"(?:[A-Za-z0-9_.-]+/)+(?:[A-Za-z0-9_.-]+)(?:\.[A-Za-z0-9_.-]+)?")
POWERSHELL_FUNC_RE = re.compile(r"(?im)^\s*function\s+([A-Za-z0-9_-]+)\s*(?:\{|$)")
SHELL_FUNC_RE = re.compile(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*\(\)\s*\{")


@dataclass(frozen=True)
class FileRecord:
    path: str
    extension: str
    kind: str
    chars: int
    lines: int
    symbols: tuple[str, ...]


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def split_path_values(items: list[str]) -> list[str]:
    out: list[str] = []
    for item in items:
        for part in str(item).split(","):
            normalized = part.strip().strip("'\"")
            if normalized:
                out.append(normalized.replace("\\", "/"))
    return out


def is_excluded(path: Path, repo_root: Path, *, include_output: bool, include_index: bool) -> bool:
    rel_parts = path.relative_to(repo_root).parts
    excludes = set(DEFAULT_EXCLUDE_DIRS)
    if include_output:
        excludes.discard("output")
    if include_index:
        excludes.discard("indexAI")
    return any(part in excludes for part in rel_parts)


def iter_files(
    repo_root: Path,
    *,
    include_all_docs: bool,
    include_all_code: bool,
    include_output: bool,
    include_index: bool,
    max_files: int,
) -> tuple[list[Path], list[Path]]:
    docs: list[Path] = []
    code: list[Path] = []
    for path in sorted(repo_root.rglob("*")):
        if not path.is_file():
            continue
        if is_excluded(path, repo_root, include_output=include_output, include_index=include_index):
            continue
        suffix = path.suffix.lower()
        rel = path.relative_to(repo_root).as_posix()
        if suffix in DOC_EXTENSIONS and (include_all_docs or rel.startswith(("docs/", "Tools/", "AGENTS", "WORKFLOW"))):
            docs.append(path)
        elif suffix in CODE_EXTENSIONS and (include_all_code or rel.startswith(("Tools/", "Scripting/", "docs/"))):
            code.append(path)
        if max_files > 0 and len(docs) + len(code) >= max_files:
            break
    return docs, code


def read_text(path: Path, max_chars: int = 0) -> tuple[str, bool, str | None]:
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError as exc:
        return "", False, f"{type(exc).__name__}: {exc}"
    truncated = bool(max_chars > 0 and len(text) > max_chars)
    if truncated:
        text = text[:max_chars]
    return text, truncated, None


def python_symbols(text: str) -> tuple[str, ...]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return tuple(sorted(set(re.findall(r"(?m)^\s*(?:def|class)\s+([A-Za-z_][A-Za-z0-9_]*)", text))))
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.append(node.name)
    return tuple(sorted(set(names)))


def extract_symbols(path: Path, text: str) -> tuple[str, ...]:
    suffix = path.suffix.lower()
    if suffix == ".py":
        return python_symbols(text)
    if suffix == ".ps1":
        return tuple(sorted(set(POWERSHELL_FUNC_RE.findall(text))))
    if suffix == ".sh":
        return tuple(sorted(set(SHELL_FUNC_RE.findall(text))))
    return ()


def build_file_records(repo_root: Path, files: Iterable[Path], *, max_chars_per_file: int) -> list[FileRecord]:
    records: list[FileRecord] = []
    for path in files:
        text, _truncated, error = read_text(path, max_chars_per_file)
        if error:
            continue
        rel = path.relative_to(repo_root).as_posix()
        suffix = path.suffix.lower()
        kind = "doc" if suffix in DOC_EXTENSIONS else "code"
        records.append(
            FileRecord(
                path=rel,
                extension=suffix,
                kind=kind,
                chars=len(text),
                lines=len(text.splitlines()),
                symbols=extract_symbols(path, text),
            )
        )
    return records


def read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"path": str(path), "exists": False, "data": None, "error": "missing"}
    try:
        return {"path": str(path), "exists": True, "data": json.loads(path.read_text(encoding="utf-8-sig")), "error": ""}
    except Exception as exc:  # noqa: BLE001 - report-only analyzer.
        return {"path": str(path), "exists": True, "data": None, "error": f"{type(exc).__name__}: {exc}"}


def collect_reports(repo_root: Path, report_files: list[str]) -> list[dict[str, Any]]:
    reports = []
    for rel in dict.fromkeys(report_files):
        path = repo_root / rel
        item = read_json_if_exists(path)
        data = item.get("data")
        reports.append(
            {
                "path": rel,
                "exists": item["exists"],
                "kind": data.get("kind") if isinstance(data, dict) else None,
                "passed": data.get("passed") if isinstance(data, dict) else None,
                "errors": data.get("errors", [])[:10] if isinstance(data, dict) and isinstance(data.get("errors", []), list) else [],
                "warnings": data.get("warnings", [])[:10] if isinstance(data, dict) and isinstance(data.get("warnings", []), list) else [],
                "provider_execution_performed": data.get("provider_execution_performed") if isinstance(data, dict) else None,
                "error": item.get("error"),
            }
        )
    return reports


def scan_doc_references(repo_root: Path, docs: Iterable[Path]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for doc in docs:
        text, _truncated, error = read_text(doc)
        if error:
            continue
        doc_rel = doc.relative_to(repo_root).as_posix()
        for match in PATH_RE.findall(text):
            normalized = match.strip("`.,:)];\"").replace("\\", "/")
            if not normalized or normalized.startswith(("http/", "https/")):
                continue
            key = (doc_rel, normalized)
            if key in seen:
                continue
            seen.add(key)
            target = repo_root / normalized
            refs.append(
                {
                    "doc": doc_rel,
                    "reference": normalized,
                    "exists": target.exists(),
                    "kind": "path_reference",
                }
            )
    return refs


def compare_docs_to_code(repo_root: Path, docs: list[Path], file_records: list[FileRecord]) -> dict[str, Any]:
    code_paths = {record.path for record in file_records if record.kind == "code"}
    symbol_to_paths: dict[str, list[str]] = {}
    for record in file_records:
        if record.kind != "code":
            continue
        for symbol in record.symbols:
            symbol_to_paths.setdefault(symbol, []).append(record.path)

    path_refs = scan_doc_references(repo_root, docs)
    missing_path_refs = [item for item in path_refs if not item["exists"] and not item["reference"].startswith("output/")]

    symbol_refs: list[dict[str, Any]] = []
    doc_symbol_candidates = sorted(symbol_to_paths.keys(), key=len, reverse=True)[:800]
    for doc in docs:
        text, _truncated, error = read_text(doc, max_chars=160_000)
        if error:
            continue
        doc_rel = doc.relative_to(repo_root).as_posix()
        for symbol in doc_symbol_candidates:
            if len(symbol) < 4:
                continue
            if symbol in text:
                symbol_refs.append({"doc": doc_rel, "symbol": symbol, "code_paths": symbol_to_paths[symbol][:8]})

    return {
        "code_path_count": len(code_paths),
        "doc_path_reference_count": len(path_refs),
        "missing_path_reference_count": len(missing_path_refs),
        "missing_path_references": missing_path_refs[:100],
        "symbol_reference_count": len(symbol_refs),
        "symbol_references_sample": symbol_refs[:100],
    }


def deterministic_findings(reports: list[dict[str, Any]], doc_code: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    failed_reports = [r for r in reports if r.get("passed") is False]
    missing_reports = [r for r in reports if not r.get("exists")]
    if failed_reports:
        findings.append(
            {
                "severity": "high",
                "area": "validation_reports",
                "title": "Some validation reports are failing",
                "details": [f"{r['path']}: {r.get('errors')}" for r in failed_reports[:8]],
            }
        )
    if missing_reports:
        findings.append(
            {
                "severity": "medium",
                "area": "validation_reports",
                "title": "Some expected validation reports are missing",
                "details": [r["path"] for r in missing_reports[:12]],
            }
        )
    if doc_code.get("missing_path_reference_count", 0):
        findings.append(
            {
                "severity": "medium",
                "area": "doc_code_consistency",
                "title": "Markdown references missing repository paths",
                "details": [f"{item['doc']} -> {item['reference']}" for item in doc_code["missing_path_references"][:20]],
            }
        )
    if not findings:
        findings.append(
            {
                "severity": "info",
                "area": "baseline",
                "title": "No deterministic blocking discrepancy found",
                "details": ["Use --use-ollama for semantic review across the collected repo summary."],
            }
        )
    return findings


def compact_records(records: list[FileRecord], *, limit: int) -> list[dict[str, Any]]:
    out = []
    for record in records[:limit]:
        out.append(
            {
                "path": record.path,
                "kind": record.kind,
                "extension": record.extension,
                "lines": record.lines,
                "chars": record.chars,
                "symbols": list(record.symbols[:30]),
            }
        )
    return out


def build_ollama_prompt(review: dict[str, Any], *, objective: str) -> str:
    compact = {
        "objective": objective,
        "repo_root": review["repo_root"],
        "resource_lanes": review["resource_lanes"],
        "summary": review["summary"],
        "reports": review["validation_reports"],
        "doc_code_consistency": review["doc_code_consistency"],
        "deterministic_findings": review["deterministic_findings"],
        "files_sample": review["files_sample"],
        "guardrails": review["guardrails"],
    }
    return (
        "You are an IA-Carmine repository reviewer. Review docs versus code.\n"
        "Return JSON only with keys: verdict, mismatches, patch_proposals, doc_review, stop_conditions.\n"
        "Do not propose destructive operations. Do not propose Blender runtime execution.\n"
        "Do not promote NPU/OpenVINO to primary advisory. Do not apply patches.\n"
        "Patch proposals must be manual-review-only and small.\n\n"
        "Input JSON:\n"
        + json.dumps(compact, indent=2, ensure_ascii=False)
    )


def maybe_run_ollama(repo_root: Path, prompt: str, *, model: str | None, max_new_tokens: int) -> dict[str, Any]:
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from Tools.npu.ollama_runtime import OllamaSession  # noqa: PLC0415

    try:
        with OllamaSession(model=model, shutdown_server=False, unload_model=True) as session:
            text = session.generate(prompt, max_new_tokens=max_new_tokens, temperature=0.1)
        parsed: Any = None
        try:
            from Tools.ai.model_json import parse_model_json_object  # noqa: PLC0415

            parsed = parse_model_json_object(text)
        except Exception:
            parsed = None
        return {
            "used": True,
            "provider": "ollama",
            "compute_lane": "gpu_cuda",
            "model": model,
            "response_text": text,
            "response_json": parsed,
            "error": "",
        }
    except Exception as exc:  # noqa: BLE001 - advisory live provider.
        return {
            "used": False,
            "provider": "ollama",
            "compute_lane": "gpu_cuda",
            "model": model,
            "response_text": "",
            "response_json": None,
            "error": f"{type(exc).__name__}: {exc}",
        }


def build_proposals(review: dict[str, Any]) -> dict[str, Any]:
    proposals: list[dict[str, Any]] = []
    for finding in review.get("deterministic_findings", []):
        if finding.get("severity") in {"high", "medium"}:
            proposals.append(
                {
                    "id": f"MEGA-{len(proposals)+1:03d}",
                    "title": finding.get("title"),
                    "area": finding.get("area"),
                    "apply_mode": "manual_review_only",
                    "content_status": "proposal_only",
                    "details": finding.get("details", []),
                }
            )
    ollama_json = review.get("ollama_review", {}).get("response_json")
    if isinstance(ollama_json, dict):
        for item in ollama_json.get("patch_proposals", []) or []:
            if isinstance(item, dict):
                proposal = dict(item)
                proposal.setdefault("id", f"OLLAMA-MEGA-{len(proposals)+1:03d}")
                proposal.setdefault("apply_mode", "manual_review_only")
                proposal.setdefault("content_status", "proposal_only")
                proposals.append(proposal)
    return {
        "schema_version": 1,
        "kind": "megalithic_repo_review_proposals",
        "repo_root": review["repo_root"],
        "passed": True,
        "errors": [],
        "warnings": [],
        "provider_execution_performed": review["provider_execution_performed"],
        "patch_application_performed": False,
        "apply_mode": "manual_review_only",
        "proposal_count": len(proposals),
        "proposals": proposals,
    }


def render_markdown(review: dict[str, Any], proposals: dict[str, Any]) -> str:
    lines = ["# Megalithic Repository Review", ""]
    lines.append(f"- Generated at: `{review['generated_at']}`")
    lines.append(f"- Provider execution performed: `{review['provider_execution_performed']}`")
    lines.append(f"- Ollama used: `{review['ollama_review']['used']}`")
    lines.append(f"- Docs scanned: `{review['summary']['doc_count']}`")
    lines.append(f"- Code files scanned: `{review['summary']['code_count']}`")
    lines.append(f"- Proposal count: `{proposals['proposal_count']}`")
    lines.append("")
    lines.append("## Resource lanes")
    lines.append("")
    for lane, details in review["resource_lanes"].items():
        lines.append(f"- `{lane}`: {details}")
    lines.append("")
    lines.append("## Deterministic findings")
    lines.append("")
    for finding in review["deterministic_findings"]:
        lines.append(f"### {finding['severity']} — {finding['title']}")
        lines.append(f"- Area: `{finding['area']}`")
        for detail in finding.get("details", [])[:20]:
            lines.append(f"- {detail}")
        lines.append("")
    if review["ollama_review"].get("response_text"):
        lines.append("## Ollama semantic review")
        lines.append("")
        lines.append("```text")
        lines.append(review["ollama_review"]["response_text"][:12000])
        lines.append("```")
        lines.append("")
    lines.append("## Proposals")
    lines.append("")
    for proposal in proposals["proposals"]:
        lines.append(f"- `{proposal.get('id')}` {proposal.get('title')} ({proposal.get('apply_mode')})")
    lines.append("")
    lines.append("## Guardrails")
    lines.append("")
    for key, value in review["guardrails"].items():
        lines.append(f"- `{key}`: `{value}`")
    return "\n".join(lines) + "\n"


def run_review(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    repo_root = Path(args.repo_root).resolve()
    report_files = list(DEFAULT_REPORTS) + split_path_values(args.report_file or [])
    docs, code = iter_files(
        repo_root,
        include_all_docs=args.include_all_docs,
        include_all_code=args.include_all_code,
        include_output=args.include_output,
        include_index=args.include_index,
        max_files=args.max_files,
    )
    records = build_file_records(repo_root, [*docs, *code], max_chars_per_file=args.max_chars_per_file)
    reports = collect_reports(repo_root, report_files)
    doc_code = compare_docs_to_code(repo_root, docs, records)
    findings = deterministic_findings(reports, doc_code)

    review: dict[str, Any] = {
        "schema_version": 1,
        "kind": "megalithic_repo_review",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": True,
        "errors": [],
        "warnings": [],
        "objective": args.objective,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "apply_mode": "report_only_manual_review_only",
        "resource_lanes": {
            "cpu": "deterministic indexing, validation report ingestion, docs/code reference scan",
            "gpu_cuda": "optional live Ollama semantic review when --use-ollama is passed",
            "npu": "consumed through existing NPU metadata/reports/knowledge-broker artifacts; no live NPU execution here",
        },
        "summary": {
            "doc_count": len(docs),
            "code_count": len(code),
            "record_count": len(records),
            "validation_report_count": len(reports),
        },
        "validation_reports": reports,
        "doc_code_consistency": doc_code,
        "deterministic_findings": findings,
        "files_sample": compact_records(records, limit=args.file_sample_limit),
        "ollama_review": {
            "used": False,
            "provider": "ollama",
            "compute_lane": "gpu_cuda",
            "model": args.ollama_model,
            "response_text": "",
            "response_json": None,
            "error": "",
        },
        "guardrails": {
            "report_only": True,
            "provider_execution_explicit_only": True,
            "patch_application_performed": False,
            "blender_runtime_touched": False,
            "full_analysis_json_touched": False,
            "sqlite_db_touched": False,
            "npu_promoted_to_advisory": False,
            "openvino_gpu_primary_lane": False,
        },
    }

    if args.use_ollama:
        prompt = build_ollama_prompt(review, objective=args.objective)
        review["ollama_review"] = maybe_run_ollama(
            repo_root,
            prompt,
            model=args.ollama_model,
            max_new_tokens=args.ollama_max_new_tokens,
        )
        review["provider_execution_performed"] = bool(review["ollama_review"].get("used"))
        if review["ollama_review"].get("error"):
            review["warnings"].append(review["ollama_review"]["error"])

    proposals = build_proposals(review)
    return review, proposals


def write_outputs(review: dict[str, Any], proposals: dict[str, Any], args: argparse.Namespace) -> None:
    output = Path(args.output)
    markdown_output = Path(args.markdown_output)
    proposal_output = Path(args.proposal_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    proposal_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(review, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    proposal_output.write_text(json.dumps(proposals, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_output.write_text(render_markdown(review, proposals), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--objective", default="Review Markdown documentation against code and validation artifacts, then propose manual-review-only follow-up patches or docs updates.")
    parser.add_argument("--include-all-docs", action="store_true")
    parser.add_argument("--include-all-code", action="store_true")
    parser.add_argument("--include-output", action="store_true")
    parser.add_argument("--include-index", action="store_true")
    parser.add_argument("--max-files", type=int, default=0)
    parser.add_argument("--max-chars-per-file", type=int, default=80_000)
    parser.add_argument("--file-sample-limit", type=int, default=200)
    parser.add_argument("--report-file", action="append", default=[])
    parser.add_argument("--use-ollama", action="store_true", help="Explicitly run live Ollama/GPU semantic review.")
    parser.add_argument("--ollama-model", default=None)
    parser.add_argument("--ollama-max-new-tokens", type=int, default=1600)
    parser.add_argument("--output", default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--markdown-output", default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--proposal-output", default=DEFAULT_PROPOSALS_JSON)
    args = parser.parse_args()

    review, proposals = run_review(args)
    write_outputs(review, proposals, args)
    print(json.dumps({
        "passed": review["passed"],
        "output": args.output,
        "markdown": args.markdown_output,
        "proposals": args.proposal_output,
        "provider_execution_performed": review["provider_execution_performed"],
        "proposal_count": proposals["proposal_count"],
    }, indent=2))
    return 0 if review["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
