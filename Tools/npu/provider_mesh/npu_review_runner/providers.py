"""Provider adapters for NPU review."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import ROOT

def create_pipeline(model_dir: Path, device: str, max_prompt_len: int, min_response_len: int):
    import openvino_genai as ov_genai

    pipeline_config = {
        "MAX_PROMPT_LEN": max_prompt_len,
        "MIN_RESPONSE_LEN": min_response_len,
        "CACHE_DIR": str(ROOT / "Tools" / "npu" / ".npucache"),
    }

    return ov_genai.LLMPipeline(str(model_dir), device, **pipeline_config)


def create_ollama_pipeline(args: argparse.Namespace):
    from Tools.npu.provider_mesh._shared.ollama_runtime import OllamaSession

    session_kwargs = {
        "model": args.ollama_model,
        "keep_alive": args.ollama_keep_alive,
        "shutdown_server": not args.keep_ollama_server,
        "unload_model": not args.keep_ollama_model,
    }
    if args.ollama_base_url:
        session_kwargs["base_url"] = args.ollama_base_url

    return OllamaSession(**session_kwargs).start()


def generate_text(pipe, prompt: str, max_new_tokens: int) -> str:
    result = pipe.generate(prompt, max_new_tokens=max_new_tokens)
    return str(result).strip()
