# Tools/npu/provider_mesh context

## Role

`Tools/npu/provider_mesh` contains NPU-side context builders and report helpers for local AI workflows.

## Main responsibilities

- Build music, code, manual and project context packets.
- Build compact provider input packets.
- Build semantic code chunk reports.
- Build provider result reports.
- Build runtime output manifests.
- Run NPU review helpers.

## Representative commands

Use through the NPU dispatcher:

```powershell
python -m Tools.npu build_music_context ...
python -m Tools.npu build_blender_manual_context ...
python -m Tools.npu build_npu_code_context ...
python -m Tools.npu build_project_ai_index ...
python -m Tools.npu build_semantic_code_chunks ...
python -m Tools.npu build_npu_knowledge_broker_packet ...
python -m Tools.npu build_ai_service_packet ...
python -m Tools.npu build_provider_result_report ...
python -m Tools.npu build_runtime_output_manifest ...
python -m Tools.npu run_npu_review ...
```

## Output role

Outputs from this area are context or evidence artifacts. They help later runtime and review stages understand the project without reading every file again.

## Notes

- Keep generated chunks and caches out of Git by default.
- Keep package outputs compact and structured.
- Add validation coverage when a packet format becomes important for a workflow.
