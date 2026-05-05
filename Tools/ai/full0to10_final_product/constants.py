"""Constants for Full0To10 final tool product."""
from __future__ import annotations

PRODUCT_NAME = "full0to10_final_tool_product"
PRODUCT_MARKDOWN = "full0to10_final_tool_product.md"
PRODUCT_MANIFEST = "full0to10_final_tool_product_manifest.json"
EVIDENCE_INDEX = "full0to10_final_tool_product_evidence_index.json"
READINESS_JSON = "full0to10_final_tool_product_readiness.json"
README_NAME = "README.md"

DEFAULT_REQUEST = (
    "Costruisci il pacchetto prodotto finale Full0To10 orientato a SQLite FTS5, "
    "runtime tools, GPU/Ollama, NPU/OpenVINO e quality gate."
)

REQUIRED_PRODUCT_EVIDENCE = (
    "effective_use_summary",
    "quality_product",
    "provider_hardening",
    "tool_telemetry",
    "optimization",
    "quality_gate",
)

FINAL_PRODUCT_SECTIONS = (
    "request",
    "deliverable_scope",
    "evidence_index",
    "sqlite_memory",
    "runtime_tools",
    "gpu_ollama",
    "npu_openvino",
    "readiness",
    "next_run",
)

SAFETY_FLAGS = {
    "provider_execution_performed": False,
    "patch_application_performed": False,
    "source_writes_performed": False,
    "persistent_memory_write_performed": False,
}
