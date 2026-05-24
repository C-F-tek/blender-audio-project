"""Checks for GPU1 code-delta file-read grounding."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def probe_code_delta_file_read_contract(repo_root: Path) -> list[str]:
    from ia_carmine.runtime.heap_gate.final_product_delta_protocol import (
        code_file_read_contract,
        final_product_protocol,
    )

    class Dummy:
        def __init__(self, payloads: list[dict[str, Any]]) -> None:
            self.repo_root = repo_root
            self._payloads = payloads

        def broker_results(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
            return self._payloads

    errors: list[str] = []
    report_path = repo_root / "output/validation/provider_loop_activation_smoke/runtime_file_window.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_rel = report_path.relative_to(repo_root).as_posix()
    report_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "kind": "runtime_file_window",
                "passed": True,
                "path": "ia_carmine/runtime/heap_gate/proposal_cycle_a.py",
                "source_ref": {"path": "ia_carmine/runtime/heap_gate/proposal_cycle_a.py"},
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    broker_payload = {
        "tool": "runtime_file_window",
        "request_id": "read:proposal_cycle_a",
        "normalized_request_id": "read:proposal_cycle_a",
        "provider_native_tool_call": True,
        "blocked": False,
        "returncode": 0,
        "errors": [],
        "outputs": {"json_report": report_rel},
        "summary": {"kind": "runtime_file_window", "passed": True},
    }
    response = (
        "FINAL_PRODUCT_KIND: text_and_code\n"
        "FINAL_PRODUCT_ACTION: append\n"
        "CURRENT_POINTER:\n"
        "- previous_block_id=\n"
        "- refines_block_id=\n"
        "- resume_from_block_id=smoke:proposal:000\n"
        "CONSUMED_EVIDENCE:\n"
        f"- tool_or_matrix_refs={report_rel}\n"
        "NEXT_RUNTIME_INTENT:\n"
        "- validate diff through matrix\n"
        "FINAL_PRODUCT_DELTA:\n"
        "# Problem\n"
        "Use the actual file contents already read by runtime_file_window.\n"
        "PATCH_SKETCH_UNIFIED_DIFF\n"
        "```diff\n"
        "diff --git a/ia_carmine/runtime/heap_gate/proposal_cycle_a.py b/ia_carmine/runtime/heap_gate/proposal_cycle_a.py\n"
        "--- a/ia_carmine/runtime/heap_gate/proposal_cycle_a.py\n"
        "+++ b/ia_carmine/runtime/heap_gate/proposal_cycle_a.py\n"
        "@@ -1 +1 @@\n"
        "-old\n"
        "+new\n"
        "```\n"
    )
    protocol = final_product_protocol(response)
    if protocol.get("delta_chars", 0) <= 30:
        errors.append("FINAL_PRODUCT_DELTA parser truncated markdown body before inner Problem/PATCH sections")
    positive = code_file_read_contract(
        Dummy([broker_payload]),
        response_text=response,
        protocol=protocol,
        target_files=["ia_carmine/runtime/heap_gate/proposal_cycle_a.py"],
        events=[],
    )
    if not positive.get("verified"):
        errors.append("code/text_and_code delta with consumed native runtime_file_window result was not verified")
    negative = code_file_read_contract(
        Dummy([]),
        response_text=response,
        protocol=protocol,
        target_files=["ia_carmine/runtime/heap_gate/proposal_cycle_a.py"],
        events=[],
    )
    if "gpu1_code_delta_without_file_read" not in negative.get("errors", []):
        errors.append("code/text_and_code delta without runtime_file_window result must fail")
    text_response = response.replace("FINAL_PRODUCT_KIND: text_and_code", "FINAL_PRODUCT_KIND: text").replace(
        "PATCH_SKETCH_UNIFIED_DIFF", "TEXT_ONLY_SECTION"
    ).replace("```diff", "```markdown").replace("diff --git a/", "not-a-diff ")
    text_protocol = final_product_protocol(text_response)
    text_contract = code_file_read_contract(
        Dummy([]),
        response_text=text_response,
        protocol=text_protocol,
        target_files=[],
        events=[],
    )
    if text_contract.get("required"):
        errors.append("text-only FINAL_PRODUCT_DELTA must not require runtime_file_window")
    return errors
