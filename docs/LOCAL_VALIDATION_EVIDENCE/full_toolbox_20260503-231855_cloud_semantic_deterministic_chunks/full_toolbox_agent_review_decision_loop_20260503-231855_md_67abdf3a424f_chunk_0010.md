# Evidence Chunk 0010/0028

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-231855.md`
- source_sha256: `67abdf3a424f48df981c09aedf66a8fdd609b54cc1cbb41f7454d4a8b714e3f1`
- line_start: `2118`
- line_end: `2167`
- section_kinds: `['markdown_heading_section', 'markdown_heading_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_md_67abdf3a424f_chunk_0009.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_md_67abdf3a424f_chunk_0011.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: `Tools/validation/run_agent_review_decision_loop_smoke.py`; `output/analysis/repository_consistency_map_full_toolbox_20260503-231855.md`; Repository Consistency Map; Severity counts; Finding kind counts. Preview: write_text_report(render_markdown(report), markdown_output) return 0 if report["passed"] else 2 if __name__ == "__main__": raise SystemExit(main()) ``` ### `output/analysis/repository_consistency_map_full_toolbox_20260503-231855.md` - Role: `auto_related_artif...

## Context before

    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = run_smoke(repo_root, args.timeout_seconds)
    output = resolve_output_path(repo_root, args.output)
    markdown_output = resolve_output_path(repo_root, args.markdown_output)
    print(write_json_report(report, output), end="")

## Chunk content

````md
    write_text_report(render_markdown(report), markdown_output)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

```

### `output/analysis/repository_consistency_map_full_toolbox_20260503-231855.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `45790`
- SHA-256: `f3d03a1ecb0ff228c05a4feb9d9eeb8531be67972c2638c3fe29c5234f75253d`
- Content included: `True`
- Content truncated: `True`

```text
# Repository Consistency Map

- Passed: `True`
- Finding count: `10409`
- Markdown files: `3620`
- Python files: `321`
- Markdown references: `177016`
- Markdown Python commands: `1949`
- Provider execution performed: `False`
- Workers requested: `8`
- Total build seconds: `81.318`
- Markdown scan seconds: `69.564`
- Python inventory seconds: `3.593`
- Patch application performed: `False`

## Severity counts

- `high`: `5233`
- `low`: `49`
- `medium`: `5127`

## Finding kind counts

- `documented_python_script_without_obvious_smoke`: `49`
- `md_cli_arg_not_in_argparse`: `4`
- `md_mentions_missing_markdown_path`: `5123`
- `md_mentions_missing_powershell_path`: `708`
- `md_mentions_missing_python_path`: `4441`
- `md_python_command_script_missing`: `84`

````

## Context after

## Findings

| Severity | Kind | Source | Line | Target | Recommendation |
|---|---|---|---:|---|---|
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 91 | `animation.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 93 | `animation.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 94 | `asset_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 96 | `asset_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 97 | `atmosphere_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 99 | `atmosphere_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 100 | `camera_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 102 | `camera_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
