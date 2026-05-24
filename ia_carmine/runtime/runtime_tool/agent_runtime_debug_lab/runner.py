"""Execution engine for the report-only agent runtime debug lab."""

from __future__ import annotations

import json
import hashlib
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from ia_carmine._shared.file_backed_transport import write_text_artifact

from .policy import (
    ALLOWED_OPERATION_TYPES,
    FORBIDDEN_OPERATION_TYPES,
    as_list,
    operation_timeout,
    validate_output_path,
    validate_python_script,
    validate_request,
    validate_source_path,
    validate_string_args,
)


def tail(text: str, limit: int) -> str:
    return text[-limit:] if len(text) > limit else text


def command_io_refs(cwd: Path, command: list[str], stdout: str, stderr: str) -> dict[str, Any]:
    digest = hashlib.sha256(json.dumps(command, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]
    io_dir = cwd / "output" / "validation" / "agent_runtime_debug_lab_io"
    stdout_ref = write_text_artifact(
        cwd,
        io_dir,
        name=f"{digest}_stdout",
        text=stdout,
        kind="debug_lab_stdout",
        producer="agent_runtime_debug_lab",
    )
    stderr_ref = write_text_artifact(
        cwd,
        io_dir,
        name=f"{digest}_stderr",
        text=stderr,
        kind="debug_lab_stderr",
        producer="agent_runtime_debug_lab",
    )
    return {
        "stdout_ref": stdout_ref,
        "stderr_ref": stderr_ref,
        "stdout_chars": len(stdout),
        "stderr_chars": len(stderr),
    }


def run_command(command: list[str], cwd: Path, timeout: int, tail_chars: int) -> dict[str, Any]:
    started = time.monotonic()
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
        stdout = result.stdout or ""
        stderr = result.stderr or ""
        elapsed = round(time.monotonic() - started, 3)
        return {
            "executed": True,
            "command": command,
            "returncode": result.returncode,
            "elapsed_seconds": elapsed,
            "timeout": False,
            "stdout_tail": tail(stdout, tail_chars),
            "stderr_tail": tail(stderr, tail_chars),
            **command_io_refs(cwd, command, stdout, stderr),
            "ok": result.returncode == 0,
        }
    except subprocess.TimeoutExpired as exc:
        stdout = str(exc.stdout or "")
        stderr = str(exc.stderr or "")
        elapsed = round(time.monotonic() - started, 3)
        return {
            "executed": True,
            "command": command,
            "returncode": 124,
            "elapsed_seconds": elapsed,
            "timeout": True,
            "stdout_tail": tail(stdout, tail_chars),
            "stderr_tail": tail(stderr, tail_chars),
            **command_io_refs(cwd, command, stdout, stderr),
            "ok": False,
            "error": f"timeout after {timeout}s",
        }


def base_operation_result(operation: dict[str, Any], error: str | None = None) -> dict[str, Any]:
    result = {
        "id": str(operation.get("id") or ""),
        "type": str(operation.get("type") or ""),
        "executed": False,
        "ok": False,
        "errors": [],
        "warnings": [],
        "outputs": [],
    }
    if error:
        result["errors"] = [error]
    return result


def run_python_compile(
    repo_root: Path, operation: dict[str, Any], timeout: int, tail_chars: int
) -> dict[str, Any]:
    paths: list[str] = []
    errors: list[str] = []
    for raw_path in as_list(operation.get("paths")):
        path, error = validate_source_path(repo_root, raw_path, suffix=".py")
        if error:
            errors.append(f"{raw_path}: {error}")
        else:
            paths.append(path)
    if errors or not paths:
        result = base_operation_result(operation, "; ".join(errors) or "no python paths supplied")
        result["paths"] = paths
        return result
    command = [sys.executable, "-m", "py_compile", *paths]
    result = {
        **base_operation_result(operation),
        **run_command(command, repo_root, timeout, tail_chars),
    }
    result["paths"] = paths
    result["errors"] = [] if result["ok"] else [result.get("stderr_tail") or "py_compile failed"]
    return result


def run_python_script(
    repo_root: Path, operation: dict[str, Any], timeout: int, tail_chars: int
) -> dict[str, Any]:
    script, script_error = validate_python_script(repo_root, operation.get("script"))
    args, args_error = validate_string_args(operation.get("args"))
    if script_error or args_error:
        return base_operation_result(
            operation, "; ".join(item for item in [script_error, args_error] if item)
        )
    command = [sys.executable, script, *args]
    result = {
        **base_operation_result(operation),
        **run_command(command, repo_root, timeout, tail_chars),
    }
    result["script"] = script
    result["args"] = args
    result["errors"] = [] if result["ok"] else [result.get("stderr_tail") or "python_script failed"]
    result["outputs"] = discover_output_args(repo_root, args)
    return result


def discover_output_args(repo_root: Path, args: list[str]) -> list[str]:
    outputs: list[str] = []
    output_flags = {"--output", "--markdown-output", "--text-output", "--report-output"}
    for index, arg in enumerate(args[:-1]):
        if arg not in output_flags:
            continue
        path, error = validate_output_path(repo_root, args[index + 1])
        if not error:
            outputs.append(path)
    return outputs


def run_powershell_parse(repo_root: Path, operation: dict[str, Any]) -> dict[str, Any]:
    paths: list[str] = []
    errors: list[str] = []
    for raw_path in as_list(operation.get("paths")):
        path, error = validate_source_path(repo_root, raw_path, suffix=".ps1")
        if error:
            errors.append(f"{raw_path}: {error}")
        else:
            paths.append(path)
    if errors or not paths:
        result = base_operation_result(
            operation, "; ".join(errors) or "no PowerShell paths supplied"
        )
        result["paths"] = paths
        return result
    powershell = shutil.which("powershell.exe") or shutil.which("pwsh")
    if not powershell:
        result = base_operation_result(
            operation, "powershell.exe/pwsh not found for parser operation"
        )
        result["paths"] = paths
        return result
    parse_results: list[dict[str, Any]] = []
    for path in paths:
        literal = "'" + str((repo_root / path).resolve()).replace("'", "''") + "'"
        command = (
            "$tokens=$null;$parseErrors=$null;"
            f"$null=[System.Management.Automation.Language.Parser]::ParseFile({literal},[ref]$tokens,[ref]$parseErrors);"
            "if($parseErrors.Count -gt 0){$parseErrors|ForEach-Object{$_.Message};exit 1}"
        )
        result = run_command([powershell, "-NoProfile", "-Command", command], repo_root, 60, 2000)
        parse_results.append(
            {
                "path": path,
                "ok": result.get("ok") is True,
                "returncode": result.get("returncode"),
                "stdout_tail": result.get("stdout_tail", ""),
                "stderr_tail": result.get("stderr_tail", ""),
                "stdout_ref": result.get("stdout_ref") or {},
                "stderr_ref": result.get("stderr_ref") or {},
                "stdout_chars": result.get("stdout_chars", 0),
                "stderr_chars": result.get("stderr_chars", 0),
                "errors": (
                    []
                    if result.get("ok") is True
                    else [
                        result.get("stdout_tail")
                        or result.get("stderr_tail")
                        or "PowerShell parser failed"
                    ]
                ),
            }
        )
    errors = [f"{item['path']}: {error}" for item in parse_results for error in item["errors"]]
    return {
        **base_operation_result(operation),
        "executed": True,
        "ok": not errors,
        "paths": paths,
        "parse_results": parse_results,
        "errors": errors,
    }


def run_git_diff_check(
    repo_root: Path, operation: dict[str, Any], timeout: int, tail_chars: int
) -> dict[str, Any]:
    result = {
        **base_operation_result(operation),
        **run_command(["git", "diff", "--check"], repo_root, timeout, tail_chars),
    }
    result["errors"] = (
        []
        if result["ok"]
        else [result.get("stdout_tail") or result.get("stderr_tail") or "git diff --check failed"]
    )
    return result


def run_git_status_short(
    repo_root: Path, operation: dict[str, Any], timeout: int, tail_chars: int
) -> dict[str, Any]:
    result = {
        **base_operation_result(operation),
        **run_command(["git", "status", "--short"], repo_root, timeout, tail_chars),
    }
    result["errors"] = (
        [] if result["ok"] else [result.get("stderr_tail") or "git status --short failed"]
    )
    return result


def run_validation_report_contract(
    repo_root: Path, operation: dict[str, Any], timeout: int, tail_chars: int
) -> dict[str, Any]:
    report_file, error = validate_output_path(
        repo_root, operation.get("report_file"), required_suffix=".json"
    )
    if error:
        return base_operation_result(operation, error)
    output, output_error = validate_output_path(
        repo_root,
        operation.get("output") or "output/validation/debug_lab_contract.json",
    )
    if output_error:
        return base_operation_result(operation, output_error)
    command = [
        sys.executable,
        "Tools/validation/pipeline/check_validation_report_contract/cli.py",
        "--repo-root",
        ".",
        "--report-file",
        report_file,
        "--output",
        output,
    ]
    result = {
        **base_operation_result(operation),
        **run_command(command, repo_root, timeout, tail_chars),
    }
    result["outputs"] = [output]
    result["errors"] = (
        []
        if result["ok"]
        else [result.get("stdout_tail") or result.get("stderr_tail") or "report contract failed"]
    )
    return result


def run_json_report_probe(repo_root: Path, operation: dict[str, Any]) -> dict[str, Any]:
    report_path, error = validate_output_path(
        repo_root, operation.get("report_file"), required_suffix=".json"
    )
    if error:
        return base_operation_result(operation, error)
    try:
        data = json.loads((repo_root / report_path).read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - diagnostic report
        return base_operation_result(operation, f"{type(exc).__name__}: {exc}")
    errors = []
    for field in ("kind", "passed", "errors", "warnings"):
        if field not in data:
            errors.append(f"missing field: {field}")
    return {
        **base_operation_result(operation),
        "executed": True,
        "ok": not errors,
        "report_file": report_path,
        "report_kind": data.get("kind") if isinstance(data, dict) else None,
        "report_passed": data.get("passed") if isinstance(data, dict) else None,
        "errors": errors,
    }


def run_operation(
    repo_root: Path, operation: dict[str, Any], default_timeout: int, tail_chars: int
) -> dict[str, Any]:
    operation_type = str(operation.get("type") or "")
    timeout = operation_timeout(operation.get("timeout_seconds"), default_timeout)
    if operation_type in FORBIDDEN_OPERATION_TYPES:
        return base_operation_result(operation, f"operation type is forbidden: {operation_type}")
    if operation_type not in ALLOWED_OPERATION_TYPES:
        return base_operation_result(
            operation, f"operation type is not allowlisted: {operation_type}"
        )
    if operation_type == "python_compile":
        return run_python_compile(repo_root, operation, timeout, tail_chars)
    if operation_type == "python_script":
        return run_python_script(repo_root, operation, timeout, tail_chars)
    if operation_type == "powershell_parse":
        return run_powershell_parse(repo_root, operation)
    if operation_type == "git_diff_check":
        return run_git_diff_check(repo_root, operation, timeout, tail_chars)
    if operation_type == "git_status_short":
        return run_git_status_short(repo_root, operation, timeout, tail_chars)
    if operation_type == "validation_report_contract":
        return run_validation_report_contract(repo_root, operation, timeout, tail_chars)
    if operation_type == "json_report_probe":
        return run_json_report_probe(repo_root, operation)
    return base_operation_result(operation, f"unhandled operation type: {operation_type}")


def run_request(
    repo_root: Path, request: dict[str, Any], timeout_seconds: int, tail_chars: int
) -> dict[str, Any]:
    request_errors = validate_request(request)
    operations = as_list(request.get("operations"))
    results = (
        []
        if request_errors
        else [
            run_operation(repo_root, operation, timeout_seconds, tail_chars)
            for operation in operations
            if isinstance(operation, dict)
        ]
    )
    non_dict_count = sum(1 for operation in operations if not isinstance(operation, dict))
    errors = list(request_errors)
    if non_dict_count:
        errors.append(f"operations contains {non_dict_count} non-object item(s)")
    errors.extend(
        f"{item.get('id') or item.get('type')}: {error}"
        for item in results
        for error in item.get("errors", [])
    )
    failed_count = (
        sum(1 for item in results if item.get("ok") is not True)
        + len(request_errors)
        + non_dict_count
    )
    return {
        "schema_version": 1,
        "kind": "agent_runtime_debug_lab",
        "repo_root": repo_root.as_posix(),
        "passed": failed_count == 0,
        "operation_count": len(results),
        "failed_count": failed_count,
        "operations": results,
        "guardrails": {
            "free_shell_exposed": False,
            "allowlist_enforced": True,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "git_write_performed": False,
            "blender_runtime_execution_performed": False,
            "ffmpeg_runtime_execution_performed": False,
        },
        "errors": errors,
        "warnings": [],
    }
