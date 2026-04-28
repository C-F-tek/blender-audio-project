#!/usr/bin/env python3
"""NPU-light guardrail service for AI artifacts and smart context packets."""
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
    "ShaderNodeTexMusgrave": "Musgrave node unavailable in Blender 5.x target failures.",
    "bpy.ops.wm.open_mainfile": "Generated scripts should not open project files implicitly.",
    "exec(": "Dynamic exec is hard to audit.",
    "eval(": "Dynamic eval is hard to audit.",
}
REQUIRED_IDEAS = ["analysis_blender_keyframes", "keyframe", "scene_script", "Blender"]


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


def targets(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if path.is_dir():
        return sorted(p for p in path.glob("*.json") if p.is_file())
    return []


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
        warnings.append("local_windows_paths_present")
    if len(text) <= 180000:
        positives.append("size_ok_for_npu_light_guardrail")
    else:
        warnings.append("artifact_large_for_npu_light_guardrail")
    return warnings, positives


def review(path: Path) -> dict[str, Any]:
    payload = read_json(path)
    text = json.dumps(payload, ensure_ascii=False)
    warnings, positives = scan_text(text)
    if isinstance(payload, dict):
        selected = payload.get("selected_capsules")
        manifest = payload.get("capsule_manifest")
        if isinstance(selected, list):
            positives.append(f"selected_capsules={len(selected)}")
            if len(selected) < 2:
                warnings.append("too_few_selected_capsules")
        if isinstance(manifest, list):
            positives.append(f"manifest_capsules={len(manifest)}")
    score = max(0.0, min(1.0, round(1.0 - len(warnings) * 0.08 + min(0.2, len(positives) * 0.015), 4)))
    return {"path": str(path), "size_chars": len(text), "score": score, "passed": not any(w.startswith("blocked_pattern") for w in warnings), "warnings": warnings, "positives": positives}


def write_md(report: dict[str, Any], path: Path) -> None:
    pre = report.get("npu_preflight") or {}
    lines = ["# NPU Guardrail Report", "", f"Generated: `{report.get('generated_at')}`", f"Passed: `{report.get('passed')}`", "", "## NPU Preflight", f"- Ready: `{pre.get('ready')}`", f"- NPU available: `{pre.get('npu_device_available')}`", f"- Devices: `{pre.get('openvino_available_devices')}`", "", "## Reviews"]
    for item in report.get("reviews", []):
        lines += ["", f"### {item.get('path')}", f"- Score: `{item.get('score')}`", f"- Passed: `{item.get('passed')}`"]
        for warning in item.get("warnings", []):
            lines.append(f"- Warning: {warning}")
        for positive in item.get("positives", [])[:12]:
            lines.append(f"- OK: {positive}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", default=str(DEFAULT_OUT))
    ap.add_argument("--device", default="NPU")
    ap.add_argument("--python-exe", default=str(DEFAULT_NPU_PYTHON))
    ap.add_argument("--model-dir", default=str(DEFAULT_MODEL_DIR))
    args = ap.parse_args()
    input_path = Path(args.input).resolve()
    preflight = npu_preflight(args.python_exe, args.model_dir)
    reviews = [review(p) for p in targets(input_path)]
    warnings = [w for r in reviews for w in r.get("warnings", [])]
    report = {"schema_version": 1, "kind": "npu_guardrail_report", "generated_at": now_iso(), "backend": "deterministic_guardrail_with_openvino_preflight", "requested_device": args.device, "npu_preflight": preflight, "review_count": len(reviews), "passed": bool(reviews) and all(r.get("passed") for r in reviews), "average_score": round(sum(r.get("score", 0.0) for r in reviews) / len(reviews), 4) if reviews else 0.0, "warnings": warnings, "reviews": reviews, "note": "NPU-light lane: useful guardrail/preflight work without using GPU VRAM."}
    out = Path(args.output).resolve(); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_npu_preflight_report(preflight, out.with_name("npu_guardrail_preflight.json"))
    write_md(report, out.with_suffix(".md"))
    append_event("guardrail_report", {"output": str(out), "passed": report["passed"], "average_score": report["average_score"], "npu_ready": preflight.get("ready")})
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
