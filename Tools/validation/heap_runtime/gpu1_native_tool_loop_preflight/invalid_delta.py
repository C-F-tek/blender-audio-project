"""Build readable artifacts when GPU1 emits text without valid delta protocol."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def invalid_delta_text(
    *,
    final_text: str,
    final_report_path: Path,
    protocol: dict[str, Any],
    unconsumed_ids: list[Any],
) -> str:
    emitted = bool(final_text.strip())
    status = "INVALID_PROTOCOL_RAW_GPU1_OUTPUT" if emitted else "NOT_EMITTED_BY_GPU1"
    text = [
        "# GPU1 FINAL_PRODUCT_DELTA",
        "",
        f"STATUS: {status}",
        "",
        "GPU1 did not produce a valid FINAL_PRODUCT_DELTA protocol in this tool loop.",
        f"provider_report: {final_report_path}",
        "protocol_errors:",
        *[f"- {item}" for item in protocol.get("errors", [])],
        "unconsumed_tool_result_ids:",
        *[f"- {item}" for item in unconsumed_ids],
    ]
    if emitted:
        text.extend(
            [
                "",
                "## RAW_ASSISTANT_OUTPUT",
                "",
                final_text.strip(),
            ]
        )
    return "\n".join(text) + "\n"
