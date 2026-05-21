# Tools/ai/contractor_universe context

## Role

`Tools/ai/contractor_universe` is the internal runtime package behind the
canonical run command. It compacts the existing Universo IA provider-lane model
into a small explicit scheduler.

It is reachable only through the canonical run command:

```text
python -m Tools.ai run ...
```

## Boundaries

- It is the only runtime route behind `python -m Tools.ai run`.
- It is not registered as a second public dispatcher command.
- It does not import `Tools.validation` from the runtime core.
- It does not perform telemetry, source writes, patch application or provider
  execution in the initial deterministic backend.
- It produces local compact evidence only: `run.json`, `run.md`,
  `pointer_graph.json`, blackboard snapshot and event log.

## Current status

Initial diagnostic/runtime scaffold. It is not a public entry command,
full-smoke evidence or proof of provider execution. Provider execution remains
unproven until a real provider adapter leaves observable evidence.
