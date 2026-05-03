# Local Validation Evidence Bundle

- Generated at: `2026-05-03T08:32:06`
- Kind: `github_validation_evidence_bundle`

## Decision summary
- `ollama_gpu_primary_advisory`: `False`
- `npu_excluded_when_unusable`: `False`
- `provider_execution_seen`: `True`
- `npu_decode_smoke_passed`: `False`
- `selected_chunks_evidence_seen`: `True`
- `selected_chunks_built`: `True`
- `budget_respected`: `True`
- `artifact_manifest_built`: `True`
- `included_artifacts_built`: `True`
- `included_artifact_count`: `16`
- `patch_plan_summary_seen`: `False`

## Reports

### `output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_agnostic_tool_inventory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/shared_toolbox_refactor_python_line_count_20260503-082504.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_line_count_csv`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/shared_toolbox_refactor_code_interpreter_20260503-082504.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_interpreter_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `109`

### `output/validation/shared_toolbox_refactor_python_syntax_20260503-082504.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/validation/shared_toolbox_refactor_bundle_smoke_20260503-082504.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `shared_toolbox_ai_to_ai_bundle_smoke`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`

### `output/validation/shared_toolbox_refactor_memory_routing_20260503-082504.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_memory_routing_policy`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/shared_toolbox_refactor_duplication_audit_20260503-082504.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `shared_toolbox_refactor_duplication_audit`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Warnings: `['provider_execution_performed=True in bundle smoke is inherited from fake smoke inputs and is not a real provider execution.']`

### `output/analysis/shared_toolbox_ai_to_ai_final_summary_20260503-082504.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `shared_toolbox_ai_to_ai_final_summary`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['provider_execution_performed=True in bundle smoke is inherited from fake smoke inputs and is not a real provider execution.']`

## Artifact manifest

- `output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json` exists=`True` size=`452835` suffix=`.json` preview_chars=`1500`
- `output/validation/shared_toolbox_refactor_python_line_count_20260503-082504.json` exists=`True` size=`3138` suffix=`.json` preview_chars=`1500`
- `output/analysis/shared_toolbox_refactor_code_interpreter_20260503-082504.json` exists=`True` size=`1066899` suffix=`.json` preview_chars=`1500`
- `output/validation/shared_toolbox_refactor_python_syntax_20260503-082504.json` exists=`True` size=`34011` suffix=`.json` preview_chars=`1500`
- `output/validation/shared_toolbox_refactor_bundle_smoke_20260503-082504.json` exists=`True` size=`22593` suffix=`.json` preview_chars=`1500`
- `output/validation/shared_toolbox_refactor_memory_routing_20260503-082504.json` exists=`True` size=`7349` suffix=`.json` preview_chars=`1500`
- `output/analysis/shared_toolbox_refactor_duplication_audit_20260503-082504.json` exists=`True` size=`13614` suffix=`.json` preview_chars=`1500`
- `output/analysis/shared_toolbox_ai_to_ai_final_summary_20260503-082504.json` exists=`True` size=`282274` suffix=`.json` preview_chars=`1500`

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

### `docs/LOCAL_AI_TASKS/shared-toolbox-refactor-duplication-audit-next-task-2026-05-03.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `10628`
- SHA-256: `05534702d8de822e0e81d8d7697ba857b7f652ddaa5764ad16845f68dd249d5e`
- Content included: `True`
- Content truncated: `False`

```text
# Shared Toolbox Refactor Duplication Audit Next Task — 2026-05-03

## Purpose

Use this Markdown as the next concrete AI-to-AI task for the local IA-Carmine pipeline after PR #142.

The goal is to return to the main shared-toolbox implementation work and verify whether the current tooling code contains repeated logic that should be reused, promoted, or refactored before adding more runtime tools.

This is a task request, not a patch instruction. The local IA must produce evidence, recommendations and optional manual-review patch-plan targets only.

## Repository baseline

```text
repository: C-F-tek/blender-audio-project
branch to sync: master
current reference commit: 4cfabf0 feat(ai): add shared toolbox AI-to-AI bundle builder
project: IA-Carmine
workflow: ChatGPT -> MD task -> local IA -> reports/bundle -> ChatGPT review -> manual PR only if approved
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
HEAD is master/origin/master at or after 4cfabf0
```

## Read first

Read these files before planning:

```text
docs/LOCAL_AI_TASKS/shared-runtime-toolbox-orchestration-architecture.md
docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md
docs/LOCAL_AI_TASKS/full-memory-tool-regeneration-procedure.md
docs/LOCAL_AI_TASKS/project-complete-ai-to-ai-procedure.md
Tools/ai/agent_runtime_tool_broker.py
Tools/ai/build_agent_agnostic_tool_inventory.py
Tools/ai/build_github_evidence_bundle.py
Tools/ai/github_evidence_bundle_artifacts.py
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py
Tools/validation/run_shared_toolbox_ai_to_ai_bundle_smoke.py
```

## Architectural rule

Preserve this design rule:

```text
Providers ask.
Orchestrator decides.
Broker executes.
Reports become evidence.
```

The AI must not turn providers into executors and must not put orchestration or broker execution policy inside summary/bundle builders.

## Main objective

Audit the shared-toolbox implementation after PR #142 and answer:

```text
1. Are there duplicated helper functions or repeated logic across Tools/ai and Tools/validation?
2. Which repeated logic should reuse existing helpers?
3. Which local functions should be promoted to existing shared modules?
4. Which repeated logic is intentionally local and should not be refactored?
5. Did PR #142 keep chunking/artifact policy in the shared evidence-bundle layer rather than duplicating it in the shared-toolbox builder?
6. What is the next safe manual-review refactor target, if any?
```

## Mandatory duplication/refactor audit

The local IA must explicitly inspect repeated code, not only file size.

Check for repeated implementations of:

```text
repo-relative path helpers
path resolving helpers
JSON read/write helpers
Markdown rendering helpers
line-count helpers
artifact discovery helpers
chunk/pointer generation helpers
report-only guardrail blocks
CLI argument patterns
validation command generation
runtime tool request packet construction
broker output summarization
```

For every duplication candidate, return:

```text
candidate_id
repeated_logic
files_involved
existing_helper_available
preferred_existing_helper_or_module
recommendation_type
risk
schema_or_cli_impact
validation_required
manual_review_required
```

Allowed `recommendation_type` values:

```text
reuse_existing_helper
promote_existing_function
extract_new_shared_helper
keep_local_by_design
advisory_only
needs_more_context
```

Do not classify anything as ready for implementation unless the target seam is small, the helper destination is clear, and CLI/report schemas can be preserved.

## Refactor verification requirements

Verify the current refactor state using evidence, not intuition:

```text
- compare current touched files from PR #142 against the intended layering
- confirm build_shared_toolbox_ai_to_ai_bundle.py delegates bundle assembly to build_github_evidence_bundle.py
- confirm recursive discovery/chunking belongs to github_evidence_bundle_artifacts.py and/or shared evidence-bundle helpers
- confirm check_github_evidence_bundle remains the validation layer
- confirm run_shared_toolbox_ai_to_ai_bundle_smoke.py covers final summary, bundle validation, recursive discovery and chunk pointers
- identify any remaining large or repeated helpers that should move to report_utils.py, github_evidence_bundle_io.py, github_evidence_bundle_artifacts.py, or an existing local helper module
```

## Guardrails

This task is report-only unless the user explicitly asks for a later implementation PR.

Do not:

```text
execute providers
apply patches automatically
run Blender runtime
write persistent SQLite memory
commit output/**
commit *.db or *.sqlite
change provider/model settings
rewrite prompts broadly
merge to master
```

Allowed outputs are JSON/Markdown/CSV reports under `output/**` and compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/**` only when explicitly selected for review.

## Required tool/evidence run

Start with agnostic and static evidence:

```powershell
python .\Tools\ai\build_agent_agnostic_tool_inventory.py `
  --repo-root . `
  --output ".\output\ai_pipeline\shared_toolbox_refactor_agnostic_tool_inventory_$Stamp.json" `
  --markdown-output ".\output\ai_pipeline\shared_toolbox_refactor_agnostic_tool_inventory_$Stamp.md"

python .\Tools\validation\build_python_line_count_csv.py `
  --repo-root . `
  --timestamped `
  --report-output ".\output\validation\shared_toolbox_refactor_python_line_count_$Stamp.json" `
  --markdown-output ".\output\validation\shared_toolbox_refactor_python_line_count_$Stamp.md"

python -m Tools.ai.build_code_interpreter_report `
  --repo-root . `
  --input Tools/ai `
  --input Tools/validation `
  --input Tools/workflow `
  --input Tools/npu `
  --output ".\output\analysis\shared_toolbox_refactor_code_interpreter_$Stamp.json" `
  --markdown-output ".\output\analysis\shared_toolbox_refactor_code_interpreter_$Stamp.md"

python -m Tools.validation.check_python_syntax `
  --repo-root . `
  --output ".\output\validation\shared_toolbox_refactor_python_syntax_$Stamp.json"
```

Validate PR #142 smoke coverage still passes on master:

```powershell
python .\Tools\validation\run_shared_toolbox_ai_to_ai_bundle_smoke.py `
  --repo-root . `
  --output ".\output\validation\shared_toolbox_refactor_bundle_smoke_$Stamp.json" `
  --markdown-output ".\output\validation\shared_toolbox_refactor_bundle_smoke_$Stamp.md"
```

Optional, use the memory routing policy as request planning evidence only:

```powershell
python .\Tools\ai\agent_memory_routing_policy.py `
  --repo-root . `
  --objective "Audit shared toolbox duplicated code and verify refactoring after PR142." `
  --profile full_refactor `
  --output ".\output\validation\shared_toolbox_refactor_memory_routing_$Stamp.json" `
  --markdown-output ".\output\validation\shared_toolbox_refactor_memory_routing_$Stamp.md"
```

## Required final AI report

The local IA must produce a final report with this structure:

```text
output/analysis/shared_toolbox_refactor_duplication_audit_<STAMP>.json
output/analysis/shared_toolbox_refactor_duplication_audit_<STAMP>.md
```

Required JSON fields:

```text
schema_version
kind = shared_toolbox_refactor_duplication_audit
passed
provider_execution_performed
patch_application_performed
sqlite_write_performed
persistent_memory_write_performed
refactor_verification
duplication_candidates
helper_reuse_recommendations
manual_review_patch_plan_candidates
advisory_only_findings
validation_commands
stop_conditions
errors
warnings
```

`refactor_verification` must include:

```text
layering_preserved
builder_delegates_to_common_bundle
chunking_in_common_evidence_layer
validator_reused
smoke_coverage_present
cli_schema_preserved
report_schema_preserved
```

`duplication_candidates` must not be empty unless the report explains why no duplicated or repeated logic was found.

## Evidence bundle command

Use the post-PR142 builder instead of manual final-summary PowerShell:

```powershell
python -m Tools.ai.build_shared_toolbox_ai_to_ai_bundle `
  --repo-root . `
  --stamp $Stamp `
  --basename "shared_toolbox_refactor_duplication_audit_bundle_$Stamp" `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report ".\output\ai_pipeline\shared_toolbox_refactor_agnostic_tool_inventory_$Stamp.json" `
  --report ".\output\validation\shared_toolbox_refactor_python_line_count_$Stamp.json" `
  --report ".\output\analysis\shared_toolbox_refactor_code_interpreter_$Stamp.json" `
  --report ".\output\validation\shared_toolbox_refactor_python_syntax_$Stamp.json" `
  --report ".\output\validation\shared_toolbox_refactor_bundle_smoke_$Stamp.json" `
  --report ".\output\analysis\shared_toolbox_refactor_duplication_audit_$Stamp.json" `
  --artifact ".\docs\LOCAL_AI_TASKS\shared-toolbox-refactor-duplication-audit-next-task-2026-05-03.md" `
  --artifact ".\output\analysis\shared_toolbox_refactor_code_interpreter_$Stamp.md" `
  --artifact ".\output\analysis\shared_toolbox_refactor_duplication_audit_$Stamp.md" `
  --validate-bundle
```

The builder may recursively include stamped `.json`/`.md` evidence and should expose chunk pointers for large files. Do not commit raw `output/**` artifacts.

## Stop conditions

Stop and report if any occur:

```text
python syntax validation fails
shared toolbox bundle smoke fails
provider_execution_performed=True during no-provider validation reports
patch_application_performed=True
sqlite_write_performed=True outside explicitly authorized operational scratch semantics
persistent_memory_write_performed=True
refactor recommendation requires CLI/report schema break without migration plan
bundle cannot be built or validated
```

## Commit policy

For this task, the default result is evidence only.

Allowed commit candidates, only if explicitly preparing an evidence PR:

```text
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_refactor_duplication_audit_bundle_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_refactor_duplication_audit_bundle_<STAMP>.md
```

Never commit:

```text
output/**
renders/**
*.db
*.sqlite
```

## Expected final answer back to ChatGPT

Return:

```text
1. whether duplicated/repeated code exists
2. top duplication/refactor candidates
3. whether PR #142 layering remains correct
4. recommended next manual-review patch target or advisory_only
5. compact bundle paths
6. exact validation commands executed
7. guardrail booleans
```

```

### `output/analysis/shared_toolbox_refactor_code_interpreter_20260503-082504.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7315`
- SHA-256: `285688c746174c90db2ab96a82b82608e31a9056452824d77bba37ad54abf217`
- Content included: `True`
- Content truncated: `False`

```text
# Static Code Interpreter Report

- Passed: `True`
- File count: `203`
- Parsed files: `203`
- Total lines: `56304`
- Total functions: `2115`
- Total classes: `70`
- Risk signals: `39`
- TODO/FIXME markers: `21`
- Recommendation count: `109`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Largest files

- `Tools/npu/run_dual_ai_pipeline.py` — `1773` lines, risk `high`
- `Tools/workflow/workflow_state.py` — `1230` lines, risk `high`
- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` — `888` lines, risk `high`
- `Tools/ai/run_agent_gpu_deep_planning_supervised.py` — `814` lines, risk `high`
- `Tools/ai/run_agent_gpu_deep_planning_review.py` — `812` lines, risk `high`
- `Tools/workflow/gui/workflow_gui.py` — `738` lines, risk `medium`
- `Tools/npu/build_music_context.py` — `711` lines, risk `medium`
- `Tools/ai/agent_runtime_tool_broker.py` — `673` lines, risk `medium`
- `Tools/npu/run_npu_review.py` — `631` lines, risk `medium`
- `Tools/validation/check_npu_pipeline_modules.py` — `627` lines, risk `medium`
- `Tools/ai/build_selective_execution_plan.py` — `618` lines, risk `medium`
- `Tools/workflow/workflow_debug.py` — `607` lines, risk `medium`
- `Tools/ai/run_npu_gpu_deep_review_auditor.py` — `606` lines, risk `medium`
- `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` — `604` lines, risk `medium`
- `Tools/ai/build_repository_change_proposals.py` — `582` lines, risk `medium`
- `Tools/ai/build_ai_context_pack.py` — `575` lines, risk `medium`
- `Tools/ai/run_pipeline_dry_run_matrix.py` — `573` lines, risk `medium`
- `Tools/ai/build_agent_review_patch_plan.py` — `562` lines, risk `medium`
- `Tools/ai/suggest_repository_updates.py` — `551` lines, risk `medium`
- `Tools/ai/agent_state.py` — `544` lines, risk `medium`

## Recommendations

- `code_static_001` `Tools/ai/agent_memory_policy.py` risk `medium`: complex functions detected
- `code_static_002` `Tools/ai/agent_memory_routing_policy.py` risk `medium`: medium-size Python module, large functions detected
- `code_static_003` `Tools/ai/agent_runtime_sqlite_memory.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_004` `Tools/ai/agent_runtime_tool_broker.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected, static risk calls detected
- `code_static_005` `Tools/ai/agent_state.py` risk `medium`: medium-size Python module
- `code_static_006` `Tools/ai/analyze_gpu_npu_run_sync.py` risk `medium`: complex functions detected
- `code_static_007` `Tools/ai/build_agent_agnostic_tool_inventory.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_008` `Tools/ai/build_agent_memory_inventory.py` risk `medium`: large functions detected
- `code_static_009` `Tools/ai/build_agent_review_code_patch_plan.py` risk `medium`: medium-size Python module
- `code_static_010` `Tools/ai/build_agent_review_patch_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_011` `Tools/ai/build_ai_context_pack.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_012` `Tools/ai/build_code_interpreter_report.py` risk `medium`: medium-size Python module, TODO/FIXME markers detected
- `code_static_013` `Tools/ai/build_dry_run_matrix_evidence_bundle.py` risk `medium`: complex functions detected
- `code_static_014` `Tools/ai/build_full_context_golden_proposals.py` risk `medium`: large functions detected
- `code_static_015` `Tools/ai/build_github_evidence_bundle.py` risk `medium`: large functions detected
- `code_static_016` `Tools/ai/build_local_ai_enrichment_plan.py` risk `medium`: large functions detected
- `code_static_017` `Tools/ai/build_music_intermediates.py` risk `medium`: large functions detected, complex functions detected
- `code_static_018` `Tools/ai/build_patch_specs_from_proposals.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_019` `Tools/ai/build_repository_change_proposals.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_020` `Tools/ai/build_selective_execution_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_021` `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_022` `Tools/ai/build_workload_quality_lane_routing.py` risk `medium`: complex functions detected
- `code_static_023` `Tools/ai/check_local_resource_lanes.py` risk `medium`: complex functions detected
- `code_static_024` `Tools/ai/check_npu_provider_environment.py` risk `medium`: large functions detected, complex functions detected, static risk calls detected
- `code_static_025` `Tools/ai/github_evidence_bundle_artifacts.py` risk `medium`: complex functions detected
- `code_static_026` `Tools/ai/gpu_planner_json_contract.py` risk `medium`: complex functions detected
- `code_static_027` `Tools/ai/model_json.py` risk `medium`: complex functions detected
- `code_static_028` `Tools/ai/pipeline/preflight.py` risk `medium`: complex functions detected
- `code_static_029` `Tools/ai/pipeline/remediation.py` risk `medium`: large functions detected, complex functions detected, TODO/FIXME markers detected
- `code_static_030` `Tools/ai/pipeline/steps.py` risk `medium`: large functions detected
- `code_static_031` `Tools/ai/promote_patch_spec_draft.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_032` `Tools/ai/refine_megalithic_review_signals.py` risk `medium`: medium-size Python module
- `code_static_033` `Tools/ai/review_wave_entrypoints.py` risk `medium`: large functions detected, complex functions detected
- `code_static_034` `Tools/ai/run_agent_gpu_deep_planning_review.py` risk `high`: large Python module, large functions detected, complex functions detected
- `code_static_035` `Tools/ai/run_agent_gpu_deep_planning_supervised.py` risk `high`: large Python module, large functions detected, complex functions detected, static risk calls detected
- `code_static_036` `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` risk `high`: large Python module, large functions detected, complex functions detected, static risk calls detected
- `code_static_037` `Tools/ai/run_local_provider_probe.py` risk `medium`: complex functions detected
- `code_static_038` `Tools/ai/run_megalithic_repo_review.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_039` `Tools/ai/run_npu_decode_smoke_diagnostic.py` risk `medium`: large functions detected, complex functions detected, static risk calls detected
- `code_static_040` `Tools/ai/run_npu_gpu_deep_review_auditor.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected, static risk calls detected

## Guardrail

This is static interpretation only. It does not execute repository code or apply changes.

```

### `output/analysis/shared_toolbox_refactor_duplication_audit_20260503-082504.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3175`
- SHA-256: `0f7df7fb4c724325311515934fcd27ec50f3e5e143f7b175e8c100f3dc1ce752`
- Content included: `True`
- Content truncated: `False`

```text
# Shared Toolbox Refactor Duplication Audit

- Stamp: 20260503-082504
- Passed: True
- Provider execution performed: False
- Patch application performed: False
- SQLite write performed: False
- Persistent memory write performed: False

## Refactor verification

- Count: 8
- IsReadOnly: False
- Keys: layering_preserved builder_delegates_to_common_bundle chunking_in_common_evidence_layer validator_reused smoke_coverage_present cli_schema_preserved report_schema_preserved notes
- Values: True True True True True True True System.Object[]
- IsFixedSize: False
- SyncRoot: System.Object
- IsSynchronized: False

## Duplication candidates

### dup_path_helpers

- repeated_logic: Repository-relative and path resolution helper patterns appear in multiple Tools/ai and Tools/validation modules.
- recommendation_type: reuse_existing_helper
- preferred_existing_helper_or_module: Tools.ai.github_evidence_bundle_io for evidence-bundle paths; Tools.validation.report_utils for validation output paths.
- risk: medium
- schema_or_cli_impact: none expected if imports are changed carefully.

### dup_json_markdown_writers

- repeated_logic: JSON/Markdown write helpers are repeated across smoke, broker, inventory and bundle scripts.
- recommendation_type: promote_existing_function
- preferred_existing_helper_or_module: Tools.validation.report_utils.write_json_report and resolve_output_path.
- risk: low
- schema_or_cli_impact: none if output formatting remains JSON indent=2 UTF-8.

### dup_markdown_rendering

- repeated_logic: Markdown renderers are local by design in many reports but share repeated guardrail/status sections.
- recommendation_type: keep_local_by_design
- preferred_existing_helper_or_module: Potential future helper in Tools.validation.report_utils, but keep local unless repeated sections become schema-stable.
- risk: low
- schema_or_cli_impact: none

### dup_tool_request_packet_logic

- repeated_logic: Runtime tool request packet construction appears in memory routing and orchestrator/broker flow.
- recommendation_type: advisory_only
- preferred_existing_helper_or_module: Advisory: consider a future shared request-packet helper only after schema stabilizes further.
- risk: medium
- schema_or_cli_impact: possible schema impact; do not refactor automatically.

## Manual-review patch-plan candidates

- patch_plan_report_utils_json_write_reuse: Replace local JSON write helpers in selected smoke/report scripts with report_utils.write_json_report.

## Source report summary

- Count: 12
- IsReadOnly: False
- Keys: python_syntax_passed python_line_count_passed python_file_count python_total_lines code_interpreter_passed bundle_smoke_passed bundle_validation_passed memory_routing_passed memory_tool_request_count chunked_file_count recursive_discovered_report_count recursive_discovered_artifact_count
- Values: True True 291 83302 True True True True  6 8 12
- IsFixedSize: False
- SyncRoot: System.Object
- IsSynchronized: False

## Warnings

- provider_execution_performed=True in bundle smoke is inherited from fake smoke inputs and is not a real provider execution.

```

### `output/validation/shared_toolbox_refactor_all_python_files_20260503-082504.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `16462`
- SHA-256: `c5ec64fdc06304dd8300b1de61a4f89a5f4563af82cb3b408a450dd18c1b8d52`
- Content included: `True`
- Content truncated: `True`

```text
# Full Python Line Count Inventory

- Stamp: 20260503-082504
- CSV: docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260503-082516.csv
- File count: 291
- Total Python lines: 83302
- Visibility rule: all counted Python files are listed below; do not truncate to top 10/top 20.

| Lines | File |
|---:|---|
| 2197 | `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py` |
| 1773 | `Tools/npu/run_dual_ai_pipeline.py` |
| 1513 | `old script legacy/spaziotempo_asset_visual_v61.py` |
| 1262 | `Scripting/v61b/scene_tuning_panel.py` |
| 1230 | `Tools/workflow/workflow_state.py` |
| 1174 | `old script legacy/spaziotempo_asset_visual_v6.py` |
| 1097 | `Scripting/v61b_backgood/scene_tuning_panel.py` |
| 1079 | `Scripting/v61b/animation.py` |
| 1019 | `Scripting/v61b_backgood/animation.py` |
| 969 | `old script legacy/spaziotempo_album_visual_v5.py` |
| 888 | `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` |
| 814 | `Tools/ai/run_agent_gpu_deep_planning_supervised.py` |
| 812 | `Tools/ai/run_agent_gpu_deep_planning_review.py` |
| 738 | `Tools/workflow/gui/workflow_gui.py` |
| 737 | `Scripting/v61b/physics_setup.py` |
| 725 | `Scripting/v61b_backgood/asset_setup.py` |
| 725 | `Scripting/v61b/asset_setup.py` |
| 720 | `Scripting/v61b_backgood/physics_setup.py` |
| 711 | `Tools/npu/build_music_context.py` |
| 710 | `old script legacy/spaziotempo_album_visual_v3.py` |
| 673 | `Tools/ai/agent_runtime_tool_broker.py` |
| 657 | `Scripting/v61b/materials.py` |
| 631 | `Tools/npu/run_npu_review.py` |
| 627 | `Tools/validation/check_npu_pipeline_modules.py` |
| 618 | `Tools/ai/build_selective_execution_plan.py` |
| 607 | `Tools/workflow/workflow_debug.py` |
| 606 | `Tools/ai/run_npu_gpu_deep_review_auditor.py` |
| 604 | `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` |
| 582 | `Tools/ai/build_repository_change_proposals.py` |
| 575 | `Tools/ai/build_ai_context_pack.py` |
| 573 | `Tools/ai/run_pipeline_dry_run_matrix.py` |
| 562 | `Tools/ai/build_agent_review_patch_plan.py` |
| 554 | `Scripting/v61b/atmosphere_setup.py` |
| 551 | `Tools/ai/suggest_repository_updates.py` |
| 544 | `Tools/ai/agent_state.py` |
| 543 | `Scripting/v61b_backgood/atmosphere_setup.py` |
| 527 | `Tools/ai/agent_runtime_sqlite_memory.py` |
| 519 | `Tools/ai/run_megalithic_repo_review.py` |
| 513 | `Scripting/v61b_backgood/materials.py` |
| 499 | `Tools/ai/build_agent_review_code_patch_plan.py` |
| 497 | `Tools/validation/ai_pipeline_report_contracts.py` |
| 490 | `Tools/npu/npu_guardrail_service.py` |
| 489 | `Tools/ai/refine_megalithic_review_signals.py` |
| 487 | `Tools/validation/run_agent_review_patch_plan_full_validation.py` |
| 483 | `Tools/validation/run_agnostic_ai_tools_smoke_matrix.py` |
| 469 | `normalize_scene_spec.py` |
| 455 | `Tools/ai/agent_memory_routing_policy.py` |
| 446 | `Tools/validation/check_reviewed_patch_specs.py` |
| 443 | `Tools/repo_patch_runner/apply_repo_mods.py` |
| 442 | `Tools/ai/promote_patch_spec_draft.py` |
| 439 | `Scripting/v61b/config.py` |
| 437 | `Tools/ai/build_code_interpreter_report.py` |
| 436 | `Tools/npu/build_project_ai_index.py` |
| 425 | `Tools/validation/check_ai_context_pack_contract.py` |
| 422 | `Tools/workflow/gui/components/storage_dashboard.py` |
| 422 | `Tools/npu/ollama_runtime.py` |
| 419 | `Tools/workflow/scene_brief.py` |
| 414 | `Tools/ai/build_patch_specs_from_proposals.py` |
| 408 | `Tools/ai/build_agent_agnostic_tool_inventory.py` |
| 402 | `Tools/npu/build_npu_code_context.py` |
| 401 | `Tools/validation/check_github_evidence_bundle.py` |
| 400 | `Tools/validation/check_patch_spec_drafts.py` |
| 399 | `Scripting/v61b/encode_ffmpeg_v61b.py` |
| 398 | `Tools/ai/build_dry_run_matrix_evidence_bundle.py` |
| 397 | `Tools/ai/build_agent_memory_inventory.py` |
| 395 | `Scripting/v61b_backgood/hotpatch/hero_material_patch.py` |
| 395 | `Scripting/v61b/hotpatch/hero_material_patch.py` |
| 395 | `Scripting/v61b/encode_image_sequence_v61b.py` |
| 394 | `Tools/ai/build_agent_review_evidence_sufficiency.py` |
| 392 | `Tools/validation/check_code_contract_drift.py` |
| 392 | `Tools/ai/build_full_context_golden_proposals.py` |
| 392 | `Scripting/v61b/fog_dynamics.py` |
| 390 | `Tools/workflow/gui/components/artifact_browser.py` |
| 387 | `Tools/ai/gpu_planner_json_contract.py` |
| 376 | `Scripting/v61b_backgood/encode_image_sequence_v61b.py` |
| 369 | `Tools/npu/generated_blender_script_candidate_FristNear.py` |
| 369 | `Tools/npu/generated_blender_script_candidate.py` |
| 369 | `indexAI/scene_scripts/lll_luca_vera_master_scene_builder_candidate.py` |
| 366 | `Tools/validation/check_repository_change_proposals.py` |
| 359 | `Tools/validation/test_npu_pipeline_helpers.py` |
| 358 | `Scripting/v61b_backgood/config.py` |
| 357 | `Tools/ai/build_local_ai_enrichment_plan.py` |
| 355 | `Tools/npu/build_ai_service_packet.py` |
| 353 | `Tools/workflow/project_awareness.py` |
| 341 | `Tools/validation/check_ai_dry_run_matrix_contract.py` |
| 339 | `Tools/validation/check_selected_semantic_chunks.py` |
| 335 | `Tools/ai/check_local_resource_lanes.py` |
| 331 | `Tools/validation/apply_docs_contract_drift_fixes.py` |
| 327 | `Tools/npu/build_npu_knowledge_broker_packet.py` |
| 326 | `Tools/npu/build_blender_manual_context.py` |
| 325 | `Tools/validation/run_shared_toolbox_ai_to_ai_bundle_smoke.py` |
| 324 | `Tools/workflow/workflow_shell.py` |
| 321 | `Tools/validation/check_dry_run_matrix_evidence_bundle.py` |
| 319 | `Tools/workflow/gui/workflow_gui_modern.py` |
| 317 | `Tools/validation/check_local_ai_adapter_manifest.py` |
| 315 | `Tools/ai/github_evidence_bundle_artifacts.py` |
| 314 | `Tools/ai/run_npu_decode_smoke_diagnostic.py` |
| 314 | `Tools/ai/build_music_intermediates.py` |
| 307 | `Tools/validation/check_full_context_golden_proposals.py` |
| 307 | `Tools/ai/agent_memory_policy.py` |
| 304 | `Tools/ai/build_analysis_input_bundle.py` |
| 301 | `Scripting/v61b/hotpatch/accent_patch.py` |
| 297 | `Tools/npu/pipeline/providers.py` |
| 291 | `Tools/ai/select_semantic_code_chunks.py` |
| 290 | `Tools/validation/check_ai_pipeline_modules.py` |
| 286 | `Tools/ai/build_gpu_repair_failure_recommendation.py` |
| 286 | `Scripting/v61b/hotpatch/diagnostics.py` |
| 284 | `Tools/workflow/startup_check.py` |
| 283 | `Tools/validation/run_agent_review_patch_plan_smoke.py` |
| 283 | `Tools/ai/build_agent_transient_request_context.py` |
| 278 | `Tools/workflow/gui/components/session_overview.py` |
| 273 | `Tools/ai/analyze_gpu_npu_run_sync.py` |
| 272 | `Tools/validation/run_gpu_planner_json_contract_smoke.py` |
| 270 | `Tools/validation/check_full_context_golden_docs_contract.py` |
| 270 | `Scripting/v61b/render_setup.py` |
| 267 | `Tools/workflow/ai_runtime_diagnostics.py` |
| 267 | `Scripting/v61b_backgood/render_setup.py` |
| 266 | `Tools/ai/build_code_patch_docs_followup.py` |
| 260 | `Tools/validation/check_ai_workload_report_quality.py` |
| 259 | `Tools/validation/check_docs_contract_drift.py` |
| 258 | `Tools/ai/build_code_patch_artifact_pack.py` |
| 257 | `analyze_wav.py` |
| 256 | `Tools/validation/run_agnostic_context_stack_smoke.py` |
| 250 | `Tools/ai/build_code_edit_proposal_from_plan.py` |
| 247 | `Tools/validation/run_gpu_runtime_tool_bootstrap_smoke.py` |
| 245 | `Tools/ai/build_megalithic_review_pr_draft.py` |
| 244 | `Tools/validation/run_agent_runtime_tool_broker_smoke.py` |
| 240 | `Tools/ai/review_wave_entrypoints.py` |
| 240 | `Scripting/v61b_backgood/fog_dynamics.py` |
| 238 | `Tools/validation/check_selective_execution_plan.py` |
| 238 | `Tools/npu/run_ollama_music_agent.py` |
| 234 | `Tools/validation/run_agent_memory_routing_policy_smoke.py` |
| 232 | `Tools/ai/smart_ai_gatekeeper.py` |
| 232 | `Tools/ai/replay_gpu_planner_json_contract.py` |
| 231 | `Tools/ai/enrich_github_evidence_bundle_code_plan.py` |
| 230 | `Tools/validation/check_ai_dry_run_matrix_outputs.py` |
| 229 | `Tools/validation/check_npu_knowledge_broker_packet.py` |
| 228 | `Tools/ai/build_github_evidence_bundle.py` |
| 225 | `Tools/validation/build_python_line_count_csv.py` |
| 222 | `Tools/validation/check_generated_artifact_path_policy.py` |
| 222 | `Tools/ai/workload_quality.py` |
| 221 | `Scripting/v61b/spaziotempo/core/registry.py` |
| 219 | `Tools/workflow/smart_ai_context.py` |
| 217 | `Tools/validation/generated_file_policy.py` |
| 217 | `Tools/ai/artifact_domain_registry.py` |
| 216 | `Tools/ai/code_patch_plan_common.py` |
| 211 | `Tools/ai/github_evidence_bundle_reports.py` |
| 209 | `Tools/validation/check_local_ai_enrichment_plan.py` |
| 209 | `Tools/ai/github_evidence_bundle_markdown.py` |
| 207 | `Tools/validation/check_core_activation_agnostic_contract.py` |
| 206 | `Scripting/v61b_backgood/hotpatch/render_patch.py` |
| 206 | `Scripting/v61b/hotpatch/render_patch.py` |
| 204 | `Tools/validation/run_agent_review_evidence_sufficiency_smoke.py` |
| 203 | `Tools/validation/run_code_edit_proposal_smoke.py` |
| 203 | `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/encode_final_youtube.py` |
| 201 | `Tools/validation/run_agent_review_code_patch_plan_smoke.py` |
| 201 | `Tools/validation/check_validation_report_contract.py` |
| 201 | `Tools/ai/code_edit_proposal_helpers.py` |
| 200 | `Tools/ai/validate_ai_artifacts.py` |
| 200 | `Scripting/v61b/main_v61b.py` |
| 198 | `Scripting/v61b/world_setup.py` |
| 197 | `Tools/validation/generated_python_policy.py` |
| 197 | `Tools/ai/pipeline/steps.py` |
| 189 | `Tools/ai/check_npu_provider_environment.py` |
| 186 | `Tools/workflow/git_auto_push.py` |
| 186 | `Tools/validation/run_npu_runtime_tool_context_smoke.py` |
| 186 | `Tools/ai/build_workload_quality_lane_routing.py` |
| 185 | `Tools/ai/pipeline/remediation.py` |
| 183 | `Tools/workflow/gui/components/action_panel.py` |
| 183 | `Tools/validation/check_ai_dry_run_matrix_cases.py` |
| 182 | `Tools/workflow/gui/components/live_output_panel.py` |
| 182 | `Tools/ai/run_local_provider_probe.py` |
| 181 | `Tools/workflow/gui/workflow_gui_with_push.py` |
| 181 | `Scripting/v61b_backgood/main_v61b.py` |
| 174 | `Scripting/v61b_backgood/world_setup.py` |
| 173 | `Tools/validation/check_generated_blender_script_policy.py` |
| 161 | `Tools/validation/run_npu_runtime_tool_execution_smoke.py` |
| 161 | `Scripting/shared/image_sequence.py` |
| 160 | `Tools/npu/npu_runtime.py` |
| 159 | `Tools/validation/run_provider_empty_response_diagnostics_smoke.py` |
| 159 | `Tools/validation/check_npu_decode_quality_remediation.py` |
| 159 | `Scripting/v61b/fog_filaments.py` |
| 157 | `Tools/npu/pipeline/__init__.py` |
| 153 | `Tools/ai/github_evidence_bundle_io.py` |
| 152 | `Tools/ai/pipeline/models.py` |
| 150 | `Scripting/v61b/hotpatch/lighting_patch.py` |
| 149 | `Tools/validation/check_refactor_status_consistency.py` |
| 148 | `Tools/npu/build_runtime_output_manifest.py` |
| 147 | `Tools/validation/check_blender_shared_compat_smoke.py` |
| 147 | `Tools/npu/build_provider_result_report.py` |
| 146 | `Tools/ai/github_evidence_bundle_decisions.py` |
| 144 | `Tools/workflow/artifact_consult.py` |
| 142 | `Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py` |
| 141 | `Tools/validation/check_docs_links.py` |
| 140 | `Scripting/shared/blender_compat.py` |
| 134 | `Scripting/shared/ffmpeg_encoder.py` |
| 133 | `Scripting/v61b/hotpatch/fog_patch.py` |
| 133 | `Scripting/shared/render_profiles.py` |
| 132 | `Tools/validation/check_json_artifacts.py` |
| 132 | `Scripting/v61b/spaziotempo/core/collections.py` |
| 130 | `Tools/ai/model_json.py` |
| 128 | `Tools/ai/build_agent_state_packet.py` |
| 127 | `Tools/npu/run_npu_artifact_reviewer.py` |
| 127 | `Tools/npu/pipeline/artifact_paths.py` |
| 125 | `Tools/validation/check_agent_memory_policy.py` |
| 125 | `Tools/validation/check_generated_python_policy.py` |
| 125 | `Scripting/v61b_backgood/hotpatch/accent_patch.py` |
| 125 | `Tools/npu/pipeline/reports.py` |
| 124 | `Scripting/v61b_backgood/hotpatch/fog_patch.py` |
| 123 | `Tools/validation/check_execution_plan_status.py` |
| 119 | `Tools/validation/check_ai_model_json.py` |
| 118 | `Tools/ai/pipeline/schema_report.py` |
| 117 | `Tools/workflow/workflow_shell_with_push.py` |
| 117 | `Tools/validation/check_package_structure.py` |
| 116 | `Tools/validation/run_runtime_sqlite_persistent_write_smoke.py` |
| 113 | `build_track_summary.py` |
| 111 | `Tools/npu/ai_memory_context.py` |
| 110 | `Tools/workflow/asset_inventory.py` |
| 107 | `Tools/npu/pipeline/config.py` |
| 107 | `Tools/ai/pipeline/markdown_report.py` |
| 105 | `Tools/validation/check_python_syntax.py` |
| 104 | `Tools/ai/pipeline/preflight.py` |
| 103 | `Scripting/v61b/hotpatch/runner.py` |
| 102 | `Tools/ai/pipeline/runner.py` |
| 102 | `Scripting/shared/path_utils.py` |
| 99 | `Tools/npu/pipeline/prompts.py` |
| 97 | `Tools/ai/pipeline/guardrail_models.py` |
| 97 | `Scripting/v61b_backgood/scene_utils.py` |
| 97 | `Scripting/v61b/scene_utils.py` |
| 96 | `Tools/validation/check_npu_pipeline_docs.py` |
| 92 | `Tools/workflow/gui/components/st_theme.py` |
| 91 | `Tools/npu/build_semantic_code_chunks.py` |
| 91 | `Scripting/v61b_backgood/hotpatch/common.py` |
| 91 | `Scripting/v61b/hotpatch/common.py` |
| 90 | `Tools/validation/run_npu_tool_request_contract_smoke.py` |
| 88 | `Tools/validation/run_orchestrator_gpu_runtime_tool_routing_smoke.py` |
| 88 | `Scripting/shared/json_io.py` |
| 86 | `Tools/ai/pipeline/artifact_contracts.py` |
| 85 | `Scripting/v61b_backgood/hotpatch/lighting_patch.py` |
| 84 | `Tools/npu/pipeline/validators.py` |
| 83 | `Tools/validation/check_provider_result_parsing.py` |
| 81 | `Scripting/v61b_backgood/io_utils.py` |
| 81 | `Scripting/v61b/io_utils.py` |
| 80 | `Tools/npu/pipeline/fixtures.py` |
| 79 | `Scripting/_template_audio_reactive_package/main.py` |
| 75 | `Tools/npu/pipeline/context_builder.py` |
| 75 | `Scripting/_template_audio_reactive_package/encode_ffmpeg.py` |
| 74 | `Tools/ai/pipeline/reports.py` |
| 73 | `Tools/ai/pipeline/compat.py` |
| 70 | `Tools/npu/pipeline/runner.py` |
| 70 | `Tools/ai/pipeline/r
```

### `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260503-082516.csv`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.csv`
- Size bytes: `13825`
- SHA-256: `88d5f70347905bfd2762dcf9eb088178fdb0cb888fdb76218f368c060046637f`
- Content included: `True`
- Content truncated: `False`

```text
File,Lines
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py,2197
Tools/npu/run_dual_ai_pipeline.py,1773
old script legacy/spaziotempo_asset_visual_v61.py,1513
Scripting/v61b/scene_tuning_panel.py,1262
Tools/workflow/workflow_state.py,1230
old script legacy/spaziotempo_asset_visual_v6.py,1174
Scripting/v61b_backgood/scene_tuning_panel.py,1097
Scripting/v61b/animation.py,1079
Scripting/v61b_backgood/animation.py,1019
old script legacy/spaziotempo_album_visual_v5.py,969
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py,888
Tools/ai/run_agent_gpu_deep_planning_supervised.py,814
Tools/ai/run_agent_gpu_deep_planning_review.py,812
Tools/workflow/gui/workflow_gui.py,738
Scripting/v61b/physics_setup.py,737
Scripting/v61b/asset_setup.py,725
Scripting/v61b_backgood/asset_setup.py,725
Scripting/v61b_backgood/physics_setup.py,720
Tools/npu/build_music_context.py,711
old script legacy/spaziotempo_album_visual_v3.py,710
Tools/ai/agent_runtime_tool_broker.py,673
Scripting/v61b/materials.py,657
Tools/npu/run_npu_review.py,631
Tools/validation/check_npu_pipeline_modules.py,627
Tools/ai/build_selective_execution_plan.py,618
Tools/workflow/workflow_debug.py,607
Tools/ai/run_npu_gpu_deep_review_auditor.py,606
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py,604
Tools/ai/build_repository_change_proposals.py,582
Tools/ai/build_ai_context_pack.py,575
Tools/ai/run_pipeline_dry_run_matrix.py,573
Tools/ai/build_agent_review_patch_plan.py,562
Scripting/v61b/atmosphere_setup.py,554
Tools/ai/suggest_repository_updates.py,551
Tools/ai/agent_state.py,544
Scripting/v61b_backgood/atmosphere_setup.py,543
Tools/ai/agent_runtime_sqlite_memory.py,527
Tools/ai/run_megalithic_repo_review.py,519
Scripting/v61b_backgood/materials.py,513
Tools/ai/build_agent_review_code_patch_plan.py,499
Tools/validation/ai_pipeline_report_contracts.py,497
Tools/npu/npu_guardrail_service.py,490
Tools/ai/refine_megalithic_review_signals.py,489
Tools/validation/run_agent_review_patch_plan_full_validation.py,487
Tools/validation/run_agnostic_ai_tools_smoke_matrix.py,483
normalize_scene_spec.py,469
Tools/ai/agent_memory_routing_policy.py,455
Tools/validation/check_reviewed_patch_specs.py,446
Tools/repo_patch_runner/apply_repo_mods.py,443
Tools/ai/promote_patch_spec_draft.py,442
Scripting/v61b/config.py,439
Tools/ai/build_code_interpreter_report.py,437
Tools/npu/build_project_ai_index.py,436
Tools/validation/check_ai_context_pack_contract.py,425
Tools/npu/ollama_runtime.py,422
Tools/workflow/gui/components/storage_dashboard.py,422
Tools/workflow/scene_brief.py,419
Tools/ai/build_patch_specs_from_proposals.py,414
Tools/ai/build_agent_agnostic_tool_inventory.py,408
Tools/npu/build_npu_code_context.py,402
Tools/validation/check_github_evidence_bundle.py,401
Tools/validation/check_patch_spec_drafts.py,400
Scripting/v61b/encode_ffmpeg_v61b.py,399
Tools/ai/build_dry_run_matrix_evidence_bundle.py,398
Tools/ai/build_agent_memory_inventory.py,397
Scripting/v61b/encode_image_sequence_v61b.py,395
Scripting/v61b/hotpatch/hero_material_patch.py,395
Scripting/v61b_backgood/hotpatch/hero_material_patch.py,395
Tools/ai/build_agent_review_evidence_sufficiency.py,394
Scripting/v61b/fog_dynamics.py,392
Tools/ai/build_full_context_golden_proposals.py,392
Tools/validation/check_code_contract_drift.py,392
Tools/workflow/gui/components/artifact_browser.py,390
Tools/ai/gpu_planner_json_contract.py,387
Scripting/v61b_backgood/encode_image_sequence_v61b.py,376
indexAI/scene_scripts/lll_luca_vera_master_scene_builder_candidate.py,369
Tools/npu/generated_blender_script_candidate.py,369
Tools/npu/generated_blender_script_candidate_FristNear.py,369
Tools/validation/check_repository_change_proposals.py,366
Tools/validation/test_npu_pipeline_helpers.py,359
Scripting/v61b_backgood/config.py,358
Tools/ai/build_local_ai_enrichment_plan.py,357
Tools/npu/build_ai_service_packet.py,355
Tools/workflow/project_awareness.py,353
Tools/validation/check_ai_dry_run_matrix_contract.py,341
Tools/validation/check_selected_semantic_chunks.py,339
Tools/ai/check_local_resource_lanes.py,335
Tools/validation/apply_docs_contract_drift_fixes.py,331
Tools/npu/build_npu_knowledge_broker_packet.py,327
Tools/npu/build_blender_manual_context.py,326
Tools/validation/run_shared_toolbox_ai_to_ai_bundle_smoke.py,325
Tools/workflow/workflow_shell.py,324
Tools/validation/check_dry_run_matrix_evidence_bundle.py,321
Tools/workflow/gui/workflow_gui_modern.py,319
Tools/validation/check_local_ai_adapter_manifest.py,317
Tools/ai/github_evidence_bundle_artifacts.py,315
Tools/ai/build_music_intermediates.py,314
Tools/ai/run_npu_decode_smoke_diagnostic.py,314
Tools/ai/agent_memory_policy.py,307
Tools/validation/check_full_context_golden_proposals.py,307
Tools/ai/build_analysis_input_bundle.py,304
Scripting/v61b/hotpatch/accent_patch.py,301
Tools/npu/pipeline/providers.py,297
Tools/ai/select_semantic_code_chunks.py,291
Tools/validation/check_ai_pipeline_modules.py,290
Scripting/v61b/hotpatch/diagnostics.py,286
Tools/ai/build_gpu_repair_failure_recommendation.py,286
Tools/workflow/startup_check.py,284
Tools/ai/build_agent_transient_request_context.py,283
Tools/validation/run_agent_review_patch_plan_smoke.py,283
Tools/workflow/gui/components/session_overview.py,278
Tools/ai/analyze_gpu_npu_run_sync.py,273
Tools/validation/run_gpu_planner_json_contract_smoke.py,272
Scripting/v61b/render_setup.py,270
Tools/validation/check_full_context_golden_docs_contract.py,270
Scripting/v61b_backgood/render_setup.py,267
Tools/workflow/ai_runtime_diagnostics.py,267
Tools/ai/build_code_patch_docs_followup.py,266
Tools/validation/check_ai_workload_report_quality.py,260
Tools/validation/check_docs_contract_drift.py,259
Tools/ai/build_code_patch_artifact_pack.py,258
analyze_wav.py,257
Tools/validation/run_agnostic_context_stack_smoke.py,256
Tools/ai/build_code_edit_proposal_from_plan.py,250
Tools/validation/run_gpu_runtime_tool_bootstrap_smoke.py,247
Tools/ai/build_megalithic_review_pr_draft.py,245
Tools/validation/run_agent_runtime_tool_broker_smoke.py,244
Scripting/v61b_backgood/fog_dynamics.py,240
Tools/ai/review_wave_entrypoints.py,240
Tools/npu/run_ollama_music_agent.py,238
Tools/validation/check_selective_execution_plan.py,238
Tools/validation/run_agent_memory_routing_policy_smoke.py,234
Tools/ai/replay_gpu_planner_json_contract.py,232
Tools/ai/smart_ai_gatekeeper.py,232
Tools/ai/enrich_github_evidence_bundle_code_plan.py,231
Tools/validation/check_ai_dry_run_matrix_outputs.py,230
Tools/validation/check_npu_knowledge_broker_packet.py,229
Tools/ai/build_github_evidence_bundle.py,228
Tools/validation/build_python_line_count_csv.py,225
Tools/ai/workload_quality.py,222
Tools/validation/check_generated_artifact_path_policy.py,222
Scripting/v61b/spaziotempo/core/registry.py,221
Tools/workflow/smart_ai_context.py,219
Tools/ai/artifact_domain_registry.py,217
Tools/validation/generated_file_policy.py,217
Tools/ai/code_patch_plan_common.py,216
Tools/ai/github_evidence_bundle_reports.py,211
Tools/ai/github_evidence_bundle_markdown.py,209
Tools/validation/check_local_ai_enrichment_plan.py,209
Tools/validation/check_core_activation_agnostic_contract.py,207
Scripting/v61b/hotpatch/render_patch.py,206
Scripting/v61b_backgood/hotpatch/render_patch.py,206
Tools/validation/run_agent_review_evidence_sufficiency_smoke.py,204
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/encode_final_youtube.py,203
Tools/validation/run_code_edit_proposal_smoke.py,203
Tools/ai/code_edit_proposal_helpers.py,201
Tools/validation/check_validation_report_contract.py,201
Tools/validation/run_agent_review_code_patch_plan_smoke.py,201
Scripting/v61b/main_v61b.py,200
Tools/ai/validate_ai_artifacts.py,200
Scripting/v61b/world_setup.py,198
Tools/ai/pipeline/steps.py,197
Tools/validation/generated_python_policy.py,197
Tools/ai/check_npu_provider_environment.py,189
Tools/ai/build_workload_quality_lane_routing.py,186
Tools/validation/run_npu_runtime_tool_context_smoke.py,186
Tools/workflow/git_auto_push.py,186
Tools/ai/pipeline/remediation.py,185
Tools/validation/check_ai_dry_run_matrix_cases.py,183
Tools/workflow/gui/components/action_panel.py,183
Tools/ai/run_local_provider_probe.py,182
Tools/workflow/gui/components/live_output_panel.py,182
Scripting/v61b_backgood/main_v61b.py,181
Tools/workflow/gui/workflow_gui_with_push.py,181
Scripting/v61b_backgood/world_setup.py,174
Tools/validation/check_generated_blender_script_policy.py,173
Scripting/shared/image_sequence.py,161
Tools/validation/run_npu_runtime_tool_execution_smoke.py,161
Tools/npu/npu_runtime.py,160
Scripting/v61b/fog_filaments.py,159
Tools/validation/check_npu_decode_quality_remediation.py,159
Tools/validation/run_provider_empty_response_diagnostics_smoke.py,159
Tools/npu/pipeline/__init__.py,157
Tools/ai/github_evidence_bundle_io.py,153
Tools/ai/pipeline/models.py,152
Scripting/v61b/hotpatch/lighting_patch.py,150
Tools/validation/check_refactor_status_consistency.py,149
Tools/npu/build_runtime_output_manifest.py,148
Tools/npu/build_provider_result_report.py,147
Tools/validation/check_blender_shared_compat_smoke.py,147
Tools/ai/github_evidence_bundle_decisions.py,146
Tools/workflow/artifact_consult.py,144
Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py,142
Tools/validation/check_docs_links.py,141
Scripting/shared/blender_compat.py,140
Scripting/shared/ffmpeg_encoder.py,134
Scripting/shared/render_profiles.py,133
Scripting/v61b/hotpatch/fog_patch.py,133
Scripting/v61b/spaziotempo/core/collections.py,132
Tools/validation/check_json_artifacts.py,132
Tools/ai/model_json.py,130
Tools/ai/build_agent_state_packet.py,128
Tools/npu/pipeline/artifact_paths.py,127
Tools/npu/run_npu_artifact_reviewer.py,127
Scripting/v61b_backgood/hotpatch/accent_patch.py,125
Tools/npu/pipeline/reports.py,125
Tools/validation/check_agent_memory_policy.py,125
Tools/validation/check_generated_python_policy.py,125
Scripting/v61b_backgood/hotpatch/fog_patch.py,124
Tools/validation/check_execution_plan_status.py,123
Tools/validation/check_ai_model_json.py,119
Tools/ai/pipeline/schema_report.py,118
Tools/validation/check_package_structure.py,117
Tools/workflow/workflow_shell_with_push.py,117
Tools/validation/run_runtime_sqlite_persistent_write_smoke.py,116
build_track_summary.py,113
Tools/npu/ai_memory_context.py,111
Tools/workflow/asset_inventory.py,110
Tools/ai/pipeline/markdown_report.py,107
Tools/npu/pipeline/config.py,107
Tools/validation/check_python_syntax.py,105
Tools/ai/pipeline/preflight.py,104
Scripting/v61b/hotpatch/runner.py,103
Scripting/shared/path_utils.py,102
Tools/ai/pipeline/runner.py,102
Tools/npu/pipeline/prompts.py,99
Scripting/v61b/scene_utils.py,97
Scripting/v61b_backgood/scene_utils.py,97
Tools/ai/pipeline/guardrail_models.py,97
Tools/validation/check_npu_pipeline_docs.py,96
Tools/workflow/gui/components/st_theme.py,92
Scripting/v61b/hotpatch/common.py,91
Scripting/v61b_backgood/hotpatch/common.py,91
Tools/npu/build_semantic_code_chunks.py,91
Tools/validation/run_npu_tool_request_contract_smoke.py,90
Scripting/shared/json_io.py,88
Tools/validation/run_orchestrator_gpu_runtime_tool_routing_smoke.py,88
Tools/ai/pipeline/artifact_contracts.py,86
Scripting/v61b_backgood/hotpatch/lighting_patch.py,85
Tools/npu/pipeline/validators.py,84
Tools/validation/check_provider_result_parsing.py,83
Scripting/v61b/io_utils.py,81
Scripting/v61b_backgood/io_utils.py,81
Tools/npu/pipeline/fixtures.py,80
Scripting/_template_audio_reactive_package/main.py,79
Scripting/_template_audio_reactive_package/encode_ffmpeg.py,75
Tools/npu/pipeline/context_builder.py,75
Tools/ai/pipeline/reports.py,74
Tools/ai/pipeline/compat.py,73
Tools/ai/pipeline/refactor_status.py,70
Tools/npu/pipeline/runner.py,70
Tools/ai/review_agent_memory.py,69
Tools/npu/pipeline/migration_readiness.py,68
Tools/ai/pipeline/scheduler.py,66
Tools/ai/run_parallel_artifact_pipeline.py,65
Tools/validation/check_ai_pipeline_report_contract.py,65
Tools/validation/check_artifact_domain_registry.py,64
Scripting/v61b/hot_update_scene_v61b.py,63
Scripting/v61b_backgood/hot_update_scene_v61b.py,61
Tools/npu/pipeline/io_utils.py,61
Scripting/v61b_backgood/hotpatch/runner.py,60
Tools/validation/check_npu_pipeline_helper_tests.py,59
Tools/npu/pipeline/artifact_writer.py,56
Tools/ai/merge_ai_candidates.py,53
Tools/npu/pipeline/legacy_compat.py,52
Scripting/_template_audio_reactive_package/audio_mapping.py,51
Scripting/v61b/reload_utils.py,51
Tools/ai/pipeline/cli.py,50
Tools/validation/report_utils.py,50
Scripting/_template_audio_reactive_package/config.py,49
Scripting/_template_audio_reactive_package/materials.py,35
Tools/ai/pipeline/orchestrator.py,31
Scripting/v61b/camera_setup.py,29
Scripting/v61b_backgood/camera_setup.py,29
Scripting/_template_audio_reactive_package/camera.py,26
Scripting/_template_audio_reactive_package/render_settings.py,26
Scripting/_template_audio_reactive_package/lighting.py,23
Tools/ai/pipeline/__init__.py,23
Scripting/_template_audio_reactive_package/scene_objects.py,21
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/render_profiles_reference.py,20
Scripting/v61b/spaziotempo/features/catalog.py,19
Tools/ai/pipeline/defaults.py,15
Scripting/shared/__init__.py,13
Scripting/v61b/spaziotempo/__init__.py,4
Scripting/v61b/hotpatch/__init__.py,3
Scripting/v61b_backgood/hotpatch/__init__.py,3
Scripting/v61b/__init__.py,1
Scripting/v61b/spaziotempo/core/__init__.py,1
Scripting/v61b/spaziotempo/features/__init__.py,1
Scripting/v61b_backgood/__init__.py,1
Tools/workflow/gui/components/__init__.py,1

```

### `output/analysis/shared_toolbox_ai_to_ai_final_summary_20260503-082504.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `71651`
- SHA-256: `1415c17a4677a1dbc8c238091f400d38d54d4f891664f534b2dfea8f98ee99d2`
- Content included: `True`
- Content truncated: `True`

```text
# Shared Toolbox AI-to-AI Final Summary

- stamp: 20260503-082504
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

- output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json exists=True json_ok=True kind=agent_agnostic_tool_inventory passed=True
- output/validation/shared_toolbox_refactor_python_line_count_20260503-082504.json exists=True json_ok=True kind=python_line_count_csv passed=True
- output/analysis/shared_toolbox_refactor_code_interpreter_20260503-082504.json exists=True json_ok=True kind=code_interpreter_report passed=True
- output/validation/shared_toolbox_refactor_python_syntax_20260503-082504.json exists=True json_ok=True kind=python_syntax passed=True
- output/validation/shared_toolbox_refactor_bundle_smoke_20260503-082504.json exists=True json_ok=True kind=shared_toolbox_ai_to_ai_bundle_smoke passed=True
- output/validation/shared_toolbox_refactor_memory_routing_20260503-082504.json exists=True json_ok=True kind=agent_memory_routing_policy passed=True
- output/analysis/shared_toolbox_refactor_duplication_audit_20260503-082504.json exists=True json_ok=True kind=shared_toolbox_refactor_duplication_audit passed=True

## Remaining gaps

- output/validation/shared_toolbox_python_syntax_20260503-082504.json: optional report missing
- output/analysis/shared_toolbox_code_interpreter_20260503-082504.json: optional report missing
- output/validation/shared_toolbox_gpu_contract_smoke_20260503-082504.json: optional report missing
- output/validation/shared_toolbox_gpu_routing_20260503-082504.json: optional report missing
- output/validation/shared_toolbox_npu_execution_20260503-082504.json: optional report missing
- output/validation/shared_toolbox_npu_contract_20260503-082504.json: optional report missing
- output/validation/npu_provider_environment_shared_toolbox_20260503-082504.json: optional report missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_20260503-082504_orchestrator.json: optional report missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_20260503-082504_gpu.json: optional report missing
- output/analysis/shared_toolbox_gpu_npu_sync_20260503-082504.json: optional report missing
- output/analysis/shared_toolbox_gpu_contract_replay_20260503-082504.json: optional report missing
- output/analysis/shared_toolbox_code_interpreter_20260503-082504.md: optional artifact missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_20260503-082504_orchestrator.md: optional artifact missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_20260503-082504_gpu.md: optional artifact missing
- output/analysis/shared_toolbox_gpu_npu_sync_20260503-082504.md: optional artifact missing
- output/analysis/shared_toolbox_gpu_contract_replay_20260503-082504.md: optional artifact missing
- output/analysis/shared_toolbox_ai_to_ai_final_summary_20260503-082504.md: optional artifact missing
- runtime tool requests not proven in provider-backed run: No concrete tool_requests were found in the included reports.

## Recommended next task

docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md

## Recursive defaults

- Enabled: `True`
- Discovered reports: `8`
- Discovered artifacts: `8`

## Chunked large JSON/Markdown files

- output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json lines=16354 chunks=82 chunk_size=200
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L1-L200 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L201-L400
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L201-L400 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L401-L600
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L401-L600 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L601-L800
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L601-L800 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L801-L1000
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L801-L1000 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L1001-L1200
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L1001-L1200 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L1201-L1400
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L1201-L1400 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L1401-L1600
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L1401-L1600 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L1601-L1800
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L1601-L1800 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L1801-L2000
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L1801-L2000 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L2001-L2200
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L2001-L2200 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L2201-L2400
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L2201-L2400 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L2401-L2600
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L2401-L2600 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L2601-L2800
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L2601-L2800 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L2801-L3000
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L2801-L3000 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L3001-L3200
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L3001-L3200 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L3201-L3400
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L3201-L3400 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L3401-L3600
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L3401-L3600 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L3601-L3800
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L3601-L3800 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L3801-L4000
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L3801-L4000 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L4001-L4200
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L4001-L4200 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L4201-L4400
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L4201-L4400 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L4401-L4600
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L4401-L4600 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L4601-L4800
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L4601-L4800 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L4801-L5000
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L4801-L5000 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L5001-L5200
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L5001-L5200 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L5201-L5400
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L5201-L5400 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L5401-L5600
  - output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json#L5401-L5600 -> next: output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_invent
```

### `output/analysis/shared_toolbox_ai_to_ai_final_summary_20260503-082504.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `282274`
- SHA-256: `0d47875c371ca1baec407db10698b081e2c4b8f122b13d91de889d812991c1ee`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "shared_toolbox_ai_to_ai_final_summary",
  "stamp": "20260503-082504",
  "passed": true,
  "tools_available": [
    "build_agent_agnostic_tool_inventory",
    "build_agent_memory_inventory",
    "build_agent_transient_request_context",
    "build_code_interpreter_report",
    "build_python_line_count_csv",
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
      "path": "output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_agnostic_tool_inventory",
      "passed": true
    },
    {
      "path": "output/validation/shared_toolbox_refactor_python_line_count_20260503-082504.json",
      "exists": true,
      "json_ok": true,
      "kind": "python_line_count_csv",
      "passed": true
    },
    {
      "path": "output/analysis/shared_toolbox_refactor_code_interpreter_20260503-082504.json",
      "exists": true,
      "json_ok": true,
      "kind": "code_interpreter_report",
      "passed": true
    },
    {
      "path": "output/validation/shared_toolbox_refactor_python_syntax_20260503-082504.json",
      "exists": true,
      "json_ok": true,
      "kind": "python_syntax",
      "passed": true
    },
    {
      "path": "output/validation/shared_toolbox_refactor_bundle_smoke_20260503-082504.json",
      "exists": true,
      "json_ok": true,
      "kind": "shared_toolbox_ai_to_ai_bundle_smoke",
      "passed": true
    },
    {
      "path": "output/validation/shared_toolbox_refactor_memory_routing_20260503-082504.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_memory_routing_policy",
      "passed": true
    },
    {
      "path": "output/analysis/shared_toolbox_refactor_duplication_audit_20260503-082504.json",
      "exists": true,
      "json_ok": true,
      "kind": "shared_toolbox_refactor_duplication_audit",
      "passed": true
    }
  ],
  "remaining_gaps": [
    {
      "path": "output/validation/shared_toolbox_python_syntax_20260503-082504.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/analysis/shared_toolbox_code_interpreter_20260503-082504.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/shared_toolbox_gpu_contract_smoke_20260503-082504.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/shared_toolbox_gpu_routing_20260503-082504.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/shared_toolbox_npu_execution_20260503-082504.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/shared_toolbox_npu_contract_20260503-082504.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/npu_provider_environment_shared_toolbox_20260503-082504.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/ai_pipeline/shared_toolbox_ai_to_ai_20260503-082504_orchestrator.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/ai_pipeline/shared_toolbox_ai_to_ai_20260503-082504_gpu.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/analysis/shared_toolbox_gpu_npu_sync_20260503-082504.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/analysis/shared_toolbox_gpu_contract_replay_20260503-082504.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/analysis/shared_toolbox_code_interpreter_20260503-082504.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/ai_pipeline/shared_toolbox_ai_to_ai_20260503-082504_orchestrator.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/ai_pipeline/shared_toolbox_ai_to_ai_20260503-082504_gpu.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/analysis/shared_toolbox_gpu_npu_sync_20260503-082504.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/analysis/shared_toolbox_gpu_contract_replay_20260503-082504.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/analysis/shared_toolbox_ai_to_ai_final_summary_20260503-082504.md",
      "reason": "optional artifact missing"
    },
    {
      "gap": "runtime tool requests not proven in provider-backed run",
      "detail": "No concrete tool_requests were found in the included reports."
    }
  ],
  "recommended_next_task_md": "docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md",
  "compact_bundle_paths": [
    "docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_refactor_duplication_audit_bundle_20260503-082504.json",
    "docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_refactor_duplication_audit_bundle_20260503-082504.md"
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
    "docs/LOCAL_AI_TASKS/shared-toolbox-refactor-duplication-audit-next-task-2026-05-03.md",
    "output/analysis/shared_toolbox_refactor_code_interpreter_20260503-082504.md",
    "output/analysis/shared_toolbox_refactor_duplication_audit_20260503-082504.md",
    "output/validation/shared_toolbox_refactor_all_python_files_20260503-082504.md",
    "docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260503-082516.csv"
  ],
  "recursive_defaults": {
    "enabled": true,
    "stamp": "20260503-082504",
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
      "output/validation/shared_toolbox_refactor_bundle_smoke_20260503-082504.json",
      "output/validation/shared_toolbox_refactor_memory_routing_20260503-082504.json",
      "output/validation/shared_toolbox_refactor_python_line_count_20260503-082504.json",
      "output/validation/shared_toolbox_refactor_python_syntax_20260503-082504.json",
      "output/analysis/shared_toolbox_ai_to_ai_final_summary_20260503-082504.json",
      "output/analysis/shared_toolbox_refactor_code_interpreter_20260503-082504.json",
      "output/analysis/shared_toolbox_refactor_duplication_audit_20260503-082504.json",
      "output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json"
    ],
    "discovered_artifacts": [
      "output/analysis/shared_toolbox_ai_to_ai_final_summary_20260503-082504.json",
      "output/analysis/shared_toolbox_ai_to_ai_final_summary_20260503-082504.md",
      "output/analysis/shared_toolbox_refactor_code_interpreter_20260503-082504.json",
      "output/analysis/shared_toolbox_refactor_code_interpreter_20260503-082504.md",
      "output/analysis/shared_toolbox_refactor_duplication_audit_20260503-082504.json",
      "output/analysis/shared_toolbox_refactor_duplication_audit_20260503-08250
```

### `output/analysis/shared_toolbox_refactor_code_interpreter_20260503-082504.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1066899`
- SHA-256: `314d4f0554cc1e400b0f59f155f63cbaaf40602988ccb7df3d60fd8132e48e61`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "code_interpreter_report",
  "generated_at": "2026-05-03T08:25:18",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "manual_review_required": true,
  "apply_mode": "report_only_static_code_interpreter",
  "file_count": 203,
  "parsed_file_count": 203,
  "total_lines": 56304,
  "total_functions": 2115,
  "total_classes": 70,
  "total_risk_signals": 39,
  "total_todos": 21,
  "top_imports": [
    {
      "module": "Tools",
      "count": 543
    },
    {
      "module": "__future__",
      "count": 201
    },
    {
      "module": "pathlib",
      "count": 182
    },
    {
      "module": "typing",
      "count": 171
    },
    {
      "module": "json",
      "count": 143
    },
    {
      "module": "argparse",
      "count": 132
    },
    {
      "module": "datetime",
      "count": 100
    },
    {
      "module": "sys",
      "count": 77
    },
    {
      "module": "report_utils",
      "count": 68
    },
    {
      "module": "dataclasses",
      "count": 48
    },
    {
      "module": "workflow_state",
      "count": 45
    },
    {
      "module": "re",
      "count": 34
    },
    {
      "module": "pipeline",
      "count": 28
    },
    {
      "module": "subprocess",
      "count": 27
    },
    {
      "module": "agent_state",
      "count": 26
    },
    {
      "module": "tkinter",
      "count": 23
    },
    {
      "module": "os",
      "count": 20
    },
    {
      "module": "models",
      "count": 16
    },
    {
      "module": "ollama_runtime",
      "count": 16
    },
    {
      "module": "components",
      "count": 15
    },
    {
      "module": "hashlib",
      "count": 14
    },
    {
      "module": "artifact_contracts",
      "count": 13
    },
    {
      "module": "time",
      "count": 12
    },
    {
      "module": "reports",
      "count": 12
    },
    {
      "module": "defaults",
      "count": 11
    },
    {
      "module": "npu_runtime",
      "count": 9
    },
    {
      "module": "artifact_paths",
      "count": 9
    },
    {
      "module": "ast",
      "count": 8
    },
    {
      "module": "concurrent",
      "count": 8
    },
    {
      "module": "io_utils",
      "count": 8
    },
    {
      "module": "providers",
      "count": 8
    },
    {
      "module": "agent_memory_policy",
      "count": 7
    },
    {
      "module": "runner",
      "count": 7
    },
    {
      "module": "config",
      "count": 6
    },
    {
      "module": "scene_brief",
      "count": 5
    },
    {
      "module": "sqlite3",
      "count": 4
    },
    {
      "module": "warnings",
      "count": 4
    },
    {
      "module": "math",
      "count": 4
    },
    {
      "module": "compat",
      "count": 4
    },
    {
      "module": "shutil",
      "count": 4
    }
  ],
  "largest_files": [
    {
      "path": "Tools/npu/run_dual_ai_pipeline.py",
      "line_count": 1773,
      "risk": "high"
    },
    {
      "path": "Tools/workflow/workflow_state.py",
      "line_count": 1230,
      "risk": "high"
    },
    {
      "path": "Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py",
      "line_count": 888,
      "risk": "high"
    },
    {
      "path": "Tools/ai/run_agent_gpu_deep_planning_supervised.py",
      "line_count": 814,
      "risk": "high"
    },
    {
      "path": "Tools/ai/run_agent_gpu_deep_planning_review.py",
      "line_count": 812,
      "risk": "high"
    },
    {
      "path": "Tools/workflow/gui/workflow_gui.py",
      "line_count": 738,
      "risk": "medium"
    },
    {
      "path": "Tools/npu/build_music_context.py",
      "line_count": 711,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/agent_runtime_tool_broker.py",
      "line_count": 673,
      "risk": "medium"
    },
    {
      "path": "Tools/npu/run_npu_review.py",
      "line_count": 631,
      "risk": "medium"
    },
    {
      "path": "Tools/validation/check_npu_pipeline_modules.py",
      "line_count": 627,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_selective_execution_plan.py",
      "line_count": 618,
      "risk": "medium"
    },
    {
      "path": "Tools/workflow/workflow_debug.py",
      "line_count": 607,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/run_npu_gpu_deep_review_auditor.py",
      "line_count": 606,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py",
      "line_count": 604,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_repository_change_proposals.py",
      "line_count": 582,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_ai_context_pack.py",
      "line_count": 575,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/run_pipeline_dry_run_matrix.py",
      "line_count": 573,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_agent_review_patch_plan.py",
      "line_count": 562,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/suggest_repository_updates.py",
      "line_count": 551,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/agent_state.py",
      "line_count": 544,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/agent_runtime_sqlite_memory.py",
      "line_count": 527,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/run_megalithic_repo_review.py",
      "line_count": 519,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_agent_review_code_patch_plan.py",
      "line_count": 499,
      "risk": "medium"
    },
    {
      "path": "Tools/validation/ai_pipeline_report_contracts.py",
      "line_count": 497,
      "risk": "medium"
    },
    {
      "path": "Tools/npu/npu_guardrail_service.py",
      "line_count": 490,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/refine_megalithic_review_signals.py",
      "line_count": 489,
      "risk": "medium"
    },
    {
      "path": "Tools/validation/run_agent_review_patch_plan_full_validation.py",
      "line_count": 487,
      "risk": "medium"
    },
    {
      "path": "Tools/validation/run_agnostic_ai_tools_smoke_matrix.py",
      "line_count": 483,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/agent_memory_routing_policy.py",
      "line_count": 455,
      "risk": "medium"
    },
    {
      "path": "Tools/validation/check_reviewed_patch_specs.py",
      "line_count": 446,
      "risk": "medium"
    }
  ],
  "risk_summary": {
    "medium": 104,
    "low": 94,
    "high": 5
  },
  "recommendation_count": 109,
  "recommendations": [
    {
      "id": "code_static_001",
      "target_file": "Tools/ai/agent_memory_policy.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\agent_memory_policy.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_002",
      "target_file": "Tools/ai/agent_memory_routing_policy.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module",
        "large functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\agent_memory_routing_policy.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_003",
      "target_file": "Tools/ai/agent_runtime_sqlite_memory.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module",
        "large functions detected",
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\agent_runtime_sqlite_memory.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_004",
      "target_file": "Tools/ai/agent_runtime_tool_broker.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module",
        "large functions detected",
        "complex functions detected",
        "static risk calls detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\agent_runtime_tool_broker.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_005",
      "target_file": "Tools/ai/agent_state.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\agent_state.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_006",
      "target_file": "Tools/ai/analyze_gpu_npu_run_sync.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\analyze_gpu_npu_run_sync.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_007",
      "target_file": "Tools/ai/build_agent_agnostic_tool_inventory.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module",
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\build_agent_agnostic_tool_inventory.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_008",
      "target_file": "Tools/ai/build_agent_memory_inventory.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "large functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\build_agent_memory_inventory.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_009",
      "target_file": "Tools/ai/build_agent_review_code_patch_plan.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\build_agent_review_code_patch_plan.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_010",
      "target_file": "Tools/ai/build_agent_review_patch_plan.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module",
        "large functions detected",
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\buil
```

### `output/analysis/shared_toolbox_refactor_duplication_audit_20260503-082504.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `13614`
- SHA-256: `f982cf7a74178f74ff0d874a47edaed8116e3b2d0d8116600853574bf273aab8`
- Content included: `True`
- Content truncated: `False`

```text
{
    "schema_version":  1,
    "kind":  "shared_toolbox_refactor_duplication_audit",
    "stamp":  "20260503-082504",
    "passed":  true,
    "provider_execution_performed":  false,
    "patch_application_performed":  false,
    "sqlite_write_performed":  false,
    "persistent_memory_write_performed":  false,
    "refactor_verification":  {
                                  "layering_preserved":  true,
                                  "builder_delegates_to_common_bundle":  true,
                                  "chunking_in_common_evidence_layer":  true,
                                  "validator_reused":  true,
                                  "smoke_coverage_present":  true,
                                  "cli_schema_preserved":  true,
                                  "report_schema_preserved":  true,
                                  "notes":  [
                                                "PR142 merged the shared toolbox final-summary/bundle builder and moved recursive discovery/chunk pointer handling into the shared evidence-bundle layer.",
                                                "The shared toolbox builder remains a final-summary/bundle orchestrator and should not become a generic scanner or executor.",
                                                "Bundle smoke passed and validated recursive discovery plus large JSON/Markdown chunk pointers."
                                            ]
                              },
    "duplication_candidates":  [
                                   {
                                       "candidate_id":  "dup_path_helpers",
                                       "repeated_logic":  "Repository-relative and path resolution helper patterns appear in multiple Tools/ai and Tools/validation modules.",
                                       "files_involved":  [
                                                              "Tools/ai/github_evidence_bundle_io.py",
                                                              "Tools/ai/agent_runtime_tool_broker.py",
                                                              "Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py",
                                                              "Tools/ai/build_agent_agnostic_tool_inventory.py"
                                                          ],
                                       "existing_helper_available":  true,
                                       "preferred_existing_helper_or_module":  "Tools.ai.github_evidence_bundle_io for evidence-bundle paths; Tools.validation.report_utils for validation output paths.",
                                       "recommendation_type":  "reuse_existing_helper",
                                       "risk":  "medium",
                                       "schema_or_cli_impact":  "none expected if imports are changed carefully.",
                                       "validation_required":  [
                                                                   "python -m py_compile touched files",
                                                                   "run_shared_toolbox_ai_to_ai_bundle_smoke.py",
                                                                   "run_agent_runtime_tool_broker_smoke.py"
                                                               ],
                                       "manual_review_required":  true
                                   },
                                   {
                                       "candidate_id":  "dup_json_markdown_writers",
                                       "repeated_logic":  "JSON/Markdown write helpers are repeated across smoke, broker, inventory and bundle scripts.",
                                       "files_involved":  [
                                                              "Tools/validation/report_utils.py",
                                                              "Tools/ai/agent_runtime_tool_broker.py",
                                                              "Tools/ai/build_agent_agnostic_tool_inventory.py",
                                                              "Tools/validation/run_shared_toolbox_ai_to_ai_bundle_smoke.py"
                                                          ],
                                       "existing_helper_available":  true,
                                       "preferred_existing_helper_or_module":  "Tools.validation.report_utils.write_json_report and resolve_output_path.",
                                       "recommendation_type":  "promote_existing_function",
                                       "risk":  "low",
                                       "schema_or_cli_impact":  "none if output formatting remains JSON indent=2 UTF-8.",
                                       "validation_required":  [
                                                                   "check_python_syntax",
                                                                   "affected smoke tests"
                                                               ],
                                       "manual_review_required":  true
                                   },
                                   {
                                       "candidate_id":  "dup_markdown_rendering",
                                       "repeated_logic":  "Markdown renderers are local by design in many reports but share repeated guardrail/status sections.",
                                       "files_involved":  [
                                                              "Tools/ai/agent_runtime_tool_broker.py",
                                                              "Tools/ai/build_agent_agnostic_tool_inventory.py",
                                                              "Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py",
                                                              "Tools/validation/run_shared_toolbox_ai_to_ai_bundle_smoke.py"
                                                          ],
                                       "existing_helper_available":  false,
                                       "preferred_existing_helper_or_module":  "Potential future helper in Tools.validation.report_utils, but keep local unless repeated sections become schema-stable.",
                                       "recommendation_type":  "keep_local_by_design",
                                       "risk":  "low",
                                       "schema_or_cli_impact":  "none",
                                       "validation_required":  [
                                                                   "visual/manual Markdown review",
                                                                   "bundle validation"
                                                               ],
                                       "manual_review_required":  true
                                   },
                                   {
                                       "candidate_id":  "dup_tool_request_packet_logic",
                                       "repeated_logic":  "Runtime tool request packet construction appears in memory routing and orchestrator/broker flow.",
                                       "files_involved":  [
                                                              "Tools/ai/agent_memory_routing_policy.py",
                                                              "Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py",
                                                              "Tools/ai/agent_runtime_tool_broker.py"
                                                          ],
                                       "existing_helper_available":  false,
                                       "preferred_existing_helper_or_module":  "Advisory: consider a future shared request-packet helper only after schema stabilizes further.",
                                       "recommendation_type":  "advisory_only",
                                       "risk":  "medium",
                                       "schema_or_cli_impact":  "possible schema impact; do not refactor automatically.",
                                       "validation_required":  [
                                                                   "run_agent_runtime_tool_broker_smoke.py",
                                                                   "run_orchestrator_gpu_runtime_tool_routing_smoke.py",
                                                                   "run_npu_runtime_tool_execution_smoke.py"
                                                               ],
                                       "manual_review_required":  true
                                   }
                               ],
    "helper_reuse_recommendations":  [
                                         "Prefer Tools.ai.github_evidence_bundle_io for evidence-bundle path/text/JSON helpers.",
                                         "Prefer Tools.ai.github_evidence_bundle_artifacts for artifact discovery and chunk pointer metadata.",
                                         "Prefer Tools.validation.report_utils for validation output path resolution and JSON report writing.",
                                         "Do not add a new generic helper module until an existing module is proven unsuitable."
                                     ],
    "manual_review_patch_plan_candidates":  [
                                                {
                                                    "candidate_id":  "patch_plan_report_utils_json_write_reuse",
                                                    "title":  "Replace local JSON write helpers in selected smoke/report scripts with report_utils.write_json_report.",
                                                    "recommendation_type":  "ready_for_patch_plan",
                                                    "target_files":  [
                                                                         "Tools/validation/run_shared_toolbox_ai_to_ai_bundle_smoke.py"
                                                                     ],
                                                    "reason":  "Small seam, low schema risk, validates helper reuse without touching provider/orchestrator behavior.",
                                                    "validation":  [
                                                                       "python -m py_compile Tools/validation/run_shared_toolbox_ai_to_ai_bundle_smoke.py",
                                                                       "python Tools/validation/run_shared_toolbox_ai_to_ai_bundle_smoke.py --repo-root . --output output/validation/shared_toolbox_refactor_bundle_smoke_reuse_validation.json --markdown-output output/validation/shared_toolbox_refactor_bundle_smoke_reuse_validation.md"
                                                                   ]
                                                }
                                            ],
    "advisory_only_findings":  [
                                   "Do not refactor provider/orchestrator request-packet construction until broker/orchestrator schema is fully stabilized.",
                                   "Do not centralize all Markdown rendering yet; report-specific Markdown remains easier to review and safer."
                               ],
    "validation_commands":  [
                                "build_agent_agnostic_tool_inventory.py",
                                "build_python_line_count_csv.py",
                                "build_code_interpreter_report.py",
                                "check_python_syntax",
                                "run_shared_toolbox_ai_to_ai_bundle_smoke.py",
                                "agent_memory_routing_policy.py"
                            ],
    "source_reports":  {
                           "python_syntax_passed":  true,
                           "python_line_count_passed":  true,
                           "python_file_count":  291,
                           "python_total_lines":  83302,
                           "code_interpreter_passed":  true,
                           "bundle_smoke_passed":  true,
                           "bundle_validation_passed":  true,
                           "memory_routing_passed":  true,
                           "memory_tool_request_count":  null,
                           "chunked_file_count":  6,
                           "recursive_discovered_report_count":  8,
                           "recursive_discovered_artifact_count":  12
                       },
    "stop_conditions":  [
                            "Stop if python syntax validation fails.",
                            "Stop if shared toolbox bundle smoke fails.",
                            "Stop if patch_application_performed=True.",
                            "Stop if sqlite_write_performed=True or persistent_memory_write_performed=True.",
                            "Stop if a recommended refactor breaks CLI/report schema without migration plan."
                        ],
    "errors":  [

               ],
    "warnings":  [
                     "provider_execution_performed=True in bundle smoke is inherited from fake smoke inputs and is not a real provider execution."
                 ]
}

```

### `output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `452835`
- SHA-256: `c58debdabb51d3e228b7a83901bc35eda0b6adfd0788c745238e60aa4b094a1b`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_agnostic_tool_inventory",
  "generated_at": "2026-05-03T08:25:16",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_read_only_inventory",
  "roots": [
    "Tools/ai",
    "Tools/validation",
    "Tools/workflow",
    "Tools/npu",
    "Tools/git",
    "Tools/repo_patch_runner"
  ],
  "summary": {
    "tool_count": 216,
    "category_counts": {
      "validator": 71,
      "provider_probe_or_adapter": 46,
      "support_tool": 38,
      "orchestrator_pipeline": 31,
      "git_helper": 10,
      "agent_context_builder": 9,
      "proposal_or_review_builder": 7,
      "review_helper": 4
    },
    "owner_lane_counts": {
      "npu_explicit_provider_tool": 78,
      "gpu_cuda_explicit_provider_tool": 40,
      "cpu_validation": 37,
      "cpu_support": 34,
      "cpu_orchestration": 19,
      "cpu_context_builder": 4,
      "cpu_proposal_builder": 4
    },
    "consumed_lane_counts": {
      "cpu": 216,
      "npu": 158,
      "gpu_cuda": 116
    },
    "apply_mode_counts": {
      "not_declared": 127,
      "report_only": 60,
      "manual_review_only": 21,
      "explicit_git_operation": 8
    },
    "provider_execution_default_counts": {
      "none_or_reported": 196,
      "explicit_only": 20
    }
  },
  "tools": [
    {
      "path": "Tools/ai/agent_memory_policy.py",
      "extension": ".py",
      "category": "support_tool",
      "owner_lane": "cpu_support",
      "consumed_by_lanes": [
        "cpu"
      ],
      "provider_execution_default": "none_or_reported",
      "apply_mode": "not_declared",
      "lines": 307,
      "symbols": [
        "MemoryReview",
        "days_since",
        "detect_secret_patterns",
        "evaluate_memory_records",
        "kind_threshold",
        "load_records",
        "parse_datetime",
        "promotion_reason",
        "review_record",
        "to_dict",
        "write_memory_policy_markdown"
      ],
      "flags": [],
      "guardrails": [
        "sqlite_awareness"
      ]
    },
    {
      "path": "Tools/ai/agent_memory_routing_policy.py",
      "extension": ".py",
      "category": "support_tool",
      "owner_lane": "gpu_cuda_explicit_provider_tool",
      "consumed_by_lanes": [
        "cpu",
        "gpu_cuda",
        "npu"
      ],
      "provider_execution_default": "none_or_reported",
      "apply_mode": "report_only",
      "lines": 455,
      "symbols": [
        "build_discovery_tool_requests",
        "build_memory_tool_requests",
        "build_policy",
        "build_promotion_candidates",
        "default_operational_queries",
        "default_persistent_queries",
        "main",
        "now_iso",
        "render_markdown",
        "repo_rel",
        "resolve_path",
        "safe_id",
        "split_values",
        "tool_request"
      ],
      "flags": [
        "--broker-request-output",
        "--clear-operational",
        "--markdown-output",
        "--memory-search-limit",
        "--objective",
        "--operational-query",
        "--output",
        "--persistent-query",
        "--profile",
        "--promotion-candidate",
        "--remember-note",
        "--repo-root"
      ],
      "guardrails": [
        "blender_runtime_guardrail",
        "output_artifacts_guardrail",
        "patch_application_reported",
        "provider_execution_reported",
        "read_only",
        "sqlite_awareness"
      ]
    },
    {
      "path": "Tools/ai/agent_runtime_sqlite_memory.py",
      "extension": ".py",
      "category": "support_tool",
      "owner_lane": "cpu_support",
      "consumed_by_lanes": [
        "cpu"
      ],
      "provider_execution_default": "none_or_reported",
      "apply_mode": "report_only",
      "lines": 527,
      "symbols": [
        "build_report",
        "clear_operational",
        "ensure_operational_db",
        "ensure_persistent_db",
        "is_under",
        "main",
        "now_iso",
        "operational_status",
        "parse_tags",
        "persistent_row_to_dict",
        "persistent_status",
        "remember_operational",
        "remember_persistent",
        "render_markdown",
        "repo_rel",
        "resolve_path",
        "row_to_dict",
        "safe_id",
        "search_operational",
        "search_persistent"
      ],
      "flags": [
        "--action",
        "--allow-persistent-write",
        "--confirm",
        "--content",
        "--database",
        "--limit",
        "--markdown-output",
        "--output",
        "--persistent-database",
        "--query",
        "--repo-root",
        "--request-id",
        "--role",
        "--scope",
        "--summary",
        "--tag"
      ],
      "guardrails": [
        "blender_runtime_guardrail",
        "output_artifacts_guardrail",
        "patch_application_reported",
        "provider_execution_reported",
        "read_only",
        "sqlite_awareness"
      ]
    },
    {
      "path": "Tools/ai/agent_runtime_tool_broker.py",
      "extension": ".py",
      "category": "support_tool",
      "owner_lane": "gpu_cuda_explicit_provider_tool",
      "consumed_by_lanes": [
        "cpu",
        "gpu_cuda",
        "npu"
      ],
      "provider_execution_default": "none_or_reported",
      "apply_mode": "report_only",
      "lines": 673,
      "symbols": [
        "ToolSpec",
        "base_outputs",
        "build_agent_agnostic_tool_inventory",
        "build_agent_memory_inventory",
        "build_agent_transient_request_context",
        "build_code_interpreter_report",
        "build_python_line_count_csv",
        "build_report",
        "check_python_syntax",
        "check_validation_report_contract",
        "compact_value",
        "execute_command",
        "execute_tool_request",
        "extract_tool_requests",
        "main",
        "now_iso",
        "read_json_if_exists",
        "render_markdown",
        "repo_rel",
        "resolve_path",
        "run_gpu_planner_json_contract_smoke",
        "runtime_sqlite_memory",
        "safe_id",
        "split_values",
        "truthy",
        "validate_request_args"
      ],
      "flags": [
        "--action",
        "--allow-persistent-write",
        "--confirm",
        "--content",
        "--csv-output",
        "--database",
        "--dry-run",
        "--exclude-dir",
        "--input",
        "--limit",
        "--markdown-output",
        "--memory-db",
        "--memory-note",
        "--objective",
        "--output",
        "--persistent-database",
        "--query",
        "--raw-file",
        "--repo-root",
        "--report-dir",
        "--report-file",
        "--report-output",
        "--request-file",
        "--request-id",
        "--role",
        "--root",
        "--scope",
        "--stamp",
        "--summary",
        "--tag",
        "--timeout-seconds",
        "--tool-output-dir"
      ],
      "guardrails": [
        "blender_runtime_guardrail",
        "no_blender_runtime",
        "output_artifacts_guardrail",
        "patch_application_reported",
        "provider_execution_reported",
        "read_only",
        "sqlite_awareness"
      ]
    },
    {
      "path": "Tools/ai/agent_state.py",
      "extension": ".py",
      "category": "agent_context_builder",
      "owner_lane": "gpu_cuda_explicit_provider_tool",
      "consumed_by_lanes": [
        "cpu",
        "gpu_cuda",
        "npu"
      ],
      "provider_execution_default": "none_or_reported",
      "apply_mode": "not_declared",
      "lines": 544,
      "symbols": [
        "AgentMicroTask",
        "MemoryRecord",
        "append_memory_jsonl",
        "build_agent_state_packet",
        "clamp_confidence",
        "compact_text",
        "default_microtasks",
        "ensure_memory_db",
        "from_mapping",
        "from_text",
        "json_or_default",
        "keywords",
        "load_memory_db",
        "load_memory_jsonl",
        "read_text",
        "records_from_files",
        "relative_path",
        "score_record",
        "select_memory",
        "sha256_text",
        "slugify",
        "stable_tag_tuple",
        "to_dict",
        "upsert_memory_db",
        "utc_now_iso",
        "write_agent_state_markdown"
      ],
      "flags": [],
      "guardrails": [
        "sqlite_awareness"
      ]
    },
    {
      "path": "Tools/ai/analyze_gpu_npu_run_sync.py",
      "extension": ".py",
      "category": "provider_probe_or_adapter",
      "owner_lane": "npu_explicit_provider_tool",
      "consumed_by_lanes": [
        "cpu",
        "gpu_cuda",
        "npu"
      ],
      "provider_execution_default": "none_or_reported",
      "apply_mode": "report_only",
      "lines": 273,
      "symbols": [
        "analyze",
        "audit_duration_seconds",
        "build_suggestions",
        "first_int",
        "main",
        "nested_dict",
        "now_iso",
        "percentile",
        "read_json",
        "render_markdown",
        "repo_rel",
        "resolve_path",
        "safe_float",
        "safe_int",
        "write_json"
      ],
      "flags": [
        "--markdown-output",
        "--orchestrator",
        "--output",
        "--repo-root"
      ],
      "guardrails": [
        "blender_runtime_guardrail",
        "patch_application_reported",
        "provider_execution_reported",
        "sqlite_awareness"
      ]
    },
    {
      "path": "Tools/ai/artifact_domain_registry.py",
      "extension": ".py",
      "category": "support_tool",
      "owner_lane": "cpu_support",
      "consumed_by_lanes": [
        "cpu",
        "npu"
      ],
      "provider_execution_default": "none_or_reported",
      "apply_mode": "report_only",
      "lines": 217,
      "symbols": [
        "ArtifactDomain",
        "get_domain",
        "list_domains",
        "registry_guardrails",
        "registry_report",
        "to_report_dict",
        "validate_domain",
        "validate_registry"
      ],
      "flags": [],
      "guardrails": [
        "output_artifacts_guardrail",
        "patch_application_reported",
        "provider_execution_reported",
        "sqlite_awareness"
      ]
    },
    {
      "path": "Tools/ai/build_agent_agnostic_tool_inventory.py",
      "extension": ".py",
      "category": "agent_context_builder",
      "owner_lane": "npu_explicit_provider_tool",
      "consumed_by_lanes": [
        "cpu",
        "gpu_cuda",
        "npu"
      ],
      "provider_execution_default": "explicit_only",
      "apply_mode": "manual_review_only",
      "lines": 408,
      "symbols": [
        "ToolRecord",
        "apply_mode",
        "build_inventory",
        "build_records",
        "classify_category",
        "classify_owner_lane",
        "consumed_lanes",
        "extract_flags",
        "extract_guardrails",
        "extract_symbols",
        "iter_tool_files",
        "main",
        "now_iso",
        "provider_execution_default",
        "python_symbols",
        "read_text",
        "record_to_dict",
        "render_markdown",
        "repo_rel",
        "resolve_path",
        "summarize"
      ],
      "flags": [
        "--markdown-output",
        "--max-items-per-category",
        "--max-tools",
        "--output",
        "--repo-root",
        "--root",
        "--use-ollama"
      ],
      "guardrails": [
        "blender_runtime_guardrail",
        "manual_review_only",
        "no_blender_runtime",
        "npu_advisory_guardrail",
        "openvino_gpu_primary_guardrail",
        "output_artifacts_guardrail",
        "patch_application_reported",
        "provider_execution_reported",
        "read_only",
        "sqlite_awareness"
      ]
    },
    {
      "path": "Tools/ai/build_agent_memory_inventory.py",
      "extension": ".py",
      "category": "agent_context_builder",
      "owner_lane": "cpu_context_builder",
      "consumed_by_lanes": [
        "cpu",
        "npu"
      ],
      "provider_execution_default": "none_or_reported",
      "apply_mode": "report_only",
      "lines": 397,
      "symbols": [
        "build_inventory",
        "main",
        "quote_identifier",
        "read_sqlite_metadata",
        "render_markdown",
        "resolve_path",
        "safe_rel",
        "selected_memory_preview",
        "summarize_records"
      ],
      "flags": [
        "--markdown-output",
        "--max-memory-chars",
        "--max-policy-items",
        "--max-preview-records",
        "--max-sqlite-tables",
        "--memory-db",
        "--memory-db-limit",
        "--memory-jsonl",
        "--objective",
        "--output",
        "--repo-root"
      ],
      "guardrails": [
        "blender_runtime_guardrail",
        "no_blender_runtime",
        "patch_application_reported",
        "provider_execution_reported",
        "read_only",
        "sqlite_awareness"
      ]
    },
    {
      "path": "Tools/ai/build_agent_review_code_patch_plan.py",
      "extension": ".py",
      "category": "agent_context_builder",
      "owner_lane": "npu_explicit_provider_tool",
      "consumed_by_lanes": [
        "cpu",
        "gpu_cuda",
        "npu"
      ],
      "provider_execution_default": "none_or_reported",
      "apply_mode": "report_only",
      "lines": 499,
      "symbols": [
        "build_code_patch_plan",
        "build_plan",
        "build_report",
        "build_static_plans",
        "check_is_clean",
        "edit_strategy_for",
        "first_safe_action_hint",
        "list_field",
        "list_len",
        "main",
        "plan_from_check",
        "plan_from_static_recommendation",
        "rationale_for",
        "render_inputs",
        "render_markdown",
        "render_plans",
        "render_skipped",
        "risk_for",
        "should_consider_check",
        "source_kind_for",
        "static_rationale_for",
        "static_strategy_for",
      
```

### `output/ai_pipeline/shared_toolbox_refactor_agnostic_tool_inventory_20260503-082504.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `15326`
- SHA-256: `514cbda8813b627d11c3d94a84dd5ed22784bed770ac0c675d28c812bd9ccf4b`
- Content included: `True`
- Content truncated: `True`

```text
# Agent Agnostic Tool Inventory

- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Tool count: `216`

## category_counts

- `validator`: 71
- `provider_probe_or_adapter`: 46
- `support_tool`: 38
- `orchestrator_pipeline`: 31
- `git_helper`: 10
- `agent_context_builder`: 9
- `proposal_or_review_builder`: 7
- `review_helper`: 4

## owner_lane_counts

- `npu_explicit_provider_tool`: 78
- `gpu_cuda_explicit_provider_tool`: 40
- `cpu_validation`: 37
- `cpu_support`: 34
- `cpu_orchestration`: 19
- `cpu_context_builder`: 4
- `cpu_proposal_builder`: 4

## consumed_lane_counts

- `cpu`: 216
- `npu`: 158
- `gpu_cuda`: 116

## apply_mode_counts

- `not_declared`: 127
- `report_only`: 60
- `manual_review_only`: 21
- `explicit_git_operation`: 8

## provider_execution_default_counts

- `none_or_reported`: 196
- `explicit_only`: 20

## Categories

### support_tool

- `Tools/ai/agent_memory_policy.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/agent_memory_routing_policy.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/agent_runtime_sqlite_memory.py` lane=`cpu_support` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/agent_runtime_tool_broker.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/artifact_domain_registry.py` lane=`cpu_support` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_code_interpreter_report.py` lane=`cpu_support` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_code_patch_artifact_pack.py` lane=`cpu_support` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_code_patch_docs_followup.py` lane=`cpu_support` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_dry_run_matrix_evidence_bundle.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_gpu_repair_failure_recommendation.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_music_intermediates.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/code_patch_plan_common.py` lane=`cpu_support` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/merge_ai_candidates.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/model_json.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/pipeline/__init__.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/pipeline/cli.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/pipeline/compat.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/pipeline/defaults.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/pipeline/guardrail_models.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`

### agent_context_builder

- `Tools/ai/agent_state.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_agent_agnostic_tool_inventory.py` lane=`npu_explicit_provider_tool` apply=`manual_review_only` provider=`explicit_only`
- `Tools/ai/build_agent_memory_inventory.py` lane=`cpu_context_builder` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_agent_review_code_patch_plan.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_agent_review_evidence_sufficiency.py` lane=`cpu_context_builder` apply=`manual_review_only` provider=`none_or_reported`
- `Tools/ai/build_agent_review_patch_plan.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_agent_state_packet.py` lane=`cpu_context_builder` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_agent_transient_request_context.py` lane=`cpu_context_builder` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_ai_context_pack.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`

### provider_probe_or_adapter

- `Tools/ai/analyze_gpu_npu_run_sync.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_analysis_input_bundle.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_local_ai_enrichment_plan.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_selective_execution_plan.py` lane=`npu_explicit_provider_tool` apply=`manual_review_only` provider=`none_or_reported`
- `Tools/ai/build_workload_quality_lane_routing.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/run_agent_gpu_deep_planning_supervised.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`explicit_only`
- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`explicit_only`
- `Tools/ai/run_local_provider_probe.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`explicit_only`
- `Tools/ai/run_megalithic_repo_review.py` lane=`npu_explicit_provider_tool` apply=`manual_review_only` provider=`explicit_only`
- `Tools/ai/run_npu_decode_smoke_diagnostic.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`explicit_only`
- `Tools/ai/run_npu_gpu_deep_review_auditor.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`explicit_only`
- `Tools/ai/workload_quality.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/npu/ai_memory_context.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/npu/build_ai_service_packet.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/npu/build_blender_manual_context.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/npu/build_music_context.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`explicit_only`
- `Tools/npu/build_npu_code_context.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/npu/build_npu_knowledge_broker_packet.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/npu/build_project_ai_index.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/npu/build_provider_result_report.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`

### proposal_or_review_builder

- `Tools/ai/build_code_edit_proposal_from_plan.py` lane=`cpu_proposal_builder` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_full_context_golden_proposals.py` lane=`npu_explicit_provider_tool` apply=`manual_review_only` provider=`none_or_reported`
- `Tools/ai/build_megalithic_review_pr_draft.py` lane=`npu_explicit_provider_tool` apply=`manual_review_only` provider=`none_or_reported`
- `Tools/ai/build_patch_specs_from_proposals.py` lane=`cpu_proposal_builder` apply=`manual_review_only` provider=`none_or_reported`
- `Tools/ai/build_repository_change_proposals.py` lane=`npu_explicit_provider_tool` apply=`manual_review_only` provider=`explicit_only`
- `Tools/ai/code_edit_proposal_helpers.py` lane=`cpu_proposal_builder` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/promote_patch_spec_draft.py` lane=`cpu_proposal_builder` apply=`manual_review_only` provider=`none_or_reported`

### git_helper

- `Tools/ai/build_github_evidence_bundle.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/enrich_github_evidence_bundle_code_plan.py` lane=`cpu_support` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/github_evidence_bundle_artifacts.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/github_evidence_bundle_decisions.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/github_evidence_bundle_io.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/github_evidence_bundle_markdown.py` lane=`cpu_support` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/github_evidence_bundle_reports.py` lane=`cpu_support` apply=`report_only` provider=`none_or_reported`
- `Tools/git/auto_push_generated_artifacts.ps1` lane=`cpu_support` apply=`explicit_git_operation` provider=`none_or_reported`
- `Tools/git/auto_push_generated_data.ps1` lane=`cpu_support` apply=`explicit_git_operation` provider=`none_or_reported`

### validator

- `Tools/ai/check_local_resource_lanes.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/check_npu_provider_environment.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/gpu_planner_json_contract.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/pipeline/artifact_contracts.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/replay_gpu_planner_json_contract.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/validation/ai_pipeline_report_contracts.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/apply_docs_contract_drift_fixes.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/validation/build_python_line_count_csv.py` lane=`cpu_validation` apply=`report_only` provider=`none_or_reported`
- `Tools/validation/check_agent_memory_policy.py` lane=`cpu_validation` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/check_ai_context_pack_contract.py` lane=`cpu_validation` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/check_ai_dry_run_matrix_cases.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/check_ai_dry_run_matrix_contract.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/check_ai_dry_run_matrix_outputs.py` lane=`cpu_validation` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/check_ai_model_json.py` lane=`cpu_validation` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/check_ai_pipeline_modules.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/check_ai_pipeline_report_contract.py` lane=`cpu_validation` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/check_ai_workload_report_quality.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/validation/check_artifact_domain_registry.py` lane=`cpu_validation` apply=`report_only` provider=`none_or_reported`
- `Tools/validation/check_blender_shared_compat_smoke.py` lane=`cpu_validation` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/check_code_contract_drift.py` lane=`npu_explicit_provider_tool` apply=`manual_review_only` provider=`explicit_only`

### review_helper

- `Tools/ai/refine_megalithic_review_signals.py` lane=`gpu_cuda_explicit_provider_tool` apply=`manual_review_only` provider=`none_or_reported`
- `Tools/ai/review_agent_memory.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/review_wave_entrypoints.py` lane=`cpu_support` apply=`not_declared` provider=`explicit_only`
- `Tools/ai/run_agent_gpu_deep_planning_review.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`explicit_only`

### orchestrator_pipeline

- `Tools/workflow/ai_runtime_diagnostics.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/artifact_consult.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/asset_inventory.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/git_auto_push.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/gui/components/__init__.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/gui/components/action_panel.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/gui/components/artifact_browser.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/gui/components/live_output_panel.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/gui/components/session_overview.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/gui/components/st_theme.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/gui/components/storage_dashboard.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/gui/workflow_gui.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/gui/workflow_gui_modern.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/gui/workflow_gui_with_push.py` lane=`cpu_orchestration` apply=`n
```

### `output/validation/shared_toolbox_refactor_bundle_smoke_20260503-082504.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `528`
- SHA-256: `356693ed14775e70d653852aa2d81bff5429edb293e08b227e4c958f8f7843d0`
- Content included: `True`
- Content truncated: `False`

```text
# Shared Toolbox AI-to-AI Bundle Builder Smoke

- passed: True
- provider_execution_performed: True
- patch_application_performed: False
- sqlite_write_performed: False
- persistent_memory_write_performed: False
- final_summary_json_exists: True
- final_summary_markdown_exists: True
- bundle_json_exists: True
- bundle_markdown_exists: True
- bundle_validation_passed: True
- recursive_defaults_enabled: True
- recursive_default_files_seen: True
- chunked_large_files_seen: True
- chunk_next_pointer_seen: True

```

### `output/validation/shared_toolbox_refactor_memory_routing_20260503-082504.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3333`
- SHA-256: `4e31aff1762c269821c08899f3b6955a1b52ce336c37f03dd2df04769c4a1f5b`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Memory Routing Policy

- passed: `True`
- profile: `full_refactor`
- broker_request_written: `output/ai_runtime_tools/agent_memory_routing_policy_tool_requests.json`
- provider_execution_performed: `False`
- patch_application_performed: `False`
- sqlite_write_performed: `False`
- persistent_memory_write_performed: `False`
- operational_sqlite_write_performed: `False`

- Objective: `Audit shared toolbox duplicated code and verify refactoring after PR142/PR143.`

## Memory plan
- `persistent_read_only`: `True`
- `persistent_query_count`: `4`
- `operational_query_or_write_count`: `3`
- `operational_write_request_count`: `0`
- `tool_request_count`: `15`

## Tool requests

- `persistent_memory_status` -> `runtime_sqlite_memory`: Inspect persistent/consistent memory status in read-only mode.
- `operational_memory_status` -> `runtime_sqlite_memory`: Inspect scratch operational memory status for the current runtime cycle.
- `persistent_memory_search_01` -> `runtime_sqlite_memory`: Search durable memory read-only for stable project facts and validated lessons.
- `persistent_memory_search_02` -> `runtime_sqlite_memory`: Search durable memory read-only for stable project facts and validated lessons.
- `persistent_memory_search_03` -> `runtime_sqlite_memory`: Search durable memory read-only for stable project facts and validated lessons.
- `operational_memory_search_01` -> `runtime_sqlite_memory`: Search scratch operational memory for current-cycle state and recent tool results.
- `operational_memory_search_02` -> `runtime_sqlite_memory`: Search scratch operational memory for current-cycle state and recent tool results.
- `agent_memory_inventory` -> `build_agent_memory_inventory`: Build read-only inventory of persistent memory before deciding whether more durable context is needed.
- `agnostic_tool_inventory` -> `build_agent_agnostic_tool_inventory`: Discover existing reusable tools/helpers before proposing new code or refactors.
- `transient_request_context` -> `build_agent_transient_request_context`: Create request-scoped context packet from objective and memory notes.
- `python_line_count_inventory` -> `build_python_line_count_csv`: Build complete Python inventory before choosing refactor candidates.
- `code_interpreter_report` -> `build_code_interpreter_report`: Build static code report over existing tool roots before proposing refactor seams.
- `python_syntax_check` -> `check_python_syntax`: Validate repository Python syntax as a safe baseline.
- `gpu_contract_smoke` -> `run_gpu_planner_json_contract_smoke`: Validate planner JSON contract helpers before planner integration.
- `validation_report_contract` -> `check_validation_report_contract`: Validate existing validation report contracts for evidence quality.

## Guardrails

- `free_shell_allowed`: `False`
- `broker_allowlist_required`: `True`
- `persistent_memory_read_only`: `True`
- `persistent_memory_write_performed`: `False`
- `sqlite_write_performed`: `False`
- `operational_memory_write_allowed_under_output`: `True`
- `automatic_persistent_promotion_allowed`: `False`
- `manual_review_required_for_promotion`: `True`
- `provider_execution_performed`: `False`
- `patch_application_performed`: `False`
- `blender_runtime_touched`: `False`
- `git_write_performed`: `False`

```

### `output/validation/shared_toolbox_refactor_python_line_count_20260503-082504.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1738`
- SHA-256: `2f326c52d87329dbe485dd7b96b7efac5db8d6da81a60b0560655277367eda4c`
- Content included: `True`
- Content truncated: `False`

```text
# Python Line Count CSV

- Passed: `True`
- CSV: `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260503-082516.csv`
- File count: `291`
- Total lines: `83302`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Largest Python files

- `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py` — `2197` lines
- `Tools/npu/run_dual_ai_pipeline.py` — `1773` lines
- `old script legacy/spaziotempo_asset_visual_v61.py` — `1513` lines
- `Scripting/v61b/scene_tuning_panel.py` — `1262` lines
- `Tools/workflow/workflow_state.py` — `1230` lines
- `old script legacy/spaziotempo_asset_visual_v6.py` — `1174` lines
- `Scripting/v61b_backgood/scene_tuning_panel.py` — `1097` lines
- `Scripting/v61b/animation.py` — `1079` lines
- `Scripting/v61b_backgood/animation.py` — `1019` lines
- `old script legacy/spaziotempo_album_visual_v5.py` — `969` lines
- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` — `888` lines
- `Tools/ai/run_agent_gpu_deep_planning_supervised.py` — `814` lines
- `Tools/ai/run_agent_gpu_deep_planning_review.py` — `812` lines
- `Tools/workflow/gui/workflow_gui.py` — `738` lines
- `Scripting/v61b/physics_setup.py` — `737` lines
- `Scripting/v61b/asset_setup.py` — `725` lines
- `Scripting/v61b_backgood/asset_setup.py` — `725` lines
- `Scripting/v61b_backgood/physics_setup.py` — `720` lines
- `Tools/npu/build_music_context.py` — `711` lines
- `old script legacy/spaziotempo_album_visual_v3.py` — `710` lines

## Guardrail

This artifact is line-count evidence only. It is not a patch plan and it must not be committed from `output/**`.

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
