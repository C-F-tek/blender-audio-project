# Code-derived AI toolchain map — 2026-05-07

Status: active code-derived map  
Scope: IA-Carmine launcher, full-toolbox engine, provider mesh, patch suggestion final phase, review PR preparation.

This document starts from source code and states current behavior. It is not a future architecture wish list.

## Source files inspected

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
Tools/workflow/run_agent_review_full_toolbox_decision_loop.py
Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_engine.py
Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_mesh.py
Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_product.py
Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_support.py
Tools/ai/apply_patch_suggestion_bundle.py
Tools/ai/patch_suggestion_bundle/cli.py
Tools/ai/patch_suggestion_bundle/common.py
Tools/ai/patch_suggestion_bundle/product.py
Tools/ai/prepare_review_pr.py
Tools/validation/check_patch_suggestion_product_separation.py
```

## Operator-facing entrypoint

Current active entrypoint:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

It owns:

```text
mode selection
Stamp propagation
Python resolution
PYTHONPATH setup
strict real-run activation
Full0To10 mode expansion
LightFull0To10 dispatch
reset planning
phase report manifest
optional review-PR product phase
```

The launcher is report/proposal-only by default. Patch application, commit, push and PR creation are separate explicit options.

## Python selection policy

Resolution order in launcher code:

```text
-PythonExe
env:IA_CARMINE_PYTHON
<repo>/.venv/Scripts/python.exe
<repo>/venv/Scripts/python.exe
<repo>/.venv314/Scripts/python.exe
auto-bootstrap .venv with py -3.12 or py -3.13
python fallback
```

Provider-capable runs should set:

```powershell
$env:IA_CARMINE_PYTHON = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:PYTHONPATH = (Resolve-Path .).Path
```

Expected provider visibility on the IA-Carmine workstation:

```text
CPU, GPU.0, GPU.1, NPU
```

## Strict real-run activation

The launcher prints and implements strict real-run activation. A non-smoke/non-reset run can be promoted to TUTTO SU TUTTO unless explicitly disabled.

For phase diagnostics, always pass:

```text
-NoStrictRealRunActivation
```

Observed diagnostic pitfall:

```text
-Mode md without -NoStrictRealRunActivation can start full-toolbox provider processes.
That may include run_agent_review_full_toolbox_decision_loop.py,
run_agent_gpu_npu_parallel_orchestrator.py,
run_agent_gpu_deep_planning_supervised.py and ollama.exe runner.
```

## Full-toolbox Python engine

`Tools/workflow/run_agent_review_full_toolbox_decision_loop.py` is the wrapper. By default it runs the Python production engine. The old PowerShell implementation is used only with `--UseLegacyPowerShellImplementation`.

Python engine modules:

```text
py_engine.py   = workflow orchestration and static foundation
py_mesh.py     = provider mesh, peer exchange, runtime heap/broker surfaces
py_product.py  = decision-loop, summaries, bundle/evidence/product reports
py_support.py  = paths, command execution, Python resolution, summaries
```

`py_engine.py` requires `--Stamp`; no stamp means the Python full-toolbox engine fails fast.

## Static foundation lane

The Python engine builds a deterministic foundation before provider execution:

```text
provider runtime heap live init
full memory/tool regeneration unless skipped
Python line-count inventory
Python syntax validation
code interpreter/static report
compile targets for core AI/validation scripts
GPU planner contract smoke
deterministic recommendation synthesizer smoke
agent review decision-loop smoke
NPU provider environment preflight
OpenVINO hardware governance report
repository consistency map and smoke
megalithic project review/refinement
evidence sufficiency report
GPU0 companion task lane and contract
```

These are deterministic/report lanes. They are not source mutation lanes.

## Provider mesh lane

Provider mesh runs only when `RunGpuNpuProvider` is true.

When enabled, `py_mesh.py` calls:

```text
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py
```

with budget/context/token parameters and runtime broker/heap paths.

Provider roles from current code:

```text
GPU1/Ollama = primary advisory orchestrator
GPU0/OpenVINO = peer support provider / companion worker
NPU = micro support lane, usually deferred/non-blocking unless explicitly configured
runtime broker = controlled tool execution surface
runtime heap = event/snapshot evidence surface
```

Legacy NPU auditor is not default. It runs only when `RunLegacyNpuAuditorProvider` is selected.

## Peer exchange lane

Peer exchange requires provider execution and a GPU primary report. When present, it runs:

```text
build_ai_peer_exchange_packet.py
run_gpu0_peer_companion_worker.py
agent_runtime_tool_broker.py for GPU0 requests
optional NPU micro peer assistant or non-blocking placeholder
check_ai_peer_exchange_contract.py
build_provider_runtime_heap_from_peer_reports.py
build_provider_runtime_heap_telemetry.py
check_provider_evidence_contract.py
```

If NPU peer provider is deferred, the code writes a non-blocking placeholder instead of treating that as product failure.

## Patch suggestion final phase

Current implementation is explicit and conservative:

```text
apply_patch_suggestion_bundle.py / patch_suggestion_bundle.cli
```

It can:

```text
discover stamped suggestion/proposal JSON reports
include current repository_update_suggestions/repository_change_proposals
dedupe explicit --suggestion-report paths against Stamp discovery through ReportPathNormalizer
perform dry-run report generation
apply deterministic operations only when --apply is supplied
create/switch an allowed review branch when requested
push that review branch when requested
separate product-facing and supplemental manual-review items
publish capped review-item lists while retaining total counts
```

It does not:

```text
run providers
commit
open a PR
merge
force-push
edit output/**, renders/**, generated chunks or DB/SQLite targets
```

## Product separation validator

Current validator:

```text
Tools/validation/check_patch_suggestion_product_separation.py
```

It is report-only. It accepts:

```text
kind=patch_suggestion_bundle_apply
kind=patch_suggestion_bundle_apply_smoke
```

It validates that product-facing patch suggestions are separate from telemetry/debug/supporting items.
The unified launcher runs this validator with `--require-product` after the patch suggestion final phase whenever review PR preparation or deterministic apply is selected.

## Review PR preparation

Current implementation:

```text
Tools/ai/prepare_review_pr.py
```

It requires explicit staging allowlist:

```text
--include-path
```

The launcher exposes this as:

```text
-ReviewPrIncludePath
```

It can:

```text
validate branch prefix
create/switch CARMINEai/* branch through shared git_branch helper
stage only allowlisted paths
reject staged paths outside allowlist
reject output/**, generated chunks, renders and DB/SQLite paths
commit staged product changes
push when requested
call gh pr create when requested
write review_pr_prepare JSON/MD reports
```

It does not currently:

```text
auto-discover include paths from patch_suggestion_bundle_apply results
create GitHub PRs as draft through --draft
merge PRs
force-push
```

Focused validation for the complete product PR chain:

```text
Tools/validation/run_full0to10_product_pr_chain_smoke.py
```

This smoke runs task Markdown extraction, deterministic apply, product
separation validation and review PR preparation together in a temporary git
repository. It also traces the canonical launcher source to verify the same
product phases are wired in the real workflow. It does not push or create a real PR.

## Current product gap

The target product is Markdown input to reviewable PR output. Current code is close, but still needs one implementation step for full automation:

```text
prepare_review_pr.py should derive safe include paths from patch_suggestion_bundle_apply results.
prepare_review_pr.py should support draft PR creation.
launcher should expose the draft/auto-include controls after code support lands.
```

Until then, production review PR runs must provide `ReviewPrIncludePath` explicitly.

## Documentation rule

Do not describe a capability as active unless the code implements it or a manifest/evidence report proves it ran.

Use this document to resolve ambiguity between historical handoffs, desired product behavior and current source-code behavior.
