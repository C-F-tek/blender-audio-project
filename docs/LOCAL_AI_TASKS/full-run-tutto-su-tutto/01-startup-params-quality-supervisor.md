# Startup parameters: quality supervisor

Il quality supervisor è safe-by-default.

## Default

```text
run_unified_full0to10_quality_supervisor.ps1
```

senza flag espliciti esegue solo:

```text
preflight quality stack
final quality stack
```

## Parametri

- `-RunLauncher`: abilita il launcher Full0To10 reale;
- `-SkipLauncher`: disabilita launcher, compatibilità esplicita;
- `-NoExternalProbes`: evita probe esterni `ollama`, `nvidia-smi`, OpenVINO;
- `-AllowGitSyncBranching`: consente al launcher di fare git sync/branching;
- `-ForwardedArgs`: inoltra argomenti al supervisor sottostante.

## Regola operativa

Senza `-RunLauncher`, nessun provider/runtime launcher deve partire.
Senza `-AllowGitSyncBranching`, il launcher deve ricevere `-SkipGitSync` e
`-NoBranch`.
