<!-- IA-CARMINE-MD-SPLIT: part -->
# README â€” parte 002 di 004

Sorgente indice: [`README.md`](README.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)
- [Parte successiva](part-003.md)

## Selective execution plan validation

The selective planner reads compact context/evidence artifacts and recommends the next validators plus candidate patch specs. It remains report-only.

Build and validate:

```powershell
python -m ia_carmine.cli build_selective_execution_plan --repo-root . --output .\output\ai_pipeline\selective_execution_plan.json --markdown-output .\output\ai_pipeline\selective_execution_plan.md
python -m Tools.validation check_selective_execution_plan --repo-root . --plan .\output\ai_pipeline\selective_execution_plan.json --output .\output\validation\selective_execution_plan.json
```

The validator checks:

```text
kind == selective_execution_plan
apply_mode == report_only
provider_execution_performed == false
patch_application_performed == false
recommended validators are command-bearing
recommended patch specs remain manual_review_only
local-only GPU/NPU evidence commands are present
```

This validator does not execute providers, run validators from the plan, apply patches, run Blender or write source targets.

## Selected semantic chunks validation

Selected semantic chunks are bounded focused-context bundles generated from the semantic chunk index. They are safe context inputs, not source patches.

Validate a selected chunk bundle and optionally emit compact evidence:

```powershell
python -m Tools.validation check_selected_semantic_chunks --repo-root . --bundle .\output\ai_context_packs\full_context_golden_selected_chunks.json --output .\output\validation\full_context_golden_selected_chunks_contract.json --evidence-output .\docs\LOCAL_VALIDATION_EVIDENCE\full_context_golden_selected_chunks_evidence.json --markdown-output .\docs\LOCAL_VALIDATION_EVIDENCE\full_context_golden_selected_chunks_evidence.md --max-total-chars 32000
```

The validator checks:

```text
kind == semantic_code_chunk_selection
source_writes_performed == false
provider_execution_performed == false
selected_count > 0
selected_count <= max_chunks
total_selected_chars stays within budget
chunk ids are unique
paths and line ranges are concrete
```

## Full-context golden proposal validation

The generic proposal validator checks schema shape. The full-context golden proposal validator adds semantic coverage requirements for the current golden path.

Run after generating deterministic full-context proposals:

```powershell
python -m ia_carmine.cli build_full_context_golden_proposals --repo-root . --source-report .\output\local_ai_runs\<run>\pipeline\full_context_golden_local_ai_context_proposals.json --output .\output\ai_pipeline\full_context_golden_proposals.json --markdown-output .\output\ai_pipeline\full_context_golden_proposals.md
python -m Tools.validation check_repository_change_proposals --repo-root . --proposal .\output\ai_pipeline\full_context_golden_proposals.json --output .\output\validation\full_context_golden_repository_proposals_contract.json
python -m Tools.validation check_full_context_golden_proposals --repo-root . --proposal .\output\ai_pipeline\full_context_golden_proposals.json --output .\output\validation\full_context_golden_proposals_contract.json --min-proposals 6
```

Required proposal families:

```text
P1 adapter manifest validator
P2 reusable enrichment-plan helper
P3 full-context golden path docs contract
P4 optional wrapper preset flag
P5 selected-chunks evidence standard validation block
P6 NPU knowledge-broker / context-oracle prototype
```

## Execution plan status validation

Completed plans must live under:

```text
docs/EXECUTION_PLANS/completed/
```

Active plans must not have top-level status `completed`, `abandoned` or `wont_fix`.

Run:

```powershell
python -m Tools.validation check_execution_plan_status --repo-root . --output .\output\validation\execution_plan_status.json
```

This check exists because completed plans left under `active/` confuse future AI task selection.

## GitHub evidence bundle validation

Compact evidence bundles under `docs/LOCAL_VALIDATION_EVIDENCE/` let GitHub-only agents review local AI/provider validation without needing ignored `output/` trees.

Run:

```powershell
python -m Tools.validation check_github_evidence_bundle --repo-root . --output .\output\validation\github_evidence_bundle.json
```

The validator checks:

```text
kind == github_validation_evidence_bundle
schema_version == 1
decision fields for Ollama/GPU primary advisory, NPU exclusion and provider execution
per-report summary fields: path, exists, json_ok, kind, passed, summary
```

Missing provider-specific optional fields are warnings, not blocking errors, so older evidence bundles remain readable while newer bundles can add richer provider decisions.

Other compact evidence kinds may also live under `docs/LOCAL_VALIDATION_EVIDENCE/`; this validator only checks `kind == github_validation_evidence_bundle` unless explicit `--bundle` paths are supplied.

## Repository change proposal validation

Repository proposal reports are generated suggestion artifacts. They may describe future code, Markdown, JSON, PowerShell or workflow changes, but they must remain manual-review-only.

Run after generating proposals:

```powershell
python -m Tools.validation check_repository_change_proposals --repo-root . --proposal .\output\ai_pipeline\repository_change_proposals.json --output .\output\validation\repository_change_proposals_contract.json
```

The validator checks:

```text
kind == repository_change_proposals
apply_mode == manual_review_only
proposal patch sketches, validation commands and stop conditions are present
suggestion_outputs describe target file kind and write policy
forbidden runtime/generated-index/full-analysis targets are not proposed
```

This validator does not execute providers, apply patches, run Blender or write suggestion targets.

## Proposal patch-spec draft validation

Proposal-derived patch specs turn validated repository proposals into reviewable patch-spec shells. They are written under ignored `output/patch_specs/`, contain target-file operations, and intentionally contain no replacements.

Generate drafts from a proposal report:

```powershell
python -m ia_carmine.cli generated_patch_specs_from_proposals --repo-root . --proposal .\output\ai_pipeline\repository_change_proposals.json --output-dir output\patch_specs --basename proposal_patch_specs
```

Validate the draft manifest:

```powershell
python -m Tools.validation check_patch_spec_drafts --repo-root . --manifest .\output\patch_specs\proposal_patch_specs_manifest.json --output .\output\validation\patch_spec_drafts.json
```

The validator checks:

```text
kind == proposal_patch_spec_manifest / proposal_patch_spec_draft
apply_mode == manual_review_only
draft_status == needs_concrete_replacements
provider_execution_performed == false
operations target existing concrete files
replacements are empty while the spec is a draft
drafts are not stored under patch_specs/inbox/
```

This validator does not execute providers, apply patch specs, run Blender or write source targets.

## Reviewed patch-spec validation

Reviewed patch specs are produced from a draft plus an explicit replacement plan. They still live under ignored `output/patch_specs/`, remain manual-review-only and are not copied to `patch_specs/inbox/` automatically.

Promote the fixture draft with dry-run:

```powershell
python -m ia_carmine.cli generated_patch_specs_promote_draft --repo-root . --draft .\ia_carmine\_shared\fixtures\patch_spec_review_draft.json --replacement-plan .\ia_carmine\_shared\fixtures\patch_spec_review_replacement_plan.json --output-dir output\patch_specs --basename reviewed_patch_spec_fixture
```

Validate the reviewed spec:

```powershell
python -m Tools.validation reviewed_patch_specs_check --repo-root . --manifest .\output\patch_specs\reviewed_patch_spec_fixture_manifest.json --output .\output\validation\reviewed_patch_specs.json
```

## AI context-pack validation

AI context packs collect bounded task-scoped repository context, validation commands and stop conditions for human/AI continuation. Full packs live under ignored `output/ai_context_packs/`; compact evidence can be committed under `docs/LOCAL_VALIDATION_EVIDENCE/`.

Build the default self-improvement prototype:

```powershell
python -m ia_carmine.cli build_ai_context_pack --repo-root . --profile project_self_improvement
```

Validate the pack and compact evidence:

```powershell
python -m Tools.validation check_ai_context_pack_contract --repo-root . --pack .\output\ai_context_packs\project_self_improvement.json --evidence .\docs\LOCAL_VALIDATION_EVIDENCE\project_self_improvement_context_pack_evidence.json --output .\output\validation\ai_context_pack_contract.json
```

The validator checks:

```text
kind == ai_context_pack / ai_context_pack_evidence
apply_mode == context_only
provider_execution_performed == false
required files are included
forbidden source/generated/runtime paths are blocked
validation commands and stop conditions are present
```

The validator checks:

```text
kind == reviewed_patch_spec_manifest / reviewed_patch_spec
apply_mode == manual_review_only
review_status == dry_run_passed
provider_execution_performed == false
operations target existing concrete files
replacements are present and structurally valid
reviewed specs are not stored under patch_specs/inbox/
dry-run still passes at validation time
```

This validator does not execute providers, apply patch specs, run Blender or write source targets.
