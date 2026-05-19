#!/usr/bin/env python3
"""Smoke-test rejected candidate previews are treated as negative examples."""

from __future__ import annotations

import json
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def read(rel_path: str) -> str:
    return (repo_root() / rel_path).read_text(encoding="utf-8")


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    gate = "\n".join(
        [
            read("Tools/ai/heap_gate/provider_commands.py"),
            read("Tools/ai/heap_gate/provider_prompt_text.py"),
            read("Tools/ai/heap_gate/provider_refinement.py"),
        ]
    )
    revision = read("Tools/ai/external_heap/revision_context/tasks.py")

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

    report = {
        "schema_version": 1,
        "kind": "heap_negative_preview_rewrite_contract_smoke",
        "passed": not errors,
        "errors": errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
