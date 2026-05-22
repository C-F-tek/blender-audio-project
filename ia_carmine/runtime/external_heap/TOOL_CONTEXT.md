# ia_carmine/runtime/external_heap context

## Role

`ia_carmine/runtime/external_heap` owns external heap artifacts used to carry context between runs, chats and revision cycles.

It provides revision context, block pointer manifests, composed block responses and postrun packages so long-running work does not depend on chat memory.

## Responsibilities

- Build external heap revision context.
- Build block pointer manifests.
- Compose external heap block responses.
- Package postrun artifacts for follow-up runs.
- Preserve forward/backward/refines/resume relationships between proposal blocks and product artifacts.

## Representative command surface

Use through the AI dispatcher:

```powershell
python -m ia_carmine.cli external_heap_revision_context ...
python -m ia_carmine.cli build_external_heap_revision_context ...
python -m ia_carmine.cli build_external_heap_block_pointer_manifest ...
python -m ia_carmine.cli compose_external_heap_block_response ...
python -m ia_carmine.cli run_external_heap_postrun_package ...
python -m ia_carmine.cli external_heap_postrun_package ...
```

## Conceptual model

```text
proposal block -> pointer manifest -> revision context -> next run startup
```

The external heap layer makes previous work discoverable and resumable without requiring the chat transcript.

## Boundaries

- External heap artifacts are context/evidence, not source patches.
- Pointer graphs do not prove provider execution by themselves.
- Postrun packages should link to artifacts, not duplicate raw output blindly.
- Do not commit raw runtime packages unless explicitly compacted and selected as evidence.

## Expected artifacts

```text
revision context Markdown/JSON
block pointer manifest
external heap block response
postrun package report
```

## Validation expectations

Relevant checks include:

```powershell
python -m Tools.validation run_external_heap_revision_context_applicability_smoke ...
python -m Tools.validation run_external_heap_postrun_provider_execution_smoke ...
python -m Tools.validation run_external_heap_provider_execution_detection_smoke ...
```

## Extension notes

When extending this area, keep artifact references stable and navigable. Prefer structured pointer fields over prose-only continuity notes.