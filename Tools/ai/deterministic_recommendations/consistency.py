from __future__ import annotations

from .common import *  # noqa: F403

def severity_rank(value: Any) -> int:
    return {"high": 0, "medium": 1, "low": 2}.get(str(value or "").lower(), 3)

def finding_priority(finding: dict[str, Any]) -> tuple[int, int, str, int]:
    kind = str(finding.get("kind") or "")
    return (
        severity_rank(finding.get("severity")),
        SUBSTANTIVE_CONSISTENCY_FINDING_PRIORITIES.get(kind, 999),
        normalize_repo_path(finding.get("source")),
        int(finding.get("line") or 0),
    )

def is_cosmetic_consistency_finding(finding: dict[str, Any]) -> bool:
    text = " ".join(
        str(finding.get(key) or "")
        for key in (
            "kind",
            "severity",
            "source",
            "target",
            "flag",
            "evidence",
            "recommendation",
        )
    ).lower()
    return any(keyword in text for keyword in COSMETIC_FINDING_KEYWORDS)

def finding_source_path(finding: dict[str, Any]) -> str:
    return normalize_repo_path(finding.get("source") or finding.get("source_path"))

def finding_target_path(finding: dict[str, Any]) -> str:
    return normalize_repo_path(finding.get("target") or finding.get("target_path"))

def finding_patch_target_file(finding: dict[str, Any]) -> str:
    area = consistency_area(str(finding.get("kind") or ""))
    source = finding_source_path(finding)
    target = finding_target_path(finding)
    # For documentation reference findings, the patch target is the document
    # containing the stale reference, not the missing referenced artifact.
    if area in {"doc_doc", "doc_python"}:
        return source
    return source or target

def is_patchable_consistency_finding(finding: dict[str, Any], repo_root: Path) -> bool:
    path = finding_patch_target_file(finding)
    return bool(path) and target_path_error(path, repo_root) is None

def consistency_target_file(finding: dict[str, Any], repo_root: Path) -> tuple[str, str | None]:
    patch_target = finding_patch_target_file(finding)
    if patch_target:
        patch_error = target_path_error(patch_target, repo_root)
        if patch_error is None:
            return patch_target, None
        return "", f"patch target {patch_target!r}: {patch_error}"
    return "", "finding has neither source/source_path nor target/target_path"

def consistency_area(kind: str) -> str:
    if kind in {"python_import_missing", "python_import_symbol_missing"}:
        return "python_python"
    if kind in {
        "md_python_command_script_missing",
        "md_cli_arg_not_in_argparse",
        "md_mentions_missing_python_path",
        "md_mentions_missing_powershell_path",
    }:
        return "doc_python"
    if kind == "md_mentions_missing_markdown_path":
        return "doc_doc"
    if kind == "documented_python_script_without_obvious_smoke":
        return "python_doc"
    if kind.startswith("policy_"):
        return "policy_violation"
    if "evidence" in kind:
        return "evidence_gap"
    return "refactor_candidate"

def consistency_validation_commands(target_file: str) -> list[str]:
    commands = list(DEFAULT_VALIDATION_COMMANDS)
    if target_file.endswith(".py"):
        commands.insert(0, f"python -m py_compile {target_file}")
    return commands

def repository_consistency_recommendation(
    *,
    finding: dict[str, Any],
    index: int,
    repo_root: Path,
    tool_refs: list[dict[str, Any]],
    npu_refs: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    kind = str(finding.get("kind") or "")
    if kind not in SUBSTANTIVE_CONSISTENCY_FINDING_PRIORITIES:
        return None, {
            "id": f"consistency_{index:03d}",
            "reason": f"unsupported finding kind: {kind}",
        }
    if is_cosmetic_consistency_finding(finding):
        return None, {
            "id": f"consistency_{index:03d}",
            "reason": "cosmetic/whitespace-only finding skipped",
        }
    target_file, target_error = consistency_target_file(finding, repo_root)
    if target_error:
        return None, {"id": f"consistency_{index:03d}", "reason": target_error}

    source = finding_source_path(finding)
    target = finding_target_path(finding)
    flag = str(finding.get("flag") or "")
    line = int(finding.get("line") or 0)
    severity = str(finding.get("severity") or "medium")
    evidence = str(finding.get("evidence") or "")
    recommendation = str(
        finding.get("recommendation")
        or "Resolve the repository consistency finding with the narrowest safe patch."
    )
    area = consistency_area(kind)
    risk = "medium" if severity == "high" else "low"
    evidence_label = f"{source}:{line}" if line else source or target_file
    mismatch = flag or target or kind
    strategy = (
        f"Build a focused patch plan for `{kind}` using mapper evidence `{evidence_label}`. "
        f"Target `{target_file}` and resolve `{mismatch}` without formatting-only edits. "
        f"Mapper recommendation: {recommendation}"
    )

    return (
        {
            "id": f"consistency_{index:03d}",
            "area": area,
            "status": "ready_for_patch_plan",
            "target_files": [target_file],
            "rationale": f"Repository consistency mapper reported {severity} `{kind}` at `{evidence_label}` targeting `{mismatch}`.",
            "proposed_strategy": strategy,
            "risk": risk,
            "validation_commands": consistency_validation_commands(target_file),
            "stop_conditions": [
                "Stop if the edit is only whitespace, tag spacing or Markdown formatting without fixing the cited finding.",
                "Stop if the target/source evidence no longer exists after refreshing master.",
                "Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.",
                "Stop if resolving the finding requires inventing behavior not supported by code evidence.",
            ],
            "source": "repository_consistency_map",
            "evidence": [evidence_label] if evidence_label else [],
            "tool_evidence": tool_refs,
            "npu_audit_refs": npu_refs,
            "repository_consistency_finding": {
                "kind": kind,
                "severity": severity,
                "source": source,
                "line": line,
                "target": target,
                "flag": flag,
                "evidence": evidence[:500],
            },
            "guardrails": {
                "patch_application_performed": False,
                "manual_review_required": True,
                "cosmetic_patch_allowed": False,
            },
        },
        None,
    )

def area_diverse_findings(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return findings in round-robin area order for ALL_ALL product diversity."""
    preferred_areas = [
        "python_python",
        "doc_python",
        "doc_doc",
        "python_doc",
        "policy_violation",
        "refactor_candidate",
        "evidence_gap",
    ]
    by_area: dict[str, list[dict[str, Any]]] = {area: [] for area in preferred_areas}
    other: list[dict[str, Any]] = []
    for finding in sorted(findings, key=finding_priority):
        area = consistency_area(str(finding.get("kind") or ""))
        if area in by_area:
            by_area[area].append(finding)
        else:
            other.append(finding)
    ordered: list[dict[str, Any]] = []
    while any(by_area.values()):
        for area in preferred_areas:
            bucket = by_area[area]
            if bucket:
                ordered.append(bucket.pop(0))
    ordered.extend(other)
    return ordered

def area_diverse_items(items: list[dict[str, Any]], *, limit: int) -> list[dict[str, Any]]:
    """Round-robin items by product area while preserving relative order within each area."""
    preferred_areas = [
        "python_python",
        "doc_python",
        "doc_doc",
        "python_doc",
        "policy_violation",
        "refactor_candidate",
        "evidence_gap",
    ]
    by_area: dict[str, list[dict[str, Any]]] = {area: [] for area in preferred_areas}
    other: list[dict[str, Any]] = []
    for item in items:
        area = str(item.get("area") or "")
        if area in by_area:
            by_area[area].append(item)
        else:
            other.append(item)
    selected: list[dict[str, Any]] = []
    while len(selected) < limit and any(by_area.values()):
        for area in preferred_areas:
            bucket = by_area[area]
            if bucket and len(selected) < limit:
                selected.append(bucket.pop(0))
    for item in other:
        if len(selected) >= limit:
            break
        selected.append(item)
    return selected

def synthesize_from_repository_consistency_maps(
    *,
    repository_maps: list[dict[str, Any]],
    repo_root: Path,
    npu_refs: list[dict[str, Any]],
    tool_refs: list[dict[str, Any]],
    max_recommendations: int,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    findings: list[dict[str, Any]] = []
    for repository_map in repository_maps:
        raw_findings = repository_map.get("findings")
        if not isinstance(raw_findings, list):
            continue
        for item in raw_findings:
            if isinstance(item, dict):
                findings.append(item)
    skipped: list[dict[str, str]] = []
    raw_finding_count = len(findings)
    patchable_findings = [
        finding for finding in findings if is_patchable_consistency_finding(finding, repo_root)
    ]
    skipped_unpatchable_count = raw_finding_count - len(patchable_findings)
    if skipped_unpatchable_count:
        skipped.append(
            {
                "id": "repository_consistency_unpatchable_filtered",
                "reason": f"filtered {skipped_unpatchable_count} generated/runtime/non-patchable consistency findings before area selection",
            }
        )
    findings = area_diverse_findings(patchable_findings)

    recommendations: list[dict[str, Any]] = []
    seen_targets: set[tuple[str, str, str]] = set()
    for index, finding in enumerate(findings, start=1):
        if len(recommendations) >= max_recommendations:
            break
        rec, skip = repository_consistency_recommendation(
            finding=finding,
            index=index,
            repo_root=repo_root,
            tool_refs=tool_refs,
            npu_refs=npu_refs,
        )
        if skip:
            skipped.append(skip)
        if not rec:
            continue
        dedupe_key = (
            str(rec.get("area")),
            str(rec.get("target_files")),
            str(rec.get("rationale")),
        )
        if dedupe_key in seen_targets:
            continue
        errors = recommendation_schema_errors(rec, len(recommendations), repo_root)
        if errors:
            skipped.append({"id": str(rec.get("id")), "reason": "; ".join(errors)})
            continue
        seen_targets.add(dedupe_key)
        recommendations.append(rec)
    return recommendations, skipped
