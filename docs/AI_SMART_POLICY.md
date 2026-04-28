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

## Required generated artifacts

AI phases that build or consume context should produce AI-readable intermediates where practical:

- `*_smart_context_packet.json`
- `*_smart_context_manifest.json`
- `*_smart_context_packet.md`
- `*_guardrail_report.json`
- `*_guardrail_report.md`
- `*_repair_packet.json` when a retry is needed
- `*_promotion_decision.json` when an artifact is accepted or blocked

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
