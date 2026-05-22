# AI Context Pack Self-Improvement Prototype

## Status

completed

## Goal

Create the first non-invasive prototype for the repository helping work on itself: task-scoped AI context packs that select relevant files, validation commands and stop conditions, plus compact evidence that can be reviewed on GitHub.

## Scope

- Add a context-pack builder under `ia_carmine/`.
- Add a context-pack contract validator under `Tools/validation/`.
- Add stable documentation for profiles, output contracts and guardrails.
- Generate and commit one compact evidence bundle for `project_self_improvement`.
- Correct small documentation drift discovered in the pre-existing analysis where it affects current AI onboarding.

## Guardrails

- No Blender runtime changes.
- No Ready To Jazz edits.
- No broad `Scripting/shared/blender_compat.py` adoption.
- No full analysis JSON edits.
- No generated index hand-edits.
- No provider execution.
- No patch-spec queue writes.
- No changes to models, temperature, prompt prose or provider execution policy.

## Validation Plan

```powershell
python -m Tools.validation check_python_syntax --repo-root . --output .\output\validation\python_syntax.json
python -m ia_carmine.cli build_ai_context_pack --repo-root . --profile project_self_improvement
python -m Tools.validation check_ai_context_pack_contract --repo-root . --pack .\output\ai_context_packs\project_self_improvement.json --evidence .\docs\LOCAL_VALIDATION_EVIDENCE\project_self_improvement_context_pack_evidence.json --output .\output\validation\ai_context_pack_contract.json
python -m Tools.validation check_json_artifacts --repo-root . --output .\output\validation\json_artifacts.json
python -m Tools.validation check_docs_links --repo-root . --output .\output\validation\docs_links.json
python -m Tools.validation check_execution_plan_status --repo-root . --output .\output\validation\execution_plan_status.json
python -m Tools.validation check_validation_report_contract --repo-root . --output .\output\validation\validation_report_contract.json
```

## Exit Criteria

- Context pack builder passes syntax validation.
- Default `project_self_improvement` pack builds under ignored `output/ai_context_packs/`.
- Compact context-pack evidence is written under `docs/LOCAL_VALIDATION_EVIDENCE/`.
- Validator passes for both pack and evidence.
- Docs describe profiles and safety boundary.

## Result

- Added a non-invasive AI context-pack builder and contract validator.
- Documented task-scoped context packs, schemas, validation and workflow placement.
- Generated the first compact context-pack evidence bundle for `project_self_improvement`.
- Corrected small documentation drift around the post-PR #48 baseline.
- Kept provider execution disabled and did not touch Blender runtime, Ready To Jazz, `blender_compat.py`, full analysis JSON or generated indexes.
