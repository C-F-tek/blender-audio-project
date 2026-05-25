"""Tool loop orchestration for the Ollama gateway."""

from __future__ import annotations

import json
from typing import Any

from .client import extract_json_object, ollama_chat, system_prompt
from .common import GatewayConfig, now_stamp, repo_rel
from .files import file_search, read_text_file
from .repo_tools import build_context_pack, memory_remember_operational, memory_search

def execute_tool(config: GatewayConfig, request: dict[str, Any]) -> dict[str, Any]:
    tool = str(request.get("tool") or "").strip()
    args = request.get("arguments") if isinstance(request.get("arguments"), dict) else {}
    try:
        if tool == "file_read":
            return read_text_file(config, str(args.get("path") or ""))
        if tool == "file_search":
            roots = args.get("roots") if isinstance(args.get("roots"), list) else []
            return file_search(config, str(args.get("query") or ""), [str(item) for item in roots])
        if tool == "memory_search":
            return memory_search(
                config,
                str(args.get("query") or ""),
                str(args.get("scope") or "operational"),
                int(args.get("limit") or 10),
            )
        if tool == "memory_remember_operational":
            tags = args.get("tags") if isinstance(args.get("tags"), list) else []
            return memory_remember_operational(
                config,
                str(args.get("summary") or ""),
                str(args.get("content") or ""),
                [str(item) for item in tags],
            )
        if tool == "build_context_pack":
            profile = str(args.get("profile") or "").strip()
            if not profile:
                return {"passed": False, "error": "context_pack_profile_explicit_required"}
            return build_context_pack(config, profile)
        return {"passed": False, "error": f"tool not allowlisted: {tool}"}
    except Exception as exc:  # noqa: BLE001 - report result for model loop.
        return {"passed": False, "error": f"{type(exc).__name__}: {exc}"}

def run_loop(config: GatewayConfig, task: str) -> dict[str, Any]:
    messages: list[dict[str, str]] = [
        {"role": "system", "content": system_prompt()},
        {"role": "user", "content": task},
    ]
    events: list[dict[str, Any]] = []
    final_answer = ""
    for round_index in range(1, config.max_rounds + 1):
        content = ollama_chat(config, messages)
        data = extract_json_object(content)
        events.append({"round": round_index, "model_raw": content, "parsed": data})
        if not data:
            final_answer = content
            break
        if data.get("type") == "final":
            final_answer = str(data.get("answer") or "")
            break
        if data.get("type") != "tool_request":
            final_answer = json.dumps(data, indent=2, ensure_ascii=False)
            break
        tool_result = execute_tool(config, data)
        events[-1]["tool_result"] = tool_result
        messages.append({"role": "assistant", "content": json.dumps(data, ensure_ascii=False)})
        messages.append(
            {
                "role": "user",
                "content": "TOOL_RESULT:\n" + json.dumps(tool_result, ensure_ascii=False),
            }
        )
    else:
        final_answer = "Max tool rounds reached before final answer."
    return {
        "schema_version": 1,
        "kind": "ollama_tool_gateway_run",
        "passed": bool(final_answer),
        "model": config.model,
        "task": task,
        "events": events,
        "final_answer": final_answer,
    }

def write_outputs(config: GatewayConfig, report: dict[str, Any]) -> dict[str, str]:
    config.output_dir.mkdir(parents=True, exist_ok=True)
    stamp = now_stamp()
    json_path = config.output_dir / f"ollama_tool_gateway_{stamp}.json"
    md_path = config.output_dir / f"ollama_tool_gateway_{stamp}.md"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(
        "# Ollama Tool Gateway\n\n" + report.get("final_answer", "") + "\n",
        encoding="utf-8",
    )
    return {
        "json": repo_rel(json_path, config.repo_root),
        "markdown": repo_rel(md_path, config.repo_root),
    }
