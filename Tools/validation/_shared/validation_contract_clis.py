"""Shared CLI entrypoints for compact validation-contract checks."""

from __future__ import annotations

import argparse
from pathlib import Path

from Tools.validation._shared.json_report_cli import run_json_report_cli

try:
    from check_ai_context_pack_contract import (
        resolve_repo_path as resolve_context_path,
        split_path_values as split_context_values,
        validate_ai_context_packs,
    )
except ModuleNotFoundError:
    from Tools.validation.check_ai_context_pack_contract import (
        resolve_repo_path as resolve_context_path,
        split_path_values as split_context_values,
        validate_ai_context_packs,
    )

try:
    from check_local_ai_adapter_manifest import (
        resolve_repo_path as resolve_manifest_path,
        split_manifest_values,
        validate_manifests,
    )
except ModuleNotFoundError:
    from Tools.validation.check_local_ai_adapter_manifest import (
        resolve_repo_path as resolve_manifest_path,
        split_manifest_values,
        validate_manifests,
    )

try:
    from Tools.validation.generated_patch_specs.patch_spec_drafts import (
        resolve_repo_path as resolve_patch_spec_path,
        split_path_values as split_patch_spec_values,
        validate_patch_spec_drafts,
    )
except ModuleNotFoundError:
    from check_patch_spec_drafts import (
        resolve_repo_path as resolve_patch_spec_path,
        split_path_values as split_patch_spec_values,
        validate_patch_spec_drafts,
    )

try:
    from Tools.validation.repository_product.github_evidence_bundle import (
        default_bundle_paths,
        split_path_values as split_bundle_values,
        validate_github_evidence_bundles,
    )
except ModuleNotFoundError:
    from check_github_evidence_bundle import (
        default_bundle_paths,
        split_path_values as split_bundle_values,
        validate_github_evidence_bundles,
    )


def configure_context_pack_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--pack", action="append", default=[], help="Context pack JSON path.")
    parser.add_argument("--evidence", action="append", default=[], help="Context pack evidence JSON path.")


def build_context_pack_report(args: argparse.Namespace, repo_root: Path) -> dict:
    pack_paths = [
        resolve_context_path(repo_root, raw) for raw in split_context_values(list(args.pack or []))
    ]
    evidence_paths = [
        resolve_context_path(repo_root, raw) for raw in split_context_values(list(args.evidence or []))
    ]
    if not pack_paths and not evidence_paths:
        pack_paths = [repo_root / "output" / "ai_context_packs" / "project_self_improvement.json"]
        evidence_paths = [
            repo_root
            / "docs"
            / "LOCAL_VALIDATION_EVIDENCE"
            / "project_self_improvement_context_pack_evidence.json"
        ]
    return validate_ai_context_packs(repo_root, pack_paths, evidence_paths)


def ai_context_pack_main() -> int:
    return run_json_report_cli(
        configure_parser=configure_context_pack_parser,
        build_report=build_context_pack_report,
        description="Validate AI context pack contract evidence.",
    )


def configure_patch_spec_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--manifest", action="append", default=[], help="Patch spec draft manifest path.")
    parser.add_argument("--spec", action="append", default=[], help="Patch spec draft JSON path.")


def build_patch_spec_report(args: argparse.Namespace, repo_root: Path) -> dict:
    manifest_paths = [
        resolve_patch_spec_path(repo_root, raw)
        for raw in split_patch_spec_values(list(args.manifest or []))
    ]
    spec_paths = [
        resolve_patch_spec_path(repo_root, raw) for raw in split_patch_spec_values(list(args.spec or []))
    ]
    if not manifest_paths and not spec_paths:
        manifest_paths = [repo_root / "output/patch_specs/proposal_patch_specs_manifest.json"]
    return validate_patch_spec_drafts(repo_root, manifest_paths, spec_paths)


def patch_spec_drafts_main() -> int:
    return run_json_report_cli(
        configure_parser=configure_patch_spec_parser,
        build_report=build_patch_spec_report,
        description="Validate generated patch spec draft reports.",
    )


def configure_github_bundle_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--bundle", action="append", default=[], help="Bundle JSON path.")


def build_github_bundle_report(args: argparse.Namespace, repo_root: Path) -> dict:
    raw_bundles = split_bundle_values(list(args.bundle or []))
    if raw_bundles:
        paths = [
            Path(item).resolve() if Path(item).is_absolute() else (repo_root / item).resolve()
            for item in raw_bundles
        ]
    else:
        paths = default_bundle_paths(repo_root)
    return validate_github_evidence_bundles(repo_root, paths)


def github_evidence_bundle_main() -> int:
    return run_json_report_cli(
        configure_parser=configure_github_bundle_parser,
        build_report=build_github_bundle_report,
        description="Validate GitHub evidence bundle reports.",
    )


def configure_adapter_manifest_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--manifest", action="append", default=[], help="Manifest path.")


def build_adapter_manifest_report(args: argparse.Namespace, repo_root: Path) -> dict:
    raw_paths = split_manifest_values(list(args.manifest or []))
    if not raw_paths:
        raw_paths = ["output/local_ai_runs/latest/pipeline/local_ai_task_pipeline_adapter_manifest.json"]
    manifests = [resolve_manifest_path(repo_root, raw) for raw in raw_paths]
    return validate_manifests(repo_root, manifests)


def local_ai_adapter_manifest_main() -> int:
    return run_json_report_cli(
        configure_parser=configure_adapter_manifest_parser,
        build_report=build_adapter_manifest_report,
        description="Validate local AI adapter manifests.",
    )
