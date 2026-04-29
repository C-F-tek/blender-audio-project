# JSON Parser Utility Review

## Status

active

## Goal

Review whether the project needs a reusable JSON parser utility for AI/model outputs, using the superseded PR #19 idea as historical input without importing the old branch wholesale.

## Current finding

The repository already has two different JSON use cases:

```text
clean JSON files
model/LLM JSON-like responses
```

These should remain separate because they have different failure modes.

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
should not be made tolerant of malformed LLM output because file JSON should fail loudly
```

## Existing model-response parser

Current helper:

```text
Tools/npu/ollama_runtime.py
```

Current relevant functions:

```text
strip_json_fence(text)
parse_json_response(text)
```

Assessment:

```text
useful behavior already exists
scope is currently tied to Ollama runtime
only handles fenced JSON and object extraction
should not become the only parser for all model providers
```

## Gap

A reusable AI/model-output parser is still useful, but it should not live in `Scripting/shared/` and should not require introducing the full old `Tools/ai_core/` package yet.

Candidate target:

```text
Tools/ai/model_json.py
```

Reason:

```text
belongs to AI tooling, not Blender scripting
avoids premature Tools/ai_core architecture
can be reused by Ollama/NPU/pipeline validators later
small and independently testable
```

## Proposed utility contract

Initial module should be minimal:

```text
strip_markdown_json_fence(text: str) -> str
extract_json_candidate(text: str) -> str
repair_common_model_json(text: str) -> str
parse_model_json(text: str, allow_repair: bool = True) -> Any
parse_model_json_object(text: str, allow_repair: bool = True) -> dict[str, Any]
```

Allowed repair behavior:

```text
remove UTF-8 BOM
strip markdown fences
extract largest likely JSON object/array
remove trailing commas before } or ]
remove line-only // comments
```

Explicitly not allowed initially:

```text
semantic repair of missing fields
inventing missing braces too aggressively
converting Python dict syntax to JSON
fixing arbitrary unquoted keys
silently returning empty dict on failure
```

Failure should raise a dedicated exception:

```text
ModelJsonParseError
```

## Validation target

Add a small validator or extend an existing validator with deterministic samples:

```text
plain object: PASS
markdown fenced object: PASS
text before/after object: PASS
trailing comma: PASS when allow_repair=true
JSON array: PASS for parse_model_json
array rejected by parse_model_json_object: PASS
invalid text: FAIL with ModelJsonParseError
```

Preferred validator:

```text
Tools/validation/check_ai_model_json.py
```

Alternative:

```text
extend Tools/validation/check_ai_pipeline_modules.py only if keeping the surface tiny
```

## Migration policy

Do not immediately refactor all callers.

Recommended sequence:

```text
1. add Tools/ai/model_json.py
2. add check_ai_model_json.py
3. validate locally
4. optionally update Tools/npu/ollama_runtime.py parse_json_response to delegate to the new utility
5. only then inspect other JSON model-output consumers
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

low if introduced as additive utility and validator only.

medium if existing runtime callers are migrated immediately.

## Decision

Proceed with an additive utility PR after the current `agent_state_packet` contract PR is merged.

Do not import old PR #19 wholesale. Reuse only the minimal concept of robust model-output JSON parsing.

## Progress log

- 2026-04-29: Reviewed current JSON helpers and confirmed the gap is model-output parsing, not normal JSON file IO.
