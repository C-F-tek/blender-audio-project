# Accelerator control plane

Il prodotto finale Full0To10 deve includere una control plane acceleratore.

## GPU corpo

La GPU deve conoscere il proprio "corpo":

- visibilità device;
- budget memoria;
- ownership processi;
- vincoli runtime;
- telemetry richiesta.

## GPU mente

La GPU deve conoscere la propria "mente":

- quando può essere primary advisory;
- quando deve restare spenta;
- quando deve produrre solo blocker;
- quali quality gate servono prima della generazione.

## NPU auditor

La NPU resta lane auditor/diagnostic:

- può campionare;
- può verificare disaccordi;
- può generare evidence diagnostica;
- non diventa primary advisory senza patch dedicata.

## OpenVINO GPU.0

GPU.0 è secondary diagnostic:

- non deve sottrarre la GPU primaria a Ollama;
- non deve generare implicitamente;
- può essere promossa solo con patch esplicita.

## Scheduler

Lo scheduler deve produrre una decisione prima della run reale:

```text
memory/tools allowed
ollama_gpu blocked until explicit launcher
npu blocked as primary
gpu0 blocked as primary
generation_allowed=false
```
