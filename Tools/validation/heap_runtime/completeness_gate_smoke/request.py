"""Request text fixture for heap runtime complete smoke."""

from __future__ import annotations

from pathlib import Path


def complete_smoke_request(repo_root: Path) -> str:
    target = repo_root / "Tools" / "ai" / "provider_tool_loop.py"
    if not target.is_file():
        target = repo_root / "Tools" / "ai" / "heap_runtime" / "completeness_gate" / "cli.py"
    rel_target = target.relative_to(repo_root).as_posix()
    return f"""
# Heap Runtime Complete Smoke Request

Operate inside the existing IA-Carmine heap/pointer/veto loop, not as a JSON-only or tool-only probe.
Use runtime universe, shared memory evidence, provider peers and brokered tool evidence as the working context.

Concrete local scope:
- Inspect and reason about the existing repo file `{rel_target}`.
- TARGET_FILES must be exactly `{rel_target}` unless you return EXIT_DECISION=NO_PATCHABLE_TARGET.
- Do not invent Java, Gradle, placeholder paths, output/**, indexAI/**, or docs/LOCAL_VALIDATION_EVIDENCE/** as patch targets.
- If a tool is useful, request it through the native provider tool-call continuation; prose is not tool execution.

Required response shape:
- # HEAP_DELTA_PROPOSAL
- EXIT_DECISION=PATCHABLE_TARGET or EXIT_DECISION=NO_PATCHABLE_TARGET
- POINTER_ACTION=STAY_FORWARD | BACKTRACK_PROPAGATE | RESUME_FORWARD | SPLIT_TASKS | NO_PATCHABLE_TARGET
- TARGET_FILES, PROBLEM, EVIDENCE, IMPLEMENTATION_CHANGES, PATCH_SKETCH, VALIDATION_COMMANDS, RISKS
""".strip()
