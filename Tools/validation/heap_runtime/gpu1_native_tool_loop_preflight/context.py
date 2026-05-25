"""Startup universe context for the GPU1 native tool-loop preflight."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from ia_carmine._shared.file_backed_transport import artifact_ref, write_text_artifact
from ia_carmine._shared.provider_tool_loop import ollama_tool_call_tool_names


DEFAULT_MEMORY_QUERY = (
    "run-unica GPU1 native tool loop FINAL_PRODUCT pointer heap context closure "
    "runtime memory tool catalog"
)


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}


def repo_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def startup_context(args: argparse.Namespace, repo_root: Path, work_dir: Path, stamp: str) -> dict[str, Any]:
    manifest_path: Path | None = None
    if args.startup_manifest:
        manifest_path = repo_path(repo_root, args.startup_manifest)
    elif not args.refresh_startup_context:
        manifest_path = _find_latest_startup_manifest(repo_root)
    if manifest_path is None or not manifest_path.exists() or args.refresh_startup_context:
        manifest_path = _run_startup_reload(args, repo_root, work_dir, stamp)
    manifest = read_json(manifest_path) if manifest_path and manifest_path.exists() else {}
    manifest = manifest if isinstance(manifest, dict) else {}
    refs = {
        "startup_manifest_ref": artifact_ref(
            manifest_path,
            repo_root,
            kind="heap_context_memory_reload_manifest",
            producer="gpu1_native_tool_loop_preflight",
        )
        if manifest_path and manifest_path.exists()
        else {},
        "gpu1_dynamic_context_pack_ref": _artifact_for_manifest(
            repo_root, manifest, "gpu1_dynamic_context_pack_json"
        ),
        "rag_context_pack_ref": _artifact_for_manifest(repo_root, manifest, "rag_context_pack_json"),
        "ai_context_pack_ref": _artifact_for_manifest(repo_root, manifest, "ai_context_pack_json"),
        "tool_catalog_ref": _artifact_for_manifest(repo_root, manifest, "tool_catalog_json"),
        "operational_memory_search_ref": _artifact_for_manifest(
            repo_root, manifest, "operational_memory_search_json"
        ),
        "startup_repo_scan_index_ref": _artifact_for_manifest(
            repo_root, manifest, "startup_repo_scan_index_json"
        ),
    }
    return {
        "manifest": manifest,
        "manifest_path": manifest_path,
        "refs": refs,
        "context_source": "heap_context_memory_reload_manifest" if manifest else "missing_startup_context",
    }


def build_preflight_prompt(
    startup: dict[str, Any],
    operator_prompt: str = "",
    max_subturns: int = 5,
    model: str = "",
    operator_prompt_ref: dict[str, Any] | None = None,
) -> str:
    task = operator_prompt.strip() or (
        "Testa l'ambiente isolato GPU1 usando memoria, context pack, RAG e tool. "
        "Descrivi cosa hai scoperto e quali tool hai usato."
    )
    refs = startup.get("refs") if isinstance(startup.get("refs"), dict) else {}
    refs_json = json.dumps(refs, indent=2, ensure_ascii=False)
    task_block = _operator_task_block(task, model, operator_prompt_ref or {})
    return f"""IA-Carmine GPU1_NATIVE_TOOL_CHAT_LOOP live preflight.

You are GPU1, the leader. Keep the full prompt/chat as the center of work.
The tool is not an external report: after the runtime injects a role=tool message,
you must use it in the next GPU1 subturn.

Catalogo operativo broker disponibile via API-native tool calls:
{_tool_catalog_prompt_block()}

Regole:
- Non ricevi una lista statica di file da leggere.
- Questo smoke testa l'ambiente isolato GPU1 sopra l'universo runtime file-backed gia' stratificato.
- Il runtime universe vive nei refs sotto: manifest, dynamic GPU1 pack, RAG, AI context pack,
  memoria operativa, tool catalog e repo scan.
- Puoi scegliere tu quale tool nativo usare; per passare lo smoke devi usare almeno un tool reale.
- Path verificato non equivale a contenuto letto.
- Per leggere contenuto reale usa runtime_file_window solo dopo avere scoperto/deciso cosa leggere.
- Tool results rientrano come role=tool nella stessa chat; devi usarli nel subturn successivo.
- Non fare sintesi da memoria interna: lavora sui tool result reiniettati.

Runtime universe refs file-backed:
```json
{refs_json}
```

{_tool_protocol_prompt(refs, model)}

Context source: {startup.get("context_source") or ""}

{task_block}

Subturn 0 instruction: choose one tool natively through the API tools channel.
Do not answer in prose. Do not write JSON in Markdown. Do not fake a tool result.
Use the tool that best inspects the live app environment and the refs above.

After each tool result: decide whether you need another native tool call or have enough evidence.
You may call additional broker tools, up to {max_subturns} GPU1 subturns.
If you call a tool, wait for the injected role=tool result before continuing.
When you stop calling tools, produce the final delta and cite every consumed broker request_id in CONSUMED_EVIDENCE.

Required final format after enough tool evidence:
FINAL_PRODUCT_KIND: text
FINAL_PRODUCT_ACTION: append
CURRENT_POINTER:
- previous_block_id=<last_consumed_request_id_or_subturn>
- refines_block_id=
- resume_from_block_id=<current_gpu1_subturn>
CONSUMED_EVIDENCE:
- <all broker request_id values you used>
NEXT_RUNTIME_INTENT:
- close_gpu1_tool_loop_after_environment_inspection
FINAL_PRODUCT_DELTA:
Write the actual operator-facing response here, grounded in the consumed tool results.
"""


def _operator_task_block(task: str, model: str, operator_prompt_ref: dict[str, Any]) -> str:
    if "qwen3-coder" in (model or "").lower() and operator_prompt_ref:
        return (
            "PROMPT OPERATORE ORIGINALE FILE-BACKED, DA RISPETTARE SENZA RIDURLO:\n"
            "```json\n"
            + json.dumps(operator_prompt_ref, indent=2, ensure_ascii=False)
            + "\n```\n"
            "Per leggerlo usa runtime_file_window sul path del ref. Non e' tagliato: e' accessibile come artifact."
        )
    return (
        "PROMPT OPERATORE ORIGINALE, DA RISPETTARE SENZA RIDURLO:\n"
        "```text\n"
        f"{task}\n"
        "```"
    )


def _tool_protocol_prompt(refs: dict[str, Any], model: str) -> str:
    preferred = _preferred_initial_tool_args(refs)
    preferred_path = str(preferred.get("arguments", {}).get("path") or "")
    if "qwen3-coder" in (model or "").lower():
        return (
            "Ollama native tools protocol for this qwen3-coder run:\n"
            "- Use the API tools channel only; do not print tool JSON in text.\n"
            "- The runtime will receive message.tool_calls[] from Ollama, execute the broker tool, "
            "then append role=tool/tool_name/content to this same chat.\n"
            "- After a role=tool result, either call another tool through message.tool_calls[] or "
            "produce FINAL_PRODUCT_DELTA in assistant content.\n"
            f"- If useful, use runtime_file_window on this artifact path through the API tool channel: {preferred_path}"
        )
    return (
        "Qwen2.5-Coder/Ollama tool-call shape:\n"
        "- Valid: API message.tool_calls[] oppure template tool call esatto:\n"
        "  <tool_call>{\"name\":\"runtime_file_window\",\"arguments\":{\"path\":\"<artifact path>\",\"offset\":0,\"limit\":16000}}</tool_call>\n"
        "- Not valid: fenced ```json blocks, placeholder paths, prose that mentions a tool.\n"
        "- The runtime will inject tool results back through Ollama's tool-response channel in the same chat history.\n"
        "- If unsure, start with one concrete runtime universe artifact:\n"
        f"{_preferred_initial_tool_call(refs)}"
    )


def _preferred_initial_tool_args(refs: dict[str, Any]) -> dict[str, Any]:
    for key in (
        "gpu1_dynamic_context_pack_ref",
        "startup_manifest_ref",
        "rag_context_pack_ref",
        "ai_context_pack_ref",
        "startup_repo_scan_index_ref",
    ):
        ref = refs.get(key) if isinstance(refs.get(key), dict) else {}
        path = str(ref.get("path") or "").strip()
        if path:
            return {
                "name": "runtime_file_window",
                "arguments": {"path": path, "offset": 0, "limit": 16000},
            }
    return {"name": "build_agent_agnostic_tool_inventory", "arguments": {}}


def _preferred_initial_tool_call(refs: dict[str, Any]) -> str:
    payload = _preferred_initial_tool_args(refs)
    return f"  <tool_call>{json.dumps(payload, ensure_ascii=False)}</tool_call>"


def native_tool_required_retry_message(
    response_text: str,
    subturn: int,
    startup: dict[str, Any],
    model: str = "",
) -> dict[str, Any]:
    requested = _tool_name_from_text(response_text)
    requested_line = f"Requested unsupported/non-native tool text: {requested}\n" if requested else ""
    if "qwen3-coder" in (model or "").lower():
        guidance = (
            "Use Ollama message.tool_calls[] through the API tools channel only. "
            "Do not print <tool_call>, fenced JSON, Markdown, or placeholder paths. "
            "The runtime will execute the tool and append role=tool/tool_name/content."
        )
    else:
        guidance = (
            "Per qwen2.5-coder/Ollama, se il tool non appare in message.tool_calls[], usa il template nativo esatto:\n"
            "<tool_call>{\"name\":\"runtime_file_window\",\"arguments\":{\"path\":\"<artifact path>\",\"offset\":0,\"limit\":16000}}</tool_call>\n"
            "Non usare fenced ```json blocks. Non usare placeholder /path/to/..."
        )
    return {
        "role": "user",
        "content": (
            "GPU1_NATIVE_TOOL_CALL_REQUIRED_RETRY.\n"
            f"{requested_line}"
            "Il subturn precedente non ha prodotto una call eseguibile in message.tool_calls[].\n"
            "Non esiste un tool build_startup_context: il contesto startup e' gia' disponibile come refs file-backed.\n"
            "Ora devi scegliere un tool reale dal catalogo API e chiamarlo nativamente.\n"
            f"{guidance}\n"
            f"Path concreto consigliato dal runtime universe:\n{_concrete_runtime_file_window_call(startup, model)}\n"
            f"Subturn retry index: {subturn + 1}\n"
        ),
    }


def tool_loop_soft_stop_message(
    *,
    subturn: int,
    max_subturns: int,
    consumed_ids: list[str],
    failed_ids: list[str] | None = None,
    model: str = "",
) -> dict[str, Any]:
    ids = [item for item in consumed_ids if item]
    failed = [item for item in (failed_ids or []) if item]
    joined = "\n".join(f"- {item}" for item in ids) or "- <no broker result ids>"
    failed_joined = "\n".join(f"- {item}" for item in failed) or "- none"
    qwen3_note = (
        "For qwen3-coder this finalization subturn intentionally has no tools in the API payload. "
        "Do not try to print tool JSON: there is no tool channel in this subturn.\n"
        if "qwen3-coder" in (model or "").lower()
        else ""
    )
    return {
        "role": "user",
        "content": (
            "GPU1_TOOL_LOOP_FINALIZE_WITHOUT_MORE_TOOLS.\n"
            f"No more native tool calls are available in this preflight finalization subturn: {subturn}/{max_subturns}.\n"
            "This is not context truncation. The runtime universe, prompt refs, chat history, "
            "and every role=tool result remain above in this same conversation.\n"
            "Compose the assistant answer from the consumed tool results already present in history.\n"
            "Do not answer with a meta-status such as 'tool execution completed' or "
            "'review the reports'. Do not mention soft stop, subturn budget, or tool loop "
            "as the operator product. If the consumed evidence is enough, answer the operator task; "
            "if it is not enough, write a concrete diagnostic answer and the runtime will classify "
            "it as non-product rather than accepting it as FINAL_PRODUCT.\n"
            f"{qwen3_note}"
            "You are still GPU1 leader. The runtime will not synthesize for you.\n"
            "Produce assistant content only, with a non-empty FINAL_PRODUCT_DELTA.\n"
            "Cite every broker request_id you used in CONSUMED_EVIDENCE:\n"
            f"{joined}\n"
            "Failed tool results are diagnostic only. Do not put failed ids in CONSUMED_EVIDENCE; "
            "mention them only under DIAGNOSTIC_TOOL_FAILURES if relevant:\n"
            f"{failed_joined}\n"
            "Required final format:\n"
            "FINAL_PRODUCT_KIND: text\n"
            "FINAL_PRODUCT_ACTION: append\n"
            "CURRENT_POINTER:\n"
            f"- previous_block_id={ids[-1] if ids else f'subturn{subturn}'}\n"
            "- refines_block_id=\n"
            f"- resume_from_block_id=subturn{subturn + 1}\n"
            "CONSUMED_EVIDENCE:\n"
            f"{joined}\n"
            "NEXT_RUNTIME_INTENT:\n"
            "- close_gpu1_tool_loop_after_operator_delta\n"
            "DIAGNOSTIC_TOOL_FAILURES:\n"
            f"{failed_joined}\n"
            "FINAL_PRODUCT_DELTA:\n"
            "Write the actual operator-facing answer now. It must quote concrete facts from "
            "passed tool results and explain what they mean for the operator's run-unica/tool-loop task.\n"
        ),
    }


def empty_delta_repair_message(
    response_text: str,
    subturn: int,
    consumed_ids: list[str],
) -> dict[str, Any]:
    ids = [item for item in consumed_ids if item]
    joined = "\n".join(f"- {item}" for item in ids) or "- <request_id consumed>"
    return {
        "role": "user",
        "content": (
            "GPU1_EMPTY_FINAL_PRODUCT_DELTA_REPAIR.\n"
            "Il subturn precedente ha provato a chiudere, ma FINAL_PRODUCT_DELTA era vuoto.\n"
            "Questo non e' accettabile: se hai abbastanza evidence, rispondi ora con un "
            "FINAL_PRODUCT_DELTA non vuoto; se manca evidence, chiama un tool concreto del catalogo GPU1.\n"
            "Non ripetere runtime_file_window a meno che ti serva nuova evidence reale.\n"
            "Se chiudi, cita gli evidence id gia' consumati:\n"
            f"{joined}\n"
            "Formato se non chiami altri tool:\n"
            "FINAL_PRODUCT_KIND: text\n"
            "FINAL_PRODUCT_ACTION: append\n"
            "CURRENT_POINTER:\n"
            f"- previous_block_id={ids[-1] if ids else f'subturn{subturn}'}\n"
            "- refines_block_id=\n"
            f"- resume_from_block_id=subturn{subturn + 1}\n"
            "CONSUMED_EVIDENCE:\n"
            f"{joined}\n"
            "NEXT_RUNTIME_INTENT:\n"
            "- close_gpu1_tool_loop_after_non_empty_delta\n"
            "FINAL_PRODUCT_DELTA:\n"
            "Scrivi qui il prodotto operatore concreto, non un placeholder e non una stringa vuota.\n"
        ),
    }


def _concrete_runtime_file_window_call(startup: dict[str, Any], model: str = "") -> str:
    refs = startup.get("refs") if isinstance(startup.get("refs"), dict) else {}
    for key in (
        "gpu1_dynamic_context_pack_ref",
        "startup_manifest_ref",
        "rag_context_pack_ref",
        "ai_context_pack_ref",
        "startup_repo_scan_index_ref",
    ):
        ref = refs.get(key) if isinstance(refs.get(key), dict) else {}
        path = str(ref.get("path") or "").strip()
        if path:
            payload = {"name": "runtime_file_window", "arguments": {"path": path, "offset": 0, "limit": 16000}}
            if "qwen3-coder" in (model or "").lower():
                return path
            return (
                "<tool_call>"
                + json.dumps(payload, ensure_ascii=False)
                + "</tool_call>"
            )
    if "qwen3-coder" in (model or "").lower():
        return "{\"name\":\"build_agent_agnostic_tool_inventory\",\"arguments\":{}}"
    return "<tool_call>{\"name\":\"build_agent_agnostic_tool_inventory\",\"arguments\":{}}</tool_call>"


def _tool_name_from_text(text: str) -> str:
    candidate = (text or "").strip()
    if candidate.startswith("```"):
        lines = candidate.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        candidate = "\n".join(lines).strip()
    try:
        payload = json.loads(candidate)
    except Exception:
        return ""
    if not isinstance(payload, dict):
        return ""
    function = payload.get("function") if isinstance(payload.get("function"), dict) else {}
    return str(payload.get("tool") or payload.get("tool_name") or payload.get("name") or function.get("name") or "")


def _artifact_for_manifest(repo_root: Path, manifest: dict[str, Any], key: str) -> dict[str, Any]:
    artifacts = manifest.get("artifacts") if isinstance(manifest.get("artifacts"), dict) else {}
    value = str(artifacts.get(key) or "").strip()
    if not value:
        return {}
    return artifact_ref(repo_path(repo_root, value), repo_root, kind=key, producer="heap_context_memory_reload")


def _find_latest_startup_manifest(repo_root: Path) -> Path | None:
    candidates = sorted(
        (repo_root / "output").glob("**/heap_context_memory_reload_manifest.json"),
        key=lambda item: item.stat().st_mtime if item.exists() else 0,
        reverse=True,
    )
    for path in candidates:
        data = read_json(path)
        if isinstance(data, dict) and data.get("kind") == "heap_context_memory_reload_manifest":
            return path
    return None


def _run_startup_reload(args: argparse.Namespace, repo_root: Path, work_dir: Path, stamp: str) -> Path:
    startup_dir = repo_path(repo_root, args.startup_output_dir or work_dir / "startup_context_memory_reload")
    request_ref = write_text_artifact(
        repo_root,
        startup_dir / "payload",
        name="gpu1_isolated_preflight_request",
        text=args.operator_prompt or DEFAULT_MEMORY_QUERY,
        kind="gpu1_isolated_preflight_startup_request",
        producer="gpu1_native_tool_loop_preflight",
        suffix=".md",
    )
    command = [
        sys.executable,
        "-m",
        "ia_carmine.cli",
        "heap_context_memory_reload",
        "--repo-root",
        str(repo_root),
        "--request-file",
        str(request_ref["path"]),
        "--output-dir",
        str(startup_dir),
        "--stamp",
        f"{stamp}-gpu1-preflight-startup",
        "--startup-provider-input-workers",
        "4",
        "--startup-required-context-profile",
        "project_self_improvement",
        "--ai-context-pack-profile",
        "core_ai_backend",
        "--startup-operational-memory-query",
        args.memory_query or DEFAULT_MEMORY_QUERY,
        "--startup-operational-memory-limit",
        "8",
        "--rag-db",
        "output/ai_runtime_memory/rag/rag.sqlite",
        "--rag-index-policy",
        "auto",
        "--rag-top-k",
        "12",
        "--rag-char-budget",
        "24000",
        "--rag-embedding-endpoint",
        args.base_url,
        "--rag-embedding-model",
        args.rag_embedding_model,
    ]
    subprocess.run(command, cwd=repo_root, check=False, text=True, capture_output=True)
    return startup_dir / "heap_context_memory_reload_manifest.json"


def _tool_catalog_prompt_block() -> str:
    purpose = {
        "repo_toolchain_probe": "verifica disponibilita' reale di rg/fd/jq/PowerShell/dotnet/msbuild/ninja/code",
        "repo_toolchain_command": "esegue solo comandi toolchain allowlistati: dotnet_info/build/test, msbuild_version, ninja_version/build, code_version",
        "repo_search_rg": "cerca testo nel repository con ripgrep; usa query/path/glob",
        "repo_search_git_grep": "cerca testo tracciato nel repository con git grep; usa query/path",
        "repo_find_fd": "trova file nel repository con fd; usa pattern/path/extension",
        "repo_json_query_jq": "interroga JSON reali del repo con jq; usa path e filter/query",
        "repo_powershell_readonly": "usa solo Get-ChildItem o Select-String read-only; niente shell arbitraria",
        "runtime_sqlite_memory": "legge/search/status della memoria SQLite operativa o persistente dell'app",
        "build_agent_memory_inventory": "inventario read-only della memoria agente persistente",
        "build_agent_transient_request_context": "costruisce contesto request-scoped da memoria/report/file gia' prodotti",
        "build_agent_agnostic_tool_inventory": "inventario dei tool IA-Carmine disponibili",
        "ai_context_pack": "costruisce context pack corrente da profili stabili",
        "rag_context_pack": "costruisce pack RAG se pubblicato dal broker/registry",
        "select_semantic_code_chunks": "seleziona chunk codice semanticamente rilevanti",
        "semantic_evidence_chunks": "produce chunk/evidence semantici file-backed",
        "runtime_file_refs": "risolve/verifica ref da text_file/path di artifact o target_file di sorgente; path e' alias accettato",
        "runtime_file_window": "legge una finestra reale di contenuto file/artifact; args path, offset, limit",
        "build_python_line_count_csv": "inventario concreto delle linee Python sorgente",
    }
    lines = [
        f"- {name}: {purpose.get(name, 'broker tool IA-Carmine concreto allowlisted')}"
        for name in ollama_tool_call_tool_names(gpu1_concrete_only=True)
    ]
    lines.append(
        "- Strumenti non esposti a GPU1 in questo loop: generic_write, debug lab, matrix, "
        "virtual env, patch synthesis e code-product analyzer; sono fasi deterministic/late-stage, "
        "non strumenti di esplorazione iniziale."
    )
    lines.append(
        "- Non esiste shell libera: PowerShell e ricerca sono esposti solo tramite wrapper read-only "
        "registrati (`repo_powershell_readonly`, `repo_search_rg`, `repo_search_git_grep`, "
        "`repo_find_fd`, `repo_json_query_jq`)."
    )
    return "\n".join(lines)
