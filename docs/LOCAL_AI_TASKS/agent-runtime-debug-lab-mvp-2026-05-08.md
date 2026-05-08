# Agent Runtime Debug Lab — MVP report-only task

## Stato

- Data: 2026-05-08
- Classificazione MVP: `SAFE_MECHANICAL`
- Validazione: `LOCAL_VALIDATION_REQUIRED`
- Broker registration: `MANUAL_REVIEW`, fuori da questa PR
- Full0To10 integration: `DEFER`, fuori da questa PR
- Dipendenza soddisfatta: PR #216 mergeata; le lane workflow devono usare Python di progetto/repo, non Python di sistema.

## Obiettivo operativo

Implementare un nuovo tool report-only per dare alle IA capacità controllate di debug/programmazione senza esporre una shell libera.

Nome consigliato:

```text
Tools/ai/agent_runtime_debug_lab.py
```

Package/moduli:

```text
Tools/ai/agent_runtime_debug_lab/policy.py
Tools/ai/agent_runtime_debug_lab/runner.py
Tools/ai/agent_runtime_debug_lab/reporting.py
Tools/validation/run_agent_runtime_debug_lab_smoke.py
```

Il tool deve accettare un piano JSON, validarlo tramite policy allowlist, eseguire solo operation type consentite, applicare timeout, produrre report JSON/Markdown e non avere side effect impliciti su Git, sorgenti, provider, Blender o FFmpeg.

## Non-obiettivi

Non implementare in questa PR:

- broker registration;
- Full0To10 automatic lane;
- patch apply;
- Git write;
- shell libera;
- provider/Ollama/OpenVINO run diretto;
- Blender runtime;
- FFmpeg runtime;
- installazioni package (`pip install`, `uv add`, `npm install`).

## Design richiesto

Il nuovo tool deve essere:

- brokerable;
- report-only;
- deterministic-first;
- timeout-bound;
- evidence-producing;
- compatibile con Python di progetto/repo introdotto dalla policy post-PR #216;
- eseguibile localmente tramite smoke controllato.

## Input JSON previsto

Esempio di richiesta:

```json
{
  "kind": "agent_runtime_debug_lab_request",
  "schema_version": 1,
  "operations": [
    {
      "id": "compile_ai_tool",
      "type": "python_compile",
      "paths": ["Tools/ai/build_task_patch_suggestion_report.py"]
    },
    {
      "id": "run_smoke",
      "type": "python_script",
      "script": "Tools/validation/run_patch_suggestion_bundle_apply_smoke.py",
      "args": ["--repo-root", ".", "--output", "output/validation/debug_lab_smoke.json"],
      "timeout_seconds": 240
    },
    {
      "id": "ps_parser",
      "type": "powershell_parse",
      "paths": ["Tools/workflow/run_unified_local_ai_refactor.ps1"]
    },
    {
      "id": "diff_check",
      "type": "git_diff_check"
    }
  ]
}
```

## Operation type ammessi per MVP

Implementare solo questi operation type:

```text
python_compile
python_script
powershell_parse
git_diff_check
git_status_short
validation_report_contract
json_report_probe
```

### Semantica operation

`python_compile`:

- input: `paths`
- usa Python runtime corrente/progetto;
- esegue compile check equivalente a `python -m py_compile <paths>`;
- path soggetti a allowlist.

`python_script`:

- input: `script`, opzionale `args`, opzionale `timeout_seconds`;
- `script` deve essere un file `.py` ammesso;
- `args` devono essere lista di stringhe, non una shell string;
- cattura stdout/stderr tail;
- registra return code e durata;
- non consente script sotto path vietati.

`powershell_parse`:

- input: `paths`;
- usa PowerShell parser per file `.ps1` ammessi;
- non esegue gli script;
- produce errori parser strutturati.

`git_diff_check`:

- esegue solo `git diff --check`;
- nessun git write.

`git_status_short`:

- esegue solo `git status --short`;
- nessun git write.

`validation_report_contract`:

- invoca il validator di contract report esistente solo con file consentiti;
- output sotto `output/validation/**` consentito come report generato.

`json_report_probe`:

- legge report JSON esistenti;
- verifica `kind`, `passed`, `errors`, `warnings` e presenza file;
- non modifica sorgenti.

## Path ammessi nel MVP

Path sorgenti ammessi per operazioni di lettura/compile/parser/script controllato:

```text
Tools/ai/**/*.py
Tools/validation/**/*.py
Tools/docs/**/*.py
Tools/workflow/**/*.ps1
docs/**/*.md
```

Note:

- `docs/**/*.md` è solo per validazione/read/probe, non per esecuzione.
- Gli output report possono essere scritti sotto `output/validation/**`.
- I path devono essere normalizzati rispetto alla repo e non possono uscire dalla repo root.

## Path vietati

Bloccare sempre:

```text
output/** come target sorgente
renders/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
*.db
*.sqlite
*.sqlite3
Scripting/** per esecuzione runtime
```

## Comandi vietati

Il tool non deve accettare stringhe shell arbitrarie. Vietare esplicitamente:

```text
git commit
git push
git merge
git reset
git clean
Remove-Item / del / rm su sorgenti
pip install
uv add
npm install
terraform apply/destroy
Blender
FFmpeg
provider/Ollama/OpenVINO run diretto
```

## Output report richiesto

Default output:

```text
output/validation/agent_runtime_debug_lab_<stamp>.json
output/validation/agent_runtime_debug_lab_<stamp>.md
```

Shape minima JSON:

```json
{
  "kind": "agent_runtime_debug_lab",
  "schema_version": 1,
  "passed": true,
  "operation_count": 4,
  "failed_count": 0,
  "operations": [
    {
      "id": "run_smoke",
      "type": "python_script",
      "executed": true,
      "returncode": 0,
      "elapsed_seconds": 2.431,
      "stdout_tail": "...",
      "stderr_tail": "",
      "outputs": ["output/validation/debug_lab_smoke.json"]
    }
  ],
  "guardrails": {
    "free_shell_exposed": false,
    "allowlist_enforced": true,
    "provider_execution_performed": false,
    "patch_application_performed": false,
    "source_writes_performed": false,
    "git_write_performed": false,
    "blender_runtime_execution_performed": false,
    "ffmpeg_runtime_execution_performed": false
  }
}
```

## File target e budget linee

```text
Tools/ai/agent_runtime_debug_lab.py <= 220
Tools/ai/agent_runtime_debug_lab/policy.py <= 260
Tools/ai/agent_runtime_debug_lab/runner.py <= 280
Tools/ai/agent_runtime_debug_lab/reporting.py <= 180
Tools/validation/run_agent_runtime_debug_lab_smoke.py <= 260
```

## Smoke richiesto

`Tools/validation/run_agent_runtime_debug_lab_smoke.py` deve creare una richiesta temporanea o fixture controllata e verificare almeno:

- compile di un tool Python ammesso;
- parse di un `.ps1` ammesso;
- `git_diff_check` report-only;
- `git_status_short` report-only;
- rifiuto di almeno un path vietato (`output/**` come sorgente o `*.sqlite`);
- rifiuto di operation type non ammesso;
- report JSON/MD prodotti sotto `output/validation/**`;
- guardrail boolean coerenti.

## Validazioni richieste per PR MVP

```powershell
python -m py_compile .\Tools\ai\agent_runtime_debug_lab.py
python -m py_compile .\Tools\ai\agent_runtime_debug_lab\policy.py
python -m py_compile .\Tools\ai\agent_runtime_debug_lab\runner.py
python -m py_compile .\Tools\ai\agent_runtime_debug_lab\reporting.py
python -m py_compile .\Tools\validation\run_agent_runtime_debug_lab_smoke.py

python .\Tools\validation\run_agent_runtime_debug_lab_smoke.py `
  --repo-root . `
  --output .\output\validation\agent_runtime_debug_lab_smoke.json `
  --markdown-output .\output\validation\agent_runtime_debug_lab_smoke.md

git diff --check
git status --short
```

Expected smoke:

```text
passed: true
failed_count: 0
```

## Acceptance criteria

La PR MVP è accettabile solo se:

- non introduce shell libera;
- non introduce Git write;
- non introduce provider/Blender/FFmpeg runtime;
- non scrive sorgenti;
- non committa `output/**`;
- produce report JSON/MD deterministici;
- rifiuta operation type e path vietati;
- ogni file nuovo resta sotto il budget linee indicato;
- smoke locale passa.

## Deferred PR 2 — Broker registration

Solo dopo MVP stabile:

```text
tool_id = runtime_debug_lab
args = request_file, timeout_seconds
```

Nota: se `agent_runtime_tool_broker.py` supera la policy linee, spostare `TOOL_SPECS` o builder in modulo dedicato prima di aggiungere il nuovo tool.

## Deferred PR 3 — Workflow/product integration

Solo dopo broker stabile:

```text
patch suggestion apply
-> debug lab mirato sui file cambiati
-> product separation validator
-> prepare_review_pr
```

In Full0To10 registrare come lane `debug/programming capability`, non come always-run pesante.
