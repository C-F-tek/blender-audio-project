"""Concrete read-only workstation tools for brokered GPU1 native calls."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from ia_carmine._shared.file_backed_transport import write_text_artifact
from ia_carmine.runtime.runtime_tool.broker.common import now_iso, repo_rel
from ia_carmine.runtime.runtime_tool.broker.search_window_refs import (
    attach_broker_report_metadata,
    attach_runtime_file_window_search_refs,
    source_broker_request_id as broker_request_source_id,
)

MAX_RESULT_CHARS = 64000
DEFAULT_TIMEOUT_SECONDS = 45


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--tool", required=True)
    parser.add_argument("--args-file", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    parser.add_argument("--timeout-seconds", default=str(DEFAULT_TIMEOUT_SECONDS))
    ns = parser.parse_args(argv)

    repo_root = Path(ns.repo_root).resolve(strict=False)
    args_path = _safe_path(repo_root, ns.args_file)
    tool_args = _read_json(args_path)
    timeout = _positive_int(tool_args.get("timeout_seconds"), _positive_int(ns.timeout_seconds, DEFAULT_TIMEOUT_SECONDS))

    try:
        report = _run_tool(repo_root, str(ns.tool), tool_args, timeout_seconds=timeout)
    except Exception as exc:  # noqa: BLE001
        report = {
            "schema_version": 1,
            "kind": str(ns.tool),
            "generated_at": now_iso(),
            "passed": False,
            "errors": [f"{type(exc).__name__}: {exc}"],
            "warnings": [],
        }

    output = _safe_output_path(repo_root, ns.output)
    markdown = _safe_output_path(repo_root, ns.markdown_output)
    attach_broker_report_metadata(repo_root, report, tool_args, output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    markdown.write_text(_render_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": report.get("passed"), "kind": report.get("kind")}, ensure_ascii=False))
    return 0 if report.get("passed") is not False else 2


def _run_tool(repo_root: Path, tool: str, args: dict[str, Any], *, timeout_seconds: int) -> dict[str, Any]:
    if tool == "repo_toolchain_probe":
        return _toolchain_probe(repo_root, args, timeout_seconds=timeout_seconds)
    if tool == "repo_toolchain_command":
        return _toolchain_command(repo_root, args, timeout_seconds=timeout_seconds)
    if tool == "repo_search_rg":
        return _repo_search_rg(repo_root, args, timeout_seconds=timeout_seconds)
    if tool == "repo_search_git_grep":
        return _repo_search_git_grep(repo_root, args, timeout_seconds=timeout_seconds)
    if tool == "repo_find_fd":
        return _repo_find_fd(repo_root, args, timeout_seconds=timeout_seconds)
    if tool == "repo_json_query_jq":
        return _repo_json_query_jq(repo_root, args, timeout_seconds=timeout_seconds)
    if tool == "repo_powershell_readonly":
        return _repo_powershell_readonly(repo_root, args, timeout_seconds=timeout_seconds)
    return {
        "schema_version": 1,
        "kind": tool,
        "generated_at": now_iso(),
        "passed": False,
        "errors": [f"unsupported concrete tool: {tool}"],
        "warnings": [],
    }


def _toolchain_probe(repo_root: Path, args: dict[str, Any], *, timeout_seconds: int) -> dict[str, Any]:
    requested = _split(args.get("tool") or args.get("tools")) or [
        "rg",
        "fd",
        "jq",
        "powershell",
        "pwsh",
        "dotnet",
        "msbuild.exe",
        "msbuild",
        "ninja",
        "code",
    ]
    tools: list[dict[str, Any]] = []
    for name in requested:
        exe = shutil.which(name)
        item: dict[str, Any] = {"name": name, "available": bool(exe), "path": exe or ""}
        if exe:
            version = _run_version(name, repo_root, timeout_seconds=timeout_seconds)
            item.update(version)
        tools.append(item)
    return _base_report(
        "repo_toolchain_probe",
        passed=True,
        command=[],
        stdout="\n".join(
            f"{item['name']}: {'available' if item['available'] else 'missing'} {item.get('path') or ''}"
            for item in tools
        ),
        stderr="",
        returncode=0,
        extra={
            "tools": tools,
            "available_tools": [item["name"] for item in tools if item.get("available")],
            "missing_tools": [item["name"] for item in tools if not item.get("available")],
        },
    )


def _toolchain_command(repo_root: Path, args: dict[str, Any], *, timeout_seconds: int) -> dict[str, Any]:
    command_name = str(args.get("command") or "").strip().lower()
    target = str(args.get("path") or args.get("target") or ".").strip() or "."
    target_path = _safe_path(repo_root, target)
    configuration = str(args.get("configuration") or "").strip()
    allowed = {
        "dotnet_info",
        "dotnet_build",
        "dotnet_test",
        "msbuild_version",
        "ninja_version",
        "ninja_build",
        "code_version",
    }
    if command_name not in allowed:
        return _invalid(
            "repo_toolchain_command",
            "command must be one of: " + ", ".join(sorted(allowed)),
        )
    if command_name == "dotnet_info":
        command = [_required_exe("dotnet"), "--info"]
    elif command_name == "dotnet_build":
        command = [_required_exe("dotnet"), "build", str(target_path), "--nologo"]
    elif command_name == "dotnet_test":
        command = [_required_exe("dotnet"), "test", str(target_path), "--nologo", "--no-restore"]
    elif command_name == "msbuild_version":
        command = [
            _required_exe("msbuild.exe") if shutil.which("msbuild.exe") else _required_exe("msbuild"),
            "-version",
        ]
    elif command_name == "ninja_version":
        command = [_required_exe("ninja"), "--version"]
    elif command_name == "ninja_build":
        command = [_required_exe("ninja"), "-C", str(target_path)]
    else:
        command = [_required_exe("code"), "--version"]
    if command_name == "dotnet_build" and configuration:
        command.extend(["--configuration", configuration])
    result = _run(command, repo_root, timeout_seconds=timeout_seconds)
    return _base_report(
        "repo_toolchain_command",
        passed=result.returncode == 0,
        command=command,
        stdout=result.stdout,
        stderr=result.stderr,
        returncode=result.returncode,
        extra={"toolchain_command": command_name, "path": repo_rel(target_path, repo_root)},
    )


def _repo_search_rg(repo_root: Path, args: dict[str, Any], *, timeout_seconds: int) -> dict[str, Any]:
    exe = _required_exe("rg")
    query = str(args.get("query") or args.get("pattern") or "").strip()
    if not query:
        return _invalid("repo_search_rg", "query is required")
    paths = [_safe_path(repo_root, value) for value in (_split(args.get("path")) or ["."])]
    command = [exe, "--line-number", "--column", "--no-heading", "--color", "never"]
    if _truthy(args.get("ignore_case")):
        command.append("--ignore-case")
    if _truthy(args.get("fixed_strings")):
        command.append("--fixed-strings")
    if _truthy(args.get("hidden")):
        command.append("--hidden")
    if args.get("context") is not None:
        command.extend(["--context", str(_positive_int(args.get("context"), 0))])
    max_count = _positive_int(args.get("max_count"), 0)
    if max_count:
        command.extend(["--max-count", str(max_count)])
    for glob in _split(args.get("glob")):
        command.extend(["--glob", glob])
    command.append(query)
    command.extend(repo_rel(path, repo_root) for path in paths)
    result = _run(command, repo_root, timeout_seconds=timeout_seconds)
    passed = result.returncode in {0, 1}
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    max_results = _positive_int(args.get("max_results"), 200)
    clipped = lines[:max_results]
    matches = _rg_matches(repo_root, clipped)
    source_broker_request_id = broker_request_source_id(args)
    authorized_refs = attach_runtime_file_window_search_refs(
        "repo_search_rg", matches, source_broker_request_id
    )
    return _base_report(
        "repo_search_rg",
        passed=passed,
        command=command,
        stdout="\n".join(clipped),
        stderr=result.stderr,
        returncode=result.returncode,
        extra={
            "match_count": len(lines),
            "returned_match_count": len(clipped),
            "query": query,
            "source_broker_request_id": source_broker_request_id,
            "matches": matches,
            "runtime_file_window_authorized_refs": authorized_refs,
        },
    )


def _repo_search_git_grep(repo_root: Path, args: dict[str, Any], *, timeout_seconds: int) -> dict[str, Any]:
    exe = _required_exe("git")
    query = str(args.get("query") or args.get("pattern") or "").strip()
    if not query:
        return _invalid("repo_search_git_grep", "query is required")
    paths = [repo_rel(_safe_path(repo_root, value), repo_root) for value in (_split(args.get("path")) or ["."])]
    command = [exe, "grep", "-n", "--no-color"]
    if _truthy(args.get("ignore_case")):
        command.append("-i")
    if _truthy(args.get("fixed_strings"), default=True):
        command.append("-F")
    command.extend(["--", query])
    command.extend(paths)
    result = _run(command, repo_root, timeout_seconds=timeout_seconds)
    passed = result.returncode in {0, 1}
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    max_results = _positive_int(args.get("max_results"), 200)
    clipped = lines[:max_results]
    matches = _git_grep_matches(repo_root, clipped)
    source_broker_request_id = broker_request_source_id(args)
    authorized_refs = attach_runtime_file_window_search_refs(
        "repo_search_git_grep", matches, source_broker_request_id
    )
    return _base_report(
        "repo_search_git_grep",
        passed=passed,
        command=command,
        stdout="\n".join(clipped),
        stderr=result.stderr,
        returncode=result.returncode,
        extra={
            "match_count": len(lines),
            "returned_match_count": len(clipped),
            "query": query,
            "source_broker_request_id": source_broker_request_id,
            "matches": matches,
            "runtime_file_window_authorized_refs": authorized_refs,
        },
    )


def _repo_find_fd(repo_root: Path, args: dict[str, Any], *, timeout_seconds: int) -> dict[str, Any]:
    exe = _required_exe("fd")
    pattern = str(args.get("pattern") or args.get("query") or ".").strip() or "."
    path = _safe_path(repo_root, str(args.get("path") or "."))
    command = [exe, "--color", "never", "--type", "f"]
    if _truthy(args.get("hidden")):
        command.append("--hidden")
    for extension in _split(args.get("extension")):
        command.extend(["--extension", extension.lstrip(".")])
    command.extend([pattern, repo_rel(path, repo_root)])
    result = _run(command, repo_root, timeout_seconds=timeout_seconds)
    passed = result.returncode in {0, 1}
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    max_results = _positive_int(args.get("max_results"), 250)
    clipped = lines[:max_results]
    matches = _fd_matches(repo_root, clipped)
    source_broker_request_id = broker_request_source_id(args)
    authorized_refs = attach_runtime_file_window_search_refs(
        "repo_find_fd", matches, source_broker_request_id
    )
    return _base_report(
        "repo_find_fd",
        passed=passed,
        command=command,
        stdout="\n".join(clipped),
        stderr=result.stderr,
        returncode=result.returncode,
        extra={
            "match_count": len(lines),
            "returned_match_count": len(clipped),
            "pattern": pattern,
            "source_broker_request_id": source_broker_request_id,
            "matches": matches,
            "runtime_file_window_authorized_refs": authorized_refs,
        },
    )


def _repo_json_query_jq(repo_root: Path, args: dict[str, Any], *, timeout_seconds: int) -> dict[str, Any]:
    exe = _required_exe("jq")
    path = _safe_path(repo_root, str(args.get("path") or ""))
    query = str(args.get("filter") or args.get("query") or ".").strip() or "."
    command = [exe, query, str(path)]
    result = _run(command, repo_root, timeout_seconds=timeout_seconds)
    matches = _jq_matches(repo_root, path, result.stdout)
    source_broker_request_id = broker_request_source_id(args)
    authorized_refs = attach_runtime_file_window_search_refs(
        "repo_json_query_jq", matches, source_broker_request_id
    )
    return _base_report(
        "repo_json_query_jq",
        passed=result.returncode == 0,
        command=command,
        stdout=result.stdout,
        stderr=result.stderr,
        returncode=result.returncode,
        extra={
            "path": repo_rel(path, repo_root),
            "filter": query,
            "source_broker_request_id": source_broker_request_id,
            "matches": matches,
            "runtime_file_window_authorized_refs": authorized_refs,
        },
    )


def _repo_powershell_readonly(repo_root: Path, args: dict[str, Any], *, timeout_seconds: int) -> dict[str, Any]:
    exe = shutil.which("pwsh") or shutil.which("powershell")
    if not exe:
        raise FileNotFoundError("pwsh/powershell not found")
    operation = str(args.get("operation") or "get_child_item").strip().lower()
    path = _safe_path(repo_root, str(args.get("path") or "."))
    limit = _positive_int(args.get("max_results"), 200)
    if operation == "select_string":
        pattern = str(args.get("pattern") or "").strip()
        if not pattern:
            return _invalid("repo_powershell_readonly", "pattern is required for select_string")
        file_filter = str(args.get("filter") or "*").strip() or "*"
        recurse = "$true" if _truthy(args.get("recurse"), default=True) else "$false"
        simple = "$true" if _truthy(args.get("simple_match"), default=True) else "$false"
        script = (
            "$ErrorActionPreference='Stop';"
            f"$files=Get-ChildItem -LiteralPath {_ps(path)} -File -Force -Recurse:{recurse} -Filter {_ps(file_filter)};"
            f"$files|Select-String -Pattern {_ps(pattern)} -SimpleMatch:{simple}|"
            f"Select-Object -First {limit} Path,LineNumber,Line|ConvertTo-Json -Depth 4"
        )
    else:
        file_filter = str(args.get("filter") or "*").strip() or "*"
        recurse = "$true" if _truthy(args.get("recurse"), default=True) else "$false"
        script = (
            "$ErrorActionPreference='Stop';"
            f"Get-ChildItem -LiteralPath {_ps(path)} -File -Force -Recurse:{recurse} -Filter {_ps(file_filter)}|"
            f"Select-Object -First {limit} FullName,Length,LastWriteTime|ConvertTo-Json -Depth 4"
        )
    command = [exe, "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script]
    result = _run(command, repo_root, timeout_seconds=timeout_seconds)
    return _base_report(
        "repo_powershell_readonly",
        passed=result.returncode == 0,
        command=[exe, "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", "<readonly script>"],
        stdout=result.stdout,
        stderr=result.stderr,
        returncode=result.returncode,
        extra={"operation": operation, "path": repo_rel(path, repo_root)},
    )


def _base_report(
    kind: str,
    *,
    passed: bool,
    command: list[str],
    stdout: str,
    stderr: str,
    returncode: int,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    stdout = stdout or ""
    stderr = stderr or ""
    report: dict[str, Any] = {
        "schema_version": 1,
        "kind": kind,
        "generated_at": now_iso(),
        "passed": bool(passed),
        "returncode": returncode,
        "command": command,
        "result_text": stdout[:MAX_RESULT_CHARS],
        "result_text_chars": len(stdout),
        "stderr_tail": stderr[-8000:],
        "errors": [] if passed else [f"{kind} returned {returncode}"],
        "warnings": [],
        "guardrails": {
            "source_writes_performed": False,
            "patch_application_performed": False,
            "git_write_performed": False,
            "read_only_command_tool": True,
        },
    }
    report.update(extra or {})
    return report


def _rg_matches(repo_root: Path, lines: list[str]) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for line in lines:
        parts = line.split(":", 3)
        if len(parts) < 4:
            continue
        rel = _repo_relative_or_value(repo_root, parts[0])
        try:
            line_number = int(parts[1])
            column = int(parts[2])
        except ValueError:
            continue
        snippet = parts[3][:500]
        matches.append(
            {
                "path": rel,
                "repo_relative": rel,
                "line": line_number,
                "column": column,
                "match": snippet,
                "snippet": snippet,
            }
        )
    return matches


def _git_grep_matches(repo_root: Path, lines: list[str]) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for line in lines:
        parts = line.split(":", 2)
        if len(parts) < 3:
            continue
        rel = _repo_relative_or_value(repo_root, parts[0])
        try:
            line_number = int(parts[1])
        except ValueError:
            continue
        snippet = parts[2][:500]
        matches.append(
            {
                "path": rel,
                "repo_relative": rel,
                "line": line_number,
                "column": None,
                "match": snippet,
                "snippet": snippet,
            }
        )
    return matches


def _fd_matches(repo_root: Path, lines: list[str]) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for line in lines:
        rel = _repo_relative_or_value(repo_root, line.strip())
        if not rel:
            continue
        matches.append(
            {
                "path": rel,
                "repo_relative": rel,
                "line": None,
                "match": rel,
                "snippet": rel,
            }
        )
    return matches


def _jq_matches(repo_root: Path, path: Path, stdout: str) -> list[dict[str, Any]]:
    text = (stdout or "").strip()
    rel = repo_rel(path, repo_root)
    if not text:
        return []
    return [
        {
            "path": rel,
            "repo_relative": rel,
            "line": None,
            "match": text[:500],
            "snippet": text[:500],
        }
    ]


def _repo_relative_or_value(repo_root: Path, value: str) -> str:
    if not value:
        return ""
    path = Path(value)
    if not path.is_absolute():
        return value.replace("\\", "/")
    return repo_rel(path, repo_root)


def _invalid(kind: str, error: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "kind": kind,
        "generated_at": now_iso(),
        "passed": False,
        "returncode": 2,
        "errors": [error],
        "warnings": [],
    }


def _render_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# {report.get('kind')}",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Return code: `{report.get('returncode')}`",
        f"- Errors: `{report.get('errors') or []}`",
        "",
        "## Result",
        "",
        "```text",
        str(report.get("result_text") or "")[:20000],
        "```",
    ]
    stderr = str(report.get("stderr_tail") or "").strip()
    if stderr:
        lines.extend(["", "## Stderr", "", "```text", stderr, "```"])
    return "\n".join(lines)


def _run(command: list[str], repo_root: Path, *, timeout_seconds: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=repo_root,
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        encoding="utf-8",
        errors="replace",
    )


def _run_version(name: str, repo_root: Path, *, timeout_seconds: int) -> dict[str, Any]:
    version_args = {
        "rg": ["--version"],
        "fd": ["--version"],
        "jq": ["--version"],
        "dotnet": ["--info"],
        "msbuild.exe": ["-version"],
        "msbuild": ["-version"],
        "ninja": ["--version"],
        "code": ["--version"],
        "powershell": ["-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"],
        "pwsh": ["-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"],
    }.get(name, ["--version"])
    try:
        result = _run([name, *version_args], repo_root, timeout_seconds=timeout_seconds)
    except Exception as exc:  # noqa: BLE001
        return {"version_returncode": 1, "version_error": f"{type(exc).__name__}: {exc}"}
    return {
        "version_returncode": result.returncode,
        "version_text": (result.stdout or result.stderr or "").strip()[:2000],
    }


def _required_exe(name: str) -> str:
    exe = shutil.which(name)
    if not exe:
        raise FileNotFoundError(f"{name} not found in PATH")
    return exe


def _safe_path(repo_root: Path, value: str | Path) -> Path:
    if not str(value or "").strip():
        raise ValueError("path is required")
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    resolved = path.resolve(strict=False)
    root = repo_root.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path outside repo is not allowed: {value}") from exc
    return resolved


def _safe_output_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve(strict=False)


def _read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return data if isinstance(data, dict) else {}


def _split(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        items = value
    else:
        items = str(value).split(",")
    return [str(item).strip().strip("'\"") for item in items if str(item).strip()]


def _truthy(value: Any, *, default: bool = False) -> bool:
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def _positive_int(value: Any, default: int) -> int:
    try:
        parsed = int(float(str(value)))
    except Exception:
        return default
    return parsed if parsed > 0 else default


def _ps(value: Any) -> str:
    return "'" + str(value).replace("'", "''") + "'"


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
