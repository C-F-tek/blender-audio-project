"""CLI for resolving runtime file references against the local repository."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import RuntimeConsumer, RuntimeRefProvenance
from .resolver import RuntimeFileRefResolver


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--text", action="append", default=[])
    parser.add_argument("--text-file", action="append", default=[])
    parser.add_argument("--target-file", action="append", default=[])
    parser.add_argument("--validation-script", action="append", default=[])
    parser.add_argument("--provenance", default=RuntimeRefProvenance.OPERATOR_REQUEST.value)
    parser.add_argument("--strict-patchable-targets", action="store_true")
    parser.add_argument("--output", default="output/validation/runtime_file_refs.json")
    parser.add_argument("--markdown-output", default="output/validation/runtime_file_refs.md")
    return parser.parse_args()


def split_values(values: list[str]) -> list[str]:
    out: list[str] = []
    for value in values:
        for item in str(value or "").split(","):
            normalized = item.strip().strip("'\"")
            if normalized:
                out.append(normalized)
    return out


def resolve_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve(strict=False)


def render_markdown(report: dict[str, object]) -> str:
    lines = [
        "# Runtime File References",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Ref count: `{report.get('ref_count')}`",
        f"- Patchable target count: `{report.get('patchable_target_count')}`",
        f"- Validation script count: `{report.get('validation_script_count')}`",
        f"- Output-only count: `{report.get('output_only_count')}`",
        f"- Strict patchable targets: `{report.get('strict_patchable_targets')}`",
        "",
        "## Patchable Targets",
        "",
    ]
    targets = report.get("patchable_targets")
    lines.extend([f"- `{item}`" for item in targets] if isinstance(targets, list) and targets else ["- none"])
    lines.extend(["", "## Validation Scripts", ""])
    scripts = report.get("validation_scripts")
    lines.extend([f"- `{item}`" for item in scripts] if isinstance(scripts, list) and scripts else ["- none"])
    lines.extend(["", "## Errors", ""])
    errors = report.get("errors")
    lines.extend([f"- {item}" for item in errors] if isinstance(errors, list) and errors else ["- none"])
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    resolver = RuntimeFileRefResolver(repo_root)
    provenance = RuntimeRefProvenance(args.provenance)

    text_chunks = list(args.text)
    for item in split_values(args.text_file):
        path = resolve_path(repo_root, item)
        if path.is_file():
            text_chunks.append(read_text(path))

    refs = []
    for text in text_chunks:
        refs.extend(resolver.operator_refs(text))
        refs.extend(resolver.provider_target_refs(text))
        refs.extend(resolver.provider_validation_refs(text))

    for target in split_values(args.target_file):
        refs.append(
            resolver.resolve(
                target,
                provenance=provenance,
                consumers=(
                    RuntimeConsumer.PROVIDER_CONTEXT,
                    RuntimeConsumer.MATRIX,
                    RuntimeConsumer.LAB,
                    RuntimeConsumer.FINAL_ASSEMBLER,
                ),
            )
        )
    for script in split_values(args.validation_script):
        refs.append(
            resolver.resolve(
                script,
                provenance=provenance,
                consumers=(RuntimeConsumer.BROKER_TOOL,),
                validation_ref=True,
            )
        )

    report = resolver.report(refs)
    patchable_targets = resolver.patchable_targets(refs)
    validation_scripts = resolver.validation_scripts(refs)
    errors = []
    if args.strict_patchable_targets and not patchable_targets:
        errors.append("no_patchable_targets_resolved")
    report.update(
        {
            "kind": "runtime_file_refs",
            "schema_version": 1,
            "passed": not errors,
            "strict_patchable_targets": bool(args.strict_patchable_targets),
            "patchable_target_count": len(patchable_targets),
            "validation_script_count": len(validation_scripts),
            "patchable_targets": patchable_targets,
            "validation_scripts": validation_scripts,
            "errors": errors,
            "source_writes_performed": False,
            "patch_application_performed": False,
            "git_write_performed": False,
        }
    )

    output = resolve_path(repo_root, args.output)
    markdown = resolve_path(repo_root, args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "output": str(output)}, indent=2))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
