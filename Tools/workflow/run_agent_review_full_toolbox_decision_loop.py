#!/usr/bin/env python3
"""Python control entrypoint for the full toolbox decision-loop workflow.

The public PowerShell file now only resolves Python and forwards arguments here.
This runner preserves the existing CLI and runs the Python production engine by
default. The old PowerShell implementation is available only through an
explicit fallback flag.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


CURRENT = Path(__file__).resolve()
WORKFLOW_DIR = CURRENT.parent
REPO_ROOT_DEFAULT = WORKFLOW_DIR.parents[1]
ENGINE_DIR = WORKFLOW_DIR / "run_agent_review_full_toolbox_decision_loop"
LEGACY_IMPL = ENGINE_DIR / "main.ps1"


INT_DEFAULTS = {
    "BudgetMinutes": 30,
    "MaxRounds": 20,
    "FilesPerRound": 8,
    "MaxContextFiles": 220,
    "MaxCharsPerFile": 6000,
    "MaxNewTokens": 3600,
    "MaxRecommendations": 20,
    "MaxPatchPlans": 20,
    "NpuAuditorEveryRounds": 3,
    "NpuAuditorTimeoutSeconds": 420,
    "NpuMaxContextChars": 8000,
    "NpuMaxPromptChars": 1200,
    "NpuMaxNewTokens": 384,
    "NpuMicroTimeoutSeconds": 60,
    "NpuMicroBrokerTimeoutSeconds": 90,
    "NpuFinalWaitSeconds": 180,
    "NpuMicroMaxLiveProviderRounds": 0,
    "MinRecommendations": 1,
    "MinPatchPlans": 1,
    "RepositoryConsistencyMapWorkers": 0,
}

STRING_DEFAULTS = {
    "RepoRoot": ".",
    "Stamp": "",
    "OutputRoot": "output",
    "EvidenceDir": "docs/LOCAL_VALIDATION_EVIDENCE",
    "KeepAlive": "35m",
    "NpuMicroStartMode": "deferred",
}

SWITCHES = (
    "RunGpuNpuProvider",
    "RequireProviderArtifacts",
    "RunLegacyNpuAuditorProvider",
    "SkipMemoryReload",
    "SkipPostValidationPacket",
    "SkipSharedToolboxBundle",
    "UseLegacyPowerShellImplementation",
    "SkipNpuMicroProvider",
    "SkipNpuLiveToolSeed",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--PowerShellExe", default="powershell.exe")
    for name, default in STRING_DEFAULTS.items():
        parser.add_argument(f"--{name}", default=default)
    for name, default in INT_DEFAULTS.items():
        parser.add_argument(f"--{name}", type=int, default=default)
    for name in SWITCHES:
        parser.add_argument(f"--{name}", action="store_true")
    return parser.parse_args()


def build_command(args: argparse.Namespace) -> list[str]:
    if not LEGACY_IMPL.exists():
        raise FileNotFoundError(f"full toolbox implementation not found: {LEGACY_IMPL}")
    command = [
        args.PowerShellExe,
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(LEGACY_IMPL),
    ]
    for name in STRING_DEFAULTS:
        value = getattr(args, name)
        if value != "":
            command.extend((f"-{name}", str(value)))
    if getattr(args, "Stamp") == "":
        command.extend(("-Stamp", ""))
    for name in INT_DEFAULTS:
        command.extend((f"-{name}", str(getattr(args, name))))
    for name in SWITCHES:
        if name != "UseLegacyPowerShellImplementation" and getattr(args, name):
            command.append(f"-{name}")
    return command


def run_python_engine(args: argparse.Namespace) -> int:
    if str(ENGINE_DIR) not in sys.path:
        sys.path.insert(0, str(ENGINE_DIR))
    from py_engine import run_workflow  # pylint: disable=import-error,import-outside-toplevel

    return run_workflow(args)


def main() -> int:
    args = parse_args()
    repo_root = Path(args.RepoRoot).resolve() if args.RepoRoot else REPO_ROOT_DEFAULT
    if args.UseLegacyPowerShellImplementation:
        command = build_command(args)
        return subprocess.call(command, cwd=repo_root)
    return run_python_engine(args)


if __name__ == "__main__":
    raise SystemExit(main())
