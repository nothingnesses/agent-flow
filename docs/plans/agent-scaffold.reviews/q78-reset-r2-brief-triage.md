# Q-78 reset shared review triage brief

## Role

Adjudicate the shared review independently from the planner and both reviewers.

Assume that every reviewer claim can be wrong.

Rebuild each demonstration from the product text.

Do not use either reviewer's fixture directory.

## Inputs

Read these findings files:

- `docs/plans/agent-scaffold.reviews/q78-reset-r2-reviewer-gpt.md`.
- `docs/plans/agent-scaffold.reviews/q78-reset-r2-reviewer-claude.md`.

Read these controlling records:

- `docs/plans/agent-scaffold.reviews/q78-reset-r1-triage.md`.
- `docs/plans/agent-scaffold.reviews/q78-reset-r1-fix-brief.md`.
- `docs/plans/agent-scaffold.reviews/q78-r8-triage.md`.
- `docs/plans/agent-scaffold.ledger.md`, from the current `RESUME HERE` line.

Read the complete reviewed product sources named by both reviewer briefs.

The reviewed product is the content authored by the paragraph revision and round 1 fix.

The product commit was rewritten by a later rebase.

Use the current branch content instead of relying on the old hash.

## Human authority

The human decided that each logical intent value can contain one or more paragraphs.

Both fields stay required and non-empty.

All three human projections preserve paragraph boundaries under clear labels.

All JSON projections preserve deserialised strings.

No sentence, line or character cap applies.

This decision supersedes D4's premise.

D6 concerns generated-view ownership and was not superseded by that decision.

The product repaired D6.

The fix brief prohibited a plan TOML edit while also requiring the registered Q-78 item to reflect the decision.

If those instructions conflict, treat the human decision and the structured source as authoritative.

## Raw findings

Adjudicate all nine raw findings:

- `GPT-R2-1` through `GPT-R2-6`.
- `C2-1` through `C2-3`.

Return `valid`, `dismissed` or `accepted risk` for each raw identifier.

Deduplicate only findings that share one cause, one violated obligation and one correction.

Keep separate findings when their correction or owning increment differs.

## Reproduction duties

Reproduce each behavioural claim with an independent fixture.

Reproduce each citation claim with the exact command or cited lines.

For `GPT-R2-1`, test repeated blank lines, CRLF and bare CR on every claimed human surface.

For `GPT-R2-2`, separate human display normalisation from unchanged `next --json` values.

For `GPT-R2-3`, test both partial optional-field permutations.

For `GPT-R2-4`, test an offsetting omission and duplicate across two step sections.

For `GPT-R2-5`, decide whether the structured Q-78 `ask` is live authority or marked history.

For `GPT-R2-6`, identify the four residuals and the scope of the eventual receipt obligation.

For `C2-1`, distinguish start of logical value from start of each line.

For `C2-2`, test the single-paragraph human `next` shape against RULE 10.

For `C2-3`, compare the accepted residual text with the repaired whole-file additions guard.

## Fan-out rule

The six backfill increments run one shared criteria block.

If one valid defect independently makes that block wrong for each batch, assign one loop finding to each affected increment.

A shared textual correction can close all fan-out findings.

Do not hide loop fan-out inside one increment's note.

## Settled items

Do not re-raise these accepted residuals without new evidence:

- `GB-4`.
- `GB-9`.
- `F2`.
- `F3`.

Do not re-raise D7 without evidence that changes its class, severity or measured boundary.

D6 is repaired and is not an accepted residual.

A claim that narrows or corrects the recorded boundary of an accepted residual is new evidence.

## Class and severity

Set your own severity and class for each distinct finding.

Class 1 permits zero findings.

Class 1 means a wrong implementation passes while it violates:

- A stated risk ground.
- A numbered rule.
- A cited Project Principle.

Class 2 permits at most three findings per increment, all `low` or `medium`.

Class 2 contains:

- A second-guard hole.
- A non-reproducing figure inside an increment block.
- A criterion that refuses a correct implementation.

Do not silently place another finding kind into class 2.

If a valid finding fits neither class, report that fact and explain its effect on the round outcome.

Use the eight Project Principles from the plan by name.

Do not substitute the separately numbered AGENTS.md principles.

## Loop identity and prior state

Assign every distinct finding to exactly one increment, except for required fan-out.

The increment set is:

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

Before this review:

- `plan-order-array-position-inc1` has clean streak one.
- `validate-missing-source-exit-inc1` has clean streak one.
- Every other loop has clean streak zero.
- Every loop has one round used against the cap.

The human scope change reset the seven formerly clean `step-intent-encoding` streaks.

It did not erase their round from the cap.

## Round outcome

Apply the Q-78 stop condition per increment.

Mark an increment `new_valid` when it exceeds a permitted threshold.

Mark an increment `clean` when it stays within the controlling threshold and carries no unpermitted finding kind.

A clean loop starting at streak one reaches streak two and converges.

A clean loop starting at streak zero reaches streak one.

A `new_valid` loop ends at streak zero.

Every loop remains `risky`.

No loop exceeds two rounds used after this review.

## High dismissal backstop

Flag every dismissed `high` or `critical` finding for an independent re-check.

Do not treat such a dismissal as clean before that re-check.

## Evidence environment

Run every project command through the project direnv environment.

Use GNU grep when ugrep differs.

Pin stdout when `validate` can exit zero on absent input.

Treat zero-match `grep -c` exit 1 as data.

Write fixtures only under:

`/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r2-triage`.

Create subdirectories that this triage owns.

Do not write into bare `/tmp`.

Do not use wildcard deletion.

## File safety

Do not edit product, plan, ledger, metrics, briefs or reviewer files.

Write verdicts only to:

`docs/plans/agent-scaffold.reviews/q78-reset-r2-triage.md`.

Do not push.

## Output

Include:

- One verdict for every raw finding identifier.
- A deduplication and fan-out map.
- One required correction for every valid distinct finding.
- One outcome row for every increment.
- Each row's valid count, severity list, class counts, outcome and resulting streak.
- The total raw count and the total loop-level distinct count.
- The severity ceiling.
- Every required backstop re-check.

Commit only the triage file with a conventional `docs:` subject.

Do not add attribution trailers.
