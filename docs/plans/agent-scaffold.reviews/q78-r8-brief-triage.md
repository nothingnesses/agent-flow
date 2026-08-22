# Brief: `Q-78` design pass, round 4 of the reset count, TRIAGE

This file is the brief itself, not a findings file. The orchestrator writes it before it dispatches, so a re-dispatch after a context loss reads this file rather than the orchestrator's memory.

## Your role

You are the TRIAGER. You are a separate agent from both reviewers and from the orchestrator, deliberately: the orchestrator drives the loop and owns convergence and cost, so it is biased toward dismissing findings in order to converge, and letting it triage would let that bias decide which findings count.

You judge each finding on its evidence and its severity. You reproduce the evidence a finding carries. You dismiss any testable claim whose demonstration does not reproduce. You do not fix anything.

Do not defer to the reviewers. Round 3's triager overruled three reviewer classes downward and rebuilt one reviewer's wrong implementation because the reviewer's did not actually pass. That is the standard.

## Your inputs

Both findings files are in your worktree, with the briefs each reviewer worked from beside them.

- `docs/plans/agent-scaffold.reviews/q78-r8-reviewer-groundblind.md`, 11 findings, reviewer self-classed 6 class 1 and 5 class 2, ceiling high.
- `docs/plans/agent-scaffold.reviews/q78-r8-reviewer-fixverify.md`, 3 findings, self-classed 1 class 1 and 2 class 2, ceiling medium.

Round 3's record is also present: `q78-r7-triage.md`, the two round 3 findings files, and `q78-r7-brief-fixpass.md`.

## The stop condition, WIDENED since round 3

- CLASS 1, A GROUND-BLIND CRITERION: a wrong implementation passes while it violates a stated risk ground, a numbered RULE or a cited Principle. COUNT ZERO.
- CLASS 2, NOW THREE KINDS: a second-guard hole, a non-reproducing figure, and A CRITERION THAT REFUSES A CORRECT IMPLEMENTATION. THREE OR FEWER, all `low` or `medium`.

A figure counts as class 2 if and only if it sits inside a step sidecar's increment block, meaning an acceptance criterion, that increment's risk-class ground, or a numbered RULE. Every other location is excluded.

## THE ARITHMETIC, WHICH IS THE CENTRAL QUESTION OF THIS TRIAGE

The pass is `risky` and needs TWO CONSECUTIVE CLEAN ROUNDS. The streak is ZERO. The cap is FIVE and THIS IS ROUND FOUR.

If round 4 is not clean, then FOUR rounds are used, ONE remains, and two consecutive clean rounds CANNOT FIT IN ONE ROUND. Convergence is then foreclosed by arithmetic and not by judgement. This is the same foreclosure that forced this pass's second escalation.

Rule on this explicitly and state the arithmetic you rule on. If convergence is foreclosed, the loop escalates to the human under `AGENTS.md:57`, and your job includes giving that escalation its options.

`AGENTS.md:57` permits resolving a valid finding by consciously accepting its residual risk. An accepted risk does not block convergence and does not save a round. The human has used that route twice in this pass.

## Your outputs

Write to `docs/plans/agent-scaffold.reviews/q78-r8-triage.md`. Write as you go and commit after each verdict.

1. A VERDICT PER FINDING: upheld, or dismissed with the reason. Where you uphold a finding but disagree with its supporting argument, say so.
2. A DEDUPLICATED COUNT across the two lenses. The fix-verification lens was told to avoid duplicating the ground-blind lens, so check whether it succeeded rather than assuming it.
3. A CLASS PER UPHELD FINDING.
4. THE ROUND OUTCOME with its arithmetic, and an explicit ruling on whether convergence is foreclosed.
5. OPTIONS FOR THE ESCALATION, if you rule it foreclosed. Give each option its trade-offs and a recommendation, judged against the plan's Project Principles BY NAME. The eight are: 1 Prefer the cleaner long-term architecture over the smallest diff, 2 Minimal by default, 3 Safe on existing projects, 4 Idempotent, 5 Make illegal states unrepresentable, 6 Ground decisions in evidence, 7 Reproducible, 8 Structured data first, project for humans.
6. WHAT MUST ROUTE TO THE HUMAN, as an explicit list, carrying forward anything routed by an earlier adjudication and not yet discharged. Round 3's triage carried four such items and TWO REMAIN OWED: the routed-decision-tracking defect still has no `[[question]]`, and the `AGENTS.md:93` rebase-rule question is still unregistered. State explicitly if there are no others.

## Two specific things to weigh

FIRST, THE MODEL SIDECAR IS BROKEN. `ledger-order-citation-currency.md` has been briefed to three agents as the model the other four are measured against, on the ground that every figure it stated reproduced. `GB-7` is a class 1 finding against it. Rule on whether that holds, because if it does, the orchestrator's framing in three briefs was wrong and the ledger must record it.

SECOND, THE FIX PASS CAME OUT WELL AND THAT IS EVIDENCE TOO. The fix-verification lens reports 16 of 18 fixes closing their finding, ALL FIVE divergences sound with every underlying claim reproducing, and BOTH new criteria holding. It also found that the triage's own `grep -rln` claim did not reproduce, returning six files rather than three. Weigh that against the count: a round can be not-clean and still be evidence that the repair process works.

## Scope

Five step sidecars under `docs/plans/agent-scaffold.steps/` carrying 13 increments, all `risky`. The frozen design input is `docs/plans/step-intent-encoding.explorations/Q-78.md` and is not under review.

OUT OF SCOPE, dismiss on scope: the four surviving design recommendations and every human decision, including the ruling that this pass does not edit `pack/`. Umbrella membership left this pass and became `Q-79`. The two accepted residuals `A-F4` and `G-F9` are not findings unless their recorded statement understates what could ship.

## The backstop

Before a DISMISSED finding at severity `high` or above counts toward a clean round, an independent second triager or a human must confirm the dismissal. Two round 4 findings are `high`, `GB-1` and `GB-2`. If you dismiss either, say so plainly, because that triggers a re-check.

## Gates

Run these from the worktree root, THROUGH THE PROJECT TOOLCHAIN. Running them bare produces `E0514` stale-cache errors that look like real compile failures and are not.

```
cd <your worktree> && direnv allow && eval "$(direnv export bash)" && <command>
```

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
- `validate` exits 0 when its input file is absent. Never treat a bare exit 0 as proof. Pin the `N steps, M questions, valid` line.
- `grep -c` exits 1 when it matches nothing, and that is the PASS case for a sweep.
- `grep -rc` prints ONE ROW PER FILE under both GNU grep and ugrep.
- This shell replaces `grep` with `ugrep`. Use `/usr/bin/grep` wherever an escape or a `-P` pattern matters.
- Never run `nix fmt` and never run `just scaffold-self`.

## File safety

Build every fixture ONLY under the session scratchpad, in a subdirectory you name yourself, and not in `groundblind/`, `adopter/`, `triage-r7/`, `planner-fixpass/`, `gb-r8/` or any directory another agent owns. Do NOT write into bare `/tmp`. Do NOT delete anything outside your own fixture subdirectory. NEVER use a wildcard glob in a delete. Restore the mode of any 000 or 600 fixture before you finish.
