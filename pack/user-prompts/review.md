# Review prompt

Copy this, choose one target mode, fill in the criteria, and paste it to an agent. This asks for a standalone review of code that already exists; it is not delivery state and does not start or advance the selected action.

---

Give me a standalone, read-only code review. Choose exactly one target mode and say which one you used.

- CURRENT TREE at `<ref>`: review the complete tree at that single ref. There is no baseline, so this is a whole-tree review, never a diff review and never an empty one.
- DIFF from `<base>` to `<tip>`: review the changes in `<base>..<tip>`, plus only the surrounding code needed to judge them. Do not widen this into a whole-tree review.

Criteria: `<paste the principles, acceptance criteria and constraints to review against>`.

Before reviewing, resolve every named ref to its full commit ID, then state the target mode, those IDs, the criteria, and whether the working tree is clean or dirty. If a ref or a criterion is missing or ambiguous, stop and ask rather than guess.

Work read-only. Do not edit, create, format, stage, commit or delete any file in the reviewed repository; do not change its index, refs or configuration; never write a findings file, report, ledger, round log, review directory, plan tree or task state anywhere. Reproduce behaviour only in a human-authorised scratch directory outside that repository. Record `git status --porcelain` before and after reviewing; report any difference rather than a read-only review. Return the review directly in this response.

Give each finding a severity of `low`, `medium`, `high` or `critical`, explain its impact against the stated criteria, and give reproducible evidence: an exact command with its relevant output, or `<full-commit-id>:<file>:<line>`. Report no unsupported suspicion. An improvement outside the criteria is out of scope, not a finding.

If nothing violates the criteria, say `No findings.` and briefly list the target, the criteria and the checks you ran.
