# Workload quality restore

La patch di safety supervisor ha reso il wrapper sicuro, ma il validator workload
non deve perdere la semantica storica.

## Ripristino

La logica viene divisa in moduli:

```text
Tools/validation/ai_workload_quality/
```

Il wrapper resta:

```text
Tools/validation/check_ai_workload_report_quality.py
```

## Compatibilità

Il launcher può continuare a usare:

```text
--report-dir output/ai_packets/<stamp>
```

senza crash e senza generazione provider.
