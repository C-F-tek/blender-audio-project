from __future__ import annotations

from common import (
    additional_context,
    classify_prompt,
    compact_list,
    excerpt_file,
    first_existing,
    json_stdout,
    latest_files,
    read_hook_input,
    repo_root,
    unique_lines,
)


CONTEXT_BY_LABEL = {
    "heap_runtime": [
        "docs/LOCAL_AI_RUN_BOOTSTRAP.md",
        "docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md",
        "ia_carmine/runtime/heap_runtime/TOOL_CONTEXT.md",
    ],
    "provider_gpu_npu": [
        "docs/LOCAL_AI_TASKS/gpu-npu-parallel-evidence-runbook.md",
        "docs/LOCAL_AI_TASKS/heavy-gpu-local-ai-diagnostics-handoff.md",
        "docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md",
    ],
    "evidence_bundle": [
        "docs/LOCAL_VALIDATION_EVIDENCE/README.md",
        "Tools/ai/build_github_evidence_bundle.py",
    ],
    "patch_or_refactor": [
        "AGENTS.md",
        "docs/LOCAL_AI_RUN_BOOTSTRAP.md",
    ],
    "docs_hygiene": [
        "docs/README.md",
        "docs/AI_DOCS_ENTRYPOINT.md",
        "docs/LOCAL_AI_RUN_BOOTSTRAP.md",
    ],
    "git_flow": [
        "AGENTS.md",
        "docs/LOCAL_AI_RUN_BOOTSTRAP.md",
    ],
}


def main() -> int:
    event = read_hook_input()
    root = repo_root(event)
    prompt = str(event.get("prompt") or "")
    labels = classify_prompt(prompt)

    candidate_paths: list[str] = []
    for label in labels:
        candidate_paths.extend(CONTEXT_BY_LABEL.get(label, []))
    candidate_paths = unique_lines(candidate_paths)

    existing = first_existing(root, candidate_paths)
    latest_tasks = latest_files(root, "docs/LOCAL_AI_TASKS/*.md", limit=3)
    latest_evidence = latest_files(root, "docs/LOCAL_VALIDATION_EVIDENCE/*", limit=3)

    lines = [
        "IA-Carmine prompt context enrichment.",
        "",
        "Hook policy:",
        "- Advisory only: add context and quality hints. Do not block Codex from this hook.",
        "",
        f"Detected work labels: {compact_list(labels)}",
        f"Relevant context files: {compact_list(existing)}",
        f"Latest task handoffs: {compact_list(latest_tasks)}",
        f"Latest evidence artifacts: {compact_list(latest_evidence)}",
        "",
        "Execution guidance:",
        "- Read the closest relevant repo docs before changing architecture.",
        "- Prefer explicit file-scoped changes over broad workspace changes.",
        "- If Python files are edited, include resulting line counts and syntax validation when practical.",
        "- If provider, heap or runtime flow is touched, preserve GPU1/GPU0/NPU role separation and evidence-first semantics.",
        "- Continue toward the requested product; this hook is not a completion gate.",
    ]

    for rel_path in existing[:2]:
        excerpt = excerpt_file(root, rel_path, max_chars=900)
        if excerpt:
            lines.extend(["", f"Context excerpt from {rel_path}:", excerpt])

    json_stdout(additional_context("UserPromptSubmit", "\n".join(lines)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
