### `plan-order-and-umbrella-structure`: delete the `order` field so the `[[step]]` array position is the plan order, and make umbrella membership typed data (`Q-78`, pending review and a human decision)

THIS STEP IS CONDITIONAL AND MUST NOT BUILD YET. `Q-78` is `open`, not `decided`. The human directed on 2026-08-19 that reviewers review the design pass before its outcome enters the plan as the plan's answer, and one of the items this step depends on goes to the human as a choice. The design pass is `docs/plans/step-intent-encoding.explorations/Q-78.md`, which carries the full reasoning, the rejected alternatives and the measurement appendix. This sidecar states what the step builds, in what order, and what each increment proves. It states no count of the plan's steps, because such a count expires and the plan's own standing cure, recorded in the ledger against orchestrator defect (12), is to carry the selecting command instead.

THE PROBLEM. The plan carries the step order twice. `[[step]].order` states it as a number, and the declaration sequence of the `[[step]]` blocks states it as a position. The two agree today at every step except one, and a reprioritisation has to renumber both. The human ruled on 2026-08-19 that a numeric field is the wrong representation, because a reprioritisation renumbers many entries where a cut and paste of an entry does not. Separately, the plan expresses umbrella grouping as prose that asserts position, and three of those positional assertions are already false.

THE APPROACH. Delete the number and keep the position. Then turn the umbrella from a paragraph that claims adjacency into typed data, and let `render` state the grouping from that data.

THE INCREMENTS ARE DECLARED IN THE PLAN TOML as `[[step.increment]]` entries with their risk classes, so a round record joins to them structurally rather than by a lexical prefix (Principle 8, Structured data first). The classes are stated at authoring time because the plan's convention is that the declared class IS the loop-open classification, which `validation-constraints` follows for its own unbuilt increments.

### Increment 1, delete `order` from the code and the schema

WHAT IT DOES. Remove `order` from the `Step` struct (`src/plan/source.rs:137`), from every `[[step]]` block, from the four TOML fixtures and from the inline TOML literals in the unit tests and the integration tests. Replace the sort at `src/plan/render.rs:177` with the declaration order. Remove `StepInfo.order` (`src/next.rs:527`), the assignments at `src/next.rs:540` and `:560`, and the `order` parameter of the `test_step` helper at `src/next.rs:1264`. Turn the three `min_by_key(order)` calls in `select_active_loop` (`src/next.rs:716`, `:723`, `:728`) into first-match searches over the slice. This increment changes NO prose. Increment 2 carries the prose.

THE ONE DATA MOVE THE MIGRATION OWES. `rename-to-agent-flow` stands 84th in the file and carries `order = 100`, which renders it 98th. Every other step's declaration position agrees with its rendered position. So that block moves to declaration position 98, and nothing else moves. Reproduce the exception with:

```
awk '/^slug = /{s=$3} /^order = /{sub(/order = /,""); if ($0+0 < p) print "out of place:", ps; p=$0+0; ps=s}' docs/plans/agent-scaffold.plan.toml
```

THE FULL CONSUMER SET IS IN THE DESIGN PASS, section 9, and it is enumerated there rather than repeated here. Two searches separate the two kinds of site: `grep -rn '\.order' src/ --include='*.rs'` finds the reads, and `grep -rn 'order = ' src/ tests/` finds the declarations. The reads are five sites in two files. The declarations reach `src/workflow.rs` (13 inline literals in unit tests), the unit tests of `src/plan/source.rs`, `src/plan/render.rs` and `src/next.rs`, four files under `tests/`, and the four TOML fixtures.

THE RENDER GOLDEN AND THE TIE-BREAK TEST MOVE TOGETHER, and this is the one place where a careless reading loses a guard. `src/plan/testdata/render-fixture.plan.toml` declares `zeta` before `epsilon` and gives both `order = 5` deliberately, so that the slug tie-break puts `epsilon` first in the golden. Under array-position authority `zeta` comes first, so the golden's two rows SWAP and the test assertion INVERTS rather than merely losing its subject.

WHY THE FIELD IS DELETED RATHER THAN REPLACED BY A SLUG LIST, and the note that the human owns this. An explicit ordered list of slugs in `[meta]` moves one line per reprioritisation, against a block of median 13 lines here and 89 in the worst case. It is rejected in the design pass under Principle 5, Make illegal states unrepresentable, because a list admits a duplicate entry, a missing entry and an entry that names no step, where an array admits none of the three, and under Principle 2, Minimal by default, because the deletion removes a field, a sort and three call sites where a list adds a field, a permutation rule and a lookup. The design pass also quotes the project's own earlier ruling: `docs/plans/structured-skeleton.explorations/design-A-minimal-schema.md:83` argued array position before the schema shipped, and `design-B-rich-schema.md:147` gave the counter-rationale that won, which is that reordering must be a field edit rather than a line move. The human's 2026-08-19 clarification reverses exactly that premise. THE HUMAN HAS NOT CHOSEN BETWEEN THE TWO. Do not start this increment until the human does.

THE SUPPORTING MEASUREMENT. `steps_from_markdown` (`src/next.rs:560`) already derives the order from the table index, because the Markdown Roadmap carries no order field. The deletion makes the two substrates agree rather than diverge.

A STALE DOC COMMENT THIS INCREMENT ALSO FIXES, found while the above was measured. `src/plan/render.rs:462` describes the Roadmap table as "(slug, status, order)". The table emits slug, status and Notes, and it emitted no order column before this step existed.

ACCEPTANCE CRITERIA.

1. `grep -c '^order = ' docs/plans/agent-scaffold.plan.toml` exits 1 and prints 0.
2. `cargo run -- render --check --strict docs/plans/agent-scaffold.plan.toml` reports the projection up to date against the COMMITTED `docs/plans/agent-scaffold.md`, with that file UNCHANGED by this increment. This is the increment's oracle: `render` emits no order column, so a correct code-and-schema migration changes the projected document not at all.
3. `git diff --stat` over `docs/plans/agent-scaffold.md` reports no change, and `git diff --name-only` lists no file under `docs/plans/agent-scaffold.steps/`. The second half is what keeps the prose sweep out of this increment.
4. `cargo run -- next --source docs/plans/agent-scaffold.plan.toml` names the same active loop as it named before the increment.
5. In `ordering_is_numeric_for_questions_and_slug_tiebroken_for_equal_order_steps` (`src/plan/render.rs:1126`), the STEP assertion goes or re-points at declaration order, and the QUESTION assertions and the status-bucket assertion STAY. The test guards three independent claims and only one loses its subject. The golden `src/plan/testdata/render-fixture.md` swaps its `epsilon` and `zeta` rows, and `render-fixture.steps/zeta.md` and `epsilon.md` lose the phrase "shares Roadmap order 5".
6. `cargo test` and `cargo clippy --all-targets -- -D warnings` exit 0.
7. `cargo run -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` reports the invariants hold.

### Increment 2, bring the prose that cites `order` up to date

WHAT IT DOES. Correct every passage that names the deleted field. This increment's diff to `docs/plans/agent-scaffold.md` is EXPECTED and is reviewed, which is why it is separate from increment 1: `docs/plans/agent-scaffold.md` inlines every step sidecar and every front sidecar verbatim, so a prose fix and a byte-exact oracle cannot live in one commit.

THE SITES ARE ENUMERATED RATHER THAN GREPPED FOR, because a grep whose empty output is the target cannot go empty here. `order` is an ordinary English word, and this step's own sidecar stays in the directory after the step closes.

- `docs/plans/agent-scaffold.success-criteria.md:20`, which lists the Roadmap as "(step status, order, dependencies)".
- `docs/plans/agent-scaffold.documentation-protocol.md:7`, whose sentence "to reorder or reprioritise, edit the Roadmap rows" describes the old operation.
- Step sidecars that cite a step by its `order` value: `checks-runner-worktree-name-collision.md`, `decision-folder-currency.md`, `generated-projection.md`, `status-resume-ignores-json.md`, `test-tmpdir-repo-assumption.md`, `workflow-enforcement-tier.md`, and this file.
- `docs/plans/agent-scaffold.ledger.md`, which carries its own `order <n>` citations. The ledger is a historical record, so a citation there is left as written unless it states a LIVE rule.

WHAT NOT TO DO WITH THOSE CITATIONS, measured because the cheap route is wrong. The absent `order` values 84 and 91 mean a citation at or below 83 stays exactly correct when reread as a position, a citation of 88 drifts by one, and a citation at or above 92 drifts by two. So a silent reinterpretation leaves some citations right and some wrong. Each one is restated by SLUG, which is the identifier the project already prefers and which survives every future reorder.

ACCEPTANCE CRITERIA.

1. Each site in the list above is either corrected or recorded as deliberately unchanged, with the reason. The list is the worklist and its completion is the oracle.
2. `grep -rn "order [0-9]" docs/plans/agent-scaffold.steps/ docs/plans/agent-scaffold.success-criteria.md docs/plans/agent-scaffold.documentation-protocol.md` returns only citations that name a value in a quotation of historical text. Any surviving hit is listed in the outcome with its reason.
3. `cargo run -- render --check --strict docs/plans/agent-scaffold.plan.toml` passes, and the reviewer reads the diff of `docs/plans/agent-scaffold.md`, which is expected to be non-empty.
4. `cargo test`, `cargo clippy --all-targets -- -D warnings` and `cargo run -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` exit 0.

### Increment 3, typed umbrella membership

WHAT IT DOES. Add a `[[umbrella]]` array of tables, each with `slug` and `title`. Add an `umbrella` field to `[[step]]` holding an umbrella slug. `validate` resolves the reference fail-closed, in the same manner as `blocked_by` and `folds`. `render` emits one group per CONTIGUOUS RUN of the `umbrella` value: the title and the shared context render on the first run, and a later run of the same umbrella renders the title with a generated continuation marker and no repeated context. The shared context lives at `docs/plans/agent-scaffold.umbrellas/<slug>.md` and is OPTIONAL, so an absent file means no context paragraph and is not an error. The umbrella prose moves out of the first member's sidecar, and every sentence that asserts a position is DELETED rather than corrected, because the position becomes structural.

THERE IS NO CONTIGUITY RULE, and the first draft of this step proposed one. The design pass rejects it on measured evidence from the plan's own corpus. `exploration-mode` is a `complete`, genuine and useful umbrella whose members render at 37, 40, 41 and 46 with six non-members between them, and whose prose asserts nothing false. So a non-contiguous member set is a LEGAL state in this plan, and a rule that forbids it invents an illegal state rather than removing one. A contiguity rule would also price the exact operation increment 1 exists to make cheap: cutting a member out of its run would make the plan invalid, and pasting any step into an umbrella's span would make the plan invalid for a reason unrelated to the step being moved.

THE `umbrella` FIELD IS NOT A SECOND COPY OF WHAT THE ARRAY CARRIES, stated because a reviewer proposed deleting it as one. `mode-enum` occupies rendered 5 to 8 and `pack-manifest` occupies 9 to 11. Position alone cannot tell a reader where one run ends and the next begins, so two adjacent runs are indistinguishable from one longer run. The field carries the PARTITION, and position does not carry the partition at all. That is the difference from `order`, which WAS fully derivable from declaration position.

THE EVIDENCE, MEASURED ON THE TREE THIS STEP IS AUTHORED INTO. Five sidecars open with an umbrella heading that names no slug. Four of the five assert adjacency in the words "the N steps below", and two of those four assertions are FALSE today, with no reorder involved.

- `convergence-accounting` claims eight steps below. Its members render at positions 13, 14, 15, 16, 20, 23, 24 and 27. Non-members sit inside that span at 17 (`file-safety-rules`), 18 (`agent-isolation`), 19 (`user-prompts-dir`), 21 (`gate-prompt-clarity`), 22 (`compaction-prep`), 25 (`no-wrap-convention`) and 26 (`findings-files`).
- `file-safety-rules` claims four steps below. Its members render at 17, 18, 19 and 22.
- `file-safety-rules` further states that `findings-files` sits "above" it. `findings-files` renders at 26 and `file-safety-rules` renders at 17, so `findings-files` sits nine rows below.
- Two assertions hold and are named so the sweep is not read as uniform: `mode-enum` at 5, 6, 7 and 8, and `pack-manifest` at 9, 10 and 11. `convergence-accounting` also states that `state-schema` follows immediately after `ledger-template`, and that claim is TRUE, at 27 and 28.
- `exploration-mode` asserts no adjacency and its members are NOT contiguous, at 37, 40, 41 and 46. It is the case that decides the design, and the first draft of this step checked it against the wrong question.

Reproduce every position with `awk '/^## Roadmap/{f=1} f&&/^\| `/{n++; print n, $2}' docs/plans/agent-scaffold.md`.

THE HEADING SURGERY IS ENUMERATED, because the increment moves headings and no automatic check catches a mixed heading level. `render --check` compares the projection against whatever the code emits, so it cannot see the problem.

- Five umbrella owners carry an umbrella heading above their own step heading: `mode-enum.md` (`###` at :1, `####` at :13), `pack-manifest.md` (`###` at :1, `####` at :15), `convergence-accounting.md` (`###` at :1, `###` at :5), `file-safety-rules.md` (`###` at :1, `###` at :5) and `exploration-mode.md` (`###` at :1, `###` at :5).
- Five member sidecars open at `####` and must be promoted to `###` once the umbrella heading leaves: `available-filter.md`, `external-packs.md`, `include-all-visible.md`, `pack-owned-principles.md` and `tag-selection.md`.
- `core-assets.md` opens with no heading at all. The increment does not fix that, and it is named here so the implementer is not surprised by it.

THE POSITIONAL PROSE IS DELETED AT A FIXED LIST OF SITES, not at whatever a grep returns. The sites are `convergence-accounting.md`, `file-safety-rules.md`, `mode-enum.md`, `pack-manifest.md` and `exploration-mode.md`, and in each the sentences that go are the ones stating "the N steps below", the ones asserting that a named step sits above or below, and the ones enumerating the members, which the `[[umbrella]]` data now carries.

ONE PACK CHANGE RIDES WITH THIS INCREMENT. `pack/plan-template.documentation-protocol.md` carries no sentence about a sidecar restating a `[[step]]` field, so no scaffolded project inherits the rule that this plan's own protocol states at `docs/plans/agent-scaffold.documentation-protocol.md:5`. Add one sentence there, SCOPED TO EXCLUDE THE HEADING: a step sidecar must not restate a `[[step]]` field other than in its heading, which `render` takes over in a later step. The unqualified form must not ship, because `pack/plan-template.steps/example-step.md:1` restates `slug` and `title` on its own first line, and so does almost every sidecar in this repository.

THE PACK REBUILD IS AN EXPLICIT DELIVERABLE OF THIS INCREMENT, and its own criterion proves it. The whole-file drift guards do NOT cover this file: `src/agents_md_drift.rs` guards the root `AGENTS.md`, `.agents/AGENTS.reference.md` and rendered assets whose `dest` starts with `.agents/prompts/` or `.agents/user-prompts/`, and its own coverage block names "the `docs/plans/TEMPLATE` family" as UNGUARDED. `pack/pack.toml:59` maps `plan-template.documentation-protocol.md` to `docs/plans/TEMPLATE.documentation-protocol.md`, which is squarely in that family, and `.agents/checks.toml` declares only `render-check`. So an edit to the pack source with no rerun of `just scaffold-self` ships a pack file and a committed template copy that disagree, silently.

THE TIDY-UP OF THE INTERLEAVED CLUSTERS IS NOT PART OF THIS INCREMENT. Nothing has to move. The design pass offers the tidy-up to the human as an OPTIONAL readability improvement over two spans, and this increment builds correctly whether the human takes it or not.

ACCEPTANCE CRITERIA.

1. `validate --source` rejects a plan whose step names an unknown umbrella, with a red-then-green test. `validate --source` ACCEPTS a plan whose umbrella members are not contiguous, with a test that pins the acceptance, so a later author does not add the invariant back by reflex.
2. `render` emits the umbrella title and its context on the first run of the value, and the title with a continuation marker on each later run. The render golden fixture covers an umbrella with a contiguous member set and an umbrella whose members are split by a non-member.
3. `render` produces the same output for an umbrella with a context sidecar and for one with no sidecar at all, apart from the context paragraph, and a test pins that an absent umbrella sidecar is not an error.
4. Every step heading in `docs/plans/agent-scaffold.md` sits at the same heading level.
5. No sentence in the five sidecars listed above states a position, an adjacency, or a membership list that the `[[umbrella]]` data now carries. The five files are the worklist and a reading of them is the oracle.
6. `just scaffold-self` runs in the increment, and `git diff --name-only` lists `docs/plans/TEMPLATE.documentation-protocol.md` alongside `pack/plan-template.documentation-protocol.md`. A pack edit with no rebuilt copy fails this criterion.
7. `cargo run -- render --check --strict docs/plans/agent-scaffold.plan.toml` passes, and the reviewer reads the diff of `docs/plans/agent-scaffold.md`.
8. `cargo test`, `cargo clippy --all-targets -- -D warnings` and `cargo run -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` exit 0.

### NOT IN SCOPE, NAMED SO IT IS NOT DRAWN IN

- THE GENERATED STEP HEADING. `render` could own the `### <slug>: <title>` heading and every sidecar could lose its own, which removes the last hand-written copy of `slug` and `title`. It is the right end state and the design pass deliberately declines to schedule it: it rewrites every sidecar, it collides with the backfill in `step-intent-encoding`, and the typed umbrella must ship first to show whether the grouping is enough on its own.
- THE TIDY-UP OF THE INTERLEAVED CLUSTERS. It is optional, it is the human's, and no increment here waits on it.
- THE 24 SIDECARS THAT KEEP AN ACCURATE STATUS LABEL. `Q-78` item (g) leaves them open, and the design pass recommends that `sidecar-status-opening-drift` widens to cover them, because that step already opens every affected file. `Q-78-statusform` set that step's scope, so the widening is a human decision and it belongs to that step rather than to this one.
- THE SIDECAR EXISTENCE CONTRACT. `render` treats a missing step or question sidecar as a hard failure, which is why every question sidecar is 0 bytes. This step makes the UMBRELLA sidecar optional and fixes nothing for the other two classes. That fix is its own step.
- THE `next` EXPLORATION-PHASE DEFECT, `Q-78` item (h). Increment 1 leaves it exactly as it stands, because `workflow-calibration` sits at order 35 and at position 35 alike.
- THE TWO INTENT FIELDS. They belong to `step-intent-encoding`, which is BLOCKED BY this step.
