# Brief: `Q-78` design pass, round 4 of the reset count, GROUND-BLIND FALSIFICATION lens

This file is the brief itself, not a findings file. The orchestrator writes it before it dispatches, so a re-dispatch after a context loss reads this file rather than the orchestrator's memory.

## Your role

You are a reviewer. You are read-only with respect to the plan and the code. You author your own findings file and nothing else. You do not fix anything you find.

## Your lens

Split each stated ground into its premise and its consequence. Build a wrong implementation for each half. The criteria must fail an implementation that falsifies the premise while the consequence still holds.

Round 3 was the first round ever run under this third form of the obligation, and it returned eight class 1 findings. The second form, one wrong implementation per stated ground, misses the half-attack whenever a ground's consequence has another cause. Use the third form.

A stated ground is any sentence that justifies a design choice, a risk class or a numbered RULE. It is not the operation the increment performs.

## What is different about this round

The round 3 fix pass changed the artefact substantially: 18 findings repaired across all five sidecars, two new criteria authored, and two residuals recorded rather than fixed. YOU ARE REVIEWING THE REPAIRED ARTEFACT, NOT THE DIFF. Read the sidecars as they now stand.

A SECOND LENS IS RUNNING SEPARATELY on fix-verification and on the five places the fix pass overrode its triager. That is not your job. Do not spend your budget checking whether a specific round 3 finding was closed. Attack the grounds as they read today.

## Target

- Branch `plan/q78-design-pass`. Read and write inside the worktree the orchestrator names in your prompt. Do not touch the main repository or any other worktree.

## Scope

Five step sidecars, carrying 13 increments, all classed `risky`.

1. `docs/plans/agent-scaffold.steps/step-intent-encoding.md`, increments `-inc1`, `-inc2a` to `-inc2f`, `-inc3`.
2. `docs/plans/agent-scaffold.steps/plan-order-array-position.md`, increments `-inc1`, `-inc2`.
3. `docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md`, increment `-inc1`.
4. `docs/plans/agent-scaffold.steps/ledger-order-citation-currency.md`, increment `-inc1`.
5. `docs/plans/agent-scaffold.steps/validate-missing-source-exit.md`, increment `-inc1`.

The frozen design input is `docs/plans/step-intent-encoding.explorations/Q-78.md`. Read it, do not review it.

## The stop condition, WIDENED since round 3

- CLASS 1, A GROUND-BLIND CRITERION: a wrong implementation passes while it violates a stated risk ground, a numbered RULE or a cited Principle. The count that keeps the round clean is ZERO.
- CLASS 2, NOW THREE KINDS AND NOT TWO: a second-guard hole, a non-reproducing figure, and A CRITERION THAT REFUSES A CORRECT IMPLEMENTATION. THREE OR FEWER, all `low` or `medium`, and the round is clean.

The third kind is new this round. It covers a criterion that blocks an implementer who did the right thing. Nothing wrong passes, so it is not ground-blind, and it is neither a hole nor a figure. The unwidened condition had no bucket for it and the placement alone could decide a round.

A figure counts as class 2 if and only if it sits inside a step sidecar's increment block, meaning an acceptance criterion, that increment's risk-class ground, or a numbered RULE. Every other location is excluded, including `Q-78.md`, any `[[question]].ask`, the ledger and its resume anchor.

Currency defects, stale counts outside an increment block, and missing receipts do not bear on cleanliness. Report them and mark them as not bearing.

State the class of every finding.

## The three rules of the one clean sidecar

`ledger-order-citation-currency.md` has now had every stated figure reproduce exactly in two consecutive rounds. Measure the other four against its three rules.

1. Its search set does not contain itself.
2. It refuses, as a stated rule, to write a concrete example into itself.
3. Every figure it states is a command's OUTPUT, never a pass condition.

## Two accepted residuals, which are NOT findings

The human accepted these under `AGENTS.md:57`. Do not re-file them. If you find that a residual's recorded statement understates what a wrong implementation could ship, THAT is a finding.

- `A-F4`: `next` and `status` report success on a plan that does not parse. Recorded as RESIDUAL 4 in `step-intent-encoding.md`.
- `G-F9`: the numstat bound of 2 and 2 against a justification supporting 1 and 1. Recorded beside criterion 5 of `sidecar-status-opening-drift.md`.

## Out of scope

The design mechanism is not under review. Four recommendations have survived every round: array-position authority with `order` deleted, two required single-line intent fields projected through `render`, `next` and `status --step`, a migration record outside the plan, and a cited backfill in bounded batches.

Every human decision is settled, including the required fields, the per-batch split, the earliest-containing-commit rule, the widening to all 45 sidecars, and the ruling that this pass does not edit `pack/`. If you think a decision is wrong, write it as a separate note, not a finding.

Umbrella membership left this pass and became `Q-79`.

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
- `validate` exits 0 when its input file is absent, printing "nothing to validate". Never treat a bare exit 0 as proof. Pin the `N steps, M questions, valid` line.
- `grep -c` exits 1 when it matches nothing, and that is the PASS case for a sweep. Never chain a sweep with `&&`.
- `grep -rc` prints ONE ROW PER FILE under both GNU grep and ugrep, so it never yields a single total.
- This shell replaces `grep` with `ugrep`. Use `/usr/bin/grep` wherever an escape or a `-P` pattern matters.
- Never run `nix fmt` and never run `just scaffold-self`.

## File safety

Build every fixture ONLY under the session scratchpad, in a subdirectory you name yourself, and not in `groundblind/`, `adopter/`, `triage-r7/` or `planner-fixpass/`, which other agents own. Do NOT write into bare `/tmp`. Do NOT delete anything outside your own fixture subdirectory. NEVER use a wildcard glob in a delete. Restore the mode of any 000 or 600 fixture before you finish.

## Your findings file

Write to the path the orchestrator gives you. WRITE AS YOU GO: create the file immediately with a header, then append each finding the moment you confirm it, and commit periodically. Agents in this loop have died to session limits having written nothing.

Severity is the four-level `low`, `medium`, `high`, `critical` scale, rating impact if left unfixed, not a ranking against your other findings. Every finding carries reproducible evidence proportional to its claim: a runnable wrong implementation with measured output for a behavioural claim, an exact command or a `file:line` citation for a documentation or design claim.

Report the counts you measure, not the counts this brief states.
