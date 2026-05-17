# Ollama Tool Gateway Usage — 2026-05-12

## Scope

This note documents the local Ollama tool gateway introduced for IA-Carmine.

The gateway lets an Ollama model use controlled memory and file-reading tools without relying on native Claude Code/Ollama tool calling.

## Added script

```text
Tools/ai/ollama_tool_gateway/
```

## Purpose

```text
user task
-> Ollama model
-> JSON tool_request
-> deterministic Python gateway
-> memory/file/context-pack tool result
-> Ollama model
-> final JSON answer
```

The gateway is useful when a model emits raw tool-call JSON instead of executing tools through Claude Code.

## Allowed tools

```text
file_search
file_read
memory_search
memory_remember_operational
build_context_pack
```

## Guardrails

```text
no free shell
no source writes
no Git writes
no patch application
no Blender runtime
no FFmpeg runtime
no reading .env or .claude/settings.local.json
no reading output/** unless --allow-output-read is explicitly passed
no reading DB/SQLite/secret/token/password paths
```

## Basic command

```powershell
python -m Tools.ai ollama_tool_gateway `
  --repo-root . `
  --model qwen3.5:cloud `
  --task "Cerca nel progetto i componenti memoria/tool e riassumi cosa esiste."
```

## From Claude Code

Claude Code can call the gateway as an external command:

```text
Esegui questo comando e usa il risultato come contesto:
python -m Tools.ai ollama_tool_gateway --repo-root . --model qwen3.5:cloud --task "analizza Tools/ai per memoria e file gateway"
```

This avoids depending on Claude Code native tool calling for non-Anthropic or local models.

## Output

The script writes local artifacts under:

```text
output/ollama_tool_gateway/
```

These files are local runtime artifacts and must not be committed.

## Suggested first task

```powershell
python -m Tools.ai ollama_tool_gateway `
  --repo-root . `
  --model qwen3.5:cloud `
  --task "Usa file_search e file_read per controllare Tools/ai/agent_runtime_tool_broker.py e python -m Tools.ai agent_runtime_sqlite_memory. Spiega come usarli per dare memoria dinamica a Ollama."
```

## Validation

```powershell
python -m py_compile .\Tools\ai\ollama_tool_gateway\cli.py -m Tools.ai common
python -m Tools.ai ollama_tool_gateway --help
```

## Notes

The gateway is an MVP. It intentionally starts CLI-first, not web-UI-first. A future UI can wrap the same script or import its functions.
