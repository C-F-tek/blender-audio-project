# AI Evidence Schema Contracts

## Status

active

## Current review note — 2026-05-07

This older execution plan remains under `active/`, but its original implementation work was already progressed on 2026-05-01. Treat it as **legacy active / schema-follow-up**, not as the primary current architecture task.

Before extending evidence schemas, read:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/MAIN_RUNTIME_ARCHITECTURE.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

The evidence schema direction must now account for:

```text
shared runtime heap / blackboard
broker unico executor
semantic tools registry
deterministic validators / CPU authority
telemetry/event stream
GPU1/GPU0/NPU lane status reports
```

Do not tighten old evidence bundles in a way that breaks historical review. New fields should be additive and warning-first until current samples are stable.

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

Historical policy from the original task:

```text
Ollama -> GPU/CUDA -> primary advisory provider when quality routing allows it.
OpenVINO -> NPU -> explicit probe, guardrail and decode diagnostic only.
Unusable NPU workload output remains excluded from advisory context.
```

Current target policy from the main runtime architecture:

```text
GPU1 -> primary advisory / planner
GPU0 -> coworker/helper OpenVINO
NPU -> microtask responder / probe / guardrail / decode diagnostic
broker unico executor -> tool execution gateway
CPU validators -> deterministic pass/fail authority
telemetry/event stream -> audit trail for executed, skipped, degraded and blocked phases
```

Evidence schemas must distinguish current implemented fields from future architecture-target fields.

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

The main risk is over-tightening historical evidence bundles. Mitigation: enforce root shape and required decision fields, but keep provider-specific and main-runtime extension fields warning-first.

## Progress log

- 2026-05-01: Started after PR #48 merge handoff; scope kept to documentation and report-only validation.
- 2026-05-01: Added `check_github_evidence_bundle.py` and documented AI orchestration report contracts for routing, NPU remediation, NPU decode smoke and GitHub evidence bundles.
- 2026-05-01: Local focused validators passed; historical pre-v2 bundles warn for missing optional `npu_decode_smoke_passed`.
- 2026-05-07: Reviewed as older active plan; aligned future schema direction with `docs/MAIN_RUNTIME_ARCHITECTURE.md` without changing validators.

## Future notes

- Add direct raw-output validators for `ai_workload_quality_lane_routing`, `npu_decode_quality_remediation` and `npu_decode_smoke_diagnostic` only after more local samples are stable.
- Add blackboard/broker/registry/validator-authority/event-stream schema checks as additive warning-first fields after code emits real reports.
- Keep compact evidence bundles under `docs/LOCAL_VALIDATION_EVIDENCE/`; do not commit ignored full `output/` report trees.
- Consider moving this plan to `completed/` in a later explicit execution-plan cleanup.
