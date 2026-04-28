from __future__ import annotations

from pathlib import Path
import sys
from tkinter import messagebox, ttk

THIS_DIR = Path(__file__).resolve().parent
WORKFLOW_DIR = THIS_DIR.parent
if str(WORKFLOW_DIR) not in sys.path:
    sys.path.insert(0, str(WORKFLOW_DIR))

from components.artifact_browser import ArtifactBrowserWindow  # noqa: E402
from git_auto_push import run_auto_push_generated_data  # noqa: E402
from workflow_gui_modern import WorkflowGui as BaseWorkflowGui  # noqa: E402
import workflow_state as wf  # noqa: E402


class WorkflowGuiWithPush(BaseWorkflowGui):
    """Workflow GUI with generated-data push and artifact consultation buttons.

    It uses the adaptive grouped modern GUI as base and injects:
    - an artifact browser button near project/debug utilities;
    - an AI runtime diagnostics button near project/debug utilities;
    - the push button after the structured-data generation steps.
    """

    def __init__(self) -> None:
        super().__init__()
        self.artifact_browser_window: ArtifactBrowserWindow | None = None
        self.inject_artifact_browser_button()
        self.inject_ai_runtime_diagnostics_button()
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
            button = ttk.Button(parent, text="Artifact browser", command=self.open_artifact_browser_window)
            button.pack(in_=parent, after=anchor_button, fill="x", padx=8, pady=3)
            self.always_enabled_buttons.append(button)
        except Exception as exc:
            messagebox.showwarning("Artifact browser", f"Impossibile aggiungere il browser artefatti: {exc}")

    def inject_ai_runtime_diagnostics_button(self) -> None:
        try:
            anchor_button = None
            for button in self.always_enabled_buttons:
                try:
                    if button.cget("text") == "Artifact browser":
                        anchor_button = button
                        break
                except Exception:
                    continue
            if anchor_button is None:
                for button in self.always_enabled_buttons:
                    try:
                        if button.cget("text") == "Project stats":
                            anchor_button = button
                            break
                    except Exception:
                        continue

            if anchor_button is None:
                messagebox.showwarning(
                    "AI runtime diagnostics",
                    "Punto di inserimento non trovato: il pulsante diagnostica AI non e' stato aggiunto.",
                )
                return

            parent = anchor_button.master
            button = ttk.Button(
                parent,
                text="AI runtime diagnostics",
                command=lambda: self.run_task("AI runtime diagnostics", self.run_ai_runtime_diagnostics),
            )
            button.pack(in_=parent, after=anchor_button, fill="x", padx=8, pady=3)
            self.always_enabled_buttons.append(button)
        except Exception as exc:
            messagebox.showwarning("AI runtime diagnostics", f"Impossibile aggiungere il pulsante diagnostica AI: {exc}")

    def run_ai_runtime_diagnostics(self):
        return wf.run_command(
            [
                str(wf.python_executable()),
                str(wf.PROJECT_DIR / "Tools" / "workflow" / "ai_runtime_diagnostics.py"),
                "--track-stem",
                self.session.track_stem,
            ],
            operation="ai_runtime_diagnostics",
            metadata={
                "track_stem": self.session.track_stem,
                "chat_model": self.session.chat_model,
                "creative_model": self.session.creative_model,
                "technical_model": self.session.technical_model,
                "script_max_tokens": self.session.script_max_tokens,
                "skip_npu_heavy_pass": self.skip_npu.get(),
                "skip_ollama": self.skip_ollama.get(),
            },
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
                    "Auto-push button",
                    "Punto di inserimento non trovato: il pulsante auto-push non e' stato aggiunto.",
                )
                return

            parent = anchor_button.master
            button = ttk.Button(
                parent,
                text="Push generated data",
                command=lambda: self.run_task(
                    "Push generated data",
                    lambda: run_auto_push_generated_data(include_output_json=True),
                ),
            )
            button.pack(in_=parent, after=anchor_button, fill="x", padx=8, pady=3)
            self.buttons.append(button)
        except Exception as exc:
            messagebox.showwarning("Auto-push button", f"Impossibile aggiungere il pulsante auto-push: {exc}")


def main() -> None:
    app = WorkflowGuiWithPush()
    app.mainloop()


if __name__ == "__main__":
    main()
