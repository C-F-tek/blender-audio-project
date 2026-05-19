"""CLI for provider evidence contract validation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .common import resolve_path
from .report import build_report, render_markdown

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--orchestrator", required=True)
    parser.add_argument("--gpu-report", required=True)
    parser.add_argument("--gpu-npu-sync", default="")
    parser.add_argument(
        "--local-provider-probe", default="output/validation/local_provider_probe.json"
    )
    parser.add_argument(
        "--hardware-manifest", default="output/validation/runtime_hardware_capability_manifest.json"
    )
    parser.add_argument(
        "--openvino-gpu0-workload", default="output/validation/openvino_gpu0_workload.json"
    )
    parser.add_argument("--require-gpu-provider", action="store_true")
    parser.add_argument("--require-openvino-gpu0-secondary", action="store_true")
    parser.add_argument("--forbid-openvino-gpu1-workload", action="store_true", default=True)
    parser.add_argument("--require-npu-auditor", action="store_true")
    parser.add_argument("--output", default="output/validation/provider_evidence_contract.json")
    parser.add_argument(
        "--markdown-output", default="output/validation/provider_evidence_contract.md"
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(args)
    output = resolve_path(repo_root, args.output)
    markdown = resolve_path(repo_root, args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown.write_text(render_markdown(report), encoding="utf-8")
    print(
        json.dumps(
            {"passed": report["passed"], "output": str(output), "markdown": str(markdown)}, indent=2
        )
    )
    return 0 if report["passed"] else 2
