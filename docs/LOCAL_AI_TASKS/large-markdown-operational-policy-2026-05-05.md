# Large Markdown operational policy — 2026-05-05

## Status

Current doc-only policy for IA-Carmine Markdown that is too large to be reliably opened, reviewed or carried into a new AI/chat context.

## Rule

A Markdown file that is too large to be read comfortably by a future chat, local AI context pack or GitHub-only reviewer must not be a primary operational entrypoint.

Large Markdown may exist only as one of:

```text
historical/supporting reference
generated compact evidence with a manifest/summary
schema notebook / catalog
application-domain documentation
legacy forensic material
```

It must have a compact bridge, index entry or summary if it is still relevant.

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
docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

If any of these become too large, split or replace the operational content with a compact bridge.

## Large-file handling

When a maintained `.md` is too large:

```text
1. Do not keep adding operational state to it.
2. Create or update a compact bridge document.
3. Mark the large file as historical/supporting/catalog/evidence where appropriate.
4. Move current state, next steps and command ownership to the compact bridge.
5. Keep executable commands in their canonical runbook/tool README only.
6. Do not delete the large file without explicit approval.
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
```

## Current doctrine reminder

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = presets or operator parameters
-No* flags = explicit opt-out from selected lanes
CSV/index/discovery surfaces are evidence lanes when relevant
```

Large historical files must not override this current compact doctrine.

## Review policy

For deep MD consistency work:

```text
Prefer small focused patches.
Prefer compact bridge docs.
Avoid rewriting very large Markdown files through API unless the target diff is tiny and safe.
Use Markdown inventory and line/count surfaces locally when available.
Treat files that cannot be opened reliably as non-primary until split or summarized.
```
