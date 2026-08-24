# Q-78 reset round 2 planner fix brief

Act only as the planner for this repair. Work only in the isolated `plan/q78-design-pass` worktree. Do not edit the main checkout.

## Authority

Read these files first:

- `AGENTS.md`.
- `docs/plans/agent-scaffold.reviews/q78-reset-r2-triage.md`.
- `docs/plans/agent-scaffold.reviews/q78-reset-r2-reviewer-gpt.md`.
- `docs/plans/agent-scaffold.reviews/q78-reset-r2-reviewer-claude.md`.
- `docs/plans/agent-scaffold.ledger.md`, starting at `RESUME HERE`.
- The current Q-78 plan source, sidecars, question sidecar and exploration.

The triage file is authoritative for finding validity, ownership, class and severity.

The human chose option A for streak accounting on 2026-08-24. Count round 1 through the paragraph-value scope change. Keep the existing increment ids. Do not add a scope-reset event. The accepted cost is that only reset round 2 reviewed paragraph values.

## Required decision record

Register the streak decision as the next numbered `[[question]]`, expected to be `Q-81` after you verify that `Q-80` is the current maximum. Set it to `decided` and fold it into `step-intent-encoding`. Add its question sidecar and add it to that step's provenance decisions.

The item must state the three presented options, their trade-offs, the chosen option and the reasoning against the plan principles. Use these option labels in the receipt:

1. `Count round 1 through the scope change`.
2. `Rename the eight affected increments`.
3. `Add a structured scope-reset event`.

The recommendation and chosen value are `Count round 1 through the scope change`. Append exactly one matching `type:"decision"` receipt to `docs/metrics/workflow.jsonl`. Use the normal `task` convention for the folded step. Do not rewrite prior metrics lines.

This numbered item replaces the provisional ledger receipt name `Q-78-scope-change-streaks`. Do not append a receipt with that suffixed id.

## Valid findings to fix

Fix only these reset round 2 findings:

- T1, add exact-byte human projection coverage for repeated blank lines, CRLF and bare CR on `render`, human `next` and human `status --step`. Require a red mutation that collapses a blank run or leaves a bare CR.
- T2, compare `next --json` values byte-for-byte with parser values across the logical-value matrix. Include outer whitespace, CRLF and bare CR. Require a red normalising mutation.
- T3, exercise both partial `status --step` states on human and JSON surfaces. Require `found: true`, exact preservation of the present field and absence only for the missing field.
- T4, reconcile each source field with exactly one correctly quoted labelled block inside its own generated Step Details section. Keep aggregate counts only as a secondary census.
- T6, make the eventual receipt boundary consistent. The owning step defines four accepted residuals. The structured Q-78 ask, the exploration and the eventual-receipt requirement must all state or point to all four.
- T8, remove the conditional `multiline` wording from the human `next` format. Add a single-paragraph human `next` fixture that requires the label-own-line quoted form.
- T9, narrow the accepted-residual text in `sidecar-status-opening-drift.md` to the exposure that the repaired whole-file word-diff guard does not cover.

Do not fix T7a through T7f. Their six loops converged under the human-decided class 2 threshold. Preserve their settled boundary unless new evidence changes their class, severity or measured scope.

Do not re-open D7 from reset round 1. Do not re-open `GPT-R2-5`, which triage dismissed.

Preserve accepted residuals `GB-4`, `GB-9`, `F2` and `F3` exactly except where T6 requires a consistent four-item pointer.

## Allowed product paths

The product repair can edit only these paths:

- `docs/plans/agent-scaffold.plan.toml`.
- `docs/plans/agent-scaffold.md`, only through `agent-flow render`.
- `docs/plans/agent-scaffold.questions/Q-81.md`.
- `docs/plans/agent-scaffold.steps/step-intent-encoding.md`.
- `docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md`.
- `docs/plans/step-intent-encoding.explorations/Q-78.md`.
- `docs/metrics/workflow.jsonl`, append-only for the decision receipt.

Do not edit source code, tests, `pack/`, the ledger, review files, other questions or other sidecars. Do not change step statuses or increment ids. Do not change the converged increment 2a through 2f criteria.

If a required correction needs another path or conflicts with a settled decision, stop and report the blocker. Do not expand scope.

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

Also run `git diff --check`, check all changed technical text for non-ASCII characters and verify the exact changed-path set.

Commit the complete planner repair with a conventional `docs:` commit. Do not push.
