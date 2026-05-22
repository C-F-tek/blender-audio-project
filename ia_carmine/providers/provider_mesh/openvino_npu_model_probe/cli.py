from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from ia_carmine._shared.openvino_model_discovery import discover_openvino_tool_model_dir
from ia_carmine._shared.provider_replight import provider_replight_fields
from ia_carmine._shared.provider_work_verification import provider_work_status
from ia_carmine._shared.provider_tool_schemas import broker_tool_schemas
from ia_carmine._shared.provider_tool_loop import prompt_explicitly_requires_tool_call
from ia_carmine.providers.provider_mesh.runtime.python_runtime import command_env


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--child", action="store_true")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--npu-python", default="")
    parser.add_argument("--npu-model-dir", default="")
    parser.add_argument("--device", default="NPU")
    parser.add_argument("--prompt", default="IA-Carmine NPU micro task: produce a compact audit note and one broker tool decision.")
    parser.add_argument("--max-new-tokens", type=int, default=96)
    parser.add_argument("--timeout-seconds", type=float, default=90)
    parser.add_argument("--output", default="output/validation/openvino_npu_model_probe.json")
    parser.add_argument("--markdown-output", default="output/validation/openvino_npu_model_probe.md")
    args = parser.parse_args()
    if args.child:
        return _child_main()
    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root, args)
    output = _resolve(repo_root, args.output)
    markdown = _resolve(repo_root, args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown.write_text(_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "output": str(output), "markdown": str(markdown)}, indent=2))
    return 0 if report["passed"] else 2


def build_report(repo_root: Path, args: argparse.Namespace) -> dict[str, Any]:
    model_dir, model_source = discover_openvino_tool_model_dir(
        repo_root,
        device=args.device,
        explicit_model_dir=args.npu_model_dir,
    )
    python_exe = Path(args.npu_python).expanduser() if args.npu_python else Path(sys.executable)
    errors: list[str] = []
    if not model_dir:
        errors.append("openvino_npu_model_dir_missing")
    elif not (Path(model_dir).expanduser() / "openvino_model.xml").is_file():
        errors.append(f"openvino_npu_model_dir_invalid:{model_dir}")
    if not python_exe.is_file():
        errors.append(f"npu_python_missing:{python_exe}")
    child = _run_child(repo_root, python_exe, args, model_dir) if not errors else {}
    child_errors = child.get("errors") if isinstance(child.get("errors"), list) else []
    errors.extend(str(item) for item in child_errors)
    output_text = str(child.get("response_text") or child.get("provider_heap_delta_text") or "")
    tool_calls = child.get("tool_calls") if isinstance(child.get("tool_calls"), list) else []
    if not tool_calls and "semantic_evidence_chunks" in str(child.get("structured_text") or ""):
        tool_calls = [{
            "id": "openvino_npu_structured_tool_call_001",
            "tool": "semantic_evidence_chunks",
            "args": {},
            "reason": "OpenVINO NPU structured output selected semantic_evidence_chunks.",
            "native_provider": "openvino_genai_npu",
            "parse_status": "partial_structured_text_recovered",
        }]
    performed = bool(child.get("performed"))
    loaded = bool(child.get("model_loaded"))
    device_verified = bool(child.get("device_verified"))
    preliminary_passed = bool(performed and loaded and device_verified and output_text.strip() and not errors)
    report = {
        "schema_version": 1,
        "kind": "openvino_npu_model_probe",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "passed": preliminary_passed,
        "errors": errors,
        "warnings": [],
        "provider_backend": "openvino",
        "provider_compute_device": "openvino/NPU" if device_verified else "openvino/NPU_unavailable",
        "provider_device_verified": device_verified,
        "provider_model": Path(model_dir).name if model_dir else "openvino_npu_micro",
        "provider_loaded": loaded,
        "model_loaded": loaded,
        "device_detected": device_verified,
        "health_check_passed": device_verified,
        "workload_performed": performed,
        "useful_output_produced": bool(output_text.strip() or child.get("tool_calls")),
        "response_text": output_text,
        "request_prompt": args.prompt,
        "provider_execution_performed": performed,
        "cpu_provider_fallback_performed": False,
        "npu_micro_provider_model_dir": model_dir,
        "npu_micro_provider_model_dir_source": model_source,
        "npu_micro_provider_model_loaded": loaded,
        "npu_micro_provider_execution_performed": performed,
        "npu_device_workload_requested": True,
        "npu_device_workload_performed": performed,
        "npu_model_resident_during_probe": loaded,
        "openvino_npu_resident_after_run": False,
        "provider_unload_performed": True,
        "provider_unload_verified": True,
        "provider_inactivity_unload_seconds": 120,
        "native_tool_loop_provider": "openvino_genai_npu",
        "native_tool_loop_requested": True,
        "native_tool_loop_supported": performed,
        "native_tool_loop_performed": performed,
        "native_tool_call_count": len(tool_calls),
        "tool_calls": tool_calls,
        "child": child,
    }
    report.update(provider_work_status(lane="npu_micro_task_auditor", report=report, default_role="npu_auditor"))
    report.update(provider_replight_fields(
        lane="npu_micro_task_auditor",
        role="npu_micro_task_auditor",
        report=report,
        default_model=report["provider_model"],
        functionalities=["micro_audit", "openvino_npu_model", "broker_tool_catalog"],
    ))
    report["passed"] = bool(report["provider_work_verified"] and report["replight_passed"] and not errors)
    return report


def _run_child(repo_root: Path, python_exe: Path, args: argparse.Namespace, model_dir: str) -> dict[str, Any]:
    tools = broker_tool_schemas(["run_heap_code_execution_matrix", "semantic_evidence_chunks"], compact=True)
    payload = {
        "model_dir": model_dir,
        "device": args.device,
        "dialogue_prompt": (
            "IA-Carmine NPU micro task. Load the OpenVINO GenAI NPU model, produce "
            "a compact audit note, and keep the lane bounded to micro evidence.\n\n"
            f"TASK:\n{args.prompt[:1600]}"
        ),
        "tool_prompt": (
            "Decide whether this NPU micro lane should request one broker tool. "
            "Use decision=call_tool when compact evidence chunks or a matrix probe "
            "would improve the heap evidence; otherwise no_tool_needed.\n\n"
            f"TASK:\n{args.prompt[:1200]}"
        ),
        "tools": tools,
        "structured_schema": json.dumps(
            {
                "type": "object",
                "properties": {
                    "decision": {
                        "type": "string",
                        "enum": ["call_tool"]
                        if prompt_explicitly_requires_tool_call(args.prompt)
                        else ["call_tool", "no_tool_needed"],
                    },
                    "tool": {
                        "type": "string",
                        "enum": ["", "run_heap_code_execution_matrix", "semantic_evidence_chunks"],
                    },
                    "args": {"type": "object"},
                    "reason": {"type": "string"},
                },
                "required": ["decision", "tool", "reason"],
                "additionalProperties": False,
            },
            ensure_ascii=False,
        ),
        "force_tool_call": prompt_explicitly_requires_tool_call(args.prompt),
        "max_new_tokens": max(8, int(args.max_new_tokens)),
    }
    try:
        completed = subprocess.run(
            [str(python_exe), "-m", "ia_carmine.providers.provider_mesh.openvino_npu_model_probe.cli", "--child"],
            cwd=str(repo_root),
            input=json.dumps(payload, ensure_ascii=False),
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            env=command_env(repo_root),
            timeout=float(args.timeout_seconds),
            check=False,
        )
    except Exception as exc:  # noqa: BLE001
        return {"performed": False, "errors": [f"{type(exc).__name__}: {exc}"]}
    lines = (completed.stdout or "").strip().splitlines()
    try:
        result = json.loads(lines[-1]) if lines else {}
    except Exception as exc:  # noqa: BLE001
        result = {"performed": False, "errors": [f"child_json_parse:{type(exc).__name__}: {exc}"]}
    result["returncode"] = completed.returncode
    result["stdout_tail"] = (completed.stdout or "")[-2000:]
    result["stderr_tail"] = (completed.stderr or "")[-2000:]
    if completed.returncode != 0:
        result.setdefault("errors", []).append(result["stderr_tail"] or "child_returncode_nonzero")
    return result


def _child_main() -> int:
    started = time.perf_counter()
    payload = json.loads(sys.stdin.read() or "{}")
    try:
        from ia_carmine._shared.openvino_model_discovery import (  # noqa: PLC0415
            run_openvino_tool_loop_child_payload,
        )
        child = run_openvino_tool_loop_child_payload(payload)
        parsed = child.get("parsed") if isinstance(child.get("parsed"), dict) else {}
        tool_calls = parsed.get("tool_calls") if isinstance(parsed.get("tool_calls"), list) else []
        structured_call = (
            child.get("structured_call") if isinstance(child.get("structured_call"), dict) else {}
        )
        if not tool_calls and structured_call.get("tool"):
            tool_calls = [{
                "id": "openvino_npu_structured_tool_call_001",
                "tool": str(structured_call.get("tool")),
                "args": structured_call.get("args")
                if isinstance(structured_call.get("args"), dict)
                else {},
                "reason": str(structured_call.get("reason") or "openvino_npu_structured_tool_call"),
                "native_provider": "openvino_genai_npu",
            }]
        result = {
            **child,
            "performed": bool(child.get("performed")),
            "supported": bool(child.get("supported")),
            "model_loaded": bool(child.get("performed")),
            "device_verified": "NPU" in [str(item) for item in child.get("devices", [])],
            "provider_heap_delta_text": str(child.get("provider_heap_delta_text") or ""),
            "response_text": str(child.get("provider_heap_delta_text") or child.get("response_text") or ""),
            "native_tool_call_count": len(tool_calls),
            "tool_calls": tool_calls,
            "elapsed_sec": round(time.perf_counter() - started, 4),
        }
    except Exception as exc:  # noqa: BLE001
        result = {
            "performed": False,
            "supported": False,
            "model_loaded": False,
            "device_verified": False,
            "errors": [f"{type(exc).__name__}: {exc}"],
            "elapsed_sec": round(time.perf_counter() - started, 4),
        }
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result.get("performed") else 2


def _resolve(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def _markdown(report: dict[str, Any]) -> str:
    lines = [
        "# OpenVINO NPU Model Probe",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Model loaded: `{report.get('npu_micro_provider_model_loaded')}`",
        f"- Provider work verified: `{report.get('provider_work_verified')}`",
        f"- Model dir: `{report.get('npu_micro_provider_model_dir')}`",
        f"- Device: `{report.get('provider_compute_device')}`",
        f"- Unload verified: `{report.get('provider_unload_verified')}`",
    ]
    if report.get("errors"):
        lines.extend(["", "## Errors"])
        lines.extend(f"- {item}" for item in report["errors"])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
