"""Brokered repository tools exposed to the Ollama gateway."""

from __future__ import annotations

import json
import subprocess
import sys
from typing import Any

from .common import GatewayConfig, now_stamp, repo_rel

def run_repo_tool(config: GatewayConfig, args: list[str], output_name: str) -> dict[str, Any]:
    output_json = config.output_dir / f"{output_name}.json"
    output_md = config.output_dir / f"{output_name}.md"
    cmd = [sys.executable, *args, "--repo-root", ".", "--output", str(output_json)]
    if "--markdown-output" not in args:
        cmd.extend(["--markdown-output", str(output_md)])
    proc = subprocess.run(cmd, cwd=config.repo_root, text=True, capture_output=True, timeout=120)
    result: dict[str, Any] = {
        "passed": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-2000:],
        "stderr_tail": proc.stderr[-2000:],
        "output": repo_rel(output_json, config.repo_root),
        "markdown_output": repo_rel(output_md, config.repo_root),
    }
    if output_json.exists():
        try:
            data = json.loads(output_json.read_text(encoding="utf-8-sig", errors="replace"))
            result["report_summary"] = {
                key: data.get(key) for key in ("kind", "passed", "errors", "warnings", "result")
            }
        except json.JSONDecodeError as exc:
            result["json_error"] = str(exc)
    return result

def memory_search(config: GatewayConfig, query: str, scope: str, limit: int) -> dict[str, Any]:
    scope = scope if scope in {"operational", "persistent"} else "operational"
    return run_repo_tool(
        config,
        [
            "-m", "ia_carmine.memory.agent_memory.sqlite_cli",
            "--action",
            "search",
            "--scope",
            scope,
            "--query",
            query,
            "--limit",
            str(max(1, min(limit, 50))),
        ],
        f"memory_search_{scope}_{now_stamp()}",
    )

def memory_remember_operational(
    config: GatewayConfig, summary: str, content: str, tags: list[str]
) -> dict[str, Any]:
    cmd = [
        "-m", "ia_carmine.memory.agent_memory.sqlite_cli",
        "--action",
        "remember",
        "--scope",
        "operational",
        "--summary",
        summary[:500],
        "--content",
        content[:8000],
        "--role",
        "ollama_tool_gateway",
    ]
    for tag in tags[:10]:
        cmd.extend(["--tag", tag])
    return run_repo_tool(config, cmd, f"memory_remember_operational_{now_stamp()}")

def build_context_pack(config: GatewayConfig, profile: str) -> dict[str, Any]:
    basename = f"ollama_gateway_context_{now_stamp()}"
    return run_repo_tool(
        config,
        [
            "-m", "ia_carmine.context.agent_context.ai_context_pack.cli",
            "--profile",
            profile or "core_ai_backend",
            "--basename",
            basename,
            "--output-dir",
            str(config.output_dir / basename),
            "--evidence-dir",
            str(config.output_dir / f"{basename}_evidence"),
            "--evidence-basename",
            f"{basename}_evidence",
        ],
        f"context_pack_{now_stamp()}",
    )
