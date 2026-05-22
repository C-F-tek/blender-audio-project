# Ollama SDK GPU0 Vulkan Refactor

## Scopo

Questo refactor rende `ia_carmine.providers.ollama` il runtime canonico per
Ollama. Le chiamate `generate`, `chat`, streaming, list, ps, unload e tool-call
passano attraverso `ollama.Client`, non attraverso HTTP custom.

## Lane provider

| Lane | Backend full/complete | Ruolo |
| --- | --- | --- |
| GPU1 | Ollama SDK | planner e sintesi principale |
| GPU0 | Ollama SDK con policy Vulkan verificata | peer reviewer/refiner |
| NPU | OpenVINO | micro task e audit |
| CPU | broker e validator Python | autorita' deterministica |

OpenVINO GPU0 resta solo diagnostico. Non e' fallback della lane GPU0 in profili
full/complete.

Su questa workstation Windows l'indice fisico resta:

- Windows GPU0 = Intel(R) Graphics;
- Windows GPU1 = NVIDIA GeForce RTX 5080.

L'indice Vulkan puo' essere diverso: `vulkaninfo --summary` enumera NVIDIA come
Vulkan GPU0 e Intel come Vulkan GPU1. Per questo `ia_carmine.providers.ollama`
risolve `--gpu0-vulkan-visible-devices auto` cercando il device integrato/Intel
e imposta `GGML_VK_VISIBLE_DEVICES` sull'indice Vulkan Intel, non sull'indice
Windows grezzo.

## Moduli principali

| Area | Modulo |
| --- | --- |
| SDK client | `ia_carmine.providers.ollama.sdk_client` |
| Sessione runtime | `ia_carmine.providers.ollama.session` |
| Manager modello | `ia_carmine.providers.ollama.manager` |
| Tool calls | `ia_carmine.providers.ollama.tool_calls` |
| Evidenza lane | `ia_carmine.providers.ollama.runtime_evidence` |
| Modelli ruolo | `ia_carmine.providers.ollama.role_models` |
| GPU0 peer report | `ia_carmine.providers.provider_mesh.ollama_gpu0_peer_report` |

Il runtime importabile Ollama e' solo `ia_carmine.providers.ollama`.

## Tool calling

`OllamaSdkClient.chat()` accetta `tools` e normalizza `message.tool_calls` con
`ia_carmine.providers.ollama.tool_calls`. IA-Carmine continua a eseguire solo
tool allowlisted tramite broker deterministico.

## Modelli ruolo vivi

`python -m ia_carmine.cli ensure_ollama_role_models` verifica i modelli per
`gpu1_planner` e `gpu0_peer`, li scarica con `ollama.Client.pull()` se mancano e
li carica con una generazione breve mantenendo `keep_alive` attivo. I default
sono `qwen3-coder:latest` per GPU1 e `qwen3:1.7b` per GPU0, oppure le
variabili `IA_CARMINE_GPU1_MODEL` e `IA_CARMINE_GPU0_MODEL`.

Il check non considera sufficiente `ollama ps`: il report GPU0 deve avere
generazione con `eval_count > 0`, log runtime Vulkan su Intel e unload verificato
a fine giro. Il server dedicato GPU0 sulla porta `11435` viene fermato a fine
giro salvo `--keep-gpu0-vulkan-server`.

## Contratti aggiornati

- `provider_command_specs` usa `build_ollama_gpu0_peer_report` per `gpu0_peer`.
- `provider_work_verification` richiede evidenza Ollama GPU0/Vulkan per GPU0.
- `provider_replight` distingue GPU0 Ollama da NPU OpenVINO.
- I validator runtime mesh e topology guardano GPU0 Ollama/Vulkan e NPU OpenVINO.
- `check_npu_provider_environment` verifica `openvino` e `openvino-genai`
  installati dalla famiglia ufficiale 2026.1 e la visibilita' `NPU`.

## Validazioni mirate

- `python -m py_compile` sui Python toccati.
- Import smoke di `ia_carmine.providers.ollama` e `OllamaSession`.
- `Tools.validation run_ollama_sdk_adapter_smoke`.
- `ollama list` e `ollama ps`.
- `ensure_ollama_role_models` per pull/load dei modelli GPU1/GPU0.
- `ia_carmine.cli run --dry-run` con profile `day0_full_code_product`.
- `check_local_resource_lanes` con `IA_CARMINE_PYTHON` reale.
- `check_npu_provider_environment` con `--npu-python` reale.
- Contract mirati: topology, runtime mesh, intrinsic capability.

## Esclusioni

Non sono state usate full run, full smoke, Blender, FFmpeg o applicazione
automatica di patch come acceptance test di questo refactor.
