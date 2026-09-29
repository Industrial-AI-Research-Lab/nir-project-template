"""Rename the package once: `make rename NAME=my_package`.

Moves src/nir_project to src/<name> and replaces the old name wherever the template mentions it.
"""

import re
import sys
from pathlib import Path

OLD = "nir_project"
ROOT_FILES = [
    "pyproject.toml",
    "Makefile",
    "AGENTS.md",
    "README.md",
    "README.ru.md",
    ".env.example",
]


def replace_in(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    updated = text.replace(old, new).replace(old.replace("_", "-"), new.replace("_", "-"))
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        print(f"updated {path}")


def main() -> int:
    if len(sys.argv) != 2 or not re.fullmatch(r"[a-z][a-z0-9_]*", sys.argv[1]):
        print("usage: rename.py <new_package_name>   (lowercase letters, digits, underscores)")
        return 1
    new = sys.argv[1]
    root = Path(__file__).resolve().parents[1]
    src_old, src_new = root / "src" / OLD, root / "src" / new
    if not src_old.exists():
        print(f"{src_old} not found: already renamed?")
        return 1
    src_old.rename(src_new)
    for path in [root / name for name in ROOT_FILES]:
        if path.exists():
            replace_in(path, OLD, new)
    for path in list(src_new.rglob("*.py")) + list((root / "tests").rglob("*.py")):
        replace_in(path, OLD, new)
    print(f"renamed {OLD} -> {new}; now run: uv lock && make check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
