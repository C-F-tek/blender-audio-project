# Code-aware Markdown coherence policy

## Scopo

Questa policy definisce il prossimo ciclo di refactor documentale IA-Carmine:
la documentazione Markdown deve essere riallineata al codice reale, non a memoria
storica, prompt precedenti o runbook obsoleti.

## Fonte primaria

Ordine operativo:

1. codice Python e PowerShell attuale;
2. contratti CLI visibili da `argparse.add_argument()` e `param(...)`;
3. launcher e wrapper workflow correnti;
4. report JSON/MD locali generati dai validator;
5. documentazione Markdown attiva;
6. evidence storica solo come contesto, non come sorgente attiva.

## Vincoli

- I Markdown attivi devono restare sotto 400 righe.
- File superiori a 400 righe devono diventare stub + cartella `.md` con parti.
- Non aggiornare documentazione copiando blocchi lunghi da `output/**`.
- Non committare `output/**`, `renders/**`, `*.db`, `*.sqlite`.
- Non eseguire Blender, FFmpeg o provider reali durante il refactor documentale.
- Non applicare patch automatiche sui finding senza classificazione.

## Classificazione finding

Ogni riferimento rotto va classificato prima di correggerlo:

- `active-current`: deve puntare a un file esistente o a un nuovo file da creare;
- `historical`: deve essere marcato come storico o rimosso dai runbook attivi;
- `evidence-only`: deve restare nei bundle/evidence, non nei percorsi operativi;
- `stale`: va rimosso o sostituito;
- `future`: va indicato come backlog/task, non come comando presente.

## Output attesi

Il ciclo produce:

- `output/validation/md_code_coherence_report.json`;
- `output/validation/md_code_coherence_report.md`;
- `docs/LOCAL_AI_TASKS/code-aware-tool-index.md`;
- `docs/LOCAL_AI_TASKS/md-code-coherence-current-state.md`;
- `docs/LOCAL_AI_TASKS/code-aware-command-contract.md`.

I file sotto `docs/LOCAL_AI_TASKS/` sono versionabili se validati e sotto 400 righe.

## Criterio di stop

Fermare il ciclo se:

- il working tree contiene modifiche inattese;
- il report genera high finding non classificati;
- un Markdown generato supera 400 righe;
- un comando documentato usa flag non presenti nel contratto codice;
- `git diff --check` fallisce;
- compaiono file staged sotto `output/**`.
