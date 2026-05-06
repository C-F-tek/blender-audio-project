# Workflow Tools

`Tools/workflow/` contains launcher and workflow helper scripts for IA-Carmine.

This directory has one canonical local-AI operator entrypoint:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Current command ownership lives in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

## Current doctrine

```text
Full0To10 = TUTTO SU TUTTO
LightFull0To10 = evidence-only profile, not provider/runtime proof
quick/balanced/deep/custom = intensity, not scope
supporting wrappers are implementation lanes, not first entrypoints
provider/probe/workload-quality lanes are opt-out in Full0To10
CSV/index/discovery/file-line-limit surfaces are evidence lanes when relevant
400-line policy applies to maintained docs and source files
limitations are backlog to overcome, not reasons to skip available tools
```

## Tool classification

| Script | Classification | Notes |
|---|---|---|
| `run_unified_local_ai_refactor.ps1` | canonical-entrypoint | Primary run-unica launcher. Dispatches `-LightFull0To10` profile when selected. |
| `run_unified_light_full0to10_profile.ps1` | evidence-only profile | Dispatches light evidence run and promotion JSON builder. |
| `run_full0to10_light_evidence_only.ps1` | evidence-only supporting lane | Produces light evidence report; no provider execution, patch apply, Blender runtime or FFmpeg runtime. |
| `run_local_validation_after_refactor.ps1` | supporting-tool | Local validation wrapper; not first entrypoint. |
| `run_local_ai_task_via_pipeline.ps1` | launcher-internal/supporting-tool | Official adapter lane. |
| `run_post_validation_ai_packet.ps1` | launcher-internal/supporting-tool | Advisory packet lane. |
| `run_parallel_ai_provider_multistep.ps1` | launcher-internal/supporting-tool | Provider/probe lane. |
| `run_agent_review_full_toolbox_decision_loop_integrated.ps1` | supporting selected phase | Not primary operator path. |
| `run_local_ai_markdown_task.ps1` | supporting-tool | Markdown helper; prefer unified launcher. |
| `run_docs_md_refactor_10min.ps1` | legacy-superseded/supporting-tool | Prefer unified launcher `md`/validation phases. |
| `startup_preflight.ps1` | diagnostic-only | Startup/preflight helper. |
| `startup_check.py` | diagnostic-only | Startup check helper. |
| `workflow_shell.py` | gui-or-shell-helper | Interactive helper; not canonical headless flow. |
| `workflow_shell_with_push.py` | unsafe-or-write-capable | Push-capable; explicit user intent required. |
| `workflow_debug.py` | diagnostic-only | Debug helper. |
| `git_auto_push.py` | unsafe-or-write-capable | Push behavior requires explicit user intent. |
| `asset_inventory.py` | supporting-tool | Asset inventory helper. |
| `scene_brief.py` | supporting-tool/application-domain | Scene brief helper. |
| `artifact_consult.py` | supporting-tool | Artifact consultation helper. |
| `project_awareness.py` | supporting-tool | Project-awareness context helper. |
| `smart_ai_context.py` | supporting-tool | Smart context helper. |
| `ai_runtime_diagnostics.py` | diagnostic-only | Runtime diagnostics helper. |

## LightFull0To10 behavior

The light profile is a report/evidence profile for fast visibility and promotion planning.

Verified behavior from `run_full0to10_light_evidence_only.ps1`:

```text
kind=full0to10_light_evidence_only_run
provider_execution_performed=false
patch_application_performed=false
blender_runtime_execution_performed=false
ffmpeg_execution_performed=false
```

It may run optional evidence steps for startup, track input contract, repo quality, Markdown line limits, accelerator/provider governance, provider invocation/bridge planning, memory visibility, provider feedback loop and final product quality. Optional missing scripts are represented as step records and must not be interpreted as silent full-run success.

## Guardrails

Workflow helpers must not silently:

```text
merge to master
force-push or rewrite history
apply patch specs
commit output/**
commit SQLite DB files
run Blender or FFmpeg
produce audio/media output
change provider/model execution semantics
claim provider execution from light evidence-only profiles
```

Push-capable helpers are not default validation commands and require explicit user intent.

## Full-run handoff rule

When a workflow helper contributes to Full0To10 evidence, recommendations, patch plans or patch specs, its output must be visible through:

```text
launcher manifest
phase_status / phase_reports
runtime tool usage telemetry when tools execute
runtime/hardware capability manifest when capabilities matter
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
CSV/index/discovery/file-line evidence when relevant
```

## 400-line policy

Maintained workflow scripts and docs must stay under 400 lines.

```text
Code/script >400 lines -> compact entrypoint + responsibility-based module/package split.
Markdown >400 lines -> compact index + <file>.md/part-001.md layout.
Existing oversized files -> technical debt to refactor progressively, not blind split targets.
```

Validator:

```text
Tools/validation/check_file_line_limits.py
```

## Related docs

```text
WORKFLOW.md
docs/WORKFLOW_HELPER_SCRIPTS_POLICY.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
```
