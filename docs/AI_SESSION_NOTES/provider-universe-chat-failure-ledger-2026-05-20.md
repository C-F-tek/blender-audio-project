# Provider Universe Chat Failure Ledger - 2026-05-20

## Purpose

This note records the failures called out during the chat so future agents do
not rediscover or repeat them. It is deliberately direct: these are failure
items, not a success narrative.

## Operator Complaints To Preserve

- The assistant wrote plans/prose while the operator expected immediate runtime
  repair.
- The assistant treated a narrow fix as "done" while the operator contract had
  many unresolved tasks.
- The assistant used broad wording that sounded like completion even though only
  targeted patches and smokes had run.
- The assistant kept explaining concepts the operator already knew, especially
  pointer purpose and provider roles.
- The assistant initially treated non-operational provider evidence as something
  that could be reported rather than a condition that must stop the run.
- The assistant did not immediately distinguish "mark lane bad" from "block the
  whole run".
- The assistant had to be corrected that all three provider lanes are part of
  the same universe and cannot be treated as optional background decoration when
  selected by the run.

## Assistant Conduct Failures

- The assistant consumed chat time with explanations when the operator had
  already provided the relevant runtime evidence.
- The assistant used broad architecture language before proving the concrete
  process and product behavior.
- The assistant treated partial targeted fixes as meaningful progress while the
  operator was asking for the whole selected runtime universe to stop or work.
- The assistant answered conceptual prompts defensively instead of immediately
  translating the correction into source-level guardrails.
- The assistant initially reasoned from status strings and summaries rather
  than enforcing the operator invariant: selected provider lanes are a single
  unit of execution.
- The assistant failed to state early enough that a run with provider lanes,
  zero provider blocks, zero proposals and rising CPU is not acceptable product
  behavior.
- The assistant added visibility first, but visibility alone was not the fix.
- The assistant had to be redirected from "lane is bad" to "the whole run must
  block and live peer processes must stop".
- The assistant used completion-sounding wording before a full product run was
  validated.

## Agent Limitation Exposed

- The agent can overfit to local smoke tests when the real operator complaint is
  end-to-end runtime behavior under live provider pressure.
- The agent can mistake evidence production for useful work when evidence is
  not converted into proposal blocks, pointer edges or product decisions.
- The agent can preserve too much machinery if not forced to distinguish
  operational provider work from diagnostic/report-only output.
- The agent can add console detail that helps debugging but does not change the
  failing runtime semantics.
- The agent can continue a coding loop on narrow files while the operator is
  pointing at a larger contract failure.
- The agent can create "game-like scripting" behavior when scripts produce
  activity, counters, telemetry or files without a causal product result.
- The agent must not treat generated artifacts, provider claims or partial text
  as proof of reasoning unless they enter the validated heap/pointer/product
  graph.
- The agent must not call a lane active just because a child process exists or
  an output JSON is being written.

## Runtime Failures Observed

- The run displayed provider lanes as active while `provider_blocks=0` and
  `proposals=0`.
- The run could continue after 100+ heap events without a usable product block.
- The flow could show `provider_lanes_running_or_written` while no proposal
  block was materialized.
- `CODE_PRODUCT_FULL_PATCH` was not produced in the interrupted run summaries.
- The final product path reported failure only after operator interruption,
  not as an immediate deterministic runtime block.
- The wrapper could return a JSON failure while provider child activity had
  already consumed CPU/GPU/NPU time.
- Cleanup/status lookup during operator interrupt could itself be interrupted,
  leaving trust in cleanup unclear.

## CPU And Process Failures

- CPU rose sharply when the provider/orchestrator section started.
- The operator observed high CPU/NPU usage with low GPU1 utilization, while GPU1
  was supposed to be the primary advisory lane.
- The assistant initially analyzed status strings instead of immediately making
  the runtime stop on a broken provider universe.
- The run needed a rule that when one selected provider lane is failed or
  non-operational, the remaining provider lane processes are terminated.
- The run also needed a product-level block, not just child termination.
- A later local process scan found no matching live provider processes, but that
  does not erase the earlier design failure.

## Provider Lane Failures

- GPU1 could produce partial text but that text did not become a proposal block
  soon enough.
- GPU1 primary activity was underpowered relative to the expected primary role.
- A second automatic GPU1 native-tool decision call after text generation could
  extend runtime without producing the actual product block.
- GPU0 was effectively workload/diagnostic evidence in the observed run, not a
  causal reviewer/refiner.
- GPU0 output risked being treated as telemetry rather than input to the next
  pointer/refinement step.
- NPU timed out or failed semantic/audit behavior and still appeared as a lane
  in the provider group.
- NPU activity was not enough if it did not produce semantic audit evidence.
- Provider "running" was treated too much like provider "alive and useful".
- Provider output needed an operational contract: semantic response, native tool
  call, review/refinement, audit, or concrete proposal evidence.

## Pointer And Heap Failures

- GPU0/NPU review evidence must feed the next pointer/revision context, not
  remain as isolated telemetry.
- `previous`, `next`, `refines`, and `resume_from` only matter if they carry
  causal input into the next proposal.
- A pointer graph that only records that something happened is not enough.
- If peer reports are diagnostic-only, they must not become valid
  `provider_peer_block` nodes.
- If provider peers fail, the heap must preserve the reason and block forward
  product composition.
- The runtime should not invent provider blocks just because a lane existed.

## Product Decision Failures

- `DIAGNOSTIC_ONLY` hid a product failure.
- Diagnostic-only reports could be marked `ready`; this was wrong.
- A provider product can be blocked for review, but should not be framed as a
  ready diagnostic product.
- The corrected decision for rejected provider artifacts with no concrete
  patchable output is `BLOCKED_PROVIDER_REVIEW`.
- A full code product must require verified targets, real diff/product evidence,
  and matrix validation.
- If those conditions are missing, the product must be blocked or explicitly
  non-applicable, not cosmetically completed.

## Console And Visibility Failures

- Early console output was too numeric and did not show enough human-auditable
  provider state.
- The console could show an orchestrator/support lane in a way that looked like
  useful work while product evidence was absent.
- More status fields helped, but visibility is not enough if the run continues
  after provider universe failure.
- Human-readable status must expose whether each lane is operational, diagnostic
  only, failed, or blocking the run.

## Context And Data Failures

- Huge runtime-generated context artifacts, including very large semantic code
  chunk Markdown, can become CPU/mechanical work in the live path.
- Generated runtime evidence must not become maintained source context unless it
  is compacted and indexed appropriately.
- Passing gigantic Markdown/context through live provider paths is not an
  acceptable substitute for SQLite/FTS/chunked reference retrieval.
- The correct pattern is refs plus bounded excerpts, with broker retrieval when
  details are needed.

## Environment Failures

- The local `.venv` under the active checkout was missing or not the configured
  provider-capable Python.
- The usable Python path observed later was
  `C:\Users\carmi\blender\blender-audio-project\.venv\Scripts\python.exe`.
- Provider/OpenVINO runs must verify the provider-capable environment before
  blaming GPU0/NPU.

## Git And Evidence Boundaries

- `output/**` and generated heavy evidence must stay out of Git.
- Compact source/docs/test changes are acceptable.
- A compact session note is appropriate when the chat itself identifies a
  failure mode that future agents must not repeat.
- Existing untracked tool-context Markdown should be reviewed as source/context,
  not confused with runtime output.

## Corrections In Current Patch

- Non-operational provider evidence is now marked `non_operational`, not
  `ready`.
- Diagnostic-only provider reports no longer publish `provider_peer_block`.
- Provider-universe failure now records `provider_universe_blocked_reason`.
- Provider-universe failure now writes product status `blocked_with_reason`.
- Provider-universe failure publishes a deterministic decision instead of
  silently continuing.
- Pending provider processes are terminated when the selected provider universe
  becomes inactive.
- The main run loop stops after provider-universe blocking.
- Provider refinement also stops after provider-universe blocking.
- GPU0 role naming was moved toward peer reviewer/refiner.
- NPU mode was moved to `peer_micro_audit`, with diagnostic-only classification
  when semantic execution is missing.
- Proposal/final readable smokes were updated for `BLOCKED_PROVIDER_REVIEW`.
- A smoke check now asserts inactive provider-universe state blocks the run.

## Still Not Proven

- A full real `python -m Tools.ai run` was not launched after these changes.
- End-to-end GPU1/GPU0/NPU semantic cooperation is not proven.
- SQL/FTS/chunk memory behavior is not fully proven by these smokes.
- Pointer/refinement composition across real provider revisions is not fully
  proven.
- The Deep Research task list remains larger than this patch.

## Rule For Future Agents

Do not treat selected provider lanes as background helpers. In this runtime, the
selected provider group is a single provider universe. If one selected lane is
failed or non-operational, the run must stop as `blocked_with_reason`, preserve
the reason, terminate live peer lanes, and refuse to invent product blocks.
