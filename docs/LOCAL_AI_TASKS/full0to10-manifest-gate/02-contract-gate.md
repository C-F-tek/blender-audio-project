# Contract gate

Questo documento descrive il contract gate desiderato per il post-bundle.

Stato corrente: non esiste un wrapper PowerShell tracciato con nome canonico per questo gate. Non documentare quindi un comando `-File` eseguibile finché il wrapper non viene aggiunto alla repository e validato.

Il gate deve essere implementato come composizione report-only di due responsabilità:

1. generazione della mappa/manifest della run;
2. validazione che bundle, memory lane e hardware delegation siano visibili nei report finali.

## Componenti logici

```text
full0to10 run manifest builder
full0to10 bundle contract validator
```

Questi nomi sono responsabilità funzionali, non path repository garantiti.

## Uso

```text
Design-only. Creare prima un wrapper tracciato in Tools/workflow, con Param block, smoke e parser PowerShell.
Dopo l'introduzione del wrapper, aggiornare questa sezione con il comando reale.
```
