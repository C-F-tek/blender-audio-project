<!-- IA-CARMINE-MD-SPLIT: part -->
# gpu-npu-parallel-evidence-runbook — parte 001 di 002

Sorgente indice: [`README.md`](README.md)

## Navigazione

- [Indice](README.md)
- [Parte successiva](part-002.md)

```powershell
python .\Tools\validation\run_agent_review_patch_plan_smoke.py `
  --repo-root . `
  --orchestrator .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_orchestrator.json `
  --evidence .\output\ai_pipeline\agent_review_evidence_sufficiency.json `
  --output .\output\validation\agent_review_patch_plan_smoke.json `
  --markdown-output .\output\validation\agent_review_patch_plan_smoke.md
```
