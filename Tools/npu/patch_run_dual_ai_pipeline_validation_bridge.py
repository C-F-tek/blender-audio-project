#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "Tools" / "npu" / "run_dual_ai_pipeline.py"

IMPORT_LINE = "from implementation_draft_validation import validate_implementation_draft_with_adapter, validation_report_to_legacy_shape\n"
MARKER_START = "def validate_implementation_draft(draft: dict[str, Any]) -> dict[str, Any]:\n"
MARKER_END = "\ndef generated_scene_script_relpath() -> str:\n"
REPLACEMENT = '''def validate_implementation_draft(draft: dict[str, Any]) -> dict[str, Any]:
    """Validate generated Blender implementation drafts.

    The actual policy lives in Tools/ai_adapters/blender and is reached through
    Tools/npu/implementation_draft_validation.py. This wrapper keeps the legacy
    return shape expected by retry prompts and downstream code.
    """
    report = validate_implementation_draft_with_adapter(draft, PROJECT_MANIFEST_JSON)
    return validation_report_to_legacy_shape(report)
'''


def main() -> int:
    text = TARGET.read_text(encoding="utf-8")
    if IMPORT_LINE not in text:
        anchor = "from run_ollama_music_agent import markdown_from_insights\n"
        if anchor not in text:
            raise SystemExit(f"Import anchor not found in {TARGET}")
        text = text.replace(anchor, anchor + IMPORT_LINE, 1)

    start = text.find(MARKER_START)
    end = text.find(MARKER_END)
    if start < 0 or end < 0 or end <= start:
        raise SystemExit("Could not locate validate_implementation_draft block safely.")

    text = text[:start] + REPLACEMENT + text[end:]
    TARGET.write_text(text, encoding="utf-8")
    print(f"[OK] Patched {TARGET}")
    print(f"[INFO] New line count: {len(text.splitlines())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
