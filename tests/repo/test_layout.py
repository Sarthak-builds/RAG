"""Phase 3, Task 1: repo skeleton and justfile."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_DIRS = ["backend", "frontend", "docs", "prompts", "evals", "infra"]
REQUIRED_FILES = ["justfile", "AGENTS.md", ".gitignore"]
REQUIRED_RECIPES = ["check", "test", "lint", "types", "gen-types", "migrate"]


def test_required_dirs_exist():
    for name in REQUIRED_DIRS:
        assert (ROOT / name).is_dir(), f"missing directory: {name}"


def test_required_top_level_files_exist():
    for name in REQUIRED_FILES:
        assert (ROOT / name).is_file(), f"missing file: {name}"


def test_justfile_defines_required_recipes():
    text = (ROOT / "justfile").read_text(encoding="utf-8")
    for recipe in REQUIRED_RECIPES:
        pattern = re.compile(rf"(?m)^{re.escape(recipe)}\s*:")
        assert pattern.search(text), f"justfile does not define recipe: {recipe}"


def test_agents_md_is_under_150_lines():
    lines = (ROOT / "AGENTS.md").read_text(encoding="utf-8").splitlines()
    assert len(lines) < 150, f"AGENTS.md has {len(lines)} lines, target is under 150"
