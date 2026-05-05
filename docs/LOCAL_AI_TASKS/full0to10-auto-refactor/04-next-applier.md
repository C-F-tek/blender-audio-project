# Next applier

Il primo applier controllato è ora disponibile.

## Entry point

```text
Tools/ai/apply_full0to10_auto_refactor_patch_specs.py
Tools/workflow/run_full0to10_auto_refactor_apply.ps1
```

## Stato

Supporta solo cleanup sicuri:

- trailing whitespace;
- final newline.

Split Markdown, split codice e contratti hardware restano manual-review.
