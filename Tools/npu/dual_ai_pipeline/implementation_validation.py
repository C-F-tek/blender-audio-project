from __future__ import annotations

from .common import *  # noqa: F403
from .implementation_parse import generated_scene_script_relpath, get_indexed_project_files

def validate_implementation_draft(draft: dict[str, Any]) -> dict[str, Any]:
    indexed_files = get_indexed_project_files()
    contract_validation = validate_implementation_draft_contract(
        draft,
        allowed_prefixes=ALLOWED_NEW_PREFIXES,
    )

    issues: list[str] = list(contract_validation.get("required_key_report", {}).get("issues", []))
    reference_files = draft.get("reference_files") or []
    proposed_files = draft.get("proposed_files") or []
    implementation_plan = draft.get("implementation_plan") or []

    if draft.get("implementation_kind") != "new_blender_scene_script_from_json":
        issues.append("implementation_kind should be new_blender_scene_script_from_json.")

    if not isinstance(reference_files, list) or not reference_files:
        issues.append("No reference_files entries were provided.")
    if not isinstance(proposed_files, list) or not proposed_files:
        issues.append("No proposed_files entries were provided.")
    if not isinstance(implementation_plan, list) or not implementation_plan:
        issues.append("No implementation_plan entries were provided.")

    if isinstance(reference_files, list):
        for item in reference_files:
            if not isinstance(item, dict):
                issues.append("A reference_files entry is not an object.")
                continue
            raw_file_name = str(item.get("file") or "").replace("\\", "/").strip()
            if not raw_file_name:
                issues.append("A reference_files entry has no file.")
                continue
            file_name = normalize_repo_relative_path(raw_file_name)
            if file_name not in indexed_files:
                issues.append(f"Reference file is not in project index: {file_name}")

    if isinstance(proposed_files, list):
        for item in proposed_files:
            if not isinstance(item, dict):
                issues.append("A proposed_files entry is not an object.")
                continue
            raw_file_name = str(item.get("file") or "").replace("\\", "/").strip()
            if not raw_file_name:
                issues.append("A proposed_files entry has no file.")
                continue
            file_name = normalize_repo_relative_path(raw_file_name)
            if file_name in indexed_files:
                issues.append(f"Proposed file must not be an existing source file: {file_name}")
            if not is_allowed_generated_artifact_path(
                file_name, allowed_prefixes=ALLOWED_NEW_PREFIXES
            ):
                issues.append(
                    f"Proposed file is not under an allowed generated-output prefix: {file_name}"
                )

    support_files = draft.get("support_files") or []
    if support_files and not isinstance(support_files, list):
        issues.append("support_files must be a list when provided.")
    if isinstance(support_files, list):
        for item in support_files:
            if not isinstance(item, dict):
                issues.append("A support_files entry is not an object.")
                continue
            raw_file_name = str(item.get("file") or "").replace("\\", "/").strip()
            if not raw_file_name:
                issues.append("A support_files entry has no file.")
                continue
            file_name = normalize_repo_relative_path(raw_file_name)
            if file_name in indexed_files:
                issues.append(f"Support file must not be an existing source file: {file_name}")
            if not is_allowed_generated_artifact_path(
                file_name, allowed_prefixes=ALLOWED_NEW_PREFIXES
            ):
                issues.append(
                    f"Support file is not under an allowed generated-output prefix: {file_name}"
                )
            if "content" not in item:
                issues.append(f"Support file has no content: {file_name}")

    script = str(
        draft.get("scene_script")
        or draft.get("hotpatch_candidate_script")
        or draft.get("script")
        or ""
    )
    script_lower = script.lower()
    stripped_script = script.strip()
    if len(stripped_script) < 2500:
        issues.append("scene_script is missing or too short.")
    if "import bpy" not in script:
        issues.append("scene_script does not appear to be a Blender Python script.")
    if "json" not in script_lower or "load_json" not in script:
        issues.append("scene_script must load and use the JSON context files.")
    if 'keyframes.get("frames"' not in script and "keyframes.get('frames'" not in script:
        issues.append("scene_script must use the full Blender keyframes JSON frames.")
    if "keyframe_insert" not in script:
        issues.append("scene_script must create Blender keyframes from the audio context.")
    if "modifiers.new" not in script and ".modifiers" not in script:
        issues.append("scene_script must include at least one mesh/modifier-driven visual system.")
    if "materials.new" not in script and ".data.materials" not in script:
        issues.append("scene_script must create or assign materials.")
    if any(
        token in script_lower for token in ["placeholder", "todo", "can't assist", "cannot assist"]
    ):
        issues.append("scene_script contains placeholder/refusal text.")
    if "\n    pass" in script or "\n\tpass" in script:
        issues.append("scene_script contains pass blocks instead of implementation.")
    if "analysis_blender_keyframes" in script and "write" in script.lower():
        issues.append("Candidate script appears to write keyframe analysis data; review required.")
    if any(token in script for token in ["apply_patch", "git ", "Remove-Item", "shutil.rmtree"]):
        issues.append(
            "Candidate script contains project/file mutation commands outside Blender scene creation."
        )

    return {
        "ok": not issues,
        "issues": issues,
        "indexed_file_count": len(indexed_files),
        "allowed_new_prefixes": list(ALLOWED_NEW_PREFIXES),
        "contract_validation": contract_validation,
    }
