"""Provider lane hierarchy and context-budget helpers."""

from __future__ import annotations

from typing import Any

GPU1_LANE = "gpu1_planner"
GPU0_LANE = "gpu0_peer"
NPU_LANE = "npu_micro_task_auditor"
GPU1_OPERATIONAL_MODEL = "qwen2.5-coder:14b"
GPU0_OPERATIONAL_MODEL = "qwen3:1.7b"
CLOSURE_OWNER = GPU1_LANE

_LANE_HIERARCHY: dict[str, dict[str, Any]] = {
    GPU1_LANE: {
        "lane_tier": "primary",
        "authority": "leader",
        "provider_role": "gpu1_planner",
        "primary_closer": True,
        "peer_only": False,
    },
    GPU0_LANE: {
        "lane_tier": "coworker_medium",
        "authority": "coworker",
        "provider_role": "gpu0_reviewer_refiner",
        "primary_closer": False,
        "peer_only": True,
    },
    NPU_LANE: {
        "lane_tier": "micro_fast",
        "authority": "micro_tool",
        "provider_role": "npu_auditor",
        "primary_closer": False,
        "peer_only": True,
    },
}


def lane_hierarchy(lane: str) -> dict[str, Any]:
    payload = dict(_LANE_HIERARCHY.get(str(lane), {}))
    payload.setdefault("lane_tier", "unknown")
    payload.setdefault("authority", "unknown")
    payload["closure_owner"] = CLOSURE_OWNER
    return payload


def preferred_gpu1_model(requested: str | None, *, strict: bool = False) -> str:
    model = str(requested or "").strip()
    if strict and model and model.lower() != "auto":
        return model
    return GPU1_OPERATIONAL_MODEL


def gpu0_ollama_num_ctx(gpu1_ctx: Any) -> int:
    try:
        parsed = int(gpu1_ctx or 0)
    except (TypeError, ValueError):
        parsed = 8192
    parsed = max(1024, parsed)
    if parsed <= 2048:
        return 1024
    return max(1024, min(2048, parsed - 1024))


def lane_context_budget(
    lane: str,
    *,
    gpu1_ctx: int,
    gpu0_ctx: int,
    args: Any,
) -> dict[str, Any]:
    if lane == GPU1_LANE:
        return {
            "kind": "ollama_context_budget",
            "ollama_num_ctx": int(gpu1_ctx),
            "max_new_tokens": int(getattr(args, "max_new_tokens", 0) or 0),
            "relative_size": "maximum",
        }
    if lane == GPU0_LANE:
        return {
            "kind": "ollama_context_budget",
            "ollama_num_ctx": int(gpu0_ctx),
            "max_new_tokens": int(min(int(getattr(args, "max_new_tokens", 0) or 0), 96)),
            "relative_size": "short_secondary_packet_only",
        }
    if lane == NPU_LANE:
        return {
            "kind": "openvino_micro_context_budget",
            "max_context_chars": int(getattr(args, "npu_max_context_chars", 0) or 0),
            "max_prompt_chars": int(getattr(args, "npu_max_prompt_chars", 0) or 0),
            "max_new_tokens": int(getattr(args, "npu_max_new_tokens", 0) or 0),
            "relative_size": "short_micro",
        }
    return {}


def context_hierarchy_payload(args: Any, *, gpu1_ctx: Any | None = None) -> dict[str, Any]:
    effective_gpu1_ctx = int(gpu1_ctx or getattr(args, "ollama_num_ctx", 0) or 8192)
    effective_gpu0_ctx = gpu0_ollama_num_ctx(effective_gpu1_ctx)
    npu_prompt = int(getattr(args, "npu_max_prompt_chars", 0) or 0)
    npu_context = int(getattr(args, "npu_max_context_chars", 0) or 0)
    valid = bool(effective_gpu1_ctx > effective_gpu0_ctx >= 1024 and 0 < npu_prompt <= npu_context)
    return {
        "gpu1_context_budget": lane_context_budget(
            GPU1_LANE, gpu1_ctx=effective_gpu1_ctx, gpu0_ctx=effective_gpu0_ctx, args=args
        ),
        "gpu0_context_budget": lane_context_budget(
            GPU0_LANE, gpu1_ctx=effective_gpu1_ctx, gpu0_ctx=effective_gpu0_ctx, args=args
        ),
        "npu_context_budget": lane_context_budget(
            NPU_LANE, gpu1_ctx=effective_gpu1_ctx, gpu0_ctx=effective_gpu0_ctx, args=args
        ),
        "context_hierarchy_valid": valid,
        "context_hierarchy_rule": "gpu1_ctx > gpu0_ctx and npu uses short prompt/context chars",
    }
