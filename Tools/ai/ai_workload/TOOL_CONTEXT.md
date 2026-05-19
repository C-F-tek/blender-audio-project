# Tools/ai/ai_workload context

## Role

`Tools/ai/ai_workload` contains workload-quality and lane-routing helpers for AI execution planning.

## Responsibilities

- Build workload quality lane routing reports.
- Help decide which runtime/provider lane is suitable for a workload.
- Keep routing evidence separate from provider execution reports.

## Representative commands

Use through the AI dispatcher:

```powershell
python -m Tools.ai build_workload_quality_lane_routing ...
```

## Output role

Outputs are workload/routing reports. They are planning evidence and not final product artifacts.

## Notes

- Routing does not execute the provider by itself.
- Inspect `Tools/ai/dispatch.py` before assuming public command names.
- Add validation when routing schema or lane policy changes.
