from __future__ import annotations

import argparse
from typing import Any

from .lifecycle import (
    close_support_lanes,
    execute_post_gpu_runtime_brokers,
    launch_startup_support_lanes,
    load_gpu_report,
    poll_until_gpu_finishes,
    start_orchestrator_state,
)
from .report_builder import build_orchestrator_report


def run_orchestrator(args: argparse.Namespace) -> dict[str, Any]:
    state = start_orchestrator_state(args)
    launch_startup_support_lanes(state)
    poll_until_gpu_finishes(state)
    close_support_lanes(state)
    load_gpu_report(state)
    execute_post_gpu_runtime_brokers(state)
    return build_orchestrator_report(args, state)
