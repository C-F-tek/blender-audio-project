#!/usr/bin/env python3
"""Always-on NPU-light guardrail service for AI artifacts and smart context packets.

The service is intentionally safe:
- it performs deterministic guardrail checks even when OpenVINO/NPU is missing;
- it records a preflight report for the real NPU stack;
- it can fail softly by default so the helper lane does not block the project;
- it only writes reports/logs under output/;
- it emits structured remediation requests that an orchestrator or AI agent can
  use to enrich intermediates or request Python/code corrections.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from npu_runtime import (
    DEFAULT_MODEL_DIR,
    DEFAULT_NPU_PYTHON,
    guardrail_runtime_summary,
    npu_preflight,
    write_npu_preflight_report,
)

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "output" / "ai_pipeline" / "npu_guardrail_report.json"
EVENT_LOG = ROOT / "output" / "workflow_logs" / "npu_guardrail_events.jsonl"

BLOCKED_PATTERNS = {
    "ShaderNodeTexMusgrave": "Musgrave node unavailable in the Blender 5.x target environment.",
    "bpy.ops.wm.open_mainfile": "Generated scripts should not open project files implicitly.",
}
WARNING_PATTERNS = {
    "C:\\Users\\": "Potential hardcoded local Windows user path.",
    "bpy.ops.object.delete": "Scene deletion should be explicit, configurable, and documented.",
    "TODO": "Unresolved TODO marker in AI artifact.",
    "not specified": "Artifact contains unspecified assumptions; review whether they are acceptable.",
}
REQUIRED_IDEAS = ["Blender", "keyframe", "scene", "audio"]
SMART_CONTEXT_IDEAS = ["analysis_blender_keyframes", "scene_script", "selected_capsules"]
INTERMEDIATE_ENRICHMENT_FIELDS = {
    "track_summary": ["duration_sec", "estimated_bpm", "primary_series", "ai_readiness"],
    "music_segments": ["segments", "visual_directive", "estimated_intensity"],
    "audio_event_map": ["peak_events", "beats_sec", "series_used_for_peaks"],
    "scene_brief": [
        "creative_intent",
        "technical_intent",
        "recommended_visual_progression",
        "assumptions",
    ],
    "smart_context_packet": ["selected_capsules", "capsule_manifest", "task", "recommended_inputs"],
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_event(event: str, payload: dict[str, Any]) -> None:
    try:
        EVENT_LOG.parent.mkdir(parents=True, exist_ok=True)
        with EVENT_LOG.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    {"time": now_iso(), "event": event, "payload": payload}, ensure_ascii=False
                )
                + "\n"
            )
    except Exception:
        pass


def read_json(path: Path) -> tuple[Any, list[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace")), []
    except Exception as exc:
        return {"read_error": str(exc), "path": str(path)}, [f"json_read_error:{exc}"]


def targets(path: Path, recursive: bool = False) -> list[Path]:
    if path.is_file():
        return [path]
    if path.is_dir():
        pattern = "**/*.json" if recursive else "*.json"
        return sorted(p for p in path.glob(pattern) if p.is_file())
    return []


def pattern_findings(text: str, patterns: dict[str, str], prefix: str) -> list[str]:
    findings: list[str] = []
    for pattern, reason in patterns.items():
        if pattern in text:
            findings.append(f"{prefix}:{pattern}: {reason}")
    return findings


def idea_scan(
    text: str, ideas: list[str], prefix: str, required: bool
) -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    positives: list[str] = []
    for idea in ideas:
        if re.search(re.escape(idea), text, re.IGNORECASE):
            positives.append(f"{prefix}_present:{idea}")
        elif required:
            warnings.append(f"{prefix}_missing:{idea}")
    return warnings, positives


def artifact_type(path: Path, payload: Any) -> str:
    if isinstance(payload, dict):
        if payload.get("kind"):
            return str(payload.get("kind"))
        if payload.get("selected_capsules") or payload.get("capsule_manifest"):
            return "smart_context_packet"
        if payload.get("segments"):
            return "music_segments"
        if payload.get("peak_events") or payload.get("beats_sec"):
            return "audio_event_map"
        if payload.get("creative_intent") or payload.get("technical_intent"):
            return "scene_brief"
        if path.name == "track_summary.json":
            return "track_summary"
    return path.stem


def is_pythonish(path: Path, payload: Any, text: str) -> bool:
    if path.suffix == ".py":
        return True
    lowered = text.lower()
    return any(token in lowered for token in ("python", "bpy.", "script", "traceback", ".py"))


def remediation(
    action_type: str,
    priority: str,
    target: Path,
    reason: str,
    instruction: str,
    suggested_stage: str,
    auto_safe: bool,
    source_finding: str,
) -> dict[str, Any]:
    return {
        "action_type": action_type,
        "priority": priority,
        "target": str(target),
        "reason": reason,
        "instruction": instruction,
        "suggested_stage": suggested_stage,
        "auto_safe": auto_safe,
        "source_finding": source_finding,
    }


def missing_fields(payload: Any, kind: str) -> list[str]:
    if not isinstance(payload, dict):
        return []
    wanted = INTERMEDIATE_ENRICHMENT_FIELDS.get(kind, [])
    missing: list[str] = []
    for field in wanted:
        if field not in payload and not any(field in str(value) for value in payload.values()):
            missing.append(field)
    return missing


def remediation_requests(
    path: Path,
    payload: Any,
    text: str,
    kind: str,
    blocking: list[str],
    warnings: list[str],
    score: float,
) -> list[dict[str, Any]]:
    requests: list[dict[str, Any]] = []
    pythonish = is_pythonish(path, payload, text)

    for finding in blocking:
        if "ShaderNodeTexMusgrave" in finding:
            requests.append(
                remediation(
                    "fix_python_code",
                    "high",
                    path,
                    "Generated or indexed code references a Blender node that is blocked for the target Blender 5.x environment.",
                    "Replace ShaderNodeTexMusgrave with a Blender 5.x compatible procedural material strategy such as ShaderNodeTexNoise, ShaderNodeTexVoronoi and ColorRamp. Keep the change local and configurable.",
                    "python_patch_or_regenerate_code",
                    False,
                    finding,
                )
            )
        elif pythonish:
            requests.append(
                remediation(
                    "fix_python_code",
                    "high",
                    path,
                    "Blocking pattern detected in a Python-like artifact.",
                    "Request a focused Python correction patch. Do not rewrite the whole package; remove the blocked construct and preserve configurable paths and entry points.",
                    "python_patch_or_regenerate_code",
                    False,
                    finding,
                )
            )
        else:
            requests.append(
                remediation(
                    "review_generated_artifact",
                    "high",
                    path,
                    "Blocking pattern detected in an AI artifact.",
                    "Request a revised artifact from the planner/generator with the blocked pattern removed and the assumption documented.",
                    "regenerate_ai_artifact",
                    False,
                    finding,
                )
            )

    for finding in warnings:
        if "schema_version_missing" in finding or "explicit_assumptions_missing" in finding:
            requests.append(
                remediation(
                    "enrich_intermediate_data",
                    "medium",
                    path,
                    "Intermediate artifact is missing metadata required for reliable downstream AI planning.",
                    "Rerun or enrich the intermediate builder so the artifact includes schema_version, explicit assumptions and planner-ready metadata.",
                    "enrich_intermediates",
                    True,
                    finding,
                )
            )
        elif "artifact_large_for_npu_light_guardrail" in finding:
            requests.append(
                remediation(
                    "create_compact_summary",
                    "medium",
                    path,
                    "Artifact is too large for NPU-light review.",
                    "Create a compact summary artifact and use the full JSON only as a read-only source of truth.",
                    "compact_context_generation",
                    True,
                    finding,
                )
            )
        elif "local_windows_paths_present" in finding or "C:\\Users" in finding:
            requests.append(
                remediation(
                    "parameterize_path",
                    "medium",
                    path,
                    "Local workstation path detected.",
                    "Move the path into config or mark the artifact as local-only. Do not hardcode private paths in reusable generated packages.",
                    "python_patch_or_config_enrichment",
                    False,
                    finding,
                )
            )
        elif "too_few_selected_capsules" in finding or "smart_context_idea_missing" in finding:
            requests.append(
                remediation(
                    "rerun_context_selection",
                    "medium",
                    path,
                    "Smart context packet is under-specified for the requested task.",
                    "Rerun smart context generation with a more specific task and include additional task capsules, code chunks and artifact references.",
                    "smart_context_generation",
                    True,
                    finding,
                )
            )

    miss = missing_fields(payload, kind)
    if miss:
        requests.append(
            remediation(
                "enrich_intermediate_data",
                "medium" if score >= 0.5 else "high",
                path,
                f"{kind} artifact is missing planner-useful fields: {', '.join(miss)}.",
                "Add the missing fields through the relevant deterministic builder or a small AI enrichment pass. Preserve the original source analysis JSON as read-only.",
                "enrich_intermediates",
                True,
                "missing_fields:" + ",".join(miss),
            )
        )

    if score < 0.55 and not blocking:
        requests.append(
            remediation(
                "multi_pass_review",
                "medium",
                path,
                "Guardrail score is low but no blocking pattern was found.",
                "Run an additional review/enrichment pass before using this artifact as central AI context.",
                "guardrail_second_pass",
                True,
                f"low_score:{score}",
            )
        )

    return requests


def review(path: Path, max_chars: int) -> dict[str, Any]:
    payload, read_warnings = read_json(path)
    text = json.dumps(payload, ensure_ascii=False)
    kind = artifact_type(path, payload)
    warnings: list[str] = list(read_warnings)
    blocking: list[str] = []
    positives: list[str] = []

    blocking.extend(pattern_findings(text, BLOCKED_PATTERNS, "blocked_pattern"))
    warnings.extend(pattern_findings(text, WARNING_PATTERNS, "warning_pattern"))

    if len(text) <= max_chars:
        positives.append("size_ok_for_npu_light_guardrail")
    else:
        warnings.append(f"artifact_large_for_npu_light_guardrail:{len(text)}>{max_chars}")

    base_warnings, base_positives = idea_scan(text, REQUIRED_IDEAS, "required_idea", required=False)
    warnings.extend(base_warnings)
    positives.extend(base_positives)

    if kind == "smart_context_packet":
        smart_warnings, smart_positives = idea_scan(
            text, SMART_CONTEXT_IDEAS, "smart_context_idea", required=True
        )
        warnings.extend(smart_warnings)
        positives.extend(smart_positives)

    if isinstance(payload, dict):
        if payload.get("schema_version"):
            positives.append("schema_version_present")
        else:
            warnings.append("schema_version_missing")
        selected = payload.get("selected_capsules")
        manifest = payload.get("capsule_manifest")
        assumptions = payload.get("assumptions")
        if isinstance(selected, list):
            positives.append(f"selected_capsules={len(selected)}")
            if len(selected) < 2:
                warnings.append("too_few_selected_capsules")
        if isinstance(manifest, list):
            positives.append(f"manifest_capsules={len(manifest)}")
        if kind in {"scene_brief", "smart_context_packet"} and not assumptions:
            warnings.append("explicit_assumptions_missing")

    score = max(
        0.0,
        min(
            1.0,
            round(
                1.0
                - len(blocking) * 0.35
                - len(warnings) * 0.045
                + min(0.22, len(positives) * 0.015),
                4,
            ),
        ),
    )
    severity = "blocking" if blocking else "warning" if warnings else "clean"
    requests = remediation_requests(path, payload, text, kind, blocking, warnings, score)
    return {
        "path": str(path),
        "artifact_type": kind,
        "size_chars": len(text),
        "score": score,
        "severity": severity,
        "passed": not blocking,
        "blocking": blocking,
        "warnings": warnings,
        "positives": positives,
        "remediation_requests": requests,
    }


def aggregate_remediation(reviews: list[dict[str, Any]]) -> dict[str, Any]:
    requests = [
        item for review_item in reviews for item in review_item.get("remediation_requests", [])
    ]
    by_stage: dict[str, list[dict[str, Any]]] = {}
    by_type: dict[str, int] = {}
    for item in requests:
        by_stage.setdefault(item["suggested_stage"], []).append(item)
        by_type[item["action_type"]] = by_type.get(item["action_type"], 0) + 1
    auto_safe = [item for item in requests if item.get("auto_safe")]
    manual = [item for item in requests if not item.get("auto_safe")]
    return {
        "request_count": len(requests),
        "auto_safe_count": len(auto_safe),
        "manual_review_count": len(manual),
        "by_type": by_type,
        "by_stage": {key: len(value) for key, value in by_stage.items()},
        "next_auto_safe_stages": sorted(by_stage.keys()),
        "requests": requests,
    }


def write_md(report: dict[str, Any], path: Path) -> None:
    pre = report.get("npu_preflight") or {}
    runtime = report.get("runtime_summary") or {}
    remediation_plan = report.get("remediation_plan") or {}
    lines = [
        "# NPU Guardrail Report",
        "",
        f"Generated: `{report.get('generated_at')}`",
        f"Passed: `{report.get('passed')}`",
        f"Soft fail: `{report.get('soft_fail')}`",
        f"Average score: `{report.get('average_score')}`",
        "",
        "## Runtime",
        f"- Mode: `{runtime.get('mode')}`",
        f"- Ready: `{runtime.get('ready')}`",
        f"- NPU available: `{runtime.get('npu_device_available')}`",
        f"- Recommended workers: `{runtime.get('recommended_workers')}`",
        f"- Devices: `{pre.get('openvino_available_devices')}`",
        "",
        "## Remediation Plan",
        f"- Requests: `{remediation_plan.get('request_count', 0)}`",
        f"- Auto-safe requests: `{remediation_plan.get('auto_safe_count', 0)}`",
        f"- Manual review requests: `{remediation_plan.get('manual_review_count', 0)}`",
    ]
    for action_type, count in (remediation_plan.get("by_type") or {}).items():
        lines.append(f"- {action_type}: `{count}`")
    lines += ["", "## Reviews"]
    for item in report.get("reviews", []):
        lines += [
            "",
            f"### {item.get('path')}",
            f"- Type: `{item.get('artifact_type')}`",
            f"- Score: `{item.get('score')}`",
            f"- Severity: `{item.get('severity')}`",
            f"- Passed: `{item.get('passed')}`",
        ]
        for block in item.get("blocking", []):
            lines.append(f"- BLOCKING: {block}")
        for warning in item.get("warnings", [])[:24]:
            lines.append(f"- Warning: {warning}")
        for request in item.get("remediation_requests", [])[:12]:
            lines.append(
                f"- Request `{request.get('action_type')}` / `{request.get('priority')}`: {request.get('instruction')}"
            )
        for positive in item.get("positives", [])[:16]:
            lines.append(f"- OK: {positive}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_action_queue(remediation_plan: dict[str, Any], report_path: Path) -> Path:
    queue_path = report_path.with_name("npu_guardrail_action_queue.json")
    payload = {
        "schema_version": 1,
        "generated_at": now_iso(),
        "source_report": str(report_path),
        "queue": remediation_plan.get("requests", []),
    }
    queue_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return queue_path


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
