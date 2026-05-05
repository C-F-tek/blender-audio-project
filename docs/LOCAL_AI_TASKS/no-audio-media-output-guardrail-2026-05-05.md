# IA-Carmine no audio/media output guardrail — 2026-05-05

Repository: `C-F-tek/blender-audio-project`

Branch: `codex/unified-local-ai-refactor-launcher`

## Purpose

The current IA-Carmine full-run and tooling layer is an orchestration, validation, provider, evidence, broker and patch-plan system.

It must not produce application-domain audio or media output unless the user explicitly asks for an application-domain Blender/audio/render/encode task.

## Rule

For normal AI/tooling runs, documentation cleanup, provider diagnostics, tool promotion, broker telemetry, patch planning and evidence generation:

    no audio playback
    no audio export
    no WAV/MP3/AAC render or conversion
    no FFmpeg encode/mux operation
    no Blender render
    no video generation
    no media output side effect

Allowed outputs are report/evidence artifacts only:

    JSON reports
    Markdown summaries
    CSV inventories
    compact evidence under docs/LOCAL_VALIDATION_EVIDENCE
    ignored local reports under output/**

## Explicit exception

Audio/media output is allowed only when the task is explicitly scoped as application-domain runtime work, for example:

    analyze this WAV
    render this Blender scene
    encode this image sequence
    generate final video
    create audio-reactive Blender output

Even then, the operator must keep generated media out of Git and report the produced paths separately.

## Tool classification

These are project tools or application tools, not broker-safe tools by default:

    analyze_wav.py
    build_track_summary.py
    Scripting/v61b/main_v61b.py
    Scripting/v61b/encode_image_sequence_v61b.py
    Scripting/v61b/encode_ffmpeg_v61b.py
    Scripting/v61b/hot_update_scene_v61b.py
    Scripting/v61b/scene_tuning_panel.py

They may be documented and promoted as project tools, but they must not be automatically executed by full-run AI/tooling validation lanes unless an explicit application-domain task enables them.

## Full-run expectation

A valid full-run tooling/evidence cycle may use provider compute, validators, inventories, context packs, memory packets, broker reports and patch-plan generation.

It must not create audio or video output as part of that flow.

If audio/media output appears during a non-application run, classify it as a workflow guardrail breach and document:

    which phase produced it
    which tool produced it
    exact file path
    whether it was tracked or ignored
    how to disable it

## Git policy

Never commit generated media outputs:

    renders/**
    output media files
    generated audio/video files
    encoded videos
    temporary muxed media

Commit only compact evidence when required by the workflow policy.

## Related docs

    AGENTS.md
    docs/LOCAL_AI_RUN_BOOTSTRAP.md
    docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
    docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
    docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
