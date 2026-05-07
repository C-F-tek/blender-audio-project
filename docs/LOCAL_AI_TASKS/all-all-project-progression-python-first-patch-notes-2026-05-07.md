# ALL_ALL Project Progression Python-First Patch Notes Task

Status: active local AI task
Date: 2026-05-07
Scope: whole repository
Mode: ALL_ALL / Python-first / policy-aware / refactor-proposal

## Objective

Produce a larger and more useful patch-notes product for progressing the project itself.

The run must inspect code, Markdown, workflow scripts, validators, telemetry builders, provider mesh, runtime broker, evidence builders, local task docs and policy docs.

The output must not only describe inconsistencies. It must generate concrete, structured, manually reviewable patch notes and patch plans that can guide future code and documentation work.

## Authority model

Python/source code is the primary truth when checking behavior.

Markdown is the declared contract and operator-facing procedure.

When Markdown contradicts tracked Python/PowerShell behavior, classify as `doc_python` or `md_python` and propose a documentation update unless the code is demonstrably wrong.

When Python contradicts Python contracts, imports, CLI behavior, JSON schema, report fields, validators or workflow expectations, classify as `python_python` and propose a code refactor or fix.

When Markdown contradicts other Markdown policy, classify as `doc_doc`.

When code or docs violate repository policy, classify as `policy_violation`.

When a file is too large, too coupled, monolithic, duplicated, or mixes runtime/provider/validation responsibilities, classify as `refactor_candidate`.

## Required finding areas

The run must explicitly search for and classify:

- `doc_doc`: stale or contradictory docs;
- `doc_python` / `md_python`: docs cite missing scripts, wrong CLI flags, wrong paths, obsolete commands or outdated behavior;
- `python_doc`: code behavior exists but relevant docs are missing or stale;
- `python_python`: import/API/CLI/schema/report/validator/workflow inconsistencies inside code;
- `policy_violation`: output commit risk, DB/SQLite risk, provider execution ambiguity, Blender/FFmpeg runtime ambiguity, patch auto-apply ambiguity, Git write ambiguity, NPU advisory promotion risk, GPU0 primary-lane risk;
- `refactor_candidate`: monoliths, duplicated helper logic, oversized Markdown, workflow files above maintainability threshold, repeated report field construction, repeated path policy code;
- `telemetry_gap`: missing elapsed time, missing status normalization, missing fallback/success case, missing provider/runtime heap signal, missing capability manifest signal;
- `evidence_gap`: missing compact evidence, stale evidence, non-final evidence being treated as production evidence.

## Required product behavior

Generate patch notes that are concrete and applicable.

Each patch note must include:

- stable id;
- classification area;
- severity;
- target files;
- source evidence path and line when available;
- current observed problem;
- proposed fix;
- whether the fix is documentation-only, code-only, or code+docs;
- whether Python/source code is authoritative for this item;
- validation commands;
- stop conditions;
- guardrail impact;
- manual review requirement.

Patch notes must be numerous enough to support real project progression. Prefer a larger queue over suppressing valid findings, but do not invent findings without evidence.

## Patch plan requirements

For every generated patch note, build or reference a patch plan with:

- exact target file list;
- edit strategy;
- expected risk;
- validation command list;
- stop conditions;
- no automatic apply;
- no output/** commit;
- no DB/SQLite commit;
- no Blender/FFmpeg runtime;
- no provider execution unless explicitly requested by the run;
- no Git write by broker/tool.

## Python-over-docs tracing

The run must trace Python and PowerShell contracts before accepting Markdown claims.

Examples:

- if docs mention a script, verify the script exists;
- if docs mention a CLI flag, verify the parser/param block exposes it;
- if docs mention JSON fields, verify builders/validators produce or consume them;
- if workflow docs mention provider/NPU/GPU behavior, verify workflow code reflects it;
- if docs mention bundle/evidence files, verify builders create them or mark docs as design-only.

## Refactor proposal policy

If code violates project policy or maintainability expectations, do not patch automatically.

Generate refactor proposals with:

- target file;
- reason;
- proposed extraction/split;
- expected line-count impact;
- validation commands;
- migration risk;
- whether docs must be updated together.

For Markdown refactors, propose split or cleanup when:

- file exceeds line budget;
- obsolete command blocks remain;
- transient output/patch bundle paths are documented as canonical commands;
- branch/PR references are stale and operationally misleading.

For Python refactors, propose split or cleanup when:

- file is monolithic;
- repeated report schema logic exists;
- repeated path normalization/policy logic exists;
- provider/runtime/workflow responsibilities are mixed;
- validators duplicate contract logic.

## Output expectations

The final evidence set must include:

- patch notes quality product;
- patch plan quality product;
- runtime tool usage telemetry;
- runtime tool capability manifest;
- provider runtime heap telemetry;
- full toolbox run telemetry summary;
- shared AI-to-AI toolbox bundle when available;
- generated artifact path policy;
- compact final evidence only.

The product is report-only. It must not apply patches.

## Acceptance gate

The run is acceptable only if:

- patch notes are concrete and applicable;
- `patch_notes_applicability.all_applicable=true`;
- invalid patch note count is zero or explicitly explained;
- success_cases[] is present;
- fallback_cases[] is present when degradation happens;
- runtime tool telemetry has normalized status;
- broker elapsed timing is non-zero when broker tools execute;
- NPU final review is classified by GPU/validator lane, not by NPU self-check alone;
- policy violations are classified separately from normal doc drift;
- code refactor candidates are separated from documentation-only fixes.

## Guardrails

Do not:

- apply patches;
- run Blender;
- run FFmpeg;
- commit output/**;
- commit *.db or *.sqlite;
- commit renders/**;
- commit indexAI/code_chunks/**;
- force-push;
- merge;
- rewrite history;
- promote NPU advisory to primary decision;
- use GPU0/OpenVINO as primary lane;
- perform Git writes from broker/tool execution.

Manual review remains required for all produced patch notes and patch plans.
