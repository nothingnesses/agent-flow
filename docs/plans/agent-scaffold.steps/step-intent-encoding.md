### `step-intent-encoding`: record each step's problem and approach as two required `[[step]]` fields, project them through `render`, `next` and `status --step`, and backfill all 101 steps from cited sources (`Q-78`, pending review and a human decision)

THIS STEP IS CONDITIONAL AND MUST NOT BUILD YET. `Q-78` is `open`, not `decided`. The human directed on 2026-08-19 that reviewers review the design pass before its outcome enters the plan as the plan's answer. The design pass is `docs/plans/step-intent-encoding.explorations/Q-78.md`, which carries the full reasoning, the rejected alternatives and the measurement appendix. This sidecar states what the step builds, in what order, and what each increment proves.

THE PROBLEM. A reader who asks what a step is for, and how it addresses that, opens a file. The `Step` struct carries `slug`, `title`, `status`, `order`, `blocked_by`, `folds`, `provenance`, `increment` and `waiver`, and none of them states the problem or the approach. `provenance` points at the artefacts that JUSTIFY a step, which is an adjacent fact. No subcommand answers the question: `status` prints counts, `next` names one step and its role prompt, and `render` emits the whole document.

THE APPROACH. Put the problem and the approach in the structured source as two single-line fields, project them through the three readers that already exist, and backfill all 101 steps from sources that are named rather than recalled.

WHY TWO FIELDS AND NOT A VALIDATED SIDECAR SECTION, stated because the choice looks arbitrary otherwise. The measured drift in this plan is a STALE claim rather than an ABSENT one: 45 step sidecars restate `[[step]].status` in prose and 21 of them now contradict it. A required-section check would have caught NONE of the 21, because each of the 21 has the section and states it wrongly. A schema field catches absence and no more. Neither form catches staleness, and what removes staleness is the removal of the second copy, which is Principle 8, Structured data first, project for humans. Principle 5, Make illegal states unrepresentable, then decides between the two forms, because a required field makes a step with no stated problem fail to parse.

WHAT COUNTS AS INTENT, AND WHAT DOES NOT. The problem and the approach, one sentence each. The measured evidence, the alternatives rejected, the scope boundary, the priced cost and the executable acceptance criteria are NOT intent. They are the record of a decision, and they stay in the sidecar. The single-line bound is load-carrying in a second way: a multi-line field would grow every `[[step]]` block, and `plan-order-and-umbrella-structure` makes each block's length the cost of a reprioritisation. Two single-line fields raise the median block from 13 lines to 15.

### Increment 1, the fields and the projections

WHAT IT DOES. Add `problem` and `approach` to the `Step` struct (`src/plan/source.rs:129`) as `Option<String>`, so the plan still parses while the backfill runs. `render` emits both into the Step Detail, above the sidecar blob (`step_details_section`, `src/plan/render.rs:573`). `next` carries both in its `context` block, which is the brief an agent is handed and the place intent is most likely to be needed. `status` gains `--step <slug>` (`StatusArgs`, `src/main.rs:496`), which prints the step's problem and approach and honours the existing `--json`.

WHY NO EIGHTH SUBCOMMAND. `agent-flow --help` lists seven. A flag on `status` covers the read query at a fraction of the surface (Principle 2, Minimal by default). The query keeps `status`'s documented best-effort stance rather than `render`'s strict one, so a step with no intent recorded reports the absence and exits 0. After increment 3 that case is unreachable.

ACCEPTANCE CRITERIA.

1. `validate --source` accepts a plan with both fields, with one field, and with neither, and a test pins each.
2. `render --check --strict` passes, and the render golden fixture covers a step that carries both fields and a step that carries neither.
3. `next --json` carries both values in the active loop's context, and a test pins the key names.
4. `status --step <slug>` and `status --step <slug> --json` both print the two values, and `status --step <unknown-slug>` reports the unknown slug and exits non-zero.
5. `cargo test` and `cargo clippy --all-targets -- -D warnings` exit 0.

### Increment 2, the cited backfill

WHAT IT DOES. Fill `problem` and `approach` for all 101 steps. `complete` steps included, because the reader who asks what a step was for asks it most often about finished work, and 68 of the 101 are `complete`.

THE HUMAN REQUIREMENT THIS INCREMENT ANSWERS, stated on 2026-08-19: the git history must be combed so the information is extracted retroactively for existing steps. A design where the field is mandatory on new steps and empty on old ones does not satisfy it.

THE FOUR RULES THAT MAKE THE EXTRACTION TRUSTWORTHY, in the order of how much each buys.

1. TRANSCRIBE BEFORE YOU PARAPHRASE. For most steps the problem and the approach are already written, in the 2312 lines of sidecar prose, by the person who had the context at the time. `pack/plan-template.steps/example-step.md` asks for exactly that text: "What this step does and how; once done, the outcome and the evidence." So the first source for each step is its own sidecar, and git history supplies the citation for that text rather than a fresh derivation of it. Comb the history for the steps whose sidecar states neither, and for those the source is the commit or the decision receipt that does.
2. NAME THE SOURCE FOR EVERY STATEMENT. Each backfilled pair carries a source reference of the form `<commit>` or `<commit>:<path>`.
3. CHECK THE CITATION MECHANICALLY, OUTSIDE THE VALIDATOR. `git cat-file -e` for the commit form and `git show <commit>:<path>` for the path form, as a `[[check]]` command in `.agents/checks.toml`. It cannot live in `validate`: `src/plan/source.rs` states in its own provenance comment that validation is a pure function over the string that never git-resolves a hash and never stats a path, and `commits` in `[step.provenance]` are shape-checked for that reason.
4. REVIEW IN BATCHES. 101 statements in one review artefact is the shape this project's loop punishes hardest, and the plan records why: the diagnosed cause of length in the `workflow-enforcement-tier-fold` loop was a document assembled in layers whose characteristic defect was an aggregate that contradicted a detail elsewhere in the same document.

WHY A CITATION CONSTRAINT ALONE IS NOT ENOUGH, recorded so a reviewer does not read rule 2 as the whole guarantee. This project's measured failure mode is not a fabricated citation. The `workflow-enforcement-tier-endproperty-fold` waiver records that the sites which failed review shared one property, a claim STATED MORE GENERALLY THAN WHAT WAS MEASURED, and a citation check passes on such a claim. Rule 1 is what reduces the exposure, because it removes the paraphrase step for most of the 101.

ACCEPTANCE CRITERIA.

1. All 101 steps carry both fields, and the count is reproduced by a command rather than asserted.
2. Every source reference resolves, proved by the check command from rule 3, run over every step.
3. Each batch carries its own review round, and the batch boundaries are recorded in the ledger before the first batch runs.
4. Each statement is one sentence and states its claim in the direction the source states it. A reviewer checks this by reading the source, and no check can prove it.
5. `render --check --strict` passes, and the sidecar text that a transcribed sentence came from is MOVED rather than duplicated, so `render` does not emit the same sentence twice.

### Increment 3, flip to required

WHAT IT DOES. Change both fields from `Option<String>` to `String` and delete the `Option` handling in `render`, `next` and `status`. Update the four TOML fixtures, the pack plan template and `docs/plans/TEMPLATE.plan.toml` so a scaffolded project declares both fields from its first step.

WHY THE MIGRATION RUNS THIS WAY. The alternative, land the fields as required and backfill all 101 in the same commit, has no optional window at all, which Principle 5 prefers. It is rejected on the review record in rule 4 above. The window in which absence is legal is one step long, and this increment closes it, so the end state makes absence unrepresentable and no `[meta]` exemption field is needed. An exemption boundary of the `[meta].w4_baseline` kind is right for a rule that will always have exempt members and wrong for a migration that finishes.

ACCEPTANCE CRITERIA.

1. `validate --source` rejects a plan whose step omits either field, with a red-then-green test for each field.
2. `cargo run -- validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl` exits 0, which is the oracle that all 101 carry both.
3. `scaffold` into an empty directory produces a plan whose example step declares both fields, and the scaffolded plan validates.
4. `cargo test`, `cargo clippy --all-targets -- -D warnings`, `render --check --strict` and `validate --workflow` exit 0.

### NOT IN SCOPE, NAMED SO IT IS NOT DRAWN IN

- THE `order` DELETION AND THE TYPED UMBRELLA. Both belong to `plan-order-and-umbrella-structure`, which neither blocks this step nor is blocked by it.
- ANY CONTENT RULE OVER THE INTENT PROSE. `validate` checks presence. It does not check that a sentence is true, and this step does not pretend that a check can.
- THE 78 EMPTY QUESTION SIDECARS. All 78 are 0 bytes and exist only to satisfy `render`'s existence check. The design pass records this under `Q-78` item (e) as a wart in the reader's contract rather than in this schema, and schedules nothing for it.
- THE `next` EXPLORATION-PHASE DEFECT, `Q-78` item (h). It keeps its own step and its own human decision.
