# Final Purpose Coding Modifications - 2026-05-14

## Scope

This note is the concrete final-purpose artifact for the current local session.
The user requested a complete coding-oriented document after many local changes,
using heap universe runs as needed, and stopping only when a real final product
exists.

The final product is this coding modification document plus the validated source
changes listed below. It does not authorize automatic patch application, commit,
push, or generated artifact commits.

## Evidence Read

- Mandatory repo contract read: `AGENTS.md`.
- Active run/heap docs read: `docs/README.md`,
  `docs/LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md`,
  `docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md`,
  `docs/LOCAL_AI_TASKS/md-line-budget-triage-2026-05-10.md`,
  `docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md`,
  `docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md`,
  `docs/LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md`,
  `docs/LOCAL_AI_TASKS/standalone-heap-universe-incubation-2026-05-10.md`,
  `docs/LOCAL_AI_TASKS/standalone-heap-universe-tool-surface-2026-05-10.md`.
- Missing required docs in this checkout:
  `CHATGPT.md`, `CHATGPT/README.md`,
  `docs/LOCAL_AI_TASKS/documentation-code-alignment-audit-2026-05-10.md`,
  `docs/LOCAL_AI_TASKS/problems-and-hygiene-candidates-2026-05-10.md`,
  `docs/LOCAL_AI_TASKS/repository-hygiene-cleanup-and-refactor-procedure-2026-05-09.md`,
  `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md`,
  `docs/LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md`,
  `docs/MAIN_RUNTIME_ARCHITECTURE.md`,
  `docs/LOCAL_AI_TASKS/patch-suggestion-review-workflow-2026-05-07.md`.
- Split drift observed: `docs/LOCAL_AI_RUN_BOOTSTRAP.md/README.md` lists
  `part-002.md`, but only `part-001.md` exists.

## Heap Run Result

Run stamp: `codex_final_purpose_20260514-081106`.

Key outcomes:

- `preflight_passed=true`.
- `startup_reload_passed=true`.
- `startup_reload_degraded=false`.
- `provider_execution_performed=true`.
- GPU0 OpenVINO peer workload ran on `GPU.0`.
- NPU micro workload ran and reported availability for `CPU`, `GPU.0`,
  `GPU.1`, `NPU`.
- Final package exported to
  `C:\Users\carmi\Documents\aicarmine_heap_final_proposals_20260514-081125`.

Heap product status:

- `heap_passed=true`.
- `composer_packaging_performed=true`.
- `launcher_packaging_succeeded=true`.
- `composer_returncode=2`.
- Operator decision: `DIAGNOSTIC_ONLY`.

Reason the heap product was not accepted as the final coding answer:

- GPU1 repeatedly emitted an invented path:
  `tools/.../real_existing_file.py`.
- The proposal repeated the same fake `process_data` patch across revisions.
- GPU0 and NPU correctly vetoed the proposal as non-concrete.
- This is valid negative evidence: the heap ran, but the accepted coding product
  had to be assembled from local source inspection and deterministic validation.

## Implemented Coding Changes

### 1. Composer Operator Gate

Target: `Tools/ai/compose_heap_final_proposals.py`.

Problem found:

- The local change had started adding proposal gating directly in the composer,
  but the gate state was never populated.
- `filtered_proposals` stayed empty, so every run would report
  `NO CONCRETE PATCHABLE PROPOSAL` even when proposal artifacts existed.
- `OPERATOR_DECISION.txt` was written before the package directory was created.
- The decision section was passed to `render_markdown` but not rendered in the
  output document.
- Duplicate imports and a stray `pass` were introduced.

Concrete change:

- Composer now imports proposal gate helpers from `Tools/ai/_shared/heap_proposal_gate.py`.
- Proposal loading preserves `response_file_reference_quality`.
- Raw proposals are passed through deterministic operator gating.
- The final JSON includes `operator_decision`.
- The final Markdown includes an `Operator decision` section.
- The Documents package includes `OPERATOR_DECISION.txt`.

Acceptance:

- A heap package now reports why a proposal is accepted, diagnostic-only, or
  blocked.
- Fake paths and repeated rejected proposals remain visible instead of being
  silently collapsed.

Line count after change:

- `Tools/ai/compose_heap_final_proposals.py`: 1147 lines.

Residual risk:

- This file was already oversized relative to the 400-line code policy. The new
  helper below begins the progressive split, but the composer still needs a
  later decomposition pass.

### 2. Proposal Gate Helper

Target: `Tools/ai/_shared/heap_proposal_gate.py`.

Concrete change:

- Added deterministic helper functions for:
  source allowlist loading,
  repo path normalization,
  target extraction,
  placeholder/fake-path detection,
  repeated rejected proposal detection,
  operator decision construction,
  `OPERATOR_DECISION.txt` writing.

Acceptance:

- Missing allowlist files do not reject proposals.
- Existing empty allowlist files reject all targets by design.
- Existing allowlist files restrict accepted targets.
- Fake paths, unresolved placeholders, and repeated rejected proposals become
  explicit operator gate reasons.

Line count:

- `Tools/ai/_shared/heap_proposal_gate.py`: 275 lines.

### 3. Proposal Gate Smoke

Target: `Tools/validation/test_proposal_gate.py`.

Concrete change:

- Added a stdlib-only smoke script, runnable without `pytest`.
- Covers:
  fake source rejection,
  repeated rejected proposal detection,
  accepted patchable target behavior.

Acceptance:

- `python -m Tools.validation test_proposal_gate` passes.

Line count:

- `Tools/validation/test_proposal_gate.py`: 149 lines.

## Validation Performed

Commands run:

```powershell
$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:IA_CARMINE_PYTHON = $RepoPy
$env:PYTHONPATH = (Resolve-Path .).Path
& $RepoPy -c "import sys; print(sys.executable); import numpy, openvino; from openvino import Core; c=Core(); print(c.available_devices)"
& $RepoPy -m py_compile .\Tools\ai\compose_heap_final_proposals.py -m Tools.ai heap_proposal_gate .\Tools\validation\test_proposal_gate.py
& $RepoPy -m Tools.validation test_proposal_gate
git diff --check
```

Observed:

- OpenVINO devices: `['CPU', 'GPU.0', 'GPU.1', 'NPU']`.
- Ollama model `qwen2.5-coder:14b` is installed and visible.
- `py_compile` passed.
- Proposal gate smoke passed.
- `git diff --check` passed.
- `pytest` was not available in `.venv`; no dependency was installed.

## Concrete Next Coding Work

### P0 - Keep the proposal gate split

Commit scope when ready:

- `Tools/ai/compose_heap_final_proposals.py`
- `Tools/ai/_shared/heap_proposal_gate.py`
- `Tools/validation/test_proposal_gate.py`
- this note, if the final-purpose artifact should be tracked.

Do not include:

- `output/**`
- `indexAI/code_chunks/**`
- `*.db`, `*.sqlite`, `*.sqlite3`
- `renders/**`
- `.claude-tools/__pycache__/**`

### P1 - Add request-file support to the standalone heap wrapper

Target:

- `Tools/ai/run_heap_runtime_context_closure.py`

Reason:

- The first heap launch failed because a long multi-line `--request` was split
  by PowerShell `Start-Process` argument handling.

Concrete change:

- Add `--request-file`.
- If present, read UTF-8 text from that file and use it as the base request.
- Preserve current `--request` behavior as fallback.
- Include the request-file path in the launcher summary.

Validation:

```powershell
& $RepoPy -m py_compile .\Tools\ai\run_heap_runtime_context_closure.py
& $RepoPy -m Tools.ai run_heap_runtime_context_closure --repo-root . --python-exe $RepoPy --request-file .\path\to\request.md --skip-preflight --skip-startup-reload --no-documents --timeout-seconds 60
```

### P1 - Stop GPU1 from recycling fake sample paths

Target:

- `Tools/ai/run_heap_runtime_completeness_gate.py`

Observed failure:

- Even with a source allowlist contract in the prompt, GPU1 emitted
  `tools/.../real_existing_file.py`.
- The deterministic gate rejected it, but the provider loop repeated the same
  non-concrete patch three more times.

Concrete change:

- In `gpu1_provider_prompt()` or the revision feedback path, add a compact
  current-run target block containing only actual candidate paths:
  `Tools/ai/compose_heap_final_proposals.py`,
  `Tools/ai/_shared/heap_proposal_gate.py`,
  `Tools/validation/test_proposal_gate.py`.
- If GPU1 emits any path containing `...`, angle-bracket placeholders, or
  `real_existing_file.py`, force the next provider prompt to require
  `EXIT_DECISION=NO_PATCHABLE_TARGET` unless it rewrites with an exact allowed
  path.
- Add a smoke fixture that feeds a fake-path provider response and verifies the
  next revision context does not accept or repeat it.

Validation:

```powershell
& $RepoPy -m py_compile .\Tools\ai\run_heap_runtime_completeness_gate.py
& $RepoPy -m Tools.validation run_heap_source_allowlist_contract_smoke --repo-root .
```

### P2 - Decide the `.claude-tools` boundary

Target:

- `.claude-tools/repo_toolbox.py`
- `.claude-tools/__pycache__/repo_toolbox.cpython-314.pyc`

Current state:

- The directory is untracked.
- The `.pyc` file should not be committed.

Concrete choices:

- If this is temporary local tooling, leave it untracked and consider adding an
  ignore rule for `.claude-tools/__pycache__/`.
- If it is intended repo tooling, promote only the `.py` file through a proper
  owner path, README entry, and validation smoke.

### P2 - Continue composer decomposition

Target:

- `Tools/ai/compose_heap_final_proposals.py`

Reason:

- Current line count is 1061, still over the repository code policy.

Concrete next splits:

- Move document-package writing into `Tools/ai/heap_final_package_writer.py`.
- Move proposal/provider report collection into
  `Tools/ai/heap_final_report_collectors.py`.
- Keep `compose_heap_final_proposals.py` as CLI orchestration only.

Validation:

```powershell
& $RepoPy -m py_compile .\Tools\ai\compose_heap_final_proposals.py -m Tools.ai heap_final_package_writer .\Tools\ai\heap_final_report_collectors.py
& $RepoPy -m Tools.validation test_proposal_gate
git diff --check
```

## Final Decision

The accepted concrete coding product for this session is:

- deterministic operator gating in the heap final composer;
- an extracted proposal gate helper under the line budget;
- a stdlib smoke covering rejection, repetition, and acceptance;
- this final-purpose document describing the actual code work, validation,
  heap evidence, blockers, and next concrete coding patches.

The heap provider product itself remains diagnostic-only for this run because
the provider repeatedly generated an invented source path. That failure is now
captured and gated instead of being mistaken for a real coding proposal.
