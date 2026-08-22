# Brief: `Q-78` design pass, round 3 of the reset count, TRIAGE

This file is the brief itself, not a findings file. The orchestrator writes it before it dispatches, so a re-dispatch after a context loss reads this file rather than the orchestrator's memory.

## Your role

You are the TRIAGER. You are a separate agent from both reviewers and from the orchestrator. `AGENTS.md:22` states why: the orchestrator drives the loop and owns convergence and cost, so it is biased toward dismissing findings in order to converge, and letting it triage would let that bias decide which findings count.

You judge each finding on its evidence and its severity. You reproduce the evidence a finding carries. You dismiss any testable claim whose demonstration does not reproduce. You do not fix anything.

Do not defer to the reviewers. Two previous triagers in this loop overruled findings they upheld, and one rebuilt a reviewer's wrong implementation independently rather than trusting the report. That is the standard.

## Your inputs

Both findings files are already in your worktree.

- `docs/plans/agent-scaffold.reviews/q78-r7-reviewer-groundblind.md`, 13 findings, 8 class 1, 5 class 2, ceiling medium.
- `docs/plans/agent-scaffold.reviews/q78-r7-reviewer-adopter.md`, 7 findings, ceiling high, 2 high and 4 medium and 1 low.

The briefs each reviewer worked from sit beside them, as `q78-r7-brief-groundblind.md` and `q78-r7-brief-adopter.md`. Read them, so you judge each finding against the lens it was written under.

## Your outputs

Write to `docs/plans/agent-scaffold.reviews/q78-r7-triage.md` in your worktree. Write as you go and commit periodically. Agents in this loop have died to session limits having written nothing.

Deliver all six of the following.

1. A VERDICT PER FINDING: upheld, or dismissed with the reason. Where you uphold a finding but disagree with its supporting argument, say so, because a fix pass reads your verdict and not the reviewer's reasoning.
2. A DEDUPLICATED COUNT across the two lenses. The two lenses overlap, and 20 raw findings is not 20 distinct ones.
3. A CLASS PER UPHELD FINDING against the stop condition below.
4. THE ROUND OUTCOME: clean or not clean, with the arithmetic.
5. WHAT MUST ROUTE TO THE HUMAN, as an explicit list. See the routing rule below.
6. YOUR RULING ON THE ONE QUESTION the orchestrator has recorded, stated below.

## The stop condition

- CLASS 1, a ground-blind criterion, meaning a wrong implementation passes while it violates a stated risk ground, a numbered RULE or a cited Principle. The count that keeps the round clean is ZERO.
- CLASS 2, a second-guard hole or a non-reproducing figure. THREE OR FEWER, all `low` or `medium`, and the round is clean.

A figure counts as class 2 if and only if it sits inside a step sidecar's increment block, meaning an acceptance criterion, that increment's risk-class ground, or a numbered RULE. Every other location is excluded, including `Q-78.md`, any `[[question]].ask`, the ledger and its resume anchor.

Currency defects, stale counts outside an increment block, and missing receipts do not bear on cleanliness.

## The one question the orchestrator has recorded, and does not answer

Class 1 went from TWO in round 2 to EIGHT in round 3, under the same lens name. Round 3 is also the FIRST round ever run under the third form of the falsification obligation: "Split each stated ground into its premise and its consequence, then build a wrong implementation for each half. The criteria must fail an implementation that falsifies the premise while the consequence still holds."

A rise on first contact with a sharpened obligation is not the same event as a regression. Round 2's own triage recorded the principle: eight highs on first contact with a region is evidence the region is unreviewed, not evidence the artefact is nearly done.

Rule on which of the two this is, and give the measurement you rule on. Do not rule from the numbers alone.

## The arithmetic you must weigh

The pass is classed `risky`, so it needs TWO CONSECUTIVE CLEAN ROUNDS. The streak is ZERO. The cap is FIVE rounds and this is round THREE of the reset count.

So if round 3 is not clean, convergence requires rounds 4 and 5 to BOTH be clean. A single new valid finding in round 4 forecloses convergence and forces an escalation at the cap. That is arithmetic and not judgement, and it is the same arithmetic that forced this pass's second escalation.

`AGENTS.md:57` ships a route this loop has used once: a valid finding may be resolved by consciously accepting its residual risk and recording that. An accepted risk does not block convergence and does not save a round. If you think the arithmetic forecloses convergence, say so, and say which findings you would put to the human as residuals.

## The routing rule, which this loop has broken three times

A decision routed to the human by one adjudication and not carried by the next disappears silently, because no rule joins one round's routed decisions to the next round's list. This loop lost three routed decisions that way, and the ledger records each loss.

So: read the previous round's triage and the ledger, list every decision that was routed to the human and has NOT been discharged, and carry it into your own routed list. State explicitly if the answer is none. Do not assume either way.

## The backstop

Before a DISMISSED finding at severity `high` or above counts toward a clean round, an independent second triager or a human must confirm the dismissal. If you dismiss either of the adopter lens's two high findings, say so plainly, because that triggers a re-check and convergence blocks until it returns.

## Scope

Five step sidecars under `docs/plans/agent-scaffold.steps/`, carrying 13 increments, all classed `risky`: `step-intent-encoding.md` (`-inc1`, `-inc2a` to `-inc2f`, `-inc3`), `plan-order-array-position.md` (`-inc1`, `-inc2`), `sidecar-status-opening-drift.md` (`-inc1`), `ledger-order-citation-currency.md` (`-inc1`), `validate-missing-source-exit.md` (`-inc1`).

The frozen design input is `docs/plans/step-intent-encoding.explorations/Q-78.md`. It is not under review.

OUT OF SCOPE, and a finding against any of these is dismissed on scope: the four surviving design recommendations (array-position authority with `order` deleted, two required single-line intent fields projected through `render`, `next` and `status --step`, a migration record outside the plan, and a cited backfill in bounded batches), and every human decision. Umbrella membership left this pass and became `Q-79`.

## Gates

Run these from the worktree root. The `<PLAN>` argument is required.

```
cargo test
cargo clippy --all-targets -- -D warnings
cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl
cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow
cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml
LC_ALL=C grep -rcP '[^\t\x20-\x7e]' docs/plans/
```

## Known defects, so you do not re-discover them

- `render --check --strict` exits 2 when the `<PLAN>` argument is absent.
- `validate` exits 0 when its input file is absent, printing "nothing to validate". Never treat a bare exit 0 as proof. Pin the `N steps, M questions, valid` line.
- `grep -c` exits 1 when it matches nothing, and that is the PASS case for a sweep. Never chain a sweep with `&&`.
- This shell replaces `grep` with `ugrep`. Use `/usr/bin/grep` wherever an escape or a `-P` pattern matters.
- Never run `nix fmt` and never run `just scaffold-self`.

## File safety

Build every fixture ONLY under the session scratchpad, in a subdirectory you name yourself. Do NOT write into bare `/tmp`. One reviewer this round wrote a stray file into bare `/tmp` and had to remove it. Do NOT delete anything outside your own fixture subdirectory. NEVER use a wildcard glob in a delete. Restore the mode of any 000 or 600 fixture before you finish.
