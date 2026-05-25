"""Legacy operator-product CLI wrapper.

Provider/product runs are not implemented here. They are forwarded to the
canonical ``python -m ia_carmine.cli run`` surface so config resolution,
profiles, field sources and gate propagation have a single owner.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from ia_carmine._shared.report_io import print_json_report

from .direct_command import resolve_config, run_dir_for
from .io_utils import now_stamp
from .models import LauncherConfig
from .runner import analyze_code_product

PROVIDER_WRAPPER_FLAGS = {"--run", "--run-and-review"}
LOCAL_CODE_PRODUCT_FLAGS = {"--code-product", "--confirm", "--require-all-integrated"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Compatibility wrapper: provider runs are forwarded to "
            "`python -m ia_carmine.cli run`; only review/apply actions execute here."
        )
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--request-file", default="")
    parser.add_argument("--run-label", default="")
    parser.add_argument("--intermediate-root", default="")
    parser.add_argument("--final-root", default="")
    parser.add_argument("--python-exe", default="")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--revision-context", default="")
    parser.add_argument("--code-product", default="")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--run-and-review", action="store_true")
    parser.add_argument("--review-code-product", action="store_true")
    parser.add_argument("--apply-safe", action="store_true")
    parser.add_argument("--confirm", default="")
    parser.add_argument("--require-all-integrated", action="store_true")
    return parser


def _option_present(argv: list[str], option: str) -> bool:
    return any(token == option or token.startswith(f"{option}=") for token in argv)


def _strip_provider_wrapper_flags(argv: list[str]) -> list[str]:
    return [token for token in argv if token not in PROVIDER_WRAPPER_FLAGS]


def _forward_to_canonical_run(raw_argv: list[str]) -> int:
    local_flags = sorted(flag for flag in LOCAL_CODE_PRODUCT_FLAGS if _option_present(raw_argv, flag))
    if local_flags:
        raise SystemExit(
            "local code-product flags require --review-code-product or --apply-safe: "
            + ", ".join(local_flags)
        )
    command = [
        sys.executable,
        "-m",
        "ia_carmine.cli",
        "run",
        *_strip_provider_wrapper_flags(raw_argv),
    ]
    completed = subprocess.run(command, check=False)
    return int(completed.returncode)


def _review_config(args: argparse.Namespace, repo_root: Path, stamp: str) -> LauncherConfig:
    _ = stamp
    missing = [
        flag
        for flag, value in (
            ("--run-label", args.run_label),
            ("--intermediate-root", args.intermediate_root),
            ("--final-root", args.final_root),
        )
        if not str(value or "").strip()
    ]
    if missing:
        raise SystemExit(
            "missing explicit local review surface parameter(s): " + ", ".join(missing)
        )
    if not str(args.request_file or args.code_product or "").strip():
        raise SystemExit("--request-file or --code-product explicit required")
    request_file = Path(args.request_file) if args.request_file else Path(args.code_product)
    return LauncherConfig(
        repo_root=repo_root,
        request_file=request_file,
        intermediate_root=Path(args.intermediate_root),
        final_root=Path(args.final_root),
        run_label=args.run_label,
        python_exe=args.python_exe,
        stamp=stamp,
        revision_context=args.revision_context,
    )


def main(argv: list[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    parser = build_parser()
    args, unknown = parser.parse_known_args(raw_argv)
    local_action = bool(args.review_code_product or args.apply_safe)
    if not local_action:
        return _forward_to_canonical_run(raw_argv)
    if unknown:
        raise SystemExit(
            "unsupported local review/apply parameter(s): " + " ".join(unknown)
        )
    if args.apply_safe and args.confirm != "safe_apply":
        raise SystemExit("--apply-safe requires --confirm safe_apply")
    if args.run or args.run_and_review:
        raise SystemExit("--run/--run-and-review are provider actions; do not mix with local review/apply")

    repo_root = Path(args.repo_root).resolve()
    stamp = args.stamp or now_stamp()
    config = _review_config(args, repo_root, stamp)
    code_product = Path(args.code_product)
    if not args.code_product and args.request_file:
        code_product = Path(args.request_file)
    output_dir = run_dir_for(resolve_config(config))
    report = analyze_code_product(
        repo_root,
        code_product,
        output_dir,
        apply_safe=args.apply_safe,
        require_all_integrated=args.require_all_integrated,
        python_exe=args.python_exe,
    )
    report["operator_product_core_cli_mode"] = "local_code_product_review_apply"
    report["provider_run_entrypoint"] = "python -m ia_carmine.cli run"
    print_json_report(report)
    return 0 if report.get("passed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
