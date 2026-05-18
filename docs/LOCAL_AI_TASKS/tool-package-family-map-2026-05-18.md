# Tool Package Family Map - 2026-05-18

This is the post-cleanup source map for `Tools/*` packages. Operators should use
dispatcher commands, not file-path script invocations:

```powershell
python -m Tools.ai <tool>
python -m Tools.validation <tool>
python -m Tools.workflow <tool>
python -m Tools.npu <tool>
python -m Tools.docs <tool>
```

## Canonical Surfaces

| Area | Public surface | Purpose |
|---|---|---|
| `Tools.ai` | `python -m Tools.ai run` | Non-GUI operator product run: task Markdown in, final bundle/patch product out. |
| `Tools.workflow` | `python -m Tools.workflow <tool>` | Human workflow helpers, GUI-adjacent shells, PowerShell-backed operational launchers. |
| `Tools.validation` | `python -m Tools.validation <tool>` | Validators, smokes and gates grouped by contract family. |
| `Tools.npu` | `python -m Tools.npu <tool>` | NPU/Ollama support lanes and context builders. |
| `Tools.docs` | `python -m Tools.docs <tool>` | Documentation hygiene, module promotion and tool-surface audits. |

## Macro Packages

| Area | Macro package | Owns |
|---|---|---|
| `Tools.ai` | `code_product` | Code interpreter reports, artifact intake and generated code-product helpers. |
| `Tools.ai` | `external_heap` | External heap pointers, revision context and postrun package logic. |
| `Tools.ai` | `patch_product` | Patch notes, patch plans, task patch suggestions and patch-suggestion bundles. |
| `Tools.ai` | `provider_mesh` | GPU1/GPU0/NPU provider probes, peers, auditors and provider runtime mesh helpers. |
| `Tools.ai` | `repository_product` | GitHub evidence, repository consistency and review PR product builders. |
| `Tools.ai` | `runtime_tool` | Broker, allowlist execution and runtime tool telemetry. |
| `Tools.ai` | `runtime_universe` | Unified chain/launcher patches and universe/observer helpers. |
| `Tools.validation` | `ai_workload` | AI workload quality core and smokes. |
| `Tools.validation` | `docs_hygiene` | Markdown and repository hygiene validators. |
| `Tools.validation` | `external_heap` | External heap behavior smokes. |
| `Tools.validation` | `generated_patch_specs` | Patch-spec draft/current-stamp/review-lane checks. |
| `Tools.validation` | `heap_exchange` | Heap exchange lifecycle, closure and peer runtime smokes. |
| `Tools.validation` | `heap_provider` | Provider budget/invocation contract smokes. |
| `Tools.validation` | `heap_runtime` | Heap runtime code execution, completeness and launcher checks. |
| `Tools.validation` | `patch_product` | Patch product separation and patch suggestion smokes. |
| `Tools.validation` | `pipeline` | AI/NPU pipeline report and dry-run matrix checks. |
| `Tools.validation` | `provider_mesh` | GPU/NPU/OpenVINO provider contract smokes. |
| `Tools.validation` | `real_product` | Operator product and real runtime mesh checks. |
| `Tools.validation` | `repository_product` | GitHub/repository/review PR product checks. |
| `Tools.validation` | `runtime_tool` | Runtime broker/tool feedback smokes. |
| `Tools.validation` | `runtime_universe` | Unified run manifest, observer and chain checks. |
| `Tools.validation` | `schema_repair` | Schema repair context/retry smokes. |
| `Tools.validation` | `workflow_run` | Workflow invocation and launcher wiring checks. |
| `Tools.docs` | `docs_hygiene` | Markdown coherence, split guide, root surface audit and package-family audit. |
| `Tools.npu` | `provider_mesh` | NPU context, guardrail, review, Ollama runtime and code chunk helpers. |
| `Tools.workflow` | `workflow_run` | Workflow core, shells, startup checks, audio analysis and scene helpers. |

## Cleanup Evidence

The cleanup is validated by report-only tools:

```powershell
python -m Tools.docs tool_package_family_audit --repo-root . --area ai --area validation --area workflow --area npu --area docs
python -m Tools.docs module_duplication_audit --repo-root . --area ai --area validation --area workflow --area npu --area docs --fail-on-findings
python -m Tools.docs repo_tool_surface_audit --repo-root . --area ai --area validation --area workflow --area npu --area docs --fail-on-findings
python -m Tools.validation check_python_syntax --repo-root .
```

Expected result after this cleanup:

```text
tool_package_family_audit.finding_count = 0
module_duplication_audit.finding_count = 0
repo_tool_surface_audit.finding_count = 0
check_python_syntax.failed_count = 0
```
