# Tools/validation/agent_memory context

## Role

`Tools/validation/agent_memory` contains checks for runtime and persistent memory policy.

## Responsibilities

- Validate agent memory policy reports.
- Validate routing policy smoke behavior.
- Validate runtime SQLite write behavior.
- Keep persistent-memory assumptions explicit.

## Representative commands

Use through the validation dispatcher:

```powershell
python -m Tools.validation check_agent_memory_policy ...
python -m Tools.validation run_agent_memory_routing_policy_smoke ...
python -m Tools.validation run_runtime_sqlite_persistent_write_smoke ...
```

## Output role

Outputs are validation reports for memory behavior and policy checks.

## Notes

- Runtime memory and persistent memory are different concerns.
- SQLite files are not committed as source artifacts.
- Add checks here when memory routing or persistence policy changes.
