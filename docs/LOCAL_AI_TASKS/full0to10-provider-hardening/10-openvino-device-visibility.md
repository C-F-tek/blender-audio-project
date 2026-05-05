# OpenVINO device visibility

La visibilità device è parte del provider hardening.

## Device supportati

- `CPU`;
- `GPU`;
- `GPU.0`;
- `NPU`;
- `AUTO`;
- `HETERO`.

## Policy

La rilevazione di `GPU.0` non promuove GPU.0 a provider primario. Serve solo a
rendere corretta l'evidence.

La rilevazione di `NPU` non promuove NPU a provider primario. Serve a rendere
effettiva la lane auditor/diagnostic.

## Smoke

```text
Tools/validation/run_full0to10_openvino_device_visibility_smoke.py
```
