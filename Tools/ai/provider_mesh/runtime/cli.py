"""Report provider mesh runtime support capability without launching providers."""

from __future__ import annotations

import argparse
import importlib.util
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from Tools.ai.provider_mesh.runtime import command_env, resolve_child_python


MODULES = (
    "Tools.ai.provider_mesh.runtime.python_runtime",
    "Tools.ai.provider_mesh.runtime.runtime_heap",
    "Tools.ai.provider_mesh.runtime.gpu0_peer",
    "Tools.ai.provider_mesh.runtime.npu_micro",
)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Provider Mesh Runtime",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Child Python: `{report.get('child_python')}`",
        f"- Provider execution performed: `{report.get('provider_execution_performed')}`",
        "",
        "## Modules",
        "",
    ]
    for item in report.get("modules") or []:
        lines.append(f"- `{item.get('module')}` available=`{item.get('available')}`")
    return "\n".join(lines) + "\n"


def build_report(repo_root: Path) -> dict[str, Any]:
    modules = [
        {"module": name, "available": importlib.util.find_spec(name) is not None}
        for name in MODULES
    ]
    errors = [item["module"] for item in modules if not item["available"]]
    return {
        "schema_version": 1,
        "kind": "provider_mesh_runtime_capability",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "child_python": resolve_child_python(repo_root),
        "command_env_keys": sorted(command_env(repo_root)),
        "modules": modules,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "git_write_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/provider_mesh_runtime.json")
    parser.add_argument(
        "--markdown-output", default="output/validation/provider_mesh_runtime.md"
    )
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root)
    output = Path(args.output)
    markdown = Path(args.markdown_output)
    if not output.is_absolute():
        output = repo_root / output
    if not markdown.is_absolute():
        markdown = repo_root / markdown
    write_json(output, report)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "output": str(output)}, indent=2))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
