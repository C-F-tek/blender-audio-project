# Core Out Of Tools Refactor

## Scope

This refactor moves IA-Carmine Core Runtime ownership from `Tools` into the
root `ia_carmine` package. `Tools` remains the operator surface for validation,
workflow, NPU command dispatch, docs utilities, Git utilities and compatibility.

## Why

`Tools` mixed runtime, providers, memory, pointer graphs, product composition,
validators and workflow launchers. That made the architecture hard to read and
made command names look like runtime ownership. The canonical runtime name is
now `ia_carmine.*`.

## Before And After

Before:

```text
Tools/
  ai/          runtime + providers + memory + products + command dispatch
  npu/         NPU provider core + command dispatch
  validation/  validators and smokes
  workflow/    workflow launchers
```

After:

```text
ia_carmine/
  runtime/
  memory/
  context/
  chunks/
  pointers/
  providers/
  product/
  validation_contracts/

Tools/
  ai/          compatibility package only
  npu/         NPU command surface plus compatibility package roots
  validation/  validators and smokes
  workflow/    workflow launchers
```

## Old Path To New Package

| Old path | New package |
| --- | --- |
| `Tools/ai/run` | `ia_carmine.runtime.run` |
| `Tools/ai/heap_gate` | `ia_carmine.runtime.heap_gate` |
| `Tools/ai/heap_runtime` | `ia_carmine.runtime.heap_runtime` |
| `Tools/ai/heap_context_closure` | `ia_carmine.runtime.heap_context_closure` |
| `Tools/ai/heap_exchange` | `ia_carmine.runtime.heap_exchange` |
| `Tools/ai/external_heap` | `ia_carmine.runtime.external_heap` |
| `Tools/ai/heap_provider` | `ia_carmine.runtime.heap_provider` |
| `Tools/ai/runtime_tool` | `ia_carmine.runtime.runtime_tool` |
| `Tools/ai/runtime_universe` | `ia_carmine.runtime.runtime_universe` |
| `Tools/ai/provider_runtime_blackboard` | `ia_carmine.runtime.provider_runtime_blackboard` |
| `Tools/ai/contractor_universe` | `ia_carmine.runtime.contractor_universe` |
| `Tools/ai/agent_memory` | `ia_carmine.memory.agent_memory` |
| `Tools/ai/agent_context` | `ia_carmine.context.agent_context` |
| `Tools/ai/heap_context_memory_reload` | `ia_carmine.context.heap_context_memory_reload` |
| `Tools/ai/provider_mesh` | `ia_carmine.providers.provider_mesh` |
| `Tools/npu/provider_mesh` | `ia_carmine.providers.npu.provider_mesh` |
| `Tools/npu/pipeline` | `ia_carmine.providers.npu.pipeline` |
| `Tools/npu/dual_ai_pipeline` | `ia_carmine.providers.npu.dual_ai_pipeline` |
| `Tools/ai/code_product` | `ia_carmine.product.code_product` |
| `Tools/ai/patch_product` | `ia_carmine.product.patch_product` |
| `Tools/ai/heap_final_proposals` | `ia_carmine.product.heap_final_proposals` |
| `Tools/ai/operator_product_core` | `ia_carmine.product.operator_product_core` |
| `Tools/ai/agent_review` | `ia_carmine.product.agent_review` |
| `Tools/ai/ai_workload` | `ia_carmine.product.ai_workload` |
| `Tools/ai/deterministic_recommendations` | `ia_carmine.product.deterministic_recommendations` |
| `Tools/ai/generated_patch_specs` | `ia_carmine.product.generated_patch_specs` |
| `Tools/ai/patchkit` | `ia_carmine.product.patchkit` |
| `Tools/ai/pipeline` | `ia_carmine.product.pipeline` |
| `Tools/ai/repository_product` | `ia_carmine.product.repository_product` |
| `Tools/ai/schema_repair` | `ia_carmine.validation_contracts.schema_repair` |

## Compatibility Files

| Path | Purpose |
| --- | --- |
| `Tools/ai/__init__.py` | exposes the compatibility package path and delegates public helpers |
| `Tools/ai/__main__.py` | delegates command execution to `ia_carmine.cli` |
| `Tools/ai/dispatch.py` | delegates dispatch imports to `ia_carmine.cli` |
| `Tools/npu/provider_mesh/__init__.py` | maps old NPU provider imports to `ia_carmine.providers.npu.provider_mesh` |
| `Tools/npu/pipeline/__init__.py` | maps old NPU pipeline imports to `ia_carmine.providers.npu.pipeline` |
| `Tools/npu/dual_ai_pipeline/__init__.py` | maps old dual-pipeline imports to `ia_carmine.providers.npu.dual_ai_pipeline` |

## Domains Left In Tools

| Domain | Reason |
| --- | --- |
| `Tools/validation` | deterministic validators, smokes and report checks |
| `Tools/workflow` | PowerShell/local launchers and GUI workflow surfaces |
| `Tools/docs` | documentation utilities |
| `Tools/git` | controlled Git helper surface |
| `Tools/repo_patch_runner` | explicit patch runner utility boundary |
| `Tools/npu/dispatch.py` and PowerShell files | command surface and local workflow wrappers |

## Commands Preserved

Canonical runtime command:

```powershell
python -m ia_carmine.cli <tool> [args...]
```

The previous AI command surface is retained only for compatibility and delegates
to `ia_carmine.cli`; it is not the canonical runtime name.

Validation and workflow surfaces remain:

```powershell
python -m Tools.validation <tool> [args...]
python -m Tools.workflow <tool> [args...]
python -m Tools.npu <tool> [args...]
```

## Provider Checks

Provider checks for this refactor are targeted only:

| Provider area | Check |
| --- | --- |
| Ollama/GPU1 | `ollama list`, `ollama ps`, local resource lanes |
| OpenVINO GPU0 | local resource lanes |
| OpenVINO NPU | NPU provider environment, local resource lanes |
| Resource lanes | `check_local_resource_lanes` through `ia_carmine.cli` |

Full product runs, full smoke, full toolbox, full GPU/NPU orchestrator runs,
Blender and FFmpeg are excluded from this refactor acceptance path.

## Validations Executed

| Check | Result |
| --- | --- |
| `python -m compileall -q ia_carmine Tools` | passed |
| `python -m ia_carmine.cli --list` | passed |
| AI compatibility command list | passed |
| `python -m ia_carmine.cli run --help` | passed |
| AI compatibility run help | passed |
| `python -m Tools.npu run_npu_review --help` | passed |
| `python -m Tools.validation check_ia_carmine_core_refactor_imports` | passed |
| `python -m Tools.validation check_python_syntax` | passed, `checked_count=1500` |
| scoped `check_validation_report_contract` | passed, `report_count=4` |
| `git diff --check` | passed with line-ending warnings only |

## Provider Checks Executed

| Check | Result |
| --- | --- |
| `ollama list` | passed, 11 local models visible |
| `ollama ps` | passed, no resident model listed |
| resource lanes without provider Python override | degraded: repository `.venv` absent in this working copy |
| resource lanes with provider Python override | passed, ready lanes `gpu`, `npu`, `ollama` |
| NPU provider environment without provider Python override | degraded: repository `.venv` absent in this working copy |
| NPU provider environment with provider Python override | passed, `npu_ready_for_auditor=true` |

## Residual Risk

The refactor intentionally preserves behavior and command names. Remaining risk
is limited to call sites that imported private modules by filesystem path rather
than Python package name; package imports and dispatcher targets have been
rewired to the canonical `ia_carmine.*` modules.
