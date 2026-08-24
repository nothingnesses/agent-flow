# Q-78 post-escalation round 3 fix brief

Act only as planner in the isolated `plan/q78-design-pass` worktree. Read `AGENTS.md`, round-3 triage, reviewer files, the ledger from `RESUME HERE`, and the active increment sidecar.

Fix only R3-1 and R3-2.

For R3-1, add end-to-end TOML `next` oracles for intent-bearing `ReadyToPlan` and `Blocked` steps on both human and JSON surfaces. Pin complete context keys and exact intent values. Add a red mutation that drops only the `build_pending_loop` transfer while leaving in-progress transfer and `build_context` correct. Require both pending-state oracles to fail and the existing matrices and seam table to stay green.

For R3-2, replace the help-row guard with one that counts every command token, including hyphenated names, or assert the exact Clap subcommand-name set through `CommandFactory`. Add a hyphenated extra-subcommand red control that must fail while the current seven product commands plus help pass.

Update the authoritative test list and increment-3 retention only when exact new test names require it.

Do not fix or re-open R3-3, R3-4, earlier class-2 findings, dismissals or accepted residuals. No waiver is authorised.

Edit only `docs/plans/agent-scaffold.steps/step-intent-encoding.md` and the generated `docs/plans/agent-scaffold.md`. Do not edit plan TOML, questions, exploration, metrics, ledger, reviews, code, tests, fixtures, README, changelog or pack. The tests specify future implementation work.

Use direnv. Run both validations, render and strict render check, tests, Clippy, diff, ASCII and exact-path checks. Commit with a `docs:` subject. Do not push.
