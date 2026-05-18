# Final Purpose Code Execution Heap Tool - 2026-05-14

## Purpose

This piece records the applied coding expansion requested after the complete
final-purpose verification: the heap/universe must be able to turn concrete
coding proposals into guarded compile/test/diff evidence, not only narrative
provider text.

## Applied Files

New:

- `Tools/ai/_shared/heap_code_execution_tool_core.py`
- `Tools/ai/heap_runtime/code_execution_tool/cli.py`
- `Tools/validation/run_heap_code_execution_tool_smoke.py`

Updated:

- `Tools/ai/agent_runtime_tool_broker.py`
- `Tools/ai/heap_runtime/completeness_gate/cli.py`

## Runtime Capability

New broker tool:

- `run_heap_code_execution_matrix`

What it does:

- accepts verified repo-relative target files;
- accepts allowlisted `Tools/validation/*.py` validation scripts;
- generates an `agent_runtime_debug_lab_request`;
- runs compile/test/status/diff through the existing report-only debug lab;
- emits a JSON/Markdown report with `concrete_code_proposals`;
- captures worktree diff excerpts;
- marks untracked new files as `developed_change_present` and includes a
  source excerpt as the patch sketch;
- keeps provider execution, patch application, source writes and git writes
  false.

## Heap Integration

The completeness gate now adds a dynamic requirement when the request asks for
code, tests, validation, patches or concrete proposals:

- requirement: `code_execution_matrix`;
- tool: `run_heap_code_execution_matrix`;
- lane: `code_execution_matrix`;
- role: `allowlisted_compile_test_diff_evidence_lane`.

The final heap product now reports:

- `code_execution_matrix_required`;
- `code_execution_matrix_passed`;
- `code_execution_matrix_reports`.

For coding requests, a `ready` product is blocked unless the code execution
matrix passed.

## Concrete Proposal Surface

Each target file in the tool report becomes a proposal item with:

- `target_file`;
- `implementation_status`;
- `git_status`;
- `code_or_patch_sketch`;
- `diff_hunk_count`;
- `validation_commands`;
- `acceptance_criteria`.

This makes the final purpose richer than a provider answer: reviewers can see
which file changed, what code was produced, and which commands validated it.

## Validation

Validated locally:

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

Observed:

- direct tool return code: `0`;
- broker return code: `0`;
- provider execution: `false`;
- patch application: `false`;
- source writes by provider lanes: `false`;
- git writes: `false`.

## Line Counts

- `Tools/ai/heap_runtime/code_execution_tool/cli.py`: 208 lines.
- `Tools/ai/_shared/heap_code_execution_tool_core.py`: 317 lines.
- `Tools/validation/run_heap_code_execution_tool_smoke.py`: 224 lines.

All new files are under the 400-line maintained script target.

## Full Heap Verification

Complete run:

- `output/validation/heap_context_closure_final_purpose_apply_code_matrix_20260514_1323`

Documents package:

- `C:/Users/carmi/Documents/aicarmine_heap_final_proposals_20260514-132354`

Observed in `heap_runtime_completeness_gate_report.json`:

- `code_execution_matrix_required=true`;
- `code_execution_matrix_passed=true`;
- completed requirements include `code_execution_matrix`;
- missing requirements: none;
- provider execution performed: `true`;
- patch application performed: `false`;
- source writes performed: `false`.

Observed in the matrix report:

- passed: `true`;
- target count: `8`;
- concrete code proposal count: `8`;
- all target files were marked `developed_change_present`;
- brokered debug-lab evidence passed.
