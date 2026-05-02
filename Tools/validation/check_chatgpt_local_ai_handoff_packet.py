#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_KIND = "chatgpt_local_ai_handoff_packet"
DEFAULT_OUTPUT = "output/validation/chatgpt_local_ai_handoff_packet_validation.json"
DEFAULT_MARKDOWN = "output/validation/chatgpt_local_ai_handoff_packet_validation.md"

REQUIRED_FIELDS = [
    "schema_version",
    "kind",
    "repository",
    "branch",
    "objective",
    "guardrails",
    "evidence",
    "last_validation",
    "next_action",
]

FORBIDDEN_COMMIT_PATTERNS = [
    "output/",
    ".db",
    ".sqlite",
    "renders/",
]

REQUIRED_GUARDRAILS = [
    "no_provider_direct_execution",
    "no_patch_application_from_provider_output",
    "no_output_artifact_commit",
    "no_sqlite_db_commit",
    "manual_review_required",
]


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def default_template() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "kind": DEFAULT_KIND,
        "repository": "C-F-tek/blender-audio-project",
        "branch": "master",
        "commit": "",
        "objective": "Describe the local IA-Carmine task ChatGPT should continue from.",
        "current_state": {
            "git_status_short": "",
            "latest_commit": "",
            "active_pr": None,
        },
        "guardrails": {
            "no_provider_direct_execution": True,
            "no_patch_application_from_provider_output": True,
            "no_output_artifact_commit": True,
            "no_sqlite_db_commit": True,
            "manual_review_required": True,
        },
        "evidence": [
            {
                "path": "docs/LOCAL_VALIDATION_EVIDENCE/example.json",
                "kind": "compact_evidence_bundle",
                "passed": True,
            }
        ],
        "last_validation": {
            "commands": [],
            "passed": None,
            "summary": "",
        },
        "next_action": {
            "requested": "inspect evidence and propose next safe step",
            "destructive": False,
            "requires_confirmation": False,
        },
        "notes": [],
    }


def validate_packet(packet: dict[str, Any], repo_root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for field in REQUIRED_FIELDS:
        if field not in packet:
            errors.append(f"missing required field: {field}")

    if packet.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if packet.get("kind") != DEFAULT_KIND:
        errors.append(f"kind must be {DEFAULT_KIND}")

    repository = packet.get("repository")
    if repository != "C-F-tek/blender-audio-project":
        warnings.append(f"unexpected repository: {repository}")

    branch = packet.get("branch")
    if not isinstance(branch, str) or not branch.strip():
        errors.append("branch must be a non-empty string")

    objective = packet.get("objective")
    if not isinstance(objective, str) or not objective.strip():
        errors.append("objective must be a non-empty string")

    guardrails = packet.get("guardrails")
    if not isinstance(guardrails, dict):
        errors.append("guardrails must be an object")
    else:
        for key in REQUIRED_GUARDRAILS:
            if guardrails.get(key) is not True:
                errors.append(f"guardrail must be true: {key}")

    evidence = packet.get("evidence")
    if not isinstance(evidence, list):
        errors.append("evidence must be a list")
    else:
        for index, item in enumerate(evidence):
            if not isinstance(item, dict):
                errors.append(f"evidence[{index}] must be an object")
                continue
            path_value = item.get("path")
            if not isinstance(path_value, str) or not path_value.strip():
                errors.append(f"evidence[{index}].path must be a non-empty string")
                continue
            evidence_path = resolve_path(repo_root, path_value)
            if not evidence_path.exists():
                warnings.append(f"evidence path does not exist locally: {path_value}")
            if any(pattern in path_value.replace("\\", "/") for pattern in FORBIDDEN_COMMIT_PATTERNS):
                warnings.append(f"evidence path is local/runtime-only, do not commit directly: {path_value}")

    last_validation = packet.get("last_validation")
    if not isinstance(last_validation, dict):
        errors.append("last_validation must be an object")
    else:
        commands = last_validation.get("commands", [])
        if commands is not None and not isinstance(commands, list):
            errors.append("last_validation.commands must be a list")

    next_action = packet.get("next_action")
    if not isinstance(next_action, dict):
        errors.append("next_action must be an object")
    else:
        if not isinstance(next_action.get("requested"), str) or not next_action.get("requested", "").strip():
            errors.append("next_action.requested must be a non-empty string")
        if next_action.get("destructive") is True and next_action.get("requires_confirmation") is not True:
            errors.append("destructive next_action requires requires_confirmation=true")

    return errors, warnings


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# ChatGPT / Local AI Handoff Packet Validation", ""]
    for key in [
        "passed",
        "packet",
        "repository",
        "branch",
        "objective_present",
        "evidence_count",
        "error_count",
        "warning_count",
    ]:
        lines.append(f"- `{key}`: `{report.get(key)}`")
    if report.get("errors"):
        lines.extend(["", "## Errors"])
        for error in report["errors"]:
            lines.append(f"- {error}")
    if report.get("warnings"):
        lines.extend(["", "## Warnings"])
        for warning in report["warnings"]:
            lines.append(f"- {warning}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--packet", default=None)
    parser.add_argument("--write-template", default=None)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()

    if args.write_template:
        template_path = resolve_path(repo_root, args.write_template)
        write_json(template_path, default_template())
        print(json.dumps({"written": str(template_path), "kind": DEFAULT_KIND}, indent=2, ensure_ascii=False))
        return 0

    if not args.packet:
        raise SystemExit("--packet is required unless --write-template is used")

    packet_path = resolve_path(repo_root, args.packet)
    packet = read_json(packet_path)
    errors, warnings = validate_packet(packet, repo_root)
    evidence = packet.get("evidence") if isinstance(packet.get("evidence"), list) else []
    report = {
        "schema_version": 1,
        "kind": "chatgpt_local_ai_handoff_packet_validation",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "packet": str(packet_path),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "sqlite_write_performed": False,
        "persistent_memory_write_performed": False,
        "repository": packet.get("repository"),
        "branch": packet.get("branch"),
        "objective_present": bool(str(packet.get("objective") or "").strip()),
        "evidence_count": len(evidence),
        "guardrails": packet.get("guardrails", {}),
        "decision": {
            "ready_for_chatgpt_handoff": not errors,
            "manual_review_required": True,
        },
    }

    output = resolve_path(repo_root, args.output)
    markdown_output = resolve_path(repo_root, args.markdown_output)
    write_json(output, report)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.write_text(render_markdown(report), encoding="utf-8")

    print(json.dumps({
        "passed": report["passed"],
        "output": str(output),
        "markdown": str(markdown_output),
        "error_count": report["error_count"],
        "warning_count": report["warning_count"],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "sqlite_write_performed": False,
        "persistent_memory_write_performed": False,
    }, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
