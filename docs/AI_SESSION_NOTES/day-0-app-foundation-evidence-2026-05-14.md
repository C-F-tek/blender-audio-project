# Day 0 app foundation evidence - 2026-05-14

## Decision

This is the private Day 0 baseline for the IA-Carmine app/runtime direction.

The accepted source change is not provider-generated source code. The provider lane remains diagnostic-only when it invents paths or emits non-applicable candidates. The accepted product is the deterministic run-owned orchestration, lab evidence, code matrix, final readable decision package and full code product artifact.

## Final run

```text
stamp: final_purpose_lab_full_code_product_20260514_1953
run_dir: output/validation/heap_context_closure_final_purpose_lab_full_code_product_20260514_1953
documents_dir: C:\Users\carmi\Documents\aicarmine_heap_final_proposals_20260514-195340
zip: C:\Users\carmi\Documents\aicarmine_heap_final_proposals_20260514-195340.zip
```

Run result:

```text
final_document_status: APPLY_REVIEW_READY
decision: DIAGNOSTIC_ONLY
product_status: blocked_with_reason
provider_execution_performed: true
patch_application_performed: false
source_writes_performed: false
code_execution_matrix_passed: true
concrete_code_proposal_count: 15
zip_member_count: 19
```

## Run-owned product

The run writes these final operator artifacts:

```text
FINAL_READABLE_PRODUCT.md
FINAL_READABLE_PRODUCT.txt
FINAL_READABLE_PRODUCT.json
CODE_PRODUCT_FULL_PATCH.md
```

`FINAL_READABLE_PRODUCT.md` is the readable operator decision. It includes:

- final document status;
- provider diagnostic reason;
- concrete code targets;
- sequence of application;
- lab evidence;
- code product pointer;
- validation commands;
- operator decision.

`CODE_PRODUCT_FULL_PATCH.md` is the full available deterministic code/diff product from the code execution matrix. In the final run it contained 15 target sections and about 172k characters of code/diff evidence.

## Lab evidence

The lab is brokered, not only narrated.

Evidence from the final run:

```text
virtual dev environment: passed
code execution matrix: passed
debug lab: passed
target count: 15
validation scripts in virtual dev: 2
guardrails free_shell/source_writes/patch_apply/git_write: false
```

The final document explicitly answers:

```text
Dov'e' il lab?
Sa usarlo?
```

with the brokered virtual dev and code matrix reports.

## Validation

Executed before GitHub publication:

```text
python -m py_compile selected Day 0 Python files
python -m Tools.validation test_proposal_gate
python -m Tools.validation test_composer_decision
python -m Tools.validation run_heap_code_execution_tool_smoke --repo-root . --timeout-seconds 180
python -m Tools.validation run_heap_virtual_dev_environment_smoke --repo-root . --timeout-seconds 180
python -m Tools.validation run_heap_final_readable_product_smoke --repo-root . --timeout-seconds 180
git diff --check
```

Provider-capable environment check:

```text
python: .venv\Scripts\python.exe
OpenVINO devices: ['CPU', 'GPU.0', 'GPU.1', 'NPU']
```

`git diff --check` passed with CRLF warnings only on pre-existing split Markdown files under `docs/LOCAL_AI_RUN_BOOTSTRAP.md/`.

## GitHub rule

This milestone and PR are private-only. Repository visibility was verified as:

```text
repository: C-F-tek/blender-audio-project
visibility: PRIVATE
```
