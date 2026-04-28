# AI Generated Package Standard

## Purpose

This document defines the preferred standard for new Blender packages generated or refined by AI systems in this repository.

## Reference model

`Scripting/v61b/` is the preferred reference model for package complexity, composition quality, and scripting organization.

Future generated packages should use `v61b` as the baseline unless the user explicitly requests a quick prototype or minimal demo.

## Quality target

Generated packages should aim for:

- rich scene composition;
- modular Python structure;
- clear configuration;
- explicit audio-to-visual mapping;
- advanced material, camera, lighting, and atmosphere logic;
- render and encoding support;
- package-level documentation;
- safe path configuration;
- traceable assumptions.

## Minimum recommended package structure

```text
Scripting/package_name/
  README.md
  AGENT_CONTEXT.md
  CREATIVE_BRIEF.md
  IMPLEMENTATION_PLAN.md
  TEST_CHECKLIST.md
  REPORT.md
  main.py
  config.py
  audio_mapping.py
  scene_objects.py
  materials.py
  camera.py
  lighting.py
  render_settings.py
  encode_ffmpeg.py
  inputs/
    README.md
    input_schema.json
    track_summary.json
    music_context.json
  outputs/
    README.md
  notes/
    known_issues.md
    tuning_notes.md
```

## Required package documentation

Every serious generated package should include:

| File | Purpose |
|---|---|
| `README.md` | Entry point, purpose, inputs, outputs, status. |
| `AGENT_CONTEXT.md` | AI-specific package context and modification rules. |
| `CREATIVE_BRIEF.md` | Visual intent, mood, references, and constraints. |
| `IMPLEMENTATION_PLAN.md` | Planned files, functions, risks, and tests. |
| `TEST_CHECKLIST.md` | Blender and render validation checklist. |
| `REPORT.md` | Final generation or modification report. |

## Required code qualities

- Keep `main.py` as orchestration, not as the only place for all logic.
- Keep paths and constants in `config.py` or equivalent.
- Keep audio mapping separate from scene object creation.
- Keep material logic separate from camera and lighting logic.
- Keep render and encoding settings explicit.
- Add comments around Blender API compatibility-sensitive code.

## Audio-driven requirements

The package should explain:

- which audio file or track it targets;
- which JSON summary or analysis data it expects;
- which audio features drive which visual parameters;
- how duration and frame range are computed;
- which values are configurable.

## AI rules

- Do not generate a simplistic one-file demo when the user asks for a complete visual package.
- Do not invent JSON fields without documenting them as assumptions.
- Do not hardcode private workstation paths unless the package is explicitly local-only.
- Do not overwrite previous generated packages.
- Create a new package folder for major visual concepts or tracks.
- Use `Scripting/v61b/` as the reference for depth and modularity.

## Not specified

- Final package generator command.
- Final local AI model.
- Final validation runner.
- Final Blender version matrix.
