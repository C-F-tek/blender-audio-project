"""Export GPU1 native tool-loop artifacts to the operator Documents folder."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from ia_carmine._shared.file_backed_transport import artifact_ref


def export_documents_copy(
    repo_root: Path,
    output: Path,
    work_dir: Path,
    stamp: str,
) -> dict[str, Any]:
    export_dir = Path.home() / "Documents" / "IA-Carmine" / (
        f"gpu1_native_tool_loop_preflight_{stamp}"
    )
    copied = [
        _copy_if_exists(output, export_dir / "live.json"),
        _copy_if_exists(work_dir / "gpu1_delta_readable.md", export_dir / "gpu1_delta_readable.md"),
        _copy_if_exists(
            work_dir / "gpu1_text_after_tool_result.md",
            export_dir / "gpu1_text_after_tool_result.md",
        ),
        _copy_if_exists(
            work_dir / "delta_review" / "gpu1_final_product_delta.md",
            export_dir / "gpu1_final_product_delta.md",
        ),
    ]
    export_ref = {
        "ref_id": f"gpu1_native_tool_loop_preflight_{stamp}",
        "path": str(export_dir),
        "kind": "gpu1_native_tool_loop_documents_export_dir",
        "required": True,
        "producer": "gpu1_native_tool_loop_preflight",
        "source": "gpu1_native_tool_loop_preflight",
        "content_type": "inode/directory",
        "exists": export_dir.is_dir(),
        "bytes": 0,
        "sha256": "",
    }
    return {
        "export_dir": str(export_dir),
        "export_dir_ref": export_ref,
        "files": copied,
    }


def _copy_if_exists(src: Path, dst: Path) -> dict[str, Any]:
    if not src.exists():
        return {"source": str(src), "destination": str(dst), "copied": False}
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return {"source": str(src), "destination": str(dst), "copied": True, "bytes": dst.stat().st_size}
