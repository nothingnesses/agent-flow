### `step-intent-encoding`: record each step's problem and approach as two required `[[step]]` fields, project them through `render`, `next` and `status --step`, and backfill every step from cited sources (`Q-78-requiredfields`, decided 2026-08-21, pending the review)

THIS STEP IS CONDITIONAL AND MUST NOT BUILD YET. `Q-78` is `open`, not `decided`. The human directed on 2026-08-19 that reviewers review the design pass before its outcome enters the plan as the plan's answer, so the review is what this step now waits on. THE ONE HUMAN DECISION THIS STEP DEPENDED ON IS TAKEN. `problem` and `approach` ARE REQUIRED, in the shipped pack as well as here, decided on 2026-08-21 with receipt `q_id:"Q-78-requiredfields"`. Increment 3 is the increment that decision governs, and it no longer waits on the human. The design pass is `docs/plans/step-intent-encoding.explorations/Q-78.md`, which carries the full reasoning, the rejected alternatives and the measurement appendix. This sidecar states what the step builds, in what order, and what each increment proves. It states no count of the plan's steps, because such a count expires and the plan's own standing cure, recorded in the ledger against orchestrator defect (12), is to carry the selecting command instead.

THIS STEP IS BLOCKED BY `plan-order-array-position`, and the direction is deliberate. Both steps rewrite every `[[step]]` block of the same file: the other step deletes a line from each and moves one block, and this step adds two lines to each. With both unblocked, `next` can select either, and whichever lands second rebases across a whole-file rewrite and gives its review round a diff dominated by the other step's churn. Deleting a field before adding two is the cheaper order, because the intent fields then never have to be threaded past a block move.

THE PROBLEM. A reader who asks what a step is for, and how it addresses that, opens a file. The `Step` struct carries `slug`, `title`, `status`, `order`, `blocked_by`, `folds`, `provenance`, `increment` and `waiver`, and none of them states the problem or the approach. `provenance` points at the artefacts that JUSTIFY a step, which is an adjacent fact. No subcommand answers the question: `status` prints counts, `next` names one step and its role prompt, and `render` emits the whole document.

THE APPROACH. Put the problem and the approach in the structured source as two single-line fields, project them through the three readers that already exist, and backfill every step from sources that are named rather than recalled.

WHY TWO FIELDS AND NOT A VALIDATED SIDECAR SECTION, stated because the choice looks arbitrary otherwise. The measured drift in this plan is a STALE claim rather than an ABSENT one: 45 step sidecars restate `[[step]].status` in prose and 21 of them now contradict it. A required-section check would have caught NONE of the 21, because each of the 21 has the section and states it wrongly. A schema field catches absence and no more. Neither form catches staleness, and what removes staleness is the removal of the second copy, which is Principle 8, Structured data first, project for humans. Principle 5, Make illegal states unrepresentable, then decides between the two forms, because a required field makes a step with no stated problem fail to parse.

WHAT COUNTS AS INTENT, AND WHAT DOES NOT. The problem and the approach, one sentence each. The measured evidence, the alternatives rejected, the scope boundary, the priced cost and the executable acceptance criteria are NOT intent. They are the record of a decision, and they stay in the sidecar. The single-line bound is load-carrying in a second way: a multi-line field would grow every `[[step]]` block, and `plan-order-array-position` makes each block's length the cost of a reprioritisation. Two single-line fields add exactly two lines to a block whatever its length. No snapshot of the block length is restated here, because the relation carries the argument and the design pass states the priced pair once, with its command.

THE SINGLE-LINE BOUND IS ENFORCED RATHER THAN TRUSTED. `deny_unknown_fields` constrains keys and not values, so without a rule a later author can write `problem = """..."""` across ten lines and the plan parses. `validate` therefore rejects a newline in either field. The rule is a pure function over the deserialised string, which fits the validator's existing stance exactly, and it catches a `"""` block, a `'''` block and a `\n` escape alike. A character cap is REJECTED: the quantity that carries the cost is the block's LINE count, and a single-line string of any length adds exactly one line.

THE INCREMENTS ARE DECLARED IN THE PLAN TOML as `[[step.increment]]` entries with their risk classes, so a round record joins to them structurally rather than by a lexical prefix (Principle 8). EACH CLASS STATES ITS GROUND, in the shape `test-tmpdir-repo-assumption.md` uses, because a class sets the required clean-round count and a class asserted without a ground is the defect this pass polices elsewhere (Principle 6, Ground decisions in evidence). AN EARLIER DRAFT CLASSED INCREMENTS 1 AND 3 `low_risk` AND STATED NO GROUND FOR ANY OF THE THREE. Both were corrected against the `AGENTS.md` test after a review round measured the inversion: a pure prose sweep in the sibling step was `risky` while an increment touching four source files and a new CLI surface was `low_risk`.

### Increment 1, the fields and the projections

RISK CLASS `risky` (two consecutive clean review rounds). THE GROUND: the increment changes the plan schema (`src/plan/source.rs`), the generated document for every project (`src/plan/render.rs`), the `context` block that `next` hands an agent as an instruction rather than a report (`src/next.rs`), a new CLI flag with a stated exit-code contract (`src/main.rs:496`), and it adds a new `validate` rejection rule. It changes product behaviour and it ships to every scaffolded project, which is the "widely depended on" clause of the `AGENTS.md` test. `workflow-enforcement-tier.md` is the plan's own precedent that `next`'s output being an instruction rather than a report is a blast-radius argument.

WHAT IT DOES. Add `problem` and `approach` to the `Step` struct (`src/plan/source.rs:129`) as `Option<String>`, so the plan still parses while the backfill runs. `render` emits both into the Step Detail (`step_details_section`, `src/plan/render.rs:573`). `next` carries both in its `context` block, which is the brief an agent is handed and the place intent is most likely to be needed. `status` gains `--step <slug>` (`StatusArgs`, `src/main.rs:496`), which prints the step's problem and approach and honours the existing `--json`. `validate` gains the newline rule.

THE PLACEMENT IS SPECIFIED AGAINST THE SIDECAR'S LEADING HEADING LINE, NOT AGAINST ITS FIRST LINE. `step_details_section` inlines each sidecar verbatim. "Above the blob" would file step N's intent under step N-1's section and the first step's intent under the bare `## Step Details` heading, which is the defect a round 1 review raised. An earlier draft fixed it by emitting after the sidecar's FIRST LINE, on the premise that every sidecar opens with its own `### <slug>` heading. THAT PREMISE IS FALSE FOR EXACTLY ONE FILE and the rule as written mandates a wrong result there:

```
for f in docs/plans/agent-scaffold.steps/*.md; do head -1 "$f" | grep -q '^#' || echo "$f"; done
```

prints `docs/plans/agent-scaffold.steps/core-assets.md`. That file opens with the lead-in sentence "Decisions carried from the resolved open questions:" and a bullet list, and its own `### \`core-assets\`:` heading sits at line 9. Under the first-line rule `render` would inject the intent between that sentence and the list it introduces, AND file it above the step's own heading. `core-assets` is the first step in the plan, so `## Step Details` opens directly on that prose.

THE RULE. `render` emits `problem` and `approach` immediately after the sidecar's FIRST HEADING LINE. When the sidecar carries no heading at all, `render` emits them before the body. No sidecar in this plan takes the second branch today, and a scaffolded project can, so both branches carry a golden. `render --check --strict` cannot catch a wrong placement on its own, because the projection is compared against whatever the code emits, so criteria 2, 3 and 4 pin it instead.

WHY NO EIGHTH SUBCOMMAND. `agent-flow --help` lists seven. A flag on `status` covers the read query at a fraction of the surface (Principle 2, Minimal by default).

WHAT AN UNKNOWN SLUG DOES, RULED HERE IN PROSE RATHER THAN LEFT IN A CRITERION. `status --step <unknown-slug>` reports the unknown slug and EXITS 0. The reason: `status --help` reads "Best-effort; a missing file yields a partial projection", and `status --source <plan> --plan /nonexistent.md` prints `note: --plan /nonexistent.md does not exist` and exits 0 today. An unknown slug and a missing file are the same class of resolution failure, so a strict exit on one and a best-effort exit on the other would split the subcommand's contract on no stated ground. A step with no intent recorded likewise reports the absence and exits 0, and after increment 3 that second case is unreachable while the first is not. The first draft of this step required a non-zero exit in a criterion while its own prose promised the best-effort stance, which is a design decision hidden in an acceptance criterion.

ACCEPTANCE CRITERIA.

1. `validate --source` accepts a plan with both fields, with one field, and with neither, and a test pins each. `validate --source` REJECTS a plan whose `problem` or `approach` contains a newline, with a red-then-green test for each field.
2. `cargo run -- render --check --strict docs/plans/agent-scaffold.plan.toml` passes, and the render golden fixture covers a step that carries both fields and a step that carries neither. In the golden, both intent lines for a step sit BELOW that step's own `###` heading and above the rest of its body.
3. THE GOLDEN COVERS A SIDECAR WITH PROSE ABOVE ITS HEADING. Add a fixture sidecar shaped like `core-assets.md`, with a paragraph, then a `### <slug>` heading, then a body. The golden pins that the intent lands after the heading and that the leading paragraph is not split. A test names `core-assets` by slug as the live instance of that shape, so the fixture cannot drift away from the case it stands for.
4. THE GOLDEN COVERS A SIDECAR WITH NO HEADING AT ALL, and pins that the intent renders before the body rather than being dropped.
5. The render golden covers a step that carries both fields and an EMPTY sidecar, and that step produces a Step Detail entry. `step_details_section` skips a step whose body is empty today, and increment 2 moves sentences out of sidecars, so a sidecar can become empty.
6. `next --json` carries both values in the active loop's context, and a test pins the key names.
7. `status --step <slug>` and `status --step <slug> --json` both print the two values. `status --step <unknown-slug>` PRINTS A NOTE NAMING THE SLUG THE USER PASSED, in the form the existing `--plan` path uses, and exits 0. A test pins the note text and the exit code, so an implementation that prints nothing cannot pass and the stance is not weakened later.
8. `cargo test` and `cargo clippy --all-targets -- -D warnings` exit 0.

### Increment 2, the cited backfill

RISK CLASS `risky` (two consecutive clean review rounds). THE GROUND: the increment authors two prose sentences for every step in the plan and moves the source text out of the sidecars, so a mistake is spread across the whole plan document and is not reversible by one revert once later edits land on top. The oracle for the sentences themselves is a reading, which is why criterion 4 bounds how much any one round carries.

WHAT IT DOES. Fill `problem` and `approach` for every step in the plan, `complete` steps included, because the reader who asks what a step was for asks it most often about finished work and most of the plan's steps are `complete`.

THE HUMAN REQUIREMENT THIS INCREMENT ANSWERS, stated on 2026-08-19: the git history must be combed so the information is extracted retroactively for existing steps. A design where the field is mandatory on new steps and empty on old ones does not satisfy it. WHAT THIS INCREMENT DELIVERS AGAINST THAT REQUIREMENT IS PROVENANCE AND NOT A PROOF OF DERIVATION, and the design pass records that as an accepted residual rather than claiming more. Rule 3 below states exactly what the check proves.

THE FIRST TASK IS A SIZING SAMPLE, NOT A BATCH. Rule 1 below claims that most steps already carry a transcribable problem sentence and a transcribable approach sentence, and NOTHING MEASURES THAT. The design pass states the gap plainly rather than papering it over with a figure, because "does this paragraph yield a transcribable sentence" is a reading and not a measurement. So the increment opens by sampling 20 sidecars across the length distribution and reporting the yield for the two fields SEPARATELY, and the review budget is sized from that result. The pass's own reading of the low end suggests the two behave differently: an approach sentence transcribes readily, and the problem half is the one that needs paraphrase for a minority of steps. `file-dropper.md`, the shortest sidecar in the plan at 54 words, states an approach and states no problem at all. CRITERION 1 ENFORCES THE SAMPLE, because an earlier draft named it in prose only and an implementer who skipped it satisfied every criterion.

A LINE COUNT IS NOT A LENGTH MEASURE HERE, and a reviewer's argument from one must be resisted. This repository does not hard-wrap prose (`no-wrap-convention`), so a sidecar paragraph is one line. Measure in words:

```
for f in docs/plans/agent-scaffold.steps/*.md; do printf "%s %s\n" "$(wc -w < $f)" "$f"; done | sort -n
```

THE FOUR RULES THAT MAKE THE EXTRACTION TRUSTWORTHY, in the order of how much each buys.

1. TRANSCRIBE BEFORE YOU PARAPHRASE. For most steps the problem and the approach are already written, in the sidecar prose, by the person who had the context at the time. `pack/plan-template.steps/example-step.md` asks for exactly that text: "What this step does and how; once done, the outcome and the evidence." So the first source for each step is its own sidecar, and git history supplies the citation for that text rather than a fresh derivation of it. Comb the history for the steps whose sidecar states neither, and for those the source is the commit or the decision receipt that does.
2. NAME THE SOURCE FOR EVERY STATEMENT, AND MARK HOW IT WAS TAKEN, IN A MIGRATION RECORD OUTSIDE THE PLAN. The human decided on 2026-08-21 (`q_id:"Q-78-backfillrecord"`) that the source reference and the mark do NOT enter the `[[step]]` schema. THE RECORD IS `docs/plans/step-intent-encoding.backfill-sources.tsv`, a tab-separated file whose first line is the header `slug	field	source	taken` and whose every later line carries four fields: the `[[step]].slug`, `problem` or `approach`, a source reference of the form `<commit>` or `<commit>:<path>`, and `transcribed` or `paraphrased`. The join key to the plan is `slug` plus `field`. THE RECORD LEAVES WITH THE MIGRATION: increment 3 deletes it, and criterion 4 of that increment pins the deletion. The ground is the design pass's own, which is also why it refuses a `[meta]` exemption field for the same backfill: migration bookkeeping must not outlive the migration. A second ground is that four extra lines on every `[[step]]` block would move the block-length pair the human weighed when choosing array position.
3. CHECK THE CITATION MECHANICALLY, OUTSIDE THE VALIDATOR. A `[[check]]` command in `.agents/checks.toml` reads the TSV, and for each row runs `git cat-file -e <commit>` for the commit form and `git show <commit>:<path> > /dev/null` for the path form. It cannot live in `validate`: `src/plan/source.rs` states in its own provenance comment that validation is a pure function over the string that never git-resolves a hash and never stats a path, and `commits` in `[step.provenance]` are shape-checked for that reason. For a row marked `transcribed` the check goes further and asserts that `git show <commit>:<path>` CONTAINS the sentence the plan carries for that slug and field. WHAT THAT PROVES, STATED EXACTLY BECAUSE AN EARLIER DRAFT OVERCLAIMED IT AS "A RELATIONSHIP PROOF": it proves WHICH COMMIT HELD THE TEXT. Under rule 1 the current sidecar is the primary source and criterion 6 requires the sentence to be MOVED, so the commit that satisfies the check is the tip before the backfill commit, by construction. That is provenance, not derivation, and no criterion here can distinguish the two. The stronger form is NOT applied to a `paraphrased` row, because a faithful paraphrase is trimmed or joined and a substring test would then fail on correct work.
4. REVIEW IN BOUNDED BATCHES. One statement per step in one review artefact is the shape this project's loop punishes hardest, and `docs/plans/agent-scaffold.ledger.md` records why in the paragraph headed "SIX-ROUND SCORECARD FOR THE PLAN FOLD": the diagnosed cause of that loop's length was a document assembled in layers whose characteristic defect was an aggregate that contradicted a detail elsewhere in the same document. A batch therefore carries a MAXIMUM OF 20 STEPS.

WHY A CITATION CONSTRAINT ALONE IS NOT ENOUGH, recorded so a reviewer does not read rule 2 as the whole guarantee. This project's measured failure mode is not a fabricated citation. The `workflow-enforcement-tier-endproperty-fold` waiver records that the sites which failed review shared one property, a claim STATED MORE GENERALLY THAN WHAT WAS MEASURED, and a citation check passes on such a claim. Rule 1 is what reduces the exposure, and criterion 5's reading is what carries the rest.

ACCEPTANCE CRITERIA.

1. THE SIZING SAMPLE RAN FIRST. 20 sidecars drawn across the word-count distribution produced by the command above, with the yield reported SEPARATELY for `problem` and for `approach`, recorded in the ledger BEFORE the first batch runs. The batch count in criterion 4 is derived from that result and the outcome states the derivation.
2. EVERY STEP CARRIES BOTH FIELDS, CHECKED PER BLOCK RATHER THAN BY A PAIR OF COUNTS. Run this from the repository root, once for `problem` and once with `approach` in place of both occurrences of `problem`:

```
awk '
/^\[\[(step|question)\]\]/ { if (instep && s != "" && !p) print "missing problem: " s; instep = ($0 ~ /step/); s=""; p=0; next }
/^slug = / { s=$3 }
/^problem = / { p=1 }
END { if (instep && s != "" && !p) print "missing problem: " s }
' docs/plans/agent-scaffold.plan.toml
```

Empty output is the oracle and it carries no literal count. It walks each `[[step]]` block separately and names the offending slug, so a step declaring `problem` twice cannot mask a step declaring none, which a pair of counts would permit. MEASURED before the backfill it prints one row per step, so it detects the condition rather than merely staying silent. `cargo run -- validate --source docs/plans/agent-scaffold.plan.toml` after increment 3's flip is the eventual oracle; this criterion is the one this increment carries for its own product.
3. THE MIGRATION RECORD COVERS EVERY STEP AND EVERY FIELD, IN BOTH DIRECTIONS. Two commands, each printing nothing and neither carrying a literal count. The first reports a step the record misses:

```
awk '
FILENAME ~ /backfill-sources/ { if (FNR > 1) { split($0, r, "\t"); have[r[1] SUBSEP r[2]] = 1 } next }
/^\[\[(step|question)\]\]/ { instep = ($0 ~ /step/); next }
/^slug = / && instep { slug = $3; gsub(/"/, "", slug); if (!((slug SUBSEP "problem") in have)) print "missing:", slug, "problem"; if (!((slug SUBSEP "approach") in have)) print "missing:", slug, "approach" }
' docs/plans/step-intent-encoding.backfill-sources.tsv docs/plans/agent-scaffold.plan.toml
```

The second reports a record row that names no step:

```
awk '{ split($0, r, "\t"); if (FNR > 1 && r[1] != "") print r[1] }' docs/plans/step-intent-encoding.backfill-sources.tsv | sort -u |
while read -r slug; do grep -q "^slug = \"$slug\"\$" docs/plans/agent-scaffold.plan.toml || echo "unknown slug: $slug"; done
```

Both were run against a three-row fixture before this criterion was written, and each reported exactly the seeded defect, so each detects its condition rather than merely staying silent. THE CITATIONS ALSO RESOLVE: the `[[check]]` command from rule 3 exits 0 over every row, and its `transcribed` rows additionally prove that the cited object contains the sentence. THE OUTCOME REPORTS THE `transcribed` AND `paraphrased` COUNTS PER BATCH, so a run that marks everything `paraphrased` and fires the stronger check zero times is visible in the record rather than silently compliant.
4. The batch boundaries are recorded in the ledger before the first batch runs, no batch exceeds 20 steps, and each batch carries its own review round.
5. Each statement is one sentence and states its claim in the direction the source states it. A reviewer checks this by reading the source, and no check can prove it. This criterion is a reading, which is why criterion 4 bounds how much of it any one round has to carry.
6. `cargo run -- render --check --strict docs/plans/agent-scaffold.plan.toml` passes, and the sidecar text that a transcribed sentence came from is MOVED rather than duplicated.
7. After the backfill, no sidecar contains its own step's `problem` or `approach` string verbatim, checked mechanically. This is a comparison between two fields of one plan, so it asserts nothing about whether a sentence is true and it stays on the admissible side of the line the design pass draws. It exists because the prose rule alone measurably failed once already: `docs/plans/agent-scaffold.documentation-protocol.md:5` already forbids repeating the status label, and 45 sidecars broke it.
8. ASCII ONLY. `LC_ALL=C grep -cP '[^\t\x20-\x7e]' <file>` prints 0 for every changed file, the TSV included. Use that pattern rather than `[^ -~]`, which matches every hard tab. Note `grep -c` exits 1 when the count is 0, so it breaks an `&&` chain. This increment authors roughly two prose strings per step, which is the largest single prose authoring in the plan.
9. `cargo test`, `cargo clippy --all-targets -- -D warnings` and `cargo run -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` exit 0.

### Increment 3, flip to required

RISK CLASS `risky` (two consecutive clean review rounds). THE GROUND: the increment makes both fields required, so every previously valid scaffolded plan fails to parse until its author edits it. That is squarely Principle 3, Safe on existing projects, and it is hard to roll back once a downstream author has edited. It also changes `pack/plan-template.plan.toml`, `pack/plan-template.documentation-protocol.md` and their committed copies under `docs/plans/`, which every scaffolded project inherits.

THE HUMAN DECISION THIS INCREMENT WAITED ON IS TAKEN (2026-08-21, receipt `q_id:"Q-78-requiredfields"`). `problem` AND `approach` ARE REQUIRED, IN THE SHIPPED PACK AS WELL AS HERE, over an optional field with a validation warning. The human rejected a third option, required here and optional in the pack. The human weighed the cost this increment states below, and accepted the residual that a placeholder satisfies a required field forever. So this increment builds what it already specifies, and it waits only on the review the whole step waits on.

WHAT IT DOES. Change both fields from `Option<String>` to `String` and delete the `Option` handling in `render`, `next` and `status`. Update the four TOML fixtures, `pack/plan-template.plan.toml` and `docs/plans/TEMPLATE.plan.toml` so a scaffolded project declares both fields from its first step. Delete `docs/plans/step-intent-encoding.backfill-sources.tsv` and the `[[check]]` entry that reads it, because the migration they serve is over.

ONE PACK PROSE CHANGE RIDES WITH THIS INCREMENT. `pack/plan-template.documentation-protocol.md` carries no sentence about a sidecar restating a `[[step]]` field, so no scaffolded project inherits the rule that this plan's own protocol states at `docs/plans/agent-scaffold.documentation-protocol.md:5`. Add one sentence there, SCOPED TO EXCLUDE THE HEADING: a step sidecar must not restate a `[[step]]` field other than in its heading, which `render` takes over in a later step. The unqualified form must not ship, because `pack/plan-template.steps/example-step.md:1` restates `slug` and `title` on its own first line, and so does almost every sidecar in this repository. It rides here rather than elsewhere because this increment already edits the pack, so it already owes the rendered-pair check below.

TWO RENDERED PAIRS ARE HAND-EDITED HERE AND NO GUARD COVERS EITHER. `pack/pack.toml` maps `plan-template.plan.toml` to `docs/plans/TEMPLATE.plan.toml` and `plan-template.documentation-protocol.md` to `docs/plans/TEMPLATE.documentation-protocol.md`, both as verbatim copies with no `render = true`, so each pair is byte-identical today. `src/agents_md_drift.rs` names "the `docs/plans/TEMPLATE` family" as UNGUARDED in its own coverage block, and `.agents/checks.toml` declares only `render-check`. Criterion 5 is the guard and it is `cmp`, not `just scaffold-self`: that recipe's second command is `nix fmt`, which formats the whole tree, and this tree is not formatter-clean, so the recipe reformats files this increment did not intend and breaks criterion 6 of this same increment until the implementer re-renders.

WHY THE MIGRATION RUNS THIS WAY. The alternative, land the fields as required and backfill every step in the same commit, has no optional window at all, which Principle 5 prefers. It is rejected on the review record in rule 4 above. The window in which absence is legal is one step long, and this increment closes it, so the end state makes absence unrepresentable and no `[meta]` exemption field is needed. An exemption boundary of the `[meta].w4_baseline` kind is right for a rule that will always have exempt members and wrong for a migration that finishes.

WHAT THIS COSTS A SCAFFOLDED PROJECT, STATED HERE AND WEIGHED BY THE HUMAN. After this increment, adding a step to any scaffolded plan requires two prose sentences before the plan parses, and for an exploratory step the problem statement is often the thing the step exists to find out. The pack template must ship placeholder values, because a required `String` needs one, so every scaffolded plan validates on day one carrying placeholder intent. The required field therefore makes ABSENCE unrepresentable and leaves MEANINGLESSNESS fully representable. A `validate` rule that rejects the placeholder strings is REJECTED: it would break criterion 3 below, which is correct under Principle 3, Safe on existing projects, and Principle 4, Idempotent. Placeholder detection, if wanted, belongs in `audit` and is a separate step.

ACCEPTANCE CRITERIA.

1. `validate --source` rejects a plan whose step omits either field, with a red-then-green test for each field.
2. `cargo run -- validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl` exits 0, which is the oracle that every step carries both.
3. `scaffold` into an empty directory produces a plan whose example step declares both fields, and the scaffolded plan validates.
4. THE MIGRATION RECORD IS GONE. `docs/plans/step-intent-encoding.backfill-sources.tsv` does not exist, and `.agents/checks.toml` declares no check that reads it. `test -e docs/plans/step-intent-encoding.backfill-sources.tsv` exits 1.
5. BOTH RENDERED PAIRS STILL AGREE. `cmp pack/plan-template.plan.toml docs/plans/TEMPLATE.plan.toml` and `cmp pack/plan-template.documentation-protocol.md docs/plans/TEMPLATE.documentation-protocol.md` each exit 0. Editing one side and not the other fails this criterion. Do NOT run `just scaffold-self` to satisfy it, for the reason stated above.
6. `cargo test`, `cargo clippy --all-targets -- -D warnings`, `cargo run -- render --check --strict docs/plans/agent-scaffold.plan.toml` and `cargo run -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` exit 0.

### THE RESIDUALS THIS STEP ACCEPTS RATHER THAN CLOSES

Three. Each is recorded so a later review round does not file it as a fresh finding, and each belongs in the eventual decision receipt. This is their single home; the design pass names them and points here.

- INTENT-PROSE STALENESS. `problem` and `approach` hold prose, and prose in a TOML string goes stale exactly as prose in Markdown does. Increment 2 criterion 7 closes the duplication case and increment 3 closes the absence case. Nothing closes the case where the recorded intent is no longer what the step is for, and no check can.
- MEANINGLESSNESS UNDER A REQUIRED FIELD. A placeholder sentence parses and validates, so a scaffolded project can carry placeholder intent indefinitely. `title` carries the same property today, and nobody raised it before this pass.
- THE CITATION PROVES PROVENANCE AND NOT DERIVATION. Rule 1 makes the current sidecar the primary source and increment 2 criterion 6 requires the sentence to be MOVED, so the commit that satisfies the `transcribed` check is the one that held the text before the move, by construction. No criterion here can distinguish that from a retroactive extraction, and no change to the criteria can, because the ambiguity comes from rule 1 rather than from the check. The human's 2026-08-19 requirement is answered in substance, because the recorded sentence IS the one the person with the context wrote and the citation names the commit that holds it. If the human wants genuine retroactive extraction TESTED, that is a different design and it must be put as one.

### NOT IN SCOPE, NAMED SO IT IS NOT DRAWN IN

- THE `order` DELETION. It belongs to `plan-order-array-position`, which BLOCKS this step.
- TYPED UMBRELLA MEMBERSHIP. It left the `Q-78` pass on 2026-08-21 and `Q-79` owns it. Nothing here waits on it.
- ANY CONTENT RULE OVER THE INTENT PROSE. `validate` checks presence and the single-line bound. It does not check that a sentence is true, and this step does not pretend that a check can. Increment 2 criterion 7 is a comparison between two fields of one plan and is not a content rule.
- PLACEHOLDER DETECTION IN `validate`. Rejected above. It belongs in `audit` and is a separate step.
- THE GENERATED STEP HEADING. `render` could own the `### <slug>: <title>` heading and every sidecar could lose its own. It rewrites every sidecar, which collides head-on with this step's backfill, so the design pass declines to schedule it.
- THE EMPTY QUESTION SIDECARS. All are 0 bytes and exist only to satisfy `render`'s existence check. The design pass records this under `Q-78` item (e) as a wart in the reader's contract rather than in this schema, and schedules nothing for it.
- THE `next` EXPLORATION-PHASE DEFECT, `Q-78` item (h). It keeps its own step and its own human decision.
