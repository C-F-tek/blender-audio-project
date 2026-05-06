#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any] | None:
    try:
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return None


def resolve(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def boolish(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1"}:
            return True
        if lowered in {"false", "no", "0"}:
            return False
    return None


def scan_for_keys(data: Any, keys: set[str]) -> dict[str, list[Any]]:
    found: dict[str, list[Any]] = {key: [] for key in keys}
    def walk(item: Any) -> None:
        if isinstance(item, dict):
            for key, value in item.items():
                if key in found:
                    found[key].append(value)
                walk(value)
        elif isinstance(item, list):
            for value in item:
                walk(value)
    walk(data)
    return found


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Full0To10 Provider Acceptance Gate", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Stamp: `{report['stamp']}`")
    lines.append(f"- Classification count: `{len(report['classifications'])}`")
    lines.append("")
    lines.append("## Classifications")
    lines.append("")
    if report["classifications"]:
        for item in report["classifications"]:
            lines.append(f"- `{item}`")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Evidence")
    lines.append("")
    for item in report["evidence"]:
        lines.append(f"- `{item['path']}` exists=`{item['exists']}` passed=`{item.get('passed')}`")
    lines.append("")
    if report["errors"]:
        lines.append("## Errors")
        lines.append("")
        for item in report["errors"]:
            lines.append(f"- {item}")
        lines.append("")
    if report["warnings"]:
        lines.append("## Warnings")
        lines.append("")
        for item in report["warnings"]:
            lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--gpu0-provider-support", default="")
    parser.add_argument("--gpu0-final-workload", default="")
    parser.add_argument("--evidence-sufficiency", default="output/ai_pipeline/agent_review_evidence_sufficiency.json")
    parser.add_argument("--workload-quality", default="output/validation/ai_workload_quality_lane_routing.json")
    parser.add_argument("--repository-suggestions-manifest", default="output/ai_pipeline/repository_update_suggestions_manifest.json")
    parser.add_argument("--output", default="output/validation/full0to10_provider_acceptance.json")
    parser.add_argument("--markdown-output", default="output/validation/full0to10_provider_acceptance.md")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    classifications: list[str] = []
    errors: list[str] = []
    warnings: list[str] = []
    evidence: list[dict[str, Any]] = []

    paths = {
        "gpu0_provider_support": args.gpu0_provider_support,
        "gpu0_final_workload": args.gpu0_final_workload,
        "evidence_sufficiency": args.evidence_sufficiency,
        "workload_quality": args.workload_quality,
        "repository_suggestions_manifest": args.repository_suggestions_manifest,
    }

    loaded: dict[str, dict[str, Any] | None] = {}
    for name, value in paths.items():
        if not value:
            loaded[name] = None
            evidence.append({"name": name, "path": "", "exists": False, "passed": None})
            continue
        path = resolve(repo_root, value)
        data = load_json(path)
        loaded[name] = data
        evidence.append({"name": name, "path": rel(repo_root, path), "exists": path.exists(), "passed": data.get("passed") if isinstance(data, dict) else None})

    gpu0_support = loaded.get("gpu0_provider_support")
    if not gpu0_support or not gpu0_support.get("passed"):
        classifications.append("gpu0_support_lane_not_integrated")
        errors.append("GPU0 provider support lane report is missing or not passed.")
    else:
        if not gpu0_support.get("openvino_gpu0_support_lane"):
            classifications.append("gpu0_support_lane_not_integrated")
            errors.append("GPU0 report passed but is not marked as provider support lane.")
        if not gpu0_support.get("openvino_gpu0_sustained_workload_performed"):
            classifications.append("gpu0_sustained_workload_not_performed")
            warnings.append("GPU0 support lane passed but did not perform sustained workload.")

    sufficiency = loaded.get("evidence_sufficiency")
    if sufficiency and sufficiency.get("passed") is False:
        for item in sufficiency.get("errors", []) or []:
            if "blocked_missing_refined_review_input" in str(item):
                classifications.append("blocked_missing_refined_review_input")
                errors.append(str(item))
    elif sufficiency is None:
        classifications.append("blocked_missing_refined_review_input")
        errors.append("Evidence sufficiency report is missing.")

    provider_keys = {
        "primary_advisory_provider_execution_requested",
        "ollama_advisory_execution_used",
        "provider_execution_requested",
        "provider_execution_performed",
        "ollama_probe_passed",
    }
    for source_name in ("workload_quality", "repository_suggestions_manifest"):
        data = loaded.get(source_name)
        if not isinstance(data, dict):
            continue
        found = scan_for_keys(data, provider_keys)
        for value in found.get("primary_advisory_provider_execution_requested", []):
            if boolish(value) is False:
                classifications.append("primary_advisory_not_executed")
                errors.append(f"{source_name}: primary advisory provider execution requested is false")
        for value in found.get("ollama_advisory_execution_used", []):
            if boolish(value) is False:
                classifications.append("primary_advisory_not_executed")
                errors.append(f"{source_name}: Ollama advisory execution used is false")
        for value in found.get("ollama_probe_passed", []):
            if boolish(value) is False:
                classifications.append("ollama_probe_failed")
                errors.append(f"{source_name}: Ollama probe failed")

    # Fallback textual scan for reports that encode status in prose.
    prose_paths = [resolve(repo_root, args.workload_quality), resolve(repo_root, args.repository_suggestions_manifest)]
    for path in prose_paths:
        if path.exists():
            text = path.read_text(encoding="utf-8-sig", errors="replace")
            if "Primary advisory provider execution requested: False" in text:
                classifications.append("primary_advisory_not_executed")
            if "Ollama advisory execution used: False" in text or "Ollama probe did not pass" in text:
                classifications.append("ollama_probe_failed")

    unique_classifications = sorted(set(classifications))
    passed = not unique_classifications
    report = {
        "schema_version": 1,
        "kind": "full0to10_provider_acceptance_gate",
        "stamp": args.stamp,
        "repo_root": str(repo_root),
        "passed": passed,
        "classifications": unique_classifications,
        "errors": errors,
        "warnings": warnings,
        "evidence": evidence,
        "provider_execution_performed": bool(gpu0_support and gpu0_support.get("provider_execution_performed")),
        "patch_application_performed": False,
        "source_writes_performed": False,
        "guardrails": {
            "report_only": True,
            "acceptance_requires_empty_classifications": True,
        },
    }

    output = resolve(repo_root, args.output)
    markdown = resolve(repo_root, args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": passed, "classifications": unique_classifications, "output": str(output), "markdown": str(markdown)}, indent=2))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
