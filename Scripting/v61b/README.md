# Scripting/v61b

This folder contains the preferred reference model for complex Blender scripting in this repository.

## Role in the project

`v61b` is the current qualitative reference for:

- scene composition complexity;
- modular Blender Python scripting;
- audio-reactive visual logic;
- scene tuning;
- render and encoding support;
- structured development of a complete visual package.

Future AI-generated Blender packages should use this folder as a reference for expected depth and technical ambition, unless a simpler prototype is explicitly requested.

## Purpose

The folder is used for scene generation, tuning, and related Blender Python logic. It represents a more advanced style than a single minimal script and should be treated as a model for production-oriented package structure.

## Expected content

- Main Blender entry-point script.
- Configuration module.
- Scene tuning modules.
- Material helpers.
- Lighting helpers.
- Camera helpers.
- Fog or atmosphere helpers.
- Animation and audio-mapping logic.
- Render or encoding helpers.
- Hotpatch and diagnostics utilities where needed.
- Workflow-specific documentation.

## Known relevant files

| File or folder | Role |
|---|---|
| `main_v61b.py` | Main known entry point for the v61b workflow. |
| `config.py` | Configuration area for the workflow. |
| `scene_tuning_panel.py` | Blender scene tuning panel or related UI logic. |
| `SCENE_TUNING_GUIDE.md` | Scene tuning guide. |
| `hot_update_scene_v61b.py` | Hot update helper for scene adjustments. |
| `encode_ffmpeg_v61b.py` | FFmpeg-oriented encoding helper. |
| `encode_image_sequence_v61b.py` | Image-sequence encoding helper. |
| `hotpatch/` | Focused diagnostic or patch utilities. |

## Preferred style for future AI-generated packages

A new package under `Scripting/` should not be just a flat script when the goal is a serious visual output. Prefer the v61b style:

```text
package_name/
  README.md
  main.py
  config.py
  audio_mapping.py
  scene_objects.py
  materials.py
  camera.py
  lighting.py
  render_settings.py
  encode_ffmpeg.py
  notes/
  inputs/
  outputs/
```

The exact module names can change, but the separation of concerns should remain.

## AI generation guidance

When an AI system creates a new Blender package from audio data:

1. Use `v61b` as the complexity and structure reference.
2. Produce modular code instead of one oversized script when practical.
3. Keep paths configurable in `config.py` or equivalent.
4. Keep audio mapping separate from object/material/camera logic.
5. Include render and encoding support where relevant.
6. Add a package README with entry point, inputs, outputs, and known limitations.
7. Do not reduce the concept to a minimal demo unless explicitly requested.

## Maintenance notes

- Document every public script entry point.
- Keep audio and JSON paths configurable.
- Mark Blender-version-specific code clearly.
- Record known failures and fixes in comments or documentation.
- Report line counts after modifying scripts.

## Not specified

A full function-level module map is not specified yet. Generate it from the code when needed.
