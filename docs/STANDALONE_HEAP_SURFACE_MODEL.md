# Standalone heap surface model

## Status

Current compact model extracted from the historical standalone heap universe task notes.

Use this document when reasoning about the heap as an explicit runtime surface rather than as model memory or a prompt-only chain.

## One-line model

```text
strict request -> preload surfaces -> heap facts -> exchange events -> broker/provider/validator evidence -> composer package
```

## Why it matters

A useful heap must expose deterministic surfaces. It cannot depend on hidden chat memory.

Required surfaces:

```text
tool catalog
operational SQLite memory
SQLite FTS5 search
markdown chunk memory
semantic code chunks
semantic evidence chunks
context namespace
AI context pack
transient request context
broker/tool execution
provider lane reports
validator evidence
exchange event stream
final composer package
```

Without these surfaces, the system falls back to a prompt chain. With them, another AI, validator or operator can inspect what happened.

## Heap vs exchange

```text
heap = shared runtime state
exchange = observable event flow around that state
```

The heap records facts:

```text
inputs
constraints
lane status
tool outputs
provider claims
validation results
candidate operations
blocked reasons
```

The exchange records interactions:

```text
run entered
lane registered
tool requested
tool completed
tool failed
provider reported
validator completed
candidate accepted
candidate rejected
exit product produced
```

The exchange is what prevents the heap from becoming an opaque JSON dump.

## Preload model

Before a heap run starts, preload should create artifact references such as:

```text
required context files
repo docs map
semantic code chunks
tool catalog
shared memory
operational memory status
operational memory search
shared context
AI context pack
semantic evidence chunks
task file
```

These become heap facts, not side logs.

## Namespace model

The heap should not flatten all inputs into one undifferentiated prompt.

Recommended namespaces:

```text
operator_request
startup_preload
repo_docs
semantic_code
semantic_evidence
shared_memory
operational_memory
tool_catalog
provider_reports
proposal_iterations
refinement_tasks
validators
composer_package
```

## Memory model

Operational memory should be explicit and inspectable:

```text
write current task/run facts
search previous facts and decisions
expose JSON reports for writes/searches
keep SQLite files local/private
never commit SQLite runtime files
```

The heap consumes memory through artifact references and compact summaries.

## Chunk model

Large repository context should become addressable chunks:

```text
large docs -> chunks
chunks -> manifest
manifest -> startup task file
heap revisions -> compact chunk references
composer -> accepted heap states and references
```

This lets the system work beyond a single model context window.

## Tool catalog model

The heap should know what tools exist before provider planning.

Tool catalog fields should answer:

```text
what tool exists?
what role does it have?
what input/output contract does it use?
is it safe/unsafe?
does it perform provider execution?
does it write source?
which artifacts does it create?
```

## Broker model

Provider-requested work must pass through controlled broker paths.

```text
provider asks for tool
broker validates request
controlled tool executes
output becomes heap event/artifact
failure becomes heap fact
```

Provider text alone is not proof of tool execution.

## Provider lane model

Minimum useful provider lanes:

```text
gpu1_provider_planner
gpu0_provider_peer
npu_micro_task_auditor
```

Names can change. The requirement stays: lane participation must be observable in same-heap evidence.

A useful lane report should answer:

```text
was execution requested?
was execution performed?
what input refs were used?
what output refs were produced?
what warnings/errors happened?
what did the lane recommend or reject?
```

## Output classification model

Heap output must be classified before it can drive source changes.

```text
diagnostic evidence
recommendation evidence
candidate operation
code product
patch product
review product
blocked reason
```

Rules:

```text
provider answer != product
recommendation != product
metadata-only draft != product
candidate without target/diff != product
blocked reason = valid exit state
```

## Refinement model

Rejected proposals should produce next actions, not dead ends.

Useful refinement artifacts:

```text
proposal revision
parallel cycle report
refinement task
rejection reason
accepted/rejected evidence map
```

## Composer boundary

The composer assembles accepted heap state into one export package.

It should include:

```text
accepted proposals
rejected proposals
rejection reasons
GPU/provider review
NPU audit
provider reports
preload manifest
parallel cycle reports
refinement tasks
action list
download/export manifest
```

The composer assembles; it must not invent source-change authority.

## Minimal evidence questions

A useful standalone heap run should answer:

```text
what entered the heap?
which namespaces were populated?
which lanes registered?
which lanes produced evidence?
which tools were requested?
which tool requests failed?
which validators ran?
which proposals were accepted or rejected?
what final product or blocked reason was produced?
```

## Related current files

```text
docs/HEAP_EXCHANGE_USEFUL_MODEL.md
Tools/ai/heap_runtime/TOOL_CONTEXT.md
Tools/ai/heap_context_memory_reload/TOOL_CONTEXT.md
Tools/ai/runtime_tool/TOOL_CONTEXT.md
Tools/ai/provider_runtime_blackboard/TOOL_CONTEXT.md
Tools/ai/agent_context/TOOL_CONTEXT.md
Tools/ai/agent_memory/TOOL_CONTEXT.md
```

## Historical source

```text
docs/LOCAL_AI_TASKS/standalone-heap-universe-tool-surface-2026-05-10.md
```