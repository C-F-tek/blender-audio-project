# Tools global context index

Use this file as the compact navigation layer for tool context files.

## Area indexes

| Area | Main context | Family index |
| --- | --- | --- |
| `Tools/ai` | `Tools/ai/TOOL_CONTEXT.md` | `Tools/ai/CONTEXT_INDEX.md` |
| `Tools/validation` | `Tools/validation/TOOL_CONTEXT.md` | `Tools/validation/CONTEXT_INDEX.md` |
| `Tools/workflow` | `Tools/workflow/TOOL_CONTEXT.md` | `Tools/workflow/CONTEXT_INDEX.md` |
| `Tools/npu` | `Tools/npu/TOOL_CONTEXT.md` | `Tools/npu/CONTEXT_INDEX.md` |
| `Tools/docs` | `Tools/docs/TOOL_CONTEXT.md` | `Tools/docs/CONTEXT_INDEX.md` |
| `Tools/git` | `Tools/git/TOOL_CONTEXT.md` | `Tools/git/CONTEXT_INDEX.md` |
| `Tools/repo_patch_runner` | `Tools/repo_patch_runner/TOOL_CONTEXT.md` | `Tools/repo_patch_runner/CONTEXT_INDEX.md` |

## Command surface

```powershell
python -m Tools.<area> <tool> [args...]
```

Dispatchers:

```text
Tools/ai/dispatch.py
Tools/validation/dispatch.py
Tools/workflow/dispatch.py
Tools/npu/dispatch.py
Tools/docs/dispatch.py
Tools/git/dispatch.py
Tools/repo_patch_runner/dispatch.py
```

## Mapping evidence

Optional mapping evidence procedure:

```text
docs/MAPPING_TOOL_EVIDENCE.md
```

Mapping is operator-scheduled and not required before normal documentation updates.