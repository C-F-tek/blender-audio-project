#!/usr/bin/env python3
"""Smoke test for OpenVINO NPU/GPU.0 device visibility normalization."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    ai_dir = repo_root / "Tools" / "ai"
    if str(ai_dir) not in sys.path:
        sys.path.insert(0, str(ai_dir))

    from full0to10_accelerator_control.device_visibility import normalized_openvino_devices
    from full0to10_accelerator_control.gpu0_contract import build_gpu0_contract
    from full0to10_accelerator_control.npu_auditor import build_npu_auditor

    cases = [
        {"npu": {"devices": ["CPU", "GPU.0", "NPU"]}},
        {"npu": {"result": {"devices": ["CPU", "GPU.0", "NPU"]}}},
        {"npu": {"result": {"stdout": "{\"import_ok\": true, \"devices\": [\"CPU\", \"GPU.0\", \"NPU\"]}"}}},
        {"npu": {"stdout": "Available devices: CPU GPU.0 NPU"}},
    ]

    results = []
    for capability in cases:
        devices = normalized_openvino_devices(capability)
        npu = build_npu_auditor(capability)
        gpu0 = build_gpu0_contract(capability)
        results.append(
            {
                "devices": devices,
                "npu_visible": npu["device_visible"],
                "gpu0_visible": gpu0["device_visible"],
            }
        )

    passed = all(item["npu_visible"] and item["gpu0_visible"] for item in results)
    print(json.dumps({"passed": passed, "cases": results}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
