"""Validate public dispatcher target module:function references."""

from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path
from typing import Any

DEFAULT_DISPATCHERS = (
    "ia_carmine.dispatch",
    "Tools.validation.dispatch",
    "Tools.workflow.dispatch",
    "Tools.npu.dispatch",
    "Tools.docs.dispatch",
    "Tools.git.dispatch",
    "Tools.repo_patch_runner.dispatch",
)


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    dispatchers = DEFAULT_DISPATCHERS if args.all or not args.dispatcher else tuple(args.dispatcher)
    checked: list[dict[str, Any]] = []
    warnings: list[str] = []
    errors: list[str] = []
    for dispatcher in dispatchers:
        result = _check_dispatcher(dispatcher)
        checked.extend(result["targets"])
        warnings.extend(result["warnings"])
        errors.extend(result["errors"])
    failures = [item for item in checked if item.get("ok") is not True]
    report = {
        "schema_version": 1,
        "kind": "dispatcher_targets_check",
        "passed": not failures and not errors,
        "repo_root": str(repo_root),
        "dispatcher_count": len(dispatchers),
        "target_count": len(checked),
        "checked_count": len(checked),
        "failed_count": len(failures),
        "failures": failures,
        "warnings": warnings,
        "errors": errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }
    _write_report(repo_root, args.output, report)
    print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
    return 0 if report["passed"] else 2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--dispatcher", action="append", default=[])
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--output", default="")
    return parser.parse_args()


def _check_dispatcher(dispatcher: str) -> dict[str, Any]:
    warnings: list[str] = []
    errors: list[str] = []
    targets: list[dict[str, Any]] = []
    try:
        module = importlib.import_module(dispatcher)
    except Exception as exc:  # noqa: BLE001
        return {
            "targets": [],
            "warnings": [],
            "errors": [f"{dispatcher}: import failed: {type(exc).__name__}: {exc}"],
        }
    mapping = getattr(module, "TOOL_MAIN_TARGETS", None)
    if mapping is None:
        mapping = getattr(module, "TARGETS", None)
        if mapping is not None:
            warnings.append(f"{dispatcher}: uses TARGETS compatibility name")
    if not isinstance(mapping, dict):
        errors.append(f"{dispatcher}: missing TOOL_MAIN_TARGETS/TARGETS mapping")
        return {"targets": targets, "warnings": warnings, "errors": errors}
    module_file = Path(str(getattr(module, "__file__", ""))).resolve()
    package_dir = module_file.parent
    for name, target in sorted(mapping.items()):
        targets.append(_check_target(dispatcher, package_dir, str(name), str(target)))
    return {"targets": targets, "warnings": warnings, "errors": errors}


def _check_target(dispatcher: str, package_dir: Path, name: str, target: str) -> dict[str, Any]:
    base = {"dispatcher": dispatcher, "name": name, "target": target}
    if target.startswith("ps1:"):
        script = package_dir / target.removeprefix("ps1:")
        return {
            **base,
            "target_type": "powershell",
            "ok": script.exists() and script.is_file(),
            "error": "" if script.exists() else f"missing PowerShell target: {script}",
        }
    if ":" not in target:
        return {**base, "target_type": "python", "ok": False, "error": "target missing ':'"}
    module_name, function_name = target.split(":", 1)
    try:
        module = importlib.import_module(module_name)
        value = getattr(module, function_name)
    except Exception as exc:  # noqa: BLE001
        return {
            **base,
            "target_type": "python",
            "ok": False,
            "error": f"{type(exc).__name__}: {exc}",
        }
    return {
        **base,
        "target_type": "python",
        "ok": callable(value),
        "error": "" if callable(value) else f"{function_name} is not callable",
    }


def _write_report(repo_root: Path, output: str, report: dict[str, Any]) -> None:
    if not output:
        return
    path = Path(output)
    if not path.is_absolute():
        path = repo_root / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
