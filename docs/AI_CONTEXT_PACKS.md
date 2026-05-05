# AI Context Packs

## Purpose

AI context packs are bounded, task-scoped JSON/Markdown packets that help a human or AI agent plan work on this repository.

They tell the next agent:

```text
which files to read
which validation ownership applies
which stop conditions protect the repo
which compact evidence can be reviewed on GitHub
```

They do not execute providers, apply patches, write `patch_specs/inbox/`, edit generated indexes or touch Blender runtime.

Current command examples live in the unified launcher runbook and validator README, not in this document:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/validation/README.md
```

## Full-run context-pack doctrine

Context packs are a lane of the unified local-AI flow.

`Full0To10` should include context-pack generation unless explicitly disabled or unavailable. `quick`, `balanced`, `deep` and `custom` can change context size and budgets, but not the fact that context-pack visibility belongs to the full-run perimeter.

Context packs are evidence-adjacent but not sufficient by themselves. When a context pack contributes to a production run or patch plan, it must be accompanied by the relevant telemetry/capability surfaces:

```text
unified launcher manifest
phase_status / phase_reports
context-pack evidence
runtime tool usage telemetry when tools executed
runtime tool capability manifest when tool capabilities are relevant
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
```

Telemetry does not replace the context pack. It explains whether the context-pack lane executed, failed, was skipped, was degraded or was only planned.

## Current toolchain

| Tool | Role | Full-run visibility |
|---|---|---|
| `Tools/ai/build_ai_context_pack.py` | Builds a local context pack under ignored `output/ai_context_packs/` and optional compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/`. | Manifest `context_files` / `phase_reports`; bundle reference when included in handoff. |
| `Tools/validation/check_ai_context_pack_contract.py` | Validates context-pack and context-pack-evidence contracts without executing providers. | Validation report and phase status. |

## Profiles

| Profile | Use |
|---|---|
| `project_self_improvement` | Default prototype for the repo planning its own next validated work. |
| `core_ai_backend` | Core orchestration, validation, lane routing and evidence work. |
| `npu_provider_diagnostics` | NPU/OpenVINO probe, guardrail and decode diagnostic work. |
| `artifact_pipeline` | AI artifact pipeline and dry-run matrix work. |
| `docs_only` | Documentation-only drift fixes and onboarding updates. |

## Outputs

Context pack outputs are local runtime artifacts:

```text
output/ai_context_packs/<profile>.json
output/ai_context_packs/<profile>.md
```

Compact Git-trackable evidence may be written under:

```text
docs/LOCAL_VALIDATION_EVIDENCE/<profile>_context_pack_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/<profile>_context_pack_evidence.md
```

Do not commit raw `output/**` context packs.

## Contract

Context pack JSON:

```text
schema_version
kind = ai_context_pack
generated_at
repo_root
profile
profile_description
apply_mode = context_only
provider_execution_performed = false
passed
errors
warnings
validation_commands
stop_conditions
files
```

Each file entry includes:

```text
path
role
required
exists
included
policy_ok
size_bytes
line_count
sha256
chars
included_chars
truncated
content
```

Evidence JSON:

```text
schema_version
kind = ai_context_pack_evidence
profile
source_pack
passed
provider_execution_performed = false
file_count
included_file_count
truncated_file_count
required_missing
forbidden_path_count
included_paths
decision
```

## Guardrails

Context packs must not include:

```text
indexAI/
output/
renders/
Ready To Jazz runtime files
Scripting/shared/blender_compat.py
full analysis JSON
patch_specs/inbox/
```

They may include compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/` when the evidence is intentionally selected for GitHub review.

## Interpretation

Context packs are not autonomous coding agents. They are context and validation planners.

The intended loop is now part of the unified launcher flow:

```text
select launcher mode/profile
  -> build context pack when selected
  -> validate context pack
  -> run task-specific validators
  -> optionally run explicit GPU/NPU provider/probe workflow
  -> build recommendations and patch-plan artifacts
  -> attach telemetry/capability surfaces for completeness
  -> commit only compact evidence when required
```

This gives future agents a smaller and safer working set before they produce proposals, patch specs or code changes.

## Future ideas

Future phases can build on this without changing the safety boundary:

- dry-run matrix evidence bundles for GitHub-only review;
- raw validators for provider probe and provider result reports;
- selective execution planner that chooses validators from changed files;
- richer context-pack profiles for memory, guardrail and NPU promotion experiments;
- NPU advisory promotion experiment only after multi-sample quality gates;
- richer context-pack telemetry fields when context-pack lanes become more complex.
