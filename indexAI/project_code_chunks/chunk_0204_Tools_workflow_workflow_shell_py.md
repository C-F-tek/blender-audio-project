# Project Code Chunk 204/212

- File: `Tools/workflow/workflow_shell.py`
- Part: `1`
- Lines: `1-269`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `sys`, `from workflow_state import DEFAULT_WAV, EVENT_LOG_PATH, LAST_RESULT_PATH, SESSION_PATH, build_project_storage_stats, format_project_storage_stats, load_session, available_ollama_models, mark_active_operation_interrupted, open_debug_monitor_window, operation_status, reset_to_default_wav, cleanup_intermediate_targets, cleanup_intermediates, cleanup_render_frame_targets, cleanup_render_frames, run_analyze_wav, run_advanced_debug_check, run_code_context, run_dual_ai, run_full_audio_prepare, run_manual_index, run_music_context, run_project_ai_index, run_scene_director_brief, run_startup_service_check, run_track_summary, set_current_wav, set_ai_models, set_debug_enabled`
- Functions: `print_header(session)` line 40; `ask_path(prompt)` line 71; `ask_bool(prompt, default)` line 75; `menu()` line 83; `choose_model(prompt, current)` line 110; `confirm_cleanup(title, targets)` line 127; `main()` line 156

## Content
```py
00001: from __future__ import annotations
00002: 
00003: from pathlib import Path
00004: import sys
00005: 
00006: from workflow_state import (
00007:     DEFAULT_WAV,
00008:     EVENT_LOG_PATH,
00009:     LAST_RESULT_PATH,
00010:     SESSION_PATH,
00011:     build_project_storage_stats,
00012:     format_project_storage_stats,
00013:     load_session,
00014:     available_ollama_models,
00015:     mark_active_operation_interrupted,
00016:     open_debug_monitor_window,
00017:     operation_status,
00018:     reset_to_default_wav,
00019:     cleanup_intermediate_targets,
00020:     cleanup_intermediates,
00021:     cleanup_render_frame_targets,
00022:     cleanup_render_frames,
00023:     run_analyze_wav,
00024:     run_advanced_debug_check,
00025:     run_code_context,
00026:     run_dual_ai,
00027:     run_full_audio_prepare,
00028:     run_manual_index,
00029:     run_music_context,
00030:     run_project_ai_index,
00031:     run_scene_director_brief,
00032:     run_startup_service_check,
00033:     run_track_summary,
00034:     set_current_wav,
00035:     set_ai_models,
00036:     set_debug_enabled,
00037: )
00038: 
00039: 
00040: def print_header(session) -> None:
00041:     status = operation_status(session)
00042:     print("\n" + "=" * 72)
00043:     print("SPAZIOTEMPO WORKFLOW SHELL")
00044:     print("=" * 72)
00045:     print(f"Sessione: {SESSION_PATH}")
00046:     print(f"WAV:      {session.artifacts['audio_path']}")
00047:     print(f"Track:    {session.track_stem}")
00048:     print(f"Default:  {'no, sessione attiva' if session.use_session_track else 'si'}")
00049:     print(f"Debug:    {'ON' if session.debug_enabled else 'OFF'}")
00050:     print(f"AI:       creative={session.creative_model} | technical={session.technical_model} | chat={session.chat_model} | tokens={session.script_max_tokens}")
00051:     print(f"Ultima:   {session.last_operation or '-'}")
00052:     print(f"Log:      {EVENT_LOG_PATH}")
00053:     print(f"Result:   {LAST_RESULT_PATH}")
00054:     print("\nOutput principali:")
00055:     for key in [
00056:         "analysis_json",
00057:         "track_summary_json",
00058:         "music_context_json",
00059:         "analysis_ai_context_json",
00060:         "blender_keyframes_json",
00061:         "dual_ai_plan_json",
00062:         "scene_brief_json",
00063:         "asset_inventory_json",
00064:         "ai_implementation_draft_json",
00065:         "generated_scene_script",
00066:     ]:
00067:         mark = "OK" if status.get(key) else "--"
00068:         print(f"  [{mark}] {key}: {session.artifacts[key]}")
00069: 
00070: 
00071: def ask_path(prompt: str) -> str:
00072:     return input(prompt).strip().strip('"')
00073: 
00074: 
00075: def ask_bool(prompt: str, default: bool = False) -> bool:
00076:     suffix = "S/n" if default else "s/N"
00077:     value = input(f"{prompt} ({suffix}): ").strip().lower()
00078:     if not value:
00079:         return default
00080:     return value in {"s", "si", "y", "yes", "true", "1"}
00081: 
00082: 
00083: def menu() -> None:
00084:     print("\nOperazioni:")
00085:     print("  1  Scegli WAV")
00086:     print("  2  Ripristina WAV default")
00087:     print("  3  Analizza WAV")
00088:     print("  4  Crea track summary")
00089:     print("  5  Crea/aggiorna music context")
00090:     print("  6  Crea/aggiorna code context + indexAI")
00091:     print("  7  Prepara audio completo (3+4+5+6+manual root)")
00092:     print("  8  Indicizza manuali locali")
00093:     print("  9  Dual AI plan")
00094:     print("  10 Dual AI scene script draft")
00095:     print("  11 Mostra sessione")
00096:     print("  12 Toggle debug dettagliato")
00097:     print("  13 Pulisci intermedi")
00098:     print("  14 Pulisci frame render")
00099:     print("  15 Debug advanced check")
00100:     print("  16 Apri debug monitor finestra")
00101:     print("  17 Registra operazione interrotta")
00102:     print("  18 Rigenera indexAI progetto")
00103:     print("  19 Scene director chat / modifica brief")
00104:     print("  20 Project storage stats")
00105:     print("  21 Configura modelli AI")
00106:     print("  22 Startup service check")
00107:     print("  0  Esci")
00108: 
00109: 
00110: def choose_model(prompt: str, current: str) -> str:
00111:     models = available_ollama_models()
00112:     print(f"\n{prompt}")
00113:     if models:
00114:         for idx, model in enumerate(models, start=1):
00115:             mark = " *" if model == current else ""
00116:             print(f"  {idx}. {model}{mark}")
00117:     value = input(f"Modello [{current}]: ").strip()
00118:     if not value:
00119:         return current
00120:     if value.isdigit() and models:
00121:         idx = int(value)
00122:         if 1 <= idx <= len(models):
00123:             return models[idx - 1]
00124:     return value
00125: 
00126: 
00127: def confirm_cleanup(title: str, targets: dict) -> bool:
00128:     files = targets.get("files", [])
00129:     dirs = targets.get("dirs", [])
00130:     print(f"\n{title}")
00131:     print(f"File da eliminare: {len(files)}")
00132:     for item in files[:20]:
00133:         print(f"  FILE {item}")
00134:     if len(files) > 20:
00135:         print(f"  ... altri {len(files) - 20} file")
00136: 
00137:     print(f"Cartelle da eliminare: {len(dirs)}")
00138:     for item in dirs[:20]:
00139:         print(f"  DIR  {item}")
00140:     if len(dirs) > 20:
00141:         print(f"  ... altre {len(dirs) - 20} cartelle")
00142: 
00143:     protected = targets.get("protected_roots", [])
00144:     if protected:
00145:         print("\nProtetti:")
00146:         for item in protected:
00147:             print(f"  {item}")
00148: 
00149:     if not files and not dirs:
00150:         print("\nNiente da pulire.")
00151:         return False
00152: 
00153:     return ask_bool("\nConfermi eliminazione?", default=False)
00154: 
00155: 
00156: def main() -> None:
00157:     session = load_session(create=True)
00158: 
00159:     while True:
00160:         print_header(session)
00161:         menu()
00162:         choice = input("\nScelta: ").strip().lower()
00163: 
00164:         try:
00165:             if choice in {"0", "q", "quit", "exit"}:
00166:                 print("Ok, shell chiusa.")
00167:                 return
00168: 
00169:             if choice == "1":
00170:                 path = ask_path(f"Percorso WAV [{DEFAULT_WAV}]: ") or str(DEFAULT_WAV)
00171:                 session = set_current_wav(Path(path))
00172: 
00173:             elif choice == "2":
00174:                 session = reset_to_default_wav()
00175: 
00176:             elif choice == "3":
00177:                 skip_context = ask_bool("Saltare music context dopo analisi?", default=True)
00178:                 run_analyze_wav(session, skip_music_context=skip_context)
00179:                 session = load_session()
00180: 
00181:             elif choice == "4":
00182:                 run_track_summary(session)
00183:                 session = load_session()
00184: 
00185:             elif choice == "5":
00186:                 run_music_context(session)
00187:                 session = load_session()
00188: 
00189:             elif choice == "6":
00190:                 run_code_context(session)
00191:                 session = load_session()
00192: 
00193:             elif choice == "7":
00194:                 run_full_audio_prepare(session)
00195:                 session = load_session()
00196: 
00197:             elif choice == "8":
00198:                 limit_raw = input("Numero massimo file manuale da indicizzare [80]: ").strip()
00199:                 limit = int(limit_raw) if limit_raw else 80
00200:                 run_manual_index(session, limit_files=limit)
00201:                 session = load_session()
00202: 
00203:             elif choice == "9":
00204:                 include_manual = ask_bool("Includere manuali?", default=False)
00205:                 skip_ollama = ask_bool("Saltare Ollama?", default=False)
00206:                 skip_npu = ask_bool("Saltare NPU heavy pass? La capsule service viene comunque creata", default=True)
00207:                 run_dual_ai(
00208:                     session,
00209:                     phase="plan",
00210:                     include_manual=include_manual,
00211:                     skip_npu=skip_npu,
00212:                     skip_ollama=skip_ollama,
00213:                 )
00214:                 session = load_session()
00215: 
00216:             elif choice == "10":
00217:                 include_manual = ask_bool("Includere manuali?", default=True)
00218:                 skip_npu = ask_bool("Saltare NPU heavy pass? La capsule service viene comunque creata", default=True)
00219:                 run_dual_ai(session, phase="implementation", include_manual=include_manual, skip_npu=skip_npu)
00220:                 session = load_session()
00221: 
00222:             elif choice == "11":
00223:                 pass
00224: 
00225:             elif choice == "12":
00226:                 session = set_debug_enabled(not session.debug_enabled)
00227:                 print(f"Debug dettagliato: {'ON' if session.debug_enabled else 'OFF'}")
00228: 
00229:             elif choice == "13":
00230:                 targets = cleanup_intermediate_targets(session, include_all_tracks=True, include_logs=True)
00231:                 if confirm_cleanup("Pulizia intermedi progetto", targets):
00232:                     result = cleanup_intermediates(session, include_all_tracks=True, include_logs=True)
00233:                     print(f"Eliminati: {result.metadata.get('deleted_count', 0) if result.metadata else 0}")
00234:                     session = load_session()
00235: 
00236:             elif choice == "14":
00237:                 targets = cleanup_render_frame_targets(session)
00238:                 if confirm_cleanup("Pulizia frame render", targets):
00239:                     result = cleanup_render_frames(session)
00240:                     print(f"Eliminati: {result.metadata.get('deleted_count', 0) if result.metadata else 0}")
00241:                     session = load_session()
00242: 
00243:             elif choice == "15":
00244:                 print(run_advanced_debug_check(probe_write=True))
00245: 
00246:             elif choice == "16":
00247:                 process = open_debug_monitor_window(interval=3.0, probe_write=True)
00248:                 print(f"Debug monitor aperto in una nuova finestra. PID: {process.pid}")
00249: 
00250:             elif choice == "17":
00251:                 result = mark_active_operation_interrupted("manual interrupt from workflow shell")
00252:                 print(f"Registrata interruzione: {result.operation}, elapsed={result.elapsed_sec}s")
00253:                 session = load_session()
00254: 
00255:             elif choice == "18":
00256:                 force = ask_bool("Forzare rebuild anche se cache valida?", default=False)
00257:                 run_project_ai_index(session, force=force)
00258:                 session = load_session()
00259: 
00260:             elif choice == "19":
00261:                 run_scene_director_brief(session)
00262:                 session = load_session()
00263: 
00264:             elif choice == "20":
00265:                 print(format_project_storage_stats(build_project_storage_stats(session)))
00266: 
00267:             elif choice == "21":
00268:                 creative = choose_model("Creative model per piano/visione", session.creative_model)
00269:                 technical = choose_model("Technical model per script Python Blender", session.technical_model)
```
