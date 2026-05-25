from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run_search_window_chain_smoke(repo_root: Path) -> tuple[list[str], Path | None]:
    errors: list[str] = []
    strict_window_output: Path | None = None
    smoke_dir = repo_root / "output" / "validation" / "provider_tool_loop_smoke"
    smoke_dir.mkdir(parents=True, exist_ok=True)
    search_args_path = smoke_dir / "repo_search_git_grep_args.json"
    search_output = smoke_dir / "repo_search_git_grep.json"
    search_md = smoke_dir / "repo_search_git_grep.md"
    search_broker_request_id = "smoke_repo_search_git_grep_request"
    search_args_path.write_text(
        json.dumps(
            {
                "query": "IA-Carmine",
                "path": "AGENTS.md",
                "max_results": 1,
                "broker_request_id": search_broker_request_id,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    search_run = subprocess.run(
        [
            sys.executable,
            "-m",
            "ia_carmine.runtime.runtime_tool.broker.concrete_tool_cli",
            "--repo-root",
            str(repo_root),
            "--tool",
            "repo_search_git_grep",
            "--args-file",
            str(search_args_path),
            "--output",
            str(search_output),
            "--markdown-output",
            str(search_md),
            "--timeout-seconds",
            "10",
        ],
        cwd=repo_root,
        text=True,
        capture_output=True,
        timeout=20,
    )
    try:
        search_report = json.loads(search_output.read_text(encoding="utf-8"))
    except Exception:
        search_report = {}
    search_matches = (
        search_report.get("matches")
        if isinstance(search_report.get("matches"), list)
        else []
    )
    search_refs = (
        search_report.get("runtime_file_window_authorized_refs")
        if isinstance(search_report.get("runtime_file_window_authorized_refs"), list)
        else []
    )
    if search_run.returncode != 0 or not search_report.get("passed") or not search_matches:
        errors.append("repo_search_git_grep did not produce structured matches[]")
    else:
        first_match = search_matches[0] if isinstance(search_matches[0], dict) else {}
        search_ref_id = str(first_match.get("runtime_file_window_ref_id") or "").strip()
        if (
            not first_match.get("repo_relative")
            or not first_match.get("runtime_file_window_hint")
            or not search_ref_id
            or not search_refs
        ):
            errors.append("repo_search_git_grep match lacks brokered runtime_file_window search ref")
        window_output = smoke_dir / "strict_runtime_file_window.json"
        window_md = smoke_dir / "strict_runtime_file_window.md"
        window_args_path = smoke_dir / "strict_runtime_file_window_args.json"
        window_args_path.write_text(
            json.dumps(
                {
                    "ref_id": search_ref_id,
                    "startup_manifest": str(search_output),
                    "strict_startup_refs": True,
                    "source_broker_request_id": search_broker_request_id,
                    "source_report_ref": str(search_output),
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        window_run = subprocess.run(
            [
                sys.executable,
                "-m",
                "ia_carmine",
                "runtime_file_window",
                "--repo-root",
                str(repo_root),
                "--request-args-file",
                str(window_args_path),
                "--output",
                str(window_output),
                "--markdown-output",
                str(window_md),
            ],
            cwd=repo_root,
            text=True,
            capture_output=True,
            timeout=20,
        )
        try:
            window_report = json.loads(window_output.read_text(encoding="utf-8"))
        except Exception:
            window_report = {}
        if window_run.returncode != 0 or window_report.get("passed") is not True:
            errors.append("runtime_file_window strict startup-ref read failed after structured search")
        if window_report.get("strict_startup_refs") is not True or window_report.get("startup_ref_allowed") is not True:
            errors.append("runtime_file_window strict search-ref gate did not prove brokered ref allowance")
        else:
            strict_window_output = window_output
        copied_path_output = smoke_dir / "strict_runtime_file_window_copied_path.json"
        copied_path_md = smoke_dir / "strict_runtime_file_window_copied_path.md"
        copied_path_args = smoke_dir / "strict_runtime_file_window_copied_path_args.json"
        copied_path_args.write_text(
            json.dumps(
                {
                    "path": str(first_match.get("repo_relative") or ""),
                    "startup_manifest": str(search_output),
                    "strict_startup_refs": True,
                    "source_broker_request_id": search_broker_request_id,
                    "source_report_ref": str(search_output),
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        copied_path_run = subprocess.run(
            [
                sys.executable,
                "-m",
                "ia_carmine",
                "runtime_file_window",
                "--repo-root",
                str(repo_root),
                "--request-args-file",
                str(copied_path_args),
                "--output",
                str(copied_path_output),
                "--markdown-output",
                str(copied_path_md),
            ],
            cwd=repo_root,
            text=True,
            capture_output=True,
            timeout=20,
        )
        try:
            copied_path_report = json.loads(copied_path_output.read_text(encoding="utf-8"))
        except Exception:
            copied_path_report = {}
        copied_path_errors = copied_path_report.get("errors")
        copied_path_errors = copied_path_errors if isinstance(copied_path_errors, list) else []
        if copied_path_run.returncode == 0 or "runtime_file_window_path_not_in_startup_refs" not in copied_path_errors:
            errors.append("runtime_file_window accepted copied search path without brokered search ref")
        fake_search_report = smoke_dir / "fake_search_report.json"
        fake_ref_id = "fake_search_match_001"
        fake_search_report.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "kind": "repo_search_git_grep",
                    "passed": True,
                    "runtime_file_window_authorized_refs": [
                        {
                            "ref_id": fake_ref_id,
                            "kind": "runtime_file_window_search_ref",
                            "path": str(first_match.get("repo_relative") or ""),
                        }
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        fake_window_args = smoke_dir / "strict_runtime_file_window_fake_search_args.json"
        fake_window_args.write_text(
            json.dumps(
                {
                    "ref_id": fake_ref_id,
                    "startup_manifest": str(fake_search_report),
                    "strict_startup_refs": True,
                    "source_broker_request_id": search_broker_request_id,
                    "source_report_ref": str(fake_search_report),
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        fake_window_output = smoke_dir / "strict_runtime_file_window_fake_search.json"
        fake_window_md = smoke_dir / "strict_runtime_file_window_fake_search.md"
        fake_window_run = subprocess.run(
            [
                sys.executable,
                "-m",
                "ia_carmine",
                "runtime_file_window",
                "--repo-root",
                str(repo_root),
                "--request-args-file",
                str(fake_window_args),
                "--output",
                str(fake_window_output),
                "--markdown-output",
                str(fake_window_md),
            ],
            cwd=repo_root,
            text=True,
            capture_output=True,
            timeout=20,
        )
        try:
            fake_window_report = json.loads(fake_window_output.read_text(encoding="utf-8"))
        except Exception:
            fake_window_report = {}
        fake_errors = fake_window_report.get("errors")
        fake_errors = fake_errors if isinstance(fake_errors, list) else []
        if (
            fake_window_run.returncode == 0
            or "runtime_file_window_search_manifest_not_broker_authorized" not in fake_errors
        ):
            errors.append("runtime_file_window accepted fake search report without broker binding")
    return errors, strict_window_output
