# Tools/npu Context

`Tools/npu` is retired as a public command surface.

NPU/provider behavior is selected by explicit run parameters or broker/helper
tool parameters. NPU packages may remain as importable implementation modules,
but they must not expose direct wrapper commands, hidden default models, hidden
device choices or standalone profile-driven launch paths.

Use:

```powershell
python -m ia_carmine.cli run [explicit provider/lane flags...]
python -m ia_carmine.cli runtime_tool_broker [explicit tool args...]
```

The NPU lane remains evidence/context until a later GPU1 turn consumes it through
the heap pointer/evidence protocol.
