"""Phase 3, Task 2: import-linter contracts hold on real code and catch violations."""

import os
import subprocess
from pathlib import Path

import pytest

BACKEND = Path(__file__).resolve().parents[1]
VIOLATING_DOMAIN_MODULE = "from violating_pkg.adapters import something\n"


def run_lint_imports(args: list[str], env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["uv", "run", "lint-imports", *args],
        cwd=BACKEND,
        check=False,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )


def test_domain_has_no_outward_imports():
    result = run_lint_imports([], env=dict(os.environ))

    assert result.returncode == 0, result.stdout + result.stderr


def test_contract_fails_on_violation(tmp_path: Path):
    package = tmp_path / "violating_pkg"
    (package / "domain").mkdir(parents=True)
    (package / "adapters").mkdir(parents=True)
    (package / "__init__.py").touch()
    (package / "domain" / "__init__.py").touch()
    (package / "adapters" / "__init__.py").touch()
    (package / "domain" / "bad_module.py").write_text(VIOLATING_DOMAIN_MODULE, encoding="utf-8")
    config = tmp_path / ".importlinter"
    config.write_text(
        "[importlinter]\n"
        "root_package = violating_pkg\n"
        "\n"
        "[importlinter:contract:forbidden]\n"
        "name = domain must not import adapters\n"
        "type = forbidden\n"
        "source_modules = violating_pkg.domain\n"
        "forbidden_modules = violating_pkg.adapters\n",
        encoding="utf-8",
    )
    env = dict(os.environ)
    env["PYTHONPATH"] = str(tmp_path)

    result = run_lint_imports(["--config", str(config)], env=env)

    assert result.returncode != 0, result.stdout
    assert "domain must not import adapters" in result.stdout


@pytest.mark.parametrize("contract", ["domain", "layers"])
def test_backend_contract_configs_list_both_contracts(contract: str):
    text = (BACKEND / ".importlinter").read_text(encoding="utf-8")

    assert f"importlinter:contract:{contract}" in text
