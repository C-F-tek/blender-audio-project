# Evidence Chunk 0012/0031

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-223900.md`
- source_sha256: `42fa09a3e087ebc6b51a8d9d2d501922dd8ed8c400791441877ab803557340fa`
- line_start: `2278`
- line_end: `2327`
- section_kinds: `['markdown_heading_section', 'markdown_heading_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_md_42fa09a3e087_chunk_0011.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_md_42fa09a3e087_chunk_0013.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Generare un report di consistenza del repository per l’analisi automatica di artefatti.  
**Segnali principali**: 11 488 findings, 3 769 file Markdown, 320 file Python; 6 265 severità alta, 5 174 media, 49 bassa.  
**Guardrail/erori**: 49 script Python non documentati, 4 argomenti CLI mancanti in argparse, 5 170 riferimenti Markdown a percorsi Python inesistenti, 972 a PowerShell, 1 020 comandi Python mancanti.  
**Perché

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

### `output/analysis/repository_consistency_map_full_toolbox_20260503-223900.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `45792`
- SHA-256: `a05eff34ca8b5ddedb7003a2893f180a7faf6eadbca67e020b02abbf0ecb12de`
- Content included: `True`
- Content truncated: `True`

```text
# Repository Consistency Map

- Passed: `True`
- Finding count: `11488`
- Markdown files: `3769`
- Python files: `320`
- Markdown references: `183678`
- Markdown Python commands: `1948`
- Provider execution performed: `False`
- Workers requested: `8`
- Total build seconds: `88.586`
- Markdown scan seconds: `72.314`
- Python inventory seconds: `4.082`
- Patch application performed: `False`

## Severity counts

- `high`: `6265`
- `low`: `49`
- `medium`: `5174`

## Finding kind counts

- `documented_python_script_without_obvious_smoke`: `49`
- `md_cli_arg_not_in_argparse`: `4`
- `md_mentions_missing_markdown_path`: `5170`
- `md_mentions_missing_powershell_path`: `972`
- `md_mentions_missing_python_path`: `5191`
- `md_python_command_script_missing`: `102`

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
