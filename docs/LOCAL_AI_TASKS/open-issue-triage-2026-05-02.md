# Open issue triage — 2026-05-02

## Scope

GitHub-only triage of open issues before local workstation validation.

No issue is closed by this note. No branch, merge, rebase, delete, force-push or repository rewrite is authorized here.

## Current open issue inventory

### Issue #104 — `Enhance local GPU task workload depth`

```text
state: open
role: future local GPU/Ollama workload-depth task
risk: medium/high because provider execution may be involved if activated
```

Summary:

```text
Explore heavier, more informative local GPU/Ollama task profiles without violating IA-Carmine guardrails.
```

Guardrail interpretation:

```text
provider execution only when explicitly requested
manual-review-only
no automatic patch application
no raw output/** commit
NPU remains non-blocking checkpoint auditor, not primary advisory lane
```

Recommended timing:

```text
after PR #108/#109 are validated and merged or intentionally deferred
```

Recommended next artifact:

```text
small task MD for GPU heavy profile, not provider execution itself
```

### Issue #57 — `Local AI task: docs congruence cleanup after selective planner merge`

```text
state: open
role: documentation/workflow-state cleanup
risk: low if kept docs-only
```

Summary:

```text
Move completed selective planner execution plan from active to completed, update status fields and validate docs/execution-plan consistency.
```

Guardrail interpretation:

```text
no provider execution
no Blender runtime
no generated-index manual edits
no full analysis JSON
no prompt/model/provider behavior changes
```

Recommended timing:

```text
can be handled after current PR stack is stable, or as a separate small docs-only PR from updated master
```

Suggested local validation from issue:

```powershell
python .\Tools\validation\check_execution_plan_status.py --repo-root . --output .\output\validation\execution_plan_status.json
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json
git diff --check
```

## Recommended order relative to current PRs

```text
1. Finish PR #109 local wiring and focused evidence bundle.
2. Validate/settle PR #108 if it is still intended as documentation/validator base.
3. Close PR #110 after confirming PR #109 contains all useful refactor work.
4. Handle Issue #57 as a small docs-only cleanup PR.
5. Handle Issue #104 only after provider-heavy work is explicitly requested and local GPU time is available.
```

## Current safe decision

Issue #57 is the safest future task candidate. Issue #104 should remain parked until local provider execution is explicitly planned.
