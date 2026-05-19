# Non-Tools script context pass — 2026-05-19

## Scope

Second documentation pass after the initial `Tools/**` context files.

The operator noted that the repository contains many scripts outside the `Tools/**` dispatcher system. This task records the additional context layer for those script surfaces.

## Reason

The first pass documented:

```text
Tools/** dispatchers and tool families
core Tools/ai families
root CHATGPT.md contract
```

That is not enough for the whole repository because important executable/semi-executable surfaces also live under:

```text
Scripting/**
docs/LOCAL_AI_TASKS/**
docs/LOCAL_VALIDATION_EVIDENCE/**
docs/AI_SESSION_NOTES/**
CHATGPT/**
config/**
assets/**
indexAI/**
```

## Files added in this pass

```text
docs/SCRIPT_SURFACE_CONTEXT.md
Scripting/TOOL_CONTEXT.md
Scripting/v61b/TOOL_CONTEXT.md
Scripting/shared/TOOL_CONTEXT.md
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/TOOL_CONTEXT.md
Scripting/_template_audio_reactive_package/TOOL_CONTEXT.md
config/TOOL_CONTEXT.md
assets/TOOL_CONTEXT.md
indexAI/TOOL_CONTEXT.md
docs/LOCAL_AI_TASKS/TOOL_CONTEXT.md
docs/LOCAL_VALIDATION_EVIDENCE/TOOL_CONTEXT.md
docs/AI_SESSION_NOTES/TOOL_CONTEXT.md
```

## Key findings captured

- `Scripting/**` is product/Blender/audio/video scripting, not IA-Carmine orchestration tooling.
- `Scripting/v61b` is the current working Blender reference package.
- `Scripting/shared` is the target for additive, validated utility extraction.
- `ready_to_jazz_wow_youtube_profiles_audio_sync` is a standalone Blender/YouTube render/encode package.
- `_template_audio_reactive_package` is a scaffold for future packages, not production runtime by itself.
- Markdown task files can drive workflows only when passed to a launcher/tool; they are not runtime by themselves.
- Compact validation evidence belongs under `docs/LOCAL_VALIDATION_EVIDENCE/**`; raw runtime output stays outside Git.
- `config/**` can change safe apply, allowlists and product gates; inspect it before changing behavior.
- `indexAI/**` is index/memory/chunk support material, not generic source code.

## Completed status

```text
[x] Non-Tools surface index created.
[x] Scripting package context added.
[x] Main Blender reference package context added.
[x] Shared scripting utility context added.
[x] Ready-to-Jazz package context added.
[x] Template package context added.
[x] Config/assets/indexAI context added.
[x] Local task/evidence/session note contexts added.
```

## Remaining candidates

```text
docs/EXECUTION_PLANS/TOOL_CONTEXT.md
docs/PACKAGE_CREATION_WORKFLOW.md alignment check
docs/PROJECT_AUDIT.md alignment check
root-level standalone file audit, if any root scripts remain after package cleanup
```

## Guardrails

This is documentation-only. Do not run Blender, providers, patch apply, or destructive Git operations as part of this pass.

Keep generated frames, renders, runtime output, databases and generated chunk caches out of Git.
