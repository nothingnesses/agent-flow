# Q-78 reset round 4 triage brief

Act only as the independent triager. Work only in your assigned isolated triage worktree. Do not edit the reviewed product.

## Inputs

Read:

- `AGENTS.md`.
- The ledger from `RESUME HERE`.
- `q78-reset-r3-triage.md` and `q78-reset-r3-fix-brief.md`.
- `q78-reset-r4-reviewer-gpt.md`.
- `q78-reset-r4-reviewer-claude.md`.
- The current plan source and the three active sidecars.

The reviewed product is the current `plan/q78-design-pass` branch after the round 3 repair. Review briefs are not product.

## Raw findings

Adjudicate all five raw findings:

- `R4G-1` through `R4G-4`.
- `C4-1`.

For each raw finding:

1. Rebuild its evidence without reading reviewer fixtures.
2. Return `valid`, `dismissed` or `accepted risk`.
3. Set the owning active increment.
4. Set final severity and class.
5. State the smallest correction for each valid non-residual finding.

Deduplicate only when two reports describe one defect. Dismiss a testable claim when its demonstration does not reproduce.

## Active loops

Only these loops are active:

- `sidecar-status-opening-drift-inc1`, entering streak 1.
- `step-intent-encoding-inc1`, entering streak 0.
- `step-intent-encoding-inc3`, entering streak 1.

All are `risky`. This is reset round 4. Each has used four of five rounds after this round. Each needs two consecutive clean outcomes.

Eleven loops already converged. Do not assign a finding to them.

## Settled boundaries

The round 3 repair addresses I1, I3, I4 and I5. Verify new evidence against those repaired boundaries.

I2, I6 and I7 remain valid permitted class 2 findings. Do not re-raise them without evidence that changes class, severity or measured scope.

Do not reopen dismissed `GPT-R3-2`, T7a through T7f, D7, `GB-4`, `GB-9`, `F2` or `F3` without new evidence.

## Classes and foreclosure

Use these definitions exactly:

- Class 1: a wrong implementation passes while violating a stated risk ground, numbered rule or cited plan Principle.
- Class 2: a second-guard hole, an in-increment non-reproducing figure or a criterion that refuses a correct implementation.

A loop is clean only with zero class 1, at most three low or medium class 2 findings, and no valid finding outside both classes.

For each active loop report counts, severities, classes, outcome, resulting streak and convergence.

Also compute:

```text
round_cap - rounds_used < required_streak - current_streak
```

After round 4, `round_cap - rounds_used` is 1. A loop reset to streak 0 needs 2 and is foreclosed. A clean streak-one loop reaches 2 and converges.

Treat foreclosure as a required human escalation under decision 24. Do not choose its disposition. If foreclosure occurs, state which loops need escalation and the viable disposition classes. Do not append an escalation record.

A dismissed `high` or `critical` finding requires an independent backstop triager. State whether any re-check is owed.

## Evidence and gates

Use only:

```text
/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r4-triage
```

Create a triager-owned child directory. Never use bare `/tmp` or wildcard deletion.

Run all project commands through the project direnv environment. Use GNU grep for GNU-regex claims. Re-run both validation modes, strict render, tests and Clippy.

## Output

Write only:

```text
docs/plans/agent-scaffold.reviews/q78-reset-r4-triage.md
```

Include:

- A raw-verdict table for all five findings.
- Deduplication results.
- Reproduced evidence for every verdict.
- Per-increment outcomes for all three loops.
- Raw and distinct totals.
- Class totals and severity ceiling.
- Backstop and foreclosure status.

Commit only that file with a conventional `docs:` commit. Do not edit plan, ledger, metrics, briefs, reviewers, code or pack. Do not push.
