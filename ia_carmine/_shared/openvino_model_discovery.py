from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


MODEL_ENV_VARS = (
    "IA_CARMINE_OPENVINO_TOOL_MODEL_DIR",
    "IA_CARMINE_GPU0_COMPANION_MODEL_DIR",
    "SPAZIOTEMPO_NPU_MODEL_DIR",
    "IA_CARMINE_NPU_MODEL_DIR",
)


def model_id_from_dir(model_dir: str) -> str:
    return Path(model_dir).expanduser().name if str(model_dir or "").strip() else ""


def discover_openvino_tool_model_dir(
    repo_root: Path,
    *,
    device: str = "GPU.0",
    explicit_model_dir: str = "",
) -> tuple[str, str]:
    if explicit_model_dir:
        return str(Path(explicit_model_dir).expanduser()), "explicit_cli"
    env_names = _model_env_vars_for_device(device)
    explicit = next((os.environ.get(name, "").strip() for name in env_names if os.environ.get(name, "").strip()), "")
    if explicit:
        return str(Path(explicit).expanduser()), "environment"
    model_name = "Phi-3.5-mini-instruct-int4-cw-ov"
    roots = (
        repo_root / "npu-models",
        repo_root / "models",
        repo_root.parent / "npu-models",
        repo_root.parent / "models",
        repo_root.parent.parent / "npu-models",
        Path.home() / "blender" / "npu-models",
        Path.home() / "ProjectsDir" / "npu-models",
    )
    for root in roots:
        for candidate, source in (
            (root, "local_verified_openvino_model_root"),
            (root / model_name, "local_verified_legacy_model"),
        ):
            if (candidate.expanduser() / "openvino_model.xml").is_file():
                return str(candidate.expanduser()), source
    return "", "missing"


def _model_env_vars_for_device(device: str) -> tuple[str, ...]:
    normalized = str(device or "").upper()
    if normalized == "NPU":
        return (
            "IA_CARMINE_NPU_MODEL_DIR",
            "SPAZIOTEMPO_NPU_MODEL_DIR",
            "IA_CARMINE_OPENVINO_TOOL_MODEL_DIR",
        )
    if normalized == "GPU.0":
        return (
            "IA_CARMINE_GPU0_COMPANION_MODEL_DIR",
            "IA_CARMINE_OPENVINO_TOOL_MODEL_DIR",
        )
    return MODEL_ENV_VARS


def run_openvino_tool_loop_child_payload(payload: dict[str, Any]) -> dict[str, Any]:
    import openvino as ov  # noqa: PLC0415
    import openvino_genai as genai  # noqa: PLC0415

    model_dir = str(payload.get("model_dir") or "")
    device = str(payload.get("device") or "GPU.0")
    dialogue_prompt = str(payload.get("dialogue_prompt") or "")
    tool_prompt = str(payload.get("tool_prompt") or "")
    tools = payload.get("tools") if isinstance(payload.get("tools"), list) else []
    structured_schema = str(payload.get("structured_schema") or "{}")
    force_tool_call = bool(payload.get("force_tool_call"))
    max_new_tokens = int(payload.get("max_new_tokens") or 96)

    core = ov.Core()
    devices = list(core.available_devices)
    if device not in devices:
        return {
            "performed": False,
            "supported": False,
            "classification": "openvino_tool_loop_device_unavailable",
            "devices": devices,
            "errors": [f"{device} not available"],
        }

    history = genai.ChatHistory()
    history.set_tools(tools)
    history.append({"role": "user", "content": tool_prompt})
    if device == "NPU":
        pipe = genai.LLMPipeline(model_dir, device, MAX_PROMPT_LEN=2048, MIN_RESPONSE_LEN=8)
    else:
        pipe = genai.LLMPipeline(model_dir, device)

    tokenizer = pipe.get_tokenizer()
    reflection_text = str(
        pipe.generate(dialogue_prompt, max_new_tokens=max(16, min(160, max_new_tokens)))
    ).strip()
    rendered = tokenizer.apply_chat_template(history, True, tools=tools)
    text = str(pipe.generate(rendered, max_new_tokens=max_new_tokens)).strip()
    parsed: dict[str, Any] = {}
    for parser_cls in (
        getattr(genai, "Llama3JsonToolParser", None),
        getattr(genai, "Llama3PythonicToolParser", None),
    ):
        if parser_cls is None:
            continue
        try:
            parsed = parser_cls().parse({"role": "assistant", "content": text}) or {}
            if parsed:
                break
        except Exception:
            pass

    structured_text = ""
    structured_call: dict[str, Any] = {}
    if not parsed:
        try:
            cfg = genai.GenerationConfig()
            cfg.max_new_tokens = 96
            soc = genai.StructuredOutputConfig()
            soc.json_schema = structured_schema
            cfg.structured_output_config = soc
            prefix = (
                "Return decision=call_tool and choose a broker tool for this task: "
                if force_tool_call
                else "Return one IA-Carmine broker tool decision JSON object for this task: "
            )
            structured_prompt = prefix + tool_prompt[:300]
            structured_text = str(pipe.generate(structured_prompt, generation_config=cfg)).strip()
            structured_call = json.loads(structured_text)
        except Exception as exc:  # noqa: BLE001 - reported to parent as provider evidence.
            structured_call = {"_structured_error": f"{type(exc).__name__}: {exc}"}

    return {
        "performed": True,
        "supported": True,
        "classification": "openvino_genai_tool_loop_executed",
        "devices": devices,
        "provider_heap_delta_text": reflection_text,
        "response_text": text,
        "parsed": parsed,
        "structured_text": structured_text,
        "structured_call": structured_call,
    }
