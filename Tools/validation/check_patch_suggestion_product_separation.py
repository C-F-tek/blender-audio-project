#!/usr/bin/env python3
"""Validate product-facing vs supplemental patch suggestion separation.

The validator is report-only. It accepts either the direct
patch_suggestion_bundle_apply JSON report or the wrapper
patch_suggestion_bundle_apply_smoke report used by the local smoke test.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report
except ImportError:  # Allows package-style imports during external checks.
    from Tools.validation.report_utils import resolve_output_path, write_json_report  # type: ignore


def load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    """Read a JSON object from path."""
    if not path.exists():
        return None, f"missing report: {path}"
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - report exact validation failure.
        return None, f"invalid JSON: {type(exc).__name__}: {exc}"
    if not isinstance(data, dict):
        return None, "report JSON root is not an object"
    return data, None


def normalize_target(value: Any) -> str:
    """Normalize a repository target path for policy checks."""
    return str(value or "").replace("\\", "/").strip().lstrip("./")


def targets_from_item(item: dict[str, Any]) -> list[str]:
    """Collect normalized target paths from a manual-review item."""
    raw_targets: list[Any] = []
    if isinstance(item.get("target_files"), list):
        raw_targets.extend(item.get("target_files") or [])
    if item.get("target"):
        raw_targets.append(item.get("target"))
    out: list[str] = []
    for raw in raw_targets:
        target = normalize_target(raw)
        if target and target not in out:
            out.append(target)
    return out


def has_safe_source_target(item: dict[str, Any]) -> bool:
    """Return true when the item has at least one non-generated source/doc target."""
    target_quality = item.get("target_quality") if isinstance(item.get("target_quality"), dict) else {}
    explicit = target_quality.get("has_safe_source_target")
    if isinstance(explicit, bool):
        return explicit

    targets = targets_from_item(item)
    if not targets:
        return False
    denied_prefixes = ("output/", "renders/", "indexAI/code_chunks/", "indexAI/project_code_chunks/")
    denied_suffixes = (".db", ".sqlite", ".sqlite3", ".sqlite-wal", ".sqlite-shm")
    safe = [
        target
        for target in targets
        if not target.startswith(denied_prefixes) and not target.lower().endswith(denied_suffixes)
    ]
    generated_like = [target for target in safe if target.startswith("docs/LOCAL_VALIDATION_EVIDENCE/")]
    return bool(safe and len(generated_like) < len(safe))


def validate_product_item(item: dict[str, Any], index: int) -> list[str]:
    """Validate one essential/product-facing suggestion item."""
    errors: list[str] = []
    label = item.get("id") or item.get("proposal_id") or f"essential[{index}]"
    if item.get("product_facing") is not True:
        errors.append(f"{label}: essential item missing product_facing=true")
    if item.get("supplemental") is True:
        errors.append(f"{label}: essential item is also marked supplemental")
    if not has_safe_source_target(item):
        errors.append(f"{label}: essential item has no safe source/doc target")
    if not (item.get("title") or item.get("description") or item.get("rationale")):
        errors.append(f"{label}: essential item has no title/description/rationale")
    if not (item.get("patch_sketch") or item.get("operation")):
        errors.append(f"{label}: essential item has no patch sketch or deterministic operation")
    if not (item.get("validation_commands") or item.get("stop_conditions")):
        errors.append(f"{label}: essential item has no validation commands or stop conditions")
    return errors


def validate_supplemental_item(item: dict[str, Any], index: int) -> list[str]:
    """Validate one supplemental telemetry/debug/evidence suggestion item."""
    errors: list[str] = []
    label = item.get("id") or item.get("proposal_id") or f"supplemental[{index}]"
    if item.get("supplemental") is not True:
        errors.append(f"{label}: supplemental item missing supplemental=true")
    if item.get("product_facing") is True:
        errors.append(f"{label}: supplemental item is also marked product_facing")
    return errors


def validate_apply_report(data: dict[str, Any], *, require_product: bool, require_supplemental: bool) -> tuple[list[str], list[str], dict[str, Any]]:
    """Validate the product/supplemental split exposed by an apply report."""
    errors: list[str] = []
    warnings: list[str] = []

    product = data.get("manual_review_product") if isinstance(data.get("manual_review_product"), dict) else {}
    essential = data.get("essential_patch_suggestion_items")
    supplemental = data.get("supplemental_telemetry_debug_items")
    if not isinstance(essential, list):
        errors.append("essential_patch_suggestion_items is missing or not a list")
        essential = []
    if not isinstance(supplemental, list):
        errors.append("supplemental_telemetry_debug_items is missing or not a list")
        supplemental = []

    expected_product_total = int(product.get("product_facing_manual_review_count") or 0)
    expected_supplemental_total = int(product.get("supplemental_manual_review_count") or 0)
    expected_product_published = int(
        product.get("product_facing_manual_review_published_count")
        if product.get("product_facing_manual_review_published_count") is not None
        else min(expected_product_total, 100)
    )
    expected_supplemental_published = int(
        product.get("supplemental_manual_review_published_count")
        if product.get("supplemental_manual_review_published_count") is not None
        else min(expected_supplemental_total, 100)
    )
    if expected_product_published != len(essential):
        errors.append(
            "product-facing count mismatch: "
            f"published={expected_product_published} essential_list={len(essential)} "
            f"total={expected_product_total}"
        )
    if expected_supplemental_published != len(supplemental):
        errors.append(
            "supplemental count mismatch: "
            f"published={expected_supplemental_published} supplemental_list={len(supplemental)} "
            f"total={expected_supplemental_total}"
        )

    deterministic_count = int(product.get("deterministic_operation_count") or data.get("operation_count") or 0)
    deterministic_apply_ready = product.get("deterministic_apply_ready")
    failed_count = int(data.get("failed_count") or 0)
    deterministic_product_ready = deterministic_count > 0 and deterministic_apply_ready is True and failed_count == 0
    if require_product and not essential and not deterministic_product_ready:
        errors.append("required product-facing patch suggestions or deterministic operations are absent")
    if require_supplemental and not supplemental:
        errors.append("required supplemental telemetry/debug items are absent")

    for index, item in enumerate(essential):
        errors.extend(validate_product_item(item, index) if isinstance(item, dict) else [f"essential[{index}]: item is not an object"])
    for index, item in enumerate(supplemental):
        errors.extend(validate_supplemental_item(item, index) if isinstance(item, dict) else [f"supplemental[{index}]: item is not an object"])

    if deterministic_count > 0 and deterministic_apply_ready is not True:
        errors.append("deterministic operations exist but deterministic_apply_ready is not true")
    if deterministic_count == 0 and deterministic_apply_ready is True:
        errors.append("deterministic_apply_ready is true with zero deterministic operations")

    for key, label in (
        ("provider_execution_performed", "provider execution"),
        ("blender_execution_performed", "Blender execution"),
        ("ffmpeg_execution_performed", "FFmpeg execution"),
        ("sqlite_writes_performed", "SQLite writes"),
    ):
        if data.get(key) is True:
            errors.append(f"validator input unexpectedly reports {label}")

    if not essential and not supplemental and deterministic_count == 0:
        warnings.append("report contains no deterministic operations, essential suggestions or supplemental items")

    metrics = {
        "validated_input_kind": "patch_suggestion_bundle_apply",
        "deterministic_operation_count": deterministic_count,
        "deterministic_product_ready": deterministic_product_ready,
        "failed_count": failed_count,
        "essential_patch_suggestion_count": len(essential),
        "essential_patch_suggestion_total_count": expected_product_total,
        "supplemental_telemetry_debug_count": len(supplemental),
        "supplemental_telemetry_debug_total_count": expected_supplemental_total,
        "patch_product_status": data.get("patch_product_status") or product.get("patch_product_status"),
        "ready_for_patch_suggestion_review": data.get("ready_for_patch_suggestion_review"),
    }
    return errors, warnings, metrics


def validate_smoke_report(data: dict[str, Any], *, require_product: bool, require_supplemental: bool) -> tuple[list[str], list[str], dict[str, Any]]:
    """Validate the smoke wrapper that already asserts product separation internally."""
    errors: list[str] = []
    warnings: list[str] = []
    if data.get("passed") is not True:
        errors.append("patch suggestion apply smoke did not pass")
    for item in data.get("errors") or []:
        errors.append(str(item))
    if data.get("provider_execution_performed") is True:
        errors.append("smoke unexpectedly reports provider execution")
    if data.get("patch_application_performed") is True:
        errors.append("smoke wrapper unexpectedly reports repository patch application")
    if data.get("source_writes_performed") is True:
        errors.append("smoke wrapper unexpectedly reports repository source writes")

    discovered = data.get("discovered_reports") if isinstance(data.get("discovered_reports"), list) else []
    current = data.get("current_suggestion_reports") if isinstance(data.get("current_suggestion_reports"), list) else []
    if require_product and "output/ai_pipeline/repository_change_proposals.json" not in current:
        errors.append("smoke did not include current product-facing proposal report")
    if require_supplemental and "output/ai_pipeline/repository_update_suggestions.json" not in current:
        errors.append("smoke did not include current supplemental update suggestion report")
    if not discovered:
        errors.append("smoke did not discover stamped deterministic suggestion report")

    commands = data.get("commands") if isinstance(data.get("commands"), list) else []
    failed_commands = [cmd for cmd in commands if isinstance(cmd, dict) and cmd.get("returncode") != 0]
    if failed_commands:
        errors.append(f"smoke has failed nested commands: {len(failed_commands)}")
    if not commands:
        warnings.append("smoke wrapper has no nested command evidence")

    metrics = {
        "validated_input_kind": "patch_suggestion_bundle_apply_smoke",
        "smoke_asserted_product_separation": bool(data.get("passed") is True),
        "discovered_report_count": len(discovered),
        "current_suggestion_report_count": len(current),
        "nested_command_count": len(commands),
    }
    return errors, warnings, metrics


def validate_report(data: dict[str, Any], *, require_product: bool, require_supplemental: bool) -> tuple[list[str], list[str], dict[str, Any]]:
    """Dispatch validation based on the input report kind."""
    kind = data.get("kind")
    if kind == "patch_suggestion_bundle_apply":
        return validate_apply_report(data, require_product=require_product, require_supplemental=require_supplemental)
    if kind == "patch_suggestion_bundle_apply_smoke":
        return validate_smoke_report(data, require_product=require_product, require_supplemental=require_supplemental)
    return [f"unexpected report kind: {kind!r}"], [], {"validated_input_kind": kind}


def main() -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--report", required=True, help="patch_suggestion_bundle_apply or smoke JSON report")
    parser.add_argument("--output", default="output/validation/patch_suggestion_product_separation.json")
    parser.add_argument("--require-product", action="store_true")
    parser.add_argument("--require-supplemental", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report_path = Path(args.report)
    if not report_path.is_absolute():
        report_path = repo_root / report_path
    data, load_error = load_json(report_path.resolve())
    errors: list[str] = []
    warnings: list[str] = []
    metrics: dict[str, Any] = {}
    if load_error:
        errors.append(load_error)
    elif data is not None:
        errors, warnings, metrics = validate_report(
            data,
            require_product=bool(args.require_product),
            require_supplemental=bool(args.require_supplemental),
        )

    report = {
        "schema_version": 1,
        "kind": "patch_suggestion_product_separation_validation",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "input_report": report_path.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "blender_execution_performed": False,
        "ffmpeg_execution_performed": False,
        "sqlite_writes_performed": False,
        "require_product": bool(args.require_product),
        "require_supplemental": bool(args.require_supplemental),
        "metrics": metrics,
        "errors": errors,
        "warnings": warnings,
    }
    output = resolve_output_path(repo_root, args.output)
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
