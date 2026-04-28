# AI Artifact Schemas

Lightweight schema notes for the additive AI pipeline.

## Required keys

| Artifact | Required keys |
|---|---|
| `track_summary.json` | `schema_version`, `source_analysis` |
| `music_segments.json` | `schema_version`, `segments` |
| `audio_event_map.json` | `schema_version` |
| `ai_scene_brief.json` | `schema_version`, `creative_intent`, `technical_intent` |
| `ai_resource_budget.json` | `schema_version`, `recommendations` |
| `ai_selected_mapping.json` | `schema_version`, `selected` |
| `ai_validation_report.json` | `schema_version`, `passed`, `score`, `blocking_errors`, `warnings` |

Validation command:

```powershell
py .\Tools\ai\validate_ai_artifacts.py --repo-root . --artifact-dir .\output\ai_pipeline
```
