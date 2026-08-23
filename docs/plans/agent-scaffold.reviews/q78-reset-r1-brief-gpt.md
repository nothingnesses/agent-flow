# Q-78 reset round 1 GPT review brief

## Role

Review the five Q-78 sidecars independently through ground-blind falsification.

Assume that the specification still contains defects.

Do not read the Claude lens brief or any round 1 findings file.

## Target

Review the complete current contents of these files:

- `docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md`.
- `docs/plans/agent-scaffold.steps/ledger-order-citation-currency.md`.
- `docs/plans/agent-scaffold.steps/plan-order-array-position.md`.
- `docs/plans/agent-scaffold.steps/step-intent-encoding.md`.
- `docs/plans/agent-scaffold.steps/validate-missing-source-exit.md`.

The repair commit is `70fd47b2296018111dea00807c432fe0b07c4faa`.

Read these records before review:

- `docs/plans/agent-scaffold.reviews/q78-r8-triage.md`.
- `docs/plans/agent-scaffold.reviews/q78-reset-fix-brief.md`.
- `docs/plans/agent-scaffold.ledger.md`, from the line that starts `RESUME HERE (2026-08-23)`.

Treat the round 4 triage as authoritative over its reviewer files.

## Loop identity

Assign every finding to exactly one of these increments:

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

If one defect independently breaks two increments, file two findings with distinct evidence.

All increments are `risky` and need two consecutive clean rounds.

This is round 1 after the counter reset.

## Falsification duty

Split each stated risk ground into its premise and its consequence.

Build a wrong implementation for each half.

The criteria must fail an implementation that falsifies the premise while the consequence still holds.

Test every numbered rule and cited Project Principle the same way.

Use these Project Principle names:

1. `Prefer the cleaner long-term architecture over the smallest diff`.
2. `Minimal by default`.
3. `Safe on existing projects`.
4. `Idempotent`.
5. `Make illegal states unrepresentable`.
6. `Ground decisions in evidence`.
7. `Reproducible`.
8. `Structured data first, project for humans`.

## Classification

Class 1 means a wrong implementation passes while it violates a stated risk ground, numbered rule, or cited Principle.

Class 1 permits zero findings.

Class 2 includes these defects:

- A second-guard hole.
- A non-reproducing figure inside an increment block.
- A criterion that refuses a correct implementation.

Class 2 permits at most three findings, all `low` or `medium`.

State `class 1`, `class 2`, or `neither` for every finding.

Use severity `low`, `medium`, `high`, or `critical`.

## Settled items

Do not re-raise `GB-4`, `GB-9`, `F2`, or `F3` without new evidence that defeats the recorded acceptance boundary.

Do not re-raise any other settled finding without new evidence that its repair remains unsound.

If you re-raise one, cite the new evidence and the earlier verdict.

Check every repair for `GB-1`, `GB-2`, `GB-3`, `GB-5`, `GB-6`, `GB-7`, `GB-8`, `GB-10`, `GB-11`, `F1`, and `T-1`.

Check each accepted residual for accurate severity, cost, owner, and non-expansion boundary.

## Evidence

Reproduce every testable claim.

Use a mutation when the claim says that a wrong implementation passes.

Use an exact command or `file:line` citation when that is sufficient.

Do not file a testable claim when its demonstration does not reproduce.

Run commands from the repository root unless the criterion states another directory.

Use GNU grep for commands whose result differs under ugrep.

Pin stdout when `validate` can exit zero on absent input.

Treat a zero-match `grep -c` exit of 1 as data, not command failure.

## File safety

Do not edit the sidecars, plan, ledger, metrics log, code, pack, or briefs.

Write fixtures only under this directory:

`/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r1-gpt`.

Create subdirectories that this review owns.

Do not write into bare `/tmp`.

Do not use wildcard deletion.

Do not push.

## Output

Write findings only to:

`docs/plans/agent-scaffold.reviews/q78-reset-r1-reviewer-gpt.md`.

For each finding, include:

- Identifier.
- Owning increment.
- Severity.
- Class.
- Claim.
- Reproducible evidence.
- Required correction.

End with one table that gives the raw finding count and severity ceiling for each of the thirteen increments.

If there are no findings, state `Zero findings` and include a zero row for every increment.

Commit only the findings file with a conventional `docs:` subject.

Do not add attribution trailers.
