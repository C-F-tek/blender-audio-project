from __future__ import annotations

import re
import subprocess
from typing import Any

GPU_HEADER_RE = re.compile(r"^GPU(?P<index>\d+):\s*$")
FIELD_RE = re.compile(r"^(?P<name>[A-Za-z][A-Za-z0-9]+)\s*=\s*(?P<value>.+)$")


def vulkan_devices() -> list[dict[str, Any]]:
    try:
        completed = subprocess.run(
            ["vulkaninfo", "--summary"],
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
    except Exception:
        return []
    devices: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for raw in (completed.stdout or "").splitlines():
        line = raw.strip()
        header = GPU_HEADER_RE.match(line)
        if header:
            current = {"index": int(header.group("index"))}
            devices.append(current)
            continue
        if current is None:
            continue
        field = FIELD_RE.match(line)
        if field:
            current[field.group("name")] = field.group("value").strip()
    return devices


def select_integrated_vulkan_device() -> dict[str, Any]:
    devices = vulkan_devices()
    for item in devices:
        vendor = str(item.get("vendorID") or "").lower()
        dtype = str(item.get("deviceType") or "").lower()
        name = str(item.get("deviceName") or "")
        if vendor == "0x8086" or "integrated" in dtype or "intel" in name.lower():
            return {
                "requested": "auto",
                "resolved": str(item["index"]),
                "target_device": item,
                "devices": devices,
            }
    return {
        "requested": "auto",
        "resolved": "1" if len(devices) > 1 else "0",
        "target_device": devices[1] if len(devices) > 1 else (devices[0] if devices else {}),
        "devices": devices,
        "warning": "integrated Vulkan device not detected by vulkaninfo",
    }


def resolve_vulkan_visible_devices(value: str) -> dict[str, Any]:
    text = str(value or "").strip().lower()
    if text in {"", "auto", "integrated", "intel", "gpu0"}:
        return select_integrated_vulkan_device()
    devices = vulkan_devices()
    target = next(
        (item for item in devices if str(item.get("index")) == text),
        {},
    )
    return {
        "requested": value,
        "resolved": value,
        "target_device": target,
        "devices": devices,
    }
