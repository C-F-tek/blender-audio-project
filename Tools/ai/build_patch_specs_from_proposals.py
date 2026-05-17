#!/usr/bin/env python3
"""Build repo patch specs from validated proposal reports.

By default, proposals remain inert metadata-only drafts. A proposal may also
carry reviewed concrete_operations; those are copied into the generated patch
spec only when they are allowlisted deterministic operations against safe,
existing repository files.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIR = "output/patch_specs"
DEFAULT_BASENAME = "proposal_patch_specs"
EXPECTED_PROPOSAL_KIND = "repository_change_proposals"
EXPECTED_APPLY_MODE = "manual_review_only"
SPEC_KIND = "proposal_patch_spec_draft"
MANIFEST_KIND = "proposal_patch_spec_manifest"

SUPPORTED_OUTPUT_KINDS = {
    "python_code",
    "markdown",
    "json",
    "powershell",
    "workflow_yaml",
    "text_or_config",
}

SKIPPED_OUTPUT_KINDS = {
    "path_group",
}

CONCRETE_OPERATION_NAMES = {
    "replace_once",
    "append_once",
    "insert_after_once",
    "insert_before_once",
    "write_file",
}

FORBIDDEN_TARGET_PREFIXES = (
    "indexAI/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
    "output/",
    "docs/LOCAL_VALIDATION_EVIDENCE/",
    "renders/",
    "Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/",
    "patch_specs/inbox/",
)

FORBIDDEN_TARGET_EXACT = {
    "Scripting/shared/blender_compat.py",
}

FORBIDDEN_TARGET_FRAGMENTS = (
    "full_analysis",
    "analysis_full",
)

DEFAULT_GUARDRAILS = [
    "Draft specs are metadata-only unless concrete_operations were explicitly supplied by a proposal.",
    "Do not copy drafts into patch_specs/inbox/ without explicit human approval.",
    "Run generated patch-spec apply in a review branch and inspect the result before PR creation.",
    "Keep provider execution explicit and report-bound.",
]


def split_path_values(items: list[str]) -> list[str]:
    values: list[str] = []
    for item in items:
        for part in str(item).split(","):
            normalized = part.strip().strip("'\"")
            if normalized:
                values.append(normalized)
    return values


def resolve_repo_path(repo_root: Path, raw: str) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def normalize_repo_path(value: Any) -> str:
    return str(value or "").strip().replace("\\", "/")


def sanitize_filename(value: str) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    sanitized = sanitized.strip("._-")
    return sanitized or "proposal"


def read_json_object(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def target_path_error(path: str, repo_root: Path) -> str | None:
    normalized = normalize_repo_path(path)
    if not normalized:
        return "empty target path"
    if Path(normalized).is_absolute():
        return "absolute target paths are not allowed"
    full = (repo_root / normalized).resolve()
    try:
        full.relative_to(repo_root)
    except ValueError:
        return "target path escapes repository root"
    if normalized in FORBIDDEN_TARGET_EXACT:
        return f"forbidden target path: {normalized}"
    if any(normalized.startswith(prefix) for prefix in FORBIDDEN_TARGET_PREFIXES):
        return f"forbidden target prefix: {normalized}"
    lower = normalized.lower()
    if any(fragment in lower for fragment in FORBIDDEN_TARGET_FRAGMENTS) and lower.endswith(
        ".json"
    ):
        return f"forbidden full-analysis JSON target: {normalized}"
    if "*" in normalized or normalized.endswith("/"):
        return "target is a path group, glob or directory"
    if not full.exists():
        return "target file does not exist"
    if not full.is_file():
        return "target is not a file"
    return None


def output_descriptor_from_target(path: str) -> dict[str, str]:
    suffix = Path(path).suffix.lower()
    if suffix == ".py":
        artifact_kind = "python_code"
    elif suffix == ".md":
        artifact_kind = "markdown"
    elif suffix == ".json":
        artifact_kind = "json"
    elif suffix == ".ps1":
        artifact_kind = "powershell"
    elif suffix in {".yml", ".yaml"}:
        artifact_kind = "workflow_yaml"
    else:
        artifact_kind = "text_or_config"
    return {
        "path": path,
        "artifact_kind": artifact_kind,
        "operation": "manual_patch_suggestion",
        "content_status": "proposal_only",
        "write_policy": EXPECTED_APPLY_MODE,
    }


def proposal_outputs(proposal: dict[str, Any]) -> list[dict[str, Any]]:
    raw_outputs = proposal.get("suggestion_outputs")
    if isinstance(raw_outputs, list) and raw_outputs:
        return [item for item in raw_outputs if isinstance(item, dict)]
    target_files = proposal.get("target_files")
    if not isinstance(target_files, list):
        return []
    return [output_descriptor_from_target(str(path)) for path in target_files if str(path).strip()]


def build_metadata_operation(*, proposal_id: str, output: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": normalize_repo_path(output.get("path")),
        "replacements": [],
        "proposal_id": proposal_id,
        "artifact_kind": output.get("artifact_kind"),
        "operation": output.get("operation") or "manual_patch_suggestion",
        "content_status": "draft_metadata_only",
        "draft_status": "needs_concrete_replacements",
        "draft_notes": [
            "Add exact, regex or insert replacements only after reviewing the target file.",
            "Keep replacements small enough for deterministic dry-run validation.",
            "Leave this draft under output/ until it has been intentionally reviewed.",
        ],
        "require_contains_after": [],
        "forbid_contains_after": [],
    }


def build_concrete_operation(
    *, proposal_id: str, raw: dict[str, Any], repo_root: Path
) -> tuple[dict[str, Any] | None, str]:
    operation = str(raw.get("operation") or "").strip().lower().replace("-", "_")
    path = normalize_repo_path(raw.get("path"))
    if operation not in CONCRETE_OPERATION_NAMES:
        return None, f"unsupported concrete operation: {operation or '(missing)'}"
    error = target_path_error(path, repo_root)
    if error:
        return None, error

    item: dict[str, Any] = {
        "proposal_id": raw.get("proposal_id") or proposal_id,
        "id": raw.get("id") or raw.get("source_id") or proposal_id,
        "path": path,
        "operation": operation,
        "content_status": "concrete_review_ready",
        "draft_status": "concrete_review_ready",
        "source_id": raw.get("source_id") or proposal_id,
        "family": raw.get("family") or "repository_change_proposals",
        "description": raw.get("description") or "concrete operation from repository proposal",
        "require_contains_after": raw.get("require_contains_after") or [],
        "forbid_contains_after": raw.get("forbid_contains_after") or [],
    }

    for key in ("find", "replace", "content"):
        value = raw.get(key)
        if isinstance(value, str):
            item[key] = value
    if operation == "replace_once" and not ("find" in item and "replace" in item):
        return None, "replace_once requires find and replace"
    if operation in {"append_once", "write_file"} and "content" not in item:
        return None, f"{operation} requires content"
    if operation in {"insert_after_once", "insert_before_once"} and not (
        "find" in item and "content" in item
    ):
        return None, f"{operation} requires find and content"
    return item, ""


def concrete_operations_from_proposal(
    proposal: dict[str, Any],
    *,
    proposal_id: str,
    repo_root: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    operations: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    raw_operations = proposal.get("concrete_operations")
    if not isinstance(raw_operations, list):
        return operations, skipped
    for raw in raw_operations:
        if not isinstance(raw, dict):
            skipped.append({"path": "", "reason": "concrete operation is not an object"})
            continue
        operation, error = build_concrete_operation(
            proposal_id=proposal_id, raw=raw, repo_root=repo_root
        )
        if error:
            skipped.append({"path": normalize_repo_path(raw.get("path")), "reason": error})
            continue
        if operation:
            operations.append(operation)
    return operations, skipped


def build_spec_for_proposal(
    *,
    proposal: dict[str, Any],
    proposal_report_path: Path,
    repo_root: Path,
) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    proposal_id = str(proposal.get("id") or "proposal")
    operations: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    seen_paths: set[str] = set()

    if proposal.get("apply_mode") != EXPECTED_APPLY_MODE:
        skipped.append({"path": "", "reason": "proposal apply_mode is not manual_review_only"})
        return None, skipped

    concrete_ops, concrete_skipped = concrete_operations_from_proposal(
        proposal,
        proposal_id=proposal_id,
        repo_root=repo_root,
    )
    operations.extend(concrete_ops)
    skipped.extend(concrete_skipped)

    concrete_paths = {str(item.get("path") or "") for item in concrete_ops}
    suppress_metadata_outputs = bool(concrete_ops)
    for output in proposal_outputs(proposal):
        path = normalize_repo_path(output.get("path"))
        if path in concrete_paths:
            continue
        if suppress_metadata_outputs:
            skipped.append(
                {
                    "path": path,
                    "reason": "metadata-only companion suppressed because concrete_operations are present",
                }
            )
            continue
        artifact_kind = str(output.get("artifact_kind") or "")
        write_policy = output.get("write_policy")
        if write_policy != EXPECTED_APPLY_MODE:
            skipped.append(
                {
                    "path": path,
                    "reason": "suggestion output write_policy is not manual_review_only",
                }
            )
            continue
        if artifact_kind in SKIPPED_OUTPUT_KINDS:
            skipped.append(
                {
                    "path": path,
                    "reason": f"artifact kind {artifact_kind} is not a concrete file",
                }
            )
            continue
        if artifact_kind not in SUPPORTED_OUTPUT_KINDS:
            skipped.append({"path": path, "reason": f"unsupported artifact kind: {artifact_kind}"})
            continue
        error = target_path_error(path, repo_root)
        if error:
            skipped.append({"path": path, "reason": error})
            continue
        if path in seen_paths:
            skipped.append({"path": path, "reason": "duplicate target path in proposal"})
            continue
        seen_paths.add(path)
        operations.append(build_metadata_operation(proposal_id=proposal_id, output=output))

    if not operations:
        return None, skipped

    draft_status = "concrete_review_ready" if concrete_ops else "needs_concrete_replacements"
    spec = {
        "version": 1,
        "schema_version": 1,
        "kind": SPEC_KIND,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "source_proposal_report": repo_relative(proposal_report_path, repo_root),
        "proposal_id": proposal_id,
        "proposal_title": proposal.get("title") or "",
        "proposal_area": proposal.get("area") or "",
        "proposal_priority": proposal.get("priority") or "",
        "apply_mode": EXPECTED_APPLY_MODE,
        "draft_status": draft_status,
        "provider_execution_performed": False,
        "description": f"Patch spec for {proposal_id}: {proposal.get('title') or 'repository proposal'}",
        "operations": operations,
        "validation_commands": proposal.get("validation_commands") or [],
        "stop_conditions": proposal.get("stop_conditions") or [],
        "do_not_touch": proposal.get("do_not_touch") or [],
        "guardrails": DEFAULT_GUARDRAILS,
        "skipped_targets": skipped,
    }
    return spec, skipped


def render_manifest_markdown(manifest: dict[str, Any]) -> str:
    lines = ["# Proposal Patch Spec Drafts", ""]
    lines.append(f"- Generated at: `{manifest['generated_at']}`")
    lines.append(f"- Source proposal report: `{manifest['source_proposal_report']}`")
    lines.append(f"- Patch spec count: `{manifest['patch_spec_count']}`")
    lines.append(f"- Concrete spec count: `{manifest['concrete_spec_count']}`")
    lines.append(f"- Skipped target count: `{manifest['skipped_target_count']}`")
    lines.append(f"- Provider execution performed: `{manifest['provider_execution_performed']}`")
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

    proposal_report_provider_execution_seen = bool(
        proposal_report.get("provider_execution_performed")
    )

    proposals = proposal_report.get("proposals")
    if not isinstance(proposals, list):
        errors.append("proposal report proposals must be a list")
        proposals = []

    provider_execution_seen = proposal_report_provider_execution_seen or any(
        bool(item.get("provider_execution_performed"))
        for item in proposals
        if isinstance(item, dict)
    )
    if require_provider_execution and not provider_execution_seen:
        errors.append(
            "provider execution is required for real-product generated patch specs; "
            "proposal report did not prove provider_execution_performed=true"
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--proposal",
        default="output/ai_pipeline/repository_change_proposals.json",
        help="Repository change proposal JSON report.",
    )
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--basename", default=DEFAULT_BASENAME)
    parser.add_argument("--max-proposals", type=int)
    parser.add_argument(
        "--require-concrete",
        action="store_true",
        help="Fail when generated specs contain no concrete deterministic operations. Disables metadata-only fallback.",
    )
    parser.add_argument(
        "--require-provider-execution",
        action="store_true",
        help="Fail unless the proposal report proves provider_execution_performed=true.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    proposal_path = resolve_repo_path(repo_root, args.proposal)
    output_dir = resolve_repo_path(repo_root, args.output_dir)
    manifest = build_patch_specs(
        repo_root=repo_root,
        proposal_path=proposal_path,
        output_dir=output_dir,
        basename=args.basename,
        max_proposals=args.max_proposals,
        require_concrete=bool(args.require_concrete),
        require_provider_execution=bool(args.require_provider_execution),
    )
    print(
        json.dumps(
            {
                "passed": manifest["passed"],
                "manifest_json": manifest["manifest_json"],
                "manifest_markdown": manifest["manifest_markdown"],
                "patch_spec_count": manifest["patch_spec_count"],
                "concrete_spec_count": manifest["concrete_spec_count"],
                "skipped_target_count": manifest["skipped_target_count"],
            },
            indent=2,
        )
    )
    return 0 if manifest["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
