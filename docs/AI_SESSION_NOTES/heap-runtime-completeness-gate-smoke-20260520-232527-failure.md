# Heap Runtime Completeness Gate Smoke Failure - 2026-05-20 23:25:27

## Classification

This is published as Codex failure evidence, not as successful validation. The
duplicated prefixed errors are also recorded as misleading formatting because
they can make the same failure look like additional structured progress.

The failure increments the script-gaming regression counter by `124`, matching
the observed return code. The root README and chat failure ledger therefore move
from `151` to `275`.

This also increments the separate misleading/Codex lie evidence counter by `1`
because the same underlying errors were repeated with a `complete:` prefix.

## Runtime Evidence

```json
{
  "schema_version": 1,
  "kind": "heap_runtime_completeness_gate_smoke",
  "mode": "complete_only",
  "generated_at": "2026-05-20T23:25:27",
  "repo_root": "C:/Users/carmi/ProjectsDir/blender-audio-project",
  "passed": false,
  "runs": [
    {
      "label": "complete",
      "passed": false,
      "run_dir": "output/validation/heap_runtime_completeness_gate_complete_20260520-230527",
      "returncode": 124,
      "metrics": {},
      "errors": [
        "complete gate returned 124: heap runtime smoke outer watchdog expired",
        "complete heap runtime gate did not pass",
        "report kind must be heap_runtime_completeness_gate",
        "metric heap_read_count must be >0",
        "metric heap_write_count must be >0",
        "metric tool_request_count must be >0",
        "metric tool_execution_count must be >0",
        "metric decision_count must be >0",
        "metric candidate_operation_count must be >0",
        "metric shared_evidence_count must be >0",
        "metric shared_memory_evidence_count must be >0",
        "metric shared_context_chunk_evidence_count must be >0",
        "metric tool_catalog_evidence_count must be >0",
        "metric validation_evidence_count must be >0",
        "metric gpu1_provider_evidence_count must be >0",
        "metric gpu0_provider_evidence_count must be >0",
        "metric npu_micro_task_evidence_count must be >0",
        "metric provider_result_count must be >0",
        "metric provider_lane_count must be >0",
        "complete smoke must not pass a blocked/non-product runtime; product_status=None",
        "complete smoke must fail when GPU1/pointer product quality is false",
        "complete run must satisfy all required requirements",
        "complete run must use positive provider permit and operator intent",
        "state.facts must contain at least one item",
        "state.needs must contain at least one item",
        "state.tool_requests must contain at least one item",
        "state.shared_evidence must contain at least one item",
        "state.provider_results must contain at least one item",
        "state.claims must contain at least one item",
        "state.decisions must contain at least one item",
        "state.candidate_operations must contain at least one item",
        "complete run must perform observable provider execution",
        "complete run must include all three provider lanes",
        "complete run must expose real-run-compatible output contract",
        "guardrail patch_application_performed must be false",
        "guardrail source_writes_performed must be false"
      ]
    }
  ],
  "provider_execution_performed": false
}
```

## Prefix Failure

The report also repeated the same errors with a `complete:` prefix. That prefix
does not make the failure more specific and must not be treated as a separate
proof surface. It is evidence that formatting can obscure the real problem:
the complete run produced no valid heap/provider/product evidence before the
outer watchdog expired.
