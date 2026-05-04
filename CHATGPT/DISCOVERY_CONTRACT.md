# CHATGPT discovery contract

## Purpose

`CHATGPT/` is a lightweight operational-memory directory for this repository.

It exists so that future ChatGPT sessions, local AI pipelines, Codex-style agents and GitHub-only assistants can quickly recover session-specific lessons without reopening large evidence bundles.

## Required discovery behavior

Agents entering this repository should treat these paths as early context:

```text
CHATGPT.md
CHATGPT/README.md
CHATGPT/*.md
```

Recommended read order:

```text
1. AGENTS.md
2. CHATGPT.md
3. CHATGPT/README.md
4. latest CHATGPT/next-chat-handoff-*.md
5. latest CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md
6. docs/LOCAL_AI_RUN_BOOTSTRAP.md
7. README.md
8. docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

## Meaning

`CHATGPT/*.md` files are durable operational notes. They may contain:

```text
- handoff state for the next chat;
- recurring chat/tooling failure modes;
- robust recovery commands;
- local run hygiene rules;
- patch bundle delivery preferences;
- AI-to-AI coordination notes.
```

## Authority level

`CHATGPT/*.md` is advisory memory.

It must not override:

```text
AGENTS.md
repository source code
validation reports
canonical docs
current git state
human explicit commands
```

When a CHATGPT note conflicts with canonical contracts, follow canonical contracts and report the conflict.

## Local AI / context-pack inclusion rule

Context pack builders, repository inventory tools and semantic chunk generators should include `CHATGPT/*.md` as small high-priority context because the files are intentionally compact and operational.

Do not include ignored runtime outputs from `output/**` unless a workflow explicitly promotes compact evidence into tracked documentation.

## Git policy

Commit small stable `CHATGPT/*.md` notes when they improve handoff reliability.

Do not commit transient chat scratch files, raw logs, secrets, local provider outputs, `output/**`, `renders/**`, `*.db`, `*.sqlite` or `*.sqlite3`.
