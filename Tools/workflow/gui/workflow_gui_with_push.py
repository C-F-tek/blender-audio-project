from __future__ import annotations

from tkinter import messagebox, ttk

from git_auto_push import run_auto_push_generated_data
from workflow_gui import WorkflowGui as BaseWorkflowGui


class WorkflowGuiWithPush(BaseWorkflowGui):
    """Workflow GUI with an extra generated-data push button.

    This wrapper avoids invasive edits to the main GUI file. It injects a button
    directly below the index rebuild operation when the GUI is initialized.
    """

    def __init__(self) -> None:
        super().__init__()
        self.inject_generated_data_push_button()

    def inject_generated_data_push_button(self) -> None:
        try:
            before_button = None
            for button in self.buttons:
                try:
                    if button.cget("text") == "Full audio prepare":
                        before_button = button
                        break
                except Exception:
                    continue

            if before_button is None:
                messagebox.showwarning(
                    "Auto-push button",
                    "Punto di inserimento non trovato: il pulsante auto-push non e' stato aggiunto.",
                )
                return

            parent = before_button.master
            button = ttk.Button(
                parent,
                text="Push generated data",
                command=lambda: self.run_task(
                    "Push generated data",
                    lambda: run_auto_push_generated_data(include_output_json=True),
                ),
            )
            button.pack(in_=parent, before=before_button, fill="x", padx=8, pady=3)
            self.buttons.append(button)
        except Exception as exc:
            messagebox.showwarning("Auto-push button", f"Impossibile aggiungere il pulsante auto-push: {exc}")


def main() -> None:
    app = WorkflowGuiWithPush()
    app.mainloop()


if __name__ == "__main__":
    main()
