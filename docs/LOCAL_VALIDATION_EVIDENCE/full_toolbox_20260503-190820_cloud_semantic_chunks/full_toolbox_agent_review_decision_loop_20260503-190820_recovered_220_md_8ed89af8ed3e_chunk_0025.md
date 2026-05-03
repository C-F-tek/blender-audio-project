# Evidence Chunk 0025/0041

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md`
- source_sha256: `8ed89af8ed3e4fa6f8a1a3a56da19fd97a274354793464078ec9f92deaf33e83`
- line_start: `2790`
- line_end: `2942`
- section_kinds: `['markdown_heading_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0024.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0026.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: definire la gestione delle referenze esterne e le linee guida per l’uso di un “reference layer” all’interno del repository, garantendo coerenza e sicurezza per gli agenti AI cloud.  

**Segnali principali**: il layer non è un duplicato di OpenVINO, ONNX Runtime, Guardrails, ecc.; non sostituisce la validazione locale, non è dipendenza runtime, non autorizza modifiche distruttive e non bypassa AGENTS.md o i piani di esecuzione.  

**Guardrail / errori**: i repository esterni devono rimanere

## Context before

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

## Chunk content

````md
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
          "doc": "docs/AI_REFERENCE_SOURCE_MAP.md",
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
              "path": "docs/AI_REFERENCE_SOURCE_MAP.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 3956,
              "lines": 94,
              "matched_terms": [
                "docs/external_references",
                "docs/external_references"
              ],
              "snippet": "command;\n- a package README update;\n- a documented execution plan.\n\n### 4. Keep AI instructions compact\n\nLarge instructions degrade agent reliability. Long background belongs in `docs/`; immediate rules belong in `AGENTS.md` and package-level README files.\n\n### 5. Prefer provider-agnostic architecture\n\nThe project may use OpenVINO, Ollama, OpenAI-compatible endpoints or local Python tools, but orchestration should avoid hard-coding one provider into core logic.\n\n## Local reference folders\n\nOptional local-only folders:\n\n```text\ndocs/external_references/\ndocs/references/\n```\n\nSuggested `.gitignore` entries if those folders are used:\n\n```gitignore\ndocs/external_references/\ndocs/references/\n```\n\n## Maintenance rules\n\nWhen adding a new reference:\n\n1. add it to this source map;\n2. explain why it matters to this repository;\n3. map it to concrete local files;\n4. avoid copying large upstream content;\n5. add or update a validator when the rule is enforceable;\n6. update `docs/README.md` if the new document is stable.\n"
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
          "doc": "docs/AI_REFERENCE_SOURCE_MAP.md",
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
              "path": "docs/AI_REFERENCE_SOURCE_MAP.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 3956,
              "lines": 94,
              "matched_terms": [
                "docs/references",
                "docs/references"
              ],
              "snippet": "E update;\n- a documented execution plan.\n\n### 4. Keep AI instructions compact\n\nLarge instructions degrade agent reliability. Long background belongs in `docs/`; immediate rules belong in `AGENTS.md` and package-level README files.\n\n### 5. Prefer provider-agnostic architecture\n\nThe project may use OpenVINO, Ollama, OpenAI-compatible endpoints or local Python tools, but orchestration should avoid hard-coding one provider into core logic.\n\n## Local reference folders\n\nOptional local-only folders:\n\n```text\ndocs/external_references/\ndocs/references/\n```\n\nSuggested `.gitignore` entries if those folders are used:\n\n```gitignore\ndocs/external_references/\ndocs/references/\n```\n\n## Maintenance rules\n\nWhen adding a new reference:\n\n1. add it to this source map;\n2. explain why it matters to this repository;\n3. map it to concrete local files;\n4. avoid copying large upstream content;\n5. add or update a validator when the rule is enforceable;\n6. update `docs/README.md` if the new document is stable.\n"
            },
            {
              "path": "docs/references",
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
          "doc": "docs/CODE_CONSULTATION_REPORT.md",
          "reference": "github/workflows/code-quality.yml",
          "candidate_references": [
            "github/workflows/code-quality.yml",
            "github/workflows/code-quality.yml"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/CODE_CONSULTATION_REPORT.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 8873,
              "lines": 267,
              "matched_terms": [
                "github/workflows/code-quality.yml",
                "github/workflows/code-quality.yml",
                "github/workflows/code-quality.yml"
              ],
              "snippet": "ty check was launched.\n\nThe review is non-destructive. No working Blender script was refactored or modified.\n\n## Repository status\n\n- Repository: `C-F-tek/blender-audio-project`\n- Default branch: `master`\n- Visibility: private\n- GitHub App permissions observed: admin, maintain, pull, push, triage\n- Repository size observed: about 2564 KB\n\n## Code quality workflow visibility\n\nNo workflow run was visible through the available GitHub connector for the checked commits.\n\nThe following common workflow paths were not found:\n\n```text\n.github/workflows/code-quality.yml\n.github/workflows/code_quality.yml\n.github/workflows/ci.yml\n```\n\nThis means that the code-quality action may be external, not indexed through the available API endpoint, manually launched in a way not returned by commit workflow lookup, or not yet committed as a workflow file.\n\n## Source index consulted\n\nThe main source index consulted was:\n\n```text\nindexAI/project_code_index.md\nindexAI/project_code_manifest.json\n```\n\nThe index reports:\n\n- 98 indexed files\n- 212 code chunks\n- generated timestamp: `2026-04-27T14:41:27`\n\nImportant: this index predates the latest documentation and template additions. It should be regenerated.\n\n## Main code areas\n\n### Root tools\n\n| File | Role | Assessment |\n|---|---|---|\n| `analyze_wav.py` | WAV analysis, low/mid/high/onset/beat extraction, Blender JSON generation | Good functional core. Needs dependency documentation and optional validation. |\n| `build_track_summary.py` | Compact summary builder from analysis JSON | Useful, but default paths are track-specific. Should be made more gener"
            },
            {
              "path": "github/workflows/code-quality.yml",
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
          "doc": "docs/CODE_CONSULTATION_REPORT.md",
          "reference": "github/workflows/code_quality.yml",
          "candidate_references": [
            "github/workflows/code_quality.yml",
            "github/workflows/code_quality.yml"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/CODE_CONSULTATION_REPORT.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 8873,
              "lines": 267,
              "matched_terms": [
                "github/workflows/code_quality.yml",
                "github/workflows/code_quality.yml",
                "github/workflows/code_quality.yml"
              ],
              "snippet": "is non-destructive. No working Blender script was refactored or modified.\n\n## Repository status\n\n- Repository: `C-F-tek/blender-audio-project`\n- Default branch: `master`\n- Visibility: private\n- GitHub App permissions observed: admin, maintain, pull, push, triage\n- Repository size observed: about 2564 KB\n\n## Code quality workflow visibility\n\nNo workflow run was visible through the available GitHub connector for the checked commits.\n\nThe following common workflow paths were not found:\n\n```text\n.github/workflows/code-quality.yml\n.github/workflows/code_quality.yml\n.github/workflows/ci.yml\n```\n\nThis means that the code-quality action may be external, not indexed through the available API endpoint, manually launched in a way not returned by commit workflow lookup, or not yet committed as a workflow file.\n\n## Source index consulted\n\nThe main source index consulted was:\n\n```text\nindexAI/project_code_index.md\nindexAI/project_code_manifest.json\n```\n\nThe index reports:\n\n- 98 indexed files\n- 212 code chunks\n- generated timestamp: `2026-04-27T14:41:27`\n\nImportant: this index predates the latest documentation and template additions. It should be regenerated.\n\n## Main code areas\n\n### Root tools\n\n| File | Role | Assessment |\n|---|---|---|\n| `analyze_wav.py` | WAV analysis, low/mid/high/onset/beat extraction, Blender JSON generation | Good functional core. Needs dependency documentation and optional validation. |\n| `build_track_summary.py` | Compact summary builder from analysis JSON | Useful, but default paths are track-specific. Should be made more generic or documented as local defaults."
````

## Context after

            },
            {
              "path": "github/workflows/code_quality.yml",
              "exist
```

### `output/ai_pipeline/full_toolbox_20260503-190820_bridge_orchestrator_recovered_220.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `37585`
