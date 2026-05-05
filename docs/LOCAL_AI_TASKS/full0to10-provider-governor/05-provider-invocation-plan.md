# Provider invocation plan

Il provider invocation plan è il livello tra permit e run reale.

## Responsabilità

- leggere permit;
- leggere quality gate;
- leggere accelerator control;
- preparare contesto;
- preparare output paths;
- preparare audit NPU;
- fermarsi prima della generazione.

## Safety

```text
generation_executes_now=false
```
