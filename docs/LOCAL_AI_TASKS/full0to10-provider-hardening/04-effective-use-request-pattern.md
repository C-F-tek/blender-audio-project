# Effective use request pattern

Ogni richiesta al tool effective-use deve essere strutturata come richiesta
operativa, non come prompt generico.

## Forma consigliata

```text
Ottimizza <area> per Full0To10 senza run reale provider, producendo evidence,
telemetry, provider contracts e next actions.
```

## Esempi

```text
Ottimizza uso SQLite FTS5, runtime tools, GPU Ollama e NPU OpenVINO per Full0To10 senza run reale provider.
```

```text
Valuta readiness GPU/NPU/Ollama e produci prodotto qualitativo operativo per decidere il prossimo loop.
```

```text
Genera evidence di memory lane e runtime tool usage per includerla nel bundle finale.
```

## Output atteso

- JSON summary;
- provider hardening contracts;
- tool telemetry;
- SQLite memory report;
- quality product Markdown;
- next actions.

## Criterio qualità

Un output è utile solo se contiene:

- request originale;
- fonti locali;
- evidence search;
- contratti provider;
- warning reali;
- azioni successive ordinabili.
