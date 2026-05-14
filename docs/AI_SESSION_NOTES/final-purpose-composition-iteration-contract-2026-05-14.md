# Final Purpose Composition - Iteration Contract - 2026-05-14

## Purpose

This piece tells GPU1, GPU0, NPU and deterministic validators how to continue
from already written final-purpose chunks. It exists because the prior heap run
proved that a single GPU1 answer can become too thin or can drift into fake
paths.

## Contract For GPU1

GPU1 may iterate on pieces that already exist.

Allowed iteration:

- Re-open a prior proposal chunk when it has a valid target but lacks depth.
- Extend it with exact repo-relative files.
- Add concrete implementation steps.
- Add acceptance criteria.
- Add validation commands.
- Add risk and rollback notes.
- Add package boundaries so the operator can decide what to apply.
- Cite the prior chunk, revision id, or document path being refined.

Forbidden iteration:

- Do not invent `tools/.../real_existing_file.py`.
- Do not use angle-bracket placeholders such as `<id-or-empty>`.
- Do not turn generated evidence files into maintained source targets.
- Do not repeat a rejected chunk as a paraphrase.
- Do not reset to a generic overview when the task asks for a composed final
  decision.

## Pointer Actions

Each new GPU1 revision should declare one of these actions:

- `STAY_FORWARD`: adds detail to the current valid chunk.
- `BACKTRACK_PROPAGATE`: revisits an older chunk to propagate symbols, CLI flags,
  docs links, imports, validation commands, or package boundaries.
- `RESUME_FORWARD`: resumes after a backtrack and updates the final package.
- `SPLIT_TASKS`: decomposes a large package into smaller apply decisions.
- `NO_PATCHABLE_TARGET`: no verified repo target exists.

## Richness Ladder

A proposal is too thin when it only says what should change.

A proposal becomes operator-grade when it includes:

- target files;
- exact reason the change is needed;
- concrete edit plan;
- affected runtime or docs surface;
- validation commands;
- expected line-count effects;
- known blockers;
- apply order;
- rollback or skip decision.

## GPU0 Role

GPU0 should review whether the enriched chunk is more concrete than the previous
one.

It should reject when:

- target files are missing;
- the patch sketch is generic;
- validation commands are absent;
- the proposal repeats a prior rejected response;
- source paths are fake, generated-only, or outside the intended package.

## NPU Role

NPU should remain a bounded audit lane.

It should flag:

- placeholders;
- guardrail violations;
- missing path evidence;
- package scope creep;
- unsafe source-write assumptions.

## Deterministic Exit

The final package is acceptable only when deterministic checks can say:

- the candidate is tied to real repo files;
- fake or placeholder paths are blocked;
- package boundaries are explicit;
- acceptance checks are runnable or clearly marked missing;
- generated evidence is not treated as source.
