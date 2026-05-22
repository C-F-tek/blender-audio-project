# Code-aware Markdown coherence policy

## Scopo

Questa policy governa il refactor documentale IA-Carmine quando i Markdown devono essere riallineati al codice reale.

La documentazione attiva non deve essere aggiornata da memoria storica, prompt precedenti o evidence obsolete. Deve partire da codice, CLI, wrapper, validator e report correnti.

## Fonti primarie

Ordine operativo:

1. codice Python e PowerShell attuale;
2. contratti CLI visibili da `argparse.add_argument()` e `param(...)`;
3. launcher e wrapper workflow correnti;
4. report JSON/MD generati localmente dai validator;
5. documentazione Markdown attiva;
6. evidence storica solo come contesto, non come sorgente attiva.

## Policy Markdown

- I Markdown attivi devono restare sotto 700 righe.
- File oltre budget diventano stub breve + cartella di parti Markdown.
- La trasformazione deve essere ricorsiva se una parte supera ancora il budget.
- Root README/WORKFLOW devono restare descrittivi e rimandare ai runbook canonici.
- I comandi lunghi vivono nei runbook proprietari o in mappe generate compatte.

## Guardrail

- Non committare `output/**`, `renders/**`, `*.db`, `*.sqlite`.
- Non committare `indexAI/code_chunks/**` o `indexAI/project_code_chunks/**`.
- Non eseguire Blender, FFmpeg o provider reali durante il refactor documentale.
- Non ricreare file mancanti solo per soddisfare link storici.
- Non applicare patch automatiche su finding non classificati.

## Classificazione finding

Ogni riferimento rotto va classificato prima di correggerlo:

- `active-current`: deve puntare a un file esistente o a un nuovo file deliberatamente creato;
- `historical`: va marcato come storico o rimosso dai runbook attivi;
- `evidence-only`: resta in bundle/evidence, non nei percorsi operativi;
- `stale`: va rimosso o sostituito;
- `future`: va indicato come backlog/task, non come comando presente.

## Output attesi

Il ciclo code-aware produce:

- `output/validation/md_code_coherence_report.json`;
- `output/validation/md_code_coherence_report.md`;
- `output/validation/md_code_coherence_check.json`;
- `docs/LOCAL_AI_TASKS/code-aware-tool-index.md`;
- `docs/LOCAL_AI_TASKS/md-code-coherence-current-state.md`;
- `docs/LOCAL_AI_TASKS/code-aware-command-contract.md`.

I primi tre sono artifact locali non versionabili; gli ultimi tre sono Markdown compatti versionabili.

## Regola finale

Prima di cancellare o riscrivere un Markdown attivo, leggere il codice collegato e verificare se il riferimento è attivo, storico, evidence-only, stale o futuro.
