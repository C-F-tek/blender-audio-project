# Documentation

Stable documentation index for `IA-Carmine Local AI Orchestration Workbench`.

The repository slug is still `C-F-tek/blender-audio-project`, but the active architecture is local AI orchestration, provider-lane routing, validation, evidence, telemetry and manual-review patch planning. Blender/audio remains the first application domain, not the architectural boundary.

## First operational rule

Before proposing or editing:

```text
read current source/canonical docs
inspect existing owners and nearby helpers
reuse existing scripts/helpers first
make the smallest safe change
keep maintained files small and reviewable
```

Canonical rule:

```text
LOCAL_AI_TASKS/read-first-reuse-first-small-files-rule-2026-05-07.md
```

## Current code-driven entrypoints

Use these first when an AI needs to understand what the project is, what exists, what can run, and which scripts may be hidden or legacy:

```text
LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md
LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md
LOCAL_AI_TASKS/script-aging-visibility-audit-2026-05-09.md
LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

Meaning:

| Map | Purpose |
|---|---|
| `heap-exchange-and-patchkit-operating-model-2026-05-09.md` | Current IN -> dynamic heap/exchange loop -> deterministic OUT model and reusable patchkit bundle procedure. |
| `current-capability-depth-map-2026-05-09.md` | Current active/report-only/provider/manual-review/target capabilities and evidence surfaces. |
| `unified-launcher-parameter-decision-map-2026-05-09.md` | How to choose launcher parameters by lane instead of reading a flat flag list. |
| `script-aging-visibility-audit-2026-05-09.md` | Oldest/hidden wrapper notice queue; not a deletion list. |
| `code-derived-ai-toolchain-map-2026-05-07.md` | Current behavior from source code. |
| `script-census-and-validation-flow-2026-05-07.md` | Script families, run variants and validation cycles. |
| `single-owner-scripts-and-flow-boundaries-2026-05-07.md` | Scripts that must not be duplicated or bypassed. |
| `code-driven-data-flow-map-2026-05-07.md` | Flow variants from input Markdown to provider, evidence, patch suggestion and PR. |
| `validator-smoke-cycle-map-2026-05-07.md` | Focused validator/smoke cycles. |

## Main doctrine

Full local-AI work must preserve **TUTTO SU TUTTO**.

```text
Full0To10 = whole-repository active-lane perimeter
quick/balanced/deep/custom = budget/intensity, not reduced semantic scope
-No* flags = explicit opt-out only
-NoStrictRealRunActivation = single-phase diagnostics only
```

New stable lanes, validators, broker capabilities, provider diagnostics, evidence surfaces, memory/context tools, discovery/index surfaces and CSV/count surfaces become candidate expansions of `tutto`.

## Primary runtime architecture

Canonical architecture:

```text
MAIN_RUNTIME_ARCHITECTURE.md
LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
```

Target topology:

```text
shared runtime heap / blackboard
├─ GPU1 primary advisory / planner
├─ GPU0 coworker/helper OpenVINO
├─ NPU microtask responder
├─ broker unico executor
├─ semantic tools registry
├─ deterministic validators / CPU authority
└─ telemetry/event stream
```

Runtime boundary:

```text
IN = controlled task/context/capability entry
LOOP = dynamic heap/exchange where GPU1/GPU0/NPU/provider lanes cooperate
OUT = deterministic exit product, lifecycle validation, patchkit bundle or review PR
```

Architecture targets do not authorize source writes, provider execution, patch application, Blender runtime, FFmpeg runtime, commit, push, merge or delete by themselves.

## Single reading flow

Use this order unless a task file says otherwise:

```text
../AGENTS.md
../CHATGPT.md
../CHATGPT/README.md
LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md
LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md
LOCAL_AI_TASKS/script-aging-visibility-audit-2026-05-09.md
LOCAL_AI_TASKS/read-first-reuse-first-small-files-rule-2026-05-07.md
LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
MAIN_RUNTIME_ARCHITECTURE.md
LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
DATA_FLOW.md
../Tools/workflow/README.md
../Tools/ai/README.md
nearest package/tool README
target source/doc file
```

Large catalogs such as `../Tools/validation/README.md` are reference material, not primary reading-order entrypoints.

Historical handoffs and generated evidence are context only. Do not let them override current source code, owner maps or manifest evidence.

## Patch bundle procedure

Future patch work should centralize the modification core and let patchkit apply it.

Preferred layout:

```text
patch_specs/<bundle>/bundle.json
patch_specs/<bundle>/fragments/*.ps1
patch_specs/<bundle>/fragments/*.py
```

Standard application:

```powershell
python .\Tools\ai\patchkit\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json `
  --dry-run

python .\Tools\ai\patchkit\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json
```

Patchkit is the deterministic OUT boundary for source modifications. It handles backup, idempotency, encoding/newlines, PowerShell/parser checks, Python compile checks, `git diff --check`, JSON/Markdown reports and line counts.

## Markdown and file-size policy

Maintained files must be compact.

```text
preferred active runbook <= 400 lines
active Markdown hard threshold <= 500 lines
maintained source/script target <= 400 lines
```

Markdown split folder naming is mandatory:

```text
path/name.md
path/name.md/part-001.md
path/name.md/part-002.md
```

Canonical policies:

```text
LOCAL_AI_TASKS/read-first-reuse-first-small-files-rule-2026-05-07.md
LOCAL_AI_TASKS/md-split-folder-naming-rule-2026-05-07.md
LOCAL_AI_TASKS/md-coherence-only-github-pass-2026-05-06.md
DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
```

## Current canonical task runbooks

| Need | File |
|---|---|
| Current operational bridge | `LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` |
| Heap/exchange and patchkit operating model | `LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md` |
| Current capability depth | `LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md` |
| Launcher parameter decision map | `LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md` |
| Script aging / hidden wrapper review | `LOCAL_AI_TASKS/script-aging-visibility-audit-2026-05-09.md` |
| Unified full 0-to-10 local AI workflow | `LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` |
| Launcher manifest/phase contract | `UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` |
| Code-derived behavior map | `LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md` |
| Script census and validation flows | `LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md` |
| Owner/boundary map | `LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md` |
| Data-flow variants | `LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md` |
| Validator/smoke cycles | `LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md` |
| Patch suggestion final phase | `LOCAL_AI_TASKS/patch-suggestion-bundle-final-phase.md` |
| GPU peer-exchange doctrine | `LOCAL_AI_TASKS/gpu-peer-exchange-operational-principle.md` |
| Markdown split naming | `LOCAL_AI_TASKS/md-split-folder-naming-rule-2026-05-07.md` |
| Tool promotion/insertion | `LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` |
| Tool placement audit | `LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md` |

## Stable architecture and workflow docs

| File | Purpose |
|---|---|
| `MAIN_RUNTIME_ARCHITECTURE.md` | Shared blackboard, GPU1/GPU0/NPU lanes, broker, semantic registry, CPU validators and telemetry. |
| `DATA_FLOW.md` | Broad data/report/provider flow; compact flow map is preferred for operations. |
| `MODULE_MAP.md` | Repository area map. |
| `WORKFLOW_HELPER_SCRIPTS_POLICY.md` | Shell/GUI/debug/push-capable helper classification and guardrails. |
| `AI_WORKLOAD_REPORT_QUALITY_GATE.md` | Workload quality-gate contract. |
| `AI_CONTEXT_PACKS.md` | Task-scoped context packs and compact evidence. |
| `AI_SELECTIVE_PLANNER.md` | Report-only selective planner. |
| `AI_MEMORY_POLICY.md` | Memory retention, promotion and quarantine policy. |
| `GITHUB_LOCAL_VALIDATION_WORKFLOW.md` | Local Git/GitHub validation workflow. |
| `GITHUB_ONLY_AI_CONTINUATION_GUIDE.md` | GitHub-only continuation and local-validation handoff. |
| `TECH_DEBT_TRACKER.md` | Known debt and remediation queue. |

Historical/supporting references stay available but must not override current maps:

```text
LOCAL_AI_WORKFLOW.md
PROJECT_STATUS_POINT.md
docs/JSON_SCHEMAS.md
large generated evidence docs
```

## Tooling README entrypoints

| Folder | README |
|---|---|
| Workflow tools | `../Tools/workflow/README.md` |
| AI tools | `../Tools/ai/README.md` |
| Validators/smokes catalog | `../Tools/validation/README.md` |
| NPU/OpenVINO package | `../Tools/npu/pipeline/README.md` |

## Blender/audio docs

Use only when entering the application domain:

```text
PROJECT_OVERVIEW.md
BLENDER_SCRIPT_ENTRYPOINTS.md
AUDIO_ANALYSIS_PIPELINE.md
AI_GENERATED_PACKAGE_STANDARD.md
PACKAGE_CREATION_WORKFLOW.md
QUALITY_GATE.md
RENDER_WORKFLOW.md
FFMPEG_WORKFLOW.md
COMPATIBILITY.md
SHARED_SCRIPTING_UTILITIES.md
```

## Evidence and generated outputs

```text
docs/LOCAL_VALIDATION_EVIDENCE/** = compact review snapshots, commit selectively
output/** = generated reports, do not commit
indexAI/code_chunks/** = generated chunks, do not commit
*.db / *.sqlite / *.sqlite3 = local/private DBs, do not commit
renders/** = media output, do not commit
```

## Validation for doc changes

For docs-only changes, use the validator cycle map and prefer focused checks:

```text
LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

Minimum local checks when available:

```text
check_docs_links.py
check_file_line_limits.py when line policy is touched
git diff --check
```
