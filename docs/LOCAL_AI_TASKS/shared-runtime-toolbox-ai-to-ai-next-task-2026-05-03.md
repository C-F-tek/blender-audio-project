# Shared Runtime Toolbox AI-to-AI Next Task — 2026-05-03

## Purpose

Use this Markdown as the next official task request for the local IA-Carmine pipeline.

This is not a generic procedure. It is a concrete AI-to-AI handoff request from ChatGPT to the local IA. The local IA should read this file as the task input, use the committed evidence bundle as context, run only safe/report-only tooling unless explicitly configured otherwise, and produce a compact evidence bundle for review.

## Repository baseline

```text
repository: C-F-tek/blender-audio-project
branch to sync: master
current reference commit: eb5ec1d test(ai): add shared runtime toolbox evidence bundle
project: IA-Carmine
workflow: ChatGPT -> MD task -> local IA -> reports/bundle -> GitHub evidence -> ChatGPT review
```

Required sync before running:

```powershell
cd C:\Users\carmi\blender\blender-audio-project

git fetch origin
git switch master
git pull --ff-only origin master
git status --short

$env:PYTHONPATH = (Get-Location).Path
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
"STAMP=$Stamp"
```

Expected:

```text
git status --short is empty
HEAD is master/origin/master
```

## Evidence to read first

Read these committed files before planning:

```text
docs/LOCAL_AI_TASKS/shared-runtime-toolbox-orchestration-architecture.md
docs/LOCAL_AI_TASKS/full-memory-tool-regeneration-procedure.md
docs/LOCAL_AI_TASKS/project-complete-ai-to-ai-procedure.md
docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_bundle_20260503-011858.json
docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_bundle_20260503-011858.md
docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_python_line_count_20260503-011858.csv
```

The evidence bundle indicates a successful full-refactor regeneration after the shared runtime toolbox work:

```text
passed=True
profile=full_refactor
provider_execution_performed=False
patch_application_performed=False
sqlite_write_performed=False
persistent_memory_write_performed=False
report_count=13
artifact_count=14
errors={}
```

## Architecture to validate

The target architecture is:

```text
GPU -> tool_requests -> orchestrator -> broker -> report
NPU -> tool_requests -> orchestrator -> broker -> report

provider -> never direct executor
orchestrator -> control-plane / routing / scheduling
broker -> only controlled executor
report -> reinjected read-only evidence
```

Design rule:

```text
Providers ask.
Orchestrator decides.
Broker executes.
Reports become evidence.
```

## Available runtime tools

The current runtime tool contract allowlist contains these tool names:

```text
build_python_line_count_csv
build_agent_memory_inventory
build_agent_agnostic_tool_inventory
build_agent_transient_request_context
check_python_syntax
check_validation_report_contract
run_gpu_planner_json_contract_smoke
build_code_interpreter_report
runtime_sqlite_memory
```

All requests for these tools must use structured `tool_requests` and must be executed only through the orchestrator/broker path in orchestrated runs.

### Tool capabilities in this context

#### `build_python_line_count_csv`

Use to build deterministic Python inventory.

Possible uses:

```text
- detect largest Python modules after recent orchestration refactors
- compare line-count drift across Tools/ai, Tools/validation, Tools/workflow, Tools/npu
- prepare compact CSV evidence for ChatGPT review
```

Example tool request:

```json
{
  "id": "request_python_line_count_shared_toolbox",
  "tool": "build_python_line_count_csv",
  "reason": "Build a fresh Python line-count inventory to identify large files after shared toolbox orchestration changes.",
  "args": {}
}
```

#### `build_agent_memory_inventory`

Use to summarize durable project memory state.

Possible uses:

```text
- verify persistent memory contains the new shared-toolbox architecture state
- detect stale memory assumptions about GPU direct broker execution
- prepare a memory state summary for handoff bundles
```

Example tool request:

```json
{
  "id": "request_memory_inventory_shared_toolbox",
  "tool": "build_agent_memory_inventory",
  "reason": "Check durable project memory for shared runtime toolbox architecture alignment.",
  "args": {}
}
```

#### `build_agent_agnostic_tool_inventory`

Use to inventory local IA tools without making provider-specific assumptions.

Possible uses:

```text
- list report-only tools available to the local IA
- confirm broker/orchestrator validation tools are discoverable
- detect missing or duplicated tool capabilities
```

Example tool request:

```json
{
  "id": "request_agnostic_tool_inventory_shared_toolbox",
  "tool": "build_agent_agnostic_tool_inventory",
  "reason": "Inventory available report-only tools for the shared toolbox control-plane.",
  "args": {}
}
```

#### `build_agent_transient_request_context`

Use to assemble a request-scoped context packet.

Possible uses:

```text
- combine this MD, architecture docs and compact evidence into a local IA context packet
- provide a smaller context surface for GPU/NPU runs
- preserve task intent without relying on chat history
```

Example tool request:

```json
{
  "id": "request_transient_context_shared_toolbox",
  "tool": "build_agent_transient_request_context",
  "reason": "Build a transient request context from the shared toolbox handoff and evidence bundle.",
  "args": {
    "objective": "Validate the shared runtime toolbox architecture and produce next-step evidence."
  }
}
```

#### `check_python_syntax`

Use as source safety gate.

Possible uses:

```text
- verify all Python files still compile after recent orchestrator/broker work
- gate any future patch plan before commit
- catch accidental syntax regressions in Tools/ai and Tools/validation
```

Example tool request:

```json
{
  "id": "request_python_syntax_shared_toolbox",
  "tool": "check_python_syntax",
  "reason": "Validate Python syntax before recommending any shared toolbox follow-up.",
  "args": {}
}
```

#### `check_validation_report_contract`

Use to validate generated JSON report contracts.

Possible uses:

```text
- check reports generated by GPU/NPU orchestration and broker smoke tools
- catch missing guardrail fields or malformed report metadata
- validate compact evidence inputs before bundling
```

Example tool request:

```json
{
  "id": "request_validation_contract_shared_toolbox",
  "tool": "check_validation_report_contract",
  "reason": "Validate generated report contracts for the shared toolbox AI-to-AI run.",
  "args": {}
}
```

#### `run_gpu_planner_json_contract_smoke`

Use to validate provider output contract handling without running a real provider.

Possible uses:

```text
- confirm GPU/NPU tool_requests schema remains valid
- verify empty/invalid model output classifications
- ensure tool request allowlist enforcement remains stable
```

Example tool request:

```json
{
  "id": "request_gpu_contract_smoke_shared_toolbox",
  "tool": "run_gpu_planner_json_contract_smoke",
  "reason": "Verify the GPU planner JSON/tool request contract before any provider run.",
  "args": {}
}
```

#### `build_code_interpreter_report`

Use for static/code-structure report generation.

Possible uses:

```text
- identify refactor opportunities in orchestration/broker code
- detect duplicated helpers between Tools/ai and Tools/validation
- produce recommendations without applying patches
```

Example tool request:

```json
{
  "id": "request_code_interpreter_shared_toolbox",
  "tool": "build_code_interpreter_report",
  "reason": "Analyze AI tooling code for next shared-toolbox refactor opportunities without applying patches.",
  "args": {
    "inputs": ["Tools/ai", "Tools/validation", "Tools/workflow", "Tools/npu"]
  }
}
```

#### `runtime_sqlite_memory`

Use only through controlled actions and scopes.

Possible uses:

```text
- read persistent memory status
- read/search operational scratch state
- confirm no unauthorized persistent writes occurred
- prepare memory-routing evidence
```

Allowed safe request patterns:

```json
{
  "id": "request_persistent_memory_status_shared_toolbox",
  "tool": "runtime_sqlite_memory",
  "reason": "Check persistent memory status in read-only mode.",
  "args": {
    "action": "status",
    "scope": "persistent"
  }
}
```

```json
{
  "id": "request_operational_memory_status_shared_toolbox",
  "tool": "runtime_sqlite_memory",
  "reason": "Check operational scratch memory status for current run context.",
  "args": {
    "action": "status",
    "scope": "operational"
  }
}
```

Do not write persistent memory unless the user explicitly authorizes a controlled persistent-memory write task.

## Requests to execute in this AI-to-AI cycle

The local IA should answer these requests using evidence, reports and brokered tool execution. It should not guess from model memory alone.

### Request 1 — Toolbox availability summary

Produce a technical summary of available runtime tools and explain what each tool can do in the shared toolbox architecture.

Required output fields:

```text
tool_name
category
safe_default_mode
what_it_can_do
what_it_must_not_do
recommended_next_use
```

### Request 2 — Architecture conformance audit

Audit whether the current repository matches the target model:

```text
GPU -> tool_requests -> orchestrator -> broker -> report
NPU -> tool_requests -> orchestrator -> broker -> report
```

Use current code and smoke reports. Identify any remaining asymmetry between GPU and NPU lanes.

### Request 3 — Tool request examples

Generate at least 10 valid tool request examples relevant to this project.

The examples must include:

```text
- 2 inventory requests
- 2 validation requests
- 2 memory/status requests
- 2 context/evidence requests
- 2 code/refactor analysis requests
```

Each example must include:

```text
id
tool
reason
args
expected_report
risk
stop_condition
```

### Request 4 — Next safe automation candidate

Recommend the next safe automation/refactor step after the shared toolbox architecture.

Allowed recommendation types:

```text
ready_for_patch_plan
needs_more_context
advisory_only
```

Do not recommend automatic patch application. If code changes are recommended, produce a manual-review patch-plan target only.

### Request 5 — Evidence bundle plan

Propose the exact compact evidence bundle to return to ChatGPT.

The plan must list:

```text
reports to include
artifacts to include
bundle basename
validation command
commit policy
```

## Recommended local commands

Start with no-provider/report-only validation:

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"

python .\Tools\validation\run_orchestrator_gpu_runtime_tool_routing_smoke.py `
  --repo-root . `
  --output ".\output\validation\shared_toolbox_ai_to_ai_gpu_routing_$Stamp.json" `
  --markdown-output ".\output\validation\shared_toolbox_ai_to_ai_gpu_routing_$Stamp.md"

python .\Tools\validation\run_npu_runtime_tool_execution_smoke.py `
  --repo-root . `
  --output ".\output\validation\shared_toolbox_ai_to_ai_npu_execution_$Stamp.json" `
  --markdown-output ".\output\validation\shared_toolbox_ai_to_ai_npu_execution_$Stamp.md"

python .\Tools\validation\run_npu_tool_request_contract_smoke.py `
  --repo-root . `
  --output ".\output\validation\shared_toolbox_ai_to_ai_npu_contract_$Stamp.json" `
  --markdown-output ".\output\validation\shared_toolbox_ai_to_ai_npu_contract_$Stamp.md"
```

Then run static evidence:

```powershell
python -m Tools.validation.check_python_syntax `
  --repo-root . `
  --output ".\output\validation\shared_toolbox_ai_to_ai_python_syntax_$Stamp.json"

python -m Tools.ai.build_code_interpreter_report `
  --repo-root . `
  --input Tools/ai `
  --input Tools/validation `
  --input Tools/workflow `
  --input Tools/npu `
  --output ".\output\analysis\shared_toolbox_ai_to_ai_code_interpreter_$Stamp.json" `
  --markdown-output ".\output\analysis\shared_toolbox_ai_to_ai_code_interpreter_$Stamp.md"
```

Optional provider run may be executed only if explicitly requested by the user.

## Expected final local outputs

The local IA should produce these runtime outputs:

```text
output/validation/shared_toolbox_ai_to_ai_gpu_routing_<STAMP>.json
output/validation/shared_toolbox_ai_to_ai_npu_execution_<STAMP>.json
output/validation/shared_toolbox_ai_to_ai_npu_contract_<STAMP>.json
output/validation/shared_toolbox_ai_to_ai_python_syntax_<STAMP>.json
output/analysis/shared_toolbox_ai_to_ai_code_interpreter_<STAMP>.json
output/analysis/shared_toolbox_ai_to_ai_code_interpreter_<STAMP>.md
```

Then it should build compact evidence:

```text
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.md
```

Do not commit raw `output/**` artifacts.

## Compact bundle command template

```powershell
$Reports = @(
  ".\output\validation\shared_toolbox_ai_to_ai_gpu_routing_$Stamp.json",
  ".\output\validation\shared_toolbox_ai_to_ai_npu_execution_$Stamp.json",
  ".\output\validation\shared_toolbox_ai_to_ai_npu_contract_$Stamp.json",
  ".\output\validation\shared_toolbox_ai_to_ai_python_syntax_$Stamp.json",
  ".\output\analysis\shared_toolbox_ai_to_ai_code_interpreter_$Stamp.json"
) | Where-Object { Test-Path $_ }

python -m Tools.ai.build_github_evidence_bundle `
  --repo-root . `
  --basename "shared_toolbox_ai_to_ai_bundle_$Stamp" `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report ($Reports -join ',') `
  --artifact ".\docs\LOCAL_AI_TASKS\shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md" `
  --artifact ".\docs\LOCAL_AI_TASKS\shared-runtime-toolbox-orchestration-architecture.md" `
  --artifact ".\output\analysis\shared_toolbox_ai_to_ai_code_interpreter_$Stamp.md" `
  --max-included-artifact-chars 14000 `
  --max-included-artifacts 40
```

## Bundle validation

If bundle validation tooling is available, validate the compact bundle before commit:

```powershell
python -m Tools.validation.check_github_evidence_bundle `
  --repo-root . `
  --bundle ".\docs\LOCAL_VALIDATION_EVIDENCE\shared_toolbox_ai_to_ai_bundle_$Stamp.json" `
  --output ".\output\validation\shared_toolbox_ai_to_ai_bundle_${Stamp}_validation.json"
```

If the validator is not available, record that as a warning in the final handoff summary.

## Commit policy

Commit only compact evidence under:

```text
docs/LOCAL_VALIDATION_EVIDENCE/
```

Allowed evidence commit candidates:

```text
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.md
```

Never commit:

```text
output/**
*.db
*.sqlite
renders/**
```

## Stop conditions

Stop and report if any of these occur:

```text
python syntax validation fails unexpectedly
GPU runtime tool routing smoke fails
NPU runtime tool execution smoke fails
NPU tool request contract smoke fails
provider execution occurs during no-provider smoke
patch_application_performed=True
sqlite_write_performed=True outside explicitly authorized operational scratch semantics
persistent_memory_write_performed=True without explicit user authorization
bundle cannot be built or parsed
```

## Final answer expected from local IA

The local IA should produce a final Markdown/JSON summary with:

```text
1. tools available and what they can do
2. requests executed
3. reports generated
4. whether architecture is still agnostic
5. any remaining gaps
6. recommended next MD handoff/task
7. compact bundle paths
```

The summary must be evidence-based and must not claim a real GPU/NPU provider run occurred unless it was actually executed.
