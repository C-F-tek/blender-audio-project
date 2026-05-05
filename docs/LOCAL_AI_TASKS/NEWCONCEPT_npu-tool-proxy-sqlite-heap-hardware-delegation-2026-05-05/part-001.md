<!-- IA-CARMINE-MD-SPLIT: part -->
# NEWCONCEPT_npu-tool-proxy-sqlite-heap-hardware-delegation-2026-05-05 — parte 001 di 002

Sorgente indice: [`../NEWCONCEPT_npu-tool-proxy-sqlite-heap-hardware-delegation-2026-05-05.md`](../NEWCONCEPT_npu-tool-proxy-sqlite-heap-hardware-delegation-2026-05-05.md)

## Navigazione

- [Indice](README.md)
- [Parte successiva](part-002.md)

# NEWCONCEPT — NPU tool-proxy, SQLite heap memory and hardware delegation — 2026-05-05

## Status

Architecture exploration and operating direction for the next IA-Carmine run-unica evolution.

This document is review-first. It does not implement runtime changes by itself.

## External verification snapshot

OpenVINO documents `GPU.X` device naming for Intel GPUs. If a system has an integrated Intel GPU, its id is always `GPU.0`, and `GPU` is an alias for `GPU.0`. OpenVINO also supports explicit execution on `GPU.0`, `GPU.1` or AUTO multi-device combinations for compatible workloads.

OpenVINO GenAI documents `LLMPipeline(model_path, "NPU")` and NPU-specific configuration such as `MAX_PROMPT_LEN`, `MIN_RESPONSE_LEN`, `PREFILL_HINT` and `GENERATE_HINT`. The NPU LLM pipeline has device-specific limitations and is more natural for bounded prompts and controlled helper work than unbounded repository-wide advisory.

Conclusion:

```text
Intel GPU.0 can be treated as a candidate OpenVINO worker lane.
NPU can be treated as a bounded helper/tool-proxy lane.
NPU should not be promoted directly to primary advisory solely because decode works.
```

## Current IA-Carmine doctrine

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = presets or operator parameters, not scope
-No* flags = explicit opt-out from selected lanes
CSV/index/discovery surfaces are evidence lanes when relevant
large Markdown must not be a primary operational entrypoint
```

## Core idea

Move the NPU lane away from direct advisory responsibility and toward a controlled local tool-proxy/helper role.

The primary AI lane remains responsible for strategic reasoning, repository-wide planning, final recommendations and patch-plan selection. The NPU lane becomes a delegated local helper that receives bounded tasks from the primary AI/broker, returns schema-valid small outputs, and optionally contributes typed memory facts to a shared SQLite heap.

## Target lane model

```text
NVIDIA GPU / Ollama
  -> primary planner / advisor / patch-plan reasoning lane

NPU / OpenVINO GenAI
  -> bounded tool-proxy helper
  -> passive context helper
  -> lightweight classifier/calculator/comparator
  -> optional typed memory fact contributor

Intel GPU.0 / OpenVINO
  -> candidate coworker lane for compatible small models, embeddings, classification or batch inference
  -> explicit worker, not silent AUTO default

CPU deterministic lane
  -> validators, parsers, inventories, report builders, CSV/index/discovery generation

SQLite heap memory
  -> shared durable state for lane outputs, distilled facts, decisions, candidate promotions and unresolved questions

Runtime broker
  -> policy, routing, capability manifest, timeout, telemetry and side-effect control
```

## Why NPU as tool-proxy, not primary advisory

NPU/OpenVINO GenAI is useful, but its natural strength here is bounded delegated work:

```text
small prompt
small answer
strict schema
timeout
controlled model
controlled context
no source write
no patch apply
```

The repository-wide advisory task needs broad context, multi-file reasoning, patch-plan prioritization and stronger recovery from ambiguous evidence. That is still better assigned to the GPU/Ollama primary lane plus deterministic validators and telemetry.

## Allowed NPU tool-proxy tasks

Initial allowed task families:

```text
classify_finding
summarize_context_slice
compare_two_snippets
lightweight_calculation
label_tool_candidate
label_dead_code_candidate
label_unused_but_useful_candidate
extract_memory_fact
triage_patch_plan_item
triage_md_code_drift
```

Examples:

```text
Given this finding and these labels, choose the safest label and confidence.
Given these two helpers, say whether they duplicate behavior.
Given this line-count/function-count summary, flag likely extraction candidates.
Given this small calculation, solve it and return JSON.
Given this tool candidate, decide whether it is broker-safe, project-tool-only or app-domain-only.
```

## NPU tool-proxy non-goals

Not allowed by default:

```text
primary repository-wide advisory
unbounded patch planning
source writes
patch application
Git writes
secret access
network access
Blender runtime
FFmpeg runtime
media output
unreviewed generated-index mutation
bulk file rewrite
```

## SQLite heap memory concept

SQLite memory becomes the shared heap for local AI lanes.

Conceptual model:

```text
GPU/Ollama primary AI lane
  -> asks questions / delegates bounded work
  -> reads shared durable state
  -> writes final decisions and reviewed facts

NPU tool-proxy helper lane
  -> receives bounded tasks
  -> returns schema-valid responses
  -> writes compact, typed observations only when policy allows

Intel GPU.0 coworker lane
  -> may run compatible OpenVINO workloads
  -> writes only report-bound observations through broker policy

CPU deterministic lane
  -> writes inventories, validators, telemetry and report facts

SQLite heap memory
  -> stores distilled facts, lane outputs, unresolved questions, promotion candidates and artifact references
  -> never becomes source authority by itself
```

## Recommended SQLite heap namespaces

Do not use a single unstructured memory table for everything.

Recommended logical tables or namespaces:

```text
runs
lane_calls
memory_facts
entities
relations
observations
promotion_candidates
unused_useful_candidates
dead_code_candidates
tool_candidates
helper_extraction_candidates
unresolved_questions
artifact_refs
quarantined_memory
```

Every memory record should include:

```text
run_stamp
lane
source_artifact
source_file_or_component
confidence
created_at
review_after_or_expiry
scope
visibility
status
```

## Memory safety policy

```text
SQLite DB files remain untracked.
Do not commit *.db / *.sqlite / *.sqlite3.
Promote only compact summaries into docs/LOCAL_VALIDATION_EVIDENCE/ when needed.
Memory writes must be visible in manifest/telemetry/bundle when enabled.
Memory facts must be typed, timestamped and source-referenced.
Stale or low-confidence memory must be quarantined, not reused silently.
No secrets intentionally stored.
```

## Multi-consciousness model

IA-Carmine may treat local lanes as cooperating specialized workers:

```text
GPU primary lane = planner / reviewer / advisor
NPU helper lane = small local assistant / passive context / bounded tool proxy
Intel GPU.0 lane = OpenVINO coworker for compatible parallel tasks
CPU deterministic lane = validators / inventories / parsers / reports
SQLite heap = shared memory substrate
runtime broker = policy and routing layer
```

This is not permission to create uncontrolled autonomous agents. Every lane must have:

```text
capability manifest entry
input schema
output schema
timeout
side-effect policy
telemetry entry
error/degradation state
source-write policy
```

## Hardware delegation policy

Primary AI lanes may delegate work to local hardware only through controlled broker/tool contracts.

Candidate local hardware/resource lanes:

```text
NVIDIA GPU / CUDA / Ollama
Intel GPU.0 / OpenVINO or compatible local inference
NPU / OpenVINO GenAI
CPU deterministic tools
SQLite memory
```

Delegation requirements:

```text
capability manifest entry
input contract
output contract
timeout
resource label
side-effect policy
provider/tool diagnostics
telemetry entry
error/degradation state
no source writes unless explicitly approved
no patch application unless explicitly approved
```

## Intel GPU.0 coworker direction

`GPU.0` can become a coworker lane if OpenVINO sees the Intel integrated GPU and a compatible model/task is available.

Good first uses:

```text
embedding batch worker
small classifier
candidate-ranking model
vision/screenshot probe when explicitly scoped
batch similarity scoring
lightweight local inference that should not occupy the NVIDIA GPU
```

Not first uses:

```text
primary LLM planner
patch planner
source writer
implicit AUTO selection including NPU without policy
Blender/FFmpeg runtime
```

## Can GPU0 be activated immediately?

Operational answer:

```text
Yes for detection, capability reporting and report-only probe.
No for autonomous coworker delegation until provider/broker contracts are added.
```

Safe immediate activation:

```text
query OpenVINO available devices
record CPU/GPU.0/NPU availability in capability manifest
run a no-source-write smoke/probe on GPU.0 with a tiny compatible model if already available
include GPU.0 status in telemetry/full toolbox summary
```

Required before real coworker use:

```text
GPU0 worker request/response schema
GPU0 task allowlist
runtime broker routing policy
timeout/degradation policy
telemetry fields
capability manifest extension
validator for GPU0 worker reports
explicit no-source-write guardrail
```

## CSV/index/discovery start-of-run rule

The next run-unica evolution should start with repository visibility surfaces before provider-heavy reasoning.

Start-of-run inventory surfaces:

```text
Markdown inventory JSON/MD
script inventory JSON/CSV/MD
Python line-count CSV/MD
function/class/method inventory CSV when available
repository consistency map/smoke
semantic chunk manifest
selected chunk evidence when useful
auto-discovery report when scanner/index drift is suspected
index repair plan/report when generated indexes are stale or missing
```

Rationale:

```text
The primary AI, NPU helper and GPU0 coworker should reason from current repository visibility, not stale indexes.
CSV/count and discovery/index surfaces give all lanes a shared factual map before recommendations and patch plans.
```
