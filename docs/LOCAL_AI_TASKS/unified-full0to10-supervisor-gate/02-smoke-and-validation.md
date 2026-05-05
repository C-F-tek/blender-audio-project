# Smoke and validation

Smoke dedicato:

```powershell
python .\Tools\validation\run_unified_full0to10_supervisor_gate_smoke.py `
  --repo-root . `
  --work-dir .\output\validation\unified_full0to10_supervisor_gate_smoke
```

Il test usa `-SkipLauncher`, genera evidence sintetica locale e verifica che il
gate finale funzioni senza provider runtime.

## Validazioni consigliate

```powershell
python -m py_compile .\Tools\validation\run_unified_full0to10_supervisor_gate_smoke.py
git diff --check
git status --short
```

Non committare gli output generati dallo smoke.
