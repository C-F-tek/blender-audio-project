from __future__ import annotations

from pathlib import Path
from typing import Any

from Tools.ai_adapters.blender import BlenderGeneratedScriptPolicy, BlenderImplementationDraftValidator
from Tools.ai_core.io_utils import read_json


ALLOWED_NEW_PREFIXES = ("indexAI/scene_scripts/", "indexAI/patch_library/")
PREFERRED_IMPLEMENTATION_FILES = (
    "Scripting/v61b/materials.py",
    "Scripting/v61b/fog_dynamics.py",
    "Scripting/v61b/physics_setup.py",
    "Scripting/v61b/scene_tuning_panel.py",
    "Scripting/v61b/config.py",
    "Scripting/v61b/render_setup.py",
    "Scripting/v61b/hot_update_scene_v61b.py",
)


def load_indexed_project_files(project_manifest_json: str | Path) -> set[str]:
    """Load indexed project files from the project AI manifest."""
    manifest_path = Path(project_manifest_json)
    if not manifest_path.exists():
        return set()
    data = read_json(manifest_path, default={})
    files = data.get("files") if isinstance(data, dict) else []
    indexed: set[str] = set()
    if isinstance(files, list):
        for item in files:
            if isinstance(item, dict) and item.get("file"):
                indexed.add(str(item["file"]).replace("\\", "/"))
    return indexed


def build_blender_draft_policy() -> BlenderGeneratedScriptPolicy:
    """Return the policy currently expected by the NPU dual AI pipeline."""
    return BlenderGeneratedScriptPolicy(
        allowed_new_prefixes=ALLOWED_NEW_PREFIXES,
        metadata={
            "source": "Tools/npu/implementation_draft_validation.py",
            "compatibility": "run_dual_ai_pipeline.validate_implementation_draft",
        },
    )


def validate_implementation_draft_with_adapter(
    draft: dict[str, Any],
    project_manifest_json: str | Path,
) -> dict[str, Any]:
    """Validate a generated Blender implementation draft using the adapter layer.

    Return shape intentionally matches the legacy helper used by
    `run_dual_ai_pipeline.py`: `{"passed": bool, "issues": list[str]}`.
    """
    indexed_files = load_indexed_project_files(project_manifest_json)
    validator = BlenderImplementationDraftValidator(
        policy=build_blender_draft_policy(),
        indexed_files=indexed_files,
    )
    report = validator.validate(draft)
    issues = [
        f"{issue.level}: {issue.message}" + (f" ({issue.path})" if issue.path else "")
        for issue in report.issues
    ]
    return {
        "passed": report.passed,
        "issues": issues,
        "issue_count": len(issues),
        "validator": "Tools.ai_adapters.blender.BlenderImplementationDraftValidator",
        "policy": build_blender_draft_policy().to_dict(),
    }


def validation_report_to_legacy_shape(report: dict[str, Any]) -> dict[str, Any]:
    """Keep only fields that old retry prompts already understand."""
    return {
        "passed": bool(report.get("passed")),
        "issues": list(report.get("issues") or []),
    }
