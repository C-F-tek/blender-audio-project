# JSON Parser Utility Review

## Status

completed

## Goal

Review and implement the reusable JSON parser boundary for AI/model outputs without importing the superseded PR #19 wholesale.

## Result

implemented, locally validated and completed.

Implemented helper:

```text
ia_carmine/_shared/model_json.py
```

Implemented validator:

```text
Tools/validation/check_ai_model_json.py
```

Runtime migration completed:

```text
Tools/npu/provider_mesh/_shared/ollama_runtime.py::parse_json_response()
```

The runtime wrapper delegates to `ia_carmine._shared.model_json.parse_model_json_object()` while preserving legacy `json.JSONDecodeError` behavior for existing callers.

## Scope kept separate

```text
clean project JSON file IO
raw model-output JSON-like parsing
```

`Scripting/shared/json_io.py` remains the helper for trusted project files and generated artifacts. `ia_carmine/_shared/model_json.py` handles model-output parsing.

## Validation summary

Reported local result:

```text
check_ai_model_json.py: PASS
errors: []
case_count: 12
```

Validated behavior includes plain JSON objects, fenced JSON, surrounding text extraction, trailing comma repair, comment stripping, array/object separation and invalid-text failures.

## Follow-up

Further caller migration is deferred. Future migrations should inspect one model-output caller at a time, add one deterministic validator case, and run syntax/model JSON/pipeline validators.

## Progress log

- 2026-04-29: Reviewed current JSON helpers and confirmed the gap is model-output parsing, not normal JSON file IO.
- 2026-04-29: Implemented additive parser and validator.
- 2026-04-29: Delegated `Tools/npu/provider_mesh/_shared/ollama_runtime.py::parse_json_response()` to the reusable parser while preserving legacy failure type.
- 2026-04-30: Moved from `active/` to `completed/` during execution-plan status cleanup.
