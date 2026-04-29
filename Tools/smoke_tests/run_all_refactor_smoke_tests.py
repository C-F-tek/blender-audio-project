#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = ROOT / "output" / "smoke_tests"


def run_command(name: str, command: list[str], cwd: Path) -> dict[str, Any]:
    started = datetime.now(timezone.utc).isoformat()
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    finished = datetime.now(timezone.utc).isoformat()
    return {
        "name": name,
        "command": command,
        "started_at": started,
        "finished_at": finished,
        "returncode": completed.returncode,
        "passed": completed.returncode == 0,
        "stdout": completed.stdout[-12000:],
        "stderr": completed.stderr[-12000:],
    }


def read_json_if_exists(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - smoke report should capture parse failures.
        return {"parse_error": f"{type(exc).__name__}: {exc}"}


def build_markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Refactor Smoke Test Summary\n",
        f"- Generated at: `{report['generated_at']}`\n",
        f"- Repository root: `{report['repo_root']}`\n",
        f"- Python: `{report['runtime']['python']}`\n",
        f"- Platform: `{report['runtime']['platform']}`\n",
        f"- Overall passed: `{report['passed']}`\n\n",
        "## Commands\n",
    ]
    for result in report["commands"]:
        lines.append(f"- `{result['name']}`: passed=`{result['passed']}`, returncode=`{result['returncode']}`\n")
    lines.extend([
        "\n## Individual reports\n",
        f"- AI core JSON: `{report['reports']['ai_core_json']}`\n",
        f"- AI core Markdown: `{report['reports']['ai_core_markdown']}`\n",
        f"- NPU bridge JSON: `{report['reports']['npu_bridge_json']}`\n",
        f"- NPU bridge Markdown: `{report['reports']['npu_bridge_markdown']}`\n\n",
        "## Share with assistant\n",
        "Share this file plus `refactor_smoke_summary.json`. If a command failed, also share the corresponding individual JSON report.\n",
    ])
    return "".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Run all non-invasive refactor smoke tests and emit an aggregate report.")
    ap.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--skip-ai-core", action="store_true")
    ap.add_argument("--skip-npu-bridge", action="store_true")
    args = ap.parse_args()

    out_root = Path(args.output_dir)
    summary_dir = out_root / "refactor_summary"
    ai_core_dir = out_root / "ai_core"
    npu_bridge_dir = out_root / "npu_validation_bridge"
    summary_dir.mkdir(parents=True, exist_ok=True)

    commands: list[tuple[str, list[str]]] = []
    if not args.skip_ai_core:
        commands.append((
            "ai_core_smoke_tests",
            [args.python, "Tools/smoke_tests/run_ai_core_smoke_tests.py", "--output-dir", str(ai_core_dir)],
        ))
    if not args.skip_npu_bridge:
        commands.append((
            "npu_validation_bridge_smoke_tests",
            [
                args.python,
                "Tools/smoke_tests/run_npu_validation_bridge_smoke_tests.py",
                "--output-dir",
                str(npu_bridge_dir),
                "--manifest",
                "Tools/npu/npu_code_manifest.json",
            ],
        ))

    results = [run_command(name, command, ROOT) for name, command in commands]

    reports = {
        "ai_core_json": str(ai_core_dir / "ai_core_smoke_report.json"),
        "ai_core_markdown": str(ai_core_dir / "ai_core_smoke_report.md"),
        "npu_bridge_json": str(npu_bridge_dir / "npu_validation_bridge_smoke_report.json"),
        "npu_bridge_markdown": str(npu_bridge_dir / "npu_validation_bridge_smoke_report.md"),
    }
    embedded_reports = {
        "ai_core": read_json_if_exists(Path(reports["ai_core_json"])),
        "npu_validation_bridge": read_json_if_exists(Path(reports["npu_bridge_json"])),
    }

    report = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(ROOT),
        "runtime": {"python": sys.version, "python_executable": args.python, "platform": platform.platform()},
        "passed": all(item["passed"] for item in results),
        "commands": results,
        "reports": reports,
        "embedded_reports": embedded_reports,
    }

    json_path = summary_dir / "refactor_smoke_summary.json"
    md_path = summary_dir / "refactor_smoke_summary.md"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(build_markdown_report(report), encoding="utf-8")

    print(json.dumps({"passed": report["passed"], "json_report": str(json_path), "markdown_report": str(md_path)}, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
