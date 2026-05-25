#!/usr/bin/env python3
"""Smoke test the heap final readable product assembler."""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")
def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)
from Tools.validation.heap_runtime.run_heap_final_readable_product_fixture import (
    TRUNCATED_DIFF_MARKER,
    build_fixture,
)
from ia_carmine._shared.heap_final_readable_synthesis import render_markdown
from ia_carmine.runtime.heap_context_closure.product_state import build_product_state

def run_smoke(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    work_dir = Path(args.work_dir).resolve() if args.work_dir else repo_root / "output" / "validation" / f"heap_final_readable_product_smoke_{now_stamp()}"
    run_dir, documents_dir = build_fixture(repo_root, work_dir)
    output = run_dir / "heap_final_readable_product.json"
    markdown = run_dir / "heap_final_readable_product.md"
    text = run_dir / "heap_final_readable_product.txt"
    command = [
        sys.executable,
        "ia_carmine/product/code_product/final_readable_product/cli.py",
        "--repo-root",
        ".",
        "--run-dir",
        str(run_dir),
        "--output",
        str(output),
        "--markdown-output",
        str(markdown),
        "--text-output",
        str(text),
        "--documents-dir",
        str(documents_dir),
        "--zip-documents",
    ]
    completed = subprocess.run(
        command,
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
        timeout=max(30, int(args.timeout_seconds)),
    )
    product = json.loads(output.read_text(encoding="utf-8-sig")) if output.exists() else {}
    final_md = documents_dir / "FINAL_READABLE_PRODUCT.md"
    full_code_product = documents_dir / "CODE_PRODUCT_FULL_PATCH.md"
    plan_product_full_patch = documents_dir / "PLAN_PRODUCT_FULL_PATCH.md"
    zip_path = Path(str(documents_dir) + ".zip")
    body = final_md.read_text(encoding="utf-8-sig") if final_md.exists() else ""
    code_product_body = full_code_product.read_text(encoding="utf-8-sig") if full_code_product.exists() else ""
    plan_product_body = (
        plan_product_full_patch.read_text(encoding="utf-8-sig")
        if plan_product_full_patch.exists()
        else ""
    )
    operator_decision_path = documents_dir / "OPERATOR_DECISION.txt"
    operator_decision_body = (
        operator_decision_path.read_text(encoding="utf-8-sig")
        if operator_decision_path.exists()
        else ""
    )
    no_product_body = render_markdown(
        run_dir=run_dir,
        composer={
            "operator_decision": {
                "decision": "BLOCKED_NO_VERIFIED_TARGET",
                "accepted_count": 0,
                "rejected_count": 1,
            }
        },
        gate={
            "metrics": {
                "product_status": "blocked_with_reason",
                "provider_revision_budget_exhausted": False,
            },
            "provider_execution_performed": False,
        },
        postrun={},
        revision={
            "resume_from_block_id": "smoke:proposal:001",
            "gpu1_block_count": 2,
            "proposal_block_count": 2,
        },
        pointer={"blocks": []},
        matrix={"target_count": 0, "verified_target_count": 0, "concrete_code_proposals": []},
        matrix_path="",
    )
    required_phrases = ["Decisione finale", "Final document status", "Piano applicabile", "Sequenza di applicazione", "Laboratorio operativo", "Sa usarlo", "Code product", "Universo pointer e memoria", "Perche il provider non si applica", "Decisione operatore", "Peer follow-up pending", "Capture failed", "Gerarchia GPU1/GPU0/NPU", "GPU1 primary workload", "GPU1 primary evidence", "Generic write", "GPU1/NVIDIA", "GPU0/Vulkan", "coworker_medium", "NPU/OpenVINO", "micro_fast", "context_budget", "Parallel provider overlap", "Device identity map", "GPU1 one-turn runtime gate", "one-turn gate passed", "Broker result consumed", "role=tool reinjected"]
    missing = [phrase for phrase in required_phrases if phrase not in body]
    pointer_reconstruction = (
        product.get("pointer_reconstruction")
        if isinstance(product.get("pointer_reconstruction"), dict)
        else {}
    )
    pointer_contract = (
        pointer_reconstruction.get("contract")
        if isinstance(pointer_reconstruction.get("contract"), dict)
        else {}
    )
    launcher_product_state = build_product_state(
        code_product_contract={"path": str(full_code_product), "real_code_product_ready": False},
        external_contract={
            "provider_execution_performed": True,
            "resume_from_block_id": "smoke:proposal:000",
            "latest_block_id": "smoke:gpu0_peer:000",
            "provider_rejection_reasons": [],
            "missing_roles": [],
            "pointer_block_count": 3,
        },
        final_result={"passed": False},
        final_payload={
            "product_kind": "blocked_continuation_product",
            "product_blocked_reason": "gpu0_peer_followup_pending",
            "soft_close_reason": "gpu0_peer_followup_pending",
        },
        launcher_contract_errors=["final readable product did not pass"],
    )
    launcher_reason_preserved = (
        launcher_product_state.get("product_blocked_reason") == "gpu0_peer_followup_pending"
        and launcher_product_state.get("soft_close_reason") == "gpu0_peer_followup_pending"
    )
    passed = (
        completed.returncode == 0
        and product.get("passed") is True
        and product.get("pointer_reconstruction_passed") is True
        and pointer_contract.get("final_code_product_composed_from_pointer_graph") is True
        and pointer_contract.get("single_run_not_single_direction") is True
        and final_md.exists()
        and full_code_product.exists()
        and plan_product_full_patch.exists()
        and "CODE_PRODUCT_FULL_PATCH" in code_product_body
        and "PLAN_PRODUCT_FULL_PATCH" in plan_product_body
        and "final_product_text_surface" in product.get("plan_product_kind", "")
        and "## FINAL_PRODUCT Text Surface" in plan_product_body
        and "FINAL_PRODUCT_DELTA" in plan_product_body
        and "Refined smoke final-product delta" in plan_product_body
        and "Initial smoke final-product delta" in plan_product_body
        and "Text surface status: `FINAL_PRODUCT_TEXT_SURFACE_AVAILABLE`" in plan_product_body
        and "packaging/evidence surfaces, not competing products" in plan_product_body
        and "ia_carmine/product/code_product/final_readable_product/cli.py" in code_product_body
        and "FULL_DIFF_SENTINEL" in code_product_body
        and "FULL_DIFF_SENTINEL" in plan_product_body
        and TRUNCATED_DIFF_MARKER not in code_product_body
        and "[code product excerpt truncated" not in body
        and "ia_carmine/runtime/heap_context_closure/cli.py" not in code_product_body
        and "ia_carmine/_shared/heap_final_code_product.py" not in code_product_body
        and "ia_carmine/worktree_extra.py" not in code_product_body
        and "Final assembler worktree fallback: `disabled`" in code_product_body
        and "Code product status: `BLOCKED_WITH_CODE_PRODUCT_REVIEW`" in code_product_body
        and "## Prodotto finale di evidenza" in no_product_body
        and "NO_APPLICABLE_CODE_PRODUCT" in no_product_body
        and "PLAN_PRODUCT_FULL_PATCH.md" in no_product_body
        and "Pointer graph, prompt/raw GPU1" in no_product_body
        and "## Piano applicabile" not in no_product_body
        and "## Sequenza di applicazione" not in no_product_body
        and "- Sa usarlo: `False`" in no_product_body
        and "e' stato chiamato via broker" not in no_product_body
        and product.get("soft_lock_closure_owner_decision") == "finalize_product"
        and product.get("gpu0_closure_agreement") == "agree_close"
        and product.get("closure_quorum_status") == "ready_to_close"
        and product.get("gpu1_one_turn_runtime_gate_passed") is True
        and product.get("gpu1_one_turn_tool_result_consumed") is True
        and "gpu1_one_turn_runtime_gate=passed" in operator_decision_body
        and "gpu1_one_turn_tool_result_consumed=true" in operator_decision_body
        and "gpu1_decision_missing" not in body
        and "not_evaluated_waiting_for_gpu1_decision" not in body
        and "GPU1 block/revision: `smoke:proposal:002` / `2`" in body
        and "GPU0 current review: `True`" in body
        and "[no worktree diff captured]" not in code_product_body
        and zip_path.exists()
        and not missing
        and launcher_reason_preserved
    )
    report = {
        "schema_version": 1,
        "kind": "heap_final_readable_product_smoke",
        "repo_root": repo_root.as_posix(),
        "passed": passed,
        "errors": [] if passed else ["heap final readable product smoke failed"],
        "warnings": [],
        "work_dir": str(work_dir),
        "run_dir": str(run_dir),
        "documents_dir": str(documents_dir),
        "product_json": str(output),
        "documents_markdown": str(final_md),
        "full_code_product": str(full_code_product),
        "plan_product_full_patch": str(plan_product_full_patch),
        "documents_zip": str(zip_path),
        "missing_required_phrases": missing,
        "no_product_markdown_preview": no_product_body[:4000],
        "pointer_reconstruction_passed": product.get("pointer_reconstruction_passed"),
        "pointer_reconstruction": pointer_reconstruction,
        "launcher_reason_preserved": launcher_reason_preserved,
        "launcher_product_state": launcher_product_state,
        "returncode": completed.returncode,
        "stdout_tail": (completed.stdout or "")[-4000:],
        "stderr_tail": (completed.stderr or "")[-4000:],
        "command": command,
    }
    report_output = Path(args.output).resolve() if args.output else work_dir / "smoke.json"
    write_json(report_output, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return report
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--work-dir", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--timeout-seconds", type=int, default=90)
    return parser.parse_args()
def main() -> int:
    report = run_smoke(parse_args())
    return 0 if report.get("passed") else 2
if __name__ == "__main__":
    raise SystemExit(main())
