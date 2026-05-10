#!/usr/bin/env python3
"""Compose heap proposal chunks into a final local review package.

The heap gate intentionally keeps provider outputs, chunked proposals and
runtime reports separated. This composer is the deterministic final stage: it
collects all proposal chunks, provider reports, context artifact references and
quality signals, then writes a bounded repository report plus an operator-facing
Documents folder.
"""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def read_text(path: Path, limit: int | None = None) -> str:
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except Exception:
        return ""
    if limit is not None and len(text) > limit:
        return text[:limit] + "\n...[truncated]\n"
    return text


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def discover_run_dir(repo_root: Path, report_file: str, run_dir: str) -> Path:
    if run_dir:
        return resolve_path(repo_root, run_dir)
    if report_file:
        report = resolve_path(repo_root, report_file)
        if report.name == "heap_runtime_completeness_gate_report.json":
            return report.parent
    validation = repo_root / "output" / "validation"
    candidates = sorted(
        [path for path in validation.glob("*") if path.is_dir() and (path / "heap_runtime_completeness_gate_report.json").exists()],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if candidates:
        return candidates[0]
    raise SystemExit("unable to discover run dir; provide --run-dir or --report-file")


def documents_root(custom_root: str, stamp: str) -> Path:
    base = Path(custom_root).expanduser() if custom_root else Path.home() / "Documents"
    return (base / f"aicarmine_heap_final_proposals_{stamp}").resolve()


def list_proposals(run_dir: Path) -> list[dict[str, Any]]:
    proposal_dir = run_dir / "team_context" / "proposal_iterations"
    proposals: list[dict[str, Any]] = []
    if not proposal_dir.exists():
        return proposals
    for json_path in sorted(proposal_dir.glob("heap_proposal_revision_*.json")):
        data = read_json(json_path)
        md_path = json_path.with_suffix(".md")
        proposals.append(
            {
                "name": json_path.name,
                "json_path": json_path,
                "markdown_path": md_path if md_path.exists() else None,
                "revision": data.get("revision"),
                "source": data.get("source"),
                "quality_passed": data.get("quality_passed"),
                "implementation_quality": data.get("implementation_quality", {}),
                "proposal_progress": data.get("proposal_progress", {}),
                "gpu0_review": data.get("gpu0_review", []),
                "npu_micro_task_piece": data.get("npu_micro_task_piece", []),
                "npu_workload_audit": data.get("npu_workload_audit", {}),
                "anchored_source_candidates": data.get("anchored_source_candidates", []),
                "response_text": data.get("response_text", ""),
            }
        )
    return proposals


def list_provider_reports(run_dir: Path) -> list[dict[str, Any]]:
    provider_dir = run_dir / "provider_teamwork"
    reports: list[dict[str, Any]] = []
    if not provider_dir.exists():
        return reports
    for path in sorted(provider_dir.glob("*.json")):
        data = read_json(path)
        reports.append(
            {
                "path": path,
                "kind": data.get("kind") or data.get("report_kind"),
                "lane": data.get("lane") or data.get("role"),
                "passed": data.get("passed"),
                "provider_execution_performed": data.get("provider_execution_performed"),
                "response_text": data.get("response_text", ""),
                "npu_device_workload": data.get("npu_device_workload"),
                "warnings": data.get("warnings", []),
                "errors": data.get("errors", []),
            }
        )
    return reports


def flatten_quality_blockers(report: dict[str, Any], proposals: list[dict[str, Any]]) -> list[str]:
    blockers: list[str] = []
    output_contract = report.get("real_run_output_contract") if isinstance(report.get("real_run_output_contract"), dict) else {}
    metrics = report.get("metrics") if isinstance(report.get("metrics"), dict) else {}
    quality = output_contract.get("quality_output_signals") if isinstance(output_contract.get("quality_output_signals"), dict) else {}
    implementation = quality.get("implementation_quality") if isinstance(quality.get("implementation_quality"), dict) else {}

    if metrics.get("product_status") == "blocked_with_reason":
        blockers.append("heap product_status=blocked_with_reason")
    if metrics.get("quality_output_passed") is False:
        blockers.append("quality_output_passed=False")
    for error in implementation.get("errors") or []:
        blockers.append(str(error))
    for proposal in proposals:
        impl = proposal.get("implementation_quality") if isinstance(proposal.get("implementation_quality"), dict) else {}
        progress = proposal.get("proposal_progress") if isinstance(proposal.get("proposal_progress"), dict) else {}
        for error in impl.get("errors") or []:
            blockers.append(f"{proposal.get('name')}: {error}")
        for error in progress.get("errors") or []:
            blockers.append(f"{proposal.get('name')}: {error}")
    return list(dict.fromkeys(blockers))


def proposal_text_for_review(proposal: dict[str, Any], max_chars: int) -> str:
    md_path = proposal.get("markdown_path")
    if isinstance(md_path, Path) and md_path.exists():
        return read_text(md_path, limit=max_chars)
    return str(proposal.get("response_text") or "")[:max_chars]


def render_markdown(
    *,
    repo_root: Path,
    run_dir: Path,
    report: dict[str, Any],
    proposals: list[dict[str, Any]],
    provider_reports: list[dict[str, Any]],
    blockers: list[str],
    max_proposal_chars: int,
) -> str:
    metrics = report.get("metrics") if isinstance(report.get("metrics"), dict) else {}
    output_contract = report.get("real_run_output_contract") if isinstance(report.get("real_run_output_contract"), dict) else {}
    context_refs = output_contract.get("context_artifact_refs") or []
    lines: list[str] = [
        "# IA-Carmine Heap Final Proposal Composer",
        "",
        "## Runtime status",
        "",
        f"- Run dir: `{repo_rel(repo_root, run_dir)}`",
        f"- Product status: `{metrics.get('product_status') or output_contract.get('product_status')}`",
        f"- Quality output passed: `{metrics.get('quality_output_passed')}`",
        f"- Provider revisions: `{metrics.get('provider_revision_count')}`",
        f"- Runtime debug lab required: `{output_contract.get('runtime_debug_lab_required')}`",
        f"- Runtime debug lab passed: `{output_contract.get('runtime_debug_lab_passed')}`",
        "",
        "## Context-limit escape protocol",
        "",
        "Il prodotto finale non dipende dalla sola finestra token di GPU1: ogni proposta viene salvata come chunk riusabile, GPU0/NPU producono review e audit separati, e questo composer assembla il risultato finale dai file persistenti.",
        "",
    ]
    if blockers:
        lines.extend(["## Blocking quality issues", ""])
        lines.extend(f"- {item}" for item in blockers)
        lines.append("")
    else:
        lines.extend(["## Blocking quality issues", "", "- Nessun blocco deterministico rilevato dal composer.", ""])

    lines.extend(["## Provider reports", ""])
    for provider in provider_reports:
        rel = repo_rel(repo_root, provider["path"]) if isinstance(provider.get("path"), Path) else ""
        workload = provider.get("npu_device_workload") if isinstance(provider.get("npu_device_workload"), dict) else {}
        lines.extend(
            [
                f"### {provider.get('lane') or 'provider'}",
                "",
                f"- Report: `{rel}`",
                f"- Passed: `{provider.get('passed')}`",
                f"- Provider execution: `{provider.get('provider_execution_performed')}`",
            ]
        )
        if workload:
            lines.extend(
                [
                    f"- NPU workload performed: `{workload.get('performed')}`",
                    f"- NPU workload iterations: `{workload.get('iterations')}`",
                    f"- NPU workload seconds: `{workload.get('seconds')}`",
                    f"- Python: `{workload.get('python_exe')}`",
                ]
            )
        summary = str(provider.get("response_text") or "").strip()
        if summary:
            lines.extend(["", summary[:1600], ""])

    lines.extend(["## Proposal chunks", ""])
    if not proposals:
        lines.append("- Nessuna proposal iteration trovata.")
    for proposal in proposals:
        lines.extend(
            [
                f"### {proposal.get('name')}",
                "",
                f"- Revision: `{proposal.get('revision')}`",
                f"- Source: `{proposal.get('source')}`",
                f"- Quality passed: `{proposal.get('quality_passed')}`",
                "",
            ]
        )
        anchored = proposal.get("anchored_source_candidates") or []
        if anchored:
            lines.extend(["Anchored source candidates:"])
            lines.extend(f"- `{item}`" for item in anchored[:20])
            lines.append("")
        lines.extend(["```markdown", proposal_text_for_review(proposal, max_proposal_chars), "```", ""])

    lines.extend(["## Context artifacts", ""])
    for ref in context_refs[:80]:
        lines.append(f"- `{ref}`")
    lines.append("")
    return "\n".join(lines)


def write_documents_package(
    *,
    repo_root: Path,
    stamp: str,
    doc_dir: Path,
    markdown: str,
    json_data: dict[str, Any],
    proposals: list[dict[str, Any]],
) -> list[str]:
    doc_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    md_path = doc_dir / f"aicarmine_heap_final_proposals_{stamp}.md"
    txt_path = doc_dir / f"aicarmine_heap_final_proposals_{stamp}.txt"
    json_path = doc_dir / f"aicarmine_heap_final_proposals_{stamp}.json"
    md_path.write_text(markdown, encoding="utf-8")
    txt_path.write_text(markdown, encoding="utf-8")
    json_path.write_text(json.dumps(json_data, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    written.extend([str(md_path), str(txt_path), str(json_path)])

    chunk_dir = doc_dir / "proposal_chunks"
    chunk_dir.mkdir(parents=True, exist_ok=True)
    for proposal in proposals:
        md = proposal.get("markdown_path")
        js = proposal.get("json_path")
        if isinstance(md, Path) and md.exists():
            target = chunk_dir / md.name
            shutil.copyfile(md, target)
            written.append(str(target))
        if isinstance(js, Path) and js.exists():
            target = chunk_dir / js.name
            shutil.copyfile(js, target)
            written.append(str(target))
    return written


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--run-dir", default="")
    parser.add_argument("--report-file", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--markdown-output", default="")
    parser.add_argument("--documents-root", default="")
    parser.add_argument("--write-documents", action="store_true")
    parser.add_argument("--max-proposal-chars", type=int, default=18000)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    run_dir = discover_run_dir(repo_root, args.report_file, args.run_dir)
    report_file = resolve_path(repo_root, args.report_file) if args.report_file else run_dir / "heap_runtime_completeness_gate_report.json"
    report = read_json(report_file)
    stamp = str(report.get("stamp") or (report.get("metrics") or {}).get("stamp") or now_stamp())

    proposals = list_proposals(run_dir)
    provider_reports = list_provider_reports(run_dir)
    blockers = flatten_quality_blockers(report, proposals)

    markdown = render_markdown(
        repo_root=repo_root,
        run_dir=run_dir,
        report=report,
        proposals=proposals,
        provider_reports=provider_reports,
        blockers=blockers,
        max_proposal_chars=max(2000, int(args.max_proposal_chars)),
    )
    result = {
        "schema_version": 1,
        "kind": "heap_final_proposal_composer",
        "stamp": stamp,
        "repo_root": repo_root.as_posix(),
        "run_dir": repo_rel(repo_root, run_dir),
        "report_file": repo_rel(repo_root, report_file),
        "proposal_count": len(proposals),
        "provider_report_count": len(provider_reports),
        "blocking_issue_count": len(blockers),
        "blocking_issues": blockers,
        "product_status": (report.get("metrics") or {}).get("product_status") or (report.get("real_run_output_contract") or {}).get("product_status"),
        "quality_output_passed": (report.get("metrics") or {}).get("quality_output_passed"),
        "proposals": [
            {
                "name": item.get("name"),
                "revision": item.get("revision"),
                "source": item.get("source"),
                "quality_passed": item.get("quality_passed"),
                "implementation_quality": item.get("implementation_quality"),
                "proposal_progress": item.get("proposal_progress"),
                "anchored_source_candidates": item.get("anchored_source_candidates"),
            }
            for item in proposals
        ],
        "provider_reports": [
            {
                "path": repo_rel(repo_root, item["path"]) if isinstance(item.get("path"), Path) else "",
                "lane": item.get("lane"),
                "passed": item.get("passed"),
                "provider_execution_performed": item.get("provider_execution_performed"),
                "npu_device_workload": item.get("npu_device_workload"),
                "errors": item.get("errors"),
                "warnings": item.get("warnings"),
            }
            for item in provider_reports
        ],
    }

    output = resolve_path(repo_root, args.output) if args.output else run_dir / "heap_final_proposal_composer.json"
    markdown_output = resolve_path(repo_root, args.markdown_output) if args.markdown_output else run_dir / "heap_final_proposal_composer.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    markdown_output.write_text(markdown, encoding="utf-8")
    result["output"] = repo_rel(repo_root, output)
    result["markdown_output"] = repo_rel(repo_root, markdown_output)

    if args.write_documents:
        doc_dir = documents_root(args.documents_root, stamp)
        result["documents_dir"] = str(doc_dir)
        result["documents_outputs"] = write_documents_package(
            repo_root=repo_root,
            stamp=stamp,
            doc_dir=doc_dir,
            markdown=markdown,
            json_data=result,
            proposals=proposals,
        )

    output.write_text(json.dumps(result, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    return 0 if not blockers else 2


if __name__ == "__main__":
    raise SystemExit(main())
