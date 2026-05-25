# WORKFLOW — IA-Carmine Runtime Contract

This file is a required context-pack contract for the heap/runtime gate.
It must remain present because the AI context pack uses it as operational workflow input.

## Purpose

The repository is operated as a local AI orchestration workbench with one controlled entry, one shared heap/exchange runtime, and one validated product exit.

The workflow is not a collection of isolated scripts. A valid run must preserve a continuous execution chain:

input request -> shared heap -> brokered tools -> shared memory/context/chunks -> provider teamwork -> validation evidence -> product output

## Canonical entry

The operator-facing product entrypoint is:

```powershell
python -m ia_carmine.cli run ...
```

PowerShell workflow wrappers are launch helpers only. They must require explicit
operator values and must not introduce model, profile, task, endpoint or budget
defaults.

The heap runtime completeness gate is not a product generator by itself. It validates that the runtime universe is connected before the larger real-product run uses it.

## External heap universe layer

The heap universe can now be extended by external, gate-safe adapters. These adapters do not replace the heap runtime completeness gate and do not modify its tool-call semantics.

Current external heap adapters:

- `ia_carmine/product/heap_final_proposals/normalize_final_causality/cli.py`
- `ia_carmine/runtime/external_heap/block_pointer_manifest/cli.py`
- `ia_carmine/runtime/external_heap/block_response/cli.py`
- `python -m ia_carmine.cli build_external_heap_revision_context`
- `ia_carmine/runtime/external_heap/postrun_package/cli.py`

The external layer models long AI work as persistent blocks rather than a single provider response window. Blocks may carry navigation and refinement pointers:

- `previous_block_id`
- `next_block_id`
- `refines_block_id`
- `resume_from_block_id`

Runtime intent:

- GPU1 can move forward or backward across proposal blocks.
- GPU1 can propagate newly discovered imports, variables, functions, classes or contracts into older blocks, then resume from the correct forward cursor.
- GPU0 can re-check old pointers in parallel and request refinement.
- NPU can audit old pointers in parallel for guardrails, placeholders, invented paths, undeclared source writes and repeated output.
- The final operator package can include a file-based long response composed from persisted blocks.

Revision context is explicit input to the canonical run. The runtime must not
select an implicit latest run or profile-derived revision context.

The standard operator path is to execute `python -m ia_carmine.cli run ...` with
all required values supplied on the command line. Post-run packaging may call
`ia_carmine/runtime/external_heap/postrun_package/cli.py` internally for the
selected `heap_context_closure_*` run:

1. causality normalization;
2. block pointer manifest generation;
3. primary long-response composition;
4. revision-context generation for the next run.

It does not replace the old composer. It consumes the old composer JSON and attaches the new long-response/revision artifacts to the same Documents package when the composer exposes `documents_dir`.

Manual debugging may call adapter modules directly, but those modules are not
alternate product run surfaces.

## Runtime policy

Every heap response must be validated by evidence produced in the same run universe.

A response is not valid when it is only static text. A valid response must prove, when required by the task:

- user request was written into the heap
- brokered tools were requested and executed
- operational memory was written and read
- transient request context was built
- semantic chunks or context pack evidence were created
- GPU0 contributed through its defined peer role
- NPU contributed through its defined micro-task/auditor role
- GPU1 consumed shared context and peer contributions before producing the final response
- product status is either ready or blocked_with_reason

When the external heap universe layer is used, a valid long response may be file-based instead of being fully contained in `response_text`. The package must then expose, as applicable:

- `external_heap_block_pointer_manifest.json/md`
- `external_heap_primary_long_response.md/json`
- `external_heap_revision_context.json/md`
- `heap_final_causality_normalized.json/md`
- `external_heap_postrun_package.json`
- the existing composer Documents package and download manifest

## Non-negotiable runtime constraints

- Do not use gpt-oss as runtime/provider model.
- Do not use system Python or WindowsApps Python for provider/broker execution.
- Use the repository Python resolver / RepoPy policy.
- Do not bypass the broker for registered tools.
- Do not mute required context files to make a gate pass.
- Do not claim provider execution unless provider reports prove it.
- Do not claim product readiness if required memory/chunk/context artifacts are missing.
- Do not claim product readiness when causal chain passed but product acceptance is blocked.
- Do not run Blender or FFmpeg unless the task explicitly enters that application-domain scope.
- Do not apply patches, write source, push, merge or delete from provider output alone.

## Expected heap heartbeat shape

For a minimal request such as:

request = ciao sei solo?

The runtime should prove:

- user_request event exists
- tool catalog evidence exists
- shared memory evidence exists
- operational memory write and search evidence exists
- transient context and chunk/context-pack evidence exist
- GPU0 peer produces a real observation from its tool/workload
- NPU micro-task produces a real audit/observation
- GPU1 sees the team context and produces the final cumulative response
- response_text is complete and not truncated, or a file-based long response artifact is present and linked from the composer package
- response_source identifies GPU1 as final synthesizer or identifies the external heap long-response composer as the file-based product assembler
- provider_refs and heap_event_refs point to real artifacts

## Failure semantics

The gate must prefer blocked_with_reason over a false ready.

If a required context file is missing, the correct behavior is to fail visibly and restore or update the missing contract, not to remove it from the required profile.

If broker tool execution fails, provider execution must not hide the failure.

If GPU1 says it is alone while GPU0/NPU contributions exist, the team manifest/context was not visible enough to the final provider and the run must be treated as semantically incomplete.

If the causal chain is passed but all proposal blocks are rejected, the correct product result is blocked_with_reason. The causality normalizer must keep causal-chain status separate from product-acceptance status.
