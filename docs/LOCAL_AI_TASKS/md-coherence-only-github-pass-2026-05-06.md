# MD Coherence Only GitHub Pass — 2026-05-06

## Scope

This runbook is for GitHub-only Markdown coherence work.

Allowed scope:

```text
Markdown documentation only
indexes and reading flow
session notes
canonical principles
superseded/historical/delete-candidate markers
Markdown split/index policy
```

Out of scope:

```text
source code changes
workflow script changes
provider/model behavior changes
local output artifacts
generated indexes
database files
renders/media
```

## Line policy

Maintained Markdown must stay compact.

```text
active .md file <= 700 lines
preferred active runbook <= 700 lines
```

When a maintained Markdown file exceeds 700 lines:

```text
keep original file as compact index
create sibling folder named exactly like the file, including .md: <file>.md/
move detail into <file>.md/part-001.md, part-002.md, ...
keep each part <= 700 lines
link every part from the compact index
```

Generated evidence may exceed 700 lines only when it is classified as evidence and has a compact manifest, summary or index.

## Add-before-prune workflow

Before deleting or replacing docs:

1. update or create the canonical target;
2. add it to the nearest index;
3. mark older overlap as one of:
   - `superseded by <path>`
   - `historical evidence`
   - `application-domain only`
   - `generated, do not hand-edit`
   - `delete candidate`
4. delete only when the user explicitly asks or the file is clearly obsolete and non-evidence;
5. never delete compact validation evidence just because it is old.

## Current canonical doctrine

```text
GPU1 / Ollama / RTX 5080 = mandatory primary advisory planner
GPU0 / OpenVINO = companion peer worker
NPU = micro-fast task assistant and lightweight tool-support lane
deterministic scripts = heavy audit and validation authority
runtime tool broker = controlled tool execution for GPU1 and GPU0 requests
```

Primary document:

```text
docs/LOCAL_AI_TASKS/gpu-peer-exchange-operational-principle.md
```

## Evidence and generated material

Do not commit these as part of MD-coherence work:

```text
output/**
indexAI/code_chunks/**
*.db
*.sqlite
*.sqlite3
renders/**
generated media
```

`docs/LOCAL_VALIDATION_EVIDENCE/` may contain compact committed snapshots. Treat them as evidence, not maintained source documentation.

## GitHub-only validation

GitHub-only MD passes should report:

```text
changed Markdown files
line-count status when known
new/updated reading-flow links
superseded or delete-candidate markings
known validation gaps due to no local execution
```

Local validation, when available, should run Markdown inventory and docs link checks through the unified launcher or validator README.
