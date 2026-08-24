# Q-78 reset round 4 Claude review brief

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

Use an adoption, executability and fix-verification lens. Assume that an implementer follows the specification literally.

For each active increment:

1. Re-run each cited current-tree command and reconcile each figure.
2. Check that every future fixture, test and changed path is named consistently.
3. Check fresh-project, existing-project and optional-window effects where relevant.
4. Verify all four round 3 corrections against their full consequences.
5. Check that one executable contract reaches every human and JSON surface.

Use these classes:

- Class 1: a wrong implementation passes while violating a stated risk ground, numbered rule or cited Principle.
- Class 2: a second-guard hole, an in-increment non-reproducing figure or a criterion that refuses a correct implementation.

A loop is clean with zero class 1, at most three low or medium class 2 findings, and no valid finding outside those classes.

## Evidence

Use only:

```text
/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r4-claude
```

Create a reviewer-owned child directory. Never use bare `/tmp` or wildcard deletion.

Run project commands through the project direnv environment. Use GNU grep for GNU-regex claims. Use runnable demonstrations for behavioural claims and exact citations for prose claims.

## Output

Write only:

```text
docs/plans/agent-scaffold.reviews/q78-reset-r4-reviewer-claude.md
```

Give each finding a stable id, owner, severity, proposed class, evidence and smallest correction. Include all three loops in a raw-count table. State the raw total and severity ceiling.

Commit only that file with a conventional `docs:` commit. Do not edit product, plan, ledger, metrics, briefs, code or pack. Do not push.
