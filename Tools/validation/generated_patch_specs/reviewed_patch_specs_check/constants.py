"""Reviewed patch-spec contract constants."""

from __future__ import annotations

EXPECTED_SPEC_KIND = "reviewed_patch_spec"
EXPECTED_MANIFEST_KIND = "reviewed_patch_spec_manifest"
EXPECTED_APPLY_MODE = "manual_review_only"
EXPECTED_REVIEW_STATUS = "dry_run_passed"

SUPPORTED_REPLACEMENT_TYPES = {
    "exact",
    "regex",
    "insert_after",
    "insert_before",
}

FORBIDDEN_TARGET_PREFIXES = (
    "indexAI/",
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

FORBIDDEN_COMMAND_FRAGMENTS = (
    "git reset --hard",
    "git clean",
    "Remove-Item -Recurse",
    "Remove-Item -Force -Recurse",
    "patch_specs/inbox/",
)

REQUIRED_SPEC_FIELDS = (
    "version",
    "schema_version",
    "kind",
    "generated_at",
    "source_draft_spec",
    "source_replacement_plan",
    "apply_mode",
    "review_status",
    "provider_execution_performed",
    "description",
    "operations",
    "dry_run",
)

REQUIRED_MANIFEST_FIELDS = (
    "schema_version",
    "kind",
    "generated_at",
    "repo_root",
    "passed",
    "errors",
    "warnings",
    "provider_execution_performed",
    "apply_mode",
    "review_status",
    "source_draft_spec",
    "source_replacement_plan",
    "reviewed_spec_count",
    "specs",
)
