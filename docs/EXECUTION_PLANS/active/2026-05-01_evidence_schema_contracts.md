# AI Evidence Schema Contracts

## Status

active

## Goal

Document the current AI orchestration evidence/report contracts and add a non-invasive validator for Git-trackable evidence bundles so GitHub-only agents can review local provider validation without requiring ignored `output/` trees.

## Scope

```text
Tools/validation/check_github_evidence_bundle.py
Tools/validation/README.md
docs/JSON_SCHEMAS.md
docs/AI_ARTIFACT_SCHEMAS.md
docs/TECH_DEBT_TRACKER.md
```

## Out of scope

```text
Blender runtime changes
provider execution behavior changes
model, temperature or prompt prose changes
full analysis JSON edits
generated index edits
OpenVINO/NPU promotion to primary advisory
```

## Provider lane policy

```text
Ollama -> GPU/CUDA -> primary advisory provider when quality routing allows it.
OpenVINO -> NPU -> explicit probe, guardrail and decode diagnostic only.
Unusable NPU workload output remains excluded from advisory context.
```

## Validation commands

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
python .\Tools\validation\check_github_evidence_bundle.py --repo-root . --output .\output\validation\github_evidence_bundle.json
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
python .\Tools\validation\check_execution_plan_status.py --repo-root . --output .\output\validation\execution_plan_status.json
```

## Risk level

low

The main risk is over-tightening historical evidence bundles. Mitigation: enforce root shape and required decision fields, but keep provider-specific extension fields warning-first.

## Progress log

- 2026-05-01: Started after PR #48 merge handoff; scope kept to documentation and report-only validation.
- 2026-05-01: Added `check_github_evidence_bundle.py` and documented AI orchestration report contracts for routing, NPU remediation, NPU decode smoke and GitHub evidence bundles.
- 2026-05-01: Local focused validators passed; historical pre-v2 bundles warn for missing optional `npu_decode_smoke_passed`.

## Future notes

- Add direct raw-output validators for `ai_workload_quality_lane_routing`, `npu_decode_quality_remediation` and `npu_decode_smoke_diagnostic` only after more local samples are stable.
- Keep compact evidence bundles under `docs/LOCAL_VALIDATION_EVIDENCE/`; do not commit ignored full `output/` report trees.
