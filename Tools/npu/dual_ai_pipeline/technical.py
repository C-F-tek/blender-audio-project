from __future__ import annotations

from .common import *  # noqa: F403

def looks_degraded_text(text: str) -> bool:
    stripped = text.strip()
    if len(stripped) < 260:
        return True
    alnum = sum(ch.isalnum() for ch in stripped)
    visible = sum(not ch.isspace() for ch in stripped)
    if visible and alnum / visible < 0.45:
        return True
    markdown_heads = stripped.count("##")
    useful_words = sum(
        stripped.lower().count(word)
        for word in ["audio", "blender", "segment", "material", "fog", "light", "mesh"]
    )
    return markdown_heads < 2 and useful_words < 5

def deterministic_technical_notes(
    music_context: dict[str, Any], project_manifest: dict[str, Any], reason: str
) -> str:
    music_summary = summarize_music_context(music_context)
    summary = music_summary["analysis_summary"]
    track_summary = music_summary["track_summary"]
    files = project_manifest.get("files") or []
    priority_files = [
        item.get("file")
        for item in files
        if item.get("file", "").endswith(
            (
                "Scripting/v61b/config.py",
                "Scripting/v61b/materials.py",
                "Scripting/v61b/fog_dynamics.py",
                "Scripting/v61b/physics_setup.py",
                "Scripting/v61b/scene_tuning_panel.py",
                "Tools/workflow/workflow_run/workflow_core/__init__.py",
                "Tools/npu/dual_ai_pipeline/cli.py",
            )
        )
    ]

    lines = [
        "# Deterministic Technical Notes\n\n",
        f"Reason: NPU output was not trusted (`{reason}`).\n\n",
        "## Track Map\n",
        f"- Duration: `{summary.get('duration_sec', track_summary.get('duration_sec', '?'))}` seconds.\n",
        f"- FPS: `{summary.get('fps', track_summary.get('fps', '?'))}`.\n",
        f"- BPM: `{summary.get('estimated_tempo_bpm', track_summary.get('estimated_tempo_bpm', '?'))}`.\n",
        f"- Segment count: `{music_summary['segment_count']}`.\n\n",
        "## Project Primary Files\n",
    ]
    for file_name in priority_files[:20]:
        lines.append(f"- `{file_name}`\n")

    lines.extend(
        [
            "\n## Safe Implementation Policy\n",
            "- Use full frame-by-frame Blender keyframe JSON as data input only.\n",
            "- Generate patch plans against existing project files, not monolithic replacement scripts.\n",
            "- Prefer hotpatch/panel/update modules for materials, fog, lights and render changes.\n",
            "- Require a reload only when primary object creation or scene topology changes.\n\n",
            "## Audio Control Map\n",
            "- Low band: hero mesh deformation scale, gravity/attractor strength, fog density body.\n",
            "- Mid band: material roughness/emission mix, secondary object motion, fog filament drift.\n",
            "- High band: small emission accents, glints, particle sparkle, sharp camera micro motion.\n",
            "- Onset/beat: short impulses, never a constant global light flash.\n\n",
        ]
    )
    return "".join(lines)

def run_npu_technical_pass(args: argparse.Namespace) -> str:
    python_exe = Path(args.npu_python)
    cmd = [
        str(python_exe),
        "-m",
        "Tools.npu",
        "run_npu_review",
        "--engine",
        "npu",
        "--domain",
        "music",
        "--mode",
        "chunked",
        "--context",
        str(TOOLS_DIR / "context_artifacts" / "npu_music_context.md"),
        "--chunk-dir",
        str(TOOLS_DIR / "npu_music_chunks"),
        "--out",
        str(NPU_TECH_MD),
        "--notes-out",
        str(TOOLS_DIR / "npu_dual_ai_chunk_notes.md"),
        "--max-context-chars",
        "0",
        "--chunk-chars",
        "10500",
        "--chunk-overlap-chars",
        "700",
        "--max-prompt-chars",
        "15000",
        "--max-chunk-tokens",
        str(args.npu_chunk_tokens),
        "--max-reduce-tokens",
        str(args.npu_reduce_tokens),
        "--max-new-tokens",
        str(args.npu_final_tokens),
        "--max-prompt-len",
        "16384",
        "--min-response-len",
        "64",
    ]

    subprocess.run(cmd, check=True, cwd=ROOT)
    return read_text(NPU_TECH_MD)
