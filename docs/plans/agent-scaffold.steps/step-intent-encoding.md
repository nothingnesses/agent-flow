### `step-intent-encoding`: record each step's problem and approach as two required `[[step]]` fields, project them through `render`, `next` and `status --step`, and backfill every step from cited sources (`Q-78`, pending review and a human decision)

THIS STEP IS CONDITIONAL AND MUST NOT BUILD YET. `Q-78` is `open`, not `decided`. The human directed on 2026-08-19 that reviewers review the design pass before its outcome enters the plan as the plan's answer. The design pass is `docs/plans/step-intent-encoding.explorations/Q-78.md`, which carries the full reasoning, the rejected alternatives and the measurement appendix. This sidecar states what the step builds, in what order, and what each increment proves. It states no count of the plan's steps, because such a count expires and the plan's own standing cure, recorded in the ledger against orchestrator defect (12), is to carry the selecting command instead.

THIS STEP IS BLOCKED BY `plan-order-and-umbrella-structure`, and the direction is deliberate. Both steps rewrite every `[[step]]` block of the same file: the other step deletes a line from each and moves one block, and this step adds two lines to each. With both unblocked, `next` can select either, and whichever lands second rebases across a whole-file rewrite and gives its review round a diff dominated by the other step's churn. Deleting a field before adding two is the cheaper order, because the intent fields then never have to be threaded past a block move.

THE PROBLEM. A reader who asks what a step is for, and how it addresses that, opens a file. The `Step` struct carries `slug`, `title`, `status`, `order`, `blocked_by`, `folds`, `provenance`, `increment` and `waiver`, and none of them states the problem or the approach. `provenance` points at the artefacts that JUSTIFY a step, which is an adjacent fact. No subcommand answers the question: `status` prints counts, `next` names one step and its role prompt, and `render` emits the whole document.

THE APPROACH. Put the problem and the approach in the structured source as two single-line fields, project them through the three readers that already exist, and backfill every step from sources that are named rather than recalled.

WHY TWO FIELDS AND NOT A VALIDATED SIDECAR SECTION, stated because the choice looks arbitrary otherwise. The measured drift in this plan is a STALE claim rather than an ABSENT one: 45 step sidecars restate `[[step]].status` in prose and 21 of them now contradict it. A required-section check would have caught NONE of the 21, because each of the 21 has the section and states it wrongly. A schema field catches absence and no more. Neither form catches staleness, and what removes staleness is the removal of the second copy, which is Principle 8, Structured data first, project for humans. Principle 5, Make illegal states unrepresentable, then decides between the two forms, because a required field makes a step with no stated problem fail to parse.

WHAT COUNTS AS INTENT, AND WHAT DOES NOT. The problem and the approach, one sentence each. The measured evidence, the alternatives rejected, the scope boundary, the priced cost and the executable acceptance criteria are NOT intent. They are the record of a decision, and they stay in the sidecar. The single-line bound is load-carrying in a second way: a multi-line field would grow every `[[step]]` block, and `plan-order-and-umbrella-structure` makes each block's length the cost of a reprioritisation. Two single-line fields raise the median block from 13 lines to 15.

THE SINGLE-LINE BOUND IS ENFORCED RATHER THAN TRUSTED. `deny_unknown_fields` constrains keys and not values, so without a rule a later author can write `problem = """..."""` across ten lines and the plan parses. `validate` therefore rejects a newline in either field. The rule is a pure function over the deserialised string, which fits the validator's existing stance exactly, and it catches a `"""` block, a `'''` block and a `\n` escape alike. A character cap is REJECTED: the quantity that carries the cost is the block's LINE count, and a single-line string of any length adds exactly one line.

THE INCREMENTS ARE DECLARED IN THE PLAN TOML as `[[step.increment]]` entries with their risk classes, so a round record joins to them structurally rather than by a lexical prefix (Principle 8).

### Increment 1, the fields and the projections

WHAT IT DOES. Add `problem` and `approach` to the `Step` struct (`src/plan/source.rs:129`) as `Option<String>`, so the plan still parses while the backfill runs. `render` emits both into the Step Detail, IMMEDIATELY AFTER THE SIDECAR'S FIRST LINE (`step_details_section`, `src/plan/render.rs:573`). `next` carries both in its `context` block, which is the brief an agent is handed and the place intent is most likely to be needed. `status` gains `--step <slug>` (`StatusArgs`, `src/main.rs:496`), which prints the step's problem and approach and honours the existing `--json`. `validate` gains the newline rule.

WHY THE PLACEMENT IS SPECIFIED AS "AFTER THE FIRST LINE" AND NOT "ABOVE THE BLOB". `step_details_section` inlines each sidecar verbatim, and each sidecar carries its own `### <slug>` heading, which this step does not move. So "above the blob" is ABOVE THAT HEADING, which would file step N's intent under step N-1's section and the first step's intent under the bare `## Step Details` heading. `render --check --strict` cannot catch that, because the projection is compared against whatever the code emits. Criteria 2 and 3 below pin it instead.

WHY NO EIGHTH SUBCOMMAND. `agent-flow --help` lists seven. A flag on `status` covers the read query at a fraction of the surface (Principle 2, Minimal by default).

WHAT AN UNKNOWN SLUG DOES, RULED HERE IN PROSE RATHER THAN LEFT IN A CRITERION. `status --step <unknown-slug>` reports the unknown slug and EXITS 0. The reason: `status --help` reads "Best-effort; a missing file yields a partial projection", and `status --source <plan> --plan /nonexistent.md` prints a note and exits 0 today. An unknown slug and a missing file are the same class of resolution failure, so a strict exit on one and a best-effort exit on the other would split the subcommand's contract on no stated ground. A step with no intent recorded likewise reports the absence and exits 0, and after increment 3 that second case is unreachable while the first is not. The first draft of this step required a non-zero exit in a criterion while its own prose promised the best-effort stance, which is a design decision hidden in an acceptance criterion.

ACCEPTANCE CRITERIA.

1. `validate --source` accepts a plan with both fields, with one field, and with neither, and a test pins each. `validate --source` REJECTS a plan whose `problem` or `approach` contains a newline, with a red-then-green test for each field.
2. `cargo run -- render --check --strict docs/plans/agent-scaffold.plan.toml` passes, and the render golden fixture covers a step that carries both fields and a step that carries neither. In the golden, both intent lines for a step sit BELOW that step's own `###` heading and above the rest of its body.
3. The render golden covers a step that carries both fields and an EMPTY sidecar, and that step produces a Step Detail entry. `step_details_section` skips a step whose body is empty today, and increment 2 moves sentences out of sidecars, so a sidecar can become empty.
4. `next --json` carries both values in the active loop's context, and a test pins the key names.
5. `status --step <slug>` and `status --step <slug> --json` both print the two values. `status --step <unknown-slug>` reports the unknown slug and exits 0, and a test pins the exit code so the stance is not weakened later.
6. `cargo test` and `cargo clippy --all-targets -- -D warnings` exit 0.

### Increment 2, the cited backfill

WHAT IT DOES. Fill `problem` and `approach` for every step in the plan, `complete` steps included, because the reader who asks what a step was for asks it most often about finished work and most of the plan's steps are `complete`.

THE HUMAN REQUIREMENT THIS INCREMENT ANSWERS, stated on 2026-08-19: the git history must be combed so the information is extracted retroactively for existing steps. A design where the field is mandatory on new steps and empty on old ones does not satisfy it.

THE FIRST TASK IS A SIZING SAMPLE, NOT A BATCH. Rule 1 below claims that most steps already carry a transcribable problem sentence and a transcribable approach sentence, and NOTHING MEASURES THAT. The design pass states the gap plainly rather than papering it over with a figure, because "does this paragraph yield a transcribable sentence" is a reading and not a measurement. So the increment opens by sampling 20 sidecars across the length distribution and reporting the yield for the two fields SEPARATELY, and the review budget is sized from that result. The pass's own reading of the low end suggests the two behave differently: an approach sentence transcribes readily, and the problem half is the one that needs paraphrase for a minority of steps. `file-dropper.md`, the shortest sidecar in the plan at 54 words, states an approach and states no problem at all.

A LINE COUNT IS NOT A LENGTH MEASURE HERE, and a reviewer's argument from one must be resisted. This repository does not hard-wrap prose (`no-wrap-convention`), so a sidecar paragraph is one line. Measure in words:

```
for f in docs/plans/agent-scaffold.steps/*.md; do printf "%s %s\n" "$(wc -w < $f)" "$f"; done | sort -n
```

THE FOUR RULES THAT MAKE THE EXTRACTION TRUSTWORTHY, in the order of how much each buys.

1. TRANSCRIBE BEFORE YOU PARAPHRASE. For most steps the problem and the approach are already written, in the sidecar prose, by the person who had the context at the time. `pack/plan-template.steps/example-step.md` asks for exactly that text: "What this step does and how; once done, the outcome and the evidence." So the first source for each step is its own sidecar, and git history supplies the citation for that text rather than a fresh derivation of it. Comb the history for the steps whose sidecar states neither, and for those the source is the commit or the decision receipt that does.
2. NAME THE SOURCE FOR EVERY STATEMENT, AND MARK HOW IT WAS TAKEN. Each backfilled pair carries a source reference of the form `<commit>` or `<commit>:<path>`, and each field is marked `transcribed` or `paraphrased`.
3. CHECK THE CITATION MECHANICALLY, OUTSIDE THE VALIDATOR. `git cat-file -e` for the commit form and `git show <commit>:<path>` for the path form, as a `[[check]]` command in `.agents/checks.toml`. It cannot live in `validate`: `src/plan/source.rs` states in its own provenance comment that validation is a pure function over the string that never git-resolves a hash and never stats a path, and `commits` in `[step.provenance]` are shape-checked for that reason. For a `transcribed` field the check goes further and asserts that `git show <commit>:<path>` CONTAINS the sentence, which turns an existence proof into a relationship proof. The stronger form is NOT applied to a `paraphrased` field, because a faithful paraphrase is trimmed or joined and a substring test would then fail on correct work.
4. REVIEW IN BOUNDED BATCHES. One statement per step in one review artefact is the shape this project's loop punishes hardest, and `docs/plans/agent-scaffold.ledger.md` records why in the paragraph headed "SIX-ROUND SCORECARD FOR THE PLAN FOLD": the diagnosed cause of that loop's length was a document assembled in layers whose characteristic defect was an aggregate that contradicted a detail elsewhere in the same document. A batch therefore carries a MAXIMUM OF 20 STEPS.

WHY A CITATION CONSTRAINT ALONE IS NOT ENOUGH, recorded so a reviewer does not read rule 2 as the whole guarantee. This project's measured failure mode is not a fabricated citation. The `workflow-enforcement-tier-endproperty-fold` waiver records that the sites which failed review shared one property, a claim STATED MORE GENERALLY THAN WHAT WAS MEASURED, and a citation check passes on such a claim. Rule 1 is what reduces the exposure, and rule 3's stronger form is what gives rule 2 teeth where a relationship is actually claimed.

ACCEPTANCE CRITERIA.

1. Every step in the plan carries both fields, proved by a command with no literal count in it. `cargo run -- validate --source docs/plans/agent-scaffold.plan.toml` after increment 3's flip is the eventual oracle, and within this increment the check is that the set of steps declaring `problem` equals the set of `[[step]]` blocks.
2. Every source reference resolves, proved by the check command from rule 3, run over every step. For every field marked `transcribed`, the check additionally proves that the cited object CONTAINS the sentence.
3. The batch boundaries are recorded in the ledger before the first batch runs, no batch exceeds 20 steps, and each batch carries its own review round.
4. Each statement is one sentence and states its claim in the direction the source states it. A reviewer checks this by reading the source, and no check can prove it. This criterion is a reading, which is why criterion 3 bounds how much of it any one round has to carry.
5. `cargo run -- render --check --strict docs/plans/agent-scaffold.plan.toml` passes, and the sidecar text that a transcribed sentence came from is MOVED rather than duplicated.
6. After the backfill, no sidecar contains its own step's `problem` or `approach` string verbatim, checked mechanically. This is a comparison between two fields of one plan, so it asserts nothing about whether a sentence is true and it stays on the admissible side of the line the design pass draws. It exists because the prose rule alone measurably failed once already: `docs/plans/agent-scaffold.documentation-protocol.md:5` already forbids repeating the status label, and 45 sidecars broke it.

### Increment 3, flip to required

WHAT IT DOES. Change both fields from `Option<String>` to `String` and delete the `Option` handling in `render`, `next` and `status`. Update the four TOML fixtures, the pack plan template and `docs/plans/TEMPLATE.plan.toml` so a scaffolded project declares both fields from its first step.

WHY THE MIGRATION RUNS THIS WAY. The alternative, land the fields as required and backfill every step in the same commit, has no optional window at all, which Principle 5 prefers. It is rejected on the review record in rule 4 above. The window in which absence is legal is one step long, and this increment closes it, so the end state makes absence unrepresentable and no `[meta]` exemption field is needed. An exemption boundary of the `[meta].w4_baseline` kind is right for a rule that will always have exempt members and wrong for a migration that finishes.

WHAT THIS COSTS A SCAFFOLDED PROJECT, STATED HERE AND WEIGHED BY THE HUMAN. After this increment, adding a step to any scaffolded plan requires two prose sentences before the plan parses, and for an exploratory step the problem statement is often the thing the step exists to find out. The pack template must ship placeholder values, because a required `String` needs one, so every scaffolded plan validates on day one carrying placeholder intent. The required field therefore makes ABSENCE unrepresentable and leaves MEANINGLESSNESS fully representable. The design pass records this as an accepted residual and routes the question of whether the fields stay required to the human. A `validate` rule that rejects the placeholder strings is REJECTED: it would break criterion 3 below, which is correct under Principle 3, Safe on existing projects, and Principle 4, Idempotent. Placeholder detection, if wanted, belongs in `audit` and is a separate step.

ACCEPTANCE CRITERIA.

1. `validate --source` rejects a plan whose step omits either field, with a red-then-green test for each field.
2. `cargo run -- validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl` exits 0, which is the oracle that every step carries both.
3. `scaffold` into an empty directory produces a plan whose example step declares both fields, and the scaffolded plan validates.
4. `cargo test`, `cargo clippy --all-targets -- -D warnings`, `cargo run -- render --check --strict docs/plans/agent-scaffold.plan.toml` and `cargo run -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` exit 0.

### THE RESIDUALS THIS STEP ACCEPTS RATHER THAN CLOSES

Both are recorded so a later review round does not file either as a fresh finding.

- INTENT-PROSE STALENESS. `problem` and `approach` hold prose, and prose in a TOML string goes stale exactly as prose in Markdown does. Increment 2 criterion 6 closes the duplication case and increment 3 closes the absence case. Nothing closes the case where the recorded intent is no longer what the step is for, and no check can.
- MEANINGLESSNESS UNDER A REQUIRED FIELD. A placeholder sentence parses and validates, so a scaffolded project can carry placeholder intent indefinitely. `title` has carried the same property since the schema shipped, which is why nobody has minded.

### NOT IN SCOPE, NAMED SO IT IS NOT DRAWN IN

- THE `order` DELETION AND THE TYPED UMBRELLA. Both belong to `plan-order-and-umbrella-structure`, which BLOCKS this step.
- ANY CONTENT RULE OVER THE INTENT PROSE. `validate` checks presence and the single-line bound. It does not check that a sentence is true, and this step does not pretend that a check can. Increment 2 criterion 6 is a comparison between two fields of one plan and is not a content rule.
- PLACEHOLDER DETECTION IN `validate`. Rejected above. It belongs in `audit` and is a separate step.
- THE EMPTY QUESTION SIDECARS. All are 0 bytes and exist only to satisfy `render`'s existence check. The design pass records this under `Q-78` item (e) as a wart in the reader's contract rather than in this schema, and schedules nothing for it.
- THE `next` EXPLORATION-PHASE DEFECT, `Q-78` item (h). It keeps its own step and its own human decision.
