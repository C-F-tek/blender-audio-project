# Evidence Chunk 0039/0041

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md`
- source_sha256: `8ed89af8ed3e4fa6f8a1a3a56da19fd97a274354793464078ec9f92deaf33e83`
- line_start: `5046`
- line_end: `5108`
- section_kinds: `['markdown_heading_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0038.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0040.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: identificare riferimenti mancanti a file Python nella documentazione Markdown.  
**Segnali principali**: 30+ avvisi “high” di tipo `md_mentions_missing_python_path` in `.aider.chat.history.md

## Context before

- `low`: `46`
- `medium`: `1465`

## Finding kind counts

- `documented_python_script_without_obvious_smoke`: `46`
- `md_cli_arg_not_in_argparse`: `2`
- `md_mentions_missing_markdown_path`: `1463`
- `md_mentions_missing_powershell_path`: `39`
- `md_mentions_missing_python_path`: `763`
- `md_python_command_script_missing`: `14`


## Chunk content

```md
## Findings

| Severity | Kind | Source | Line | Target | Recommendation |
|---|---|---|---:|---|---|
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 91 | `animation.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 93 | `animation.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 94 | `asset_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 96 | `asset_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 97 | `atmosphere_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 99 | `atmosphere_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 100 | `camera_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 102 | `camera_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 103 | `config.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 105 | `config.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 106 | `fog_dynamics.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 108 | `fog_dynamics.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 109 | `fog_filaments.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 111 | `fog_filaments.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 112 | `io_utils.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 114 | `io_utils.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 115 | `materials.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 117 | `materials.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 118 | `physics_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 120 | `physics_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 121 | `render_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 123 | `render_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 124 | `scene_tuning_panel.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 126 | `scene_tuning_panel.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 127 | `scene_utils.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 129 | `scene_utils.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 130 | `world_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 132 | `world_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 146 | `__init__.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 148 | `__init__.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 149 | `accent_patch.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 151 | `accent_patch.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 152 | `common.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 154 | `common.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 155 | `diagnostics.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 157 | `diagnostics.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 158 | `fog_patch.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 160 | `fog_patch.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 161 | `hero_material_patch.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 163 | `hero_material_patch.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 164 | `lighting_patch.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 166 | `lighting_patch.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 167 | `render_patch.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 169 | `render_patch.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 170 | `runner.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 172 | `runner.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 189 | `__init__.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 191 | `__init__.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 193 | `__init__.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 195 | `__init__.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 196 | `collections.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 198 | `collections.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 199 | `registry.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 201 | `registry.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 209 | `animation.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 211 | `animation.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 212 | `asset_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 214 | `asset_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 215 | `atmosphere_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
```

## Context after

| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 217 | `atmosphere_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 218 | `camera_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 220 | `camera_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 221 | `config.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 223 | `config.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 224 | `fog_dynamics.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 226 | `fog_dynamics.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 227 | `io_utils.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 229 | `io_utils.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 230 | `materials.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 232 | `materials.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 233 | `physics_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
