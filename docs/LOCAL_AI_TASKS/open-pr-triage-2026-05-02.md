# Open PR triage — 2026-05-02

## Scope

GitHub-only triage of pull requests before local workstation validation.

No merges, rebases, deletes, force-pushes or branch rewrites are authorized by this note.

## Current open PR inventory

### PR #109 — `docs(ai): design manual-review code patch plan lane`

```text
state: open
mergeable: true
draft: false
base: master
head: codex/design-code-patch-plan-lane
role: official current work lane
```

Status:

```text
primary active PR
local wiring still pending for Tools/ai/build_github_evidence_bundle.py
fresh compact evidence required before merge
```

Next action:

```text
return home -> sync branch -> compile -> local wiring -> focused validation -> fresh evidence bundle -> push
```

### PR #110 — `refactor(ai): temporary PR109 workspace`

```text
state: open
mergeable: false
draft: true
base: codex/design-code-patch-plan-lane
head: codex/refactor-workspace-109
role: scratch/workspace only
```

Status:

```text
do not merge
use only as historical workspace reference
close after PR #109 has local wiring evidence and all useful changes are mirrored into #109
```

### PR #108 — `docs(ai): document contract drift validation lane`

```text
state: open
mergeable: true
draft: false
base: master
head: codex/doc-contract-drift-crossrefs
role: documentation/validator lane that PR #109 conceptually builds on
```

Status:

```text
clean candidate for local validation
should likely be validated/merged before PR #109 if ordering matters
```

Suggested local checks:

```powershell
python -m Tools.validation check_python_syntax --repo-root . --output .\output\validation\python_syntax_pr108.json
python -m Tools.validation check_docs_links --repo-root . --output .\output\validation\docs_links_pr108.json
# Removed obsolete check_markdown_command_hygiene.py command; the script is not tracked in current master. Use check_docs_links.py plus check_validation_report_contract.py for this gate.
python -m Tools.validation check_validation_report_contract --repo-root . --output .\output\validation\validation_report_contract_pr108.json
git diff --check
```

## Closed as stale/superseded during triage

### PR #2 — `Add safe AI artifact pipeline optimization layer`

```text
state: closed
merged: false
was_draft: true
base: master
head: ai-pipeline-optimization-safe
role: older AI artifact pipeline layer
```

Closure rationale:

```text
stale/non-mergeable draft
likely superseded by later AI pipeline work and PR #109 concepts
recover any still-useful ideas selectively after PR #108/#109 settle
```

No branch deletion, rewrite, merge or destructive repository action was performed.

### PR #1 — `docs: add AI-friendly GitHub developer guide`

```text
state: closed
merged: false
was_draft: false
base: master
head: docs/ai-friendly-github-dev-guide-v2
role: older documentation/CI bootstrap PR
```

Closure rationale:

```text
stale/non-mergeable
some documentation or CI ideas may already be superseded by later docs and validation lanes
recover useful docs/CI concepts selectively into a fresh branch if still relevant
```

No branch deletion, rewrite, merge or destructive repository action was performed.

## Recommended order

```text
1. Finish PR #109 local wiring and focused validation.
2. Validate PR #108 locally; consider merging PR #108 before PR #109 if it is a prerequisite documentation/validator base.
3. Rebase/update PR #109 if PR #108 is merged first.
4. Close PR #110 after confirming no unique useful changes remain.
5. Reassess closed PR #1/#2 only as idea sources, not merge candidates.
```

## Current safe decision

Do not merge any remaining open PR from GitHub-only state. The next destructive/structural operations require local validation evidence first.
