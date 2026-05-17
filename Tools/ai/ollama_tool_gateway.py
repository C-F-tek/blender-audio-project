#!/usr/bin/env python3
"""Local Ollama tool gateway for IA-Carmine.

The gateway wraps Ollama as a text/reasoning provider and keeps tool execution
inside deterministic Python code. It gives a model controlled access to:

- repository file search/read;
- operational or persistent SQLite memory search;
- operational SQLite memory remember;
- existing request/context-pack builders through safe subprocess calls.

Guardrails:
- no source writes;
- no Git writes;
- no patch application;
- no Blender/FFmpeg runtime;
- no free shell;
- no reading secrets or generated heavy trees by default.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_MODEL = "qwen3.5:cloud"
DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_OUTPUT_DIR = "output/ollama_tool_gateway"
MAX_FILE_CHARS = 12000
MAX_SEARCH_RESULTS = 20

DENY_PREFIXES = (
    ".git/",
    ".venv/",
    "venv/",
    "output/",
    "renders/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
    "__pycache__/",
)
DENY_EXACT = {
    ".claude/settings.local.json",
    ".env",
}
DENY_FRAGMENTS = (
    "secret",
    "token",
    "password",
    "credential",
    "full_analysis",
    "analysis_full",
    ".sqlite",
    ".db",
)
TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".py",
    ".ps1",
    ".sh",
    ".json",
    ".jsonl",
    ".yaml",
    ".yml",
    ".csv",
    ".toml",
}


@dataclass(frozen=True)
class GatewayConfig:
    repo_root: Path
    model: str
    ollama_url: str
    output_dir: Path
    max_rounds: int
    max_file_chars: int
    max_search_results: int
    allow_output_read: bool


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def resolve_repo_path(repo_root: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve(strict=False)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(parent.resolve(strict=False))
        return True
    except ValueError:
        return False


def path_policy_error(rel_path: str, *, allow_output_read: bool = False) -> str:
    normalized = rel_path.replace("\\", "/").strip()
    lower = normalized.lower()
    if not normalized:
        return "empty path"
    if Path(normalized).is_absolute():
        return "absolute paths are not allowed"
    if normalized in DENY_EXACT:
        return "path is explicitly denied"
    prefixes = (
        DENY_PREFIXES
        if not allow_output_read
        else tuple(p for p in DENY_PREFIXES if p != "output/")
    )
    if any(lower.startswith(prefix.lower()) for prefix in prefixes):
        return "path prefix is denied"
    if any(fragment in lower for fragment in DENY_FRAGMENTS):
        return "path fragment is denied"
    return ""


def compact_text(text: str, max_chars: int) -> tuple[str, bool]:
    if len(text) <= max_chars:
        return text, False
    return text[:max_chars] + "\n...[truncated]", True


def read_text_file(config: GatewayConfig, raw_path: str) -> dict[str, Any]:
    rel_input = raw_path.replace("\\", "/").strip()
    error = path_policy_error(rel_input, allow_output_read=config.allow_output_read)
    path = resolve_repo_path(config.repo_root, rel_input)
    if error:
        return {"passed": False, "path": rel_input, "error": error}
    if not is_under(path, config.repo_root):
        return {"passed": False, "path": rel_input, "error": "path escapes repo root"}
    if not path.is_file():
        return {
            "passed": False,
            "path": rel_input,
            "error": "file missing or not a file",
        }
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return {
            "passed": False,
            "path": repo_rel(path, config.repo_root),
            "error": "extension not allowed",
        }
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError as exc:
        return {
            "passed": False,
            "path": repo_rel(path, config.repo_root),
            "error": f"{type(exc).__name__}: {exc}",
        }
    preview, truncated = compact_text(text, config.max_file_chars)
    return {
        "passed": True,
        "path": repo_rel(path, config.repo_root),
        "chars": len(text),
        "lines": len(text.splitlines()),
        "truncated": truncated,
        "content": preview,
    }


def iter_candidate_files(config: GatewayConfig, roots: list[str]) -> list[Path]:
    found: list[Path] = []
    seen: set[Path] = set()
    selected_roots = roots or [
        "docs",
        "Tools/ai",
        "Tools/validation",
        "Tools/workflow",
        "AGENTS.md",
        "README.md",
    ]
    for raw_root in selected_roots:
        root_rel = raw_root.replace("\\", "/").strip()
        if path_policy_error(root_rel, allow_output_read=config.allow_output_read):
            continue
        root = resolve_repo_path(config.repo_root, root_rel)
        if not is_under(root, config.repo_root) or not root.exists():
            continue
        candidates = [root] if root.is_file() else sorted(p for p in root.rglob("*") if p.is_file())
        for path in candidates:
            rel = repo_rel(path, config.repo_root)
            if path in seen:
                continue
            if path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            if path_policy_error(rel, allow_output_read=config.allow_output_read):
                continue
            seen.add(path)
            found.append(path)
    return found


def file_search(config: GatewayConfig, query: str, roots: list[str]) -> dict[str, Any]:
    terms = [item.lower() for item in query.split() if item.strip()]
    if not terms:
        return {"passed": False, "error": "query is required", "results": []}
    results: list[dict[str, Any]] = []
    for path in iter_candidate_files(config, roots):
        rel = repo_rel(path, config.repo_root)
        haystack = rel.lower()
        try:
            text = path.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        body = text.lower()
        score = sum(3 for term in terms if term in haystack) + sum(
            1 for term in terms if term in body
        )
        if score <= 0:
            continue
        first_line = ""
        for line in text.splitlines():
            if any(term in line.lower() for term in terms):
                first_line = line.strip()[:240]
                break
        results.append(
            {
                "path": rel,
                "score": score,
                "lines": len(text.splitlines()),
                "match_preview": first_line,
            }
        )
    results.sort(key=lambda item: (-int(item["score"]), str(item["path"])))
    return {
        "passed": True,
        "query": query,
        "results": results[: config.max_search_results],
        "result_count": len(results),
    }


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
            "Tools/ai/agent_runtime_sqlite_memory.py",
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
        "Tools/ai/agent_runtime_sqlite_memory.py",
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
            "Tools/ai/build_ai_context_pack.py",
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
            return build_context_pack(config, str(args.get("profile") or "core_ai_backend"))
        return {"passed": False, "error": f"tool not allowlisted: {tool}"}
    except Exception as exc:  # noqa: BLE001 - report result for model loop.
        return {"passed": False, "error": f"{type(exc).__name__}: {exc}"}


def extract_json_object(text: str) -> dict[str, Any] | None:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.strip("`").strip()
        if stripped.lower().startswith("json"):
            stripped = stripped[4:].strip()
    try:
        data = json.loads(stripped)
        return data if isinstance(data, dict) else None
    except json.JSONDecodeError:
        pass
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start >= 0 and end > start:
        try:
            data = json.loads(stripped[start : end + 1])
            return data if isinstance(data, dict) else None
        except json.JSONDecodeError:
            return None
    return None


def ollama_chat(config: GatewayConfig, messages: list[dict[str, str]]) -> str:
    payload = {
        "model": config.model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.2},
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        config.ollama_url.rstrip("/") + "/api/chat",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=240) as response:  # noqa: S310 - local/operator configured endpoint.
            raw = response.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Ollama request failed: {exc}") from exc
    parsed = json.loads(raw)
    return str((parsed.get("message") or {}).get("content") or parsed.get("response") or "")


def system_prompt() -> str:
    return """You are IA-Carmine local tool gateway planner.
Use tools when project memory or files are needed. Answer ONLY valid JSON.

Allowed tool request:
{"type":"tool_request","tool":"file_search","arguments":{"query":"...","roots":["Tools/ai","docs"]}}
{"type":"tool_request","tool":"file_read","arguments":{"path":"Tools/ai/example.py"}}
{"type":"tool_request","tool":"memory_search","arguments":{"query":"...","scope":"operational","limit":10}}
{"type":"tool_request","tool":"memory_remember_operational","arguments":{"summary":"...","content":"...","tags":["..."]}}
{"type":"tool_request","tool":"build_context_pack","arguments":{"profile":"core_ai_backend"}}

Final answer:
{"type":"final","answer":"..."}

Never invent file content. Ask file_search/file_read when needed. Do not request writes, git, shell, delete, patch apply, Blender or secrets."""


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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a safe Ollama tool loop over IA-Carmine memory and files."
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--model", default=os.environ.get("OLLAMA_TOOL_GATEWAY_MODEL", DEFAULT_MODEL)
    )
    parser.add_argument(
        "--ollama-url", default=os.environ.get("OLLAMA_HOST_URL", DEFAULT_OLLAMA_URL)
    )
    parser.add_argument("--task", required=True)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-rounds", type=int, default=6)
    parser.add_argument("--max-file-chars", type=int, default=MAX_FILE_CHARS)
    parser.add_argument("--max-search-results", type=int, default=MAX_SEARCH_RESULTS)
    parser.add_argument("--allow-output-read", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    config = GatewayConfig(
        repo_root=repo_root,
        model=args.model,
        ollama_url=args.ollama_url,
        output_dir=resolve_repo_path(repo_root, args.output_dir),
        max_rounds=max(1, args.max_rounds),
        max_file_chars=max(1000, args.max_file_chars),
        max_search_results=max(1, args.max_search_results),
        allow_output_read=args.allow_output_read,
    )
    report = run_loop(config, args.task)
    outputs = write_outputs(config, report)
    print(
        json.dumps(
            {
                "passed": report["passed"],
                "model": config.model,
                "outputs": outputs,
                "final_answer": report["final_answer"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
