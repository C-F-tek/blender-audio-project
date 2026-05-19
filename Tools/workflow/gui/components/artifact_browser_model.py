from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

WORKFLOW_DIR = Path(__file__).resolve().parents[2]
if str(WORKFLOW_DIR) not in sys.path:
    sys.path.insert(0, str(WORKFLOW_DIR))

from workflow_run._shared.artifact_catalog import (  # noqa: E402
    AUDIO_EXTENSIONS,
    IMAGE_EXTENSIONS,
    TEXT_EXTENSIONS,
    VIDEO_EXTENSIONS,
    ArtifactEntry,
    classify_path,
    collect_artifact_entries,
    human_bytes,
    open_external,
)

ArtifactItem = ArtifactEntry


def collect_session_artifacts(
    session: Any, extra_roots: list[Path] | None = None
) -> list[ArtifactItem]:
    return collect_artifact_entries(session, extra_roots=extra_roots)
