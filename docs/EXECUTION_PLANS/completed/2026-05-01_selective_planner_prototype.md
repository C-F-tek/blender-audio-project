# Selective Planner Prototype

Status: completed
Date: 2026-05-01
Completed: 2026-05-01
Scope: core AI/backend orchestration, validation and evidence planning

## Goal

Create the first report-only selective planner prototype:

```text
context pack + evidence bundle -> recommended validators + candidate patch specs
```

The prototype must read existing context/evidence artifacts and produce JSON/Markdown recommendations. It must not apply patches or execute providers.

## Non-goals

- No Blender runtime changes.
- No Ready To Jazz changes.
- No `Scripting/shared/blender_compat.py` adoption.
- No manual generated-index edits.
- No full analysis JSON edits.
- No prompt prose, provider model, temperature or orchestration behavior changes.
- No implicit Ollama/OpenVINO/GPU/NPU execution.

## Planned files

| File | Action | Purpose |
|---|---|---|
| `Tools/ai/build_selective_execution_plan.py` | add | Build report-only selective execution plans. |
| `Tools/validation/check_selective_execution_plan.py` | add | Validate selective plan contract. |
| `docs/AI_SELECTIVE_PLANNER.md` | add | Stable documentation for the prototype. |
| `docs/EXECUTION_PLANS/active/2026-05-01_selective_planner_prototype.md` | add | Durable task control for this PR. |
| `Tools/validation/README.md` | update | Register validator command and tool map. |
| `docs/README.md` | update | Add documentation index entry. |

## Output paths

The planner writes ignored local outputs:

```text
output/ai_pipeline/selective_execution_plan.json
output/ai_pipeline/selective_execution_plan.md
```

The validator writes:

```text
output/validation/selective_execution_plan.json
```

## Validation commands

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
python .\Tools\ai\build_selective_execution_plan.py --repo-root . --output .\output\ai_pipeline\selective_execution_plan.json --markdown-output .\output\ai_pipeline\selective_execution_plan.md
python .\Tools\validation\check_selective_execution_plan.py --repo-root . --plan .\output\ai_pipeline\selective_execution_plan.json --output .\output\validation\selective_execution_plan.json
python .\Tools\validation\check_json_artifacts.py --repo-root . --output .\output\validation\json_artifacts.json
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
python .\Tools\validation\check_execution_plan_status.py --repo-root . --output .\output\validation\execution_plan_status.json
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json
git diff --check
```

## Local real GPU/NPU evidence command for Carmine

Only Carmine can run real GPU/NPU evidence on the workstation:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_parallel_ai_provider_multistep.ps1 `
  -Profile npu `
  -RunOllamaProbe `
  -RunNpuProbe `
  -RunNpuDecodeSmoke `
  -UsePrimaryAdvisoryProvider `
  -Basename parallel_gpu_npu_selective_planner_real `
  -ProposalBasename parallel_gpu_npu_selective_planner_real_proposals `
  -EvidenceBasename parallel_gpu_npu_selective_planner_real_evidence

python .\Tools\ai\build_github_evidence_bundle.py --repo-root . --basename parallel_gpu_npu_selective_planner_real_evidence
python .\Tools\validation\check_github_evidence_bundle.py --repo-root . --output .\output\validation\github_evidence_bundle.json
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json
```

## Acceptance criteria

- The planner output has `kind == selective_execution_plan`.
- `apply_mode == report_only`.
- `provider_execution_performed == false`.
- `patch_application_performed == false`.
- Recommended validators include the selective plan validator.
- Recommended patch specs remain manual-review-only candidates.
- Local-only GPU/NPU evidence commands are included when needed.
- Existing Blender/runtime guardrails remain untouched.

## Completion summary

Completed in PR #55 and merged by commit `f88c8453e0945bcb117372a3aa62e597010f030f`.

The local validation evidence for the selective planner real GPU/NPU workflow is recorded in:

```text
docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_selective_planner_real_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_selective_planner_real_evidence.md
```

## Risks

- Context-pack JSON evidence may be absent in GitHub-only mode; the planner may use the committed Markdown evidence fallback.
- Real provider freshness is bounded by the latest committed compact evidence bundle.
- This prototype recommends candidate patch specs but does not generate concrete replacement operations.
