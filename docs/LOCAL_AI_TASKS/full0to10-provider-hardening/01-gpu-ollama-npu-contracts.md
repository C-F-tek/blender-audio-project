# GPU/Ollama/NPU contracts

## Ollama/GPU

Ruolo: primary advisory solo quando esplicito.

Requisiti:

- quality preflight;
- workload report quality;
- telemetry GPU;
- no generation implicita.

## NPU/OpenVINO

Ruolo: sampled auditor o diagnostic lane.

Requisiti:

- non primary advisory di default;
- no model load obbligatorio in preflight;
- evidence separata.

## OpenVINO GPU.0

Ruolo: secondary diagnostic.

Requisiti:

- non sottrarre lane primaria GPU/Ollama;
- promozione solo con patch esplicita.
