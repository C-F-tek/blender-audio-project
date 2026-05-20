"""Provider-native tool-call scheduling helpers for the heap gate."""

from __future__ import annotations

from typing import Any


def provider_patch_synthesis_plan(
    *,
    call: dict[str, Any],
    target_files: list[str],
    operator_request: str,
    operator_request_file: str = "",
    files_per_round: int,
    timeout_seconds: int,
) -> dict[str, Any]:
    provider_args = call.get("args") if isinstance(call.get("args"), dict) else {}
    args = {
        "target_file": target_files,
        "max_candidates": min(5, max(1, int(files_per_round))),
        "timeout_seconds": 0,
        "time_input_semantics": "counter_not_hard_tool_timeout",
    }
    if operator_request_file:
        args["operator_request_file"] = operator_request_file
        provider_args.pop("operator_request", None)
    else:
        args["operator_request"] = operator_request
    args.update(provider_args)
    return {
        "stage": 4,
        "requirement": "patch_candidate_synthesis",
        "id": "provider-native-patch-candidate-synthesis",
        "tool": "synthesize_patch_candidates",
        "args": args,
        "reason": "provider native tool call requested standalone patch candidate synthesis",
    }
