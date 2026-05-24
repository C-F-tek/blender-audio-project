#!/usr/bin/env python3
"""Smoke-test rejected candidate previews are treated as negative examples."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def default_repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def read(repo_root: Path, rel_path: str) -> str:
    return (repo_root / rel_path).read_text(encoding="utf-8")


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def build_report(repo_root: Path) -> dict[str, object]:
    errors: list[str] = []
    gate = "\n".join(
        [
            read(repo_root, "ia_carmine/runtime/heap_gate/provider_commands.py"),
            read(repo_root, "ia_carmine/runtime/heap_gate/provider_prompt_text.py"),
            read(repo_root, "ia_carmine/runtime/heap_gate/provider_refinement.py"),
        ]
    )
    revision = read(repo_root, "ia_carmine/runtime/external_heap/revision_context/tasks.py")

    require(
        "tratta candidate_response_preview come esempio negativo" in revision,
        "revision rewrite task must mark bad preview as negative example",
        errors,
    )
    require(
        "senza copiare candidate_response_preview" in revision,
        "revision rewrite task must forbid copying rejected preview",
        errors,
    )
    require(
        "Rejected/non-allowlisted source refs blacklist" in gate,
        "gate feedback must blacklist rejected refs",
        errors,
    )
    require(
        "non copiarne TARGET_FILES/PATCH_SKETCH" in gate,
        "gate feedback must forbid copying target files from rejected preview",
        errors,
    )
    require(
        "candidate_response_preview as a negative example" in gate,
        "rewrite feedback must tell GPU1 candidate preview is negative",
        errors,
    )
    require(
        "tratta candidate_response_preview come esempio negativo" in gate,
        "provider prompt must tell GPU1 candidate preview is negative",
        errors,
    )
    require(
        "invented_source_path" in gate and "unresolved_pointer_placeholder" in gate,
        "negative-preview rule must mention concrete flags",
        errors,
    )
    require(
        "EXIT_DECISION=NO_PATCHABLE_TARGET" in revision,
        "revision instruction must keep no-target exit",
        errors,
    )

    return {
        "schema_version": 1,
        "kind": "heap_negative_preview_rewrite_contract_smoke",
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default="")
    parser.add_argument("--output", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve() if args.repo_root else default_repo_root()
    report = build_report(repo_root)

    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = repo_root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
