# Audio Reactive Package Template

## Purpose

This folder is a reusable template for new Blender audio-reactive packages generated or refined by AI systems.

Copy this folder to a new package name before starting a new project.

Example:

```text
Scripting/track_name_visual_concept/
```

This is application-domain runtime material. It is not part of normal local-AI run-unica validation unless an explicit Blender/audio/media task scopes it.

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
  -> explicit Blender validation when scoped
  -> explicit render test when scoped
  -> explicit FFmpeg encoding when scoped
  -> final report
```

Blender render, FFmpeg encode/mux and media output are explicit application-domain actions, not normal AI/tooling side effects.

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

## 400-line policy

Maintained generated package files should stay under 400 lines.

```text
Code/script >400 lines -> compact entrypoint + responsibility-based module/package split.
Markdown >400 lines -> compact index + <file>.md/part-001.md layout.
Existing oversized files -> technical debt to refactor progressively, not blind split targets.
```

## Rules

- Do not hardcode private paths in reusable code.
- Keep paths configurable in `config.py`.
- Keep audio mapping separate from scene construction.
- Use `Scripting/shared/` for reusable operational utilities when available.
- Keep package-specific creative logic inside the package.
- Document unverified assumptions and limitations as backlog to overcome.
- Do not apply patches automatically from generated plans.
- Do not run Blender, FFmpeg or media output unless explicitly scoped.
- Report changed files, risks, validation status and script line counts.
