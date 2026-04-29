# Copilot Instructions

These instructions apply to AI coding assistants working on `blender-audio-project`.

## Repository role

This repository is a Blender audio-reactive production workspace. It contains Python audio-analysis tools, Blender scene packages, FFmpeg encoding helpers, AI/NPU artifact pipelines, generated indexes, and project documentation.

## Required context

Before editing code, read:

1. `AGENTS.md`
2. `README.md`
3. `docs/README.md`
4. `docs/MODULE_MAP.md`
5. `docs/DATA_FLOW.md`
6. `docs/REFACTORING_AND_REUSE_PLAN.md`
7. `docs/QUALITY_GATE.md`
8. the README of the target package under `Scripting/`
9. the target source file

## Fast validation commands

Prefer focused checks:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
```

Use report files when useful:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output output\validation\python_syntax.json
python .\Tools\validation\check_package_structure.py --repo-root . --output output\validation\package_structure.json
python .\Tools\validation\check_json_artifacts.py --repo-root . --output output\validation\json_artifacts.json
```

## Safe editing rules

- Prefer additive changes.
- Do not destructively refactor `Scripting/v61b/`.
- Do not rewrite large generated scene scripts unless explicitly requested.
- Do not overwrite full frame-by-frame analysis JSON files.
- Do not hardcode private workstation paths in reusable modules.
- Keep Blender runtime behavior separate from infrastructure refactors.
- Keep generated indexes under `indexAI/` out of source-level refactors.
- Report line counts for created or modified scripts.

## Shared utility direction

Reusable operational logic belongs under `Scripting/shared/`.

Current preferred extraction order:

```text
path_utils.py
json_io.py
image_sequence.py
ffmpeg_encoder.py
render_profiles.py
blender_compat.py
```

Create shared modules first, validate them, then add adapters to existing packages.

## Package-specific instructions

Additional instructions live under `.github/instructions/`:

- `blender-python.instructions.md`
- `audio-pipeline.instructions.md`
- `ffmpeg-render.instructions.md`
- `ai-pipeline.instructions.md`
