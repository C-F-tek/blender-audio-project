"""Manifest assembly for proposal-derived patch specs."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .proposal_common import (
    DEFAULT_GUARDRAILS,
    EXPECTED_APPLY_MODE,
    EXPECTED_PROPOSAL_KIND,
    MANIFEST_KIND,
    SPEC_KIND,
    read_json_object,
    repo_relative,
    sanitize_filename,
)
from .proposal_operations import build_spec_for_proposal

def render_manifest_markdown(manifest: dict[str, Any]) -> str:
    lines = ["# Proposal Patch Spec Drafts", ""]
    lines.append(f"- Generated at: `{manifest['generated_at']}`")
    lines.append(f"- Source proposal report: `{manifest['source_proposal_report']}`")
    lines.append(f"- Patch spec count: `{manifest['patch_spec_count']}`")
    lines.append(f"- Concrete spec count: `{manifest['concrete_spec_count']}`")
    lines.append(f"- Skipped target count: `{manifest['skipped_target_count']}`")
    lines.append(f"- Provider execution performed: `{manifest['provider_execution_performed']}`")
    lines.append(f"- Provider execution claim seen: `{manifest['provider_execution_claim_seen']}`")
    lines.append("")
    lines.append("## Specs")
    lines.append("")
    if manifest["specs"]:
        for item in manifest["specs"]:
            lines.append(
                f"- `{item['proposal_id']}` -> `{item['path']}` "
                f"({item['operation_count']} target operations, status `{item['draft_status']}`)"
            )
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Skipped targets")
    lines.append("")
    if manifest["skipped_targets"]:
        for item in manifest["skipped_targets"]:
            path = item.get("path") or "(proposal)"
            lines.append(f"- `{item.get('proposal_id')}` `{path}`: {item.get('reason')}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Guardrail")
    lines.append("")
    lines.append(
        "Specs remain review-only. Concrete operations are deterministic candidates, not an automatic merge."
    )
    return "\n".join(lines) + "\n"

def build_patch_specs(
    *,
    repo_root: Path,
    proposal_path: Path,
    output_dir: Path,
    basename: str,
    max_proposals: int | None,
    require_concrete: bool = False,
    require_provider_execution: bool = False,
) -> dict[str, Any]:
    proposal_report = read_json_object(proposal_path)
    errors: list[str] = []
    warnings: list[str] = []
    if proposal_report.get("kind") != EXPECTED_PROPOSAL_KIND:
        errors.append(f"proposal report kind must be {EXPECTED_PROPOSAL_KIND}")
    if proposal_report.get("apply_mode") != EXPECTED_APPLY_MODE:
        errors.append("proposal report apply_mode must be manual_review_only")

    proposal_report_provider_execution_claim_seen = bool(
        proposal_report.get("provider_execution_performed")
        or proposal_report.get("provider_execution_attempted")
        or proposal_report.get("provider_io_observed")
    )
    proposal_report_provider_execution_seen = bool(proposal_report.get("provider_work_verified"))

    proposals = proposal_report.get("proposals")
    if not isinstance(proposals, list):
        errors.append("proposal report proposals must be a list")
        proposals = []

    provider_execution_claim_seen = proposal_report_provider_execution_claim_seen or any(
        bool(
            item.get("provider_execution_performed")
            or item.get("provider_execution_attempted")
            or item.get("provider_io_observed")
        )
        for item in proposals
        if isinstance(item, dict)
    )
    provider_execution_seen = proposal_report_provider_execution_seen or any(
        bool(item.get("provider_work_verified"))
        for item in proposals
        if isinstance(item, dict)
    )
    if require_provider_execution and not provider_execution_seen:
        errors.append(
            "provider execution is required for real-product generated patch specs; "
            "proposal report did not prove provider_work_verified=true"
        )

    spec_dir = output_dir / basename
    spec_dir.mkdir(parents=True, exist_ok=True)
    specs: list[dict[str, Any]] = []
    skipped_targets: list[dict[str, str]] = []

    proposal_items = proposals[:max_proposals] if max_proposals is not None else proposals
    for item in proposal_items:
        if not isinstance(item, dict):
            skipped_targets.append(
                {
                    "proposal_id": "unknown",
                    "path": "",
                    "reason": "proposal item is not an object",
                }
            )
            continue
        proposal_id = str(item.get("id") or "proposal")
        spec, skipped = build_spec_for_proposal(
            proposal=item,
            proposal_report_path=proposal_path,
            repo_root=repo_root,
        )
        skipped_targets.extend({"proposal_id": proposal_id, **target} for target in skipped)
        if spec is None:
            continue
        spec_path = spec_dir / f"{sanitize_filename(proposal_id)}.json"
        spec_path.write_text(
            json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        specs.append(
            {
                "proposal_id": proposal_id,
                "path": repo_relative(spec_path, repo_root),
                "kind": SPEC_KIND,
                "draft_status": spec["draft_status"],
                "operation_count": len(spec["operations"]),
                "concrete_operation_count": sum(
                    1
                    for op in spec["operations"]
                    if op.get("draft_status") == "concrete_review_ready"
                ),
                "operations": [
                    {
                        "path": op["path"],
                        "artifact_kind": op.get("artifact_kind"),
                        "operation": op.get("operation"),
                        "draft_status": op.get("draft_status"),
                    }
                    for op in spec["operations"]
                ],
            }
        )

    concrete_spec_count = sum(1 for item in specs if item.get("concrete_operation_count", 0) > 0)
    if require_concrete and concrete_spec_count <= 0:
        errors.append(
            "concrete patch specs are required for this real-product run; "
            "metadata-only fallback is disabled"
        )
    manifest = {
        "schema_version": 1,
        "kind": MANIFEST_KIND,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "source_proposal_report": repo_relative(proposal_path, repo_root),
        "output_dir": repo_relative(spec_dir, repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": provider_execution_seen,
        "provider_execution_claim_seen": provider_execution_claim_seen,
        "provider_work_verified": provider_execution_seen,
        "provider_execution_required": bool(require_provider_execution),
        "concrete_patch_specs_required": bool(require_concrete),
        "metadata_fallback_enabled": not bool(require_concrete),
        "apply_mode": EXPECTED_APPLY_MODE,
        "draft_status": (
            "concrete_review_ready" if concrete_spec_count else "needs_concrete_replacements"
        ),
        "patch_spec_count": len(specs),
        "concrete_spec_count": concrete_spec_count,
        "skipped_target_count": len(skipped_targets),
        "specs": specs,
        "skipped_targets": skipped_targets,
        "guardrails": DEFAULT_GUARDRAILS,
    }
    if not specs and not errors:
        manifest["warnings"].append("no concrete file targets produced draft specs")

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_json = output_dir / f"{basename}_manifest.json"
    manifest_md = output_dir / f"{basename}_manifest.md"
    manifest_json.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    manifest_md.write_text(render_manifest_markdown(manifest), encoding="utf-8")
    manifest["manifest_json"] = repo_relative(manifest_json, repo_root)
    manifest["manifest_markdown"] = repo_relative(manifest_md, repo_root)
    return manifest
