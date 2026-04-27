# Project Code Chunk 189/212

- File: `Tools/workflow/gui/workflow_gui.py`
- Part: `1`
- Lines: `1-265`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `contextlib`, `json`, `queue`, `sys`, `threading`, `traceback`, `tkinter`, `from tkinter import filedialog, messagebox, ttk`, `workflow_state`, `from scene_brief import append_scene_message, clear_scene_chat_history, generate_scene_chat_reply, load_or_create_scene_brief`
- Classes: `QueueWriter` line 23 methods: __init__, write, flush; `LogWindow` line 36 methods: __init__, hide, show, read_tail, refresh, refresh_loop; `AdvancedDebugWindow` line 98 methods: __init__, hide, show, refresh, refresh_loop, open_shell_monitor; `ProjectStatsWindow` line 154 methods: __init__, hide, show, refresh, refresh_loop; `SceneDirectorChatWindow` line 202 methods: __init__, hide, show, scene_path, refresh, send_message, clear_chat, append_system_line, on_return, on_shift_return; `WorkflowGui` line 360 methods: __init__, build_layout, append_output, drain_output_queue, set_buttons_enabled, run_task, refresh_session_loop, refresh_session, choose_wav, reset_wav
- Functions: `main()` line 708
- Assignments: `THIS_DIR`, `WORKFLOW_DIR`

## Content
```py
00001: from __future__ import annotations
00002: 
00003: from pathlib import Path
00004: import contextlib
00005: import json
00006: import queue
00007: import sys
00008: import threading
00009: import traceback
00010: import tkinter as tk
00011: from tkinter import filedialog, messagebox, ttk
00012: 
00013: 
00014: THIS_DIR = Path(__file__).resolve().parent
00015: WORKFLOW_DIR = THIS_DIR.parent
00016: if str(WORKFLOW_DIR) not in sys.path:
00017:     sys.path.insert(0, str(WORKFLOW_DIR))
00018: 
00019: import workflow_state as wf  # noqa: E402
00020: from scene_brief import append_scene_message, clear_scene_chat_history, generate_scene_chat_reply, load_or_create_scene_brief  # noqa: E402
00021: 
00022: 
00023: class QueueWriter:
00024:     def __init__(self, target_queue: queue.Queue[str]) -> None:
00025:         self.target_queue = target_queue
00026: 
00027:     def write(self, text: str) -> int:
00028:         if text:
00029:             self.target_queue.put(text)
00030:         return len(text)
00031: 
00032:     def flush(self) -> None:
00033:         return None
00034: 
00035: 
00036: class LogWindow(tk.Toplevel):
00037:     def __init__(self, master: tk.Tk) -> None:
00038:         super().__init__(master)
00039:         self.title("Spaziotempo Workflow Logs")
00040:         self.geometry("980x620")
00041:         self.protocol("WM_DELETE_WINDOW", self.hide)
00042: 
00043:         toolbar = ttk.Frame(self)
00044:         toolbar.pack(fill="x", padx=8, pady=6)
00045:         ttk.Button(toolbar, text="Refresh", command=self.refresh).pack(side="left")
00046:         ttk.Button(toolbar, text="Hide", command=self.hide).pack(side="left", padx=(6, 0))
00047: 
00048:         self.text = tk.Text(self, wrap="none", height=32)
00049:         self.text.pack(fill="both", expand=True, padx=8, pady=(0, 8))
00050: 
00051:         yscroll = ttk.Scrollbar(self.text, orient="vertical", command=self.text.yview)
00052:         self.text.configure(yscrollcommand=yscroll.set)
00053:         yscroll.pack(side="right", fill="y")
00054: 
00055:         self.after(1000, self.refresh_loop)
00056: 
00057:     def hide(self) -> None:
00058:         self.withdraw()
00059: 
00060:     def show(self) -> None:
00061:         self.deiconify()
00062:         self.lift()
00063:         self.refresh()
00064: 
00065:     def read_tail(self, path: Path, max_lines: int = 160) -> str:
00066:         if not path.exists():
00067:             return f"{path}\n<missing>\n"
00068:         try:
00069:             lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
00070:         except Exception as exc:
00071:             return f"{path}\n<read failed: {exc}>\n"
00072:         return "\n".join(lines[-max_lines:]) + "\n"
00073: 
00074:     def refresh(self) -> None:
00075:         body = []
00076:         body.append(f"EVENT LOG: {wf.EVENT_LOG_PATH}\n")
00077:         body.append(self.read_tail(wf.EVENT_LOG_PATH))
00078:         body.append("\nLAST RESULT:\n")
00079:         if wf.LAST_RESULT_PATH.exists():
00080:             try:
00081:                 payload = json.loads(wf.LAST_RESULT_PATH.read_text(encoding="utf-8"))
00082:                 body.append(json.dumps(payload, indent=2, ensure_ascii=False))
00083:             except Exception:
00084:                 body.append(self.read_tail(wf.LAST_RESULT_PATH, max_lines=120))
00085:         else:
00086:             body.append("<missing>")
00087: 
00088:         self.text.delete("1.0", "end")
00089:         self.text.insert("1.0", "".join(body))
00090:         self.text.see("end")
00091: 
00092:     def refresh_loop(self) -> None:
00093:         if self.state() != "withdrawn":
00094:             self.refresh()
00095:         self.after(2500, self.refresh_loop)
00096: 
00097: 
00098: class AdvancedDebugWindow(tk.Toplevel):
00099:     def __init__(self, master: tk.Tk) -> None:
00100:         super().__init__(master)
00101:         self.title("Spaziotempo Advanced Debug")
00102:         self.geometry("1120x760")
00103:         self.protocol("WM_DELETE_WINDOW", self.hide)
00104:         self.auto_refresh = tk.BooleanVar(value=True)
00105: 
00106:         toolbar = ttk.Frame(self)
00107:         toolbar.pack(fill="x", padx=8, pady=6)
00108:         ttk.Button(toolbar, text="Check", command=self.refresh).pack(side="left")
00109:         ttk.Checkbutton(toolbar, text="Auto refresh", variable=self.auto_refresh).pack(side="left", padx=(8, 0))
00110:         ttk.Button(toolbar, text="Open shell monitor", command=self.open_shell_monitor).pack(side="left", padx=(8, 0))
00111:         ttk.Button(toolbar, text="Hide", command=self.hide).pack(side="left", padx=(8, 0))
00112: 
00113:         self.text = tk.Text(self, wrap="none")
00114:         self.text.pack(fill="both", expand=True, padx=8, pady=(0, 8))
00115: 
00116:         yscroll = ttk.Scrollbar(self.text, orient="vertical", command=self.text.yview)
00117:         self.text.configure(yscrollcommand=yscroll.set)
00118:         yscroll.pack(side="right", fill="y")
00119: 
00120:         self.after(1000, self.refresh_loop)
00121: 
00122:     def hide(self) -> None:
00123:         self.withdraw()
00124: 
00125:     def show(self) -> None:
00126:         self.deiconify()
00127:         self.lift()
00128:         self.refresh()
00129: 
00130:     def refresh(self) -> None:
00131:         try:
00132:             report = wf.run_advanced_debug_check(probe_write=True)
00133:         except Exception:
00134:             report = traceback.format_exc()
00135:         self.text.delete("1.0", "end")
00136:         self.text.insert("1.0", report)
00137:         self.text.see("end")
00138: 
00139:     def refresh_loop(self) -> None:
00140:         if self.state() != "withdrawn" and self.auto_refresh.get():
00141:             self.refresh()
00142:         self.after(3000, self.refresh_loop)
00143: 
00144:     def open_shell_monitor(self) -> None:
00145:         try:
00146:             process = wf.open_debug_monitor_window(interval=3.0, probe_write=True)
00147:             self.text.insert("end", f"\n\nOpened shell debug monitor PID: {process.pid}\n")
00148:             self.text.see("end")
00149:         except Exception:
00150:             self.text.insert("end", "\n\n" + traceback.format_exc())
00151:             self.text.see("end")
00152: 
00153: 
00154: class ProjectStatsWindow(tk.Toplevel):
00155:     def __init__(self, master: tk.Tk) -> None:
00156:         super().__init__(master)
00157:         self.title("Spaziotempo Project Stats")
00158:         self.geometry("1120x760")
00159:         self.protocol("WM_DELETE_WINDOW", self.hide)
00160:         self.auto_refresh = tk.BooleanVar(value=False)
00161: 
00162:         toolbar = ttk.Frame(self)
00163:         toolbar.pack(fill="x", padx=8, pady=6)
00164:         ttk.Button(toolbar, text="Refresh", command=self.refresh).pack(side="left")
00165:         ttk.Checkbutton(toolbar, text="Auto refresh", variable=self.auto_refresh).pack(side="left", padx=(8, 0))
00166:         ttk.Button(toolbar, text="Hide", command=self.hide).pack(side="left", padx=(8, 0))
00167: 
00168:         self.text = tk.Text(self, wrap="none")
00169:         self.text.pack(fill="both", expand=True, padx=8, pady=(0, 8))
00170: 
00171:         yscroll = ttk.Scrollbar(self.text, orient="vertical", command=self.text.yview)
00172:         self.text.configure(yscrollcommand=yscroll.set)
00173:         yscroll.pack(side="right", fill="y")
00174: 
00175:         self.after(1000, self.refresh_loop)
00176: 
00177:     def hide(self) -> None:
00178:         self.withdraw()
00179: 
00180:     def show(self) -> None:
00181:         self.deiconify()
00182:         self.lift()
00183:         self.refresh()
00184: 
00185:     def refresh(self) -> None:
00186:         try:
00187:             session = wf.load_session(create=True)
00188:             stats = wf.build_project_storage_stats(session)
00189:             report = wf.format_project_storage_stats(stats)
00190:         except Exception:
00191:             report = traceback.format_exc()
00192:         self.text.delete("1.0", "end")
00193:         self.text.insert("1.0", report)
00194:         self.text.see("1.0")
00195: 
00196:     def refresh_loop(self) -> None:
00197:         if self.state() != "withdrawn" and self.auto_refresh.get():
00198:             self.refresh()
00199:         self.after(5000, self.refresh_loop)
00200: 
00201: 
00202: class SceneDirectorChatWindow(tk.Toplevel):
00203:     def __init__(self, master: tk.Tk) -> None:
00204:         super().__init__(master)
00205:         self.title("Spaziotempo Scene Director Chat")
00206:         self.geometry("980x720")
00207:         self.protocol("WM_DELETE_WINDOW", self.hide)
00208:         self.worker: threading.Thread | None = None
00209: 
00210:         toolbar = ttk.Frame(self)
00211:         toolbar.pack(fill="x", padx=8, pady=6)
00212:         ttk.Button(toolbar, text="Refresh", command=self.refresh).pack(side="left")
00213:         ttk.Button(toolbar, text="Save message", command=self.send_message).pack(side="left", padx=(6, 0))
00214:         ttk.Button(toolbar, text="Clear chat", command=self.clear_chat).pack(side="left", padx=(6, 0))
00215:         ttk.Button(toolbar, text="Hide", command=self.hide).pack(side="left", padx=(6, 0))
00216: 
00217:         self.transcript = tk.Text(self, wrap="word", height=26)
00218:         self.transcript.pack(fill="both", expand=True, padx=8, pady=(0, 6))
00219:         self.transcript.configure(state="disabled")
00220: 
00221:         input_frame = ttk.Frame(self)
00222:         input_frame.pack(fill="x", padx=8, pady=(0, 8))
00223: 
00224:         self.input = tk.Text(input_frame, wrap="word", height=5)
00225:         self.input.pack(side="left", fill="both", expand=True)
00226:         self.input.bind("<Return>", self.on_return)
00227:         self.input.bind("<Shift-Return>", self.on_shift_return)
00228: 
00229:         send_button = ttk.Button(input_frame, text="Send", command=self.send_message)
00230:         send_button.pack(side="right", padx=(8, 0), fill="y")
00231: 
00232:     def hide(self) -> None:
00233:         self.withdraw()
00234: 
00235:     def show(self) -> None:
00236:         self.deiconify()
00237:         self.lift()
00238:         self.refresh()
00239:         self.input.focus_set()
00240: 
00241:     def scene_path(self) -> Path:
00242:         session = wf.load_session(create=True)
00243:         return Path(session.artifacts["scene_brief_json"])
00244: 
00245:     def refresh(self) -> None:
00246:         session = wf.load_session(create=True)
00247:         brief = load_or_create_scene_brief(
00248:             track_stem=session.track_stem,
00249:             audio_path=session.artifacts["audio_path"],
00250:             output_path=Path(session.artifacts["scene_brief_json"]),
00251:         )
00252:         lines = [
00253:             f"Track: {session.track_stem}",
00254:             f"Brief: {session.artifacts['scene_brief_json']}",
00255:             "",
00256:         ]
00257:         memory = brief.get("conversation_memory") if isinstance(brief.get("conversation_memory"), dict) else {}
00258:         if memory:
00259:             lines.append(f"Memory: {memory.get('message_count', 0)} messaggi, aggiornata {memory.get('updated_at', '-')}")
00260:             constraints = memory.get("durable_constraints") if isinstance(memory.get("durable_constraints"), list) else []
00261:             for item in constraints[-4:]:
00262:                 lines.append(f"- {item}")
00263:             lines.append("")
00264:         transcript = brief.get("conversation_transcript") or []
00265:         if not transcript:
```
