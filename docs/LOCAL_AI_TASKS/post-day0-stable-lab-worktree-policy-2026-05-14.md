# Post Day 0 stable/lab worktree policy

Generated: 2026-05-14

## Purpose

This document records the local operating rule adopted after the Day 0 heap lab baseline.

The repository must be used with two separate local worktrees/clones:

- a stable production/reference checkout on `master`;
- a lab checkout for PR and AI/Codex experimentation.

This prevents experimental PR state, generated artifacts, temporary launchers, smoke fixtures, AI-generated code products, and local trial patches from contaminating the stable Blender/audio project checkout.

## Stable checkout

Path:

```text
C:\Users\carmi\blender\blender-audio-project
```

Required branch:

```text
master
```

Role:

- stable local baseline;
- normal project work only;
- no destructive PR experiments;
- no dirty AI/Codex trial state;
- no local lab-only generated launcher files;
- no PR branch reset/testing unless explicitly intended.

The stable checkout must track `origin/master` and must contain the Day 0 baseline merge commit from PR #300, or a later `master` commit that includes it.

Known Day 0 baseline commit:

```text
4ef07a90a07853a04b326567254991321b2b8df4
```

## Lab checkout

Path:

```text
C:\Users\carmi\ProjectsDir\blender-audio-project
```

Current lab branch for PR #301:

```text
codex/code-product-intake
```

Role:

- PR work;
- AI/Codex runs;
- experimental launcher work;
- resettable validation lab;
- generated local artifacts;
- destructive clean/retry cycles when needed.

The lab checkout may be force-aligned to the remote PR branch using `git reset --hard` and `git clean`, because it is intentionally disposable except for explicitly committed work.

## Expected sync behavior

During lab sync, Git may first show modified tracked files or untracked files, for example:

```text
M ia_carmine/README.md
M config/allowlist.json
Removing ia_carmine/operator_product_launcher.py
```

This is expected when the lab contains residue from previous runs.

The authoritative state is reached only after:

```powershell
git reset --hard origin/codex/code-product-intake
git clean -fd -e .venv/
```

After these commands, `git status --short` must be empty.

## Stable sync procedure

Run this only in the stable checkout:

```powershell
$ErrorActionPreference = 'Stop'

$StableRepo = 'C:\Users\carmi\blender\blender-audio-project'
$PR300Merge = '4ef07a90a07853a04b326567254991321b2b8df4'
$PR301Head = '2b5b374103b5c161ae56410006aff0a2ed19efc3'

cd $StableRepo

git fetch origin --prune
git fetch origin master

git switch master
git reset --hard origin/master
git clean -fd -e .venv/

$StableHead = git rev-parse HEAD
$StableBranch = git branch --show-current
$StableDirty = git status --short

if ($StableDirty) {
  git status --short
  throw 'ERRORE: repo stabile sporca dopo sync.'
}

git merge-base --is-ancestor $PR300Merge HEAD
if ($LASTEXITCODE -ne 0) {
  throw 'ERRORE: master stabile non contiene il merge commit PR #300.'
}

if ($StableHead -eq $PR301Head) {
  throw 'ERRORE: repo stabile e finita sulla PR #301. Stop.'
}

Write-Host 'OK stabile'
Write-Host "Branch: $StableBranch"
Write-Host "HEAD:   $StableHead"
git log -1 --oneline
git status --short
```

## Lab sync procedure

Run this for the PR #301 lab checkout:

```powershell
$ErrorActionPreference = 'Stop'

$RepoUrl = 'https://github.com/C-F-tek/blender-audio-project.git'
$LabRepo = 'C:\Users\carmi\ProjectsDir\blender-audio-project'
$PR301Branch = 'codex/code-product-intake'
$PR301Head = '2b5b374103b5c161ae56410006aff0a2ed19efc3'

$LabParent = Split-Path -Parent $LabRepo
New-Item -ItemType Directory -Force -Path $LabParent | Out-Null

if (-not (Test-Path -LiteralPath $LabRepo)) {
  git clone $RepoUrl $LabRepo
}

cd $LabRepo

if (-not (Test-Path -LiteralPath '.git')) {
  throw "ERRORE: LabRepo esiste ma non e una repo Git: $LabRepo"
}

git fetch origin --prune
git fetch origin $PR301Branch

git switch -C $PR301Branch origin/$PR301Branch
git reset --hard origin/$PR301Branch
git clean -fd -e .venv/

$LabHead = git rev-parse HEAD
$LabBranch = git branch --show-current
$LabDirty = git status --short

if ($LabHead -ne $PR301Head) {
  throw 'ERRORE: lab non e sulla head attesa della PR #301.'
}

if ($LabDirty) {
  git status --short
  throw 'ERRORE: lab sporco dopo sync PR #301.'
}

Write-Host 'OK lab PR #301'
Write-Host "Branch: $LabBranch"
Write-Host "HEAD:   $LabHead"
git log -1 --oneline
git status --short
```

## Operating rule

Use the stable checkout for stable project work.
Use the lab checkout for PR branches, AI-generated code product testing, launcher experiments, validation retries, and destructive clean/reset cycles.

Do not run experimental PR workflows inside the stable checkout unless explicitly intended.
