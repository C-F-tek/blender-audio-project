from __future__ import annotations

from .common import *  # noqa: F403

def safe_parse_json(text: str, fallback_key: str) -> dict[str, Any]:
    try:
        parsed = parse_json_response(text)
        return parsed if isinstance(parsed, dict) else {fallback_key: text, "parse_error": True}
    except Exception:
        return {fallback_key: text, "parse_error": True}

def extract_python_script(text: str) -> str:
    stripped = text.strip()
    if "```" in stripped:
        parts = stripped.split("```")
        for index, part in enumerate(parts):
            body = part
            if index % 2 == 1:
                lines = body.splitlines()
                if lines and lines[0].strip().lower() in {"python", "py"}:
                    body = "\n".join(lines[1:])
                if "import bpy" in body:
                    return body.strip()
    if "import bpy" in stripped:
        start = stripped.find("from __future__")
        if start < 0:
            start = stripped.find("import bpy")
        return stripped[start:].strip()
    return ""

def draft_from_raw_python_script(
    text: str, model: str | None, reason: str
) -> dict[str, Any] | None:
    script = extract_python_script(text)
    if not script:
        return None
    new_file = generated_scene_script_relpath()
    reference_files = [
        {
            "file": path,
            "exists_in_project_index": True,
            "reason": "Style/source reference only; not modified by this generated scene script.",
        }
        for path in PREFERRED_IMPLEMENTATION_FILES
        if path in get_indexed_project_files()
    ]
    return {
        "implementation_kind": "new_blender_scene_script_from_json",
        "safety": {
            "does_not_modify_full_analysis_json": True,
            "does_not_modify_project_source_files": True,
            "requires_manual_review": True,
            "needs_blender_run": True,
        },
        "reference_files": reference_files,
        "proposed_files": [
            {
                "file": new_file,
                "kind": "standalone_blender_scene_builder",
                "why": "The model returned raw Python; the pipeline wrapped it into the required review JSON.",
            }
        ],
        "implementation_plan": [
            {
                "reference_file": item["file"],
                "new_file": new_file,
                "change": "Use this source as reference style while reviewing the raw generated Blender script.",
                "why": "Preserve project structure while creating a separate candidate script.",
                "risk": "medium",
                "manual_check": "Run only inside Blender on a disposable scene.",
            }
            for item in reference_files[:6]
        ],
        "new_files_allowed": ["indexAI/scene_scripts/...", "indexAI/patch_library/..."],
        "scene_script": script,
        "support_files": [],
        "notes": [reason, "Raw Python was accepted only after wrapping and normal validation."],
        "files_to_review_before_applying": [item["file"] for item in reference_files],
        "expected_panel_or_operator": "Run as standalone Blender Text script on a new/empty scene.",
        "model": model,
    }

def get_indexed_project_files() -> set[str]:
    manifest = read_json(PROJECT_MANIFEST_JSON) if PROJECT_MANIFEST_JSON.exists() else {}
    return {item.get("file") for item in manifest.get("files", []) if item.get("file")}

def generated_scene_script_relpath() -> str:
    return f"indexAI/scene_scripts/{packet_slugify(TRACK_STEM)}_scene_builder_candidate.py"

def generated_scene_script_abspath() -> Path:
    return ROOT / generated_scene_script_relpath()
