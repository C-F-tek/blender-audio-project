#!/usr/bin/env python3
"""Controlled virtual development environment report for heap runs."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import importlib
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from ia_carmine.runtime.runtime_tool.file_refs import (
        RuntimeConsumer,
        RuntimeFileRefResolver,
        RuntimeRefProvenance,
    )
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[4]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from ia_carmine.runtime.runtime_tool.file_refs import (  # type: ignore
        RuntimeConsumer,
        RuntimeFileRefResolver,
        RuntimeRefProvenance,
    )

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def normalize_repo_path(repo_root: Path, raw: str) -> tuple[str, str]:
    ref = RuntimeFileRefResolver(repo_root).resolve(
        raw,
        provenance=RuntimeRefProvenance.TOOL_REQUEST,
        consumers=(RuntimeConsumer.LAB,),
    )
    if not ref.patchable:
        return ref.repo_relative or str(raw or ""), ref.reason
    return ref.repo_relative, ""


def normalize_validation_path(repo_root: Path, raw: str) -> tuple[str, str]:
    ref = RuntimeFileRefResolver(repo_root).resolve(
        raw,
        provenance=RuntimeRefProvenance.TOOL_REQUEST,
        consumers=(RuntimeConsumer.BROKER_TOOL,),
        validation_ref=True,
    )
    if not ref.validation_only:
        return ref.repo_relative or str(raw or ""), ref.reason
    return ref.repo_relative, ""


def split_values(values: list[str]) -> list[str]:
    out: list[str] = []
    for value in values:
        for item in str(value).split(","):
            if item.strip():
                out.append(item.strip())
    return out


def run_command(command: list[str], cwd: Path, timeout: int, tail_chars: int) -> dict[str, Any]:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            command, cwd=cwd, text=True, capture_output=True, check=False, timeout=timeout
        )
        return {
            "command": command,
            "returncode": completed.returncode,
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "stdout_tail": (completed.stdout or "")[-tail_chars:],
            "stderr_tail": (completed.stderr or "")[-tail_chars:],
            "ok": completed.returncode == 0,
            "timeout": False,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "returncode": 124,
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "stdout_tail": str(exc.stdout or "")[-tail_chars:],
            "stderr_tail": str(exc.stderr or "")[-tail_chars:],
            "ok": False,
            "timeout": True,
        }


def package_module_name(repo_root: Path, rel: str) -> str | None:
    if not rel.endswith(".py"):
        return None
    path = (repo_root / rel).resolve(strict=False)
    try:
        relative = path.relative_to(repo_root)
    except ValueError:
        return None
    parts = list(relative.parts)
    if not parts or parts[-1] == "__init__.py":
        return None
    package_dirs = [repo_root.joinpath(*parts[:index]) for index in range(1, len(parts))]
    if not package_dirs or any(not (directory / "__init__.py").is_file() for directory in package_dirs):
        return None
    parts[-1] = Path(parts[-1]).stem
    return ".".join(parts)


def python_command_for_target(repo_root: Path, rel: str, *args: str) -> list[str]:
    module_name = package_module_name(repo_root, rel)
    if module_name:
        return [sys.executable, "-m", module_name, *args]
    return [sys.executable, rel, *args]


def ast_probe(repo_root: Path, rel: str) -> dict[str, Any]:
    path = repo_root / rel
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        tree = ast.parse(text, filename=rel)
    except Exception as exc:
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
    imports: list[str] = []
    functions: list[str] = []
    classes: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
    return {
        "ok": True,
        "line_count": len(text.splitlines()),
        "sha256": hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest(),
        "imports": sorted(set(imports))[:40],
        "functions": functions[:80],
        "classes": classes[:40],
    }


def import_probe(repo_root: Path, rel: str) -> dict[str, Any]:
    if not rel.endswith(".py"):
        return {"executed": False, "ok": True, "reason": "not Python"}
    path = repo_root / rel
    package_name = package_module_name(repo_root, rel)
    try:
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))
        if package_name:
            module = importlib.import_module(package_name)
            names = [name for name in dir(module) if not name.startswith("_")][:80]
            return {
                "executed": True,
                "ok": True,
                "module": package_name,
                "public_names": names,
            }
        module_name = "heap_vdev_" + hashlib.sha1(rel.encode("utf-8")).hexdigest()[:12]
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise ImportError("module spec unavailable")
        module = importlib.util.module_from_spec(spec)
        old_module = sys.modules.get(module_name)
        sys.modules[module_name] = module
        try:
            spec.loader.exec_module(module)
        finally:
            if old_module is None:
                sys.modules.pop(module_name, None)
            else:
                sys.modules[module_name] = old_module
        names = [name for name in dir(module) if not name.startswith("_")][:80]
        return {"executed": True, "ok": True, "public_names": names}
    except Exception as exc:
        return {"executed": True, "ok": False, "error": f"{type(exc).__name__}: {exc}"}


def help_probe(repo_root: Path, rel: str, timeout: int, tail_chars: int) -> dict[str, Any]:
    if not rel.endswith(".py"):
        return {"executed": False, "ok": True, "reason": "not Python"}
    return {
        "executed": True,
        **run_command(python_command_for_target(repo_root, rel, "--help"), repo_root, timeout, tail_chars),
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Heap Virtual Development Environment",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Target count: `{report.get('target_count')}`",
        f"- Validation count: `{report.get('validation_count')}`",
        "",
        "## Target probes",
        "",
    ]
    for item in report.get("targets") or []:
        lines.append(
            f"- `{item.get('target_file')}` ast=`{item.get('ast_ok')}` import=`{item.get('import_ok')}` help=`{item.get('help_ok')}`"
        )
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report.get("errors") or [])
    return "\n".join(lines) + "\n"


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    resolver = RuntimeFileRefResolver(repo_root)
    errors: list[str] = []
    targets: list[str] = []
    for raw in split_values(args.target_file):
        rel, error = normalize_repo_path(repo_root, raw)
        if error:
            errors.append(f"{raw}: {error}")
        elif rel not in targets:
            targets.append(rel)
    if not targets:
        errors.append("no valid target files supplied")
    target_reports: list[dict[str, Any]] = []
    for rel in targets:
        ast_result = ast_probe(repo_root, rel)
        import_result = import_probe(repo_root, rel) if args.dynamic_import else {}
        help_result = (
            help_probe(repo_root, rel, args.timeout_seconds, args.tail_chars)
            if args.help_probe
            else {}
        )
        target_reports.append(
            {
                "target_file": rel,
                "ast_ok": ast_result.get("ok"),
                "import_ok": import_result.get("ok") if import_result else None,
                "help_ok": help_result.get("ok") if help_result else None,
                "ast_probe": ast_result,
                "import_probe": import_result,
                "help_probe": help_result,
            }
        )
    py_targets = [target for target in targets if target.endswith(".py")]
    compile_result = (
        run_command(
            [sys.executable, "-m", "py_compile", *py_targets],
            repo_root,
            args.timeout_seconds,
            args.tail_chars,
        )
        if py_targets
        else {}
    )
    validations: list[dict[str, Any]] = []
    for raw in split_values(args.validation_script):
        rel, error = normalize_validation_path(repo_root, raw)
        if error:
            validations.append({"script": raw, "ok": False, "errors": [error]})
        else:
            validations.append(
                {
                    "script": rel,
                    **run_command(
                        python_command_for_target(repo_root, rel),
                        repo_root,
                        args.timeout_seconds,
                        args.tail_chars,
                    ),
                }
            )
    errors.extend(
        f"{item['target_file']}: {key} failed"
        for item in target_reports
        for key in ("ast_ok", "import_ok", "help_ok")
        if item.get(key) is False
    )
    if compile_result and compile_result.get("ok") is not True:
        errors.append("py_compile failed")
    errors.extend(
        f"{item.get('script')}: validation failed"
        for item in validations
        if item.get("ok") is not True
    )
    return {
        "schema_version": 1,
        "kind": "heap_virtual_development_environment",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": not errors,
        "target_count": len(targets),
        "validation_count": len(validations),
        "dynamic_import_performed": bool(args.dynamic_import),
        "help_probe_performed": bool(args.help_probe),
        "compile_result": compile_result,
        "targets": target_reports,
        "validation_results": validations,
        "resolved_file_refs": [
            item.as_dict()
            for item in resolver.resolve_many(
                targets,
                provenance=RuntimeRefProvenance.TOOL_REQUEST,
                consumers=(RuntimeConsumer.LAB,),
            )
        ],
        "validation_file_refs": [
            item.as_dict()
            for item in resolver.resolve_many(
                [str(item.get("script") or "") for item in validations],
                provenance=RuntimeRefProvenance.TOOL_REQUEST,
                consumers=(RuntimeConsumer.BROKER_TOOL,),
                validation_ref=True,
            )
        ],
        "guardrails": {
            "free_shell_exposed": False,
            "allowlist_enforced": True,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "git_write_performed": False,
        },
        "errors": errors,
        "warnings": [],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--target-file", action="append", default=[])
    parser.add_argument("--validation-script", action="append", default=[])
    parser.add_argument("--output", default="output/validation/heap_virtual_dev_environment.json")
    parser.add_argument(
        "--markdown-output", default="output/validation/heap_virtual_dev_environment.md"
    )
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--tail-chars", type=int, default=4000)
    parser.add_argument("--dynamic-import", action="store_true")
    parser.add_argument("--help-probe", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = build_report(args)
    output = Path(args.output)
    markdown = Path(args.markdown_output)
    if not output.is_absolute():
        output = repo_root / output
    if not markdown.is_absolute():
        markdown = repo_root / markdown
    write_json(output, report)
    write_text(markdown, render_markdown(report))
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("passed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
