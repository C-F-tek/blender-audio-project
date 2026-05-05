<!-- IA-CARMINE-MD-SPLIT: part -->
# TOOL_AGNOSTIC_ARTIFACT_EXPANSION — parte 002 di 002

Sorgente indice: [`../TOOL_AGNOSTIC_ARTIFACT_EXPANSION.md`](../TOOL_AGNOSTIC_ARTIFACT_EXPANSION.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)

## New horizon: universal artifact proposal

The code edit proposal can evolve into a universal proposal shape.

Generic shape:

```json
{
  "kind": "artifact_proposal",
  "domain": "code|docs|audio|text|scene_spec|prompt",
  "target": {},
  "rationale": "why",
  "strategy": "how",
  "payload": {},
  "validation_commands": [],
  "stop_conditions": [],
  "manual_review_required": true,
  "provider_execution_performed": false,
  "artifact_write_performed": false
}
```

Do not replace domain-specific proposals too early. First collect fixtures and real examples.

## Recommended next implementation sequence

### Phase A — complete code lane base

```text
code_edit_proposal_smoke
code patch artifact pack includes code edit proposal summaries
macro evidence bundle includes code edit proposal smoke
local validation proves contract
```

### Phase B — introduce artifact domain registry

```text
create registry module
add code/docs domains
add smoke validator for registry
consume registry in proposal validators where useful
```

### Phase C — add non-code fixture lane

Choose one low-risk domain first:

```text
text artifact proposal
```

Reason:

```text
text has low runtime risk
text is easy to validate structurally
text can reuse docs/prompt workflows
```

Then add:

```text
audio summary proposal
scene spec proposal
provider result proposal
```

### Phase D — measure limits

For each domain, measure:

```text
artifact size
summary quality
validator strictness
manual review burden
cross-domain follow-up quality
```

## Decision rule

A new capability is acceptable only when it preserves:

```text
explicit evidence
bounded artifact size
manual review
validated report contract
no implicit runtime side effects
compact GitHub evidence
```

If a capability requires hidden execution, raw output commits or automatic mutation, it belongs in a separate explicit implementation branch, not in the agnostic base layer.
