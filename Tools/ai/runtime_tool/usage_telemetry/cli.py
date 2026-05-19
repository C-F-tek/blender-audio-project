from __future__ import annotations

from .common import *  # noqa: F403
from .report import build_report, render_markdown

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--orchestrator", required=True)
    parser.add_argument("--gpu-report", required=True)
    parser.add_argument("--gpu-npu-sync", default="")
    parser.add_argument("--decision-loop", default="")
    parser.add_argument(
        "--broker-report",
        action="append",
        default=[],
        help="Explicit agent_runtime_tool_broker JSON report. Repeatable or comma-separated.",
    )
    parser.add_argument("--max-entries", type=int, default=400)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = build_report(args)
    output = resolve_output_path(repo_root, args.output)
    markdown_output = resolve_output_path(repo_root, args.markdown_output)
    print(write_json_report(report, output), end="")
    write_text_report(render_markdown(report), markdown_output)
    return 0 if report["passed"] else 2
