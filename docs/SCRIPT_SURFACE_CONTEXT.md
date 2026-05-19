# Script surface context

## Purpose

This document maps important executable or semi-executable surfaces that are outside the `Tools/**` dispatcher system.

`Tools/**` is the IA-Carmine operator/runtime/tooling layer. Other script areas exist and must not be ignored by AI agents when analyzing the repository.

## Primary non-Tools areas

| Area | Role | Notes |
| --- | --- | --- |
| `Scripting/**` | Blender/audio/video product scripting | Scene generation, render setup, animation, encoding and shared Blender utilities. |
| `docs/LOCAL_AI_TASKS/**` | Operator task/run request documents | Markdown task specs consumed by local AI workflows or used as handoff/run instructions. |
| `docs/LOCAL_VALIDATION_EVIDENCE/**` | Compact Git-trackable evidence | Validation/evidence summaries. Raw runtime output should remain under `output/**`. |
| `docs/AI_SESSION_NOTES/**` | Session and decision notes | Human/AI-readable notes; not runtime source by themselves. |
| `CHATGPT.md` | Root ChatGPT/GPT operating contract | Defines how chat clients should read, verify and avoid replacing heap/runtime memory. |
| `CHATGPT/**` | Historical/advisory handoff folder | Useful context, but subordinate to root `CHATGPT.md`. |
| `config/**` | Repository configuration and allowlists | Can affect source allowlists, product gates and safe apply behavior. |
| `assets/**` | Project assets | Inputs for creative/Blender workflows; generated outputs are not committed. |
| `indexAI/**` | AI index/memory area | Contains memory/index/chunk artifacts; generated chunk caches are normally excluded. |

## Scripting packages

`Scripting/TOOL_CONTEXT.md` is the index for Blender/audio/video package scripts.

Known important packages:

```text
Scripting/v61b
Scripting/shared
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync
Scripting/_template_audio_reactive_package
```

`Scripting/v61b` is the current working Blender reference package. Its main script is `main_v61b.py`; encoding helpers include `encode_image_sequence_v61b.py` and related FFmpeg/image-sequence utilities.

## Docs as executable context

Markdown in `docs/LOCAL_AI_TASKS/**` may be used as request input for local AI runs. It is not code, but it can drive a workflow when passed to a launcher or task runner.

Rules:

- A task Markdown is not executed by itself.
- A generated command is not a completed run.
- A completed run requires output artifacts, reports and return codes.
- Stale task docs must not override current dispatchers or code.

## Evidence boundaries

`docs/LOCAL_VALIDATION_EVIDENCE/**` may contain compact evidence intended for Git. It should not be used as a dump location for raw runtime output.

Do not commit:

```text
output/**
*.db
*.sqlite
*.sqlite-wal
*.sqlite-shm
renders/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
```

## Recommended AI navigation order

When analyzing the repository, use this order:

1. `CHATGPT.md` for operating contract.
2. `Tools/TOOL_CONTEXT.md` for tool areas.
3. Area-level `TOOL_CONTEXT.md` files.
4. `docs/SCRIPT_SURFACE_CONTEXT.md` for non-Tools surfaces.
5. `Scripting/TOOL_CONTEXT.md` and package-local context files.
6. Current dispatchers and actual source files.
7. Current run/evidence artifacts only when explicitly relevant.

## Extension rule

If a new executable surface is added outside `Tools/**`, add a short context file or update this index. Otherwise future AI runs will miss it or treat it as an unrelated script.
