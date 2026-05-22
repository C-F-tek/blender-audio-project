#!/usr/bin/env python3
"""PowerShell-specific patchkit helpers."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


def run_parser(path: Path) -> tuple[bool, str]:
    ps_path = str(path).replace("'", "''")
    command = (
        "$tokens=$null;"
        "$errors=$null;"
        f"$null=[System.Management.Automation.Language.Parser]::ParseFile('{ps_path}',[ref]$tokens,[ref]$errors);"
        "if($errors.Count -gt 0){$errors | ForEach-Object { Write-Error $_.Message };exit 1}else{exit 0}"
    )
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0, result.stdout + result.stderr


def brace_delta(line: str) -> int:
    return line.count("{") - line.count("}")


def find_invoke_checked_block_end(lines: list[str], label: str) -> int | None:
    start = None
    for index, line in enumerate(lines):
        if label in line:
            start = index
            break
    if start is None:
        return None
    depth = 0
    seen_open = False
    for index in range(start, len(lines)):
        depth += brace_delta(lines[index])
        if "{" in lines[index]:
            seen_open = True
        if seen_open and depth <= 0:
            return index
    return None


def insert_after_invoke_checked(
    text: str, label: str, content: str, *, idempotency_marker: str = ""
) -> tuple[bool, str, str]:
    if idempotency_marker and idempotency_marker in text:
        return False, text, "idempotency marker already present"
    lines = text.splitlines()
    end = find_invoke_checked_block_end(lines, label)
    if end is None:
        raise ValueError(f"Invoke-Checked block not found or unterminated: {label}")
    new_lines = lines[: end + 1] + ["", *content.strip("\n").splitlines(), ""] + lines[end + 1 :]
    return True, "\n".join(new_lines) + "\n", "insert_after_invoke_checked"


def assert_no_naked_throw(text: str) -> None:
    if re.search(r"^\s*throw\s*$", text, flags=re.MULTILINE):
        raise ValueError("naked throw remains in PowerShell file")
