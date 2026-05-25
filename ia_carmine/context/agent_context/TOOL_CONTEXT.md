# ia_carmine/context/agent_context context

## Role

`ia_carmine/context/agent_context` prepares the input universe consumed by heap runtime, brokered tools and provider lanes. It is responsible for context packs, internal RAG retrieval packs, tool inventory, transient request context, semantic evidence chunks and selected code chunks.

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
SQLite/FTS5/vector RAG context pack
shared toolbox AI-to-AI bundle
```

Most outputs are runtime artifacts. Commit only compact documentation/evidence that is explicitly intended for Git.

## Key command surface

Use context builders through the broker/runtime path. Direct module execution is
for focused diagnostics only and still requires explicit profiles/paths:

```powershell
python -m ia_carmine.cli build_agent_agnostic_tool_inventory ...
python -m ia_carmine.cli build_agent_memory_inventory ...
python -m ia_carmine.cli build_agent_transient_request_context ...
python -m ia_carmine.context.agent_context.ai_context_pack.cli --profile <profile> ...
python -m ia_carmine.context.agent_context.rag_context.ingest_repo_cli --rag-profile <profile> ...
python -m ia_carmine.context.agent_context.rag_context.build_context_pack_cli --rag-profile <profile> ...
python -m ia_carmine.context.agent_context.rag_context.query_context_cli --rag-profile <profile> ...
python -m ia_carmine.cli semantic_evidence_chunks ...
python -m ia_carmine.cli select_semantic_code_chunks ...
python -m ia_carmine.cli shared_toolbox_bundle ...
```

## Boundaries

- Context is not a patch target list.
- Semantic chunks are retrieval/evidence inputs, not proof of applicability.
- The RAG SQLite DB is an ignored runtime artifact; commit the code/contracts, not `*.sqlite` outputs.
- RAG uses an explicit `--rag-profile` separate from run/provider/lane profiles.
- `gpu1_dynamic_context_pack` is the active provider surface for GPU1; `startup_unified_context_pack` is a legacy technical attachment and is not a terminal startup blocker.
- The final target shortlist must be verified later by lab/matrix/validation.
- Do not add source-write behavior in context builders.

## When extending

Add a new package family only when it produces a new kind of reusable context artifact. Otherwise extend the existing context pack, semantic evidence or inventory builders.
