# Project Code Chunk 172/212

- File: `Tools/npu/ollama_runtime.py`
- Part: `2`
- Lines: `303-351`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `json`, `os`, `shutil`, `subprocess`, `time`, `urllib.error`, `urllib.request`
- Classes: `OllamaModelManager` line 199 methods: __init__, generate, close, __enter__, __exit__; `OllamaSession` line 253 methods: __init__, start, generate, unload_model, close, __enter__, __exit__
- Functions: `normalize_base_url(value)` line 13; `ollama_home()` line 24; `manifest_root()` line 31; `find_ollama_exe()` line 36; `_json_request(base_url, path, payload, timeout)` line 74; `is_server_ready(base_url, timeout)` line 91; `list_models(base_url)` line 99; `list_models_from_disk()` line 110; `start_server(ollama_exe, base_url, startup_timeout)` line 139; `choose_model(preferred_model, available_models)` line 160; `strip_json_fence(text)` line 175; `parse_json_response(text)` line 187
- Assignments: `DEFAULT_BASE_URL`, `DEFAULT_MODELS`

## Content
```py
00303:             },
00304:         }
00305:         data = _json_request(self.base_url, "/api/generate", payload=payload, timeout=600.0)
00306:         return str(data.get("response", "")).strip()
00307: 
00308:     def unload_model(self) -> None:
00309:         if not self.model:
00310:             return
00311: 
00312:         payload = {
00313:             "model": self.model,
00314:             "prompt": "",
00315:             "stream": False,
00316:             "keep_alive": 0,
00317:         }
00318:         try:
00319:             _json_request(self.base_url, "/api/generate", payload=payload, timeout=30.0)
00320:         except Exception:
00321:             pass
00322: 
00323:         if self.ollama_exe:
00324:             try:
00325:                 subprocess.run(
00326:                     [str(self.ollama_exe), "stop", self.model],
00327:                     stdout=subprocess.DEVNULL,
00328:                     stderr=subprocess.DEVNULL,
00329:                     stdin=subprocess.DEVNULL,
00330:                     timeout=30.0,
00331:                     check=False,
00332:                 )
00333:             except Exception:
00334:                 pass
00335: 
00336:     def close(self) -> None:
00337:         if self.unload_model_on_close:
00338:             self.unload_model()
00339: 
00340:         if self.started_server and self.shutdown_server and self.process:
00341:             self.process.terminate()
00342:             try:
00343:                 self.process.wait(timeout=8.0)
00344:             except subprocess.TimeoutExpired:
00345:                 self.process.kill()
00346: 
00347:     def __enter__(self) -> "OllamaSession":
00348:         return self.start()
00349: 
00350:     def __exit__(self, exc_type, exc, tb) -> None:
00351:         self.close()
```
