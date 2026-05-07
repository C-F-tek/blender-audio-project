<!-- IA-CARMINE-MD-SPLIT: index -->
# Local AI Tasks

This document is split to keep Markdown reviewable and compatible with AI context builders.

- Original file: `docs/LOCAL_AI_TASKS/README.md`
- Active Markdown hard threshold: `500` lines
- Preferred active runbook size: `400` lines
- Full index: [`README/README.md`](README/README.md)

## Parts

- [`README/part-001.md`](README/part-001.md)
- [`README/part-002.md`](README/part-002.md)

## Current canonical additions

- [`code-derived-ai-toolchain-map-2026-05-07.md`](code-derived-ai-toolchain-map-2026-05-07.md)
- [`script-census-and-validation-flow-2026-05-07.md`](script-census-and-validation-flow-2026-05-07.md)
- [`single-owner-scripts-and-flow-boundaries-2026-05-07.md`](single-owner-scripts-and-flow-boundaries-2026-05-07.md)
- [`code-driven-data-flow-map-2026-05-07.md`](code-driven-data-flow-map-2026-05-07.md)
- [`md-split-folder-naming-rule-2026-05-07.md`](md-split-folder-naming-rule-2026-05-07.md)
- [`gpu-peer-exchange-operational-principle.md`](gpu-peer-exchange-operational-principle.md)
- [`md-coherence-only-github-pass-2026-05-06.md`](md-coherence-only-github-pass-2026-05-06.md)
- [`patch-suggestion-bundle-final-phase.md`](patch-suggestion-bundle-final-phase.md)

## Operational note

Keep this file as the stable entrypoint so existing references do not break.

For current behavior, prefer code-derived docs over historical handoff docs. The current code-derived map is the first stop when launcher/review-PR/provider behavior is unclear.

For script navigation, run variants, smoke strategy and validation cycles, use `script-census-and-validation-flow-2026-05-07.md`.

For ownership boundaries and scripts that must not be duplicated or bypassed, use `single-owner-scripts-and-flow-boundaries-2026-05-07.md`.

For operational data-flow variants, use `code-driven-data-flow-map-2026-05-07.md`.

For split Markdown, the sibling folder must keep the full file name including `.md`; see `md-split-folder-naming-rule-2026-05-07.md`.
