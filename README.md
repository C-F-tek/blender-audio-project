# IA-Carmine Local AI Orchestration Workbench

`C-F-tek/blender-audio-project` is now primarily a local AI orchestration, validation, telemetry, evidence and guardrail workbench.

The repository name is historical. Blender/audio remains the first application domain, but the active architecture is app-agnostic AI/backend orchestration.

## GitHub About description

Recommended repository description:

```text
IA-Carmine local AI orchestration workbench for code-driven validation, provider lanes, runtime telemetry, evidence bundles and reviewable PR automation.
```

Recommended topics:

```text
local-ai, ai-orchestration, validation, telemetry, evidence, openvino, ollama, npu, gpu, powershell, python, automation
```

This field is GitHub repository metadata, not a tracked source file. Keep the GitHub About/Description aligned with this README and `AGENTS.md` whenever the project identity changes.

## First rule: read, inspect, reuse, then change

Before proposing or editing:

```text
read current source/canonical docs
inspect existing owners and nearby helpers
reuse existing scripts/helpers first
propose the smallest safe change
then modify docs/source
```

Canonical rule:

```text
docs/LOCAL_AI_TASKS/read-first-reuse-first-small-files-rule-2026-05-07.md
```

## Current operating doctrine: run unica real product

The current product doctrine is one controlled entry, one dynamic heap/exchange center and one validated product exit.

```text
operator product entrypoint = Tools/workflow/run_unified_real_product_pr.ps1
internal dynamic launcher = Tools/workflow/run_unified_local_ai_refactor.ps1
active_perimeter = whole-repository guarded heap/team runtime lanes
single_dynamic_heap_exchange_run = current report/manifest model
quick/balanced/deep/custom = intensity or budget, not reduced semantic scope
-No* flags = explicit opt-out from selected lanes
-NoStrictRealRunActivation = single-phase diagnostics only
```

Full local-AI work remains **TUTTO SU TUTTO**, but not by blindly executing every script. It means every relevant mapped, guarded, observable and evidence-producing capability can be selected, coordinated, validated and reported inside the run-unica model.

## Current runtime boundary

Canonical operating model:

```text
docs/LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md
docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
docs/MAIN_RUNTIME_ARCHITECTURE.md
```

Current boundary:

```text
IN
  Task MD or generated process-gate task
  mandatory real product preflight
  RepoPy/PYTHONPATH gate
  inventories/context/agent-state
  workload/capability evidence

LOOP / HEAP / EXCHANGE
  dynamic heap knowledge surface
  GPU1/Ollama advisory lane
  GPU0/OpenVINO observable support workload
  NPU micro peer diagnostic/report lane
  provider/context/broker lanes
  runtime state and public exchange events

OUT
  heap exchange exit product
  runtime evidence correlation
  repository change proposals
  generated patch specs with concrete deterministic operations
  lifecycle/final product validation
  agent_review_prepare_pr.py
  draft review PR product when requested
```

The center is dynamic. Entry and exit are controlled.

Do not claim that a lane executed unless manifest, telemetry, provider diagnostics or validator evidence proves it.

## Main runtime architecture

Current target topology:

```text
shared runtime heap / blackboard
├─ GPU1 primary advisory / Ollama planner
├─ GPU0 OpenVINO observable support workload
├─ NPU peer micro diagnostic/report lane
├─ broker unico executor
├─ semantic tools registry
├─ deterministic validators / CPU authority
├─ generated patch-spec product lane
└─ telemetry/event stream
```

Runtime meaning:

```text
provider lanes advise, classify, plan or respond through explicit roles;
broker unico executor is the execution gateway for registered tools;
semantic tools registry is the capability source of truth;
deterministic CPU validators remain local pass/fail authority;
telemetry/event stream records executed, skipped, degraded and blocked phases;
generated patch specs are product only when they carry concrete deterministic operations.
```

This architecture is implemented incrementally. Architecture targets do not authorize source writes, provider execution, patch application, Blender runtime, FFmpeg runtime, commit, push, merge or delete by themselves.

## Canonical code-driven reading flow

```text
AGENTS.md
  -> CHATGPT.md
  -> CHATGPT/README.md
  -> docs/README.md
  -> docs/LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md
  -> docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md
  -> docs/LOCAL_AI_TASKS/documentation-code-alignment-audit-2026-05-10.md
  -> docs/LOCAL_AI_TASKS/problems-and-hygiene-candidates-2026-05-10.md
  -> docs/LOCAL_AI_TASKS/md-line-budget-triage-2026-05-10.md
  -> docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
  -> docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
  -> docs/LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md
  -> docs/LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md
  -> docs/LOCAL_AI_TASKS/script-aging-visibility-audit-2026-05-09.md
  -> docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
  -> docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
  -> docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
  -> docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
  -> docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
  -> docs/MAIN_RUNTIME_ARCHITECTURE.md
  -> docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
  -> docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
  -> task-specific docs / package README / target source file
```

Historical handoffs, old `current-*` docs, generated evidence and monolithic runbooks are context only. They do not override current source code, owner maps, launcher manifests or validation evidence.

The root README is descriptive only. It must not carry long executable PowerShell command blocks because launcher options change faster than project identity docs.

## Current local AI entrypoints

Operator-facing real product entrypoint:

```text
Tools/workflow/run_unified_real_product_pr.ps1
```

Internal dynamic launcher and diagnostic entrypoint:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Canonical runbooks/contracts:

```text
docs/LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md
docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

Use those documents for current commands, intensity profiles, provider flags, reset mode, memory controls, patch-spec generation, review-PR options and validation modes.

## Current product path: Markdown input to review PR

A valid product run starts from a controlled task Markdown file or generated process-gate task, enters the dynamic heap/exchange with context and lane evidence, and exits only through deterministic product validation.

Current chain:

```text
run_unified_real_product_pr.ps1
  -> Task MD or generated process-gate task
  -> mandatory real product preflight
  -> run_unified_local_ai_refactor.ps1
  -> inventories/context/agent-state/workload-quality
  -> heap/exchange runtime entry and peer manifest
  -> GPU1/GPU0/NPU/provider lanes
  -> runtime evidence correlation
  -> repository change proposals
  -> generated patch specs
  -> generated patch-spec apply report
  -> agent_review_prepare_pr.py
  -> final review PR product contract
  -> draft review PR for manual review when selected
```

Current deterministic source-write boundary for patchkit bundles:

```text
Tools/ai/patchkit/apply_patch_bundle.py
```

Current generated review product boundary:

```text
Tools/ai/build_repository_change_proposals.py
Tools/ai/generated_patch_specs/proposal_cli.py
Tools/ai/generated_patch_specs/apply_cli.py
Tools/ai/agent_review/review_pr_cli.py
Tools/validation/repository_product/review_pr_final_product_contract/cli.py
```

Metadata-only patch drafts are not enough for a successful review-PR product. `operation_count=0` under generated patch-spec apply is a hard failure.

## Current stable docs

| Need | Start here |
|---|---|
| Agent contract and guardrails | `AGENTS.md` |
| ChatGPT/session memory and handoff notes | `CHATGPT.md`, then `CHATGPT/README.md` |
| Documentation index | `docs/README.md` |
| Real product run documentation router | `docs/LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md` |
| Real product run-unica runbook | `docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md` |
| Documentation/code alignment audit | `docs/LOCAL_AI_TASKS/documentation-code-alignment-audit-2026-05-10.md` |
| Problems and hygiene candidates | `docs/LOCAL_AI_TASKS/problems-and-hygiene-candidates-2026-05-10.md` |
| Markdown line-budget triage | `docs/LOCAL_AI_TASKS/md-line-budget-triage-2026-05-10.md` |
| Heap/exchange and patchkit model | `docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md` |
| AI first-orientation map | `docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md` |
| Current code/state bridge | `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` |
| Current capability depth | `docs/LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md` |
| Launcher parameter decision map | `docs/LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md` |
| Script aging / hidden wrapper review | `docs/LOCAL_AI_TASKS/script-aging-visibility-audit-2026-05-09.md` |
| Code-derived current behavior | `docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md` |
| Script census and run variants | `docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md` |
| Single-owner scripts / do-not-bypass rules | `docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md` |
| Operational data-flow variants | `docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md` |
| Validator and smoke cycles | `docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md` |
| Main runtime architecture | `docs/MAIN_RUNTIME_ARCHITECTURE.md` |
| Unified launcher manifest contract | `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` |
| Unified launcher internal workflow | `docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` |
| Validators and inventories | `Tools/validation/README.md` and validator-smoke map |
| NPU/helper package | `Tools/npu/pipeline/README.md` |
| Repository area map | `docs/MODULE_MAP.md` |
| Documentation map and pruning | `docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md` |
| Workflow helper policy | `docs/WORKFLOW_HELPER_SCRIPTS_POLICY.md` |

## Full-run handoff completeness

A production run-unica handoff is not complete from evidence or patch plan alone.

Review this group together:

```text
wrapper report when product path was used
launcher manifest
phase_status / phase_reports
mandatory preflight report
heap/exchange runtime entry
heap peer runtime manifest
heap/exchange runtime exit product
heap/exchange lifecycle report
runtime evidence correlation
repository change proposals
generated patch-spec manifest and apply report
review PR prepare report
final review PR product contract
evidence artifacts
runtime_tool_usage_telemetry_<STAMP>.json/md
runtime_tool_capability_manifest_<STAMP>.json/md
full_toolbox_run_telemetry_summary_<STAMP>.json/md
shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
CSV/count summaries when inventory lanes ran
discovery/index repair reports when relevant
file-line-limit reports when maintainability is in scope
blackboard/broker/registry/validator/event-stream reports when implemented
```

Never infer success only from file existence, focused validator output, dry-run matrix output, provider report existence, NPU smoke, patch plan existence or large Markdown text.

## File-size and Markdown split rule

Maintained documentation and source files must stay reviewable.

```text
preferred active runbook <= 400 lines
active Markdown hard threshold <= 500 lines
maintained source/script target <= 400 lines
```

Markdown split layout is exact:

```text
path/name.md
path/name.md/part-001.md
path/name.md/part-002.md
```

Legacy extensionless split folders are historical only. Do not copy them for new splits.

## Operating rules

Do not infer project state from the repository name. Current core/backend work must not:

```text
modify Blender runtime packages without explicit scope
produce audio playback/export or media output
run FFmpeg encode/mux or Blender render
modify full analysis JSON files
commit output/**, renders/**, generated media, *.db or *.sqlite
hand-edit generated indexes
reintroduce retired legacy compatibility naming as runtime semantics
promote NPU/OpenVINO to compute-provider lane without quality-gated architecture change
claim GPU0 success from device visibility only
claim metadata-only generated patch specs as reviewable product
create tool execution paths outside broker/registry/validator/telemetry architecture
merge to master without explicit user command
```

Use compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/` instead of raw `output/**` reports.

## Audio/media output policy

Normal AI/tooling runs are evidence/report workflows, not media-generation workflows.

Forbidden unless explicitly scoped as application-domain work:

```text
audio playback
audio export
WAV/MP3/AAC conversion
FFmpeg encode/mux
Blender render
video generation
media output side effect
```

Detailed policy:

```text
docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md
```

## Inventory and evidence

Current documentation cleanup and refactoring use:

```text
Markdown inventory
script/function/class/method inventory
script aging / hidden wrapper audit
CSV/count evidence surfaces
auto-discovery and index repair reports/plans
tool placement audit
validation report contracts
runtime broker telemetry
runtime evidence correlation
repository change proposals
generated patch-spec apply reports
compact GitHub evidence bundles
heap/exchange lifecycle evidence
patchkit reports
```

Commands for these tools live in the real product runbook, unified launcher runbook and tool-specific README files, not in this root README.

## GitHub / PR description policy

GitHub PR descriptions and repository-facing summaries should point to canonical docs instead of duplicating executable commands.

Required wording principle:

```text
Root/project descriptions describe purpose and canonical docs.
Operational commands live in docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md and docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md.
Runtime architecture lives in docs/MAIN_RUNTIME_ARCHITECTURE.md and the heap/exchange operating model.
The GitHub About description must not describe this as only a Blender/audio project.
```

## Legacy Blender/audio role

The repository still contains mature Blender/audio-reactive workflows under `Scripting/`, including `Scripting/v61b/` and shared helpers.

Treat them as application-domain assets. Do not refactor or run them unless the task explicitly enters that milestone.
