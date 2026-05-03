# Runtime Tool Capability Manifest

- Passed: `True`
- Tool count: `10`
- Provider execution performed: `False`
- Patch application performed: `False`

## Cloud handoff policy

- `include_with_evidence_chunks`: `True`
- `include_runtime_usage_telemetry`: `True`
- `include_patch_plan_and_recommendations`: `True`
- `no_free_shell`: `True`
- `tool_execution_requires_local_broker`: `True`
- `cloud_model_may_reason_about_tools_but_must_not_execute_them`: `True`

## Caller modes

- Supported callers: `['gpu', 'npu', 'orchestrator', 'ollama-local', 'deterministic']`
- Rule: cloud receives capability manifest plus runtime usage telemetry; local execution remains broker-controlled

## Tools

### `build_agent_agnostic_tool_inventory`

- Category: `inventory`
- Safe mode: `report-only`
- Description: Inventory existing reusable IA-Carmine tools and guardrails.
- Allowed args: `['root']`
- Usage observed: `{'count': 0, 'executed': 0, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
- Guardrails:
  - no free shell exposure
  - broker allowlist required
  - no provider execution
  - no patch application
  - no Blender runtime execution
  - no Git writes
  - no SQLite or persistent memory write

### `build_agent_memory_inventory`

- Category: `inventory`
- Safe mode: `report-only`
- Description: Read-only SQLite/JSONL agent memory inventory.
- Allowed args: `['objective', 'memory_db']`
- Usage observed: `{'count': 0, 'executed': 0, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
- Guardrails:
  - no free shell exposure
  - broker allowlist required
  - no provider execution
  - no patch application
  - no Blender runtime execution
  - no Git writes
  - no SQLite or persistent memory write

### `build_agent_transient_request_context`

- Category: `context`
- Safe mode: `report-only`
- Description: Build request-scoped context from memory notes, raw files and reports.
- Allowed args: `['objective', 'memory_note', 'raw_file', 'report_file']`
- Usage observed: `{'count': 0, 'executed': 0, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
- Guardrails:
  - no free shell exposure
  - broker allowlist required
  - no provider execution
  - no patch application
  - no Blender runtime execution
  - no Git writes
  - no SQLite or persistent memory write

### `build_code_interpreter_report`

- Category: `static_analysis`
- Safe mode: `report-only`
- Description: Build static code-interpreter style report over selected roots.
- Allowed args: `['input']`
- Usage observed: `{'count': 0, 'executed': 0, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
- Guardrails:
  - no free shell exposure
  - broker allowlist required
  - no provider execution
  - no patch application
  - no Blender runtime execution
  - no Git writes
  - no SQLite or persistent memory write

### `build_python_line_count_csv`

- Category: `inventory`
- Safe mode: `report-only`
- Description: Build full Python line-count CSV/JSON/MD evidence.
- Allowed args: `['exclude_dir']`
- Usage observed: `{'count': 0, 'executed': 0, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
- Guardrails:
  - no free shell exposure
  - broker allowlist required
  - no provider execution
  - no patch application
  - no Blender runtime execution
  - no Git writes
  - no SQLite or persistent memory write

### `build_refactor_duplication_audit`

- Category: `refactor_analysis`
- Safe mode: `report-only`
- Description: Build a report-only duplicated-helper/refactor audit over selected code roots and existing evidence reports.
- Allowed args: `['root', 'report', 'input_audit_report', 'line_count_report', 'code_interpreter_report', 'python_syntax_report', 'bundle_smoke_report', 'memory_routing_report']`
- Usage observed: `{'count': 0, 'executed': 0, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
- Guardrails:
  - no free shell exposure
  - broker allowlist required
  - no provider execution
  - no patch application
  - no Blender runtime execution
  - no Git writes
  - no SQLite or persistent memory write

### `check_python_syntax`

- Category: `validation`
- Safe mode: `report-only`
- Description: Validate Python syntax across repository.
- Allowed args: `[]`
- Usage observed: `{'count': 0, 'executed': 0, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
- Guardrails:
  - no free shell exposure
  - broker allowlist required
  - no provider execution
  - no patch application
  - no Blender runtime execution
  - no Git writes
  - no SQLite or persistent memory write

### `check_validation_report_contract`

- Category: `validation`
- Safe mode: `report-only`
- Description: Validate validation report contract for a scoped report-dir or explicit report files.
- Allowed args: `['report_file']`
- Usage observed: `{'count': 0, 'executed': 0, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
- Guardrails:
  - no free shell exposure
  - broker allowlist required
  - no provider execution
  - no patch application
  - no Blender runtime execution
  - no Git writes
  - no SQLite or persistent memory write

### `run_gpu_planner_json_contract_smoke`

- Category: `validation`
- Safe mode: `report-only`
- Description: Run GPU planner JSON contract smoke tests without provider.
- Allowed args: `[]`
- Usage observed: `{'count': 0, 'executed': 0, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
- Guardrails:
  - no free shell exposure
  - broker allowlist required
  - no provider execution
  - no patch application
  - no Blender runtime execution
  - no Git writes
  - no SQLite or persistent memory write

### `runtime_sqlite_memory`

- Category: `memory_status`
- Safe mode: `controlled read-only/status by default; persistent write requires explicit confirm`
- Description: Use protected persistent SQLite read-only or operational scratch SQLite memory under output/**.
- Allowed args: `['action', 'scope', 'database', 'persistent_database', 'summary', 'content', 'role', 'tag', 'query', 'limit', 'confirm', 'allow_persistent_write']`
- Usage observed: `{'count': 0, 'executed': 0, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
- Guardrails:
  - no free shell exposure
  - broker allowlist required
  - no provider execution
  - no patch application
  - no Blender runtime execution
  - no Git writes
  - persistent memory write requires allow_persistent_write=true and confirm=persistent_write
  - operational scratch writes allowed only under output/** when broker-controlled

## Source files

- `Tools/ai/agent_runtime_tool_broker.py` role=`runtime_tool_broker_allowlist_source` exists=`True` sha256=`f948a459a39709877fac86cf098601b01f9560628644ec87d080c11f6fe3f449`
- `Tools/ai/build_runtime_tool_usage_telemetry.py` role=`runtime_tool_usage_telemetry_builder` exists=`True` sha256=`6199fb9f331ce3d36089756e2fd8e18b486a60be86fd82944cfb1df735884ccd`
- `Tools/ai/build_semantic_evidence_chunks.py` role=`semantic_cloud_handoff_chunker` exists=`True` sha256=`5fdcbc74f6eb931f3b95c6b54b1eb1071e57f8f41a34c694864b3ac8cdab80f7`
- `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` role=`shared_toolbox_bundle_builder` exists=`True` sha256=`0e20f26f7f15f8994bfc4b22ee420d068b6ce9c6aa8b2c5236b5f6f6c3eab812`
- `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260503-223900.json` role=`observed_runtime_tool_usage_report` exists=`True` sha256=`4fca7f9bc6eb11f72c45b00d149677b00372ef44287dc14967c9628b12cfc1b8`
