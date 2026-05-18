"""NPU pipeline module smoke checker."""

from __future__ import annotations

import sys
from pathlib import Path

from .base_context import build_base_context
from .boundary import build_boundary_context
from .evaluation import build_report_from_context
from .runtime_context import build_runtime_context

def npu_pipeline_modules_check(repo_root: Path) -> dict[str, object]:
    root_text = str(repo_root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    npu_tools_text = str(repo_root / "Tools" / "npu")
    if npu_tools_text not in sys.path:
        sys.path.insert(0, npu_tools_text)

    context = {"repo_root": repo_root}
    context.update(build_base_context(repo_root))
    context.update(
        build_runtime_context(
            repo_root,
            context["music_context"],  # type: ignore[arg-type]
            context["raw_preflight"],  # type: ignore[arg-type]
        )
    )
    context.update(build_boundary_context(context))
    return build_report_from_context(context)
