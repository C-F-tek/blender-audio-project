# Validazione CarmineLike

Ogni patch deve fornire:

- lista file;
- numero righe;
- comandi `py_compile`;
- smoke test;
- `git diff --check`;
- `git status --short`;
- commit message consigliato.

Le patch non devono richiedere run reale provider finché Ollama/GPU/tool/memory
non sono cablati e verificati.
