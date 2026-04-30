# AI Onboarding

## Purpose

This file is the first-session guide for AI agents entering `blender-audio-project`.

Use it to quickly understand what is source-of-truth, what is generated context, what is safe to touch, and how to avoid damaging working Blender workflows.

## Source-of-truth order

Use this priority when documents disagree:

1. `AGENTS.md` for repository rules, safety limits and required validation.
2. This file for first-session orientation.
3. `README.md` and `docs/PROJECT_AI_CONSCIOUSNESS.md` for current project posture.
4. `docs/MODULE_MAP.md`, `docs/DATA_FLOW.md` and `docs/REFACTORING_AND_REUSE_PLAN.md` for architecture and migration direction.
5. The README nearest to the target package or tool.
6. The target source file itself.
7. Generated indexes under `indexAI/` and `Tools/npu/*_index.md` as derived context only.

If a status document says a file is missing but the file exists, treat the file tree as current evidence and update the stale document in a small documentation patch.

## Current baseline

As of 2026-04-30:

| Area | Baseline |
|---|---|
| `Scripting/v61b/` | Stable reference package. Do not destructively refactor. |
| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/` | Usable standalone package, still monolithic. |
| `Scripting/shared/` | Initial package-agnostic utilities exist: path, JSON, image sequence, FFmpeg command building and render profiles. |
| `Tools/validation/` | Lightweight non-invasive validators exist, including NPU helper smoke/unit/docs validators on active NPU decomposition branches. |
| `Tools/npu/` | Active AI/NPU/Ollama context and review tooling, with large orchestrators still needing staged decomposition. |
| `Tools/npu/pipeline/` | Additive app-agnostic helper package exists on the NPU decomposition branch; it is not wired into the runtime orchestrator until local validation and index regeneration pass. |
| `indexAI/` | Generated AI context. Regenerate after structural or documentation changes; do not hand-refactor as source. |
| JSON schemas | Documented as partial. Preserve unknown fields and avoid destructive normalization. |

Not yet complete:

```text
Scripting/shared/blender_compat.py
Scripting/shared/config_model.py
Scripting/shared/diagnostics.py
runtime adoption of Tools/npu/pipeline/ helpers inside Tools/npu/run_dual_ai_pipeline.py
full production JSON schemas
automated Blender runtime validation
```

## First-session checklist

Run only lightweight inspection first:

```powershell
git status --short
git remote -v
Get-ChildItem -File .\docs
Get-ChildItem -Directory .\Scripting
Get-ChildItem -File .\Scripting\shared
```

Before code changes, run the smallest relevant validation:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
```

For NPU helper work, run the focused helper validation before the full runner:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1
```

For documentation-only changes, a path/link review and `git diff` may be enough unless generated indexes must be refreshed.

## Common traps

- Do not assume every status document is current; compare it with the actual file tree.
- Do not treat `indexAI/` as source code. It is generated context.
- Do not overwrite full frame-by-frame analysis JSON files.
- Do not rewrite `Scripting/v61b/main_v61b.py` to improve architecture.
- Do not split the Ready To Jazz package before shared infrastructure and adapters are validated.
- Do not push patch specs that trigger GitHub Actions without explicit human approval.
- Do not add dependencies, CI changes, long Blender renders or GPU-heavy jobs without explicit approval.
- Do not assume Blender version compatibility unless it is documented or tested; mark it `not specified`.
- Do not wire `Tools/npu/pipeline/` helpers into `Tools/npu/run_dual_ai_pipeline.py` until local validation, index regeneration and migration readiness gates are green.

## Task routing

| Task type | Preferred first move |
|---|---|
| Documentation clarity | Patch docs directly, keep edits small, update `docs/README.md` if adding a stable doc. |
| Shared utility extraction | Add package-agnostic module first, validate without Blender, then consider adapters. |
| v61b runtime issue | Read `Scripting/v61b/README.md` and target source; patch one concern only. |
| New generated package | Start from `Scripting/_template_audio_reactive_package/` and `docs/QUALITY_GATE.md`. |
| NPU/AI pipeline refactor | Split provider, prompt, validation and artifact-writing concerns without changing CLI behavior. |
| NPU helper package work | Keep helpers app-agnostic, run focused helper validation, and defer runtime wiring to a later proven phase. |
| GitHub or parallel AI work | Inspect local git state first; coordinate branch or PR scope before changing overlapping files. |

## Reporting template

Every implementation response should include:

```text
changed files
purpose
line counts for created or modified scripts
assumptions
validation commands and results
risks
recommended next step
```

For documentation-only changes, script line counts can be reported as `not applicable`.
