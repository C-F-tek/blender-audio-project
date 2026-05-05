# GPU/NPU optimization planning

Il planner include candidati per:

- visibilità telemetry GPU;
- contratto NPU sampled-auditor;
- integrazione/relazione OpenVINO `GPU.0`;
- separazione tra GPU primary advisory lane e NPU diagnostic lane.

Questa patch non cambia impostazioni runtime e non promuove NPU a lane primaria.
