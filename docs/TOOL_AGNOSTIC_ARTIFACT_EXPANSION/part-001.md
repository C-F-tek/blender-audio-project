<!-- IA-CARMINE-MD-SPLIT: part -->
# TOOL_AGNOSTIC_ARTIFACT_EXPANSION — parte 001 di 002

Sorgente indice: [`../TOOL_AGNOSTIC_ARTIFACT_EXPANSION.md`](../TOOL_AGNOSTIC_ARTIFACT_EXPANSION.md)

## Navigazione

- [Indice](README.md)
- [Parte successiva](part-002.md)

# Tool-Agnostic Artifact Expansion Roadmap

## Purpose

This document reframes the current local AI work as a tool-agnostic artifact engine rather than a Blender-only prototype.

The immediate implementation is code-focused because code is the safest and most testable base layer. The same philosophy should generalize to audio, text, documentation, scene descriptions, validation reports, prompts and future domain-specific artifacts.

## Core shift

Previous framing:

```text
Blender prototype support
```

Current framing:

```text
tool-agnostic artifact production and validation framework
```

The framework should be able to ingest evidence, generate proposals, validate contracts, produce compact bundles and keep every high-risk action manual-review-first.

## Stable primitives already emerging

The current PR introduces or connects these primitives:

```text
contract drift report
agent review patch plan
code patch plan
complete code edit proposal
docs follow-up suggestion
artifact pack
evidence bundle
line-count evidence
agnostic context stack smoke
manual review gate
```

These are not code-only concepts. They can be generalized as:

```text
domain evidence
artifact proposal
artifact validator
artifact follow-up
artifact pack
artifact evidence bundle
manual promotion gate
```

## Domains

The framework should treat domains as lanes, not as hard-coded project identities.

Initial domains:

```text
code
docs
validation
workflow
local_ai_context
```

Planned domains:

```text
audio
text
prompt
scene_spec
render_plan
asset_manifest
model_context
provider_result
```

Each domain should declare:

```text
input evidence types
allowed output artifact types
validators
blocked targets
manual review rules
promotion rules
bundle summary shape
```

## Artifact lifecycle

Every artifact should pass through the same lifecycle:

```text
collect evidence
normalize evidence
produce proposal
validate proposal
pack compact evidence
manual review
promote or reject
```

No artifact should jump directly from AI generation to source/runtime mutation.

## Universal guardrails

All lanes inherit these default guardrails:

```text
provider_execution_performed = false unless explicitly requested
patch_application_performed = false unless explicitly requested
source_writes_performed = false unless explicitly requested
manual_review_required = true
output/** is local only
raw runtime artifacts are not versioned
compact evidence is preferred
full analysis JSON is not committed
SQLite/database artifacts are not committed
Blender runtime is not executed unless the task is explicitly runtime-scoped
```

## Artifact categories

### Evidence artifact

Evidence artifacts describe what was observed.

Examples:

```text
code_contract_drift
docs_contract_drift
python_line_count_csv
agnostic_context_stack_smoke
provider_result_report
audio_analysis_summary
text_corpus_summary
```

Requirements:

```text
schema_version
kind
passed
errors
warnings
provider_execution_performed
patch_application_performed
source_writes_performed
source references
compact summary
```

### Proposal artifact

Proposal artifacts describe what could be changed or generated.

Examples:

```text
agent_review_code_patch_plan
code_edit_proposal
agent_review_code_docs_followup
scene_patch_plan
audio_feature_mapping_plan
text_rewrite_plan
prompt_refinement_plan
```

Requirements:

```text
kind
apply_mode
manual_review_required
targets
rationale
strategy
validation_commands
stop_conditions
risk
status
```

### Pack artifact

Pack artifacts summarize large proposal/evidence sets for GitHub review.

Examples:

```text
code_patch_artifact_pack
github_evidence_bundle
future audio_artifact_pack
future text_artifact_pack
future scene_spec_artifact_pack
```

Requirements:

```text
raw content minimized
large payloads omitted or bounded
reviewable summaries only
links/paths to source local artifacts
manual decision section
```

## Limits to actively test

The next phase should intentionally find limits in these areas.

### 1. Schema pressure

Question:

```text
Can one schema family describe code, docs, audio, text and scene artifacts without becoming vague?
```

Test strategy:

```text
create one minimal proposal fixture per domain
run common smoke validator concepts
compare required fields
split only when field semantics truly diverge
```

### 2. Evidence size pressure

Question:

```text
How much raw evidence can be summarized before decisions lose traceability?
```

Test strategy:

```text
large code file summary
large audio analysis summary
large text corpus summary
large provider result summary
compact pack output
manual review check
```

### 3. Target safety pressure

Question:

```text
Can target path policies stay generic while still blocking dangerous domain-specific outputs?
```

Test strategy:

```text
code target policy
docs target policy
audio output target policy
scene spec target policy
runtime artifact target policy
```

### 4. Validator portability

Question:

```text
Can validators be declared as metadata and executed separately from artifact generation?
```

Test strategy:

```text
proposal declares validators
smoke validates validators exist as strings
runner remains separate
no automatic execution in proposal generation
```

### 5. Provider boundary

Question:

```text
Can provider outputs be consumed as evidence without turning provider execution into a hidden dependency?
```

Test strategy:

```text
provider_result_report fixture
provider_execution_performed flag
source prompt hash
output summary only
manual review gate
```

### 6. Domain handoff quality

Question:

```text
Can one artifact from a domain notify another domain safely?
```

Examples:

```text
code patch plan -> docs follow-up
audio analysis -> scene spec proposal
text analysis -> prompt refinement plan
provider result -> validation follow-up
```

Test strategy:

```text
build bridge artifacts
validate no writes
validate compact summary
require manual review
```

## New horizon: artifact domain registry

The framework should eventually define a domain registry.

Potential file:

```text
Tools/ai/artifact_domain_registry.py
```

Initial registry record:

```json
{
  "domain": "code",
  "proposal_kinds": ["agent_review_code_patch_plan", "code_edit_proposal"],
  "evidence_kinds": ["code_contract_drift", "python_line_count_csv"],
  "pack_kinds": ["code_patch_artifact_pack"],
  "blocked_target_prefixes": ["output/", "renders/"],
  "blocked_target_suffixes": [".db", ".sqlite", ".sqlite3"],
  "requires_manual_review": true
}
```

This would let future domains plug into the same lifecycle without copying logic.
