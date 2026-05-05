# Package contract

Il pacchetto prodotto finale deve essere autosufficiente.

## File richiesti

```text
README.md
full0to10_final_tool_product.md
full0to10_final_tool_product_manifest.json
full0to10_final_tool_product_evidence_index.json
full0to10_final_tool_product_readiness.json
```

## Evidence obbligatorie

- `effective_use_summary`;
- `quality_product`;
- `provider_hardening`;
- `tool_telemetry`;
- `optimization`;
- `quality_gate`.

## Guardrail

Il package deve dichiarare:

```text
provider_execution_performed=false
patch_application_performed=false
source_writes_performed=false
persistent_memory_write_performed=false
```

## Non versionare

Il contenuto generato sotto `output/**` non va committato. Si committano solo
tool, workflow, validatori e documentazione.
