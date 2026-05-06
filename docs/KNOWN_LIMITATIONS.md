# Known Limitations

## Status

Active limitation and technical-risk backlog.

This file tracks current architectural, operational and application-domain limits so they can be measured, challenged and progressively overcome.

It must not be used to avoid tool usage. IA-Carmine policy is **TUTTO SU TUTTO**: use every available and relevant tool lane unless a current validator, manifest, telemetry report, provider diagnostic or explicit operator flag blocks it.

## Tool usage rule

```text
Use the full toolbox by default.
Do not treat historical tool-limitation notes as a reason to skip a tool.
A tool/capability is unavailable only when current code/evidence says so.
Record unavailable/degraded lanes in telemetry, capability manifests or validation reports.
Keep limitations visible as an overcome backlog, not as a static prohibition list.
```

Current sources of truth for tool/capability status:

```text
source code
AGENTS.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
runtime tool usage telemetry
runtime capability manifests
provider diagnostics
validator reports
repository consistency map/smoke
```

## Current architectural limitations to overcome

```text
Some legacy docs still describe pre-unified workflows or stale tool assumptions.
Some large docs and source files still exceed the 400-line maintainability policy.
Some evidence branches can become too large or diverge from master before review.
Repository-consistency findings can still be noisy and need classification.
Provider-declared runtime tool requests are not yet fully equivalent to broker-executed feedback unless evidence proves execution.
GPU timing can be degraded when reports infer per-round timing from aggregate elapsed time.
NPU is intentionally a probe/guardrail/decode diagnostic lane, not primary advisory.
```

## Current application-domain limitations to overcome

These remain valid mainly for Blender/audio/media work:

```text
Blender version compatibility must be verified per active script/API surface.
External Python dependencies need explicit bootstrap/validation when used locally.
Input JSON schemas need maintained contracts for application-domain pipelines.
Automated tests and smoke coverage should be expanded.
Release process and reproducible examples need stronger documentation.
Local absolute paths can reduce portability.
Large generated files may not be suitable for Git.
Audio analysis data may be too large for manual review.
Rendering results may vary between GPU, CPU, codecs and platforms.
```

## Obsolete interpretation

The obsolete pattern is not "documenting a limitation". The obsolete pattern is using old limitation notes to avoid current tool usage.

Correct interpretation:

```text
limitation documented -> backlog item to overcome
current validator failure -> current blocker/degraded state
current capability manifest unavailable -> current unavailable state
historical note saying no tool access -> obsolete unless current evidence confirms it
```

## Recommended improvements

```text
Convert stale limitation notes into measurable validators or manifests.
Promote recurring limitations into explicit TECH_DEBT_TRACKER items.
Add current evidence links when a limitation is observed.
Prefer report-only checks before destructive changes.
Keep Full0To10 lanes enabled unless explicitly disabled or diagnosed unavailable.
```
