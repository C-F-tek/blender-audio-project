# Code Consultation Report

## Scope

This report summarizes a broad code consultation of `blender-audio-project` after the GitHub code-quality check was launched.

The review is non-destructive. No working Blender script was refactored or modified.

## Repository status

- Repository: `C-F-tek/blender-audio-project`
- Default branch: `master`
- Visibility: private
- GitHub App permissions observed: admin, maintain, pull, push, triage
- Repository size observed: about 2564 KB

## Code quality workflow visibility

No workflow run was visible through the available GitHub connector for the checked commits.

The following common workflow paths were not found:

```text
.github/workflows/code-quality.yml
.github/workflows/code_quality.yml
.github/workflows/ci.yml
```

This means that the code-quality action may be external, not indexed through the available API endpoint, manually launched in a way not returned by commit workflow lookup, or not yet committed as a workflow file.

## Source index consulted

The main source index consulted was:

```text
indexAI/project_code_index.md
indexAI/project_code_manifest.json
```

The index reports:

- 98 indexed files
- 212 code chunks
- generated timestamp: `2026-04-27T14:41:27`

Important: this index predates the latest documentation and template additions. It should be regenerated.

## Main code areas

### Root tools

| File | Role | Assessment |
|---|---|---|
| `analyze_wav.py` | WAV analysis, low/mid/high/onset/beat extraction, Blender JSON generation | Good functional core. Needs dependency documentation and optional validation. |
| `build_track_summary.py` | Compact summary builder from analysis JSON | Useful, but default paths are track-specific. Should be made more generic or documented as local defaults. |
| `normalize_scene_spec.py` | Scene-spec normalization | Useful, but contains duplicated helper function definitions that should be reviewed. |

### Blender package area

| Area | Role | Assessment |
|---|---|---|
| `Scripting/v61b/` | Main complex reference package | Strong reference model. Do not refactor broadly without Blender tests. |
| `Scripting/v61b_backgood/` | Backup or previous-good version | Useful safety copy, but should be documented as backup/reference. |
| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/` | Additional generated package | Should be compared with v61b standards and documented per package. |
| `Scripting/_template_audio_reactive_package/` | New package template | Good structure. Not part of old index yet. |
| `Scripting/shared/` | Shared utility target area | Policy exists; code extraction is intentionally pending. |

### AI and NPU tooling

| Area | Role | Assessment |
|---|---|---|
| `Tools/npu/` | Local AI, NPU, context generation, dual AI pipeline | Rich but complex. Needs validation and clearer CLI documentation. |
| `Tools/workflow/` | Workflow shell, GUI, state, startup and debugging tools | Large operational layer. Needs its own workflow documentation and validation. |
| `Tools/repo_patch_runner/` | Structured patch runner | Relevant for safe local patch workflows. |
| `indexAI/` | Generated index and patch artifacts | Valuable but generated. Must be regenerated after structural changes. |

## Detailed observations

### 1. Root tools are functional but partly workstation-specific

`analyze_wav.py` is configurable through CLI arguments and produces full analysis JSON, Blender keyframe JSON alias, diagnostic PNG, and optional NPU/music context.

`build_track_summary.py` is CLI-driven but still has default constants tied to a specific track under `output/`.

Recommendation:

- Keep CLI arguments as source of truth.
- Document default paths as local defaults.
- Add a root tools guide.

### 2. `normalize_scene_spec.py` has duplicated helpers

The file defines `safe_scene_name` and `safe_visual_concept` twice. The definitions are equivalent or near-equivalent, but duplication increases maintenance risk.

Recommendation:

- Do not change it blindly.
- Add a targeted cleanup task only after a simple regression test is available.

### 3. `Scripting/v61b/` is the strongest reference implementation

The package is modular and includes:

- `main_v61b.py`
- `config.py`
- `animation.py`
- `asset_setup.py`
- `atmosphere_setup.py`
- `camera_setup.py`
- `materials.py`
- `physics_setup.py`
- `render_setup.py`
- `world_setup.py`
- `scene_tuning_panel.py`
- encode helpers
- hotpatch utilities
- `spaziotempo/` subpackage

This package should remain the quality reference.

Recommendation:

- Do not refactor destructively.
- Extract reusable utilities only additively into `Scripting/shared/`.
- Use v61b as a style and complexity reference for future packages.

### 4. `scene_tuning_panel.py` is powerful but large

The tuning panel is a strong candidate for future shared abstractions, but it is also scene-specific.

Good shared candidates:

- runtime profile normalization;
- render profile application pattern;
- panel/operator layout patterns;
- encode/hot-update invocation pattern.

Package-specific logic should remain local when tied to scene object names, material names, or project-specific controls.

### 5. FFmpeg helpers are good shared candidates

`encode_ffmpeg_v61b.py` includes useful operational logic:

- FFmpeg executable discovery;
- image sequence detection;
- contiguous frame detection;
- audio offset handling;
- CPU/GPU profile generation;
- BT.709 color metadata;
- visible shell launcher.

Recommendation:

- Extract a new shared copy to `Scripting/shared/ffmpeg_encoder.py` later.
- Do not update v61b to consume it until tested.

### 6. `Tools/npu/run_dual_ai_pipeline.py` is central but complex

The dual AI pipeline coordinates music context, code context, Blender manual context, NPU preflight, Ollama runtime, implementation drafts, validation, and generated scene scripts.

Recommendation:

- Add a CLI usage guide for `Tools/npu/`.
- Add smoke validation for required inputs.
- Split only if tests or usage docs exist; do not refactor blindly.

### 7. Generated indexes are stale

The index was created before recent additions:

- new docs;
- package template;
- shared folder policy;
- quality gates;
- project audit.

Recommendation:

Regenerate:

```text
indexAI/project_code_index.md
indexAI/project_code_manifest.json
Tools/npu/npu_code_index.md
Tools/npu/npu_code_manifest.json
```

### 8. Code quality automation is not committed as a visible workflow

The repository does not currently expose common workflow files for code quality in `.github/workflows/`.

Recommendation:

Add a non-invasive workflow later for:

- Python syntax compile check;
- optional ruff linting;
- documentation link/path sanity checks;
- package structure validation.

Do not require Blender runtime in the first workflow.

## Risk matrix

| Risk | Level | Reason | Recommended action |
|---|---|---|---|
| Breaking v61b through refactor | High | v61b is complex and working-reference code | Only additive extraction and Blender tests. |
| Stale AI index | Medium | New files are not represented | Regenerate indexes. |
| Hardcoded local paths | Medium | Several tools use `Path.home() / "blender"` defaults | Keep CLI overrides and document defaults. |
| Missing CI visibility | Medium | Code quality not visible as committed workflow | Add lightweight workflow. |
| JSON schema drift | Medium | Multiple JSON artifacts and compact/full variants | Document confirmed schemas. |
| Large script complexity | Medium | Several files exceed hundreds or thousands of lines | Add validation before refactor. |
| Duplicate helpers in normalize_scene_spec | Low/Medium | Maintainer confusion and possible drift | Clean only with regression check. |

## Recommended next actions

### Priority 1

Regenerate project indexes so AI tools can see the new structure.

### Priority 2

Create `docs/ROOT_TOOLS.md` for:

- `analyze_wav.py`
- `build_track_summary.py`
- `normalize_scene_spec.py`

### Priority 3

Add `Tools/validation/` with non-invasive checks:

```text
Tools/validation/check_python_syntax.py
Tools/validation/check_package_structure.py
Tools/validation/check_docs_paths.py
```

### Priority 4

Add a minimal `.github/workflows/code-quality.yml` that runs syntax and structure checks only. Do not require Blender.

### Priority 5

Plan additive shared utility extraction:

```text
Scripting/shared/path_utils.py
Scripting/shared/ffmpeg_encoder.py
Scripting/shared/render_profiles.py
```

## Conclusion

The repository is now well structured for AI-assisted development, but the next maturity step is automated validation.

The safest path is:

```text
regenerate indexes
  -> add validation tools
  -> add GitHub workflow
  -> document root tools
  -> extract shared utilities additively
```

No broad refactor of working Blender packages should be performed before these validation layers exist.
