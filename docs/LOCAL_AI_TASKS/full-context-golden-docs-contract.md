# Full-Context Golden Docs Contract

This document defines P3: the full-context golden path documentation contract.

## Purpose

The full-context golden path is the stable repository contract for local AI/NPU/GPU workflow tasks. It connects task Markdown, bootstrap instructions, workflow docs, validation docs and compact evidence without requiring implicit provider execution.

The contract is docs-only and report-only. It exists so future agents can verify the golden-path documentation layer before proposing or implementing workflow changes.

## Required source documents

The contract spans these tracked files:

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_WORKFLOW.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/full-context-ai-npu-golden-path.md
docs/LOCAL_AI_TASKS/full-context-golden-docs-contract.md
docs/JSON_SCHEMAS.md
Tools/validation/README.md
```

## Required golden-path semantics

The documentation layer must preserve these semantics:

```text
report-only
proposal-only
manual-review-only
provider execution explicit-only
no automatic patch apply
no automatic source rewrite
no automatic merge
```

The lane model must remain:

```text
Ollama/GPU remains primary advisory provider behind quality gates.
NPU remains knowledge broker, context oracle, probe, guardrail and decode diagnostic.
OpenVINO GPU must not become primary lane.
```

## Required workflow chain

The golden path must describe this bounded workflow:

```text
Task Markdown
  -> semantic code chunks
  -> selected focused chunks
  -> selected chunks evidence
  -> bounded context pack
  -> SQLite-backed agent state packet
  -> enrichment plan
  -> optional explicit provider workflow
  -> proposals
  -> draft patch specs
  -> compact GitHub evidence
  -> manual review / PR
```

## Required P-family coverage

The task and proposal contract must preserve these proposal families:

```text
P1 adapter manifest validator
P2 reusable enrichment-plan helper
P3 full-context golden path docs contract
P4 optional wrapper preset flag
P5 selected-chunks evidence standard validation block
P6 NPU knowledge-broker / context-oracle prototype
```

## Safe preset contract

The `-FullContextGoldenPath` wrapper preset is allowed only as a safe context-enrichment preset.

It may enable:

```text
semantic chunks
selected chunks
selected-chunks evidence
context pack
agent state packet
enrichment plan
standard golden-path basenames
```

It must not enable:

```text
provider execution
Ollama probe
NPU probe
NPU decode smoke
multistep provider workflow
patch spec generation
patch application
Blender runtime execution
```

## Compact evidence contract

Only compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/` may be committed for GitHub review.

Do not commit:

```text
output/**
output/ai_context_packs/**
output/local_ai_runs/**
output/patch_specs/**
indexAI/agent_memory/**
SQLite DB files
raw provider outputs
full analysis JSON files
```

## Validation command

Validate this contract with:

```powershell
python -m Tools.validation check_full_context_golden_docs_contract `
  --repo-root . `
  --output .\output\validation\full_context_golden_docs_contract.json
```

Recommended local validation block for P3 changes:

```powershell
python -m Tools.validation check_python_syntax --repo-root . --output .\output\validation\python_syntax.json
python -m Tools.validation check_full_context_golden_docs_contract --repo-root . --output .\output\validation\full_context_golden_docs_contract.json
python -m Tools.validation check_docs_links --repo-root . --output .\output\validation\docs_links.json
python -m Tools.validation check_validation_report_contract --repo-root . --output .\output\validation\validation_report_contract.json
git diff --check
```

## Guardrails

This contract must not be used to promote advisory providers, apply patches, run Blender, execute production workflows, rewrite history, change secrets or bypass manual review.
