"""Preflight gating policy for heap context closure."""

from __future__ import annotations

from typing import Any

RUNTIME_BLOCKING_STEPS = {
    "gpu1_native_tool_loop_preflight",
    "provider_lane_activation",
}


def classify_preflight_gate(
    *,
    skipped: bool,
    result: dict[str, Any],
    report: dict[str, Any],
) -> dict[str, Any]:
    """Classify preflight failures without making stale checks hard blockers."""

    if skipped:
        return _policy(
            status="skipped",
            product_entry_allowed=True,
            blocks_startup=False,
        )
    if result.get("passed") is True:
        return _policy(
            status="passed",
            product_entry_allowed=True,
            blocks_startup=False,
        )
    if not report:
        return _policy(
            status="blocked",
            product_entry_allowed=False,
            blocks_startup=True,
            blocking_failures=[
                {
                    "name": "preflight_report",
                    "report_errors": ["preflight report missing or unreadable"],
                }
            ],
        )

    product_entry_allowed = _product_entry_allowed(report)
    blocking: list[dict[str, Any]] = []
    diagnostic: list[dict[str, Any]] = []
    for step in _failed_steps(report):
        if step.get("name") in RUNTIME_BLOCKING_STEPS:
            blocking.append(step)
        else:
            diagnostic.append(step)

    if not product_entry_allowed:
        blocking.append(
            {
                "name": "preflight_product_entry",
                "report_errors": ["product_entry_allowed=false"],
            }
        )
    if not blocking and not diagnostic:
        diagnostic.append(
            {
                "name": "preflight_returncode",
                "returncode": result.get("returncode"),
                "report_errors": report.get("errors") or ["preflight failed"],
            }
        )

    blocks_startup = bool(blocking)
    status = "blocked" if blocks_startup else "diagnostic_failed_runtime_allowed"
    return _policy(
        status=status,
        product_entry_allowed=product_entry_allowed,
        blocks_startup=blocks_startup,
        blocking_failures=blocking,
        diagnostic_failures=diagnostic,
    )


def _product_entry_allowed(report: dict[str, Any]) -> bool:
    value = report.get("product_entry_allowed")
    if value is not None:
        return bool(value)
    return bool(report.get("preflight_only"))


def _failed_steps(report: dict[str, Any]) -> list[dict[str, Any]]:
    steps = report.get("failed_steps")
    if not isinstance(steps, list):
        return []
    failed: list[dict[str, Any]] = []
    for step in steps:
        if not isinstance(step, dict):
            continue
        failed.append(
            {
                "name": str(step.get("name") or ""),
                "returncode": step.get("returncode"),
                "report_kind": step.get("report_kind"),
                "report_errors": step.get("report_errors") or [],
                "report_warnings": step.get("report_warnings") or [],
            }
        )
    return failed


def _policy(
    *,
    status: str,
    product_entry_allowed: bool,
    blocks_startup: bool,
    blocking_failures: list[dict[str, Any]] | None = None,
    diagnostic_failures: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    blocking = blocking_failures or []
    diagnostic = diagnostic_failures or []
    return {
        "preflight_status": status,
        "preflight_product_entry_allowed": product_entry_allowed,
        "preflight_blocks_startup": blocks_startup,
        "preflight_failed_but_runtime_allowed": bool(diagnostic and not blocks_startup),
        "preflight_blocking_failures": blocking,
        "preflight_diagnostic_failures": diagnostic,
        "preflight_blocking_failure_count": len(blocking),
        "preflight_diagnostic_failure_count": len(diagnostic),
    }
