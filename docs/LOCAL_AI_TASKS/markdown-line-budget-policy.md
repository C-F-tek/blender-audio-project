# Markdown line budget policy

## Scopo

Questa policy stabilisce il limite operativo per la documentazione Markdown attiva del progetto IA-Carmine.

## Regola

- Ogni file Markdown attivo dovrebbe restare entro 400 righe.
- Se un file supera il limite, deve diventare un entrypoint breve e puntare a una cartella di parti Markdown.
- La conversione deve essere ricorsiva: anche le parti generate devono rispettare il limite.
- I file sotto `output/**`, `renders/**`, `indexAI/code_chunks/**`, `indexAI/project_code_chunks/**` e `docs/LOCAL_VALIDATION_EVIDENCE/**` sono esclusi dal controllo standard.

## Comandi

Dry-run:

```powershell
python .\Tools\docs\split_large_markdown.py `
  --repo-root . `
  --max-lines 400
```

Apply:

```powershell
python .\Tools\docs\split_large_markdown.py `
  --repo-root . `
  --max-lines 400 `
  --apply
```

Validazione:

```powershell
python .\Toolsalidation\check_markdown_line_limits.py `
  --repo-root . `
  --max-lines 400
```

## Versioning

Versionare solo file sorgente, documentazione e report compatti intenzionali. Non committare `output/**`.
