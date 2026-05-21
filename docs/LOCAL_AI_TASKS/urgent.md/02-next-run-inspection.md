# 02 — Next run-unica inspection

## Inspection goal

Inspect the next run as a single Universo IA product path:

```text
operator request / task Markdown
-> startup/preload context
-> heap/exchange entry
-> provider departments
-> brokered tool evidence
-> validators
-> candidate operations
-> code/patch product or blocked reason
-> compact evidence
-> commit/PR only after reviewed apply boundary
```

## Required questions

For every run or smoke claim, answer:

```text
What exact command ran?
Which profile was selected?
Which task/request file entered the heap?
Which lanes were required by that profile?
Which lanes produced valid evidence?
Which lanes were missing/degraded/diagnostic-only?
Which tools were requested and executed?
Which validators ran and what did they prove?
Was there a concrete candidate operation?
Was there a code/patch product?
Was a commit or PR produced?
```

## Full smoke acceptance

A full smoke can pass only when every required core lane has valid evidence. A narrow smoke may pass its own fixture, but it must remain named as partial/diagnostic.

## Local lab note

If a local lab with provider devices is available, run the canonical dispatcher surfaces rather than direct legacy paths:

```powershell
python -m Tools.ai run --repo-root . --request-file <task.md> <profile args>
python -m Tools.validation <validator> --repo-root . <args>
python -m Tools.ai build_github_evidence_bundle --repo-root . <reports>
```

Do not infer that this chat executed those commands unless concrete command output and artifact paths are attached.

## No unanalyzed surface rule

The next inspection should proceed by families, not by random file names:

```text
root contracts and context indexes
Tools/ai/run and heap/exchange packages
provider mesh packages
runtime tool/broker packages
patch/code product packages
validation packages
docs/LOCAL_AI_TASKS current entrypoints
docs/LOCAL_VALIDATION_EVIDENCE compact current evidence
recent PRs/commits touching the run path
```

## Immediate blockers to report honestly

```text
no command output inspected -> runtime state not proven
no lane report inspected -> lane viability not proven
no code/patch product inspected -> product not proven
no validator report inspected -> validation not proven
no commit SHA/PR inspected -> GitHub write not proven
```

## Expected compact evidence

The follow-up bundle should include:

```text
run identity and stamp
source branch and commit
task/request file path
lane viability summary
provider/tool/validator report summaries
patch-plan summary when present
artifact manifest for reports and related artifacts
blocked/product classification
next concrete action
```
