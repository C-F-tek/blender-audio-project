# Tools/docs context

<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:START -->
## Current Runtime/Tool Contract (2026-05-24)

Canonical wording: `docs/CURRENT_RUNTIME_MARKDOWN_CONTRACT.md`.

- GPU1/NVIDIA primary Ollama lane is the operational center and advances by heap pointer/recovery turns without waiting for GPU0/NPU sidecar completion.
- GPU0/NPU are `packet_review_only` sidecars: they start only after a reviewable GPU1 packet, do not close product, and remain deferred evidence until a later GPU1 turn consumes their pointer ids.
- Tool/lab/matrix/debug reporting must distinguish `lab_called`, `lab_report_written`, `lab_usable` and `lab_status`; attempted tool calls are evidence, not automatic usable lab output.
- `FINAL_PRODUCT` is single: text, code, or text+code. `PLAN_PRODUCT_FULL_PATCH.md` is its text/prose surface; `CODE_PRODUCT_FULL_PATCH.md` is its code/diff surface only when verified code exists. GPU1 emits causal `FINAL_PRODUCT_DELTA` records; blocked status is runtime/gate classification, not GPU1 output.
- Missing optional values stay empty/null; required missing devices or provider prerequisites raise or block with a typed reason rather than emitting placeholder text.
- Complete runs require explicit config flags, including `--files-per-round`, `--gpu0-ollama-num-ctx`, `--npu-micro-start-mode`, `--npu-final-wait-seconds` and `--max-degraded-lanes`.
<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:END -->


## Role

`Tools/docs` owns documentation hygiene, Markdown/code coherence checks, repository tool-surface audits, split/refactor helpers and migration utilities for tool packaging.

Canonical invocation:

```powershell
python -m Tools.docs <tool> [tool args...]
```

The source of truth for public documentation tools is `Tools/docs/dispatch.py`.

## Main families

### Repository and tool surface audits

Use these to map what exists before changing the repository. They are the first tools to run when the codebase has shifted after a large refactor.

Representative tools:

```text
tool_root_inventory
repo_tool_surface_audit
tool_package_family_audit
module_duplication_audit
```

These tools help answer:

```text
Which tools are exposed?
Which scripts are still root-level entrypoints?
Which packages duplicate responsibilities?
Which docs still reference legacy invocation paths?
```

### Tool package migration

Use these when converting legacy root scripts into package-owned CLIs or fixing references after a move.

Representative tools:

```text
promote_root_tool_package
move_tool_package
rewrite_legacy_tool_invocations
internalize_root_module
```

Migration tools must preserve operator command surfaces through dispatchers. Do not move scripts without updating references and validation docs.

### Markdown split and refactor helpers

Use these for large Markdown files, generated docs and split manifests.

Representative tools:

```text
split_large_markdown
refactor_markdown_splits
markdown_split_tool_guide
```

Split directories must include enough context for agents to reassemble intent. Avoid producing split docs that hide the canonical source.

### Code-aware documentation coherence

Use these to align documentation with actual code and command surfaces.

Representative tools:

```text
build_code_aware_md_coherence
code_aware_md_coherence_render
code_aware_md_refs
apply_md_code_coherence_refactor
md_code_coherence_refactor_core
```

A doc is useful only if it points to real files, real dispatchers and current invocation forms.

### Hygiene plan generation

Use these to create structured documentation cleanup plans before large edits.

Representative tools:

```text
build_repo_hygiene_plan
```

Plans should distinguish obsolete docs, canonical docs, generated evidence and runtime artifacts.

## Documentation rules

- Prefer small context files near the relevant tool area.
- Keep `AGENTS.md`/root guidance concise and link deeper files.
- Document command surfaces using dispatcher invocations.
- Do not present raw `output/**` artifacts as canonical docs.
- Mark generated/session evidence clearly when it is not a stable runbook.

## Safe extension rules

- Add new docs hygiene tools under `Tools/docs/docs_hygiene/<family>/` or `_shared/` only when shared.
- Register public commands in `Tools/docs/dispatch.py`.
- Validate new docs with validation docs-hygiene checks when available.
