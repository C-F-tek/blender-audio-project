from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> dict:
    completed = subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return {
        "command": cmd,
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout[-4000:],
        "stderr_tail": completed.stderr[-4000:],
        "ok": completed.returncode == 0,
    }


def main() -> int:
    repo_root = Path.cwd()
    if len(sys.argv) >= 3 and sys.argv[1] == "--repo-root":
        repo_root = Path(sys.argv[2]).resolve()

    launcher = repo_root / "Tools" / "workflow" / "run_unified_local_ai_refactor.ps1"
    helper = repo_root / "Tools" / "workflow" / "heap_exchange_review_bridge.ps1"

    errors: list[str] = []

    launcher_text = launcher.read_text(encoding="utf-8-sig")
    helper_text = helper.read_text(encoding="utf-8-sig") if helper.exists() else ""

    required_launcher_markers = [
        "IA-CARMINE-HEAP-EXCHANGE-REVIEW-BRIDGE-IMPORT-BEGIN",
        "IA-CARMINE-HEAP-EXCHANGE-PRE-REVIEW-BRIDGE-BEGIN",
        "Invoke-UnifiedHeapExchangePreReviewBridge",
    ]

    required_helper_markers = [
        "function Publish-UnifiedHeapExchangeEvents",
        "function Reset-UnifiedNonProductArtifactsBeforeReviewBridge",
        "function Assert-UnifiedReviewBridgeCleanTree",
        "function Invoke-UnifiedHeapExchangePreReviewBridge",
        "Write-UnifiedRunAiPublicEvent",
        "ai_pipeline",
        "official_adapter_patch_specs_manifest",
        "nonproduct_artifacts_before_review_bridge",
    ]

    for marker in required_launcher_markers:
        if marker not in launcher_text:
            errors.append(f"missing launcher marker: {marker}")

    for marker in required_helper_markers:
        if marker not in helper_text:
            errors.append(f"missing helper marker: {marker}")

    if "AllowDirty" in helper_text or "--allow-dirty" in helper_text:
        errors.append("helper must not enable AllowDirty/--allow-dirty")

    parse_script = (
        "$tokens=$null;$errors=$null;"
        f"$null=[System.Management.Automation.Language.Parser]::ParseFile('{str(launcher).replace(chr(92), '/')}',[ref]$tokens,[ref]$errors);"
        f"$null=[System.Management.Automation.Language.Parser]::ParseFile('{str(helper).replace(chr(92), '/')}',[ref]$tokens,[ref]$errors);"
        "if($errors.Count -gt 0){$errors | ForEach-Object { Write-Error $_.Message }; exit 1}else{exit 0}"
    )

    parser_result = run(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", parse_script],
        repo_root,
    )

    if not parser_result["ok"]:
        errors.append("PowerShell parser failed")

    report = {
        "schema_version": 1,
        "kind": "heap_exchange_review_bridge_smoke",
        "repo_root": str(repo_root).replace("\\", "/"),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "parser_result": parser_result,
        "errors": errors,
        "warnings": [],
    }

    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
