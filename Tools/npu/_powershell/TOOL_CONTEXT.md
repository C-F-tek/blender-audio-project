# Tools/npu/_powershell context

## Role

`Tools/npu/_powershell` contains maintained Windows/PowerShell wrapper entrypoints registered by `Tools/npu/dispatch.py`.

## Responsibilities

- Provide operator-friendly NPU context launch wrappers.
- Keep wrapper access discoverable through the NPU dispatcher.
- Bridge local Windows shell usage to packaged NPU tools where needed.

## Representative commands

Prefer the dispatcher form:

```powershell
python -m Tools.npu run_npu_context ...
```

Known wrapper:

```text
Tools/npu/_powershell/run_npu_context.ps1
```

## Boundaries

- Wrapper scripts should stay thin.
- Core NPU/provider behavior should live in packaged Python modules.
- Do not commit generated runtime output from wrapper runs by default.
