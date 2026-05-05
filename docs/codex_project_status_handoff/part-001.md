<!-- IA-CARMINE-MD-SPLIT: part -->
# codex_project_status_handoff — parte 001 di 002

Sorgente indice: [`../codex_project_status_handoff.md`](../codex_project_status_handoff.md)

## Navigazione

- [Indice](README.md)
- [Parte successiva](part-002.md)

# Codex Handoff — blender-audio-project

Data: 2026-04-29
Repository: `C-F-tek/blender-audio-project`
Branch principale: `master`

## Scopo di questo documento

Questo file è un handoff operativo da dare a Codex o a un altro agente locale.

Serve per capire rapidamente:

- che progetto è;
- quale refactor è stato appena fatto;
- quali file leggere prima di lavorare;
- quali validazioni eseguire;
- quali aree non toccare;
- qual è il prossimo lavoro consigliato.

## Sintesi del progetto

`blender-audio-project` è un workspace Python/Blender per generare visual audio-reactive partendo da file audio e JSON di analisi.

Flusso principale:

```text
audio file
  -> audio analysis JSON
  -> compact music/context data
  -> AI artifact pipeline
  -> Blender Python package / scene script
  -> rendered image sequence
  -> FFmpeg final video encode
```

Il progetto contiene:

```text
root tools Python
Scripting/ packages Blender
Scripting/shared/ utility riusabili
Tools/ai/ pipeline AI modulare
Tools/npu/ indicizzazione, contesto e tooling locale AI/NPU
Tools/validation/ validator non invasivi
Tools/workflow/ runner locali
indexAI/ indici generati per AI
patch_specs/ patch spec reviewabili
docs/ documentazione stabile e AI-friendly
```

## Stato corrente validato

La pipeline AI modulare è stata validata localmente.

Risultati recenti:

```text
Python syntax validation: PASS
AI pipeline module smoke validation: PASS
AI pipeline dry-run matrix: PASS
Package structure validation: PASS
JSON artifact validation: PASS
Project AI index generation: PASS
NPU code context generation: PASS
```

La dry-run matrix produce:

```text
output/ai_pipeline/dry_run_matrix_report.json
output/ai_pipeline/dry_run_matrix_report.md
```

L’ultimo report Markdown locale mostrava 5 casi su 5 `PASS`:

```text
base
no_auto_remediation
no_npu_guardrail
with_validation
with_chunks
```

## Refactor già completato

### 1. AI artifact pipeline modulare

La pipeline prima era più concentrata nell’entrypoint. Ora è divisa in moduli sotto:

```text
Tools/ai/pipeline/
```

Moduli principali:

```text
Tools/ai/pipeline/defaults.py
Tools/ai/pipeline/models.py
Tools/ai/pipeline/runner.py
Tools/ai/pipeline/compat.py
Tools/ai/pipeline/artifact_contracts.py
Tools/ai/pipeline/cli.py
Tools/ai/pipeline/preflight.py
Tools/ai/pipeline/steps.py
Tools/ai/pipeline/scheduler.py
Tools/ai/pipeline/orchestrator.py
Tools/ai/pipeline/schema_report.py
Tools/ai/pipeline/markdown_report.py
Tools/ai/pipeline/guardrail_models.py
Tools/ai/pipeline/remediation.py
Tools/ai/pipeline/refactor_status.py
```

Entrypoint da mantenere sottile:

```text
Tools/ai/run_parallel_artifact_pipeline.py
```

Dry-run matrix:

```text
Tools/ai/run_pipeline_dry_run_matrix.py
```

Status marker:

```text
Tools/ai/pipeline/refactor_status.py
```

### 2. Report Markdown per dry-run matrix

Aggiunto:

```text
Tools/ai/pipeline/markdown_report.py
```

Ora la matrix scrive anche:

```text
output/ai_pipeline/dry_run_matrix_report.md
```

### 3. Shared Blender compatibility helper

Aggiunto:

```text
Scripting/shared/blender_compat.py
```

Funzioni principali:

```text
require_bpy
get_scene
ensure_sequence_editor
clear_sequence_editor
create_sound_strip
safe_set_scene_sync_audio
safe_create_node
safe_create_noise_texture_node
set_frame_range_from_seconds
set_render_fps
```

Importante: non è ancora adottato nei package runtime. Prima serve test manuale dentro Blender.

### 4. Runner locale unattended

Aggiunto:

```text
Tools/workflow/run_local_validation_after_refactor.ps1
```

Serve per eseguire validazione lunga locale.

### 5. Workflow agent-first e controllo task

Aggiunti:

```text
WORKFLOW.md
docs/EXECUTION_PLANS/README.md
docs/EXECUTION_PLANS/active/README.md
docs/EXECUTION_PLANS/completed/README.md
docs/EXECUTION_PLANS/abandoned/README.md
docs/TECH_DEBT_TRACKER.md
```

### 6. Validator aggiunti

Aggiunti:

```text
Tools/validation/check_refactor_status_consistency.py
Tools/validation/check_docs_links.py
```

`check_refactor_status_consistency.py` controlla coerenza tra:

```text
Tools/ai/pipeline/refactor_status.py
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/AI_PIPELINE_ARCHITECTURE.md
docs/PROJECT_AI_CONSCIOUSNESS.md
AGENTS.md
```

`check_docs_links.py` controlla link Markdown locali, ignorando URL esterni e cartelle output/cache.

## Fix già applicati durante validazione locale

Sono stati corretti vari bug emersi durante test reali su Windows/PowerShell:

```text
PowerShell runner:
- rimosse code fence Markdown con backtick da stringhe PowerShell
- evitata collisione con variabile automatica $args
- tollerato stderr nativo di git
- reso array-safe il conteggio dei risultati

AI pipeline:
- remedial_steps ora accetta GuardrailPlan, list, tuple o dict legacy

JSON validator:
- check_json_artifacts.py legge UTF-8 con o senza BOM usando utf-8-sig
```

## Documenti da leggere prima di lavorare

Ordine consigliato:

```text
AGENTS.md
WORKFLOW.md
README.md
docs/README.md
docs/PROJECT_AI_CONSCIOUSNESS.md
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/AI_PIPELINE_ARCHITECTURE.md
docs/GITHUB_LOCAL_VALIDATION_WORKFLOW.md
docs/AI_EXTERNAL_KNOWLEDGE.md
docs/OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md
docs/EXECUTION_PLANS/README.md
docs/TECH_DEBT_TRACKER.md
docs/MODULE_MAP.md
docs/DATA_FLOW.md
docs/REFACTORING_AND_REUSE_PLAN.md
docs/QUALITY_GATE.md
Tools/validation/README.md
Scripting/shared/README.md
```

## Regole operative per Codex

### Fare

- Leggere i documenti prima di modificare.
- Fare modifiche piccole e mirate.
- Preferire documentazione e validator additivi.
- Eseguire validazioni locali.
- Rigenerare gli indici AI/NPU dopo modifiche strutturali.
- Segnalare file cambiati, motivazione e comandi di test.
- Indicare line count per script creati o modificati.

### Non fare senza conferma

```text
non cancellare file
non riscrivere Scripting/v61b/main_v61b.py
non splittare subito Ready To Jazz monolith
non migrare runtime packages a blender_compat senza test Blender
non cambiare comportamento render/FFmpeg
non modificare full frame-level analysis JSON
non aggiungere dipendenze
non cambiare schema-v6 della pipeline
non lanciare render Blender lunghi o workload GPU pesanti
```

## Comandi di validazione principali

### Validazione base

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
```

### Validazione pipeline AI

```powershell
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\validation\check_refactor_status_consistency.py --repo-root . --output .\output\validation\refactor_status_consistency.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
```

### Runner unattended

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -ContinueOnError
```

Nota: dopo l’aggiunta dei due nuovi validator, il runner potrebbe dover essere aggiornato per includerli direttamente.

### Rigenerazione indici

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

File generati tipici:

```text
indexAI/project_code_index.md
indexAI/project_code_manifest.json
Tools/npu/npu_code_context.md
Tools/npu/npu_code_index.md
Tools/npu/npu_code_manifest.json
```

## Stato Git atteso dopo lavoro locale

Dopo rigenerazione indici, se cambiano solo questi file:

```text
Tools/npu/npu_code_context.md
Tools/npu/npu_code_index.md
Tools/npu/npu_code_manifest.json
indexAI/project_code_index.md
indexAI/project_code_manifest.json
```

commit consigliato:

```powershell
git add Tools/npu/npu_code_context.md `
        Tools/npu/npu_code_index.md `
        Tools/npu/npu_code_manifest.json `
        indexAI/project_code_index.md `
        indexAI/project_code_manifest.json

git commit -m "chore: regenerate ai and npu indexes"
git push origin master
```
