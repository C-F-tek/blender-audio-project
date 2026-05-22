# Ollama Python SDK Adapter

## Scopo

IA-Carmine usa `ia_carmine.providers.ollama` come runtime canonico Ollama. Il backend e' la libreria ufficiale `ollama-python` tramite `ollama.Client`.

## Cosa sostituisce

- chiamate HTTP custom a `/api/generate`;
- chiamate HTTP custom a `/api/chat`;
- parser streaming HTTP line-by-line;
- list/ps manuali per Ollama;
- tool-call parsing custom fuori dal runtime Ollama.

## Cosa non sostituisce

- NPU/OpenVINO micro task;
- CPU validators;
- broker deterministico IA-Carmine;
- product composer e patch/code product boundary.

## Lane policy

| Lane | Backend canonico | Ruolo |
| --- | --- | --- |
| GPU1 | Ollama SDK | planner/sintesi principale |
| GPU0 | Ollama SDK / Vulkan | reviewer/refiner peer |
| NPU | OpenVINO | micro task/audit |
| CPU | Python validators/broker | autorita' deterministica |

OpenVINO GPU0 e' diagnostico, non fallback full/complete per GPU0.

## Validazione locale

```powershell
$RepoRoot = (Resolve-Path .).Path
$RepoPy = "C:\Users\carmi\blender\blender-audio-project\.venv\Scripts\python.exe"
$env:IA_CARMINE_PYTHON = $RepoPy
$env:PYTHONPATH = $RepoRoot

& $RepoPy -m pip install "ollama>=0.6,<0.7"
& $RepoPy -m pip install "openvino>=2026.1,<2026.2" "openvino-genai>=2026.1,<2026.2"
& $RepoPy -c "import ia_carmine.providers.ollama; from ia_carmine.providers.ollama.session import OllamaSession"
& $RepoPy -m ia_carmine.cli ensure_ollama_role_models --repo-root . --gpu1-base-url http://127.0.0.1:11434 --gpu0-base-url http://127.0.0.1:11435 --start-gpu0-vulkan-server --restart-gpu0-vulkan-server --gpu0-vulkan-visible-devices auto --gpu1-model qwen3-coder:latest --gpu0-model qwen3:1.7b --keep-alive 120s --output .\output\validation\ollama_role_models.json --markdown-output .\output\validation\ollama_role_models.md
& $RepoPy -m Tools.validation run_ollama_sdk_adapter_smoke --repo-root . --output .\output\validation\ollama_sdk_adapter_smoke.json --markdown-output .\output\validation\ollama_sdk_adapter_smoke.md
ollama list
ollama ps
```

Non usare questo smoke come full run. Serve solo a provare adapter SDK, import compatibility, tool calls e assenza di HTTP custom nel runtime canonico.
