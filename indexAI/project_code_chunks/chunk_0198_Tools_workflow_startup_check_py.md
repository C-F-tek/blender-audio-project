# Project Code Chunk 198/212

- File: `Tools/workflow/startup_check.py`
- Part: `2`
- Lines: `265-284`

## Symbol Map
- Imports: `from __future__ import annotations`, `argparse`, `from dataclasses import asdict, dataclass`, `from datetime import datetime`, `from pathlib import Path`, `json`, `os`, `shutil`, `subprocess`, `sys`, `tempfile`, `time`
- Classes: `Check` line 31
- Functions: `now_iso()` line 38; `add(checks, name, status, detail, path)` line 42; `probe_write(path)` line 46; `run_probe(command, timeout, cwd)` line 57; `powershell_test_path(path)` line 74; `powershell_get_command(name)` line 88; `visible_path_exists(path)` line 101; `fallback_ollama_exe()` line 105; `check_python_runtime(checks, label, python_path, code, timeout)` line 129; `check_ollama(checks)` line 137; `build_report(project, root)` line 178; `format_report(report)` line 242; `save_report(report)` line 261; `main()` line 267
- Assignments: `THIS_DIR`, `PROJECT_DIR`, `ROOT`, `NPU_DIR`, `LOG_DIR`, `REPORT_JSON`, `REPORT_TXT`

## Content
```py
00265: 
00266: 
00267: def main() -> int:
00268:     parser = argparse.ArgumentParser(description="Spaziotempo startup service check")
00269:     parser.add_argument("--project", default=str(PROJECT_DIR))
00270:     parser.add_argument("--root", default=str(ROOT))
00271:     parser.add_argument("--json", action="store_true")
00272:     args = parser.parse_args()
00273: 
00274:     report = build_report(Path(args.project).resolve(strict=False), Path(args.root).resolve(strict=False))
00275:     save_report(report)
00276:     if args.json:
00277:         print(json.dumps(report, indent=2, ensure_ascii=False))
00278:     else:
00279:         print(format_report(report))
00280:     return 0
00281: 
00282: 
00283: if __name__ == "__main__":
00284:     raise SystemExit(main())
```
