# Local Validation Evidence Bundle Policy

## Purpose

This directory stores compact Git-trackable validation evidence for manual review.

It must not become a raw output archive.

The repository source of truth is:

```text
raw local run outputs -> output/** only, ignored/local
compact review evidence -> docs/LOCAL_VALIDATION_EVIDENCE/
GitHub audit -> from committed compact bundles only
```

## Bundle law

Use this rule for every run:

```text
commit the smallest bundle that proves the decision
```

Do not commit every generated intermediate artifact.

Do not commit raw provider output directories.

Do not commit full analysis JSON unless it is a compact bounded evidence bundle.

## Allowed committed files

Allowed here:

```text
small compact bundle JSON
small compact bundle Markdown
selected golden evidence files that are intentionally reused across many runs
README/policy files
```

Typical accepted names:

```text
pr<NUMBER>_<topic>_bundle_<timestamp>.json
pr<NUMBER>_<topic>_bundle_<timestamp>.md
project_complete_ai_to_ai_bundle_<timestamp>.json
project_complete_ai_to_ai_bundle_<timestamp>.md
full_context_golden_selected_chunks_evidence.json
```

## Forbidden committed files

Do not commit:

```text
raw output/** directories
full provider transcripts unless bounded/truncated by the bundle builder
full analysis JSON dumps copied by hand
checkpoint directories
raw NPU audit context dumps
raw GPU planner responses
SQLite/database files
render outputs
large binary artifacts
```

## Size guidance

Soft limits:

```text
single bundle JSON: prefer under 250 KB
single bundle Markdown: prefer under 250 KB
single PR evidence addition: prefer under 1 MB total
included_artifact_count: prefer <= 10 for normal PRs
included_artifact_count: prefer <= 20 for complete-run PRs
max included chars per artifact: prefer <= 12000
```

If a bundle exceeds these limits, reduce included artifacts or include summaries instead of raw content.

## Retention guidance

Keep:

```text
one final evidence bundle per PR
one final evidence bundle per complete run
one after-fix bundle when an earlier bundle had a validation defect
stable golden evidence used by many tools
```

Avoid keeping:

```text
multiple failed bundles for the same PR
superseded pre-fix bundles when an after-fix bundle exists
large duplicate bundles that prove the same state
```

Current non-destructive policy:

```text
new work should avoid adding redundant bundles
existing bundles are not deleted automatically
cleanup/removal requires explicit human approval
```

## Bundle replacement rule

When a validation defect is found in a bundle:

```text
1. create an after-fix bundle
2. make the after-fix bundle the reviewed artifact
3. reference the superseded bundle only as historical context
4. do not add more bundles unless the reviewed evidence changes materially
```

For example:

```text
pr113_gpu_npu_sync_bundle_*.json        -> initial bundle
pr113_gpu_npu_sync_bundle_after_fix_*.json -> reviewed bundle after analyzer fix
```

The after-fix bundle is the authoritative one for review.

## Required metadata in future bundles

Future bundle builders or bundle quality checks should prefer including:

```text
run_id or PR number
source commit SHA
branch name
request Markdown path, when applicable
procedure Markdown path, when applicable
primary reports included
explicit guardrail flags
included_artifact_count
budget/truncation status
recommended_next_layer
whether this bundle supersedes another bundle
```

## Review rule

Reviewers should reject evidence if:

```text
raw output/** was committed directly
bundle does not include the task/request when the run was AI-to-AI
bundle is too large because it includes raw transcripts instead of summaries
bundle lacks guardrail flags
bundle hides which earlier bundle it supersedes
```

## Future cleanup tool candidate

A future report-only tool may inventory this directory and propose cleanup candidates:

```text
Tools/ai/analyze_evidence_bundle_retention.py
```

It should only report candidates. It must not delete files automatically.

Potential outputs:

```text
docs/LOCAL_VALIDATION_EVIDENCE/evidence_bundle_retention_inventory_<timestamp>.json
docs/LOCAL_VALIDATION_EVIDENCE/evidence_bundle_retention_inventory_<timestamp>.md
```

Deletion or archival remains explicit/manual only.
