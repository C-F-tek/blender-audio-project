#!/usr/bin/env python3
"""Mocked smoke for IA-Carmine Ollama SDK adapter and GPU0 Ollama contract."""

from __future__ import annotations

import argparse
import inspect
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT_FOR_IMPORT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT_FOR_IMPORT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORT))


class FakeClient:
    calls: list[dict[str, Any]] = []

    def __init__(self, host: str) -> None:
        self.host = host

    def list(self) -> dict[str, Any]:
        return {"models": [{"model": "fake-ollama:latest"}]}

    def ps(self) -> dict[str, Any]:
        return {"models": [{"model": "fake-ollama:latest", "processor": "100% GPU"}]}

    def generate(self, **kwargs: Any) -> dict[str, Any] | list[dict[str, Any]]:
        self.calls.append({"method": "generate", "kwargs": kwargs})
        if kwargs.get("stream"):
            return [
                {"response": "hello", "done": False},
                {"response": " world", "done": True, "eval_count": 80},
            ]
        return {
            "response": "hello world from sdk",
            "done": True,
            "eval_count": 80,
            "eval_duration": 2_000_000_000,
            "prompt_eval_count": 12,
        }

    def chat(self, **kwargs: Any) -> dict[str, Any] | list[dict[str, Any]]:
        self.calls.append({"method": "chat", "kwargs": kwargs})
        response = {
            "message": {
                "content": "tool selected",
                "tool_calls": [
                    {
                        "function": {
                            "name": "run_heap_code_execution_matrix",
                            "arguments": {"target_file": ["ia_carmine/dispatch.py"]},
                        }
                    }
                ],
            },
            "done": True,
            "eval_count": 96,
        }
        if kwargs.get("stream"):
            return [response]
        return response


def fake_factory(host: str) -> FakeClient:
    return FakeClient(host)


def build_report(repo_root: Path) -> dict[str, Any]:
    from ia_carmine._shared.provider_work_verification import provider_work_status
    from ia_carmine.providers.ollama.sdk_client import OllamaSdkClient
    from ia_carmine.providers.ollama.session import OllamaSession
    from ia_carmine.providers.ollama.tool_calls import normalize_ollama_tool_calls

    errors: list[str] = []
    FakeClient.calls = []
    session = OllamaSession(
        model="fake-ollama:latest",
        shutdown_server=False,
        unload_model=True,
        gpu_layers="all",
        num_thread=4,
        num_ctx=8192,
        client_factory=fake_factory,
    ).start()
    generated = session.generate("prompt", max_new_tokens=123, temperature=0.25)
    chat = session.chat(
        [{"role": "user", "content": "pick a tool"}],
        tools=[{"type": "function", "function": {"name": "run_heap_code_execution_matrix"}}],
        max_new_tokens=77,
        temperature=0.0,
    )
    session.close()
    calls = normalize_ollama_tool_calls(chat)
    client = OllamaSdkClient(client_factory=fake_factory)
    ps = client.ps()

    generate_call = next(item for item in FakeClient.calls if item["method"] == "generate")
    chat_call = next(item for item in FakeClient.calls if item["method"] == "chat")
    options = generate_call["kwargs"].get("options", {})
    if generated != "hello world from sdk":
        errors.append("OllamaSession.generate did not return SDK text")
    if options.get("num_ctx") != 8192 or options.get("num_thread") != 4:
        errors.append("generate options did not propagate num_ctx/num_thread")
    if options.get("temperature") != 0.25 or options.get("num_predict") != 123:
        errors.append("generate options did not propagate temperature/num_predict")
    if options.get("num_gpu") != -1:
        errors.append("generate options did not propagate gpu_layers=all as num_gpu=-1")
    if not chat_call["kwargs"].get("tools"):
        errors.append("chat tools were not propagated to ollama-python")
    if not calls or calls[0].get("tool") != "run_heap_code_execution_matrix":
        errors.append("ollama-python tool_calls were not normalized")
    if not ps.get("models"):
        errors.append("OllamaSdkClient.ps did not return process data")
    if OllamaSession.__module__ != "ia_carmine.providers.ollama.session":
        errors.append("OllamaSession is not exported from canonical ia_carmine.providers.ollama")

    gpu0_status = provider_work_status(
        lane="gpu0_peer",
        report={
            "provider_backend": "ollama",
            "provider_compute_device": "ollama/gpu0-vulkan",
            "provider_device_verified": True,
            "ollama_residency_verified": True,
            "ollama_compute_verified": True,
            "selected_model": "fake-ollama:latest",
            "eval_count": 80,
            "done": True,
            "response_text": "GPU0 reviewed concrete target refs and requested broker evidence.",
        },
    )
    if not gpu0_status.get("provider_work_verified"):
        errors.append(f"GPU0 Ollama status rejected: {gpu0_status}")

    canonical_sources = [
        repo_root / "ia_carmine" / "providers" / "ollama" / "sdk_client.py",
        repo_root / "ia_carmine" / "providers" / "ollama" / "session.py",
        repo_root / "ia_carmine" / "providers" / "provider_mesh" / "ollama_tool_gateway" / "client.py",
    ]
    for source in canonical_sources:
        text = source.read_text(encoding="utf-8")
        if "urllib.request" in text:
            errors.append(f"canonical Ollama runtime still uses urllib.request: {source}")

    return {
        "schema_version": 1,
        "kind": "ollama_sdk_adapter_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "provider_execution_performed": False,
        "ollama_request_performed": False,
        "gpu0_ollama_contract": gpu0_status,
        "tool_call_count": len(calls),
        "session_signature": str(inspect.signature(OllamaSession.generate)),
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Ollama SDK Adapter Smoke",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Tool call count: `{report.get('tool_call_count')}`",
        f"- Provider execution performed: `{report.get('provider_execution_performed')}`",
        f"- Ollama request performed: `{report.get('ollama_request_performed')}`",
    ]
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report["errors"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/ollama_sdk_adapter_smoke.json")
    parser.add_argument(
        "--markdown-output", default="output/validation/ollama_sdk_adapter_smoke.md"
    )
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root)
    output = Path(args.output)
    markdown = Path(args.markdown_output)
    if not output.is_absolute():
        output = repo_root / output
    if not markdown.is_absolute():
        markdown = repo_root / markdown
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "output": str(output)}, indent=2))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
