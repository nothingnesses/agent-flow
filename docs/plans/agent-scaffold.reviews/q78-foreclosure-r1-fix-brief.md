# Q-78 post-escalation round 1 fix brief

Act only as the planner for this repair in the isolated `plan/q78-design-pass` worktree. Do not edit main.

Read `AGENTS.md`, `q78-foreclosure-r1-triage.md`, both reviewer files, the ledger from `RESUME HERE`, and the current `step-intent-encoding` sidecar.

The triage is authoritative.

## Required correction

Fix only class 1 finding FR1-2 in `step-intent-encoding-inc1`.

Add a table-driven test at the `build_context` seam over every production `LoopState`. For each state, assert that both `problem` and `approach` keys are present with the exact supplied values. Keep the existing human and JSON matrix tests for review and writer states.

The state table must include every current enum variant, including ready, blocked, both reviewer states, awaiting fixes, converged, escalate, risk-class conflict and done. Design the table so adding a new enum variant forces an explicit test update rather than silently omitting the state.

Add a red mutation or equivalent negative control that inserts intent only in the currently sampled states. Require the complete state table to fail on every omitted variant, then restore unconditional insertion and run it green.

Update the authoritative increment-1 projection-test list and increment-3 retention clause if the new exact test name requires it.

## Settled findings

Do not fix or re-open:

- FR1-1 and FR1-4 in increment 1.
- FR1-3 in increment 3.
- I2, I6, I7, D7 or T7a through T7f.
- `GPT-R2-5`, `GPT-R3-2`, `GB-4`, `GB-9`, `F2` or `F3`.

These are settled permitted class 2 findings or earlier settled boundaries. No waiver is authorised.

## Scope

Edit only:

- `docs/plans/agent-scaffold.steps/step-intent-encoding.md`.
- `docs/plans/agent-scaffold.md`, only through `agent-flow render`.

Do not edit the plan TOML, questions, exploration, metrics, ledger, review files, other sidecars, code, tests, fixtures, README, changelog or `pack/`.

The test specifies future implementation work. Do not create it now.

Do not change statuses, increment ids, risk classes, decisions, receipts or provenance.

## Validation

Use the project direnv environment. Run and read:

```text
cargo run -- validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl
cargo run -- validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl --workflow
cargo run -- render docs/plans/agent-scaffold.plan.toml
cargo run -- render --check --strict docs/plans/agent-scaffold.plan.toml
cargo test
cargo clippy --all-targets --all-features -- -D warnings
```

Run `git diff --check`, the ASCII check and the exact changed-path check.

Commit with a conventional `docs:` subject. Do not push.
