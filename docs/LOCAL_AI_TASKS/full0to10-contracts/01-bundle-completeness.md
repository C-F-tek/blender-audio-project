# Bundle completeness

Il bundle Full0To10 completo deve rendere tracciabili tutte le superfici operative
necessarie a una AI successiva per capire la run senza raw dump pesanti.

## Ruoli obbligatori

- workflow report;
- orchestrator raw report;
- GPU raw report;
- GPU/NPU sync diagnostics;
- repository consistency map;
- repository consistency smoke;
- decision loop report;
- deterministic recommendations;
- patch plan;
- runtime tool usage telemetry;
- runtime tool capability manifest;
- full toolbox run telemetry summary;
- semantic chunk manifest;
- shared toolbox AI-to-AI bundle.

## Regola

Il bundle può contenere manifest e preview controllate, ma non deve copiare per intero:

```text
output/ai_pipeline/*checkpoints*
output/ai_context_packs/*
indexAI/code_chunks/*
indexAI/project_code_chunks/*
renders/*
*.sqlite
*.db
full_analysis*.json
*analysis_full*.json
```

## Validazione

```powershell
python .\Tools\validation\check_full0to10_bundle_contracts.py `
  --repo-root . `
  --bundle .\docs\LOCAL_VALIDATION_EVIDENCE\<bundle>.json `
  --evidence-dir .\docs\LOCAL_VALIDATION_EVIDENCE `
  --output .\output\validation\full0to10_contract_validation.json `
  --markdown-output .\output\validation\full0to10_contract_validation.md
```
