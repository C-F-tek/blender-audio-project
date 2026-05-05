"""Build shadow split file plans for Markdown."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .constants import MAX_CHILD_FILENAME_CHARS, MAX_SECTIONS, SHADOW_SUFFIX
from .headings import Section, slugify, split_sections


def shadow_dir_for(target: Path) -> Path:
    return target.with_name(target.name + SHADOW_SUFFIX)


def child_name(section: Section) -> str:
    slug = slugify(section.title)
    prefix = f"{section.index + 1:02d}-"
    suffix = ".md"
    budget = MAX_CHILD_FILENAME_CHARS - len(prefix) - len(suffix)
    safe_slug = slug[:budget].strip("-._ ") or "section"
    return f"{prefix}{safe_slug}{suffix}"


def readme_text(target: Path, sections: list[Section]) -> str:
    lines = [
        f"# {target.name} split",
        "",
        f"Source: `{target.as_posix()}`",
        "",
        "## Sections",
        "",
    ]
    for section in sections:
        lines.append(f"- [{section.title}]({child_name(section)})")
    lines.append("")
    return "\n".join(lines)


def build_shadow_plan(target: Path) -> dict[str, Any]:
    text = target.read_text(encoding="utf-8", errors="replace")
    sections = split_sections(text)[:MAX_SECTIONS]
    out_dir = shadow_dir_for(target)
    files = [{"path": (out_dir / "README.md").as_posix(), "content": readme_text(target, sections)}]
    seen: set[str] = {"README.md"}
    for section in sections:
        name = child_name(section)
        if name in seen:
            name = f"{section.index + 1:02d}-section-{section.index + 1}.md"
        seen.add(name)
        files.append({"path": (out_dir / name).as_posix(), "content": section.text})
    return {
        "target_path": target.as_posix(),
        "shadow_dir": out_dir.as_posix(),
        "section_count": len(sections),
        "files": files,
    }


def write_shadow_plan(plan: dict[str, Any]) -> int:
    written = 0
    for item in plan["files"]:
        path = Path(str(item["path"]))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(str(item["content"]), encoding="utf-8")
        written += 1
    return written
