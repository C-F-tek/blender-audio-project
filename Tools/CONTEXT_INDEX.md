# Tools global context index

Use this file as the compact navigation layer for tool context files.

## Core contracts before tool navigation

Read these before treating any tool, dispatcher, smoke or provider artifact as proof:

| Contract | File |
| --- | --- |
| AI limitations and anti-ambiguity | `docs/AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md` |
| Core lane completeness | `docs/CORE_LANE_COMPLETENESS_CONTRACT.md` |
| IA Universe model-to-code map | `docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md` |

## Area indexes

| Area | Main context | Family index |
| --- | --- | --- |
| `ia_carmine` | `ia_carmine/TOOL_CONTEXT.md` | `ia_carmine/CONTEXT_INDEX.md` |
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
ia_carmine/dispatch.py
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
