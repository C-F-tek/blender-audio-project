"""Controller layer shared by the operator CLI run and GUI view."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import LauncherConfig
from .profiles import build_heap_command, resolve_config, run_dir_for
from .runner import analyze_code_product, run_operator_lab


class OperatorProductController:
    """Application controller for the heap/universe operator product run."""

    def __init__(self, config: LauncherConfig) -> None:
        self.config = config

    def resolved_config(self) -> LauncherConfig:
        return resolve_config(self.config)

    def build_command(self) -> list[str]:
        return build_heap_command(self.config)

    def run(
        self,
        *,
        timeout: int = 24000,
        apply_safe: bool = False,
        require_all_integrated: bool = False,
    ) -> dict[str, Any]:
        return run_operator_lab(
            self.config,
            timeout=timeout,
            apply_safe=apply_safe,
            require_all_integrated=require_all_integrated,
        )

    def review_code_product(self, code_product: Path) -> dict[str, Any]:
        cfg = self.resolved_config()
        return analyze_code_product(cfg.repo_root, code_product, run_dir_for(cfg))

    def apply_safe_code_product(self, code_product: Path) -> dict[str, Any]:
        cfg = self.resolved_config()
        return analyze_code_product(
            cfg.repo_root,
            code_product,
            run_dir_for(cfg),
            apply_safe=True,
            require_all_integrated=True,
        )
