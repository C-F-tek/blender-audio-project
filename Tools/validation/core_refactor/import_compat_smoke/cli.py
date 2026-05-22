"""Validate IA-Carmine core imports and compatibility command packages."""

from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path
from typing import Any


CORE_IMPORTS = [
    "ia_carmine",
    "ia_carmine.runtime",
    "ia_carmine.memory",
    "ia_carmine.context",
    "ia_carmine.chunks",
    "ia_carmine.pointers",
    "ia_carmine.providers",
    "ia_carmine.product",
    "ia_carmine.validation_contracts",
    "ia_carmine.runtime.run.cli",
    "ia_carmine.providers.provider_mesh.local_resource_lanes_check.cli",
    "ia_carmine.providers.npu.provider_mesh.npu_review_runner.cli",
    "ia_carmine.product.operator_product_core",
]

COMPAT_IMPORTS = [
    ".".join(("Tools", "ai")),
    ".".join(("Tools", "ai", "run", "cli")),
    ".".join(("Tools", "ai", "heap_gate", "provider_time")),
    ".".join(("Tools", "npu", "provider_mesh", "npu_review_runner", "cli")),
]


def _import_many(names: list[str]) -> tuple[list[str], list[dict[str, str]]]:
    imported: list[str] = []
    errors: list[dict[str, str]] = []
    for name in names:
        try:
            importlib.import_module(name)
            imported.append(name)
        except Exception as exc:  # pragma: no cover - report path
            errors.append({"module": name, "error": f"{type(exc).__name__}: {exc}"})
    return imported, errors


def build_report(repo_root: Path) -> dict[str, Any]:
    core_imports, core_errors = _import_many(CORE_IMPORTS)
    compat_imports, compat_errors = _import_many(COMPAT_IMPORTS)
    dispatch = importlib.import_module("ia_carmine.cli")
    target_errors = [
        {"tool": name, "target": target}
        for name, target in dispatch.TOOL_MAIN_TARGETS.items()
        if target.startswith(".".join(("Tools", "ai")))
    ]
    errors = core_errors + compat_errors + target_errors
    return {
        "schema_version": 1,
        "kind": "ia_carmine_core_refactor_import_compat_smoke",
        "repo_root": str(repo_root),
        "passed": not errors,
        "core_imports": core_imports,
        "compatibility_imports": compat_imports,
        "dispatch_target_count": len(dispatch.TOOL_MAIN_TARGETS),
        "errors": errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="")
    args = parser.parse_args(argv)

    report = build_report(Path(args.repo_root).resolve())
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if report["passed"] else 2
