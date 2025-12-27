#!/usr/bin/env python3
"""Phase Boundary Import Guard for Base 1.0 - Lexical AST-based checker."""

from __future__ import annotations

import ast
import sys
from pathlib import Path


FORBIDDEN_PACKAGES = {
    "communication", "events", "experience", "identity", "learning",
    "maintenance", "media", "memory", "notifications", "presence",
    "relational", "social_rhythm", "subsystems",
}


class ImportVisitor(ast.NodeVisitor):
    def __init__(self):
        self.violations: list[tuple[str, int]] = []

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            parts = alias.name.split(".")
            root = parts[0] if parts else None
            if root == "src" and len(parts) > 1 and parts[1] in FORBIDDEN_PACKAGES:
                self.violations.append((alias.name, node.lineno))
            elif root in FORBIDDEN_PACKAGES:
                self.violations.append((alias.name, node.lineno))

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.level > 0:  # ALL relative imports ALLOWED
            return
        if not node.module:
            return
        if node.module == "src":  # Special case: `from src import X`
            for alias in node.names:
                if alias.name in FORBIDDEN_PACKAGES:
                    self.violations.append((f"src.{alias.name}", node.lineno))
            return
        parts = node.module.split(".")
        root = parts[0] if parts else None
        if root == "src" and len(parts) > 1 and parts[1] in FORBIDDEN_PACKAGES:
            self.violations.append((node.module, node.lineno))
        elif root in FORBIDDEN_PACKAGES:
            self.violations.append((node.module, node.lineno))


def check_file(file_path: Path) -> list[tuple[str, int]]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(file_path))
    except (OSError, SyntaxError) as e:
        print(f"WARNING: Could not parse {file_path}: {e}", file=sys.stderr)
        return []
    visitor = ImportVisitor()
    visitor.visit(tree)
    return visitor.violations


def main() -> int:
    repo_root = Path(__file__).parent.parent
    state_dir = repo_root / "src" / "state"
    if not state_dir.exists():
        print(f"ERROR: {state_dir} does not exist", file=sys.stderr)
        return 1
    all_violations: list[tuple[Path, str, int]] = []
    for py_file in state_dir.rglob("*.py"):
        for module_name, lineno in check_file(py_file):
            all_violations.append((py_file, module_name, lineno))
    if all_violations:
        print("=" * 80, file=sys.stderr)
        print("PHASE BOUNDARY VIOLATION DETECTED", file=sys.stderr)
        print("=" * 80, file=sys.stderr)
        print("", file=sys.stderr)
        print("Files under src/state/ must not import from forbidden modules.", file=sys.stderr)
        print("", file=sys.stderr)
        for file_path, module_name, lineno in all_violations:
            rel_path = file_path.relative_to(repo_root)
            print(f"  {rel_path}:{lineno}", file=sys.stderr)
            print(f"    Illegal import: {module_name}", file=sys.stderr)
            print("", file=sys.stderr)
        print("=" * 80, file=sys.stderr)
        return 1
    print("✓ Phase boundary check passed: no forbidden imports detected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
