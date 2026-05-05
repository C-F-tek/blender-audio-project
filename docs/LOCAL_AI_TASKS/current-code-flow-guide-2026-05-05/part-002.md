<!-- IA-CARMINE-MD-SPLIT: part -->
# current-code-flow-guide-2026-05-05 — parte 002 di 002

Sorgente indice: [`../current-code-flow-guide-2026-05-05.md`](../current-code-flow-guide-2026-05-05.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)

## Production AI-to-AI bundle flow

Builder:

    Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py

Standard production communication bundle:

    docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.json
    docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.md

Companion evidence:

    docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_<STAMP>.json
    docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_<STAMP>.md
    docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_<STAMP>.json
    docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_<STAMP>.md
    docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_<STAMP>.json
    docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_<STAMP>.md
    docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_<STAMP>_cloud_semantic_deterministic_chunk_manifest.json
    docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_<STAMP>_cloud_semantic_deterministic_chunk_manifest.md
    docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_<STAMP>.json
    docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_<STAMP>.md

Production-complete requires:

    patch_plan_summary_seen=True
    provider_diagnostics present
    runtime broker telemetry executed_count >= 3 when broker lane ran
    runtime broker capability manifest present
    repository consistency map/smoke present when produced
    discovery/index/CSV surfaces present when selected or relevant
    full toolbox telemetry summary present
    patch_application_performed=false
    source_writes_performed=false

## Non-canonical tool flow

Some project tools live outside `Tools/**`.

Root audio tools:

    analyze_wav.py
    build_track_summary.py

Blender/audio runtime tools:

    Scripting/v61b/main_v61b.py
    Scripting/v61b/hot_update_scene_v61b.py
    Scripting/v61b/encode_image_sequence_v61b.py
    Scripting/v61b/encode_ffmpeg_v61b.py
    Scripting/v61b/scene_tuning_panel.py

Template/candidate scripts:

    Scripting/_template_audio_reactive_package/main.py
    Tools/npu/generated_blender_script_candidate.py
    Tools/npu/generated_blender_script_candidate_FristNear.py

Rule:

    These can be project tools, but not broker tools by default.
    They may touch Blender, FFmpeg, renders, audio, UI or generated code.

## Git and manual-only flow

Manual-only or dangerous tools include:

    Tools/workflow/workflow_shell_with_push.py
    Tools/workflow/git_auto_push.py
    Tools/git/auto_push_generated_data.ps1
    Tools/git/auto_push_generated_artifacts.ps1
    Tools/workflow/gui/workflow_gui_with_push.py

Rules:

    no broker execution
    no unattended full-run execution
    explicit user command required
    no merge to master without explicit instruction
    no force push
    no delete/rewrite history

## Evidence commit flow

After a successful production run, stage only selected files under:

    docs/LOCAL_VALIDATION_EVIDENCE

Do not stage:

    output/**
    indexAI/code_chunks/**
    docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_*
    docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_*_cloud_semantic_deterministic_chunks/
    *.db
    *.sqlite
    renders/**

Allowed compact production evidence examples:

    shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
    full_toolbox_run_telemetry_summary_<STAMP>.json/md
    runtime_tool_usage_telemetry_<STAMP>.json/md
    runtime_tool_capability_manifest_<STAMP>.json/md
    full_toolbox_<STAMP>_cloud_semantic_deterministic_chunk_manifest.json/md
    full_toolbox_agent_review_decision_loop_<STAMP>.json/md
    script/function/class inventory CSV/MD summaries
    Python line-count CSV/MD summaries
    repository consistency map/smoke summaries
    discovery/index repair plan summaries

## Current known next step

Current P1:

    inspect the refactor/reuse full-run runtime bundle for 20260505-143844 and classify recommendations/patch plans before selecting a review-first patch

Candidate P1 patch family, pending bundle review:

    centralize report/telemetry helper functions in Tools/validation/report_utils.py
    reuse them from Tools/ai/build_runtime_tool_usage_telemetry.py
    reuse them from Tools/ai/build_full_toolbox_run_telemetry_summary.py
    evaluate Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py separately

Follow-up, not current P1 unless explicitly selected:

    finish external-control pass-through for the unified launcher subordinate calls
    docs/LOCAL_AI_TASKS/next-chat-unified-launcher-external-controls.md

Do not relabel old broker-telemetry loss as an open issue; it was closed by a85bbf4 and validated by run 20260505-073332.

## Related docs

    docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
    docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
    docs/LOCAL_AI_TASKS/refactor-reuse-full-run-documentation-coherence-2026-05-05.md
    docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
    docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
    docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
    FULL_RUN_UNICA_TUTTO_SU_TUTTO.md
    CHATGPT/README.md
