# OpenVINO device visibility normalization

Il Full0To10 accelerator control deve riconoscere NPU e GPU.0 anche quando il
probe OpenVINO salva i device dentro payload annidati.

## Problema

Alcuni probe scrivono:

```json
{"result": {"stdout": "{\"devices\": [\"CPU\", \"GPU.0\", \"NPU\"]}"}}
```

oppure:

```json
{"result": {"devices": ["CPU", "GPU.0", "NPU"]}}
```

Se i consumer leggono solo `npu.devices`, NPU e GPU.0 risultano assenti.

## Regola

I consumer devono usare il normalizzatore:

```text
full0to10_accelerator_control.device_visibility
```

## Effetto

- `npu_auditor.device_visible=true` quando `NPU` è presente;
- `openvino_gpu0.device_visible=true` quando `GPU.0` è presente;
- GPU.0 resta secondary diagnostic;
- NPU resta sampled auditor.
