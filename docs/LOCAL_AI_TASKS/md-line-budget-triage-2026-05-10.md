# Markdown line-budget triage — 2026-05-10

## Policy applicata

Owner validator:

- `python -m Tools.validation check_file_line_limits`

Soglia operativa corrente:

- default hard limit: 400 righe per file monitorato;
- policy storica README: runbook attivo preferito entro 400 righe;
- Markdown oltre soglia: trasformare in indice compatto o directory-form split controllato;
- non fare split cieco se il file contiene anchor usati da smoke/validator.

Il validator esclude runtime/generated paths come `output/**`, `renders/**`, `indexAI/code_chunks/**`, `indexAI/project_code_chunks/**`.

## Stato dei nuovi documenti real product

| Documento | Stato policy | Azione |
|---|---|---|
| `real-product-run-doc-index-2026-05-10.md` | indice compatto | Keep. |
| `real-product-run-unica-runbook-2026-05-10.md` | runbook dedicato | Keep; non espandere oltre. |
| `documentation-code-alignment-audit-2026-05-10.md` | audit compatto | Keep. |
| `problems-and-hygiene-candidates-2026-05-10.md` | backlog igiene compatto | Keep; se cresce, split P0/P1/P2/P3. |

Questi documenti sono nati per scaricare `Tools/workflow/README.md`, non per duplicarne la lunghezza.

## File storici da trattare con cautela

### `Tools/workflow/README.md`

Classificazione:

- sovradimensionato;
- contiene anchor usati da smoke validator;
- contiene contratti storici e correnti;
- non va tagliato senza aggiornare test/validator.

Azione safe:

1. mantenerlo come router generale;
2. aggiungere solo link a documenti dedicati;
3. spostare progressivamente sezioni storiche in documenti split;
4. mantenere marker HTML `IA-CARMINE-*` finché i validator li cercano.

Candidate split future:

- `docs/LOCAL_AI_TASKS/workflow-readme-contracts/README.md`;
- `docs/LOCAL_AI_TASKS/workflow-readme-contracts/part-001-current-routing.md`;
- `docs/LOCAL_AI_TASKS/workflow-readme-contracts/part-002-real-product-contracts.md`;
- `docs/LOCAL_AI_TASKS/workflow-readme-contracts/part-003-runtime-evidence-contracts.md`;
- `docs/LOCAL_AI_TASKS/workflow-readme-contracts/part-004-legacy-aliases.md`.

Stop condition:

- non rimuovere anchor `IA-CARMINE-*` senza aggiornare gli smoke che li richiedono.

### `Tools/ai/README.md`

Classificazione:

- probabile file lungo da controllare con validator;
- prima leggere owner sections e anchor;
- non fare split automatico se è usato da docs/tests.

Azione safe:

- generare report line-limit;
- se over-limit, creare index + split directory-form solo con mapping sezione -> file;
- preservare link relativi.

### Documenti AI pipeline storici

Candidati da validare con `check_file_line_limits.py`:

- `docs/AI_PIPELINE_REFACTOR_STATUS.md`;
- `docs/AI_PIPELINE_ARCHITECTURE.md`;
- `docs/AI_ARTIFACT_SCHEMAS.md`;
- `docs/README.md`.

Azione safe:

- non aggiornare contenuto tecnico in massa;
- prima produrre report line-limit;
- poi decidere index/split per documento.

## Comando validator consigliato

~~~powershell
$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path

& $RepoPy -m Tools.validation check_file_line_limits `
  --repo-root . `
  --output .\output\validation\file_line_limits.json `
  --markdown-output .\output\validation\file_line_limits.md
~~~

Per farlo diventare bloccante in una PR dedicata:

~~~powershell
& $RepoPy -m Tools.validation check_file_line_limits `
  --repo-root . `
  --output .\output\validation\file_line_limits.json `
  --markdown-output .\output\validation\file_line_limits.md `
  --fail-on-violations
~~~

## Regola operativa per domani

1. Non espandere README già lunghi.
2. Ogni nuovo runbook deve restare sotto 400 righe.
3. Se un runbook supera 400 righe, trasformarlo in indice + parti.
4. Se un file lungo contiene anchor validator, prima aggiornare validator/smoke o lasciare anchor nel file indice.
5. Se si splitta, usare directory-form `.md` riconosciuta dal validator:
   - contenitore `qualcosa.md/`;
   - `README.md` come indice;
   - `part-001-*.md`, `part-002-*.md` come parti.
6. Non splittare generated/runtime docs dentro `output/**` perché sono esclusi e non sono sorgente.

## Candidati igiene line-budget

| Priorità | Candidato | Motivo |
|---|---|---|
| P1 | `Tools/workflow/README.md` | lungo, ma con anchor validator: split controllato. |
| P2 | `Tools/ai/README.md` | probabile runbook tecnico cresciuto troppo. |
| P2 | `docs/AI_PIPELINE_ARCHITECTURE.md` | possibile documento storico monolitico. |
| P2 | `docs/AI_ARTIFACT_SCHEMAS.md` | possibile schema doc da indicizzare. |
| P3 | `docs/README.md` | solo se supera soglia o duplica altri indici. |

## Validazione attesa dopo una patch docs

~~~powershell
$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path

& $RepoPy -m Tools.validation check_file_line_limits `
  --repo-root . `
  --output .\output\validation\file_line_limits.json `
  --markdown-output .\output\validation\file_line_limits.md

git diff --check
~~~

Se la patch tocca anchor README, aggiungere anche gli smoke specifici che cercano quegli anchor.
