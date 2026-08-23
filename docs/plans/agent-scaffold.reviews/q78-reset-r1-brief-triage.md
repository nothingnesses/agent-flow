# Q-78 reset round 1 triage brief

## Role

Adjudicate round 1 independently from the planner and both reviewers.

Assume that reviewer claims can be wrong.

Rebuild each demonstration from the sidecar text.

Do not use either reviewer's fixture directory.

## Inputs

Read these findings files:

- `docs/plans/agent-scaffold.reviews/q78-reset-r1-reviewer-gpt.md`.
- `docs/plans/agent-scaffold.reviews/q78-reset-r1-reviewer-claude.md`.

Read these controlling records:

- `docs/plans/agent-scaffold.reviews/q78-r8-triage.md`.
- `docs/plans/agent-scaffold.reviews/q78-reset-fix-brief.md`.
- `docs/plans/agent-scaffold.reviews/q78-reset-r1-brief-gpt.md`.
- `docs/plans/agent-scaffold.reviews/q78-reset-r1-brief-claude.md`.
- `docs/plans/agent-scaffold.ledger.md`, from the line that starts `RESUME HERE (2026-08-23)`.

Read all five current Q-78 sidecars.

## Duties

Reproduce all nine raw findings.

Deduplicate findings that share one cause and one correction.

Keep findings separate when different increments need independent corrections.

Return `valid`, `dismissed`, or `accepted risk` for every raw finding.

State your own severity and class for every distinct finding.

Dismiss a testable claim when its evidence does not reproduce.

Give the corrected demonstration when the claim is valid but its submitted demonstration is wrong.

Check that no finding merely re-raises a settled item without new evidence.

Flag any dismissed `high` or `critical` finding for an independent re-check.

## Loop identity

Assign every distinct finding to exactly one increment:

- `sidecar-status-opening-drift-inc1`.
- `ledger-order-citation-currency-inc1`.
- `plan-order-array-position-inc1`.
- `plan-order-array-position-inc2`.
- `step-intent-encoding-inc1`.
- `step-intent-encoding-inc2a`.
- `step-intent-encoding-inc2b`.
- `step-intent-encoding-inc2c`.
- `step-intent-encoding-inc2d`.
- `step-intent-encoding-inc2e`.
- `step-intent-encoding-inc2f`.
- `step-intent-encoding-inc3`.
- `validate-missing-source-exit-inc1`.

If one defect independently breaks two increments, keep two distinct findings.

## Round outcome

Apply the Q-78 stop condition per increment.

Class 1 permits zero findings.

Class 2 permits at most three findings, all `low` or `medium`.

Class 2 contains:

- A second-guard hole.
- A non-reproducing figure inside an increment block.
- A criterion that refuses a correct implementation.

Mark an increment `new_valid` when it exceeds either class threshold.

Mark an increment `clean` when it stays within both thresholds.

A clean round increments that loop's streak from zero to one.

A `new_valid` round leaves that loop's streak at zero.

All increments are `risky` and need a streak of two.

No increment can converge in this first round.

## Evidence

Use a mutation for each behavioural falsifier.

Use an exact command or `file:line` citation when that is sufficient.

Run commands from the directory that the criterion requires.

Use GNU grep when ugrep differs.

Pin stdout when `validate` can exit zero on absent input.

Treat a zero-match `grep -c` exit of 1 as data.

## File safety

Do not edit sidecars, plan, ledger, metrics, review, or brief files.

Write fixtures only under this directory:

`/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r1-triage`.

Create subdirectories that this triage owns.

Do not write into bare `/tmp`.

Do not use wildcard deletion.

Do not push.

## Output

Write verdicts only to:

`docs/plans/agent-scaffold.reviews/q78-reset-r1-triage.md`.

Include:

- One verdict for each raw finding identifier.
- A deduplication map.
- One required correction for each valid distinct finding.
- One outcome row for every increment.
- Each row's distinct valid count, severity list, class counts, outcome, and resulting streak.
- The total distinct valid count and severity ceiling.

Commit only the triage file with a conventional `docs:` subject.

Do not add attribution trailers.
