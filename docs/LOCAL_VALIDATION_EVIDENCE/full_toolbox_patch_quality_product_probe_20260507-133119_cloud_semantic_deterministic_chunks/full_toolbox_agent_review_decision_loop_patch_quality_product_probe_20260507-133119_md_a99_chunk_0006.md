# Evidence Chunk 0006/0024

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.md`
- source_sha256: `a996111fa318d87d97d3b80eb2d1e49442622645214c899236220d62065e9ccb`
- line_start: `727`
- line_end: `826`
- section_kinds: `['markdown_heading_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_md_a99_chunk_0005.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_md_a99_chunk_0007.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: Findings. Preview: ## Findings | Severity | Kind | Source | Line | Target | Recommendation | |---|---|---|---:|---|---| | `high` | `md_mentions_missing_python_path` | `AGENTS.md` | 374 | `run_patch_bundle.py` | Correct the documentation reference or restore the missing target if...

## Context before

- `low`: `48`
- `medium`: `8321`

## Finding kind counts

- `documented_python_script_without_obvious_smoke`: `48`
- `md_cli_arg_not_in_argparse`: `2`
- `md_mentions_missing_markdown_path`: `8319`
- `md_mentions_missing_powershell_path`: `524`
- `md_mentions_missing_python_path`: `3384`
- `md_python_command_script_missing`: `44`


## Chunk content

```md
## Findings

| Severity | Kind | Source | Line | Target | Recommendation |
|---|---|---|---:|---|---|
| `high` | `md_mentions_missing_python_path` | `AGENTS.md` | 374 | `run_patch_bundle.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AGENTS.md` | 375 | `patches/00_check_repo_ready.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AGENTS.md` | 372 | `text
README.md
run_patch_bundle.py
patches/00_check_repo_ready.py
patches/01_*.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 237 | `run_patch_bundle.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_powershell_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 292 | `some_script.ps1` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 302 | `changed.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 323 | `some_tool.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 324 | `some_smoke.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_powershell_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 325 | `some_runner.ps1` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 323 | `Tools/validation/some_smoke.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT.md` | 60 | `text
CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md
AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` | 22 | `agent_memory_schema.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` | 23 | `agent_memory_chunker.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` | 24 | `agent_memory_embeddings.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` | 25 | `agent_memory_search.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` | 26 | `agent_memory_tools.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` | 325 | `agent_memory_tools.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` | 328 | `agent_memory_tools.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` | 334 | `agent_memory_tools.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` | 339 | `agent_memory_tools.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 74 | `Tools/validation/check_runtime_hardware_capability_manifest.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 98 | `Tools/ai/agent_memory_schema.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 99 | `Tools/ai/agent_memory_tools.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 139 | `Tools/ai/simulate_npu_tool_proxy.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 157 | `Tools/ai/run_npu_tool_proxy.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 230 | `check_runtime_hardware_capability_manifest.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 52 | `text
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 73 | `text
Tools/validation/check_runtime_hardware_capability_manifest.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 97 | `text
Tools/ai/agent_memory_schema.py
Tools/ai/agent_memory_tools.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 138 | `text
Tools/ai/simulate_npu_tool_proxy.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 156 | `text
Tools/ai/run_npu_tool_proxy.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 55 | `hardware-memory.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 68 | `02-chunking.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 70 | `04-cli.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 94 | `01-overview.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 95 | `02-contract.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 96 | `03-commands.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 97 | `04-validation.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 98 | `05-next-steps.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 17 | `text
<name>.md/
  README.md
  01-*.md
  02-*.md
  03-*.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 52 | `text
CHATGPT.md/
  README.md
  hardware-memory.md/
    README.md
    01-architecture-summary.md
    02-sqlite-heap-memory-design.md
    03-broker-hardware-delegation-contract.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 64 | `text
02-sqlite-heap-memory-design.md/
  README.md
  01-schema.md
  02-chunking.md
  03-search.md
  04-cli.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 91 | `text
<topic>.md/
  README.md
  01-overview.md
  02-contract.md
  03-commands.md
  04-validation.md
  05-next-steps.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 103 | `text
CHATGPT/<date>-<topic>/
  README.md
  01-*.md
  02-*.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/README.md` | 21 | `text
01-architecture-summary.md
02-sqlite-heap-memory-design.md
03-broker-hardware-delegation-contract.md
04-implementation-plan.md
05-reset-sync-commands.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/DISCOVERY_CONTRACT.md` | 13 | `text
CHATGPT.md
CHATGPT/README.md
CHATGPT/*.md` | Correct the documentation reference or restore the missing target if it is still required. |
```

## Context after

| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/README.md` | 25 | `text
1. AGENTS.md
2. CHATGPT.md
3. docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
4. docs/MAIN_RUNTIME_ARCHITECTURE.md
5. docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
6. docs/AI_PIPELINE_ARCHITECTURE.md
7. docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
8. docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
9. docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
10. docs/LOCAL_AI_TASKS/refactor-reuse-full-run-documentation-coherence-2026-05-05.md
11. docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
