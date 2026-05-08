# Read-first, reuse-first and small-files rule — 2026-05-07

Status: active repository rule.

## Rule

Before proposing or applying a change, an agent must:

```text
1. read the relevant source file or canonical document
2. inspect the current implementation and nearby helpers
3. check the owner maps and data-flow maps
4. prefer reuse of existing scripts/helpers/docs
5. propose the smallest safe change
6. only then edit documentation or source
```

## Reuse-first policy

Do not create a new script, helper, runbook or validator when an existing owner already covers the responsibility.

Required checks before adding new files:

```text
single-owner-scripts-and-flow-boundaries-2026-05-07.md
script-census-and-validation-flow-2026-05-07.md
code-driven-data-flow-map-2026-05-07.md
nearest package README
source tree search
```

## Small-file policy

Maintained files must remain reviewable.

```text
preferred active runbook <= 400 lines
active Markdown hard threshold <= 500 lines
maintained source/script target <= 400 lines
```

When splitting Markdown, the split folder must preserve the complete file name including `.md`:

```text
path/name.md
path/name.md/part-001.md
path/name.md/part-002.md
```

## Stop condition

Stop and report conflict if the requested change would:

```text
duplicate an existing owner
bypass the launcher, broker, validator or review-PR owner
turn a historical handoff into a current contract
make a large monolithic doc/script instead of a compact map/index
claim code behavior not proven by source, manifest or evidence
```
