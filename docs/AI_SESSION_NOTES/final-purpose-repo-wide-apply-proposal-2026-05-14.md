# Final Purpose Repo-Wide Apply Proposal - 2026-05-14

## Purpose

This is the decision document for the current local session. It converts the
heap universe run, deterministic repository inventories, and local source
inspection into concrete coding work that can be accepted, split, postponed, or
rejected before application.

No commit, push, merge, destructive cleanup, generated evidence commit, or broad
provider semantic change is authorized by this document alone.

## Composition Package

This file is the operator decision index. The final product is now composed from
six persistent pieces, so a future GPU1 run can refine existing chunks instead
of starting again from a thin one-shot answer.

Pieces:

1. This decision index:
   `docs/AI_SESSION_NOTES/final-purpose-repo-wide-apply-proposal-2026-05-14.md`.
2. GPU1 iteration contract:
   `docs/AI_SESSION_NOTES/final-purpose-composition-iteration-contract-2026-05-14.md`.
3. Apply package detail:
   `docs/AI_SESSION_NOTES/final-purpose-composition-apply-packages-detail-2026-05-14.md`.
4. Repo coverage and validation:
   `docs/AI_SESSION_NOTES/final-purpose-composition-repo-coverage-and-validation-2026-05-14.md`.
5. Complete run verification:
   `docs/AI_SESSION_NOTES/final-purpose-complete-run-verification-2026-05-14.md`.
6. Code execution matrix:
   `docs/AI_SESSION_NOTES/final-purpose-code-execution-heap-tool-2026-05-14.md`.

Composition rule:

- Do not treat this as a single final answer window.
- GPU1 may re-open and enrich any existing piece when the target is valid but
  under-specified.
- A richer final decision should be built by COMPOSE/REFINE over the pieces:
  add exact targets, acceptance criteria, validation, risks and apply order.
- If a candidate still uses fake paths, placeholders, or non-existing targets,
  keep it as negative evidence and do not turn it into a patch proposal.

## Current Decision

Recommended immediate application scope:

1. Accept the proposal gate candidate already present in the working tree.
2. Add the small heap wrapper `--request-file` hardening patch next.
3. Fix the fatal `docs/LOCAL_AI_RUN_BOOTSTRAP.md` split-link drift.
4. Add the guarded heap code execution matrix for compile/test/diff evidence.
5. Do not apply broad line-budget or documentation-pruning work in the same
   patch.

Reason:

- The heap provider product was useful as negative evidence, but not acceptable
  as a coding proposal.
- The deterministic gate and local inspection found concrete source work.
- Repo-wide hygiene is real, but too broad for the first apply package.

## Evidence Snapshot

Working tree at the first decision point:

- Modified: `Tools/ai/heap_final_proposals/cli.py`.
- Untracked candidate: `Tools/ai/_shared/heap_proposal_gate.py`.
- Untracked candidate: `Tools/validation/test_proposal_gate.py`.
- Untracked note: `docs/AI_SESSION_NOTES/final-purpose-coding-modifications-2026-05-14.md`.
- Untracked local toolbox: `.claude-tools/repo_toolbox.py`.
- Ignored/generated local cache: `.claude-tools/__pycache__/`.

Heap run:

- Run dir: `output/validation/heap_context_closure_codex_final_purpose_20260514-081106`.
- Documents package:
  `C:/Users/carmi/Documents/aicarmine_heap_final_proposals_20260514-081125`.
- Preflight: passed.
- Startup reload: passed, not degraded.
- GPU0 and NPU evidence: present.
- Heap runtime: passed.
- Composer package: written, but composer returned `2` because product
  acceptance was blocked.
- Operator decision: `DIAGNOSTIC_ONLY`.
- Accepted proposals: `0`.
- Rejected proposals: `4`.

Provider failure captured:

- GPU1 repeatedly emitted `tools/.../real_existing_file.py`.
- The repeated patch was fake `process_data` sample code, not a real repo
  modification.
- GPU0 and NPU rejected the proposal as non-concrete.
- The new deterministic operator gate preserved that as an explicit block
  instead of turning it into a false proposal.

Repo-wide deterministic inventory:

- Script inventory passed: 593 scripts, 554 Python, 39 PowerShell.
- Markdown inventory passed after composition: 756 Markdown files,
  461 compact evidence files, 84 local AI task entrypoints,
  99 files needing index/lifecycle review,
  7 prune candidates.
- File line limit check passed only because violations are advisory:
  1350 files checked, 164 advisory violations, 0 enforced violations.
- Docs link validation now passes after Package B. The prior failure was the
  missing `part-002.md` link under `docs/LOCAL_AI_RUN_BOOTSTRAP.md`.

Mandatory-doc drift in this checkout:

- Missing: `CHATGPT.md`, `CHATGPT/README.md`,
  `docs/LOCAL_AI_TASKS/documentation-code-alignment-audit-2026-05-10.md`,
  `docs/LOCAL_AI_TASKS/problems-and-hygiene-candidates-2026-05-10.md`,
  `docs/LOCAL_AI_TASKS/repository-hygiene-cleanup-and-refactor-procedure-2026-05-09.md`,
  `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md`,
  `docs/LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md`,
  `docs/MAIN_RUNTIME_ARCHITECTURE.md`,
  `docs/LOCAL_AI_TASKS/patch-suggestion-review-workflow-2026-05-07.md`.

## Apply Package A - Proposal Gate Candidate

Status: already implemented in the current working tree, not committed.

Files:

- `Tools/ai/heap_final_proposals/cli.py`
- `Tools/ai/_shared/heap_proposal_gate.py`
- `Tools/validation/test_proposal_gate.py`

Problem:

- The composer could package heap output, but operator acceptance was too weak.
- Fake paths and repeated rejected suggestions could still appear as proposal
  material unless a deterministic gate surfaced them.
- A previous local attempt started this gate but left it nonfunctional:
  proposal gate state was not populated, the decision section was not rendered,
  and `OPERATOR_DECISION.txt` handling was incomplete.

Concrete implementation:

- Extracted deterministic proposal gating to `Tools/ai/_shared/heap_proposal_gate.py`.
- Composer now loads raw proposal chunks, gates them, renders an
  `Operator decision` Markdown section, and writes `OPERATOR_DECISION.txt` into
  the Documents package.
- Gate checks include fake path markers, placeholder markers, optional source
  allowlist, reviewable target extraction, and repeated rejected proposal
  similarity.
- Added stdlib smoke coverage for fake-source rejection, repeated-rejection loop
  breaking, and accepted patchable target behavior.

Acceptance criteria:

- Fake `tools/.../real_existing_file.py` proposals are blocked.
- Repeated rejected proposals are visible as operator gate reasons.
- A real accepted target can still pass the gate.
- The composer output contains a machine-readable `operator_decision` block and
  a human-readable decision file.

Validation already performed:

```powershell
& $RepoPy -m py_compile .\Tools\ai\heap_final_proposals\cli.py -m Tools.ai heap_proposal_gate .\Tools\validation\test_proposal_gate.py
& $RepoPy -m Tools.validation test_proposal_gate
git diff --check
```

Line counts:

- `Tools/ai/heap_final_proposals/cli.py`: 1147 lines, still oversized.
- `Tools/ai/_shared/heap_proposal_gate.py`: 275 lines.
- `Tools/validation/test_proposal_gate.py`: 149 lines.

Risk:

- `compose_heap_final_proposals.py` remains above the 400-line policy. This is
  existing technical debt plus a small current edit, so Package D should split
  it later.

## Apply Package B - Immediate Wrapper And Docs Fixes

Status: proposed next, not yet applied.

### B1 - Add `--request-file` to the standalone heap wrapper

Target:

- `Tools/ai/heap_context_closure/cli.py`

Problem:

- The first launch failed because a long multiline `--request` was fragile under
  PowerShell `Start-Process` argument passing.
- Downstream tools already use request files; the wrapper should accept one at
  the operator boundary too.

Concrete change:

- Add `--request-file`.
- If present, read UTF-8 text from the file and use it as the base request.
- Preserve current `--request` fallback behavior.
- Report the source request path in launcher JSON.

Acceptance:

- Long prompts no longer depend on shell argument quoting.
- Existing `--request` invocations remain compatible.

### B2 - Fix fatal `LOCAL_AI_RUN_BOOTSTRAP` split drift

Targets:

- `docs/LOCAL_AI_RUN_BOOTSTRAP.md/README.md`
- `docs/LOCAL_AI_RUN_BOOTSTRAP.md/part-001.md`
- `docs/LOCAL_AI_RUN_BOOTSTRAP.md/_ia_carmine_md_split_manifest.json`

Problem:

- The split index and manifest claim `part-002.md`, but the file is absent.
- `Tools/validation/check_docs_links.py` fails with 2 fatal errors.

Concrete safe option:

- If the missing content cannot be recovered, convert this split container to a
  one-part container: remove the `part-002.md` link and set manifest
  `part_count` to `1`.

Acceptance:

- `check_docs_links.py` passes.
- No invented documentation content is created.

## Apply Package C - Heap Provider Hardening

Status: proposed, apply after A and B.

Targets:

- `Tools/ai/heap_runtime/completeness_gate/cli.py`
- Existing or new focused smoke under `Tools/validation/`.

Problem:

- GPU1 consumed the operator guardrail but still emitted fake sample paths.
- The deterministic composer gate catches this at the end; the runtime loop
  should also stop recycling the bad candidate earlier.

Concrete changes:

- Feed GPU1 an explicit current-run target allowlist made from verified
  repo-relative paths.
- Treat paths containing `...`, angle-bracket placeholders, or
  `real_existing_file.py` as terminal non-concrete evidence.
- On repeated non-concrete output, force the next revision step to either
  rewrite with a verified target or emit `EXIT_DECISION=NO_PATCHABLE_TARGET`.
- Add a smoke fixture with a fake-path provider response and assert that the
  next revision context does not accept or repeat it as a patch candidate.

Acceptance:

- Provider failure becomes early-loop feedback, not only final-package failure.
- GPU0/NPU rejection remains visible.
- Product status can still become `DIAGNOSTIC_ONLY` when appropriate, but the
  reason is direct and non-ambiguous.

## Apply Package D - Composer And Runtime Line-Budget Work

Status: backlog, not first patch.

High-risk oversized owners:

- `Tools/ai/heap_runtime/completeness_gate/cli.py`: 4785 lines.
- `Tools/ai/heap_final_proposals/cli.py`: 1147 lines after Package A.
- `Tools/ai/heap_context_closure/cli.py`: 908 lines.
- Multiple `Tools/ai/*`, `Tools/workflow/*`, and `Tools/validation/*` files
  remain over the 400-line script policy.

Concrete composer split:

- Move document package writing to `Tools/ai/heap_final_package_writer.py`.
- Move proposal/provider collection to `Tools/ai/heap_final_report_collectors.py`.
- Keep `compose_heap_final_proposals.py` as CLI orchestration.

Concrete runtime split:

- Split prompt construction, provider revision state, peer evidence absorption,
  and final report writing out of `python -m Tools.ai run_heap_runtime_completeness_gate`.
- Keep behavior stable and validate after each small extraction.

Acceptance:

- No behavior change without matching smoke evidence.
- Each new helper is under 400 lines.
- Original oversized files trend downward instead of accumulating new logic.

## Apply Package E - Documentation And Index Hygiene

Status: backlog, separate docs PR or patch bundle.

Findings:

- 752 Markdown files are present.
- 95 need index/lifecycle review.
- 7 are prune candidates, mostly old `CHATGPT/` notes plus
  `guida_git_github_blender_audio_project.md` and `problems.md`.
- Maintained docs with line issues include `AGENTS.md`,
  `Tools/workflow/README.md`, `Tools/validation/README.md`, and several
  `docs/LOCAL_AI_TASKS/*` entries.

Concrete changes:

- Reconcile the missing mandatory docs: either restore them, replace references
  with current canonical paths, or mark them historical in `AGENTS.md` and the
  docs index.
- Run the repository Markdown split/refactor tool for maintained oversized docs,
  not manual bulk rewrites.
- Keep generated evidence as evidence, not canonical source docs.

Acceptance:

- Docs link validator passes.
- Markdown inventory still passes.
- No generated evidence is committed as maintained source.

## Apply Package F - `.claude-tools` Boundary

Status: explicit decision needed.

File:

- `.claude-tools/repo_toolbox.py` at 260 lines.

Decision options:

- Keep local-only: leave untracked and ensure `.claude-tools/__pycache__/` is
  ignored/excluded.
- Promote to repo tooling: move the `.py` into a maintained `Tools/*` owner,
  add README/tool inventory coverage, and add smoke validation.

Recommendation:

- Do not include `.claude-tools` in Package A. Classify it first.

## Apply Sequence

Recommended order:

1. Package A: accept the already implemented proposal gate candidate.
2. Package B: add `--request-file` and fix the fatal bootstrap split link.
3. Package C: harden provider revision feedback against fake paths.
4. Package D: split composer/runtime files in small extraction passes.
5. Package E: reconcile docs/index/line-budget drift in a dedicated docs pass.
6. Package F: decide whether `.claude-tools` is local-only or promotable.

Validation matrix for Packages A and B:

```powershell
$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:IA_CARMINE_PYTHON = $RepoPy
$env:PYTHONPATH = (Resolve-Path .).Path
& $RepoPy -m py_compile .\Tools\ai\heap_final_proposals\cli.py -m Tools.ai heap_proposal_gate .\Tools\validation\test_proposal_gate.py -m Tools.ai run_heap_runtime_context_closure
& $RepoPy -m Tools.validation test_proposal_gate
& $RepoPy -m Tools.validation check_docs_links --repo-root . --output output/validation/docs_links_after_final_purpose_apply.json
git diff --check
```

Optional provider smoke after Package C:

```powershell
& $RepoPy -m Tools.ai run_heap_runtime_context_closure --repo-root . --python-exe $RepoPy --request-file .\docs\AI_SESSION_NOTES\final-purpose-repo-wide-apply-proposal-2026-05-14.md --budget-minutes 3 --max-iterations 1 --max-provider-revisions 1 --no-documents --timeout-seconds 180
```

## Non-Goals For The First Apply

- Do not commit `output/**`, `indexAI/code_chunks/**`, `renders/**`,
  `*.db`, `*.sqlite`, or `*.sqlite3`.
- Do not merge, push, force-push, delete, or rewrite history.
- Do not run broad Blender renders or heavy provider workloads as part of the
  small acceptance patch.
- Do not treat generated heap proposals as source patches unless they pass the
  deterministic operator gate.

## Final Apply Recommendation

Apply Package A now if the goal is to preserve the real product from this
session: a deterministic gate that converts fake heap proposals into a clear
operator decision.

Then apply Package B immediately after, because it fixes the exact launch
fragility seen in this session and the current fatal docs-link validator
failure.

Packages C through F should be separate reviewable patches. They are real repo
work, but mixing them into Package A would make the decision surface too large
and harder to verify.
