# Agent Context

## Package role

This is a template package for future Blender audio-reactive visual projects.

AI systems should copy this folder to a new package name before generating project-specific code.

## Required reading

Before editing a package based on this template, read:

1. repository `AGENTS.md`;
2. `docs/AI_GENERATED_PACKAGE_STANDARD.md`;
3. `docs/PACKAGE_CREATION_WORKFLOW.md`;
4. `docs/QUALITY_GATE.md`;
5. `docs/SHARED_SCRIPTING_UTILITIES.md`;
6. this package README;
7. the target Python file.

## Modification rules

- Keep `main.py` as orchestration.
- Keep paths and constants in `config.py`.
- Keep audio mapping in `audio_mapping.py`.
- Keep object creation in `scene_objects.py`.
- Keep materials in `materials.py`.
- Keep camera logic in `camera.py`.
- Keep lighting in `lighting.py`.
- Keep render setup in `render_settings.py`.
- Keep FFmpeg wrapper logic in `encode_ffmpeg.py`.
- Prefer shared utilities for generic logic.

## Safety rules

- Do not overwrite full analysis JSON files.
- Do not hardcode private paths unless explicitly marked local-only.
- Do not remove package documentation.
- Do not merge unrelated package concepts.
- Do not reduce a full visual package to a minimal demo unless requested.

## Required output after changes

Report:

- files changed;
- purpose;
- assumptions;
- tests performed;
- risks;
- line counts for every created or modified script.
