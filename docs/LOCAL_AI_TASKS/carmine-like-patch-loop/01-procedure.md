# Procedura CarmineLike

Regole operative:

1. usare micro-file sotto 300 righe;
2. produrre bundle ZIP applicabile localmente;
3. includere `run_patch_bundle.py`;
4. stampare righe risultanti;
5. validare con `py_compile`, smoke dedicato e `git diff --check`;
6. committare solo sorgenti/docs/test;
7. non committare `output/**`, DB, SQLite, render o artifact runtime;
8. ripetere il ciclo fino a chiusura obiettivo.

## Sequenza

```text
prepare patch -> apply -> validate -> git add mirato -> commit -> push -> next patch
```
