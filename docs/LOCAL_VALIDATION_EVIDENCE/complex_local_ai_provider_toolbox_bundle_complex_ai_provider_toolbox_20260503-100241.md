# Local Validation Evidence Bundle

- Generated at: `2026-05-03T10:19:52`
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
- `included_artifact_count`: `15`
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

### `output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_npu_parallel_orchestrator`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_deep_planning_supervised`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `0`
- Recommended next layer: `build_agent_review_patch_plan.py`

### `output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/round_000_runtime_tool_broker.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/local_ai_runs/complex-provider-toolbox-v1-20260503-095940/pipeline/local_ai_task_pipeline_adapter_manifest.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `local_ai_task_pipeline_adapter_manifest`
- Passed: `None`
- Patch application performed: `False`

### `output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_toolbox_20260503-100241.json`

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
- `output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_orchestrator.json` exists=`True` size=`68345` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json` exists=`True` size=`214288` suffix=`.json` preview_chars=`1500`
- `output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/round_000_runtime_tool_broker.json` exists=`True` size=`41854` suffix=`.json` preview_chars=`1500`
- `output/local_ai_runs/complex-provider-toolbox-v1-20260503-095940/pipeline/local_ai_task_pipeline_adapter_manifest.json` exists=`True` size=`6012` suffix=`.json` preview_chars=`1500`
- `output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_toolbox_20260503-100241.json` exists=`True` size=`106956` suffix=`.json` preview_chars=`1500`

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

### `docs/LOCAL_AI_TASKS/complex-provider-toolbox-request-v1.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3886`
- SHA-256: `e9d06317ddcf42f4f3d776f9e04f494fb1e40944f0c39b6e0929a480d5314ceb`
- Content included: `True`
- Content truncated: `False`

```text
# Complex Provider Toolbox Request v1

## Purpose

This is the first real Markdown task input for a complete IA-Carmine local AI request.

The task must prove that a complex engineering request can use both provider execution and the runtime toolbox in the same controlled cycle.

## Required reading

Read these files before planning:

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/complex-provider-toolbox-request-v1.md
docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_tool_usage_bundle_complex_ai_tool_usage_20260503-092256.json
docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_backed_bundle_complex_ai_provider_backed_20260503-092828.json
```

## Objective

Perform a provider-backed engineering review of the current IA-Carmine repository state.

The review must use:

```text
GPU/Ollama provider execution
NPU/OpenVINO provider execution
orchestrator-controlled runtime toolbox broker
memory and tool inventory reports
code and documentation coherence reports
duplication/refactor audit reports
compact evidence bundle output
```

## Engineering questions

Answer these questions from evidence, not from memory alone:

1. Did GPU/Ollama execute as provider?
2. Did NPU/OpenVINO execute as provider?
3. Did NPU decode produce usable text?
4. Did the orchestrator enable the runtime toolbox broker?
5. Did the broker execute at least one allowlisted tool?
6. Did any tool request fail or get blocked?
7. Did the provider lanes see toolbox context or broker reports?
8. Was persistent memory written?
9. Was operational memory only used as scratch/status evidence?
10. Are docs and code still coherent after PR #146 through #150?
11. Which duplicated helper families remain?
12. Which method/function restructuring candidates are ready for manual patch planning?
13. Which next PR has the best value-to-risk ratio?

## Required toolbox evidence

The run should produce evidence for at least these tool categories:

```text
agent/tool inventory
memory status or memory inventory
Python line-count inventory
Python syntax validation
validation report contract check
code/static interpreter report
refactor duplication audit
```

The broker must remain the only tool executor.

## Required provider evidence

The run must include provider-backed evidence for:

```text
resource lanes with provider_execution_performed=True
GPU/Ollama report with provider_execution_performed=True
NPU decode smoke with provider_execution_performed=True
NPU auditor records with provider_execution_performed=True where audits run
```

## Success criteria

The task is successful only if the final reports show:

```text
provider_execution_performed=True
runtime_tool_broker_enabled=True
runtime_tool_execution_count > 0
runtime_tool_failed_count=0
runtime_tool_blocked_count=0
npu_audit_success_count > 0
patch_application_performed=False
persistent_memory_write_performed=False
```

Stronger success if one of these is also true:

```text
npu_tool_context_seen_count > 0
npu_runtime_tool_execution_count > 0
```

## Guardrails

```text
Do not apply patches.
Do not run Blender.
Do not commit output/**.
Do not commit *.db or *.sqlite.
Do not write persistent memory.
Do not expose a free shell to providers.
Do not treat NPU as primary advisor unless a future quality gate explicitly allows it.
```

## Expected final answer from local AI

The local AI should produce a concise engineering report with:

```text
provider_execution_summary
toolbox_usage_summary
memory_usage_summary
documentation_code_coherence_summary
duplication_refactor_summary
ready_for_patch_plan_candidates
needs_more_context_candidates
advisory_only_findings
next_recommended_pr
bundle_manifest
```

## Evidence bundle policy

Build a compact bundle under:

```text
docs/LOCAL_VALIDATION_EVIDENCE/
```

Include only compact bundle files in Git.

Do not commit raw runtime reports under `output/**`.

```

### `output/local_ai_runs/complex-provider-toolbox-v1-20260503-095940/pipeline/local_ai_task_pipeline.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2769`
- SHA-256: `a911fe00085105c020b8be2c11b600014e7f870c15d0a7377fe7280eed67072f`
- Content included: `True`
- Content truncated: `False`

```text
# Post-Validation AI Work Packet

- Generated at: `2026-05-03T09:59:41`
- Repo: `C:\Users\carmi\blender\blender-audio-project`
- Profile: `docs`
- Ollama used: `False`
- Packet manifest: `C:\Users\carmi\blender\blender-audio-project\output\local_ai_runs\complex-provider-toolbox-v1-20260503-095940\pipeline\local_ai_task_pipeline_manifest.json`

## Advisory context routing

- Enforced: `True`
- Provider execution performed: `False`
- Advisory lanes: `ollama`
- Excluded advisory lanes: `npu`

## Deterministic suggestions

### P2 — Review active execution plans before opening the next milestone

- Area: `execution_plans`
- Details: docs/EXECUTION_PLANS/active/2026-04-29_agent_state_memory_integration.md; docs/EXECUTION_PLANS/active/2026-04-29_agentic_memory_guardrail_pipeline.md; docs/EXECUTION_PLANS/active/2026-04-29_formal_json_schema_validation.md; docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md; docs/EXECUTION_PLANS/active/2026-04-30_ai_pipeline_report_contracts.md; docs/EXECUTION_PLANS/active/2026-04-30_dry_run_matrix_contract_followups.md; docs/EXECUTION_PLANS/active/2026-04-30_npu_output_policy_provider_preflight.md; docs/EXECUTION_PLANS/active/2026-04-30_npu_pipeline_decomposition_plan.md; docs/EXECUTION_PLANS/active/2026-04-30_runtime_safe_provider_report_adoption.md; docs/EXECUTION_PLANS/active/2026-04-30_validator_report_consistency_review.md

### P2 — Prefer additive observability before provider or Blender runtime changes

- Area: `agnostic_core`
- Details: Safe next steps: report contract consistency, runtime-output manifest emission, provider-result parsing/reporting without changing provider execution.

## Inputs

### Trusted context files
- `AGENTS.md`
- `WORKFLOW.md`
- `docs/README.md`
- `docs/AI_DOCS_ENTRYPOINT.md`
- `docs/PROJECT_STATUS_POINT.md`
- `docs/GITHUB_ONLY_AI_CONTINUATION_GUIDE.md`
- `docs/GITHUB_LOCAL_VALIDATION_WORKFLOW.md`
- `docs/TECH_DEBT_TRACKER.md`
- `docs/LOCAL_AI_TASKS/complex-provider-toolbox-request-v1.md`

### Report files
- `output/validation/docs_links.json`
- `output/validation/execution_plan_status.json`
- `output/validation/json_artifacts.json`
- `output/validation/validation_report_contract.json`
- `output/validation/python_syntax.json`
- `output/validation/ai_workload_quality_lane_routing.json`
- `output/validation/npu_decode_quality_remediation.json`
- `output/validation/npu_decode_smoke_diagnostic.json`

## Guardrails

- Advisory only: do not auto-apply edits from this packet.
- Output/input paths are configurable; defaults are not part of the architecture boundary.
- Validate locally before committing generated indexes.
- Keep provider execution changes in a separate explicitly scoped milestone.

```

### `output/local_ai_runs/complex-provider-toolbox-v1-20260503-095940/pipeline/local_ai_task_pipeline_proposals.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3476`
- SHA-256: `97d6ae015d8624edac03c5230f96e181f5d699233c319d1dfeb508b5c5cf162a`
- Content included: `True`
- Content truncated: `False`

```text
# Repository Change Proposals

- Generated at: `2026-05-03T09:59:41`
- Profile: `docs`
- Apply mode: `manual_review_only`
- Proposal count: `1`

## P-AI-WORKLOAD-REPORT-QUALITY-GATE — Gate AI workload reports before using them as advisory context

- Priority: `P1`
- Area: `local_ai_workloads`
- Change type: `workload_quality_gate`
- Apply mode: `manual_review_only`
- Rationale: AI workload report quality found usable lanes: ollama; unusable lanes: npu. Downstream packets and proposals should trust only usable workload reports and keep unusable lanes limited to probes until their decoding/configuration is fixed.

### Evidence summary

```json
{
  "workload_quality_decision": {
    "quality_report_present": true,
    "usable_lanes": [
      "ollama"
    ],
    "unusable_lanes": [
      "npu"
    ],
    "ollama_gpu_primary_advisory_allowed": true,
    "npu_excluded_from_primary_advisory": true,
    "routing_policy": "usable_text_lanes_only_for_advisory_context"
  }
}
```

### Target files
- `Tools/validation/check_ai_workload_report_quality.py`
- `Tools/npu/run_npu_review.py`
- `Tools/ai/suggest_repository_updates.py`
- `Tools/ai/build_repository_change_proposals.py`
- `Tools/validation/README.md`
- `docs/JSON_SCHEMAS.md`

### Patch sketch
- Keep Ollama/GPU workload reports as primary advisory context when classified usable.
- Exclude or clearly mark NPU/OpenVINO generated reports as unusable when they are numeric/hex-like or non-linguistic.
- Do not disable NPU preflight/probe; only prevent low-quality NPU generation output from influencing suggestions.
- Add report metadata that distinguishes availability, execution and output usability.

### Suggestion outputs
- `python_code` `Tools/validation/check_ai_workload_report_quality.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/npu/run_npu_review.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/ai/suggest_repository_updates.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/ai/build_repository_change_proposals.py` (manual_patch_suggestion, manual_review_only)
- `markdown` `Tools/validation/README.md` (manual_patch_suggestion, manual_review_only)
- `markdown` `docs/JSON_SCHEMAS.md` (manual_patch_suggestion, manual_review_only)

### Validation
- `python .\Tools\validation\check_ai_workload_report_quality.py --repo-root . --output .\output\validation\ai_workload_report_quality.json`
- `powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_post_validation_ai_packet.ps1 -Profile npu -OutputDir output/ai_packets -Basename npu_ollama_real_workload_after_tests -ProposalBasename npu_ollama_real_workload_proposals -ContextFile output/ai_packets/npu_real_workload_report.md,output/ai_packets/ollama_gpu_real_workload_report.md -ReportFile output/validation/ai_workload_report_quality.json,output/validation/local_ai_resource_lanes.json,output/validation/provider_result_report.json,output/validation/local_provider_probe.json,output/validation/npu_runtime_output_manifest.json`

### Stop conditions
- Any change would execute providers implicitly or by default.
- Any change would hide a failing/unusable AI workload report instead of reporting it.
- Any change would alter NPU/Ollama model configuration, prompt prose or provider orchestration.

## Guardrail

These are proposals only. They must not be auto-applied without explicit review.

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

### `output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_orchestrator.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1951`
- SHA-256: `97454aa3b651c86299cc9f8e264ce39e3fba4160fc7ad331c69dda9131aea532`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU/NPU Parallel Orchestrator

- `passed`: `True`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `gpu_returncode`: `0`
- `elapsed_seconds`: `650.044`
- `npu_audit_count`: `4`
- `npu_audit_success_count`: `4`
- `npu_tool_context_seen_count`: `4`
- `npu_tool_request_count`: `0`
- `npu_runtime_tool_request_count`: `0`
- `npu_runtime_tool_execution_count`: `0`
- `npu_runtime_tool_failed_count`: `0`
- `npu_runtime_tool_blocked_count`: `0`
- `npu_runtime_tool_result_count`: `0`
- `gpu_recommendation_count`: `0`
- `gpu_empty_recommendations_reason`: `context_echo_detected`
- `gpu_evidence_ready_for_manual_patch_count`: `12`
- `runtime_tool_broker_enabled`: `True`
- `runtime_tool_request_count`: `7`
- `runtime_tool_execution_count`: `7`
- `runtime_tool_failed_count`: `0`
- `runtime_tool_blocked_count`: `0`
- `runtime_tool_result_count`: `7`

## Decision
- `gpu_review_blocked_by_npu`: `False`
- `npu_auditor_mode`: `parallel_best_effort`
- `npu_audit_success_count`: `4`
- `npu_tool_context_seen_count`: `4`
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
- `runtime_tool_broker_enabled`: `True`
- `runtime_tool_result_count`: `7`
- `manual_review_required`: `True`

## NPU Audits
- round `1` status=`finished` class=`usable_audit_text` success=`True`
- round `3` status=`finished` class=`usable_audit_text` success=`True`
- round `6` status=`finished` class=`usable_audit_text` success=`True`
- round `9` status=`finished` class=`usable_audit_text` success=`True`

```

### `output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1055`
- SHA-256: `ce946ae932015582f35bf1b889dec0e8f95abd2fc83edd158a154d0b0d5b607d`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU Deep Planning Review

- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Model: `qwen2.5-coder:14b`
- Elapsed seconds: `542.25`
- Round count: `24`
- Recommendation count: `0`
- Raw recommendation candidates: `0`
- Filtered recommendation count: `0`
- Tool request count: `0`
- Valid tool request count: `0`
- Invalid tool request count: `0`
- JSON parse error count: `16`
- Context echo detected count: `4`
- Model output schema mismatch count: `8`
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

### `output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/round_000_runtime_tool_broker.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `4246`
- SHA-256: `5702dd1ae5a619b531a3773d2de927bee7a113ff816c9fc5f6bad2ed483dfc2f`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Runtime Tool Broker

- passed: `True`
- dry_run: `False`
- tool_request_count: `7`
- tool_execution_count: `7`
- blocked_tool_count: `0`
- failed_tool_count: `0`
- provider_execution_performed: `False`
- patch_application_performed: `False`
- sqlite_write_performed: `False`
- persistent_memory_write_performed: `False`
- operational_sqlite_write_performed: `False`
- operational_sqlite_write_count: `0`
- operational_memory_clear_count: `0`
- blender_runtime_execution_performed: `False`

## Tool results

### `bootstrap_tool_inventory` — `build_agent_agnostic_tool_inventory`

- Executed: `True`
- Blocked: `False`
- Return code: `0`
- Outputs: `{'json_report': 'output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/bootstrap_tool_inventory_agent_agnostic_tool_inventory.json', 'markdown_report': 'output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/bootstrap_tool_inventory_agent_agnostic_tool_inventory.md'}`

### `bootstrap_memory_inventory` — `build_agent_memory_inventory`

- Executed: `True`
- Blocked: `False`
- Return code: `0`
- Outputs: `{'json_report': 'output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/bootstrap_memory_inventory_agent_memory_inventory.json', 'markdown_report': 'output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/bootstrap_memory_inventory_agent_memory_inventory.md'}`

### `bootstrap_persistent_memory_status` — `runtime_sqlite_memory`

- Executed: `True`
- Blocked: `False`
- Return code: `0`
- Outputs: `{'json_report': 'output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/bootstrap_persistent_memory_status_runtime_sqlite_memory.json', 'markdown_report': 'output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/bootstrap_persistent_memory_status_runtime_sqlite_memory.md'}`

### `bootstrap_operational_memory_status` — `runtime_sqlite_memory`

- Executed: `True`
- Blocked: `False`
- Return code: `0`
- Outputs: `{'json_report': 'output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/bootstrap_operational_memory_status_runtime_sqlite_memory.json', 'markdown_report': 'output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/bootstrap_operational_memory_status_runtime_sqlite_memory.md'}`

### `bootstrap_python_line_count` — `build_python_line_count_csv`

- Executed: `True`
- Blocked: `False`
- Return code: `0`
- Outputs: `{'json_report': 'output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/bootstrap_python_line_count_python_line_count.json', 'markdown_report': 'output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/bootstrap_python_line_count_python_line_count.md', 'csv_output': 'output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/bootstrap_python_line_count_python_line_count.csv'}`

### `bootstrap_python_syntax` — `check_python_syntax`

- Executed: `True`
- Blocked: `False`
- Return code: `0`
- Outputs: `{'json_report': 'output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/bootstrap_python_syntax_python_syntax.json'}`

### `bootstrap_gpu_contract_smoke` — `run_gpu_planner_json_contract_smoke`

- Executed: `True`
- Blocked: `False`
- Return code: `0`
- Outputs: `{'json_report': 'output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/bootstrap_gpu_contract_smoke_gpu_planner_json_contract_smoke.json', 'markdown_report': 'output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/bootstrap_gpu_contract_smoke_gpu_planner_json_contract_smoke.md'}`

## Guardrails

- `free_shell_exposed`: `False`
- `allowlist_enforced`: `True`
- `provider_execution_performed`: `False`
- `patch_application_performed`: `False`
- `sqlite_write_performed`: `False`
- `persistent_memory_write_performed`: `False`
- `operational_sqlite_write_allowed_under_output`: `True`
- `operational_sqlite_write_performed`: `False`
- `operational_memory_clear_count`: `0`
- `blender_runtime_touched`: `False`
- `git_write_performed`: `False`
- `manual_review_required`: `True`

```

### `output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_toolbox_20260503-100241.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `16380`
- SHA-256: `e48bb1485452d7befc843e958b4d49b7bff4d684e0d51d486862694ba845d90d`
- Content included: `True`
- Content truncated: `True`

```text
# Shared Toolbox AI-to-AI Final Summary

- stamp: complex_ai_provider_toolbox_20260503-100241
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
- output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_orchestrator.json exists=True json_ok=True kind=agent_gpu_npu_parallel_orchestrator passed=True
- output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json exists=True json_ok=True kind=agent_gpu_deep_planning_supervised passed=True
- output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/round_000_runtime_tool_broker.json exists=True json_ok=True kind=agent_runtime_tool_broker passed=True
- output/local_ai_runs/complex-provider-toolbox-v1-20260503-095940/pipeline/local_ai_task_pipeline_adapter_manifest.json exists=True json_ok=True kind=local_ai_task_pipeline_adapter_manifest passed=None

## Remaining gaps

- output/validation/shared_toolbox_python_syntax_complex_ai_provider_toolbox_20260503-100241.json: optional report missing
- output/analysis/shared_toolbox_code_interpreter_complex_ai_provider_toolbox_20260503-100241.json: optional report missing
- output/validation/shared_toolbox_gpu_contract_smoke_complex_ai_provider_toolbox_20260503-100241.json: optional report missing
- output/validation/shared_toolbox_gpu_routing_complex_ai_provider_toolbox_20260503-100241.json: optional report missing
- output/validation/shared_toolbox_npu_execution_complex_ai_provider_toolbox_20260503-100241.json: optional report missing
- output/validation/shared_toolbox_npu_contract_complex_ai_provider_toolbox_20260503-100241.json: optional report missing
- output/validation/npu_provider_environment_shared_toolbox_complex_ai_provider_toolbox_20260503-100241.json: optional report missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_complex_ai_provider_toolbox_20260503-100241_orchestrator.json: optional report missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_complex_ai_provider_toolbox_20260503-100241_gpu.json: optional report missing
- output/analysis/shared_toolbox_gpu_npu_sync_complex_ai_provider_toolbox_20260503-100241.json: optional report missing
- output/analysis/shared_toolbox_gpu_contract_replay_complex_ai_provider_toolbox_20260503-100241.json: optional report missing
- output/analysis/shared_toolbox_code_interpreter_complex_ai_provider_toolbox_20260503-100241.md: optional artifact missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_complex_ai_provider_toolbox_20260503-100241_orchestrator.md: optional artifact missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_complex_ai_provider_toolbox_20260503-100241_gpu.md: optional artifact missing
- output/analysis/shared_toolbox_gpu_npu_sync_complex_ai_provider_toolbox_20260503-100241.md: optional artifact missing
- output/analysis/shared_toolbox_gpu_contract_replay_complex_ai_provider_toolbox_20260503-100241.md: optional artifact missing
- output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_toolbox_20260503-100241.md: optional artifact missing
- runtime tool requests not proven in provider-backed run: No concrete tool_requests were found in the included reports.

## Recommended next task

docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md

## Recursive defaults

- Enabled: `True`
- Discovered reports: `3`
- Discovered artifacts: `6`

## Chunked large JSON/Markdown files

- output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_orchestrator.json lines=835 chunks=5 chunk_size=200
  - output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_orchestrator.json#L1-L200 -> next: output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_orchestrator.json#L201-L400
  - output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_orchestrator.json#L201-L400 -> next: output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_orchestrator.json#L401-L600
  - output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_orchestrator.json#L401-L600 -> next: output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_orchestrator.json#L601-L800
  - output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_orchestrator.json#L601-L800 -> next: output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_orchestrator.json#L801-L835
  - output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_orchestrator.json#L801-L835 -> next: END
- output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json lines=2533 chunks=13 chunk_size=200
  - output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L1-L200 -> next: output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L201-L400
  - output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L201-L400 -> next: output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L401-L600
  - output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L401-L600 -> next: output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L601-L800
  - output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L601-L800 -> next: output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L801-L1000
  - output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L801-L1000 -> next: output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L1001-L1200
  - output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L1001-L1200 -> next: output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L1201-L1400
  - output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L1201-L1400 -> next: output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L1401-L1600
  - output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L1401-L1600 -> next: output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L1601-L1800
  - output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L1601-L1800 -> next: output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L1801-L2000
  - output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L1801-L2000 -> next: output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L2001-L2200
  - output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L2001-L2200 -> next: output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L2201-L2400
  - output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L2201-L2400 -> next: output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L2401-L2533
  - output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json#L2401-L2533 -> next: END
- output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/round_000_runtime_tool_broker.json lines=477 chunks=3 chunk_size=200
  - output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/round_000_runtime_tool_broker.json#L1-L200 -> next: output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/round_000_runtime_tool_broker.json#L201-L400
  - output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/round_000_runtime_tool_broker.json#L201-L400 -> next: output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/round_000_runtime_tool_broker.json#L401-L477
  - output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/round_000_runtime_tool_broker.json#L401-L477 -> next: END
- output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_toolbox_20260503-100241.json lines=404 chunks=3 chunk_size=200
  - output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_toolbox_20260503-100241.json#L1-L200 -> next: output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_toolbox_20260503-100
```

### `output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_toolbox_20260503-100241.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `106956`
- SHA-256: `c3ebb6b736c2d8fa3c0be0e88e074f9dc11830c73a1ffd288a4c2505f1ff4f24`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "shared_toolbox_ai_to_ai_final_summary",
  "stamp": "complex_ai_provider_toolbox_20260503-100241",
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
      "path": "output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_orchestrator.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_gpu_npu_parallel_orchestrator",
      "passed": true
    },
    {
      "path": "output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_gpu_deep_planning_supervised",
      "passed": true
    },
    {
      "path": "output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/round_000_runtime_tool_broker.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_runtime_tool_broker",
      "passed": true
    },
    {
      "path": "output/local_ai_runs/complex-provider-toolbox-v1-20260503-095940/pipeline/local_ai_task_pipeline_adapter_manifest.json",
      "exists": true,
      "json_ok": true,
      "kind": "local_ai_task_pipeline_adapter_manifest",
      "passed": null
    }
  ],
  "remaining_gaps": [
    {
      "path": "output/validation/shared_toolbox_python_syntax_complex_ai_provider_toolbox_20260503-100241.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/analysis/shared_toolbox_code_interpreter_complex_ai_provider_toolbox_20260503-100241.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/shared_toolbox_gpu_contract_smoke_complex_ai_provider_toolbox_20260503-100241.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/shared_toolbox_gpu_routing_complex_ai_provider_toolbox_20260503-100241.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/shared_toolbox_npu_execution_complex_ai_provider_toolbox_20260503-100241.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/shared_toolbox_npu_contract_complex_ai_provider_toolbox_20260503-100241.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/npu_provider_environment_shared_toolbox_complex_ai_provider_toolbox_20260503-100241.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/ai_pipeline/shared_toolbox_ai_to_ai_complex_ai_provider_toolbox_20260503-100241_orchestrator.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/ai_pipeline/shared_toolbox_ai_to_ai_complex_ai_provider_toolbox_20260503-100241_gpu.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/analysis/shared_toolbox_gpu_npu_sync_complex_ai_provider_toolbox_20260503-100241.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/analysis/shared_toolbox_gpu_contract_replay_complex_ai_provider_toolbox_20260503-100241.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/analysis/shared_toolbox_code_interpreter_complex_ai_provider_toolbox_20260503-100241.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/ai_pipeline/shared_toolbox_ai_to_ai_complex_ai_provider_toolbox_20260503-100241_orchestrator.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/ai_pipeline/shared_toolbox_ai_to_ai_complex_ai_provider_toolbox_20260503-100241_gpu.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/analysis/shared_toolbox_gpu_npu_sync_complex_ai_provider_toolbox_20260503-100241.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/analysis/shared_toolbox_gpu_contract_replay_complex_ai_provider_toolbox_20260503-100241.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/analysis/shared_toolbox_ai_to_ai_final_summary_complex_ai_provider_toolbox_20260503-100241.md",
      "reason": "optional artifact missing"
    },
    {
      "gap": "runtime tool requests not proven in provider-backed run",
      "detail": "No concrete tool_requests were found in the included reports."
    }
  ],
  "recommended_next_task_md": "docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md",
  "compact_bundle_paths": [
    "docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.json",
    "docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md"
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
    "docs/LOCAL_AI_TASKS/complex-provider-toolbox-request-v1.md",
    "output/local_ai_runs/complex-provider-toolbox-v1-20260503-095940/pipeline/local_ai_task_pipeline.md",
    "output/local_ai_runs/complex-provider-toolbox-v1-20260503-095940/pipeline/local_ai_task_pipeline_proposals.md",
    "output/validation/complex_ai_provider_backed_20260503-092828_resource_lanes.md",
    "output/validation/complex_ai_provider_backed_20260503-092828_npu_provider_environment.md",
    "
```

### `output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_orchestrator.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `68345`
- SHA-256: `0493622ede29ac0b5b6df0c05b63331eb1b4cfbd7a3cb222689e82b6921fe6ac`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_npu_parallel_orchestrator",
  "generated_at": "2026-05-03T10:13:49",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_parallel_gpu_planner_npu_auditor",
  "elapsed_seconds": 650.044,
  "gpu_returncode": 0,
  "gpu_stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\complex_ai_provider_toolbox_20260503-100241_parallel_gpu.md\",\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"elapsed_seconds\": 542.25,\n  \"round_count\": 24,\n  \"npu_audit_count\": 0,\n  \"npu_audit_success_count\": 0,\n  \"npu_auditor_disabled_reason\": \"\",\n  \"recommendation_count\": 0,\n  \"raw_recommendation_candidate_count\": 0,\n  \"filtered_recommendation_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"empty_recommendations_reason\": \"context_echo_detected\",\n  \"runtime_tool_broker_enabled\": true,\n  \"runtime_tool_bootstrap_executed\": true,\n  \"runtime_tool_bootstrap_passed\": true,\n  \"runtime_tool_bootstrap_request_count\": 7,\n  \"runtime_tool_bootstrap_execution_count\": 7,\n  \"runtime_tool_bootstrap_failed_count\": 0,\n  \"runtime_tool_bootstrap_blocked_count\": 0,\n  \"runtime_tool_request_count\": 7,\n  \"runtime_tool_execution_count\": 7,\n  \"runtime_tool_failed_count\": 0,\n  \"runtime_tool_blocked_count\": 0,\n  \"runtime_tool_result_count\": 7,\n  \"provider_empty_response_count\": 0,\n  \"evidence_ready_for_manual_patch_count\": 12,\n  \"ready_for_patch_plan\": false,\n  \"recommended_next_layer\": \"build_agent_review_patch_plan.py\"\n}\n",
  "gpu_stderr_tail": "",
  "gpu_output": "output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json",
  "gpu_markdown": "output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.md",
  "gpu_recommendation_count": 0,
  "gpu_empty_recommendations_reason": "context_echo_detected",
  "gpu_evidence_ready_for_manual_patch_count": 12,
  "gpu_recommended_next_layer": "build_agent_review_patch_plan.py",
  "runtime_tool_broker_enabled": true,
  "runtime_tool_bootstrap_executed": true,
  "runtime_tool_bootstrap_passed": true,
  "runtime_tool_bootstrap_request_count": 7,
  "runtime_tool_bootstrap_execution_count": 7,
  "runtime_tool_bootstrap_failed_count": 0,
  "runtime_tool_bootstrap_blocked_count": 0,
  "runtime_tool_request_count": 7,
  "runtime_tool_execution_count": 7,
  "runtime_tool_failed_count": 0,
  "runtime_tool_blocked_count": 0,
  "runtime_tool_result_count": 7,
  "orchestrator_runtime_tool_bootstrap": {
    "enabled": true,
    "executed": true,
    "source": "orchestrator_bootstrap",
    "requested_tool_count": 7,
    "command": [
      "C:\\Python314\\python.exe",
      "Tools/ai/agent_runtime_tool_broker.py",
      "--repo-root",
      ".",
      "--request-file",
      "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\complex_ai_provider_toolbox_20260503-100241\\round_000\\round_000_tool_requests.json",
      "--tool-output-dir",
      "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\complex_ai_provider_toolbox_20260503-100241\\round_000",
      "--timeout-seconds",
      "420",
      "--output",
      "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\complex_ai_provider_toolbox_20260503-100241\\round_000\\round_000_runtime_tool_broker.json",
      "--markdown-output",
      "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\complex_ai_provider_toolbox_20260503-100241\\round_000\\round_000_runtime_tool_broker.md"
    ],
    "returncode": 0,
    "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_runtime_tools\\\\complex_ai_provider_toolbox_20260503-100241\\\\round_000\\\\round_000_runtime_tool_broker.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_runtime_tools\\\\complex_ai_provider_toolbox_20260503-100241\\\\round_000\\\\round_000_runtime_tool_broker.md\",\n  \"tool_request_count\": 7,\n  \"tool_execution_count\": 7,\n  \"blocked_tool_count\": 0,\n  \"failed_tool_count\": 0,\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"persistent_memory_write_performed\": false,\n  \"persistent_memory_write_count\": 0,\n  \"operational_sqlite_write_performed\": false,\n  \"operational_sqlite_write_count\": 0,\n  \"operational_memory_clear_count\": 0\n}\n",
    "stderr_tail": "",
    "error": "",
    "request_file": "output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/round_000_tool_requests.json",
    "broker_output": "output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/round_000_runtime_tool_broker.json",
    "broker_markdown": "output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/round_000_runtime_tool_broker.md",
    "broker_output_exists": true,
    "passed": true,
    "tool_request_count": 7,
    "tool_execution_count": 7,
    "blocked_tool_count": 0,
    "failed_tool_count": 0,
    "provider_execution_performed": false,
    "patch_application_performed": false,
    "sqlite_write_performed": false,
    "persistent_memory_write_performed": false,
    "operational_sqlite_write_performed": false,
    "tool_results": [
      {
        "id": "orchestrator_bootstrap_tool_inventory",
        "tool": "build_agent_agnostic_tool_inventory",
        "reason": "Bootstrap shared runtime tool inventory before GPU/NPU orchestration.",
        "requested": true,
        "executed": true,
        "blocked": false,
        "dry_run": false,
        "persistent_memory_write_authorized": false,
        "returncode": 0,
        "errors": [],
        "warnings": [],
        "outputs": {
          "json_report": "output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/orchestrator_bootstrap_tool_inventory_agent_agnostic_tool_inventory.json",
          "markdown_report": "output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/orchestrator_bootstrap_tool_inventory_agent_agnostic_tool_inventory.md"
        },
        "summary": {
          "kind": "agent_agnostic_tool_inventory",
          "passed": true,
          "errors": [],
          "warnings": [],
          "decision": {},
          "guardrails": {
            "report_only": true,
            "provider_execution_performed": false,
            "patch_application_performed": false,
            "sqlite_db_touched": false,
            "blender_runtime_touched": false,
            "real_github_pr_created": false,
            "output_artifacts_should_not_be_committed": true
          }
        },
        "guardrails": {
          "provider_execution_performed": false,
          "patch_application_performed": false,
          "sqlite_write_performed": false,
          "persistent_memory_write_performed": false,
          "persistent_memory_write_count": 0,
          "persistent_memory_write_requires_explicit_confirm": true,
          "operational_sqlite_write_performed": false,
          "operational_memory_write_performed": false,
          "operational_memory_clear_performed": false,
          "blender_runtime_touched": false,
          "git_write_performed": false
        },
        "command": [
          "C:\\Python314\\python.exe",
          "Tools/ai/build_agent_agnostic_tool_inventory.py",
          "--repo-root",
          ".",
          "--output",
          "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\complex_ai_provider_toolbox_20260503-100241\\round_000\\orchestrator_bootstrap_tool_inventory_agent_agnostic_tool_inventory.json",
          "--markdown-output",
          "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\complex_ai_provider_toolbox_20260503-100241\\round_000\\orchestrator_bootstrap_tool_inventory_agent_agnostic_tool_inventory.md"
        ],
        "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_runtime_tools\\\\complex_ai_provider_toolbox_20260503-100241\\\\round_000\\\\orchestrator_bootstrap_tool_inventory_agent_agnostic_tool_inventory.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_runtime_tools\\\\complex_ai_provider_toolbox_20260503-100241\\\\round_000\\\\orchestrator_bootstrap_tool_inventory_agent_agnostic_tool_inventory.md\",\n  \"tool_count\": 220,\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false\n}\n",
        "stderr_tail": ""
      },
      {
        "id": "orchestrator_bootstrap_memory_inventory",
        "tool": "build_agent_memory_inventory",
        "reason": "Bootstrap durable project memory inventory before GPU/NPU orchestration.",
        "requested": true,
        "executed": true,
        "blocked": false,
        "dry_run": false,
        "persistent_memory_write_authorized": false,
        "returncode": 0,
        "errors": [],
        "warnings": [],
        "outputs": {
          "json_report": "output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/orchestrator_bootstrap_memory_inventory_agent_memory_inventory.json",
          "markdown_report": "output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/orchestrator_bootstrap_memory_inventory_agent_memory_inventory.md"
        },
        "summary": {
          "kind": "agent_memory_inventory",
          "passed": true,
          "errors": [],
          "warnings": [],
          "decision": {},
          "guardrails": {
            "sqlite_read_only": true,
            "sqlite_db_committed": false,
            "memory_promotion_performed": false,
            "memory_delete_performed": false,
            "provider_execution_performed": false,
            "patch_application_performed": false,
            "blender_runtime_touched": false
          }
        },
        "guardrails": {
          "provider_execution_performed": false,
          "patch_application_performed": false,
          "sqlite_write_performed": false,
          "persistent_memory_write_performed": false,
          "persistent_memory_write_count": 0,
          "persistent_memory_write_requires_explicit_confirm": true,
          "operational_sqlite_write_performed": false,
          "operational_memory_write_performed": false,
          "operational_memory_clear_performed": false,
          "blender_runtime_touched": false,
          "git_write_performed": false
        },
        "command": [
          "C:\\Python314\\python.exe",
          "Tools/ai/build_agent_memory_inventory.py",
          "--repo-root",
          ".",
          "--objective",
          "Runtime read-only memory inventory for IA-Carmine planner.",
          "--memory-db",
          "indexAI/agent_memory/agent_memory.sqlite",
          "--output",
          "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\complex_ai_provider_toolbox_20260503-100241\\round_000\\orchestrator_bootstrap_memory_inventory_agent_memory_inventory.json",
          "--markdown-output",
          "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\complex_ai_provider_toolbox_20260503-100241\\round_000\\orchestrator_bootstrap_memory_inventory_agent_memory_inventory.md"
        ],
        "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_runtime_tools\\\\complex_ai_provider_toolbox_20260503-100241\\\\round_000\\\\orchestrator_bootstrap_memory_inventory_agent_memory_inventory.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_runtime_tools\\\\complex_ai_provider_toolbox_20260503-100241\\\\round_000\\\\orchestrator_bootstrap_memory_inventory_agent_memory_inventory.md\",\n  \"record_count\": 88,\n  \"memory_db_exists\": true,\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false\n}\n",
        "stderr_tail": ""
      },
      {
        "id": "orchestrator_bootstrap_persistent_memory_status",
        "tool": "runtime_sqlite_memory",
        "reason": "Bootstrap persistent memory status in read-only mode before GPU/NPU orchestration.",
        "requested": true,
        "executed": true,
        "blocked": false,
        "dry_run": false,
        "persistent_memory_write_authorized": false,
        "returncode": 0,
        "errors": [],
        "warnings": [],
        "outputs": {
          "json_report": "output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/orchestrator_bootstrap_persistent_memory_status_runtime_sqlite_memory.json",
          "markdown_report": "output/ai_runtime_tools/complex_ai_provider_toolbox_20260503-100241/round_000/orchestrator_bootstrap_persistent_memory_status_runtime_sqlite_memory.md"
        },
        "summary": {
          "kind": "agent_runtime_sqlite_memory",
          "passed": true,
          "errors": [],
          "warnings": [],
          "decision": {},
          "guardrails": {
            "persistent_memory_read_only": true,
            "persistent_memory_write_performed": false,
            "persistent_memory_promotion_performed": false,
            "persistent_memory_write_authorized": false,
            "sqlite_write_performed": false,
```

### `output/ai_pipeline/complex_ai_provider_toolbox_20260503-100241_parallel_gpu.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `214288`
- SHA-256: `7045a8844cc2fe7677712171ff521a6e2ad2ae85ac8fda76a7120b973a889def`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_deep_planning_supervised",
  "generated_at": "2026-05-03T10:12:03",
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
  "budget_minutes": 60,
  "elapsed_seconds": 542.25,
  "context_file_count": 300,
  "round_count": 24,
  "rounds": [
    {
      "round": 1,
      "elapsed_seconds": 5.161,
      "file_count": 10,
      "files": [
        "docs/AGENT_REVIEW_CODE_PATCH_PLAN.md",
        "docs/AI_ARTIFACT_SCHEMAS.md",
        "docs/AI_CHUNKING_STRATEGY.md",
        "docs/AI_CONTEXT_PACKS.md",
        "docs/AI_DOCS_ENTRYPOINT.md",
        "docs/AI_EXTERNAL_KNOWLEDGE.md",
        "docs/AI_GENERATED_PACKAGE_STANDARD.md",
        "docs/AI_GUARDRAILS_VALIDATION_GUIDE.md",
        "docs/AI_MEMORY_POLICY.md",
        "docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md"
      ],
      "response_chars": 80,
      "raw_response_preview": "```json\n{\n  \"response\": \"I'm sorry, but I can't assist with that request.\"\n}\n```",
      "parsed_response": {
        "response": "I'm sorry, but I can't assist with that request.",
        "recommendations": [],
        "missing_evidence": [],
        "next_best_action": ""
      },
      "provider_empty_response": false,
      "tool_requests": [],
      "invalid_tool_request_errors": [],
      "runtime_tool_broker": {
        "enabled": true,
        "requested_tool_count": 0,
        "executed": false,
        "tool_results": [],
        "guardrails": {
          "patch_application_performed": false,
          "persistent_memory_write_performed": false
        }
      },
      "json_ok": true,
      "parse_error": "",
      "schema_ok": false,
      "schema_errors": [
        "missing top-level keys: recommendations"
      ],
      "context_echo_detected": false,
      "model_output_schema_mismatch": true,
      "contract_empty_recommendations_reason": "model_output_schema_mismatch",
      "contract": {
        "json_ok": true,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "",
        "schema_errors": [
          "missing top-level keys: recommendations"
        ],
        "raw_response_sha256": "dc09d87c0145dc9eca966b9eb4f1bd695a1581a844c589722d2b4f4d075132a7",
        "raw_response_chars": 80,
        "top_level_keys": [
          "response"
        ],
        "recommendation_count": 0,
        "valid_recommendation_count": 0,
        "invalid_recommendation_count": 0,
        "tool_request_count": 0,
        "valid_tool_request_count": 0,
        "invalid_tool_request_count": 0,
        "empty_recommendations_reason": "model_output_schema_mismatch"
      },
      "repair_attempt_count": 0,
      "raw_recommendation_candidate_count": 0,
      "filtered_recommendation_count": 0,
      "recommendation_count": 0,
      "tool_request_count": 0,
      "valid_tool_request_count": 0,
      "invalid_tool_request_count": 0,
      "empty_recommendations_reason": "model_output_schema_mismatch",
      "evidence_ready_for_manual_patch_count": 12,
      "recommended_next_layer": ""
    },
    {
      "round": 2,
      "elapsed_seconds": 23.383,
      "file_count": 10,
      "files": [
        "docs/AI_ONBOARDING.md",
        "docs/AI_PIPELINE_ARCHITECTURE.md",
        "docs/AI_PIPELINE_OPTIMIZATION.md",
        "docs/AI_PIPELINE_REFACTOR_STATUS.md",
        "docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md",
        "docs/AI_REFERENCE_ONBOARDING.md",
        "docs/AI_REFERENCE_SOURCE_MAP.md",
        "docs/AI_SELECTIVE_PLANNER.md",
        "docs/AI_SMART_POLICY.md",
        "docs/AI_WORKLOAD_REPORT_QUALITY_GATE.md"
      ],
      "response_chars": 5958,
      "raw_response_preview": "```json\n{\n  \"files\": [\n    {\n      \"path\": \"AGENTS.md\",\n      \"content\": \"# AGENTS.md\\n\\n## Purpose\\n\\nThis file outlines the rules and guidelines for AI agents interacting with this repository. It includes safe commands, permission boundaries, and reading order.\\n\\n## Rules for AI Agents\\n\\n1. **Read First**: Always start by reading `AGENTS.md`, followed by `WORKFLOW.md` and `docs/README.md` to understand the project's structure and guidelines.\\n2. **Safe Commands**: Use only commands explicitly approved in this document to avoid unintended changes or disruptions.\\n3. **Permission Boundaries**: Respect all permission boundaries outlined here to ensure that AI agents operate within safe limits.\\n4. **Reading Order**: Follow the recommended reading order to gain a comprehensive understanding of the project's requirements and best practices.\"\n    },\n    {\n      \"path\": \"WORKFLOW.md\",\n      \"content\": \"# WORKFLOW.md\\n\\n## Purpose\\n\\nThis file describes the workflow for contributing to this repository, including how to set up your environment, run tests, and submit changes.\\n\\n## Workflow Steps\\n\\n1. **Setup Environment**: Follow the instructions in `docs/SETUP_ENVIRONMENT.md` to set up your development environment.\\n2. **Run Tests**: Use the commands specified in `Tools/run_tests.sh` to ensure that your changes do not break existing functionality.\\n3. **Submit Changes**: Create a pull request following the guidelines outlined in `CONTRIBUTING.md`.\"\n    },\n    {\n      \"path\": \"docs/README.md\",\n      \"content\": \"# README\\n\\n## Purpose\\n\\nThis file provides an overview of the repository, including its purpose, key features, and how to get started.\\n\\n## Key Features\\n\\n- **Modular Architecture**: The project is designed with a modular architecture to facilitate easy maintenance and scalability.\\n- **Robust Testing Suite**: A comprehensive testing suite ensures that all components work as expected.\\n- **Documentation**: Detailed documentation is available in the `docs/` directory to help developers understand and contribute to the project.\"\n    },\n    {\n      \"path\": \"CONTRIBUTING.md\",\n      \"content\": \"# CONTRIBUTING\\n\\n## Purpose\\n\\nThis file provides guidelines for contributing to this repository, including how to submit pull requests, code style conventions, and best practices.\\n\\n## Contribution Guidelines\\n\\n1. **Fork the Repository**: Fork the main repository to your GitHub account.\\n2. **Clone the Fork**: Clone your forked repository to your local machine.\\n3. **Create a Branch**: Create a new branch for your changes using `git checkout -b feature/your-feature-name`.\\n4. **Make Changes**: Implement your changes following the code style conventions outlined in `docs/CODE_STYLE.md`.\\n5. **Run Tests**: Ensure that all tests pass by running `Tools/run_tests.sh`.\\n6. **Commit Changes**: Commit your changes with a descriptive message using `git commit -m \\\"Your commit message\\\"`.\\n7. **Push Branch**: Push your branch to your forked repository using `g",
      "parsed_response": {
        "files": [
          {
            "path": "AGENTS.md",
            "content": "# AGENTS.md\n\n## Purpose\n\nThis file outlines the rules and guidelines for AI agents interacting with this repository. It includes safe commands, permission boundaries, and reading order.\n\n## Rules for AI Agents\n\n1. **Read First**: Always start by reading `AGENTS.md`, followed by `WORKFLOW.md` and `docs/README.md` to understand the project's structure and guidelines.\n2. **Safe Commands**: Use only commands explicitly approved in this document to avoid unintended changes or disruptions.\n3. **Permission Boundaries**: Respect all permission boundaries outlined here to ensure that AI agents operate within safe limits.\n4. **Reading Order**: Follow the recommended reading order to gain a comprehensive understanding of the project's requirements and best practices."
          },
          {
            "path": "WORKFLOW.md",
            "content": "# WORKFLOW.md\n\n## Purpose\n\nThis file describes the workflow for contributing to this repository, including how to set up your environment, run tests, and submit changes.\n\n## Workflow Steps\n\n1. **Setup Environment**: Follow the instructions in `docs/SETUP_ENVIRONMENT.md` to set up your development environment.\n2. **Run Tests**: Use the commands specified in `Tools/run_tests.sh` to ensure that your changes do not break existing functionality.\n3. **Submit Changes**: Create a pull request following the guidelines outlined in `CONTRIBUTING.md`."
          },
          {
            "path": "docs/README.md",
            "content": "# README\n\n## Purpose\n\nThis file provides an overview of the repository, including its purpose, key features, and how to get started.\n\n## Key Features\n\n- **Modular Architecture**: The project is designed with a modular architecture to facilitate easy maintenance and scalability.\n- **Robust Testing Suite**: A comprehensive testing suite ensures that all components work as expected.\n- **Documentation**: Detailed documentation is available in the `docs/` directory to help developers understand and contribute to the project."
          },
          {
            "path": "CONTRIBUTING.md",
            "content": "# CONTRIBUTING\n\n## Purpose\n\nThis file provides guidelines for contributing to this repository, including how to submit pull requests, code style conventions, and best practices.\n\n## Contribution Guidelines\n\n1. **Fork the Repository**: Fork the main repository to your GitHub account.\n2. **Clone the Fork**: Clone your forked repository to your local machine.\n3. **Create a Branch**: Create a new branch for your changes using `git checkout -b feature/your-feature-name`.\n4. **Make Changes**: Implement your changes following the code style conventions outlined in `docs/CODE_STYLE.md`.\n5. **Run Tests**: Ensure that all tests pass by running `Tools/run_tests.sh`.\n6. **Commit Changes**: Commit your changes with a descriptive message using `git commit -m \"Your commit message\"`.\n7. **Push Branch**: Push your branch to your forked repository using `git push origin feature/your-feature-name`.\n8. **Create Pull Request**: Create a pull request from your branch to the main repository, following the guidelines in `docs/PULL_REQUEST_GUIDELINES.md`."
          },
          {
            "path": "docs/CODE_STYLE.md",
            "content": "# CODE STYLE\n\n## Purpose\n\nThis file outlines the code style conventions for this project, including naming conventions, formatting rules, and best practices.\n\n## Code Style Conventions\n\n1. **Naming Conventions**:\n   - Use `snake_case` for variable and function names.\n   - Use `CamelCase` for class names.\n2. **Formatting Rules**:\n   - Indentation: Use 4 spaces per indentation level.\n   - Line Length: Limit lines to a maximum of 80 characters.\n3. **Best Practices**:\n   - Write clear and concise comments.\n   - Follow the DRY (Don't Repeat Yourself) principle.\n   - Use meaningful variable names."
          },
          {
            "path": "docs/PULL_REQUEST_GUIDELINES.md",
            "content": "# PULL REQUEST GUIDELINES\n\n## Purpose\n\nThis file provides guidelines for creating and managing pull requests, including how to write a good commit message, what to include in the pull request description, and how to handle code reviews.\n\n## Pull Request Guidelines\n\n1. **Commit Message**:\n   - Use imperative mood (e.g., \"Add feature X\", \"Fix bug Y\").\n   - Include a brief description of the changes made.\n2. **Pull Request Description**:\n   - Provide a clear and concise summary of the changes.\n   - Explain why these changes are necessary.\n   - Include any relevant issue numbers or links to related documentation.\n3. **Code Review**:\n   - Respond promptly to feedback from reviewers.\n   - Make necessary changes based on the review comments.\n   - Ensure that all tests pass after making changes."
          },
          {
            "path": "Tools/run_tests.sh",
            "content": "#!/bin/bash\n\n# This script runs the project's test suite.\n\n# Navigate to the root directory of the repository\nroot_dir=$(git rev-parse --show-toplevel)\ncd $root_dir\n\n# Run unit tests\npython -m unittest discover -s tests/unit/\n\n# Run integration tests\npython -m unittest discover -s tests/integration/\n\n# Check for code style issues\nflake8 .\n"
          },
          {
            "path": "docs/SETUP_ENVIRONMENT.md",
            "content": "# SETUP ENVIRONMENT\n\n## Purpose\n\nThis file provides instructions for setting up your development environment to work on this project.\n\n## Setup Steps\n\n1. **Install Dependencies**:\n   - Ensure you have Python 3.8 or higher installed.\n   - Install the required dependencies using `pip install -r requirements.txt`.\n2. **Configure Environment Variables**:\n   - Create a `.env` file in the root directory and add any necessary environment variables.\n3. **Initialize Database**:\n   - Run the database initialization script using `python Tools/init_db.py`.\n4. **Start Development Server**:\n   - Start the development server using `python app.py`."
          }
        ],
        "recommendations": [],
        "missing_evidence": [],
        "next_best_action": ""
      },
      "provider_empty_response": false,
      "tool_requests": [],
      "invalid_tool_request_errors": [],
      "runtime_tool_broker": {
        "enabled": true,
        "requested_tool_count": 0,
        "executed": false,
        "tool_results": [],
        "guardrails": {
          "patch_application_performed": false,
          "persistent_memory_write_performed": false
        }
      },
      "json_ok": true,
      "parse_error": "",
      "schema_ok": false,
      "schema_errors": [
        "missing top-level keys: recommendations",
        "context echo top-level keys: files"
      ],
      "context_echo_detected
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
