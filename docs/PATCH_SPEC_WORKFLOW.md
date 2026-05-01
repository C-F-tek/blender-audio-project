# Patch Spec Workflow

## Purpose

This document explains the repository patch-spec workflow used by `blender-audio-project`.

The workflow allows small, reviewable file modifications to be described as JSON specs, validated with a dry run, applied safely, shown as a Git diff, and optionally queued for automatic application by GitHub Actions.

## Main files

| Path | Role |
|---|---|
| `Tools/repo_patch_runner/apply_repo_mods.py` | Safe repository patch runner. |
| `Tools/ai/build_patch_specs_from_proposals.py` | Builds inert proposal-derived draft specs under `output/patch_specs/`. |
| `Tools/validation/check_patch_spec_drafts.py` | Validates draft specs before any review-to-concrete promotion. |
| `Tools/ai/promote_patch_spec_draft.py` | Promotes one draft plus an explicit replacement plan into a reviewed dry-run-passing spec. |
| `Tools/validation/check_reviewed_patch_specs.py` | Revalidates reviewed specs and reruns dry-run without applying patches. |
| `output/patch_specs/` | Ignored local workspace for generated draft patch specs. |
| `patch_specs/inbox/` | Queue of patch specs waiting to be applied. |
| `patch_specs/applied/` | Patch specs already applied by the GitHub Action. |
| `patch_specs/README.md` | Existing quick workflow notes. |
| `.github/workflows/apply_repo_mods.yml` | GitHub Action that applies queued specs on push or manual dispatch. |

## What the runner does

`Tools/repo_patch_runner/apply_repo_mods.py` can:

- read a JSON patch spec;
- validate paths stay inside the repository root;
- remove UTF-8 BOM when present;
- apply exact replacements;
- apply regex replacements;
- insert text before or after anchors;
- validate required strings before and after patching;
- validate forbidden strings before and after patching;
- check expected line-count deltas;
- create backups unless disabled;
- print line counts before/after;
- show `git diff` after applying changes.

## Local dry run

Always dry-run first:

```powershell
python .\Tools\repo_patch_runner\apply_repo_mods.py --spec .\patch_specs\inbox\example.json --dry-run
```

## Local apply with diff

Apply locally and print diff:

```powershell
python .\Tools\repo_patch_runner\apply_repo_mods.py --spec .\patch_specs\inbox\example.json --write --show-diff
```

Apply locally without backup when the patch is generated and already reviewed:

```powershell
python .\Tools\repo_patch_runner\apply_repo_mods.py --spec .\patch_specs\inbox\example.json --write --no-backup --show-diff
```

## GitHub Action queue

The Action watches:

```text
patch_specs/inbox/*.json
```

When a spec is pushed to `master`, the workflow:

1. collects specs from `patch_specs/inbox/`;
2. runs dry-run;
3. applies with `--write --no-backup --show-diff`;
4. moves the spec to `patch_specs/applied/`;
5. commits the resulting file changes with message:

```text
Apply repo patch specs
```

Manual dispatch is also supported through the `spec_path` input.

## Minimal spec format

```json
{
  "version": 1,
  "description": "Short description of the patch",
  "operations": [
    {
      "path": "relative/path/file.md",
      "replacements": [
        {
          "type": "exact",
          "old": "old text",
          "new": "new text",
          "count": 1
        }
      ],
      "require_contains_after": ["new text"],
      "forbid_contains_after": ["old text"]
    }
  ]
}
```

## Supported replacement types

### exact

```json
{
  "type": "exact",
  "old": "old text",
  "new": "new text",
  "count": 1
}
```

### regex

```json
{
  "type": "regex",
  "pattern": "old\\s+pattern",
  "new": "new text",
  "count": 1,
  "flags": ["MULTILINE"]
}
```

Supported regex flags:

```text
MULTILINE
DOTALL
IGNORECASE
```

### insert_after

```json
{
  "type": "insert_after",
  "anchor": "existing text",
  "insert": "\nnew inserted text\n",
  "count": 1
}
```

### insert_before

```json
{
  "type": "insert_before",
  "anchor": "existing text",
  "insert": "new inserted text\n",
  "count": 1
}
```

## Validation fields

Use these fields to make patches safe:

| Field | Meaning |
|---|---|
| `require_contains_before` | Strings that must exist before the patch. |
| `forbid_contains_before` | Strings that must not exist before the patch. |
| `require_contains_after` | Strings that must exist after the patch. |
| `forbid_contains_after` | Strings that must not exist after the patch. |
| `expected_line_delta` | Exact line-count delta expected for the operation. |

## Recommended use cases

Good use cases:

- documentation edits;
- replacing repeated text blocks;
- adding small sections to README files;
- targeted config corrections;
- mechanical edits with stable anchors;
- AI-generated patch proposals that require deterministic validation.

Avoid patch specs for:

- large code rewrites;
- artistic Blender scene behavior changes;
- patches requiring runtime reasoning;
- binary files;
- generated full frame-by-frame analysis JSON files.

## AI usage policy

AI agents may generate patch specs when:

- the change is small;
- the target anchor is explicit;
- before/after validation strings are included;
- the patch can be dry-run before application;
- line count and diff can be reviewed.

AI agents should not push queued specs without human approval.

## Proposal-derived draft specs

Validated repository proposals can be converted into draft patch-spec shells:

```powershell
python .\Tools\ai\build_patch_specs_from_proposals.py --repo-root . --proposal .\output\ai_pipeline\repository_change_proposals.json --output-dir output\patch_specs --basename proposal_patch_specs
python .\Tools\validation\check_patch_spec_drafts.py --repo-root . --manifest .\output\patch_specs\proposal_patch_specs_manifest.json --output .\output\validation\patch_spec_drafts.json
```

These drafts are intentionally inert:

- they live under ignored `output/patch_specs/`;
- they contain target operations and review metadata;
- they contain empty `replacements` lists;
- they use `draft_status=needs_concrete_replacements`;
- they must not be copied into `patch_specs/inbox/` without a separate review step.

The draft validator rejects concrete replacements and queued inbox paths.

## Review-to-concrete promotion

Promotion from draft to a concrete reviewed spec requires a separate replacement plan:

```powershell
python .\Tools\ai\promote_patch_spec_draft.py --repo-root . --draft .\Tools\ai\fixtures\patch_spec_review_draft.json --replacement-plan .\Tools\ai\fixtures\patch_spec_review_replacement_plan.json --output-dir output\patch_specs --basename reviewed_patch_spec_fixture
python .\Tools\validation\check_reviewed_patch_specs.py --repo-root . --manifest .\output\patch_specs\reviewed_patch_spec_fixture_manifest.json --output .\output\validation\reviewed_patch_specs.json
```

The promotion tool:

- reads a draft spec and a replacement plan;
- requires replacement operations to target files already listed in the draft;
- writes a `reviewed_patch_spec` under ignored `output/patch_specs/`;
- runs `apply_repo_mods.py` in dry-run mode through the shared runner code;
- refuses reviewed specs whose dry-run does not change at least one target;
- never uses `--write` and never writes `patch_specs/inbox/`.

Reviewed specs are still not queued patches. Choosing local apply or GitHub Action queue remains a separate explicit step after human or trusted-agent approval.

## Local workflow for AI-assisted patching

```powershell
# 1. create patch spec under patch_specs/inbox/
python .\Tools\repo_patch_runner\apply_repo_mods.py --spec .\patch_specs\inbox\my_patch.json --dry-run

# 2. apply locally when dry-run is clean
python .\Tools\repo_patch_runner\apply_repo_mods.py --spec .\patch_specs\inbox\my_patch.json --write --show-diff

# 3. validate repository
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .

# 4. inspect and commit manually
git status
git diff --stat
git diff
```

## Remote queue workflow

```powershell
# create or copy a reviewed spec into patch_specs/inbox/
git add patch_specs/inbox/my_patch.json
git commit -m "queue repo patch spec"
git push origin master
```

The GitHub Action will apply the spec and create the final commit if the patch succeeds.

## Current recommendation

Use patch specs for mechanical documentation and validation-policy edits.

For source-code refactors, prefer normal commits unless the edit is small, exact and easy to validate.
