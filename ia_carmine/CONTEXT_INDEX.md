# ia_carmine Context Index

`ia_carmine` is the IA-Carmine Core Runtime package. Use this index to find
the nearest package family before editing runtime code.

| Family | Context file |
| --- | --- |
| Shared helpers | `ia_carmine/_shared/TOOL_CONTEXT.md` |
| Runtime run command | `ia_carmine/runtime/run/TOOL_CONTEXT.md` |
| Runtime heap gate | `ia_carmine/runtime/heap_gate/TOOL_CONTEXT.md` |
| Runtime heap closure | `ia_carmine/runtime/heap_context_closure/` |
| Runtime heap exchange | `ia_carmine/runtime/heap_exchange/TOOL_CONTEXT.md` |
| Runtime heap provider contracts | `ia_carmine/runtime/heap_provider/` |
| Runtime tool broker/registry | `ia_carmine/runtime/runtime_tool/` |
| Runtime universe | `ia_carmine/runtime/runtime_universe/` |
| Runtime provider blackboard | `ia_carmine/runtime/provider_runtime_blackboard/TOOL_CONTEXT.md` |
| Runtime contractor universe | `ia_carmine/runtime/contractor_universe/TOOL_CONTEXT.md` |
| Memory | `ia_carmine/memory/agent_memory/` |
| Context reload, packs and internal RAG | `ia_carmine/context/` |
| Provider mesh | `ia_carmine/providers/provider_mesh/TOOL_CONTEXT.md` |
| OpenVINO NPU provider core | `ia_carmine/providers/npu/` |
| Product code/final artifacts | `ia_carmine/product/code_product/TOOL_CONTEXT.md` |
| Product patch artifacts | `ia_carmine/product/patch_product/TOOL_CONTEXT.md` |
| Product composer | `ia_carmine/product/heap_final_proposals/TOOL_CONTEXT.md` |
| Product operator controller | `ia_carmine/product/operator_product_core/TOOL_CONTEXT.md` |
| Product review and repository products | `ia_carmine/product/` |
| Validation contracts | `ia_carmine/validation_contracts/` |

Canonical command surface:

```powershell
python -m ia_carmine.cli <tool> [args...]
```

Public tool names are registered in `ia_carmine/dispatch.py`.
