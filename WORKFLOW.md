# WORKFLOW — IA-Carmine Runtime Contract

This file is a required context-pack contract for the heap/runtime gate.
It must remain present because the AI context pack uses it as operational workflow input.

## Purpose

The repository is operated as a local AI orchestration workbench with one controlled entry, one shared heap/exchange runtime, and one validated product exit.

The workflow is not a collection of isolated scripts. A valid run must preserve a continuous execution chain:

input request -> shared heap -> brokered tools -> shared memory/context/chunks -> provider teamwork -> validation evidence -> product output

## Canonical entry

The operator-facing product entrypoint is:

Tools/workflow/run_unified_real_product_pr.ps1

The internal dynamic launcher is:

Tools/workflow/run_unified_local_ai_refactor.ps1

The heap runtime completeness gate is not a product generator by itself. It validates that the runtime universe is connected before the larger real-product run uses it.

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

## Non-negotiable runtime constraints

- Do not use gpt-oss as runtime/provider model.
- Do not use system Python or WindowsApps Python for provider/broker execution.
- Use the repository Python resolver / RepoPy policy.
- Do not bypass the broker for registered tools.
- Do not mute required context files to make a gate pass.
- Do not claim provider execution unless provider reports prove it.
- Do not claim product readiness if required memory/chunk/context artifacts are missing.
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
- response_text is complete and not truncated
- response_source identifies GPU1 as final synthesizer
- provider_refs and heap_event_refs point to real artifacts

## Failure semantics

The gate must prefer blocked_with_reason over a false ready.

If a required context file is missing, the correct behavior is to fail visibly and restore or update the missing contract, not to remove it from the required profile.

If broker tool execution fails, provider execution must not hide the failure.

If GPU1 says it is alone while GPU0/NPU contributions exist, the team manifest/context was not visible enough to the final provider and the run must be treated as semantically incomplete.
