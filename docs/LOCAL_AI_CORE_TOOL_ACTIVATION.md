# Local AI Core/Tool Activation

This document defines the priority activation lane for IA-Carmine repository work.

## Intent

The project should now use the local AI core/tools to produce concrete artifacts that can be validated, reviewed and iterated on.

The activation lane is app-agnostic. It is not Blender-specific, audio-specific or provider-specific. Blender/audio remain downstream domains that consume the same repository workflow contracts.

## Philosophy

```text
artifact-first
validator-first
manual-review-only
provider execution explicit-only
app-agnostic core before domain runtime
macro patch as draft/spec, never automatic apply
```

The core/tool workflow should produce real artifacts:

```text
selected chunks
selected-chunks evidence
context pack
agent state packet
enrichment plan
adapter manifest
repository proposals
NPU knowledge-broker packet
GitHub evidence bundle
optional macro patch draft specs
```

These artifacts give the repo concrete material for review and tests instead of relying only on chat summaries.

## Runner

Use:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_core_tool_activation.ps1
```

Default behavior is provider-free and patch-free.

## Provider execution

Provider execution is opt-in only:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_core_tool_activation.ps1 `
  -UseExplicitProviders
```

This may run explicit Ollama/GPU and OpenVINO/NPU probes through the existing provider workflow, but it must still preserve:

```text
Ollama/GPU = primary advisory provider behind quality gate
NPU/OpenVINO = probe / guardrail / decode diagnostic / knowledge broker
OpenVINO GPU != primary lane
```

## Macro patch lane

Macro patch mode is allowed only as draft/spec generation:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_core_tool_activation.ps1 `
  -GenerateMacroPatchDrafts
```

Macro patch mode may produce:

```text
output/patch_specs/local_ai_core_tool_activation_patch_specs_manifest.json
output/patch_specs/local_ai_core_tool_activation_*.json
```

It must not:

```text
apply patches
queue patch specs for automatic execution
merge branches
rewrite source files directly
change Blender runtime
edit full analysis JSON
commit SQLite DB files
```

Macro patch promotion remains a separate reviewed step.

## Documentation patch-plan lane

For documentation-only manual-review patch plans, use the narrower task-specific lane rather than the full activation runner.

Canonical task and wrapper:

```text
docs/LOCAL_AI_TASKS/apply-agent-review-doc-patch-plan.md
Tools/validation/run_agent_review_patch_plan_full_validation.py
```

Expected compact evidence:

```text
docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.md
```

This lane is for already-generated review/evidence reports. It must remain:

```text
documentation-only
provider-free
patch-runner-free
manual-review-only
task-scoped evidence only
```

Use it when a GPU/NPU review has produced a manual-review patch plan and the next step is to apply small documentation corrections, not to run providers again.

## Contract drift validation lane

Use contract-drift validation when the repository has gained new workflow contracts, validators or evidence-bundle fields and the documentation/code map may have diverged.

Canonical guide:

```text
docs/CONTRACT_DRIFT_VALIDATION.md
```

Code contract drift validator:

```powershell
python .\Tools\validation\check_code_contract_drift.py `
  --repo-root . `
  --output .\output\validation\code_contract_drift.json `
  --markdown-output .\output\validation\code_contract_drift.md
```

Documentation contract drift validator:

```powershell
python .\Tools\validation\check_docs_contract_drift.py `
  --repo-root . `
  --output .\output\validation\docs_contract_drift.json `
  --markdown-output .\output\validation\docs_contract_drift.md
```

Expected semantics:

```text
kind = code_contract_drift or docs_contract_drift
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
manual_review_only for promotion
```

These reports are upstream signals for patch plans. They are not automatic apply queues.

## Combined local activation

For concrete local evidence with providers and macro patch draft specs:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_core_tool_activation.ps1 `
  -UseExplicitProviders `
  -GenerateMacroPatchDrafts
```

Use this when Carmine wants real workstation artifacts for deeper testing.

## AI workload report quality gate

The local AI core/tool activation lane should use the AI workload report quality gate after provider/probe reports exist and before generated workload reports influence advisory packets.

Canonical contract:

```text
docs/AI_WORKLOAD_REPORT_QUALITY_GATE.md
```

Validator:

```powershell
python .\Tools\validation\check_ai_workload_report_quality.py `
  --repo-root . `
  --output .\output\validation\ai_workload_report_quality.json
```

Expected routing semantics:

```text
Ollama/GPU usable_text -> primary advisory context
NPU/OpenVINO unusable_output -> excluded from advisory context
```

The quality gate remains report-only. It must not execute providers, promote NPU to advisory, introduce OpenVINO GPU as primary lane or apply patches.

## Expected outputs

```text
output/local_ai_runs/<timestamp>_local_ai_core_tool_activation/
output/ai_pipeline/local_ai_core_tool_activation_summary.json
output/ai_pipeline/local_ai_core_tool_activation_summary.md
output/ai_pipeline/local_ai_core_tool_activation_npu_knowledge_broker_packet.json
output/ai_pipeline/local_ai_core_tool_activation_npu_knowledge_broker_packet.md
output/validation/local_ai_core_tool_activation_adapter_manifest_contract.json
output/validation/local_ai_core_tool_activation_npu_knowledge_broker_packet_contract.json
output/validation/local_ai_core_tool_activation_github_evidence_bundle.json
docs/LOCAL_VALIDATION_EVIDENCE/local_ai_core_tool_activation_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/local_ai_core_tool_activation_evidence.md
```

If `-GenerateMacroPatchDrafts` is used, also expect draft-only patch specs under:

```text
output/patch_specs/
```

For the documentation patch-plan lane, expected tracked evidence is instead:

```text
docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.md
```

## Validation block

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
python .\Tools\validation\check_local_ai_adapter_manifest.py --repo-root . --manifest .\output\local_ai_runs\<run>\pipeline\local_ai_core_tool_activation_adapter_manifest.json --output .\output\validation\local_ai_core_tool_activation_adapter_manifest_contract.json
python .\Tools\validation\check_npu_knowledge_broker_packet.py --repo-root . --packet .\output\ai_pipeline\local_ai_core_tool_activation_npu_knowledge_broker_packet.json --output .\output\validation\local_ai_core_tool_activation_npu_knowledge_broker_packet_contract.json --min-candidates 3 --max-candidates 24
python .\Tools\validation\check_github_evidence_bundle.py --repo-root . --bundle .\docs\LOCAL_VALIDATION_EVIDENCE\local_ai_core_tool_activation_evidence.json --output .\output\validation\local_ai_core_tool_activation_github_evidence_bundle.json
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json
git diff --check
```

For macro patch drafts:

```powershell
python .\Tools\validation\check_patch_spec_drafts.py --repo-root . --manifest .\output\patch_specs\local_ai_core_tool_activation_patch_specs_manifest.json --output .\output\validation\local_ai_core_tool_activation_macro_patch_drafts.json
```

For agent-review documentation patch plans:

```powershell
python .\Tools\validation\run_agent_review_patch_plan_full_validation.py --repo-root . --min-patch-plans 12 --expect-fallback
```

For contract drift checks:

```powershell
python .\Tools\validation\check_code_contract_drift.py --repo-root . --output .\output\validation\code_contract_drift.json --markdown-output .\output\validation\code_contract_drift.md
python .\Tools\validation\check_docs_contract_drift.py --repo-root . --output .\output\validation\docs_contract_drift.json --markdown-output .\output\validation\docs_contract_drift.md
```

## Commit policy

Allowed tracked outputs:

```text
docs/LOCAL_VALIDATION_EVIDENCE/local_ai_core_tool_activation_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/local_ai_core_tool_activation_evidence.md
docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.md
docs/LOCAL_VALIDATION_EVIDENCE/<task-scoped_contract_drift_evidence>.json
docs/LOCAL_VALIDATION_EVIDENCE/<task-scoped_contract_drift_evidence>.md
```

Do not commit:

```text
output/**
output/patch_specs/**
indexAI/agent_memory/**
SQLite DB files
raw provider outputs
full analysis JSON files
manual generated-index edits
```

## Guardrails

The activation lane must remain:

```text
app-agnostic
report-only by default
provider-free by default
manual-review-only for macro patch
destructive-operation-free
```

The documentation patch-plan and contract-drift lanes inherit the same guardrails and additionally stay task-scoped to explicit validation/evidence artifacts.
