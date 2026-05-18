# Full Memory / Tool Regeneration Procedure — IA-Carmine

## Purpose

Use this procedure when the runtime tool stack is ready and the project needs to rebuild all memory, tool, context, validation and evidence artifacts from the current repository state.

This procedure is the stable entry point after these merged layers:

```text
feat(ai): add report-only runtime tool broker
feat(ai): add operational SQLite runtime memory tool
feat(ai): add memory routing policy for runtime tools
```

Default mode is safe and report-only:

```text
no provider execution
no GPU/NPU execution by default
no patch application
no Blender runtime
no persistent memory write
no automatic persistent promotion
no raw output/** commit
```

## Memory model

Persistent / consistent memory:

```text
path: indexAI/agent_memory/agent_memory.sqlite
mode: read-only in this workflow
purpose: durable project facts, validated lessons, architecture state and guardrails
```

Operational / scratch memory:

```text
path: output/ai_runtime_memory/operational_context.sqlite
mode: runtime scratch
purpose: current run state, temporary planner notes, tool results and hypotheses
clearable: yes
committable: no
```

Transient context:

```text
purpose: request-scoped packet assembled from memory notes, report files and selected context
committable: no, except through compact evidence bundle previews
```

Promotion policy:

```text
operational -> persistent is never automatic
promotion requires evidence, manual review and explicit future command
```

## Required tools

```text
Tools/ai/runtime_tool/agent_broker.py
python -m Tools.ai agent_runtime_sqlite_memory
python -m Tools.ai agent_memory_routing_policy
Tools/ai/agent_context/memory_inventory/cli.py
Tools/ai/agent_context/agnostic_tool_inventory/cli.py
Tools/ai/agent_context/transient_request_context/cli.py
Tools/ai/code_product/interpreter_report/cli.py
Tools/ai/repository_product/github_evidence_bundle.py
Tools/validation/build_python_line_count_csv.py
Tools/validation/check_python_syntax.py
Tools/validation/check_validation_report_contract.py
Tools/validation/runtime_tool/agent_runtime_tool_broker_smoke/cli.py
Tools/validation/run_agent_memory_routing_policy_smoke.py
```

## One-command workflow

Safe smoke/basic mode:

```powershell
.\Tools\workflow\run_full_memory_tool_regeneration.ps1 `
  -RepoRoot . `
  -Profile basic `
  -Objective "Smoke full memory/tool regeneration workflow." `
  -SkipCodeInterpreter `
  -SkipBundle
```

Full report-only regeneration:

```powershell
.\Tools\workflow\run_full_memory_tool_regeneration.ps1 `
  -RepoRoot . `
  -Profile full_refactor `
  -Objective "Regenerate IA-Carmine memory, runtime tools and context from current repository state."
```

Fresh operational scratch tray:

```powershell
.\Tools\workflow\run_full_memory_tool_regeneration.ps1 `
  -RepoRoot . `
  -Profile full_refactor `
  -ClearOperational
```

## Regeneration sequence

The workflow runs these layers in order:

```text
1. persistent memory inventory, read-only
2. agnostic tool inventory
3. persistent SQLite memory status, read-only
4. operational SQLite memory status
5. memory routing policy
6. runtime broker execution against generated tool_requests
7. transient request context
8. full Python line-count CSV/JSON/MD
9. optional code interpreter/static report
10. Python syntax validation
11. validation report contract check
12. runtime broker smoke
13. memory routing policy smoke
14. workflow summary JSON/MD
15. optional compact evidence bundle
```

## Expected guardrails

The workflow summary must keep:

```text
provider_execution_performed=false
patch_application_performed=false
sqlite_write_performed=false
persistent_memory_write_performed=false
```

Operational scratch writes are allowed only under `output/**` and must not be interpreted as protected SQLite writes.

## Evidence policy

Allowed to commit only when intentionally creating an evidence PR:

```text
docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_bundle_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_bundle_<STAMP>.md
docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_python_line_count_<STAMP>.csv
```

Never commit:

```text
output/**
*.db
*.sqlite
renders/**
```

## External GitHub tool import note

External GitHub tools must not be downloaded and executed directly.

Future safe lane:

```text
external repo
  -> output/tool_quarantine/**
  -> static scan
  -> license/security/guardrail report
  -> adapter proposal
  -> manual review
  -> broker allowlist
```

Never do:

```text
download from GitHub -> execute immediately
```

## Follow-up integration

After this regeneration workflow is stable:

```text
1. wire planner outputs to tool_requests
2. run broker between GPU planner rounds
3. feed tool_results into GPU context
4. feed tool_results and memory context into NPU audit
5. add latest_due/milestone NPU scheduling
6. add external tool import quarantine scanner
```
