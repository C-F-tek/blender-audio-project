# Project Code Chunk 171/212

- File: `Tools/npu/ollama_runtime.py`
- Part: `1`
- Lines: `1-302`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `json`, `os`, `shutil`, `subprocess`, `time`, `urllib.error`, `urllib.request`
- Classes: `OllamaModelManager` line 199 methods: __init__, generate, close, __enter__, __exit__; `OllamaSession` line 253 methods: __init__, start, generate, unload_model, close, __enter__, __exit__
- Functions: `normalize_base_url(value)` line 13; `ollama_home()` line 24; `manifest_root()` line 31; `find_ollama_exe()` line 36; `_json_request(base_url, path, payload, timeout)` line 74; `is_server_ready(base_url, timeout)` line 91; `list_models(base_url)` line 99; `list_models_from_disk()` line 110; `start_server(ollama_exe, base_url, startup_timeout)` line 139; `choose_model(preferred_model, available_models)` line 160; `strip_json_fence(text)` line 175; `parse_json_response(text)` line 187
- Assignments: `DEFAULT_BASE_URL`, `DEFAULT_MODELS`

## Content
```py
00001: from __future__ import annotations
00002: 
00003: from pathlib import Path
00004: import json
00005: import os
00006: import shutil
00007: import subprocess
00008: import time
00009: import urllib.error
00010: import urllib.request
00011: 
00012: 
00013: def normalize_base_url(value: str | None) -> str:
00014:     base_url = value or "http://127.0.0.1:11434"
00015:     if not base_url.startswith(("http://", "https://")):
00016:         base_url = "http://" + base_url
00017:     return base_url.rstrip("/")
00018: 
00019: 
00020: DEFAULT_BASE_URL = normalize_base_url(os.environ.get("OLLAMA_API_BASE") or os.environ.get("OLLAMA_HOST"))
00021: DEFAULT_MODELS = ("qwen2.5-coder:14b", "gpt-oss:20b", "autumnzsd/qwen2.5-coder-tools:latest")
00022: 
00023: 
00024: def ollama_home() -> Path:
00025:     env_home = os.environ.get("OLLAMA_MODELS")
00026:     if env_home:
00027:         return Path(env_home).expanduser().resolve().parent
00028:     return Path.home() / ".ollama"
00029: 
00030: 
00031: def manifest_root() -> Path:
00032:     models_dir = Path(os.environ.get("OLLAMA_MODELS", str(Path.home() / ".ollama" / "models"))).expanduser()
00033:     return models_dir / "manifests"
00034: 
00035: 
00036: def find_ollama_exe() -> Path | None:
00037:     env_path = os.environ.get("OLLAMA_EXE")
00038:     candidates = []
00039:     if env_path:
00040:         candidates.append(Path(env_path))
00041: 
00042:     which_path = shutil.which("ollama")
00043:     if which_path:
00044:         candidates.append(Path(which_path))
00045: 
00046:     local_app = os.environ.get("LOCALAPPDATA")
00047:     program_files = os.environ.get("ProgramFiles")
00048:     user_profile = os.environ.get("USERPROFILE")
00049: 
00050:     if local_app:
00051:         candidates.extend(
00052:             [
00053:                 Path(local_app) / "Programs" / "Ollama" / "ollama.exe",
00054:                 Path(local_app) / "Ollama" / "ollama.exe",
00055:                 Path(local_app) / "Microsoft" / "WindowsApps" / "ollama.exe",
00056:             ]
00057:         )
00058:     if program_files:
00059:         candidates.append(Path(program_files) / "Ollama" / "ollama.exe")
00060:     if user_profile:
00061:         candidates.append(Path(user_profile) / "AppData" / "Local" / "Programs" / "Ollama" / "ollama.exe")
00062: 
00063:     for candidate in candidates:
00064:         try:
00065:             exists = candidate.exists()
00066:         except PermissionError:
00067:             exists = True
00068:         if exists:
00069:             return candidate
00070: 
00071:     return None
00072: 
00073: 
00074: def _json_request(base_url: str, path: str, payload: dict | None = None, timeout: float = 10.0) -> dict:
00075:     url = base_url.rstrip("/") + path
00076:     data = None
00077:     headers = {}
00078:     method = "GET"
00079: 
00080:     if payload is not None:
00081:         data = json.dumps(payload).encode("utf-8")
00082:         headers["Content-Type"] = "application/json"
00083:         method = "POST"
00084: 
00085:     request = urllib.request.Request(url, data=data, headers=headers, method=method)
00086:     with urllib.request.urlopen(request, timeout=timeout) as response:
00087:         raw = response.read().decode("utf-8", errors="replace")
00088:     return json.loads(raw) if raw else {}
00089: 
00090: 
00091: def is_server_ready(base_url: str = DEFAULT_BASE_URL, timeout: float = 2.0) -> bool:
00092:     try:
00093:         _json_request(base_url, "/api/tags", timeout=timeout)
00094:     except Exception:
00095:         return False
00096:     return True
00097: 
00098: 
00099: def list_models(base_url: str = DEFAULT_BASE_URL) -> list[str]:
00100:     data = _json_request(base_url, "/api/tags", timeout=8.0)
00101:     models = data.get("models", [])
00102:     names = []
00103:     for item in models:
00104:         name = item.get("name") if isinstance(item, dict) else None
00105:         if name:
00106:             names.append(str(name))
00107:     return names
00108: 
00109: 
00110: def list_models_from_disk() -> list[str]:
00111:     root = manifest_root()
00112:     if not root.exists():
00113:         return []
00114: 
00115:     names = []
00116:     for manifest in root.rglob("*"):
00117:         if not manifest.is_file():
00118:             continue
00119:         rel = manifest.relative_to(root).parts
00120:         if len(rel) < 4:
00121:             continue
00122: 
00123:         registry = rel[0]
00124:         namespace = rel[1]
00125:         model_parts = rel[2:-1]
00126:         tag = rel[-1]
00127:         model_name = "/".join(model_parts)
00128: 
00129:         if registry == "registry.ollama.ai" and namespace == "library":
00130:             names.append(f"{model_name}:{tag}")
00131:         elif registry == "registry.ollama.ai":
00132:             names.append(f"{namespace}/{model_name}:{tag}")
00133:         else:
00134:             names.append(f"{namespace}/{model_name}:{tag}")
00135: 
00136:     return sorted(set(names))
00137: 
00138: 
00139: def start_server(ollama_exe: Path, base_url: str = DEFAULT_BASE_URL, startup_timeout: float = 20.0) -> subprocess.Popen:
00140:     creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
00141:     process = subprocess.Popen(
00142:         [str(ollama_exe), "serve"],
00143:         stdout=subprocess.DEVNULL,
00144:         stderr=subprocess.DEVNULL,
00145:         stdin=subprocess.DEVNULL,
00146:         creationflags=creationflags,
00147:     )
00148: 
00149:     deadline = time.time() + startup_timeout
00150:     while time.time() < deadline:
00151:         if process.poll() is not None:
00152:             raise RuntimeError("Ollama server stopped during startup.")
00153:         if is_server_ready(base_url):
00154:             return process
00155:         time.sleep(0.5)
00156: 
00157:     raise TimeoutError("Ollama server did not become ready in time.")
00158: 
00159: 
00160: def choose_model(preferred_model: str | None, available_models: list[str]) -> str:
00161:     if preferred_model and preferred_model in available_models:
00162:         return preferred_model
00163: 
00164:     for model in DEFAULT_MODELS:
00165:         if model in available_models:
00166:             return model
00167: 
00168:     if available_models:
00169:         return available_models[0]
00170: 
00171:     wanted = preferred_model or " or ".join(DEFAULT_MODELS)
00172:     raise RuntimeError(f"No Ollama models are available. Install or pull: {wanted}")
00173: 
00174: 
00175: def strip_json_fence(text: str) -> str:
00176:     stripped = text.strip()
00177:     if stripped.startswith("```"):
00178:         lines = stripped.splitlines()
00179:         if lines and lines[0].strip().startswith("```"):
00180:             lines = lines[1:]
00181:         if lines and lines[-1].strip() == "```":
00182:             lines = lines[:-1]
00183:         stripped = "\n".join(lines).strip()
00184:     return stripped
00185: 
00186: 
00187: def parse_json_response(text: str) -> dict:
00188:     stripped = strip_json_fence(text)
00189:     try:
00190:         return json.loads(stripped)
00191:     except json.JSONDecodeError:
00192:         start = stripped.find("{")
00193:         end = stripped.rfind("}")
00194:         if start >= 0 and end > start:
00195:             return json.loads(stripped[start : end + 1])
00196:         raise
00197: 
00198: 
00199: class OllamaModelManager:
00200:     def __init__(
00201:         self,
00202:         base_url: str = DEFAULT_BASE_URL,
00203:         keep_alive: str = "5m",
00204:         shutdown_server: bool = True,
00205:         startup_timeout: float = 20.0,
00206:     ) -> None:
00207:         self.base_url = normalize_base_url(base_url)
00208:         self.keep_alive = keep_alive
00209:         self.shutdown_server = shutdown_server
00210:         self.startup_timeout = startup_timeout
00211:         self.session: OllamaSession | None = None
00212:         self.current_model: str | None = None
00213: 
00214:     def generate(
00215:         self,
00216:         model: str,
00217:         prompt: str,
00218:         max_new_tokens: int = 900,
00219:         temperature: float = 0.15,
00220:     ) -> tuple[str, str]:
00221:         if self.session and self.current_model != model:
00222:             self.session.close()
00223:             self.session = None
00224:             self.current_model = None
00225: 
00226:         if not self.session:
00227:             self.session = OllamaSession(
00228:                 model=model,
00229:                 base_url=self.base_url,
00230:                 keep_alive=self.keep_alive,
00231:                 shutdown_server=False,
00232:                 unload_model=True,
00233:                 startup_timeout=self.startup_timeout,
00234:             ).start()
00235:             self.current_model = self.session.model
00236: 
00237:         text = self.session.generate(prompt, max_new_tokens=max_new_tokens, temperature=temperature)
00238:         return text, self.session.model or model
00239: 
00240:     def close(self) -> None:
00241:         if self.session:
00242:             self.session.close()
00243:             self.session = None
00244:         self.current_model = None
00245: 
00246:     def __enter__(self) -> "OllamaModelManager":
00247:         return self
00248: 
00249:     def __exit__(self, exc_type, exc, tb) -> None:
00250:         self.close()
00251: 
00252: 
00253: class OllamaSession:
00254:     def __init__(
00255:         self,
00256:         model: str | None = None,
00257:         base_url: str = DEFAULT_BASE_URL,
00258:         keep_alive: str = "5m",
00259:         shutdown_server: bool = True,
00260:         unload_model: bool = True,
00261:         startup_timeout: float = 20.0,
00262:     ) -> None:
00263:         self.base_url = base_url
00264:         self.base_url = normalize_base_url(base_url)
00265:         self.preferred_model = model
00266:         self.keep_alive = keep_alive
00267:         self.shutdown_server = shutdown_server
00268:         self.unload_model_on_close = unload_model
00269:         self.startup_timeout = startup_timeout
00270:         self.ollama_exe = find_ollama_exe()
00271:         self.process: subprocess.Popen | None = None
00272:         self.started_server = False
00273:         self.model: str | None = None
00274: 
00275:     def start(self) -> "OllamaSession":
00276:         if not is_server_ready(self.base_url):
00277:             if not self.ollama_exe:
00278:                 raise FileNotFoundError(
00279:                     "Ollama server is not reachable and ollama.exe was not found. "
00280:                     "Set OLLAMA_EXE or restart the shell after installing Ollama."
00281:                 )
00282:             self.process = start_server(self.ollama_exe, self.base_url, self.startup_timeout)
00283:             self.started_server = True
00284: 
00285:         available = list_models(self.base_url)
00286:         if not available:
00287:             available = list_models_from_disk()
00288:         self.model = choose_model(self.preferred_model, available)
00289:         return self
00290: 
00291:     def generate(self, prompt: str, max_new_tokens: int = 900, temperature: float = 0.15) -> str:
00292:         if not self.model:
00293:             self.start()
00294: 
00295:         payload = {
00296:             "model": self.model,
00297:             "prompt": prompt,
00298:             "stream": False,
00299:             "keep_alive": self.keep_alive,
00300:             "options": {
00301:                 "temperature": temperature,
00302:                 "num_predict": max_new_tokens,
```
