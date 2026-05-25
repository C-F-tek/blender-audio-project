from __future__ import annotations

import sys
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
WORKFLOW_RUN_DIR = THIS_DIR.parent / "workflow_run"
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))
if str(WORKFLOW_RUN_DIR) not in sys.path:
    sys.path.insert(0, str(WORKFLOW_RUN_DIR))

from workflow_gui_app import WorkflowGui


def main() -> None:
    app = WorkflowGui()
    app.mainloop()


if __name__ == "__main__":
    main()
