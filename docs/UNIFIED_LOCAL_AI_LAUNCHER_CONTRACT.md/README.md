<!-- IA-CARMINE-MD-SPLIT: index -->
# Indice — UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md

Documento monolitico trasformato da file `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` a directory-form.
Limite massimo configurato: `400` righe per file Markdown.

## Parti

1. [`part-001.md`](part-001.md)
2. [`part-002.md`](part-002.md)

## Nomenclatura canonica

```text
0Full10 = run unica concettuale
Full0To10 / -Full0To10 = spelling CLI/flag di compatibilità quando presente nel launcher
run unica = workflow completo 0-to-10 sul perimetro attivo del progetto
```

Regola pratica: `0Full10` non deve diventare un flag magico. La run unica deve essere descrivibile dalla combinazione esplicita degli altri parametri: task input, run identity, real-run activation, intensity/budget, provider lanes, evidence lanes, patch/review lanes e opt-out `-No*`. Il flag `-Full0To10`, quando usato, è una scorciatoia compatibile che seleziona quel profilo completo; nel tempo può essere assorbito dalla configurazione esplicita delle lane.

## Guida operativa parametri

Per scegliere correttamente i parametri del launcher senza leggere l'intera superficie CLI, usare:

```text
docs/LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md
```

Regola pratica: scegliere prima la lane/prodotto (`smoke`, fase singola, `0Full10`/run unica, `LightFull0To10`, provider, review PR), poi modificare solo il gruppo di parametri pertinente.

## Mappa profondità capability

Per capire cosa esiste davvero, quanto è profondo, cosa produce e quali potenzialità sono attive o solo target, usare:

```text
docs/LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md
```

Regola pratica: non confondere un target architetturale con una capability eseguita. Una capability è provata solo da manifest, phase report, validator report, telemetry, observer pointer, bundle o report prodotto dalla lane.

## Regola

Split directory-form conforme alla policy: `nomefile.md/part-xxx.md`.
