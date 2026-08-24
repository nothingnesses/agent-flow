# Q-78 reset round 4 GPT review brief

Act only as an independent reviewer. Work only in your assigned isolated review worktree. Do not edit the reviewed product.

## Target

Review the current `plan/q78-design-pass` branch after commit `efce61a`, excluding review briefs from the product.

Read:

- `AGENTS.md`.
- The ledger from `RESUME HERE`.
- `q78-reset-r3-triage.md` and `q78-reset-r3-fix-brief.md`.
- The current plan source, generated view, Q-78 exploration and active sidecars.

Do not read another reset round 4 reviewer file.

## Active loops

Review only:

- `sidecar-status-opening-drift-inc1`, entering streak 1.
- `step-intent-encoding-inc1`, entering streak 0.
- `step-intent-encoding-inc3`, entering streak 1.

All three are `risky`. This is reset round 4, with four of five rounds used after this review.

A clean outcome makes the first and third loops converge. A clean `step-intent-encoding-inc1` outcome gives streak 1. It then needs a clean round 5. A `new_valid` round 4 outcome on that loop forecloses convergence before the cap.

Eleven other loops already converged. Do not assign findings to them.

## Settled boundaries

The round 3 repair addresses class 1 findings I1, I3, I4 and I5. Verify each repair independently.

These valid class 2 findings remain permitted:

- I2, the README path exclusion.
- I6, the status-opening residual wording.
- I7, the ledger figures.

Do not re-raise them without new evidence that changes their class, severity or measured boundary. I7 belongs to a converged loop and is outside this review.

Do not reopen dismissed `GPT-R3-2`, T7a through T7f, D7, `GB-4`, `GB-9`, `F2` or `F3` without new evidence.

## Lens

Use a ground-blind falsification lens. Assume that a wrong implementation can satisfy each criterion.

For each active increment:

1. Map each criterion to its numbered rule, risk ground or cited Principle.
2. Build the smallest wrong implementation that can pass the criteria.
3. Exercise all matrix rows and all named red mutations independently.
4. Check exact-byte expectations, fixture ownership, path sets and documentation impact.
5. Re-run every cited current-tree command.

Use these classes:

- Class 1: a wrong implementation passes while violating a stated risk ground, numbered rule or cited Principle.
- Class 2: a second-guard hole, an in-increment non-reproducing figure or a criterion that refuses a correct implementation.

A loop is clean with zero class 1, at most three low or medium class 2 findings, and no valid finding outside those classes.

## Evidence

Use only:

```text
/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r4-gpt
```

Create a reviewer-owned child directory. Never use bare `/tmp` or wildcard deletion.

Run project commands through the project direnv environment. Use runnable demonstrations for behavioural claims and exact citations for prose claims.

## Output

Write only:

```text
docs/plans/agent-scaffold.reviews/q78-reset-r4-reviewer-gpt.md
```

Give each finding a stable id, owner, severity, proposed class, evidence and smallest correction. Include all three loops in a raw-count table. State the raw total and severity ceiling.

Commit only that file with a conventional `docs:` commit. Do not edit product, plan, ledger, metrics, briefs, code or pack. Do not push.
