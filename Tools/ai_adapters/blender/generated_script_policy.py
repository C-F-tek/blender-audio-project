from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


DEFAULT_ALLOWED_NEW_PREFIXES = (
    "indexAI/scene_scripts/",
    "indexAI/patch_library/",
)

DEFAULT_READ_ONLY_SOURCE_PREFIXES = (
    "Scripting/",
    "Tools/",
    "docs/",
    "indexAI/task_capsules/",
)

DEFAULT_REQUIRED_SCRIPT_TOKENS = (
    "import bpy",
    "keyframe_insert",
)

DEFAULT_FORBIDDEN_SCRIPT_TOKENS = (
    "ShaderNodeTexMusgrave",
    "bpy.ops.wm.save_as_mainfile",
    "bpy.ops.wm.open_mainfile",
)


@dataclass(slots=True)
class BlenderGeneratedScriptPolicy:
    """Policy for AI-generated Blender script drafts.

    This object is intentionally data-oriented so it can be serialized into
    smoke-test reports and reused by CLI tools.
    """

    allowed_new_prefixes: tuple[str, ...] = DEFAULT_ALLOWED_NEW_PREFIXES
    read_only_source_prefixes: tuple[str, ...] = DEFAULT_READ_ONLY_SOURCE_PREFIXES
    required_script_tokens: tuple[str, ...] = DEFAULT_REQUIRED_SCRIPT_TOKENS
    forbidden_script_tokens: tuple[str, ...] = DEFAULT_FORBIDDEN_SCRIPT_TOKENS
    min_script_chars: int = 1600
    require_full_keyframes_reference: bool = True
    full_keyframes_names: tuple[str, ...] = (
        "analysis_blender_keyframes",
        "BLENDER_KEYFRAMES_JSON",
        "keyframes",
        "frames",
    )
    metadata: dict[str, Any] = field(default_factory=dict)

    def normalize_path(self, path: str | Path) -> str:
        return str(path).replace("\\", "/").strip()

    def is_allowed_new_file(self, path: str | Path) -> bool:
        value = self.normalize_path(path)
        return bool(value) and value.startswith(self.allowed_new_prefixes)

    def is_existing_source_path(self, path: str | Path) -> bool:
        value = self.normalize_path(path)
        return bool(value) and value.startswith(self.read_only_source_prefixes)

    def script_references_full_keyframes(self, script: str) -> bool:
        if not self.require_full_keyframes_reference:
            return True
        lowered = script.lower()
        return any(name.lower() in lowered for name in self.full_keyframes_names)

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed_new_prefixes": list(self.allowed_new_prefixes),
            "read_only_source_prefixes": list(self.read_only_source_prefixes),
            "required_script_tokens": list(self.required_script_tokens),
            "forbidden_script_tokens": list(self.forbidden_script_tokens),
            "min_script_chars": self.min_script_chars,
            "require_full_keyframes_reference": self.require_full_keyframes_reference,
            "full_keyframes_names": list(self.full_keyframes_names),
            "metadata": self.metadata,
        }
