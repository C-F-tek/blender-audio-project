# AGENTS.md

Primary repository contract for AI assistants, local agents, automated review systems and GitHub-only assistants working on this repository.

## Mandatory contract

Before planning, editing, validating, opening a PR or suggesting changes, the agent must:

1. read `AGENTS.md`;
2. read `CHATGPT.md` and `CHATGPT/README.md` when resuming ChatGPT-assisted, local-AI, full-toolbox or handoff-driven work;
3. read `docs/README.md` for the current documentation index;
4. read `docs/LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md` for the current run/document router;
5. read `docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md` before launching or modifying the real product run path;
6. read `docs/LOCAL_AI_TASKS/documentation-code-alignment-audit-2026-05-10.md` when checking whether docs still match code;
7. read `docs/LOCAL_AI_TASKS/problems-and-hygiene-candidates-2026-05-10.md` before hygiene work on run/product artifacts;
8. read `docs/LOCAL_AI_TASKS/md-line-budget-triage-2026-05-10.md` before adding or expanding operational Markdown;
9. read `docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md` for the IN -> dynamic heap/exchange -> deterministic OUT operating model;
10. read `docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md` for the compact AI first-orientation map;
11. read `docs/LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md` when documentation appears conflicting or stale;
12. read `docs/LOCAL_AI_TASKS/repository-hygiene-cleanup-and-refactor-procedure-2026-05-09.md` when classifying, deleting, splitting or refactoring old docs/index/discovery surfaces;
13. read `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` for older code/state bridge context when present;
14. read `docs/MAIN_RUNTIME_ARCHITECTURE.md` when working on runtime, provider, broker, validator, telemetry or workflow architecture;
15. read `docs/LOCAL_AI_RUN_BOOTSTRAP.md` when working from or delegating to a local checkout;
16. read `docs/LOCAL_AI_TASKS/patch-suggestion-review-workflow-2026-05-07.md` before converting patch-note suggestions into source edits;
17. follow hard guardrails unless the human explicitly approves a normally restricted action;
18. inspect the target source/document before proposing or applying a patch;
19. report conflicts between the request, code, docs, evidence and guardrails before modifying files.

## Repository identity

| Field | Value |
|---|---|
| Working title | `IA-Carmine Local AI Orchestration Workbench` |
| Repository | `C-F-tek/blender-audio-project` |
| Main language | Python |
| Active architecture | Shared runtime heap / blackboard, provider-lane orchestration, broker execution, semantic tools registry, deterministic CPU validators, telemetry/evidence workflows |
| Operator product entrypoint | `python -m Tools.ai run` |
| Dynamic heap/exchange launcher | `python -m Tools.workflow run_unified_local_ai_refactor` |
| Primary provider lane | `GPU1 / Ollama / RTX 5080 -> primary advisory planner/worker` |
| Secondary provider lane | `GPU0 / OpenVINO -> observable support workload and peer evidence lane` |
| Micro peer lane | `NPU / OpenVINO -> peer micro diagnostic/report lane until compute-provider behavior is validated` |
| Current source-write boundary | `Tools/ai/patchkit/apply_patch_bundle.py` for reviewed patchkit bundles when operations can express the change |
| Current generated-product boundary | generated patch specs plus `Tools/ai/apply_generated_patch_specs_for_review_pr.py` for concrete review PR operations |
| Legacy domain | Blender audio-reactive scene automation |

The repository name is historical. Do not infer that Blender/audio is the current architectural boundary.

## Canonical reading order

```text
AGENTS.md
CHATGPT.md
CHATGPT/README.md
docs/README.md
docs/LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md
docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md
docs/LOCAL_AI_TASKS/documentation-code-alignment-audit-2026-05-10.md
docs/LOCAL_AI_TASKS/problems-and-hygiene-candidates-2026-05-10.md
docs/LOCAL_AI_TASKS/md-line-budget-triage-2026-05-10.md
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
docs/LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md
docs/LOCAL_AI_TASKS/repository-hygiene-cleanup-and-refactor-procedure-2026-05-09.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md
docs/MAIN_RUNTIME_ARCHITECTURE.md
CHATGPT/next-chat-handoff-*.md                 # when present and relevant
CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md                 # local checkout only
README.md
WORKFLOW.md
docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md
docs/LOCAL_AI_TASKS/gpu-peer-exchange-operational-principle.md
docs/LOCAL_AI_TASKS/md-coherence-only-github-pass-2026-05-06.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/patch-notes-quality-product-2026-05-07.md
docs/LOCAL_AI_TASKS/patch-suggestion-review-workflow-2026-05-07.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
docs/AI_PIPELINE_ARCHITECTURE.md
docs/PROJECT_STATUS_POINT.md
docs/DATA_FLOW.md
docs/LOCAL_AI_WORKFLOW.md
docs/JSON_SCHEMAS.md
Tools/ai/README.md
Tools/workflow/README.md
Tools/validation/README.md
nearest package/tool README
target file
```

For real product, full toolbox, refactor, provider or run-unica local AI runs, the current entrypoint model is:

```text
Operator product path:
  python -m Tools.ai run
  docs/LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md
  docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md

Dynamic launcher / diagnostic path:
  python -m Tools.workflow run_unified_local_ai_refactor
  docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
  docs/LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md
```

## Markdown coherence policy

This repository uses compact Markdown as an operational surface.

Hard rule for maintained Markdown:

```text
active .md file <= 500 lines
preferred active runbook <= 400 lines
```

When a maintained Markdown file exceeds 500 lines:

```text
keep the original file as a compact index
create a sibling folder named exactly like the file, including .md: <file>.md/
move detailed content into <file>.md/part-001.md, part-002.md, ...
keep each part <= 500 lines
link all parts from the compact index
```

Generated evidence may exceed 500 lines only when it has compact JSON/Markdown manifest, summary or index and is not used as a primary entrypoint.

## Markdown edit and encoding safety rule

AI agents must preserve Markdown encoding and structure. Do not use Windows PowerShell `Set-Content` or fragile multiline `if/elseif` chat-pasted snippets for Unicode Markdown files.

Required safe edit methods:

~~~text
prefer repository PatchKit bundles for repeatable edits
prefer Python UTF-8 read/write scripts for direct local Markdown edits
preserve UTF-8 without mojibake
verify no corrupted mojibake/BOM byte markers before staging
run git diff before staging
~~~

For structural Markdown hygiene, use the repository tool instead of manual splitting:

~~~powershell
python -m Tools.docs refactor_markdown_splits --repo-root . --migrate-legacy-splits --split-monolithic
~~~

Do not manually split, rewrite or delete Markdown trees when `Tools/docs/refactor_markdown_splits.py`, `Tools/docs/build_repo_hygiene_plan.py`, PatchKit, or validators can express the change safely.

Markdown cleanup rules:

```text
update canonical docs before adding parallel runbooks
mark stale docs as superseded/historical/delete-candidate before removal
do not commit output/**, indexAI/code_chunks/**, *.db, *.sqlite, renders/** or generated media
never treat generated indexes/evidence as maintained source docs
```

Current compact operational state:

```text
Baseline: master after PR #296 merge and subsequent docs alignment commits
Product wrapper: python -m Tools.ai run
Dynamic launcher: python -m Tools.workflow run_unified_local_ai_refactor
Current run index: docs/LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md
Current runbook: docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md
Current operating model: docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
AI orientation map: docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
Documentation panorama/staleness map: docs/LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md
Repository hygiene procedure: docs/LOCAL_AI_TASKS/repository-hygiene-cleanup-and-refactor-procedure-2026-05-09.md
Capability map: docs/LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md
Parameter map: docs/LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md
Docs/code alignment audit: docs/LOCAL_AI_TASKS/documentation-code-alignment-audit-2026-05-10.md
Problems/hygiene backlog: docs/LOCAL_AI_TASKS/problems-and-hygiene-candidates-2026-05-10.md
Markdown line-budget triage: docs/LOCAL_AI_TASKS/md-line-budget-triage-2026-05-10.md
Docs bridge: docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
Main runtime architecture: docs/MAIN_RUNTIME_ARCHITECTURE.md
Patchkit boundary: Tools/ai/patchkit/apply_patch_bundle.py
Generated product boundary: Tools/ai/apply_generated_patch_specs_for_review_pr.py
Current mode: code-driven, docs-first updates unless source changes are explicitly scoped
Review posture: no destructive actions, force-push, deploy, permission/secret changes or protected-branch merge unless explicitly requested
```

The earlier broker telemetry gap is resolved/historical unless a new regression is found. Use `docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md` and newer telemetry evidence for the recent baseline.

## Main runtime architecture target

The primary runtime target is:

```text
shared runtime heap / blackboard
├─ GPU1 primary advisory / planner
├─ GPU0 OpenVINO observable support workload
├─ NPU peer micro diagnostic/report lane
├─ broker unico executor
├─ semantic tools registry
├─ deterministic validators / CPU authority
├─ generated patch-spec product lane
└─ telemetry/event stream
```

Operational meaning:

```text
provider lanes advise, help, classify or respond through explicit roles
broker unico executor is the execution gateway for registered tools
semantic tools registry is the capability source of truth
deterministic validators on CPU remain local pass/fail authority
telemetry/event stream records executed, skipped, degraded and blocked phases
generated patch specs must become concrete deterministic operations before review PR product success
```

Current runtime boundary:

```text
IN = controlled task/context/capability entry
LOOP = dynamic heap/exchange where GPU1/GPU0/NPU/provider lanes cooperate
OUT = deterministic exit product, lifecycle validation, patchkit bundle or review PR
```

Architecture targets do not authorize source writes, provider execution, patch application, Blender runtime, FFmpeg runtime, commit, push, merge or delete by themselves.

## Patch suggestion ledger policy

A patch-notes quality product is a proposal ledger, not executable code.

```text
patch_notes_quality_product_<stamp>.json = review input
summary.proposal_core = compact bundle handoff ledger
patchkit bundle / branch diff = reviewed implementation artifact
```

Agents must not convert ledger entries directly into source writes. Review order is:

```text
1. python_python
2. python_doc
3. doc_doc
4. doc_python
```

Before patching any suggestion:

```text
refresh against current master
verify source/target still exists
verify missing imports/symbols are still missing
reject generated-evidence noise and placeholder fenced-code paths
use a small reviewed patchkit bundle or branch diff
run py_compile/smoke/git diff --check
```

If a suggestion is stale, record it as stale evidence when useful and do not patch it.

## Patchkit source-write policy

Future long, delicate or repeated patch work should centralize the modification core in a repository-native patchkit bundle when patchkit operations can express the change:

```text
patch_specs/<bundle>/bundle.json
patch_specs/<bundle>/fragments/*.ps1
patch_specs/<bundle>/fragments/*.py
```

Standard apply path:

```powershell
python -m Tools.ai apply_patch_bundle `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json `
  --dry-run

python -m Tools.ai apply_patch_bundle `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json
```

Patchkit is not an authorization layer. It is a deterministic application boundary. Human/operator scope, branch policy and guardrails still apply.

## Remote-AI PatchKit handoff policy

When an AI does not have local terminal access, PatchKit remains the preferred controlled route for large local changes.

The AI should produce:

```text
patch_specs/<bundle>/bundle.json
patch_specs/<bundle>/fragments/*
local dry-run command
local apply command
local validation commands
expected touched files and line-count reporting requirement
```

The AI must not claim local application or validation until the user returns terminal output.

The local operator applies:

```powershell
$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:IA_CARMINE_PYTHON = $RepoPy
$env:PYTHONPATH = (Resolve-Path .).Path

& $RepoPy -m Tools.ai apply_patch_bundle `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json `
  --dry-run

& $RepoPy -m Tools.ai apply_patch_bundle `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json
```

Remote handoff bundles must be idempotent where practical, use stable anchors or guarded delete markers and include validators when possible.

## Code length policy

Hard limit for maintained code/script files:

```text
Python/PowerShell/scripts/source code: <= 400 lines per maintained source file
```

When modifying code, report resulting line count for every created or modified code/script file.

Existing oversized files are technical debt; split them progressively when touching that area for a code task.

## AI session notes

`docs/AI_SESSION_NOTES/` stores compact Markdown notes from long AI-assisted sessions.

Rules:

```text
keep notes factual and compact
record decisions, validation outcomes, blockers and next actions
do not paste private reasoning
do not let notes override AGENTS.md, source, validation reports or canonical docs
promote stable principles into canonical docs/LOCAL_AI_TASKS or contract docs
```

## Provider and peer-exchange posture

Canonical production roles:

```text
GPU1 / Ollama / RTX 5080 = primary advisory planner/worker
GPU0 / OpenVINO = observable companion peer support workload and tool-request producer
NPU = peer micro diagnostic/report lane until compute-provider behavior is validated
deterministic scripts = heavy audit and validation authority
runtime tool broker = controlled tool execution for GPU1, GPU0 and NPU requests
broker unico executor = target central execution gateway for registered tools
semantic tools registry = target capability source of truth
telemetry/event stream = target visibility surface for executed, skipped, degraded and blocked phases
```

GPU1/Ollama must execute the primary advisory lane for real run-unica execution unless explicitly disabled by an operator flag or classified as unavailable/degraded by evidence.

GPU0 is not complete when it only performs device visibility preflight. GPU0 must provide observable workload/support evidence and move toward peer-worker behavior:

```text
GPU1 planner/worker task packet
  -> GPU0 companion execution or observable support workload
  -> GPU0 response/evidence packet
  -> optional GPU0 tool requests
  -> runtime broker execution for GPU0 requests
  -> non-blocking NPU micro/tool-support signal
  -> runtime broker execution for NPU requests when present
  -> GPU1 planner/auditor consumption
  -> final telemetry, bundle and gate evidence
```

When `IA_CARMINE_GPU0_COMPANION_MODEL_DIR` is configured, GPU0 may run OpenVINO GenAI tasks on GPU.0. When no companion model is configured, GPU0 may still produce numeric, static, tool-request or report-only evidence, but the run must classify missing semantic companion mode explicitly.

NPU should not be documented as a heavy audit or compute authority until a validated compute-provider lane exists. Preferred current NPU role:

```text
peer micro diagnostic/report lane
micro-fast task support
small checkpoint review when cheap and available
provider/device diagnostics
structured helper output
tool-intelligence support when cheap and available
```

Heavy audit, report validation and acceptance decisions stay with deterministic repository scripts unless a task explicitly requests NPU semantic review.
NPU tool-support output must stay non-blocking, broker-controlled and visible in telemetry/bundle evidence when provider lanes are selected.

## Provider-capable `.venv` rule

Before running provider, GPU0, NPU, OpenVINO or run-unica validation, agents must verify:

```powershell
$env:IA_CARMINE_PYTHON = "<repo>\.venv\Scripts\python.exe"
$env:PYTHONPATH = "<repo>"
& $env:IA_CARMINE_PYTHON -c "import sys; print(sys.executable); import numpy, openvino; from openvino import Core; c=Core(); print(c.available_devices)"
```

Required OpenVINO/GPU0/NPU packages:

```text
numpy
openvino
openvino-genai
```

Expected IA-Carmine workstation visibility:

```text
['CPU', 'GPU.0', 'GPU.1', 'NPU']
```

If `.venv` is missing dependencies, classify as `provider_python_environment_missing_dependency`, not as GPU0/NPU provider failure. GPU.1 may be visible through OpenVINO, but it is reserved for CUDA/Ollama and must not receive OpenVINO workload.

## Production-grade tool promotion rule

A new capability is not complete when code is merely inserted.

Every added or changed tool/lane must move through the production path before it is called done:

```text
implemented code
  -> wired into the canonical operator entrypoint or internal launcher according to scope
  -> visible in CLI/help/runbook/operator docs
  -> environment preflight documented when dependencies/providers matter
  -> activated by intended profile or explicit flag
  -> emits compact JSON/Markdown evidence
  -> appears in phase_status / phase_reports or equivalent manifest surfaces
  -> is understood by contract validators
  -> is included in evidence/bundle/handoff when relevant
  -> has unavailable/degraded/disabled classification when it cannot run
```

Do not stop at an internal module, helper function, isolated smoke script or hidden command.

For real run-unica, promoted lanes must be included by default unless disabled by explicit operator flags or classified as unavailable/degraded through manifest, telemetry, phase reports or validator evidence.

## TUTTO SU TUTTO / run-unica rule

TUTTO SU TUTTO means intelligent combined use of all relevant mapped tools/scripts inside the complete run-unica flow.

It does not mean executing every script blindly. It means the run unica can discover, select, coordinate, validate and report every applicable capability from the maps while respecting guardrails, provider availability, evidence quality and explicit `-No*` opt-outs.

```text
mapped capability
  -> lane selection
  -> mandatory/static preflight when product path is selected
  -> availability classification
  -> execution or explicit skip/degraded state
  -> deterministic validation when applicable
  -> telemetry/evidence/bundle publication
  -> recommendation, patch-plan or review-PR product when requested
```

The heap/exchange model is the canonical semantics for the whole active project perimeter. Broad runs must remain explicit lane compositions, not compatibility aliases:

```text
task input
run identity
real-run activation
intensity/budget
provider lanes
evidence lanes
patch/review lanes
explicit opt-outs
```

A valid run-unica execution includes every major selected phase unless the operator disables a phase explicitly with a `-No*` flag or the phase is classified unavailable/degraded.

Expected by default when the product path selects the corresponding lanes:

```text
mandatory real product preflight passed before dynamic runtime
pipeline adapter ufficiale eseguito
packet/proposals generati
GPU1/Ollama primary advisory executed or explicitly classified degraded
GPU0 observable support workload evidence present when configured or explicitly classified degraded
NPU peer micro diagnostic/report evidence present when available
patch specs creati e validati
workload quality routing presente
context pack presente
SQLite memory IN/OUT presente quando non disabilitata
heap/exchange runtime entry presente
heap/exchange runtime state/peer manifest presente
heap/exchange runtime exit product presente quando product lanes are selected
heap/exchange lifecycle validator presente quando product lanes are selected
runtime evidence correlation presente quando richiesta
runtime broker report absorbed into telemetry
repository change proposals consume current-stamp runtime evidence when available
generated patch-spec apply report has concrete operations before review PR success
patch_application_performed=false unless an explicit reviewed patch boundary is selected
```

As the main runtime architecture lands, run-unica should progressively expose:

```text
blackboard state report
broker unico executor report
semantic tools registry snapshot
deterministic validators / CPU authority summary
telemetry/event stream summary
GPU1/GPU0/NPU lane status reports
```

Future tools become part of TUTTO SU TUTTO only after they are mapped, wired, guarded, observable and evidence-producing. Architecture targets are expansion space, not current execution claims.

`-RunIntensity quick|balanced|deep|custom` changes budget, rounds, context limits, token limits and keep-alive only. It must not reduce the run-unica semantic perimeter.

A missing full-run lane is valid only when one of these is true:

```text
explicit -No* disabler is present
manifest/report records unavailable-tool or provider failure
-DryRun records the phase as planned but not executed
```

## Important folders

| Path | Meaning |
|---|---|
| `CHATGPT/` | Lightweight handoff notes. |
| `docs/AI_SESSION_NOTES/` | Compact session notes and decisions. |
| `Tools/ai/` | AI orchestration, provider probes, evidence bundles, heap/exchange lifecycle helpers and patch-plan tooling. |
| `Tools/ai/patchkit/` | Reusable controlled patch-bundle application helpers. |
| `Tools/workflow/` | Real product wrapper, unified launcher, local workflow runners and post-validation packet generation. |
| `Tools/npu/` | NPU/OpenVINO support and diagnostics. |
| `Tools/validation/` | Non-invasive validators and inventory builders. |
| `docs/` | Stable documentation contracts and project state. |
| `docs/MAIN_RUNTIME_ARCHITECTURE.md` | Main runtime topology and blackboard/broker/registry/validator/telemetry contract. |
| `docs/LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md` | Current run documentation router. |
| `docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md` | Current operator real product runbook. |
| `docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md` | Current runtime operating model. |
| `docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md` | Compact first-orientation map for AI agents. |
| `docs/LOCAL_AI_TASKS/repository-hygiene-cleanup-and-refactor-procedure-2026-05-09.md` | Automated hygiene/refactor/delete allowlist procedure. |
| `indexAI/` | Generated indexes/context/patch material. Do not hand-refactor as source. |
| `Scripting/` | Blender application-domain packages; frozen for core/backend work unless scoped. |

## Allowed by default

```text
read files
inspect repository structure
add/update non-destructive documentation
add report-only validators and inventory tools
create manual-review patch specs/bundles
run focused local validation when execution is available
open/update PRs without merging
```

## Requires explicit human approval

```text
delete files
force-push
rewrite history
merge to master/protected branch
change secrets, permissions, billing or visibility
deploy production
rename repository
run long Blender renders or heavy GPU workloads outside an explicitly selected full/provider workflow
change provider/model execution semantics
add dependencies
move package entrypoints
rewrite large Blender scripts
modify full frame-level analysis JSON
```

## Never commit

```text
output/**
renders/**
*.db
*.sqlite
*.sqlite3
raw checkpoints
large full analysis JSON outside compact evidence policy
indexAI/code_chunks/** unless explicitly requested as generated index evidence
```

## Patch delivery policy

For long, multi-file or delicate changes, especially on workflow, broker, memory, GPU/NPU provider or runner code, prefer repository-native patchkit bundles when supported:

```text
patch_specs/<bundle>/bundle.json
patch_specs/<bundle>/fragments/*.ps1
patch_specs/<bundle>/fragments/*.py
```

Patchkit bundles must be idempotent where possible, create backups when writing, block on failed validators, report resulting line counts for modified scripts and never commit automatically.

For remote AI sessions without local terminal access, PatchKit is the official handoff format for large controlled changes:

```text
AI authors bundle + local commands
user runs dry-run/apply/validators locally
user returns output
AI continues from real terminal evidence
```

ZIP patch bundles remain acceptable for external/manual transfer when repository-native patchkit cannot express the change. ZIP-internal names such as `README.md`, bundle runner script and `patches/` are bundle members, not repository-tracked source paths.

Patch-note products and `summary.proposal_core` ledgers are not patch bundles. They must be converted into reviewed patchkit bundles or branch diffs before any source write.

## Refactoring rules

```text
prefer existing helpers before creating new ones
keep path/JSON/provider/evidence logic app-agnostic when practical
keep generated indexes out of source-level refactors
keep artistic scene behavior separate from infrastructure refactors
do not migrate Blender packages broadly unless explicitly scoped
when implementing the main runtime architecture, centralize execution through broker/registry/validator/telemetry surfaces instead of duplicating per-runner logic
```

## Reporting contract

For code/script changes report:

```text
changed files
purpose
resulting line count for every created/modified script
validation performed or missing
provider/runtime execution status
risks
follow-up recommendations
```

A workflow change is incomplete unless it produces compact evidence or clearly states which checks are missing.
