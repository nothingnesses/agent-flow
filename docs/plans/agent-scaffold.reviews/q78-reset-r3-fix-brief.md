# Q-78 reset round 3 planner fix brief

Act only as the planner for this repair. Work only in the isolated `plan/q78-design-pass` worktree. Do not edit the main checkout.

## Authority

Read these files first:

- `AGENTS.md`.
- `docs/plans/agent-scaffold.reviews/q78-reset-r3-triage.md`.
- `docs/plans/agent-scaffold.reviews/q78-reset-r3-reviewer-gpt.md`.
- `docs/plans/agent-scaffold.reviews/q78-reset-r3-reviewer-claude.md`.
- `docs/plans/agent-scaffold.ledger.md`, starting at `RESUME HERE`.
- The current `step-intent-encoding` sidecar and generated plan view.

The triage file is authoritative for validity, ownership, class and severity.

## Required corrections

Fix only these four class 1 findings in `step-intent-encoding-inc1`:

- I1, add an interior-line-whitespace row to the logical-value matrix. Run it through all three human projections and the independent reference formatter. Add a per-line-trim red mutation that makes all three surface tests fail.
- I3, add the outer-whitespace row to criterion 7's human `next` fixtures. Pin its complete expected context block.
- I4, run the CRLF row through `status --step --json`. Compare decoded bytes with the parser oracle. Extend the JSON-normalising red control to a named status JSON test.
- I5, add a no-heading render fixture. Permit its fixture sidecar in the future increment changed-path set. Pin labelled intent first, one blank line, then the original body.

Keep the implementation contract internally consistent after each correction. Update nearby matrix descriptions, test names, mutation lists and fixture path lists when they directly depend on these four corrections.

## Settled findings

Do not fix these permitted class 2 findings:

- I2, the README path exclusion in `step-intent-encoding-inc1`.
- I6, the status-opening accepted-residual wording.
- I7, the ledger criterion 1 figures.

Their loops are clean or converged under the human-decided threshold. Do not re-open them without new evidence that changes their class, severity or measured boundary.

Do not re-open dismissed `GPT-R3-2`. Do not edit T7a through T7f, D7, `GB-4`, `GB-9`, `F2` or `F3`.

## Scope

The product repair can edit only:

- `docs/plans/agent-scaffold.steps/step-intent-encoding.md`.
- `docs/plans/agent-scaffold.md`, only through `agent-flow render`.

Do not edit the plan TOML, questions, exploration, metrics, ledger, review files, other sidecars, source code, tests, fixtures, README, changelog or `pack/`.

The references to tests and fixtures specify future implementation work. Do not create those product files in this design pass.

Do not change statuses, increment ids, risk classes, decisions, receipts or provenance. Do not change increment 2a through 2f or increment 3 criteria.

If a required correction needs another current product path or conflicts with a settled decision, stop and report the blocker. Do not expand scope.

## Validation

Use the project direnv environment for every toolchain command. Run and read all output from:

```text
cargo run -- validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl
cargo run -- validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl --workflow
cargo run -- render docs/plans/agent-scaffold.plan.toml
cargo run -- render --check --strict docs/plans/agent-scaffold.plan.toml
cargo test
cargo clippy --all-targets --all-features -- -D warnings
```

Also run `git diff --check`, check every changed technical file for non-ASCII characters and verify the exact changed-path set.

Commit the complete planner repair with a conventional `docs:` commit. Do not push.
