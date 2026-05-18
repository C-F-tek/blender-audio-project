"""CLI for workflow debug reports."""

from __future__ import annotations

import argparse
import json
import os
import time

from .formatting import format_debug_report
from .report import build_debug_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Spaziotempo workflow advanced debug checker.")
    parser.add_argument("--json", action="store_true", help="Print raw JSON report.")
    parser.add_argument("--watch", action="store_true", help="Refresh the report in this window.")
    parser.add_argument("--interval", type=float, default=3.0, help="Watch refresh interval.")
    parser.add_argument(
        "--no-write-probe",
        action="store_true",
        help="Use access checks only, no temporary write probes.",
    )
    args = parser.parse_args()

    probe_write = not args.no_write_probe
    if args.watch:
        try:
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                report = build_debug_report(probe_write=probe_write)
                print(format_debug_report(report))
                print("\nCtrl+C per chiudere questa finestra debug.")
                time.sleep(max(1.0, args.interval))
        except KeyboardInterrupt:
            return 0

    report = build_debug_report(probe_write=probe_write)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(format_debug_report(report))
    return 0
