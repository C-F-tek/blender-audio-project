from __future__ import annotations

from .cli import main, parse_args
from .common import (
    DEFAULT_LOG_DIR,
    DEFAULT_REPORT_JSON,
    NPU_DIR,
    PROJECT_DIR,
    THIS_DIR,
    WORKSPACE_ROOT,
    Check,
    add,
    check_ollama,
    check_python_runtime,
    fallback_ollama_exe,
    now_iso,
    powershell_get_command,
    powershell_test_path,
    probe_write,
    run_probe,
    visible_path_exists,
)
from .report import build_report, format_report, save_report

__all__ = [
    "Check",
    "DEFAULT_LOG_DIR",
    "DEFAULT_REPORT_JSON",
    "NPU_DIR",
    "PROJECT_DIR",
    "THIS_DIR",
    "WORKSPACE_ROOT",
    "add",
    "build_report",
    "check_ollama",
    "check_python_runtime",
    "fallback_ollama_exe",
    "format_report",
    "main",
    "now_iso",
    "parse_args",
    "powershell_get_command",
    "powershell_test_path",
    "probe_write",
    "run_probe",
    "save_report",
    "visible_path_exists",
]
