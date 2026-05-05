# Probe contract

Il probe controlla capability e disponibilità, non esegue generazione.

## Consentito

- `ollama list`;
- `ollama ps`;
- `nvidia-smi --query-gpu`;
- import OpenVINO e lista device;
- inventario script repo.

## Vietato

- prompt generation;
- model loading NPU pesante;
- Blender runtime;
- FFmpeg/media output;
- patch application;
- persistent SQLite write.
