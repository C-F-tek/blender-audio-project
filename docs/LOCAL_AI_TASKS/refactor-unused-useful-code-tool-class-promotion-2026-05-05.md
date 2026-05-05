# IA-Carmine — Run unica refactor unused/useful code + tool/class promotion

## Scope

Repository: C-F-tek/blender-audio-project
Branch: codex/unified-local-ai-refactor-launcher
Mode: review-only
Patch application: forbidden
Source writes: forbidden unless explicitly requested later
Runtime media: forbidden

## Doctrine

run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = presets or operator parameters, not scope
-No* flags = explicit opt-out from selected lanes
CSV/index/discovery surfaces are evidence lanes when relevant
large Markdown must not be a primary operational entrypoint

## Objective

Perform a whole-repository refactor intelligence run to identify:

1. unused but useful code;
2. dead-code candidates;
3. reusable functions/methods/classes;
4. superclass/base-class/mixin opportunities;
5. helper extraction candidates;
6. project tool promotion candidates;
7. broker-safe tool promotion candidates;
8. run-unica lane promotion candidates;
9. documentation drift caused by obsolete code references;
10. generated/index/evidence material that must not be treated as source.

## Required analysis surfaces

Use and cross-check:

- Markdown inventory;
- script inventory;
- Python line-count CSV/MD;
- function/class/method inventory CSV;
- repository consistency map;
- repository consistency smoke;
- semantic chunk manifest;
- selected chunk evidence;
- auto-discovery/index drift evidence;
- index repair plan/report if relevant;
- runtime tool usage telemetry;
- runtime tool capability manifest;
- full toolbox telemetry summary;
- shared AI-to-AI bundle;
- provider diagnostics;
- workload quality report.

## Classification labels

Classify recommendations and patch plans into:

PROMOTE_TO_PROJECT_TOOL
PROMOTE_TO_BROKER_TOOL
PROMOTE_TO_RUN_UNICA_LANE
EXTRACT_SHARED_HELPER
EXTRACT_BASE_CLASS_OR_MIXIN
KEEP_APP_DOMAIN
KEEP_HISTORICAL_SUPPORTING
DEPRECATE_DOC_ONLY
DEAD_CODE_CANDIDATE
UNUSED_BUT_USEFUL
GENERATED_DO_NOT_TOUCH
LOCAL_VALIDATION_REQUIRED
BLENDER_RUNTIME_REQUIRED
PROVIDER_VALIDATION_REQUIRED
DEFER
DO_NOT_PROMOTE

## Priority areas

Inspect especially:

Tools/workflow/**
Tools/ai/**
Tools/ai/pipeline/**
Tools/validation/**
Tools/npu/**
Tools/npu/pipeline/**
docs/**
CHATGPT/**
Scripting/shared/**
Scripting/v61b/**
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/**
root-level tools:
  analyze_wav.py
  build_track_summary.py
  normalize_scene_spec.py

## Guardrails

Do not apply patches automatically.
Do not delete files.
Do not rewrite history.
Do not force-push.
Do not merge to master.
Do not run Blender runtime.
Do not run FFmpeg runtime.
Do not produce audio/video/media output.
Do not commit output/**.
Do not commit indexAI/code_chunks/**.
Do not commit *.db / *.sqlite / *.sqlite3.
Do not treat generated indexes as source.
Do not treat large Markdown as primary operational entrypoint.

## Required output

Produce review-only outputs:

1. executive summary;
2. tool/class/helper promotion matrix;
3. unused-but-useful code inventory;
4. dead-code candidate inventory with confidence;
5. duplicate function/method/class clusters;
6. project-tool promotion candidates;
7. broker-tool promotion candidates;
8. run-unica lane candidates;
9. MD/code drift findings;
10. safe mechanical patch candidates;
11. manual-review refactor candidates;
12. validation plan;
13. patch plan review-only;
14. evidence/telemetry completeness report.

## Patch plan requirements

Every patch-plan item must include:

- target file;
- category label;
- evidence source;
- rationale;
- risk;
- validation minimum;
- whether source write is required later;
- whether provider validation is required;
- whether Blender runtime validation is required;
- why it does not touch forbidden runtime/generated paths.

