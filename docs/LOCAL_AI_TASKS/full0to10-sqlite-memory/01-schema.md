# Schema

Tabelle principali:

- `memory_items`;
- `memory_chunks`;
- `memory_chunks_fts`;
- `embedding_cache`;
- `memory_meta`.

`embedding_cache` è già presente nello schema, ma questa patch non chiama provider
embedding. La semantica provider arriverà in una patch dedicata.
