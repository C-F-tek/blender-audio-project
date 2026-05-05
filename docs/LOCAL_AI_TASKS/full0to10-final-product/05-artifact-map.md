# Artifact map

Questa mappa collega gli artifact del prodotto finale al loro scopo operativo.

## Product markdown

```text
full0to10_final_tool_product.md
```

Scopo:

- lettura umana;
- handoff AI-to-AI;
- sintesi decisionale;
- riepilogo blocker.

## Product manifest

```text
full0to10_final_tool_product_manifest.json
```

Scopo:

- lettura macchina;
- validazione automatica;
- inclusione bundle;
- tracciamento output.

## Evidence index

```text
full0to10_final_tool_product_evidence_index.json
```

Scopo:

- verificare artifact obbligatori;
- segnalare evidence mancante;
- impedire run basata su intuizione.

## Readiness

```text
full0to10_final_tool_product_readiness.json
```

Scopo:

- distinguere product review da real provider run;
- dichiarare blocker;
- dichiarare warning;
- dare score operativo.

## Effective use summary

```text
effective_use/full0to10_effective_use_summary.json
```

Scopo:

- dimostrare che SQLite FTS5 e tool sono stati usati;
- collegare request a output;
- esporre telemetry;
- esporre provider hardening.

## Quality product

```text
effective_use/full0to10_effective_use_quality_product.md
```

Scopo:

- produrre output qualitativo da richiesta tool;
- usare evidence locale;
- non usare generazione provider.

## Provider contracts

```text
effective_use/full0to10_provider_hardening_contracts.json
```

Scopo:

- fissare ruolo GPU/Ollama;
- fissare ruolo NPU/OpenVINO;
- fissare ruolo OpenVINO GPU.0;
- impedire promozioni implicite.

## Tool telemetry

```text
effective_use/full0to10_effective_use_tool_telemetry.json
```

Scopo:

- contare tool usati;
- registrare azioni;
- segnalare errori;
- rendere verificabile il lavoro.

## Quality gate

```text
quality_gate/full0to10_quality_gate.json
```

Scopo:

- verificare precondizioni;
- bloccare source-side artifact;
- esporre readiness preliminare;
- mantenere separata la run reale.
