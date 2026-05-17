function New-HeapExchangeProcessGateTask {
    param(
        [string]$Root,
        [string]$StampValue
    )

    $TaskDir = Join-Path $Root "output/local_ai_task_inputs"
    New-Item -ItemType Directory -Force -Path $TaskDir | Out-Null

    $TaskPath = Join-Path $TaskDir ("heap-exchange-process-gate-{0}.md" -f $StampValue)

    $TaskContent = @"
# Heap Exchange Process Gate - $StampValue

## Objective

Run the complete IA-Carmine local-AI orchestration as a real process-product gate.

The run must prove that the system can enter the heap/exchange runtime layer, allow the internal runtime lanes to operate dynamically, and exit with observable exchange evidence plus concrete reviewable code/document changes.

This gate runs before implementing or enabling the runtime_debug_lab broker tool.

## Architecture rule

Do not guide the internal heap/exchange route step by step.

The center of the run is dynamic.

Inside the heap/exchange layer, the following runtime lanes may cooperate according to their current contracts and routing logic:

- GPU.0 workload support lane;
- GPU.1 reserved/provider lane when visible;
- NPU diagnostics/probe/decode lane;
- Ollama/provider advisory lane;
- official local AI adapter;
- context pack and agent-state packet;
- generated patch-spec proposal path;
- review-PR bridge.

The task defines the entry contract and exit contract only.

## Entry contract

The run must start from the unified launcher with:

- repository RepoPy only;
- clean working tree;
- Markdown task input;
- JSON/report validation;
- Python/tool inventory;
- semantic chunks;
- context pack;
- agent state;
- official local AI adapter;
- provider workflow;
- Ollama advisory/provider path;
- NPU diagnostic path selected by the launcher;
- OpenVINO GPU.0 workload evidence;
- workload quality routing;
- generated patch specs;
- review-PR bridge;
- unified heap/exchange chain contract;
- product separation;
- prepare_review_pr;
- GitHub draft PR creation.

## Exit contract

The run is successful only if all of these are true:

1. the official adapter completes successfully;
2. the GPU.0 workload report passes;
3. the provider/Ollama path completes successfully;
4. the heap/exchange layer emits observable exchange evidence;
5. generated patch specs are current-stamp and concrete;
6. at least one concrete deterministic operation is available for review;
7. product separation classifies the output as reviewable product, not supplemental telemetry only;
8. prepare_review_pr creates a draft PR with real source/doc changes;
9. the review PR final product contract validates the remote PR product.

Concrete patch operations may use only safe deterministic operations such as:

- replace_once;
- append_once;
- insert_after_once;
- insert_before_once;
- write_file.

Metadata-only patch specs are not acceptable as final product.

Evidence-only reports are not acceptable as final product.

## Preferred output

Prefer one small, safe, code-driven enhancement that improves the orchestration itself.

Good targets:

- heap/exchange event emission;
- exchange evidence manifest;
- generated patch-spec concreteness;
- review PR evidence summary;
- context-pack input/output contract;
- memory/context namespace manifest;
- broker/tool capability map for future runtime_debug_lab integration.

Do not implement or auto-enable runtime_debug_lab in this run.

## Hard failure policy

Do not soft-fail.

Do not continue past a broken gate.

If the run cannot produce exchange evidence or concrete patch specs, stop at the unified chain contract with a structured error.

If the run cannot create a real review PR product, stop before creating a misleading PR.

## Guardrails

Do not:

- merge to master;
- delete files;
- force-push;
- rewrite history;
- deploy;
- modify secrets, permissions, billing or visibility;
- execute Blender runtime;
- execute FFmpeg runtime;
- commit output/**;
- commit indexAI/code_chunks/**;
- commit *.db or *.sqlite;
- activate runtime_debug_lab automatically;
- create a fake patch_suggestion_json block just to pass validation;
- create docs-only filler changes unrelated to the detected process need.

## Validation expected in the generated PR

The generated PR body must include:

- touched files;
- line counts for touched code/scripts;
- PowerShell parser command for touched ps1 files;
- python -m py_compile command for touched Python files;
- relevant smoke validator command;
- git diff --check.

## Operator gate

Create only a draft PR.

Do not merge automatically.

If no concrete product emerges from the heap/exchange run, fail honestly.
"@

    Set-Content -LiteralPath $TaskPath -Value $TaskContent -Encoding UTF8
    return $TaskPath
}
