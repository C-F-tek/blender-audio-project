# Agent Runtime Debug Lab — proposta completa

## Stato

- Data: 2026-05-08
- Classificazione proposta: `SAFE_MECHANICAL` per MVP report-only, `LOCAL_VALIDATION_REQUIRED` per smoke, `MANUAL_REVIEW` per broker registration, `DEFER` per integrazione workflow pesante.
- Dipendenza soddisfatta: PR #216 mergeata; le lane workflow devono usare Python di progetto/repo, non Python di sistema.
- Obiettivo: trasformare la capacità di programmazione/debug delle IA da richiesta manuale a tool controllato, tracciato e validabile.

## Problema

Il progetto ha ormai molte lane AI, workflow, validator, patch suggestion e report. Le IA riescono a proporre codice, ma quando serve verificare compile check, smoke mirati o parser PowerShell il ciclo operativo dipende ancora da comandi manuali esterni.

La soluzione non deve diventare una shell libera. Deve essere una capability runtime limitata, dove l'IA produce un piano JSON e il sistema esegue solo operazioni allowlist, timeout-bound e report-only.

## Decisione architetturale

Implementare una nuova capability:

```text
agent_runtime_debug_lab
```

Entry point consigliato:

```text
Tools/ai/agent_runtime_debug_lab.py
```

Moduli interni:

```text
Tools/ai/agent_runtime_debug_lab/policy.py
Tools/ai/agent_runtime_debug_lab/runner.py
Tools/ai/agent_runtime_debug_lab/reporting.py
```

Smoke:

```text
Tools/validation/run_agent_runtime_debug_lab_smoke.py
```

La capability deve essere progettata da subito per tre livelli:

1. MVP locale report-only;
2. registrazione broker;
3. integrazione workflow/prodotto.

## Principi non negoziabili

Il tool deve essere:

- brokerable;
- report-only;
- deterministic-first;
- timeout-bound;
- evidence-producing;
- path-guarded;
- operation-allowlisted;
- compatibile con Python di progetto/repo introdotto dalla policy post-PR #216;
- privo di Git write impliciti;
- privo di provider/Blender/FFmpeg runtime impliciti.

Il tool non deve essere:

- un wrapper bash generico;
- un terminale libero per provider;
- un esecutore di patch;
- un runner Blender;
- un runner FFmpeg;
- un tool Git write;
- un sistema per installare dipendenze.

## Request JSON canonica

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

## Operation type ammessi

MVP:

```text
python_compile
python_script
powershell_parse
git_diff_check
git_status_short
validation_report_contract
json_report_probe
```

Deferred, solo dopo review:

```text
python_test_subset
markdown_link_check
markdown_line_limit_check
workflow_python_policy_check
```

Vietati sempre:

```text
free_shell
git_commit
git_push
git_merge
git_reset
git_clean
patch_apply
pip_install
uv_add
npm_install
terraform_apply
terraform_destroy
blender_run
ffmpeg_run
provider_run
ollama_run
openvino_run
```

## Semantica operation MVP

### python_compile

- input: `paths`;
- esegue equivalente sicuro di `python -m py_compile <paths>`;
- usa Python runtime corrente/progetto;
- accetta solo `.py` sotto path ammessi;
- non accetta path sotto `output/**` come sorgente.

### python_script

- input: `script`, opzionale `args`, opzionale `timeout_seconds`;
- `script` deve essere `.py` ammesso;
- `args` deve essere lista di stringhe;
- non deve accettare una shell string;
- cattura stdout/stderr tail;
- registra return code, durata e timeout;
- accetta output report solo sotto `output/validation/**`.

### powershell_parse

- input: `paths`;
- usa PowerShell parser su `.ps1` ammessi;
- non esegue gli script;
- produce errori parser strutturati.

### git_diff_check

- esegue solo `git diff --check`;
- nessun Git write.

### git_status_short

- esegue solo `git status --short`;
- nessun Git write.

### validation_report_contract

- invoca validator report-contract esistente;
- input report file e output devono rispettare policy;
- output consentito solo sotto `output/validation/**`.

### json_report_probe

- legge report JSON esistenti;
- verifica shape minima: `kind`, `passed`, `errors`, `warnings`;
- non modifica sorgenti.

## Path policy

Path sorgenti ammessi:

```text
Tools/ai/**/*.py
Tools/validation/**/*.py
Tools/docs/**/*.py
Tools/workflow/**/*.ps1
docs/**/*.md
```

Regole:

- `docs/**/*.md` è solo read/probe/validation, mai esecuzione;
- output report scrivibili solo sotto `output/validation/**`;
- ogni path deve essere normalizzato rispetto alla repo root;
- vietare path assoluti fuori repo;
- vietare traversal fuori repo.

Path vietati:

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

## Report JSON/Markdown

Default output:

```text
output/validation/agent_runtime_debug_lab_<stamp>.json
output/validation/agent_runtime_debug_lab_<stamp>.md
```

Shape minima:

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

Markdown report minimo:

- riepilogo passed/failed;
- tabella operations;
- elenco errori;
- guardrail matrix;
- output prodotti.

## Roadmap PR

### PR 1 — MVP report-only

Scopo:

- implementare entrypoint, policy, runner, reporting e smoke;
- nessun broker;
- nessuna integrazione Full0To10 automatica;
- nessuna modifica a patch apply.

File nuovi:

```text
Tools/ai/agent_runtime_debug_lab.py
Tools/ai/agent_runtime_debug_lab/policy.py
Tools/ai/agent_runtime_debug_lab/runner.py
Tools/ai/agent_runtime_debug_lab/reporting.py
Tools/validation/run_agent_runtime_debug_lab_smoke.py
```

Budget linee:

```text
Tools/ai/agent_runtime_debug_lab.py <= 220
Tools/ai/agent_runtime_debug_lab/policy.py <= 260
Tools/ai/agent_runtime_debug_lab/runner.py <= 280
Tools/ai/agent_runtime_debug_lab/reporting.py <= 180
Tools/validation/run_agent_runtime_debug_lab_smoke.py <= 260
```

Smoke PR 1 deve verificare:

- compile di un tool Python ammesso;
- parse di un `.ps1` ammesso;
- `git_diff_check` report-only;
- `git_status_short` report-only;
- rifiuto di path vietato;
- rifiuto di operation type vietato;
- report JSON/MD sotto `output/validation/**`;
- guardrail boolean coerenti.

Validazioni PR 1:

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

Acceptance PR 1:

```text
passed: true
failed_count: 0
```

### PR 2 — Broker registration

Scopo:

- registrare tool broker con `tool_id = runtime_debug_lab`;
- accettare `request_file` e `timeout_seconds`;
- usare helper broker esistente per timeout/stdout/stderr quando possibile;
- evitare duplicazione subprocess se `agent_runtime_tool_broker.py` ha già helper `execute_command_timed()`.

Argomenti broker:

```text
request_file
timeout_seconds
```

Regola linee:

- se `agent_runtime_tool_broker.py` supera 400 righe, non gonfiarlo;
- prima spostare `TOOL_SPECS` o builder in modulo dedicato;
- poi registrare `runtime_debug_lab`.

Validazioni PR 2:

- smoke broker con request file controllato;
- verifica report output;
- verifica che provider execution sia false;
- verifica che shell libera non sia esposta.

### PR 3 — Workflow/product integration

Scopo:

Integrare il lab nel ciclo prodotto solo dopo broker stabile:

```text
patch suggestion apply
-> debug lab mirato sui file cambiati
-> product separation validator
-> prepare_review_pr
```

Regole:

- non always-run pesante;
- registrare in Full0To10 come lane `debug/programming capability`;
- esecuzione attivabile solo quando ci sono file cambiati o richiesta esplicita;
- report incluso nell'evidence bundle, non committato come output.

### PR 4 — Quality gates e regressioni

Scopo:

- aggiungere smoke negativi per path traversal;
- aggiungere smoke per timeout;
- aggiungere smoke per operation type vietato;
- aggiungere smoke per tentativo `pip install`/`git push`/`ffmpeg` come argomento;
- validare che stdout/stderr tail non superi budget.

### PR 5 — UX/task templates

Scopo:

- aggiungere esempi di request JSON;
- aggiungere template task MD per debug lab;
- documentare come usarlo da AI-to-AI bundle;
- documentare quando non usarlo.

## Run completa veloce proposta prima dell'implementazione

Dopo merge PR #216, eseguire run veloce usando questo task come `TaskFile`, in modo da vedere se la pipeline produce proposta coerente prima di implementare codice.

Comando consigliato:

```powershell
$Stamp = "agent_runtime_debug_lab_fast_$(Get-Date -Format 'yyyyMMdd-HHmmss')"
$Task = ".\docs\LOCAL_AI_TASKS\agent-runtime-debug-lab-mvp-2026-05-08.md"

powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File ".\Tools\workflow\run_unified_local_ai_refactor.ps1" `
  -RepoRoot "." `
  -Mode smoke,md,python,context_pack,agent_state,official,provider,patch_specs,contract,full_validation `
  -TaskFile $Task `
  -Stamp $Stamp `
  -SkipGitSync `
  -NoBranch `
  -AllowDirty `
  -NoStrictRealRunActivation `
  -Prod `
  -NoExecutionTail `
  -RunIntensity quick `
  -BudgetMinutes 10 `
  -MaxRounds 8 `
  -FilesPerRound 6 `
  -MaxContextFiles 120 `
  -MaxCharsPerFile 5000 `
  -MaxNewTokens 2400 `
  -KeepAlive 15m `
  -OfficialAdapterTimeoutSeconds 240
```

Se la proposta prodotta è debole o non produce codice sufficiente, procedere manualmente con PR 1 MVP usando questo MD come specifica normativa.

## Rischi principali

### Rischio: shell libera mascherata

Mitigazione:

- operation type enum;
- nessuna command string;
- subprocess solo costruito da argomenti tipizzati.

### Rischio: esecuzione provider involontaria

Mitigazione:

- denylist su script/provider path;
- guardrail boolean obbligatori;
- test negativo per Ollama/OpenVINO direct run.

### Rischio: source write implicito

Mitigazione:

- consentire output solo in `output/validation/**`;
- vietare operations di patch/apply;
- vietare path sorgente sotto output/renders/index chunks.

### Rischio: timeout/hang

Mitigazione:

- timeout default per operation;
- timeout massimo globale;
- stdout/stderr tail limitato.

### Rischio: broker troppo grande

Mitigazione:

- PR2 deve rifattorizzare specs se necessario;
- nessun gonfiaggio monolitico oltre policy linee.

## Criteri di maturità

La capability è matura quando:

- MVP smoke passa;
- broker smoke passa;
- almeno un ciclo patch suggestion -> debug lab -> prepare_review_pr produce evidence utile;
- fallimenti sono diagnostici, non solo return code;
- nessuna lane può eseguire shell libera o provider diretto;
- la documentazione spiega esempi positivi e negativi.

## Decisione operativa

La proposta migliore non è dare shell alla IA. La proposta corretta è introdurre `agent_runtime_debug_lab` come laboratorio runtime controllato:

```text
JSON plan
operation allowlist
path allowlist
timeout
stdout/stderr tail
report JSON/MD
broker integration differita
zero Git/source/provider side effect implicito
```

Prossimo passo consigliato:

1. merge di questo task MD;
2. run veloce usando questo task;
3. se output buono, implementare PR 1 MVP;
4. se output debole, implementare manualmente PR 1 MVP rispettando questa specifica;
5. solo dopo smoke stabile procedere con PR2/PR3.
