# Scripting

This folder is the main workspace for Blender script packages generated, refined, or maintained from audio-analysis data and AI-assisted workflows.

## Purpose

`Scripting/` is not only a generic script folder. It is the area where Blender packages and scene-generation scripts are collected after they are produced from audio inputs, JSON analysis files, and AI-assisted design or coding sessions.

At the current stage, JSON files are prepared and then processed with external AI systems such as Codex or GPT. A future objective is to move more of this generation and refinement workflow to a local AI/NPU/GPU-assisted pipeline.

## Current roles

- Store Blender Python scripts.
- Store versioned scene-generation workflows.
- Store AI-generated or AI-refined Blender packages.
- Keep package-specific documentation near the generated code.
- Preserve multiple project variants when they represent different songs, visual concepts, or rendering approaches.

## Known project/package areas

| Path | Role |
|---|---|
| `Scripting/v61b/` | Current versioned Blender workflow with main script, tuning tools, and encoding helpers. |
| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/` | Additional AI-generated or AI-refined Blender package related to audio-sync/profile workflow. |

## Guidelines for AI systems

- Treat each subfolder as a potentially independent Blender package or project variant.
- Read the subfolder README before editing its files.
- Do not assume that every package uses the same JSON schema or entry point.
- Keep audio paths, JSON paths, render paths, and FFmpeg paths configurable.
- Do not collapse separate generated packages into one folder unless explicitly requested.
- Preserve package-specific installation notes such as `INSTALL_LOCATION.txt`.
- When modifying scripts, report the resulting line count for every script changed.

## Versioned folders and generated packages

Versioned folders such as `v61b/` represent implementation snapshots or workflow iterations.

Named folders such as `ready_to_jazz_wow_youtube_profiles_audio_sync/` may represent generated packages based on a specific track, concept, or audio-analysis workflow.

## Future local AI objective

The intended direction is to reduce dependency on remote/manual AI coding loops by using local tools where possible. Candidate local components may include:

- local code indexing;
- local compact context generation;
- local model-assisted patch planning;
- NPU/GPU-assisted review or implementation support;
- validated patch application through repository tooling.

This future workflow is not fully specified yet and should be documented in `docs/LOCAL_AI_WORKFLOW.md` when implemented.
