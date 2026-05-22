# Tools Core Refactor Map

Discovery date: 2026-05-22. Repository branch observed locally: `master`.

This map records the code-driven split between IA-Carmine Core Runtime and
operator tooling. `Tools` remains a command/validation/workflow surface;
runtime ownership is `ia_carmine.*`.

| Path before | Module/function | Real role | Core runtime | CLI wrapper | Validation/smoke | Workflow/launcher | Side effects | Imports provider | Writes source | Writes output | SQLite/memory | Chunks/pointers | GPU/NPU/Ollama | Candidate target package | Migration risk | Minimum targeted test | Provider check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Tools/ai/run` | `cli.main` | product entry and launcher args | yes | yes | no | yes | launches subprocesses | yes | no | yes | indirect | yes | yes | `ia_carmine.runtime.run` | high | `python -m ia_carmine.cli run --help` | resource lanes |
| `Tools/ai/heap_runtime` | completeness gate, event pointers | heap gate execution | yes | no | no | no | reports/output | yes | no | yes | yes | yes | yes | `ia_carmine.runtime.heap_runtime` | high | import + py_compile | resource lanes |
| `Tools/ai/heap_gate` | provider loop mixins | runtime provider loop | yes | no | no | no | provider subprocesses | yes | no | yes | yes | yes | yes | `ia_carmine.runtime.heap_gate` | high | import provider loop modules | Ollama/OpenVINO checks |
| `Tools/ai/heap_context_closure` | closure launcher | heap closure orchestration | yes | yes | no | yes | subprocesses/output | yes | no | yes | yes | yes | yes | `ia_carmine.runtime.heap_context_closure` | high | help/import smoke | resource lanes |
| `Tools/ai/external_heap` | pointer/revision reports | external heap graph | yes | yes | no | no | output docs | no | no | yes | no | yes | no | `ia_carmine.runtime.external_heap` | medium | import revision context | none |
| `Tools/ai/heap_exchange` | exchange lifecycle | runtime exchange events | yes | yes | no | no | jsonl writes | no | no | yes | yes | yes | no | `ia_carmine.runtime.heap_exchange` | medium | import lifecycle CLIs | none |
| `Tools/ai/runtime_tool` | broker/file refs/debug lab | broker and tool registry | yes | yes | no | no | tool execution/output | no | possible via tools | yes | yes | yes | no | `ia_carmine.runtime.runtime_tool` | high | broker import smoke | none |
| `Tools/ai/provider_runtime_blackboard` | heap/blackboard bridge | provider runtime memory | yes | yes | no | no | sqlite/output | yes | no | yes | yes | yes | yes | `ia_carmine.runtime.provider_runtime_blackboard` | high | import blackboard | resource lanes |
| `Tools/ai/agent_memory` | sqlite memory CLI | persistent memory | yes | yes | no | no | sqlite writes | no | no | yes | yes | no | no | `ia_carmine.memory.agent_memory` | medium | import sqlite CLI | none |
| `Tools/ai/agent_context` | context packs/chunks | startup context, packs, chunks | yes | yes | no | no | output artifacts | no | no | yes | yes | yes | no | `ia_carmine.context.agent_context` | medium | import pack/chunk CLIs | none |
| `Tools/ai/heap_context_memory_reload` | startup reload | context/memory reload | yes | yes | no | no | output and memory writes | no | no | yes | yes | yes | no | `ia_carmine.context.heap_context_memory_reload` | high | import reload CLI | none |
| `Tools/ai/provider_mesh` | Ollama/GPU/OpenVINO probes | provider lane coordination | yes | yes | no | no | provider subprocesses/output | yes | no | yes | no | no | yes | `ia_carmine.providers.provider_mesh` | high | resource lane check | Ollama/GPU/NPU |
| `Tools/npu/provider_mesh` | NPU provider modules | OpenVINO NPU provider core | yes | via `Tools.npu` | no | no | provider subprocesses/output | yes | no | yes | no | yes | yes | `ia_carmine.providers.npu.provider_mesh` | high | NPU import/help | NPU env |
| `Tools/npu/pipeline` | NPU artifact pipeline | provider pipeline core | yes | via `Tools.npu` | no | no | output artifacts | yes | no | yes | no | yes | yes | `ia_carmine.providers.npu.pipeline` | medium | import pipeline | NPU env |
| `Tools/npu/dual_ai_pipeline` | dual provider pipeline | provider pipeline core | yes | via `Tools.npu` | no | no | output artifacts | yes | no | yes | no | yes | yes | `ia_carmine.providers.npu.dual_ai_pipeline` | medium | import dual CLI | NPU env |
| `Tools/ai/code_product` | code product/final readable | product assembly | yes | yes | no | no | product docs | no | possible when intake applies | yes | no | yes | no | `ia_carmine.product.code_product` | high | help/import smoke | none |
| `Tools/ai/patch_product` | patch plans/suggestions | patch product | yes | yes | no | no | patch docs | no | no by default | yes | no | yes | no | `ia_carmine.product.patch_product` | high | import patch CLIs | none |
| `Tools/ai/heap_final_proposals` | product composer | final product composer | yes | yes | no | no | product docs | yes | no | yes | no | yes | yes | `ia_carmine.product.heap_final_proposals` | high | import composer CLI | none |
| `Tools/ai/operator_product_core` | controller/runner | operator product core | yes | yes | no | yes | subprocesses/output | yes | no | yes | yes | yes | yes | `ia_carmine.product.operator_product_core` | high | run help/import | resource lanes |
| `Tools/ai/repository_product` | evidence/review products | repository product tooling | yes | yes | no | no | docs/output | optional | possible only explicit | yes | no | no | optional | `ia_carmine.product.repository_product` | medium | import evidence CLI | none |
| `Tools/ai/schema_repair` | schema repair contracts | validation contract helper | yes | yes | no | no | reports | no | no | yes | no | no | no | `ia_carmine.validation_contracts.schema_repair` | low | import schema repair | none |
| `Tools/validation` | validators/smokes | deterministic validation surface | no | no | yes | no | reports/output | may import core | no | yes | no | no | optional | stays `Tools.validation` | low | targeted validator run | none |
| `Tools/workflow` | PowerShell/local launchers | workflow surface | no | no | no | yes | subprocesses/output | may call providers | no | yes | no | no | optional | stays `Tools.workflow` | medium | dispatcher/help smoke | resource lanes if touched |
| `Tools/docs`, `Tools/git`, `Tools/repo_patch_runner` | utilities | repo utilities and controlled apply | no | no | no | no | docs/git/patch outputs | no | possible by design | yes | no | no | no | stay under `Tools` | medium | import/help smoke | none |

No core domain was intentionally left inside `Tools/ai`; that directory now
contains only compatibility package files and context text.
