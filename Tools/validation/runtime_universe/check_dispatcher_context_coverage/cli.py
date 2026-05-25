"""Check macro-family context coverage for public dispatcher targets."""

from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path
from typing import Any

DISPATCHERS = (
    "ia_carmine.dispatch",
    "Tools.validation.dispatch",
    "Tools.workflow.dispatch",
    "Tools.npu.dispatch",
    "Tools.docs.dispatch",
    "Tools.git.dispatch",
    "Tools.repo_patch_runner.dispatch",
)


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    docs_text = _coverage_text(repo_root)
    families = _dispatcher_families(repo_root)
    missing: list[dict[str, Any]] = []
    stubs: list[dict[str, Any]] = []
    covered = 0
    for family in sorted(families.values(), key=lambda item: item["family"]):
        context = _nearest_context(repo_root, family["path"])
        area_index = _nearest_index(repo_root, family["path"])
        doc_mentioned = _mentioned(docs_text, family["family"])
        status = _coverage_status(docs_text, family["family"], context)
        item = {
            **family,
            "tool_context": _rel(repo_root, context) if context else "",
            "area_context_index": _rel(repo_root, area_index) if area_index else "",
            "mentioned_in_coverage_docs": doc_mentioned,
            "coverage_status": status,
        }
        if status in {"stub", "stub-missing", "partial"}:
            stubs.append(item)
        if context or area_index or doc_mentioned:
            covered += 1
        else:
            missing.append(item)
    warnings = [
        f"{len(stubs)} dispatcher families are partial/stub coverage; inspect source before relying on docs."
    ] if stubs else []
    report = {
        "schema_version": 1,
        "kind": "dispatcher_context_coverage_check",
        "passed": not missing,
        "repo_root": str(repo_root),
        "family_count": len(families),
        "covered_count": covered,
        "missing_count": len(missing),
        "missing": missing,
        "stub_count": len(stubs),
        "stubs": stubs,
        "warnings": warnings,
        "errors": [f"{item['family']}: missing context coverage" for item in missing],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }
    _write_report(repo_root, args.output, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="")
    return parser.parse_args()


def _dispatcher_families(repo_root: Path) -> dict[str, dict[str, Any]]:
    families: dict[str, dict[str, Any]] = {}
    for dispatcher in DISPATCHERS:
        try:
            module = importlib.import_module(dispatcher)
        except Exception:
            continue
        mapping = getattr(module, "TOOL_MAIN_TARGETS", None)
        if mapping is None:
            mapping = getattr(module, "TARGETS", {})
        if not isinstance(mapping, dict):
            continue
        visibility = getattr(module, "TOOL_VISIBILITY", {})
        if not isinstance(visibility, dict):
            visibility = {}
        for name, target in mapping.items():
            if visibility and visibility.get(name, "internal") == "internal":
                continue
            family, path = _family_from_target(repo_root, dispatcher, str(target))
            if not family:
                continue
            entry = families.setdefault(
                family,
                {
                    "family": family,
                    "path": _rel(repo_root, path),
                    "dispatchers": [],
                    "target_count": 0,
                },
            )
            if dispatcher not in entry["dispatchers"]:
                entry["dispatchers"].append(dispatcher)
            entry["target_count"] += 1
    return families


def _family_from_target(repo_root: Path, dispatcher: str, target: str) -> tuple[str, Path]:
    if target.startswith("ps1:"):
        area = dispatcher.removesuffix(".dispatch").replace(".", "/")
        path = repo_root / area / "_powershell"
        return f"{area}/_powershell", path
    module = target.split(":", 1)[0]
    parts = module.split(".")
    if not parts:
        return "", repo_root
    if parts[0] == "ia_carmine":
        family_parts = parts[:3] if len(parts) >= 3 else parts
    elif parts[0] == "Tools" and len(parts) >= 3:
        family_parts = parts[:3]
    else:
        family_parts = parts[:2]
    family = "/".join(family_parts)
    return family, repo_root / family


def _coverage_text(repo_root: Path) -> str:
    paths = [
        repo_root / "docs" / "CONTEXT_COVERAGE_STATUS.md",
        repo_root / "docs" / "DISPATCHER_CONTEXT_COVERAGE.md",
        repo_root / "docs" / "IA_UNIVERSE_MODEL_TO_CODE_MAP.md",
    ]
    return "\n".join(_read(path) for path in paths).lower()


def _mentioned(docs_text: str, family: str) -> bool:
    normalized = family.lower()
    return normalized in docs_text or normalized.replace("/", " ") in docs_text


def _coverage_status(docs_text: str, family: str, context: Path | None) -> str:
    family_l = family.lower()
    for status in ("stub-missing", "complete-enough", "partial", "stub", "deferred"):
        if family_l in docs_text and status in _nearby(docs_text, family_l):
            return status
    if context and context.exists():
        text = _read(context).lower()
        if "stub" in text:
            return "stub"
        return "context-present"
    return "undocumented"


def _nearby(text: str, needle: str, window: int = 220) -> str:
    pos = text.find(needle)
    if pos < 0:
        return ""
    return text[max(0, pos - window) : pos + len(needle) + window]


def _nearest_context(repo_root: Path, family_path: str) -> Path | None:
    path = repo_root / family_path
    candidates = [path, *path.parents]
    for candidate in candidates:
        if repo_root not in candidate.parents and candidate != repo_root:
            continue
        context = candidate / "TOOL_CONTEXT.md"
        if context.exists():
            return context
    return None


def _nearest_index(repo_root: Path, family_path: str) -> Path | None:
    path = repo_root / family_path
    candidates = [path, *path.parents]
    for candidate in candidates:
        if repo_root not in candidate.parents and candidate != repo_root:
            continue
        index = candidate / "CONTEXT_INDEX.md"
        if index.exists():
            return index
    return None


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return ""


def _write_report(repo_root: Path, output: str, report: dict[str, Any]) -> None:
    if not output:
        return
    path = Path(output)
    if not path.is_absolute():
        path = repo_root / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


if __name__ == "__main__":
    raise SystemExit(main())
