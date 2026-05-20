# 01 — Architecture summary

## Accepted direction

The current IA-Carmine architecture should evolve by enriching the existing run-unica, broker, evidence and SQLite-memory lanes instead of adding disconnected parallel memory systems or uncontrolled autonomous agents.

Primary direction:

```text
GPU/Ollama primary lane
  -> planner / reviewer / advisory / patch-plan reasoning

NPU/OpenVINO lane
  -> bounded tool-proxy helper
  -> passive context helper
  -> lightweight classifier/calculator/comparator
  -> optional typed memory fact contributor

Intel GPU0/OpenVINO lane
  -> possible coworker for compatible workloads after report-only capability contracts

CPU deterministic lane
  -> validators, parsers, inventories, CSV/index/discovery, reports

SQLite heap memory
  -> shared typed memory substrate for lane outputs, decisions, promotion candidates and unresolved questions

runtime broker
  -> mandatory policy, routing, capability, timeout, evidence and side-effect control plane
```

## Why NPU tool-proxy, not advisory

NPU should not be promoted directly to primary advisory just because it can decode text.

Better fit:

```text
small prompt
small response
strict JSON schema
bounded context
timeout
classification / calculation / summary
no source write
no patch application
```

NPU becomes useful as a callable local helper used by the main AI, not as an independent repository-wide reasoning agent.

## GPU0 coworker stance

Intel GPU0 can be used first as:

```text
device detection
capability reporting
report-only OpenVINO probe
future embedding/classification/batch worker
```

Do not activate it immediately as an autonomous worker. Real delegation requires request/response schemas, broker policy, evidence and validators.

## CSV/index/discovery before reasoning

The run-unica should start by generating factual repository visibility surfaces:

```text
Markdown inventory
script inventory
Python line-count CSV/MD
function/class/method inventory CSV
repository consistency map/smoke
semantic chunk manifest
selected chunk evidence
auto-discovery report
index repair plan/report
```

These artifacts should become the shared factual base consumed by GPU primary lane, NPU helper lane and future GPU0 coworker lane.

## Evidence push rule

For serious runs, push selected compact evidence manually for now.

Push/review:

```text
docs/LOCAL_VALIDATION_EVIDENCE/*.json
docs/LOCAL_VALIDATION_EVIDENCE/*.md
selected compact CSV/MD evidence when useful
bundle ZIP uploaded/attached for chat/master-AI review
```

Never push as normal source:

```text
output/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
*.db
*.sqlite
*.sqlite3
renders/**
raw media
```

## Candidate next patch family

```text
GPU0/NPU hardware capability manifest report-only
+ SQLite heap memory schema/policy
+ NPU tool-proxy schema docs + validator
+ broker delegation contract
```

Implementation should be report-only first.
