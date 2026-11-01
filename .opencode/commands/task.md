---
description: Execute exactly one task from the active phase task list, verify with the gate, report, stop.
agent: build
---

Read AGENTS.md before anything else; it is the operating contract.

Task: $ARGUMENTS

Procedure:
1. Restate the task as a todo item and identify the files it expects to create or change.
2. Write the failing test first (TDD). Run it and confirm it fails for the right reason.
3. Add the minimal code to pass. Every outbound call needs an explicit timeout.
4. Run the verify-chain, then run `just check` - the only gate. Paste its output in your report.
5. Report in this order: discrepancies found and how you resolved them (flag for veto),
   files changed, failing-test output, passing output, full `just check` output.
6. Stop after this one task. Do not start the next until told to continue.

Hard rules: never commit unless asked; never edit lint/type/CI/opencode config, add
dependencies, or add `# type: ignore` without an explicit task; log secrets or result rows never.
