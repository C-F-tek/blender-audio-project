from __future__ import annotations

import sys
from pathlib import Path
from tkinter import messagebox, ttk

THIS_DIR = Path(__file__).resolve().parent
WORKFLOW_DIR = THIS_DIR.parent
if str(WORKFLOW_DIR) not in sys.path:
    sys.path.insert(0, str(WORKFLOW_DIR))

try:
    import workflow_core as wf  # noqa: E402
except ImportError:
    from Tools.workflow import workflow_core as wf  # noqa: E402
from components.artifact_browser import ArtifactBrowserWindow  # noqa: E402
from git_auto_push import run_auto_push_full_project, run_auto_push_generated_data  # noqa: E402
from workflow_gui_modern import WorkflowGui as BaseWorkflowGui  # noqa: E402


class WorkflowGuiWithPush(BaseWorkflowGui):
    """Workflow GUI with generated-data publishing and artifact consultation buttons."""

    def __init__(self) -> None:
        super().__init__()
        self.artifact_browser_window: ArtifactBrowserWindow | None = None
        self.inject_artifact_browser_button()
        self.inject_generated_data_push_button()

    def inject_artifact_browser_button(self) -> None:
        try:
            anchor_button = None
            for button in self.always_enabled_buttons:
                try:
                    if button.cget("text") == "Project stats":
                        anchor_button = button
                        break
                except Exception:
                    continue

            if anchor_button is None:
                messagebox.showwarning(
                    "Artifact browser",
                    "Punto di inserimento non trovato: il pulsante Artifact browser non e' stato aggiunto.",
                )
                return

            parent = anchor_button.master
            button = ttk.Button(
                parent, text="Artifact browser", command=self.open_artifact_browser_window
            )
            button.pack(in_=parent, after=anchor_button, fill="x", padx=8, pady=3)
            self.always_enabled_buttons.append(button)
        except Exception as exc:
            messagebox.showwarning(
                "Artifact browser", f"Impossibile aggiungere il browser artefatti: {exc}"
            )

    def artifact_extra_roots(self, session) -> list[Path]:
        roots: list[Path] = []
        for key in ("output_dir", "render_frames_dir"):
            value = session.artifacts.get(key)
            if value:
                roots.append(Path(value))
        for key in ("render_mp4", "render_ffmpeg_mp4"):
            value = session.artifacts.get(key)
            if value:
                roots.append(Path(value).parent)
        return roots

    def open_artifact_browser_window(self) -> None:
        if self.artifact_browser_window is None or not self.artifact_browser_window.winfo_exists():
            self.artifact_browser_window = ArtifactBrowserWindow(
                self,
                session_loader=lambda: self.session,
                extra_roots_loader=self.artifact_extra_roots,
            )
        self.artifact_browser_window.show()

    def inject_generated_data_push_button(self) -> None:
        try:
            anchor_button = None
            for button in self.buttons:
                try:
                    if button.cget("text") == "Dual AI scene script":
                        anchor_button = button
                        break
                except Exception:
                    continue

            if anchor_button is None:
                messagebox.showwarning(
                    "Publish button",
                    "Punto di inserimento non trovato: i pulsanti Git non sono stati aggiunti.",
                )
                return

            parent = anchor_button.master
            data_button = ttk.Button(
                parent,
                text="Push generated data",
                command=lambda: self.run_task(
                    "Push generated data",
                    lambda: run_auto_push_generated_data(include_output_json=True),
                ),
            )
            data_button.pack(in_=parent, after=anchor_button, fill="x", padx=8, pady=3)
            self.buttons.append(data_button)

            all_button = ttk.Button(
                parent,
                text="Push all project changes",
                command=lambda: self.run_task(
                    "Push all project changes",
                    lambda: run_auto_push_full_project(message="chore: update full project"),
                ),
            )
            all_button.pack(in_=parent, after=data_button, fill="x", padx=8, pady=3)
            self.buttons.append(all_button)
        except Exception as exc:
            messagebox.showwarning(
                "Publish button", f"Impossibile aggiungere i pulsanti Git: {exc}"
            )


def main() -> None:
    app = WorkflowGuiWithPush()
    app.mainloop()


if __name__ == "__main__":
    main()
