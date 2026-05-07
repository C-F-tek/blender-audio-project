# Patch Plan Quality Product Gate

- passed: `True`
- quality_gate_passed: `True`
- classification: `ready_for_manual_patch_review`
- non_blocking: `True`
- Patch plans: `20`
- Average plan score: `100.0`
- SQLite FTS5 enabled: `True`
- FTS total hits: `40`

## Fallback path notes

- None.

## Plan scores

- `consistency_001` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- `consistency_002` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- `consistency_003` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- `consistency_004` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- `consistency_005` score=`100` targets=`['CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md']`
- `consistency_006` score=`100` targets=`['docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md']`
- `consistency_007` score=`100` targets=`['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md']`
- `consistency_008` score=`100` targets=`['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- `consistency_009` score=`100` targets=`['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- `consistency_010` score=`100` targets=`['docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md']`
- `consistency_011` score=`100` targets=`['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']`
- `consistency_012` score=`100` targets=`['docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md']`
- `consistency_013` score=`100` targets=`['docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md']`
- `consistency_045` score=`100` targets=`['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- `consistency_046` score=`100` targets=`['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- `consistency_047` score=`100` targets=`['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']`
- `consistency_048` score=`100` targets=`['docs/AUTO_PUSH_GENERATED_ARTIFACTS.md']`
- `consistency_049` score=`100` targets=`['docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md']`
- `consistency_050` score=`100` targets=`['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md']`
- `consistency_051` score=`100` targets=`['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md']`

## Concrete utility

- scores patch plans for target concreteness, rationale, strategy, validation and stop conditions
- indexes request/evidence/telemetry/memory into operational SQLite FTS under output/**
- records query hit counts proving which evidence was reachable
- preserves run completion by writing fallback_path_notes instead of failing on weak patch-note quality
