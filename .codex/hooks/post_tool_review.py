from __future__ import annotations

from common import (
    VALIDATION_HINTS,
    additional_context,
    git_status_paths,
    is_advisory_git_path,
    json_stdout,
    read_hook_input,
    repo_root,
    tool_name,
)


def main() -> int:
    event = read_hook_input()
    root = repo_root(event)
    tool = tool_name(event)
    status_paths = git_status_paths(root)
    runtime_paths = [path for path in status_paths if is_advisory_git_path(path)]
    python_paths = [path for path in status_paths if path.endswith(".py")]

    lines = [
        "IA-Carmine post-tool context.",
        "",
        "Mode: advisory context only.",
        f"Tool: {tool or 'unknown'}",
    ]

    if python_paths:
        lines.extend(["", "Python paths in working tree:", *[f"- {path}" for path in python_paths[:20]]])
        lines.append("Suggested follow-up: validate modified Python files and report line counts.")

    if runtime_paths:
        lines.extend(["", "Runtime/local paths in working tree:", *[f"- {path}" for path in runtime_paths[:20]]])
        lines.append("Suggested follow-up: keep runtime/local artifacts separate from source commits.")

    lines.extend(["", "Validation reminders:", *[f"- {hint}" for hint in VALIDATION_HINTS]])

    json_stdout(additional_context("PostToolUse", "\n".join(lines)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
