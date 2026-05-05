# Full run TUTTO su TUTTO

Documento operativo per i cambi di logica e parametri della full run.

## Regola

Ogni patch che modifica:

- parametri di avvio;
- default di sicurezza;
- logica supervisor;
- logica quality gate;
- logica provider/tool;
- contratti SQLite/GPU/NPU;

deve aggiornare questa directory documentale.

## Stato corrente

La full run reale resta separata dalla quality lane. La qualità deve produrre
evidenza prima di qualsiasi generazione provider.
