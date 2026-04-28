# AI Artifact Schemas

This document records lightweight schemas for the additive AI artifact pipeline.

The implementation currently uses conservative structural checks in `Tools/ai/validate_ai_artifacts.py`.

## `track_summary.json`

Required keys:

```json
{
  "schema_version": 1,
  "source_analysis": "...",
  "duration_sec": 0,
  "estimated_bpm": 0,
  "segment_count": 0
}
```

## `music_segments.json`

Required keys:

```json
{
  "schema_version": 1,
  "segments": [
    {
      "name": "intro",
      "start_sec": 0,
      "end_sec": 10,
      "duration_sec": 10
    }
  ]
}
```

## `audio_event_map.json`

Required keys:

```json
{
  "schema_version": 1,
  "beats_sec": [],
  "peak_events": []
}
```

## `ai_scene_brief.json`

Required keys:

```json
{
  "schema_version": 1,
  "creative_intent": "...",
  "technical_intent": "...",
  "track_facts": {}
}
```

## `ai_resource_budget.json`

Required keys:

```json
{
  "schema_version": 1,
  "target_profile": "...",
  "recommendations": {}
}
```

## `ai_selected_mapping.json`

Required keys:

```json
{
  "schema_version": 1,
  "selected": {},
  "selected_candidates": []
}
```

## `ai_validation_report.json`

Required keys:

```json
{
  "schema_version": 1,
  "passed": true,
  "score": 1.0,
  "blocking_errors": [],
  "warnings": []
}
```
