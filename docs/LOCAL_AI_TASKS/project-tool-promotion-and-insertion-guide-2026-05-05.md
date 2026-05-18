# IA-Carmine project tool promotion and insertion guide — 2026-05-05

Repository: `C-F-tek/blender-audio-project`

Branch: `codex/unified-local-ai-refactor-launcher`

## Purpose

This guide defines how to insert a new tool into the current IA-Carmine tooling system and how to promote an existing script to a documented project tool.

A tool may live outside `Tools/**`. Promotion is based on contract, safety and integration level, not only on folder path.

## Tool lifecycle

### Level 0 — discovered script

A file looks executable or operational but has no stable project-tool contract.

Discovery signals:

    argparse.ArgumentParser
    if __name__ == "__main__"
    PowerShell param(...)
    shebang
    run_*, check_*, build_*, validate_*, encode_*, analyze_*, *_smoke.py
    root-level Python entrypoint
    Scripting/** runtime entrypoint
    GUI/wrapper script

Required action:

    classify placement and safety before promotion.

### Level 1 — documented candidate

Minimum documentation exists:

    purpose
    path
    owner lane
    inputs
    outputs
    guardrails
    manual/broker/full-run eligibility

### Level 2 — project tool

Requirements:

    stable CLI or PowerShell parameter contract
    deterministic return code policy
    JSON report output where applicable
    Markdown report output when human review is expected
    repo-root aware path handling
    output path configurable by CLI
    no hardcoded local user path unless explicitly documented
    validation command documented
    examples documented

### Level 3 — broker tool

Additional requirements:

    safe for `Tools/ai/agent_runtime_tool_broker.py`
    no free shell
    no provider execution unless explicitly designated diagnostic and safe
    no patch application
    no Git write
    no Blender runtime
    no FFmpeg runtime
    no source writes except reports under output/**
    no persistent SQLite write unless guarded by explicit confirm/policy
    all accepted args must be allowlisted

### Level 4 — full-run lane

Additional requirements:

    invoked by workflow or broker bootstrap
    telemetry produced
    included or referenced in production bundle
    validation included in full-run acceptance
    failure class explicit and schema-valid

## Placement decision tree

### 1. Is it runtime/rendering/audio production code?

Examples:

    Tools/workflow/audio_analysis/analyze_cli.py
    Tools/workflow/audio_analysis/summary_cli.py
    Scripting/v61b/main_v61b.py
    Scripting/v61b/encode_image_sequence_v61b.py
    Scripting/v61b/encode_ffmpeg_v61b.py

Placement:

    BLENDER_AUDIO_PIPELINE

Promotion:

    project tool: yes
    broker tool: no by default
    full-run evidence: only via static inventory/diagnostic, not execution

Reason:

    These can touch Blender, FFmpeg, audio files, renders or local workstation resources.

### 2. Is it report-only validation or inventory?

Examples:

    Tools/validation/check_python_syntax.py
    Tools/validation/build_python_line_count_csv.py
    Tools/validation/check_validation_report_contract.py
    Tools/validation/build_markdown_inventory.py
    Tools/validation/check_docs_links.py

Placement:

    FULL_RUN_EVIDENCE / DOCS_MAINTENANCE / VALIDATION

Promotion:

    project tool: yes
    broker tool: yes if no writes outside output/**
    full-run lane: yes if useful every run

### 3. Is it provider/NPU/GPU diagnostic?

Examples:

    Tools/ai/run_local_provider_probe.py
    Tools/ai/check_local_resource_lanes.py
    Tools/validation/check_ai_workload_report_quality.py
    Tools/validation/run_orchestrator_gpu_runtime_tool_routing_smoke.py

Placement:

    PROVIDER_DIAGNOSTIC

Promotion:

    project tool: yes
    broker tool: only if no actual provider execution or safe smoke-only
    full-run lane: yes for report-only diagnostics

### 4. Is it patch-plan/code-edit planning?

Examples:

    Tools/ai/agent_review/patch_plan/cli.py
    Tools/ai/agent_review/code_patch_plan_cli.py
    Tools/ai/code_product/edit_proposal_from_plan/cli.py
    Tools/ai/code_product/patch_artifact_pack/cli.py

Placement:

    PATCH_PLAN_SUPPORT

Promotion:

    project tool: yes
    broker tool: only if proposal/report-only
    full-run lane: yes

### 5. Can it write Git, push, delete, merge, apply patches or change permissions?

Examples:

    python -m Tools.workflow workflow_shell_with_push
    python -m Tools.workflow git_auto_push
    python -m Tools.git auto_push_generated_data
    python -m Tools.git auto_push_generated_artifacts

Placement:

    GIT_WRITE_TOOL / LOCAL_UI_OR_MANUAL

Promotion:

    project tool: maybe manual-only
    broker tool: no
    full-run lane: no unattended execution

## New tool insertion checklist

### A. Choose canonical path

Preferred paths:

    Tools/validation/<tool>.py       report-only checks and validators
    Tools/ai/<tool>.py               AI evidence, planning, broker, context, telemetry
    Tools/workflow/<tool>.ps1        orchestration wrappers
    Tools/workflow/<tool>.py         workflow helpers
    Tools/npu/<tool>.py              NPU/provider-specific tooling
    Scripting/v61b/<tool>.py         Blender/audio runtime helpers

Do not add new root-level tool entrypoints; user-facing tools should live under `Tools/workflow/`, `Tools/ai/`, `Tools/validation/`, `Tools/npu/` or `Scripting/` according to ownership.

### B. Define CLI contract

Python tools should use `argparse` and support:

    --repo-root .
    --output <json path>
    --markdown-output <md path> where useful

PowerShell tools should use `param(...)` and avoid implicit global state.

### C. Define report contract

JSON report should include at minimum:

    schema_version
    kind
    repo_root
    passed
    errors
    warnings
    provider_execution_performed
    patch_application_performed
    source_writes_performed

Recommended extras:

    generated_at
    inputs
    outputs
    checks
    decision
    guardrails

### D. Guardrails

For broker/full-run eligibility, assert these explicitly:

    provider_execution_performed = false unless diagnostic actually executed provider
    patch_application_performed = false
    source_writes_performed = false
    git_write_performed = false
    blender_runtime_touched = false
    ffmpeg_runtime_touched = false
    sqlite_write_performed = false unless explicitly policy-approved

### E. Markdown report

Human-facing tools should write a compact MD report with:

    title
    passed
    error/warning summary
    key decisions
    produced artifacts
    next action

### F. Add validation

At minimum:

    python -m py_compile <tool>.py

If the tool emits JSON reports, validate with:

    python -m Tools.validation check_validation_report_contract --repo-root . --report-file <report> --output <contract-report>

If it becomes workflow-critical, add a smoke under:

    Tools/validation/run_<tool>_smoke.py

### G. Add documentation

Update one or more:

    docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
    docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
    docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md
    FULL_RUN_UNICA_TUTTO_SU_TUTTO.md
    CHATGPT/README.md if it affects handoff/discovery

### H. Broker insertion only if safe

To add to `Tools/ai/agent_runtime_tool_broker.py`:

    1. add builder function;
    2. add ToolSpec entry;
    3. allow only explicit args;
    4. ensure command writes only report artifacts under output/**;
    5. ensure result guardrails do not allow provider/Git/Blender/patch side effects;
    6. update runtime capability manifest expectations;
    7. add/adjust smoke validation.

Required broker acceptance:

    runtime_tool_usage_telemetry_<STAMP>.json:
      inputs.broker_reports.Count >= 1
      summary.executed_count includes the new tool if it is part of bootstrap/full-run lane
      failed_count = 0
      blocked_count = 0

## Example: adding a report-only validation tool

Target path:

```text
Tools/validation/<new_contract_validator>
```

The exact filename must be created in the same PR before executable examples use it. Until then, keep this as a placeholder contract, not a runnable command.

CLI pattern after the file exists:

```text
python <tracked validation tool> --repo-root . --output output/validation/example_contract.json --markdown-output output/validation/example_contract.md
```

Broker ID:

```text
check_example_contract
```

Broker builder pattern:

```python
def check_example_contract(repo_root, out_dir, request_id, args):
    report = out_dir / f"{request_id}_example_contract.json"
    markdown = out_dir / f"{request_id}_example_contract.md"
    command = [sys.executable, "<tracked validation tool>", "--repo-root", ".", "--output", str(report), "--markdown-output", str(markdown)]
    return command, {"json_report": repo_rel(report, repo_root), "markdown_report": repo_rel(markdown, repo_root)}
```

ToolSpec pattern:

```python
"check_example_contract": ToolSpec(
    name="check_example_contract",
    description="Validate example contract as report-only runtime tool.",
    allowed_args=(),
    builder=check_example_contract,
)
```

Validation after the concrete file exists:

```text
python -m py_compile <tracked validation tool> Tools/ai/agent_runtime_tool_broker.py
```

## Example: promoting the workflow audio analyzer

Path:

    Tools/workflow/audio_analysis/analyze_cli.py

Placement:

    BLENDER_AUDIO_PIPELINE

Promotion:

    Level 2 project tool, not broker.

Required docs:

    purpose: audio WAV analysis for scene generation
    input: WAV path
    output: analysis JSON
    runtime: local audio processing
    broker: no
    full-run: static inventory only

Reason:

    It is a real project tool, but not a report-only broker-safe tool.

## Versioning rule

Every promoted tool must have one of these states documented:

    active
    candidate
    deprecated
    manual-only
    generated-candidate

Do not delete or rename tools during promotion unless explicitly requested and separately validated.
