from __future__ import annotations

from .collectors import discover_provider_functions, scan_doc_references
from .common import *  # noqa: F403

def compare_docs_to_code(
    repo_root: Path, docs: list[Path], file_records: list[FileRecord]
) -> dict[str, Any]:
    code_paths = {record.path for record in file_records if record.kind == "code"}
    symbol_to_paths: dict[str, list[str]] = {}
    for record in file_records:
        if record.kind != "code":
            continue
        for symbol in record.symbols:
            symbol_to_paths.setdefault(symbol, []).append(record.path)
    path_refs = scan_doc_references(repo_root, docs)
    missing_path_refs = [
        item
        for item in path_refs
        if not item["exists"] and not item["reference"].startswith("output/")
    ]
    doc_code_refs = [item for item in path_refs if item["reference"] in code_paths]
    symbol_refs: list[dict[str, Any]] = []
    candidates = sorted(symbol_to_paths.keys(), key=len, reverse=True)[:1200]
    for doc in docs:
        text, _truncated, error = read_text(doc, max_chars=220_000)
        if error:
            continue
        doc_rel = doc.relative_to(repo_root).as_posix()
        for symbol in candidates:
            if len(symbol) >= 4 and symbol in text:
                symbol_refs.append(
                    {
                        "doc": doc_rel,
                        "symbol": symbol,
                        "code_paths": symbol_to_paths[symbol][:8],
                    }
                )
    return {
        "code_path_count": len(code_paths),
        "doc_path_reference_count": len(path_refs),
        "doc_code_reference_count": len(doc_code_refs),
        "missing_path_reference_count": len(missing_path_refs),
        "missing_path_references": missing_path_refs[:160],
        "symbol_reference_count": len(symbol_refs),
        "symbol_references_sample": symbol_refs[:160],
    }

def compare_docs_to_docs(repo_root: Path, records: list[FileRecord]) -> dict[str, Any]:
    canonical_results = []
    for rel in CANONICAL_DOCS:
        path = repo_root / rel
        text, _truncated, error = (
            read_text(path, max_chars=220_000) if path.exists() else ("", False, "missing")
        )
        missing_terms = [term for term in CONTRACT_TERMS if term not in text]
        canonical_results.append(
            {
                "path": rel,
                "exists": path.exists(),
                "missing_terms": missing_terms,
                "error": error or "",
            }
        )
    heading_index: dict[str, list[str]] = {}
    for record in records:
        if record.kind != "doc":
            continue
        for heading in record.headings:
            normalized = heading.strip().lower()
            if len(normalized) >= 6:
                heading_index.setdefault(normalized, []).append(record.path)
    duplicates = [
        {"heading": heading, "docs": paths[:12], "count": len(paths)}
        for heading, paths in sorted(heading_index.items())
        if len(paths) > 4
    ][:80]
    return {
        "canonical_doc_count": len(CANONICAL_DOCS),
        "canonical_docs": canonical_results,
        "canonical_missing_count": sum(
            1 for item in canonical_results if item["missing_terms"] or not item["exists"]
        ),
        "duplicate_heading_count": len(duplicates),
        "duplicate_headings": duplicates,
    }

def compare_code_to_code(records: list[FileRecord]) -> dict[str, Any]:
    symbol_index: dict[str, list[str]] = {}
    for record in records:
        if record.kind != "code":
            continue
        for symbol in record.symbols:
            symbol_index.setdefault(symbol, []).append(record.path)
    duplicates = [
        {"symbol": symbol, "paths": paths[:16], "count": len(paths)}
        for symbol, paths in sorted(symbol_index.items())
        if len(paths) > 1 and symbol not in COMMON_DUPLICATE_SYMBOLS
    ][:160]
    return {
        "symbol_count": len(symbol_index),
        "duplicate_symbol_count": len(duplicates),
        "duplicate_symbols": duplicates,
        "provider_functions": discover_provider_functions(records),
    }

def deterministic_findings(
    reports: list[dict[str, Any]],
    doc_code: dict[str, Any],
    doc_doc: dict[str, Any],
    code_code: dict[str, Any],
    sqlite_memory: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    failed_reports = [r for r in reports if r.get("passed") is False]
    missing_reports = [r for r in reports if not r.get("exists")]
    if failed_reports:
        findings.append(
            {
                "severity": "high",
                "area": "validation_reports",
                "title": "Some validation reports are failing",
                "details": [f"{r['path']}: {r.get('errors')}" for r in failed_reports[:10]],
            }
        )
    if missing_reports:
        findings.append(
            {
                "severity": "medium",
                "area": "validation_reports",
                "title": "Some expected validation reports are missing",
                "details": [r["path"] for r in missing_reports[:16]],
            }
        )
    if doc_code.get("missing_path_reference_count", 0):
        findings.append(
            {
                "severity": "medium",
                "area": "doc_code",
                "title": "Markdown references missing repository paths",
                "details": [
                    f"{item['doc']} -> {item['reference']}"
                    for item in doc_code["missing_path_references"][:30]
                ],
            }
        )
    if doc_doc.get("canonical_missing_count", 0):
        findings.append(
            {
                "severity": "medium",
                "area": "doc_doc",
                "title": "Canonical docs are missing expected contract terms",
                "details": [
                    f"{item['path']}: {item['missing_terms']}"
                    for item in doc_doc["canonical_docs"]
                    if item.get("missing_terms") or not item.get("exists")
                ],
            }
        )
    if code_code.get("duplicate_symbol_count", 0):
        findings.append(
            {
                "severity": "low",
                "area": "code_code",
                "title": "Duplicate code symbols may deserve consolidation review",
                "details": [
                    f"{item['symbol']} -> {item['paths']}"
                    for item in code_code["duplicate_symbols"][:30]
                ],
            }
        )
    sqlite_errors = [item for item in sqlite_memory if item.get("error")]
    if sqlite_errors:
        findings.append(
            {
                "severity": "low",
                "area": "sqlite_memory",
                "title": "Some SQLite memory databases could not be read in read-only mode",
                "details": [f"{item['path']}: {item['error']}" for item in sqlite_errors[:12]],
            }
        )
    if not findings:
        findings.append(
            {
                "severity": "info",
                "area": "baseline",
                "title": "No deterministic blocking discrepancy found",
                "details": [
                    "Use --use-ollama for semantic review across collected all-resource summary."
                ],
            }
        )
    return findings

def compact_records(records: list[FileRecord], *, limit: int) -> list[dict[str, Any]]:
    return [
        {
            "path": r.path,
            "kind": r.kind,
            "extension": r.extension,
            "lines": r.lines,
            "chars": r.chars,
            "symbols": list(r.symbols[:30]),
            "headings": list(r.headings[:16]),
        }
        for r in records[:limit]
    ]
