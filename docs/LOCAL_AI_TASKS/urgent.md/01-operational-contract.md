# 01 — Operational contract

## Canonical constraints

This urgent queue is governed by the current root and docs contracts:

```text
AGENTS.md
CHATGPT.md
docs/AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
docs/CORE_LANE_COMPLETENESS_CONTRACT.md
docs/HEAP_EXCHANGE_USEFUL_MODEL.md
docs/STANDALONE_HEAP_SURFACE_MODEL.md
docs/PROVIDER_LANES_UNIFIED_MIND_MODEL.md
docs/REAL_PRODUCT_RUN_MODEL.md
docs/COMPACT_EVIDENCE_MODEL.md
docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
```

## Evidence language

Use only explicit status words:

```text
not_proven
blocked_with_reason
diagnostic_only
evidence_only
candidate_operation
code_patch_product
validated
failed
unviable
```

Avoid completion-sounding language unless the evidence path is named.

## Product boundary

The requested outcome is a real product path, not activity. A product path requires:

```text
runtime evidence exists
candidate operations exist
target files are concrete
code/patch product or explicit no-op/block exists
validation commands are present
review artifact or commit/PR path is explicit
```

If source writes are expected, `changed_count > 0` or a real commit SHA must exist. Otherwise the state remains `not_proven` or `blocked_with_reason`.

## Lane completeness

For full/complete profiles, required lanes are not optional:

```text
request/input lane
startup/preload lane
heap/exchange lane
Ollama/main provider lane
GPU0 coworker lane when selected
NPU micro-lane when selected
runtime tool/broker lane
CPU validator lane
product boundary lane
compact evidence lane
```

`degraded`, `missing`, `unavailable` and `diagnostic_only` are unviable for complete/full pass semantics.

## Patch publication rule

GitHub publication is proven only by one of:

```text
commit SHA containing the intended source/docs changes
pull request containing the intended source/docs changes
merge commit containing the intended source/docs changes
```

Tool permission or repository push permission alone is not a commit.

## Urgent source of truth

This directory records the urgent operator request and the next inspection queue. It is not runtime evidence. Runtime evidence must still come from reports, validators, heap state, provider reports, tool broker outputs, code/patch products and Git metadata.
