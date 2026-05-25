"""Request text fixture for heap runtime complete smoke."""

from __future__ import annotations

from pathlib import Path


def complete_smoke_request(repo_root: Path) -> str:
    target = repo_root / "ia_carmine" / "runtime" / "heap_runtime" / "completeness_gate" / "cli.py"
    rel_target = target.relative_to(repo_root).as_posix()
    return f"""
# Heap Runtime Complete Smoke Request

Operate inside the existing IA-Carmine heap/pointer/veto loop, not as a JSON-only or tool-only probe.
Use runtime universe, shared memory evidence, provider peers and brokered tool evidence as the working context.

Concrete local scope:
- Inspect and reason about the existing repo file `{rel_target}`.
- TARGET_FILES must be exactly `{rel_target}` unless the FINAL_PRODUCT_DELTA states that no applicable code target is verified.
- Do not invent Java, Gradle, placeholder paths, output/**, indexAI/**, or docs/LOCAL_VALIDATION_EVIDENCE/** as patch targets.
- If a tool is useful, request it through the native provider tool-call continuation; prose is not tool execution.

Required response shape:
- FINAL_PRODUCT_KIND: text | code | text_and_code
- FINAL_PRODUCT_ACTION: append | replace | supersede | refine
- CURRENT_POINTER with previous_block_id, refines_block_id and resume_from_block_id
- CONSUMED_EVIDENCE with successful same-run broker request ids only
- NEXT_RUNTIME_INTENT
- FINAL_PRODUCT_DELTA with TARGET_FILES, PROBLEM, EVIDENCE, IMPLEMENTATION_CHANGES, PATCH_SKETCH, VALIDATION_COMMANDS and RISKS when code is applicable
""".strip()
