"""Project AI index builder package."""

from .builder import build_project_ai_index
from .config import PROJECT_INDEX_MD, PROJECT_MANIFEST_JSON

__all__ = ["PROJECT_INDEX_MD", "PROJECT_MANIFEST_JSON", "build_project_ai_index"]
