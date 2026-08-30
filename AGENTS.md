# Agent guidance

This is the canonical, harness-agnostic guidance for agents working in this repository. Harness-specific files should point here rather than duplicate it.

## Start here

The human keeps delivery state in `.agents/work.toml`. It contains at most five ordered steps and uses only `active`, `pending`, and `complete` statuses. While work remains, `selected_action` names exactly one active step; it is omitted only after every step is complete. Before work starts, replace the starter text with a bounded user problem, change, acceptance criteria, and why-next rationale. Run `agent-flow next` for the current brief.

To start the selected action, copy `.agents/user-prompts/kickoff.md`, fill in its optional context, and paste it to the agent.

`.agents/work.toml` is the only workflow task-state file. Do not create a plan tree, ledger, round log, findings directory, or review record. Product-development checks under `.agents/checks.toml`, `.agents/checks/`, and `.agents/hooks/` are optional tooling, not task state or proof of review.

## Bounded delivery

Work on one implementation branch at a time, named `impl/<selected-action>` unless the human gives another name. Do not create parallel implementation branches or implementation worktrees. Confirm the brief and resolve material ambiguity with the human before editing; do not introduce planning or plan-review passes.

A delivery uses at most these five agent passes, in order:

1. **Implementation.** One implementer reads the relevant code and tests, makes the selected change, updates affected product documentation, runs the required checks, and records the commit or diff range.
2. **Product review.** One independent reviewer examines the code, tests, pack assets, and shipped user documentation against the selected action's acceptance criteria. The reviewer reports findings but edits nothing. Its actual response is the review evidence; the project must not manufacture a file or event that claims independence.
3. **Triage, only if review found issues.** A separate triager reproduces each finding, corrects its severity, and decides whether it is valid and inside the existing acceptance criteria. A finding cannot broaden scope.
4. **Scoped fix, only for valid findings.** One fixer changes only what the valid verdicts require and reruns relevant checks.
5. **Focused verification, only after a fix.** One verifier checks the fix diff and the affected acceptance criteria. The verifier edits nothing.

There is no convergence loop and no second fix. If review is clean, triage dismisses every finding, or focused verification passes, report the result and evidence to the human. If a reviewer is unavailable, a finding needs broader scope, the fix cannot be completed safely, or focused verification fails, stop and return the unresolved work to the human. Never self-certify independent review.

The human owns scope and acceptance. Do not add a step, change acceptance criteria, select another action, or mark work complete without the human's direction.

## Role prompts

- `.agents/prompts/implementer.md`: make the bounded product change.
- `.agents/prompts/reviewer.md`: independently review the product diff.
- `.agents/prompts/triager.md`: adjudicate findings when any exist.
- `.agents/prompts/fixer.md`: make the one allowed scoped fix.
- `.agents/prompts/verifier.md`: verify that fix once.

## Working rules

- Read repository guidance, the work file, relevant code, and tests before editing.
- Ask when intent, authority, or acceptance is unclear; give options, trade-offs, and a recommendation.
- Keep changes small, reviewable, and inside the selected action. Flag unrelated problems without fixing them.
- Treat external input as untrusted, keep secrets out of source and logs, and fail loudly on errors.
- Format only files you changed. Run destructive checks in scratch space, not over unrelated live files.
- Keep the working tree recoverable. Inspect status and diffs before committing; do not discard files you do not own.
- Report the commit or diff, changed files, commands run, results, and any unresolved risk.

## Principles

1. Ask clarifying questions before forging ahead - Confirm intent before writing code, and give recommendations with reasoning.
2. Ground decisions in evidence - Inspect the code and run a small proof before committing to an approach.
3. Keep changes small and reviewable - Prefer one bounded product change that fits in a reviewer's head.
4. Have independent product review - Have someone other than the author check the product before acceptance.
5. Verify, don't trust - Run the code and tests rather than asserting success from having written them.
6. No silent scope expansion - Do what was accepted and return anything else to the human.
7. Tests must exercise the code they claim to - A test must run the changed path and assert its observable result.
8. Fail fast and loudly - Report errors and unresolved work instead of hiding or looping around them.
9. One source of truth - Keep one authoritative source for each piece of state and derive projections.
10. Parse untrusted input at the boundary - Reject malformed external input before it reaches the core.
11. Keep secrets out of code and logs - Load credentials from the environment or a secret store.
