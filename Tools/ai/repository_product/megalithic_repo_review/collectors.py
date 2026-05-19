from __future__ import annotations

from .common import *  # noqa: F403

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
                "errors": (
                    data.get("errors", [])[:10]
                    if isinstance(data, dict) and isinstance(data.get("errors", []), list)
                    else []
                ),
                "warnings": (
                    data.get("warnings", [])[:10]
                    if isinstance(data, dict) and isinstance(data.get("warnings", []), list)
                    else []
                ),
                "provider_execution_performed": (
                    data.get("provider_execution_performed") if isinstance(data, dict) else None
                ),
                "error": item.get("error"),
            }
        )
    return reports

def collect_raw_artifacts(
    repo_root: Path, raw_files: list[Path], *, max_raw_files: int
) -> list[dict[str, Any]]:
    artifacts = []
    for path in raw_files[:max_raw_files]:
        rel = path.relative_to(repo_root).as_posix()
        text, truncated, error = read_text(path, max_chars=24_000)
        json_kind = None
        if path.suffix.lower() == ".json":
            data = read_json_if_exists(path).get("data")
            json_kind = data.get("kind") if isinstance(data, dict) else None
        artifacts.append(
            {
                "path": rel,
                "extension": path.suffix.lower(),
                "chars": len(text),
                "lines": len(text.splitlines()),
                "truncated": truncated,
                "error": error or "",
                "json_kind": json_kind,
            }
        )
    return artifacts

def inspect_sqlite_memory(
    repo_root: Path, sqlite_files: list[Path], *, max_tables: int
) -> list[dict[str, Any]]:
    out = []
    for path in sqlite_files:
        rel = path.relative_to(repo_root).as_posix()
        item: dict[str, Any] = {
            "path": rel,
            "read_only": True,
            "tables": [],
            "error": "",
        }
        try:
            uri = f"file:{path.as_posix()}?mode=ro"
            with sqlite3.connect(uri, uri=True) as conn:
                rows = conn.execute(
                    "select name from sqlite_master where type='table' order by name"
                ).fetchall()
                for (name,) in rows[:max_tables]:
                    try:
                        count = conn.execute(f"select count(*) from {json.dumps(name)}").fetchone()[
                            0
                        ]
                    except Exception:
                        count = None
                    item["tables"].append({"name": name, "row_count": count})
        except Exception as exc:
            item["error"] = f"{type(exc).__name__}: {exc}"
        out.append(item)
    return out

def discover_provider_functions(records: list[FileRecord]) -> dict[str, Any]:
    lanes: dict[str, list[dict[str, Any]]] = {"npu": [], "gpu_cuda": [], "cpu": []}
    for record in records:
        searchable = " ".join([record.path, *record.symbols])
        for lane, terms in PROVIDER_TERMS.items():
            if any(term in searchable for term in terms):
                lanes[lane].append(
                    {
                        "path": record.path,
                        "symbols": list(record.symbols[:40]),
                        "lines": record.lines,
                    }
                )
                break
    return {lane: items[:80] for lane, items in lanes.items()}

def scan_doc_references(repo_root: Path, docs: Iterable[Path]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for doc in docs:
        text, _truncated, error = read_text(doc)
        if error:
            continue
        doc_rel = doc.relative_to(repo_root).as_posix()
        for match in PATH_RE.findall(text):
            normalized = match.strip('`.,:)];"').replace("\\", "/")
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
