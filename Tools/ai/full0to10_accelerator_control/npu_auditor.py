"""NPU auditor contract for Full0To10."""
from __future__ import annotations

from typing import Any


def build_npu_auditor(capability: dict[str, Any]) -> dict[str, Any]:
    npu = capability.get("npu", {}) if isinstance(capability, dict) else {}
    devices = npu.get("devices") or []
    has_npu = any(str(item).upper() == "NPU" for item in devices)
    return {
        "kind": "npu_auditor_contract",
        "passed": True,
        "role": "sampled_auditor_or_diagnostic",
        "device_visible": has_npu,
        "probe_performed": npu.get("probe_performed"),
        "allowed_actions": [
            "sampled review",
            "diagnostic evidence",
            "provider disagreement audit",
            "quality gate cross-check",
        ],
        "blocked_actions": [
            "primary advisory by default",
            "implicit model loading",
            "patch application",
            "runtime generation without explicit promotion",
        ],
        "promotion_requirements": [
            "dedicated patch",
            "smoke evidence",
            "quality stack approval",
            "operator explicit request",
        ],
    }
