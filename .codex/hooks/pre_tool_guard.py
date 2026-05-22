from __future__ import annotations

from common import (
    RISKY_COMMAND_PATTERNS,
    additional_context,
    command_matches,
    command_text,
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
    command = command_text(event)
    tool = tool_name(event)
    risky_patterns = command_matches(command, RISKY_COMMAND_PATTERNS)

    dirty_paths = git_status_paths(root)
    advisory_paths = [path for path in dirty_paths if is_advisory_git_path(path)]

    lines = [
        "IA-Carmine pre-tool advisory context.",
        "",
        "Policy:",
        "- Non-blocking: this hook does not deny, rewrite, approve, or stop the tool call.",
        "- Use this warning only as model-visible context to improve command quality.",
        "",
        f"Tool: {tool or 'unknown'}",
    ]

    if risky_patterns:
        lines.extend(
            [
                "",
                "Risky command pattern detected:",
                *[f"- {pattern}" for pattern in risky_patterns],
                "",
                "Recommended safer behavior:",
                "- Prefer exact path staging over broad workspace staging.",
                "- Keep runtime outputs, render outputs, databases and generated code indexes out of commits.",
                "- For protected or destructive operations, rely on explicit operator instruction.",
            ]
        )

    if advisory_paths:
        lines.extend(
            [
                "",
                "Current working tree contains paths that are normally local/runtime-only:",
                *[f"- {path}" for path in advisory_paths[:20]],
            ]
        )

    if not risky_patterns and not advisory_paths:
        lines.extend(
            [
                "",
                "No IA-Carmine advisory issue detected for this tool call.",
            ]
        )

    json_stdout(additional_context("PreToolUse", "\n".join(lines)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
