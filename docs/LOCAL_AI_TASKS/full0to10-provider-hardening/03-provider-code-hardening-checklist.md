# Provider code hardening checklist

Questa checklist guida le patch future sul codice provider e sul wiring runtime.

## Principi

- nessun provider viene eseguito implicitamente;
- ogni provider espone capability prima di generare;
- ogni provider produce telemetry dopo ogni invocazione;
- ogni errore provider deve diventare JSON diagnosticabile;
- ogni fallback deve essere esplicito nel report.

## Ollama/GPU

Controlli richiesti:

1. `ollama list` disponibile;
2. `ollama ps` disponibile;
3. modello target dichiarato;
4. GPU primaria dichiarata;
5. timeout dichiarato;
6. keep-alive dichiarato;
7. max-new-tokens dichiarato;
8. no prompt generation in preflight;
9. workload report quality passato;
10. telemetry runtime allegata al bundle.

## NPU/OpenVINO

Controlli richiesti:

1. import OpenVINO;
2. lista device disponibile;
3. `NPU` rilevato quando presente;
4. `GPU.0` documentato come secondary;
5. nessun model load nel preflight;
6. sampled auditor contract dichiarato;
7. output separato dalla primary advisory lane.

## SQLite FTS5/tool

Controlli richiesti:

1. schema init;
2. namespace obbligatorio;
3. ingest request;
4. ingest context;
5. FTS/hybrid search;
6. telemetry tool;
7. quality product Markdown;
8. DB sotto output o path ignorato;
9. niente commit DB.
