#!/usr/bin/env python3
"""Normalize final heap composer causality into separate chain/product statuses.

This adapter is external to the gate. It reads an existing composer JSON and
writes an enriched report that distinguishes:

- causal_chain: whether the heap universe produced traceable evidence/artifacts;
- product_acceptance: whether the produced proposal is acceptable/concrete.

A run can have causal_chain_passed=true and product_acceptance_passed=false. That
is expected when GPU1/GPU0/NPU exchanged evidence but all proposal chunks were
rejected for placeholders, stubs or repeated output.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def normalize_bool(value: Any) -> bool:
    return value is True or str(value).lower() == "true"


EXECUTION_TRUE_PATTERNS = (
    re.compile(
        r"\b(provider_execution_performed|gpu0_provider_execution_performed|gpu1_provider_execution_performed|npu_provider_execution_performed|workload_performed)\b\s*[:=]\s*true\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"[\"'](provider_execution_performed|gpu0_provider_execution_performed|gpu1_provider_execution_performed|npu_provider_execution_performed|workload_performed)[\"']\s*:\s*true\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(NPU|GPU|provider|workload)[^\n]{0,120}\bperformed\s*[:=]\s*true\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bperformed\s*=\s*true\b", re.IGNORECASE),
)
EXECUTION_BOOL_KEYS = {
    "provider_execution_performed",
    "gpu0_provider_execution_performed",
    "gpu1_provider_execution_performed",
    "npu_provider_execution_performed",
    "workload_performed",
}
WORKLOAD_CONTAINER_KEYS = {
    "npu_device_workload",
    "gpu_device_workload",
    "device_workload",
    "workload",
}


def mapping_has_execution_evidence(value: Any, parent_key: str = "") -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            key_lower = key_text.lower()
            if key_lower in EXECUTION_BOOL_KEYS and normalize_bool(item):
                return True
            if (
                key_lower == "performed"
                and parent_key.lower() in WORKLOAD_CONTAINER_KEYS
                and normalize_bool(item)
            ):
                return True
            if mapping_has_execution_evidence(item, key_text):
                return True
    elif isinstance(value, list):
        return any(mapping_has_execution_evidence(item, parent_key) for item in value)
    return False


def text_has_execution_evidence(text: str) -> bool:
    return any(pattern.search(text) for pattern in EXECUTION_TRUE_PATTERNS)


def list_len(value: Any) -> int:
    return len(value) if isinstance(value, list) else 0


def artifact_count(composer: dict[str, Any]) -> int:
    startup = (
        composer.get("startup_manifest")
        if isinstance(composer.get("startup_manifest"), dict)
        else {}
    )
    artifacts = startup.get("artifacts") if isinstance(startup.get("artifacts"), dict) else {}
    reconciliation = (
        composer.get("startup_reconciliation")
        if isinstance(composer.get("startup_reconciliation"), dict)
        else {}
    )
    refs = set()
    for value in artifacts.values():
        if isinstance(value, str) and value:
            refs.add(value.replace("\\", "/"))
    for value in reconciliation.get("artifact_refs") or []:
        if isinstance(value, str) and value:
            refs.add(value.replace("\\", "/"))
    return len(refs)


def provider_execution_performed(composer: dict[str, Any]) -> bool:
    metrics = composer.get("metrics") if isinstance(composer.get("metrics"), dict) else {}
    output_contract = (
        composer.get("real_run_output_contract")
        if isinstance(composer.get("real_run_output_contract"), dict)
        else {}
    )
    if any(
        normalize_bool(value)
        for value in (
            composer.get("provider_execution_performed"),
            metrics.get("provider_execution_performed"),
            output_contract.get("provider_execution_performed"),
        )
    ):
        return True
    for provider in composer.get("provider_reports") or []:
        if not isinstance(provider, dict):
            continue
        workload = (
            provider.get("npu_device_workload")
            if isinstance(provider.get("npu_device_workload"), dict)
            else {}
        )
        if (
            mapping_has_execution_evidence(provider)
            or normalize_bool(workload.get("performed"))
            or text_has_execution_evidence(str(provider.get("response_text") or ""))
        ):
            return True
    for audit in composer.get("npu_audits") or []:
        if not isinstance(audit, dict):
            continue
        workload = (
            audit.get("npu_device_workload")
            if isinstance(audit.get("npu_device_workload"), dict)
            else {}
        )
        if (
            mapping_has_execution_evidence(audit)
            or normalize_bool(workload.get("performed"))
            or text_has_execution_evidence(
                str(
                    audit.get("summary")
                    or audit.get("response_text")
                    or audit.get("micro_task_piece")
                    or ""
                )
            )
        ):
            return True
    return False


def compute_causal_chain(composer: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    startup = (
        composer.get("startup_manifest")
        if isinstance(composer.get("startup_manifest"), dict)
        else {}
    )
    startup_contract = startup.get("contract") if isinstance(startup.get("contract"), dict) else {}
    reconciliation = (
        composer.get("startup_reconciliation")
        if isinstance(composer.get("startup_reconciliation"), dict)
        else {}
    )
    provider_count = int(
        composer.get("provider_report_count") or list_len(composer.get("provider_reports"))
    )
    proposal_count = int(composer.get("proposal_count") or list_len(composer.get("proposals")))
    gpu0_count = int(composer.get("gpu0_review_count") or list_len(composer.get("gpu0_reviews")))
    npu_count = int(composer.get("npu_audit_count") or list_len(composer.get("npu_audits")))
    refs = artifact_count(composer)

    if not (
        startup.get("input_ready_before_heap") is True
        or startup_contract.get("input_ready_before_heap") is True
    ):
        reasons.append("startup input_ready_before_heap not proven")
    if refs <= 0:
        reasons.append("startup/context artifact refs missing")
    if provider_count <= 0:
        reasons.append("provider reports missing")
    if proposal_count <= 0:
        reasons.append("proposal chunks missing")
    if gpu0_count <= 0:
        reasons.append("GPU0 review/refine evidence missing")
    if npu_count <= 0:
        reasons.append("NPU audit/workload evidence missing")
    if reconciliation and reconciliation.get("passed") is not True:
        reasons.append("startup reconciliation did not pass")

    status = "passed" if not reasons else "failed"
    return {
        "status": status,
        "passed": not reasons,
        "artifact_ref_count": refs,
        "provider_report_count": provider_count,
        "proposal_count": proposal_count,
        "gpu0_review_count": gpu0_count,
        "npu_audit_count": npu_count,
        "reasons": reasons,
    }


def compute_product_acceptance(composer: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    product_status = str(composer.get("product_status") or "")
    quality_output_passed = composer.get("quality_output_passed")
    accepted_count = int(composer.get("accepted_proposal_count") or 0)
    rejected_count = int(composer.get("rejected_proposal_count") or 0)
    blockers = (
        composer.get("blocking_issues") if isinstance(composer.get("blocking_issues"), list) else []
    )

    if product_status != "ready":
        reasons.append(f"product_status={product_status or 'missing'}")
    if quality_output_passed is not True:
        reasons.append(f"quality_output_passed={quality_output_passed}")
    if accepted_count <= 0:
        reasons.append("no accepted proposal chunks")
    if blockers:
        reasons.append(f"blocking_issue_count={len(blockers)}")
    if rejected_count > 0 and accepted_count <= 0:
        reasons.append("all proposal chunks rejected")

    if not reasons:
        status = "passed"
        passed: bool | None = True
    elif product_status == "blocked_with_reason" or blockers:
        status = "blocked"
        passed = False
    else:
        status = "failed"
        passed = False
    return {
        "status": status,
        "passed": passed,
        "product_status": product_status,
        "quality_output_passed": quality_output_passed,
        "accepted_proposal_count": accepted_count,
        "rejected_proposal_count": rejected_count,
        "blocking_issue_count": len(blockers),
        "reasons": reasons,
    }


def build_report(composer: dict[str, Any], composer_path: Path) -> dict[str, Any]:
    causal_chain = compute_causal_chain(composer)
    product_acceptance = compute_product_acceptance(composer)
    return {
        "schema_version": 1,
        "kind": "external_heap_final_causality_normalization",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "composer_json": str(composer_path),
        "causal_chain_status": causal_chain["status"],
        "causal_chain_passed": causal_chain["passed"],
        "product_acceptance_status": product_acceptance["status"],
        "product_acceptance_passed": product_acceptance["passed"],
        "legacy_product_causality_status": composer.get("product_causality_status"),
        "legacy_product_causality_passed": composer.get("product_causality_passed"),
        "causal_chain": causal_chain,
        "product_acceptance": product_acceptance,
        "provider_execution_performed": provider_execution_performed(composer),
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": [],
        "warnings": [
            "causal_chain_passed does not imply product_acceptance_passed",
            "this adapter is external to python -m ia_carmine.cli run_heap_runtime_completeness_gate",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# External Heap Final Causality Normalization",
        "",
        f"- Causal chain status: `{report['causal_chain_status']}`",
        f"- Causal chain passed: `{report['causal_chain_passed']}`",
        f"- Product acceptance status: `{report['product_acceptance_status']}`",
        f"- Product acceptance passed: `{report['product_acceptance_passed']}`",
        f"- Provider execution performed: `{report['provider_execution_performed']}`",
        "",
        "## Causal chain reasons",
        "",
    ]
    chain_reasons = report.get("causal_chain", {}).get("reasons", [])
    (
        lines.extend(f"- {item}" for item in chain_reasons)
        if chain_reasons
        else lines.append("- none")
    )
    lines.extend(["", "## Product acceptance reasons", ""])
    product_reasons = report.get("product_acceptance", {}).get("reasons", [])
    (
        lines.extend(f"- {item}" for item in product_reasons)
        if product_reasons
        else lines.append("- none")
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--composer-json", required=True)
    parser.add_argument("--output", default="")
    parser.add_argument("--markdown-output", default="")
    args = parser.parse_args()

    composer_path = Path(args.composer_json).resolve()
    composer = read_json(composer_path)
    if not composer:
        raise SystemExit(f"composer JSON unreadable or empty: {composer_path}")
    output = (
        Path(args.output).resolve()
        if args.output
        else composer_path.with_name("heap_final_causality_normalized.json")
    )
    markdown_output = (
        Path(args.markdown_output).resolve() if args.markdown_output else output.with_suffix(".md")
    )
    report = build_report(composer, composer_path)
    write_json(output, report)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["causal_chain_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
