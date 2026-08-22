# Brief: `Q-78` design pass, round 4 of the reset count, FIX-VERIFICATION AND DIVERGENCE lens

This file is the brief itself, not a findings file. The orchestrator writes it before it dispatches, so a re-dispatch after a context loss reads this file rather than the orchestrator's memory.

## Your role

You are a reviewer. You are read-only with respect to the plan and the code. You author your own findings file and nothing else. You do not fix anything you find.

## Why this lens exists

The round 3 fix pass repaired 18 findings, and in FIVE of them it OVERRODE ITS TRIAGER on its own judgement. That pattern has produced defects in this loop before: the round 1 fix pass of this same pass disagreed with its triager in seven places, and the ledger records that as a reason a later round found what it found.

A fix pass that overrides its adjudicator may be right. It is not reviewed by anybody unless a lens is pointed at it, and no lens ever has been.

## Your three questions

1. DID EACH FIX ACTUALLY CLOSE ITS FINDING? Take the round 3 findings and the triage verdicts, and for each of the 18 fixed items, build the wrong implementation the finding named and run the repaired criterion against it. A fix that does not fail its own attack is a finding.
2. ARE THE FIVE DIVERGENCES SOUND? Each is listed below with the reason given. For each, decide whether the fix pass's reasoning holds, and reproduce the claim it rests on. A divergence justified by a claim that does not reproduce is a finding.
3. ARE THE TWO NEW CRITERIA SOUND? They are unreviewed content. Attack them the way you would attack any criterion: build a wrong implementation and see whether it passes.

## The five divergences, with the reason each was given

1. `A-F7`. The triage asked for the figure to be stated as 36 or 19. The fix DELETED the figure and cited the anchored selector instead. Reason given: the triage's own second half shows neither 45, 36 nor 19 is the population RULE 9 meets, so any restated number is wrong on arrival.
2. `G-F4`. The triage asked for a second `cmp`. The fix runs THREE. Reason given: the `A-F3` fix adds a third copied pair to the same increment, so the same rule requires three.
3. `A-F1`. The triage's `grep -rln 'entries with status and order'` was said to return exactly three files. The fix says it DOES NOT REPRODUCE, also reaching the rendered plan, the sidecar and the review records, and scoped the search to `pack/ AGENTS.md .agents/`. VERIFY BOTH FORMS YOURSELF.
4. `G-F8`. The triage offered `grep -rc` over `tests/` or naming the file. The fix says `grep -rc` prints one row per file under both GNU grep and ugrep and so never yields the single count the outcome records, and named the file and five test functions instead. VERIFY THE GREP BEHAVIOUR YOURSELF.
5. `G-F13`. The fix stated only the one row measured over the worklist and DROPPED the four-row count over the selected set. Reason given: a count inside an acceptance criterion expires.

## The two new criteria

- `step-intent-encoding` increment 1, criterion 13, authored for `G-F2`, pinning RULE 2 and RULE 3 in the suite with a red measurement carrying the premise.
- `step-intent-encoding` increment 3, criterion 12, authored for `G-F12`, running `status --step` against the Markdown substrate.

## Target

- Branch `plan/q78-design-pass`. Read and write inside the worktree the orchestrator names in your prompt. Do not touch the main repository or any other worktree.

## Your inputs

- `docs/plans/agent-scaffold.reviews/q78-r7-triage.md`, the verdicts the fix pass worked from.
- `docs/plans/agent-scaffold.reviews/q78-r7-reviewer-groundblind.md` and `q78-r7-reviewer-adopter.md`, the raw findings.
- `docs/plans/agent-scaffold.reviews/q78-r7-brief-fixpass.md`, what the fix pass was told to do.

The three fix commits are the most recent on the branch. `git log --oneline -4` finds them.

## The stop condition, WIDENED since round 3

- CLASS 1, A GROUND-BLIND CRITERION: a wrong implementation passes while it violates a stated risk ground, a numbered RULE or a cited Principle. COUNT ZERO.
- CLASS 2, NOW THREE KINDS: a second-guard hole, a non-reproducing figure, and A CRITERION THAT REFUSES A CORRECT IMPLEMENTATION. THREE OR FEWER, all `low` or `medium`.

The third kind is new. A repair that closes a hole by making a criterion refuse correct work has traded one defect for another, and this lens is well placed to catch it. A figure counts as class 2 if and only if it sits inside a step sidecar's increment block.

State the class of every finding.

## Two accepted residuals, which are NOT findings

The human accepted these under `AGENTS.md:57`, so a re-file is out of scope. If a residual's recorded statement UNDERSTATES what a wrong implementation could ship, that IS a finding.

- `A-F4`, recorded as RESIDUAL 4 in `step-intent-encoding.md`.
- `G-F9`, recorded beside criterion 5 of `sidecar-status-opening-drift.md`.

## Out of scope

The design mechanism and every human decision are settled, including the ruling that this pass does not edit `pack/`, so the fix for the two `high` pack findings is deliberately a changed-path-set and documentation-impact edit rather than the edit itself. That cost is accepted and recorded. What IS in scope is whether the recorded promise names the right files and the right changes.

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
- `validate` exits 0 when its input file is absent. Never treat a bare exit 0 as proof. Pin the `N steps, M questions, valid` line.
- `grep -c` exits 1 when it matches nothing, and that is the PASS case for a sweep.
- `grep -rc` prints ONE ROW PER FILE under both GNU grep and ugrep. Divergence 4 turns on this. Verify it rather than assuming it.
- This shell replaces `grep` with `ugrep`. Use `/usr/bin/grep` wherever an escape or a `-P` pattern matters, and note that divergence 3 and divergence 4 are both claims about grep behaviour.
- Never run `nix fmt` and never run `just scaffold-self`.

## File safety

Build every fixture ONLY under the session scratchpad, in a subdirectory you name yourself, and not in `groundblind/`, `adopter/`, `triage-r7/` or `planner-fixpass/`, which other agents own. Do NOT write into bare `/tmp`. Do NOT delete anything outside your own fixture subdirectory. NEVER use a wildcard glob in a delete. Restore the mode of any 000 or 600 fixture before you finish.

## Your findings file

Write to the path the orchestrator gives you. WRITE AS YOU GO: create the file immediately with a header, then append each finding the moment you confirm it, and commit periodically. Agents in this loop have died to session limits having written nothing.

Severity is the four-level `low`, `medium`, `high`, `critical` scale, rating impact if left unfixed. Every finding carries reproducible evidence proportional to its claim.

Report explicitly, whatever the answer: how many of the 18 fixes you verified as closing their finding, how many of the five divergences you judged sound, and whether the two new criteria hold. A clean answer on any of those three is as useful as a finding.
