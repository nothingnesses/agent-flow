# Q-78 reset round 4 foreclosure fix brief

Act only as the planner for this repair. Work only in the isolated `plan/q78-design-pass` worktree. Do not edit the main checkout.

## Authority

Read:

- `AGENTS.md`.
- `docs/plans/agent-scaffold.reviews/q78-reset-r4-triage.md`.
- Both reset round 4 reviewer files.
- `docs/plans/agent-scaffold.ledger.md`, starting at `RESUME HERE`.
- The current `step-intent-encoding` sidecar and generated plan view.

The triage is authoritative for validity, ownership, severity and class.

The human chose the recommended foreclosure disposition. Both unconverged loops reset to round zero and streak zero. Fix all five findings, then require two consecutive clean rounds. No waiver is authorised.

## Required corrections

Fix all five class 1 findings:

- I8, make criterion 8 run the full criterion-2 value matrix through both `problem` and `approach` on both `status --step` surfaces. Include explicit outer-whitespace human and interior-whitespace JSON comparisons. Add field-specific red mutations.
- I9, make the no-heading render check compare the complete generated `beta` fragment from its first byte. It must detect any generated heading or other content before `**Problem**`.
- I10, add an increment-1 render unit case with an empty Markdown body and at least one present intent field. Compare the complete emitted Step Details fragment.
- I11, make increment 3 retain every named increment-1 projection test without weakened expectations. Run a fresh scaffold through human and JSON `next` plus TOML human and JSON `status --step`, observing both required values.
- I12, repeat criterion 7's human and JSON `next` matrix checks in one non-review state. Use `awaiting-fixes`, pin its complete five-key context, and add a red mutation that places intent only in review states.

Update nearby test-name lists, matrix descriptions, mutation blocks and acceptance text when these corrections directly require it. Keep one executable contract across increment 1 and increment 3.

## Settled boundaries

Do not fix or re-open:

- I2, I6 or I7, which remain permitted class 2 findings.
- D7 or T7a through T7f.
- `GPT-R2-5` or `GPT-R3-2`.
- `GB-4`, `GB-9`, `F2` or `F3`.

Do not change Q-81 or the foreclosure decision.

## Scope

The product repair can edit only:

- `docs/plans/agent-scaffold.steps/step-intent-encoding.md`.
- `docs/plans/agent-scaffold.md`, only through `agent-flow render`.

Do not edit the plan TOML, questions, exploration, metrics, ledger, review files, other sidecars, source code, tests, fixtures, README, changelog or `pack/`.

The named tests and fixtures specify future implementation work. Do not create them in this design pass.

Do not change step statuses, increment ids, risk classes, decisions, receipts or provenance. Do not change the six converged backfill increment criteria.

If a required correction needs another current product path or conflicts with a settled decision, stop and report the blocker. Do not expand scope.

## Validation

Use the project direnv environment for every toolchain command. Run and read:

```text
cargo run -- validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl
cargo run -- validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl --workflow
cargo run -- render docs/plans/agent-scaffold.plan.toml
cargo run -- render --check --strict docs/plans/agent-scaffold.plan.toml
cargo test
cargo clippy --all-targets --all-features -- -D warnings
```

Also run `git diff --check`, check each changed technical file for non-ASCII characters and verify the exact changed-path set.

Commit the complete planner repair with a conventional `docs:` commit. Do not push.
