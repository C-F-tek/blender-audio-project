# Final Product Real Patch Apply Smoke

Status: active local product test  
Scope: task Markdown to concrete patch suggestion to applied PR patch.

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
