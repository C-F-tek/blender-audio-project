# Evidence Chunk 0024/0041

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md`
- source_sha256: `8ed89af8ed3e4fa6f8a1a3a56da19fd97a274354793464078ec9f92deaf33e83`
- line_start: `2574`
- line_end: `2789`
- section_kinds: `['markdown_heading_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_chunk_0023.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_chunk_0025.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Valutare la sufficienza delle prove per l’aggiornamento manuale delle referenze documentali all’interno del progetto

## Context before

## By phase


## By tool


## First tool call entries



```


## Chunk content

````md
### `output/ai_pipeline/agent_review_evidence_sufficiency.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `35905`
- SHA-256: `a2216b89a69fc267b8015cfcbf775591b4c8b05abd127aef322936947f80683c`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_review_evidence_sufficiency",
  "generated_at": "2026-05-01T17:46:48",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_evidence_sufficiency",
  "inputs": {
    "refined_review": "output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_review_v3.json",
    "refined_proposals": "output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_proposals_v3.json",
    "refined_proposal_count": 2,
    "context_reports": [
      {
        "path": "output/ai_pipeline/local_ai_core_tool_activation_agent_memory_inventory.json",
        "exists": true,
        "kind": "agent_memory_inventory",
        "passed": true,
        "error": "",
        "summary": {}
      },
      {
        "path": "output/ai_pipeline/local_ai_core_tool_activation_agnostic_tool_inventory.json",
        "exists": true,
        "kind": "agent_agnostic_tool_inventory",
        "passed": true,
        "error": "",
        "summary": {
          "tool_count": 166,
          "category_counts": {
            "validator": 50,
            "provider_probe_or_adapter": 41,
            "orchestrator_pipeline": 30,
            "support_tool": 28,
            "agent_context_builder": 6,
            "proposal_or_review_builder": 5,
            "git_helper": 3,
            "review_helper": 3
          },
          "owner_lane_counts": {
            "npu_explicit_provider_tool": 65,
            "cpu_validation": 29,
            "gpu_cuda_explicit_provider_tool": 27,
            "cpu_support": 22,
            "cpu_orchestration": 18,
            "cpu_context_builder": 3,
            "cpu_proposal_builder": 2
          },
          "consumed_lane_counts": {
            "cpu": 166,
            "npu": 123,
            "gpu_cuda": 89
          },
          "apply_mode_counts": {
            "not_declared": 121,
            "manual_review_only": 20,
            "report_only": 16,
            "explicit_git_operation": 9
          },
          "provider_execution_default_counts": {
            "none_or_reported": 151,
            "explicit_only": 15
          }
        }
      },
      {
        "path": "output/ai_pipeline/local_ai_core_tool_activation_transient_request_context.json",
        "exists": true,
        "kind": "agent_transient_request_context",
        "passed": true,
        "error": "",
        "summary": {}
      }
    ]
  },
  "areas": {
    "doc_code": {
      "area": "doc_code",
      "item_count": 9,
      "ready_for_manual_patch_count": 9,
      "needs_more_context_count": 0,
      "items": [
        {
          "doc": "docs/AI_ONBOARDING.md",
          "reference": "Scripting/shared/config_model.py",
          "candidate_references": [
            "Scripting/shared/config_model.py"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/AI_ONBOARDING.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 5329,
              "lines": 115,
              "matched_terms": [
                "Scripting/shared/config_model.py",
                "Scripting/shared/config_model.py"
              ],
              "snippet": " still needing staged decomposition. |\n| `Tools/npu/pipeline/` | Additive app-agnostic helper package exists on the NPU decomposition branch; it is not wired into the runtime orchestrator until local validation and index regeneration pass. |\n| `indexAI/` | Generated AI context. Regenerate after structural or documentation changes; do not hand-refactor as source. |\n| JSON schemas | Documented as partial. Preserve unknown fields and avoid destructive normalization. |\n\nNot yet complete:\n\n```text\nScripting/shared/blender_compat.py\nScripting/shared/config_model.py\nScripting/shared/diagnostics.py\nruntime adoption of Tools/npu/pipeline/ helpers inside Tools/npu/run_dual_ai_pipeline.py\nfull production JSON schemas\nautomated Blender runtime validation\n```\n\n## First-session checklist\n\nRun only lightweight inspection first:\n\n```powershell\ngit status --short\ngit remote -v\nGet-ChildItem -File .\\docs\nGet-ChildItem -Directory .\\Scripting\nGet-ChildItem -File .\\Scripting\\shared\n```\n\nBefore code changes, run the smallest relevant validation:\n\n```powershell\npython .\\Tools\\validation\\check_python_syntax.py --repo-root .\npython .\\Tools\\validation\\check_package_structure.py --repo-root .\npython .\\Tools\\validation\\check_json_artifacts.py --repo-root .\n```\n\nFor NPU helper work, run the focused helper validation before the full runner:\n\n```powershell\npowershell.exe -ExecutionPolicy Bypass -File .\\Tools\\workflow\\run_npu_pipeline_helper_validation.ps1\n```\n\nFor documentation-only changes, a path/link review and `git diff` may be enough unless generated indexes must be refreshed.\n\n## Common traps\n\n- Do"
            },
            {
              "path": "Scripting/shared/config_model.py",
              "exists": false,
              "kind": "target_path",
              "chars": 0,
              "lines": 0,
              "matched_terms": [],
              "snippet": ""
            }
          ]
        },
        {
          "doc": "docs/AI_ONBOARDING.md",
          "reference": "Scripting/shared/diagnostics.py",
          "candidate_references": [
            "Scripting/shared/diagnostics.py"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/AI_ONBOARDING.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 5329,
              "lines": 115,
              "matched_terms": [
                "Scripting/shared/diagnostics.py",
                "Scripting/shared/diagnostics.py"
              ],
              "snippet": "on. |\n| `Tools/npu/pipeline/` | Additive app-agnostic helper package exists on the NPU decomposition branch; it is not wired into the runtime orchestrator until local validation and index regeneration pass. |\n| `indexAI/` | Generated AI context. Regenerate after structural or documentation changes; do not hand-refactor as source. |\n| JSON schemas | Documented as partial. Preserve unknown fields and avoid destructive normalization. |\n\nNot yet complete:\n\n```text\nScripting/shared/blender_compat.py\nScripting/shared/config_model.py\nScripting/shared/diagnostics.py\nruntime adoption of Tools/npu/pipeline/ helpers inside Tools/npu/run_dual_ai_pipeline.py\nfull production JSON schemas\nautomated Blender runtime validation\n```\n\n## First-session checklist\n\nRun only lightweight inspection first:\n\n```powershell\ngit status --short\ngit remote -v\nGet-ChildItem -File .\\docs\nGet-ChildItem -Directory .\\Scripting\nGet-ChildItem -File .\\Scripting\\shared\n```\n\nBefore code changes, run the smallest relevant validation:\n\n```powershell\npython .\\Tools\\validation\\check_python_syntax.py --repo-root .\npython .\\Tools\\validation\\check_package_structure.py --repo-root .\npython .\\Tools\\validation\\check_json_artifacts.py --repo-root .\n```\n\nFor NPU helper work, run the focused helper validation before the full runner:\n\n```powershell\npowershell.exe -ExecutionPolicy Bypass -File .\\Tools\\workflow\\run_npu_pipeline_helper_validation.ps1\n```\n\nFor documentation-only changes, a path/link review and `git diff` may be enough unless generated indexes must be refreshed.\n\n## Common traps\n\n- Do not assume every status document"
            },
            {
              "path": "Scripting/shared/diagnostics.py",
              "exists": false,
              "kind": "target_path",
              "chars": 0,
              "lines": 0,
              "matched_terms": [],
              "snippet": ""
            }
          ]
        },
        {
          "doc": "docs/AI_REFERENCE_ONBOARDING.md",
          "reference": "docs/external_references",
          "candidate_references": [
            "docs/external_references"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/AI_REFERENCE_ONBOARDING.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 3909,
              "lines": 106,
              "matched_terms": [
                "docs/external_references",
                "docs/external_references"
              ],
              "snippet": "rnal repositories.\n\n## What this layer is not\n\nThis layer is not:\n\n- a complete mirror of OpenVINO, ONNX Runtime, Guardrails, Promptfoo, DeepEval, OpenAI Evals, AGENTS.md or MCP documentation;\n- a replacement for local validation;\n- a runtime dependency;\n- a permission to perform destructive changes;\n- a reason to bypass `AGENTS.md`, execution plans or validators.\n\n## Repository policy\n\nFull external repositories, if downloaded locally for study, should remain outside committed source or under ignored folders such as:\n\n```text\ndocs/external_references/\ndocs/references/\n```\n\nThe committed repository should contain only:\n\n```text\ndocs/AI_REFERENCE_ONBOARDING.md\ndocs/AI_REFERENCE_SOURCE_MAP.md\ndocs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md\ndocs/AI_GUARDRAILS_VALIDATION_GUIDE.md\ndocs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md\n```\n\nThis keeps remote AI agents effective without bloating the repository.\n\n## Recommended agent behavior\n\nWhen an AI agent uses this reference layer, it should:\n\n1. identify the target work area;\n2. read the related guide;\n3. map external concepts to existing project files;\n4. avoid introducing new dependencies unless explicitly approved;\n5. prefer additive documentation, validators and helper modules;\n6. preserve current Blender package behavior;\n7. keep NPU helper work provider-free unless a validated phase says otherwise;\n8. update `docs/README.md` when adding stable documentation;\n9. report uncertainty rather than inventing unsupported repository state.\n\n## Task routing\n\n| Task | Read first |\n|---|---|\n| AI artifact pipeline changes | `docs/AI_PROVIDER_AGNOSTIC_"
            },
            {
              "path": "docs/external_references",
              "exists": false,
              "kind": "target_path",
              "chars": 0,
              "lines": 0,
              "matched_terms": [],
              "snippet": ""
            }
          ]
        },
        {
          "doc": "docs/AI_REFERENCE_ONBOARDING.md",
          "reference": "docs/references",
          "candidate_references": [
            "docs/references"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/AI_REFERENCE_ONBOARDING.md",
````

## Context after

              "exists": true,
              "kind": "source_markdown",
              "chars": 3909,
              "lines": 106,
              "matched_terms": [
                "docs/references",
                "docs/references"
              ],
              "snippet": "t this layer is not\n\nThis layer is not:\n\n- a complete mirror of OpenVINO, ONNX Runtime, Guardrails, Promptfoo, DeepEval, OpenAI Evals, AGENTS.md or MCP documentation;\n- a replacement for local validation;\n- a runtime dependency;\n- a permission to perform destructive changes;\n- a reason to bypass `AGENTS.md`, execution plans or validators.\n\n## Repository policy\n\nFull external repositories, if downloaded locally for study, should remain outside committed source or under ignored folders such as:\n\n```text\ndocs/external_references/\ndocs/references/\n```\n\nThe committed repository should contain only:\n\n```text\ndocs/AI_REFERENCE_ONBOARDING.md\ndocs/AI_REFERENCE_SOURCE_MAP.md\ndocs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md\ndocs/AI_GUARDRAILS_VALIDATION_GUIDE.md\ndocs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md\n```\n\nThis keeps remote AI agents effective without bloating the repository.\n\n## Recommended agent behavior\n\nWhen an AI agent uses this reference layer, it should:\n\n1. identify the target work area;\n2. read the related guide;\n3. map external concepts to existing project files;\n4. avoid introducing new dependencies unless explicitly approved;\n5. prefer additive documentation, validators and helper modules;\n6. preserve current Blender package behavior;\n7. keep NPU helper work provider-free unless a validated phase says otherwise;\n8. update `docs/README.md` when adding stable documentation;\n9. report uncertainty rather than inventing unsupported repository state.\n\n## Task routing\n\n| Task | Read first |\n|---|---|\n| AI artifact pipeline changes | `docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md` |\n| NPU"
            },
            {
              "path": "docs/references",
