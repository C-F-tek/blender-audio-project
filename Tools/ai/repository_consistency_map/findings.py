"""Finding construction for repository consistency maps."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from Tools.ai.repository_consistency_map.python_inventory import smoke_candidates_for_script


PLANNED_SHARED_UTILITY_DOC = "docs/SHARED_SCRIPTING_UTILITIES.md"
PLANNED_SHARED_PREFIX = "Scripting/shared/"
PLANNED_SHARED_BASENAMES = {
    "config_model.py",
    "hotpatch_base.py",
    "panel_base.py",
    "scene_registry.py",
}
GENERATED_CONTEXT_PREFIXES = (
    "Tools/npu/npu_code_chunks/",
    "npu_code_chunks/",
    "indexAI/project_code_chunks/",
    "indexAI/code_chunks/",
)
GENERATED_CONTEXT_GLOB_PREFIXES = (
    "Tools/npu/npu_code_chunks/chunk_",
    "npu_code_chunks/chunk_",
)


def normalized_path(value: Any) -> str:
    """Return a normalized repository path string."""
    return str(value or "").replace("\\", "/").strip().strip("`")


def is_planned_shared_utility_reference(ref: dict[str, Any]) -> bool:
    """Return true for documented future shared utility modules.

    `docs/SHARED_SCRIPTING_UTILITIES.md` contains roadmap sections such as
    "Target shared modules" and "Extraction candidates". Several entries
    intentionally name modules that may not exist yet, for example
    `Scripting/shared/config_model.py` or the bare target `panel_base.py`.
    Those should remain visible as planned work, but they should not be
    escalated as high-severity stale documentation defects.
    """
    source = normalized_path(ref.get("source"))
    target = normalized_path(ref.get("raw_ref"))
    evidence = str(ref.get("snippet") or "")
    if source != PLANNED_SHARED_UTILITY_DOC or not target.endswith(".py"):
        return False
    if target.startswith(PLANNED_SHARED_PREFIX):
        return "Target shared modules" in evidence or "Scripting/shared/" in evidence
    if "/" not in target and target in PLANNED_SHARED_BASENAMES:
        return any(
            marker in evidence
            for marker in (
                "Target shared modules",
                "Extraction candidates",
                "Scripting/shared/",
                "panel_base.py",
                "hotpatch_base.py",
            )
        )
    return False


def is_generated_context_reference(ref: dict[str, Any]) -> bool:
    """Return true for generated/index context paths referenced from docs."""
    target = normalized_path(ref.get("raw_ref"))
    source = normalized_path(ref.get("source"))
    if not source.startswith("Tools/npu/"):
        return False
    if any(target.startswith(prefix) for prefix in GENERATED_CONTEXT_PREFIXES):
        return True
    if "*" in target and any(target.startswith(prefix) for prefix in GENERATED_CONTEXT_GLOB_PREFIXES):
        return True
    return False


def missing_reference_finding(ref: dict[str, Any]) -> dict[str, Any]:
    """Build a semantically classified missing-reference finding."""
    if is_planned_shared_utility_reference(ref):
        return {
            "kind": "md_mentions_planned_python_path",
            "severity": "low",
            "source": ref["source"],
            "line": ref["line"],
            "target": ref["raw_ref"],
            "evidence": ref["snippet"],
            "recommendation": (
                "Keep as planned shared-utility roadmap item until the module is "
                "implemented or intentionally removed from the roadmap."
            ),
            "classification": "planned_missing_reference",
            "patch_recommendation": "manual_review_only",
        }

    if is_generated_context_reference(ref):
        return {
            "kind": "md_mentions_generated_context_markdown_path",
            "severity": "low",
            "source": ref["source"],
            "line": ref["line"],
            "target": ref["raw_ref"],
            "evidence": ref["snippet"],
            "recommendation": (
                "Regenerate the context/chunk artifact when needed; do not create "
                "or edit generated chunk files by hand."
            ),
            "classification": "generated_context_reference",
            "patch_recommendation": "regenerate_source_artifact",
        }

    severity = "high" if ref["kind"] in {"python", "powershell"} else "medium"
    return {
        "kind": f"md_mentions_missing_{ref['kind']}_path",
        "severity": severity,
        "source": ref["source"],
        "line": ref["line"],
        "target": ref["raw_ref"],
        "evidence": ref["snippet"],
        "recommendation": "Correct the documentation reference or restore the missing target if it is still required.",
    }


def build_findings(
    *,
    md_refs: list[dict[str, Any]],
    md_commands: list[dict[str, Any]],
    py_inventory: dict[str, dict[str, Any]],
    import_findings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for ref in md_refs:
        if ref["kind"] in {"python", "powershell", "markdown"} and not ref["exists"]:
            findings.append(missing_reference_finding(ref))
    for command in md_commands:
        if not command["script_exists"]:
            findings.append(
                {
                    "kind": "md_python_command_script_missing",
                    "severity": "high",
                    "source": command["source"],
                    "line": command["line"],
                    "target": command["script_raw"],
                    "evidence": command["snippet"],
                    "recommendation": "Update the command to a real script path or remove the obsolete command.",
                }
            )
            continue
        script = command["script_resolved"]
        known_flags = set(py_inventory.get(script, {}).get("argparse_flags", []))
        for flag in command["flags"]:
            if known_flags and flag not in known_flags:
                findings.append(
                    {
                        "kind": "md_cli_arg_not_in_argparse",
                        "severity": "medium",
                        "source": command["source"],
                        "line": command["line"],
                        "target": script,
                        "flag": flag,
                        "known_flags_sample": sorted(known_flags)[:40],
                        "evidence": command["snippet"],
                        "recommendation": "Correct the documented CLI flag or update the script argparse contract in a focused PR.",
                    }
                )
    for item in import_findings:
        findings.append(
            {
                "kind": item["kind"],
                "severity": "high",
                "source": item["source"],
                "line": item["line"],
                "target": item["module"],
                "evidence": f"local import `{item['module']}` cannot be resolved to a repository Python module",
                "recommendation": "Fix the import or add the missing module in a focused code PR.",
            }
        )
    all_py = sorted(py_inventory)
    cited_scripts = sorted({command["script_resolved"] for command in md_commands if command.get("script_exists")})
    for script in cited_scripts:
        if script not in py_inventory:
            continue
        if not smoke_candidates_for_script(script, all_py):
            findings.append(
                {
                    "kind": "documented_python_script_without_obvious_smoke",
                    "severity": "low",
                    "source": script,
                    "line": 0,
                    "target": script,
                    "evidence": "Script is cited by documentation commands but no obvious smoke/check/test file references its stem under Tools/validation.",
                    "recommendation": "Consider adding a smoke validator or documenting why none is needed.",
                }
            )
    return findings


def build_provider_hints(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_kind: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for finding in findings:
        by_kind[str(finding.get("kind"))].append(finding)
    hints: list[dict[str, Any]] = []
    for kind, items in sorted(by_kind.items(), key=lambda pair: (-len(pair[1]), pair[0])):
        targets = sorted({str(item.get("target") or item.get("source") or "") for item in items if item.get("target") or item.get("source")})
        sources = sorted({str(item.get("source") or "") for item in items if item.get("source")})
        hints.append(
            {
                "kind": kind,
                "count": len(items),
                "severity_counts": dict(Counter(str(item.get("severity")) for item in items)),
                "sample_sources": sources[:12],
                "sample_targets": targets[:12],
                "planner_instruction": "Prioritize concrete patch plans that correct the cited source/target pairs without touching generated output, SQLite, provider settings or Blender runtime.",
            }
        )
    return hints
