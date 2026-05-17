"""Decision, product, bundle and telemetry phases for the Python workflow."""

from __future__ import annotations

from pathlib import Path

from py_mesh import existing, live_signal
from py_patch_notes import run_patch_notes_quality_product
from py_support import WorkflowContext, add_existing, now_iso, read_json, write_json, write_text

TOOL_REPORT_KEYS = [
    "repo_consistency_json",
    "repo_consistency_smoke_json",
    "code_interpreter_json",
    "line_count_json",
    "python_syntax_json",
    "gpu_contract_smoke_json",
    "deterministic_smoke_json",
    "decision_loop_smoke_json",
    "npu_env_json",
    "openvino_governance_json",
    "megalithic_review_json",
    "megalithic_proposals_json",
    "refined_review",
    "refined_proposals",
    "gpu_replay_json",
    "gpu_npu_sync_json",
    "provider_contract_json",
    "gpu0_companion_json",
    "gpu0_companion_contract_json",
    "gpu0_support_bootstrap",
    "npu_support_bootstrap",
    "gpu1_primary_json",
    "gpu0_task_json",
    "gpu0_response_json",
    "gpu0_tools_json",
    "gpu0_broker_json",
    "npu_micro_json",
    "npu_broker_json",
    "peer_json",
    "peer_contract_json",
    "heap_init_json",
    "heap_gpu1_request_json",
    "heap_broker_json",
    "heap_npu_json",
    "heap_catalog_json",
    "heap_snapshot_json",
    "heap_telemetry_json",
    "memory_workflow",
]
