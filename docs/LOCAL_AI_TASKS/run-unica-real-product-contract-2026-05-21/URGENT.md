# Urgent Run Unica Contract Notes

## Hard Rule

`run unica` must be one integrated recursive flow:

```text
single input / task file
-> file-backed runtime payload and dynamic context universe
-> startup/memory/RAG/tool/chunk preload
-> heap blackboard, pointer graph and revision context
-> GPU1 primary planner/proposal packet
-> async GPU0 packet_review_only coworker review/refine
-> async NPU packet_review_only controlled microtask audit
-> broker/native tool request-result evidence
-> GPU1 recovery/congruence turn consumes GPU0/NPU pointer ids
-> matrix/lab/debug/virtual-dev validation and patch candidate synthesis
-> PLAN_PRODUCT_FULL_PATCH.md technical prompt/chat/proposal product
-> CODE_PRODUCT_FULL_PATCH.md patch/code product when verified diff/code exists
-> final readable Documents package or typed blocked continuation
```

The final package must be reconstructed from heap memory, provider blocks,
pointer links and file-backed artifact refs produced at each round. It publishes
two sibling product surfaces: `PLAN_PRODUCT_FULL_PATCH.md` for the recomposed
GPU1 prompt/chat/proposal product, and `CODE_PRODUCT_FULL_PATCH.md` for the
verified patch/code product when an applicable diff/code product exists. It must
not depend on chat context, token window continuity, copied provider prose,
inline HTTP/report blobs or a second out-of-band flow.

`contractor_universe` is not excluded. Its `UniverseHeap`, `LogicalClock` and
contractor-role model describe the dynamic heap scheduler and soft-time closure
that must live inside the same run. The deterministic scaffold is not provider
proof by itself and must not become a parallel product entry.

Useful surfaces must be integrated into the one universe, not selected as
mutually exclusive paths:

```text
runtime universe / file-tool index
startup manifest, RAG hard surface and dynamic GPU1 context pack
tool catalog, native schemas and broker bridge
semantic code/evidence chunks
contractor_universe scheduler surface
GPU1 leader/proposal packet and closure decision
async GPU0/NPU packet_review_only sidecar collections
sidecar polling, recovery/congruence and consumed peer refs
runtime debug lab, virtual dev environment and code execution matrix
patch candidate synthesis and code-product intake boundary
external pointer manifest and revision context
final readable Documents package
PLAN_PRODUCT_FULL_PATCH.md technical product
CODE_PRODUCT_FULL_PATCH.md patch/code product
```

The operator-provided `deep-research-report (1).md` is useful research input.
Adopt its heap/clock/contractor and report-I/O ideas only when they reinforce
the single run-unica flow. Do not adopt its optional standalone dispatcher or
runtime selector as a second product entry.

The provider leader packet and dynamic GPU1 context pack must expose this as
`integrated_surface_map`, `contractor_universe_surface_contract`,
`sidecar_scope_mode=packet_review_only` and artifact refs so GPU1, GPU0 and NPU
operate inside the same heap/pointer universe without forcing GPU1 to wait for
sidecar completion before its next pointer/recovery step.

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
mechanics, CPU pressure, GPU/NPU probes or a violation of an operator stop.

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

## Operator Update 2026-05-24

The current direct command surface is valid when the dry run reports
`canonical_entrypoint=python -m ia_carmine.cli run`, all fields come from direct
CLI/profile-derived sources, and `--dry-run` performs no provider execution.
For this workstation the active command must keep:

```text
repo_root = C:\Users\carmi\ProjectsDir\blender-audio-project
python_exe = C:\Users\carmi\blender\blender-audio-project\.venv\Scripts\python.exe
request_file = docs\LOCAL_AI_TASKS\run-unica-real-product-contract-2026-05-21\URGENT.md
npu_model_dir = C:\Users\carmi\blender\npu-models\Phi-3.5-mini-instruct-int4-cw-ov
```

Current run-unica priority is not to make a stale static context file pass. The
startup/provider boundary must use the current dynamic surfaces:

```text
gpu1_dynamic_context_pack
rag_context_pack / hard RAG surface
runtime_file_refs
native broker tool schemas and tool request/result artifacts
file-backed provider prompts, responses, stdout/stderr and patches
```

HTTP/API boundaries coordinate `job_id`, `payload_file` and metadata only. Large
operator request text, GPU1 prompt/chat material, heap chunks, provider output,
patch candidates, stdout/stderr and debug logs must live on filesystem artifacts
with refs, bytes and sha256. Tail/excerpt fields are preview only. If a gate
needs semantic evidence and a full ref is missing or corrupt, the run must block
with a typed reason instead of accepting the tail.

GPU1 remains the primary reasoning and closure lane. This does not reduce GPU1
to a tool runner: GPU1 may produce prompt/chat/proposal/plan evidence, but
tool, lab, matrix, debug and patch validation count only through native broker
tool calls and deterministic artifacts. JSON/Markdown/prose that describes a
tool call is not executable evidence.

Terminal blockers must now be classified by cause:

```text
AI STAI GIOCANDO: fake tool/product/decision evidence was promoted
PROVIDER_START_BLOCKED: provider prereq missing, for example runtime_file_refs
LANE_UNVIABLE: required provider lane evidence missing or degraded
PRODUCT_ACCEPTANCE_BLOCKED: ready/product acceptance is not proven
CAUSALITY_BLOCKED: pointer/quorum/review chain is inconsistent
RECOVERY_REQUIRED: a valid recovery/refinement turn is required
METRIC_CONSISTENCY_BLOCKED: state counters contradict closure
PROVIDER_OUTPUT_CONTRACT_VIOLATION: provider emitted non-executable tool text
```

`AI STAI GIOCANDO` must not be attached to every failed run. A blocked run with
`runtime_file_refs_missing_before_provider_start` is a provider-start blocker,
not script-gaming. GPU0 free text used as product/decision is script-gaming.
Ready status with a missing matrix/lab/product acceptance blocker is product
acceptance failure. The Codex failure counters must follow those categories and
must not increment script-gaming only because a process returned nonzero.

For the run produced by the current command, the final decision must be read
from its own `intermediate_run_dir`, `final_root`, launcher summary and final
readable product package. Do not verify this run by sorting old output folders
or scraping the newest `operator_product_lab_summary.json` from an unrelated
run. If the product cannot close, the correct result is
`blocked_continuation_product` with typed blockers and resume/pointer evidence,
not an empty code product or a post-hoc success claim.

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
