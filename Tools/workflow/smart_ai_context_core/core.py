from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_MAX_PACKET_CHARS = 22000
DEFAULT_MAX_CAPSULE_CHARS = 3200


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "_", value.strip().lower())
    return re.sub(r"_+", "_", value).strip("_") or "track"


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def compact(value: Any, limit: int = 900) -> str:
    text = " ".join(str(value or "").split())
    return text if len(text) <= limit else text[: limit - 3].rstrip() + "..."


def keywords(text: str, limit: int = 24) -> list[str]:
    words = re.findall(r"[\w]{4,}", text.lower(), flags=re.UNICODE)
    stop = {
        "json",
        "true",
        "false",
        "none",
        "null",
        "path",
        "file",
        "data",
        "output",
        "input",
        "della",
        "delle",
        "come",
        "sono",
        "deve",
    }
    counts: dict[str, int] = {}
    for word in words:
        if word not in stop and not word.isdigit():
            counts[word] = counts.get(word, 0) + 1
    return [w for w, _ in sorted(counts.items(), key=lambda i: (-i[1], i[0]))[:limit]]


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None


def read_text(path: Path, limit: int = 240000) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")[:limit]


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(root.resolve(strict=False)).as_posix()
    except Exception:
        return str(path)


def capsule(
    source: str, path: str, kind: str, title: str, value: Any, priority: int, max_chars: int
) -> dict[str, Any]:
    content = value if isinstance(value, str) else json.dumps(value, indent=2, ensure_ascii=False)
    if len(content) > max_chars:
        content = content[:max_chars].rstrip() + "\n..."
    summary = compact(content, 800)
    cid = sha(f"{source}:{path}:{title}:{sha(content)[:12]}")[:16]
    return {
        "capsule_id": cid,
        "source": source,
        "path": path,
        "kind": kind,
        "title": title,
        "priority": priority,
        "size_chars": len(content),
        "sha256": sha(content),
        "keywords": keywords(title + " " + summary),
        "summary": summary,
        "content": content,
    }
