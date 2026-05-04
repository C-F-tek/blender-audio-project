# IA-Carmine current code flow guide — 2026-05-05

Repository: `C-F-tek/blender-audio-project`

Branch: `codex/unified-local-ai-refactor-launcher`

Purpose: describe the current code/tool flow after the full-run, provider bundle and broker telemetry work.

## High-level flow

The current IA-Carmine full-run flow is:

    user task markdown
      -> unified launcher
      -> static inventories and validations
      -> context pack and agent state
      -> provider/probe/workload quality lanes
      -> full-toolbox decision loop
      -> patch plan proposal lane
      -> runtime broker telemetry lane
      -> shared production AI-to-AI bundle
      -> production evidence under docs/LOCAL_VALIDATION_EVIDENCE

Primary launcher:

    Tools/workflow/run_unified_local_ai_refactor.ps1

Full-toolbox decision workflow:

    Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1

Integrated warning policy wrapper:

    Tools/workflow/run_agent_review_full_toolbox_decision_loop_integrated.ps1

## Operator entrypoint

For current branch work, run with:

    -SkipGitSync
    -NoBranch

Reason:

    Without these flags the launcher may switch back to master and create a runtime branch from master, losing branch-specific fixes.

Canonical command family:

    powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
      -Mode all `
      -Full0To10 `
      -SkipGitSync `
      -NoBranch `
      -Stamp $Stamp `
      -TaskFile $TaskFile `
      -OutputDir $OutputDir `
      -EvidenceDir $EvidenceDir `
      -AiPacketsRoot $AiPacketsRoot `
      -AiPacketsDir $AiPacketsDir `
      -Profile core `
      -RunIntensity custom

## Launcher phases

The unified launcher resolves modes such as:

    md
    json
    python
    chunks
    context_pack
    agent_state
    official
    provider
    patch_specs
    evidence
    contract
    full_validation

Main output roots:

    output/validation
    output/ai_pipeline
    output/ai_context_packs
    output/ai_packets/<STAMP>
    output/local_ai_runs/<STAMP>_..._unified
    docs/LOCAL_VALIDATION_EVIDENCE

Git-trackable compact evidence belongs under:

    docs/LOCAL_VALIDATION_EVIDENCE

Runtime/local artifacts belong under:

    output/**

## Static inventory and validation flow

Typical early phases:

    Baseline compile validation/inventory tools
    Build Markdown inventory
    Check docs links
    Validate current JSON/report contracts
    Build script/tool inventory
    Build semantic code chunks
    Build AI context pack
    Build agent state packet
    Validate task-scoped reports

Typical tools:

    Tools/validation/check_python_syntax.py
    Tools/validation/build_markdown_inventory.py
    Tools/validation/check_docs_links.py
    Tools/validation/check_json_artifacts.py
    Tools/validation/build_script_inventory.py
    Tools/npu/build_semantic_code_chunks.py
    Tools/ai/build_ai_context_pack.py
    Tools/ai/build_agent_state_packet.py

## Provider/probe/workload flow

Provider-related phases include:

    Generate provider workload probe inputs
    Build AI workload quality routing report
    Run GPU/NPU provider or orchestrator lane when enabled

Key tools:

    Tools/ai/run_local_provider_probe.py
    Tools/ai/check_local_resource_lanes.py
    Tools/ai/build_workload_quality_lane_routing.py
    Tools/validation/check_ai_workload_report_quality.py
    Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py
    Tools/ai/analyze_gpu_npu_run_sync.py

Important distinction:

    provider_execution_requested can be true even if primary advisory is degraded.
    A run may pass through deterministic recovery if diagnostics are explicit and patch application remains false.

Known current evidence from `20260505-002508`:

    local_provider_probe passed=false with "ollama: probe failed"
    workload quality passed with usable lane npu
    shared bundle exposed provider diagnostics

## Full-toolbox decision loop

Main workflow:

    Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1

Core products:

    output/validation/agent_review_full_toolbox_decision_loop_<STAMP>_workflow.json
    output/validation/agent_review_full_toolbox_decision_loop_<STAMP>_workflow.md
    output/validation/agent_review_full_toolbox_decision_loop_<STAMP>_integrated.json
    output/validation/agent_review_full_toolbox_decision_loop_<STAMP>_integrated.md
    docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_<STAMP>.json
    docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_<STAMP>.md

Decision loop should report:

    passed
    recommendation_count
    patch_plan_count
    provider_execution_performed
    patch_application_performed=false
    source_writes_performed=false

## Patch-plan/proposal flow

Patch-plan support tools include:

    Tools/ai/build_agent_review_patch_plan.py
    Tools/ai/build_agent_review_code_patch_plan.py
    Tools/ai/build_code_edit_proposal_from_plan.py
    Tools/ai/build_code_patch_artifact_pack.py
    Tools/ai/build_code_patch_docs_followup.py

Important output:

    output/patch_specs/full_toolbox_<STAMP>_agent_review_patch_plan.json
    output/patch_specs/full_toolbox_<STAMP>_agent_review_patch_plan.md

The shared production bundle should promote this patch-plan summary.

Acceptance:

    shared_toolbox_ai_to_ai_bundle_<STAMP>.md has patch_plan_summary_seen=True
    patch_plan_count >= 1

## Runtime broker flow

Broker:

    Tools/ai/agent_runtime_tool_broker.py

Runtime telemetry:

    Tools/ai/build_runtime_tool_usage_telemetry.py

Capability manifest:

    Tools/ai/build_runtime_tool_capability_manifest.py

Minimal broker bootstrap tools:

    check_python_syntax
    build_python_line_count_csv
    check_validation_report_contract

Expected artifacts:

    output/validation/runtime_tool_bootstrap_requests_<STAMP>.json
    output/validation/runtime_tool_broker_full_toolbox_<STAMP>.json
    output/validation/runtime_tool_broker_full_toolbox_<STAMP>.md
    docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_<STAMP>.json
    docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_<STAMP>.md
    docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_<STAMP>.json
    docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_<STAMP>.md

Current known bug:

    The broker report can be produced and listed in the shared bundle, but final runtime usage telemetry may still have broker_reports=[] and executed_count=0.

Active follow-up:

    docs/LOCAL_AI_TASKS/fix-final-runtime-broker-telemetry-task-2026-05-05.md

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
    runtime broker telemetry executed_count >= 3
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

## Current known next step

Next code patch:

    fix(ai): preserve broker report in final runtime telemetry

Then rerun a short full-toolbox smoke/full run and verify:

    inputs.broker_reports.Count >= 1
    summary.executed_count >= 3
    summary.failed_count = 0
    summary.blocked_count = 0

## Related docs

    docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
    docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
    docs/LOCAL_AI_TASKS/fix-final-runtime-broker-telemetry-task-2026-05-05.md
    docs/LOCAL_AI_TASKS/post-broker-runtime-telemetry-followup-2026-05-05.md
    FULL_RUN_UNICA_TUTTO_SU_TUTTO.md
    CHATGPT/README.md
