#!/usr/bin/env python3
"""Non-destructive codemod to wire unified chain contract into launcher.

The launcher remains responsible only for the envelope boundaries. It does not
control the dynamic center of the heap/exchange. The inserted gate validates
that a full review-PR run leaves observable exchange evidence and concrete patch
products before continuing toward product separation / PR creation.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


CHAIN_GATE_MARKER = "# IA-CARMINE-UNIFIED-CHAIN-CONTRACT-GATE-BEGIN"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def normalize_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def detect_newline(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def write_preserved(path: Path, text_lf: str, newline: str) -> None:
    path.write_text(text_lf.rstrip("\n").replace("\n", newline) + newline, encoding="utf-8-sig")


def run_parser(path: Path) -> tuple[bool, str]:
    ps_path = str(path).replace("'", "''")
    command = (
        "$tokens=$null;"
        "$errors=$null;"
        f"$null=[System.Management.Automation.Language.Parser]::ParseFile('{ps_path}',[ref]$tokens,[ref]$errors);"
        "if($errors.Count -gt 0){$errors | ForEach-Object { Write-Error $_.Message };exit 1}else{exit 0}"
    )
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0, result.stdout + result.stderr


def build_gate_block() -> str:
    return r'''
# IA-CARMINE-UNIFIED-CHAIN-CONTRACT-GATE-BEGIN
$UnifiedChainContractJson = Join-Path $OutputDir ("validation/unified_chain_contract_{0}.json" -f $DataStamp)
$UnifiedChainContractMd = Join-Path $OutputDir ("validation/unified_chain_contract_{0}.md" -f $DataStamp)
$RequireAiExchangeForChain = [bool]($UsePrimaryAdvisoryProvider -or $RunMultistepProviderWorkflow -or $UseOllamaAdvisory -or $RunOllamaProbe -or $OpenExtendedObserverConsoles)
$RequireConcretePatchSpecsForChain = [bool]$ReviewPrFromGeneratedPatchSpecs
$RequireReviewPrProductForChain = [bool]($PrepareReviewPr -and ($ReviewPrFromGeneratedPatchSpecs -or $ReviewPrApplyDeterministicSuggestions))

$UnifiedChainArgs = @(
    "Tools/validation/check_unified_chain_contract.py",
    "--repo-root", ".",
    "--stamp", $DataStamp,
    "--mode-name", $ModeName,
    "--output", $UnifiedChainContractJson,
    "--markdown-output", $UnifiedChainContractMd
)

if ($RequireAiExchangeForChain) { $UnifiedChainArgs += "--require-ai-exchange" }
if ($RequireConcretePatchSpecsForChain) { $UnifiedChainArgs += "--require-concrete-patch-specs" }
if ($RequireReviewPrProductForChain) { $UnifiedChainArgs += "--require-review-pr-product" }

$UnifiedChainContractOk = Invoke-Checked "Validate unified heap/exchange chain contract" {
    & $ResolvedPythonExe @UnifiedChainArgs
}
$ReportFiles += $UnifiedChainContractJson
$ContextFiles = Add-ExistingContextFile -Current $ContextFiles -PathValue $UnifiedChainContractMd
# IA-CARMINE-UNIFIED-CHAIN-CONTRACT-GATE-END
'''.strip("\n")


def patch_launcher(text_lf: str) -> tuple[str, list[str]]:
    changes: list[str] = []
    if CHAIN_GATE_MARKER in text_lf:
        return text_lf, changes

    anchor = "=== Validate patch suggestion product separation ==="
    label = '$PatchSuggestionProductSeparationOk = Invoke-Checked "Validate patch suggestion product separation" {'
    index = text_lf.find(label)
    if index < 0:
        raise RuntimeError("could not locate product separation gate anchor")

    before = text_lf[:index]
    after = text_lf[index:]
    block = build_gate_block()
    changes.append("insert_chain_contract_before_product_separation")
    return before.rstrip("\n") + "\n\n" + block + "\n\n" + after.lstrip("\n"), changes


def validate_policy(text_lf: str) -> list[str]:
    errors: list[str] = []
    required = [
        CHAIN_GATE_MARKER,
        "Validate unified heap/exchange chain contract",
        "Tools/validation/check_unified_chain_contract.py",
        "--require-ai-exchange",
        "--require-concrete-patch-specs",
        "--require-review-pr-product",
    ]
    for token in required:
        if token not in text_lf:
            errors.append(f"missing required wiring token: {token}")
    if text_lf.find("Validate unified heap/exchange chain contract") > text_lf.find("Validate patch suggestion product separation"):
        errors.append("chain contract gate must run before product separation")
    if re.search(r"^\s*throw\s*$", text_lf, flags=re.MULTILINE):
        errors.append("naked throw remains in launcher")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--target", default="Tools/workflow/run_unified_local_ai_refactor.ps1")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    target = (repo / args.target).resolve()
    backup_dir = repo / "output" / "validation" / "unified_chain_contract_wiring_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)

    parser_ok, parser_output = run_parser(target)
    if not parser_ok:
        print("PRE_PATCH_POWERSHELL_PARSE_FAILED")
        print(parser_output)
        return 2

    original = read_text(target)
    newline = detect_newline(original)
    original_lf = normalize_lf(original)
    patched_lf, changes = patch_launcher(original_lf)
    errors = validate_policy(patched_lf)
    if errors:
        print("POLICY_VALIDATION_FAILED")
        for error in errors:
            print(f"- {error}")
        return 3

    if patched_lf == original_lf:
        print("NO_CHANGES_NEEDED")
        print(f"line_count={len(original_lf.splitlines())}")
        return 0

    backup = backup_dir / f"{target.name}.{datetime.now().strftime('%Y%m%d-%H%M%S')}.bak"
    shutil.copy2(target, backup)

    if args.dry_run:
        print("DRY_RUN")
        print(f"changes={','.join(changes)}")
        print(f"backup={backup}")
        print(f"line_count={len(patched_lf.splitlines())}")
        return 0

    write_preserved(target, patched_lf, newline)
    parser_ok, parser_output = run_parser(target)
    if not parser_ok:
        shutil.copy2(backup, target)
        print("POWERSHELL_PARSE_FAILED_RESTORED_BACKUP")
        print(parser_output)
        return 4

    print("PATCHED")
    print(f"target={target.relative_to(repo).as_posix()}")
    print(f"backup={backup.relative_to(repo).as_posix()}")
    print(f"changes={','.join(changes)}")
    print(f"line_count={len(read_text(target).splitlines())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
