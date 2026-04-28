#!/usr/bin/env python3
"""Lightweight NPU guardrail/service helper.

This script is intentionally small and safe. It gives the NPU lane useful work:
preflight OpenVINO/NPU availability, review smart context packets, detect blocked
Blender/API patterns, and write AI-readable guardrail reports.

When OpenVINO GenAI is ready, this can be extended to run an actual small model
on NPU. Until then it still records device readiness and performs deterministic
review without consuming GPU VRAM.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from npu_runtime import DEFAULT_MODEL_DIR, DEFAULT_NPU_PYTHON, npu_preflight, write_npu_preflight_report


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "output" / "ai_pipeline" / "npu_guardrail_report.json"
EVENT_LOG = ROOT / "output" / "workflow_logs" / "npu_guardrail_events.jsonl"

BLOCKED_PATTERNS = {
    "ShaderNodeTexMusgrave": "Musgrave node is unavailable in target Blender 5.x failures; use Noise/Voronoi alternatives.",
    "bpy.ops.wm.open_mainfile": "Generated scripts should not open project files implicitly.",
    "exec(": "Generated dynamic exec is unsafe and hard to review.",
    "eval(": "Generated dynamic eval is unsafe and hard to review.",
}

REQUIRED_IDEAS = [
    "analysis_blender_keyframes",
    "keyframe",
    "scene_script",
    "Blender",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_event(event: str, payload: dict[str, Any]) -> None:
    try:
        EVENT_LOG.parent.mkdir(parents=True, exist_ok=True)
        with EVENT_LOG.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"time": now_iso(), "event": event, "payload": payload}, ensure_ascii=False) + "\n")
    except Exception:
        pass


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception as exc:
        return {"read_error": str(exc), "path": str(path)}


def scan_text(text: str) -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    positives: list[str] = []
    for pattern, reason in BLOCKED_PATTERNS.items():
        if pattern in text:
            warnings.append(f"blocked_pattern:{pattern}: {reason}")
    for idea in REQUIRED_IDEAS:
        if re.search(re.escape(idea), text, re.IGNORECASE):
            positives.append(f"required_idea_present:{idea}")
        else:
            warnings.append(f"required_idea_missing:{idea}")
    if "C:\\Users\\" in text:
        warnings.append("local_windows_paths_present: paths must be local-only metadata or configurable.")
    if len(text) > 160000:
        warnings.append("packet_large_for_light_guardrail: consider selecting fewer capsules before central generation.")
    else:
        positives.append("packet_size_ok_for_light_guardrail")
    return warnings, positives


def review_packet(path: Path) -> dict[str, Any]:
    payload = read_json(path)
    text = json.dumps(payload, ensure_ascii=False)
    warnings, positives = scan_text(text)
    selected = payload.get("selected_capsules") if isinstance(payload, dict) else []
    manifest = payload.get("capsule_manifest") if isinstance(payload, dict) else []
    if isinstance(selected, list):
        positives.append(f"selected_capsules={len(selected)}")
        if len(selected) < 2:
            warnings.append("too_few_selected_capsules")
    if isinstance(manifest, list):
        positives.append(f"manifest_capsules={len(manifest)}")
        if len(manifest) < len(selected or []):
            warnings.append("manifest_smaller_than_selected_set")

    score = max(0.0, min(1.0, round(1.0 - len(warnings) * 0.08 + min(0.2, len(positives) * 0.015), 4)))
    return {
        "path": str(path),
        "size_chars": len(text),
        "score": score,
        "passed": not any(item.startswith("blocked_pattern") for item in warnings),
        "warnings": warnings,
        "positives": positives,
    }


def write_markdown(report: dict[str, Any], md_path: Path) -> None:
    lines = [
        "# NPU Guardrail Report",
        "",
        f"Generated: `{report.get('generated_at')}`",
        f"Backend: `{report.get('backend')}`",
        f"Requested device: `{report.get('requested_device')}`",
        f"Passed: `{report.get('passed')}`",
        "",
        "## NPU Preflight",
    ]
    pre = report.get("npu_preflight") or {}
    lines.extend([
        f"- Ready: `{pre.get('ready')}`",
        f"- NPU available: `{pre.get('npu_device_available')}`",
        f"- Devices: `{pre.get('openvino_available_devices')}`",
        f"- Python: `{pre.get('python_exe')}`",
        f"- Model dir: `{pre.get('model_dir')}`",
    ])
    if pre.get("errors"):
        lines.append("- Errors:")
        for item in pre.get("errors") or []:
            lines.append(f"  - {item}")
    lines.extend(["", "## Reviews"])
    for review in report.get("reviews", []):
        lines.extend(["", f"### {review.get('path')}", f"- Score: `{review.get('score')}`", f"- Passed: `{review.get('passed')}`"])
        for warning in review.get("warnings", []):
            lines.append(f"- Warning: {warning}")
        for positive in review.get("positives", [])[:12]:
            lines.append(f"- OK: {positive}")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Smart context packet JSON, artifact JSON, or directory containing JSON files.")
    ap.add_argument("--output", default=str(DEFAULT_OUT))
    ap.add_argument("--device", default="NPU")
    ap.add_argument("--python-exe", default=str(DEFAULT_NPU_PYTHON))
    ap.add_argument("--model-dir", default=str(DEFAULT_MODEL_DIR))
    args = ap.parse_args()

    input_path = Path(args.input).resolve()
    if input_path.is_dir():
        targets = sorted(path for path in input_path.glob("*.json") if path.is_file())
    elif input_path.is_file():
        targets = [input_path]
    else:
        targets = []

    preflight = npu_preflight(args.python_exe, args.model_dir)
    reviews = [review_packet(path) for path in targets]
    warnings = [warning for review in reviews for warning in review.get("warnings", [])]
    report = {
        "schema_version": 1,
        "kind": "npu_guardrail_report",
        "generated_at": now_iso(),
        "backend": "deterministic_guardrail_with_openvino_preflight",
        "requested_device": args.device,
        "npu_preflight": preflight,
        "review_count": len(reviews),
        "passed": bool(reviews) and all(review.get("passed") for review in reviews),
        "average_score": round(sum(review.get("score", 0.0) for review in reviews) / len(reviews), 4) if reviews else 0.0,
        "warnings": warnings,
        "reviews": reviews,
        "note": "This is the always-on NPU-light lane. It can be upgraded to OpenVINO GenAI inference when the NPU model is stable.",
    }
    out = Path(args.output).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_npu_preflight_report(preflight, out.with_name("npu_guardrail_preflight.json"))
    write_markdown(report, out.with_suffix(".md"))
    append_event("guardrail_report", {"output": str(out), "passed": report["passed"], "average_score": report["average_score"], "npu_ready": preflight.get("ready")})
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
