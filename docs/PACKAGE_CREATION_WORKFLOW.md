# Package Creation Workflow

## Purpose

This document defines the recommended workflow for creating a new Blender package under `Scripting/` from audio data, JSON analysis, and AI-assisted coding.

## Workflow overview

```text
Audio track
  -> technical analysis
  -> full JSON data
  -> compact summary JSON
  -> creative brief
  -> implementation plan
  -> generated Blender package
  -> Blender validation
  -> render test
  -> FFmpeg encoding
  -> report
```

## Step 1: create a package folder

Use a descriptive package folder name:

```text
Scripting/track_name_visual_concept/
```

Avoid overwriting older attempts. Create a new folder for major concepts or versions.

## Step 2: prepare context files

Before generating code, prepare:

```text
README.md
AGENT_CONTEXT.md
CREATIVE_BRIEF.md
IMPLEMENTATION_PLAN.md
TEST_CHECKLIST.md
inputs/track_summary.json
inputs/music_context.json
inputs/input_schema.json
```

The full analysis JSON may live outside the package if it is too large. The package should document where it is expected.

## Step 3: define the visual intent

The creative brief should specify:

- mood;
- color language;
- scene objects;
- motion style;
- camera behavior;
- lighting behavior;
- fog or atmosphere behavior;
- audio features mapped to visuals;
- what to avoid.

## Step 4: generate an implementation plan

The implementation plan should define:

- files to create;
- files to modify;
- functions or modules needed;
- input data used;
- output expected;
- known risks;
- test procedure.

Do not generate complex code before the plan is coherent.

## Step 5: generate modular code

Use the `v61b` style as the quality reference.

Recommended modules:

```text
main.py
config.py
audio_mapping.py
scene_objects.py
materials.py
camera.py
lighting.py
render_settings.py
encode_ffmpeg.py
```

For reusable operational logic, check `Scripting/shared/` first.

## Step 6: validate in Blender

Run the script in Blender and check:

- syntax errors;
- missing paths;
- missing JSON fields;
- missing materials or nodes;
- camera and lights;
- frame range;
- render settings.

## Step 7: render test

Before final render, run a small test range and inspect output.

## Step 8: encode video

Use FFmpeg settings documented by the package. Keep CPU and GPU profiles separate.

## Step 9: write report

Create or update `REPORT.md` with:

- files created;
- files modified;
- entry point;
- input files;
- output files;
- tests performed;
- issues found;
- next improvements.

## AI rules

- Do not skip documentation files for serious packages.
- Do not generate code directly from a large JSON without a compact summary.
- Do not overwrite previous packages.
- Do not refactor working reference packages unless explicitly requested and tested.
- Use `docs/QUALITY_GATE.md` for acceptance criteria.
