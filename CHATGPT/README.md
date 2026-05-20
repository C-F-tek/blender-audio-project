# CHATGPT handoff — NEWCONCEPT hardware memory — 2026-05-05

## Purpose

Compact ChatGPT handoff folder for the architecture discussion about:

```text
NPU tool-proxy helper
Intel GPU0 coworker lane
SQLite shared heap memory
FTS5 + embedding cache + hybrid search
broker delegation contract
start-of-run CSV/index/discovery bootstrap
manual evidence/bundle push policy
```

This folder is advisory memory for future chats and local AI agents. It does not implement runtime changes.

## Files

```text
01-architecture-summary.md
02-sqlite-heap-memory-design.md
03-broker-hardware-delegation-contract.md
04-implementation-plan.md
05-reset-sync-commands.md
```

## Current decision

The accepted direction is:

```text
NPU = bounded delegated tool worker, not primary advisory
GPU0 = possible OpenVINO coworker after report-only capability/probe contract
SQLite = shared heap memory with typed facts and strict persistence policy
CSV/index/discovery = start-of-run factual base and compact evidence
runtime broker = mandatory policy/control plane for delegated hardware calls
```

## Current priority proposal

Next architectural patch candidate:

```text
GPU0/NPU hardware capability manifest report-only
+ SQLite heap memory schema/policy
+ NPU tool-proxy schema docs + validator
+ broker delegation contract
```

Do not implement autonomous coworker behavior before report-only contracts, evidence and validators exist.
