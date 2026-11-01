"""Phase 3, Task 5 acceptance: no create_all outside test fixtures (AGENTS: schema only via Alembic)."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_SRC = ROOT / "backend" / "src"
_TESTS = ROOT / "tests"
_CREATE_ALL = re.compile(r"\bcreate_all\b")


def test_no_create_all_in_src():
    offenders = [str(p.relative_to(ROOT)) for p in _SRC.rglob("*.py") if _CREATE_ALL.search(p.read_text(encoding="utf-8"))]
    assert offenders == [], f"create_all must not appear in backend/src: {offenders}"


def test_create_all_only_in_test_fixtures():
    offenders = []
    guard = Path(__file__).name
    for path in _TESTS.rglob("*.py"):
        relative = path.relative_to(ROOT)
        if relative.name == guard:
            continue
        if _CREATE_ALL.search(path.read_text(encoding="utf-8")) and relative.name not in ("conftest.py",):
            offenders.append(str(relative))
    assert offenders == [], f"create_all outside test fixtures: {offenders}"
