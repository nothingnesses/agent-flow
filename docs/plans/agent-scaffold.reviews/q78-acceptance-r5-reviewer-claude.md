# Q-78 acceptance pass 5, adoption and executability lens (Claude)

Reviewed artifact: branch `review/q78-acceptance-r5-claude` at `37b1b92c`, whose product content is the pass-4 planner repair `f0c43995` plus its ancestors. Baseline `main` at merge-base `a6b83b4f`, 87 changed files, all under `docs/` (`git diff --name-only a6b83b4f..HEAD | grep -v '^docs/'` returns nothing), so the product under acceptance is the plan, not code. Lens: can a fresh implementer execute what this plan now says against THIS repository's own committed data, and does the pass-4 repair close its six dispositions without introducing a new contradiction.

## Verification actually performed, and the one gate family that could not run

Gates run from the repository root against the prebuilt `agent-flow 0.0.4` at `/nix/store/4rayq0a6f1cq2cdcxm6cnhnlgqgbdjhk-source/target/debug/agent-flow`:

- `validate --source docs/plans/agent-scaffold.plan.toml`: exit 0, `467 records, valid`, `114 steps, 83 questions, valid`.
- `validate --workflow --source docs/plans/agent-scaffold.plan.toml`: exit 0, `workflow invariants hold`.
- `render --check --strict docs/plans/agent-scaffold.plan.toml`: exit 0, `up to date`.
- `git diff --check` and `git diff --check a6b83b4f..HEAD`: exit 0.
- ASCII: `LC_ALL=C grep -c -P '[^\t\x20-\x7e]'` sums to 0 over all 87 files changed since the merge-base.

I DID NOT ADOPT THAT BINARY ON TRUST. The source tree beside it differs from HEAD in exactly one file, `src/plan/source.rs`, and only by the retired `problem`/`approach` `[[step]]` fields (`diff -rq` over `src/`, `tests/` and `pack/` reports that one file and nothing else). Two probes establish that the BINARY matches HEAD rather than that store copy on the paths I rely on. (1) A scratch plan carrying `problem = "p"` on a `[[step]]` is rejected with ``unknown field `problem`, expected one of `slug`, `title`, `status`, `order`, `blocked_by`, `folds`, `provenance`, `increment`, `waiver` ``, which is HEAD's `Step` field list (`src/plan/source.rs:129-158`). (2) A scratch `[[step.increment]] id = "a-incA"` is rejected with `increment id `a-incA` is not a well-formed kebab-case id`, HEAD's message at `src/plan/source.rs:540-545` and its pinned test at `:1223`. This is evidence of correspondence on the parser paths this report uses, not proof the binary is HEAD in every respect.

`cargo test` AND `cargo clippy` DID NOT RUN, and nothing below claims them green. A toolchain exists (`cargo 1.94.1` at `/nix/store/5zzy37fv5g4wjdg9zqqyrb9gl7ypfkjl-rust-mixed/bin`), but the crate sources do not: `cargo metadata --offline` on a scratch copy of HEAD exits 101 with ``no matching package named `include_dir` found / location searched: crates.io index``, there is no cargo registry under `/home/jessea` or the scratch tree, and every `*-vendor*` path in `/nix/store` is an unrealised `.drv`. `direnv` and `nix` are not on `PATH` in this container. This is an environment fact, not a product defect, and it is unchanged from passes 3 and 4. The product diff touches no `src/`, `tests/` or `pack/` path, so no test outcome can have moved on this branch. All destructive work stayed inside `/tmp/r5scratch`; the reviewed tree was not modified.

Everything else below is reproduced with GNU grep, `awk`, `jq`, `sha256sum`, `git` and scratch fixtures driven through that binary. The join used throughout is the tool's own: a round's step is its structured `step` id else `leading_slug(task)`, and its increment is its structured `increment` id else the full `task` (`src/workflow.rs:88-96,114-135`).

## The six pass-4 dispositions

### R4-1 (`high`, unauthorable historical increment identities): CLOSED

The repair adds a typed two-arm increment-id contract: `Canonical` is today's lowercase `is_kebab_case_token`, and `LegacyFieldlessSuffix` is accepted only when the owner step slug is itself canonical and the id is the exact byte string `<owner-step-slug>-inc<X>` with `<X>` one ASCII uppercase letter, stored and compared without case-folding (`docs/plans/agent-scaffold.steps/structured-risk-class-source.md:11`). Criterion 2 pins `round-log-core-incA` and `round-log-core-incB` declaring, retaining `low_risk`/`risky` and joining the five fieldless rounds, with lowercasing as the red control; criterion 3 pins the rejections (`:37-38`).

I checked the contract against the whole population rather than the two named ids. Of the 97 increment identities that join a Roadmap step, exactly two fall outside canonical kebab-case, and both match the legacy form with the right owner:

```
round-log-core-incA   owner=round-log-core   legacy_form=YES
round-log-core-incB   owner=round-log-core   legacy_form=YES
```

So the narrow arm spans the live population with nothing left over, and it does not widen step slugs or any other token class. The step's own migration sentence now names both ids explicitly (`:15`).

### R4-2 (`high`, no declarable class home for task loops): CLOSED AS SPECIFIED, but its arm does not span the population (findings A and B)

The repair adds a top-level `[[task_loop]]` row carrying exactly `task`, `phase` and `risk_class`, keyed on the exact `(task, phase)` pair, with `task` required to equal `[meta].title` or resolve through `[meta].orphan_tasks` and `phase` parsing through a closed `TaskConvergencePhase` whose only current value is `plan_review` (`structured-risk-class-source.md:7`). The foreclosure reconstruction consumes it as a phase-bearing loop identity (`review-loop-foreclosure-enforcement.md:7,9`), `workflow-loop-visibility.md:9` requires a task `plan_review` active row to resolve it, `review-loop-class-inheritance.md:7` applies Q-80 to both arms, and criterion 5 pins the live `q78-design-pass` shape (`structured-risk-class-source.md:40`). SC 37 was rewritten to the same model.

The `q78-design-pass` evidence reproduces exactly. `sed -n '386p' docs/metrics/workflow.jsonl | tr -d '\n' | sha256sum` returns `4e7aed64e77ca228347de1cfbcf620ca2d6b6f3d8550b606212b3b448d0e95c6`, byte-identical to the digest pinned at `review-loop-foreclosure-enforcement.md:15`; records 380-386 are the seven `risky` `plan_review` rounds, record 387 belongs to another task, and `q78-design-pass` is in `[meta].orphan_tasks` (`docs/plans/agent-scaffold.plan.toml:5-25`). Every `(task, plan_review)` group in the log is internally class-consistent, so no historical plan-review window is unmigratable for want of one class.

The disposition is closed on its own terms. Findings A and B are new evidence that the two arms, taken together, do not cover the (phase x identity) product this repository's committed log actually contains; neither reopens the authority model Q-83 settled.

### R4-3 (`medium`, active increment selection): CLOSED

`structured-risk-class-source.md:13` adds the open-increment operation as a durable fact rather than a rule for readers to infer: the step introduces the two convergence-bearing `[[active_work]]` variants (task `plan_review` carrying its exact task; step `work_review` carrying a resolving step AND a resolving increment owned by it), states that a declaration is not an open-loop signal because the plan predeclares siblings, and forbids `next` and the shared reconstruction from guessing by declaration order, lexical order, latest round or first unconverged group. `workflow-loop-visibility.md:11` extends that same union without forking it, and criterion 7 (`structured-risk-class-source.md:42`) plus visibility criterion 6 (`workflow-loop-visibility.md:34`) pin the exact fixture the pass-4 report showed was unimplementable: a converged `low_risk` sibling beside a newly selected zero-round `risky` sibling reporting `awaiting-first-review`, `risky` and streak 2, with red controls for all four cheap inventions. The requirement that the referenced step be `in-progress` (`workflow-loop-visibility.md:11`) is consistent with `next` needing pre-round output only for an opened loop.

### R4-4 (`low`, stale Stage-3 scheduler gate): PARTLY CLOSED (finding C)

Both cited sites carry the bounded supersession note (`docs/plans/mealy-workflow-driver.explorations/r2-requirements-scope.md:127,170` and `docs/plans/agent-scaffold.explorations/Q-64-delivery-fsm.md:76`), each preserving the separate write-path and authoritative-driving gates. Three further statements of the same retired gate in the same requirements document were not updated; see finding C.

### R4-5 (`low`, Q-58 interval semantics): CLOSED

The distinction is now stated the same way in all three places: descriptive marginal/per-arm intervals and their overlap are never decision rules, while a precommitted paired confidence bound or paired hypothesis test may implement the frozen non-inferiority/equivalence rule (`docs/plans/code-value-audit.explorations/Q-58-ablation-design.md:88,95,116`; `docs/plans/agent-scaffold.steps/q58-output-ablation.md:21` criterion 5; `docs/plans/agent-scaffold.success-criteria.md:35`). `:81` still requires the protocol to fix "the confidence level and the exact interval or hypothesis-test method", which the repaired wording now permits rather than contradicts. `grep -n "interval\|overlap"` over the design, the step and the Success Criteria returns no site that still forbids the allowed paired procedure.

### R4-6 (`low`, stale Stage-2 authority paragraph): CLOSED

`docs/plans/agent-scaffold.steps/workflow-driver.md:20` now specifies "nested `TaskMachine`, `QuestionMachine` and `StepMachine`" and "the full task/question/step active-unit fleet", and adds that task `plan_review` reads its typed task-loop declaration and question exploration stays Roadmap-independent. That agrees with the architecture record (`docs/plans/mealy-workflow-driver.explorations/r2-architecture-build-path.md:134-149`) and with the focused sidecar's criteria (`docs/plans/agent-scaffold.steps/workflow-driver-typed-fleet.md:17-20`), which still names that paragraph as its authoritative scope at `:3`.

## Remaining shortfalls

### A. `high` - the phase-bearing split re-homes 63 of this repository's own plan-review rounds into the task arm, and two of those identities cannot be registered there at all

THE RULE. `review-loop-foreclosure-enforcement.md:7` makes loop identity phase-bearing and splits it in two: "A recorded Roadmap work window uses each event's resolved step, exact increment and `work_review`; ... A task-level convergence window uses its exact registered task and `plan_review`". `structured-risk-class-source.md:7` fixes the corresponding declaration homes and closes the crossover in both directions: the Roadmap arm is for a "Roadmap `work_review` loop", and "Roadmap `work_review` remains increment-scoped and cannot be smuggled into the task table". The task arm's key is constrained: "`task` must equal `[meta].title` or resolve through `[meta].orphan_tasks`". Migration is doubly constrained: existing task-level convergence histories migrate "with their registered exact task/phase/class ... an unregistered historical task must first enter the orphan registry", and "The append-only round log is not rewritten" (`:15`). Criterion 8 closes every escape: "A round for either convergence identity with no declaration fails closed ... neither a waiver nor the historical cap-adoption boundary suppresses a missing declaration, unresolved selection or mismatch" (`:43`). Criterion 9 forbids the remaining moves: the migration "preserves every existing converged Roadmap and task-loop identity/class, adds no round/escalation/waiver event, changes no Roadmap status" (`:44`). SC 37 ships the same rule.

THE POPULATION IS NOT THE ONE THE PASS REASONED ABOUT. Resolving every `type:"round"` record by the tool's own join and grouping by phase:

```
ROADMAP  plan_review    63
ROADMAP  work_review   202
TASK     plan_review    36
TASK     work_review     8
TASK     acceptance      4
```

The pass reasoned about the 36 orphan plan-review rounds (`q78-design-pass`, `q70-capture`, `plan-fold`, `step-intent-fold`, `q77-fold` and the rest). The 63 plan-review rounds that RESOLVE TO A ROADMAP STEP are the ones the split moves, and they are 18 distinct identities. Sixteen of the eighteen are ALREADY DECLARED `[[step.increment]]` ids carrying a `risk_class` (for example `workflow-enforcement-tier-fold` and `workflow-enforcement-tier-endproperty-fold`, both `risky`, `docs/plans/agent-scaffold.plan.toml:1334-1339`, under the `complete` step `workflow-enforcement-tier` at `:1307-1309`; also `step-intent-encoding-inc1`, `plan-order-array-position-inc1`/`-inc2`, `sidecar-status-opening-drift-inc1`, `ledger-order-citation-currency-inc1`, `validate-missing-source-exit-inc1` and the six `step-intent-encoding-inc2*`). No increment group in the log mixes phases, so each of these groups is plan-review-only: under the split their Roadmap increment declaration owns zero rounds and their history must move to a `[[task_loop]]` keyed by a string that is simultaneously a declared increment id, registered in a field whose own definition is "tasks that appear in the round log but own no Roadmap step" (`src/plan/source.rs:107-108`) when these demonstrably do own one.

TWO OF THE EIGHTEEN ARE UNAUTHORABLE OUTRIGHT. `structured-skeleton` (3 `plan_review` rounds) and `checks-runner-worktree-name-collision` (4 `plan_review` rounds) carry a `task` string that IS the Roadmap step slug (`docs/plans/agent-scaffold.plan.toml:582-584` and `:1287-1289`, both `complete`). The orphan registry refuses exactly that: "an orphan token equal to a declared step slug contradicts the field's own definition", `src/plan/source.rs:755-771`, pinned by `an_orphan_task_equal_to_a_step_slug_is_flagged` at `:1195`.

REPRODUCED, in scratch: a plan declaring a step `real-step` and `orphan_tasks = ["real-step"]` exits 1 from `validate --source` with

```
meta orphan task `real-step` is also a step slug, so it is not orphan
```

so neither identity can enter the registry, and without the registry neither can key a `[[task_loop]]`. Reproduce the population with

```bash
jq -r 'select(.type=="round") | [(.step // ""), (.increment // ""), .task, .phase] | @tsv' docs/metrics/workflow.jsonl
```

and resolving each record's step as the structured `step` else `leading_slug(task)`; then intersect the `plan_review` task strings with the plan's step slugs.

WHY THIS IS NOT ALREADY OWNED. The pass measured the orphan population and built the task arm for it, but nothing in the three sidecars or SC 37 states what happens to a `plan_review` round whose task resolves to a Roadmap step. Today it is simply an increment group of that step: W3 filters a `complete` step's rounds by step slug with no phase test and groups them by increment id (`src/workflow.rs:466-497`), which is why `structured-skeleton`'s three plan-review rounds and `checks-runner-worktree-name-collision`'s four currently serve as those steps' convergence evidence and `validate --workflow` is green.

THE CONSEQUENCE, which is why this is `high` rather than a nit. An implementer executing the step as written reaches the same shape R4-1 named. For the two colliding identities: the task arm refuses them, the Roadmap arm is `work_review`-scoped by `:7`, renaming is refused by `:44`, rewriting the log is refused by `:15`, and a waiver or the adoption boundary is refused by `:43`. The only syntactically legal move left is to declare a plan-review history as a Roadmap `work_review` increment (`[[step.increment]] id = "structured-skeleton"` parses today, since increment ids need only be canonical and unique, `src/plan/source.rs:539-549`), which is the crossover the same paragraph forbids. For the other sixteen the migration is authorable but unplanned: it silently converts sixteen declared Roadmap increments into task loops and populates the orphan registry with identities that own a Roadmap step, contradicting that field's stated definition and criterion 9's "preserves every existing converged Roadmap ... identity/class". Either way the implementer must invent an identity policy on the fail-closed enforcement path, exactly the state Q-83 exists to remove. It is not `critical` because it fails loudly at implementation and validation time rather than admitting a false green.

SMALLEST SAFE DISPOSITION. State the (phase x identity) mapping for every shape the committed log contains, not only the orphan one: say explicitly whether a `plan_review` history joined to a Roadmap step remains a Roadmap increment group (in which case the Roadmap arm is not `work_review`-only and `:7` needs correcting) or becomes a task window (in which case the task arm needs a key that does not inherit the orphan registry's not-a-step-slug rule, for example its own declared identity list, and the registry's definition needs correcting). Name `structured-skeleton`, `checks-runner-worktree-name-collision` and `workflow-enforcement-tier-fold` as migration fixtures, add a red control that a phase-blind grouping of the same records is refused, and correct criterion 9, which today asserts a preservation the schema refuses for two of this repository's own identities.

### B. `medium` - a non-Roadmap `work_review` loop has no declaration arm at all, so the population the pass newly brings under enforcement still excludes eight of this repository's own convergence rounds

`[[task_loop]]`'s phase is closed to `plan_review`, and criterion 4 requires the parser to REJECT `work_review` outright (`structured-risk-class-source.md:39`). Increments nest under a `[[step]]` (`src/plan/source.rs:153-155`), so a work-review loop that resolves to no Roadmap step can own neither arm.

THAT SHAPE IS IN THE LOG. Eight `work_review` rounds across seven identities resolve to no Roadmap step, at JSONL records 1 (`workflow-hardening`), 47 and 48 (`metrics-fields`), 164 (`q59-backlog-fold`), 173 (`decision-fold-q60-q62`), 177 (`q64-capture`), 178 (`q65-capture`) and 379 (`ship-v0-0-4`). Three of those tasks (`ship-v0-0-4`, and the plan-review-phase `q77-fold` and `step-intent-fold`) are not even in `[meta].orphan_tasks` today, so the registry is not an exhaustive record of the shape.

REPRODUCED, in scratch: a plan with one `complete` Roadmap step plus a registered orphan task, and a log whose orphan `work_review` loop runs ten rounds with `outcome` `new_valid` throughout and never converges, exits 0 from `validate --workflow` with `workflow invariants hold`. W3 iterates Roadmap steps only (`src/workflow.rs:466-470`), so nothing today reads that loop's class, streak or round count, and the repair adds no arm that would.

IMPACT. Two shipped statements are false for this population. SC 37 opens "Every convergence-loop risk class has one authoritative typed plan declaration selected before round one", and `review-loop-foreclosure-enforcement.md:17` says the adoption boundary "preserves fail-loud enforcement for future Roadmap and task loops"; a future non-Roadmap work review can still log `low_risk` on round one of a risky artefact and converge at one clean round with every validator green, which is the exact silent downgrade Q-83 was chosen to eliminate. Read the other way, as criterion 8's "either convergence identity with no declaration fails closed", the eight historical records have no authorable declaration and validation fails permanently on this repository. It is `medium` rather than `high` because the first reading is a continuation of today's behaviour with no data loss and the second fails loudly; a triager applying the pass-4 precedent for R4-2 (where the same silent-downgrade argument carried `high`) may reasonably raise it.

SMALLEST SAFE DISPOSITION. Either widen `TaskConvergencePhase` to admit `work_review` for a task that owns no Roadmap step (and drop that rejection from criterion 4), or state plainly in SC 37 and `structured-risk-class-source.md:7` that a work review is a convergence loop ONLY when it joins a Roadmap increment, name the eight records as the closed historical set that is out of scope, and give the reason. Pin whichever choice with a fixture built from record 379, and a red control that a new non-Roadmap `work_review` round after the fix is classified the way the text says.

### C. `low` - three further statements of the retired real-parallelism gate survive in the document the pass annotated twice

The pass chose to annotate rather than freeze: `r2-requirements-scope.md:127` and `:170` now carry "Q-82 later schedules the typed fleet and supersedes the former real-parallelism gate for the read-only scheduler alone", each preserving the separate write-path and authoritative-driving gates. Three statements of the same gate in the same document were left unannotated:

- `:34` "The full FLEET (many units tracked at once) is an S2 requirement; it earns its keep only when parallel units actually run (see FR-SCHED and the non-functional multi-agent requirement), so the MVP does not need it."
- `:67` "the scheduler is IN scope for the full driver but is an S2 requirement gated on the multi-agent non-functional requirement below actually being exercised; ship the single-unit advisory reconstruction (S1) with the scheduler stubbed to 'the one ready unit' until parallel runs occur."
- `:175`, inside the YAGNI boundary, "Do NOT build the fleet + scheduler before parallel units actually run; ship S1 with a single-unit 'the one ready unit' scheduler and expand when NFR-PARALLEL is exercised."

`:175` is the sharpest, because a YAGNI boundary reads as a live directive and the Roadmap now schedules `workflow-ready-frontier-scheduler` (`docs/plans/agent-scaffold.plan.toml:1752-1756`) and its typed fleet. This is `low`: the focused sidecar is the implementation authority (`docs/plans/agent-scaffold.steps/workflow-ready-frontier-scheduler.md:3`) so no implementer is blocked, but the acceptance documentation-currency check is not met and one document answers the same question two ways. Smallest disposition: extend the same one-clause note to those three sites, or state once at the head of the document that its Stage-2/Stage-3 gates are pre-Q-82 history and name the sidecar that supersedes them.

### D. `low` - the current-history evidence paragraph still enumerates two acceptance records where the log now carries four

`review-loop-foreclosure-enforcement.md:13` reads "Acceptance records 432 and 433 are later single-pass phases, not an eighth/ninth plan-review round and do not read that declaration." The log carries four `q78-design-pass` `acceptance` records, at lines 432, 433, 434 and 435, the last two being the pass-3 and pass-4 acceptance rounds (record 435's `artifact` names `q78-acceptance-r4-triage.md`). Both already existed when the pass-4 repair edited this exact sentence: `git show 503dd3e5:docs/metrics/workflow.jsonl | sed -n '435p'` returns the pass-4 record, and `git show f0c43995 -- .../review-loop-foreclosure-enforcement.md` shows the sentence rewritten around the unchanged ordinal pair. Criterion 6 asks for a current-history fixture with "separate acceptance records" (`:30`), so a fixture built from this paragraph under-represents the real set, and this pass adds a fifth record, which is the pattern rather than the accident. `low`: the load-bearing claim (acceptance is single-pass and does not join the plan-review window) is correct and the digest-pinned boundary is unaffected. Smallest disposition: state the selector (`task == "q78-design-pass" && phase == "acceptance"`) as the paragraph already does for the plan-review rounds, instead of enumerating ordinals that grow with each pass.

## Result

Four shortfalls remain: one `high` (A), one `medium` (B) and two `low` (C, D). All six pass-4 dispositions are closed on their own terms; R4-4 is closed at both cited sites with three uncited siblings left stale (C). Findings A and B are one root cause seen from two sides, that the two declaration arms do not span the (phase x identity) product the committed log actually contains, but they need different fixes and are reported separately for that reason; neither reopens Q-83's settled authority model. I also re-checked the pass-1 through pass-3 dispositions this pass touches (the pending ready/blocked fallback, the question-scoped exploration carrier, the scheduler eligibility and precedence rules, the frozen ablation protocol and the digest-pinned cap-adoption boundary) without finding a regression. Q-78 should not settle acceptance until A is dispositioned, because the migration it mandates has no legal state for two of this repository's own converged identities.
