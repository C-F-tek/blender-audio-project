# Tools/npu

## Purpose

This folder contains tooling and notes for AI-assisted review, context generation, and implementation planning.

## Known roles

- Build compact project context for AI systems.
- Generate or store technical notes for local AI workflows.
- Support dual-AI or NPU-assisted planning.
- Produce implementation notes, manifests, or service packets.

## Known files and patterns

| Pattern | Role |
|---|---|
| `build_*context*.py` | Build compact code context or project manifests. |
| `run_*pipeline*.py` | Run AI-assisted workflow stages. |
| `*_technical_notes.md` | Technical notes for AI or NPU workflows. |
| `*_manifest.json` | Machine-readable file or context manifest. |
| `*_context.md` | Markdown context file for AI consumption. |

## AI rules

- Treat generated context files as derived artifacts.
- Inspect generator scripts before replacing generated files.
- Keep model paths and device names configurable.
- Do not assume NPU availability on all systems.
- Preserve technical notes unless replacing them with a newer documented version.

## Not specified

- Canonical NPU model.
- Canonical OpenVINO configuration.
- Required package versions.
- Supported devices beyond local experimentation.
