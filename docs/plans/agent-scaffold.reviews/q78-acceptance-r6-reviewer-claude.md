# Q-78 acceptance pass 6, adoption and executability lens (Claude)

Reviewed artifact: branch `review/q78-acceptance-r6-claude` at `43d6309c`, whose product content is the pass-5 planner repair `9decef03` plus its ancestors. Baseline `main` at merge-base `f79c92a7`, 95 changed files, all under `docs/` (`git diff --name-only f79c92a7..HEAD | grep -v '^docs/'` returns nothing), so the product under acceptance is the planning artefact, not code. Lens: does the pass-5 repair close its five dispositions without introducing a new contradiction, and can a fresh implementer execute what the plan now says against THIS repository's own committed log.

## Verification actually performed, and the one gate family that could not run

Gates run from the repository root against the prebuilt `agent-flow 0.0.4` at `/nix/store/4rayq0a6f1cq2cdcxm6cnhnlgqgbdjhk-source/target/debug/agent-flow`:

- `validate --source docs/plans/agent-scaffold.plan.toml`: exit 0, `468 records, valid`, `114 steps, 83 questions, valid`.
- `validate --workflow --source docs/plans/agent-scaffold.plan.toml`: exit 0, `workflow invariants hold`.
- `render --check --strict docs/plans/agent-scaffold.plan.toml`: exit 0, `up to date`.
- `agent-flow checks` through a scratch-only `PATH` shim: `1 passed, 0 failed, 0 skipped`.
- `git diff --check` and `git diff --check f79c92a7..HEAD`: exit 0.
- ASCII: `LC_ALL=C grep -cP '[^\t\x20-\x7e]'` sums to 0 over all 95 files changed since the merge-base.

I DID NOT ADOPT THAT BINARY ON TRUST. The source tree beside it differs from HEAD in exactly one file, `src/plan/source.rs`, and only by the retired `problem`/`approach` `[[step]]` fields (`diff -rq` over `src/`, `tests/` and `pack/` reports that one file and nothing else), so the store copy is NOT the binary's provenance on the paths this report uses. Two scratch probes establish correspondence with HEAD instead. (1) A plan carrying `problem = "p"` on a `[[step]]` is rejected with ``unknown field `problem`, expected one of `slug`, `title`, `status`, `order`, `blocked_by`, `folds`, `provenance`, `increment`, `waiver` ``, which is HEAD's `Step` field list. (2) `[[step.increment]] id = "alpha-incA"` is rejected with ``increment id `alpha-incA` is not a well-formed kebab-case id``, HEAD's current lowercase-only rule. This is evidence of correspondence on the parser paths below, not proof the binary is HEAD in every respect.

`cargo test` AND `cargo clippy` DID NOT RUN, and nothing below claims them green. A toolchain exists (`cargo 1.95.0` at `/nix/store/9l9lclxjw8ns5q4k13lxld7pl90paa3g-rust-mixed/bin`), but the crate sources do not: `cargo metadata --offline` exits 101 with ``no matching package named `include_dir` found / location searched: crates.io index``, there is no cargo registry under `/home/jessea`, and every `*-vendor*` path in `/nix/store` is an unrealised `.drv`. `direnv` and `nix` are not on `PATH` in this container. This is an environment fact, not a product defect, and it is unchanged from passes 3, 4 and 5. The product diff touches no `src/`, `tests/` or `pack/` path, so no test or lint outcome can have moved on this branch.

Everything else below is reproduced with GNU grep, `awk`, `jq`, `sha256sum`, `git` and scratch fixtures. All destructive work stayed inside the authorised scratch mount; the reviewed tree was not modified. The join used throughout is the tool's own: a round's step is its structured `step` id else `task` with a trailing `-inc<alnum>` removed, and its increment is its structured `increment` id else the full `task`.

The historical population reproduces exactly as the repair describes it: 63 Roadmap-owned `plan_review` rounds, 202 Roadmap-owned `work_review`, 36 non-Roadmap `plan_review`, 8 non-Roadmap `work_review`, 5 non-Roadmap `acceptance`.

## The five pass-5 dispositions

### R5-1 (`high`, no phase-preserving home for Roadmap-resolving plan review): CLOSED

The repair adds a phase-bearing `LoopDeclaration` with a `RoadmapIncrement` arm carrying a required `phase`, a `TaskPlanReview` arm keyed on the exact `(task, phase)` pair, and a migration-only `[[step.historical_plan_review]]` category for the exact step-slug identities (`docs/plans/agent-scaffold.steps/structured-risk-class-source.md:11-12,26`). Phase-blind grouping by `(step, increment)` is expressly forbidden (`:18`).

I reproduced the population rather than reading the claim. The 63 Roadmap-owned `plan_review` rounds carry exactly 18 distinct identities: 2 exact step-slug (`structured-skeleton` at records 98/99/115, `checks-runner-worktree-name-collision` at 217/219/220/221 - 7 rounds), 3 fieldless-increment (`decision-folder-currency-fold`, `workflow-enforcement-tier-fold`, `workflow-enforcement-tier-endproperty-fold`), and the 13 structured Q-81 increments. All seven `[[step.historical_plan_review]]` digests in `:28` reproduce byte-for-byte with `sed -n "${n}p" docs/metrics/workflow.jsonl | tr -d '\n' | sha256sum`. No Roadmap slug is placed in `orphan_tasks` and no recorded `plan_review` is relabelled `work_review`. The Q-81 pin in criterion 6 also reproduces: 41 `plan_review` rounds at records 387-430 over exactly 13 structured increments, with escalations at 421, 422 and 429.

Population coverage is not complete, however; see finding A.

### R5-2 (`medium`, non-Roadmap work review unrepresented): CLOSED

`:30` adds a typed migration-only `[[meta.historical_work_review]]` category that parses as `HistoricalUnownedWorkReview` rather than `LoopDeclaration`, cannot be active, cannot satisfy W3, and states outright that "An unselected future record fails workflow validation rather than remaining accepted and unjoined." The eight retained records are pinned at `:32` as seven rows over seven exact tasks (`metrics-fields` carries two). I reproduced the population - records 1, 47, 48, 164, 173, 177, 178, 379, all `low_risk` - and all eight digests match byte-for-byte. Criterion 8 (`:62`) pins the record-379-shaped fixture and the append-a-new-shape red control the triage asked for.

### R5-3 (`medium`, the single `ReviewLoop` type cannot implement its own single-pass contract): CLOSED

The authoritative type sketch is now a disjoint enum. `ConvergencePhase` admits only `PlanReview | WorkReview`; `SinglePassPhase` admits only `Acceptance | Review`; `SinglePassReview` has no round counter, streak, foreclosure, cap or declaration parameter, while retaining `SinglePassAwait::Recheck` for a high/critical dismissal (`docs/plans/mealy-workflow-driver.explorations/r2-architecture-build-path.md:99-160`). The same split is carried through `review-loop-foreclosure-enforcement.md:9-11` and its criteria 2 and 4, `workflow-driver-typed-fleet.md:58-63` and its criterion 2 compile-fail controls, and back into round 1's `fsm-concurrency-model.md:52,64`, which no longer calls acceptance a "degenerate variant" of the loop. `grep -rn 'degenerate' docs/plans/` returns no surviving use of the retired framing in the driver explorations.

### R5-4 (`low`, stale real-parallelism gate at three requirements-scope sites): CLOSED

All three cited sites now carry the bounded supersession, and so do two further statements the triage did not enumerate: `r2-requirements-scope.md:34,67,127,170,175`. Each preserves the two gates the triage required to survive - the `record-*` write path behind advisory-adoption evidence plus reopening Q-24, and authoritative driving behind a measured-low override rate. `:175`, the YAGNI imperative the triage flagged as the sharpest of the three, now reads "SUPERSEDED BY Q-82 for the typed fleet and read-only scheduler" while still forbidding fan-out, the write path and authoritative driving.

### R5-5 (`low`, growing acceptance ordinals): CLOSED, and this pass demonstrates why it mattered

`review-loop-foreclosure-enforcement.md:19` and its criterion 9 (`:39`) now select by `task == "q78-design-pass" && phase == "acceptance"` and state that "no acceptance ordinal is part of the contract". The selector is durable in fact and not just in wording: the log carried four such records when the pass-5 triage ran and carries five now (records 432-436), and the plan-review assertion is unchanged. Both halves of the reproduction command in `:19` hold - selecting `task == "q78-design-pass" && type == "round" && phase == "plan_review"` yields exactly records 380-386, and selecting an escalation for that task yields nothing. The `[[meta.review_cap_adoption]]` digest for record 386 (`4e7aed64e77ca228347de1cfbcf620ca2d6b6f3d8550b606212b3b448d0e95c6`) reproduces.

## Remaining shortfalls

### A. `medium` - the migration worklist does not home three of this repository's own plan-review identities, and the completeness sentence asserts that it does

`structured-risk-class-source.md:34` states the migration as complete: "the two exact step-slug histories gain digest-pinned `[[step.historical_plan_review]]` rows; all sixteen increment identities retain their existing `[[step.increment]]` class and gain the observed `plan_review` phase; ... task plan-review histories gain exact task declarations". `:45`'s changed-plan-source worklist implements exactly that list, whose only increment-declaration instruction is "retain every increment id/class" and whose only task instruction is "add task-loop declarations for REGISTERED task plan-review histories". Three identities in the committed log satisfy neither.

POPULATION 1, one of the sixteen has nothing to retain. `:7` names `decision-folder-currency-fold` as one of the three fieldless-increment identities. `grep -n 'id = "decision-folder-currency' docs/plans/agent-scaffold.plan.toml` returns one line, `1259: id = "decision-folder-currency-inc1"`. Its sibling `workflow-enforcement-tier-fold` and `workflow-enforcement-tier-endproperty-fold` ARE declared (`:1334`, `:1338`), so 15 of the 16 retain an existing class and this one has none to retain. It is also not a step slug, not in `[meta].orphan_tasks` (`docs/plans/agent-scaffold.plan.toml:5-24`), and not one of the two digest-pinned exact-step rows, whose selectors `:28` closes with "no cutoff admits another record". Under `:16`'s mapping - a round carrying `step` but no `increment` resolves only if `task` equals an increment owned by that step or equals the step slug, and "any other value fails" - its five rounds (records 210-214, `step` `decision-folder-currency`, `phase` `plan_review`, `low_risk`, peak `consecutive_clean` 1) reach the failing branch.

POPULATION 2, two task identities cannot be declared without a registration step nobody instructs. `:12` requires a `[[task_loop]]`'s `task` to equal `[meta].title` or resolve through `[meta].orphan_tasks`, and `:16` says "A non-Roadmap `plan_review` resolves only through its exact task declaration". Of the 14 non-Roadmap `plan_review` task identities in the log, `q77-fold` (4 rounds) and `step-intent-fold` (6 rounds plus the phase-less escalation at `human_decision` `decision`) are absent from `orphan_tasks`. Reproduce with `comm -23` over the two sorted lists:

```
#!/usr/bin/env bash
# Non-Roadmap plan-review task identities that are not registered in [meta].orphan_tasks.
PLAN=docs/plans/agent-scaffold.plan.toml
LOG=docs/metrics/workflow.jsonl
grep -oP '^slug = "\K[^"]+' "$PLAN" | sort > /tmp/steps.$$
sed -n '/^orphan_tasks = \[/,/^\]/p' "$PLAN" | grep -oP '"\K[^"]+' | sort > /tmp/orphans.$$
jq -r 'select(.type=="round" and .phase=="plan_review")
       | [(.step // (.task | sub("-inc[a-zA-Z0-9]+$"; ""))), .task] | @tsv' "$LOG" |
  sort -u | while IFS=$'\t' read -r step task; do
    grep -qxF "$step" /tmp/steps.$$ || printf '%s\n' "$task"
  done | sort -u > /tmp/npr.$$
comm -23 /tmp/npr.$$ /tmp/orphans.$$
rm -f /tmp/steps.$$ /tmp/orphans.$$ /tmp/npr.$$
```

MEASURED, run under bash from the repository root, it prints exactly two lines, `q77-fold` and `step-intent-fold`; dropping the final `comm` prints the whole 14-task population. `:45`'s "registered" qualifier scopes the worklist away from exactly these two.

WHY THIS IS A SHORTFALL AND NOT A NIT. `:14` makes a missing declaration or unresolved join fail closed before any convergence arithmetic, so on the migrated tree either `validate --workflow` goes red on 15 of this repository's own plan-review rounds, or these three identities stay "accepted and unjoined" - the state `:30` calls insufficient for the symmetric work-review case one paragraph later. This is R5-1's class recurring at a smaller radius. It is `medium` rather than `high` because, unlike R5-1's step-slug identities (which a Roadmap slug in `orphan_tasks` structurally cannot register), every route here exists and needs no human decision: the classes are unambiguous in the log (all three are `low_risk`), and `decision-folder-currency-fold`'s peak streak of 1 already meets the low-risk bar.

NO CRITERION CATCHES POPULATION 2. Criterion 5 (`:59`) pins the 63 Roadmap-resolving rounds, so it would fail on population 1 at implementation time and force the implementer to author an identity the worklist does not authorise. Criterion 6 pins Q-81, criterion 7 pins `q78-design-pass` alone, and criterion 8 pins the eight unowned work reviews. Nothing pins the other 13 non-Roadmap plan-review task identities or names `q77-fold` or `step-intent-fold`, so population 2 would land silently.

SMALLEST SAFE DISPOSITION. Correct `:34` to distinguish the fifteen retained increment declarations from the one that must be authored, and extend `:45` with the two missing actions: declare `decision-folder-currency-fold` as a `[[step.increment]]` of `decision-folder-currency` with its observed `low_risk` class and `phase = "plan_review"`, and register `q77-fold` and `step-intent-fold` in `[meta].orphan_tasks` before giving each its `[[task_loop]]` row. Then widen criterion 5 (or add a criterion) so the current-history fixture covers all 99 plan-review rounds - the 63 Roadmap-resolving ones and the 36 non-Roadmap ones - rather than the Roadmap half plus two named tasks, with a red control for an unregistered task identity.

### B. `low` - the drift step's one dated measurement paragraph no longer reproduces, and this pass is what moved it

`sidecar-status-opening-drift.md:19` heads the paragraph "THE MEASUREMENT THE SPLIT DIRECTED IS NOW MADE" and instructs "Reproduce the three numbers with the commands under ACCEPTANCE below, on a throwaway copy of `docs/`". `:21` states 45 for the unanchored selector and 28 flagged, adding "That is the 28 the decision named, and it reproduces"; `:23` states 36 for the anchored selector and "THE AUTHORED-REPLACEMENT POPULATION IS NINETEEN"; `:25` states "THE SPLIT STANDS AT 19"; `:29` and `:116` both repeat 19 as the handover size. `:205` names this paragraph as "the one dated statement of them", which is why the figures live here and not in the criteria.

Running the two criterion-1 selectors (`:123-131` unanchored-relaxed at `:136-143`) and the criterion-2 `H1` script (`:168-185`) verbatim on HEAD prints 44 / 35 / 27 / 18. Running the identical commands against `f05c3678`, the tree before this pass's second acceptance repair, prints 45 / 36 / 28 / 19 - the four stated figures exactly. The single member that left is `workflow-driver`: `dde47d19` ("docs: repair Q-78 second acceptance findings") rewrote its opening from "Not started; the build-start is a separate pending human decision..." to "The umbrella carries a delivered foundation and scheduled successors..." (`docs/plans/agent-scaffold.steps/workflow-driver.md:3`), which is the authored-replacement work the handover exists to schedule, done inside an acceptance repair. `comm -23` over the two anchored sets confirms `workflow-driver` is the only difference.

IMPACT IS BOUNDED, WHICH IS WHY THIS IS `low`. `:205` deliberately keeps figures out of the criteria; criterion 1's pass condition compares slug columns rather than counts (`:147-153`); and `sidecar-status-authored-openings.md:218` captures the handover dynamically at its own base and states "no implementation criterion hard-codes its old count". So no implementer is misdirected into wrong work. What is wrong is the plan's own published statement, in the sidecar whose entire subject is a stale second copy of a fact the structured source owns, and the pass's own recorded discipline for this exact movement - `:25`, "A size the human weighed had moved, so the decision was re-put rather than adjusted here" - was applied the first time and not the second.

SMALLEST SAFE DISPOSITION. Re-measure and restate the four figures in that one dated paragraph, name `workflow-driver` as the member this pass removed and why, and either re-put the corrected split size under `Q-78-driftsize`'s own precedent or record explicitly why a one-file movement in the same direction does not warrant re-putting it.

## What I checked and found sound, recorded so a later round does not re-derive it

- The nine adjectival openings the anchored selector excludes reproduce at nine, and all nine steps are `status = "deferred"`, as `step-intent-encoding.md:53,756` and `sidecar-status-opening-drift.md:22` claim. `exploration-mode.md:7` opens "Next." on a `complete` step, as `:113` records.
- Q-79's positional claims reproduce on today's rendered Roadmap: `file-safety-rules` at row 17 and `findings-files` at row 26 (nine rows below), and `exploration-mode`'s four members at 37, 40, 41 and 46 with exactly six non-members between them.
- SC 39's executability clauses hold. `step-intent-encoding.md`'s R2 admits a prose source only at `docs/plans/agent-scaffold.md` or `docs/plans/agent-scaffold.steps/<slug>.md` (`:675-679`), requires a decision source to be one `<commit>:docs/metrics/workflow.jsonl#L<line>` receipt whose `task` equals the row's slug (`:659-662`), and rejects the unqualified metrics path (`:666-668`). I ran R2's exact jq predicate against every `type:"decision"` record whose `task` is a Roadmap step slug: 116 of 116 pass, so the receipt route is executable against real data rather than only well-formed on paper. R4's eight named front/tail sidecars match `[meta.sidecars]` exactly (`docs/plans/agent-scaffold.plan.toml:27-37`).
- The four design residuals enumerated in `docs/plans/step-intent-encoding.explorations/Q-78.md:324` match the four under `THE RESIDUALS THIS STEP ACCEPTS RATHER THAN CLOSES` at `step-intent-encoding.md:1073-1083` one for one, and the paragraph-value decision agrees across the question sidecar, the exploration (`:7,82-91`) and the owning step (`:27-29`).
- SC 39's second sentence holds: `sidecar-status-authored-openings` is authored and blocked on its predecessor, and `validate-missing-source-exit.md:124-128` puts the exit-code change in `CHANGELOG.md` while recording, with its measurement, that the README carries no promise the change falsifies and therefore stays outside the changed-path set.
- SC 35's single-source rule holds: the reopening measurement has exactly one exact home (`docs/plans/code-value-audit.explorations/Q-58-ablation-design.md:17-28`, commit `3ad7b2b`, 1434 lines / 113409 words / 727754 bytes), every other site says "roughly 728 KB" and points there, and `q58-output-ablation.md:17` makes a fresh pre-run measurement mandatory while barring the old figures as pass conditions.
- Every declared increment id and risk class in the plan TOML matches its sidecar's stated class for all fourteen branch-touched steps, and the `blocked_by` edges match the sequencing the Q-82 and Q-58 decisions record (`resume-state-currency-signal` on `q58-output-ablation`; `workflow-driver-typed-fleet` on visibility, currency and foreclosure; the scheduler on the fleet).
- `docs/metrics/workflow.jsonl` contains no `type:"waiver"` record, and the live nested `[[step.waiver]]` rows validate, as `toml-primary-waiver-guidance.md:175` requires. That step's premise also reproduces: `pack/instrument.md:11` still presents `type:"waiver"` as the live exemption record with no TOML-primary qualification, which is the shipped staleness it schedules.
- The ledger's round-records narrative is current through this pass (`docs/plans/agent-scaffold.ledger.md:535,541,549` record passes 1-5 and name pass 6 as the next action), and the 2026-08-02 supersession paragraph at `:529` explicitly overrides the older `CURRENT TRANSIENT STATE` anchor at `:337`, so the two are ordered rather than contradictory.

## Result

TWO SHORTFALLS: one `medium` (A, the migration worklist does not home `decision-folder-currency-fold`, `q77-fold` or `step-intent-fold`, while `:34` asserts the migration is complete) and one `low` (B, the drift step's dated measurement paragraph reads 45/36/28/19 where the tree now reproduces 44/35/27/18, moved by this pass's own repair). All five pass-5 dispositions are CLOSED on their own terms; finding A is a smaller recurrence of R5-1's class at a population R5-1 did not reach, not a re-raise of it.
