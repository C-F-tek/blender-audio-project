# Complex Provider Toolbox Request v1

## Purpose

This is the first real Markdown task input for a complete IA-Carmine local AI request.

The task must prove that a complex engineering request can use both provider execution and the runtime toolbox in the same controlled cycle.

## Required reading

Read these files before planning:

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/complex-provider-toolbox-request-v1.md
docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_tool_usage_bundle_complex_ai_tool_usage_20260503-092256.json
docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_backed_bundle_complex_ai_provider_backed_20260503-092828.json
```

## Objective

Perform a provider-backed engineering review of the current IA-Carmine repository state.

The review must use:

```text
GPU/Ollama provider execution
NPU/OpenVINO provider execution
orchestrator-controlled runtime toolbox broker
memory and tool inventory reports
code and documentation coherence reports
duplication/refactor audit reports
compact evidence bundle output
```

## Engineering questions

Answer these questions from evidence, not from memory alone:

1. Did GPU/Ollama execute as provider?
2. Did NPU/OpenVINO execute as provider?
3. Did NPU decode produce usable text?
4. Did the orchestrator enable the runtime toolbox broker?
5. Did the broker execute at least one allowlisted tool?
6. Did any tool request fail or get blocked?
7. Did the provider lanes see toolbox context or broker reports?
8. Was persistent memory written?
9. Was operational memory only used as scratch/status evidence?
10. Are docs and code still coherent after PR #146 through #150?
11. Which duplicated helper families remain?
12. Which method/function restructuring candidates are ready for manual patch planning?
13. Which next PR has the best value-to-risk ratio?

## Required toolbox evidence

The run should produce evidence for at least these tool categories:

```text
agent/tool inventory
memory status or memory inventory
Python line-count inventory
Python syntax validation
validation report contract check
code/static interpreter report
refactor duplication audit
```

The broker must remain the only tool executor.

## Required provider evidence

The run must include provider-backed evidence for:

```text
resource lanes with provider_execution_performed=True
GPU/Ollama report with provider_execution_performed=True
NPU decode smoke with provider_execution_performed=True
NPU auditor records with provider_execution_performed=True where audits run
```

## Success criteria

The task is successful only if the final reports show:

```text
provider_execution_performed=True
runtime_tool_broker_enabled=True
runtime_tool_execution_count > 0
runtime_tool_failed_count=0
runtime_tool_blocked_count=0
npu_audit_success_count > 0
patch_application_performed=False
persistent_memory_write_performed=False
```

Stronger success if one of these is also true:

```text
npu_tool_context_seen_count > 0
npu_runtime_tool_execution_count > 0
```

## Guardrails

```text
Do not apply patches.
Do not run Blender.
Do not commit output/**.
Do not commit *.db or *.sqlite.
Do not write persistent memory.
Do not expose a free shell to providers.
Do not treat NPU as primary advisor unless a future quality gate explicitly allows it.
```

## Expected final answer from local AI

The local AI should produce a concise engineering report with:

```text
provider_execution_summary
toolbox_usage_summary
memory_usage_summary
documentation_code_coherence_summary
duplication_refactor_summary
ready_for_patch_plan_candidates
needs_more_context_candidates
advisory_only_findings
next_recommended_pr
bundle_manifest
```

## Evidence bundle policy

Build a compact bundle under:

```text
docs/LOCAL_VALIDATION_EVIDENCE/
```

Include only compact bundle files in Git.

Do not commit raw runtime reports under `output/**`.
