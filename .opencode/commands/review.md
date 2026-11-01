---
description: Hand the current working-tree state to the reviewer subagent and return its verdict.
agent: reviewer
---

Review mode: $ARGUMENTS

The reviewer examines the completed state of the last task (or the working-tree diff) against
AGENTS.md, runs `just check`, and reports a verdict with file references and the gate output.
Do not apply fixes during review; document them instead.
