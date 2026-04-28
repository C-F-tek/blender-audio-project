# Module Map

## Purpose

This document maps the main repository areas so developers and AI systems can quickly understand where to look before modifying code.

## Repository areas

| Area | Role | Notes |
|---|---|---|
| `Scripting/` | Blender Python scripting workspace | Main area for scene-generation scripts. |
| `Scripting/v61b/` | Current versioned Blender workflow | Contains the current v61b implementation and scene-tuning material. |
| `Scripting/v61b/main_v61b.py` | Main known Blender script entry point | Treat as a primary script until a newer entry point is documented. |
| `Scripting/v61b/SCENE_TUNING_GUIDE.md` | Scene tuning guide | Existing technical guide for tuning the scene. |
| `Scripting/v61b/hotpatch/` | Patch and diagnostic scripts | Use for focused fixes, diagnostics, and isolated changes. |
| `Tools/npu/` | AI and NPU support tooling | Contains context builders, dual-AI pipeline tools, and technical notes. |
| `indexAI/` | AI-oriented project index | Contains generated code indexes, manifests, and patch-library material. |
| `indexAI/patch_library/` | AI patch and task packet material | Contains generated or curated patch/task artifacts. |
| `docs/` | Stable project documentation | Human and AI-readable documentation. |
| `examples/` | Example area | Reserved for reproducible examples. |

## AI navigation order

1. Read `README.md`.
2. Read `AGENTS.md`.
3. Read this file.
4. Read `docs/DATA_FLOW.md`.
5. Read the folder README for the target area.
6. Inspect the actual script before editing.

## Editing guidance

- Prefer changes in the smallest relevant module.
- Preserve versioned folders.
- Do not replace generated context files without checking their source generator.
- For Blender runtime issues, inspect `Scripting/v61b/main_v61b.py` first.
- For AI context or generated implementation packets, inspect `Tools/npu/` and `indexAI/` first.

## Not specified

A full function-level module index is not specified yet. Generate it from code when needed.
