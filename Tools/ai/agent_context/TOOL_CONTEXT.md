# Tools/ai/agent_context context

## Role

`Tools/ai/agent_context` prepares the input universe consumed by heap runtime, brokered tools and provider lanes. It is responsible for context packs, tool inventory, transient request context, semantic evidence chunks and selected code chunks.

This area does not apply patches. It builds structured context and evidence so later stages can decide what is targetable.

## Typical inputs

```text
request Markdown
docs/**
Tools/**
configuration files
previous compact evidence
memory inventory
semantic/code chunk manifests
```

## Typical outputs

```text
AI context pack
agent state packet
agnostic tool inventory
memory inventory summary
transient request context
semantic evidence chunks
selected semantic code chunks
shared toolbox AI-to-AI bundle
```

Most outputs are runtime artifacts. Commit only compact documentation/evidence that is explicitly intended for Git.

## Key command surface

Use through the area dispatcher:

```powershell
python -m Tools.ai build_agent_agnostic_tool_inventory ...
python -m Tools.ai build_agent_memory_inventory ...
python -m Tools.ai build_agent_transient_request_context ...
python -m Tools.ai ai_context_pack ...
python -m Tools.ai semantic_evidence_chunks ...
python -m Tools.ai select_semantic_code_chunks ...
python -m Tools.ai shared_toolbox_bundle ...
```

## Boundaries

- Context is not a patch target list.
- Semantic chunks are retrieval/evidence inputs, not proof of applicability.
- The final target shortlist must be verified later by lab/matrix/validation.
- Do not add source-write behavior in context builders.

## When extending

Add a new package family only when it produces a new kind of reusable context artifact. Otherwise extend the existing context pack, semantic evidence or inventory builders.
