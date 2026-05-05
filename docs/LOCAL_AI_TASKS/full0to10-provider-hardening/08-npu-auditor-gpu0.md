# NPU auditor and GPU.0 contract

## NPU

Ruolo stabile:

```text
sampled_auditor_or_diagnostic
```

La NPU è preziosa per qualità e cross-check, ma non deve guidare la primary
advisory lane senza promozione esplicita.

## GPU.0

Ruolo stabile:

```text
secondary_diagnostic_accelerator
```

OpenVINO `GPU.0` può essere utile, ma non deve rubare la GPU primaria.

## Guardrail

- no model load implicito;
- no provider generation implicita;
- no primary advisory default;
- evidence separata;
- promozione solo tramite patch dedicata.
