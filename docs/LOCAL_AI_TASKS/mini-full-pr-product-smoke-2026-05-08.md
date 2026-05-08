# Mini Full PR Product Smoke

Status: active one-shot smoke task  
Date: 2026-05-08  
Scope: verify the current Full0To10 product path can turn a Markdown task into a review PR with a concrete documentation patch.

## Objective

Run a short, bounded product smoke:

```text
task Markdown input
-> task-scoped patch suggestion report
-> deterministic patch apply on CARMINEai review branch
-> review PR with applied Markdown change
-> telemetry/evidence as supplemental proof
```

## Guardrails

```text
No merge to master.
No force-push.
No rewrite history.
No destructive delete.
No output/** commit.
No indexAI/code_chunks/** commit.
No DB/SQLite/render commit.
No Blender runtime.
No FFmpeg runtime.
```

Obsolete or superseded Markdown may be marked, clarified or routed to a pruning task. Deletion is not part of this smoke.

## Deterministic Patch Suggestion

```patch_suggestion
{
  "suggestions": [
    {
      "id": "mini_full_pr_smoke_obsolete_docs_policy_20260508",
      "family": "docs",
      "title": "Record mini Full0To10 review-PR smoke policy for obsolete Markdown",
      "operation": "append_once",
      "target_file": "docs/LOCAL_AI_TASKS/obsolete-monolithic-docs-review-2026-05-07.md",
      "marker": "mini_full_pr_smoke_obsolete_docs_policy_20260508",
      "content": "\n## Mini Full0To10 PR Smoke Note\n\n`mini_full_pr_smoke_obsolete_docs_policy_20260508`: obsolete or superseded Markdown found during a product smoke can be clarified, marked, or routed to an explicit pruning task. This smoke proves review-PR production and does not authorize destructive deletion by itself.\n",
      "patch_sketch": [
        "Append a compact note to the obsolete/monolithic docs review index.",
        "Keep deletion out of this smoke; retain destructive pruning as an explicit task."
      ],
      "validation_commands": [
        "git diff --check",
        "python -m py_compile .\\Tools\\ai\\apply_patch_suggestion_bundle.py .\\Tools\\ai\\prepare_review_pr.py"
      ],
      "stop_conditions": [
        "Do not delete Markdown files in this smoke.",
        "Do not stage output/**, generated chunks, DBs, SQLite files or renders."
      ]
    }
  ]
}
```
