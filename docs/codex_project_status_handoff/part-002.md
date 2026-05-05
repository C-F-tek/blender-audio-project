<!-- IA-CARMINE-MD-SPLIT: part -->
# codex_project_status_handoff — parte 002 di 002

Sorgente indice: [`../codex_project_status_handoff.md`](../codex_project_status_handoff.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)

## Technical debt attuale rilevante

Vedi:

```text
docs/TECH_DEBT_TRACKER.md
```

Item principali ancora aperti:

```text
TD-001 PowerShell runner compatibility
TD-003 Blender shared compatibility not runtime validated
TD-004 Ready To Jazz monolithic package
TD-005 v61b_backgood backup folder
TD-006 Formal JSON schemas partial
TD-007 NPU pipeline decomposition
```

Item risolti recentemente:

```text
TD-002 JSON validation UTF-8 BOM
TD-008 Documentation link validation
TD-009 Refactor status consistency
```

## Prossimo task consigliato

### Task A — aggiornare runner unattended con i nuovi validator

File da modificare:

```text
Tools/workflow/run_local_validation_after_refactor.ps1
```

Aggiungere questi step dopo `ai pipeline module smoke validation` e prima della dry-run matrix:

```powershell
python .\Tools\validation\check_refactor_status_consistency.py --repo-root . --output .\output\validation\refactor_status_consistency.json
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
```

Aggiornare anche summary Markdown del runner se utile.

Validazione dopo modifica:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError
```

### Task B — creare execution plan per `blender_compat.py`

Creare:

```text
docs/EXECUTION_PLANS/active/2026-04-29_blender_compat_manual_smoke.md
```

Obiettivo: pianificare test manuale Blender per:

```text
create_sound_strip
clear_sequence_editor
set_frame_range_from_seconds
safe_create_noise_texture_node
```

Non migrare ancora nessun runtime package.

### Task C — creare manual smoke script per Blender

Possibile file futuro:

```text
Tools/blender/smoke_test_blender_compat.py
```

Oppure:

```text
Scripting/shared/tests/manual_blender_compat_smoke.py
```

Da eseguire dentro Blender, non da Python normale.

## Output richiesto a Codex dopo ogni modifica

Codex deve restituire:

```text
changed files
purpose
line counts for scripts created or modified
validation commands run
validation results
risks
next recommended action
```

## Stato attuale in una frase

Il progetto è stato portato a una forma più agent-first: pipeline AI modulare validata, reportistica dry-run Markdown/JSON, workflow root, execution plans, tech debt tracker, validator per coerenza refactor e link docs; il prossimo passo è integrare i nuovi validator nel runner locale e poi preparare il test Blender manuale per `Scripting/shared/blender_compat.py`.
