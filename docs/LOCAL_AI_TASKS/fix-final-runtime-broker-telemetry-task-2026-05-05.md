# IA-Carmine task — fix final runtime broker telemetry

Repository: `C-F-tek/blender-audio-project`

Branch: `codex/unified-local-ai-refactor-launcher`

Evidence run: `20260505-002508`

Evidence commit: `469722a test(ai): add post-broker full-run production evidence`

Follow-up doc:

    docs/LOCAL_AI_TASKS/post-broker-runtime-telemetry-followup-2026-05-05.md

## Objective

Implement a focused code patch so the final Git-trackable runtime usage telemetry includes broker-executed report-only tool calls.

Current failed acceptance:

    docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260505-002508.json
      inputs.broker_reports = []
      summary.tool_call_entry_count = 1
      summary.executed_count = 0
      summary.runtime_tool_request_count = 44
      summary.runtime_tool_execution_count = 0
      summary.declared_not_executed_count = 44

But the same run produced a broker report:

    output/validation/runtime_tool_broker_full_toolbox_20260505-002508.json

and the shared bundle lists it as present and passed.

## Required patch

Commit message:

    fix(ai): preserve broker report in final runtime telemetry

Primary behavior:

    - When `$RuntimeToolBrokerJson` exists, every final generation of `runtime_tool_usage_telemetry_<STAMP>.json` must pass `--broker-report $RuntimeToolBrokerJson`.
    - No later phase may overwrite the Git-trackable runtime usage telemetry with a version that has `broker_reports=[]`.
    - If the parent unified launcher regenerates runtime telemetry, it must receive or discover the broker report path.

## Scope

Inspect and patch as needed:

    Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1
    Tools/workflow/run_unified_local_ai_refactor.ps1
    Tools/ai/build_runtime_tool_usage_telemetry.py

Do not change provider execution semantics in this patch unless the same code path is proven responsible.

Do not change patch-plan generation, deterministic recommendations, or repository consistency filtering in this patch.

## Investigation commands

    Select-String -Path .\Tools\workflow\run_agent_review_full_toolbox_decision_loop.ps1 `
      -Pattern "build_runtime_tool_usage_telemetry|RuntimeToolTelemetryJson|broker-report|RuntimeToolBrokerJson" `
      -Context 4,6

    Select-String -Path .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
      -Pattern "build_runtime_tool_usage_telemetry|runtime_tool_usage_telemetry|broker-report|RuntimeToolBroker" `
      -Context 4,6

    Select-String -Path .\Tools\ai\build_runtime_tool_usage_telemetry.py `
      -Pattern "broker-report|collect_explicit_broker_reports|broker_reports" `
      -Context 4,6

## Acceptance criteria

After a new full run or focused full-toolbox decision loop run:

    docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_<STAMP>.json

must show:

    inputs.broker_reports.Count >= 1
    summary.tool_call_entry_count >= 3
    summary.executed_count >= 3
    summary.failed_count = 0
    summary.blocked_count = 0

Expected broker-executed tools:

    check_python_syntax
    build_python_line_count_csv
    check_validation_report_contract

The final telemetry may still include declared GPU planner counters. That is acceptable only if broker-executed entries are also present.

## Validation commands

Python syntax:

    python -m py_compile `
      .\Tools\ai\build_runtime_tool_usage_telemetry.py `
      .\Tools\ai\agent_runtime_tool_broker.py

PowerShell parser:

    powershell -NoProfile -ExecutionPolicy Bypass -Command '$p=(Resolve-Path ".\Tools\workflow\run_agent_review_full_toolbox_decision_loop.ps1").Path; $t=$null; $e=$null; [System.Management.Automation.Language.Parser]::ParseFile($p,[ref]$t,[ref]$e)|Out-Null; $e'

    powershell -NoProfile -ExecutionPolicy Bypass -Command '$p=(Resolve-Path ".\Tools\workflow\run_unified_local_ai_refactor.ps1").Path; $t=$null; $e=$null; [System.Management.Automation.Language.Parser]::ParseFile($p,[ref]$t,[ref]$e)|Out-Null; $e'

Diff hygiene:

    git diff --check

## Guardrails

No automatic patch application.
No provider execution during patch application.
No Blender runtime.
No FFmpeg.
No `output/**` commit.
No SQLite/DB commit.
No merge to master.
No force push.
No destructive operation.

## Proposal classification from `20260505-002508`

P0 — fix broker telemetry absorption:

    ready for immediate code patch.

P1 — investigate Ollama probe failure:

    separate diagnostic follow-up. Do not mix with broker telemetry unless proven same root cause.

P2 — filter patch-plan noise from archived evidence docs:

    future patch-plan quality improvement.

P2 — hardware/memory tuning:

    local operational tuning. NPU/GPU activation was visible, but RAM pressure was high.
