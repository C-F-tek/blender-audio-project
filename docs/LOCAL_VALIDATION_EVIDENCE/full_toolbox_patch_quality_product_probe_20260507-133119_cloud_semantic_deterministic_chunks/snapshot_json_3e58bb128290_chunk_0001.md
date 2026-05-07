# Evidence Chunk 0001/0001

- source: `output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/snapshot.json`
- source_sha256: `3e58bb12829011d743a91981c1a900e41d456a4a684177155eb5e787d142888a`
- line_start: `2`
- line_end: `203`
- section_kinds: `['json_key_section']`
- previous_chunk_file: ``
- next_chunk_file: ``
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: schema_version; generated_at; stamp; event_log; event_count. Preview: "schema_version": 1, "kind": "provider_runtime_heap_snapshot", "generated_at": "2026-05-07T13:33:30", "stamp": "patch_quality_product_probe_20260507-133119", "event_log": "output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/events.jsonl", "event...

## Context before

{

## Chunk content

```json
  "schema_version": 1,
  "kind": "provider_runtime_heap_snapshot",
  "generated_at": "2026-05-07T13:33:30",
  "stamp": "patch_quality_product_probe_20260507-133119",
  "event_log": "output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/events.jsonl",
  "event_count": 32,
  "parse_error_count": 0,
  "by_lane": {
    "orchestrator": {
      "event_count": 8,
      "latest_event_at": "2026-05-07T13:33:30",
      "event_types": {
        "provider_state": 3,
        "evidence_request": 5
      }
    },
    "gpu0": {
      "event_count": 13,
      "latest_event_at": "2026-05-07T13:33:30",
      "event_types": {
        "evidence_response": 7,
        "broker_request": 6
      }
    },
    "gpu1": {
      "event_count": 2,
      "latest_event_at": "2026-05-07T13:33:30",
      "event_types": {
        "evidence_request": 2
      }
    },
    "broker": {
      "event_count": 6,
      "latest_event_at": "2026-05-07T13:33:30",
      "event_types": {
        "broker_result": 6
      }
    },
    "npu": {
      "event_count": 2,
      "latest_event_at": "2026-05-07T13:33:30",
      "event_types": {
        "evidence_response": 2
      }
    },
    "deterministic": {
      "event_count": 1,
      "latest_event_at": "2026-05-07T13:33:30",
      "event_types": {
        "validation_signal": 1
      }
    }
  },
  "by_event_type": {
    "provider_state": 3,
    "evidence_request": 7,
    "evidence_response": 9,
    "broker_request": 6,
    "broker_result": 6,
    "validation_signal": 1
  },
  "pending_broker_request_count": 0,
  "pending_broker_requests": [],
  "tool_catalog": {
    "schema_version": 1,
    "kind": "semantic_tool_catalog_snapshot",
    "generated_at": "2026-05-07T13:33:30",
    "tool_count": 10,
    "tools": [
      {
        "tool": "build_agent_agnostic_tool_inventory",
        "description": "Inventory existing reusable IA-Carmine tools and guardrails.",
        "allowed_args": [
          "root"
        ],
        "broker_builder": "build_agent_agnostic_tool_inventory",
        "execution_rule": "request_only; execution must be mediated by agent_runtime_tool_broker"
      },
      {
        "tool": "build_agent_memory_inventory",
        "description": "Read-only SQLite/JSONL agent memory inventory.",
        "allowed_args": [
          "objective",
          "memory_db"
        ],
        "broker_builder": "build_agent_memory_inventory",
        "execution_rule": "request_only; execution must be mediated by agent_runtime_tool_broker"
      },
      {
        "tool": "build_agent_transient_request_context",
        "description": "Build request-scoped context from memory notes, raw files and reports.",
        "allowed_args": [
          "objective",
          "memory_note",
          "raw_file",
          "report_file"
        ],
        "broker_builder": "build_agent_transient_request_context",
        "execution_rule": "request_only; execution must be mediated by agent_runtime_tool_broker"
      },
      {
        "tool": "build_code_interpreter_report",
        "description": "Build static code-interpreter style report over selected roots.",
        "allowed_args": [
          "input"
        ],
        "broker_builder": "build_code_interpreter_report",
        "execution_rule": "request_only; execution must be mediated by agent_runtime_tool_broker"
      },
      {
        "tool": "build_python_line_count_csv",
        "description": "Build full Python line-count CSV/JSON/MD evidence.",
        "allowed_args": [
          "exclude_dir"
        ],
        "broker_builder": "build_python_line_count_csv",
        "execution_rule": "request_only; execution must be mediated by agent_runtime_tool_broker"
      },
      {
        "tool": "build_refactor_duplication_audit",
        "description": "Build a report-only duplicated-helper/refactor audit over selected code roots and existing evidence reports.",
        "allowed_args": [
          "root",
          "report",
          "input_audit_report",
          "line_count_report",
          "code_interpreter_report",
          "python_syntax_report",
          "bundle_smoke_report",
          "memory_routing_report"
        ],
        "broker_builder": "build_refactor_duplication_audit",
        "execution_rule": "request_only; execution must be mediated by agent_runtime_tool_broker"
      },
      {
        "tool": "check_python_syntax",
        "description": "Validate Python syntax across repository.",
        "allowed_args": [],
        "broker_builder": "check_python_syntax",
        "execution_rule": "request_only; execution must be mediated by agent_runtime_tool_broker"
      },
      {
        "tool": "check_validation_report_contract",
        "description": "Validate validation report contract for a scoped report-dir or explicit report files.",
        "allowed_args": [
          "report_file"
        ],
        "broker_builder": "check_validation_report_contract",
        "execution_rule": "request_only; execution must be mediated by agent_runtime_tool_broker"
      },
      {
        "tool": "run_gpu_planner_json_contract_smoke",
        "description": "Run GPU planner JSON contract smoke tests without provider.",
        "allowed_args": [],
        "broker_builder": "run_gpu_planner_json_contract_smoke",
        "execution_rule": "request_only; execution must be mediated by agent_runtime_tool_broker"
      },
      {
        "tool": "runtime_sqlite_memory",
        "description": "Use protected persistent SQLite read-only or operational scratch SQLite memory under output/**.",
        "allowed_args": [
          "action",
          "scope",
          "database",
          "persistent_database",
          "summary",
          "content",
          "role",
          "tag",
          "query",
          "limit",
          "confirm",
          "allow_persistent_write"
        ],
        "broker_builder": "runtime_sqlite_memory",
        "execution_rule": "request_only; execution must be mediated by agent_runtime_tool_broker"
      }
    ],
    "guardrails": {
      "free_shell_exposed": false,
      "broker_allowlist_required": true,
      "provider_direct_tool_execution_allowed": false
    }
  },
  "architecture": {
    "gpu1": "primary_advisory_planner",
    "gpu0": "coworker_helper_openvino",
    "npu": "microtask_responder",
    "broker": "single_controlled_executor",
    "semantic_tools_registry": "agent_runtime_tool_broker.TOOL_SPECS",
    "deterministic_validators": "cpu_authority_validation_lane",
    "telemetry": "append_only_event_stream"
  },
  "guardrails": {
    "report_only": true,
    "provider_execution_performed": false,
    "direct_tool_execution_allowed": false,
    "broker_required_for_tool_execution": true,
    "patch_application_performed": false,
    "source_writes_performed": false
  }
}
```
