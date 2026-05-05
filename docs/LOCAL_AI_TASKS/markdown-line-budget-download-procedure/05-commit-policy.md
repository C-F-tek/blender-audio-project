# 05 - Commit policy

## Prima controlla

```powershell
git status --short
git diff --name-only
```

## Non aggiungere

```text
output/**
docs/LOCAL_VALIDATION_EVIDENCE/**
indexAI/**
renders/**
*.db
*.sqlite
Downloads/*.zip
```

## Minimo

```powershell
git add `
  .\Tools\docs\split_large_markdown.py `
  .\Tools\docs\README.md `
  .\Tools\validation\check_markdown_line_limits.py `
  .\docs\LOCAL_AI_TASKS\markdown-line-budget-policy.md
```

Poi aggiungere solo Markdown sorgenti modificati dallo split.
