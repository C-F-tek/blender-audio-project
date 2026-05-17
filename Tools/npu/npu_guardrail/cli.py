"""CLI for NPU guardrail service."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from Tools.npu._shared.npu_runtime import (
    guardrail_runtime_summary,
    npu_preflight,
    write_npu_preflight_report,
)

from .common import append_event, now_iso, targets
from .config import DEFAULT_MODEL_DIR, DEFAULT_NPU_PYTHON, DEFAULT_OUT
from .reporting import write_action_queue, write_md
from .review import aggregate_remediation, review

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", default=str(DEFAULT_OUT))
    ap.add_argument("--device", default="NPU")
    ap.add_argument("--python-exe", default=str(DEFAULT_NPU_PYTHON))
    ap.add_argument("--model-dir", default=str(DEFAULT_MODEL_DIR))
    ap.add_argument("--max-chars", type=int, default=180000)
    ap.add_argument("--recursive", action="store_true")
    ap.add_argument(
        "--strict", action="store_true", help="Return non-zero when blocking findings are present."
    )
    ap.add_argument("--soft-fail", dest="soft_fail", action="store_true", default=True)
    ap.add_argument("--hard-fail", dest="soft_fail", action="store_false")
    ap.add_argument("--write-action-queue", action="store_true", default=True)
    args = ap.parse_args()

    input_path = Path(args.input).resolve()
    preflight = npu_preflight(args.python_exe, args.model_dir)
    runtime = guardrail_runtime_summary(preflight)
    items = targets(input_path, recursive=args.recursive)
    reviews = [review(p, args.max_chars) for p in items]
    blocking = [b for r in reviews for b in r.get("blocking", [])]
    warnings = [w for r in reviews for w in r.get("warnings", [])]
    remediation_plan = aggregate_remediation(reviews)
    passed = bool(reviews) and not blocking
    report = {
        "schema_version": 3,
        "kind": "npu_guardrail_report",
        "generated_at": now_iso(),
        "backend": "always_on_deterministic_guardrail_with_openvino_preflight_and_remediation_requests",
        "requested_device": args.device,
        "soft_fail": args.soft_fail,
        "npu_preflight": preflight,
        "runtime_summary": runtime,
        "input": str(input_path),
        "review_count": len(reviews),
        "passed": passed,
        "average_score": round(sum(r.get("score", 0.0) for r in reviews) / len(reviews), 4)
        if reviews
        else 0.0,
        "blocking": blocking,
        "warnings": warnings,
        "remediation_plan": remediation_plan,
        "reviews": reviews,
        "note": "Always-on NPU-light lane: validates, critiques, and emits safe correction/enrichment requests without directly modifying source files.",
    }
    out = Path(args.output).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_npu_preflight_report(preflight, out.with_name("npu_guardrail_preflight.json"))
    if args.write_action_queue:
        action_queue = write_action_queue(remediation_plan, out)
    else:
        action_queue = None
    write_md(report, out.with_suffix(".md"))
    append_event(
        "guardrail_report",
        {
            "output": str(out),
            "passed": report["passed"],
            "average_score": report["average_score"],
            "runtime": runtime,
            "blocking_count": len(blocking),
            "warning_count": len(warnings),
            "remediation_request_count": remediation_plan["request_count"],
            "action_queue": str(action_queue) if action_queue else None,
        },
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))

    should_fail = args.strict or not args.soft_fail
    return 0 if report["passed"] or not should_fail else 2


if __name__ == "__main__":
    raise SystemExit(main())
