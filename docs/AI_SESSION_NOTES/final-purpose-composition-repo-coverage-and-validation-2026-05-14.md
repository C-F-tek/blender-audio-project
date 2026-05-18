# Final Purpose Composition - Repo Coverage And Validation - 2026-05-14

## Purpose

This piece records the repository coverage behind the final-purpose proposal.
It keeps evidence separate from the operator decision index.

## Coverage Sources

Read or inspected:

- repository contract and current run docs;
- heap and standalone universe docs;
- current source owners for composer and heap closure;
- generated heap run output;
- script inventory;
- Markdown inventory;
- file line-limit report;
- docs link report;
- git status and diff.

## Heap Evidence

Successful evidence:

- preflight passed;
- startup reload passed;
- startup reload was not degraded;
- GPU0 evidence was present;
- NPU evidence was present;
- heap runtime passed;
- final Documents package was written.

Blocked product evidence:

- composer returned `2`;
- product acceptance was blocked;
- accepted proposal count was `0`;
- rejected proposal count was `4`;
- GPU1 repeated a fake path;
- GPU0 and NPU vetoed the non-concrete proposal.

Conclusion:

- The heap run is valid diagnostic evidence.
- It is not an accepted source patch proposal.

## Complete Run Verification

First composition run:

- Run dir:
  `output/validation/heap_context_closure_final_purpose_composition_verify_20260514_0848`.
- Documents package:
  `C:/Users/carmi/Documents/aicarmine_heap_final_proposals_20260514-084605`.
- Provider execution: performed.
- Proposal chunks: 7.
- Product acceptance: blocked.
- Reason: GPU1 repeated fake source paths despite prompt-level guidance.

Second composition run after terminal-loop hardening:

- Run dir:
  `output/validation/heap_context_closure_final_purpose_composition_verify2_20260514_0854`.
- Documents package:
  `C:/Users/carmi/Documents/aicarmine_heap_final_proposals_20260514-085107`.
- Preflight: passed.
- Startup reload: passed, not degraded.
- Heap runtime: passed.
- Composer packaging: performed.
- Provider execution: performed.
- GPU0 and NPU roles: present.
- Proposal chunks: 2.
- Product acceptance: blocked, diagnostic-only.
- Terminal event: `provider_revision_terminal_no_patchable_target`.

Conclusion:

- The new final-purpose composition was exercised by a complete run.
- The provider still failed to produce an accepted patchable proposal.
- The deterministic loop hardening worked: repeated fake proposals were stopped
  after one failed revision instead of consuming all six revisions.

## Deterministic Inventory

Latest post-update values:

- script inventory passed;
- script count: 593;
- Markdown inventory passed;
- Markdown count: 756;
- missing index/lifecycle review count: 99;
- prune candidates: 7;
- line-limit report passed in advisory mode;
- checked files: 1350;
- advisory violations: 164;
- enforced violations: 0.

## Docs Link State

Before Package B:

- docs link validator failed;
- fatal errors: 2;
- both errors pointed at missing `part-002.md` under
  `docs/LOCAL_AI_RUN_BOOTSTRAP.md`.

After Package B:

- docs link validator passes;
- failed count: 0;
- broken link count: 0.
- If it still fails, the new errors should be treated as Package F scope.

## Line-Budget State

Changed or candidate code files:

- `Tools/ai/heap_final_proposals/cli.py`: oversized, 1147 lines before the
  latest wrapper/prompt edits.
- `Tools/ai/_shared/heap_proposal_gate.py`: under budget.
- `Tools/validation/test_proposal_gate.py`: under budget.
- `Tools/ai/heap_context_closure/cli.py`: oversized, 945 lines after
  Package B.
- `Tools/ai/heap_runtime/completeness_gate/cli.py`: heavily oversized,
  4787 lines after Package C.

Decision:

- Do not let line-budget debt block the narrow correctness patches.
- Do create follow-up split packages for the oversized runtime owners.

## Validation Commands

Required after A/B/C:

```powershell
$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:IA_CARMINE_PYTHON = $RepoPy
$env:PYTHONPATH = (Resolve-Path .).Path
& $RepoPy -m py_compile .\Tools\ai\heap_final_proposals\cli.py -m Tools.ai heap_proposal_gate .\Tools\validation\test_proposal_gate.py -m Tools.ai run_heap_runtime_context_closure .\Tools\ai\heap_runtime\completeness_gate\cli.py
& $RepoPy -m Tools.validation test_proposal_gate
& $RepoPy -m Tools.validation check_docs_links --repo-root . --output output/validation/docs_links_after_final_purpose_apply.json
git diff --check
```

Additional validation after code execution matrix:

```powershell
& $RepoPy -m py_compile `
  .\Tools\ai\heap_runtime\code_execution_tool\cli.py `
  .\Tools\ai\_shared\heap_code_execution_tool_core.py `
  .\Tools\validation\run_heap_code_execution_tool_smoke.py `
  .\Tools\ai\agent_runtime_tool_broker.py `
  .\Tools\ai\heap_runtime\completeness_gate\cli.py

& $RepoPy -m Tools.validation run_heap_code_execution_tool_smoke `
  --repo-root . `
  --output output/validation/heap_code_execution_tool_smoke_after_split_20260514.json `
  --markdown-output output/validation/heap_code_execution_tool_smoke_after_split_20260514.md
```

Result:

- direct code execution matrix passed;
- brokered code execution matrix passed;
- new files are below 400 lines;
- no provider execution, patch application, source writes or git writes were
  performed by the tool.

Optional request-file smoke:

```powershell
& $RepoPy -m Tools.ai run_heap_runtime_context_closure --repo-root . --python-exe $RepoPy --request-file .\docs\AI_SESSION_NOTES\final-purpose-repo-wide-apply-proposal-2026-05-14.md --skip-preflight --skip-startup-reload --no-documents --timeout-seconds 60
```

## Risks

- Package C changes provider prompt behavior; it should improve iteration, but
  provider output remains non-deterministic.
- Runtime files are already oversized; every new edit should be followed by a
  split/refactor pass.
- The missing mandatory docs indicate contract drift that must be resolved in a
  docs-focused pass.
- Generated heap output is useful evidence but must not be committed as source.
