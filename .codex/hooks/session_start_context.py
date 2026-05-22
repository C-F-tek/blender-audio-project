from __future__ import annotations

from common import (
    additional_context,
    compact_list,
    excerpt_file,
    first_existing,
    json_stdout,
    latest_files,
    read_hook_input,
    repo_root,
    summarize_git,
)


GUIDE_CANDIDATES = [
    "AGENTS.md",
    "README.md",
    "docs/LOCAL_AI_RUN_BOOTSTRAP.md",
    "docs/LOCAL_AI_TASKS/README.md",
    "docs/LOCAL_AI_TASKS/gpu-npu-parallel-evidence-runbook.md",
    "docs/LOCAL_AI_TASKS/heavy-gpu-local-ai-diagnostics-handoff.md",
]


def main() -> int:
    event = read_hook_input()
    root = repo_root(event)
    found_guides = first_existing(root, GUIDE_CANDIDATES)
    latest_tasks = latest_files(root, "docs/LOCAL_AI_TASKS/*.md", limit=5)
    latest_evidence = latest_files(root, "docs/LOCAL_VALIDATION_EVIDENCE/*", limit=5)

    lines = [
        "IA-Carmine repository startup context.",
        "",
        "Hook policy:",
        "- Non-blocking advisory mode only: these hooks add context, warnings and quality hints; they do not deny commands and do not stop Codex.",
        "- The goal is better continuity, not stricter operator approval or a hard completion gate.",
        "",
        "Git state:",
        *[f"- {item}" for item in summarize_git(root)],
        "",
        "Known repo guides:",
        f"- {compact_list(found_guides)}",
        "",
        "Latest task handoffs:",
        f"- {compact_list(latest_tasks)}",
        "",
        "Latest validation evidence:",
        f"- {compact_list(latest_evidence)}",
        "",
        "Operational policy to keep in mind:",
        "- Avoid `git add .`; stage only explicit source/test/doc/evidence files.",
        "- Keep `output/**`, `renders/**`, SQLite databases and code chunk indexes out of commits.",
        "- Do not run Blender, production deploys, force-push, history rewrite, destructive deletes, secret/permission/billing/visibility changes, or merge to protected branches without explicit operator approval.",
        "- Prefer file-scoped validation before full runs; when editing Python, report resulting line counts.",
        "- Keep raw runtime artifacts local; version only source, tests, docs, and compact evidence under docs/LOCAL_VALIDATION_EVIDENCE/.",
        "- Treat GPU1 as primary planner/closure owner, GPU0 as reviewer/refiner, NPU as bounded micro-task auditor.",
    ]

    if "AGENTS.md" in found_guides:
        excerpt = excerpt_file(root, "AGENTS.md", max_chars=1200)
        if excerpt:
            lines.extend(["", "AGENTS.md excerpt:", excerpt])

    json_stdout(
        additional_context(
            "SessionStart",
            "\n".join(lines),
            system_message="IA-Carmine advisory context loaded; no blocking hook is active.",
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
