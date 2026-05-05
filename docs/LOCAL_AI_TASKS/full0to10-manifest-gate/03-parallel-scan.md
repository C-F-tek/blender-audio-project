# Parallel scan

Il manifest builder usa thread paralleli per scansionare più radici senza bloccare
il flusso su una sola directory.

## Default

```text
Workers: 6
```

Aumentare il valore solo se il filesystem locale resta reattivo.

## Regola

Il parallelismo serve alla discovery e alla classificazione, non autorizza:

- patch apply automatico;
- write persistente SQLite;
- Blender runtime;
- FFmpeg/media output;
- commit di `output/**`.
