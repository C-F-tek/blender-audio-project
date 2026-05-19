# config context

## Role

`config/` contains repository-level configuration that can affect source allowlists, product gates, generated artifact policy, launcher behavior and safe-apply boundaries.

This area is not runtime output. Treat files here as configuration inputs that may change how tools interpret the repository.

## Responsibilities

Typical configuration concerns include:

```text
source allowlists
artifact allowlists
generated file policy
safe apply constraints
launcher/profile configuration references
validation gates and product-readiness inputs
```

Exact files may evolve. Always inspect current file contents before changing behavior.

## Safety rules

- Configuration changes can alter what the system is allowed to touch.
- Do not loosen allowlists or guardrails without explicit rationale and validation.
- Do not add secrets, tokens or workstation-private credentials.
- Keep config changes small and reviewable.
- Validate downstream behavior with the relevant `Tools.validation` checks.

## AI usage

When an AI agent sees a blocked file, missing target or safe-apply refusal, inspect `config/` before assuming the tool is broken.

When adding a new source-writing capability, update config only together with validation evidence proving that the new path is intended and safe.
