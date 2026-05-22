"""Ollama provider role evidence helpers."""

from __future__ import annotations

from typing import Any


def ollama_lane_role(lane: str) -> str:
    if lane == "gpu0_peer":
        return "gpu0_peer_reviewer_refiner"
    if lane == "gpu1_planner":
        return "primary_planner_cumulative_responder"
    return "ollama_provider"


def ollama_lane_compute_device(lane: str, verified: bool) -> str:
    if lane == "gpu0_peer":
        return "ollama/gpu0-vulkan" if verified else "ollama/gpu0-vulkan_unproven"
    if lane == "gpu1_planner":
        return "ollama/gpu1" if verified else "ollama/gpu1_unproven"
    return "ollama/gpu" if verified else "ollama/gpu_unproven"


def apply_ollama_lane_evidence(
    *,
    lane: str,
    residency: dict[str, Any],
    require_gpu_residency: bool,
) -> dict[str, Any]:
    evidence = dict(residency)
    verified = bool(evidence.get("provider_device_verified"))
    evidence["provider_backend"] = "ollama"
    evidence["provider_compute_device"] = ollama_lane_compute_device(lane, verified)
    if lane == "gpu0_peer":
        evidence["ollama_vulkan_required"] = True
        evidence["ollama_vulkan_backend_assumed_from_server_policy"] = True
        if require_gpu_residency and not verified:
            evidence["product_blocked_reason"] = "gpu0_ollama_vulkan_unavailable"
    return evidence
