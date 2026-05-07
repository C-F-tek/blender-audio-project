# Final Product Real Patch Apply Smoke

Status: active local product test  
Scope: task Markdown to concrete patch suggestion to applied PR patch.

## Product North Star

Current product: read a task Markdown, evaluate this repository, produce concrete
patch suggestions, apply the accepted deterministic suggestion on a dedicated
`CARMINEai/...$Stamp` branch, push it, and open a GitHub PR for human review.

Future product: an agnostic AI tool receives a request and project paths, runs
the tool chain in the middle, and returns the requested output plus reviewable
evidence.

Runtime rule: all wrappers and subprocesses must use the same provider-capable
repo `.venv` Python through `IA_CARMINE_PYTHON`, `PYTHONPATH` and `PATH`, because
GPU0/OpenVINO and NPU visibility depend on that interpreter.

## Objective

Apply one deterministic documentation patch from this task Markdown and publish
it through the dedicated `CARMINEai/...$Stamp` PR flow.

The primary product is the applied Markdown change. Telemetry/evidence only
proves the run.

## Deterministic Patch Suggestion

```patch_suggestion_json
{
  "suggestions": [
    {
      "id": "final_product_real_patch_policy_note",
      "family": "docs",
      "title": "Clarify that the final product is an applied patch PR",
      "operation": "insert_after_once",
      "target_file": "docs/LOCAL_AI_TASKS/patch-suggestion-bundle-final-phase.md",
      "find": "The primary product is the applied code/Markdown patch in the GitHub PR. Patch\nnotes, telemetry, heap data and evidence are control surfaces: they prove why\nthe patch is acceptable or why it fell back, but they are not the product by\nthemselves.\n",
      "content": "\nA final product test is complete only when a task Markdown produces at least one concrete patch suggestion and that suggestion is applied to code or maintained Markdown on the dedicated review PR branch.\n",
      "marker": "A final product test is complete only when a task Markdown produces at least one concrete patch suggestion",
      "validation_commands": [
        "git diff --check",
        "python -m py_compile .\\Tools\\ai\\build_task_patch_suggestion_report.py .\\Tools\\ai\\prepare_review_pr.py"
      ],
      "stop_conditions": [
        "target anchor is missing or appears more than once",
        "current branch is master or main",
        "review branch does not start with CARMINEai/"
      ]
    }
  ]
}
```

## Guardrails

```text
No merge to master.
No force-push.
No automatic patch-spec apply outside this deterministic suggestion.
No output/**, generated code chunks, DB, SQLite or render commit.
```

## Follow-up: Provider Acceptance Gate

The patch sub-chain can pass while the Full0To10 provider acceptance gate still
fails closed. In that state the complete product is not accepted yet.

Current failing gate to resolve before claiming full green:

```text
Full0To10 provider acceptance gate after final GPU0 workload failed with exit code 2
```

Classifications observed:

```text
gpu0_peer_semantic_model_unconfigured
blocked_missing_refined_review_input
```

Resolution tasks:

```text
1. Configure or explicitly classify IA_CARMINE_GPU0_COMPANION_MODEL_DIR so GPU0
   can be semantic companion when a model is available.
2. Produce or intentionally supersede
   output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_review_v3.json
   before the provider acceptance gate.
3. Update the acceptance gate so product-patch success and provider-mesh
   degradation are reported as separate statuses.
4. Keep NPU as non-blocking support; final NPU acceptance checks must be
   verified by GPU0/GPU1 plus deterministic validators, not by NPU itself.
```
