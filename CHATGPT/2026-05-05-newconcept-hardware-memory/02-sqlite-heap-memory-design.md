# 02 — SQLite heap memory design

## Direction

Do not add a disconnected second memory system.

Evolve the existing memory lane around:

```text
Tools/ai/agent_runtime_sqlite_memory.py
Tools/ai/agent_runtime_tool_broker.py
semantic chunks
runtime telemetry
shared AI-to-AI bundle evidence
```

## Proposed module layout

```text
Tools/ai/
  agent_runtime_sqlite_memory.py          # existing SQLite backend to extend
  agent_memory_schema.py                  # DB schema + migrations
  agent_memory_chunker.py                 # Markdown/text chunking
  agent_memory_embeddings.py              # embedding cache
  agent_memory_search.py                  # FTS5 + vector/hybrid search
  agent_memory_tools.py                   # memory_add_text / memory_add_file / memory_search CLI
  agent_runtime_tool_broker.py            # exposes memory tools via allowlist broker

output/ai_runtime_memory/
  operational_context.sqlite              # scratch, local, never commit

indexAI/agent_memory/
  agent_memory.sqlite                     # persistent, read-only default, never commit
```

## Physical and logical model

SQLite remains the physical database.

FTS5 provides keyword/BM25 search.

Embedding cache avoids repeated embedding work.

Namespaces separate memory scopes.

Hybrid search merges lexical and semantic retrieval.

## Minimum SQLite schema

```sql
CREATE TABLE memory_items (
    id TEXT PRIMARY KEY,
    namespace TEXT NOT NULL,
    source_type TEXT NOT NULL,
    source_path TEXT,
    title TEXT,
    content_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE memory_chunks (
    id TEXT PRIMARY KEY,
    item_id TEXT NOT NULL,
    namespace TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    text TEXT NOT NULL,
    text_hash TEXT NOT NULL,
    token_estimate INTEGER,
    heading_path TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY(item_id) REFERENCES memory_items(id)
);

CREATE VIRTUAL TABLE memory_chunks_fts USING fts5(
    text,
    heading_path,
    content='memory_chunks',
    content_rowid='rowid',
    tokenize='unicode61'
);

CREATE TABLE embedding_cache (
    text_hash TEXT NOT NULL,
    model TEXT NOT NULL,
    dimension INTEGER NOT NULL,
    embedding_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY(text_hash, model)
);

CREATE TABLE memory_events (
    id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    namespace TEXT,
    item_id TEXT,
    details_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL
);
```

## Required namespaces

Namespaces are mandatory, not optional.

Recommended namespaces:

```text
repo_docs
repo_code
chatgpt_handoff
runtime_reports
patch_plans
validation_evidence
blender_manual
customer_context
temporary_session
```

This prevents contamination between current repository facts, old evidence, Blender/manual domain material and transient chat/session notes.

## memory_add_text

Tool for handoff notes, decisions and manual summaries.

Conceptual signature:

```python
def memory_add_text(
    db_path: Path,
    namespace: str,
    text: str,
    title: str | None = None,
    metadata: dict[str, Any] | None = None,
    persistent: bool = False,
) -> dict[str, Any]:
    ...
```

Required output shape:

```json
{
  "kind": "memory_add_text",
  "passed": true,
  "namespace": "chatgpt_handoff",
  "item_id": "...",
  "chunk_count": 4,
  "embedding_cache_hits": 2,
  "embedding_cache_misses": 2,
  "persistent_write_performed": false,
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "errors": [],
  "warnings": []
}
```

## memory_add_file

Tool for Markdown, JSON, TXT and compact reports.

Conceptual signature:

```python
def memory_add_file(
    db_path: Path,
    namespace: str,
    path: Path,
    repo_root: Path | None = None,
    include_glob: list[str] | None = None,
    exclude_glob: list[str] | None = None,
    persistent: bool = False,
) -> dict[str, Any]:
    ...
```

Ingestion rules:

```text
.md  -> chunk by heading + max chars
.txt -> linear chunks
.json -> extract summary, decision, errors, warnings, patch_plan_summary when report-like
.py -> optional only under repo_code namespace
.db/.sqlite -> forbidden
output/** -> forbidden unless explicit compact report allowlist
renders/** -> forbidden
indexAI/code_chunks/** -> forbidden by default
```

## Markdown chunk memory

Recommended chunker:

```text
split by Markdown headings
preserve heading_path
split long sections at about 3000-6000 chars
overlap 5-12 lines
compute content_hash for dedup
record source_path plus line_start/line_end when possible
```

Chunk metadata example:

```json
{
  "source_path": "docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md",
  "heading_path": ["Launcher unico", "Full0To10"],
  "line_start": 120,
  "line_end": 188,
  "kind": "markdown_chunk"
}
```

## Embedding cache

Cache key:

```text
text_hash + embedding_model
```

Example metrics:

```json
{
  "embedding_model": "bge-m3:latest",
  "embedding_cache_hits": 120,
  "embedding_cache_misses": 8,
  "embedding_generated": 8,
  "embedding_skipped": 0
}
```

If Ollama/embedding provider fails, memory search must degrade to FTS5-only instead of failing the full run.

## FTS5 search

FTS5 is the always-available first ranking layer.

SQLite FTS5 `bm25()` returns lower-is-better scores. The Python layer should normalize that into higher-is-better `fts_score`.

## Hybrid search

Recommended first formula:

```text
hybrid_score =
  0.55 * normalized_vector_score
+ 0.35 * normalized_fts_score
+ 0.10 * freshness_or_namespace_boost
```

Modes:

```text
fts_only
vector_only
hybrid
hybrid_rerank
```

Default recommended mode:

```text
hybrid, with fallback to fts_only when embeddings are unavailable
```

## memory_search output

```json
{
  "kind": "memory_search",
  "passed": true,
  "namespace": "repo_docs",
  "query": "runtime broker telemetry memory",
  "mode": "hybrid",
  "result_count": 8,
  "results": [
    {
      "chunk_id": "...",
      "source_path": "...",
      "heading_path": "...",
      "hybrid_score": 0.87,
      "fts_score": 0.71,
      "vector_score": 0.91,
      "text_preview": "..."
    }
  ],
  "provider_execution_performed": false,
  "persistent_memory_write_performed": false
}
```

## Broker memory tools

Candidate allowlist entries:

```text
memory_add_text
memory_add_file
memory_search
memory_rebuild_fts
memory_rebuild_embeddings
memory_export_manifest
```

Guardrails:

```text
memory_search -> always allowed
memory_add_text scratch -> allowed
memory_add_file scratch -> allowed with denylist path policy
persistent write -> requires --allow-persistent-write + explicit confirmation
memory_rebuild_embeddings -> allowed, provider embedding optional
delete/reset memory -> double confirmation only
```

## CLI sketch

```powershell
python .\Tools\ai\agent_memory_tools.py init `
  --db .\output\ai_runtime_memory\operational_context.sqlite

python .\Tools\ai\agent_memory_tools.py memory_add_text `
  --db .\output\ai_runtime_memory\operational_context.sqlite `
  --namespace chatgpt_handoff `
  --title "Decisione hybrid search" `
  --text "SQLite FTS5 + embedding cache + namespace..."

python .\Tools\ai\agent_memory_tools.py memory_add_file `
  --db .\output\ai_runtime_memory\operational_context.sqlite `
  --namespace repo_docs `
  --path .\docs\LOCAL_AI_TASKS\unified-local-ai-refactor-launcher.md

python .\Tools\ai\agent_memory_tools.py memory_search `
  --db .\output\ai_runtime_memory\operational_context.sqlite `
  --namespace repo_docs `
  --query "Full0To10 SQLite memory evidence" `
  --mode hybrid `
  --limit 10
```

## Policy summary

```text
SQLite DB = local/private runtime state
compact memory summaries = review evidence when needed
persistent writes = explicit confirmation only
embedding failure = degrade to FTS5-only
namespace = mandatory
raw DB never committed
```
