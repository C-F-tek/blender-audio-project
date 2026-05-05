# CarmineLike patch loop

Questa directory registra la procedura operativa "CarmineLike" adottata nel
mega-loop Full0To10.

## Definizione

CarmineLike significa:

```text
micro-patch -> zip applicabile -> validazione locale -> commit mirato -> push -> prossima patch
```

Il ciclo privilegia passi grandi ma atomici, con file piccoli e validabili.
