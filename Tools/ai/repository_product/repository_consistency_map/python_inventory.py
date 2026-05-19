"""Python inventory extraction for repository consistency maps."""

from __future__ import annotations

import ast
from collections.abc import Iterable
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path
from typing import Any

from Tools.ai.repository_product.repository_consistency_map.paths import (
    bounded_worker_count,
    iter_files,
    read_text,
    repo_rel,
)


def resolve_scan_worker_backend(worker_backend: str, worker_count: int) -> str:
    normalized = (worker_backend or "process").strip().lower()
    if worker_count <= 1:
        return "serial"
    if normalized in {"process", "cpu", "multiprocessing"}:
        return "process"
    if normalized in {"thread", "threads"}:
        return "thread"
    if normalized == "auto":
        return "process"
    raise ValueError(f"Unsupported repository consistency worker backend: {worker_backend}")


def literal_string(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def extract_argparse_flags(tree: ast.AST) -> list[str]:
    flags: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        attr = node.func
        if not isinstance(attr, ast.Attribute) or attr.attr != "add_argument":
            continue
        for arg in node.args:
            value = literal_string(arg)
            if value and value.startswith("--"):
                flags.add(value)
    return sorted(flags)


def extract_python_symbols(tree: ast.AST) -> dict[str, list[str]]:
    functions: list[str] = []
    classes: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
    return {"functions": sorted(set(functions)), "classes": sorted(set(classes))}


def module_to_paths(module: str, repo_root: Path) -> list[str]:
    parts = [part for part in module.split(".") if part]
    if not parts:
        return []
    return [
        (repo_root / Path(*parts)).with_suffix(".py").as_posix(),
        (repo_root / Path(*parts) / "__init__.py").as_posix(),
    ]


def local_module_exists(module: str, repo_root: Path) -> bool:
    for candidate in module_to_paths(module, repo_root):
        if Path(candidate).exists():
            return True
    return False


def extract_exported_symbols(tree: ast.AST) -> set[str]:
    symbols: set[str] = set(extract_python_symbols(tree)["functions"])
    symbols.update(extract_python_symbols(tree)["classes"])
    for node in tree.body if isinstance(tree, ast.Module) else []:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    symbols.add(target.id)
                elif isinstance(target, (ast.Tuple, ast.List)):
                    for item in target.elts:
                        if isinstance(item, ast.Name):
                            symbols.add(item.id)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                symbols.add(alias.asname or alias.name.split(".", 1)[0])
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name != "*":
                    symbols.add(alias.asname or alias.name)
    return symbols


def local_module_symbol_exists(module: str, symbol: str, repo_root: Path) -> bool:
    if symbol == "*":
        return True
    for candidate in module_to_paths(module, repo_root):
        path = Path(candidate)
        if not path.exists() or not path.is_file():
            continue
        text, error = read_text(path)
        if error:
            continue
        try:
            tree = ast.parse(text, filename=repo_rel(path, repo_root))
        except SyntaxError:
            continue
        if symbol in extract_exported_symbols(tree):
            return True
    return False


def extract_local_import_findings(
    tree: ast.AST, source: str, repo_root: Path
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    local_prefixes = ("Tools", "Scripting", "indexAI")
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                if root in local_prefixes and not local_module_exists(alias.name, repo_root):
                    findings.append(
                        {
                            "source": source,
                            "line": getattr(node, "lineno", 0),
                            "module": alias.name,
                            "kind": "python_import_missing",
                        }
                    )
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                continue
            module = node.module or ""
            root = module.split(".", 1)[0]
            if root not in local_prefixes:
                continue
            if not local_module_exists(module, repo_root):
                findings.append(
                    {
                        "source": source,
                        "line": getattr(node, "lineno", 0),
                        "module": module,
                        "kind": "python_import_missing",
                    }
                )
                continue
            for alias in node.names:
                symbol = alias.name
                if symbol == "*":
                    continue
                if not local_module_symbol_exists(module, symbol, repo_root):
                    findings.append(
                        {
                            "source": source,
                            "line": getattr(node, "lineno", 0),
                            "module": module,
                            "symbol": symbol,
                            "kind": "python_import_symbol_missing",
                        }
                    )
    return findings


def scan_python_file_task(
    task: tuple[str, str],
) -> tuple[str, dict[str, Any], list[dict[str, Any]], list[str]]:
    repo_root_raw, path_raw = task
    repo_root = Path(repo_root_raw)
    path = Path(path_raw)
    rel = repo_rel(path, repo_root)
    text, error = read_text(path)
    file_warnings: list[str] = []
    if error:
        file_warnings.append(f"{rel}: {error}")
        return (
            rel,
            {
                "argparse_flags": [],
                "functions": [],
                "classes": [],
                "syntax_error": error,
            },
            [],
            file_warnings,
        )
    try:
        tree = ast.parse(text, filename=rel)
    except SyntaxError as exc:
        file_warnings.append(f"{rel}: SyntaxError line {exc.lineno}: {exc.msg}")
        return (
            rel,
            {
                "argparse_flags": [],
                "functions": [],
                "classes": [],
                "syntax_error": str(exc),
            },
            [],
            file_warnings,
        )
    symbols = extract_python_symbols(tree)
    item = {
        "argparse_flags": extract_argparse_flags(tree),
        "functions": symbols["functions"],
        "classes": symbols["classes"],
        "syntax_error": "",
    }
    return rel, item, extract_local_import_findings(tree, rel, repo_root), file_warnings


def extract_python_inventory(
    repo_root: Path,
    *,
    workers: int,
    python_files: list[Path] | None = None,
    worker_backend: str = "process",
    worker_cpu_target: float = 0.40,
    max_auto_workers: int | None = 8,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], list[str]]:
    inventory: dict[str, dict[str, Any]] = {}
    import_findings: list[dict[str, Any]] = []
    warnings: list[str] = []
    python_files = python_files if python_files is not None else iter_files(repo_root, {".py"})
    worker_count = bounded_worker_count(
        workers,
        len(python_files),
        cpu_target=worker_cpu_target,
        max_auto_workers=max_auto_workers,
    )
    actual_backend = resolve_scan_worker_backend(worker_backend, worker_count)
    tasks = [(str(repo_root), str(path)) for path in python_files]

    if actual_backend in {"process", "thread"}:
        executor_class = ProcessPoolExecutor if actual_backend == "process" else ThreadPoolExecutor
        with executor_class(max_workers=worker_count) as executor:
            for rel, item, file_import_findings, file_warnings in executor.map(
                scan_python_file_task, tasks
            ):
                inventory[rel] = item
                import_findings.extend(file_import_findings)
                warnings.extend(file_warnings)
    else:
        for task in tasks:
            rel, item, file_import_findings, file_warnings = scan_python_file_task(task)
            inventory[rel] = item
            import_findings.extend(file_import_findings)
            warnings.extend(file_warnings)
    return inventory, import_findings, warnings


def smoke_candidates_for_script(script: str, all_python_files: Iterable[str]) -> list[str]:
    stem = Path(script).stem.lower()
    candidates: list[str] = []
    for path in all_python_files:
        lowered = path.lower()
        if "/validation/" not in lowered and not lowered.startswith("tools/validation/"):
            continue
        if stem in lowered and ("smoke" in lowered or "check" in lowered or "test" in lowered):
            candidates.append(path)
    return sorted(candidates)
