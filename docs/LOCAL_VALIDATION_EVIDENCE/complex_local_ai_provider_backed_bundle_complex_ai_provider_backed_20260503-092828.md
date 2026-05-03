# Local Validation Evidence Bundle

- Generated at: `2026-05-03T09:42:59`
- Kind: `github_validation_evidence_bundle`

## Decision summary
- `ollama_gpu_primary_advisory`: `False`
- `npu_excluded_when_unusable`: `False`
- `provider_execution_seen`: `True`
- `npu_decode_smoke_passed`: `True`
- `selected_chunks_evidence_seen`: `True`
- `selected_chunks_built`: `True`
- `budget_respected`: `True`
- `artifact_manifest_built`: `True`
- `included_artifacts_built`: `True`
- `included_artifact_count`: `11`
- `patch_plan_summary_seen`: `False`

## Reports

### `output/validation/complex_ai_provider_backed_20260503-092828_resource_lanes.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `local_ai_resource_lanes`
- Passed: `True`
- Provider execution performed: `True`

### `output/validation/complex_ai_provider_backed_20260503-092828_npu_provider_environment.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_provider_environment`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/complex_ai_provider_backed_20260503-092828_npu_decode_smoke.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_decode_smoke_diagnostic`
- Passed: `True`
- Provider execution performed: `True`
- Python executable: `C:\Users\carmi\blender\venvs\blender-npu-ai\Scripts\python.exe`

### `output/ai_pipeline/complex_ai_provider_backed_20260503-092828_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_npu_parallel_orchestrator`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_deep_planning_supervised`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `0`
- Recommended next layer: `build_agent_review_patch_plan.py`

### `output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_backed_20260503-092828.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `shared_toolbox_ai_to_ai_final_summary`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`

## Artifact manifest

- `output/validation/complex_ai_provider_backed_20260503-092828_resource_lanes.json` exists=`True` size=`2871` suffix=`.json` preview_chars=`1500`
- `output/validation/complex_ai_provider_backed_20260503-092828_npu_provider_environment.json` exists=`True` size=`1745` suffix=`.json` preview_chars=`1500`
- `output/validation/complex_ai_provider_backed_20260503-092828_npu_decode_smoke.json` exists=`True` size=`2193` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/complex_ai_provider_backed_20260503-092828_orchestrator.json` exists=`True` size=`22392` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json` exists=`True` size=`160313` suffix=`.json` preview_chars=`1500`
- `output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_backed_20260503-092828.json` exists=`True` size=`99199` suffix=`.json` preview_chars=`1500`

## Included artifact contents

### `docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `15584`
- SHA-256: `302c2f4ff41c5fc4b144ac175a9d40383b992aebad14c1cd722bd71c1a3a1fe3`
- Content included: `True`
- Content truncated: `True`

```text
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
  --bundle ".\docs\LOCAL
```

### `docs/LOCAL_AI_TASKS/shared-runtime-toolbox-orchestration-architecture.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `6484`
- SHA-256: `da90623dc168a694fe44d738a5cdf652d2cdd9e894663d475fe461e03af25f30`
- Content included: `True`
- Content truncated: `False`

```text
# Shared Runtime Toolbox Orchestration Architecture

## Scope

This document records the IA-Carmine runtime-tool architecture after the GPU/NPU orchestration refactor.

The goal is to keep the system provider-agnostic while allowing multiple reasoning lanes to request and consume tool evidence through a single controlled execution path.

## Current target topology

```text
GPU -> tool_requests -> orchestrator -> broker -> report
NPU -> tool_requests -> orchestrator -> broker -> report

provider -> never direct executor
orchestrator -> control-plane / routing / scheduling
broker -> only controlled executor
report -> reinjected read-only evidence
```

## Roles

### Provider lanes

GPU and NPU lanes are requesters and consumers.

They may:

- read repository evidence and generated reports;
- produce recommendations;
- produce structured `tool_requests`;
- consume broker reports as read-only context;
- classify missing evidence and runtime failures.

They must not:

- execute shell commands directly;
- apply patches directly;
- write persistent SQLite memory without explicit controlled authorization;
- create GitHub PRs directly;
- run Blender runtime;
- bypass broker allowlists.

### Orchestrator

The orchestrator is the control-plane.

It is responsible for:

- launching GPU planning;
- launching NPU audits;
- collecting checkpoint reports;
- collecting GPU and NPU `tool_requests`;
- scheduling report-only tool execution;
- passing requests to the broker;
- reinjecting broker reports into later context;
- preserving non-blocking behavior for NPU audits;
- surfacing guardrail counters in final reports.

The orchestrator decides when a request is executed, but it does not implement the tools themselves.

### Broker

The broker is the only executor.

It is responsible for:

- validating request packets;
- enforcing the allowlist;
- executing only known report-only tools;
- blocking or reporting disallowed requests;
- writing JSON and Markdown reports;
- exposing guardrail counters.

The broker should remain deterministic, narrow, and low-policy. High-level scheduling belongs to the orchestrator.

## Supported shared toolbox capabilities

The shared toolbox currently includes report-only capabilities such as:

- agent agnostic tool inventory;
- agent memory inventory;
- transient request context;
- runtime SQLite memory status/search under controlled modes;
- Python line-count inventory;
- Python syntax validation;
- validation report contract checks;
- GPU planner JSON contract smoke;
- code-interpreter report inventory.

Tool execution is always mediated by `Tools/ai/agent_runtime_tool_broker.py`.

## GPU path

### Standalone mode

The GPU supervised runner remains able to execute runtime tools directly through the broker for standalone workflows.

This compatibility mode is intentionally preserved because the supervised runner is still useful outside the full GPU/NPU orchestrator.

### Orchestrated mode

In orchestrated mode, the GPU runner should behave as a provider/requester:

1. The GPU planner receives evidence and toolbox context.
2. The GPU planner emits structured `tool_requests`.
3. The orchestrator collects the requests from GPU reports/checkpoints.
4. The orchestrator passes valid requests to the broker.
5. The broker executes allowlisted tools and writes reports.
6. The orchestrator reinjects the broker reports as read-only context.

The architectural preference is to keep this path symmetrical with the NPU path.

## NPU path

The NPU auditor is non-blocking and non-primary.

It may:

- read GPU checkpoints;
- read runtime toolbox context;
- classify provider states;
- produce audit reports;
- propose structured `tool_requests`.

The NPU must not execute tools directly. NPU tool requests are routed through the orchestrator and broker.

## Memory model

The memory model is split by scope:

- persistent memory: durable project rules, decisions and long-lived facts;
- operational memory: scratch/runtime context that can be regenerated or cleared;
- report artifacts: JSON/Markdown evidence under `output/**` or compact committed evidence under `docs/LOCAL_VALIDATION_EVIDENCE` when explicitly needed.

Persistent writes require explicit controlled authorization. Report-only reads/status checks are safe default operations.

## Guardrails

Permanent guardrails:

- no provider direct execution;
- no free shell from provider output;
- no patch application from provider output;
- no production deploy path;
- no Blender runtime in these validation lanes;
- no implicit persistent SQLite writes;
- no SQLite/database artifacts committed;
- no `output/**` artifacts committed except selected compact evidence when explicitly intended;
- NPU remains non-blocking and non-primary;
- broker remains the only executor.

## Smoke coverage

Key smoke coverage after the orchestration work:

```text
Tools/validation/run_orchestrator_gpu_runtime_tool_routing_smoke.py
Tools/validation/run_npu_runtime_tool_execution_smoke.py
Tools/validation/run_npu_tool_request_contract_smoke.py
Tools/validation/run_npu_runtime_tool_context_smoke.py
Tools/validation/run_provider_empty_response_diagnostics_smoke.py
Tools/validation/run_agent_runtime_tool_broker_smoke.py
```

Expected no-provider/report-only invariants:

```text
provider_execution_performed=False
patch_application_performed=False
sqlite_write_performed=False
persistent_memory_write_performed=False
*_runtime_tool_request_count >= 1 when testing request routing
*_runtime_tool_execution_count >= 1 when testing broker execution
*_runtime_tool_failed_count=0 for positive smoke cases
*_runtime_tool_blocked_count=0 for positive smoke cases
```

## Operational workflow

Recommended local sequence after major toolbox/orchestrator changes:

1. Run targeted smoke for the changed lane.
2. Run GPU runtime routing smoke.
3. Run NPU runtime execution smoke.
4. Run syntax validation.
5. Run full memory/tool regeneration workflow when the architecture changes materially.
6. Commit only code/docs and selected compact validation evidence when needed.
7. Do not commit `output/**`, SQLite files, or generated runtime databases.

## Design rule

The high-level design rule is:

```text
Providers ask.
Orchestrator decides.
Broker executes.
Reports become evidence.
```

This preserves agnosticism: new providers or future local AI workers can join the same loop by producing structured requests and consuming reports, without receiving direct execution authority.

```

### `output/validation/complex_ai_provider_backed_20260503-092828_resource_lanes.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `452`
- SHA-256: `52e0bff8d54cfc4a424f4b02518ccbd10f59a3dfdaa5397bd0c1755b96a4dada`
- Content included: `True`
- Content truncated: `False`

```text
# Local AI Resource Lanes

- Passed: `True`
- Parallel: `True`
- Provider execution performed: `True`
- Ready lanes: `gpu, npu, ollama`
- Available lanes: `gpu, npu, ollama`

| Lane | Ready | Available | Elapsed sec | Provider execution |
|---|---:|---:|---:|---:|
| gpu | True | True | 1.2377 | False |
| npu | True | True | 2.0582 | False |
| ollama | True | True | 5.1718 | True |

This report is observability-only and app-agnostic.

```

### `output/validation/complex_ai_provider_backed_20260503-092828_npu_provider_environment.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `304`
- SHA-256: `ebcef793de1795cfc3f55063d9a02cad3467d28b6cee31e068b8067e70e75ded`
- Content included: `True`
- Content truncated: `False`

```text
# NPU Provider Environment

- `passed`: `True`
- `npu_python`: `C:\Users\carmi\blender\venvs\blender-npu-ai\Scripts\python.exe`
- `npu_python_exists`: `True`
- `openvino_import`: `True`
- `openvino_genai_import`: `True`
- `openvino_genai_pip_package`: `openvino-genai`
- `npu_available`: `True`

```

### `output/ai_packets/complex_ai_provider_backed_20260503-092828_npu_decode_smoke_output.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `72`
- SHA-256: `f9a3dc96e3a9c0e13ff4ea24b11380c64b5b7df1ef1ab586aa579180119989fd`
- Content included: `True`
- Content truncated: `False`

```text
## NPU Decode Smoke
The NPU decode smoke test produced readable text.

```

### `output/ai_pipeline/complex_ai_provider_backed_20260503-092828_orchestrator.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1953`
- SHA-256: `01e5cc4ea9e4952701e71a7bffcf69cb2af046c5e2479ac1dc8eddcf63574fa5`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU/NPU Parallel Orchestrator

- `passed`: `True`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `gpu_returncode`: `0`
- `elapsed_seconds`: `518.146`
- `npu_audit_count`: `4`
- `npu_audit_success_count`: `4`
- `npu_tool_context_seen_count`: `0`
- `npu_tool_request_count`: `0`
- `npu_runtime_tool_request_count`: `0`
- `npu_runtime_tool_execution_count`: `0`
- `npu_runtime_tool_failed_count`: `0`
- `npu_runtime_tool_blocked_count`: `0`
- `npu_runtime_tool_result_count`: `0`
- `gpu_recommendation_count`: `0`
- `gpu_empty_recommendations_reason`: `context_echo_detected`
- `gpu_evidence_ready_for_manual_patch_count`: `12`
- `runtime_tool_broker_enabled`: `False`
- `runtime_tool_request_count`: `0`
- `runtime_tool_execution_count`: `0`
- `runtime_tool_failed_count`: `0`
- `runtime_tool_blocked_count`: `0`
- `runtime_tool_result_count`: `0`

## Decision
- `gpu_review_blocked_by_npu`: `False`
- `npu_auditor_mode`: `parallel_best_effort`
- `npu_audit_success_count`: `4`
- `npu_tool_context_seen_count`: `0`
- `npu_tool_request_count`: `0`
- `npu_runtime_tool_request_count`: `0`
- `npu_runtime_tool_execution_count`: `0`
- `npu_runtime_tool_failed_count`: `0`
- `npu_runtime_tool_blocked_count`: `0`
- `npu_runtime_tool_result_count`: `0`
- `ready_for_patch_plan`: `False`
- `fallback_patch_plan_recommended`: `True`
- `recommended_next_layer`: `build_agent_review_patch_plan.py`
- `gpu_empty_recommendations_reason`: `context_echo_detected`
- `runtime_tool_broker_enabled`: `False`
- `runtime_tool_result_count`: `0`
- `manual_review_required`: `True`

## NPU Audits
- round `1` status=`finished` class=`usable_audit_text` success=`True`
- round `3` status=`finished` class=`usable_audit_text` success=`True`
- round `6` status=`finished` class=`usable_audit_text` success=`True`
- round `9` status=`finished` class=`usable_audit_text` success=`True`

```

### `output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1056`
- SHA-256: `16fba849e7924f2455593100fd6e9863b1ac6d55aa6846659bb0e1e9f9d1c897`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU Deep Planning Review

- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Model: `qwen2.5-coder:14b`
- Elapsed seconds: `408.616`
- Round count: `23`
- Recommendation count: `0`
- Raw recommendation candidates: `0`
- Filtered recommendation count: `0`
- Tool request count: `0`
- Valid tool request count: `0`
- Invalid tool request count: `0`
- JSON parse error count: `19`
- Context echo detected count: `1`
- Model output schema mismatch count: `4`
- Empty recommendations reason: `context_echo_detected`
- Evidence ready for manual patch count: `12`

## Decision

- `ready_for_patch_plan`: `False`
- `ready_count`: `0`
- `needs_more_context_count`: `0`
- `fallback_patch_plan_recommended`: `True`
- `npu_auditor_non_blocking`: `True`
- `npu_unusable_or_failed_count`: `0`
- `npu_audit_success_count`: `0`
- `npu_auditor_disabled_reason`: ``
- `recommended_next_layer`: `build_agent_review_patch_plan.py`
- `manual_review_required`: `True`

## Recommendations


```

### `output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_backed_20260503-092828.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `13699`
- SHA-256: `a13ac1108a2a919ac72b9fd21184754dca6994f1ce9fad69f0e6fb9c92f165fc`
- Content included: `True`
- Content truncated: `False`

```text
# Shared Toolbox AI-to-AI Final Summary

- stamp: complex_ai_provider_backed_20260503-092828
- passed: True
- provider_execution_performed: True
- patch_application_performed: False
- source_writes_performed: False
- sqlite_write_performed: False
- persistent_memory_write_performed: False
- blender_runtime_execution_performed: False

## Tools available

### build_agent_agnostic_tool_inventory

- Category: inventory
- Safe default mode: report-only
- Recommended next use: Discover reusable tooling before adding new scripts.
- Allowed args: `['root']`
- Can do:
  - Inventory existing reusable IA-Carmine tools and guardrails.
- Must not do:
  - execute arbitrary shell commands
  - apply patches
  - run Blender runtime
  - commit output artifacts
  - write SQLite or persistent memory

### build_agent_memory_inventory

- Category: inventory
- Safe default mode: report-only
- Recommended next use: Summarize durable project memory as read-only context.
- Allowed args: `['objective', 'memory_db']`
- Can do:
  - Read-only SQLite/JSONL agent memory inventory.
- Must not do:
  - execute arbitrary shell commands
  - apply patches
  - run Blender runtime
  - commit output artifacts
  - write SQLite or persistent memory

### build_agent_transient_request_context

- Category: context
- Safe default mode: report-only
- Recommended next use: Assemble request-scoped context for local AI planning.
- Allowed args: `['objective', 'memory_note', 'raw_file', 'report_file']`
- Can do:
  - Build request-scoped context from memory notes, raw files and reports.
- Must not do:
  - execute arbitrary shell commands
  - apply patches
  - run Blender runtime
  - commit output artifacts
  - write SQLite or persistent memory

### build_code_interpreter_report

- Category: static_analysis
- Safe default mode: report-only
- Recommended next use: Build static analysis/refactor evidence.
- Allowed args: `['input']`
- Can do:
  - Build static code-interpreter style report over selected roots.
- Must not do:
  - execute arbitrary shell commands
  - apply patches
  - run Blender runtime
  - commit output artifacts
  - write SQLite or persistent memory

### build_python_line_count_csv

- Category: inventory
- Safe default mode: report-only
- Recommended next use: Refresh complete Python inventory before refactor planning.
- Allowed args: `['exclude_dir']`
- Can do:
  - Build full Python line-count CSV/JSON/MD evidence.
- Must not do:
  - execute arbitrary shell commands
  - apply patches
  - run Blender runtime
  - commit output artifacts
  - write SQLite or persistent memory

### build_refactor_duplication_audit

- Category: support_tool
- Safe default mode: report-only
- Recommended next use: Use through the runtime tool broker when a report-only request requires it.
- Allowed args: `['root', 'report', 'input_audit_report', 'line_count_report', 'code_interpreter_report', 'python_syntax_report', 'bundle_smoke_report', 'memory_routing_report']`
- Can do:
  - Build a report-only duplicated-helper/refactor audit over selected code roots and existing evidence reports.
- Must not do:
  - execute arbitrary shell commands
  - apply patches
  - run Blender runtime
  - commit output artifacts
  - write SQLite or persistent memory

### check_python_syntax

- Category: validation
- Safe default mode: report-only
- Recommended next use: Gate Python source changes.
- Allowed args: `[]`
- Can do:
  - Validate Python syntax across repository.
- Must not do:
  - execute arbitrary shell commands
  - apply patches
  - run Blender runtime
  - commit output artifacts
  - write SQLite or persistent memory

### check_validation_report_contract

- Category: validation
- Safe default mode: report-only
- Recommended next use: Gate report quality before evidence bundling.
- Allowed args: `['report_file']`
- Can do:
  - Validate validation report contract for a scoped report-dir or explicit report files.
- Must not do:
  - execute arbitrary shell commands
  - apply patches
  - run Blender runtime
  - commit output artifacts
  - write SQLite or persistent memory

### run_gpu_planner_json_contract_smoke

- Category: validation
- Safe default mode: report-only
- Recommended next use: Validate planner JSON contract without providers.
- Allowed args: `[]`
- Can do:
  - Run GPU planner JSON contract smoke tests without provider.
- Must not do:
  - execute arbitrary shell commands
  - apply patches
  - run Blender runtime
  - commit output artifacts
  - write SQLite or persistent memory

### runtime_sqlite_memory

- Category: memory_status
- Safe default mode: controlled read-only/status by default
- Recommended next use: Read memory status/search through broker-controlled actions.
- Allowed args: `['action', 'scope', 'database', 'persistent_database', 'summary', 'content', 'role', 'tag', 'query', 'limit', 'confirm', 'allow_persistent_write']`
- Can do:
  - Use protected persistent SQLite read-only or operational scratch SQLite memory under output/**.
- Must not do:
  - execute arbitrary shell commands
  - apply patches
  - run Blender runtime
  - commit output artifacts
  - write persistent memory without explicit confirmation and authorization

## Tool requests executed or proposed

- request_build_code_interpreter_report: build_code_interpreter_report - Build static analysis/refactor evidence.
- request_check_python_syntax: check_python_syntax - Gate Python source changes.
- request_check_validation_report_contract: check_validation_report_contract - Gate report quality before evidence bundling.

## Reports generated

- output/validation/complex_ai_provider_backed_20260503-092828_resource_lanes.json exists=True json_ok=True kind=local_ai_resource_lanes passed=True
- output/validation/complex_ai_provider_backed_20260503-092828_npu_provider_environment.json exists=True json_ok=True kind=npu_provider_environment passed=True
- output/validation/complex_ai_provider_backed_20260503-092828_npu_decode_smoke.json exists=True json_ok=True kind=npu_decode_smoke_diagnostic passed=True
- output/ai_pipeline/complex_ai_provider_backed_20260503-092828_orchestrator.json exists=True json_ok=True kind=agent_gpu_npu_parallel_orchestrator passed=True
- output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json exists=True json_ok=True kind=agent_gpu_deep_planning_supervised passed=True

## Remaining gaps

- output/validation/shared_toolbox_python_syntax_complex_ai_provider_backed_20260503-092828.json: optional report missing
- output/analysis/shared_toolbox_code_interpreter_complex_ai_provider_backed_20260503-092828.json: optional report missing
- output/validation/shared_toolbox_gpu_contract_smoke_complex_ai_provider_backed_20260503-092828.json: optional report missing
- output/validation/shared_toolbox_gpu_routing_complex_ai_provider_backed_20260503-092828.json: optional report missing
- output/validation/shared_toolbox_npu_execution_complex_ai_provider_backed_20260503-092828.json: optional report missing
- output/validation/shared_toolbox_npu_contract_complex_ai_provider_backed_20260503-092828.json: optional report missing
- output/validation/npu_provider_environment_shared_toolbox_complex_ai_provider_backed_20260503-092828.json: optional report missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_complex_ai_provider_backed_20260503-092828_orchestrator.json: optional report missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_complex_ai_provider_backed_20260503-092828_gpu.json: optional report missing
- output/analysis/shared_toolbox_gpu_npu_sync_complex_ai_provider_backed_20260503-092828.json: optional report missing
- output/analysis/shared_toolbox_gpu_contract_replay_complex_ai_provider_backed_20260503-092828.json: optional report missing
- output/analysis/shared_toolbox_code_interpreter_complex_ai_provider_backed_20260503-092828.md: optional artifact missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_complex_ai_provider_backed_20260503-092828_orchestrator.md: optional artifact missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_complex_ai_provider_backed_20260503-092828_gpu.md: optional artifact missing
- output/analysis/shared_toolbox_gpu_npu_sync_complex_ai_provider_backed_20260503-092828.md: optional artifact missing
- output/analysis/shared_toolbox_gpu_contract_replay_complex_ai_provider_backed_20260503-092828.md: optional artifact missing
- output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_backed_20260503-092828.md: optional artifact missing
- runtime tool requests not proven in provider-backed run: No concrete tool_requests were found in the included reports.

## Recommended next task

docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md

## Recursive defaults

- Enabled: `True`
- Discovered reports: `6`
- Discovered artifacts: `6`

## Chunked large JSON/Markdown files

- output/ai_pipeline/complex_ai_provider_backed_20260503-092828_orchestrator.json lines=346 chunks=2 chunk_size=200
  - output/ai_pipeline/complex_ai_provider_backed_20260503-092828_orchestrator.json#L1-L200 -> next: output/ai_pipeline/complex_ai_provider_backed_20260503-092828_orchestrator.json#L201-L346
  - output/ai_pipeline/complex_ai_provider_backed_20260503-092828_orchestrator.json#L201-L346 -> next: END
- output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json lines=1872 chunks=10 chunk_size=200
  - output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json#L1-L200 -> next: output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json#L201-L400
  - output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json#L201-L400 -> next: output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json#L401-L600
  - output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json#L401-L600 -> next: output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json#L601-L800
  - output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json#L601-L800 -> next: output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json#L801-L1000
  - output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json#L801-L1000 -> next: output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json#L1001-L1200
  - output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json#L1001-L1200 -> next: output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json#L1201-L1400
  - output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json#L1201-L1400 -> next: output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json#L1401-L1600
  - output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json#L1401-L1600 -> next: output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json#L1601-L1800
  - output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json#L1601-L1800 -> next: output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json#L1801-L1872
  - output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json#L1801-L1872 -> next: END
- output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_backed_20260503-092828.json lines=386 chunks=2 chunk_size=200
  - output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_backed_20260503-092828.json#L1-L200 -> next: output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_backed_20260503-092828.json#L201-L386
  - output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_backed_20260503-092828.json#L201-L386 -> next: END
- docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md lines=578 chunks=3 chunk_size=200
  - docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md#L1-L200 -> next: docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md#L201-L400
  - docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md#L201-L400 -> next: docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md#L401-L578
  - docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md#L401-L578 -> next: END
- docs/LOCAL_AI_TASKS/shared-runtime-toolbox-orchestration-architecture.md lines=202 chunks=2 chunk_size=200
  - docs/LOCAL_AI_TASKS/shared-runtime-toolbox-orchestration-architecture.md#L1-L200 -> next: docs/LOCAL_AI_TASKS/shared-runtime-toolbox-orchestration-architecture.md#L201-L202
  - docs/LOCAL_AI_TASKS/shared-runtime-toolbox-orchestration-architecture.md#L201-L202 -> next: END
- output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_backed_20260503-092828.md lines=216 chunks=2 chunk_size=200
  - output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_backed_20260503-092828.md#L1-L200 -> next: output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_backed_20260503-092828.md#L201-L216
  - output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_backed_20260503-092828.md#L201-L216 -> next: END

## Compact bundle paths

- docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_backed_bundle_complex_ai_provider_backed_20260503-092828.json
- docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_backed_bundle_complex_ai_provider_backed_20260503-092828.md

```

### `output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_backed_20260503-092828.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `99199`
- SHA-256: `b2812a98d7afc2ee4c4a712614d787c773d75f865193765ca6f7a5f3e10506cd`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "shared_toolbox_ai_to_ai_final_summary",
  "stamp": "complex_ai_provider_backed_20260503-092828",
  "passed": true,
  "tools_available": [
    "build_agent_agnostic_tool_inventory",
    "build_agent_memory_inventory",
    "build_agent_transient_request_context",
    "build_code_interpreter_report",
    "build_python_line_count_csv",
    "build_refactor_duplication_audit",
    "check_python_syntax",
    "check_validation_report_contract",
    "run_gpu_planner_json_contract_smoke",
    "runtime_sqlite_memory"
  ],
  "tool_capabilities": [
    {
      "tool_name": "build_agent_agnostic_tool_inventory",
      "category": "inventory",
      "safe_default_mode": "report-only",
      "what_it_can_do": [
        "Inventory existing reusable IA-Carmine tools and guardrails."
      ],
      "what_it_must_not_do": [
        "execute arbitrary shell commands",
        "apply patches",
        "run Blender runtime",
        "commit output artifacts",
        "write SQLite or persistent memory"
      ],
      "recommended_next_use": "Discover reusable tooling before adding new scripts.",
      "allowed_args": [
        "root"
      ]
    },
    {
      "tool_name": "build_agent_memory_inventory",
      "category": "inventory",
      "safe_default_mode": "report-only",
      "what_it_can_do": [
        "Read-only SQLite/JSONL agent memory inventory."
      ],
      "what_it_must_not_do": [
        "execute arbitrary shell commands",
        "apply patches",
        "run Blender runtime",
        "commit output artifacts",
        "write SQLite or persistent memory"
      ],
      "recommended_next_use": "Summarize durable project memory as read-only context.",
      "allowed_args": [
        "objective",
        "memory_db"
      ]
    },
    {
      "tool_name": "build_agent_transient_request_context",
      "category": "context",
      "safe_default_mode": "report-only",
      "what_it_can_do": [
        "Build request-scoped context from memory notes, raw files and reports."
      ],
      "what_it_must_not_do": [
        "execute arbitrary shell commands",
        "apply patches",
        "run Blender runtime",
        "commit output artifacts",
        "write SQLite or persistent memory"
      ],
      "recommended_next_use": "Assemble request-scoped context for local AI planning.",
      "allowed_args": [
        "objective",
        "memory_note",
        "raw_file",
        "report_file"
      ]
    },
    {
      "tool_name": "build_code_interpreter_report",
      "category": "static_analysis",
      "safe_default_mode": "report-only",
      "what_it_can_do": [
        "Build static code-interpreter style report over selected roots."
      ],
      "what_it_must_not_do": [
        "execute arbitrary shell commands",
        "apply patches",
        "run Blender runtime",
        "commit output artifacts",
        "write SQLite or persistent memory"
      ],
      "recommended_next_use": "Build static analysis/refactor evidence.",
      "allowed_args": [
        "input"
      ]
    },
    {
      "tool_name": "build_python_line_count_csv",
      "category": "inventory",
      "safe_default_mode": "report-only",
      "what_it_can_do": [
        "Build full Python line-count CSV/JSON/MD evidence."
      ],
      "what_it_must_not_do": [
        "execute arbitrary shell commands",
        "apply patches",
        "run Blender runtime",
        "commit output artifacts",
        "write SQLite or persistent memory"
      ],
      "recommended_next_use": "Refresh complete Python inventory before refactor planning.",
      "allowed_args": [
        "exclude_dir"
      ]
    },
    {
      "tool_name": "build_refactor_duplication_audit",
      "category": "support_tool",
      "safe_default_mode": "report-only",
      "what_it_can_do": [
        "Build a report-only duplicated-helper/refactor audit over selected code roots and existing evidence reports."
      ],
      "what_it_must_not_do": [
        "execute arbitrary shell commands",
        "apply patches",
        "run Blender runtime",
        "commit output artifacts",
        "write SQLite or persistent memory"
      ],
      "recommended_next_use": "Use through the runtime tool broker when a report-only request requires it.",
      "allowed_args": [
        "root",
        "report",
        "input_audit_report",
        "line_count_report",
        "code_interpreter_report",
        "python_syntax_report",
        "bundle_smoke_report",
        "memory_routing_report"
      ]
    },
    {
      "tool_name": "check_python_syntax",
      "category": "validation",
      "safe_default_mode": "report-only",
      "what_it_can_do": [
        "Validate Python syntax across repository."
      ],
      "what_it_must_not_do": [
        "execute arbitrary shell commands",
        "apply patches",
        "run Blender runtime",
        "commit output artifacts",
        "write SQLite or persistent memory"
      ],
      "recommended_next_use": "Gate Python source changes.",
      "allowed_args": []
    },
    {
      "tool_name": "check_validation_report_contract",
      "category": "validation",
      "safe_default_mode": "report-only",
      "what_it_can_do": [
        "Validate validation report contract for a scoped report-dir or explicit report files."
      ],
      "what_it_must_not_do": [
        "execute arbitrary shell commands",
        "apply patches",
        "run Blender runtime",
        "commit output artifacts",
        "write SQLite or persistent memory"
      ],
      "recommended_next_use": "Gate report quality before evidence bundling.",
      "allowed_args": [
        "report_file"
      ]
    },
    {
      "tool_name": "run_gpu_planner_json_contract_smoke",
      "category": "validation",
      "safe_default_mode": "report-only",
      "what_it_can_do": [
        "Run GPU planner JSON contract smoke tests without provider."
      ],
      "what_it_must_not_do": [
        "execute arbitrary shell commands",
        "apply patches",
        "run Blender runtime",
        "commit output artifacts",
        "write SQLite or persistent memory"
      ],
      "recommended_next_use": "Validate planner JSON contract without providers.",
      "allowed_args": []
    },
    {
      "tool_name": "runtime_sqlite_memory",
      "category": "memory_status",
      "safe_default_mode": "controlled read-only/status by default",
      "what_it_can_do": [
        "Use protected persistent SQLite read-only or operational scratch SQLite memory under output/**."
      ],
      "what_it_must_not_do": [
        "execute arbitrary shell commands",
        "apply patches",
        "run Blender runtime",
        "commit output artifacts",
        "write persistent memory without explicit confirmation and authorization"
      ],
      "recommended_next_use": "Read memory status/search through broker-controlled actions.",
      "allowed_args": [
        "action",
        "scope",
        "database",
        "persistent_database",
        "summary",
        "content",
        "role",
        "tag",
        "query",
        "limit",
        "confirm",
        "allow_persistent_write"
      ]
    }
  ],
  "tool_requests_executed_or_proposed": [
    {
      "id": "request_build_code_interpreter_report",
      "tool": "build_code_interpreter_report",
      "reason": "Build static analysis/refactor evidence.",
      "args": {},
      "status": "proposed_or_reported"
    },
    {
      "id": "request_check_python_syntax",
      "tool": "check_python_syntax",
      "reason": "Gate Python source changes.",
      "args": {},
      "status": "proposed_or_reported"
    },
    {
      "id": "request_check_validation_report_contract",
      "tool": "check_validation_report_contract",
      "reason": "Gate report quality before evidence bundling.",
      "args": {},
      "status": "proposed_or_reported"
    }
  ],
  "reports_generated": [
    {
      "path": "output/validation/complex_ai_provider_backed_20260503-092828_resource_lanes.json",
      "exists": true,
      "json_ok": true,
      "kind": "local_ai_resource_lanes",
      "passed": true
    },
    {
      "path": "output/validation/complex_ai_provider_backed_20260503-092828_npu_provider_environment.json",
      "exists": true,
      "json_ok": true,
      "kind": "npu_provider_environment",
      "passed": true
    },
    {
      "path": "output/validation/complex_ai_provider_backed_20260503-092828_npu_decode_smoke.json",
      "exists": true,
      "json_ok": true,
      "kind": "npu_decode_smoke_diagnostic",
      "passed": true
    },
    {
      "path": "output/ai_pipeline/complex_ai_provider_backed_20260503-092828_orchestrator.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_gpu_npu_parallel_orchestrator",
      "passed": true
    },
    {
      "path": "output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_gpu_deep_planning_supervised",
      "passed": true
    }
  ],
  "remaining_gaps": [
    {
      "path": "output/validation/shared_toolbox_python_syntax_complex_ai_provider_backed_20260503-092828.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/analysis/shared_toolbox_code_interpreter_complex_ai_provider_backed_20260503-092828.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/shared_toolbox_gpu_contract_smoke_complex_ai_provider_backed_20260503-092828.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/shared_toolbox_gpu_routing_complex_ai_provider_backed_20260503-092828.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/shared_toolbox_npu_execution_complex_ai_provider_backed_20260503-092828.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/shared_toolbox_npu_contract_complex_ai_provider_backed_20260503-092828.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/npu_provider_environment_shared_toolbox_complex_ai_provider_backed_20260503-092828.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/ai_pipeline/shared_toolbox_ai_to_ai_complex_ai_provider_backed_20260503-092828_orchestrator.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/ai_pipeline/shared_toolbox_ai_to_ai_complex_ai_provider_backed_20260503-092828_gpu.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/analysis/shared_toolbox_gpu_npu_sync_complex_ai_provider_backed_20260503-092828.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/analysis/shared_toolbox_gpu_contract_replay_complex_ai_provider_backed_20260503-092828.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/analysis/shared_toolbox_code_interpreter_complex_ai_provider_backed_20260503-092828.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/ai_pipeline/shared_toolbox_ai_to_ai_complex_ai_provider_backed_20260503-092828_orchestrator.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/ai_pipeline/shared_toolbox_ai_to_ai_complex_ai_provider_backed_20260503-092828_gpu.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/analysis/shared_toolbox_gpu_npu_sync_complex_ai_provider_backed_20260503-092828.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/analysis/shared_toolbox_gpu_contract_replay_complex_ai_provider_backed_20260503-092828.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_backed_20260503-092828.md",
      "reason": "optional artifact missing"
    },
    {
      "gap": "runtime tool requests not proven in provider-backed run",
      "detail": "No concrete tool_requests were found in the included reports."
    }
  ],
  "recommended_next_task_md": "docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md",
  "compact_bundle_paths": [
    "docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_backed_bundle_complex_ai_provider_backed_20260503-092828.json",
    "docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_backed_bundle_complex_ai_provider_backed_20260503-092828.md"
  ],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "sqlite_write_performed": false,
  "persistent_memory_write_performed": false,
  "blender_runtime_execution_performed": false,
  "artifact_paths_considered": [
    "docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md",
    "docs/LOCAL_AI_TASKS/shared-runtime-toolbox-orchestration-architecture.md",
    "output/validation/complex_ai_provider_backed_20260503-092828_resource_lanes.md",
    "output/validation/complex_ai_provider_backed_20260503-092828_npu_provider_environment.md",
    "output/ai_packets/complex_ai_provider_backed_20260503-092828_npu_decode_smoke_output.md",
    "output/ai_pipeline/complex_ai_provider_backed_20260503-092828_orchestrator.md",
    "output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.md"
  ],
  "recursive_defaults": {
    "enabled": true,
    "stamp": "complex_ai_provider_backed_20260503-092828",
    "include_unstamped": false,
    "max_files": 120,
    "report_roots": [
      "output/validation",
      "output/analysis",
      "output/ai_pipeline"
    ],
    "artifact_roots": [
      "output/analysis",
      "output/ai_pipeline",
      "docs/LOCAL_AI_TASKS"
    ],
    "discovered_reports": [
      "output/validation/complex_ai_provider_backed_20260503-092828_npu_decode_smoke.json",
      "output/validation/complex_ai_provider_backed_20260503-092828_npu_pr
```

### `output/ai_pipeline/complex_ai_provider_backed_20260503-092828_orchestrator.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `22392`
- SHA-256: `fa1f656321d784c608ede27c26a85aba6873296ed111a88915209a0cd1e21c6c`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_npu_parallel_orchestrator",
  "generated_at": "2026-05-03T09:41:37",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_parallel_gpu_planner_npu_auditor",
  "elapsed_seconds": 518.146,
  "gpu_returncode": 0,
  "gpu_stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\complex_ai_provider_backed_20260503-092828_parallel_gpu.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\complex_ai_provider_backed_20260503-092828_parallel_gpu.md\",\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"elapsed_seconds\": 408.616,\n  \"round_count\": 23,\n  \"npu_audit_count\": 0,\n  \"npu_audit_success_count\": 0,\n  \"npu_auditor_disabled_reason\": \"\",\n  \"recommendation_count\": 0,\n  \"raw_recommendation_candidate_count\": 0,\n  \"filtered_recommendation_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"empty_recommendations_reason\": \"context_echo_detected\",\n  \"runtime_tool_broker_enabled\": false,\n  \"runtime_tool_bootstrap_executed\": false,\n  \"runtime_tool_bootstrap_passed\": null,\n  \"runtime_tool_bootstrap_request_count\": 0,\n  \"runtime_tool_bootstrap_execution_count\": 0,\n  \"runtime_tool_bootstrap_failed_count\": 0,\n  \"runtime_tool_bootstrap_blocked_count\": 0,\n  \"runtime_tool_request_count\": 0,\n  \"runtime_tool_execution_count\": 0,\n  \"runtime_tool_failed_count\": 0,\n  \"runtime_tool_blocked_count\": 0,\n  \"runtime_tool_result_count\": 0,\n  \"provider_empty_response_count\": 0,\n  \"evidence_ready_for_manual_patch_count\": 12,\n  \"ready_for_patch_plan\": false,\n  \"recommended_next_layer\": \"build_agent_review_patch_plan.py\"\n}\n",
  "gpu_stderr_tail": "",
  "gpu_output": "output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json",
  "gpu_markdown": "output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.md",
  "gpu_recommendation_count": 0,
  "gpu_empty_recommendations_reason": "context_echo_detected",
  "gpu_evidence_ready_for_manual_patch_count": 12,
  "gpu_recommended_next_layer": "build_agent_review_patch_plan.py",
  "runtime_tool_broker_enabled": false,
  "runtime_tool_bootstrap_executed": false,
  "runtime_tool_bootstrap_passed": null,
  "runtime_tool_bootstrap_request_count": 0,
  "runtime_tool_bootstrap_execution_count": 0,
  "runtime_tool_bootstrap_failed_count": 0,
  "runtime_tool_bootstrap_blocked_count": 0,
  "runtime_tool_request_count": 0,
  "runtime_tool_execution_count": 0,
  "runtime_tool_failed_count": 0,
  "runtime_tool_blocked_count": 0,
  "runtime_tool_result_count": 0,
  "orchestrator_runtime_tool_bootstrap": {
    "enabled": false,
    "executed": false,
    "bootstrap": true,
    "requested_tool_count": 0,
    "tool_results": []
  },
  "orchestrator_runtime_tool_bootstrap_executed": false,
  "orchestrator_runtime_tool_bootstrap_passed": null,
  "orchestrator_runtime_tool_bootstrap_request_count": 0,
  "orchestrator_runtime_tool_bootstrap_execution_count": 0,
  "orchestrator_runtime_tool_bootstrap_failed_count": 0,
  "orchestrator_runtime_tool_bootstrap_blocked_count": 0,
  "orchestrator_runtime_tool_bootstrap_result_count": 0,
  "gpu_orchestrated_runtime_tool_brokers": [],
  "gpu_orchestrated_runtime_tool_request_count": 0,
  "gpu_orchestrated_runtime_tool_execution_count": 0,
  "gpu_orchestrated_runtime_tool_failed_count": 0,
  "gpu_orchestrated_runtime_tool_blocked_count": 0,
  "gpu_orchestrated_runtime_tool_result_count": 0,
  "gpu_runner_direct_runtime_tool_broker": false,
  "gpu_summary": {
    "passed": true,
    "round_count": 23,
    "recommendation_count": 0,
    "raw_recommendation_candidate_count": 0,
    "filtered_recommendation_count": 0,
    "json_parse_error_count": 19,
    "repair_attempt_count": 0,
    "empty_recommendations_reason": "context_echo_detected",
    "evidence_ready_for_manual_patch_count": 12,
    "recommended_next_layer": "build_agent_review_patch_plan.py",
    "runtime_tool_broker_enabled": false,
    "runtime_tool_request_count": 0,
    "runtime_tool_execution_count": 0,
    "runtime_tool_failed_count": 0,
    "runtime_tool_blocked_count": 0,
    "runtime_tool_result_count": 0,
    "decision": {
      "ready_for_patch_plan": false,
      "ready_count": 0,
      "needs_more_context_count": 0,
      "fallback_patch_plan_recommended": true,
      "npu_auditor_non_blocking": true,
      "npu_unusable_or_failed_count": 0,
      "npu_audit_success_count": 0,
      "npu_auditor_disabled_reason": "",
      "recommended_next_layer": "build_agent_review_patch_plan.py",
      "manual_review_required": true
    }
  },
  "checkpoint_dir": "output/ai_pipeline/complex_ai_provider_backed_20260503-092828_checkpoints",
  "npu_audit_count": 4,
  "npu_audit_success_count": 4,
  "npu_tool_context_seen_count": 0,
  "npu_tool_request_count": 0,
  "npu_runtime_tool_request_count": 0,
  "npu_runtime_tool_execution_count": 0,
  "npu_runtime_tool_failed_count": 0,
  "npu_runtime_tool_blocked_count": 0,
  "npu_runtime_tool_result_count": 0,
  "npu_audits": [
    {
      "round": 1,
      "checkpoint": "output/ai_pipeline/complex_ai_provider_backed_20260503-092828_checkpoints/round_001.json",
      "audit_output": "output/ai_pipeline/complex_ai_provider_backed_20260503-092828_checkpoints/round_001_npu_async_audit.json",
      "started_at": "2026-05-03T09:33:05",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\complex_ai_provider_backed_20260503-092828_checkpoints\\round_001.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\complex_ai_provider_backed_20260503-092828_checkpoints\\round_001_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\complex_ai_provider_backed_20260503-092828_checkpoints\\round_001_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\complex_ai_provider_backed_20260503-092828_checkpoints\\round_001_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\complex_ai_provider_backed_20260503-092828_checkpoints\\round_001_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\complex_ai_provider_backed_20260503-092828_checkpoints\\round_001_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\complex_ai_provider_backed_20260503-092828_checkpoints\\round_001_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "420",
        "--max-context-chars",
        "10000",
        "--max-prompt-chars",
        "1400",
        "--max-new-tokens",
        "512",
        "--run-npu"
      ],
      "finished_at": "2026-05-03T09:35:19",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\complex_ai_provider_backed_20260503-092828_checkpoints\\\\round_001_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\complex_ai_provider_backed_20260503-092828_checkpoints\\\\round_001_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"runtime_tool_context_seen\": false,\n  \"runtime_tool_context_report_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "runtime_tool_context_seen": false,
      "runtime_tool_context_report_count": 0,
      "npu_tool_request_count": 0,
      "npu_valid_tool_request_count": 0,
      "npu_invalid_tool_request_count": 0,
      "npu_tool_requests": [],
      "gpu_review_blocked": false
    },
    {
      "round": 3,
      "checkpoint": "output/ai_pipeline/complex_ai_provider_backed_20260503-092828_checkpoints/round_003.json",
      "audit_output": "output/ai_pipeline/complex_ai_provider_backed_20260503-092828_checkpoints/round_003_npu_async_audit.json",
      "started_at": "2026-05-03T09:35:21",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\complex_ai_provider_backed_20260503-092828_checkpoints\\round_003.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\complex_ai_provider_backed_20260503-092828_checkpoints\\round_003_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\complex_ai_provider_backed_20260503-092828_checkpoints\\round_003_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\complex_ai_provider_backed_20260503-092828_checkpoints\\round_003_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\complex_ai_provider_backed_20260503-092828_checkpoints\\round_003_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\complex_ai_provider_backed_20260503-092828_checkpoints\\round_003_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\complex_ai_provider_backed_20260503-092828_checkpoints\\round_003_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "420",
        "--max-context-chars",
        "10000",
        "--max-prompt-chars",
        "1400",
        "--max-new-tokens",
        "512",
        "--run-npu"
      ],
      "finished_at": "2026-05-03T09:37:25",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\complex_ai_provider_backed_20260503-092828_checkpoints\\\\round_003_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\complex_ai_provider_backed_20260503-092828_checkpoints\\\\round_003_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"runtime_tool_context_seen\": false,\n  \"runtime_tool_context_report_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "runtime_tool_context_seen": false,
      "runtime_tool_context_report_count": 0,
      "npu_tool_request_count": 0,
      "npu_valid_tool_request_count": 0,
      "npu_invalid_tool_request_count": 0,
      "npu_tool_requests": [],
      "gpu_review_blocked": false
    },
    {
      "round": 6,
      "checkpoint": "output/ai_pipeline/complex_ai_provider_backed_20260503-092828_checkpoints/round_006.json",
      "audit_output": "output/ai_pipeline/complex_ai_provider_backed_20260503-092828_checkpoints/round_006_npu_async_audit.json",
      "started_at": "2026-05-03T09:37:27",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\complex_ai_provider_backed_20260503-092828_checkpoints\\round_006.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\complex_ai_provider_backed_20260503-092828_checkpoints\\round_006_npu_async_audit.json",
        "--markdown-output
```

### `output/ai_pipeline/complex_ai_provider_backed_20260503-092828_parallel_gpu.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `160313`
- SHA-256: `ded10a218eadbd98742c1b8e7b71761ea5db9c8d03f801916875ec83fda5ff88`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_deep_planning_supervised",
  "generated_at": "2026-05-03T09:39:48",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_gpu_deep_planning_with_non_blocking_npu_audit",
  "model_used": "qwen2.5-coder:14b",
  "ollama_base_url": "http://127.0.0.1:11434",
  "budget_minutes": 40,
  "elapsed_seconds": 408.616,
  "context_file_count": 180,
  "round_count": 23,
  "rounds": [
    {
      "round": 1,
      "elapsed_seconds": 5.012,
      "file_count": 8,
      "files": [
        "docs/AGENT_REVIEW_CODE_PATCH_PLAN.md",
        "docs/AI_ARTIFACT_SCHEMAS.md",
        "docs/AI_CHUNKING_STRATEGY.md",
        "docs/AI_CONTEXT_PACKS.md",
        "docs/AI_DOCS_ENTRYPOINT.md",
        "docs/AI_EXTERNAL_KNOWLEDGE.md",
        "docs/AI_GENERATED_PACKAGE_STANDARD.md",
        "docs/AI_GUARDRAILS_VALIDATION_GUIDE.md"
      ],
      "response_chars": 398,
      "raw_response_preview": "It seems like you have provided a detailed preview of several documents related to AI-generated content and validation processes within a Blender repository. These documents cover various aspects such as the standard for generated packages, guardrails and validation guidelines, JSON schemas, and more.\n\nIf you need further assistance or specific information from these documents, feel free to ask!",
      "parsed_response": {
        "summary": "It seems like you have provided a detailed preview of several documents related to AI-generated content and validation processes within a Blender repository. These documents cover various aspects such as the standard for generated packages, guardrails and validation guidelines, JSON schemas, and more.\n\nIf you need further assistance or specific information from these documents, feel free to ask!",
        "confidence": "low",
        "recommendations": [],
        "tool_requests": [],
        "missing_evidence": [
          "model_response_not_valid_json"
        ],
        "next_best_action": "review raw model response"
      },
      "provider_empty_response": false,
      "tool_requests": [],
      "invalid_tool_request_errors": [],
      "runtime_tool_broker": {
        "enabled": false,
        "requested_tool_count": 0,
        "executed": false,
        "tool_results": [],
        "guardrails": {
          "broker_execution_requires_enable_runtime_tool_broker": true,
          "patch_application_performed": false,
          "persistent_memory_write_performed": false
        }
      },
      "json_ok": false,
      "parse_error": "ModelJsonParseError: Unable to parse model JSON: Expecting value: line 1 column 1 (char 0)",
      "schema_ok": false,
      "schema_errors": [],
      "context_echo_detected": false,
      "model_output_schema_mismatch": false,
      "contract_empty_recommendations_reason": "json_parse_failure",
      "contract": {
        "json_ok": false,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "ModelJsonParseError: Unable to parse model JSON: Expecting value: line 1 column 1 (char 0)",
        "schema_errors": [],
        "raw_response_sha256": "11406257f2fbfb47b63af0987dfbf0da2b71cd7c69a1bded0a1ee36d32d2030b",
        "raw_response_chars": 398,
        "top_level_keys": [],
        "recommendation_count": 0,
        "valid_recommendation_count": 0,
        "invalid_recommendation_count": 0,
        "tool_request_count": 0,
        "valid_tool_request_count": 0,
        "invalid_tool_request_count": 0,
        "empty_recommendations_reason": "json_parse_failure"
      },
      "repair_attempt_count": 0,
      "raw_recommendation_candidate_count": 0,
      "filtered_recommendation_count": 0,
      "recommendation_count": 0,
      "tool_request_count": 0,
      "valid_tool_request_count": 0,
      "invalid_tool_request_count": 0,
      "empty_recommendations_reason": "json_parse_failure",
      "evidence_ready_for_manual_patch_count": 12,
      "recommended_next_layer": ""
    },
    {
      "round": 2,
      "elapsed_seconds": 9.866,
      "file_count": 8,
      "files": [
        "docs/AI_MEMORY_POLICY.md",
        "docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md",
        "docs/AI_ONBOARDING.md",
        "docs/AI_PIPELINE_ARCHITECTURE.md",
        "docs/AI_PIPELINE_OPTIMIZATION.md",
        "docs/AI_PIPELINE_REFACTOR_STATUS.md",
        "docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md",
        "docs/AI_REFERENCE_ONBOARDING.md"
      ],
      "response_chars": 1854,
      "raw_response_preview": "It seems like you have provided a detailed set of documentation files related to an AI pipeline project. These files cover various aspects such as the architecture, refactoring status, provider-agnostic guidelines, and optimization strategies. Here's a summary of the key points from each file:\n\n1. **AI_PIPELINE_ARCHITECTURE.md**:\n   - Describes the modular architecture of the AI artifact pipeline.\n   - Lists the main components like `defaults.py`, `models.py`, `runner.py`, etc.\n   - Explains the data flow and interaction between different modules.\n\n2. **AI_PIPELINE_REFACTOR_STATUS.md**:\n   - Provides a status marker for the current state of the pipeline refactor.\n   - Indicates that the modular split is complete but local validation is pending.\n   - Lists the required steps for local validation, including running specific Python scripts and regenerating indexes.\n\n3. **AI_PIPELINE_OPTIMIZATION.md**:\n   - Outlines the optimization priorities for the pipeline.\n   - Provides a checklist of tasks to be completed after the refactoring, such as improving report readability and refining lane policies.\n   - Includes instructions for running validation scripts to ensure compatibility and correctness.\n\n4. **AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md**:\n   - Explains how the AI pipeline should remain reusable across different providers and runtimes.\n   - Defines the roles of the orchestration, provider, and artifact layers.\n   - Provides guidelines for implementing each stage of the pipeline in a runtime-agnostic manner.\n\nThese documents are essential for maintaining and extending the AI pipeline project. They ensure that changes are made in a structured way, preserving compatibility with existing systems and allowing for future enhancements. If you have any specific questions or need further assistance with these files, feel free to ask!",
      "parsed_response": {
        "summary": "It seems like you have provided a detailed set of documentation files related to an AI pipeline project. These files cover various aspects such as the architecture, refactoring status, provider-agnostic guidelines, and optimization strategies. Here's a summary of the key points from each file:\n\n1. **AI_PIPELINE_ARCHITECTURE.md**:\n   - Describes the modular architecture of the AI artifact pipeline.\n   - Lists the main components like `defaults.py`, `models.py`, `runner.py`, etc.\n   - Explains the data flow and interaction between different modules.\n\n2. **AI_PIPELINE_REFACTOR_STATUS.md**:\n   - Provides a status marker for the current state of the pipeline refactor.\n   - Indicates that the modular split is complete but local validation is pending.\n   - Lists the required steps for local validation, including running specific Python scripts and regenerating indexes.\n\n3. **AI_PIPELINE_OPTIMIZATION.md**:\n   - Outlines the optimization priorities for the pipeline.\n   - Provides a checklist of tasks to be completed after the refactoring, such as improving report readability and refining lane policies.\n   - Includes instructions for running validation scripts to ensure compatibility and correctness.\n\n4. **AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md**:\n   - Explains how the AI pipeline should remain reusable across different providers and runtimes.\n   - Defines the roles of the orchestration, provider, and artifact layers.\n   - Provides guidelines for implementing each stage of the pipeline in a runtime-agnostic manner.\n\nThese documents are essential for maintaining and extending the AI pipeline project. They ensure that changes are made in a structured way, preserving compatibility with existing systems and allowing for future enhancements. If you have any specific questions or need further assistance with these files, feel free to ask!",
        "confidence": "low",
        "recommendations": [],
        "tool_requests": [],
        "missing_evidence": [
          "model_response_not_valid_json"
        ],
        "next_best_action": "review raw model response"
      },
      "provider_empty_response": false,
      "tool_requests": [],
      "invalid_tool_request_errors": [],
      "runtime_tool_broker": {
        "enabled": false,
        "requested_tool_count": 0,
        "executed": false,
        "tool_results": [],
        "guardrails": {
          "broker_execution_requires_enable_runtime_tool_broker": true,
          "patch_application_performed": false,
          "persistent_memory_write_performed": false
        }
      },
      "json_ok": false,
      "parse_error": "ModelJsonParseError: Unable to parse model JSON: Expecting value: line 1 column 1 (char 0)",
      "schema_ok": false,
      "schema_errors": [],
      "context_echo_detected": false,
      "model_output_schema_mismatch": false,
      "contract_empty_recommendations_reason": "json_parse_failure",
      "contract": {
        "json_ok": false,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "ModelJsonParseError: Unable to parse model JSON: Expecting value: line 1 column 1 (char 0)",
        "schema_errors": [],
        "raw_response_sha256": "5878afdd193426dd0e665533a93edc8b75f7b9ab118fee83c4b034dbe9258c8b",
        "raw_response_chars": 1854,
        "top_level_keys": [],
        "recommendation_count": 0,
        "valid_recommendation_count": 0,
        "invalid_recommendation_count": 0,
        "tool_request_count": 0,
        "valid_tool_request_count": 0,
        "invalid_tool_request_count": 0,
        "empty_recommendations_reason": "json_parse_failure"
      },
      "repair_attempt_count": 0,
      "raw_recommendation_candidate_count": 0,
      "filtered_recommendation_count": 0,
      "recommendation_count": 0,
      "tool_request_count": 0,
      "valid_tool_request_count": 0,
      "invalid_tool_request_count": 0,
      "empty_recommendations_reason": "json_parse_failure",
      "evidence_ready_for_manual_patch_count": 12,
      "recommended_next_layer": ""
    },
    {
      "round": 3,
      "elapsed_seconds": 25.214,
      "file_count": 8,
      "files": [
        "docs/AI_REFERENCE_SOURCE_MAP.md",
        "docs/AI_SELECTIVE_PLANNER.md",
        "docs/AI_SMART_POLICY.md",
        "docs/AI_WORKLOAD_REPORT_QUALITY_GATE.md",
        "docs/AUDIO_ANALYSIS_PIPELINE.md",
        "docs/AUTO_PUSH_GENERATED_ARTIFACTS.md",
        "docs/BLENDER_SCRIPT_ENTRYPOINTS.md",
        "docs/CODE_CONSULTATION_REPORT.md"
      ],
      "response_chars": 5369,
      "raw_response_preview": "```json\n{\n  \"path\": \"docs/CODE_CONSULTATION_REPORT.md\",\n  \"exists\": true,\n  \"lines\": 151,\n  \"chars\": 6000,\n  \"content_preview\": \"# Code Consultation Report\\n\\n## Scope\\n\\nThis report summarizes a broad code consultation of `blender-audio-project` after the GitHub code-quality check was launched.\\n\\nThe review is non-destructive. No working Blender script was refactored or modified.\\n\\n## Repository status\\n\\n- Repository: `C-F-tek/blender-audio-project`\\n- Default branch: `master`\\n- Visibility: private\\n- GitHub App permissions observed: admin, maintain, pull, push, triage\\n- Repository size observed: about 2564 KB\\n\\n## Code quality workflow visibility\\n\\nNo workflow run was visible through the available GitHub connector for the checked commits.\\n\\nThe following common workflow paths were not found:\\n\\n```text\\n.github/workflows/code-quality.yml\\n.github/workflows/code_quality.yml\\n.github/workflows/ci.yml\\n```\\n\\nThis means that the code-quality action may be external, not indexed through the available API endpoint, manually launched in a way not returned by commit workflow lookup, or not yet committed as a workflow file.\\n\\n## Source index consulted\\n\\nThe main source index consulted was:\\n\\n```text\\nindexAI/project_code_index.md\\nindexAI/project_code_manifest.json\\n```\\n\\nThe index reports:\\n\\n- 98 indexed files\\n- 212 code chunks\\n- generated timestamp: `2026-04-27T14:41:27`\\n\\nImportant: this index predates the latest documentation and template additions. It should be regenerated.\\n\\n## Main code areas\\n\\n### Root tools\\n\\n| File | Role | Assessment |\\n|---|---|---|\\n| `analyze_wav.py` | WAV analysis, low/mid/high/onset/beat extraction, Blender JSON generation | Good functional core. Needs dependency documentation and optional validation. |\\n| `build_track_summary.py` | Compact summary builder from analysis JSON | Useful, but default paths are track-specific. Should be made more generic or documented as local defaults. |\\n| `normalize_scene_spec.py` | Scene-spec normalization | Useful, but contains duplicated helper function definitions that should be reviewed. |\\n\\n### Blender package area\\n\\n| Area | Role | Assessment |\\n|---|---|---|\\n| `Scripting/v61b/` | Main complex reference package | Strong reference model. Do not refactor broadly without Blender tests. |\\n| `Scripting/v61b_backgood/` | Backup or previous-good version | Useful safety copy, but should be documented as backup/reference. |\\n| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/` | Additional generated package | Should be compared with v61b standards and documented per package. |\\n| `Scripting/_template_audio_reactive_package/` | New package template | Good structure. Not pa
```

## Selected chunks evidence

### `docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `selected_semantic_chunks_evidence`
- Passed: `True`
- Provider execution performed: `False`
- Source writes performed: `False`
- Selected count: `24`
- Total selected chars: `28649`
- Max total chars: `32000`
- Decision: `{'selected_chunks_built': True, 'budget_respected': True, 'provider_execution_seen': False, 'source_writes_performed': False, 'forbidden_paths_blocked': True}`

## Git push helper

```powershell
git add docs/LOCAL_VALIDATION_EVIDENCE/
git commit -m "test: add local ai workflow evidence bundle"
git push
```
