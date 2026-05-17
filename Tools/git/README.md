# Tools/git

Utilities for local Git automation used by the project application.

## Canonical entrypoint

Use the module dispatcher from the repository root:

```powershell
python -m Tools.git <tool> [native PowerShell args...]
```

Available tools:

```powershell
python -m Tools.git --list
```

The `.ps1` files under `_powershell/` are implementation files. Do not call
them directly from operator docs or automation.

## auto_push_generated_data

Script intended to be called after the local app regenerates technical data such as:

- `indexAI/` project indexes;
- `Tools/npu/context_artifacts/*.json` manifests;
- `Tools/npu/context_artifacts/*.md` generated context files;
- optional `output/*.json`, `output/*.md`, `output/*.txt` files;
- optional documentation updates.

## Basic usage

From repository root:

```powershell
python -m Tools.git auto_push_generated_data
```

## Dry run

```powershell
python -m Tools.git auto_push_generated_data -DryRun
```

## Include output JSON files

```powershell
python -m Tools.git auto_push_generated_data -IncludeOutputJson
```

## Include documentation updates

```powershell
python -m Tools.git auto_push_generated_data -IncludeDocs
```

## Include all generated allowlisted areas

```powershell
python -m Tools.git auto_push_generated_data -IncludeAllGenerated
```

## Pull before push

Use only when the local branch is expected to fast-forward cleanly:

```powershell
python -m Tools.git auto_push_generated_data -PullFirst
```

## Suggested app integration

After the application regenerates indexes or technical JSON files, it can call:

```powershell
python -m Tools.git auto_push_generated_data -IncludeOutputJson
```

or, if only `indexAI/` and `Tools/npu/` were updated:

```powershell
python -m Tools.git auto_push_generated_data
```

## Safety notes

- The script stages only allowlisted generated-data paths.
- The script does not commit if no generated-data changes are staged.
- The script refuses to push from a branch different from `master` unless `-Branch` is changed.
- The script does not perform broad `git add .`.
- Use `-DryRun` before integrating it permanently into the application.
