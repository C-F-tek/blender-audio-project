#!/usr/bin/env python3
"""Tests for runtime heap state, diagnostics and deterministic pipeline."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from Tools.ai.evidence_to_recommendation import write_recommendation_event
from Tools.ai.heap_event_pointers import source_pointer_bundle
from Tools.ai._shared.heap_source_anchors import (
    real_source_file_candidates,
    response_file_reference_quality,
)
from Tools.ai.patch_product.patch_plan_generator import write_patch_plan_event
from Tools.ai.provider_runtime_blackboard import ProviderRuntimeHeap, record_lane_diagnostic
from Tools.ai.provider_mesh.gpu_npu_parallel_orchestrator import runtime_state_gate
from Tools.ai.heap_runtime.completeness_gate import runtime_state_lane_gate
from Tools.ai.validation_step import write_validation_event


class RuntimeStateTests(unittest.TestCase):
    def make_heap(self, root: Path) -> ProviderRuntimeHeap:
        return ProviderRuntimeHeap.from_args(
            root,
            "unit",
            "heap/events.jsonl",
            "heap/snapshot.json",
            "heap/snapshot.md",
        )

    def test_add_event_updates_lane_status(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            heap = self.make_heap(Path(temp))
            heap.add_event(
                "provider_state",
                {"lane": "gpu0", "status": "degraded", "message": "probe failed"},
                lane="gpu0",
            )
            snapshot = heap.write_snapshot()
            state = snapshot["runtime_state"]
            self.assertEqual(state["lane_status"]["gpu0"], "degraded")
            self.assertEqual(state["degraded_lanes"], ["gpu0"])

    def test_record_lane_diagnostic_standard_payload(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            heap = self.make_heap(Path(temp))
            event = record_lane_diagnostic(
                heap,
                "npu",
                "ready",
                "micro lane ready",
                {"provider_execution_performed": True},
            )
            payload = event["payload"]
            self.assertEqual(payload["lane"], "npu")
            self.assertEqual(payload["status"], "ready")
            self.assertEqual(heap.runtime_state.lane_status["npu"], "ready")


class RuntimeGateTests(unittest.TestCase):
    def test_gate_respects_zero_tolerance(self) -> None:
        status = {"gpu1": "ready", "gpu0": "degraded", "npu": "ready"}
        gate = runtime_state_gate(status, 0)
        self.assertFalse(gate["passed"])
        self.assertEqual(gate["degraded_lanes"], ["gpu0"])

    def test_gate_allows_one_degraded_when_configured(self) -> None:
        status = {"gpu1": "ready", "gpu0": "degraded", "npu": "ready"}
        gate = runtime_state_lane_gate(status, 1)
        self.assertTrue(gate["passed"])
        self.assertEqual(gate["degraded_lane_count"], 1)


class DeterministicPipelineTests(unittest.TestCase):
    def test_degraded_lane_recommendation_and_validation_chain(self) -> None:
        repo_root = Path(__file__).resolve().parents[3]
        heap = ProviderRuntimeHeap.from_args(
            repo_root,
            "unit_pipeline",
            "output/test_runtime_state_pipeline/events.jsonl",
            "output/test_runtime_state_pipeline/snapshot.json",
            "output/test_runtime_state_pipeline/snapshot.md",
        )
        record_lane_diagnostic(heap, "gpu1", "ready", "GPU1 ready")
        record_lane_diagnostic(heap, "gpu0", "degraded", "GPU0 forced failure")
        record_lane_diagnostic(heap, "npu", "ready", "NPU ready")
        heap.add_event(
            "lane_evidence",
            {
                "lane": "gpu1",
                "status": "ready",
                "output": "output/test_runtime_state_pipeline/gpu1_evidence.json",
                "raw_output": {"passed": True},
            },
            lane="gpu1",
        )
        gate = runtime_state_gate({"gpu1": "ready", "gpu0": "degraded", "npu": "ready"}, 1)
        self.assertTrue(gate["passed"])
        recommendation = write_recommendation_event(heap)["recommendation"]
        self.assertEqual(recommendation["action"], "repair_degraded_lane")
        self.assertEqual(recommendation["target_lane"], "gpu0")
        pointers = recommendation["source_pointers"]["evidence_pointers"]
        self.assertTrue(pointers)
        self.assertEqual(
            pointers[-1]["artifact_refs"],
            ["output/test_runtime_state_pipeline/gpu1_evidence.json"],
        )
        patch_plan = write_patch_plan_event(heap)["patch_plan"]
        self.assertEqual(patch_plan["target_lane"], "gpu0")
        self.assertTrue(patch_plan["tool_pointer_inputs"]["evidence_pointers"])
        validation = write_validation_event(heap)["validation"]
        self.assertTrue(validation["passed"], validation.get("errors"))
        self.assertTrue(validation["tool_pointer_inputs"]["evidence_pointers"])

    def test_failed_gate_blocks_recommendation_step(self) -> None:
        gate = runtime_state_gate({"gpu1": "ready", "gpu0": "degraded", "npu": "ready"}, 0)
        self.assertFalse(gate["passed"])


class HeapProductContractHelperTests(unittest.TestCase):
    def test_source_anchor_prefers_operator_existing_files(self) -> None:
        repo_root = Path(__file__).resolve().parents[3]
        request = (
            "Use Tools/ai/provider_runtime_blackboard/cli.py and "
            "Tools/ai/evidence_to_recommendation/cli.py. "
            "Do not use Tools/data_processor/real_existing_file.py."
        )
        candidates = real_source_file_candidates(
            repo_root=repo_root,
            request_texts=[request],
            broker_output_refs=[],
            limit=4,
        )
        self.assertEqual(candidates[0], "Tools/ai/provider_runtime_blackboard/cli.py")
        self.assertIn("Tools/ai/evidence_to_recommendation/cli.py", candidates)
        quality = response_file_reference_quality(
            repo_root=repo_root,
            text="TARGET_FILES:\n- Tools/data_processor/real_existing_file.py",
            requires_existing=True,
            implementation_required=True,
        )
        self.assertFalse(quality["passed"])
        self.assertIn(
            "Tools/data_processor/real_existing_file.py",
            quality["unverified_source_file_refs"],
        )

    def test_event_pointer_bundle_reads_heap_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            events = root / "events.jsonl"
            events.write_text(
                '{"kind":"provider_runtime_event","event_type":"evidence_response",'
                '"source":"gpu0","correlation_id":"c1",'
                '"payload":{"output":"output/evidence.json","status":"ready",'
                '"message":"ready"}}\n',
                encoding="utf-8",
            )
            bundle = source_pointer_bundle(
                root,
                {
                    "kind": "provider_runtime_heap_snapshot",
                    "event_log": "events.jsonl",
                },
            )
            self.assertEqual(bundle["tool_pointer_protocol"], "runtime_heap_event_log_v1")
            self.assertEqual(
                bundle["evidence_pointers"][0]["artifact_refs"],
                ["output/evidence.json"],
            )


if __name__ == "__main__":
    unittest.main()
