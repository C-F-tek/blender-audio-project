# SQLite memory visibility

La memoria SQLite deve essere visibile nella run, ma i database non devono essere
versionati né copiati nel bundle.

## Path canonici

```text
output/ai_runtime_memory/operational_context.sqlite
indexAI/agent_memory/agent_memory.sqlite
```

## Contratto

- scratch memory: ammessa come artifact locale;
- persistent memory: read/default guarded;
- `persistent_memory_write_performed=false` nel default Full0To10;
- ogni write persistente richiede consenso esplicito;
- il bundle deve mostrare se la lane SQLite è stata letta, saltata o scritta.

## Divieti

Non committare:

```text
*.db
*.sqlite
*.sqlite-wal
*.sqlite-shm
```

Non includere contenuto DB in `artifact_manifest.preview` o sezioni equivalenti.
