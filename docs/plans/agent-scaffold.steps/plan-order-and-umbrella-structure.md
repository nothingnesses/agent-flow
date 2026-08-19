### `plan-order-and-umbrella-structure`: delete the `order` field so the `[[step]]` array position is the plan order, and make umbrella membership typed data with a contiguity rule (`Q-78`, pending review and a human decision)

THIS STEP IS CONDITIONAL AND MUST NOT BUILD YET. `Q-78` is `open`, not `decided`. The human directed on 2026-08-19 that reviewers review the design pass before its outcome enters the plan as the plan's answer, and two of the three items this step depends on go to the human as choices. The design pass is `docs/plans/step-intent-encoding.explorations/Q-78.md`, which carries the full reasoning, the rejected alternatives and the measurement appendix. This sidecar states what the step builds, in what order, and what each increment proves.

THE PROBLEM. The plan carries the step order twice. `[[step]].order` states it as a number, and the declaration sequence of the `[[step]]` blocks states it as a position. The two agree today at every step except one, and a reprioritisation has to renumber both. The human ruled on 2026-08-19 that a numeric field is the wrong representation, because a reprioritisation renumbers many entries where a cut and paste of an entry does not. Separately, the plan expresses umbrella grouping as prose that asserts position, and three of those positional assertions are already false.

THE APPROACH. Delete the number and keep the position. Then turn the umbrella from a paragraph that claims adjacency into typed data whose adjacency the validator enforces.

### Increment 1, delete `order`

WHAT IT DOES. Remove `order` from the `Step` struct (`src/plan/source.rs:137`), from all 101 `[[step]]` blocks, from the four TOML fixtures and from the inline TOML literals in the unit tests. Replace the sort at `src/plan/render.rs:177` with the declaration order. Remove `StepInfo.order` (`src/next.rs:527`) and the two assignments at `src/next.rs:540` and `src/next.rs:560`, and turn the three `min_by_key(order)` calls in `select_active_loop` (`src/next.rs:716`, `:723`, `:728`) into first-match searches over the slice.

THE ONE DATA MOVE THE MIGRATION OWES. `rename-to-agent-flow` stands 84th in the file and carries `order = 100`, which renders it 98th. Every other step's declaration position agrees with its rendered position. So the block moves from declaration position 84 to declaration position 98, and nothing else moves.

WHY THE FIELD IS DELETED RATHER THAN REPLACED BY A SLUG LIST, and the note that the human owns this. An explicit ordered list of slugs in `[meta]` moves one line per reprioritisation, against a block of median 13 lines here. It is rejected in the design pass under Principle 5, Make illegal states unrepresentable, because a list admits a duplicate entry, a missing entry and an entry that names no step, where an array admits none of the three, and under Principle 2, Minimal by default, because the deletion removes a field, a sort and three call sites where a list adds a field, a permutation rule and a lookup. THE HUMAN HAS NOT CHOSEN BETWEEN THE TWO. Do not start this increment until the human does.

THE SUPPORTING MEASUREMENT. `steps_from_markdown` (`src/next.rs:560`) already derives the order from the table index, because the Markdown Roadmap carries no order field. The deletion makes the two substrates agree rather than diverge.

A STALE DOC COMMENT THIS INCREMENT ALSO FIXES, found while the above was measured. `src/plan/render.rs:462` describes the Roadmap table as "(slug, status, order)". The table emits slug, status and Notes, and it emitted no order column before this step existed.

ACCEPTANCE CRITERIA.

1. `grep -c '^order = ' docs/plans/agent-scaffold.plan.toml` exits 1 and prints 0.
2. `cargo run -- render --check --strict` reports the projection up to date against the COMMITTED `docs/plans/agent-scaffold.md`, with that file UNCHANGED by this increment. This is the whole migration's oracle: `render` emits no order column, so a correct migration changes the projected document not at all.
3. `git diff --stat` over `docs/plans/agent-scaffold.md` reports no change.
4. `cargo run -- next --source docs/plans/agent-scaffold.plan.toml` names the same active loop as it named before the increment.
5. `cargo test` and `cargo clippy --all-targets -- -D warnings` exit 0. The equal-order tie-break test at `src/plan/render.rs:1126` loses its subject and must be deleted or re-pointed, not silently weakened.
6. `cargo run -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` reports the invariants hold.

### Increment 2, typed umbrella membership

WHAT IT DOES. Add a `[[umbrella]]` array of tables, each with `slug` and `title`, whose shared context lives at `docs/plans/agent-scaffold.umbrellas/<slug>.md` under the same filename convention `render` already uses for steps and questions. Add an `umbrella` field to `[[step]]` holding an umbrella slug. `validate` resolves the reference fail-closed, in the same manner as `blocked_by` and `folds`, and additionally requires that the members of one umbrella occupy CONTIGUOUS positions in the step array. `render` emits the umbrella title and its context once, before the first member, and emits each member under it. The umbrella prose moves out of the first member's sidecar, and every sentence that asserts a position is DELETED rather than corrected, because the position becomes structural.

WHY CONTIGUITY IS ENFORCED RATHER THAN WORKED AROUND. The proposal put to the design pass was that `render` groups by membership rather than by adjacency. The pass rejected that specific mechanism: a `render` that gathers scattered members means the array position no longer determines the rendered sequence, which contradicts increment 1 in the same schema. A contiguity invariant satisfies both.

THE EVIDENCE, MEASURED ON THE TREE THIS STEP IS AUTHORED INTO. Five sidecars open with an umbrella heading that names no slug. Four of the five assert adjacency in the words "the N steps below", and two of those four assertions are FALSE today, with no reorder involved.

- `convergence-accounting` claims eight steps below. Its members render at positions 13, 14, 15, 16, 20, 23, 24 and 27.
- `file-safety-rules` claims four steps below. Its members render at 17, 18, 19 and 22.
- The two clusters interleave with each other and with `gate-prompt-clarity` at 21, `no-wrap-convention` at 25 and `findings-files` at 26.
- `file-safety-rules` further states that `findings-files` sits "above" it. `findings-files` renders at 26 and `file-safety-rules` renders at 17, so `findings-files` sits nine rows below.
- Two assertions hold and are named so the sweep is not read as uniform: `mode-enum` at 5, 6, 7 and 8, and `pack-manifest` at 9, 10 and 11. `exploration-mode` asserts no adjacency at all. `convergence-accounting` also states that `state-schema` follows immediately after `ledger-template`, and that claim is TRUE, at 27 and 28.

Reproduce every position with `awk '/^## Roadmap/{f=1} f&&/^\| `/{n++; print n, $2}' docs/plans/agent-scaffold.md`.

THE COST THIS INCREMENT CARRIES, AND THE HUMAN DECISION IT WAITS ON. Contiguity does not hold today for two clusters, so the 15 steps at rendered positions 13 to 27 must be reordered. All 15 are `complete`, and `select_active_loop` skips terminal phases, so the reorder is inert for `next` and changes only the reading order of the projected document. It falsifies no chronology, because the plan order is already not the build order: `validation-constraints` is `not-started` at position 96, ahead of `ship-v0-0-2`, which is `complete` at 97. THE HUMAN OWNS THE REORDER, because it changes the published plan document, and this increment does not start until the human rules on it.

ONE PACK CHANGE RIDES WITH THIS INCREMENT. `pack/plan-template.documentation-protocol.md` carries no sentence about a sidecar restating a `[[step]]` field, so no scaffolded project inherits the rule that this plan's own protocol states at `docs/plans/agent-scaffold.documentation-protocol.md:5`. Add one sentence there, scoped to what the tool can enforce today: a step sidecar must not restate a `[[step]]` field. The whole-file drift guards cover the pack copies, so the rebuild is part of the increment.

ACCEPTANCE CRITERIA.

1. `validate --source` rejects a plan whose step names an unknown umbrella, and rejects a plan whose umbrella members are not contiguous. Each rejection has a red-then-green test.
2. No step sidecar states a position, an adjacency or a count of the steps around it. Reproduce with a grep for "steps below" and "above" over `docs/plans/agent-scaffold.steps/`, which returns nothing.
3. `render` emits each umbrella's title and context exactly once, before the first member, and the render golden fixture covers a two-member umbrella.
4. `render --check --strict` passes, and the reviewer reads the diff of `docs/plans/agent-scaffold.md` against the reorder the human approved.
5. `cargo test`, `cargo clippy --all-targets -- -D warnings` and `validate --workflow` exit 0.

### NOT IN SCOPE, NAMED SO IT IS NOT DRAWN IN

- THE GENERATED STEP HEADING. `render` could own the `### <slug>: <title>` heading and all 101 sidecars could lose theirs, which removes the last hand-written copy of `slug` and `title`. It is the right end state and the design pass deliberately declines to schedule it: it rewrites all 101 sidecars, it collides with the backfill in `step-intent-encoding`, and the typed umbrella must ship first to show whether the grouping is enough on its own.
- THE 24 SIDECARS THAT KEEP AN ACCURATE STATUS LABEL. `Q-78` item (g) leaves them open, and the design pass recommends that `sidecar-status-opening-drift` widens to cover them, because that step already opens every affected file. `Q-78-statusform` set that step's scope, so the widening is a human decision and it belongs to that step rather than to this one.
- THE `next` EXPLORATION-PHASE DEFECT, `Q-78` item (h). Increment 1 leaves it exactly as it stands, because `workflow-calibration` sits at order 35 and at position 35 alike.
- THE TWO INTENT FIELDS. They belong to `step-intent-encoding`, which neither blocks this step nor is blocked by it.
