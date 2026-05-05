# Deny is not failure

Il run permit negato non deve rompere il workflow.

## Esempi di deny valido

- manca operator intent;
- quality gate non pulito;
- provider generation non richiesta;
- NPU audit non promossa;
- GPU.0 non autorizzata.

## Errori veri

- artifact non scritto;
- JSON non valido;
- eccezione Python;
- telemetry strutturale fallita.

## Policy

Il governor deve produrre output utilizzabile dal final product package anche
quando blocca la run provider.
