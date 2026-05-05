<!-- IA-CARMINE-MD-SPLIT: part -->
# QUALITY_GATE — parte 002 di 002

Sorgente indice: [`../QUALITY_GATE.md`](../QUALITY_GATE.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)

## Runtime telemetry/capability checklist

For run-unica, provider, broker, recommendation or patch-plan handoff, inspect or provide:

```text
runtime_tool_usage_telemetry_<STAMP>.json/md
runtime_tool_capability_manifest_<STAMP>.json/md
full_toolbox_run_telemetry_summary_<STAMP>.json/md
shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
```

Minimum semantics to verify:

```text
tool_call_entry_count
executed_count
failed_count
blocked_count
broker_reports
provider_advisory_state
provider_failure_reasons
degraded_provider_components
deterministic_recovery_used
gpu_metrics_source
round_duration_source
patch_application_performed
source_writes_performed
```

## Discovery/index/CSV-count checklist

For refactor/reuse, repository-wide visibility, documentation cleanup or run-unica handoff, inspect or provide relevant surfaces:

```text
Markdown inventory JSON/MD
script inventory JSON/CSV/MD
Python line-count CSV/MD
function/class/method inventory CSV
semantic chunk manifest JSON/MD
selected chunk evidence JSON/MD
repository consistency map/smoke JSON/MD
auto-discovery report
index repair plan/report
```

Minimum semantics to verify:

```text
provider_execution_performed=false for pure inventory/count/report lanes
source_writes_performed=false unless explicit apply/regeneration is selected
patch_application_performed=false unless explicit patch apply is selected
output paths stay under ignored output/** unless compact evidence is intentionally promoted
indexAI/code_chunks/** is not commit-ready source
index repair is plan/report-first unless explicitly requested
```

## FFmpeg validation checklist

FFmpeg validation is application-domain work and must be explicitly scoped.

- Frame sequence path is explicit.
- Start frame number is explicit.
- Frame rate is explicit.
- Audio path is explicit.
- Output path is explicit.
- Codec is explicit.
- Pixel format is explicit.
- Color metadata is explicit when publishing to video platforms.
- CPU/GPU profile is documented.

## AI acceptance criteria

An AI-generated change is acceptable only if it includes:

- files changed;
- reason for each change;
- assumptions;
- test status;
- risks;
- follow-up recommendations;
- line counts for created or modified scripts;
- telemetry/capability/final-summary context when it derives from run-unica evidence or patch plans;
- discovery/index/CSV-count context when it derives from refactor/reuse, inventory or repository-wide evidence.

## Non-destructive rule

Do not break known working scripts to improve architecture.

When extracting reusable logic:

1. create shared utility or generic policy first;
2. keep original package unchanged;
3. test the shared utility/policy;
4. use it in new packages or validators first;
5. migrate existing packages only after validation.

## Red flags

Reject or review carefully when a generated change:

- rewrites a large working script without a clear reason;
- removes package-specific documentation;
- hardcodes paths without explanation;
- invents JSON fields;
- assumes application/runtime compatibility without test evidence;
- assumes all generated Python scripts are Blender scripts;
- assumes all input data is WAV/audio;
- uses obsolete Blender APIs such as `ShaderNodeTexMusgrave`;
- opens, saves or quits Blender sessions unexpectedly;
- mixes input analysis, output application control, rendering and encoding in one oversized function;
- deletes generated context or analysis data;
- adds paid or external AI GitHub Actions without explicit opt-in;
- uses prompt-based repair where deterministic parsing is available;
- hardens report schemas so much that additive future fields fail validation;
- claims run-unica Full0To10 success from dry-run, focused validator, provider report, NPU smoke, oversized Markdown or file existence alone;
- presents evidence or patch plans without telemetry/capability/final-summary context when the output derives from run-unica evidence;
- presents refactor/reuse or repository-wide plans without relevant discovery/index/CSV-count context.

## Current reference

`Scripting/v61b/` remains the current reference for richer Blender package structure and visual ambition.

The current generated-file policy reference is:

```text
Tools/validation/generated_file_policy.py
Tools/validation/generated_python_policy.py
Tools/validation/check_generated_python_policy.py
Tools/validation/check_generated_blender_script_policy.py
```

The current report-contract validator reference is:

```text
Tools/validation/check_ai_dry_run_matrix_contract.py
```

The current run-unica telemetry/handoff reference is:

```text
Tools/ai/build_runtime_tool_usage_telemetry.py
Tools/ai/build_runtime_tool_capability_manifest.py
Tools/ai/build_full_toolbox_run_telemetry_summary.py
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py
```

The generated-file policy architecture is intended to outgrow Blender and audio/WAV inputs through small, validated adapters.
