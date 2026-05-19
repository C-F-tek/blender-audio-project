# Tools/ai/_shared context

## Role

`Tools/ai/_shared` contains internal helper modules reused by multiple AI tool families.

This is not a public dispatcher surface. It supports packaged tools registered in `Tools/ai/dispatch.py`.

## Responsibilities

- Shared provider probing helpers.
- Shared provider tool-loop helpers.
- Shared path/import helpers.
- Shared runtime/report utilities.
- Shared live-flow/status helpers.
- Shared template/context helpers used by package CLIs.

## Example modules

```text
provider_ollama_probe.py
provider_tool_loop.py
provider_probe_paths.py
live_flow_status.py
ensure_ai_context_templates.py
```

## Boundaries

- Do not call `_shared` modules as operator entrypoints.
- Prefer public commands through `python -m Tools.ai <tool>`.
- Keep shared helpers small and reusable.
- If a helper becomes public workflow surface, register a CLI in `Tools/ai/dispatch.py` instead of exposing the helper directly.

## Validation

Shared helper changes should be validated by the public tools or smokes that consume them.
