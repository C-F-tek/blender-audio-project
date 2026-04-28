from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime


ROOT = Path.home() / "blender"
PROJECT_DIR = ROOT / "blender-audio-project"
AUTO_PUSH_SCRIPT = PROJECT_DIR / "Tools" / "git" / "auto_push_generated_data.ps1"


@dataclass
class AutoPushResult:
    operation: str
    ok: bool
    started_at: str
    ended_at: str
    elapsed_sec: float
    command: list[str]
    cwd: str
    returncode: int
    stdout_tail: str
    error: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def powershell_executable() -> str:
    for candidate in ("pwsh", "powershell.exe", "powershell"):
        try:
            completed = subprocess.run(
                [candidate, "-NoProfile", "-Command", "$PSVersionTable.PSVersion.Major"],
                cwd=str(PROJECT_DIR),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
        except FileNotFoundError:
            continue
        if completed.returncode == 0:
            return candidate
    raise FileNotFoundError("PowerShell non trovato: serve pwsh o powershell.exe nel PATH.")


def build_auto_push_command(
    *,
    include_output_json: bool = False,
    include_docs: bool = False,
    include_all_generated: bool = False,
    pull_first: bool = False,
    dry_run: bool = False,
    message: str = "chore: update app-generated technical data",
) -> list[str]:
    if not AUTO_PUSH_SCRIPT.exists():
        raise FileNotFoundError(f"Script auto-push non trovato: {AUTO_PUSH_SCRIPT}")

    command = [
        powershell_executable(),
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(AUTO_PUSH_SCRIPT),
        "-RepoPath",
        str(PROJECT_DIR),
        "-Message",
        message,
    ]

    if include_output_json:
        command.append("-IncludeOutputJson")
    if include_docs:
        command.append("-IncludeDocs")
    if include_all_generated:
        command.append("-IncludeAllGenerated")
    if pull_first:
        command.append("-PullFirst")
    if dry_run:
        command.append("-DryRun")

    return command


def run_auto_push_generated_data(
    *,
    include_output_json: bool = False,
    include_docs: bool = False,
    include_all_generated: bool = False,
    pull_first: bool = False,
    dry_run: bool = False,
    message: str = "chore: update app-generated technical data",
    check: bool = True,
) -> AutoPushResult:
    started_at = now_iso()
    start = time.perf_counter()
    command = build_auto_push_command(
        include_output_json=include_output_json,
        include_docs=include_docs,
        include_all_generated=include_all_generated,
        pull_first=pull_first,
        dry_run=dry_run,
        message=message,
    )

    print("\n$ " + " ".join(f'\"{part}\"' if " " in part else part for part in command))
    completed = subprocess.run(
        command,
        cwd=str(PROJECT_DIR),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = completed.stdout or ""
    if output:
        print(output.rstrip())

    result = AutoPushResult(
        operation="auto_push_generated_data",
        ok=completed.returncode == 0,
        started_at=started_at,
        ended_at=now_iso(),
        elapsed_sec=round(time.perf_counter() - start, 4),
        command=command,
        cwd=str(PROJECT_DIR),
        returncode=completed.returncode,
        stdout_tail=output[-8000:],
        error=None if completed.returncode == 0 else f"auto-push fallito con exit code {completed.returncode}",
    )

    if check and not result.ok:
        raise RuntimeError(result.error or "auto-push fallito")

    return result


def main() -> int:
    include_output_json = "--include-output-json" in sys.argv
    include_docs = "--include-docs" in sys.argv
    include_all_generated = "--include-all-generated" in sys.argv
    pull_first = "--pull-first" in sys.argv
    dry_run = "--dry-run" in sys.argv
    result = run_auto_push_generated_data(
        include_output_json=include_output_json,
        include_docs=include_docs,
        include_all_generated=include_all_generated,
        pull_first=pull_first,
        dry_run=dry_run,
        check=False,
    )
    return 0 if result.ok else result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
