from __future__ import annotations

from pathlib import Path
from typing import Any


def write_root_tool_guide(root: Path, apply: bool, write, rel) -> dict[str, Any]:
    path = root / "TOOL_UTILI_CODING.md"
    text = """# TOOL UTILI CODING

## Scopo

Indice operativo dei tool utili per coding assistito da IA, refactor Markdown, validazione e PR reviewabile.

## Refactor Markdown

| Tool | Uso |
|---|---|
| `python -m Tools.docs refactor_markdown_splits` | Migra split legacy `nomefile/part-xxx.md` in `nomefile.md/part-xxx.md`, divide Markdown monolitici e pruna snapshot obsoleti allowlist-only. |
| `Tools/validation/check_markdown_line_limits/cli.py` | Valida il budget righe Markdown. Usare `--max-lines 400` per policy preferita e `500` come soglia hard. |
| `Tools/validation/check_docs_links/cli.py` | Controlla link Markdown dopo split, rename o pruning. |

Comando tipico:

```powershell
python -m Tools.docs refactor_markdown_splits `
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
| `Tools/ai/build_task_patch_suggestion_report/cli.py` | Estrae suggestion concrete da task Markdown. |
| `Tools/ai/patch_suggestion_bundle/cli.py` | Applica/dry-run deterministic operations da patch suggestion report. |
| `Tools/validation/check_patch_suggestion_product_separation/cli.py` | Separa prodotto essenziale da telemetry/debug supplementare. |
| `Tools/ai/agent_review/review_pr_cli.py` | Prepara branch/commit/PR reviewabile con allowlist/autodiscovery include-path. |

## Validazioni minime

```powershell
python -m py_compile .\\Tools\\docs\\markdown_splits_refactor_core.py .\\Tools\\docs\\refactor_markdown_splits_cli.py
python -m Tools.validation check_docs_links --repo-root .
python -m Tools.validation check_markdown_line_limits --repo-root . --max-lines 500
python -m Tools.validation check_file_line_limits --repo-root . --output .\\output\\validation\\file_line_limits.json
git diff --check
git status --short
```

## Guardrail

Non committare `output/**`, `renders/**`, DB SQLite, chunk generati o patch bundle locali. Le modifiche distruttive devono restare su branch reviewabile e passare da PR.
"""
    lines = write(path, text, apply)
    return {"path": rel(path, root), "action": "write_root_tool_guide", "lines": lines}
