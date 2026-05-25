# Tools/workflow Context

`Tools/workflow` is retired as an operator command surface.

The canonical runtime entrypoint is:

```powershell
python -m ia_carmine.cli run [explicit flags...]
```

Workflow packages may remain as importable implementation modules while they are
being migrated, but they must not expose standalone wrapper commands, PowerShell
launchers, hidden profiles, implicit task files or model/device defaults.

Validation, smoke and test execution must go through the public validation
commands with explicit `--mode` / `--section` arguments. Helper execution must go
through the broker/helper command surface, not workflow wrappers.
