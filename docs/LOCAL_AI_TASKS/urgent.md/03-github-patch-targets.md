# 03 — GitHub patch targets

## Patch target A — urgent split-document entrypoint

Create and maintain:

```text
docs/LOCAL_AI_TASKS/urgent.md/README.md
docs/LOCAL_AI_TASKS/urgent.md/01-operational-contract.md
docs/LOCAL_AI_TASKS/urgent.md/02-next-run-inspection.md
docs/LOCAL_AI_TASKS/urgent.md/03-github-patch-targets.md
```

Update:

```text
docs/LOCAL_AI_TASKS/README.md/README.md
```

Purpose: keep urgent operator intent visible without appending another large unstructured Markdown file.

## Patch target B — evidence bundle manifest completeness

Current builder direction:

```text
python -m Tools.ai build_github_evidence_bundle ...
```

Patch target files:

```text
Tools/ai/repository_product/github_evidence_bundle/cli.py
Tools/ai/repository_product/github_evidence_bundle_ready/cli.py
Tools/ai/_shared/github_evidence_bundle_artifacts.py
Tools/ai/_shared/github_evidence_bundle_markdown.py
```

Required behavior:

```text
artifact_manifest lists reports, explicit artifacts, recursive artifacts and auto-included related artifacts
manifest previews are marked preview_only, not full content inclusion
manifest entries declare git_trackable_copy=false
Markdown output shows role, copy policy and content mode
raw output deny prefixes/fragments remain enforced
```

## Validation commands

Use dispatcher/module commands where possible:

```powershell
python -m py_compile `
  .\Tools\ai\_shared\github_evidence_bundle_artifacts.py `
  .\Tools\ai\_shared\github_evidence_bundle_markdown.py `
  .\Tools\ai\repository_product\github_evidence_bundle\cli.py `
  .\Tools\ai\repository_product\github_evidence_bundle_ready\cli.py

python -m Tools.ai build_github_evidence_bundle `
  --repo-root . `
  --basename urgent_manifest_smoke `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report .\output\patch_specs\agent_review_patch_plan.json `
  --artifact .\output\patch_specs\agent_review_patch_plan.md `
  --no-auto-discover-selected-chunks-evidence

python -m Tools.validation check_github_evidence_bundle `
  --repo-root . `
  --bundle .\docs\LOCAL_VALIDATION_EVIDENCE\urgent_manifest_smoke.json `
  --output .\output\validation\urgent_manifest_smoke_validation.json

git diff --check
git status --short
```

Do not commit `output/**`. Commit generated `docs/LOCAL_VALIDATION_EVIDENCE/*` only when it is current, compact and intentionally selected.

## Commit scope

Commit only:

```text
Tools/ai/_shared/github_evidence_bundle_artifacts.py
Tools/ai/_shared/github_evidence_bundle_markdown.py
Tools/ai/repository_product/github_evidence_bundle/cli.py
Tools/ai/repository_product/github_evidence_bundle_ready/cli.py
docs/LOCAL_AI_TASKS/README.md/README.md
docs/LOCAL_AI_TASKS/urgent.md/**
```

## Commit message

```text
feat(ai): record urgent run unica patch queue
```
