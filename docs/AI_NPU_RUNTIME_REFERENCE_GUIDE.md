# AI NPU Runtime Reference Guide

## Purpose

This guide explains how NPU, OpenVINO-style local inference and runtime fallback concepts should be applied inside this repository.

It is a project-specific guide for AI agents. It does not replace upstream OpenVINO or hardware documentation.

## Current project policy

`Tools/npu/pipeline/` is currently an app-agnostic helper package under staged decomposition.

Until a later validated phase explicitly changes this, AI agents must treat it as:

```text
provider-free
runtime-free
safe to import
focused on contracts, paths, config, IO and planning helpers
```

It must not be wired into runtime orchestrators unless local validation and regenerated indexes are green.

## Hardware role separation

Recommended local strategy:

| Device | Preferred project role |
|---|---|
| NPU | Lightweight local inference, compact review, creative proposal, low-power helper generation. |
| GPU | Blender rendering, heavy graphics/AI acceleration, image/video workloads. |
| CPU | Orchestration, validation, JSON/schema processing, fallback inference, FFmpeg CPU encoding. |

This separation prevents local inference experiments from blocking Blender rendering or corrupting validated pipeline behavior.

## Runtime-agnostic NPU design

NPU-related helpers should not assume one fixed provider. They should describe capability and intent.

Preferred abstraction:

```text
NpuCapability
  -> ProviderDescriptor
  -> StagePlan
  -> InputBundle
  -> ProviderResult
  -> ValidationReport
```

The helper layer may prepare:

- config objects;
- path plans;
- compact context bundles;
- provider descriptors;
- validation contracts;
- report stubs;
- migration-readiness reports.

The helper layer should not perform actual inference unless a specific runtime module is introduced and validated.

## Safe NPU helper scope

Allowed in helper modules:

- pure path helpers;
- JSON/text IO helpers;
- artifact path planning;
- context bundle creation;
- contract validation;
- provider descriptors;
- dry-run stage reports;
- fixture-based tests;
- migration-readiness gates.

Not allowed without explicit validated phase:

- direct NPU inference calls;
- direct Ollama calls;
- direct Blender runtime modification;
- automatic provider fallback that hides failures;
- writing source files from model output;
- changing `Tools/npu/run_dual_ai_pipeline.py` behavior without local validation.

## Expected NPU workflow

```text
1. build compact project context
2. prepare input bundle
3. select planned provider descriptor
4. run provider or dry-run outside helper contracts
5. normalize provider output
6. validate structured artifact
7. write safe output report
8. regenerate indexes after accepted structural changes
```

## Failure handling

NPU failures must be explicit.

Recommended report fields:

```text
status
stage
provider
device
error
fallback_used
artifact_written
validation_status
```

Do not convert NPU failure into a successful creative artifact unless the fallback provider actually produced a validated artifact and the report states that fallback was used.

## Integration with existing docs

For NPU helper work, read:

```text
AGENTS.md
WORKFLOW.md
docs/README.md
Tools/npu/pipeline/README.md
docs/AI_PIPELINE_ARCHITECTURE.md
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md
docs/AI_GUARDRAILS_VALIDATION_GUIDE.md
```

## Validation commands

Focused NPU helper workflow:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1
```

Individual checks:

```powershell
python .\Tools\validation\check_npu_pipeline_modules.py --repo-root . --output .\output\validation\npu_pipeline_modules.json
python .\Tools\validation\check_npu_pipeline_helper_tests.py --repo-root . --output .\output\validation\npu_pipeline_helper_tests.json
python .\Tools\validation\check_npu_pipeline_docs.py --repo-root . --output .\output\validation\npu_pipeline_docs.json
```

General syntax and package checks:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
python .\Tools\validation\check_package_structure.py --repo-root . --output .\output\validation\package_structure.json
```

## Migration readiness checklist

Before wiring NPU helpers into runtime code, require:

- helper docs updated;
- helper validators passing;
- fixture or dry-run reports available;
- provider boundary documented;
- fallback behavior documented;
- generated indexes regenerated;
- no Blender runtime behavior changed unintentionally;
- no source writes from raw model output;
- maintainer approval for runtime wiring.

## Practical advice for AI agents

When asked to improve NPU usage:

1. inspect current helper contracts first;
2. avoid editing runtime orchestrators immediately;
3. add or refine pure helpers;
4. add validation before integration;
5. document provider boundary;
6. keep GPU free for Blender unless the task explicitly targets GPU AI;
7. state when local hardware validation is required.
