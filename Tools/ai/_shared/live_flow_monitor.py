"""Live process monitoring helpers for human-visible operator runs."""

from __future__ import annotations

import json
import queue
import re
import subprocess
import threading
import time
from pathlib import Path
from typing import Any

from Tools.ai._shared.live_flow_status import (
    collect_flow_status,
    render_console_line,
    render_flow_markdown,
)
from Tools.ai._shared.process_tree import terminate_process_tree

CRLF_WARNING_RE = re.compile(r"^warning: in the working copy of '([^']+)', CRLF will be replaced by LF the next time Git touches it$")


def run_monitored_command(
    command: list[str],
    cwd: Path,
    *,
    timeout_seconds: int | None = None,
    env: dict[str, str] | None = None,
    flow_dir: Path | None = None,
    status_name: str = "operator_live_flow",
    phase: str = "command",
    status_interval_seconds: float = 10.0,
    tail_chars: int = 6000,
    keyboard_interrupt: str = "return",
) -> dict[str, Any]:
    """Run a child process with heartbeat artifacts and compact console status."""

    flow_paths = _flow_paths(flow_dir, status_name)
    if flow_dir:
        Path(flow_dir).mkdir(parents=True, exist_ok=True)
    stdout_tail = ""
    stderr_tail = ""
    crlf_paths: set[str] = set()
    crlf_count = 0
    output_queue: queue.Queue[tuple[str, str]] = queue.Queue()
    started = time.time()
    process: subprocess.Popen[str] | None = None
    timed_out = False
    interrupted = False
    returncode = 127

    def remember(text: str, value: str) -> str:
        text = (text + value)[-tail_chars * 2 :]
        return text[-tail_chars:]

    def drain_output() -> None:
        nonlocal stdout_tail, stderr_tail, crlf_count
        while True:
            try:
                stream, line = output_queue.get_nowait()
            except queue.Empty:
                return
            if stream == "stdout":
                stdout_tail = remember(stdout_tail, line)
                continue
            match = CRLF_WARNING_RE.match(line.rstrip())
            if match:
                crlf_count += 1
                crlf_paths.add(match.group(1))
                continue
            stderr_tail = remember(stderr_tail, line)

    def write_status(status: str) -> None:
        elapsed = max(0.0, time.time() - started)
        run_status = collect_flow_status(flow_dir) if flow_dir else {}
        payload = {
            "schema_version": 1,
            "kind": "operator_live_flow_status",
            "phase": phase,
            "status": status,
            "pid": process.pid if process is not None else None,
            "elapsed_seconds": round(elapsed, 3),
            "timeout_seconds": timeout_seconds,
            "command": command,
            "cwd": str(cwd),
            "returncode": process.returncode if process is not None else None,
            "crlf_warning_count": crlf_count,
            "crlf_warning_sample_paths": sorted(crlf_paths)[:20],
            "stdout_tail": stdout_tail[-2000:],
            "stderr_tail": stderr_tail[-2000:],
            "run_status": run_status,
        }
        _write_json(flow_paths.get("json"), payload)
        _write_text(flow_paths.get("markdown"), render_flow_markdown(payload))
        _append_jsonl(flow_paths.get("events"), payload)
        print(render_console_line(payload), flush=True)

    try:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
        )
        _start_reader(process.stdout, "stdout", output_queue)
        _start_reader(process.stderr, "stderr", output_queue)
        next_status = 0.0
        while True:
            drain_output()
            now = time.time()
            if now >= next_status:
                write_status("running")
                next_status = now + max(2.0, float(status_interval_seconds))
            if timeout_seconds is not None and now - started > timeout_seconds:
                timed_out = True
                terminate_process_tree(process)
                break
            if process.poll() is not None:
                break
            time.sleep(0.2)
    except Exception as exc:  # noqa: BLE001 - process launch/runtime failure is report evidence.
        returncode = 127
        stderr_tail = remember(stderr_tail, f"\n{type(exc).__name__}: {exc}")
    except KeyboardInterrupt:
        interrupted = True
        if process is not None:
            terminate_process_tree(process)
    finally:
        if process is not None:
            try:
                process.wait(timeout=5)
            except Exception:
                terminate_process_tree(process)
            drain_output()
            returncode = process.returncode if process.returncode is not None else 130
        if timed_out:
            returncode = 124
            stderr_tail = remember(stderr_tail, f"\ncommand timeout after {timeout_seconds} seconds")
        if interrupted:
            returncode = 130
            stderr_tail = remember(stderr_tail, "\ncommand interrupted by operator")
        write_status("interrupted" if interrupted else ("timeout" if timed_out else "completed"))

    result = {
        "command": command,
        "returncode": returncode,
        "passed": returncode == 0 and not timed_out and not interrupted,
        "timeout": timed_out,
        "keyboard_interrupt": interrupted,
        "stdout_tail": stdout_tail[-tail_chars:],
        "stderr_tail": stderr_tail[-tail_chars:],
        "crlf_warning_count": crlf_count,
        "crlf_warning_sample_paths": sorted(crlf_paths)[:50],
        "flow_status_json": str(flow_paths.get("json") or ""),
        "flow_status_markdown": str(flow_paths.get("markdown") or ""),
        "flow_event_log": str(flow_paths.get("events") or ""),
    }
    if interrupted and keyboard_interrupt == "exit":
        raise SystemExit(130)
    return result


def _start_reader(stream: Any, name: str, output_queue: queue.Queue[tuple[str, str]]) -> None:
    def read() -> None:
        if stream is None:
            return
        for line in stream:
            output_queue.put((name, line))

    thread = threading.Thread(target=read, daemon=True)
    thread.start()


def _flow_paths(flow_dir: Path | None, status_name: str) -> dict[str, Path | None]:
    if not flow_dir:
        return {"json": None, "markdown": None, "events": None}
    root = Path(flow_dir)
    return {"json": root / f"{status_name}.json", "markdown": root / f"{status_name}.md", "events": root / f"{status_name}.jsonl"}


def _write_json(path: Path | None, payload: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_text(path: Path | None, text: str) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _append_jsonl(path: Path | None, payload: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
