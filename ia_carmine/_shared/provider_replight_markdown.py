"""Markdown rendering for provider replight evidence."""

from __future__ import annotations

from typing import Any


def provider_replight_table(gate: dict[str, Any]) -> list[str]:
    reports = _as_list(gate.get("provider_reports")) or _as_list(
        gate.get("provider_replight_reports")
    ) or _as_list(
        _as_dict(gate.get("metrics")).get("provider_replight_reports")
    )
    lines = [
        "## Provider replight",
        "",
        "| Provider | Modello | Backend/device | Stage | Loaded | Work verified | Rejection | Token | Esito |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    if not reports:
        return [*lines, "| none |  |  |  | false | false | missing |  | missing |", ""]
    for report in reports:
        item = _as_dict(report)
        backend = "/".join(
            part
            for part in (
                str(item.get("provider_backend") or ""),
                str(item.get("provider_compute_device") or ""),
            )
            if part
        )
        result = (
            "pass"
            if item.get("replight_passed") is True
            else str(item.get("replight_blocked_reason") or "failed")
        )
        lines.append(
            "| "
            + " | ".join(
                _cell(value)
                for value in (
                    str(item.get("provider_id") or item.get("lane") or ""),
                    str(item.get("provider_model") or item.get("selected_model") or ""),
                    backend,
                    item.get("provider_stage"),
                    item.get("provider_loaded"),
                    item.get("provider_work_verified"),
                    item.get("provider_rejection_reason") or item.get("role_rejection_reason"),
                    f"{item.get('prompt_token_count')}/{item.get('completion_token_count')}",
                    result,
                )
            )
            + " |"
        )
    return [*lines, ""]


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _cell(value: Any) -> str:
    return str(value if value is not None else "").replace("|", "/").replace("\n", " ")[:180]
