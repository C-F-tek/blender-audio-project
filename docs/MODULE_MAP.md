# Module Map

## Purpose

This document maps the main repository areas so developers and AI systems can quickly understand where to look before modifying code.

## Repository areas

| Area | Role | Notes |
|---|---|---|
| `Scripting/` | Blender package/script workspace | Contains versioned workflows and AI-generated Blender packages based on audio-analysis data. |
| `Scripting/v61b/` | Current versioned Blender workflow | Contains the current v61b implementation, tuning tools, and encoding helpers. |
| `Scripting/v61b/main_v61b.py` | Main known Blender script entry point for v61b | Treat as a primary script for the v61b workflow until a newer entry point is documented. |
| `Scripting/v61b/SCENE_TUNING_GUIDE.md` | Scene tuning guide | Existing technical guide for tuning the scene. |
| `Scripting/v61b/hotpatch/` | Patch and diagnostic scripts | Use for focused fixes, diagnostics, and isolated changes. |
| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/` | Additional Blender package/project variant | AI-generated or AI-refined workflow related to audio-sync/profile-based generation. |
| `Tools/npu/` | AI and NPU support tooling | Contains context builders, dual-AI pipeline tools, and technical notes. |
| `Tools/repo_patch_runner/` | Patch runner tooling | Supports structured repository patch workflows. |
| `indexAI/` | AI-oriented project index | Contains generated code indexes, manifests, and patch-library material. |
| `indexAI/patch_library/` | AI patch and task packet material | Contains generated or curated patch/task artifacts. |
| `docs/` | Stable project documentation | Human and AI-readable documentation. |
| `examples/` | Example area | Reserved for reproducible examples. |

## AI navigation order

1. Read `README.md`.
2. Read `AGENTS.md`.
3. Read this file.
4. Read `docs/DATA_FLOW.md`.
5. Read `Scripting/README.md`.
6. Read the README of the specific package under `Scripting/`.
7. Inspect the actual script before editing.

## Generated package model

The `Scripting/` folder can contain multiple generated Blender packages. A package may correspond to:

- a track;
- a visual concept;
- an audio-analysis workflow;
- a render target;
- an AI-generated implementation attempt;
- a refined production version.

Do not assume that all packages share the same entry point, JSON schema, installation path, or render strategy.

## Editing guidance

- Prefer changes in the smallest relevant package or module.
- Preserve versioned folders and named generated packages.
- Do not replace generated context files without checking their source generator.
- For v61b runtime issues, inspect `Scripting/v61b/main_v61b.py` first.
- For package-specific issues, inspect that package README and installation notes first.
- For AI context or generated implementation packets, inspect `Tools/npu/` and `indexAI/` first.

## Not specified

A full function-level module index is not specified yet. Generate it from code when needed.
