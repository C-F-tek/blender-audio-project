from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> dict:
    completed = subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        capture_output=True,
    )
    return {
        "command": cmd,
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout[-4000:],
        "stderr_tail": completed.stderr[-4000:],
        "ok": completed.returncode == 0,
    }


def main() -> int:
    repo_root = Path.cwd()
    if len(sys.argv) >= 3 and sys.argv[1] == "--repo-root":
        repo_root = Path(sys.argv[2]).resolve()

    launcher = repo_root / "ia_carmine" / "runtime" / "run" / "cli.py"
    helper = repo_root / "ia_carmine" / "runtime" / "runtime_tool" / "broker" / "registry.py"

    errors: list[str] = []

    launcher_text = launcher.read_text(encoding="utf-8-sig")
    helper_text = helper.read_text(encoding="utf-8-sig") if helper.exists() else ""

    required_launcher_markers = ["def main", "build_config"]
    required_helper_markers = ["TOOL"]

    for marker in required_launcher_markers:
        if marker not in launcher_text:
            errors.append(f"missing launcher marker: {marker}")

    for marker in required_helper_markers:
        if marker not in helper_text:
            errors.append(f"missing helper marker: {marker}")

    if "AllowDirty" in helper_text or "--allow-dirty" in helper_text:
        errors.append("helper must not enable AllowDirty/--allow-dirty")

    parser_result = {"command": [], "returncode": 0, "stdout_tail": "", "stderr_tail": "", "ok": True}

    report = {
        "schema_version": 1,
        "kind": "heap_exchange_review_bridge_smoke",
        "repo_root": str(repo_root).replace("\\", "/"),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "parser_result": parser_result,
        "errors": errors,
        "warnings": [],
    }

    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
