# IA-Carmine post-broker runtime telemetry follow-up — 2026-05-05

Repository: `C-F-tek/blender-audio-project`

Branch: `codex/unified-local-ai-refactor-launcher`

Evidence run stamp: `20260505-002508`

Evidence commit: `469722a test(ai): add post-broker full-run production evidence`

Implementation commit under test: `fa1b75f feat(ai): complete full-run provider bundle and broker telemetry`

## Executive verdict

The post-`fa1b75f` run completed and produced useful production evidence, but it did not fully satisfy the runtime broker activation acceptance criteria.

Classifications:

    production_bundle_completeness: PASS
    provider_diagnostics_visibility: PASS_WITH_OLLAMA_PROBE_DEGRADED
    runtime_broker_telemetry: FAIL_NOT_ABSORBED

The run is valid evidence, but not final proof that the runtime broker lane is fully wired into final telemetry.

## Evidence summary

Observed from the `20260505-002508` production evidence set:

    unified launcher completed: true
    provider execution requested: true
    patch specs requested: true
    patch application performed: false
    source writes performed: false
    shared bundle patch_plan_summary_seen: true
    shared bundle patch_plan_count: 20
    orchestrator passed: true
    GPU report passed: true
    local_provider_probe passed: false
    local_provider_probe error: ollama: probe failed
    workload quality passed: true
    workload usable lanes: npu
    runtime broker full-toolbox report exists: true
    runtime broker full-toolbox report passed: true
    runtime usage telemetry broker_reports: []
    runtime usage telemetry tool_call_entry_count: 1
    runtime usage telemetry executed_count: 0
    runtime usage telemetry runtime_tool_request_count: 44
    runtime usage telemetry runtime_tool_execution_count: 0
    runtime usage telemetry declared_not_executed_count: 44

Interpretation:

    - provider and production-bundle changes worked;
    - the shared bundle now sees the patch plan summary;
    - provider diagnostics expose the Ollama probe degradation instead of hiding it;
    - the runtime broker report is generated and visible in the shared bundle report list;
    - the final runtime usage telemetry does not absorb that broker report.

## Proposal analysis

### P0 — fix final runtime telemetry broker-report wiring

Status: ready for next code patch.

Problem:

    output/validation/runtime_tool_broker_full_toolbox_<STAMP>.json exists and passed,
    but docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_<STAMP>.json reports broker_reports=[] and executed_count=0.

Likely cause:

    A later/final call to build_runtime_tool_usage_telemetry.py overwrites the pre-bundle telemetry without passing --broker-report $RuntimeToolBrokerJson, or the launcher parent regenerates telemetry without broker-report after the integrated lane.

Primary targets:

    Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1
    Tools/workflow/run_unified_local_ai_refactor.ps1

Secondary target only if needed:

    Tools/ai/runtime_tool/usage_telemetry/cli.py

Required investigation commands:

    Select-String -Path .\Tools\workflow\run_agent_review_full_toolbox_decision_loop.ps1 `
      -Pattern "build_runtime_tool_usage_telemetry|RuntimeToolTelemetryJson|broker-report|RuntimeToolBrokerJson" `
      -Context 4,6

    Select-String -Path .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
      -Pattern "build_runtime_tool_usage_telemetry|runtime_tool_usage_telemetry|broker-report" `
      -Context 4,6

Acceptance after patch:

    runtime_tool_usage_telemetry_<STAMP>.json:
      inputs.broker_reports.Count >= 1
      summary.tool_call_entry_count >= 3
      summary.executed_count >= 3
      summary.failed_count = 0
      summary.blocked_count = 0

The expected tool entries are:

    check_python_syntax
    build_python_line_count_csv
    check_validation_report_contract

### P1 — keep provider diagnostics, investigate Ollama probe separately

Status: diagnostic follow-up, not blocker for deterministic recovery.

Observed:

    local_provider_probe passed=false
    errors=["ollama: probe failed"]
    ai_workload_report_quality passed=true
    usable_lanes=["npu"]
    orchestrator passed=true
    GPU report passed=true

Interpretation:

    The full run can proceed with recovered/degraded provider state when diagnostics are explicit and patch application remains false.

Next investigation should inspect:

    output/validation/local_provider_probe.json
    output/validation/ai_workload_report_quality.json
    output/ai_pipeline/full_toolbox_<STAMP>_orchestrator.json
    output/ai_pipeline/full_toolbox_<STAMP>_parallel_gpu.json

Do not mix this with the broker telemetry wiring patch unless the same code path is proven responsible.

### P2 — reduce patch-plan noise from archived evidence documents

Status: useful but lower priority.

Observed:

    Several consistency patch plans target historical files under docs/LOCAL_VALIDATION_EVIDENCE/.

Risk:

    Patching archived evidence can produce self-referential churn and distract from live docs/source repairs.

Future rule:

    docs/LOCAL_VALIDATION_EVIDENCE/*.md should not be normal patch targets unless:
      - the task explicitly asks to normalize evidence;
      - the file is a current production communication artifact;
      - the patch is evidence-policy/documentation maintenance.

Likely targets:

    Tools/ai/agent_review/patch_plan/cli.py
    Tools/ai/deterministic_recommendations/cli.py
    repository consistency mapper configuration if present

### P2 — hardware/resource note

Observed from local run screenshot:

    NPU near saturation
    NVIDIA GPU active
    RAM around 91 percent on 32 GB system

Operational note:

    If full runs become unstable or slow, reduce context first or upgrade RAM. GPU/NPU activation is visible; memory pressure is the likely bottleneck.

## Updated acceptance classes

### COMPLETE

A full run is production-complete only when all of these hold:

    shared_toolbox_ai_to_ai_bundle_<STAMP>.md has patch_plan_summary_seen=True
    shared_toolbox_ai_to_ai_final_summary_<STAMP>.json has provider_diagnostics
    runtime_tool_usage_telemetry_<STAMP>.json has inputs.broker_reports.Count >= 1
    runtime_tool_usage_telemetry_<STAMP>.json has summary.executed_count >= 3
    patch_application_performed=false
    source_writes_performed=false

### RECOVERED_DEGRADED

Acceptable for evidence, not full operational success:

    patch plan summary exists
    provider diagnostics expose failed lane(s)
    deterministic recovery produced valid recommendations/patch plans
    patch application remains false

### INCOMPLETE_BROKER_TELEMETRY

Current `20260505-002508` class:

    runtime broker report exists
    final runtime telemetry broker_reports is empty
    executed_count is zero
    only declared planner counters are recorded

## Required next patch

Commit message recommendation:

    fix(ai): preserve broker report in final runtime telemetry

Patch objective:

    Ensure the final Git-trackable runtime_tool_usage_telemetry_<STAMP>.json is generated with --broker-report $RuntimeToolBrokerJson and is not overwritten later without broker context.

Validation:

    python -m py_compile .\Tools\ai\runtime_tool\usage_telemetry\cli.py -m Tools.ai agent_runtime_tool_broker

    powershell -NoProfile -ExecutionPolicy Bypass -Command '$p=(Resolve-Path ".\Tools\workflow\run_agent_review_full_toolbox_decision_loop.ps1").Path; $t=$null; $e=$null; [System.Management.Automation.Language.Parser]::ParseFile($p,[ref]$t,[ref]$e)|Out-Null; $e'

    powershell -NoProfile -ExecutionPolicy Bypass -Command '$p=(Resolve-Path ".\Tools\workflow\run_unified_local_ai_refactor.ps1").Path; $t=$null; $e=$null; [System.Management.Automation.Language.Parser]::ParseFile($p,[ref]$t,[ref]$e)|Out-Null; $e'

    git diff --check

Post-run validation:

    $S = "<STAMP>"
    $rt = Get-Content ".\docs\LOCAL_VALIDATION_EVIDENCE\runtime_tool_usage_telemetry_${S}.json" -Raw | ConvertFrom-Json
    $rt.inputs.broker_reports
    $rt.summary

Expected:

    broker_reports.Count >= 1
    executed_count >= 3
    failed_count = 0
    blocked_count = 0
