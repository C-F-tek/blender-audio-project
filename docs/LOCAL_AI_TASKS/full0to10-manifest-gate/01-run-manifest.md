# Run manifest

Il manifest Full0To10 indicizza ricorsivamente le radici operative:

```text
docs/LOCAL_VALIDATION_EVIDENCE
output/validation
output/ai_pipeline
output/ai_packets
output/patch_specs
output/semantic_chunks
```

Classifica gli artifact in ruoli:

- CSV/index/discovery;
- telemetry;
- capability;
- provider diagnostics;
- decision loop;
- recommendations;
- patch plan;
- evidence bundle.

Il manifest non include contenuto di DB SQLite o artifact vietati.
