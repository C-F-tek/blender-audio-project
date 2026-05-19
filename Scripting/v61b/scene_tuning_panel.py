# Canonical module loader split from scene_tuning_panel.py.
from __future__ import annotations

from pathlib import Path as _Path

_PARTS_DIR = _Path(__file__).with_name('scene_tuning_panel_parts')
_PART_NAMES = (
    'part_001.py',
    'part_002.py',
    'part_003.py',
    'part_004.py',
    'part_005.py',
)

for _part_name in _PART_NAMES:
    _part_path = _PARTS_DIR / _part_name
    exec(compile(_part_path.read_text(encoding="utf-8"), str(_part_path), "exec"), globals(), globals())

del _Path, _PARTS_DIR, _PART_NAMES, _part_name, _part_path
