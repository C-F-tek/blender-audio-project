# Evidence Chunk 0001/0002

- source: `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_20260503-231855.json`
- source_sha256: `a545ff4a9bb4e2b0f6ff96ea64034f639739a6fd7d06dbe5bf81b4337ecb0341`
- line_start: `2`
- line_end: `378`
- section_kinds: `['json_key_section']`
- previous_chunk_file: ``
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/runtime_tool_capability_manifest_20260503-231855_json_a545ff4a9bb4_chunk_0002.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: schema_version; generated_at; repo_root; provider_execution_performed; patch_application_performed. Preview: "schema_version": 1, "kind": "runtime_tool_capability_manifest", "generated_at": "2026-05-03T23:22:59", "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project", "passed": true, "errors": [], "warnings": [], "provider_execution_performed": false, "patch...

## Context before

{

## Chunk content

```json
  "schema_version": 1,
  "kind": "runtime_tool_capability_manifest",
  "generated_at": "2026-05-03T23:22:59",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "sqlite_write_performed": false,
  "persistent_memory_write_performed": false,
  "blender_runtime_execution_performed": false,
  "tool_count": 10,
  "tool_usage_summary": {
    "tool_call_entry_count": 1,
    "executed_count": 0,
    "failed_count": 0,
    "blocked_count": 0,
    "total_reported_tool_elapsed_seconds": 0.0,
    "by_caller_ai": {
      "gpu": {
        "count": 1,
        "executed": 0,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      }
    },
    "by_tool": {
      "declared_runtime_tool_request_summary": {
        "count": 2,
        "executed": 0,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      }
    },
    "by_phase": {
      "gpu_planner_declared_tool_request_counters": {
        "count": 1,
        "executed": 0,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      }
    },
    "runtime_tool_request_count": 16,
    "runtime_tool_execution_count": 0,
    "runtime_tool_failed_count": 0,
    "runtime_tool_blocked_count": 0,
    "runtime_tool_provider_request_count": 16,
    "runtime_tool_provider_request_execution_count": 0,
    "deterministic_runtime_tool_fallback_request_count": 0,
    "deterministic_runtime_tool_fallback_execution_count": 0,
    "declared_not_executed_count": 16
  },
  "declared_runtime_tool_counters": {
    "runtime_tool_request_count": 16,
    "runtime_tool_execution_count": 0,
    "runtime_tool_failed_count": 0,
    "runtime_tool_blocked_count": 0,
    "runtime_tool_provider_request_count": 16,
    "runtime_tool_provider_request_execution_count": 0,
    "deterministic_runtime_tool_fallback_request_count": 0,
    "deterministic_runtime_tool_fallback_execution_count": 0,
    "declared_not_executed_count": 16
  },
  "tools": [
    {
      "tool_name": "build_agent_agnostic_tool_inventory",
      "category": "inventory",
      "description": "Inventory existing reusable IA-Carmine tools and guardrails.",
      "allowed_args": [
        "root"
      ],
      "safe_default_mode": "report-only",
      "guardrails": [
        "no free shell exposure",
        "broker allowlist required",
        "no provider execution",
        "no patch application",
        "no Blender runtime execution",
        "no Git writes",
        "no SQLite or persistent memory write"
      ],
      "usage_observed": {
        "count": 0,
        "executed": 0,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      },
      "broker_builder": "build_agent_agnostic_tool_inventory"
    },
    {
      "tool_name": "build_agent_memory_inventory",
      "category": "inventory",
      "description": "Read-only SQLite/JSONL agent memory inventory.",
      "allowed_args": [
        "objective",
        "memory_db"
      ],
      "safe_default_mode": "report-only",
      "guardrails": [
        "no free shell exposure",
        "broker allowlist required",
        "no provider execution",
        "no patch application",
        "no Blender runtime execution",
        "no Git writes",
        "no SQLite or persistent memory write"
      ],
      "usage_observed": {
        "count": 0,
        "executed": 0,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      },
      "broker_builder": "build_agent_memory_inventory"
    },
    {
      "tool_name": "build_agent_transient_request_context",
      "category": "context",
      "description": "Build request-scoped context from memory notes, raw files and reports.",
      "allowed_args": [
        "objective",
        "memory_note",
        "raw_file",
        "report_file"
      ],
      "safe_default_mode": "report-only",
      "guardrails": [
        "no free shell exposure",
        "broker allowlist required",
        "no provider execution",
        "no patch application",
        "no Blender runtime execution",
        "no Git writes",
        "no SQLite or persistent memory write"
      ],
      "usage_observed": {
        "count": 0,
        "executed": 0,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      },
      "broker_builder": "build_agent_transient_request_context"
    },
    {
      "tool_name": "build_code_interpreter_report",
      "category": "static_analysis",
      "description": "Build static code-interpreter style report over selected roots.",
      "allowed_args": [
        "input"
      ],
      "safe_default_mode": "report-only",
      "guardrails": [
        "no free shell exposure",
        "broker allowlist required",
        "no provider execution",
        "no patch application",
        "no Blender runtime execution",
        "no Git writes",
        "no SQLite or persistent memory write"
      ],
      "usage_observed": {
        "count": 0,
        "executed": 0,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      },
      "broker_builder": "build_code_interpreter_report"
    },
    {
      "tool_name": "build_python_line_count_csv",
      "category": "inventory",
      "description": "Build full Python line-count CSV/JSON/MD evidence.",
      "allowed_args": [
        "exclude_dir"
      ],
      "safe_default_mode": "report-only",
      "guardrails": [
        "no free shell exposure",
        "broker allowlist required",
        "no provider execution",
        "no patch application",
        "no Blender runtime execution",
        "no Git writes",
        "no SQLite or persistent memory write"
      ],
      "usage_observed": {
        "count": 0,
        "executed": 0,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      },
      "broker_builder": "build_python_line_count_csv"
    },
    {
      "tool_name": "build_refactor_duplication_audit",
      "category": "refactor_analysis",
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
      "safe_default_mode": "report-only",
      "guardrails": [
        "no free shell exposure",
        "broker allowlist required",
        "no provider execution",
        "no patch application",
        "no Blender runtime execution",
        "no Git writes",
        "no SQLite or persistent memory write"
      ],
      "usage_observed": {
        "count": 0,
        "executed": 0,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      },
      "broker_builder": "build_refactor_duplication_audit"
    },
    {
      "tool_name": "check_python_syntax",
      "category": "validation",
      "description": "Validate Python syntax across repository.",
      "allowed_args": [],
      "safe_default_mode": "report-only",
      "guardrails": [
        "no free shell exposure",
        "broker allowlist required",
        "no provider execution",
        "no patch application",
        "no Blender runtime execution",
        "no Git writes",
        "no SQLite or persistent memory write"
      ],
      "usage_observed": {
        "count": 0,
        "executed": 0,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      },
      "broker_builder": "check_python_syntax"
    },
    {
      "tool_name": "check_validation_report_contract",
      "category": "validation",
      "description": "Validate validation report contract for a scoped report-dir or explicit report files.",
      "allowed_args": [
        "report_file"
      ],
      "safe_default_mode": "report-only",
      "guardrails": [
        "no free shell exposure",
        "broker allowlist required",
        "no provider execution",
        "no patch application",
        "no Blender runtime execution",
        "no Git writes",
        "no SQLite or persistent memory write"
      ],
      "usage_observed": {
        "count": 0,
        "executed": 0,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      },
      "broker_builder": "check_validation_report_contract"
    },
    {
      "tool_name": "run_gpu_planner_json_contract_smoke",
      "category": "validation",
      "description": "Run GPU planner JSON contract smoke tests without provider.",
      "allowed_args": [],
      "safe_default_mode": "report-only",
      "guardrails": [
        "no free shell exposure",
        "broker allowlist required",
        "no provider execution",
        "no patch application",
        "no Blender runtime execution",
        "no Git writes",
        "no SQLite or persistent memory write"
      ],
      "usage_observed": {
        "count": 0,
        "executed": 0,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      },
      "broker_builder": "run_gpu_planner_json_contract_smoke"
    },
    {
      "tool_name": "runtime_sqlite_memory",
      "category": "memory_status",
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
      "safe_default_mode": "controlled read-only/status by default; persistent write requires explicit confirm",
      "guardrails": [
        "no free shell exposure",
        "broker allowlist required",
        "no provider execution",
        "no patch application",
        "no Blender runtime execution",
        "no Git writes",
        "persistent memory write requires allow_persistent_write=true and confirm=persistent_write",
        "operational scratch writes allowed only under output/** when broker-controlled"
      ],
      "usage_observed": {
        "count": 0,
        "executed": 0,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      },
      "broker_builder": "runtime_sqlite_memory"
    }
  ],
  "caller_modes": {
    "observed_by_caller_ai": {
      "gpu": {
        "count": 1,
        "executed": 0,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      }
    },
    "observed_by_phase": {
      "gpu_planner_declared_tool_request_counters": {
        "count": 1,
        "executed": 0,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      }
    },
    "supported_callers": [
      "gpu",
      "npu",
      "orchestrator",
      "ollama-local",
      "deterministic"
    ],
    "cloud_handoff_rule": "cloud receives capability manifest plus runtime usage telemetry; local execution remains broker-controlled"
  },
```

## Context after

  "source_files": [
    {
      "path": "Tools/ai/agent_runtime_tool_broker.py",
      "role": "runtime_tool_broker_allowlist_source",
      "exists": true,
      "size_bytes": 29351,
      "sha256": "f948a459a39709877fac86cf098601b01f9560628644ec87d080c11f6fe3f449"
    },
    {
      "path": "Tools/ai/build_runtime_tool_usage_telemetry.py",
      "role": "runtime_tool_usage_telemetry_builder",
      "exists": true,
