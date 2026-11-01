"""Phase 3, Task 7: opencode config mirrors the mentor procedure and is verified against docs."""

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

ACTIONS = ("allow", "ask", "deny")


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"no frontmatter in {path}"
    body, _ = text.split("\n---\n", 1)
    return yaml.safe_load(body)


def _assert_valid_actions(rules, path="permission"):
    if isinstance(rules, str):
        assert rules in ACTIONS, f"{path}: invalid action {rules!r}"
    elif isinstance(rules, dict):
        for key, value in rules.items():
            _assert_valid_actions(value, f"{path}.{key}")
    else:
        raise AssertionError(f"{path}: unexpected type {type(rules)!r}")


def test_opencode_json_configures_permissions():
    config = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
    assert config["$schema"] == "https://opencode.ai/config.json"

    permission = config["permission"]
    _assert_valid_actions(permission)

    assert permission["*"] == "ask"
    assert permission["bash"]["*"] == "ask"
    assert permission["bash"]["git push*"] == "deny"
    assert permission["bash"]["git commit *"] == "ask"


def test_reviewer_agent_has_no_edit_permission():
    agent = _frontmatter(ROOT / ".opencode" / "agents" / "reviewer.md")
    assert agent["mode"] == "subagent"
    assert agent["description"]
    assert agent["permission"]["edit"] == "deny"
    _assert_valid_actions(agent["permission"], "reviewer.permission")


def test_task_command_references_the_procedure():
    command = _frontmatter(ROOT / ".opencode" / "commands" / "task.md")
    body = (ROOT / ".opencode" / "commands" / "task.md").read_text(encoding="utf-8")
    assert command["description"]
    assert "AGENTS.md" in body
    assert "just check" in body
    assert "$ARGUMENTS" in body


def test_review_command_invokes_the_reviewer():
    command = _frontmatter(ROOT / ".opencode" / "commands" / "review.md")
    assert command["agent"] == "reviewer"
