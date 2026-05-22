from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any

from ia_carmine.providers.ollama.sdk_client import OllamaSdkClient


FALLBACK_ORDER = (
    "qwen3-coder:latest",
    "qwen2.5-coder:14b",
    "autumnzsd/qwen2.5-coder-tools:latest",
    "qwen3:1.7b",
)
CTX_OVERHEAD_BYTES_PER_TOKEN = 128 * 1024
VRAM_SAFETY = 0.90


def parse_context_candidates(value: str | None, fallback: int) -> list[int]:
    parsed: list[int] = []
    for raw in str(value or "").replace(";", ",").split(","):
        try:
            item = int(raw.strip())
        except ValueError:
            continue
        if item >= 1024 and item not in parsed:
            parsed.append(item)
    if not parsed:
        parsed = [int(fallback)] if int(fallback or 0) >= 1024 else [8192, 4096]
    return parsed


def ollama_model_inventory() -> dict[str, dict[str, Any]]:
    inventory = _api_inventory()
    cli_inventory = _cli_inventory()
    for name, item in cli_inventory.items():
        inventory.setdefault(name, {}).update(
            {key: value for key, value in item.items() if value not in ("", None)}
        )
    return inventory


def nvidia_gpu_inventory() -> list[dict[str, Any]]:
    command = [
        "nvidia-smi",
        "--query-gpu=name,uuid,memory.total,memory.free",
        "--format=csv,noheader,nounits",
    ]
    try:
        completed = subprocess.run(command, text=True, capture_output=True, timeout=4, check=False)
    except Exception as exc:  # noqa: BLE001 - hardware discovery is report evidence.
        return [{"error": f"{type(exc).__name__}: {exc}"}]
    gpus: list[dict[str, Any]] = []
    for line in (completed.stdout or "").splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) < 4:
            continue
        gpus.append(
            {
                "name": parts[0],
                "uuid": parts[1],
                "memory_total_mib": _int_or_none(parts[2]),
                "memory_free_mib": _int_or_none(parts[3]),
            }
        )
    return gpus


def controlled_ollama_env_fields() -> dict[str, str]:
    fields = {"OLLAMA_MAX_LOADED_MODELS": "1", "OLLAMA_NUM_PARALLEL": "1"}
    gpus = nvidia_gpu_inventory()
    uuid = str((gpus[0] if gpus else {}).get("uuid") or "").strip()
    if uuid:
        fields["CUDA_VISIBLE_DEVICES"] = uuid
    return fields


def select_ollama_provider_model(
    requested: str | None,
    available_models: list[Any],
    *,
    num_ctx: int,
    context_candidates: str | None,
    strict: bool,
) -> dict[str, Any]:
    requested_model = str(requested or "auto").strip() or "auto"
    auto_mode = requested_model.lower() == "auto"
    contexts = parse_context_candidates(context_candidates, num_ctx)
    inventory = ollama_model_inventory()
    available = _merge_available_model_inventory(available_models, inventory)
    gpus = nvidia_gpu_inventory()
    total_mib = _first_gpu_total_mib(gpus)
    attempts: list[dict[str, Any]] = []
    candidates = _candidate_models(requested_model, auto_mode, strict, available)
    for candidate in candidates:
        if candidate not in available:
            attempts.append({"model": candidate, "available": False, "fit": False})
            continue
        size_bytes = _model_size_bytes(candidate, inventory)
        for ctx in contexts:
            fit, reason, required_mib = _fits_vram(size_bytes, ctx, total_mib)
            attempts.append(
                {
                    "model": candidate,
                    "available": True,
                    "num_ctx": ctx,
                    "size_bytes": size_bytes,
                    "required_mib_estimate": required_mib,
                    "gpu_total_mib": total_mib,
                    "fit": fit,
                    "reason": reason,
                }
            )
            if fit is not False:
                return {
                    "blocked": False,
                    "requested_provider_model": requested_model,
                    "selected_provider_model": candidate,
                    "selected_ollama_num_ctx": ctx,
                    "model_switch_reason": _switch_reason(requested_model, candidate, auto_mode),
                    "provider_repair_attempts": attempts,
                    "nvidia_gpus": gpus,
                    "ollama_models": sorted(available),
                    "ollama_context_candidates": contexts,
                }
    reason = (
        "strict_provider_model_not_vram_fit"
        if strict
        else "provider_model_auto_no_installed_model_fits_full_gpu_vram"
    )
    return {
        "blocked": True,
        "blocked_reason": reason,
        "requested_provider_model": requested_model,
        "selected_provider_model": requested_model if not auto_mode else "",
        "selected_ollama_num_ctx": contexts[0] if contexts else num_ctx,
        "model_switch_reason": reason,
        "provider_repair_attempts": attempts,
        "nvidia_gpus": gpus,
        "ollama_models": sorted(available),
        "ollama_context_candidates": contexts,
    }


def operator_gpu_observation_block_reason(text: str) -> str:
    normalized = " ".join(str(text or "").lower().split())
    if not normalized:
        return ""
    inactive_markers = (
        "gpu inattiva",
        "gpu non ha lavorato",
        "gpu non ha lav",
        "gpu1 non ha lavorato",
        "gpu1 non ha lav",
        "non ha lavor",
        "non ha lavior",
        "no observable compute",
        "no observable gpu compute",
        "no useful gpu work",
        "task manager",
        "gestione attività",
        "gestione attivita",
        "utilizzo 3%",
        "3% gpu",
    )
    if any(marker in normalized for marker in inactive_markers):
        return "gpu1_no_observable_compute"
    markers = ("cpu/gpu", "swap", "memoria sistema", "system memory", "cpu offload")
    if any(marker in normalized for marker in markers):
        return "gpu1_operator_observed_cpu_swap_or_partial_offload"
    return ""


def _candidate_models(requested: str, auto_mode: bool, strict: bool, available: list[str]) -> list[str]:
    if strict and not auto_mode:
        return [requested]
    ordered = list(FALLBACK_ORDER)
    if auto_mode:
        return [item for item in ordered if item in available] + [item for item in available if item not in ordered]
    return [requested] + [item for item in ordered if item != requested]


def _fits_vram(size_bytes: int | None, ctx: int, total_mib: int | None) -> tuple[bool | None, str, int | None]:
    if total_mib is None:
        return None, "gpu_vram_unknown_runtime_will_verify_ollama_ps", None
    if size_bytes is None:
        return None, "model_size_unknown_runtime_will_verify_ollama_ps", None
    required_mib = int((size_bytes + ctx * CTX_OVERHEAD_BYTES_PER_TOKEN) / (1024 * 1024))
    capacity_mib = int(total_mib * VRAM_SAFETY)
    return required_mib <= capacity_mib, "fits_vram_estimate" if required_mib <= capacity_mib else "exceeds_vram_estimate", required_mib


def _switch_reason(requested: str, selected: str, auto_mode: bool) -> str:
    if auto_mode:
        return "auto_selected_vram_fit_model"
    if requested == selected:
        return "requested_model_fits_full_gpu_vram"
    return "requested_model_not_vram_fit_auto_switched"


def _merge_available_model_inventory(
    available_models: list[Any], inventory: dict[str, dict[str, Any]]
) -> list[str]:
    names: list[str] = []
    for item in available_models or []:
        if isinstance(item, dict):
            name = str(item.get("name") or item.get("model") or "").strip()
            size = _int_or_none(item.get("size_bytes") or item.get("size"))
            if name and size:
                inventory.setdefault(name, {})["size_bytes"] = size
        else:
            name = str(item or "").strip()
        if name:
            names.append(name)
    return list(dict.fromkeys([*names, *inventory.keys()]))


def _api_inventory() -> dict[str, dict[str, Any]]:
    try:
        payload = OllamaSdkClient().list_payload()
    except Exception:
        return {}
    result: dict[str, dict[str, Any]] = {}
    for item in payload.get("models") or []:
        if isinstance(item, dict) and item.get("name"):
            result[str(item["name"])] = {"size_bytes": _int_or_none(item.get("size"))}
    return result


def _cli_inventory() -> dict[str, dict[str, Any]]:
    try:
        completed = subprocess.run(["ollama", "list"], text=True, capture_output=True, timeout=6, check=False)
    except Exception:
        return {}
    result: dict[str, dict[str, Any]] = {}
    for line in (completed.stdout or "").splitlines():
        parts = line.split()
        if len(parts) < 4 or parts[0].lower() == "name":
            continue
        result[parts[0]] = {"size_bytes": _parse_size(parts[2], parts[3])}
    return result


def _model_size_bytes(model: str, inventory: dict[str, dict[str, Any]]) -> int | None:
    value = inventory.get(model, {}).get("size_bytes")
    return int(value) if isinstance(value, int) and value > 0 else None


def _parse_size(value: str, unit: str) -> int | None:
    try:
        amount = float(value.replace(",", "."))
    except ValueError:
        return None
    scale = {"kb": 1024, "mb": 1024**2, "gb": 1024**3, "tb": 1024**4}.get(unit.lower())
    return int(amount * scale) if scale else None


def _first_gpu_total_mib(gpus: list[dict[str, Any]]) -> int | None:
    for item in gpus:
        value = item.get("memory_total_mib")
        if isinstance(value, int) and value > 0:
            return value
    return None


def _int_or_none(value: Any) -> int | None:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None
