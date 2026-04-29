# AI Smart Policy

This project uses AI as a staged production system, not as a single prompt sink.

## Core principle

Do not solve token limits by making prompts poor. Solve them by decomposing project knowledge into structured, traceable, reusable context artifacts.

## Policy

Every AI-facing workflow should prefer:

1. **Source files**: raw project files, analysis JSON, music context, code index, manuals and scene briefs.
2. **Capsules**: small semantic chunks with path, source, kind, title, priority, keywords and SHA-256.
3. **Packets**: ranked task-specific selections of capsules.
4. **Manifests**: complete lists of available capsules that can be expanded by `capsule_id`.
5. **Guardrails**: deterministic and NPU-light checks before promoting an artifact.
6. **Repair loops**: if checks fail, create a repair packet and rerun only the failing slice.
7. **Agent state packets**: task-local state that combines selected memory, durable constraints, file references, hardware lane policy and planned microtasks.

## Required generated artifacts

AI phases that build or consume context should produce AI-readable intermediates where practical:

- `*_smart_context_packet.json`
- `*_smart_context_manifest.json`
- `*_smart_context_packet.md`
- `*_guardrail_report.json`
- `*_guardrail_report.md`
- `*_repair_packet.json` when a retry is needed
- `*_promotion_decision.json` when an artifact is accepted or blocked
- `*_agent_state_packet.json` or `agent_state_packet.json` when the app or an agent needs explicit memory and microtask state

## NPU role

The NPU lane is not the main heavy generator. It should be used as an always-available helper where it does not slow the central process:

- preflight OpenVINO/NPU readiness;
- deterministic guardrail scoring;
- capsule packet review;
- repair packet generation;
- schema and blocked-pattern checks;
- future small-model classification/review when the NPU model path is stable.

## GPU / Ollama role

The GPU/Ollama lane can perform expensive generation and synthesis, but should receive smart packets, not raw unlimited context.

When a guardrail fails, the central AI should be asked to repair only the relevant capsule subset or artifact field.

## Blender script boundary

Generated Blender destination scripts should remain clean and production-oriented.

Debugging and guardrail logs belong in workflow tools, `output/workflow_logs`, and AI pipeline reports, not inside final scene scripts unless explicitly requested.

## Promotion rule

An artifact should only be considered ready for the next stage when:

- required files exist;
- schema is readable;
- blocked patterns are absent;
- key Blender constraints are present;
- known Blender 5.x compatibility hazards are absent;
- guardrail report passes or includes an explicit accepted-risk reason;
- if a script is expected, it is non-trivial and contains concrete Blender operations.

## Repair rule

If an artifact fails validation:

1. Write a repair packet describing the exact failure.
2. Reference affected files and capsule ids.
3. Ask the central model for a targeted correction.
4. Re-run validation/guardrail.
5. Repeat up to the configured retry count.

Default maximum repair attempts: `2`.

## Agent state rule

Agent state packets should remain generic. They may describe audio files, Blender packages, documentation, source code, future media types or multiple files at once, but the structure should stay stable:

```text
objective
selected_memory
memory_manifest
microtasks
policy
budgets
assumptions
```

The packet is a planning and awareness artifact. It should not directly run heavy GPU work, NPU inference, Blender renders or source-code rewrites. Those actions must remain explicit pipeline steps or app-controlled tasks.

## Persistent memory rule

Persistent memory may use JSONL for reviewable append-only records or SQLite for faster local lookup. SQLite is preferred as the first local memory database because it requires no external dependency and can live under an app-controlled generated-data folder such as:

```text
indexAI/agent_memory/agent_memory.sqlite
```

External vector databases or embedding stores should remain optional providers until the project has a stable schema for memory records, privacy policy, backup behavior and index regeneration.
