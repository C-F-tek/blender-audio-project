# Tool Package Family Map - 2026-05-18

This is the post-cleanup source map for `Tools/*` packages. Operators should use
dispatcher commands, not file-path script invocations:

```powershell
python -m ia_carmine.cli <tool>
python -m Tools.validation <tool>
python -m Tools.workflow <tool>
python -m Tools.npu <tool>
python -m Tools.docs <tool>
```

## Canonical Surfaces

| Area | Public surface | Purpose |
|---|---|---|
| `ia_carmine` | `python -m ia_carmine.cli run` | Non-GUI operator product run: task Markdown in, final bundle/patch product out. |
| `Tools.workflow` | `python -m Tools.workflow <tool>` | Human workflow helpers, GUI-adjacent shells, PowerShell-backed operational launchers. |
| `Tools.validation` | `python -m Tools.validation <tool>` | Validators, smokes and gates grouped by contract family. |
| `Tools.npu` | `python -m Tools.npu <tool>` | NPU/Ollama support lanes and context builders. |
| `Tools.docs` | `python -m Tools.docs <tool>` | Documentation hygiene, module promotion and tool-surface audits. |

## Macro Packages

| Area | Macro package | Owns |
|---|---|---|
| `ia_carmine` | `agent_context` | Context packs, semantic chunks, shared toolbox bundles, task context and candidate merge helpers. |
| `ia_carmine` | `agent_memory` | Runtime memory policy, routing, SQLite-backed memory and memory review helpers. |
| `ia_carmine` | `agent_review` | Agent review patch plans, evidence sufficiency, warning policy and decision-loop helpers. |
| `ia_carmine` | `ai_workload` | AI workload quality routing helpers. |
| `ia_carmine` | `code_product` | Code interpreter reports, artifact intake and generated code-product helpers. |
| `ia_carmine` | `deterministic_recommendations` | Deterministic recommendation synthesis and evidence-to-recommendation mapping. |
| `ia_carmine` | `external_heap` | External heap pointers, revision context and postrun package logic. |
| `ia_carmine` | `heap_context_closure` | Runtime heap/context closure orchestration. |
| `ia_carmine` | `heap_context_memory_reload` | Heap startup memory reload and reconciliation logic. |
| `ia_carmine` | `heap_exchange` | Heap exchange entry/exit, closure audit and peer runtime manifests. |
| `ia_carmine` | `heap_final_proposals` | Final heap proposal composition, causality normalization and operator decision artifacts. |
| `ia_carmine` | `heap_gate` | Heap gate prompt/runtime contract support. |
| `ia_carmine` | `heap_provider` | Provider budget and invocation contract helpers. |
| `ia_carmine` | `heap_runtime` | Heap runtime launcher command, code execution, completeness and virtual environment helpers. |
| `ia_carmine` | `operator_product_core` | Shared model/controller/profile core for CLI run and GUI view. |
| `ia_carmine` | `patch_product` | Patch notes, patch plans, task patch suggestions and patch-suggestion bundles. |
| `ia_carmine` | `patchkit` | Deterministic PatchKit bundle application boundary. |
| `ia_carmine` | `pipeline` | Pipeline dry-run matrix, artifact runner, validation step and artifact validation helpers. |
| `ia_carmine` | `provider_mesh` | GPU1/GPU0/NPU provider probes, peers, auditors and provider runtime mesh helpers. |
| `ia_carmine` | `provider_runtime_blackboard` | Provider runtime blackboard, evidence, peer report and broker bridge helpers. |
| `ia_carmine` | `repository_product` | GitHub evidence, repository consistency and review PR product builders. |
| `ia_carmine` | `run` | Canonical non-GUI operator product command. |
| `ia_carmine` | `runtime_tool` | Broker, allowlist execution and runtime tool evidence. |
| `ia_carmine` | `runtime_universe` | Unified chain/launcher patches and universe/observer helpers. |
| `ia_carmine` | `schema_repair` | Provider response schema repair helpers. |
| `Tools.validation` | `agent_context` | Agent-context contract checks and semantic context smokes. |
| `Tools.validation` | `agent_memory` | Agent-memory policy and SQLite/routing smokes. |
| `Tools.validation` | `agent_review` | Agent-review decision loop, patch plan and warning-policy smokes. |
| `Tools.validation` | `code_product` | Code product artifact intake smoke. |
| `Tools.validation` | `deterministic_recommendations` | Deterministic recommendation synthesizer smoke. |
| `Tools.validation` | `ai_workload` | AI workload quality core and smokes. |
| `Tools.validation` | `docs_hygiene` | Markdown and repository hygiene validators. |
| `Tools.validation` | `external_heap` | External heap behavior smokes. |
| `Tools.validation` | `generated_artifacts` | Generated artifact, Blender-script and generated-Python policy checks. |
| `Tools.validation` | `generated_patch_specs` | Patch-spec draft/current-stamp/review-lane checks. |
| `Tools.validation` | `heap_exchange` | Heap exchange lifecycle, closure and peer runtime smokes. |
| `Tools.validation` | `heap_final_proposals` | Final proposal gate and operator decision smokes. |
| `Tools.validation` | `heap_provider` | Provider budget/invocation contract smokes. |
| `Tools.validation` | `heap_runtime` | Heap runtime code execution, completeness and launcher checks. |
| `Tools.validation` | `legacy_blender` | Legacy Blender compatibility checks kept out of current runtime domains. |
| `Tools.validation` | `patch_product` | Patch product separation and patch suggestion smokes. |
| `Tools.validation` | `pipeline` | AI/NPU pipeline report and dry-run matrix checks. |
| `Tools.validation` | `provider_mesh` | GPU/NPU/OpenVINO provider contract smokes. |
| `Tools.validation` | `real_product` | Operator product and real runtime mesh checks. |
| `Tools.validation` | `repository_product` | GitHub/repository/review PR product checks. |
| `Tools.validation` | `runtime_tool` | Runtime broker/tool feedback smokes. |
| `Tools.validation` | `runtime_universe` | Unified run manifest, observer and chain checks. |
| `Tools.validation` | `schema_repair` | Schema repair context/retry smokes. |
| `Tools.validation` | `validation_gate` | Unified validation gate registry and runner. |
| `Tools.validation` | `workflow_run` | Workflow invocation and launcher wiring checks. |
| `Tools.docs` | `docs_hygiene` | Markdown coherence, split guide, root surface audit and package-family audit. |
| `Tools.npu` | `provider_mesh` | NPU context, guardrail, review, Ollama runtime and code chunk helpers. |
| `Tools.workflow` | `workflow_run` | Workflow core, shells, startup checks, audio analysis and scene helpers. |

## Non-Command Support Paths

| Path | Role |
|---|---|
| `ia_carmine/runtime/run/profiles/heap_runtime_launcher_profiles.json` | Runtime profile data owned by the canonical `run` surface. |
| `ia_carmine/_shared/fixtures/` | Shared test/review fixtures; not a public command package. |
| `Tools/npu/context_artifacts/` | Generated local NPU context output; ignored by Git and regenerated by `python -m Tools.npu build_npu_code_context`. |

## Cleanup Evidence

The cleanup is validated by report-only tools:

```powershell
python -m Tools.docs tool_package_family_audit --repo-root . --area ai --area validation --area workflow --area npu --area docs
python -m Tools.docs module_duplication_audit --repo-root . --area ai --area validation --area workflow --area npu --area docs --similarity-threshold 0.55 --fail-on-findings
python -m Tools.docs repo_tool_surface_audit --repo-root . --area ai --area validation --area workflow --area npu --area docs --fail-on-findings
python -m Tools.validation check_python_syntax --repo-root .
```

Expected result after this cleanup:

```text
tool_package_family_audit.finding_count = 0
module_duplication_audit.finding_count = 0 at threshold 0.55
repo_tool_surface_audit has no random Tools/* root-script findings; remaining findings are legacy line-budget items
check_python_syntax.failed_count = 0
```

## Internal Module Consolidation Owners

The second cleanup pass removed module-level clone logic, not only root script
placement noise.

| Shared owner | Replaces repeated logic in |
|---|---|
| `ia_carmine/product/agent_review/cli_output.py` and `report_cli_specs.py` | Agent-review evidence and patch-bundle CLI report wiring. |
| `ia_carmine/product/generated_patch_specs/cli_specs.py` | Generated patch-spec proposal/review CLI boilerplate. |
| `ia_carmine/_shared/evidence_item_planning.py` | Doc/code and doc/doc evidence item normalization used by fallback plans and deterministic recommendations. |
| `ia_carmine/_shared/revision_context_prompt.py` | External heap revision-context prompt rendering for heap closure and launcher command code. |
| `ia_carmine/_shared/report_markdown.py` | Reusable compact report Markdown sections. |
| `Tools/workflow/workflow_run/_shared/artifact_catalog.py` | GUI and shell artifact collection, classification, external-open and size formatting. |
| `ia_carmine/providers/provider_mesh/gpu_npu_parallel_orchestrator/support_lanes.py` | Common GPU0/NPU peer support launch, harvest, runtime event and diagnostic plumbing. |

Validation evidence for this pass:

```text
module_duplication_audit_threshold_055_final.json: passed=true, finding_count=0
check_python_syntax_after_module_cleanup.json: passed=true, failed_count=0
tool_package_family_audit_after_module_cleanup.json: passed=true, finding_count=0
```

## Macro-Move Evidence

The third cleanup pass removed immediate micro-package strata from `ia_carmine`,
`Tools.validation` and `Tools.docs`; the public command names remain dispatcher
aliases.

```text
tool_root_inventory_after_macro_moves.json: package_count=82, root_script_entrypoint_count=0
tool_package_family_after_macro_moves.json: passed=true, finding_count=0
module_duplication_after_macro_moves.json: passed=true, finding_count=0
check_python_syntax_after_macro_moves.json: passed=true, failed_count=0
```

## Final Support-Path Cleanup

The fourth cleanup pass moved profile/fixture data out of top-level package
slots and removed stale tracked NPU context artifacts.

```text
ia_carmine/runtime/runtime_profiles/* -> ia_carmine/runtime/run/profiles/*
ia_carmine/fixtures/* -> ia_carmine/_shared/fixtures/*
Tools/npu/context_artifacts/* removed from Git tracking and ignored
tool_root_inventory_final_macro_cleanup.json: package_count=70, root_script_entrypoint_count=0
```
