#!/usr/bin/env python3
"""Smoke-test GPU1 source allowlist hardening."""

from __future__ import annotations

import json
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read(rel_path: str) -> str:
    return (repo_root() / rel_path).read_text(encoding="utf-8")


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    gate = read("Tools/ai/run_heap_runtime_completeness_gate.py")
    anchors = read("Tools/ai/heap_source_anchors.py")
    provider_probe = read("Tools/ai/run_local_provider_probe.py")
    contract_text = gate + "\n" + anchors
    revision = read("Tools/ai/build_external_heap_revision_context.py")

    require(
        "def source_allowlist_contract" in gate,
        "gate must expose source allowlist contract",
        errors,
    )
    require(
        "SOURCE_PATH_ALLOWLIST_CONTRACT" in contract_text,
        "GPU1 prompt must include hard source allowlist contract",
        errors,
    )
    require(
        "TARGET_FILES deve essere copiato esattamente da Allowed source paths" in gate,
        "GPU1 prompt must force exact allowlist target copy",
        errors,
    )
    require(
        "Rejected/non-allowlisted source refs blacklist" in gate,
        "provider refinement must blacklist rejected source refs",
        errors,
    )
    require(
        "repeated_unverified_loop" in gate,
        "terminal loop breaker must stop repeated non-allowlisted refs",
        errors,
    )
    require(
        "EXIT_DECISION=NO_PATCHABLE_TARGET" in gate,
        "GPU1 prompt must force no-target exit for missing allowlist match",
        errors,
    )
    require(
        "BLOCKED_NO_VERIFIED_TARGET_REASON" in gate,
        "GPU1 prompt must require blocked reason field",
        errors,
    )
    require(
        '"docs/LOCAL_VALIDATION_EVIDENCE/"' in anchors,
        "source anchors must exclude generated validation evidence docs",
        errors,
    )
    require(
        "generated evidence/output prefixes" in anchors,
        "source contract must explicitly forbid generated evidence/output target prefixes",
        errors,
    )
    require(
        "Do not invent files such as tools/data_processor/real_existing_file.py" in contract_text,
        "GPU1 prompt must explicitly forbid observed invented fixture path",
        errors,
    )
    require(
        "invented/non-allowlisted source path refs" in gate,
        "quality report must classify invented source refs",
        errors,
    )
    require(
        "invented_source_path_refs" in gate,
        "quality report must expose invented source refs",
        errors,
    )
    require(
        "veto=invented_source_path_or_non_allowlisted_target" in gate,
        "NPU review must produce invented path veto",
        errors,
    )
    require(
        "GPU0 deterministic review: invented_source_path veto" in gate,
        "GPU0 review must veto invented paths",
        errors,
    )
    require(
        "<id-or-empty>" in gate and "Never output unresolved angle-bracket placeholders" in gate,
        "GPU1 prompt must forbid unresolved pointer placeholders",
        errors,
    )
    require(
        "tools/.../real_existing_file.py" not in provider_probe,
        "provider positive prompt must not seed fake paths",
        errors,
    )
    require(
        "<id-or-empty>" not in provider_probe,
        "provider positive prompt must not seed unresolved pointer placeholders",
        errors,
    )
    require(
        "docs/LOCAL_VALIDATION_EVIDENCE/" in provider_probe,
        "provider prompt must explicitly blacklist generated validation evidence docs",
        errors,
    )
    require(
        '"invented_source_path"' in revision,
        "revision context must classify invented source path candidates",
        errors,
    )
    require(
        '"unresolved_pointer_placeholder"' in revision,
        "revision context must classify pointer placeholders separately",
        errors,
    )
    require(
        "EXIT_DECISION=NO_PATCHABLE_TARGET invece di inventare path" in revision,
        "revision runtime instruction must forbid invented paths",
        errors,
    )

    report = {
        "schema_version": 1,
        "kind": "heap_source_allowlist_contract_smoke",
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
