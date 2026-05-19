# Tools/validation/workflow_run context

## Role

`Tools/validation/workflow_run` contains checks for workflow launchers, startup CLI contracts, invocation policy and workflow evidence correlation.

## Responsibilities

- Validate operator product launcher behavior.
- Validate startup check CLI contract.
- Validate workflow Python invocation policy.
- Validate runtime evidence correlation launcher wiring.

## Representative commands

Use through the validation dispatcher:

```powershell
python -m Tools.validation run_operator_product_launcher_smoke ...
python -m Tools.validation run_startup_check_cli_contract_smoke ...
python -m Tools.validation check_workflow_python_invocation_policy ...
python -m Tools.validation run_runtime_evidence_correlation_launcher_wiring_smoke ...
```

## Output role

Outputs are validation reports for workflow entrypoint behavior.

## Notes

- Workflow validation checks command surfaces and launcher contracts.
- A launcher smoke is not proof that a full runtime product completed.
