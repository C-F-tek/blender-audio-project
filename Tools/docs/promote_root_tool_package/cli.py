"""Promote a root ``Tools/<area>/<tool>.py`` script into a package CLI."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from Tools.docs.repo_tool_surface_audit import repo_root_from

from .references import (
    candidate_tools,
    git_mv,
    increment_parent_indexes,
    line_count_text,
    relative,
    rewrite_code_path_references,
    scan_references,
)
from .reporting import build_batch_report, build_report, render_markdown


def promote_one(
    *,
    root: Path,
    area: str,
    tool: str,
    apply: bool,
    allow_references: bool,
    rewrite_code_references: bool,
) -> dict[str, object]:
    area_dir = root / "Tools" / area
    source = area_dir / f"{tool}.py"
    package_dir = area_dir / tool
    cli = package_dir / "cli.py"
    init = package_dir / "__init__.py"
    if not source.exists():
        raise SystemExit(f"source script not found: {source}")
    if package_dir.exists():
        raise SystemExit(f"target package already exists: {package_dir}")
    refs = scan_references(root, area, tool)
    own_refs = {relative(root, source)}
    external_refs = [item for item in refs if item.path not in own_refs]
    if external_refs and apply and not allow_references:
        raise SystemExit(f"refusing to move {source}: {len(external_refs)} external references found")

    source_text = source.read_text(encoding="utf-8")
    promoted_text = increment_parent_indexes(source_text)
    init_text = '"""Package CLI promoted from a root tool script."""\n\nfrom .cli import *  # noqa: F401,F403\nfrom .cli import main as main\n'
    actions = [
        f"move {relative(root, source)} -> {relative(root, cli)}",
        f"write {relative(root, init)}",
        f"cli_lines={line_count_text(promoted_text)}",
        f"init_lines={line_count_text(init_text)}",
    ]
    if apply:
        package_dir.mkdir(parents=True, exist_ok=True)
        git_mv(root, source, cli)
        if promoted_text != source_text:
            cli.write_text(promoted_text, encoding="utf-8")
        init.write_text(init_text, encoding="utf-8")
    reference_rewrites = (
        rewrite_code_path_references(root, area=area, tool=tool, apply=apply)
        if rewrite_code_references
        else []
    )
    return build_report(
        root=root,
        area=area,
        tool=tool,
        source=source,
        package_dir=package_dir,
        apply=apply,
        refs=refs,
        actions=actions,
        reference_rewrites=reference_rewrites,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--area", required=True)
    parser.add_argument("--tool", default="")
    parser.add_argument("--max-tools", type=int, default=0)
    parser.add_argument("--only-unreferenced", action="store_true")
    parser.add_argument("--output", default="output/validation/root_tool_package_promotion.json")
    parser.add_argument("--markdown-output", default="output/validation/root_tool_package_promotion.md")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--allow-references", action="store_true")
    parser.add_argument("--rewrite-code-references", action="store_true")
    args = parser.parse_args()

    root = repo_root_from(Path(args.repo_root))
    if args.tool:
        report = promote_one(
            root=root,
            area=args.area,
            tool=args.tool,
            apply=args.apply,
            allow_references=args.allow_references,
            rewrite_code_references=args.rewrite_code_references,
        )
    else:
        if args.max_tools <= 0:
            raise SystemExit("batch mode requires --max-tools > 0")
        selected: list[str] = []
        skipped: list[dict[str, object]] = []
        promotions: list[dict[str, object]] = []
        for tool in candidate_tools(root, args.area):
            refs = scan_references(root, args.area, tool)
            source = root / "Tools" / args.area / f"{tool}.py"
            package_dir = root / "Tools" / args.area / tool
            if package_dir.exists():
                skipped.append(
                    {
                        "tool": tool,
                        "reason": "target_package_exists",
                        "target": relative(root, package_dir),
                    }
                )
                continue
            own_refs = {relative(root, source)}
            external_refs = [item for item in refs if item.path not in own_refs]
            if args.only_unreferenced and external_refs:
                skipped.append(
                    {
                        "tool": tool,
                        "reason": "external_references",
                        "external_reference_count": len(external_refs),
                    }
                )
                continue
            selected.append(tool)
            promotions.append(
                promote_one(
                    root=root,
                    area=args.area,
                    tool=tool,
                    apply=args.apply,
                    allow_references=args.allow_references,
                    rewrite_code_references=args.rewrite_code_references,
                )
            )
            if len(selected) >= args.max_tools:
                break
        report = build_batch_report(
            root=root,
            area=args.area,
            apply=args.apply,
            selected=selected,
            skipped=skipped,
            promotions=promotions,
        )
    output = root / args.output
    markdown_output = root / args.markdown_output
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": True, "apply": args.apply, "summary": report.get("summary")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
