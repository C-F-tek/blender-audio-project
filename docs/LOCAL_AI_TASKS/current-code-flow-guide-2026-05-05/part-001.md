<!-- IA-CARMINE-MD-SPLIT: part -->
# current-code-flow-guide-2026-05-05 — parte 001 di 002

Sorgente indice: [`../current-code-flow-guide-2026-05-05.md`](../current-code-flow-guide-2026-05-05.md)

## Navigazione

- [Indice](README.md)
- [Parte successiva](part-002.md)

# IA-Carmine current code flow guide — 2026-05-05

Repository: `C-F-tek/blender-audio-project`

Baseline: `master` after PR #187 merge

Purpose: describe the current code/tool flow after the unified launcher, provider bundle, broker telemetry and refactor/reuse full-run work.

## Operating doctrine

The current IA-Carmine flow is a single full-run system: **TUTTO SU TUTTO**.

There is one active operator flow:

    Tools/workflow/run_unified_local_ai_refactor.ps1
    docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md

All quick, balanced, deep and custom full runs must traverse the same semantic lane set. Intensity changes budget and depth, not scope. A quick full run is still a whole-repository run with reduced capacity; smoke remains a separate mode.

The perimeter of `tutto` may expand. When a new production-ready broker tool, provider diagnostic, validation lane, memory/context surface, repository-consistency check, registry, evidence builder, auto-discovery repair, index repair, file-line-limit surface or CSV/count surface is promoted, it must be wired into this flow or explicitly documented as excluded.

Telemetry is part of the run payload, not a side note. AI agents must be able to reason from telemetry about what actually executed, what failed, what was blocked, what was degraded, what was skipped intentionally and which tools/capabilities were available.

Limitations are backlog to overcome, not reasons to skip available tools. A lane/tool is unavailable only when current code, telemetry, capability manifest, provider diagnostic or validator evidence says so.

## Current active phase

Current active work:

    Current documentation PR: #193 docs(ai): align operational docs with post-PR187 code state
    Next clean report-only foundation candidate: PR #192
    Useful but diverged evidence branch: PR #191
    Mode: GitHub-only/API when maintainer is away

Compact bridge docs:

    docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
    docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
    docs/LOCAL_AI_TASKS/refactor-reuse-full-run-documentation-coherence-2026-05-05.md
    docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
    docs/KNOWN_LIMITATIONS.md

PR #187 is no longer the active branch. It is the merged baseline on `master`.

## High-level flow

The current IA-Carmine full-run flow is:

    user task markdown
      -> unified launcher
      -> static inventories, discovery and validation
      -> CSV/count surfaces and index/discovery drift evidence
      -> file-line-limit maintainability evidence
      -> context pack and agent state
      -> provider/probe/workload quality lanes
      -> repository consistency evidence
      -> full-toolbox decision loop
      -> patch plan proposal lane
      -> runtime broker telemetry lane
      -> runtime capability manifest
      -> shared production AI-to-AI bundle
      -> production evidence under docs/LOCAL_VALIDATION_EVIDENCE

Primary launcher:

    Tools/workflow/run_unified_local_ai_refactor.ps1

Full-toolbox decision workflow:

    Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1

Integrated warning policy wrapper:

    Tools/workflow/run_agent_review_full_toolbox_decision_loop_integrated.ps1

## Operator entrypoint

Canonical command family is owned by:

    docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md

The root/flow docs should not duplicate executable command blocks that can drift from launcher implementation.

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

Discovery/index/CSV/file-line-limit surfaces are produced through the inventory, validation, chunks, context, repository-consistency and evidence lanes. If a future dedicated index-repair lane is added, it must remain report/plan-first and must be visible in the manifest.

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

Generated index/code-chunk artifacts are not source authority and must not be hand-edited as source.

## Static inventory, discovery and validation flow

Typical early phases:

    Baseline compile validation/inventory tools
    Build Markdown inventory
    Check docs links
    Validate current JSON/report contracts
    Build script/tool inventory
    Build Python line-count CSV/Markdown surfaces
    Build function/class/method inventory CSV surfaces
    Build file-line-limit report when maintainability is in scope
    Build semantic code chunks and deterministic manifests
    Build selected-chunk evidence when available
    Build AI context pack
    Build agent state packet
    Build repository consistency map/smoke
    Validate task-scoped reports
    Surface auto-discovery/index drift when suspected

Typical tools:

    Tools/validation/check_python_syntax.py
    Tools/validation/build_markdown_inventory.py
    Tools/validation/check_docs_links.py
    Tools/validation/check_json_artifacts.py
    Tools/validation/build_script_inventory.py
    Tools/validation/check_file_line_limits.py
    Tools/validation/check_validation_report_contract.py
    Tools/npu/build_semantic_code_chunks.py
    Tools/ai/build_ai_context_pack.py
    Tools/ai/build_agent_state_packet.py

Expected evidence surfaces:

    Markdown inventory JSON/MD
    docs link report JSON
    script inventory JSON/CSV/MD
    function/class/method inventory CSV
    Python line-count CSV/MD
    file-line-limit JSON/MD
    semantic chunk manifest JSON/MD
    selected chunk evidence JSON when available
    repository consistency map JSON/MD
    repository consistency smoke JSON/MD
    validation report contract JSON
    index/discovery drift report or plan when relevant

Policy:

    CSV/count and file-line-limit surfaces are evidence surfaces, not source authority.
    Auto-discovery and index repair must be report/plan-first unless explicitly requested.
    Do not commit output/** or indexAI/code_chunks/**.
    Commit only compact evidence under docs/LOCAL_VALIDATION_EVIDENCE when needed.

## 400-line maintainability flow

Current policy:

    Maintained Markdown <= 400 lines.
    Maintained Python/PowerShell/scripts/source files <= 400 lines.

Validator:

    Tools/validation/check_file_line_limits.py
    docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md

Remediation:

    Markdown over 400 lines -> compact index plus <file>.md/part-001.md layout.
    Code over 400 lines -> compact entrypoint plus responsibility-based modules/package.
    Existing oversized files -> technical debt, not blind split targets.

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

Known production evidence from `20260505-081141`:

    local_provider_probe reported "ollama: probe failed"
    provider_advisory_state=recovered_degraded_provider
    provider_failure_reasons and degraded_provider_components were exposed in the shared final summary
    deterministic recovery remained valid
    patch_application_performed=false
    source_writes_performed=false

For newer reports, inspect telemetry fields such as `round_duration_source`, `round_duration_sample_count`, `provider_advisory_state`, `provider_failure_reasons` and workload quality status before making timing/provider claims.

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
    manual_review_required=True
    patch_application_performed=false
    source_writes_performed=false

Current classification set:

    SAFE_MECHANICAL
    MANUAL_REVIEW
    LOCAL_VALIDATION_REQUIRED
    BLENDER_RUNTIME_REQUIRED
    PROVIDER_VALIDATION_REQUIRED
    DEFER
    DO_NOT_PROMOTE

## Telemetry and AI reasoning contract

Telemetry is evidence for AI agents. It must travel with the bundle so the next local/cloud AI can distinguish real execution from missing output, intentional skip, degraded provider and failed tool execution.

Required telemetry/capability surfaces:

    runtime_tool_usage_telemetry_<STAMP>.json/md
    runtime_tool_capability_manifest_<STAMP>.json/md
    full_toolbox_run_telemetry_summary_<STAMP>.json/md
    shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
    shared_toolbox_ai_to_ai_final_summary_<STAMP>.json

These surfaces answer different AI-critical questions:

    usage telemetry: which broker/tool calls executed, failed or were blocked
    capability manifest: which tools were available and under which guardrails
    run telemetry summary: cross-run performance, provider, GPU/NPU and bundle state
    shared bundle: what evidence and recommendations should be handed to the next AI
    final summary: compact pass/fail, provider degradation and patch-plan status

Telemetry must expose:

    tool_call_entry_count
    executed_count
    failed_count
    blocked_count
    broker_reports
    provider_advisory_state
    provider_failure_reasons
    degraded_provider_components
    gpu_metrics_source
    round_duration_source
    patch_application_performed
    source_writes_performed

AI agents must not infer success from file existence alone. They must use telemetry fields to decide whether a lane was executed, degraded, blocked, intentionally disabled or unavailable.

## Runtime broker flow

Broker:

    Tools/ai/agent_runtime_tool_broker.py

Runtime telemetry:

    Tools/ai/build_runtime_tool_usage_telemetry.py

Capability manifest:

    runtime capability manifest builder for the active run/toolbox lane

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

Closed production fix:

    Commit a85bbf4 preserved broker report inputs in final runtime telemetry.
    Run 20260505-073332 validated broker_reports propagation with executed_count=3, failed_count=0, blocked_count=0.

Current expected state:

    inputs.broker_reports has at least one broker report when the broker lane ran.
    summary.executed_count reflects broker executions.
    broker telemetry is absorbed into the AI-to-AI production bundle.
