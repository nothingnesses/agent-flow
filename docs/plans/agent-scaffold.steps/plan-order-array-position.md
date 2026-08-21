### `plan-order-array-position`: delete the `order` field so the `[[step]]` array position is the plan order (`Q-78-arrayorder`, decided 2026-08-21)

THIS STEP MUST NOT BUILD UNTIL THE `Q-78` REVIEW LOOP CONVERGES. The direction is decided: the human chose array position over an explicit slug list on 2026-08-21, receipt `type:"decision"` `q_id:"Q-78-arrayorder"` in `docs/metrics/workflow.jsonl`. What is not finished is the review the human directed on 2026-08-19, which runs on the design pass and on this sidecar before either enters the plan as the plan's answer. The design pass is `docs/plans/step-intent-encoding.explorations/Q-78.md`, which carries the reasoning, the rejected alternatives and the measurement appendix. This sidecar states what the step builds, in what order, and what each increment proves. It states no count of the plan's steps, because such a count expires and the plan's own standing cure, recorded in the ledger against orchestrator defect (12), is to carry the selecting command instead.

NO COMMIT SHA IS WRITTEN FOR THE RECEIPT AND THE REASON IS RECORDED. The receipt is named by `q_id`, which is stable. The commit that carries the receipt is the same commit that carries this paragraph, and the ledger already records what happens when a paragraph names the commit that writes it: the commit named is never the commit that carries the paragraph, because writing the paragraph moves `HEAD` past it. `q_id` has no such trap.

THIS STEP LOST ITS UMBRELLA HALF ON 2026-08-21, and the slug changed with it. The human split typed umbrella membership out of the `Q-78` pass into its own (`q_id:"Q-78-umbrellascope"`), so the third increment of the earlier draft left with it. `Q-79` owns that work and `docs/plans/umbrella-membership.explorations/Q-79.md` carries its evidence, its recommended form and the seven specification defects two review rounds found in it. This step is the `order` deletion and the prose sweep it forces, and nothing else.

THE PROBLEM. The plan carries the step order twice. `[[step]].order` states it as a number, and the declaration sequence of the `[[step]]` blocks states it as a position. The two agree today at every step except one, and a reprioritisation has to renumber both. The human ruled on 2026-08-19 that a numeric field is the wrong representation, because a reprioritisation renumbers many entries where a cut and paste of an entry does not.

THE APPROACH. Delete the number and keep the position.

### WHAT IT DOES

Delete the `order` field from `[[step]]`, so the position of a block in the `[[step]]` array is the plan order (`Q-78-arrayorder`, human, 2026-08-21). The field goes from the schema, from `render`'s sort, from `next`'s `StepInfo` and its three loop-selection arms, from every inline `[[step]]` literal in `src/` and `tests/`, from the four TOML fixtures and from every block of the live plan, which is 105 of them on the tree this sidecar was spliced into.

THE MIGRATION HAS A BYTE-EXACT ORACLE AND IT COVERS THE CODE ONLY. `render` sorts by `order` then slug and emits no order column, so the rendered document does not change, on one condition: the declaration sequence must equal today's rendered sequence. It does not, at exactly one place. `rename-to-agent-flow` stands 84th in the file and renders 98th, because the values 84 and 91 are absent from the range. So increment 1 moves that one block to declaration position 98, and then a fresh render matches the committed `docs/plans/agent-scaffold.md` byte for byte.

THE ORACLE DOES NOT COVER THE PROSE, WHICH IS WHY THE STEP SPLITS. The rendered plan inlines every step sidecar verbatim, so a prose correction changes the projection. A byte-exact criterion and a prose fix cannot share a commit. Increment 1 is the code and schema change under the unchanged projection. Increment 2 is the prose currency pass whose diff to the rendered plan is expected and enumerated.

### RULES

RULE 1. ARRAY POSITION IS THE ORDER, AND NOTHING RESTORES A SORT. `render` emits the steps in declaration order. `next` takes the FIRST match in each of its three selection arms. A sort by slug, a sort by title and a reverse iteration are each a defect, and criterion 4 is what detects them.

RULE 2. THE THREE ARMS ARE THREE SEPARATE OBLIGATIONS. `select_active_loop` has three arms and the live plan exercises one of them, because the live plan always holds an in-progress step. A criterion that reads `next` against the live plan alone proves arm 1 and proves nothing about arms 2 and 3. This is measured, under WRONG IMPLEMENTATION A-2 in the specification rebuild.

RULE 3. THE TEMPLATE PAIR IS ONE ARTEFACT IN TWO FILES. `pack/pack.toml:39` copies `pack/plan-template.plan.toml` to `docs/plans/TEMPLATE.plan.toml` verbatim, and `src/agents_md_drift.rs` names that family as unguarded. Measured: an edit to the pack source alone, with the committed copy left stale, gives `cargo test` zero failures, `render --check --strict` exit 0 and `validate` exit 0. Only `cmp` detects it. Every increment that touches either file runs the `cmp`. Do not run `just scaffold-self` in its place, because that recipe also runs `nix fmt` over a tree that is not formatter-clean.

RULE 4. THE PROSE FIX RESTATES BY SLUG AND NEVER RENUMBERS. A renumbered citation is still a positional citation and it drifts again on the next reorder. Principle 8, Structured data first, project for humans, decides it: the slug is the stable identifier and the position is a projection. Criterion 2 of increment 2 detects a renumbering.

RULE 5. THE STEP DETAILS SIDECAR OF THIS STEP AND OF ITS SIBLING BOTH CITE `reviewer-reproducible-evidence`. That sidecar's opening carries `step 86`, which is a citation by `order` value, and `sidecar-status-opening-drift` edits the same line for its leading token. The two edits touch different parts of one line. Whichever step runs second must leave the other's edit intact.

THE INCREMENTS ARE DECLARED IN THE PLAN TOML as `[[step.increment]]` entries with their risk classes, so a round record joins to them structurally rather than by a lexical prefix (Principle 8, Structured data first). The classes are stated at authoring time because the plan's convention is that the declared class IS the loop-open classification, which `validation-constraints` follows for its own unbuilt increments. EACH CLASS STATES ITS GROUND, in the shape `test-tmpdir-repo-assumption.md` uses, because a class sets the required clean-round count and a class asserted without a ground is the defect this pass polices elsewhere (Principle 6, Ground decisions in evidence).

### Increment 1, `plan-order-array-position-inc1`: the code and schema deletion

RISK CLASS `risky` (two consecutive clean review rounds). THE GROUND: the increment removes a field from the plan schema, so every previously valid plan in every scaffolded project fails to parse until edited, and it changes the sequencing rule that `render` and `next` both read. That is widely depended on and it is hard to roll back once a downstream plan is edited, which is the `AGENTS.md` test. It is the opposite of the plan's worked `low_risk` example at `test-tmpdir-repo-assumption.md`, which is confined to `#[cfg(test)]` code and ships nothing to a scaffolded project.

THE CHANGED-PATH SET, ESTABLISHED BY SEARCH. Reproduce the declaration sites with this command, and treat its output rather than this list as the record:

```
for f in $(grep -rlE '(\\n|^)order = ' src tests pack docs/plans/TEMPLATE.plan.toml | sort); do
  printf '%s\t%s\n' "$(grep -oE '(\\n|^)order = ' "$f" | wc -l)" "$f"
done
```

Measured on the tree this file was written against, that command returns 12 files and 69 sites. Note that the plain search `grep -rn 'order = '` returns two false positives that the anchored form above excludes: `src/tui.rs:626` matches inside `let border = if focused {`, and `src/main.rs:2427` matches inside `default_order = 1`. Neither file changes.

CODE THAT READS THE FIELD, complete:

- `src/plan/source.rs`, the `order` field on `Step` and its doc comment. Deleted.
- `src/plan/render.rs`, the sort by `order` then slug. Deleted, and the caller keeps declaration order.
- `src/plan/render.rs`, the Roadmap table doc comment that says `(slug, status, order)`. Corrected to name the emitted columns. It is stale today, before any change.
- `src/next.rs`, `StepInfo.order`. Deleted, with the assignment in `steps_from_toml` and the index derivation in `steps_from_markdown`.
- `src/next.rs`, the three `min_by_key` calls in `select_active_loop`. Each becomes a first-match `find` over the slice.
- `src/next.rs`, the `test_step` helper and its 25 call sites. The `order: u64` parameter goes.

DECLARATIONS, TESTS AND FIXTURES:

- `src/plan/source.rs` (32 sites), `src/workflow.rs` (13), `src/plan/render.rs` (3), `src/next.rs` (2).
- `tests/unsafe_pairings_are_refused_and_omitted.rs` (4), `tests/metrics_and_ledger_anchor_to_the_plan_source.rs` (1), `tests/validate_toml_primary_skips_markdown_plan.rs` (1), `tests/validate_workflow_toml_source_needs_no_plan.rs` (1).
- `src/plan/testdata/render-fixture.plan.toml` (7), `src/plan/testdata/skeleton.plan.toml` (3), `pack/plan-template.plan.toml` (1), `docs/plans/TEMPLATE.plan.toml` (1).
- `docs/plans/agent-scaffold.plan.toml`, every `order` line, 105 of them on the tree this sidecar was spliced into, plus the move of one block.

THE RENDER GOLDEN AND THE TIE-BREAK TEST ARE ONE MOVE:

- `src/plan/testdata/render-fixture.md`, where the `epsilon` and `zeta` Roadmap rows swap AND their two Step Details bodies swap.
- `src/plan/testdata/render-fixture.steps/zeta.md` and `epsilon.md`, which both say "shares Roadmap order 5".
- `src/plan/testdata/render-fixture.plan.toml`, whose header comment and whose `zeta` block comment both state the tie-break claim.
- `ordering_is_numeric_for_questions_and_slug_tiebroken_for_equal_order_steps` in `src/plan/render.rs`. Its STEP assertion re-points at declaration order and the test takes a name that matches. The QUESTION assertions and the skipped/optional/deferred bucket assertion stay. Do not delete the test.

NO FILE UNDER `docs/plans/` OTHER THAN THE PLAN TOML CHANGES IN THIS INCREMENT. `docs/plans/agent-scaffold.md` in particular must not change, and criterion 2 is what proves it.

THE ONE DATA MOVE THE MIGRATION OWES, REPRODUCED. Every step's declaration position agrees with its rendered position except `rename-to-agent-flow`. Reproduce the exception with:

```
awk '/^slug = /{s=$3} /^order = /{sub(/order = /,""); if ($0+0 < p) print "out of place:", ps; p=$0+0; ps=s}' docs/plans/agent-scaffold.plan.toml
```

WHY THE FIELD IS DELETED RATHER THAN REPLACED BY A SLUG LIST. An explicit ordered list of slugs in `[meta]` moves one line per reprioritisation, against a whole `[[step]]` block. The design pass states the priced pair once, with its command, and this sidecar does not restate it. The design pass rejects the list under Principle 5, Make illegal states unrepresentable, because a list admits a duplicate entry, a missing entry and an entry that names no step, where an array admits none of the three, and under Principle 2, Minimal by default, because the deletion removes a field, a sort and three call sites where a list adds a field, a permutation rule and a lookup. The design pass also quotes the project's own earlier ruling: `docs/plans/structured-skeleton.explorations/design-A-minimal-schema.md:83` argued array position before the schema shipped, and `design-B-rich-schema.md:147` gave the counter-rationale that won, which is that reordering must be a field edit rather than a line move. The human's 2026-08-19 clarification reverses exactly that premise, and the human chose array position on 2026-08-21.

THE SUPPORTING MEASUREMENT. `steps_from_markdown` (`src/next.rs:560`) already derives the order from the table index, because the Markdown Roadmap carries no order field. The deletion makes the two substrates agree rather than diverge.

ACCEPTANCE, EACH EXECUTABLE.

1. THE FIELD IS GONE, EVERYWHERE. Run the declaration-site command above. It prints nothing and exits 1. `grep -c '^order = ' docs/plans/agent-scaffold.plan.toml` prints `0` and exits 1. `grep -rn '\.order' src/ --include='*.rs'` prints nothing and exits 1. Note that `grep -c` exits 1 on a zero count, so none of the three can join an `&&` chain. MEASURED BEFORE THE CHANGE, the three print 12 rows, `105` and 5 rows, so each detects the condition rather than merely staying silent. The middle figure is the plan's step count on the day and it rises as the plan grows, so the outcome records what the command prints rather than this number.

2. THE BYTE-EXACT ORACLE. `./target/debug/agent-flow render --check docs/plans/agent-scaffold.plan.toml --strict` prints exactly `docs/plans/agent-scaffold.plan.toml: up to date` on stdout, prints nothing on stderr and exits 0. `docs/plans/agent-scaffold.md` is NOT hand-edited and NOT re-rendered, and `git diff --name-only` over the increment does not list it. That second half is the criterion, because a re-render of a changed projection also prints `up to date`.

3. RED THEN GREEN ON THE BLOCK MOVE. Move the `rename-to-agent-flow` block back to declaration position 84, run criterion 2's command, and record its stderr in the outcome. Restore the block to position 98 and show criterion 2 green again. MEASURED, the red output is exactly:

```
error: docs/plans/agent-scaffold.md differs from a fresh render (a hand-edit, or a stale render after a source edit) (first difference at line 261: expected "| `rename-to-agent-flow` | complete | blocked on `audit-user-prompt`; waived: st...", committed "| `drift-guard-test-hook-hygiene` | deferred |  |")
```

on stderr with exit 1 and nothing on stdout. The line number and the two quoted cells move as the plan grows. What the outcome records is that the message names `rename-to-agent-flow` as the expected row.

4. ALL THREE SELECTION ARMS TAKE THE FIRST DECLARED STEP. Build these three plans in a scratch directory OUTSIDE the repository. Each declares `zzz-first` before `aaa-second`, so declaration order and slug order disagree and a slug sort cannot pass by accident.

`arm1.plan.toml`, which exercises the in-progress arm:

```
[meta]
title = "Arm 1"
primary = "toml"

[[step]]
slug = "zzz-first"
title = "Declared first, sorts last"
status = "in-progress"

[[step]]
slug = "aaa-second"
title = "Declared second, sorts first"
status = "in-progress"
```

`arm2.plan.toml`, which exercises the ready-to-plan arm, is the same file with both statuses set to `not-started`.

`arm3.plan.toml`, which exercises the blocked arm:

```
[meta]
title = "Arm 3"
primary = "toml"

[[step]]
slug = "mmm-blocker"
title = "A deferred blocker, never complete"
status = "deferred"

[[step]]
slug = "zzz-first"
title = "Declared first, sorts last"
status = "not-started"
blocked_by = ["mmm-blocker"]

[[step]]
slug = "aaa-second"
title = "Declared second, sorts first"
status = "not-started"
blocked_by = ["mmm-blocker"]
```

Run one command per fixture. Each prints exactly `"step": "zzz-first"` on stdout and exits 0.

```
./target/debug/agent-flow next --source arm1.plan.toml --json | grep -o '"step": "[^"]*"'
```

```
./target/debug/agent-flow next --source arm2.plan.toml --json | grep -o '"step": "[^"]*"'
```

```
./target/debug/agent-flow next --source arm3.plan.toml --json | grep -o '"step": "[^"]*"'
```

The three commands are given once each rather than as one command with a substitution instruction, because the three fixtures are three different files and a reader who substitutes once proves one arm.

THIS CRITERION IS THE ONE THAT CATCHES THE MEASURED DEFECT. Against an implementation whose arms 2 and 3 take the LAST match, `cargo test` reports 0 failures, `cargo clippy --all-targets -- -D warnings` exits 0, `render --check --strict` exits 0 and `next` against the live plan prints `workflow-calibration`, which is the correct answer. Arms 2 and 3 then print `"step": "aaa-second"` here. The full measurement is WRONG IMPLEMENTATION A-2 in the specification rebuild.

5. THE THREE ARMS ARE PINNED IN THE SUITE, NOT ONLY IN A SCRATCH DIRECTORY. `src/next.rs` gains three unit tests, named `the_in_progress_arm_takes_the_first_declared_step`, `the_ready_to_plan_arm_takes_the_first_declared_step` and `the_blocked_arm_takes_the_first_declared_step`. Each builds at least TWO candidate steps through `test_step` and asserts the FIRST. A test with one candidate proves nothing, because first-match and last-match agree on a one-element slice, and every `select_active_loop` test in the file today has exactly one candidate per arm. Verify the count with `grep -c 'fn the_.*_arm_takes_the_first_declared_step' src/next.rs`, which prints `3`.

6. THE RENDER GOLDEN INVERTS THE PAIR IN BOTH PLACES. In `src/plan/testdata/render-fixture.md`, the `zeta` Roadmap row precedes the `epsilon` row, AND the `zeta` Step Details body precedes the `epsilon` body. Both halves are checked, because the Roadmap and the Step Details take their order from the same slice and a regression that fixes one and not the other is not reachable, so a criterion that reads one half reads half the guard.

```
awk '/^\| `zeta`/{z=NR} /^\| `epsilon`/{e=NR} /^### `zeta`/{zd=NR} /^### `epsilon`/{ed=NR} END{printf "roadmap zeta<epsilon=%d details zeta<epsilon=%d\n", (z<e), (zd<ed)}' src/plan/testdata/render-fixture.md
```

Pass: stdout is exactly `roadmap zeta<epsilon=1 details zeta<epsilon=1`. MEASURED BEFORE THE CHANGE it prints `roadmap zeta<epsilon=0 details zeta<epsilon=0`. An absent file prints `roadmap zeta<epsilon=1 details zeta<epsilon=1` from two zero comparisons, so pair this criterion with `test -s src/plan/testdata/render-fixture.md`, which must exit 0.

7. THE TEMPLATE PAIR STAYS BYTE-IDENTICAL. `cmp pack/plan-template.plan.toml docs/plans/TEMPLATE.plan.toml` prints nothing and exits 0. MEASURED, an implementation that updates the pack source and leaves the committed copy stale gives `cargo test` 0 failures, `render --check --strict` exit 0 and `validate` exit 0, and this `cmp` prints `pack/plan-template.plan.toml docs/plans/TEMPLATE.plan.toml differ: byte 1511, line 37` with exit 1.

8. THE CHANGED PATH SET IS THE 12 SEARCHED FILES PLUS THE FOUR GOLDEN AND FIXTURE FILES. `git diff --name-only` over the increment lists exactly:

```
docs/plans/TEMPLATE.plan.toml
docs/plans/agent-scaffold.plan.toml
pack/plan-template.plan.toml
src/next.rs
src/plan/render.rs
src/plan/source.rs
src/plan/testdata/render-fixture.md
src/plan/testdata/render-fixture.plan.toml
src/plan/testdata/render-fixture.steps/epsilon.md
src/plan/testdata/render-fixture.steps/zeta.md
src/plan/testdata/skeleton.plan.toml
src/workflow.rs
tests/metrics_and_ledger_anchor_to_the_plan_source.rs
tests/unsafe_pairings_are_refused_and_omitted.rs
tests/validate_toml_primary_skips_markdown_plan.rs
tests/validate_workflow_toml_source_needs_no_plan.rs
```

`docs/plans/agent-scaffold.md` must not appear, no file under `docs/plans/agent-scaffold.steps/` must appear, `pack/principles.toml` must not appear and `src/tui.rs` must not appear. The last two are named because a search on the bare string `order = ` reaches both and a whole-tree substitution damages both.

9. THE SUITE AND THE VALIDATORS STAY GREEN. `cargo test` passes. `cargo clippy --all-targets -- -D warnings` exits 0. `./target/debug/agent-flow validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl` prints a `docs/plans/agent-scaffold.plan.toml: <N> steps, 80 questions, valid` line on stdout and exits 0. `./target/debug/agent-flow validate --source docs/plans/agent-scaffold.plan.toml --workflow` prints `docs/plans/agent-scaffold.plan.toml vs docs/metrics/workflow.jsonl: workflow invariants hold` and exits 0. The `valid` line is pinned as well as the exit code, because `validate` exits 0 on a source that is not there, which `validate-missing-source-exit` fixes.

10. ASCII ONLY. `LC_ALL=C grep -cP '[^\t\x20-\x7e]' <file>` prints `0` for every changed file. Use that pattern rather than `[^ -~]`, which matches every hard tab. `grep -c` exits 1 when the count is 0, so it breaks an `&&` chain.

### Increment 2, `plan-order-array-position-inc2`: the prose currency pass

RISK CLASS `risky` (two consecutive clean review rounds). THE GROUND: the increment rewrites prose in the published plan document, and a missed site leaves a citation that resolves to nothing, or worse, to the wrong step, which is the same class of miss that produced the drift this step exists to remove. Criterion 2 is a mechanical oracle over the numbered citations, and criterion 3 is a bounded worklist that a reviewer disposes of row by row, so one half of the increment carries a reading. It ships nothing to a scaffolded project and it is reversible in a single revert, which argues the other way, and the reading half is what decides it.

SCOPE. Every numbered citation of a step in the step sidecars and in the front sidecars, plus the three front-sidecar sentences that name `order` as a Roadmap field. The ledger is NOT in this increment. The human decided on 2026-08-21 that the ledger's citations become their own step, `ledger-order-citation-currency`, receipt `q_id:"Q-78-ledgersplit"`, and criterion 6 records the exclusion and the count behind it.

THE TWO SPELLINGS, AND WHY THE NUMBER MATTERS. The rendered positions and the `order` values are two different quantities, because 84 and 91 are absent from the value range. A citation at or below 83 reads correctly as a position. A citation from 85 to 90 drifts by one. A citation at or above 92 drifts by two. So the citations at or above 85 are the drifting set, and the citations at or below 83 are safe as positions and stay on the worklist only as a recorded exemption.

The drift lives in both spellings. Do not search one.

ACCEPTANCE, EACH EXECUTABLE.

1. THE WORKLIST AND THE EXEMPTION LIST ARE CAPTURED BEFORE THE EDIT. Run these two commands against the pre-increment tree and write both outputs to a scratch file OUTSIDE the repository, or to a file the increment deletes before it commits.

```
grep -rnoE '\b(order|step) [0-9]+\b' docs/plans/agent-scaffold.steps/ docs/plans/agent-scaffold.success-criteria.md docs/plans/agent-scaffold.documentation-protocol.md docs/plans/agent-scaffold._status-narrative.md | awk -F: '{print $1"\t"$3}' | sort -u > pre.txt
```

```
awk -F'\t' '{n=$2; gsub(/[^0-9]/,"",n); if (n+0 <= 83) print}' pre.txt | sort -u > exempt.txt
```

The outcome records `wc -l` of both. MEASURED on the tree this file was written against, `pre.txt` holds 34 rows and `exempt.txt` holds 17. Those two numbers move as the plan grows and as the two withheld sidecars return, which is why the criterion pins the commands and not the numbers.

2. EVERY DRIFTING CITATION IS RESTATED BY SLUG, AND NONE IS RENUMBERED. After the edit, run:

```
grep -rnoE '\b(order|step) [0-9]+\b' docs/plans/agent-scaffold.steps/ docs/plans/agent-scaffold.success-criteria.md docs/plans/agent-scaffold.documentation-protocol.md docs/plans/agent-scaffold._status-narrative.md | awk -F: '{print $1"\t"$3}' | sort -u > post.txt
printf 'pre=%d exempt=%d post=%d unexplained=%d\n' "$(wc -l < pre.txt)" "$(wc -l < exempt.txt)" "$(wc -l < post.txt)" "$(comm -13 exempt.txt post.txt | wc -l)"
```

Pass: the printed line ends `unexplained=0`, AND `post` equals `exempt`, AND `pre` is greater than `exempt`. The oracle is the printed line and not an exit status. A tree with the sidecar directory missing prints `post=0`, which fails `post == exempt`, so an absent input cannot pass.

MEASURED, an implementation that RENUMBERS every citation at or above 85 rather than restating it by slug prints `unexplained=17`, and `comm -13 exempt.txt post.txt` lists all 17. A correct restatement prints `pre=34 exempt=17 post=17 unexplained=0`.

3. THE BARE-WORD WORKLIST IS DISPOSED OF ROW BY ROW. The two searches above find no citation that names `order` without a number, and three such sentences become false. Run:

```
grep -rnw 'order' docs/plans/agent-scaffold.success-criteria.md docs/plans/agent-scaffold.documentation-protocol.md docs/plans/agent-scaffold._status-narrative.md docs/plans/agent-scaffold.repo-layout.md docs/plans/agent-scaffold.roadmap-intro.md
```

This is NOT a pass-or-fail oracle and its empty output is not the target, because several matches are legitimate prose. It is a bounded worklist. MEASURED before the fix it prints 8 rows across 5 files. THE OBLIGATION: the outcome records, for every row this prints after the fix, either the correction made or the reason that match is legitimate. A row left with neither is the increment not finished. Three rows are known and are named so the implementer does not hunt for them:

- `docs/plans/agent-scaffold.success-criteria.md:20`, which lists the Roadmap as "(step status, order, dependencies)". Corrected.
- `docs/plans/agent-scaffold.documentation-protocol.md:7`, whose reprioritisation sentence needs restating. The same sentence's umbrella clause belongs to `Q-79` and stays.
- `docs/plans/agent-scaffold._status-narrative.md:1`, which sends the reader to the Roadmap "for per-step status and order". The Roadmap stays an ordered table with no order column, so this one is TRUE after the deletion and is recorded as unchanged. Its absence from the diff is a choice.

4. THE PROJECTION IS REGENERATED AND ITS DIFF IS ENUMERATED. `./target/debug/agent-flow render docs/plans/agent-scaffold.plan.toml` then `./target/debug/agent-flow render --check docs/plans/agent-scaffold.plan.toml --strict`, which prints `docs/plans/agent-scaffold.plan.toml: up to date` and exits 0. Unlike increment 1, `docs/plans/agent-scaffold.md` DOES appear in `git diff --name-only`, and the outcome records `git diff --numstat -- docs/plans/agent-scaffold.md`. That number must equal the sum of the sidecar numstats, because the rendered file inlines them verbatim. A larger number means a hand-edit of the generated file.

5. THE CHANGED PATH SET. `git diff --name-only` lists only files under `docs/plans/agent-scaffold.steps/`, the front sidecars named in criterion 3, and `docs/plans/agent-scaffold.md`. `docs/plans/agent-scaffold.plan.toml` does not appear, because no `status` flips and no `[[step]]` block moves in this increment. No file under `src/`, `tests/` or `pack/` appears. `docs/metrics/workflow.jsonl` does not appear.

6. THE LEDGER IS A NAMED EXCLUSION. The outcome records that `docs/plans/agent-scaffold.ledger.md` is out of scope and states the count that motivated the split, from:

```
grep -noE '\b(order|step) [0-9]+\b' docs/plans/agent-scaffold.ledger.md | awk -F: '{n=$NF; gsub(/[^0-9]/,"",n); if (n+0 >= 85) print}' | wc -l
```

MEASURED, that prints `96`. THAT FIGURE IS DATED AND THE OUTCOME MUST NOT COPY IT. The specification measured 96 against a 101-step tree. The same command against the tree this sidecar was spliced into prints 116, and the count rises with every appended review round, so the outcome records what the command prints on the day. THE SPLIT IS DECIDED, so the specification's alternative branch is spent: `ledger-order-citation-currency` owns the ledger and it does not return to this increment. Do not run the increment with the ledger half in.

7. THE SUITE, THE VALIDATORS AND ASCII. As increment 1 criteria 9 and 10. None of the three reads sidecar prose, so they are the no-regression check rather than the oracle. Criterion 2 is the oracle.

### NOT IN SCOPE, NAMED SO IT IS NOT DRAWN IN

- THE LEDGER'S `order` CITATIONS. `ledger-order-citation-currency` owns them, decided by the human on 2026-08-21 with receipt `q_id:"Q-78-ledgersplit"`. The ground is that `render` never inlines `docs/plans/agent-scaffold.ledger.md`, so increment 2's enumerated-diff oracle cannot reach them.
- TYPED UMBRELLA MEMBERSHIP. It left this step on 2026-08-21 and `Q-79` owns it. Nothing here waits on it, and nothing here is made harder by it.
- THE GENERATED STEP HEADING. `render` could own the `### <slug>: <title>` heading and every sidecar could lose its own. The design pass declines to schedule it, because it rewrites every sidecar and collides with the backfill in `step-intent-encoding`.
- THE SIDECAR STATUS OPENINGS. `sidecar-status-opening-drift` carries them, widened by the human on 2026-08-21 to every sidecar that opens with a status token.
- THE SIDECAR EXISTENCE CONTRACT. `render` treats a missing step or question sidecar as a hard failure, which is why every question sidecar is 0 bytes. That fix is its own step.
- THE `next` EXPLORATION-PHASE DEFECT, `Q-78` item (h). This increment leaves it exactly as it stands, because `workflow-calibration` sits at order 35 and at position 35 alike.
- THE TWO INTENT FIELDS. They belong to `step-intent-encoding`, which is BLOCKED BY this step.
