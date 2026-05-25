# IA-Carmine Coherence Guardrails

## Objective

Keep IA-Carmine source, dispatcher surfaces, runtime contracts, validation names
and documentation claims aligned. These guardrails are code-driven: dispatcher
registries and current source are checked before historical runbooks or old
handoffs are trusted.

## Contracts Read

This guardrail pass is grounded in:

```text
docs/CURRENT_RUNTIME_MARKDOWN_CONTRACT.md
docs/CORE_LANE_COMPLETENESS_CONTRACT.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
docs/DISPATCHER_CONTEXT_COVERAGE.md
docs/CONTEXT_COVERAGE_STATUS.md
docs/architecture/core_out_of_tools_refactor.md
docs/architecture/tools_core_refactor_map.md
ia_carmine/dispatch.py
Tools/validation/dispatch.py
Tools/workflow/dispatch.py
Tools/npu/dispatch.py
Tools/docs/dispatch.py
Tools/git/dispatch.py
Tools/repo_patch_runner/dispatch.py
```

## Core And Tools Boundary

`ia_carmine` owns the canonical runtime, product, provider, context, memory and
dispatcher core. `Tools` remains compatibility, validation, workflow,
documentation, Git and operator utility surface.

Rules:

- Core runtime must not depend on `Tools` implementation modules.
- Reusable dispatch logic lives in `ia_carmine._shared.tool_dispatch`.
- `Tools.*` dispatchers import `ToolDispatcher` directly from the core helper.
- Generic report helpers used by `ia_carmine` live in
  `ia_carmine._shared.report_io`; `Tools.validation._shared.report_utils`
  remains a validation-surface helper only.
- Shared patch-runner logic used by core review code lives in
  `ia_carmine._shared.apply_repo_mods`; `Tools.repo_patch_runner` remains the
  public command surface.
- The boundary check rejects both direct imports and dynamic string imports
  such as `importlib.import_module("Tools...")` from `ia_carmine`.

Validator:

```powershell
python -m Tools.validation check_ia_carmine_tools_boundary --repo-root .
```

## Dispatcher Source Of Truth

Public tool availability is derived from dispatcher registries, not arbitrary
files:

```text
ia_carmine.dispatch
Tools.validation.dispatch
Tools.workflow.dispatch
Tools.npu.dispatch
Tools.docs.dispatch
Tools.git.dispatch
Tools.repo_patch_runner.dispatch
```

Every Python target must resolve as `module:function` and the function must be
callable. PowerShell targets are checked as files and not executed.

Validator:

```powershell
python -m Tools.validation check_dispatcher_targets --repo-root . --all
```

## Context Coverage Rule

Dispatcher macro-families need orientation coverage through nearest
`TOOL_CONTEXT.md`, area `CONTEXT_INDEX.md`, or the central coverage documents.
Partial/stub coverage is allowed only as a visible warning; missing dispatcher
family coverage is not silent.

Validator:

```powershell
python -m Tools.validation check_dispatcher_context_coverage --repo-root .
```

## Full And Complete Claims

`full`, `complete`, `ready` and `product ready` wording is risky unless the
report names the concrete evidence. A complete/full claim must preserve the
semantic perimeter from request input through startup, heap/exchange, provider
lanes, tool/broker evidence, CPU validators and product boundary. `degraded` is
not success for complete/full run modes selected by explicit CLI flags.

Validator:

```powershell
python -m Tools.validation check_full_complete_wording_contract --repo-root .
```

## Validation Set

Run these before claiming coherence for this guardrail layer:

```powershell
python -m Tools.validation check_ia_carmine_tools_boundary --repo-root .
python -m Tools.validation check_dispatcher_targets --repo-root . --all
python -m Tools.validation check_dispatcher_context_coverage --repo-root .
python -m Tools.validation check_full_complete_wording_contract --repo-root .
python -m Tools.validation check_python_syntax --repo-root .
git diff --check
```

These checks do not run providers, apply patches, launch Blender/FFmpeg or write
source. Their reports are validation evidence, not product success.
