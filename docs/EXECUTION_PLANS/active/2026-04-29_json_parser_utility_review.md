# JSON Parser Utility Review

## Status

completed

## Goal

Review whether the project needs a reusable JSON parser utility for AI/model outputs, using the superseded PR #19 idea as historical input without importing the old branch wholesale.

## Current finding

The repository has two different JSON use cases:

```text
clean JSON files
model/LLM JSON-like responses
```

These remain separate because they have different failure modes.

## Existing clean JSON file helper

Current helper:

```text
Scripting/shared/json_io.py
```

Current role:

```text
read_json(path)
read_json_if_exists(path, default)
write_json(path, data)
require_mapping(data)
require_keys(data, keys)
summarize_json_file(path)
```

Assessment:

```text
keep as-is for trusted project files and generated artifacts
not suitable as-is for raw model output
must continue to fail loudly when project artifact JSON is invalid
```

## Implemented model-response parser

Implemented helper:

```text
Tools/ai/model_json.py
```

Implemented contract:

```text
strip_markdown_json_fence(text: str) -> str
extract_json_candidate(text: str) -> str
repair_common_model_json(text: str) -> str
parse_model_json(text: str, allow_repair: bool = True) -> Any
parse_model_json_object(text: str, allow_repair: bool = True) -> dict[str, Any]
ModelJsonParseError
```

Allowed repair behavior:

```text
remove UTF-8 BOM
strip markdown fences
extract largest likely JSON object/array
remove trailing commas before } or ]
remove line-only // comments
```

Explicitly not allowed:

```text
semantic repair of missing fields
inventing missing braces too aggressively
converting Python dict syntax to JSON
fixing arbitrary unquoted keys
silently returning empty dict on failure
```

## Ollama migration

Completed migration:

```text
Tools/npu/ollama_runtime.py::parse_json_response()
```

Current behavior:

```text
parse_json_response() delegates to Tools.ai.model_json.parse_model_json_object()
strip_json_fence() remains as a backward-compatible wrapper
ModelJsonParseError is converted back to json.JSONDecodeError for legacy callers
```

## Validation

Validator:

```text
Tools/validation/check_ai_model_json.py
```

Reported local result:

```text
check_ai_model_json.py: PASS
errors: []
case_count: 12
```

Validated cases:

```text
plain object: PASS
markdown fenced object: PASS
text before/after object: PASS
trailing comma: PASS
line-only // comment: PASS
JSON array: PASS for parse_model_json
array rejected by parse_model_json_object: PASS with ModelJsonParseError
invalid text: PASS with ModelJsonParseError
ollama parse_json_response plain: PASS
ollama parse_json_response fenced: PASS
ollama parse_json_response surrounding text: PASS
ollama parse_json_response invalid: PASS with JSONDecodeError
```

## Migration policy

Further caller migration is intentionally deferred.

Future migrations should happen only after reading the current caller and adding a focused validator case.

Recommended future sequence:

```text
1. inspect one model-output JSON caller
2. migrate only that caller to Tools.ai.model_json
3. add one deterministic validation case
4. run syntax, model JSON, pipeline module and JSON artifact validators
```

## Out of scope

```text
Scripting/shared/json_io.py behavior changes
full Tools/ai_core package import
large refactor of current AI pipeline
prompt injection changes
runtime Blender changes
FFmpeg changes
```

## Risk

low after validation.

## Decision

The project now has a reusable model-output JSON parser. The old PR #19 `Tools/ai_core/json_utils.py` idea is considered absorbed in a smaller, safer form.

Do not import old PR #19 wholesale. Continue recovering only focused concepts through small PRs.

## Progress log

- 2026-04-29: Reviewed current JSON helpers and confirmed the gap is model-output parsing, not normal JSON file IO.
- 2026-04-29: Implemented additive parser with `Tools/ai/model_json.py` and `Tools/validation/check_ai_model_json.py`.
- 2026-04-29: Delegated `Tools/npu/ollama_runtime.py::parse_json_response()` to the reusable parser while preserving the legacy `json.JSONDecodeError` failure type.
