# indexAI context

## Role

`indexAI/` contains AI-oriented index, memory, scene-script and patch-library material used by IA-Carmine workflows.

This area is not a general source-code package. It is a repository-local knowledge/index space that may include persistent memory, generated indexes, chunk manifests, patch library material and scene-script bundles.

## Typical subareas

```text
agent_memory/          -> persistent agent memory database/material
patch_library/         -> patch/task packets and service capsules
scene_scripts/         -> generated or curated scene script bundles
code_chunks/           -> generated semantic code chunk cache/manifests
project_code_chunks/   -> generated project code chunk cache/manifests
```

Exact folders may vary by branch/run.

## Memory policy

Persistent memory may live under:

```text
indexAI/agent_memory/agent_memory.sqlite
```

Default policy:

```text
read-only unless explicit persistent-write confirmation is provided
```

Do not silently write persistent memory from chat or provider output.

## Generated chunk policy

Generated semantic chunks are normally runtime/index artifacts and should not be committed unless the repository explicitly tracks a compact manifest as evidence.

Do not commit generated caches such as:

```text
indexAI/code_chunks/**
indexAI/project_code_chunks/**
```

unless a specific Git-trackable artifact has been intentionally selected.

## AI usage

Use this area as context/evidence only after checking current files. Do not infer that a path under `indexAI` is source code or an apply target.

Patch/library packets can guide planning, but source changes must still go through code product, patch candidate validation, and normal Git review.

## Guardrails

- No database commits unless explicitly intended and reviewed.
- No raw chunk cache commits.
- No source write claims based only on index material.
- Persistent memory writes require explicit confirmation.
