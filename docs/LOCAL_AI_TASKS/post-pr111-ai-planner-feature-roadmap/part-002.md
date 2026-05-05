<!-- IA-CARMINE-MD-SPLIT: part -->
# post-pr111-ai-planner-feature-roadmap — parte 002 di 002

Sorgente indice: [`../post-pr111-ai-planner-feature-roadmap.md`](../post-pr111-ai-planner-feature-roadmap.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)

## Feature 10 — Bundle quality score

Goal:

```text
score whether a compact evidence bundle is review-ready
```

Inputs:

```text
bundle JSON
included artifacts
report summaries
decision flags
```

Score categories:

```text
provider evidence present when expected
manual review flag present
no forbidden raw artifacts
artifact count within budget
request MD included
procedure MD linked
parse failures explained
next layer explicit
```

Output:

```text
bundle_quality_score
blocking_findings
warnings
recommended_next_action
```

Why it matters:

```text
After PR #109 and PR #111, bundle generation works; next step is making bundle quality measurable.
```

## Recommended PR order

```text
1. feat(ai): harden GPU planner JSON output contract
2. feat(ai): detect GPU context-echo outputs
3. feat(ai): add compact GPU prompt retry lane
4. feat(ai): validate model recommendation schema
5. feat(ai): build provider agreement matrix
6. feat(ai): extract AI improvement impressions
7. feat(ai): add issue/task candidate pack
8. feat(ai): introduce reusable AI pipeline profiles
9. feat(ai): add complete-run manifest
10. feat(ai): score compact evidence bundle quality
```

## Immediate next PR candidate

Start with:

```text
feat(ai): harden GPU planner JSON output contract
```

Minimal scope:

```text
Tools/ai/run_agent_gpu_deep_planning_review.py
Tools/ai/run_agent_gpu_deep_planning_supervised.py
docs/LOCAL_AI_TASKS/gpu-repair-failure-recommendation.md
new or updated evidence bundle
```

Validation focus:

```text
py_compile
unit/smoke for model JSON parse helper
replay against project_complete_20260502-195523_parallel_gpu.json if possible
bundle evidence
```

## Guardrails

```text
no provider setting changes in the first hardening PR
no automatic patch application
no source writes through patch runner
no Blender runtime execution
no raw output/** commit
no full analysis JSON commit
no SQLite/database commit
manual review required
```
