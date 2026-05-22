"""Process-tree termination helpers for bounded runtime phases."""

from __future__ import annotations

import os
import signal
import subprocess
from typing import Any


def terminate_process_tree(process: Any, timeout_seconds: float = 3.0) -> None:
    """Terminate a subprocess and its children without raising on cleanup errors."""
    pid = int(getattr(process, "pid", 0) or 0)
    if pid <= 0:
        return
    if os.name == "nt":
        try:
            subprocess.run(
                ["taskkill", "/PID", str(pid), "/T", "/F"],
                capture_output=True,
                text=True,
                check=False,
                timeout=timeout_seconds,
            )
        except BaseException:
            try:
                process.kill()
            except BaseException:
                pass
        return
    try:
        os.killpg(os.getpgid(pid), signal.SIGTERM)
    except BaseException:
        try:
            process.terminate()
        except BaseException:
            return
