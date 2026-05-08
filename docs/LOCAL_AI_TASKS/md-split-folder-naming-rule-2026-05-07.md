# Markdown split folder naming rule

Status: active rule.

When a Markdown file is split, the folder for its parts must keep the full file name including `.md`.

Pattern:

```text
path/name.md
path/name.md/part-001.md
path/name.md/part-002.md
```

Do not use extensionless folders for split Markdown documents.

The original `name.md` remains the compact index and links every part.
