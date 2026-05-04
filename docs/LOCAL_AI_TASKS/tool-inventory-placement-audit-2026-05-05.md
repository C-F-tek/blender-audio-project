# IA-Carmine tool inventory placement audit — 2026-05-05

Repository: `C-F-tek/blender-audio-project`

Branch: `codex/unified-local-ai-refactor-launcher`

Mode: GitHub-only audit.

## Scope

Tools and candidate tools are not limited to canonical `Tools/**` paths. Search and placement must include:

    Tools/**
    Tools/ai/**
    Tools/validation/**
    Tools/workflow/**
    Tools/npu/**
    Tools/git/**
    Scripting/**
    repository-root Python entrypoints
    GUI/wrapper scripts
    generated or candidate Blender scripts

Do not promote a file only because it is executable-looking. Do not exclude a file only because it is outside `Tools/**`.

## Placement classes

    PROJECT_TOOL
      Stable, documented, reusable tool with CLI contract, JSON/MD output, validation and guardrails.

    BROKER_TOOL
      Safe report-only tool allowed in `Tools/ai/agent_runtime_tool_broker.py`.

    FULL_RUN_EVIDENCE
      Tool should feed full-run evidence, production bundle or handoff artifacts.

    PROVIDER_DIAGNOSTIC
      GPU/NPU/Ollama/provider probe, smoke or quality-routing tool.

    PATCH_PLAN_SUPPORT
      Supports recommendations, decision loop, code-edit proposal or patch-plan creation.

    MEMORY_LANE
      Reads/writes memory under explicit policy and DB guardrails.

    DOCS_MAINTENANCE
      Markdown inventory, link validation, documentation pruning/refactor.

    BLENDER_AUDIO_PIPELINE
      Actual Blender/audio/render/encode code. Not safe for broker by default.

    LOCAL_UI_OR_MANUAL
      GUI, shell, or operator-only workflow.

    GIT_WRITE_TOOL
      Can commit, push, delete, merge or mutate Git state. Manual-only.

    SUPPORT_LIBRARY
      Imported internal code, not standalone project tool.

    GENERATED_OR_CANDIDATE
      Candidate/generated script requiring policy validation before promotion.

## Promotion levels

    Level 0 — discovered script
      Exists in repo, maybe executable, not yet documented as tool.

    Level 1 — documented candidate
      Has purpose, inputs, outputs, guardrails and placement class in MD.

    Level 2 — project tool
      Has stable CLI, JSON output, optional MD output, validation command, examples and docs entry.

    Level 3 — broker tool
      Meets project-tool requirements and is safe for `agent_runtime_tool_broker.py` allowlist.

    Level 4 — full-run lane
      Broker/project tool is invoked by the full-run workflow and appears in production evidence.

## Runtime broker allowlist — installed tools

Primary source: `Tools/ai/agent_runtime_tool_broker.py`.

| Tool | Current level | Placement | Notes |
|---|---:|---|---|
| `check_python_syntax` | 4 | BROKER_TOOL / FULL_RUN_EVIDENCE | Must remain part of minimal broker bootstrap. |
| `build_python_line_count_csv` | 4 | BROKER_TOOL / FULL_RUN_EVIDENCE | Inventory evidence; excludes virtualenv/cache dirs. |
| `check_validation_report_contract` | 4 | BROKER_TOOL / FULL_RUN_EVIDENCE | Contract validation for reports. |
| `build_agent_memory_inventory` | 3 | BROKER_TOOL / MEMORY_LANE | Read-only inventory unless explicit write policy changes. |
| `build_agent_agnostic_tool_inventory` | 3 | BROKER_TOOL / FULL_RUN_EVIDENCE | Should become standard input for this audit. |
| `build_agent_transient_request_context` | 3 | BROKER_TOOL / PATCH_PLAN_SUPPORT | Request/context lane. |
| `run_gpu_planner_json_contract_smoke` | 3 | BROKER_TOOL / PROVIDER_DIAGNOSTIC | Safe smoke, no provider execution. |
| `build_code_interpreter_report` | 3 | BROKER_TOOL / FULL_RUN_EVIDENCE | Static code interpreter inventory/report. |
| `build_refactor_duplication_audit` | 3 | BROKER_TOOL / PATCH_PLAN_SUPPORT | Refactor planning evidence. |
| `runtime_sqlite_memory` | 3 | BROKER_TOOL / MEMORY_LANE | Persistent writes require explicit policy. |

## Strong project-tool candidates outside the current broker focus

These are good candidates for documented project-tool status, but not necessarily broker status.

| Path | Proposed level | Placement | Action |
|---|---:|---|---|
| `analyze_wav.py` | 2 | BLENDER_AUDIO_PIPELINE | Root audio analyzer; document as canonical audio analysis entrypoint, not broker. |
| `build_track_summary.py` | 2 | BLENDER_AUDIO_PIPELINE / FULL_RUN_EVIDENCE | Root track-summary builder; document near audio workflow. |
| `Scripting/v61b/main_v61b.py` | 2 | BLENDER_AUDIO_PIPELINE | Main Blender scene runner; manual/runtime only. |
| `Scripting/v61b/encode_image_sequence_v61b.py` | 2 | BLENDER_AUDIO_PIPELINE | Encoding helper; never brokered because FFmpeg/runtime side effects. |
| `Scripting/v61b/encode_ffmpeg_v61b.py` | 2 | BLENDER_AUDIO_PIPELINE | FFmpeg encode lane; manual/runtime only. |
| `Scripting/v61b/hot_update_scene_v61b.py` | 1 | BLENDER_AUDIO_PIPELINE | Candidate hot-update script; document as manual Blender-side utility. |
| `Scripting/v61b/scene_tuning_panel.py` | 1 | LOCAL_UI_OR_MANUAL | UI/tuning panel; manual only. |
| `Scripting/_template_audio_reactive_package/main.py` | 1 | GENERATED_OR_CANDIDATE / TEMPLATE | Template package entrypoint; document as scaffold. |
| `Tools/npu/generated_blender_script_candidate.py` | 0 | GENERATED_OR_CANDIDATE | Must pass generated script policy before promotion. |
| `Tools/npu/generated_blender_script_candidate_FristNear.py` | 0 | GENERATED_OR_CANDIDATE | Same; likely typo/name cleanup candidate. |

## High-value validation/provider tools to document as project tools

| Path | Proposed level | Placement | Action |
|---|---:|---|---|
| `Tools/workflow/startup_check.py` | 2 | CORE_BOOTSTRAP | Promote as project startup diagnostic tool. |
| `Tools/workflow/startup_preflight.ps1` | 2 | CORE_BOOTSTRAP | Wrapper; document after `startup_check.py`. |
| `Tools/workflow/ai_runtime_diagnostics.py` | 2 | PROVIDER_DIAGNOSTIC | Good preflight diagnostics candidate. |
| `Tools/ai/run_local_provider_probe.py` | 2 | PROVIDER_DIAGNOSTIC | Canonical provider probe. |
| `Tools/ai/check_local_resource_lanes.py` | 2 | PROVIDER_DIAGNOSTIC | Local resource-lane checker. |
| `Tools/ai/build_workload_quality_lane_routing.py` | 2 | PROVIDER_DIAGNOSTIC | Workload quality routing report. |
| `Tools/validation/check_ai_workload_report_quality.py` | 2 | PROVIDER_DIAGNOSTIC / VALIDATION | Already important; document as quality gate. |
| `Tools/validation/run_orchestrator_gpu_runtime_tool_routing_smoke.py` | 2 | PROVIDER_DIAGNOSTIC / RUNTIME_BROKER | Important for broker telemetry follow-up. |
| `Tools/validation/run_npu_runtime_tool_execution_smoke.py` | 2 | PROVIDER_DIAGNOSTIC / RUNTIME_BROKER | Runtime execution smoke. |
| `Tools/validation/run_npu_runtime_tool_context_smoke.py` | 2 | PROVIDER_DIAGNOSTIC / RUNTIME_BROKER | Runtime context smoke. |
| `Tools/validation/run_npu_runtime_tool_fallback_smoke.py` | 2 | PROVIDER_DIAGNOSTIC / RUNTIME_BROKER | Runtime fallback smoke. |
| `Tools/validation/run_npu_tool_request_contract_smoke.py` | 2 | PROVIDER_DIAGNOSTIC / RUNTIME_BROKER | Tool-request contract smoke. |

## Patch-plan/code-edit project-tool candidates

| Path | Proposed level | Placement | Action |
|---|---:|---|---|
| `Tools/ai/build_agent_review_patch_plan.py` | 2 | PATCH_PLAN_SUPPORT | Canonical patch-plan builder. |
| `Tools/ai/build_agent_review_code_patch_plan.py` | 2 | PATCH_PLAN_SUPPORT | Code patch-plan lane. |
| `Tools/ai/build_code_edit_proposal_from_plan.py` | 2 | PATCH_PLAN_SUPPORT | Converts plan to code edit proposal. |
| `Tools/ai/build_code_patch_artifact_pack.py` | 2 | PATCH_PLAN_SUPPORT / FULL_RUN_EVIDENCE | Artifact pack builder. |
| `Tools/ai/build_code_patch_docs_followup.py` | 2 | PATCH_PLAN_SUPPORT / DOCS_MAINTENANCE | Docs follow-up builder. |
| `Tools/ai/merge_ai_candidates.py` | 2 | PATCH_PLAN_SUPPORT | Candidate merge helper; review safety before broker. |
| `Tools/validation/run_code_edit_proposal_smoke.py` | 2 | VALIDATION | Smoke for code-edit proposal. |
| `Tools/validation/run_agent_review_code_patch_plan_smoke.py` | 2 | VALIDATION | Smoke for code patch plan. |
| `Tools/validation/run_agent_review_patch_plan_smoke.py` | 2 | VALIDATION | Smoke for patch-plan builder. |
| `Tools/validation/run_agent_review_patch_plan_full_validation.py` | 2 | VALIDATION | Full patch-plan validation. |

## Docs/project awareness tools

| Path | Proposed level | Placement | Action |
|---|---:|---|---|
| `Tools/validation/build_markdown_inventory.py` | 2 | DOCS_MAINTENANCE / FULL_RUN_EVIDENCE | Canonical markdown inventory. |
| `Tools/validation/check_docs_links.py` | 2 | DOCS_MAINTENANCE / VALIDATION | Canonical docs link checker. |
| `Tools/validation/build_script_inventory.py` | 2 | FULL_RUN_EVIDENCE | Script/tool inventory. |
| `Tools/workflow/project_awareness.py` | 1 | FULL_RUN_EVIDENCE / CONTEXT | Project-awareness helper. |
| `Tools/workflow/smart_ai_context.py` | 1 | FULL_RUN_EVIDENCE / CONTEXT | Context helper. |
| `Tools/workflow/artifact_consult.py` | 1 | FULL_RUN_EVIDENCE / CONTEXT | Artifact consult helper. |
| `Tools/workflow/asset_inventory.py` | 1 | FULL_RUN_EVIDENCE / BLENDER_AUDIO_PIPELINE | Asset inventory candidate. |
| `Tools/workflow/scene_brief.py` | 1 | BLENDER_AUDIO_PIPELINE / PATCH_PLAN_SUPPORT | Scene-brief candidate. |

## Manual-only or unsafe-to-broker tools

These may be useful, but must not be auto-brokered or included in unattended full-run execution.

| Path | Placement | Reason |
|---|---|---|
| `Tools/workflow/workflow_shell.py` | LOCAL_UI_OR_MANUAL | Interactive shell/wrapper. |
| `Tools/workflow/workflow_shell_with_push.py` | GIT_WRITE_TOOL | Push-capable; manual only. |
| `Tools/workflow/git_auto_push.py` | GIT_WRITE_TOOL | Git mutation. |
| `Tools/git/auto_push_generated_data.ps1` | GIT_WRITE_TOOL | Git mutation. |
| `Tools/git/auto_push_generated_artifacts.ps1` | GIT_WRITE_TOOL | Git mutation. |
| `Tools/workflow/gui/workflow_gui_modern.py` | LOCAL_UI_OR_MANUAL | GUI. |
| `Tools/workflow/gui/workflow_gui_with_push.py` | GIT_WRITE_TOOL / LOCAL_UI_OR_MANUAL | GUI with push behavior. |

## Support-library examples

These should be documented as internal components, not promoted directly unless they receive a stable CLI contract.

    Tools/ai/pipeline/*.py
    Tools/npu/pipeline/*.py
    Tools/ai/workload_quality.py
    Tools/ai/schema_repair_context.py
    Tools/ai/agent_memory_policy.py
    Tools/ai/agent_memory_routing_policy.py
    Tools/validation/report_utils.py

## Immediate recommendations

### P0 — fix final runtime broker telemetry absorption

The next code patch remains:

    fix(ai): preserve broker report in final runtime telemetry

Reason:

    Broker tools exist, but the final Git-trackable telemetry did not absorb broker execution evidence in run `20260505-002508`.

### P1 — create a canonical project-tool registry document

Create and maintain:

    docs/LOCAL_AI_TASKS/project-tool-registry.md

or keep this audit as the registry seed.

The registry should include:

    path
    tool id
    placement class
    promotion level
    broker eligibility
    CLI contract
    JSON/MD outputs
    validation command
    guardrails

### P1 — promote startup/provider/smoke validators to documented project tools

Prioritize:

    Tools/workflow/startup_check.py
    Tools/ai/run_local_provider_probe.py
    Tools/validation/check_ai_workload_report_quality.py
    Tools/validation/run_orchestrator_gpu_runtime_tool_routing_smoke.py

### P2 — document audio/Blender root entrypoints as project tools, not broker tools

Prioritize:

    analyze_wav.py
    build_track_summary.py
    Scripting/v61b/main_v61b.py
    Scripting/v61b/encode_image_sequence_v61b.py
    Scripting/v61b/encode_ffmpeg_v61b.py

## Rule for future audits

Always scan the whole repository for potential tools using at least these signals:

    argparse.ArgumentParser
    if __name__ == "__main__"
    PowerShell param(...)
    shebang lines
    filenames matching run_*, check_*, build_*, validate_*, encode_*, analyze_*, *_smoke.py
    GUI/wrapper filenames
    root-level Python entrypoints
    Scripting/** entrypoints

Then classify each candidate by safety and placement before adding it to any broker or full-run lane.
