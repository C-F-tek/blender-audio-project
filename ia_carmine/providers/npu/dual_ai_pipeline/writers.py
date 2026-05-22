from __future__ import annotations

from .common import *  # noqa: F403
from .implementation import generated_scene_script_abspath, generated_scene_script_relpath
from .implementation_validation import validate_implementation_draft

def write_brief(
    plan: dict[str, Any], creative: dict[str, Any], technical: dict[str, Any], npu_notes: str
) -> None:
    lines = [
        "# Dual AI Blender Agent Brief\n\n",
        f"Generated: `{datetime.now().isoformat(timespec='seconds')}`\n\n",
        "## Policy\n",
        "- Full Blender keyframe JSON remains untouched.\n",
        "- AI compact context is analysis only.\n",
        "- Ollama model switch unloads the previous model before loading the next.\n\n",
        "## Recommended Plan\n",
        json.dumps(plan.get("recommended_scene_plan", plan), indent=2, ensure_ascii=False),
        "\n\n## Audio Mapping\n",
        json.dumps(plan.get("audio_mapping_plan", {}), indent=2, ensure_ascii=False),
        "\n\n## Creative Source\n",
        json.dumps(creative, indent=2, ensure_ascii=False)[:12000],
        "\n\n## Technical Source\n",
        json.dumps(technical, indent=2, ensure_ascii=False)[:12000],
        "\n\n## NPU Notes\n",
        npu_notes[:12000],
        "\n",
    ]
    write_legacy_text_output(DUAL_BRIEF_MD, "".join(lines))

def write_implementation_draft(draft: dict[str, Any]) -> None:
    draft["validation"] = validate_implementation_draft(draft)
    write_legacy_json_output(IMPLEMENTATION_DRAFT_JSON, draft)

    script = draft.get(
        "scene_script", draft.get("hotpatch_candidate_script", draft.get("script", ""))
    )
    if not script:
        script = (
            "# AI implementation draft did not contain a scene script.\n"
            "# Review the JSON draft for reference_files, proposed_files, validation and notes.\n"
        )
    write_legacy_text_output(IMPLEMENTATION_SCRIPT, str(script).rstrip() + "\n")
    scene_path = write_planned_artifact(
        ROOT,
        PlannedArtifactWrite(
            repo_relative_path=generated_scene_script_relpath(),
            kind="standalone_blender_scene_builder",
            content=str(script).rstrip() + "\n",
        ),
        allowed_prefixes=ALLOWED_NEW_PREFIXES,
    )

    planned_support_writes: list[PlannedArtifactWrite] = []
    for item in draft.get("support_files", []) or []:
        if not isinstance(item, dict):
            continue
        raw_relpath = str(item.get("file") or "").replace("\\", "/").strip()
        if not raw_relpath:
            continue
        relpath = normalize_repo_relative_path(raw_relpath)
        if not is_allowed_generated_artifact_path(relpath, allowed_prefixes=ALLOWED_NEW_PREFIXES):
            continue
        planned_support_writes.append(
            PlannedArtifactWrite(
                repo_relative_path=relpath,
                kind=str(item.get("kind") or "support_file"),
                content=str(item.get("content", "")).rstrip() + "\n",
            )
        )

    written_support_files: list[str] = []
    for planned_write in planned_support_writes:
        support_path = write_planned_artifact(
            ROOT,
            planned_write,
            allowed_prefixes=ALLOWED_NEW_PREFIXES,
        )
        written_support_files.append(str(support_path))
    if written_support_files:
        draft["written_support_files"] = written_support_files
        write_legacy_json_output(IMPLEMENTATION_DRAFT_JSON, draft)

    notes = [
        "# Generated Implementation Notes\n\n",
        "This file is an AI draft. Review before loading in Blender.\n\n",
        "## Validation\n",
        json.dumps(draft.get("validation", {}), indent=2, ensure_ascii=False),
        "\n\n",
        "## Safety\n",
        json.dumps(draft.get("safety", {}), indent=2, ensure_ascii=False),
        "\n\n## Notes\n",
    ]
    for note in draft.get("notes", []):
        notes.append(f"- {note}\n")
    notes.append("\n## Files To Review\n")
    for path in draft.get("files_to_review_before_applying", []):
        notes.append(f"- `{path}`\n")
    notes.append("\n## Generated Scene Script\n")
    notes.append(f"- `{scene_path}`\n")
    if written_support_files:
        notes.append("\n## Generated Support Files\n")
        for path in written_support_files:
            notes.append(f"- `{path}`\n")
    write_legacy_text_output(IMPLEMENTATION_NOTES, "".join(notes))
