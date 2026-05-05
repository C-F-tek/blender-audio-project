# GPU body/mind control

La GPU deve diventare padrona del proprio stato operativo, non solo essere un
device disponibile.

## Corpo

Il corpo GPU include:

- driver visibility;
- memory budget;
- process ownership;
- runtime telemetry;
- thermal/driver state quando disponibile.

## Mente

La mente GPU include:

- advisory policy;
- provider selection;
- quality gate awareness;
- fallback reasoning;
- no implicit generation.

## Effetto pratico

Prima di generare, il sistema deve sapere:

1. se la GPU è visibile;
2. quale lane la usa;
3. se la generation è ammessa;
4. quali blocker esistono;
5. quale evidence entra nel prodotto finale.
