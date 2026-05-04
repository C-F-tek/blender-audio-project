# Workflow

## Purpose

Root operational lifecycle for `IA-Carmine Local AI Orchestration Workbench`.

This file defines durable process and guardrails. It must not carry executable PowerShell command blocks because launcher flags, validation options and local paths change faster than root workflow policy.

Scenario-specific commands live in task runbooks under `docs/LOCAL_AI_TASKS/`. Tool-specific commands live next to the tool package, for example `Tools/validation/README.md` and `Tools/npu/pipeline/README.md`.

## Canonical lifecycle

```text
read contract
  -> classify task
  -> build inventories/context when useful
  -> choose one scope
  -> change minimal files
  -> validate locally
  -> build compact evidence or patch bundle when needed
  -> open/update PR
  -> human review / merge
```

## Required reading

```text
AGENTS.md
README.md
WORKFLOW.md
docs/README.md
docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
docs/WORKFLOW_HELPER_SCRIPTS_POLICY.md
docs/PROJECT_STATUS_POINT.md
docs/DATA_FLOW.md
docs/LOCAL_AI_WORKFLOW.md
Tools/validation/README.md
```

For code/provider/refactor work, also read the nearest tool/package README and the target source file.

## Canonical local AI workflow

The active local AI workflow entrypoint is:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Use the runbook for current `-Full0To10`, `-RunIntensity`, interactive, reset, provider, memory, patch-spec, evidence and validation examples.

Legacy monolithic 0-to-10 scripts/runbooks are not an active operator path. Historical details belong in git history or compact evidence, not in parallel maintained entrypoints.

## Command placement policy

Root workflow and README files are descriptive. They should link to command owners instead of copying executable command blocks.

| Command family | Canonical owner |
|---|---|
| Full local AI / 0-to-10 launcher commands | `docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` |
| Launcher manifest fields | `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` |
| Markdown/script inventories | `Tools/validation/README.md` and unified launcher runbook |
| NPU helper validation | `Tools/npu/pipeline/README.md` |
| Patch-spec workflow | `docs/PATCH_SPEC_WORKFLOW.md` |
| Local checkout/bootstrap notes | `docs/LOCAL_AI_RUN_BOOTSTRAP.md` |

If a command becomes outdated, update the owning runbook/tool README only. Do not duplicate it into root docs.

## Provider policy

```text
Ollama -> GPU/CUDA -> primary advisory provider only when explicitly requested and quality-gated
OpenVINO -> NPU -> probe / guardrail / decode diagnostic
Blender runtime -> application target, frozen unless explicitly scoped
```

Provider execution must stay explicit and report-bound.

A full 0-to-10 run must not silently degrade if provider quality routing is missing. It must build workload quality routing evidence or fail clearly; dry-run may mark the routing report as planned.

## Preflight policy

Before local execution, the operator should verify:

```text
correct branch
fast-forward sync where appropriate
clean or intentionally dirty working tree
Python interpreter/venv selection
PYTHONPATH rooted at repository root
ignored output/cache/state files not staged
```

The unified launcher resolves Python through `-PythonExe`, `IA_CARMINE_PYTHON`, `.venv`, `venv` and fallback `python`. It also sets `PYTHONPATH` to the repository root.

## Inventory policy

Use inventories before broad documentation or code refactors.

```text
Markdown inventory -> canonical docs, obsolete docs, generated/evidence docs, missing index review.
Script inventory -> scripts/tools, functions/classes/methods, descriptions, refactor discovery.
```

Do not commit inventory outputs from `output/**`. Commit compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/` only when needed for review.

## Validation policy

For full workflow, provider, full-toolbox or code-refactor runs, prefer the unified launcher.

For focused validator work, use `Tools/validation/README.md` as the command catalog.

The minimum validation evidence for a PR should state:

```text
which launcher/tool command was run
whether provider/runtime execution occurred
where the manifest/report/evidence is located
whether patch application occurred
what remains unvalidated locally
```

## Evidence and patch bundles

Compact evidence belongs under:

```text
docs/LOCAL_VALIDATION_EVIDENCE/
```

Full local reports remain ignored under `output/**` unless a compact Git-trackable evidence artifact is intentionally generated.

Patch application remains manual-review-only unless the user explicitly requests apply. Patch-spec generation may be requested through the unified launcher, but source application must remain a separate reviewed action.

## Index regeneration

Regenerate generated indexes only after structural source/doc/workflow changes when the index is required for review or the next run.

Generated index files are not manually maintained source. Do not hand-edit generated chunks or manifests.

## Guardrails

Do not do without explicit approval:

```text
delete files
force-push or rewrite history
merge to master/protected branch
change secrets, permissions, billing or visibility
deploy production
run heavy Blender/GPU workloads automatically
change provider/model execution from explicit to implicit
```

Never commit:

```text
output/**
renders/**
*.db
*.sqlite
*.sqlite3
raw checkpoints
large full analysis JSON outside compact evidence policy
```

## PR report contract

Every PR should state:

```text
changed files
purpose
script line counts for created/modified scripts
validation run or missing
provider/runtime execution status
risk
follow-up
```

## Acceptance criteria for workflow docs

```text
root docs are command-free
commands live in owning runbooks/tool READMEs
unified launcher remains the active local-AI entrypoint
provider execution remains explicit
patch application remains explicit
long evidence is indexed by compact manifests
obsolete monolithic runbooks are not active entrypoints
```
