# Script aging and visibility audit — 2026-05-09

Status: code-search and commit-history derived review map  
Scope: scripts that may be hidden by age, wrapper proliferation, legacy domain boundaries or old task-specific names.

This is not a deletion list. It is a notice/work queue for future cleanup and owner verification.

## Evidence limits

GitHub connector access in this pass did not expose a full recursive tree with per-file last-modified timestamps. The audit therefore uses:

```text
oldest commit search results sorted by committer date
file-level commit inspection for early script history
code search for script/wrapper names
current owner/capability docs in AGENTS.md, Tools/ai/README.md and capability maps
```

Classification is conservative. A script is marked `review-candidate`, not obsolete, unless current docs/code clearly supersede it.

## Aging model

| Bucket | Meaning | Action |
|---|---|---|
| legacy-domain | Belongs to Blender/audio application layer. | Leave scoped unless a Blender task requests it. |
| active-owner | Has clear current owner role. | Keep and document. |
| wrapper-candidate | Thin or older workflow wrapper may be superseded by unified launcher. | Verify references before removal. |
| smoke-validator | Focused validator/smoke. | Keep if referenced by docs/PR validation. |
| evidence-only | Produces reports/evidence, no source mutation. | Keep if still in runbook/manifest path. |
| review-candidate | Hidden or unclear current lane. | Investigate with local script inventory. |

## Oldest observed script lineage

| Observed date | Path / area | Bucket | Notes |
|---|---|---|---|
| 2026-04-25 | `Scripting/v61b/main_v61b.py` | legacy-domain | Oldest observed script commit in this pass. Blender runtime domain; do not refactor during AI orchestration cleanup. |
| 2026-04-30 | `Tools/ai/build_ai_context_pack.py` | active-owner | Context-pack prototype became an active evidence/context lane. Still relevant but should stay bounded and split if touched. |
| 2026-05-01/02 | validation and patch-spec helpers | active-owner / smoke-validator | Early AI backend hardening. Keep if still referenced by validation docs. |
| 2026-05-02 | `replay_gpu_planner_json_contract.py` area | evidence-only / review-candidate | Historical GPU planner replay evidence. Verify whether still needed after current provider probe hardening. |
| 2026-05-08 | `prepare_review_pr.py`, patch suggestion bundle path | active-owner | Current Markdown-to-review-PR product path; do not prune. |

## Current active owner scripts

These are not cleanup targets unless an implementation task changes their owner contract:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
Tools/workflow/python_env.ps1
Tools/workflow/unified_phase_visibility.ps1
Tools/workflow/unified_run_observer.ps1
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py
Tools/ai/run_agent_gpu_deep_planning_supervised.py
Tools/ai/run_gpu0_peer_companion_worker.py
Tools/ai/build_ai_peer_exchange_packet.py
Tools/ai/agent_runtime_tool_broker.py
Tools/ai/build_runtime_tool_usage_telemetry.py
Tools/ai/build_full_toolbox_run_telemetry_summary.py
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py
Tools/ai/build_github_evidence_bundle.py
Tools/ai/apply_patch_suggestion_bundle.py
Tools/ai/prepare_review_pr.py
Tools/ai/build_ai_context_pack.py
Tools/ai/build_agent_state_packet.py
Tools/ai/select_semantic_code_chunks.py
```

## Wrapper candidates to notice

These surfaced by code search and should be reviewed against the unified launcher before future maintenance:

| Path | Initial classification | Review question |
|---|---|---|
| `Tools/workflow/run_docs_md_refactor_10min.ps1` | wrapper-candidate | Is this still a supported shortcut or superseded by `run_unified_local_ai_refactor.ps1 -Mode md`? |
| `Tools/workflow/run_local_ai_markdown_task.ps1` | wrapper-candidate | Is this old Markdown task runner still referenced, or should docs point to unified launcher/task file flow? |
| `Tools/workflow/run_full0to10_quality_gate.ps1` | wrapper-candidate / evidence-only | Is this still independently useful, or now a phase behind Full0To10/final product tooling? |
| `Tools/workflow/run_full0to10_final_tool_product.ps1` | wrapper-candidate / active product wrapper | Keep if it is the canonical thin wrapper for final product builder; otherwise document as delegated phase. |
| `Tools/workflow/run_full0to10_effective_use_optimization.ps1` | wrapper-candidate | Verify whether it is still in active final product chain or historical quality step. |
| `Tools/workflow/run_full_memory_tool_regeneration.ps1` | review-candidate | Verify whether memory/tool regeneration is still called directly or only through unified/full-toolbox phases. |
| `Tools/workflow/run_ai_cycle_startup_preflight.ps1` | smoke-validator / wrapper-candidate | Keep if current Python policy/preflight docs call it; otherwise mark as legacy preflight. |
| `Tools/ai/run_agent_gpu_deep_planning_review.py` | review-candidate | Compare with `run_agent_gpu_deep_planning_supervised.py`; avoid duplicate GPU1 advisory owners. |

## Legacy-domain scripts to avoid accidental refactor

```text
Scripting/**
Blender runtime scripts
FFmpeg/media helper scripts
full frame-level analysis JSON producers/consumers
```

These are not obsolete merely because they are old. They belong to the downstream application domain and should be touched only by a scoped Blender/audio task.

## Review procedure before marking obsolete

For each candidate:

1. Search exact path in docs and code.
2. Check whether unified launcher still calls it.
3. Check whether a validator/smoke references it.
4. Check whether recent PR bodies mention it as active validation.
5. Run local inventory by last commit date.
6. If no references remain, mark as `deprecated-candidate` in docs first.
7. Delete only in a separate cleanup PR with explicit human approval.

## Local authoritative inventory command

Run locally for a full oldest-to-newest script view:

```powershell
$ScriptExt = '*.py','*.ps1','*.psm1','*.sh','*.bat','*.cmd'
$Rows = foreach ($Ext in $ScriptExt) {
  Get-ChildItem -Recurse -File -Filter $Ext |
    Where-Object { $_.FullName -notmatch '\\(\.git|\.venv|venv|__pycache__|output|renders|indexAI\\code_chunks|indexAI\\project_code_chunks)\\' } |
    ForEach-Object {
      $Rel = Resolve-Path -Relative $_.FullName
      $Last = git log -1 --format='%cI|%h|%s' -- $Rel 2>$null
      [PSCustomObject]@{
        File = $Rel
        Lines = (Get-Content $_.FullName | Measure-Object -Line).Lines
        LastCommit = $Last
      }
    }
}
$Rows | Sort-Object LastCommit, File | Export-Csv ".\output\validation\script_age_inventory_$(Get-Date -Format 'yyyyMMdd-HHmmss').csv" -NoTypeInformation -Encoding UTF8
```

Do not commit the generated CSV under `output/**`. Promote only compact findings into docs after review.

## Immediate next work queue

```text
1. Run the local authoritative inventory command.
2. Compare wrapper candidates with unified launcher references.
3. Add a small owner/status table to Tools/workflow/README.md.
4. For confirmed superseded wrappers, open a docs-only deprecation PR first.
5. Remove scripts only in a later explicit cleanup PR.
```
