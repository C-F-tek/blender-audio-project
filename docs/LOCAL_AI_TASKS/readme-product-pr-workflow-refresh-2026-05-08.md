# README product PR workflow refresh

Status: active task input for product-chain validation  
Date: 2026-05-08  
Scope: root README, patch-suggestion product flow, review PR evidence.

## Objective

Refresh the root README so a remote reviewer sees the current product goal:

```text
task Markdown input -> patch suggestion product -> deterministic apply/review branch -> product separation validation -> review PR
```

The change must be small, source-controlled and reviewable. It must not run providers, Blender or FFmpeg, and it must not stage `output/**`.

## Deterministic patch suggestion

```patch_suggestion
{
  "suggestions": [
    {
      "id": "readme_product_pr_workflow_refresh_20260508",
      "family": "docs",
      "title": "Document the current Markdown-to-PR product path in the root README",
      "operation": "insert_after_once",
      "target_file": "README.md",
      "find": "Use those documents for current commands, `-Full0To10`, intensity profiles, provider flags, reset mode, memory controls, patch-spec generation and validation modes.\n",
      "marker": "README_PRODUCT_PR_WORKFLOW_20260508",
      "content": "\n## Current product path: Markdown input to review PR\n\n<!-- README_PRODUCT_PR_WORKFLOW_20260508 -->\n\nThe immediate product is a reviewable branch and GitHub PR derived from a concrete task Markdown file. A valid product run starts from `docs/LOCAL_AI_TASKS/*.md`, extracts patch suggestions, applies only deterministic source/doc operations on an allowed review branch, validates product-vs-telemetry separation, and prepares a PR for human review.\n\nCurrent chain:\n\n```text\ntask Markdown patch_suggestion\n  -> Tools/ai/build_task_patch_suggestion_report.py\n  -> Tools/ai/apply_patch_suggestion_bundle.py\n  -> Tools/validation/check_patch_suggestion_product_separation.py\n  -> Tools/ai/prepare_review_pr.py\n  -> GitHub PR for manual review\n```\n\nThe focused workflow proof is `Tools/validation/run_full0to10_product_pr_chain_smoke.py`: it runs the product chain in a temporary git repository and also traces `Tools/workflow/run_unified_local_ai_refactor.ps1` to confirm the real launcher keeps the same phase order.\n",
      "patch_sketch": [
        "Insert a compact README section after the current local AI entrypoint description."
      ],
      "validation_commands": [
        "python .\\Tools\\validation\\run_full0to10_product_pr_chain_smoke.py --repo-root . --output .\\output\\validation\\full0to10_product_pr_chain_smoke_20260508.json --markdown-output .\\output\\validation\\full0to10_product_pr_chain_smoke_20260508.md",
        "python .\\Tools\\validation\\check_docs_links.py --repo-root . --output .\\output\\validation\\docs_links_coherence_20260508.json --nonfatal-prefix docs/LOCAL_VALIDATION_EVIDENCE",
        "git diff --check"
      ],
      "stop_conditions": [
        "Do not stage output/**.",
        "Do not modify generated chunks, database files, renders, Blender runtime or FFmpeg runtime.",
        "Do not merge to master."
      ]
    }
  ]
}
```
