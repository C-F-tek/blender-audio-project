"""Python symbol extraction for the project AI index."""

from __future__ import annotations

import ast
import warnings

def target_name(target: ast.expr) -> str | None:
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute):
        return target.attr
    return None


def format_syntax_warning(message: warnings.WarningMessage) -> str:
    """Return a compact warning string for manifest/index output."""
    return f"line {message.lineno}: {message.message}"


def extract_symbols(source: str, filename: str = "<unknown>") -> dict:
    symbols = {
        "imports": [],
        "functions": [],
        "classes": [],
        "assignments": [],
        "syntax_warnings": [],
    }
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", SyntaxWarning)
            tree = ast.parse(source, filename=filename)
        symbols["syntax_warnings"] = [format_syntax_warning(item) for item in caught]
    except SyntaxError as exc:
        symbols["syntax_error"] = f"{filename}: {exc}"
        return symbols

    for node in tree.body:
        if isinstance(node, ast.Import):
            symbols["imports"].extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            names = ", ".join(alias.name for alias in node.names)
            symbols["imports"].append(f"from {module} import {names}")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            symbols["functions"].append(
                {
                    "name": node.name,
                    "line": node.lineno,
                    "args": [arg.arg for arg in node.args.args],
                    "async": isinstance(node, ast.AsyncFunctionDef),
                }
            )
        elif isinstance(node, ast.ClassDef):
            methods = []
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods.append({"name": child.name, "line": child.lineno})
            symbols["classes"].append({"name": node.name, "line": node.lineno, "methods": methods})
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                name = target_name(target)
                if name:
                    symbols["assignments"].append(name)
        elif isinstance(node, ast.AnnAssign):
            name = target_name(node.target)
            if name:
                symbols["assignments"].append(name)

    return symbols
