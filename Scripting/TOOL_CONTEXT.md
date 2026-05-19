# Scripting context index

## Role

`Scripting/` contains Blender/audio/video production scripts and package-specific scene generation code. This area is separate from `Tools/`: it is product/project scripting, not IA-Carmine orchestration infrastructure.

Use this context when an AI agent needs to understand render scripts, Blender scene packages, FFmpeg encoding helpers, shared scripting utilities or generated creative packages.

## Main areas

| Area | Role |
| --- | --- |
| `Scripting/v61b` | Current working Blender package/reference model for the Spaziotempo audio-reactive scene. |
| `Scripting/shared` | Target area for reusable Blender/FFmpeg/path/JSON/render utilities extracted safely from working packages. |
| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync` | Standalone Blender/YouTube profile package with frame sequence + audio sync encoding workflow. |
| `Scripting/_template_audio_reactive_package` | Template/scaffold area for generated or future audio-reactive packages. |

## Distinction from Tools

```text
Tools/**      -> AI/runtime/broker/validation/operator tooling
Scripting/**  -> Blender scene code, render setup, encoding helpers and package scripts
```

Do not move Blender package code into `Tools` just because it is a script. Use `Tools` to inspect, validate, package or generate support artifacts; keep creative/runtime Blender package code in `Scripting`.

## Execution model

Many scripts here are meant to run inside Blender, not plain Python:

```text
Blender Text Editor -> open script -> Alt+P
or Blender Python context with bpy available
```

Pure helpers under `Scripting/shared` should be designed to compile/test outside Blender when possible.

## Safety rules

- Do not destructively refactor working scene packages only for abstraction.
- Keep `Scripting/v61b` stable unless the change is targeted and validated.
- Extract shared utilities additively into `Scripting/shared` first.
- Validate Blender-specific changes in Blender when they touch `bpy`, VSE, render settings, nodes or scene objects.
- Generated frames, renders and encoded videos are runtime outputs and must not be committed.

## Related docs

- `docs/SHARED_SCRIPTING_UTILITIES.md` defines the shared extraction policy.
- Package-local README files remain the first reference for package-specific run instructions.
