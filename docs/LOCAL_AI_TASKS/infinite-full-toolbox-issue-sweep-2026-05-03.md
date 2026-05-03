# IA-Carmine — Infinite Full Toolbox Issue Sweep

## Objective

Use the evidence merged from PR #179 as the new baseline and run a controlled mega-fix lane to reduce systemic issues across the IA-Carmine local AI orchestration stack.

This is not an uncontrolled rewrite. The operating model remains:

```text
tools -> evidence -> recommendation -> decision -> patch plan -> patch bundle -> explicit apply -> validation -> PR
Baseline

Merged baseline:

PR #179
merge_commit: 165deb7dcf59f9975469ddbd2b65ca34b76ae008
branch merged: codex/full-toolbox-provider-advisory-and-caps

Key merged capabilities:

provider failures advisory
MaxRecommendations / MaxPatchPlans controls
GPU runner provider-error hardening
runtime tool usage telemetry
runtime tool capability manifest
deterministic/no-Ollama semantic chunks
repository consistency generated chunk exclusion
declared vs broker-executed runtime tool telemetry
full toolbox telemetry/evidence bundle
Guardrails

Do not:

merge to master without explicit command
force-push
rewrite history
delete evidence/chunks without explicit command
run Blender runtime
commit output/**
commit renders/**
commit *.db / *.sqlite / *.sqlite-wal / *.sqlite-shm
modify secrets/permissions/billing/visibility
Primary issue sweep targets
A. Validate deterministic/no-Ollama handoff

Prove with a fresh mini-run that:

semantic chunk basename = full_toolbox_<STAMP>_cloud_semantic_deterministic
ollama.enabled=false
summary_source=deterministic
no summary_source=ollama
B. Validate repository consistency exclusion

Prove that generated evidence chunk folders no longer inflate repository consistency findings.

Generated chunk paths must not drive high-signal patch planning:

docs/LOCAL_VALIDATION_EVIDENCE/*_cloud_semantic_chunks/**
docs/LOCAL_VALIDATION_EVIDENCE/*_cloud_semantic_deterministic_chunks/**
docs/LOCAL_VALIDATION_EVIDENCE/*_chunks/**
C. Validate runtime tool telemetry

Prove that planner-declared tool requests and broker executions are distinct:

runtime_tool_request_count
runtime_tool_execution_count
declared_not_executed_count
tool_call_entry_count
D. Add per-round GPU elapsed telemetry

Current known limitation:

gpu_metrics_source = gpu_elapsed_divided_by_round_count

Target:

each GPU round should include elapsed_seconds
sync report should prefer measured per-round durations
fallback to divided average only when round timing is absent
E. Enforce diagnostics_and_telemetry_required

Every valid AI-to-AI bundle must include:

workflow report
orchestrator raw report
GPU raw report
GPU/NPU sync diagnostics
repository consistency map
repository consistency smoke
decision loop report
deterministic recommendations
patch plan
runtime tool usage telemetry
runtime tool capability manifest
full toolbox run telemetry summary
semantic chunk manifest deterministic/no-Ollama
shared toolbox AI-to-AI bundle

Missing required diagnostics should fail bundle validation.

F. Stale proposal/evidence triage

Generated historical evidence and stale chunks should not become first-class patch targets.

Required behavior:

generated evidence = context/diagnostics
source code/docs = primary patch targets
stale generated proposals = advisory/triaged
G. PR size hygiene

The previous PR was intentionally large. This PR should add enforcement and validation, not another uncontrolled evidence flood.

Policy:

commit only compact evidence if needed
avoid committing raw output
prefer manifests/summaries over full generated chunk dumps unless explicitly needed
Initial validation commands
python .\Tools\validation\run_full_toolbox_deterministic_chunks_telemetry_smoke.py `
  --repo-root . `
  --output .\output\validation\full_toolbox_deterministic_chunks_telemetry_smoke.json `
  --markdown-output .\output\validation\full_toolbox_deterministic_chunks_telemetry_smoke.md

python .\Tools\validation\check_python_syntax.py `
  --repo-root . `
  --output .\output\validation\python_syntax_infinite_issue_sweep_baseline.json

git diff --check
git status --short
Mini-run proof target
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"

.\Tools\workflow\run_agent_review_full_toolbox_decision_loop.ps1 `
  -RepoRoot "." `
  -Stamp $Stamp `
  -RunGpuNpuProvider `
  -BudgetMinutes 8 `
  -MaxRounds 4 `
  -FilesPerRound 6 `
  -MaxContextFiles 80 `
  -MaxCharsPerFile 5000 `
  -MaxNewTokens 2400 `
  -MaxRecommendations 20 `
  -MinRecommendations 3 `
  -MaxPatchPlans 0 `
  -MinPatchPlans 3 `
  -KeepAlive "15m" `
  -NpuAuditorEveryRounds 4 `
  -NpuAuditorTimeoutSeconds 420 `
  -RepositoryConsistencyMapWorkers 8
Success criteria
baseline smoke passes
CodeQL passes
mini-run generates deterministic/no-Ollama chunks
runtime telemetry exposes declared vs executed tool counts
repository consistency ignores generated chunks
no output/** committed
no DB committed
no Blender runtime touched

