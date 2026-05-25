"""Shared broker-result validation for GPU1/native tool evidence."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ia_carmine.runtime.heap_gate.runtime_common import read_json, safe_dict, safe_int


def broker_result_report(
    payload: dict[str, Any],
    *,
    repo_root: Path | str | None = None,
) -> dict[str, Any]:
    outputs = safe_dict(payload.get("outputs"))
    report_path = str(
        outputs.get("json_report")
        or outputs.get("evidence_json")
        or outputs.get("debug_lab_report")
        or ""
    ).strip()
    if not report_path:
        return {}
    path = Path(report_path)
    if not path.is_absolute() and repo_root is not None:
        path = Path(repo_root) / path
    return safe_dict(read_json(path))


def broker_result_passed(
    payload: dict[str, Any],
    *,
    repo_root: Path | str | None = None,
    require_report_passed: bool = False,
) -> bool:
    errors = payload.get("errors") if isinstance(payload.get("errors"), list) else []
    if payload.get("blocked") or errors:
        return False

    returncode = payload.get("returncode")
    execution_ok = (
        safe_int(returncode, default=1) == 0
        if returncode is not None
        else payload.get("executed") is True
    )
    if not execution_ok:
        return False

    summary = safe_dict(payload.get("summary"))
    if summary.get("passed") is False:
        return False

    report = broker_result_report(payload, repo_root=repo_root)
    if report:
        report_errors = report.get("errors") if isinstance(report.get("errors"), list) else []
        if report.get("passed") is False or report_errors:
            return False
        if require_report_passed and report.get("passed") is not True:
            return False
    elif require_report_passed:
        return False

    return True
