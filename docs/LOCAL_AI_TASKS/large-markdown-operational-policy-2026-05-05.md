# Large Markdown operational policy — 2026-05-05

## Status

Current policy for IA-Carmine Markdown that is too large to be reliably opened, reviewed or carried into a new AI/chat context.

Numeric policy:

```text
Active maintained Markdown hard threshold: 500 lines
Preferred active runbook size: 400 lines
```

## Rule

A maintained Markdown file above 500 lines must not remain a primary operational entrypoint in monolithic form.

Large Markdown may exist only as one of:

```text
historical/supporting reference
generated compact evidence with a manifest/summary
schema notebook / catalog
application-domain documentation
legacy forensic material
```

It must have a compact bridge, index entry or summary if it is still relevant.

## Required split layout

When an active maintained Markdown file would exceed 500 lines:

```text
Keep the original file as a compact index.
Create a sibling folder named exactly like the file, including .md: <file>.md/.
Move detailed content into <file>.md/part-001.md, part-002.md, ...
Keep each part <= 500 lines.
The index must list all parts and state that the document was split for the line-budget policy.
```

Example:

```text
docs/LOCAL_AI_TASKS/example.md
docs/LOCAL_AI_TASKS/example.md/part-001.md
docs/LOCAL_AI_TASKS/example.md/part-002.md
```

## Primary path requirement

The primary reading path must stay compact and openable:

```text
AGENTS.md
CHATGPT.md
CHATGPT/README.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
README.md
WORKFLOW.md
docs/README.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/gpu-peer-exchange-operational-principle.md
docs/LOCAL_AI_TASKS/md-coherence-only-github-pass-2026-05-06.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

If any primary-path file exceeds 500 lines, split it or replace the operational content with a compact bridge.

## Large-file handling

When a maintained `.md` is above 500 lines:

```text
1. Do not keep adding operational state to it.
2. Create or update a compact bridge document.
3. Mark the large file as historical/supporting/catalog/evidence where appropriate.
4. Move current state, next steps and command ownership to the compact bridge.
5. Keep executable commands in their canonical runbook/tool README only.
6. Do not delete compact evidence automatically.
```

## Current examples

```text
docs/JSON_SCHEMAS.md
  -> schema notebook / broad historical catalog
  -> current launcher semantics belong in docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
  -> current run-unica state belongs in docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md

docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md
  -> historical/supporting snapshot
  -> current commands belong in docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md

Tools/validation/README.md
  -> oversized validator catalog / technical debt
  -> new validator notes should be compact task docs until the catalog is split
```

## Current doctrine reminder

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = budget/intensity, not scope reduction
-No* flags = explicit opt-out from selected lanes
CSV/index/discovery/file-line-limit surfaces are evidence lanes when relevant
GPU1/Ollama/RTX5080 = mandatory primary advisory planner
GPU0/OpenVINO = companion peer worker
NPU = micro-fast task/tool-support lane
```

Large historical files must not override this current compact doctrine.

## Validator

Use the report-only line-limit validator to measure current drift:

```text
Tools/validation/check_file_line_limits.py
docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
```

The validator reports oversized files. It does not split, rewrite or delete anything.

## Review policy

For deep MD consistency work:

```text
Prefer small focused patches.
Prefer compact bridge docs.
Avoid rewriting very large Markdown files through API unless the target diff is tiny and safe.
Use Markdown inventory and file line-limit reports when available.
Treat files that cannot be opened reliably as non-primary until split or summarized.
```
