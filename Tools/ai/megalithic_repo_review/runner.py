from __future__ import annotations

from .analysis import compact_records, compare_code_to_code, compare_docs_to_code, compare_docs_to_docs, deterministic_findings
from .collectors import collect_raw_artifacts, collect_reports, inspect_sqlite_memory
from .common import *  # noqa: F403
from .provider import build_ollama_prompt, maybe_run_ollama
from .reporting import build_proposals

def run_review(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    repo_root = Path(args.repo_root).resolve()
    report_files = list(DEFAULT_REPORTS) + split_path_values(args.report_file or [])
    docs, code, raw_files, sqlite_files = iter_files(
        repo_root,
        include_all_docs=args.include_all_docs,
        include_all_code=args.include_all_code,
        include_output=args.include_output,
        include_index=args.include_index,
        include_raw=args.include_raw,
        include_sqlite_memory=args.include_sqlite_memory,
        max_files=args.max_files,
    )
    records = build_file_records(
        repo_root, [*docs, *code], max_chars_per_file=args.max_chars_per_file
    )
    reports = collect_reports(repo_root, report_files)
    raw_artifacts = (
        collect_raw_artifacts(repo_root, raw_files, max_raw_files=args.max_raw_files)
        if args.include_raw
        else []
    )
    sqlite_memory = (
        inspect_sqlite_memory(repo_root, sqlite_files, max_tables=args.max_sqlite_tables)
        if args.include_sqlite_memory
        else []
    )
    doc_code = compare_docs_to_code(repo_root, docs, records)
    doc_doc = compare_docs_to_docs(repo_root, records)
    code_code = compare_code_to_code(records)
    findings = deterministic_findings(reports, doc_code, doc_doc, code_code, sqlite_memory)
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
            "cpu": "deterministic indexing, validation report ingestion, doc/code/doc-doc/code-code scans, RAW and SQLite read-only metadata",
            "gpu_cuda": "optional live Ollama semantic review when --use-ollama is passed; GPU/Ollama functions are inventoried from project code",
            "npu": "NPU/OpenVINO functions are inventoried from project code; live NPU execution remains separate and explicit; existing NPU reports are ingested",
        },
        "summary": {
            "doc_count": len(docs),
            "code_count": len(code),
            "record_count": len(records),
            "raw_artifact_count": len(raw_artifacts),
            "sqlite_memory_count": len(sqlite_memory),
            "validation_report_count": len(reports),
        },
        "validation_reports": reports,
        "raw_artifacts": raw_artifacts,
        "sqlite_memory": sqlite_memory,
        "doc_code_consistency": doc_code,
        "doc_doc_consistency": doc_doc,
        "code_code_consistency": code_code,
        "provider_function_inventory": code_code.get("provider_functions", {}),
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
            "sqlite_memory_read_only": True,
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
