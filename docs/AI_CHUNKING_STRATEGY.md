# AI Chunking Strategy

Semantic chunks give AI systems precise context without loading unrelated files.

## Generated files

```text
indexAI/code_chunks/semantic_code_chunks.json
indexAI/code_chunks/semantic_code_chunks_manifest.json
```

## Command

```powershell
py .\Tools\npu\build_semantic_code_chunks.py --repo-root .
```

Dry run:

```powershell
py .\Tools\npu\build_semantic_code_chunks.py --repo-root . --dry-run
```

## Chunk fields

Each chunk includes path, symbol, line range, domain tags, Blender API references, risk level, compatibility notes, dependencies and SHA-256.

`Scripting/v61b/` chunks are marked with `do_not_change: true` so it remains a quality reference, not a refactoring target.
