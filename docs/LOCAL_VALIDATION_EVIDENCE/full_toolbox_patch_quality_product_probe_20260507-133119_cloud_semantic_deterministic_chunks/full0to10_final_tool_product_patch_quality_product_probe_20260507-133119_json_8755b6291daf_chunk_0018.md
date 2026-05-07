# Evidence Chunk 0018/0035

- source: `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `8755b6291dafb02a9387e89ef9948a1c0a9850a172d212bce6b03df7ba6ca391`
- line_start: `4673`
- line_end: `4928`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0017.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0019.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: artifacts. Preview: "provider_lane": "openvino_npu", "would_execute": false, "requires_primary_output": true, "audit_hooks": [ "compare provider recommendations to memory evidence", "verify no patch apply occurred", "verify GPU.0 did not become primary", "verify telemetry complet...

## Context before

                "max_rounds": 8,
                "max_new_tokens": 2400,
                "keep_alive": "20m"
              },
              "expected_outputs": [
                "ollama_gpu_real_workload_report.md",
                "full0to10_provider_runtime_telemetry.json",
                "full0to10_provider_recommendations.json"
              ]
            },
            {
              "name": "npu_after_run_audit",

## Chunk content

```json
              "provider_lane": "openvino_npu",
              "would_execute": false,
              "requires_primary_output": true,
              "audit_hooks": [
                "compare provider recommendations to memory evidence",
                "verify no patch apply occurred",
                "verify GPU.0 did not become primary",
                "verify telemetry completeness"
              ]
            },
            {
              "name": "gpu0_diagnostic_probe",
              "provider_lane": "openvino_gpu0",
              "would_execute": false,
              "requires_promotion": true,
              "reason": "GPU.0 remains secondary diagnostic"
            }
          ],
          "all_commands_are_non_executing": true,
          "future_execution_flag_required": true,
          "provider_execution_performed": false,
          "patch_application_performed": false,
          "source_writes_performed": false,
          "persistent_memory_write_performed": false
        }
      },
      "provider_workload_output_paths": {
        "path": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/full0to10_provider_workload_output_paths.json",
        "exists": true,
        "type": "json",
        "required": false,
        "size_bytes": 1751,
        "json": {
          "kind": "full0to10_provider_workload_output_paths",
          "passed": true,
          "workload_dir": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/future_real_run_outputs",
          "paths": {
            "ollama_workload_report": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/future_real_run_outputs/ollama_gpu_real_workload_report.md",
            "runtime_telemetry": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/future_real_run_outputs/full0to10_provider_runtime_telemetry.json",
            "recommendations": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/future_real_run_outputs/full0to10_provider_recommendations.json",
            "npu_audit_report": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/future_real_run_outputs/full0to10_npu_after_run_audit.json",
            "quality_validation": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/future_real_run_outputs/ai_workload_report_quality.json"
          },
          "write_policy": {
            "future_real_run_only": true,
            "current_bridge_writes_placeholder": false,
            "output_root_only": true
          },
          "validator_command": "python Tools/validation/check_ai_workload_report_quality.py --report-dir <workload_dir> --output <quality_validation>",
          "provider_execution_performed": false,
          "patch_application_performed": false,
          "source_writes_performed": false,
          "persistent_memory_write_performed": false
        }
      },
      "track_input_contract": {
        "path": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/track_inputs/full0to10_track_input_contract.json",
        "exists": true,
        "type": "json",
        "required": false,
        "size_bytes": 7275,
        "json": {
          "kind": "full0to10_track_input_contract",
          "track_name": "current",
          "passed": true,
          "complete": true,
          "require_inputs": false,
          "required_roles": [
            "analysis_json",
            "music_context_json",
            "blender_keyframes_json"
          ],
          "selected_inputs": {
            "analysis_json": {
              "path": "output/validation/md_code_coherence_report_current.json",
              "score": 25,
              "size_bytes": 581441,
              "role": "analysis_json"
            },
            "music_context_json": {
              "path": "Scripting/_template_audio_reactive_package/inputs/music_context.json",
              "score": 80,
              "size_bytes": 237,
              "role": "music_context_json"
            },
            "blender_keyframes_json": {
              "path": "output/validation/md_code_coherence_report_current.json",
              "score": 25,
              "size_bytes": 581441,
              "role": "blender_keyframes_json"
            }
          },
          "candidates": {
            "analysis_json": [
              {
                "path": "output/validation/md_code_coherence_report_current.json",
                "score": 25,
                "size_bytes": 581441,
                "role": "analysis_json"
              },
              {
                "path": "output/validation/md_code_coherence_report_semantic_current.json",
                "score": 25,
                "size_bytes": 597481,
                "role": "analysis_json"
              },
              {
                "path": "output/validation/md_code_coherence_report_semantic_v8_current.json",
                "score": 25,
                "size_bytes": 515888,
                "role": "analysis_json"
              },
              {
                "path": "output/ai_context_packs/full_context_golden_core_ai_backend.json",
                "score": 5,
                "size_bytes": 45075,
                "role": "analysis_json"
              },
              {
                "path": "output/ai_context_packs/full_context_golden_selected_chunks.json",
                "score": 5,
                "size_bytes": 56392,
                "role": "analysis_json"
              },
              {
                "path": "output/ai_context_packs/unified_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_context_pack_full_access_md_telemetry_20260506-154554.json",
                "score": 5,
                "size_bytes": 45308,
                "role": "analysis_json"
              },
              {
                "path": "output/ai_context_packs/unified_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_context_pack_gpu0_companion_full0to10_quick_20260506-191903.json",
                "score": 5,
                "size_bytes": 45322,
                "role": "analysis_json"
              },
              {
                "path": "output/ai_context_packs/unified_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_context_pack_gpu0_full0to10_quick_20260506-180824.json",
                "score": 5,
                "size_bytes": 45300,
                "role": "analysis_json"
              }
            ],
            "music_context_json": [
              {
                "path": "Scripting/_template_audio_reactive_package/inputs/music_context.json",
                "score": 80,
                "size_bytes": 237,
                "role": "music_context_json"
              },
              {
                "path": "output/validation/md_code_coherence_report_current.json",
                "score": 25,
                "size_bytes": 581441,
                "role": "music_context_json"
              },
              {
                "path": "output/validation/md_code_coherence_report_semantic_current.json",
                "score": 25,
                "size_bytes": 597481,
                "role": "music_context_json"
              },
              {
                "path": "output/validation/md_code_coherence_report_semantic_v8_current.json",
                "score": 25,
                "size_bytes": 515888,
                "role": "music_context_json"
              },
              {
                "path": "output/ai_context_packs/full_context_golden_core_ai_backend.json",
                "score": 5,
                "size_bytes": 45075,
                "role": "music_context_json"
              },
              {
                "path": "output/ai_context_packs/full_context_golden_selected_chunks.json",
                "score": 5,
                "size_bytes": 56392,
                "role": "music_context_json"
              },
              {
                "path": "output/ai_context_packs/unified_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_context_pack_full_access_md_telemetry_20260506-154554.json",
                "score": 5,
                "size_bytes": 45308,
                "role": "music_context_json"
              },
              {
                "path": "output/ai_context_packs/unified_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_context_pack_gpu0_companion_full0to10_quick_20260506-191903.json",
                "score": 5,
                "size_bytes": 45322,
                "role": "music_context_json"
              }
            ],
            "blender_keyframes_json": [
              {
                "path": "output/validation/md_code_coherence_report_current.json",
                "score": 25,
                "size_bytes": 581441,
                "role": "blender_keyframes_json"
              },
              {
                "path": "output/validation/md_code_coherence_report_semantic_current.json",
                "score": 25,
                "size_bytes": 597481,
                "role": "blender_keyframes_json"
              },
              {
                "path": "output/validation/md_code_coherence_report_semantic_v8_current.json",
                "score": 25,
                "size_bytes": 515888,
                "role": "blender_keyframes_json"
              },
              {
                "path": "output/ai_context_packs/full_context_golden_core_ai_backend.json",
                "score": 5,
                "size_bytes": 45075,
                "role": "blender_keyframes_json"
              },
              {
                "path": "output/ai_context_packs/full_context_golden_selected_chunks.json",
                "score": 5,
                "size_bytes": 56392,
                "role": "blender_keyframes_json"
              },
              {
                "path": "output/ai_context_packs/unified_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_context_pack_full_access_md_telemetry_20260506-154554.json",
                "score": 5,
                "size_bytes": 45308,
                "role": "blender_keyframes_json"
              },
              {
                "path": "output/ai_context_packs/unified_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_context_pack_gpu0_companion_full0to10_quick_20260506-191903.json",
                "score": 5,
                "size_bytes": 45322,
                "role": "blender_keyframes_json"
              },
              {
                "path": "output/ai_context_packs/unified_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_context_pack_gpu0_full0to10_quick_20260506-180824.json",
                "score": 5,
                "size_bytes": 45300,
                "role": "blender_keyframes_json"
              }
            ]
          },
          "missing_roles": [],
          "errors": [],
          "warnings": [],
          "policy": {
            "missing_inputs_default": "warning",
            "missing_inputs_when_require_inputs": "error",
            "template_generated": true,
            "no_blender_runtime": true,
            "no_provider_execution": true
          },
          "provider_execution_performed": false,
          "patch_application_performed": false,
```

## Context after

          "source_writes_performed": false,
          "persistent_memory_write_performed": false,
          "blender_runtime_execution_performed": false,
          "ffmpeg_execution_performed": false
        }
      },
      "track_input_template": {
        "path": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/track_inputs/full0to10_track_input_template.json",
        "exists": true,
        "type": "json",
        "required": false,
        "size_bytes": 1056,
