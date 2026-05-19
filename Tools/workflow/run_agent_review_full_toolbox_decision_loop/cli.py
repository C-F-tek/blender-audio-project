#!/usr/bin/env python3
"""Python control entrypoint for the full toolbox decision-loop workflow.

The public PowerShell file only resolves Python and forwards arguments here.
This runner preserves the existing CLI and runs the Python production engine.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent


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
    "RepositoryConsistencyMapWorkers": 8,
}

STRING_DEFAULTS = {
    "RepoRoot": ".",
    "Stamp": "",
    "OutputRoot": "output",
    "EvidenceDir": "docs/LOCAL_VALIDATION_EVIDENCE",
    "TaskMarkdown": "docs/LOCAL_AI_TASKS/patch-notes-quality-product-2026-05-07.md",
    "IssueNumber": "",
    "KeepAlive": "35m",
    "NpuMicroStartMode": "startup",
    "RepositoryConsistencyMapWorkerBackend": "process",
    "RepositoryConsistencyMapWorkerCpuTarget": 0.40,
    "RepositoryConsistencyMapMaxAutoWorkers": 8,
}

SWITCHES = (
    "RunGpuNpuProvider",
    "RequireProviderArtifacts",
    "RunLegacyNpuAuditorProvider",
    "SkipMemoryReload",
    "SkipPostValidationPacket",
    "SkipSharedToolboxBundle",
    "SkipNpuMicroProvider",
    "SkipNpuLiveToolSeed",
    "BuildEvidence",
    "GeneratePatchSpecs",
    "ContinueOnValidationError",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    for name, default in STRING_DEFAULTS.items():
        parser.add_argument(f"--{name}", default=default)
    for name, default in INT_DEFAULTS.items():
        parser.add_argument(f"--{name}", type=int, default=default)
    for name in SWITCHES:
        parser.add_argument(f"--{name}", action="store_true")
    return parser.parse_args()


def run_python_engine(args: argparse.Namespace) -> int:
    if str(ENGINE_DIR) not in sys.path:
        sys.path.insert(0, str(ENGINE_DIR))
    from py_engine import run_workflow  # pylint: disable=import-error,import-outside-toplevel

    return run_workflow(args)


def main() -> int:
    args = parse_args()
    return run_python_engine(args)


if __name__ == "__main__":
    raise SystemExit(main())
