"""Phase 3, Task 6: workflow and pre-commit use the one gate, no duplication (ADR-0012)."""

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

GATE_PIECES = ("ruff", "mypy", "pytest", "lint-imports", "eslint", "tsc", "npm run lint", "npm run types")


def test_ci_runs_just_check():
    workflow = yaml.safe_load((ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8"))
    runs = [
        step.get("run", "")
        for job in workflow["jobs"].values()
        for step in job.get("steps", [])
    ]

    check_runs = [run for run in runs if run.strip() == "just check"]
    assert check_runs == ["just check"], f"exactly one 'just check' step expected, got {check_runs}"

    for run in runs:
        if run.strip() == "just check" or run.strip().startswith("npm ci"):
            continue
        for piece in GATE_PIECES:
            assert piece not in run, f"gate piece '{piece}' run outside just: {run}"


def test_pre_commit_runs_format_lint_secret_scan():
    configuration = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    hooks = [hook for repo in configuration["repos"] for hook in repo["hooks"]]
    entries = [hook["entry"] for hook in hooks]

    assert any("ruff" in entry and "format" in entry for entry in entries), entries
    assert any(entry.strip().startswith("just lint") for entry in entries), entries
    assert any("detect-secrets" in entry for entry in entries), entries


def test_secret_scan_baseline_ready():
    baseline = json.loads((ROOT / ".secrets.baseline").read_text(encoding="utf-8"))
    assert isinstance(baseline.get("results"), dict)
