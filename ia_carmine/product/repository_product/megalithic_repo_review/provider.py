from __future__ import annotations

from .common import *  # noqa: F403

def build_ollama_prompt(review: dict[str, Any], *, objective: str) -> str:
    compact = {
        "objective": objective,
        "repo_root": review["repo_root"],
        "resource_lanes": review["resource_lanes"],
        "summary": review["summary"],
        "reports": review["validation_reports"],
        "doc_code_consistency": review["doc_code_consistency"],
        "doc_doc_consistency": review["doc_doc_consistency"],
        "code_code_consistency": review["code_code_consistency"],
        "raw_artifacts_sample": review["raw_artifacts"][:80],
        "sqlite_memory": review["sqlite_memory"],
        "deterministic_findings": review["deterministic_findings"],
        "provider_function_inventory": review["provider_function_inventory"],
        "guardrails": review["guardrails"],
    }
    return (
        "You are an IA-Carmine all-resources repository reviewer. Review doc/code, doc/doc, code/code, RAW artifacts, SQLite memory metadata, and provider tool inventories.\nReturn JSON only with keys: verdict, mismatches, patch_proposals, doc_review, code_review, stop_conditions.\nDo not propose destructive operations. Do not propose Blender runtime execution. Do not commit output or SQLite DB files.\nDo not promote NPU/OpenVINO to primary advisory. Do not apply patches. Patch proposals must be manual-review-only and small.\n\nInput JSON:\n"
        + json.dumps(compact, indent=2, ensure_ascii=False)
    )

def maybe_run_ollama(
    repo_root: Path, prompt: str, *, model: str | None, max_new_tokens: int
) -> dict[str, Any]:
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from ia_carmine.providers.ollama.session import OllamaSession

    try:
        with OllamaSession(model=model, shutdown_server=False, unload_model=True) as session:
            text = session.generate(prompt, max_new_tokens=max_new_tokens, temperature=0.1)
        parsed: Any = None
        try:
            from ia_carmine._shared.model_json import parse_model_json_object

            parsed = parse_model_json_object(text)
        except Exception:
            parsed = None
        return {
            "used": True,
            "provider": "ollama",
            "compute_lane": "gpu_cuda",
            "model": model,
            "response_text": text,
            "response_json": parsed,
            "error": "",
        }
    except Exception as exc:
        return {
            "used": False,
            "provider": "ollama",
            "compute_lane": "gpu_cuda",
            "model": model,
            "response_text": "",
            "response_json": None,
            "error": f"{type(exc).__name__}: {exc}",
        }
