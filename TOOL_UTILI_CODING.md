# TOOL UTILI CODING

## Scopo

Indice operativo dei tool utili per coding assistito da IA, refactor Markdown, validazione e PR reviewabile.

## Refactor Markdown

| Tool | Uso |
|---|---|
| `Tools/docs/refactor_markdown_splits.py` | Migra split legacy `nomefile/part-xxx.md` in `nomefile.md/part-xxx.md`, divide Markdown monolitici e pruna snapshot obsoleti allowlist-only. |
| `Tools/validation/check_markdown_line_limits.py` | Valida il budget righe Markdown. Usare `--max-lines 400` per policy preferita e `500` come soglia hard. |
| `Tools/validation/check_docs_links.py` | Controlla link Markdown dopo split, rename o pruning. |

Comando tipico:

```powershell
python .\Tools\docs\refactor_markdown_splits.py `
  --repo-root . `
  --apply `
  --migrate-legacy-splits `
  --split-monolithic `
  --prune-obsolete-snapshots `
  --write-root-tool-guide
```

## Coding/PR product lane

| Tool | Uso |
|---|---|
| `Tools/ai/build_task_patch_suggestion_report.py` | Estrae suggestion concrete da task Markdown. |
| `Tools/ai/apply_patch_suggestion_bundle.py` | Applica/dry-run deterministic operations da patch suggestion report. |
| `Tools/validation/check_patch_suggestion_product_separation.py` | Separa prodotto essenziale da telemetry/debug supplementare. |
| `Tools/ai/prepare_review_pr.py` | Prepara branch/commit/PR reviewabile con allowlist/autodiscovery include-path. |

## Validazioni minime

```powershell
python -m py_compile .\Tools\docs\refactor_markdown_splits.py
python .\Tools\validation\check_docs_links.py --repo-root .
python .\Tools\validation\check_markdown_line_limits.py --repo-root . --max-lines 500
python .\Tools\validation\check_file_line_limits.py --repo-root . --output .\output\validation\file_line_limits.json
git diff --check
git status --short
```

## Guardrail

Non committare `output/**`, `renders/**`, DB SQLite, chunk generati o patch bundle locali. Le modifiche distruttive devono restare su branch reviewabile e passare da PR.
