# AI Chunking Strategy

## Purpose

This document describes the semantic chunking layer used by the AI artifact pipeline.

The goal is to give AI systems precise code context without loading unrelated repository files or rewriting existing source code.

## Strategy

Chunks are extracted by Python symbol:

- module;
- class;
- function.

Each chunk receives metadata:

- path;
- symbol;
- line range;
- domain tags;
- Blender API references;
- dependencies;
- risk level;
- compatibility notes;
- SHA-256 hash.

## Generated files

Default outputs:

```text
indexAI/code_chunks/semantic_code_chunks.json
indexAI/code_chunks/semantic_code_chunks_manifest.json
```

These files are generated context. They are not runtime source code.

## Command

```powershell
py .\Tools\npu\build_semantic_code_chunks.py --repo-root .
```

Dry run:

```powershell
py .\Tools\npu\build_semantic_code_chunks.py --repo-root . --dry-run
```

## Safety

The script only reads source files and writes generated JSON context. It does not modify files under `Scripting/`.

`Scripting/v61b/` chunks are marked with `do_not_change: true` so AI systems treat that package as reference material rather than a refactoring target.
