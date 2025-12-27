#!/usr/bin/env python3
"""State Model Purity Guard for Base 1.0.

Verifies that all classes in src/state/models/ and src/state/subsystems/
are pure Pydantic BaseModel classes with no business logic.

Allowed:
- class definition
- type annotations (annotated assignments)
- pass statements
- docstrings
- field assignments with defaults

Forbidden:
- custom methods (except empty __init__)
- validators (@validator, @field_validator, @root_validator, @model_validator)
- model_post_init
- business logic
- any method that performs computation
- imports inside class bodies
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path


class ModelPurityVisitor(ast.NodeVisitor):
    """AST visitor to check model purity."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.violations: list[tuple[str, int, str]] = []
        self.current_class: str | None = None
        # Track BaseModel names (including aliases like BaseModel as BM)
        self.basemodel_names: set[str] = {"BaseModel"}

    def visit_Import(self, node: ast.Import) -> None:
        """Track imports to detect BaseModel aliases."""
        for alias in node.names:
            if alias.name == "pydantic":
                # Track if BaseModel is imported from pydantic
                # We'll check for BaseModel usage in class bases
                pass
            elif alias.name.startswith("pydantic."):
                # from pydantic import BaseModel
                if "BaseModel" in alias.name:
                    if alias.asname:
                        self.basemodel_names.add(alias.asname)
                    else:
                        self.basemodel_names.add("BaseModel")

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Track imports to detect BaseModel aliases."""
        if node.module == "pydantic" or (node.module and node.module.startswith("pydantic.")):
            for alias in node.names:
                if alias.name == "BaseModel":
                    if alias.asname:
                        self.basemodel_names.add(alias.asname)
                    else:
                        self.basemodel_names.add("BaseModel")

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Check class definition."""
        # Check if this class inherits from BaseModel (including aliases)
        has_basemodel = False
        for base in node.bases:
            base_name = None
            if isinstance(base, ast.Name):
                base_name = base.id
            elif isinstance(base, ast.Attribute):
                # Handle pydantic.BaseModel or typing.BaseModel
                # Only recognize these explicit patterns to avoid false positives
                if isinstance(base.value, ast.Name):
                    if base.value.id == "pydantic" and base.attr == "BaseModel":
                        has_basemodel = True
                        break
                    elif base.value.id in ("typing", "typing_extensions") and base.attr == "BaseModel":
                        has_basemodel = True
                        break
                # Do not check base.attr for other attributes - this would incorrectly
                # match classes like "mymodule.BaseModel" which are not Pydantic models
            
            # Check if base_name (from ast.Name) matches any known BaseModel alias
            if base_name and base_name in self.basemodel_names:
                has_basemodel = True
                break

        if not has_basemodel:
            # Not a BaseModel class, skip (but visit nested classes)
            self.generic_visit(node)
            return

        # This is a BaseModel class - check it
        self.current_class = node.name
        self._check_class_body(node)
        self.current_class = None
        
        # Also check nested classes (they might also be BaseModel)
        for item in node.body:
            if isinstance(item, ast.ClassDef):
                self.visit_ClassDef(item)

    def _check_class_body(self, node: ast.ClassDef) -> None:
        """Check class body for purity violations."""
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                # Check method name
                method_name = item.name

                # Allow __init__ if it's empty or only has pass/docstring
                if method_name == "__init__":
                    if self._has_logic(item):
                        self.violations.append(
                            (
                                self.current_class or "Unknown",
                                item.lineno,
                                f"__init__ contains logic (should be empty or pass only)",
                            )
                        )
                    continue

                # Check for validator decorators
                has_validator_decorator = False
                for decorator in item.decorator_list:
                    decorator_name = self._get_decorator_name(decorator)
                    if decorator_name in (
                        "validator",
                        "field_validator",
                        "root_validator",
                        "model_validator",
                        "field_serializer",
                        "model_serializer",
                    ):
                        has_validator_decorator = True
                        self.violations.append(
                            (
                                self.current_class or "Unknown",
                                item.lineno,
                                f"Validator decorator '{decorator_name}' found (not allowed in pure models)",
                            )
                        )

                # All other methods are violations (unless it's a validator we already flagged)
                if not has_validator_decorator:
                    self.violations.append(
                        (
                            self.current_class or "Unknown",
                            item.lineno,
                            f"Custom method '{method_name}' found (only empty __init__ allowed)",
                        )
                    )

            elif isinstance(item, ast.Import) or isinstance(item, ast.ImportFrom):
                # Imports inside BaseModel class body are not allowed
                self.violations.append(
                    (
                        self.current_class or "Unknown",
                        item.lineno,
                        "Import inside BaseModel class body (not allowed in pure models)",
                    )
                )

            elif isinstance(item, ast.Expr):
                # Allow docstrings (Expr with Constant string)
                if isinstance(item.value, ast.Constant) and isinstance(
                    item.value.value, str
                ):
                    continue
                # Also allow old-style docstrings (Str nodes in older Python)
                if isinstance(item.value, ast.Str):
                    continue
                # Non-docstring expressions are not allowed (e.g., function calls, computations)
                self.violations.append(
                    (
                        self.current_class or "Unknown",
                        item.lineno,
                        f"Non-docstring expression found (not allowed in pure models): {type(item.value).__name__}",
                    )
                )

            elif isinstance(item, ast.Pass):
                # Allow pass statements
                continue

            elif isinstance(item, ast.AnnAssign):
                # Allow type annotations (field definitions)
                continue

            elif isinstance(item, ast.Assign):
                # Allow field assignments with defaults
                continue

            elif isinstance(item, ast.If):
                # Conditional logic is not allowed
                self.violations.append(
                    (
                        self.current_class or "Unknown",
                        item.lineno,
                        "Conditional logic found (not allowed in pure models)",
                    )
                )

            elif isinstance(item, ast.For) or isinstance(item, ast.While):
                # Loops are not allowed
                self.violations.append(
                    (
                        self.current_class or "Unknown",
                        item.lineno,
                        f"Loop found (not allowed in pure models)",
                    )
                )

            elif isinstance(item, ast.With):
                # Context managers are not allowed
                self.violations.append(
                    (
                        self.current_class or "Unknown",
                        item.lineno,
                        "Context manager found (not allowed in pure models)",
                    )
                )

            elif isinstance(item, ast.Try) or isinstance(item, ast.TryStar):
                # Exception handling is not allowed
                self.violations.append(
                    (
                        self.current_class or "Unknown",
                        item.lineno,
                        "Exception handling found (not allowed in pure models)",
                    )
                )

            elif isinstance(item, ast.AsyncFunctionDef):
                # Async methods are not allowed
                self.violations.append(
                    (
                        self.current_class or "Unknown",
                        item.lineno,
                        f"Async method '{item.name}' found (not allowed in pure models)",
                    )
                )

            elif isinstance(item, ast.ClassDef):
                # Nested classes are handled separately via visit_ClassDef
                # This is allowed, but we'll check it recursively
                pass

            # Any other AST node type in a BaseModel class is suspicious
            # Be conservative and flag unknown constructs
            else:
                # Unknown construct - flag it
                self.violations.append(
                    (
                        self.current_class or "Unknown",
                        item.lineno,
                        f"Unexpected construct '{type(item).__name__}' found (not allowed in pure models)",
                    )
                )

    def _get_decorator_name(self, decorator: ast.expr) -> str:
        """Extract decorator name from AST node."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return decorator.attr
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                return decorator.func.id
            elif isinstance(decorator.func, ast.Attribute):
                return decorator.func.attr
        return "unknown"

    def _has_logic(self, func: ast.FunctionDef) -> bool:
        """Check if function has any logic beyond pass/docstring."""
        for item in func.body:
            if isinstance(item, ast.Pass):
                continue
            if isinstance(item, ast.Expr):
                # Check if it's a docstring
                if isinstance(item.value, ast.Constant) and isinstance(
                    item.value.value, str
                ):
                    continue
                if isinstance(item.value, ast.Str):  # Old-style docstring
                    continue
            # Any other statement means there's logic
            return True
        return False


def check_file(file_path: Path) -> list[tuple[str, int, str]]:
    """Check a single Python file for model purity violations."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR: Could not read {file_path}: {e}", file=sys.stderr)
        return []

    try:
        tree = ast.parse(content, filename=str(file_path))
    except SyntaxError as e:
        print(f"WARNING: Could not parse {file_path}: {e}", file=sys.stderr)
        return []

    visitor = ModelPurityVisitor(file_path)
    visitor.visit(tree)
    return visitor.violations


def main() -> int:
    """Main entry point."""
    repo_root = Path(__file__).parent.parent
    models_dir = repo_root / "src" / "state" / "models"
    subsystems_dir = repo_root / "src" / "state" / "subsystems"

    all_violations: list[tuple[Path, str, int, str]] = []

    # Check models directory
    if models_dir.exists():
        for py_file in models_dir.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue  # Skip __init__.py files
            violations = check_file(py_file)
            for class_name, lineno, message in violations:
                all_violations.append((py_file, class_name, lineno, message))

    # Check subsystems directory
    if subsystems_dir.exists():
        for py_file in subsystems_dir.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue  # Skip __init__.py files
            violations = check_file(py_file)
            for class_name, lineno, message in violations:
                all_violations.append((py_file, class_name, lineno, message))

    if all_violations:
        print("=" * 80, file=sys.stderr)
        print("STATE MODEL PURITY VIOLATION DETECTED", file=sys.stderr)
        print("=" * 80, file=sys.stderr)
        print("", file=sys.stderr)
        print(
            "State models must be pure Pydantic BaseModel classes with no business logic.",
            file=sys.stderr,
        )
        print("", file=sys.stderr)

        for file_path, class_name, lineno, message in all_violations:
            rel_path = file_path.relative_to(repo_root)
            print(f"  {rel_path}:{lineno}", file=sys.stderr)
            print(f"    Class: {class_name}", file=sys.stderr)
            print(f"    Violation: {message}", file=sys.stderr)
            print("", file=sys.stderr)

        print("=" * 80, file=sys.stderr)
        return 1

    print("✓ State model purity check passed: all models are pure BaseModel classes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
