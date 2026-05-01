# AI Context Packs

## Purpose

AI context packs are the first prototype of the repository helping plan work on itself.

They produce bounded, task-scoped JSON/Markdown packets that tell a human or AI agent:

```text
which files to read
which validation commands belong to the task
which stop conditions protect the repo
which compact evidence can be reviewed on GitHub
```

They do not execute providers, apply patches, write `patch_specs/inbox/`, edit generated indexes or touch Blender runtime.

## Current toolchain

| Tool | Role |
|---|---|
| `Tools/ai/build_ai_context_pack.py` | Builds a local context pack under ignored `output/ai_context_packs/` and an optional compact evidence file under `docs/LOCAL_VALIDATION_EVIDENCE/`. |
| `Tools/validation/check_ai_context_pack_contract.py` | Validates context-pack and context-pack-evidence contracts without executing providers. |

## Profiles

| Profile | Use |
|---|---|
| `project_self_improvement` | Default prototype for the repo planning its own next validated work. |
| `core_ai_backend` | Core orchestration, validation, lane routing and evidence work. |
| `npu_provider_diagnostics` | NPU/OpenVINO probe, guardrail and decode diagnostic work. |
| `artifact_pipeline` | AI artifact pipeline and dry-run matrix work. |
| `docs_only` | Documentation-only drift fixes and onboarding updates. |

## Build

Default prototype:

```powershell
python .\Tools\ai\build_ai_context_pack.py --repo-root . --profile project_self_improvement
```

Outputs:

```text
output/ai_context_packs/project_self_improvement.json
output/ai_context_packs/project_self_improvement.md
docs/LOCAL_VALIDATION_EVIDENCE/project_self_improvement_context_pack_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/project_self_improvement_context_pack_evidence.md
```

## Validate

```powershell
python .\Tools\validation\check_ai_context_pack_contract.py `
  --repo-root . `
  --pack .\output\ai_context_packs\project_self_improvement.json `
  --evidence .\docs\LOCAL_VALIDATION_EVIDENCE\project_self_improvement_context_pack_evidence.json `
  --output .\output\validation\ai_context_pack_contract.json
```

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

They may include compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/`.

## Prototype interpretation

The first prototype is intentionally not an autonomous coding agent. It is a context and validation planner.

The intended loop is:

```text
choose task profile
  -> build context pack
  -> validate context pack
  -> run task-specific validators
  -> optionally run explicit GPU/NPU multistep workflow
  -> build proposal/draft/reviewed patch artifacts
  -> commit compact evidence
```

This gives future agents a smaller and safer working set before they produce proposals, patch specs or code changes.

## Future ideas

Future phases can build on this without changing the safety boundary:

- dry-run matrix evidence bundles for GitHub-only review;
- raw validators for provider probe and provider result reports;
- selective execution planner that chooses validators from changed files;
- richer context-pack profiles for memory, guardrail and NPU promotion experiments;
- NPU advisory promotion experiment only after multi-sample quality gates.
