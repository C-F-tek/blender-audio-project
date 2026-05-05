# P0 status and next priorities

## P0 resolved

`full0to10_provider_invocation_plan` è presente e viene importato dallo smoke:

```text
Tools/validation/run_full0to10_final_product_import_smoke.py
```

OpenVINO NPU/GPU.0 usa il normalizzatore:

```text
full0to10_accelerator_control.device_visibility
```

## Next P1

- launcher output controls;
- provider tool requests reinjection;
- semantic contract validator;
- runtime registry validator.

## Provider policy

La GPU/Ollama resta primary advisory solo con permit/gate espliciti. NPU e
GPU.0 restano audit/diagnostic.
