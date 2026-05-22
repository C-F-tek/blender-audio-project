"""Surface contract for contractor-universe semantics inside the main run."""

from __future__ import annotations

from typing import Any

from ia_carmine.runtime.heap_gate.provider_time import build_provider_time_counter_contract

from .models import ContractorRole


def build_contractor_universe_surface_contract(args: Any) -> dict[str, Any]:
    """Return the scheduler/role model as reusable main-flow evidence.

    This is intentionally not a second runtime launcher. It exposes the useful
    contractor-universe semantics so heap_gate/provider packets can consume them
    inside the single canonical run.
    """
    return {
        "kind": "contractor_universe_surface_contract",
        "runtime_scope": "single_canonical_universe_component",
        "not_a_public_entrypoint": True,
        "not_product_evidence_by_itself": True,
        "scheduler_model": {
            "heap": "UniverseHeap priority queue backed by ProviderRuntimeHeap events",
            "clock": "LogicalClock using heap_gate provider time counter contract",
            "soft_time_source": "ia_carmine.runtime.heap_gate.provider_time.build_provider_time_counter_contract",
            "soft_close_semantics": "coordinated_finalization_signal_not_pointer_truncation",
        },
        "time_counter_contract": build_provider_time_counter_contract(args),
        "roles": {
            "gpu1_primary": ContractorRole.STRATEGIST.value,
            "gpu0_coworker": ContractorRole.REVIEWER.value,
            "npu_microtask": ContractorRole.AUDITOR.value,
        },
        "pointer_fields": [
            "previous_block_id",
            "refines_block_id",
            "resume_from_block_id",
        ],
        "integration_boundary": [
            "operator input remains single ingress",
            "startup memory/chunks/tool catalog remain heap inputs",
            "GPU1/GPU0/NPU remain same-heap lanes",
            "matrix/lab and patch synthesis remain product boundary",
            "final product is reconstructed from pointer graph and evidence blocks",
        ],
    }
