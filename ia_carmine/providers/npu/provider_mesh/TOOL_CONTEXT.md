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

## Representative access

```powershell
python -m ia_carmine.cli run [explicit NPU/provider flags...]
python -m ia_carmine.cli runtime_tool_broker [explicit tool args...]
```

Direct NPU dispatcher commands are retired. These packages are implementation
modules used by the run and broker surfaces.

## Output role

Outputs from this area are context or evidence artifacts. They help later runtime and review stages understand the project without reading every file again.

## Notes

- Keep generated chunks and caches out of Git by default.
- Keep package outputs compact and structured.
- Add validation coverage when a packet format becomes important for a workflow.
