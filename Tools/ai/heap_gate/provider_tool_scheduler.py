"""Provider-native tool-call scheduling helpers for the heap gate."""

from __future__ import annotations

from typing import Any


def provider_patch_synthesis_plan(
    *,
    call: dict[str, Any],
    target_files: list[str],
    operator_request: str,
    files_per_round: int,
    timeout_seconds: int,
) -> dict[str, Any]:
    provider_args = call.get("args") if isinstance(call.get("args"), dict) else {}
    args = {
        "target_file": target_files,
        "operator_request": operator_request,
        "max_candidates": min(5, max(1, int(files_per_round))),
        "timeout_seconds": min(max(int(timeout_seconds), 60), 600),
    }
    args.update(provider_args)
    return {
        "stage": 4,
        "requirement": "patch_candidate_synthesis",
        "id": "provider-native-patch-candidate-synthesis",
        "tool": "synthesize_patch_candidates",
        "args": args,
        "reason": "provider native tool call requested standalone patch candidate synthesis",
    }
