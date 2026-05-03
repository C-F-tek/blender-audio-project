# Evidence Chunk 0008/0028

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-231855.md`
- source_sha256: `67abdf3a424f48df981c09aedf66a8fdd609b54cc1cbb41f7454d4a8b714e3f1`
- line_start: `1743`
- line_end: `1805`
- section_kinds: `['markdown_heading_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_md_67abdf3a424f_chunk_0007.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_md_67abdf3a424f_chunk_0009.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: `Tools/ai/run_agent_review_decision_loop.py`. Preview: lines.append("") lines.append("## Warnings") lines.append("") for warning in report["warnings"]: lines.append(f"- {warning}") lines.append("") lines.append("## Guardrails") lines.append("") lines.append("Report-only decision loop. No provider execution, patch ...

## Context before

    lines.append("")
    for key, value in report.get("outputs", {}).items():
        lines.append(
            f"- `{key}`: `{value.get('path')}` exists=`{value.get('exists')}` size=`{value.get('size_bytes')}`"
        )
    if report.get("errors"):
        lines.append("")
        lines.append("## Errors")
        lines.append("")
        for error in report["errors"]:
            lines.append(f"- {error}")
    if report.get("warnings"):

## Chunk content

````md
        lines.append("")
        lines.append("## Warnings")
        lines.append("")
        for warning in report["warnings"]:
            lines.append(f"- {warning}")
    lines.append("")
    lines.append("## Guardrails")
    lines.append("")
    lines.append("Report-only decision loop. No provider execution, patch application, SQLite write or Blender runtime.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--evidence", default=DEFAULT_EVIDENCE)
    parser.add_argument("--orchestrator", default=DEFAULT_ORCHESTRATOR)
    parser.add_argument("--gpu-report", default="")
    parser.add_argument("--tool-report", action="append", default=[])
    parser.add_argument("--max-recommendations", type=int, default=20)
    parser.add_argument("--max-patch-plans", type=int, default=0, help="Maximum patch plans to keep; 0 means no additional cap.")
    parser.add_argument("--min-recommendations", type=int, default=1)
    parser.add_argument("--min-patch-plans", type=int, default=1)
    parser.add_argument("--recommendations-output", default=DEFAULT_RECOMMENDATIONS_OUTPUT)
    parser.add_argument("--recommendations-markdown", default=DEFAULT_RECOMMENDATIONS_MARKDOWN)
    parser.add_argument("--bridge-orchestrator-output", default=DEFAULT_BRIDGE_ORCHESTRATOR)
    parser.add_argument("--patch-plan-output", default=DEFAULT_PATCH_PLAN_OUTPUT)
    parser.add_argument("--patch-plan-markdown", default=DEFAULT_PATCH_PLAN_MARKDOWN)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_decision_loop_report(args)
    output = resolve_path(repo_root, args.output)
    markdown_output = resolve_path(repo_root, args.markdown_output)
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown_output)
    print(
        json.dumps(
            {
                "passed": report["passed"],
                "output": str(output),
                "markdown": str(markdown_output),
                "recommendation_count": report["recommendation_count"],
                "patch_plan_count": report["patch_plan_count"],
                "deterministic_synthesizer_used": report["deterministic_synthesizer_used"],
                "patch_plan_fallback_used": report["patch_plan_fallback_used"],
                "provider_execution_performed": report["provider_execution_performed"],
                "patch_application_performed": report["patch_application_performed"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

```

````

## Context after

### `Tools/validation/run_agent_review_decision_loop_smoke.py`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.py`
- Size bytes: `11896`
- SHA-256: `91be3dd92478bee3cb4eb1b85d481c93502860677b12a0f34167cd519e13cdcc`
- Content included: `True`
- Content truncated: `False`

```text
#!/usr/bin/env python3
