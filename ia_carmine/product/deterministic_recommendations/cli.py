from __future__ import annotations

from .common import *  # noqa: F403
from .report import build_patch_plan_bridge_orchestrator, build_recommendation_report, render_markdown

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--evidence", default=DEFAULT_EVIDENCE)
    parser.add_argument("--orchestrator", default=DEFAULT_ORCHESTRATOR)
    parser.add_argument("--gpu-report", default="")
    parser.add_argument("--tool-report", action="append", default=[])
    parser.add_argument("--max-recommendations", type=int, default=20)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    parser.add_argument("--patch-plan-orchestrator-output", default="")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_recommendation_report(args)
    output = resolve_path(repo_root, args.output)
    markdown_output = resolve_path(repo_root, args.markdown_output)
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown_output)

    bridge_output_text = ""
    if args.patch_plan_orchestrator_output:
        source_orchestrator, _bridge_warnings = load_report_at(
            repo_root, args.orchestrator, missing_is_error=False
        )
        bridge_output = resolve_path(repo_root, args.patch_plan_orchestrator_output)
        bridge = build_patch_plan_bridge_orchestrator(
            repo_root=repo_root,
            recommendation_report=report,
            recommendation_output=output,
            source_orchestrator=source_orchestrator,
        )
        write_json_report(bridge, bridge_output)
        bridge_output_text = str(bridge_output)

    print(
        json.dumps(
            {
                "passed": report["passed"],
                "output": str(output),
                "markdown": str(markdown_output),
                "patch_plan_orchestrator_output": bridge_output_text,
                "recommendation_count": report["recommendation_count"],
                "deterministic_synthesizer_used": report["decision"][
                    "deterministic_synthesizer_used"
                ],
                "next_best_action": report["next_best_action"],
                "provider_execution_performed": report["provider_execution_performed"],
                "patch_application_performed": report["patch_application_performed"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report["passed"] else 2
