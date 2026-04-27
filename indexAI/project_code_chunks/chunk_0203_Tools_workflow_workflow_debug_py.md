# Project Code Chunk 203/212

- File: `Tools/workflow/workflow_debug.py`
- Part: `3`
- Lines: `506-607`

## Symbol Map
- Imports: `from __future__ import annotations`, `from datetime import datetime`, `from pathlib import Path`, `argparse`, `json`, `os`, `shutil`, `subprocess`, `time`, `workflow_state`
- Functions: `_iso_to_dt(value)` line 15; `_format_age(seconds)` line 24; `_format_size(size)` line 37; `_read_json(path)` line 48; `read_events(max_events)` line 57; `detect_active_operation(events)` line 75; `_tail_non_empty(path, max_lines)` line 116; `_write_probe(directory)` line 126; `path_check(label, path, required, expect)` line 145; `expected_paths_for_operation(session, operation)` line 189; `collect_processes()` line 304; `collect_write_checks(probe_write)` line 338; `active_compute_processes(processes, operation)` line 361; `build_debug_report(probe_write)` line 390; `_format_check(item)` line 467; `_format_process(item)` line 475; `format_debug_report(report)` line 485; `main()` line 578

## Content
```py
00506:                 f"elapsed {_format_age(active.get('elapsed_sec'))}"
00507:             )
00508:     else:
00509:         lines.append(f"Active:    no running operation detected, checks based on {report['operation_for_checks']}")
00510: 
00511:     last = report.get("last_result") or {}
00512:     if isinstance(last, dict) and last:
00513:         lines.append(
00514:             f"Last:      {last.get('operation')} ok={last.get('ok')} "
00515:             f"ended={last.get('ended_at')} elapsed={last.get('elapsed_sec')}"
00516:         )
00517: 
00518:     if report["warnings"]:
00519:         lines.append("")
00520:         lines.append("Warnings:")
00521:         for warning in report["warnings"]:
00522:             lines.append(f"  - {warning}")
00523: 
00524:     lines.append("")
00525:     lines.append("Write Checks:")
00526:     for item in report["write_checks"]:
00527:         lines.append("  " + _format_check(item))
00528: 
00529:     lines.append("")
00530:     lines.append("Common Paths:")
00531:     for item in report["common_checks"]:
00532:         lines.append("  " + _format_check(item))
00533: 
00534:     if report["input_checks"]:
00535:         lines.append("")
00536:         lines.append("Inputs For Active Operation:")
00537:         for item in report["input_checks"]:
00538:             lines.append("  " + _format_check(item))
00539: 
00540:     if report["output_checks"]:
00541:         lines.append("")
00542:         lines.append("Expected Outputs / Pending Files:")
00543:         for item in report["output_checks"]:
00544:             lines.append("  " + _format_check(item))
00545: 
00546:     if report["progress_checks"]:
00547:         lines.append("")
00548:         lines.append("Progress Files:")
00549:         for item in report["progress_checks"]:
00550:             lines.append("  " + _format_check(item))
00551: 
00552:     if report["progress_previews"]:
00553:         lines.append("")
00554:         lines.append("Progress Preview:")
00555:         for preview in report["progress_previews"]:
00556:             lines.append(f"  {preview['label']}: {preview['path']}")
00557:             tail = preview.get("tail") or ["<empty or missing>"]
00558:             for line in tail:
00559:                 lines.append(f"    {line[:240]}")
00560: 
00561:     lines.append("")
00562:     lines.append("AI / Render Processes:")
00563:     processes = report.get("processes") or []
00564:     if processes:
00565:         for item in processes[:14]:
00566:             lines.append("  " + _format_process(item))
00567:     else:
00568:         lines.append("  <no process snapshot available>")
00569: 
00570:     lines.append("")
00571:     lines.append("Recent Events:")
00572:     for event in report["recent_events"]:
00573:         lines.append(f"  {event.get('time')} {event.get('operation')}::{event.get('event')}")
00574: 
00575:     return "\n".join(lines)
00576: 
00577: 
00578: def main() -> int:
00579:     parser = argparse.ArgumentParser(description="Spaziotempo workflow advanced debug checker.")
00580:     parser.add_argument("--json", action="store_true", help="Print raw JSON report.")
00581:     parser.add_argument("--watch", action="store_true", help="Refresh the report in this window.")
00582:     parser.add_argument("--interval", type=float, default=3.0, help="Watch refresh interval in seconds.")
00583:     parser.add_argument("--no-write-probe", action="store_true", help="Use access checks only, no temporary write probes.")
00584:     args = parser.parse_args()
00585: 
00586:     probe_write = not args.no_write_probe
00587:     if args.watch:
00588:         try:
00589:             while True:
00590:                 os.system("cls" if os.name == "nt" else "clear")
00591:                 report = build_debug_report(probe_write=probe_write)
00592:                 print(format_debug_report(report))
00593:                 print("\nCtrl+C per chiudere questa finestra debug.")
00594:                 time.sleep(max(1.0, args.interval))
00595:         except KeyboardInterrupt:
00596:             return 0
00597: 
00598:     report = build_debug_report(probe_write=probe_write)
00599:     if args.json:
00600:         print(json.dumps(report, indent=2, ensure_ascii=False))
00601:     else:
00602:         print(format_debug_report(report))
00603:     return 0
00604: 
00605: 
00606: if __name__ == "__main__":
00607:     raise SystemExit(main())
```
