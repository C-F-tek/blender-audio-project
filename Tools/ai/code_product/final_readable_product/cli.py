#!/usr/bin/env python3
"""Assemble the run-owned final readable product for heap context closure."""
from __future__ import annotations
import argparse
import json
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any
try:
    from Tools.ai._shared.heap_final_code_product import (
        code_product_items,
        code_product_status,
        render_full_code_product_markdown,
    )
    from Tools.ai._shared.heap_final_readable_synthesis import render_markdown
    from Tools.ai.code_product.final_readable_product.product_contract import (
        code_product_markdown_metrics,
        final_product_blockers,
        real_code_product_ready,
    )
    from Tools.ai.code_product.final_readable_product.pointer_reconstruction import build_pointer_reconstruction
except ImportError:  # pragma: no cover
    repo_root_for_import = Path(__file__).resolve().parents[4]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai._shared.heap_final_code_product import (  # type: ignore
        code_product_items,
        code_product_status,
        render_full_code_product_markdown,
    )
    from Tools.ai._shared.heap_final_readable_synthesis import render_markdown  # type: ignore
    from Tools.ai.code_product.final_readable_product.product_contract import (  # type: ignore
        code_product_markdown_metrics,
        final_product_blockers,
        real_code_product_ready,
    )
    from Tools.ai.code_product.final_readable_product.pointer_reconstruction import build_pointer_reconstruction  # type: ignore
def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")
def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}
def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig", errors="replace")
    except Exception:
        return ""
def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False, default=str) + "\n",
        encoding="utf-8",
    )
def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
def resolve_path(root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = root / path
    return path.resolve(strict=False)
def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []
def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}
def count_from_decision(decision: dict[str, Any], key: str, items: list[Any]) -> int:
    try:
        return max(len(items), int(decision.get(key) or 0))
    except (TypeError, ValueError):
        return len(items)
def discover_code_matrix_reports(
    repo_root: Path, run_dir: Path, gate: dict[str, Any]
) -> list[Path]:
    paths: list[Path] = []
    for container in (gate.get("metrics"), gate.get("real_run_output_contract")):
        for value in as_list(as_dict(container).get("code_execution_matrix_reports")):
            raw = Path(str(value))
            if raw.is_absolute():
                paths.append(raw)
            elif str(value).replace("\\", "/").startswith("output/"):
                paths.append(repo_root / raw)
            else:
                paths.append(run_dir / raw)
    paths.extend(run_dir.glob("broker_bridge/tool_outputs/*heap_code_execution_tool.json"))
    paths.extend(run_dir.glob("**/*heap_code_execution_tool.json"))
    deduped: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        key = str(path.resolve(strict=False))
        if key not in seen and path.exists():
            deduped.append(path.resolve(strict=False))
            seen.add(key)
    return deduped
def load_code_matrix(
    repo_root: Path, run_dir: Path, gate: dict[str, Any]
) -> tuple[dict[str, Any], str]:
    for path in discover_code_matrix_reports(repo_root, run_dir, gate):
        payload = read_json(path)
        if payload.get("kind") == "heap_code_execution_tool":
            return payload, str(path)
    return {}, ""
def append_download_manifest(manifest_path: Path, paths: list[Path]) -> None:
    if not manifest_path:
        return
    try:
        lines = manifest_path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    except Exception:
        lines = []
    existing = set(lines)
    additions = ["", "Final readable product:"]
    for path in paths:
        line = f"- {path}"
        if line not in existing:
            additions.append(line)
    if len(additions) > 2:
        write_text(manifest_path, "\n".join(lines + additions))
def zip_documents_dir(documents_dir: Path, zip_path: Path) -> int:
    members: list[Path] = [
        path for path in documents_dir.rglob("*") if path.is_file() and path != zip_path
    ]
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(members):
            archive.write(path, path.relative_to(documents_dir).as_posix())
    return len(members)
def build_report(args: argparse.Namespace) -> tuple[dict[str, Any], str]:
    repo_root = Path(args.repo_root).resolve()
    run_dir = resolve_path(repo_root, args.run_dir)
    composer_path = resolve_path(
        repo_root, args.composer_json or run_dir / "heap_final_proposal_composer.json"
    )
    gate_path = resolve_path(
        repo_root, args.gate_report or run_dir / "heap_runtime_completeness_gate_report.json"
    )
    composer = read_json(composer_path)
    gate = read_json(gate_path)
    postrun = read_json(run_dir / "external_heap_postrun_package.json")
    revision = read_json(run_dir / "external_heap_revision_context.json")
    pointer = read_json(run_dir / "external_heap_block_pointer_manifest.json")
    matrix, matrix_path = load_code_matrix(repo_root, run_dir, gate)
    pointer_reconstruction = build_pointer_reconstruction(pointer, revision)
    decision = as_dict(composer.get("operator_decision"))
    gate_product_status = str(as_dict(gate.get("metrics")).get("product_status") or "")
    markdown = render_markdown(
        run_dir=run_dir,
        composer=composer,
        gate=gate,
        postrun=postrun,
        revision=revision,
        matrix=matrix,
        matrix_path=matrix_path,
    )
    full_code_product = render_full_code_product_markdown(matrix, matrix_path, gate_product_status)
    output = resolve_path(repo_root, args.output or run_dir / "heap_final_readable_product.json")
    markdown_output = resolve_path(
        repo_root, args.markdown_output or run_dir / "heap_final_readable_product.md"
    )
    text_output = resolve_path(
        repo_root, args.text_output or run_dir / "heap_final_readable_product.txt"
    )
    full_code_product_output = run_dir / "CODE_PRODUCT_FULL_PATCH.md"
    write_text(markdown_output, markdown)
    write_text(text_output, markdown)
    write_text(full_code_product_output, full_code_product)
    documents_outputs: dict[str, str] = {}
    documents_zip = ""
    zip_member_count = 0
    zip_path_for_later: Path | None = None
    documents_dir_for_later: Path | None = None
    documents_json_path: Path | None = None
    documents_dir_value = args.documents_dir or str(composer.get("documents_dir") or "")
    if documents_dir_value:
        documents_dir = Path(documents_dir_value).expanduser().resolve()
        documents_dir_for_later = documents_dir
        documents_md = documents_dir / "FINAL_READABLE_PRODUCT.md"
        documents_txt = documents_dir / "FINAL_READABLE_PRODUCT.txt"
        documents_json = documents_dir / "FINAL_READABLE_PRODUCT.json"
        documents_code_product = documents_dir / "CODE_PRODUCT_FULL_PATCH.md"
        documents_json_path = documents_json
        write_text(documents_md, markdown)
        write_text(documents_txt, markdown)
        write_text(documents_code_product, full_code_product)
        documents_outputs = {
            "documents_markdown": str(documents_md),
            "documents_text": str(documents_txt),
            "documents_json": str(documents_json),
            "documents_code_product": str(documents_code_product),
        }
        manifest = str(composer.get("download_manifest_txt") or "")
        if manifest:
            append_download_manifest(
                Path(manifest).expanduser().resolve(),
                [documents_md, documents_txt, documents_json, documents_code_product],
            )
        if args.zip_documents:
            zip_path_for_later = (
                Path(args.zip_output).expanduser().resolve()
                if args.zip_output
                else Path(str(documents_dir) + ".zip")
            )
            documents_zip = str(zip_path_for_later)
    matrix_items = code_product_items(matrix)
    code_product_state = code_product_status(matrix, gate_product_status)
    provider_decision = str(decision.get("decision") or "")
    concrete_code_proposal_count = len(matrix_items)
    if gate_product_status and gate_product_status != "ready":
        final_document_status = (
            "BLOCKED_WITH_CODE_PRODUCT_REVIEW"
            if concrete_code_proposal_count > 0
            else "DIAGNOSTIC_REVIEW_READY"
        )
    elif concrete_code_proposal_count > 0:
        final_document_status = code_product_state
    elif provider_decision in {
        "DIAGNOSTIC_ONLY",
        "BLOCKED_PROVIDER_REVIEW",
        "BLOCKED_NO_VERIFIED_TARGET",
        "NO CONCRETE PATCHABLE PROPOSAL",
    }:
        final_document_status = "DIAGNOSTIC_REVIEW_READY"
    else:
        final_document_status = "NO_APPLICABLE_CODE_PRODUCT"
    code_product_report = code_product_markdown_metrics(full_code_product)
    code_product_ready = real_code_product_ready(
        final_document_status=final_document_status,
        concrete_code_proposal_count=concrete_code_proposal_count,
        code_product_metrics=code_product_report,
    )
    blockers = final_product_blockers(
        markdown_output=markdown_output,
        final_document_status=final_document_status,
        concrete_code_proposal_count=concrete_code_proposal_count,
        code_product_metrics=code_product_report,
        code_product_ready=code_product_ready,
        pointer=pointer,
        revision=revision,
        matrix=matrix,
        gate=gate,
    )
    blockers.extend(str(item) for item in pointer_reconstruction.get("errors", []))
    report = {
        "schema_version": 1,
        "kind": "heap_final_readable_product",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "run_dir": str(run_dir),
        "passed": bool(
            markdown.strip()
            and markdown_output.exists()
            and code_product_ready
            and not blockers
        ),
        "final_document_status": final_document_status,
        "decision": decision.get("decision"),
        "product_status": gate_product_status,
        "code_product_status": code_product_state,
        "real_code_product_ready": code_product_ready,
        "code_product_metrics": code_product_report,
        "blocking_reasons": blockers,
        "accepted_provider_proposal_count": count_from_decision(
            decision, "accepted_count", as_list(decision.get("accepted_proposals"))
        ),
        "rejected_provider_proposal_count": count_from_decision(
            decision, "rejected_count", as_list(decision.get("rejected_proposals"))
        ),
        "code_execution_matrix_passed": matrix.get("passed"),
        "pointer_manifest_passed": pointer.get("passed"),
        "pointer_reconstruction": pointer_reconstruction,
        "pointer_reconstruction_performed": pointer_reconstruction.get("performed"),
        "pointer_reconstruction_passed": pointer_reconstruction.get("passed"),
        "pointer_edge_count": pointer.get("edge_count"),
        "pointer_roles_present": pointer.get("all_roles_present", pointer.get("roles_present")),
        "linked_gpu0_block_count": revision.get("linked_gpu0_block_count")
        or revision.get("gpu0_block_count"),
        "linked_npu_block_count": revision.get("linked_npu_block_count")
        or revision.get("npu_block_count"),
        "concrete_code_proposal_count": concrete_code_proposal_count,
        "matrix_target_count": matrix.get("target_count"),
        "verified_target_count": matrix.get("verified_target_count"),
        "matrix_report": matrix_path,
        "markdown_output": str(markdown_output),
        "text_output": str(text_output),
        "full_code_product_output": str(full_code_product_output),
        "json_output": str(output),
        "documents_outputs": documents_outputs,
        "documents_zip": documents_zip,
        "zip_member_count": zip_member_count,
        "provider_execution_performed": gate.get("provider_execution_performed"),
        "patch_application_performed": gate.get("patch_application_performed"),
        "source_writes_performed": gate.get("source_writes_performed"),
    }
    write_json(output, report)
    if documents_json_path:
        write_json(documents_json_path, report)
    if zip_path_for_later and documents_dir_for_later:
        zip_member_count = zip_documents_dir(documents_dir_for_later, zip_path_for_later)
        report["zip_member_count"] = zip_member_count
        write_json(output, report)
        if documents_json_path:
            write_json(documents_json_path, report)
    return report, markdown
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--composer-json", default="")
    parser.add_argument("--gate-report", default="")
    parser.add_argument("--documents-dir", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--markdown-output", default="")
    parser.add_argument("--text-output", default="")
    parser.add_argument("--zip-output", default="")
    parser.add_argument("--zip-documents", action="store_true")
    return parser.parse_args()
def main() -> int:
    report, _markdown = build_report(parse_args())
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("passed") else 2
if __name__ == "__main__":
    raise SystemExit(main())
