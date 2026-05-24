"""Provider lane hierarchy and context-budget helpers."""

from __future__ import annotations

from typing import Any

GPU1_LANE = "gpu1_planner"
GPU0_LANE = "gpu0_peer"
NPU_LANE = "npu_micro_task_auditor"
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
    if model and model.lower() != "auto":
        return model
    raise RuntimeError("missing explicit GPU1 provider model; pass --provider-model")


def gpu0_ollama_num_ctx_config(args: Any) -> dict[str, Any]:
    cli_value = _positive_int(getattr(args, "gpu0_ollama_num_ctx", 0))
    if not cli_value:
        raise RuntimeError("missing explicit GPU0 context budget; pass --gpu0-ollama-num-ctx")
    return _cfg(cli_value, _source(args, "gpu0_ollama_num_ctx"), "--gpu0-ollama-num-ctx")


def gpu0_ollama_num_ctx(args: Any) -> int:
    return int(gpu0_ollama_num_ctx_config(args)["effective_value"])


def gpu0_max_new_tokens_config(args: Any) -> dict[str, Any]:
    cli_value = _positive_int(getattr(args, "gpu0_max_new_tokens", 0))
    if not cli_value:
        raise RuntimeError("missing explicit GPU0 token budget; pass --gpu0-max-new-tokens")
    value = cli_value
    source = _source(args, "gpu0_max_new_tokens")
    override_path = "--gpu0-max-new-tokens"
    max_new = _positive_int(getattr(args, "max_new_tokens", 0)) or value
    return {
        "effective_value": max(32, min(max_new, value)),
        "source": source,
        "override_path": override_path,
    }


def gpu0_max_new_tokens(args: Any) -> int:
    return int(gpu0_max_new_tokens_config(args)["effective_value"])


def operator_effective_config(args: Any, *, gpu1_ctx: int, gpu0_ctx: int) -> dict[str, Any]:
    gpu0_tokens = gpu0_max_new_tokens_config(args)
    return {
        "gpu1.ollama_num_ctx": _cfg(gpu1_ctx, _source(args, "ollama_num_ctx"), "--ollama-num-ctx"),
        "gpu1.max_new_tokens": _cfg(
            _positive_int(getattr(args, "max_new_tokens", 0)), _source(args, "max_new_tokens"), "--max-new-tokens"
        ),
        "gpu0.ollama_num_ctx": _cfg(gpu0_ctx, _source(args, "gpu0_ollama_num_ctx"), "--gpu0-ollama-num-ctx"),
        "gpu0.max_new_tokens": gpu0_tokens,
        "npu.max_context_chars": _cfg(
            _positive_int(getattr(args, "npu_max_context_chars", 0)),
            _source(args, "npu_max_context_chars"),
            "--npu-max-context-chars",
        ),
        "npu.max_prompt_chars": _cfg(
            _positive_int(getattr(args, "npu_max_prompt_chars", 0)),
            _source(args, "npu_max_prompt_chars"),
            "--npu-max-prompt-chars",
        ),
        "npu.max_new_tokens": _cfg(
            _positive_int(getattr(args, "npu_max_new_tokens", 0)),
            _source(args, "npu_max_new_tokens"),
            "--npu-max-new-tokens",
        ),
        "max_provider_revisions": _cfg(
            _positive_int(getattr(args, "max_provider_revisions", 0)),
            _source(args, "max_provider_revisions"),
            "--max-provider-revisions",
        ),
        "keep_alive": _cfg(str(getattr(args, "keep_alive", "") or ""), _source(args, "keep_alive"), "--keep-alive"),
    }


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
            "max_new_tokens_source": _source(args, "max_new_tokens"),
            "max_new_tokens_override_path": "--max-new-tokens",
            "relative_size": "maximum",
        }
    if lane == GPU0_LANE:
        gpu0_tokens = gpu0_max_new_tokens_config(args)
        return {
            "kind": "ollama_context_budget",
            "ollama_num_ctx": int(gpu0_ctx),
            "max_new_tokens": int(gpu0_tokens["effective_value"]),
            "max_new_tokens_source": gpu0_tokens["source"],
            "max_new_tokens_override_path": gpu0_tokens["override_path"],
            "relative_size": "short_secondary_packet_only",
        }
    if lane == NPU_LANE:
        return {
            "kind": "openvino_micro_context_budget",
            "max_context_chars": int(getattr(args, "npu_max_context_chars", 0) or 0),
            "max_prompt_chars": int(getattr(args, "npu_max_prompt_chars", 0) or 0),
            "max_new_tokens": int(getattr(args, "npu_max_new_tokens", 0) or 0),
            "max_new_tokens_source": _source(args, "npu_max_new_tokens"),
            "max_new_tokens_override_path": "--npu-max-new-tokens",
            "relative_size": "short_micro",
        }
    return {}


def context_hierarchy_payload(
    args: Any,
    *,
    gpu1_ctx: Any | None = None,
    field_sources: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if field_sources is not None:
        setattr(args, "field_sources", dict(field_sources))
    effective_gpu1_ctx = _positive_int(gpu1_ctx or getattr(args, "ollama_num_ctx", 0))
    if not effective_gpu1_ctx:
        raise RuntimeError("missing explicit GPU1 context budget; pass --ollama-num-ctx")
    effective_gpu0_ctx = gpu0_ollama_num_ctx(args)
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
        "context_hierarchy_label": "context budget hierarchy valid",
        "context_hierarchy_scope": "budget_only_not_workload_or_leadership",
        "gpu1_lane_identity": "GPU1/NVIDIA primary Ollama lane",
        "gpu1_replight_scope": "health_residency_only",
        "context_hierarchy_rule": "gpu1_ctx > gpu0_ctx and npu uses short prompt/context chars",
        "operator_effective_config": operator_effective_config(
            args, gpu1_ctx=effective_gpu1_ctx, gpu0_ctx=effective_gpu0_ctx
        ),
    }


def _positive_int(value: Any) -> int:
    try:
        parsed = int(value or 0)
    except (TypeError, ValueError):
        return 0
    return parsed if parsed > 0 else 0


def _cfg(value: Any, source: str, override_path: str) -> dict[str, Any]:
    return {
        "effective_value": value,
        "source": source,
        "override_path": override_path,
    }


def _source(args: Any, field: str, default: str = "runtime_derived") -> str:
    sources = getattr(args, "field_sources", {}) or {}
    if isinstance(sources, dict):
        source = str(sources.get(field) or "").strip()
        if source:
            return source
    return default
