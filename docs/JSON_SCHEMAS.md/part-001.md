<!-- IA-CARMINE-MD-SPLIT: part -->
# JSON_SCHEMAS — parte 001 di 002

Sorgente indice: [`README.md`](README.md)

## Navigazione

- [Indice](README.md)
- [Parte successiva](part-002.md)

```text
File pattern:
output/ai_pipeline/full_context_golden_proposals.json
Producer:
Tools/ai/build_full_context_golden_proposals.py
Consumer:
Maintainers, proposal validators and future patch-spec promotion tools.
Required fields:
Same generic `repository_change_proposals` root/proposal fields plus coverage of required proposal families P1-P6.
Required kind:
repository_change_proposals
Required proposal families:
P1 adapter manifest validator
P2 reusable enrichment-plan helper
P3 full-context golden path docs contract
P4 optional wrapper preset flag
P5 selected-chunks evidence standard validation block
P6 NPU knowledge-broker / context-oracle prototype
Provider semantics:
The generator is deterministic and report-only. It does not execute providers, apply patches or mutate source.
Current validators:
Tools/validation/check_repository_change_proposals.py
Tools/validation/check_full_context_golden_proposals.py
Notes:
The full-context validator catches semantic insufficiency even when the generic proposal schema passes.
```
