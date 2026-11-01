"""Render .env.example at the repo root from app.settings (ADR-0014). Run via `just gen-env`."""

from pathlib import Path

from app.settings import render_env_example

REPO_ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    target = REPO_ROOT / ".env.example"
    target.write_text(render_env_example(), encoding="utf-8")


if __name__ == "__main__":
    main()
