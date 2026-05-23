# Tools/validation/agent_context context

## Role

`Tools/validation/agent_context` contains checks for agent context packs, RAG context packs, selected semantic chunks, local enrichment plans and shared toolbox bundles.

## Responsibilities

- Validate AI context pack contracts.
- Validate internal RAG context-pack contracts and retrieval smokes.
- Validate selected semantic chunk reports.
- Validate full-context golden proposal docs/reports.
- Validate local AI enrichment plan reports.
- Validate shared toolbox AI-to-AI bundle reports.

## Representative commands

Use through the validation dispatcher:

```powershell
python -m Tools.validation check_ai_context_pack_contract ...
python -m Tools.validation check_rag_context_pack_contract ...
python -m Tools.validation run_rag_ingest_resilience_smoke ...
python -m Tools.validation run_rag_retrieval_smoke ...
python -m Tools.validation run_rag_ollama_embed_smoke ...
python -m Tools.validation check_selected_semantic_chunks ...
python -m Tools.validation check_full_context_golden_docs_contract ...
python -m Tools.validation check_full_context_golden_proposals ...
python -m Tools.validation check_local_ai_enrichment_plan ...
python -m Tools.validation run_shared_toolbox_ai_to_ai_bundle_smoke ...
python -m Tools.validation run_substantive_planning_smoke ...
```

## Output role

Outputs are validation reports for context artifacts and planning inputs.

## Notes

- Context validation does not prove patch applicability.
- Keep chunk/context reports bounded and traceable.
- Add checks here when context artifact schemas change.
