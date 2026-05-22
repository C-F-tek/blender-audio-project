# Urgent Run Unica Contract Notes

## Hard Rule

`run unica` must be one integrated recursive flow:

```text
single input
-> universe creation
-> startup/memory/tool/chunk preload
-> heap blackboard and pointer graph
-> GPU1 primary planner
-> GPU0 coworker reviewer/refiner
-> NPU controlled microtask auditor
-> broker/tool evidence
-> matrix/lab and patch candidate synthesis
-> product bundle / CODE_PRODUCT_FULL_PATCH.md
```

The product bundle must be reconstructed from heap memory, provider blocks and
pointer links produced at each round. It must not depend on chat context, token
window continuity, copied provider prose or a second out-of-band flow.

`contractor_universe` is not excluded. Its `UniverseHeap`, `LogicalClock` and
contractor-role model describe the dynamic heap scheduler and soft-time closure
that must live inside the same run. The deterministic scaffold is not provider
proof by itself and must not become a parallel product entry.

Useful surfaces must be integrated into the one universe, not selected as
mutually exclusive paths:

```text
runtime universe / file-tool index
startup manifest and memory reload
tool catalog and broker bridge
semantic code/evidence chunks
contractor_universe scheduler surface
GPU1/GPU0/NPU provider teamwork packet
runtime debug lab and virtual dev environment
code execution matrix and patch candidate synthesis
external pointer manifest and revision context
final readable product / CODE_PRODUCT_FULL_PATCH.md
```

The operator-provided `deep-research-report (1).md` is useful research input.
Adopt its heap/clock/contractor and report-I/O ideas only when they reinforce
the single run-unica flow. Do not adopt its optional standalone dispatcher or
runtime selector as a second product entry.

The provider leader packet must expose this as `integrated_surface_map` and
`contractor_universe_surface_contract` so GPU1, GPU0 and NPU operate inside the
same heap/pointer universe.

Resource/provider preflight is not static inspection. A report can correctly
say `provider_execution_performed=false` and still have performed resource
mechanics such as Ollama availability checks or OpenVINO GPU/NPU device
enumeration. Those reports must expose separate pointer/counter evidence:

```text
resource_mechanics_performed
resource_probe_performed
mechanical_not_static_read
operator_authorization_required
```

The absence of provider generation must not be used to hide or soften resource
mechanics, CPU pressure, GPU/NPU probes or a violation of an operator block.

## Operator Evidence 2026-05-21

The operator reported this validation state:

```text
real_product_single_entry_exit_smoke: true
real_product_runtime_mesh_contract: true
real_product_intrinsic_capability_contract: false
  error: missing intrinsic capability: product_readiness
heap_startup_context_ingestion_smoke: true
patch_candidate_synthesis_smoke: true
heap_final_readable_product_smoke: true
  pointer_reconstruction_passed: true
```

Interpretation:

```text
single-entry/shared-controller shape now has local evidence
mesh shape evidence exists
startup/pointer/final-readable fixtures are useful
one real-product static contract is still failing: product_readiness
fixture passes do not prove a full provider/product run
resource-lane preflight is not authorized as a harmless test
```

Concrete correction scope:

```text
single entry visibly constructs the shared controller before controller.run
final readable product must expose truncation_marker in its own report
product_readiness must not be made to pass by editing validator/smoke logic
resource-lane reports must expose mechanics/probe counters separately
pointer manifests must preserve those mechanics counters when present
```

Deep-research report-I/O evidence:

```text
ia_carmine._shared.report_io exists and is the correct runtime-side home for
generic JSON/Markdown report I/O.
Many ia_carmine modules still import Tools.validation._shared.report_utils.
That remaining coupling is a known surface to decouple progressively.
It must not be used to claim validation is part of the runtime product core.
```

Provider Python contract evidence:

```powershell
$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:IA_CARMINE_PYTHON = $RepoPy
$env:PYTHONPATH = (Resolve-Path .).Path
```

This is defined by the project contract and runbooks. Do not answer with
generic Python path examples when the repository already defines `RepoPy` and
`IA_CARMINE_PYTHON`. `SPAZIOTEMPO_NPU_PYTHON` is a legacy/NPU fallback surface,
not the canonical run-unica provider Python contract.

Current workstation evidence:

```text
C:\Users\carmi\ProjectsDir\blender-audio-project\.venv\Scripts\python.exe = missing
C:\Users\carmi\blender\blender-audio-project\.venv\Scripts\python.exe = exists
```

For this active checkout, local commands must use the provider-capable Python
from the `blender` checkout while keeping `PYTHONPATH` pointed at the current
source checkout:

```powershell
$RepoRoot = (Resolve-Path .).Path
$RepoPy = "C:\Users\carmi\blender\blender-audio-project\.venv\Scripts\python.exe"
$env:IA_CARMINE_PYTHON = $RepoPy
$env:PYTHONPATH = $RepoRoot
```

Do not replace run-unica verification with a disconnected PowerShell scraper
that finds the newest `operator_product_lab_summary.json`. A script based on
`Get-ChildItem ... Sort-Object LastWriteTime` is not a single product surface,
not a single entrypoint and not parallel provider orchestration. It is only
post-hoc file discovery and can mix stale or unrelated artifacts. Operator
severity override for presenting this as verification: `100`.

The required variable for local command contracts is `$RepoRoot`, not an
invented `$Root` alias. Any operator-facing command sequence that changes this
variable name must be treated as untrusted unless the contract is explicitly
updated first.

`ia_carmine run` must expose run-unica values as direct CLI parameters. Do not
load operator-facing runtime values from a hidden external JSON parameter file.
That surface has been removed for this product path. The direct default is a
bounded spark/scintilla configuration. `--dry-run` is preview only; removing it
must request GPU1/GPU0/NPU provider generation by default.

A real run that produces an empty/no-applicable/no-diff
`CODE_PRODUCT_FULL_PATCH.md` must not continue into code-product intake. It
must exit as `blocked_with_reason` and write the Codex failure counters once for
the real blocked run.

The final product is not forced to be source code. The run has one canonical
product outcome, selected from:

```text
code_patch_product
text_product
technical_plan_product
diagnostic_decision_product
blocked_continuation_product
```

Code requires target/diff/validation. Text or plan products require a complete
operational document approved by the heap/pointer cycle. A partial provider
answer remains evidence. If the universe cannot close within the soft runtime
governors, the correct exit is `blocked_continuation_product` with
`resume_from_block_id`, not a hard empty product.

Preflight static failures from stale contract surfaces must be counted and
reported, but they must not skip startup/provider when
`product_entry_allowed=true`. Only real runtime blockers may stop startup.

## Provider Viability

For complete/full provider generation, all three provider roles are required:

```text
gpu1_planner
gpu0_reviewer_refiner
npu_auditor
```

Missing, failed, degraded, unavailable, unlinked or diagnostic-only lanes make
the complete run unviable. They are not warnings.

## Recovery State

`provider_graph_recoverable=true` means the same run universe can resume from
GPU1/GPU0/NPU provider evidence and request the missing
`HEAP_DELTA_PROPOSAL`.

It does not mean:

```text
proposal_graph_product_passed=true
final_product_passed=true
apply-ready patch exists
provider prose is product
```

The next action is `recover_missing_proposal_chunk` inside the run.

GPU0 may enrich the pointer graph with coherent information when a partial
answer is rejected:

```text
propagation_notes
script_or_text_delta_refs
previous/refines/resume pointer updates
response typology change request
return_to_main_block_id
```

The cycle then restarts inside the same heap with the rejected answer as
evidence. The first GPU1 turn may be a `PLAN_THEN_PROPOSAL` text plan only when
it explains the complete steps needed before code; that plan remains evidence,
not final product.

## Product Boundary

`CODE_PRODUCT_FULL_PATCH.md` is a real code product only when it contains a
reviewable, non-truncated `diff --git` block for verified repo-relative targets
or an explicit blocked/no-op state.

If provider blocks exist but no proposal chunk or patch candidate exists, the
correct output is blocked/recoverable evidence, not success.

## Operator-Local Check

Do not add or modify validator/smoke logic to satisfy this task. After the
product source change, use the direct contract command when the desired output
is `output/validation/real_product_intrinsic_capability_contract.json`:

```powershell
python -m Tools.validation check_real_product_intrinsic_capability_contract
Get-Content .\output\validation\real_product_intrinsic_capability_contract.json -Raw |
  ConvertFrom-Json |
  Select-Object passed, product_readiness, errors, warnings
```

The smoke command is separate and writes separate files:

```powershell
python -m Tools.validation run_real_product_intrinsic_capability_contract_smoke
Get-Content .\output\validation\real_product_intrinsic_capability_contract_smoke_contract.json -Raw |
  ConvertFrom-Json |
  Select-Object passed, product_readiness, errors, warnings
```

Expected invariant for both current reports:

```text
product_readiness == true only because final_readable_product exposes the
runtime code-product truncation marker evidence directly.
```

Legacy profile-based validators/smokes that read
`ia_carmine/runtime/run/profiles/heap_runtime_launcher_profiles.json` or
`ia_carmine/product/operator_product_core/profiles.py` are stale after removal of the
hidden JSON parameter surface. They are not the verification path for this
task unless their contract is explicitly rewritten later.
