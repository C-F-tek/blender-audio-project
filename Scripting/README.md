# Scripting

`Scripting/` is the main workspace for Blender scene packages generated, refined or maintained from audio-analysis data and AI-assisted workflows.

This folder is not a generic script dump. Each subfolder should be treated as a potential Blender package, workflow snapshot, generated scene implementation or reusable support area.

## Current roles

- Store Blender Python packages and scene scripts.
- Preserve versioned scene-generation workflows.
- Store AI-generated or AI-refined packages.
- Keep package-specific documentation near the code.
- Preserve multiple project variants when they represent different tracks, visual concepts or render strategies.
- Provide a shared utility target for reusable operational code.

## Known project/package areas

| Path | Role |
|---|---|
| `Scripting/v61b/` | Current reference Blender workflow with modular scene setup, tuning tools, hotpatch support and encoding helpers. |
| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/` | Additional generated/refined package with a large scene script and YouTube-oriented encoding workflow. |
| `Scripting/_template_audio_reactive_package/` | Template for future generated packages. |
| `Scripting/shared/` | Target for reusable package-agnostic utilities. |

## Package rules

Each non-shared package should document:

- entry point;
- required input JSON files;
- required audio file;
- expected output folders;
- Blender version assumptions;
- FFmpeg/render workflow;
- known limitations;
- line counts for generated scripts when relevant.

## Preferred package structure

For future production packages:

```text
package_name/
  README.md
  main.py
  config.py
  pipeline.py
  audio_mapping.py
  scene_objects.py
  materials.py
  lighting.py
  camera.py
  animation.py
  render_settings.py
  encode.py
  diagnostics.py
  inputs/
    README.md
    input_schema.json
  outputs/
    README.md
  notes/
    known_issues.md
    tuning_notes.md
```

The exact module names may change, but separation of concerns should remain.

## Shared utility strategy

Reusable operational code should move toward:

```text
Scripting/shared/path_utils.py
Scripting/shared/json_io.py
Scripting/shared/blender_compat.py
Scripting/shared/image_sequence.py
Scripting/shared/ffmpeg_encoder.py
Scripting/shared/render_profiles.py
Scripting/shared/diagnostics.py
```

Do not move code out of a working package destructively. First create the shared utility, test it, then add an optional adapter.

## AI generation guidance

When an AI system creates or edits a package:

1. Read the root `README.md`.
2. Read `AGENTS.md`.
3. Read `docs/MODULE_MAP.md`.
4. Read `docs/REFACTORING_AND_REUSE_PLAN.md`.
5. Read this file.
6. Read the target package README.
7. Inspect the target script before editing.
8. Prefer focused patches over complete rewrites.
9. Keep paths configurable.
10. Report changed files, risks, tests and script line counts.

## Versioned folders and generated packages

Versioned folders such as `v61b/` represent implementation snapshots or workflow iterations.

Named folders such as `ready_to_jazz_wow_youtube_profiles_audio_sync/` may represent generated packages based on a specific track, concept or audio-analysis workflow.

Do not collapse separate generated packages into one folder unless that is explicitly requested.

## Future local AI objective

The intended direction is to reduce dependency on manual remote-AI coding loops by using local tools where practical:

- local code indexing;
- compact context generation;
- NPU technical review;
- GPU/Ollama creative or implementation planning;
- deterministic fallback generation;
- validated patch application.

The detailed roadmap is documented in `docs/LOCAL_AI_WORKFLOW.md`, `docs/AI_PIPELINE_OPTIMIZATION.md` and `docs/REFACTORING_AND_REUSE_PLAN.md`.
