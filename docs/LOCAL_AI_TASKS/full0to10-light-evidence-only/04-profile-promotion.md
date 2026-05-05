# Light profile promotion

Questa fase non modifica il launcher grande.

## Perché

Il profilo light evidence-only è passato. Prima di inserirlo direttamente nel
launcher unico, viene aggiunto un wrapper di promozione:

```text
Tools/workflow/run_unified_light_full0to10_profile.ps1
```

## Output

```text
output/validation/unified_light_full0to10_profile/run
output/validation/unified_light_full0to10_profile/promotion
```

## Regola

Non cancellare Markdown in lavorazione. Non usare `git restore docs` durante
questa fase.
