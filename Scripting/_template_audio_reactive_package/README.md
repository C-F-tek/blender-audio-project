# Audio Reactive Package Template

## Purpose

This folder is a reusable template for new Blender audio-reactive packages generated or refined by AI systems.

Copy this folder to a new package name before starting a new project.

Example:

```text
Scripting/track_name_visual_concept/
```

## Package status

Template only. Do not run this package as a final production script without filling the configuration and project-specific files.

## Reference model

Use `Scripting/v61b/` as the quality and complexity reference.

This template provides structure; `v61b` provides the richer working example.

## Expected workflow

```text
Audio track
  -> analysis JSON
  -> compact summary JSON
  -> creative brief
  -> implementation plan
  -> generated Blender package
  -> Blender validation
  -> render test
  -> FFmpeg encoding
  -> final report
```

## Main files

| File | Role |
|---|---|
| `main.py` | Package entry point and orchestration. |
| `config.py` | Paths, render settings, and package constants. |
| `audio_mapping.py` | Audio feature to visual parameter mapping. |
| `scene_objects.py` | Scene object creation. |
| `materials.py` | Material and shader setup. |
| `camera.py` | Camera creation and animation. |
| `lighting.py` | Light setup and animation. |
| `render_settings.py` | Blender render configuration. |
| `encode_ffmpeg.py` | FFmpeg wrapper or package-specific encoding entry point. |

## Documentation files

| File | Role |
|---|---|
| `AGENT_CONTEXT.md` | Rules for AI systems working on this package. |
| `CREATIVE_BRIEF.md` | Visual intent and audio-reactive concept. |
| `IMPLEMENTATION_PLAN.md` | Planned implementation structure. |
| `TEST_CHECKLIST.md` | Validation checklist. |
| `REPORT.md` | Final generation or modification report. |

## Rules

- Do not hardcode private paths in reusable code.
- Keep paths configurable in `config.py`.
- Keep audio mapping separate from scene construction.
- Use `Scripting/shared/` for reusable operational utilities when available.
- Keep package-specific creative logic inside the package.
- Document unverified assumptions as `not specified`.
