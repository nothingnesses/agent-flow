### `plan-order-array-position`: delete the `order` field so the `[[step]]` array position is the plan order (`Q-78-arrayorder`, decided 2026-08-21, pending the review)

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

RULE 5. THERE ARE TWO LINE COLLISIONS WITH `sidecar-status-opening-drift`, AND NEITHER IS WITH THE SIBLING STEP. Both concern the same sentence, and the second is the one an earlier draft missed.

THE FIRST COLLISION. The opening line of `docs/plans/agent-scaffold.steps/reviewer-reproducible-evidence.md` carries a numbered citation of `code-value-audit-static`, which increment 2 restates by slug, and the drift step's successor re-authors the leading token of that same line. The two edits touch different parts of one line. Whichever step runs second must leave the other's edit intact. That file sits on the drift step's HANDOVER list, so the drift step itself does not open it.

THE SECOND COLLISION. `docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md` QUOTES that same opening line verbatim, numbered citation included, in the borderline-case bullet criterion 2 of increment 2 names. That quotation is itself a row in this increment's drift set, and it is the one row a correct implementation leaves alone. See criterion 2 for the decision and its receipt.

AN EARLIER DRAFT NAMED THE SIBLING HERE AND THAT WAS FALSE, measured: `grep -rln 'reviewer-reproducible-evidence' docs/plans/agent-scaffold.steps/` returns four files and `step-intent-encoding.md` is not one of them.

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

THE PACK PROSE NO DECLARATION-SITE SEARCH REACHES, WHICH IS AN EDIT THIS INCREMENT OWES AND AN EARLIER FORM OF THIS SIDECAR OMITTED. The search above is anchored on a TOML assignment, and it is correct for what it searches: it returns the 12 files and the per-file counts tabulated above, and both were reproduced. The sentence below is PROSE, so no anchored search reaches it, and a path set derived from a search cannot contain what the search cannot match.

- `pack/AGENTS.md`, the phase 2 sentence reading "the `<task>.plan.toml` skeleton holds the Roadmap (`[[step]]` entries with status and order)". The `and order` clause goes. MEASURED OVER THE SHIPPED SURFACES, `grep -rln 'entries with status and order' pack/ AGENTS.md .agents/` returns exactly those three paths. The search is scoped rather than whole-tree because the whole-tree form also reaches the rendered plan, this sidecar and this pass's own review records, none of which is shipped and all of which quote the sentence in order to discuss it.
- `AGENTS.md` and `.agents/AGENTS.reference.md`, the two committed copies. `pack/pack.toml` copies `pack/AGENTS.md` to both destinations with `render = true`, so neither is a byte copy and rule 3's `cmp` does not apply to either. `the_committed_scaffold_matches_a_fresh_render` in `src/agents_md_drift.rs` pins them against a fresh render, so correcting the pack source alone fails `cargo test`, and so does correcting a committed copy alone. The three move together or the suite goes red.

WHY THIS BELONGS TO INCREMENT 1 AND NOT TO THE PROSE SWEEP. Increment 1 ships the deletion, and this increment's own risk ground is that "every previously valid plan in every scaffolded project fails to parse until edited" and that this is widely depended on. An implementation that satisfies every other criterion here ships, to every one of those projects, the instruction to write the field that now makes the plan fail to parse: the criteria would be blind to the consequence their own risk ground names. Increment 2 cannot carry it either, because its criterion 5 reads "No file under `src/`, `tests/` or `pack/` appears."

NO FILE UNDER `docs/plans/` OTHER THAN THE PLAN TOML CHANGES IN THIS INCREMENT. `docs/plans/agent-scaffold.md` in particular must not change, and criterion 2 is what proves it. `docs/plans/TEMPLATE.md` does not change either, and that is measured rather than assumed: `render` emits no order column and the template holds one step, so deleting `order` from `docs/plans/TEMPLATE.plan.toml` leaves that projection byte-identical.

THE ONE DATA MOVE THE MIGRATION OWES, REPRODUCED. Every step's declaration position agrees with its rendered position except `rename-to-agent-flow`. Reproduce the exception with:

```
awk '/^slug = /{s=$3} /^order = /{sub(/order = /,""); if ($0+0 < p) print "out of place:", ps; p=$0+0; ps=s}' docs/plans/agent-scaffold.plan.toml
```

WHY THE FIELD IS DELETED RATHER THAN REPLACED BY A SLUG LIST. An explicit ordered list of slugs in `[meta]` moves one line per reprioritisation, against a whole `[[step]]` block. The design pass states the priced pair once, with its command, and this sidecar does not restate it. The design pass rejects the list under Principle 5, Make illegal states unrepresentable, because a list admits a duplicate entry, a missing entry and an entry that names no step, where an array admits none of the three, and under Principle 2, Minimal by default, because the deletion removes a field, a sort and three call sites where a list adds a field, a permutation rule and a lookup. The design pass also quotes the project's own earlier ruling: `docs/plans/structured-skeleton.explorations/design-A-minimal-schema.md:83` argued array position before the schema shipped, and `design-B-rich-schema.md:147` gave the counter-rationale that won, which is that reordering must be a field edit rather than a line move. The human's 2026-08-19 clarification reverses exactly that premise, and the human chose array position on 2026-08-21.

THE SUPPORTING MEASUREMENT. `steps_from_markdown` (`src/next.rs:560`) already derives the order from the table index, because the Markdown Roadmap carries no order field. The deletion makes the two substrates agree rather than diverge.

ACCEPTANCE, EACH EXECUTABLE.

1. THE FIELD IS GONE FROM THE SCHEMA, SO A PLAN WRITTEN BEFORE THE DELETION FAILS TO PARSE. THIS IS THE EXECUTABLE FORM OF THE INCREMENT'S OWN RISK GROUND, and it is the only command in the increment that separates a deletion from a retention. Write this one-step plan to a scratch directory OUTSIDE the repository:

```
[meta]
title = "A plan written before the deletion"
primary = "toml"

[[step]]
slug = "a"
title = "A step"
status = "not-started"
order = 5
```

Then run `./target/debug/agent-flow validate --source old.plan.toml`. Pass: stderr carries ``unknown field `order` ``, stdout carries no `valid` line at all, and the exit status is 1. MEASURED BEFORE THE CHANGE, the same file prints `old.plan.toml: 1 steps, 0 questions, valid` on stdout and exits 0, and a plan carrying an unknown field on today's schema prints ``unknown field `bogus`, expected one of `slug`, `title`, `status`, `order`, `blocked_by`, `folds`, `provenance`, `increment`, `waiver` `` with exit 1, so the message shape is measured rather than predicted. WHY THIS COMMAND EXISTS: an implementation that keeps `order: u64` on `Step` under `#[serde(default)]`, and deletes every read, every site, the sort and the three `min_by_key` calls, passes every other criterion in this increment, and the risk ground above is false of it. That implementation was built and every other criterion was run against it.

Then the field is gone from every SITE. Run the declaration-site command above. Pass: it prints nothing ON STDOUT. Its exit status is NOT part of the pass condition, because a `for` loop over an empty command substitution exits 0. `grep -c '^order = ' docs/plans/agent-scaffold.plan.toml` prints `0` and exits 1, and `grep -rn '\.order' src/ --include='*.rs'` prints nothing and exits 1; for those two the exit status does hold. `grep -c 'slug, status, order' src/plan/render.rs` prints `0` and exits 1, which is the stale Roadmap doc comment this increment corrects. Note that `grep -c` exits 1 on a zero count, so none of them can join an `&&` chain. MEASURED BEFORE THE CHANGE, the four print 12 rows, `105`, 5 rows and `1`, so each detects the condition rather than merely staying silent. The `105` is the plan's step count on the day and it rises as the plan grows, so the outcome records what the command prints rather than this number.

2. THE BYTE-EXACT ORACLE. `./target/debug/agent-flow render --check docs/plans/agent-scaffold.plan.toml --strict` prints exactly `docs/plans/agent-scaffold.plan.toml: up to date` on stdout, prints nothing on stderr and exits 0. `docs/plans/agent-scaffold.md` is NOT hand-edited and NOT re-rendered, and `git diff --name-only` over the increment does not list it. That second half is the criterion, because a re-render of a changed projection also prints `up to date`.

3. RED THEN GREEN ON THE BLOCK MOVE. Move the `rename-to-agent-flow` block back to declaration position 84, run criterion 2's command, and record its stderr in the outcome. Restore the block to position 98 and show criterion 2 green again. MEASURED, the red output is exactly:

```
error: docs/plans/agent-scaffold.md differs from a fresh render (a hand-edit, or a stale render after a source edit) (first difference at line 261: expected "| `rename-to-agent-flow` | complete | blocked on `audit-user-prompt`; waived: st...", committed "| `drift-guard-test-hook-hygiene` | deferred |  |")
```

on stderr with exit 1 and nothing on stdout. The line number and the two quoted cells move as the plan grows. What the outcome records is that the message names `rename-to-agent-flow` as the expected row.

4. ALL THREE SELECTION ARMS TAKE THE FIRST DECLARED STEP. Build these three plans in a scratch directory OUTSIDE the repository. Each declares `zzz-first` before `aaa-second`, and gives `zzz-first` the title `Zulu, declared first` against `Alpha, declared second`. So declaration order disagrees with slug order AND with title order, and neither a slug sort nor a title sort can pass by accident. THE TITLES CARRY THAT SECOND HALF, which is why they read as they do: an earlier draft titled them `Declared first, sorts last` and `Declared second, sorts first`, and `printf 'Declared first, sorts last\nDeclared second, sorts first\n' | sort` returns them in declaration order, so the fixture cannot separate a title sort from a correct implementation and rule 1 claimed a coverage the fixture did not have.

`arm1.plan.toml`, which exercises the in-progress arm:

```
[meta]
title = "Arm 1"
primary = "toml"

[[step]]
slug = "zzz-first"
title = "Zulu, declared first"
status = "in-progress"

[[step]]
slug = "aaa-second"
title = "Alpha, declared second"
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
title = "Zulu, declared first"
status = "not-started"
blocked_by = ["mmm-blocker"]

[[step]]
slug = "aaa-second"
title = "Alpha, declared second"
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

5. THE THREE ARMS ARE PINNED IN THE SUITE, NOT ONLY IN A SCRATCH DIRECTORY. `src/next.rs` gains three unit tests, named `the_in_progress_arm_takes_the_first_declared_step`, `the_ready_to_plan_arm_takes_the_first_declared_step` and `the_blocked_arm_takes_the_first_declared_step`. Each builds at least TWO candidate steps through `test_step`, named `zzz-first` and `aaa-second` as in criterion 4, and asserts the FIRST. A test with one candidate proves nothing, because first-match and last-match agree on a one-element slice, and every `select_active_loop` test in the file today has exactly one candidate per arm.

THE GROUND SPLITS INTO A PREMISE AND A CONSEQUENCE, AND THE CRITERION RUNS AGAINST BOTH HALVES. THE PREMISE: each of the three tests builds at least two candidates, names them `zzz-first` and `aaa-second`, and asserts the FIRST. THE CONSEQUENCE: three functions with those names exist in `src/next.rs` and the file names both candidates. A grep set can only reach the consequence, so a RED measurement carries the premise.

THREE COMMANDS, BECAUSE THE NAME COUNT ALONE IS NOT AN ORACLE. Each is given once.

```
grep -c 'fn the_.*_arm_takes_the_first_declared_step' src/next.rs
```

```
grep -c 'zzz-first' src/next.rs
```

```
grep -c 'aaa-second' src/next.rs
```

Pass: the first prints `3`, and the second and third each print `3` or more. MEASURED, three correctly named no-op stub functions satisfy the first command on their own, which is why the other two exist.

THEN THE RED MEASUREMENT, WHICH IS PART OF THE CRITERION AND NOT A NOTE. Flip all three arms of `select_active_loop` from a first-match `find` to a last-match `rev().find`, run `cargo test --bin agent-flow arm_takes_the_first_declared_step`, and record the output in the outcome. Pass: ALL THREE named tests FAIL under the flip. Restore the arms and show the three green again. This is the shape criterion 3 already uses for the block move.

WHY THE RED MEASUREMENT IS THE HALF THAT CARRIES THE PREMISE, MEASURED ON TWO CONSTRUCTIONS THAT WERE BUILT, COMPILED AND RUN.

- THREE CORRECTLY NAMED ONE-CANDIDATE TESTS, each holding `zzz-first` alone. The first two commands print `3` and `6`, so both PASS. The third prints `0` and exits 1, so it FAILS. Under the flip the three tests print `test result: ok. 3 passed; 0 failed`, so the RED measurement also FAILS. By the criterion's own sentence that suite proves nothing, and it is exactly the state the paragraph above says the file is in today.
- THREE TWO-CANDIDATE TESTS THAT NAME BOTH SLUGS AND ASSERT ONLY `!step.is_empty()`. All three commands print `3`, so the whole grep set PASSES. Under the flip the three tests print `test result: ok. 3 passed; 0 failed`, so the RED measurement FAILS. This is the construction the third grep alone cannot reach.
- THE CONTROL, the implementation this criterion specifies. All three commands print `3` or more, and under the flip the run prints `test result: FAILED. 0 passed; 3 failed`, with `left: "aaa-second"` against `right: "zzz-first"` on each.

6. THE RENDER GOLDEN INVERTS THE PAIR IN BOTH PLACES. In `src/plan/testdata/render-fixture.md`, the `zeta` Roadmap row precedes the `epsilon` row, AND the `zeta` Step Details body precedes the `epsilon` body. Both halves are checked, because the Roadmap and the Step Details take their order from the same slice and a regression that fixes one and not the other is not reachable, so a criterion that reads one half reads half the guard.

```
awk '/^\| `zeta`/{z=NR} /^\| `epsilon`/{e=NR} /^### `zeta`/{zd=NR} /^### `epsilon`/{ed=NR} END{printf "zeta=%d epsilon=%d roadmap zeta<epsilon=%d details zeta<epsilon=%d\n", (z>0 && zd>0), (e>0 && ed>0), (z>0 && e>0 && z<e), (zd>0 && ed>0 && zd<ed)}' src/plan/testdata/render-fixture.md
```

Pass: stdout is exactly `zeta=1 epsilon=1 roadmap zeta<epsilon=1 details zeta<epsilon=1`. All four fields are the criterion, because the first two assert that the pair is still IN the fixture and the last two assert its order.

MEASURED BEFORE THE CHANGE it prints `zeta=1 epsilon=1 roadmap zeta<epsilon=0 details zeta<epsilon=0`. MEASURED on a fixture with every `zeta` line deleted it prints `zeta=0 epsilon=1 roadmap zeta<epsilon=0 details zeta<epsilon=0`. MEASURED on an empty file it prints all zeros. AN EARLIER FORM OF THIS COMMAND OMITTED THE FIRST TWO FIELDS, and on the deleted-pair fixture it printed `roadmap zeta<epsilon=1 details zeta<epsilon=1`, which is byte-identical to what a correct regeneration prints, so a fixture that had stopped exercising the tie-break passed. That form also stated that an absent file prints two ones; measured, `awk` on an absent file writes a fatal error to stderr and prints nothing, and an empty file prints two zeros, so the `test -s` pairing addressed a case that cannot arise and is dropped.

7. THE TEMPLATE PAIR STAYS BYTE-IDENTICAL. `cmp pack/plan-template.plan.toml docs/plans/TEMPLATE.plan.toml` prints nothing and exits 0. MEASURED, an implementation that updates the pack source and leaves the committed copy stale gives `cargo test` 0 failures, `render --check --strict` exit 0 and `validate` exit 0, and this `cmp` prints `pack/plan-template.plan.toml docs/plans/TEMPLATE.plan.toml differ: byte 1511, line 37` with exit 1.

8. THE CHANGED PATH SET IS THE 12 SEARCHED FILES, PLUS THE FOUR GOLDEN AND FIXTURE FILES, PLUS THE FOUR THE SEARCH CANNOT REACH. `git diff --name-only` over the increment lists exactly:

```
.agents/AGENTS.reference.md
AGENTS.md
CHANGELOG.md
docs/plans/TEMPLATE.plan.toml
docs/plans/agent-scaffold.plan.toml
pack/AGENTS.md
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

`docs/plans/agent-scaffold.md` must not appear, no file under `docs/plans/agent-scaffold.steps/` must appear, `docs/plans/TEMPLATE.md` must not appear, `pack/principles.toml` must not appear and `src/tui.rs` must not appear. The last two are named because a search on the bare string `order = ` reaches both and a whole-tree substitution damages both. `docs/plans/TEMPLATE.md` is named because the sibling step's increment 3 DOES have to re-render it and this one does not, for the reason recorded above.

THE FOUR PATHS THE SEARCH CANNOT REACH ARE NAMED HERE WITH THEIR REASONS, because this criterion reads as an exact enumeration: an implementer who made those edits under an earlier form of it FAILED the criterion, and one who obeyed it shipped the defect instead. `pack/AGENTS.md` carries the `and order` clause, and `AGENTS.md` and `.agents/AGENTS.reference.md` are its two committed renders, which the drift test pins. `CHANGELOG.md` carries the entry this step's DOCUMENTATION IMPACT owes. Every one of them is a file a CORRECT implementation must change, which is what makes the omission a defect in the criterion rather than in the implementation.

THE SHIPPED INSTRUCTION IS GONE, AND THIS IS A CONTENT CHECK RATHER THAN A PATH CHECK:

```
grep -rln 'entries with status and order' pack/ AGENTS.md .agents/
```

Pass: stdout is empty and the exit status is 1. MEASURED BEFORE THE CHANGE, the command prints exactly `pack/AGENTS.md`, `AGENTS.md` and `.agents/AGENTS.reference.md`. Criterion 8's path enumeration proves only that those files moved; this command proves that the stale clause did not ride through a mechanically green regeneration.

9. THE SUITE AND THE VALIDATORS STAY GREEN. `cargo test` passes. `cargo clippy --all-targets -- -D warnings` exits 0. `./target/debug/agent-flow validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl` prints a `docs/plans/agent-scaffold.plan.toml: <N> steps, <M> questions, valid` line on stdout and exits 0. The outcome records the complete line rather than pinning either changing count. `./target/debug/agent-flow validate --source docs/plans/agent-scaffold.plan.toml --workflow` prints `docs/plans/agent-scaffold.plan.toml vs docs/metrics/workflow.jsonl: workflow invariants hold` and exits 0. The `valid` line is pinned as well as the exit code, because `validate` exits 0 on a source that is not there, which `validate-missing-source-exit` fixes.

10. ASCII ONLY. `LC_ALL=C grep -cP '[^\t\x20-\x7e]' <file>` prints `0` for every changed file. Use that pattern rather than `[^ -~]`, which matches every hard tab. `grep -c` exits 1 when the count is 0, so it breaks an `&&` chain.

### Increment 2, `plan-order-array-position-inc2`: the prose currency pass

RISK CLASS `risky` (two consecutive clean review rounds). THE GROUND: the increment rewrites prose in the published plan document, and a missed site leaves a citation that resolves to nothing, or worse, to the wrong step, which is the same class of miss that produced the drift this step exists to remove. Criterion 2 is a mechanical oracle over the numbered citations, and criterion 3 is a bounded worklist that a reviewer disposes of row by row, so one half of the increment carries a reading. It ships nothing to a scaffolded project and it is reversible in a single revert, which argues the other way, and the reading half is what decides it.

SCOPE. Every numbered citation of a step in the step sidecars and in the front sidecars, plus the three front-sidecar sentences that name `order` as a Roadmap field. The ledger is NOT in this increment. The human decided on 2026-08-21 that the ledger's citations become their own step, `ledger-order-citation-currency`, receipt `q_id:"Q-78-ledgersplit"`, and criterion 6 records the exclusion and the count behind it.

THE TWO SPELLINGS, AND WHY THE NUMBER MATTERS. The rendered positions and the `order` values are two different quantities, because 84 and 91 are absent from the value range. A citation at or below 83 reads correctly as a position. A citation from 85 to 90 drifts by one. A citation at or above 92 drifts by two. So the citations at or above 85 are the drifting set, and the citations at or below 83 are safe as positions and stay on the worklist only as a recorded exemption.

The drift lives in both spellings and in both leading-word cases. Matching is intentionally case-insensitive: `order`, `Order`, `step` and `Step` are one citation class. Do not search one spelling or one case.

ACCEPTANCE, EACH EXECUTABLE.

1. THE WORKLIST, THE EXEMPTION LIST AND THE RESOLUTION TABLE ARE CAPTURED BEFORE THE EDIT. Run these against the pre-increment tree and write every output to a scratch directory OUTSIDE the repository, or to files the increment deletes before it commits.

```
grep -rnoE '\b([Oo]rder|[Ss]tep) [0-9]+\b' docs/plans/agent-scaffold.steps/ docs/plans/agent-scaffold.success-criteria.md docs/plans/agent-scaffold.documentation-protocol.md docs/plans/agent-scaffold._status-narrative.md | awk -F: '{print $1"\t"$2"\t"$3}' | sort -u > pre.txt
```

```
awk -F'\t' '{n=$3; gsub(/[^0-9]/,"",n); if (n+0 <= 83) print}' pre.txt | sort -u > exempt.txt
awk -F'\t' '{n=$3; gsub(/[^0-9]/,"",n); if (n+0 == 84) print}' pre.txt | sort -u > eighty-four.txt
awk -F'\t' '{n=$3; gsub(/[^0-9]/,"",n); if (n+0 >= 85) print}' pre.txt | sort -u > drift.txt
```

```
git show <pre-deletion-commit>:docs/plans/agent-scaffold.plan.toml | awk '/^slug = /{s=$3} /^order = /{sub(/order = /,""); print $0"\t"s}' | tr -d '"' | sort -n > order-to-slug.tsv
```

`<pre-deletion-commit>` is a named commit recorded in the outcome and containing the `order` field before increment 1 deletes it. The working tree is NOT a permitted table source: increment 2 always runs after increment 1, so a working-tree table is empty and forces the implementer to invent a mapping. The named commit makes the table independent of increment order and preserves the pre-deletion order-to-slug relation that this criterion exists to check (Principle 7, Reproducible).

A ROW IS A PATH, A LINE NUMBER AND A CITATION, and the line number is load-carrying, because criterion 2 reads the line back at that number. An earlier form of this command dropped the line number, so three citations on one line collapsed into one row and the worklist was short by the surplus.

THE WORKLIST COUNTS LINES AND NOT SITES, AND THAT IS AN ACCEPTED RESIDUAL RATHER THAN A REPAIR. `sort -u` still collapses the SAME citation repeated on one line, which the line number cannot separate. The sibling step drops `sort -u` for exactly this case (`ledger-order-citation-currency.md`, criterion 1). Reproduce the surplus and record it in the outcome, so a line that needs several edits and shows up once is not a surprise:

```
raw=$(grep -rnoE '\b([Oo]rder|[Ss]tep) [0-9]+\b' docs/plans/agent-scaffold.steps/ docs/plans/agent-scaffold.success-criteria.md docs/plans/agent-scaffold.documentation-protocol.md docs/plans/agent-scaffold._status-narrative.md | awk -F: '{print $1"\t"$2"\t"$3}' | awk -F'\t' '{n=$3; gsub(/[^0-9]/,"",n); if (n+0 >= 85) print}' | wc -l)
printf 'raw_sites=%d worklist_rows=%d surplus=%d\n' "$raw" "$(wc -l < drift.txt)" "$((raw - $(wc -l < drift.txt)))"
```

The human accepted this on 2026-08-21 as residual risk, receipt `type:"decision"` `q_id:"Q-78-residuals"` in `docs/metrics/workflow.jsonl`. THE CONSEQUENCE THE HUMAN WEIGHED: nothing wrong can ship, because P1 computes `actual` over the WHOLE line, so a line with one of several occurrences removed still reports `NUMBER SURVIVES`. MEASURED by construction, removing one of two repeated occurrences from a line leaves P1 printing that line as `NUMBER SURVIVES`, and only removing both moves it to `restated`. The cost accepted is a worklist that understates the work by the surplus the command above prints.

Capture the line count of every file the worklist names as well, so criterion 2 can prove those line numbers still resolve:

```
cut -f1 pre.txt | sort -u | while IFS= read -r f; do printf '%s\t%s\n' "$(wc -l < "$f")" "$f"; done > lines-pre.txt
```

The outcome records `wc -l` of `pre.txt`, `exempt.txt`, `eighty-four.txt` and `drift.txt`, and the resolution table's own `wc -l`. NO ROW COUNT IS WRITTEN INTO THIS CRITERION, AND THE REASON IS MEASURED RATHER THAN CAUTIONARY. This search set includes `docs/plans/agent-scaffold.steps/`, which holds this sidecar and its four siblings, so every edit to a `Q-78` sidecar moves the figures this criterion would state. An earlier form stated three counts as a measurement on "the tree this file was spliced into", and the very fix pass that edited these criteria moved all three of them. A specification whose search set contains itself cannot state a snapshot that survives its own edit. The relation that holds is `pre` equals the disjoint union of `exempt`, `eighty-four` and `drift`, and criterion 2's pass condition is stated against `wc -l < drift.txt` rather than against any number.

NO CONCRETE VALUE-AND-SLUG PAIR IS WRITTEN INTO THIS SIDECAR AS AN EXAMPLE, WHICH IS A RULE AND NOT A PREFERENCE. A concrete pair here is itself a numbered citation inside this increment's own search set, so writing one adds a row to the worklist that the increment then owes. This is the rule `ledger-order-citation-currency.md` states for itself, adopted here for the same reason.

2. EVERY DRIFTING CITATION IS RESTATED BY THE SLUG ITS `order` VALUE RESOLVES TO, AND THE NUMBER GOES. Run this under bash from the repository root. It uses no process substitution, so it needs no `bash -c` wrapper, but it does need bash rather than nu.

```
#!/usr/bin/env bash
# P1: the number goes, the right slug arrives, and the exempt citations on the same line survive.
PRE="$1"; DRIFT="$2"; TABLE="$3"
rows=0; restated=0; wrong=0; residual=0
while IFS=$'\t' read -r path lineno cit; do
  rows=$((rows+1))
  n=${cit##* }
  want=$(awk -F'\t' -v n="$n" '$1==n {print $2}' "$TABLE")
  line=$(sed -n "${lineno}p" "$path")
  expect=$(awk -F'\t' -v p="$path" -v l="$lineno" '$1==p && $2==l {n=$3; gsub(/[^0-9]/,"",n); if (n+0 <= 83) print $3}' "$PRE" | sort)
  actual=$(printf '%s' "$line" | grep -oE '\b([Oo]rder|[Ss]tep) [0-9]+\b' | sort)
  if [ "$expect" != "$actual" ]; then
    echo "NUMBER SURVIVES $path:$lineno (was $cit)"; residual=$((residual+1)); continue
  fi
  if printf '%s' "$line" | grep -qF -- "\`$want\`"; then
    restated=$((restated+1))
  else
    echo "WRONG SLUG $path:$lineno (was $cit) wants \`$want\`"; wrong=$((wrong+1))
  fi
done < "$DRIFT"
printf 'rows=%d restated=%d wrong_slug=%d number_survives=%d\n' "$rows" "$restated" "$wrong" "$residual"
```

Pass, all four clauses: `rows` equals `wc -l < drift.txt`; `wrong_slug=0`; `restated` equals `rows` MINUS `E`; and `number_survives` EQUALS `E`. `E` is the count of `NUMBER SURVIVES` rows the outcome enumerates as verbatim quotations of another file's text whose restatement would falsify the quotation, and every such row is enumerated that way, and a row left without that is the increment not finished. The oracle is the printed line and not an exit status.

THE LAST TWO CLAUSES ARE THE ONLY DISCRIMINATING ONES, AND AN EARLIER FORM CARRIED NEITHER. It read "`restated` plus the count of `NUMBER SURVIVES` rows equals `rows`". That is an IDENTITY OF THE LOOP and not a condition: every row takes exactly one of three exits, so `rows = restated + wrong + residual` holds on every tree whatever the implementation did, and once `wrong_slug=0` is required that clause is `wrong_slug=0` restated. The first clause is an identity too, because the loop increments `rows` once per line of `drift.txt`. MEASURED, AN UNTOUCHED TREE AND A RENUMBERED TREE BOTH PRINT A BYTE-IDENTICAL `restated=0 wrong_slug=0` LINE WITH `number_survives` EQUAL TO `rows`, and both satisfied all three of the earlier clauses. A renumbering cannot escape the residual arm in either direction, because `expect` holds only the citations at or below 83 on the line and `actual` holds every citation still on it, so any surviving number sends the row to `NUMBER SURVIVES`. RULE 4 is a numbered RULE, it cites Principle 8 by name, and its own last sentence reads "Criterion 2 of increment 2 detects a renumbering", which the earlier pass condition did not; this increment's ground says criterion 2 is the mechanical oracle and criterion 3 is the reading, and under that form BOTH halves carried a reading. The two equalities above are this criterion's own MEASURED table's line for a correct implementation, and moving them into the Pass clause is the whole of the repair. THE BACKSTOP THAT ALREADY WORKED IS UNCHANGED AND IS NOT THE FIX: the obligation to enumerate every `NUMBER SURVIVES` row refuses both trees for an implementer who discharges it, and what failed was the pass condition and the ground's claim about which half is mechanical.

EXACTLY ONE SUCH ROW EXISTS TODAY AND IT IS NAMED, so a correct implementation prints `number_survives=1` rather than `0`. THE ROW is the borderline-case bullet in `docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md` that quotes the opening line of `docs/plans/agent-scaffold.steps/reviewer-reproducible-evidence.md`. Find it with:

```
grep -n 'opens "Next (built first' docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md
```

NO LINE NUMBER IS WRITTEN HERE, because that file sits inside this increment's own search set and every edit to it moves the number. The quotation carries the numbered citation, and the sentence after it states in its own words that the number is a citation by `order` value, so a restatement strands that sentence as well as falsifying the quotation.

THE HUMAN DECIDED THIS ON 2026-08-21, over a restatement by slug, receipt `type:"decision"` `q_id:"Q-78-quotationrow"` in `docs/metrics/workflow.jsonl`. THE REASONING ACCEPTED, cited by name: Principle 8, Structured data first, project for humans. A restatement makes the quotation stop matching the text it quotes, and `render` publishes both files. The exception applies whether the quoted leading word is lower-case or capitalized: case does not turn a verbatim quotation into live prose. `reviewer-reproducible-evidence` also sits on the drift step's HANDOVER list, so its opening gets re-authored by the successor step in any case. AN EARLIER FORM OF THIS PARAGRAPH SAID NO SUCH ROW EXISTS and directed a correct implementation to print `number_survives=0`. That sentence was false on every tree this file has sat on, and its guidance clause pointed the implementer at the destructive route.

Then prove the line numbers still resolved, and that the edit disturbed no exempt citation and created no new drifting one:

```
cut -f1 pre.txt | sort -u | while IFS= read -r f; do printf '%s\t%s\n' "$(wc -l < "$f")" "$f"; done | diff - lines-pre.txt
grep -rnoE '\b([Oo]rder|[Ss]tep) [0-9]+\b' docs/plans/agent-scaffold.steps/ docs/plans/agent-scaffold.success-criteria.md docs/plans/agent-scaffold.documentation-protocol.md docs/plans/agent-scaffold._status-narrative.md | awk -F: '{print $1"\t"$2"\t"$3}' | sort -u > post.txt
printf 'post=%d exempt_lost=%d eighty_four_lost=%d\n' \
  "$(wc -l < post.txt)" \
  "$(comm -13 post.txt exempt.txt | wc -l)" \
  "$(comm -13 post.txt eighty-four.txt | wc -l)"
```

Pass: the `diff` prints nothing and exits 0, `exempt_lost=0`, `eighty_four_lost=0`, and `post` equals `wc -l < exempt.txt` plus `wc -l < eighty-four.txt` plus the enumerated `NUMBER SURVIVES` rows. The 84 rows are neither exempt nor drifting and intentionally survive, so omitting their captured term refuses a correct implementation. A tree with the sidecar directory missing gives `post=0` and `exempt_lost` equal to the whole exemption list, so an absent input cannot pass.

MEASURED, five trees against P1, each built on a copy of the sidecar tree. EVERY ROW BELOW IS A RELATION AND NOT A ROW COUNT. Write `R` for `wc -l < drift.txt`, `H` for `wc -l < eighty-four.txt`, and `E` for the count of enumerated quotation rows, which is one today. `H` contributes to the post-sweep relation and not to P1, whose input is `drift.txt`. AN EARLIER FORM KEYED ALL FIVE TREES TO A LITERAL ROW COUNT, and the fix pass that edited these criteria moved that count while it edited them, because this increment's search set holds this sidecar and its four siblings.

- The untouched tree prints `rows=R restated=0 wrong_slug=0 number_survives=R`.
- A CORRECT IMPLEMENTATION prints `rows=R restated=R-E wrong_slug=0 number_survives=E`.
- An implementation that DELETES every drifting citation, replacing it with the bare words `that step`, prints `number_survives=0` and `wrong_slug` GREATER THAN ZERO. A deleted number leaves the line carrying no `order` citation, so it clears the first test, and every line that did not already name the step then carries no slug.
- An implementation that RENUMBERS every drifting citation prints `restated=0 wrong_slug=0 number_survives=R`, which is the untouched tree's own line. That is why the pass condition reads `restated` rather than a before-and-after diff.
- An implementation that restates every one by a REAL BUT WRONG slug prints `number_survives=0` and `wrong_slug` GREATER THAN ZERO.

CAPITALIZED RED CONTROL. In a throwaway copy of a correct implementation, restore one captured capitalized `Order` or `Step` citation at or above 85 on a non-quotation row, removing its slug restatement. Run P1 and the post sweep. Pass for the red control: P1 reports that row as `NUMBER SURVIVES` and the post sweep grows by one beyond the required `exempt + eighty-four + E` relation. Restore the slug restatement and show both relations passing again. A lower-case-only pre-capture or `actual` recomputation leaves the mutation invisible and fails this control.

THE DELETION IS WHY THIS CRITERION READS THE LINE BACK. An earlier form counted rows before and after and required the drifting rows to be gone, and the deletion satisfied every clause of it while it destroyed cross-references across the sidecar tree, all of which `render` ships into every reader's copy of the plan. NO COUNT OF DESTROYED REFERENCES IS WRITTEN HERE, for the reason criterion 1 records. THE WRONG-SLUG CASE IS WHY THE RESOLUTION TABLE EXISTS: it is the "or worse, to the wrong step" half of this increment's own risk ground, and nothing that reads only the shape of the line can reach it.

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
grep -noE '\b([Oo]rder|[Ss]tep) [0-9]+\b' docs/plans/agent-scaffold.ledger.md | awk -F: '{n=$NF; gsub(/[^0-9]/,"",n); if (n+0 >= 85) print}' | wc -l
```

NO COUNT IS WRITTEN HERE AND THE OUTCOME RECORDS WHAT THE COMMAND PRINTS ON THE DAY. The count rises with every appended review round, and the ledger paragraph that motivated the split states the figure the human weighed, dated. THE SPLIT IS DECIDED, so the specification's alternative branch is spent: `ledger-order-citation-currency` owns the ledger and it does not return to this increment. Do not run the increment with the ledger half in.

7. THE SUITE, THE VALIDATORS AND ASCII. As increment 1 criteria 9 and 10. None of the three reads sidecar prose, so they are the no-regression check rather than the oracle. Criterion 2 is the oracle.

### DOCUMENTATION IMPACT

`CHANGELOG.md`, THE `## [Unreleased]` SECTION, WHICH INCREMENT 1 OPENS. `grep -n 'Unreleased' CHANGELOG.md` exits 1 today, so the entry means opening the section rather than appending to one. It records that `[[step]].order` is DELETED, that the array position of a `[[step]]` block is now the plan order, and that a plan written against an earlier version does not parse until every `order = ` line is removed. The entry belongs to increment 1, which ships the schema deletion, and not to increment 2, whose criterion 5 admits no file outside `docs/plans/`. `AGENTS.md` states this duty in this repository's own copy and in the shipped pack copy alike, and `validation-constraints.md` already names `CHANGELOG.md` and its `## [Unreleased]` section for a comparable pending step, which is the shape this section follows. `CHANGELOG.md` is in increment 1 criterion 8's path set for that reason.

ACCEPTED RESIDUAL `F3` (`low`), OWNED BY INCREMENT 1 CRITERION 8 AND THIS DOCUMENTATION-IMPACT DUTY, AND RECORDED AGAIN BESIDE THE OTHER OWNER IN `step-intent-encoding` INCREMENT 3. The human accepted the cost that both schema-breaking increments currently say they open `## [Unreleased]`, although the declared dependency means this increment runs first and the later one must append to the section this one leaves. A literal implementation of both instructions can duplicate the heading or clobber the first entry, and neither increment has a content check for that collision. THE NON-EXPANSION BOUNDARY: this accepts only the sequencing ambiguity between these two already-declared documentation duties; it does not permit duplicate headings generally, does not waive either changelog entry, and does not change either increment's changed-path set. The acceptance is decision `Q-78-round4-low-residuals`, as revised by `Q-78-gb11-revision` to retain four residuals.

THE SHIPPED PACK PROSE IS A FILE EDIT AND NOT A NOTE, so it is stated in increment 1's own path set rather than deferred to here: `pack/AGENTS.md` loses the `and order` clause and its two committed renders move with it, for the reasons that block records.

`README.md` IS NOT MADE STALE, MEASURED. Its one description of the plan source names the Roadmap `[[step]]` entries and lists no field of them, and its other matches on the word `order` are about principle ordering, module declaration order and token de-duplication. Its absence from the path set is a choice.

### NOT IN SCOPE, NAMED SO IT IS NOT DRAWN IN

- THE LEDGER'S `order` CITATIONS. `ledger-order-citation-currency` owns them, decided by the human on 2026-08-21 with receipt `q_id:"Q-78-ledgersplit"`. The ground is that `render` never inlines `docs/plans/agent-scaffold.ledger.md`, so increment 2's enumerated-diff oracle cannot reach them.
- `structured-skeleton.md:7`, THE ONE STEP SIDECAR THAT NAMES `order` AS A SCHEMA FIELD RATHER THAN CITING A STEP BY IT. Find it with `grep -rl '`order`' docs/plans/agent-scaffold.steps/`, which returns five files, four of them the `Q-78` sidecars. The fifth is `structured-skeleton.md`, whose increment 1 bullet records the schema that increment DELIVERED and names its merge commit `27bd647`. THE GROUND FOR EXCLUDING IT IS THAT IT IS FROZEN HISTORY, the same ground the ledger's own frozen blocks carry: the increment did ship `order`, a reader can resolve that schema at the named commit, and correcting the sentence would rewrite an outcome record to describe a state it never delivered. It is named here so its absence is a choice, because it escapes all three of increment 2's instruments: criterion 2's regex needs a number after the word and there is none, criterion 3's search runs over the five front sidecars only, and criterion 5's changed-path set would reject a fix that reached it.
- TYPED UMBRELLA MEMBERSHIP. It left this step on 2026-08-21 and `Q-79` owns it. Nothing here waits on it, and nothing here is made harder by it.
- THE GENERATED STEP HEADING. `render` could own the `### <slug>: <title>` heading and every sidecar could lose its own. The design pass declines to schedule it, because it rewrites every sidecar and collides with the backfill in `step-intent-encoding`.
- THE SIDECAR STATUS OPENINGS. `sidecar-status-opening-drift` carries them, widened by the human on 2026-08-21 to every sidecar that opens with a status token.
- THE SIDECAR EXISTENCE CONTRACT. `render` treats a missing step or question sidecar as a hard failure, so question sidecars must exist and most are empty. Reproduce the current non-empty set with `find docs/plans/agent-scaffold.questions -type f -size +0`, and treat its path output rather than a count as the sole authority for that set. That fix is its own step.
- THE `next` EXPLORATION-PHASE DEFECT, `Q-78` item (h). This increment leaves it exactly as it stands, because `workflow-calibration` sits at order 35 and at position 35 alike.
- THE TWO INTENT FIELDS. They belong to `step-intent-encoding`, which is BLOCKED BY this step.
