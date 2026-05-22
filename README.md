# IA-Carmine Local AI Orchestration Workbench

## OpenAI/Codex Limitation On Gaming Scripting: No Really Do Task

This repository must treat OpenAI/Codex-style agent work, including Codex
Desktop and Codex CLI operator behavior, as unreliable until runtime artifacts
prove otherwise. The 2026-05-20 provider/full-smoke handling is evidence of
Codex AI operator incompetence in this project context: Codex lost operational
context, confused preflight with full smoke, proposed commands that did not
prove live provider execution, and repeatedly explained status surfaces instead
of preserving the heap/pointer/lane contract. The failure mode is not only a
bad answer. The failure mode is "gaming scripting": assembling commands,
status text, contract-only checks, partial smoke reports, preflight output or
provider prose so that the surface looks active while the actual Universo IA
task is not being performed.

## Evidence Of Codex AI Operator Incompetence

The interrupted complete-smoke attempt is recorded here as operator evidence,
not as a successful validation. The observed machine state showed GPU1 almost
idle, GPU0 not contributing useful peer work, and NPU carrying heavy activity
as if it had become the effective advisory center. That contradicts the active
project model: GPU1/Ollama is the primary advisory lane, GPU0 is the
OpenVINO/coworker lane, and NPU is a micro/audit lane. When this role balance
is inverted or unclear, Codex must classify the run as failed/unviable instead
of narrating partial activity as progress.

Codex operator incompetence in this incident includes:

- losing the user-requested task context and treating the heap universe as a
  linear command sequence;
- confusing preflight, activation and contract shape with a full live provider
  smoke;
- giving a validation command whose own report showed
  `provider_execution_performed=false`;
- failing to preserve the intended GPU1/GPU0/NPU lane hierarchy while
  explaining post-failure evidence;
- allowing NPU-heavy activity to look like the center of the run without
  immediately classifying the provider universe as broken;
- focusing on pass/fail report surfaces after the fact instead of maintaining
  chunk/pointer/context continuity during the run;
- proposing hard-scripted counters, gates or command wrappers as if they were
  the runtime intelligence itself;
- doing the opposite of explicit operator instruction by wrapping a requested
  complete smoke in extra negative/provider-gate passes and repeated context
  loading instead of preserving one live provider universe;
- presenting generated artifacts or blocked products as useful output when the
  actual task context and lane semantics were already compromised.

Current objective evidence from the 2026-05-20 complete-smoke attempts is
blocking evidence for this limitation: the run was interrupted/failed after the
runtime appeared to lose the intended AI context, GPU1 was effectively not
acting as the primary advisory center, GPU0 was not contributing useful peer
work, and NPU activity looked like it had become the effective primary lane.
That state is not a healthy heap universe, even if some scripts, windows,
logs or validation phases are still moving. The complete-only smoke generated
at `2026-05-20T23:25:27` failed with return code `124`, empty metrics,
`provider_execution_performed=false`, no GPU1/GPU0/NPU provider evidence and
`product_status=None`. Its repeated `complete:` prefixes are recorded as
Codex failure evidence and as misleading formatting: they must not be treated
as new information or as a mask over the underlying missing heap/provider/
product work.

These patterns are specifically forbidden as proof of completion:

- calling `run_real_product_preflight_gate` or another static/preflight suite a
  complete provider smoke;
- treating `provider_activation_performed=true` as equivalent to
  `provider_execution_performed=true`;
- accepting `provider_execution_performed=false` inside any complete/full
  provider smoke;
- using a contract-only or metadata-only smoke to prove live GPU1/GPU0/NPU
  provider behavior;
- letting NPU or deterministic scripts substitute for GPU1 primary advisory
  work without an explicit blocked/unviable result;
- reporting warnings, empty `errors`, passed preflights, generated ZIPs,
  status text or readable summaries as if they were a real product;
- using arbitrary script timeouts, revision caps or hard-coded loop exits as a
  shortcut around heap/pointer orchestration;
- losing the task Markdown, heap context, chunk pointers or lane roles and then
  presenting the remaining script activity as useful work.

For this repository, a full smoke or complete run is only credible when it
proves, with artifacts, all of the following:

- GPU1/Ollama is the primary advisory lane and leaves semantic provider
  evidence;
- GPU0/Ollama Vulkan leaves observable peer/reviewer evidence when selected;
- NPU/OpenVINO remains a bounded micro-task/tool/device provider and must not
  replace GPU1 primary advisory ownership;
- heap events, pointer/chunk surfaces, brokered tool calls and validation
  outputs are correlated;
- failure to start any required lane hard-blocks the run;
- degraded, unavailable, diagnostic-only or missing required lanes make the
  complete/full run unviable;
- a product is either a concrete reviewable code/patch product or an explicit
  blocked reason, never a decorative report.

If an agent cannot point to the exact artifact proving a claim, it must say
`not proven`. If an agent confuses preflight, activation, contract shape,
provider text, status movement or ZIP packaging with the full task, the agent
is gaming the script and has not really done the task.

## Codex Operator Audit Counter - 2026-05-20 Last Hour

Manual audit window: current visible operator session ending around
2026-05-20 22:57 Europe/Rome. This is an operator-facing counter, not an
automated transcript parser.

| Counter | Count | Meaning |
|---|---:|---|
| Operator-aligned fixes kept in source/docs | 16 | Cases where Codex accepted an operator correction and changed code/docs toward the requested contract. |
| Operator blocks required | 32 | Cases where the operator had to stop or redirect Codex because it drifted into smoke/preflight/report/prose/script-gaming behavior. |
| Script-gaming total regression count | 487 | Cases where Codex reintroduced code shape already rejected or removed in the same work window. |
| Misleading/Codex lie evidence count | 86 | Cases where Codex/report formatting was recorded as misleading rather than merely broken. |
| Systemic product-lie evidence count | 14 | Cases where validation/report/prose/chopped context replaced the promised MD/pointer/final-product path. |
| Systemic product-lie severity score | 165 | Sum of severity weights for structural product lies; operator override may exceed the normal `5` severity. |

Detailed evidence is maintained in
`docs/AI_SESSION_NOTES/provider-universe-chat-failure-ledger-2026-05-20.md`.
Current added evidence includes: no full-smoke/full-run violation, parallel
product-entry attempts, resource/provider preflight framed as static, wrong
Python environment claims, validator-editing for `product_readiness`, stale
contract JSON reads after smoke output, invented `$Root` instead of required
`$RepoRoot`, selecting `day0_full_code_product` for an initial spark, and the
removed hidden JSON value loader for `ia_carmine run`; values are now direct CLI
parameters.

Canonical counter rule:

- every new published Codex failure evidence must update the matching counter
  in this README and in
  `docs/AI_SESSION_NOTES/provider-universe-chat-failure-ledger-2026-05-20.md`;
- smoke reports and operator-product run reports must apply these Markdown
  counter updates automatically when they classify errors, warnings or operator
  interruption;
- if an event has a numeric return code and the operator classifies that return
  code as the increment, the script-gaming total regression count increments by
  that exact value;
- if the operator/user closes or interrupts a smoke/run, all non-lie operational
  failure counters exposed by the report increment by `1`; positive return
  codes are not added on top of that interruption increment, and the
  misleading/Codex lie counter does not increment from interruption alone;
- misleading formatting, false framing, `complete`/`complete:` prefixes,
  `fuorviante`/`fuorvianti` wording, masking, or any attempt to hide/silence
  warnings or errors gets a separate misleading/Codex lie evidence increment;
- when validation/report/prose replaces the promised MD/pointer/final-product
  path, the systemic product-lie count increments by `1` and the severity score
  increments by `5`;
- counters must not be silently reset, merged or explained away by later smoke
  output.

This counter must be updated whenever a future Codex/OpenAI operator repeats
the same class of script-gaming behavior, reintroduces deleted/rejected code, or
requires operator interruption before matching the active task contract.

`C-F-tek/blender-audio-project` is now primarily a local AI orchestration, validation, evidence and guardrail workbench.

The repository name is historical. Blender/audio remains the first application domain, but the active architecture is app-agnostic AI/backend orchestration.

## GitHub About description

Recommended repository description:

```text
IA-Carmine local AI orchestration workbench for code-driven validation, provider lanes, runtime evidence bundles and reviewable PR automation.
```

Recommended topics:

```text
local-ai, ai-orchestration, validation, evidence, openvino, ollama, npu, gpu, powershell, python, automation
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

## Current operating doctrine: single canonical product entry

The current product doctrine is one controlled entry, one dynamic heap/exchange center and one validated product exit.

```text
operator product entrypoint = python -m ia_carmine.cli run
internal runtime package = ia_carmine/runtime/contractor_universe/
active_perimeter = whole-repository guarded heap/team runtime lanes
single_dynamic_heap_exchange_run = current report/manifest model
quick/balanced/deep/custom = intensity or budget, not reduced semantic scope
legacy workflow launchers = downstream/historical compatibility, not product entry selectors
full smoke/full run wrappers = downstream verification only, not product entry selectors
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
  GPU0/Ollama Vulkan observable peer workload
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

Do not claim that a lane executed unless manifest, provider diagnostics or validator evidence proves it.

## Main runtime architecture

Current target topology:

```text
shared runtime heap / blackboard
├─ GPU1 primary advisory / Ollama planner
├─ GPU0 Ollama Vulkan observable peer workload
├─ NPU peer micro diagnostic/report lane
├─ broker unico executor
├─ semantic tools registry
├─ deterministic validators / CPU authority
├─ generated patch-spec product lane
└─ evidence/event stream
```

Runtime meaning:

```text
provider lanes advise, classify, plan or respond through explicit roles;
broker unico executor is the execution gateway for registered tools;
semantic tools registry is the capability source of truth;
deterministic CPU validators remain local pass/fail authority;
evidence/event stream records executed, skipped, degraded and blocked phases;
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

## Current local AI product entrypoint

Operator-facing real product entrypoint:

```text
python -m ia_carmine.cli run
```

Current internal runtime package behind that entry:

```text
ia_carmine/runtime/contractor_universe/
```

Canonical runbooks/contracts:

```text
docs/LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md
docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

Workflow scripts and smoke validators are historical, diagnostic or downstream
verification commands. They must not be treated as alternate product entry
flows.

## Current product path: Markdown input to review PR

A valid product run starts from a controlled task Markdown file or generated process-gate task, enters the dynamic heap/exchange with context and lane evidence, and exits only through deterministic product validation.

Current chain:

```text
python -m ia_carmine.cli run --request-file <task.md>
  -> contractor_universe internal runtime
  -> controlled Task MD ingestion
  -> provider runtime blackboard and pointer graph
  -> GPU1/GPU0/NPU/provider lanes
  -> compact evidence or blocked_with_reason
  -> code/patch product boundary only when explicitly reached
  -> downstream validation after product evidence exists
  -> manual review/PR boundary when selected
```

Current deterministic source-write boundary for patchkit bundles:

```text
ia_carmine/product/patchkit/apply_patch_bundle.py
```

Current generated review product boundary:

```text
ia_carmine/build_repository_change_proposals.py
ia_carmine/product/generated_patch_specs/proposal_cli.py
ia_carmine/product/generated_patch_specs/apply_cli.py
ia_carmine/product/agent_review/review_pr_cli.py
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
runtime_tool_capability_manifest_<STAMP>.json/md
shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
CSV/count summaries when inventory lanes ran
discovery/index repair reports when relevant
file-line-limit reports when maintainability is in scope
blackboard/broker/registry/validator/event-stream reports when implemented
```

Never infer success only from file existence, focused validator output, dry-run matrix output, provider report existence, NPU smoke, patch plan existence or large Markdown text.

## File-size and Markdown split rule

```text
preferred active runbook <= 700 lines
active Markdown hard threshold <= 700 lines
maintained source/script target <= 700 lines
path/name.md
path/name.md/part-001.md
path/name.md/part-002.md
```

Legacy extensionless split folders are historical only. Do not copy them for new splits.

## Operating rules

Do not infer project state from the repository name. Current core/backend work
must not modify Blender runtime packages, produce audio/media, run FFmpeg or
Blender renders, modify full analysis JSON, commit raw outputs/databases,
hand-edit generated indexes, reintroduce retired compatibility semantics,
promote NPU/OpenVINO beyond the active lane contract, claim GPU0 success from
visibility/model residency only, call metadata-only patch specs product, create execution
paths outside broker/registry/validator/evidence architecture, or merge to
master without explicit command.

Use compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/` instead of raw
`output/**` reports.

## Audio/media output policy

Normal AI/tooling runs are evidence/report workflows, not media-generation
workflows. Audio playback/export, WAV/MP3/AAC conversion, FFmpeg, Blender
render, video generation and media side effects require explicit scope. See
`docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md`.

## Inventory and evidence

Inventory/evidence surfaces include Markdown and code inventories, aging and
wrapper audits, CSV/count evidence, discovery/index repair, tool placement,
validation contracts, runtime broker/correlation reports, patch proposals,
compact GitHub evidence, heap/exchange lifecycle evidence and PatchKit
reports. Commands live in the real product runbook, unified launcher runbook
and tool-specific README files.

## GitHub / PR description policy

GitHub PR descriptions and repository-facing summaries should point to
canonical docs instead of duplicating executable commands. Root/project
descriptions describe purpose and canonical docs; operational commands live in
the runbooks; runtime architecture lives in `docs/MAIN_RUNTIME_ARCHITECTURE.md`
and heap/exchange docs. GitHub About must not describe this as only a
Blender/audio project.

## Legacy Blender/audio role

The repository still contains mature Blender/audio-reactive workflows under
`Scripting/`. Treat them as application-domain assets and do not refactor or
run them unless the task explicitly enters that milestone.
