### `plan-order-array-position`: delete the `order` field so the `[[step]]` array position is the plan order (`Q-78-arrayorder`, decided 2026-08-21)

THIS STEP MUST NOT BUILD UNTIL THE `Q-78` REVIEW LOOP CONVERGES. The direction is decided: the human chose array position over an explicit slug list on 2026-08-21, receipt `type:"decision"` `q_id:"Q-78-arrayorder"` in `docs/metrics/workflow.jsonl`. What is not finished is the review the human directed on 2026-08-19, which runs on the design pass and on this sidecar before either enters the plan as the plan's answer. The design pass is `docs/plans/step-intent-encoding.explorations/Q-78.md`, which carries the reasoning, the rejected alternatives and the measurement appendix. This sidecar states what the step builds, in what order, and what each increment proves. It states no count of the plan's steps, because such a count expires and the plan's own standing cure, recorded in the ledger against orchestrator defect (12), is to carry the selecting command instead.

NO COMMIT SHA IS WRITTEN FOR THE RECEIPT AND THE REASON IS RECORDED. The receipt is named by `q_id`, which is stable. The commit that carries the receipt is the same commit that carries this paragraph, and the ledger already records what happens when a paragraph names the commit that writes it: the commit named is never the commit that carries the paragraph, because writing the paragraph moves `HEAD` past it. `q_id` has no such trap.

THIS STEP LOST ITS UMBRELLA HALF ON 2026-08-21, and the slug changed with it. The human split typed umbrella membership out of the `Q-78` pass into its own (`q_id:"Q-78-umbrellascope"`), so the third increment of the earlier draft left with it. `Q-79` owns that work and `docs/plans/umbrella-membership.explorations/Q-79.md` carries its evidence, its recommended form and the seven specification defects two review rounds found in it. This step is the `order` deletion and the prose sweep it forces, and nothing else.

THE PROBLEM. The plan carries the step order twice. `[[step]].order` states it as a number, and the declaration sequence of the `[[step]]` blocks states it as a position. The two agree today at every step except one, and a reprioritisation has to renumber both. The human ruled on 2026-08-19 that a numeric field is the wrong representation, because a reprioritisation renumbers many entries where a cut and paste of an entry does not.

THE APPROACH. Delete the number and keep the position.

THE INCREMENTS ARE DECLARED IN THE PLAN TOML as `[[step.increment]]` entries with their risk classes, so a round record joins to them structurally rather than by a lexical prefix (Principle 8, Structured data first). The classes are stated at authoring time because the plan's convention is that the declared class IS the loop-open classification, which `validation-constraints` follows for its own unbuilt increments. EACH CLASS STATES ITS GROUND, in the shape `test-tmpdir-repo-assumption.md` uses, because a class sets the required clean-round count and a class asserted without a ground is the defect this pass polices elsewhere (Principle 6, Ground decisions in evidence).

### Increment 1, delete `order` from the code and the schema

RISK CLASS `risky` (two consecutive clean review rounds). THE GROUND: the increment removes a field from the plan schema, so every previously valid plan in every scaffolded project fails to parse until edited, and it changes the sequencing rule that `render` and `next` both read. That is widely depended on and it is hard to roll back once a downstream plan is edited, which is the `AGENTS.md` test. It is the opposite of the plan's worked `low_risk` example at `test-tmpdir-repo-assumption.md`, which is confined to `#[cfg(test)]` code and ships nothing to a scaffolded project.

WHAT IT DOES. Remove `order` from the `Step` struct (`src/plan/source.rs:137`), from every `[[step]]` block, from the four TOML fixtures and from the inline TOML literals in the unit tests and the integration tests. Replace the sort at `src/plan/render.rs:177` with the declaration order. Remove `StepInfo.order` (`src/next.rs:527`), the assignments at `src/next.rs:540` and `:560`, and the `order` parameter of the `test_step` helper at `src/next.rs:1264`. Turn the three `min_by_key(order)` calls in `select_active_loop` (`src/next.rs:716`, `:723`, `:728`) into first-match searches over the slice. This increment changes NO prose. Increment 2 carries the prose.

THE ONE DATA MOVE THE MIGRATION OWES. `rename-to-agent-flow` stands 84th in the file and carries `order = 100`, which renders it 98th. Every other step's declaration position agrees with its rendered position. So that block moves to declaration position 98, and nothing else moves. Reproduce the exception with:

```
awk '/^slug = /{s=$3} /^order = /{sub(/order = /,""); if ($0+0 < p) print "out of place:", ps; p=$0+0; ps=s}' docs/plans/agent-scaffold.plan.toml
```

THE FULL CONSUMER SET IS IN THE DESIGN PASS, under the heading "The consumers, established by search", and it is enumerated there rather than repeated here. Two searches separate the two kinds of site: `grep -rn '\.order' src/ --include='*.rs'` finds the reads, and `grep -rn 'order = ' src/ tests/` finds the declarations. The reads are five sites in two files. The declarations reach `src/workflow.rs` (13 inline literals in unit tests), the unit tests of `src/plan/source.rs`, `src/plan/render.rs` and `src/next.rs`, four files under `tests/`, and the four TOML fixtures.

TWO OF THE FOUR FIXTURES ARE THE TWO SIDES OF ONE RENDERED PAIR, AND NO GUARD COVERS THE PAIR. `pack/pack.toml:39` maps `plan-template.plan.toml` to `docs/plans/TEMPLATE.plan.toml`, and the asset carries no `render = true`, so it is copied verbatim and the two files are byte-identical today. `src/agents_md_drift.rs` guards the root `AGENTS.md`, `.agents/AGENTS.reference.md` and rendered assets whose `dest` starts with `.agents/prompts/` or `.agents/user-prompts/`, and its own coverage block names "the `docs/plans/TEMPLATE` family" as UNGUARDED. `.agents/checks.toml` declares only `render-check`. So editing one side and not the other ships a pack source and a committed copy that disagree, silently. CRITERION 6 IS THE GUARD AND IT IS `cmp`, NOT `just scaffold-self`. The recipe's second command is `nix fmt`, which formats the whole tree, and this tree is not formatter-clean, so the recipe reformats files this increment did not intend and breaks criterion 2 of this same increment until the implementer re-renders. `cmp` tests the property directly, changes nothing and costs nothing.

THE RENDER GOLDEN AND THE TIE-BREAK TEST MOVE TOGETHER, and this is the one place where a careless reading loses a guard. `src/plan/testdata/render-fixture.plan.toml` declares `zeta` before `epsilon` and gives both `order = 5` deliberately, so that the slug tie-break puts `epsilon` first in the golden. Under array-position authority `zeta` comes first, so the golden's two rows SWAP and the test assertion INVERTS rather than merely losing its subject.

WHY THE FIELD IS DELETED RATHER THAN REPLACED BY A SLUG LIST. An explicit ordered list of slugs in `[meta]` moves one line per reprioritisation, against a whole `[[step]]` block. The design pass states the priced pair once, with its command, and this sidecar does not restate it. The design pass rejects the list under Principle 5, Make illegal states unrepresentable, because a list admits a duplicate entry, a missing entry and an entry that names no step, where an array admits none of the three, and under Principle 2, Minimal by default, because the deletion removes a field, a sort and three call sites where a list adds a field, a permutation rule and a lookup. The design pass also quotes the project's own earlier ruling: `docs/plans/structured-skeleton.explorations/design-A-minimal-schema.md:83` argued array position before the schema shipped, and `design-B-rich-schema.md:147` gave the counter-rationale that won, which is that reordering must be a field edit rather than a line move. The human's 2026-08-19 clarification reverses exactly that premise, and the human chose array position on 2026-08-21.

THE SUPPORTING MEASUREMENT. `steps_from_markdown` (`src/next.rs:560`) already derives the order from the table index, because the Markdown Roadmap carries no order field. The deletion makes the two substrates agree rather than diverge.

A STALE DOC COMMENT THIS INCREMENT ALSO FIXES, found while the above was measured. `src/plan/render.rs:462` describes the Roadmap table as "(slug, status, order)". The table emits slug, status and Notes, and it emitted no order column before this step existed.

ACCEPTANCE CRITERIA.

1. `grep -c '^order = ' docs/plans/agent-scaffold.plan.toml` exits 1 and prints 0. Note that `grep -c` exits 1 when the count is 0, so it breaks an `&&` chain.
2. `cargo run -- render --check --strict docs/plans/agent-scaffold.plan.toml` reports the projection up to date against the COMMITTED `docs/plans/agent-scaffold.md`, with that file UNCHANGED by this increment. This is the increment's oracle: `render` emits no order column, so a correct code-and-schema migration changes the projected document not at all.
3. `git diff --stat` over `docs/plans/agent-scaffold.md` reports no change, and `git diff --name-only` lists no file under `docs/plans/agent-scaffold.steps/`. The second half is what keeps the prose sweep out of this increment.
4. `cargo run -- next --source docs/plans/agent-scaffold.plan.toml` names `workflow-calibration`, state `awaiting-first-review`, `rounds 0/5`, which is the value it names before the increment. The expected value is written here so a reviewer arriving after the increment needs no pre-increment tree.
5. In `ordering_is_numeric_for_questions_and_slug_tiebroken_for_equal_order_steps` (`src/plan/render.rs:1126`), the STEP assertion goes or re-points at declaration order, and the QUESTION assertions and the status-bucket assertion STAY. The test guards three independent claims and only one loses its subject. The golden `src/plan/testdata/render-fixture.md` swaps its `epsilon` and `zeta` rows, and `render-fixture.steps/zeta.md` and `epsilon.md` lose the phrase "shares Roadmap order 5".
6. THE RENDERED PAIR STILL AGREES. `cmp pack/plan-template.plan.toml docs/plans/TEMPLATE.plan.toml` exits 0. Editing one side and not the other fails this criterion. Do NOT run `just scaffold-self` to satisfy it, for the reason stated above.
7. `cargo test` and `cargo clippy --all-targets -- -D warnings` exit 0.
8. `cargo run -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` reports the invariants hold.

### Increment 2, bring the prose that cites `order` up to date

RISK CLASS `risky` (two consecutive clean review rounds). THE GROUND: the increment rewrites prose in the published plan document, and its oracle is a worklist plus a reading rather than a test. A missed site leaves a citation that resolves to nothing, or worse, to the wrong step, and the same class of miss is what produced the drift this step exists to remove. It ships nothing to a scaffolded project and it is reversible in a single revert, which argues the other way, and the reading-based oracle is what decides it.

WHAT IT DOES. Correct every passage that names the deleted field. This increment's diff to `docs/plans/agent-scaffold.md` is EXPECTED and is reviewed, which is why it is separate from increment 1: `docs/plans/agent-scaffold.md` inlines every step sidecar and every front sidecar verbatim, so a prose fix and a byte-exact oracle cannot live in one commit.

THE SITES ARE ENUMERATED RATHER THAN GREPPED FOR, because a grep whose empty output is the target cannot go empty here. `order` is an ordinary English word, and this step's own sidecar stays in the directory after the step closes.

TWO SPELLINGS CITE A STEP BY ITS `order` VALUE, AND THE FIRST DRAFT SEARCHED ONE. The searches that built the list below are stated so the next reader extends the list rather than trusts it:

```
grep -rno "order [0-9]\+" docs/plans/agent-scaffold.steps/
grep -rnoE '\bstep [0-9]+\b' docs/plans/agent-scaffold.steps/
```

No third spelling was searched. `#<n>`, "position <n>" and a bare number in a sentence would all escape both, and nothing here claims they do not occur.

- `docs/plans/agent-scaffold.success-criteria.md:20`, which lists the Roadmap as "(step status, order, dependencies)".
- `docs/plans/agent-scaffold.documentation-protocol.md:7`, whose sentence "To add a step, add its detail block and insert its slug into the Roadmap at the right position; to reorder or reprioritise, edit the Roadmap rows" describes the old operation on BOTH halves. Restate the whole sentence, not the second clause alone: adding a step becomes a TOML array insert, and reprioritising becomes a block move. The SAME LINE also carries an umbrella clause, which belongs to `Q-79` and which this increment leaves exactly as it is.
- `docs/plans/agent-scaffold._status-narrative.md:1`, which sends the reader to the Roadmap "for per-step status and order". RECORDED AS DELIBERATELY UNCHANGED. The rendered Roadmap has no order column and never did, and it stays an ordered table after the deletion, so the sentence is imprecise today and no less true afterwards. It is listed so its absence from the edit set is a choice rather than a miss.
- Step sidecars that cite a step in the `order <n>` spelling: `decision-folder-currency.md`, `generated-projection.md`, `status-resume-ignores-json.md`, `test-tmpdir-repo-assumption.md`, `workflow-enforcement-tier.md`, and this file.
- `checks-runner-worktree-name-collision.md` matches the `order <n>` search and is a FALSE POSITIVE. Its only hit reads "so of order 1e-6 per pair", which cites no step and names no `order` value. It is listed so the implementer does not re-derive that, and it needs no edit for that hit. It DOES carry a real `step <n>` citation, below.
- Step sidecars that cite a step in the `step <n>` spelling: `checks-runner-worktree-name-collision.md`, `code-value-audit-static.md`, `decision-folder-currency.md`, `planner-folds-decisions.md`, `prompt-drift-guard.md`, `reviewer-reproducible-evidence.md`, `sidecar-status-opening-drift.md` and `workflow-enforcement-tier.md`. Five of those eight are on no `order <n>` list, and they hold the whole drifting population.
- `docs/plans/agent-scaffold.ledger.md`, which carries its own citations. The ledger is a historical record, so a citation there is left as written unless it states a LIVE rule.

WHAT NOT TO DO WITH THOSE CITATIONS, measured because the cheap route is wrong. The absent `order` values 84 and 91 mean a citation at or below 83 stays exactly correct when reread as a position, a citation between 85 and 90 drifts by one, and a citation at or above 92 drifts by two. So a silent reinterpretation leaves some citations right and some wrong. Each one is restated by SLUG, which is the identifier the project already prefers and which survives every future reorder.

ACCEPTANCE CRITERIA.

1. RED THEN GREEN ON ONE CITATION. Take one citation from the `step <n>` list, restate it by slug, then revert it and show that criterion 2 prints it. Restore it and show criterion 2 prints only the enumerated survivors. The red output lands as evidence in the outcome.
2. THE SEARCH RETURNS ONLY ENUMERATED SURVIVORS. Run:

```
grep -rnoE '\b(order|step) [0-9]+' docs/plans/agent-scaffold.steps/
```

Every remaining hit is listed in the outcome BY FILE AND LINE, with the reason it survives, and the permitted reasons are exactly two: a quotation of historical text, and the "of order 1e-6" false positive. A survivor for any other reason fails this criterion. The two front-sidecar paths an earlier draft put in this grep are dropped, because neither carries a digit after `order` and the pattern could never match them; criterion 3 covers them instead.
3. THE TWO FRONT SIDECARS ARE DISPOSED OF EXPLICITLY. `docs/plans/agent-scaffold.success-criteria.md` no longer lists `order` among the Roadmap's contents, and `docs/plans/agent-scaffold.documentation-protocol.md:7` no longer describes reprioritisation as a Roadmap-row edit. `docs/plans/agent-scaffold._status-narrative.md` is unchanged, and the outcome records that as the deliberate choice above.
4. THE CHANGED PATH SET IS THE WORKLIST PLUS THE PROJECTION. `git diff --name-only` lists `docs/plans/agent-scaffold.md`, the two front sidecars in criterion 3, and the step sidecars named on the two spelling lists that the implementer actually edited. No file under `src/`, `pack/` or `tests/` appears, and `docs/plans/agent-scaffold.plan.toml` does not appear.
5. `cargo run -- render --check --strict docs/plans/agent-scaffold.plan.toml` passes, and the reviewer reads the diff of `docs/plans/agent-scaffold.md`, which is expected to be non-empty.
6. ASCII ONLY. `LC_ALL=C grep -cP '[^\t\x20-\x7e]' <file>` prints 0 for every changed file. Use that pattern rather than `[^ -~]`, which matches every hard tab. Note `grep -c` exits 1 when the count is 0, so it breaks an `&&` chain.
7. `cargo test`, `cargo clippy --all-targets -- -D warnings` and `cargo run -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` exit 0.

### NOT IN SCOPE, NAMED SO IT IS NOT DRAWN IN

- TYPED UMBRELLA MEMBERSHIP. It left this step on 2026-08-21 and `Q-79` owns it. Nothing here waits on it, and nothing here is made harder by it.
- THE GENERATED STEP HEADING. `render` could own the `### <slug>: <title>` heading and every sidecar could lose its own. The design pass declines to schedule it, because it rewrites every sidecar and collides with the backfill in `step-intent-encoding`.
- THE SIDECAR STATUS OPENINGS. `sidecar-status-opening-drift` carries them, widened by the human on 2026-08-21 to every sidecar that opens with a status token.
- THE SIDECAR EXISTENCE CONTRACT. `render` treats a missing step or question sidecar as a hard failure, which is why every question sidecar is 0 bytes. That fix is its own step.
- THE `next` EXPLORATION-PHASE DEFECT, `Q-78` item (h). This increment leaves it exactly as it stands, because `workflow-calibration` sits at order 35 and at position 35 alike.
- THE TWO INTENT FIELDS. They belong to `step-intent-encoding`, which is BLOCKED BY this step.
