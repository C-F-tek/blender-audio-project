# Tools/docs - Markdown/code coherence

Strumenti locali per confrontare documentazione Markdown e codice reale.

## Comandi

```powershell
python -m Tools.docs build_code_aware_md_coherence --repo-root . --max-lines 700
python -m Tools.docs repo_tool_surface_audit --repo-root . --area ai --area validation
python -m Tools.docs rewrite_legacy_tool_invocations --repo-root . --area ai --area validation
python -m Tools.docs promote_root_tool_package --repo-root . --area <area> --tool <tool>
python -m Tools.docs tool_root_inventory --repo-root . --area ai --area validation
python -m Tools.docs apply_md_code_coherence_refactor --repo-root . --apply
python -m Tools.validation check_md_code_coherence --repo-root . --max-high 0
```

`repo_tool_surface_audit` e report-only: trova invocazioni legacy
`python Tools/<area>/<script>.py`, script ancora in root `Tools/<area>` e file
fuori budget, senza applicare modifiche.

`rewrite_legacy_tool_invocations` e dry-run di default; con `--apply` riscrive
le invocazioni Python legacy verso `python -m Tools.<area> <tool>`.

`promote_root_tool_package` e dry-run di default; con `--apply` sposta uno
script root `Tools/<area>/<tool>.py` in `Tools/<area>/<tool>/cli.py`.

`tool_root_inventory` fotografa i file rimasti direttamente nelle root
`Tools/<area>` e separa entrypoint, helper interni, superfici consentite e package.

Gli output completi vanno sotto `output/validation/**` e non devono essere
committati.
