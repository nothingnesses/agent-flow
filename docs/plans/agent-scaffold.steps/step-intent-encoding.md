### `step-intent-encoding`: record each step's problem and approach as two required `[[step]]` fields, project them through `render`, `next` and `status --step`, and backfill every step from cited sources (`Q-78-requiredfields`, decided 2026-08-21, pending the review)

THIS STEP IS CONDITIONAL AND MUST NOT BUILD YET. `Q-78` is `open`, not `decided`. The human directed on 2026-08-19 that reviewers review the design pass before its outcome enters the plan as the plan's answer, so the review is what this step now waits on. THE ONE HUMAN DECISION THIS STEP DEPENDED ON IS TAKEN. `problem` and `approach` ARE REQUIRED, in the shipped pack as well as here, decided on 2026-08-21 with receipt `q_id:"Q-78-requiredfields"`. Increment 3 is the increment that decision governs, and it no longer waits on the human. The design pass is `docs/plans/step-intent-encoding.explorations/Q-78.md`, which carries the full reasoning, the rejected alternatives and the measurement appendix. This sidecar states what the step builds, in what order, and what each increment proves. It states no count of the plan's steps, because such a count expires and the plan's own standing cure, recorded in the ledger against orchestrator defect (12), is to carry the selecting command instead.

THIS STEP IS BLOCKED BY `plan-order-array-position`, and the direction is deliberate. Both steps rewrite every `[[step]]` block of the same file: the other step deletes a line from each and moves one block, and this step adds two lines to each. With both unblocked, `next` can select either, and whichever lands second rebases across a whole-file rewrite and gives its review round a diff dominated by the other step's churn. Deleting a field before adding two is the cheaper order, because the intent fields then never have to be threaded past a block move.

THE PROBLEM. A reader who asks what a step is for, and how it addresses that, opens a file. The `Step` struct carries `slug`, `title`, `status`, `order`, `blocked_by`, `folds`, `provenance`, `increment` and `waiver`, and none of them states the problem or the approach. `provenance` points at the artefacts that JUSTIFY a step, which is an adjacent fact. No subcommand answers the question: `status` prints counts, `next` names one step and its role prompt, and `render` emits the whole document.

THE APPROACH. Put the problem and the approach in the structured source as two single-line fields, project them through the three readers that already exist, and backfill every step from sources that are named rather than recalled.

### WHAT IT DOES

Record each step's intent as two required single-line `[[step]]` fields, `problem` and `approach`, project them through `render`, `next` and a new `status --step <slug>`, and backfill every existing step from cited sources (`Q-78-requiredfields`, human, 2026-08-21).

The step runs in three phases and eight increments. The fields land as `Option<String>` with their projections and their validation, so the plan still parses while the backfill runs. Six reviewed batches then fill every step, each batch with a migration record that names the source of every single field. The last increment flips the fields to required, ships the pack change, and deletes the migration record.

THE BACKFILL SPLITS INTO PER-BATCH INCREMENTS BECAUSE THE ROUND CAP IS HARD. One increment that covers every step needs six review batches inside one loop against a cap of five rounds. That guarantees either a forced escalation with a batch unreviewed, or a convergence certified while a batch is still owed. Each batch is its own increment with its own loop and its own record.

WHAT THIS STEP DOES NOT DO. It states no rule about what a sentence says. `validate` checks presence, emptiness and the single-line bound, and no check can judge truth. It generates no step heading. It deletes no empty question sidecar. It does not touch `next`'s loop selection, which belongs to the blocking step.

WHY TWO FIELDS AND NOT A VALIDATED SIDECAR SECTION, stated because the choice looks arbitrary otherwise. The measured drift in this plan is a STALE claim rather than an ABSENT one: 45 step sidecars restate `[[step]].status` in prose and 21 of them now contradict it. A required-section check would have caught NONE of the 21, because each of the 21 has the section and states it wrongly. A schema field catches absence and no more. Neither form catches staleness, and what removes staleness is the removal of the second copy, which is Principle 8, Structured data first, project for humans. Principle 5, Make illegal states unrepresentable, then decides between the two forms, because a required field makes a step with no stated problem fail to parse.

WHAT COUNTS AS INTENT, AND WHAT DOES NOT. The problem and the approach, one sentence each. The measured evidence, the alternatives rejected, the scope boundary, the priced cost and the executable acceptance criteria are NOT intent. They are the record of a decision, and they stay in the sidecar. The single-line bound is load-carrying in a second way: a multi-line field would grow every `[[step]]` block, and `plan-order-array-position` makes each block's length the cost of a reprioritisation. Two single-line fields add exactly two lines to a block whatever its length. No snapshot of the block length is restated here, because the relation carries the argument and the design pass states the priced pair once, with its command.

A CHARACTER CAP IS REJECTED: the quantity that carries the cost is the block's LINE count, and a single-line string of any length adds exactly one line.

### RULES

RULE 1, THE ENCODING. Two fields on `[[step]]`. `problem` states in one sentence the problem the step addresses. `approach` states in one sentence how the step addresses it. Both are single-line TOML strings, never `"""` or `'''` blocks.

RULE 2, THE BOUND IS ENCODED AND NOT LEFT AS A CONVENTION. `deny_unknown_fields` constrains keys and not values, so nothing today stops a ten-line `"""` block. `validate` therefore rejects a newline in either field, as a pure function over the deserialised string. That catches all three ways a newline arrives: a `"""` block, a `'''` block, and a `\n` escape inside a basic string. Principle 5, Make illegal states unrepresentable, decides it.

RULE 3, AN EMPTY VALUE IS ABSENCE SPELLED DIFFERENTLY, AND `validate` REJECTS IT. A required `String` accepts `""`, so a whole-plan backfill of empty strings survives the flip and satisfies any per-field presence check. `validate` therefore rejects a value that is empty after a trim. This is arithmetic over data the tool already loads and it asserts nothing about truth, so it sits on the admissible side of the line the design draws. MEASURED: with this rule, an empty backfill over the whole plan prints TWO PROBLEMS PER STEP and exits 1, which is `2 x $(grep -c '^\[\[step\]\]' docs/plans/agent-scaffold.plan.toml)` lines, 210 on the tree this sidecar was spliced into. The count is stated as the rule times the command rather than as a figure, because the figure expires the next time the plan gains a step.

RULE 4, TRANSCRIBE BEFORE YOU PARAPHRASE. The problem and the approach for most steps are already written down, in the sidecar prose, by the person who had the context. The first source for each step is its own sidecar, and git history supplies the citation for that text rather than a fresh derivation of it.

RULE 5, NAME THE SOURCE FOR EVERY FIELD, AND MARK HOW IT WAS TAKEN, OUTSIDE THE PLAN. The migration record is `docs/plans/step-intent-encoding.migration.tsv`. It is a tab-separated file with a header line and one row per FIELD, not per step. Its columns are `slug`, `field`, `mark`, `source`. `field` is `problem` or `approach`. `mark` is `transcribed` or `paraphrased`. `source` is `<commit>:<path>` and nothing else, where `<path>` is the path AS OF THAT COMMIT. The record lives outside the schema because migration bookkeeping must not outlive the migration, and increment 3 deletes it.

THE BARE `<commit>` SOURCE FORM IS DELETED FROM THE GRAMMAR. A `transcribed` row that cites a bare commit cannot run the substring check that makes `transcribed` mean anything, and the transcribed count does not reveal it. Every row carries `<commit>:<path>`, `paraphrased` included. A decision receipt is reachable as `<commit>:docs/metrics/workflow.jsonl`, so the bare form buys nothing. Principle 5, Make illegal states unrepresentable, decides it: a format that cannot express the unprovable row beats a check that hunts for it. The human decided on 2026-08-21 (`q_id:"Q-78-backfillrecord"`) that the source reference and the mark do NOT enter the `[[step]]` schema, and this record is where they live instead.

THE CITED PATH IS THE PATH AT THAT COMMIT, NOT TODAY'S PATH. This is measured. The step sidecar tree did not exist until `0fadd90` (2026-07-19). For `ledger-template` the earliest commit that holds its opening sentence is `5e7ee58` (2026-07-14), and at that commit the sentence lives in `docs/plans/agent-scaffold.md` alone. A row that cites `5e7ee58:docs/plans/agent-scaffold.steps/ledger-template.md` fails `git show`, and criterion 4 of the batch block reports it as `UNRESOLVED SOURCE`. Most transcribed rows for the older steps will therefore cite `<commit>:docs/plans/agent-scaffold.md`.

RULE 6, THE SOURCE IS THE EARLIEST COMMIT THAT HOLDS THE SENTENCE. Any commit that contains a sentence satisfies a naive citation check, and the latest such commit is usually the tip, which proves nothing. `git log --oneline --reverse -S'<sentence>' -- .` returns the earliest across renames. MEASURED, the earliest commit for two live sidecar sentences is `5e7ee58` (2026-07-14) and `c44d8d1` (2026-07-28), and at `5e7ee58` the only file that holds the sentence is `docs/plans/agent-scaffold.md`, because the sidecar tree did not exist until `0fadd90` on 2026-07-19.

RULE 7, THE PARAPHRASE ROUTE IS AN OPT-OUT, SO IT IS BOUNDED AND MEASURED. A faithful paraphrase is trimmed or joined, so a substring test fails on correct work, and the substring test is therefore not applied to a `paraphrased` field. Each batch reports its transcribed and paraphrased counts, so an implementation that marks every field `paraphrased` is visible rather than silently compliant.

WHAT A `paraphrased` ROW'S `source` COLUMN PROVES, STATED SO IT IS NOT READ AS MORE. On such a row R2 runs the resolution check and the relevance check and nothing else, so the column proves that the blob exists and that its path belongs to this step. It does not tie the recorded sentence to that blob in any way, and no command can. The bound is the count in criterion 5 and the reading in criterion 8, and criterion 8's side-by-side worklist covers the paraphrased rows' sources for exactly that reason.

RULE 8, THE SENTENCE MOVES OUT OF THE SIDECAR. After a step is backfilled, its sidecar must not contain its own `problem` or `approach` string verbatim. This is a pure string comparison inside one plan, it needs no git resolution, and it catches the transcribe-then-forget-to-delete case. It is the guard duty (g) owes.

RULE 9, NO INTENT VALUE OPENS WITH A ROADMAP STATUS LABEL. A sidecar opening that carries a status LABEL is that step's first source under rule 4, so a transcription that starts at the opening word writes the label into the TOML. That re-creates the duplicate `sidecar-status-opening-drift` deletes. The transcription starts after the label.

THE RULE REACHES A LEADING LABEL AND NOT A LEADING ORDINARY ADJECTIVE, AND THE ANCHORED SELECTOR IS WHAT SEPARATES THE TWO. `sidecar-status-opening-drift` criterion 1 states that anchor, criterion 6's R3 regex reuses it, and that sidecar enumerates by slug the adjectival openings it excludes, every one of them declared `deferred`. Transcribing such an opening from its first word is CORRECT, and rewriting it to satisfy this rule mutilates a legitimate problem statement. NO POPULATION FIGURE IS WRITTEN HERE, AND AN EARLIER FORM STATED 45: that is the RELAXED selector's count and it includes exactly those adjectival openings, so the rule asserted of all 45 something that is false of nine. The population is what the ANCHORED selector prints on the day, and it is smaller again by the time a batch runs, because `sidecar-status-opening-drift` is declared ahead of this step and deletes the label from its own worklist first.

RULE 10, THE RENDER FORMAT IS FROZEN BY A GOLDEN BEFORE THE LIVE PLAN GAINS ONE VALUE. `render --check --strict` is a byte comparison over the whole document, so the first implementer's format choice becomes the golden and every other correct-in-spirit form becomes a hard failure. Increment 1 therefore pins the format in `src/plan/testdata/render-fixture.md`, where the plan carries no intent at all, so the first batch inherits a fixed format rather than invents one.

WHY A CITATION CONSTRAINT ALONE IS NOT ENOUGH, recorded so a reviewer does not read rule 5 as the whole guarantee. This project's measured failure mode is not a fabricated citation. The `workflow-enforcement-tier-endproperty-fold` waiver records that the sites which failed review shared one property, a claim STATED MORE GENERALLY THAN WHAT WAS MEASURED, and a citation check passes on such a claim. Rule 4 is what reduces the exposure, and the batch block's criterion 8 reading is what carries the rest.

THE INCREMENTS ARE DECLARED IN THE PLAN TOML as `[[step.increment]]` entries with their risk classes, so a round record joins to them structurally rather than by a lexical prefix (Principle 8). EACH CLASS STATES ITS GROUND, in the shape `test-tmpdir-repo-assumption.md` uses, because a class sets the required clean-round count and a class asserted without a ground is the defect this pass polices elsewhere (Principle 6, Ground decisions in evidence). AN EARLIER DRAFT CLASSED INCREMENTS 1 AND 3 `low_risk` AND STATED NO GROUND FOR ANY OF THEM. Both were corrected against the `AGENTS.md` test after a review round measured the inversion: a pure prose sweep in the sibling step was `risky` while an increment touching four source files and a new CLI surface was `low_risk`. THE BACKFILL THEN SPLIT FROM ONE INCREMENT INTO SIX, so the step declares eight increments rather than three, and every one of the eight is `risky`.

### Increment 1, `step-intent-encoding-inc1`: the optional fields and the three projections

RISK CLASS `risky` (two consecutive clean review rounds). THE GROUND: the increment changes the plan schema (`src/plan/source.rs`), the generated document for every project (`src/plan/render.rs`), the `context` block that `next` hands an agent as an instruction rather than a report (`src/next.rs`), a new CLI flag with a stated exit-code contract (`src/main.rs:496`), and it adds a new `validate` rejection rule. It changes product behaviour and it ships to every scaffolded project, which is the "widely depended on" clause of the `AGENTS.md` test. `workflow-enforcement-tier.md` is the plan's own precedent that `next`'s output being an instruction rather than a report is a blast-radius argument.

THE RULES THIS INCREMENT IMPLEMENTS, STATED SO A BYTE COMPARISON HAS SOMETHING TO COMPARE AGAINST.

THE SCHEMA. `Step` gains `problem: Option<String>` and `approach: Option<String>`, both `#[serde(default, skip_serializing_if = "Option::is_none")]`, declared immediately after `status`. An existing step deserialises to `None` and re-serialises to nothing, so the plan is byte-identical until a batch fills it.

`validate`. Two rules per field, in this order. An empty-after-trim value gives:

```
step `<slug>` field `problem` is empty
```

```
step `<slug>` field `approach` is empty
```

A value that contains `\n` or `\r` gives:

```
step `<slug>` field `problem` must be a single line
```

```
step `<slug>` field `approach` must be a single line
```

All four strings appear on stderr, prefixed by the source path and a colon and a space, and `validate` exits 1. The four strings are given once each rather than as one string with a field name to substitute.

`render`. `step_details_section` emits, immediately after the sidecar's LEADING HEADING LINE, one blank line and then these two lines:

```
- problem: <the problem value>
- approach: <the approach value>
```

followed by one blank line and then the rest of the body. Each value passes through the existing `one_line` helper before emission, so no value can break the line structure even before the validate rule lands. Four sub-rules complete the format:

- THE LEADING HEADING LINE IS THE FIRST LINE WHOSE FIRST CHARACTER IS `#`, not the first line of the file. One sidecar, `core-assets`, carries a lead-in sentence and a bullet list above its own heading, which sits at line 9.
- A BODY WITH NO HEADING LINE takes the two lines first, then a blank line, then the body.
- A STEP THAT CARRIES ONLY ONE FIELD emits only that line.
- A STEP THAT CARRIES AT LEAST ONE FIELD CONTRIBUTES AN ENTRY EVEN WHEN ITS BODY IS EMPTY. A step with neither field and an empty body contributes nothing, which is today's behaviour unchanged. THAT SECOND CASE CEASES TO EXIST AT INCREMENT 3, where no step can carry neither field, so from that increment on the sentence describes a state nobody can build.

THIS SUB-RULE COLLIDES WITH A NAMED EXISTING TEST, AND THE COLLISION FIRES AT INCREMENT 3 RATHER THAN HERE. `empty_details_sections_emit_no_bare_heading` in `src/plan/render.rs`, marked `N1` in its own comment, asserts that `## Step Details` is ABSENT for a plan whose one step has an empty body. MEASURED, that test's inline `[[step]]` fixture is one of the declaration sites increment 3 criterion 2 requires to carry both fields: `grep -nE '(\\n|^)slug = ' src/plan/render.rs` prints three sites and the `N1` fixture is the first of them. At increment 1 the fixture carries neither field, so this sub-rule's second sentence holds and the test passes unchanged. At increment 3 the fixture carries both, so this sub-rule makes the section appear and the assertion inverts. INCREMENT 3 CRITERION 2 NAMES THE TEST AND STATES THE DIRECTION. Do not delete the test, in the shape `plan-order-array-position` increment 1 uses for `ordering_is_numeric_for_questions_and_slug_tiebroken_for_equal_order_steps`.

REPRODUCE THE ONE SIDECAR THAT FORCES THE LEADING-HEADING RULE, so the sub-rule above is checked rather than trusted:

```
for f in docs/plans/agent-scaffold.steps/*.md; do head -1 "$f" | grep -q '^#' || echo "$f"; done
```

It prints `docs/plans/agent-scaffold.steps/core-assets.md` and nothing else. That file opens with the lead-in sentence "Decisions carried from the resolved open questions:" and a bullet list, and its own heading sits at line 9. `core-assets` is the first step in the plan, so `## Step Details` opens directly on that prose, and a first-line rule would file the intent above the step's own heading.

`next`. `StepInfo` gains `problem: Option<String>` and `approach: Option<String>`. `steps_from_toml` copies them. `steps_from_markdown` sets both to `None`, because the Markdown Roadmap carries no such column, and the parity comment on that function records it. `LoopFacts` carries both, and `build_context` inserts a `problem` slot and an `approach` slot when the field is present, in every loop state. The context map is a `BTreeMap`, so the six slots print in this order: `approach`, `isolation_tier`, `ledger`, `problem`, `review_findings`, `triage_findings`.

`status`. `StatusArgs` gains `--step <slug>`, declared `conflicts_with = "resume"`. For a step the source declares, the command prints exactly three lines on stdout and exits 0:

```
step: <slug>
problem: <the problem value>
approach: <the approach value>
```

For a field the substrate does not carry, the value prints as `(not recorded)`, so an absent field is never mistaken for an empty one. For a slug the source declares no step for, the command prints one line on stdout and exits 0, which keeps the documented best-effort stance:

```
step: <slug> not in this plan
```

WHY NO EIGHTH SUBCOMMAND. `agent-flow --help` lists seven. A flag on `status` covers the read query at a fraction of the surface (Principle 2, Minimal by default).

WHY AN UNKNOWN SLUG EXITS 0, RULED HERE IN PROSE RATHER THAN LEFT IN A CRITERION. `status --help` reads "Best-effort; a missing file yields a partial projection", and `status --source <plan> --plan /nonexistent.md` prints `note: --plan /nonexistent.md does not exist` and exits 0 today. An unknown slug and a missing file are the same class of resolution failure, so a strict exit on one and a best-effort exit on the other would split the subcommand's contract on no stated ground. A step with no intent recorded likewise reports the absence and exits 0, and after increment 3 that second case is unreachable while the first is not. The first draft of this step required a non-zero exit in a criterion while its own prose promised the best-effort stance, which is a design decision hidden in an acceptance criterion.

THE CHANGED-PATH SET. `src/plan/source.rs`, `src/plan/render.rs`, `src/next.rs`, `src/main.rs`, `src/plan/testdata/render-fixture.plan.toml`, `src/plan/testdata/render-fixture.md`, `src/plan/testdata/render-fixture.steps/gamma.md`. No other file changes. In particular `docs/plans/agent-scaffold.plan.toml` does NOT change, and neither does `docs/plans/agent-scaffold.md`, because no live step carries a field yet.

The 69 inline `[[step]]` declaration sites do NOT change in this increment, because both fields are optional. They all change in increment 3.

ACCEPTANCE, EACH EXECUTABLE.

1. THE SCHEMA CARRIES BOTH FIELDS AND THEY ARE OPTIONAL. `./target/debug/agent-flow validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl` prints a `docs/plans/agent-scaffold.plan.toml: <N> steps, 80 questions, valid` line and exits 0, against a plan where no step carries either field. `grep -c 'problem: Option<String>' src/plan/source.rs` prints `1`.

2. THE SINGLE-LINE RULE FIRES ON ALL THREE WAYS A NEWLINE ARRIVES, AND IT FIRES FOR EACH FIELD. Build SIX one-step plans in a scratch directory outside the repository. For `problem`, one with a `"""` block value, one with a `'''` block value and one with a `\n` escape inside a basic string. Then the same three for `approach`. Run `./target/debug/agent-flow validate --source <file>` on each of the six. Each exits 1 and prints nothing on stdout.

Each of the three `problem` files prints, on stderr, a line that ends with this string:

```
step `a` field `problem` must be a single line
```

Each of the three `approach` files prints, on stderr, a line that ends with this string:

```
step `a` field `approach` must be a single line
```

THE TWO STRINGS ARE GIVEN ONCE EACH RATHER THAN AS ONE STRING WITH A FIELD NAME TO SUBSTITUTE, and that is why this criterion runs six files rather than three. RULE 2 reads that `validate` rejects a newline in EITHER field, so an implementation that applies the rejection to `problem` alone satisfies a three-file form of this criterion, satisfies criterion 3, which already runs both fields, and satisfies every other criterion of this increment and of increment 3, while RULE 2 and the Principle 5 it cites are false of it on half their subject. Criterion 13's `approach` single-line test is the same guard in the suite.

MEASURED on the `"""` form and the `\n` form, the whole stderr line is that string with `<file>: ` in front of it. The strings are given inside fenced blocks rather than inline, because an inline form needs a backslash before each backtick, CommonMark keeps the backslash as a literal character, and `render` inlines this sidecar verbatim, so a reviewer comparing real output against the printed string sees a mismatch that the implementation did not cause.

3. THE EMPTY-VALUE RULE FIRES PER FIELD. A one-step plan with `problem = ""` and `approach = ""` gives two stderr lines and exit 1:

```
<file>: step `a` field `problem` is empty
<file>: step `a` field `approach` is empty
```

MEASURED at whole-plan scale, `problem = ""` and `approach = ""` across every step of the live plan gives exit 1 and exactly `2 x $(grep -c '^\[\[step\]\]' docs/plans/agent-scaffold.plan.toml)` stderr lines, which is 210 on the tree this sidecar was spliced into and was 202 when the rule was first measured against a 101-step tree. The outcome records both the step count and the line count, so the pair reproduces on the day rather than expiring. This is the criterion that closes the measured trap where an empty backfill survives the required-field flip.

4. THE RENDER FORMAT IS PINNED IN THE GOLDEN. `src/plan/testdata/render-fixture.plan.toml` gains both fields on `alpha`, both on `gamma`, and `problem` ALONE on `eta`, which is the fixture criterion 6 reads, and the golden is regenerated. AN EARLIER FORM READ "BOTH on `eta` with only one of them filled", AND NO CORRECT IMPLEMENTATION SATISFIES IT ALONGSIDE CRITERION 6. An `approach` key present and empty is a value RULE 3 rejects, and once `eta` carries both keys the render sub-rule for a step that carries only one field stops applying to it, so `render` emits an `- approach: ` line where criterion 6 requires the fourth line to be blank. The two criteria could not both be met. Criterion 6 states the intent unambiguously and it is the criterion the render sub-rule needs a fixture for, so criterion 6 is the one that stands and this sentence is corrected to match it. Then:

```
grep -c -F -- '- problem: The render golden pins no projected intent.' src/plan/testdata/render-fixture.md
```

Pass: stdout is exactly `1` and the exit status is 0. A missing golden file prints nothing on stdout and exits 2, so an absent input cannot pass.

THIS CRITERION IS THE ONE THAT CATCHES THE `title` TRAP. MEASURED against an implementation that adds both fields to the schema and emits neither, `cargo test` reports 0 failures, `validate --source` exits 0 and prints `7 steps, 5 questions, valid`, `render --check --strict` exits 0 and prints `up to date`, and `status --step alpha` prints both values correctly. This grep prints `0` and exits 1. Nothing else in the increment detects it.

5. THE LEADING-HEADING RULE IS PINNED BY A SIDECAR WITH PROSE ABOVE ITS HEADING. `src/plan/testdata/render-fixture.steps/gamma.md` takes a lead-in sentence above its own `###` heading, the `core-assets` shape. Then:

```
grep -A5 -F -- 'A lead-in sentence above the step' src/plan/testdata/render-fixture.md
```

Pass: SIX printed lines, in this order: the lead-in sentence, a blank line, the `gamma` heading line, a blank line, a `- problem:` line, a `- approach:` line. THE LAST TWO ARE THE CRITERION, because they are what proves the intent went BELOW the heading, and `-A3` stops before them. The failing implementation to look for emits the intent after line 1, which puts it above the heading. This command also pins the rendered PAIR ORDER, which nothing else in the increment does; criterion 7 pins the order in the context map and the two surfaces are separate.

6. THE PARTIAL CASE IS PINNED. `eta` carries `problem` and no `approach` in the fixture. Run:

```
grep -A3 -F -- '### `eta`: The deferred step' src/plan/testdata/render-fixture.md
```

Pass: FOUR printed lines, the heading, a blank line, a `- problem:` line and a BLANK line. THE FOURTH LINE IS THE CRITERION. MEASURED with `-A3` against an implementation that emits `- approach: (not recorded)` for `eta`, the fourth line is that `- approach:` line instead; measured with `-A2` against the same pair, the two outputs are byte-identical, so the negative half of this criterion is untestable at `-A2`.

7. `next` CARRIES BOTH SLOTS, ON BOTH SURFACES. Build a one-step in-progress plan with both fields in a scratch directory, then run both of these. They are two commands because `next`'s human form is what an agent reads as an instruction, which is the increment's own risk ground, and the JSON form is what a tool reads.

```
./target/debug/agent-flow next --source intent.plan.toml --json | grep -oE '"(problem|approach)": "[^"]*"'
```

Pass: two lines on stdout, `"approach": "<value>"` then `"problem": "<value>"`, in that order, exit 0.

```
./target/debug/agent-flow next --source intent.plan.toml | grep -cE '^    (problem|approach): '
```

Pass: stdout is exactly `2`. MEASURED BEFORE THE CHANGE, against the live plan, that command prints `0` and exits 1, while the same command widened to all six slot names prints `4`. An implementation that adds both fields to `StepInfo` and to the JSON while leaving `build_context` untouched satisfies the JSON command and fails this one, and nothing else in the increment reaches the human surface.

8. `status --step` ANSWERS FOUR WAYS, AND EACH IS RUN. Four commands, given once each.

```
./target/debug/agent-flow status --source good.plan.toml --step a
```

Pass: stdout is exactly the three lines `step: a`, `problem: A stated problem.`, `approach: A stated approach.`, stderr is empty, exit 0.

```
./target/debug/agent-flow status --source good.plan.toml --step nope
```

Pass: stdout is exactly `step: nope not in this plan`, exit 0.

```
./target/debug/agent-flow status --source no-intent.plan.toml --step a
```

Pass: stdout is exactly the three lines `step: a`, `problem: (not recorded)`, `approach: (not recorded)`, exit 0.

```
./target/debug/agent-flow status --source good.plan.toml --step a --resume
```

Pass: stderr carries `error: the argument '--step <STEP>' cannot be used with '--resume'` and the exit status is 2.

AND NO EIGHTH SUBCOMMAND WAS ADDED, which is the executable form of the Principle 2 ruling above rather than a promise in prose:

```
./target/debug/agent-flow --help | sed -n '/^Commands:/,/^$/p' | grep -cE '^  [a-z]+ '
```

Pass: stdout is exactly `8`, the seven subcommands plus `help`. MEASURED BEFORE THE CHANGE it prints `8` as well, so this is a bar rather than a detector, the same shape increment 3 criterion 10 uses; an implementation that answers the read query with a new subcommand as well as the flag prints `9`.

9. THE LIVE PROJECTION IS UNCHANGED. `./target/debug/agent-flow render --check docs/plans/agent-scaffold.plan.toml --strict` prints `docs/plans/agent-scaffold.plan.toml: up to date` and exits 0, and `git diff --name-only` over the increment does NOT list `docs/plans/agent-scaffold.md` or `docs/plans/agent-scaffold.plan.toml`. Both halves are the criterion.

10. THE BATCH BOUNDARIES ARE CAPTURED AND RECORDED IN THIS INCREMENT. Run:

```
N=$(grep -c '^\[\[step\]\]' docs/plans/agent-scaffold.plan.toml)
K=1; while [ $(( (N + K - 1) / K )) -gt 20 ]; do K=$((K+1)); done
S=$(( (N + K - 1) / K ))
printf 'steps=%d batches=%d size=%d\n' "$N" "$K" "$S"
```

The rule is: K is the smallest batch count whose batch size is 20 or less, and the batch size S is `ceil(N/K)`. Batch i covers declaration positions `(i-1)*S+1` to `min(i*S, N)`, and declaration position is the plan order because the blocking step deleted `order`. The outcome records the printed line and the per-batch slug list from:

```
sed -n 's/^slug = "\(.*\)"$/\1/p' docs/plans/agent-scaffold.plan.toml | awk -v s="$S" '{printf "%d\t%s\n", int((NR-1)/s)+1, $0}'
```

MEASURED at N=101, the rule gives `steps=101 batches=6 size=17`, and the slug list splits 17, 17, 17, 17, 17, 16. The rule holds at six batches for any N from 101 to 120, so the split of `sidecar-status-opening-drift` does not change the count. MEASURED AGAIN at N=105, the tree this sidecar was spliced into, the rule prints `steps=105 batches=6 size=18`.

THE SIX `[[step.increment]]` ENTRIES ARE ALREADY DECLARED, `step-intent-encoding-inc2a` to `step-intent-encoding-inc2f`, all `risky`, authored in the plan pass rather than in this increment. So K is CHECKED against the declarations rather than used to create them. `grep -c 'id = "step-intent-encoding-inc2' docs/plans/agent-scaffold.plan.toml` prints `6`, and the `batches` field of the printed line equals `6`. A disagreement means the plan grew past 120 steps and the declarations need a planner pass before any batch runs. Capture the boundaries here rather than in the first batch, because a boundary chosen inside batch 1 is a boundary batch 1 marks its own homework against.

11. THE CHANGED PATH SET. `git diff --name-only` lists exactly `src/plan/source.rs`, `src/plan/render.rs`, `src/next.rs`, `src/main.rs`, `src/plan/testdata/render-fixture.plan.toml`, `src/plan/testdata/render-fixture.md` and `src/plan/testdata/render-fixture.steps/gamma.md`. `docs/plans/agent-scaffold.plan.toml` does NOT appear, because the six batch increments are declared in the plan pass rather than here, and no `[[step]]` field changes in this increment.

12. THE SUITE, THE VALIDATORS AND ASCII. `cargo test` passes, `cargo clippy --all-targets -- -D warnings` exits 0, both `validate` invocations print their `valid` line and exit 0, and `LC_ALL=C grep -cP '[^\t\x20-\x7e]' <file>` prints `0` for every changed file.

13. RULE 2 AND RULE 3 ARE PINNED IN THE SUITE, ONE TEST PER RULE PER FIELD. `src/plan/source.rs` gains four unit tests in its own `mod tests`, named `validate_rejects_an_empty_problem`, `validate_rejects_an_empty_approach`, `validate_rejects_a_multi_line_problem` and `validate_rejects_a_multi_line_approach`. Each builds a one-step plan carrying the defect its name states, calls `validate_source`, and asserts that the returned problems carry that field's own string from the `validate` block above. NO PATH JOINS CRITERION 11'S SET, because `src/plan/source.rs` is already in it.

WHY THIS IS A CRITERION AND NOT LEFT TO `cargo test`. Criterion 12 runs whatever tests exist, and nothing else in either increment obliges either rule to have one: criterion 11 names no test file, and increment 3 rewrites the code that implements both rules. Increment 3's own stated edit taken literally, turning the two `if let Some` arms into direct reads and dropping the check bodies, leaves BOTH halves of increment 3's ground true, because both fields are still required and every previously valid plan still fails to parse, while RULE 2, RULE 3 and the Principle 5 both cite are false of the result. A hand-run command at increment 1 says nothing about the state of the code after increment 3 rewrites it, which is why the pair lives in the suite. The metrics log's own empty-field rejections are already pinned this way in `src/metrics.rs`, and the `[[step]]` rules get the same treatment here.

THE GROUND SPLITS INTO A PREMISE AND A CONSEQUENCE, AND THE CRITERION RUNS AGAINST BOTH HALVES. THE PREMISE: each of the four tests fails when the rejection it names is removed. THE CONSEQUENCE: four functions with those names exist and `cargo test` passes. A grep can only reach the consequence, so a RED measurement carries the premise.

```
grep -c 'fn validate_rejects_a' src/plan/source.rs
```

Pass: stdout is exactly `4`.

THEN THE RED MEASUREMENT, WHICH IS PART OF THE CRITERION AND NOT A NOTE. Delete the empty-after-trim check and the newline check from `validate_source`, leaving both fields read and every other rule in place, run `cargo test --bin agent-flow validate_rejects_a`, and record the output in the outcome. Pass: ALL FOUR named tests FAIL under the deletion. Restore the two checks and show the four green again. This is the shape `plan-order-array-position` increment 1 criterion 5 uses for its own three arms.

WHY BOTH HALVES ARE LOAD-CARRYING. Four correctly named tests that assert nothing satisfy the grep and survive the deletion, so only the RED measurement refuses them. Four tests that pin `problem` on both rules and stub the two `approach` names satisfy the grep and fail the RED measurement on two of the four, which is why the pass condition is ALL FOUR rather than a count of failures.

### Increments 2a to 2f, `step-intent-encoding-inc2a` and the rest: the cited backfill, one batch each

RISK CLASS `risky` FOR EVERY ONE OF THE SIX (two consecutive clean review rounds each). THE GROUND, WHICH IS THE SAME FOR EACH: a batch authors two prose sentences for up to 18 steps and MOVES the source text out of those sidecars, so a mistake spreads across the published plan document and is not reversible by one revert once a later batch lands on top. The oracle for the sentences themselves is a reading, which is what the batch split bounds. The batch split does not lower the class: it lowers how much any one review round carries, and each batch still ships prose into every scaffolded reader's copy of the plan.

Each batch increment carries the SAME criteria. The batch letter and its slug list come from increment 1 criterion 10. Criterion 2 runs in batch a only.

WHAT ONE BATCH DOES. For every step in the batch, fill `problem` and `approach`, append one row per field to `docs/plans/step-intent-encoding.migration.tsv`, delete the transcribed sentence from the step's sidecar, and regenerate the rendered plan. Nothing else changes.

THE MIGRATION RECORD. The file carries this header line, with real tab characters:

```
slug	field	mark	source
```

and one row per field, in the same four columns. Batch a creates the file with its header. Every later batch appends rows and leaves the earlier rows untouched.

ACCEPTANCE, EACH EXECUTABLE. The three check scripts below are stated once here and run once per batch. Save each to a scratch file OUTSIDE the repository. Run them under bash. Each uses process substitution, so it cannot run in nu.

1. THE BATCH IS EXACTLY ITS DECLARED SLUG LIST. `git diff --name-only` over the increment lists exactly: `docs/plans/agent-scaffold.plan.toml`, `docs/plans/step-intent-encoding.migration.tsv`, `docs/plans/agent-scaffold.md`, and one file under `docs/plans/agent-scaffold.steps/` for each step in the batch that had a sentence to move.

THE COUNT AND THE IDENTITY ARE TWO SEPARATE CHECKS AND BOTH RUN. The count, over both fields, from the pre-increment tree and again after:

```
printf 'problem=%d approach=%d\n' "$(grep -c '^problem = ' docs/plans/agent-scaffold.plan.toml)" "$(grep -c '^approach = ' docs/plans/agent-scaffold.plan.toml)"
```

Pass: each post count minus its pre count equals the batch size, and the two counts are equal to each other. The outcome records both pairs. Both fields are counted because a batch that fills `problem` and forgets `approach` satisfies a single-field check.

`m` IS DEFINED HERE, ONCE, AND CRITERIA 6 AND 7 READ IT FROM HERE RATHER THAN RESTATING IT. `m` is the POST count of `^problem = ` this command prints, which the pass condition above requires to equal the post count of `^approach = `. It is NOT the number of steps carrying at least one filled field, and the two agree only when every filled step carries both. AN EARLIER FORM LEFT `m` UNDEFINED WHERE CRITERION 6 USES IT AND UNNAMED WHERE CRITERION 7 USES IT, so against a batch that fills one field on twice as many steps the `checked` clause PASSED under one reading and REFUSED under the other, and which reading a reader happened to take decided the outcome. A clause that only refuses a wrong implementation on one of its available readings has not refused it.

THE BATCH-SIZE HALF OF THAT CLAUSE READS FALSE FOR THE LAST BATCH, AND THAT IS AN ACCEPTED RESIDUAL RATHER THAN A REPAIR. Increment 1 criterion 10 defines batch i as declaration positions `(i-1)*S+1` to `min(i*S, N)`, so the last batch covers `N - (K-1)*S`, which is FEWER than `S` whenever `S` does not divide `N`. Read literally, a correct last batch fails the count clause and the implementer must stop and ask, or override the clause without a record. The human accepted this on 2026-08-21 as residual risk, receipt `type:"decision"` `q_id:"Q-78-residuals"` in `docs/metrics/workflow.jsonl`. THE CONSEQUENCE THE HUMAN WEIGHED: nothing wrong can ship, because the IDENTITY check below is a separate check against the batch's declared slug list, and it binds correctly at the last batch's real size. The cost accepted is one avoidable escalation, or one unrecorded override, at the last batch.

The identity, which is what makes the criterion's own heading true. IT RUNS OVER BOTH FIELDS AND NOT OVER `problem` ALONE, for the reason the count half already states in its own last sentence. Capture the filled slug set PER FIELD before and after, and compare each against the batch's declared slug list from increment 1 criterion 10:

```
sed -n 's/^slug = "\(.*\)"$/\1/p' docs/plans/agent-scaffold.plan.toml | awk -v s="$S" -v b="$B" '{if (int((NR-1)/s)+1 == b) print}' | sort > declared.txt
for field in problem approach; do
  awk -v f="^$field = " '/^slug = /{s=$0} $0 ~ f {print s}' docs/plans/agent-scaffold.plan.toml |
    sed -n 's/^slug = "\(.*\)"$/\1/p' | sort > "filled-$field-post.txt"
  comm -13 "filled-$field-pre.txt" "filled-$field-post.txt" > "gained-$field.txt"
  printf '%s declared=%d gained=%d outside=%d missing=%d\n' "$field" \
    "$(wc -l < declared.txt)" "$(wc -l < "gained-$field.txt")" \
    "$(comm -13 declared.txt "gained-$field.txt" | wc -l)" \
    "$(comm -23 declared.txt "gained-$field.txt" | wc -l)"
done
```

where `B` is the batch number, `S` the batch size, and each `filled-<field>-pre.txt` is the same per-field capture run against the pre-increment tree. Pass, on BOTH printed rows: `gained` equals `declared`, `outside=0` and `missing=0`. Run it under bash, as with the other scripts in this block.

MEASURED, a count-only check passes on a batch that fills the right NUMBER of steps from the wrong part of the plan, and `outside` is what reports that. THE SECOND ROW IS WHAT REFUSES THE SPLIT-FIELD BATCH, and a `problem`-only identity check does not. An implementation that fills `problem` on its own declared slugs and `approach` on as many steps drawn from a LATER batch satisfies the count clause, because both counts rise by the batch size and stay equal to each other, and it satisfies a `problem`-only identity check in full. It falsifies this block's shared risk ground on the premise half, that a batch authors two prose sentences FOR ITS OWN STEPS, while the consequence half holds whole, because the prose still ships into the published plan and is still not reversible by one revert. On that implementation the `approach` row prints `outside` and `missing` each equal to `declared`, and no figure is written here because the batch size moves with the plan.

2. THE SIZING SAMPLE RUNS FIRST, IN BATCH a ONLY, AND IT REPORTS THE TWO FIELDS SEPARATELY. Before any field is filled, take the first ten steps of batch a, read each sidecar, and record in the outcome, for `problem` and for `approach` separately, how many of the ten yield a transcribable sentence and how many need a paraphrase. The design's own claim that most steps already state their intent is UNMEASURED, and this sample is the measurement. It is an acceptance criterion rather than a paragraph, because a named remedy that no criterion enforces is a remedy an implementer can skip. The recorded pair is what later batches are read against under criterion 8. One known case is named so the sample is not read as a formality: `file-dropper.md`, the shortest sidecar in the plan, states an approach and states no problem at all.

3. THE RECORD'S SHAPE AND ITS COVERAGE OF THE PLAN. Run:

```
#!/usr/bin/env bash
# R1: the migration record's shape, its per-field distinctness, and its coverage of the filled fields.
REC="$1"; PLAN="$2"; AF="$3"
rows=0; bad=0
keys=$(mktemp)
if [ "$(head -1 "$REC" 2>/dev/null)" != "$(printf 'slug\tfield\tmark\tsource')" ]; then
  echo "BAD HEADER"; bad=$((bad+1))
fi
while IFS=$'\t' read -r slug field mark source; do
  rows=$((rows+1))
  printf '%s\t%s\n' "$slug" "$field" >> "$keys"
  case "$field" in problem|approach) ;; *) echo "BAD FIELD row $rows: $field"; bad=$((bad+1));; esac
  case "$mark" in transcribed|paraphrased) ;; *) echo "BAD MARK row $rows: $mark"; bad=$((bad+1));; esac
  case "$source" in
    [0-9a-f]*:?*) ;;
    *) echo "BAD SOURCE row $rows: $source"; bad=$((bad+1));;
  esac
  value=$("$AF" status --source "$PLAN" --step "$slug" | sed -n "s/^$field: //p")
  if [ -z "$value" ] || [ "$value" = "(not recorded)" ]; then
    echo "NO SUCH FILLED FIELD row $rows: $slug $field"; bad=$((bad+1))
  fi
done < <(tail -n +2 "$REC")
sort "$keys" | uniq -d | sed 's/^/DUPLICATE KEY: /'
dupes=$(sort "$keys" | uniq -d | wc -l)
rm -f "$keys"
filled=$(grep -c '^\(problem\|approach\) = ' "$PLAN")
printf 'rows=%d filled=%d dupes=%d bad=%d\n' "$rows" "$filled" "$dupes" "$bad"
```

Pass, all four clauses: `rows` is GREATER THAN ZERO, `rows` equals `filled`, `dupes=0`, and `bad=0`. The oracle is the printed line and not the exit status, which is 0 in every case.

`dupes` IS WHAT MAKES `rows == filled` A COVERAGE CHECK. Without it the equality counts rows rather than keying them, so a copy-paste satisfies it. MEASURED against a two-step plan with all four fields filled: a record naming `alpha problem` twice, `alpha approach` once and `beta problem` once prints `rows=4 filled=4 bad=0` under the earlier form and a FULL PASS, while `beta approach` has no named source at all; a record whose four rows all name `alpha problem` does the same. With `dupes` both print `dupes=1` and fail.

`rows > 0` IS THE ABSENT-INPUT CLAUSE. An empty record with a correct header prints `rows=0 filled=0 dupes=0 bad=0`, which satisfies `rows == filled` literally.

MEASURED against four defective records:

- The record ABSENT prints `BAD HEADER` and `rows=0 filled=4 dupes=0 bad=1`. This closes the measured trap where the record's absence satisfied the stated pass condition.
- A record with only `slug` and `field` columns prints `BAD HEADER` and eight `BAD` rows, `rows=4 filled=4 dupes=0 bad=9`.
- A `transcribed` row that cites a bare commit prints `BAD SOURCE row 1: 5e7ee58` and `bad=1`. One row failing one check gives one, and an earlier draft stated `bad=2`.
- A filled field with no row prints `rows=2 filled=4 dupes=0 bad=0`, which fails on `rows != filled` rather than on `bad`. Every clause of the pass condition is therefore load-carrying and every one is stated.

4. EVERY SOURCE RESOLVES, EVERY TRANSCRIBED SENTENCE IS AT ITS SOURCE, AND THAT SOURCE IS THE EARLIEST COMMIT THAT HOLDS IT. Run:

```
#!/usr/bin/env bash
# R2: source resolution, source relevance, the transcribed substring test, and the earliest-commit rule.
REC="$1"; PLAN="$2"; AF="$3"
rows=0; tr=0; pa=0; bad=0
if [ "$(head -1 "$REC" 2>/dev/null)" != "$(printf 'slug\tfield\tmark\tsource')" ]; then
  echo "BAD HEADER"; bad=$((bad+1))
fi
while IFS=$'\t' read -r slug field mark source; do
  rows=$((rows+1))
  if ! git show "$source" > /dev/null 2>&1; then
    echo "UNRESOLVED SOURCE row $rows: $slug $field $source"; bad=$((bad+1)); continue
  fi
  path=${source#*:}
  case "$path" in
    docs/plans/agent-scaffold.md) ;;
    docs/plans/agent-scaffold.steps/"$slug".md) ;;
    *) echo "SOURCE NOT THIS STEP row $rows: $slug $field $path"; bad=$((bad+1)); continue;;
  esac
  value=$("$AF" status --source "$PLAN" --step "$slug" | sed -n "s/^$field: //p")
  case "$mark" in
    paraphrased) pa=$((pa+1)) ;;
    transcribed)
      tr=$((tr+1))
      if ! git show "$source" | grep -qF -- "$value"; then
        echo "SENTENCE NOT AT SOURCE row $rows: $slug $field $source"; bad=$((bad+1)); continue
      fi
      earliest=$(git log --reverse --format=%H -S"$value" -- . | head -1)
      cited=$(git rev-parse "${source%%:*}^{commit}" 2>/dev/null)
      if [ "$earliest" != "$cited" ]; then
        echo "NOT THE EARLIEST row $rows: $slug $field cited $cited, earliest $earliest"; bad=$((bad+1))
      fi
      ;;
  esac
done < <(tail -n +2 "$REC")
printf 'rows=%d transcribed=%d paraphrased=%d bad=%d\n' "$rows" "$tr" "$pa" "$bad"
```

Pass: the printed line ends `bad=0`, its `rows` equals criterion 3's `rows`, and `rows` is GREATER THAN ZERO. The `rows > 0` clause is here for the same reason it is in criterion 3: this loop over an empty record prints `rows=0 transcribed=0 paraphrased=0 bad=0`, which reads as a clean run. The header check is here so that a record with the wrong columns is reported by R2 as well as by R1, rather than being read as four unnamed fields. The full commit hashes are compared through `git rev-parse`, because the abbreviated `%h` width varies with repository size.

THE SOURCE-RELEVANCE ARM IS WHAT MAKES RULE 5's ADMISSIBLE SET EXECUTABLE. Rule 4 makes the step's own sidecar the first source and rule 5's path-at-that-commit paragraph makes `docs/plans/agent-scaffold.md` the source for the older steps, so the admissible set is already written down. Without this arm an intent value transcribed from `README.md`, cited to the earliest commit holding that sentence, satisfies every other mechanical check in this block: R1 checks shape and coverage, the substring test passes because the sentence really is there, the earliest-commit test passes because the commit really is the earliest, and R3 looks in the step's own sidecar, which an unrelated source does not reach. A row that genuinely needs another path is reported as `SOURCE NOT THIS STEP` and becomes a visible exception the outcome disposes of under criterion 8.

MEASURED against three defective citations:

- A commit that DOES hold the sentence but is not the earliest prints `NOT THE EARLIEST row 1: ledger-template problem cited 0fadd90fc1703cc1df1c03b1486ca3bf2d39b1bf, earliest 5e7ee58aa0954ee77492227a7ac9a7c4d7bb5f0e`.
- A commit and path that do not hold the sentence print `SENTENCE NOT AT SOURCE`.
- Today's sidecar path against a commit that predates the sidecar tree prints `UNRESOLVED SOURCE`, which is the path-at-that-commit case rule 5 states.

5. THE TRANSCRIBED AND PARAPHRASED COUNTS ARE REPORTED PER BATCH. Criterion 4's printed line carries them. The outcome records the pair for this batch and the running total across batches. This is what makes the paraphrase opt-out visible rather than silently compliant.

6. NO SIDECAR REPEATS ITS OWN INTENT, AND NO VALUE OPENS WITH A STATUS TOKEN. Run:

```
#!/usr/bin/env bash
# R3: the moved-not-copied rule, and the status-token rule.
PLAN="$1"; AF="$2"; STEPS="$3"
checked=0; dup=0; token=0
for slug in $(sed -n 's/^slug = "\(.*\)"$/\1/p' "$PLAN"); do
  for field in problem approach; do
    value=$("$AF" status --source "$PLAN" --step "$slug" | sed -n "s/^$field: //p")
    [ -z "$value" ] && continue
    [ "$value" = "(not recorded)" ] && continue
    checked=$((checked+1))
    if [ -f "$STEPS/$slug.md" ] && grep -qF -- "$value" "$STEPS/$slug.md"; then
      echo "SIDECAR REPEATS $slug $field"; dup=$((dup+1))
    fi
    if printf '%s' "$value" | grep -qE '^(Not started|In progress|Complete|Skipped|Next|Optional|Deferred)([.;,:]|$| \(| (and|by|but|or|nor|for|so|yet|until|unless|pending|while|after|before|because|since|though|although|then|with|without|on|in|at|to|from|as|per)\b)'; then
      echo "STATUS TOKEN $slug $field: $(printf '%s' "$value" | cut -c1-40)"; token=$((token+1))
    fi
  done
done
printf 'checked=%d duplicated=%d status_token=%d\n' "$checked" "$dup" "$token"
```

Pass: the printed line reads `checked=<2m> duplicated=0 status_token=0`, where `m` IS THE QUANTITY CRITERION 1 DEFINES AND IS NOT RE-DEFINED HERE, AND `checked` is greater than zero. The last clause is the absent-input guard: the loop over a plan with no filled field prints `checked=0 duplicated=0 status_token=0`, which reads as a clean run.

EVERY ARM IS ANCHORED ON A SENTENCE BOUNDARY, AND THE ANCHOR IS THE SAME ONE `sidecar-status-opening-drift` USES. A status word is a LABEL when the token is followed by punctuation, by an opening parenthesis, by end of value, or by a conjunction or preposition. It is an ORDINARY ADJECTIVE when a noun follows it, and an adjective is not what rule 9 forbids. MEASURED, an earlier form of this test matched `Complete`, `Skipped`, `Optional` and `Deferred` unanchored, so the sentence "Deferred cleanup from the `Q-44` audit (`architecture-audit`), raised there and scheduled here." fired it, and that sentence is the faithful opening of six sidecars in this plan and a legitimate problem statement. The anchored form does not fire on it. Nine sidecars in this plan open that way and every one is declared `deferred`.

THE CONNECTIVE LIST IS A CLOSED LIST, SO R3 PRINTS ITS COMPLEMENT RATHER THAN ASSUMES IT EMPTY. Run this alongside R3, from the repository root under bash, and record its output in the outcome:

```
#!/usr/bin/env bash
# R3b: the values a relaxed status test reaches and the anchored arm of R3 does not.
PLAN="$1"; AF="$2"
for slug in $(sed -n 's/^slug = "\(.*\)"$/\1/p' "$PLAN"); do
  for field in problem approach; do
    value=$("$AF" status --source "$PLAN" --step "$slug" | sed -n "s/^$field: //p")
    [ -z "$value" ] && continue
    [ "$value" = "(not recorded)" ] && continue
    printf '%s' "$value" | grep -qE '^(Not started|In progress|Complete|Skipped|Next|Optional|Deferred)([.;,: ]|$)' || continue
    printf '%s' "$value" | grep -qE '^(Not started|In progress|Complete|Skipped|Next|Optional|Deferred)([.;,:]|$| \(| (and|by|but|or|nor|for|so|yet|until|unless|pending|while|after|before|because|since|though|although|then|with|without|on|in|at|to|from|as|per)\b)' && continue
    printf '%s\t%s\t%s\n' "$slug" "$field" "$(printf '%s' "$value" | cut -c1-40)"
  done
done
```

THIS IS NOT A PASS-OR-FAIL ORACLE AND ITS EMPTY OUTPUT IS NOT THE TARGET. It is a bounded worklist, in the same shape and for the same reason as the drift step's complement command. THE OBLIGATION: the outcome disposes of every row it prints, either as an adjectival opening that rule 9 does not forbid, or as a connective the list must gain, and a row left with neither is the batch not finished.

WHY THIS COMPLEMENT MATTERS MORE FOR R3 THAN FOR THE DRIFT SELECTOR. The drift selector reads openings that already exist, so its vocabulary is fixed in advance and measurable. R3 reads sentences a batch has just authored, so its vocabulary is not. MEASURED against R3's own regex, four openings carry a label and do not fire: "Complete once the batch lands", "Deferred whilst the design settles", "Next up, the schema flip" and "Optional under the current scope". The connectives `once`, `whilst`, `up` and `under` are absent from the list. MEASURED, R3b prints all four, prints nothing for "Complete, and the record is written", which R3 already catches, and prints nothing for a value that opens with no status word at all.

THE HUMAN DECLINED TO ACCEPT THIS AS RESIDUAL RISK ON 2026-08-21, receipt `type:"decision"` `q_id:"Q-78-residuals"` in `docs/metrics/workflow.jsonl`, on the ground that its acceptance could ship a real defect. An evading value re-creates in the structured field exactly the duplication `sidecar-status-opening-drift` deletes from the prose, and the only other guard is criterion 8's reading, which is the weakest guard this pass uses.

MEASURED, a transcribed sentence left in its sidecar prints `SIDECAR REPEATS checks-runner-worktree-name-collision approach` and `duplicated=1`, and a value that opens `Next. Decided (` prints a `STATUS TOKEN ledger-template problem` row whose value is truncated at 40 characters, and `status_token=1`. A correct batch prints `checked=4 duplicated=0 status_token=0` on the same fixture.

7. THE PROJECTION IS REGENERATED AND IT RECONCILES AGAINST THE SOURCE. `./target/debug/agent-flow render docs/plans/agent-scaffold.plan.toml` then `render --check --strict`, which prints `docs/plans/agent-scaffold.plan.toml: up to date` and exits 0. Then run R4:

```
#!/usr/bin/env bash
# R4: the projection is total, counted in the source and reconciled against the projection.
TOML=docs/plans/agent-scaffold.plan.toml
MD=docs/plans/agent-scaffold.md
quoted () {
  cat docs/plans/agent-scaffold.steps/*.md \
      docs/plans/agent-scaffold._status-narrative.md \
      docs/plans/agent-scaffold.motivations.md \
      docs/plans/agent-scaffold.principles-note.md \
      docs/plans/agent-scaffold.documentation-protocol.md \
      docs/plans/agent-scaffold.repo-layout.md \
      docs/plans/agent-scaffold.queue-intro.md \
      docs/plans/agent-scaffold.roadmap-intro.md \
      docs/plans/agent-scaffold.success-criteria.md | grep -c "^- $1: "
}
printf 'steps=%d source=%d/%d quoted=%d/%d projected=%d/%d\n' \
  "$(grep -c '^\[\[step\]\]' "$TOML")" \
  "$(grep -c '^problem = ' "$TOML")" "$(grep -c '^approach = ' "$TOML")" \
  "$(quoted problem)" "$(quoted approach)" \
  "$(grep -c '^- problem: ' "$MD")" "$(grep -c '^- approach: ' "$MD")"
```

Pass, for a batch: `projected` minus `quoted` equals `source`, for BOTH fields, and both halves of `source` are equal to each other and each equals `m`, THE QUANTITY CRITERION 1 DEFINES AND WHICH IS NOT RE-DEFINED HERE. The outcome records the whole printed line.

WHY THE COUNT IS TAKEN IN THE SOURCE AND ONLY RECONCILED IN THE PROJECTION. `render` inlines every sidecar verbatim, so a sidecar that QUOTES a `- problem: ` line contributes one to the projection and nothing to the source. This sidecar quotes exactly such a pair, in the fenced block under `render` in increment 1. MEASURED on the untouched tree, before any batch runs, R4 prints `steps=105 source=0/0 quoted=1/1 projected=1/1`, so a criterion that compares the projection against the step count directly cannot be satisfied by a correct implementation at any point in the migration. The reconciliation holds at every point, which is why increment 3 criterion 8 runs the same script. Principle 8, Structured data first, project for humans, is the ground: the TOML is the source and the `.md` is the projection, so the totality claim is a claim about the source.

The eight named sidecars are the front and tail sidecars from `[meta.sidecars]`. The 80 question sidecars are not listed because every one of them is 0 bytes, which `find docs/plans/agent-scaffold.questions -type f -size +0` shows by printing nothing.

8. EVERY PARAPHRASED FIELD, AND EVERY EXCEPTIONAL SOURCE, IS DISPOSED OF IN THE OUTCOME. This is NOT a pass-or-fail oracle and it is a bounded worklist. For every row this batch marks `paraphrased`, the outcome names the row's `source` and quotes the source sentence and the recorded sentence side by side. For every row R2 reports as `SOURCE NOT THIS STEP`, the outcome quotes the sentence and states why no admissible path holds it. A row left without its pair, or a reported row left without its reason, is the batch not finished.

The criterion exists because no command can test a paraphrase, criterion 4 deliberately exempts it, and a batch that marks every field `paraphrased` otherwise satisfies every mechanical check in this block. On a `paraphrased` row the `source` column proves only that the blob exists and that its path belongs to this step, which rule 7 records, so the side-by-side is the only thing that reads it. Read the count against the sizing sample recorded in batch a.

9. THE CHANGED PATH SET AND THE UNCHANGED REST. `git diff --name-only` matches criterion 1. No file under `src/`, `tests/` or `pack/` appears. `docs/metrics/workflow.jsonl` does not appear.

10. THE VALIDATORS, THE SUITE AND ASCII. Both `validate` invocations print their `valid` line and exit 0. `cargo test` passes. `LC_ALL=C grep -cP '[^\t\x20-\x7e]' <file>` prints `0` for every changed file, the migration record included.

### Increment 3, `step-intent-encoding-inc3`: the required flip, the pack, and the record deletion

RISK CLASS `risky` (two consecutive clean review rounds). THE GROUND IS STATED AS A PREMISE AND A CONSEQUENCE, AND EACH HALF NAMES THE COMMAND THAT REFUSES IT. Stating it as one conjunction is what let a wrong implementation through two review rounds, because the consequence held for a second reason and the criterion tested only the consequence.

THE PREMISE. The increment makes BOTH fields required. `problem` and `approach` each become a bare `String` with no `serde` default, so a `[[step]]` that omits EITHER one fails to deserialise.

THE CONSEQUENCE. Every previously valid scaffolded plan fails to parse until its author edits it. That is squarely Principle 3, Safe on existing projects, and it is hard to roll back once a downstream author has edited.

THE TWO HALVES COME APART, AND THE SEPARATION WAS BUILT, COMPILED AND RUN. A pre-increment plan carries neither field, so it fails to parse whenever EITHER field is required. The consequence therefore survives an implementation that requires `problem` and leaves `approach` optional, while the premise is false of it. MEASURED on that build: the schema greps for `problem` both pass, the parse check on a plan with no `problem` prints ``missing field `problem` `` and exits 1, and a plan carrying `problem` and no `approach` prints `1 steps, 0 questions, valid` and exits 0. THE MIRROR CONSTRUCTION also comes apart the other way: both fields declared `String` under `#[serde(default)]` keeps the premise's wording and falsifies the consequence, because MEASURED on that build a plan with neither field prints `1 steps, 0 questions, valid` and exits 0 rather than failing to parse. Criterion 1 below runs against both halves and refuses both constructions.

THE INCREMENT ALSO CHANGES `pack/plan-template.plan.toml`, `pack/plan-template.documentation-protocol.md`, `pack/plan-template.steps/example-step.md` and their committed copies under `docs/plans/`, which every scaffolded project inherits.

THE BATCH BLOCK ONE INCREMENT EARLIER ALREADY CLOSED THE IDENTICAL HOLE, in its own words at criterion 1: "Both fields are counted because a batch that fills `problem` and forgets `approach` satisfies a single-field check." Its ground is stated symmetrically and has no surviving half to hide behind, which is why the same author saw the hazard there and missed it here.

THE HUMAN DECISION THIS INCREMENT WAITED ON IS TAKEN (2026-08-21, receipt `q_id:"Q-78-requiredfields"`). `problem` AND `approach` ARE REQUIRED, IN THE SHIPPED PACK AS WELL AS HERE, over an optional field with a validation warning. The human rejected a third option, required here and optional in the pack. The human weighed the cost this increment states below, and accepted the residual that a placeholder satisfies a required field forever. So this increment builds what it already specifies, and it waits only on the review the whole step waits on.

WHAT CHANGES. `Option<String>` becomes `String` on both fields and the two `if let Some` arms in `validate` become direct reads, and the four rejections themselves stay, pinned by the four tests increment 1 criterion 13 puts in the suite. `render` emits both lines unconditionally. `next` wraps both in `Some` at the `steps_from_toml` boundary, so `StepInfo` keeps its `Option` for the Markdown substrate, which carries no such column. `status --step` drops the `(not recorded)` fallback for a TOML source and keeps it for the Markdown one, WHICH IS AN EDIT TO `src/main.rs`: `StatusArgs` is declared there and `run_status` is the function that prints the fallback, and `step_views` projects `slug` and `status` alone, so `status --step` cannot read the intent through `PlanProjection`. `src/main.rs` is therefore in criterion 9's path set and criterion 12 is the command that reads the surviving half.

Every inline `[[step]]` declaration in `src/`, `tests/` and the two template files gains both fields.

`pack/plan-template.plan.toml` and `docs/plans/TEMPLATE.plan.toml` ship placeholder values of the form `problem = "<the problem this step addresses>"` and `approach = "<how this step addresses it>"`.

`pack/plan-template.documentation-protocol.md` gains the duty (g) sentence, scoped so it does not break on the template that carries it:

```
A Step Detail below its own heading line must not repeat a `[[step]]` field. The heading line is the exception, and `render` takes it over later.
```

THE SENTENCE LANDS AS ITS OWN PARAGRAPH BELOW THE ANGLE-BRACKET PLACEHOLDER NOTE AND OUTSIDE IT, and the placement is specified rather than left open. The entire body of that file below its heading is one angle-bracket placeholder note, and `pack/prompts/planner.md` directs the adopter's planner to "Delete the template's angle-bracket placeholder notes as you fill each part in". A sentence written INSIDE the brackets is therefore a rule the first planner of every scaffolded project deletes on sight, while a sentence written outside them survives into that project's own plan. Criterion 6's `grep -c -F` cannot tell the two placements apart, which is why it gains the placement command as well. The same placement holds in the committed copy `docs/plans/TEMPLATE.documentation-protocol.md`, which is a verbatim copy of the pack source.

`pack/plan-template.steps/example-step.md` AND ITS COMMITTED COPY `docs/plans/TEMPLATE.steps/example-step.md` GAIN THE TWO FIELDS IN THE PACK'S ONE HOW-TO-ADD-A-STEP SENTENCE. That sentence reads today "To add a step, add a `[[step]]` entry to the `.plan.toml` and a matching `<slug>.md` body sidecar in this directory, then re-render", and it is the only such guidance the pack ships. After the flip its literal execution produces a plan that no longer parses, and the parser aborts on the FIRST missing field, so an operator following it learns about `approach` only after supplying `problem` and re-running. Shipping that instruction to every scaffolded project is what Principle 3, Safe on existing projects, is cited to prevent in this increment's own cost paragraph, and every criterion below would otherwise pass over it. The corrected sentence names `problem` and `approach` as required entries of the `[[step]]` block. `render` inlines this file into `docs/plans/TEMPLATE.md`, so that projection changes with it.

`docs/plans/TEMPLATE.md` IS RE-RENDERED, AND IT IS NOT OPTIONAL. `docs/plans/TEMPLATE.plan.toml` is one of the declaration sites this increment requires to carry both fields, increment 1's render rule emits the two lines into the Step Details body immediately after the leading heading line, and `docs/plans/TEMPLATE.md` is a committed render of that source which `render --check --strict` reports up to date today. So the committed projection changes twice over, once from the placeholder values and once from the corrected example-step sentence. Nothing else detects a stale one: `.agents/checks.toml` declares one check and it names `docs/plans/agent-scaffold.plan.toml`, and `src/agents_md_drift.rs` names the `docs/plans/TEMPLATE` family as outside its coverage. A FRESH SCAFFOLD IS UNAFFECTED EITHER WAY, because `scaffold` re-renders `TEMPLATE.md` into the target project rather than copying the committed one; what would ship stale is this repository's own committed copy. THE SIBLING CONTRAST IS WHY THIS IS NOT A GENERAL RULE: `plan-order-array-position` increment 1 also edits `docs/plans/TEMPLATE.plan.toml` and correctly omits `docs/plans/TEMPLATE.md`, because `render` emits no order column and the template holds one step, so that edit leaves the projection byte-identical.

`docs/plans/step-intent-encoding.migration.tsv` is deleted.

WHY THE SENTENCE IS SCOPED. The unqualified form must not ship, because `pack/plan-template.steps/example-step.md:1` restates `slug` and `title` on its own first line, and so does almost every sidecar in this repository. The rule rides in this increment rather than elsewhere because this increment already edits the pack, so it already owes the rendered-pair check below.

THREE COPIED PAIRS ARE HAND-EDITED HERE AND NO GUARD COVERS ANY OF THEM. `pack/pack.toml` maps `plan-template.plan.toml` to `docs/plans/TEMPLATE.plan.toml`, `plan-template.documentation-protocol.md` to `docs/plans/TEMPLATE.documentation-protocol.md` and `plan-template.steps/example-step.md` to `docs/plans/TEMPLATE.steps/example-step.md`, all three as verbatim copies with no `render = true`, so each pair is byte-identical today. `src/agents_md_drift.rs` names "the `docs/plans/TEMPLATE` family" as UNGUARDED in its own coverage block, and `.agents/checks.toml` declares only `render-check`. Criterion 5 is the guard and it is `cmp`, not `just scaffold-self`: that recipe's second command is `nix fmt`, which formats the whole tree, and this tree is not formatter-clean, so the recipe reformats files this increment did not intend and breaks criterion 9, the changed-path set, until the implementer re-renders.

THE DECLARATION-SITE SET, ESTABLISHED BY SEARCH.

```
for f in $(grep -rlE '(\\n|^)slug = ' src tests pack docs/plans/TEMPLATE.plan.toml | sort); do
  printf '%s\t%s\n' "$(grep -oE '(\\n|^)slug = ' "$f" | wc -l)" "$f"
done
```

MEASURED, that returns 12 files and 69 sites:

```
1	docs/plans/TEMPLATE.plan.toml
1	pack/plan-template.plan.toml
2	src/next.rs
3	src/plan/render.rs
32	src/plan/source.rs
7	src/plan/testdata/render-fixture.plan.toml
3	src/plan/testdata/skeleton.plan.toml
13	src/workflow.rs
1	tests/metrics_and_ledger_anchor_to_the_plan_source.rs
4	tests/unsafe_pairings_are_refused_and_omitted.rs
1	tests/validate_toml_primary_skips_markdown_plan.rs
1	tests/validate_workflow_toml_source_needs_no_plan.rs
```

THE ANCHOR IS THE `slug` LINE AND NOT THE `status` LINE. A `status` line also belongs to every `[[question]]` and to some waivers, so a substitution anchored on `status` over-patches. MEASURED on the tree this sidecar was spliced into, the `status` anchor reaches 99 sites against the `slug` anchor's 69, and a substitution across all of them produces test failures from `deny_unknown_fields`. Re-run the two anchors rather than copying the pair, because both move as the plan and the suite grow.

WHY THE MIGRATION RUNS THIS WAY. The alternative, land the fields as required and backfill every step in the same commit, has no optional window at all, which Principle 5 prefers. It is rejected because one review loop would then carry every step in the plan against a cap of five rounds, which is the reason the backfill splits into six batch increments in the first place. The window in which absence is legal is six batches long, and this increment closes it, so the end state makes absence unrepresentable and no `[meta]` exemption field is needed. An exemption boundary of the `[meta].w4_baseline` kind is right for a rule that will always have exempt members and wrong for a migration that finishes.

WHAT THIS COSTS A SCAFFOLDED PROJECT, STATED HERE AND WEIGHED BY THE HUMAN. After this increment, adding a step to any scaffolded plan requires two prose sentences before the plan parses, and for an exploratory step the problem statement is often the thing the step exists to find out. The pack template must ship placeholder values, because a required `String` needs one, so every scaffolded plan validates on day one carrying placeholder intent. The required field therefore makes ABSENCE unrepresentable and leaves MEANINGLESSNESS fully representable. A `validate` rule that rejects the placeholder strings is REJECTED: it would break criterion 3 below, which is correct under Principle 3, Safe on existing projects, and Principle 4, Idempotent. Placeholder detection, if wanted, belongs in `audit` and is a separate step.

ACCEPTANCE, EACH EXECUTABLE.

1. BOTH FIELDS ARE REQUIRED, AND EACH IS CHECKED ON ITS OWN. THIS IS THE EXECUTABLE FORM OF THIS INCREMENT'S OWN RISK GROUND, and it runs against the PREMISE and the CONSEQUENCE separately, because the consequence holds for a second reason. FOUR GREPS AND TWO PARSE CHECKS, EACH GIVEN ONCE, in the shape this sidecar already uses at increment 1 criterion 8 and that `validate-missing-source-exit` criterion 3 states as a rule: a reader who substitutes once proves one field.

THE FOUR GREPS. The first two print `1` and exit 0. The second two print `0` and exit 1, so neither can join an `&&` chain.

```
grep -c 'pub(crate) problem: String,' src/plan/source.rs
```

```
grep -c 'pub(crate) approach: String,' src/plan/source.rs
```

```
grep -c 'problem: Option<String>' src/plan/source.rs
```

```
grep -c 'approach: Option<String>' src/plan/source.rs
```

THE TWO PARSE CHECKS. Write two one-step plans to a scratch directory OUTSIDE the repository. The first carries `approach` and no `problem`. The second carries `problem` and no `approach`. Run `validate --source` on each. Each exits 1 and prints on stderr a line carrying its own string:

```
missing field `problem`
```

```
missing field `approach`
```

The strings are in fenced blocks rather than inline for the reason increment 1 criterion 2 records.

WHY EVERY ONE OF THE SIX IS LOAD-CARRYING, MEASURED AGAINST TWO CONSTRUCTIONS THAT WERE BUILT WITH THE PROJECT TOOLCHAIN AND RUN.

- THE ASYMMETRIC BUILD, `problem: String` required and `approach: Option<String>` optional, which falsifies the premise while the consequence still holds. The `problem` grep prints `1`, the `problem: Option<String>` grep prints `0` and the no-`problem` plan prints ``missing field `problem` `` and exits 1, so the three commands an earlier form of this criterion stated all PASS. The `approach` grep prints `0` against a required `1`, the `approach: Option<String>` grep prints `1` against a required `0`, and the no-`approach` plan prints `1 steps, 0 questions, valid` and exits 0. Three of the six REFUSE it. That build satisfied every other criterion in this increment, and it ships a plan carrying one field and not the other.
- THE DEFAULTED BUILD, both fields `String` under `#[serde(default)]`, which keeps the premise's wording and falsifies the consequence. All four greps PASS. Both parse checks print `1 steps, 0 questions, valid` and exit 0 rather than the `missing field` line, so both REFUSE it.
- THE CONTROL, both fields a bare `String`. All four greps pass, and both parse checks print their own `missing field` line and exit 1.

2. THE 69 DECLARATION SITES ALL CARRY BOTH FIELDS. `cargo test` passes and `cargo build` reports no error. MEASURED, a flip that leaves the sites unpatched still BUILDS with 0 errors and gives 54 test failures, so the suite is a real oracle here. The path set in criterion 9 is what proves the enumeration was complete rather than lucky.

ONE NAMED TEST CHANGES DIRECTION HERE, AND THE DIRECTION IS STATED SO THE IMPLEMENTER DOES NOT CHOOSE IT. `empty_details_sections_emit_no_bare_heading` in `src/plan/render.rs`, marked `N1`, asserts that `## Step Details` is ABSENT for a step with an empty body. Its inline `[[step]]` fixture is one of the sites this criterion requires to carry both fields, so after the patch the step carries intent and increment 1's render sub-rule makes the section appear. ITS STEP-DETAILS ASSERTION RE-POINTS: the section is PRESENT and carries the two projected lines, and the test takes a name that matches. Its Question-Details assertion and its non-vacuous half stay. DO NOT DELETE THE TEST. Without this instruction the implementer meets `cargo test` by editing a named regression test with no stated direction, which is the shape `plan-order-array-position` increment 1 already rules on for its own tie-break test.

THE FOUR RULE 2 AND RULE 3 TESTS INCREMENT 1 CRITERION 13 ADDS STAY, AND THEY STAY GREEN. `grep -c 'fn validate_rejects_a' src/plan/source.rs` still prints `4`, and `cargo test --bin agent-flow validate_rejects_a` reports four passing tests and none failing. This increment rewrites the code both rules sit in, and the cheapest way to make `cargo test` pass after dropping a check body is to delete the test that reads it. DO NOT DELETE THEM.

3. A FRESH SCAFFOLD VALIDATES AND RENDERS. In an empty directory outside the repository:

```
./target/debug/agent-flow scaffold --output-dir . --write --vcs none
```

then

```
./target/debug/agent-flow validate --source docs/plans/TEMPLATE.plan.toml
```

Pass: stdout carries exactly `docs/plans/TEMPLATE.plan.toml: 1 steps, 0 questions, valid` and the exit status is 0. The stdout line is the oracle and the exit status is not, because `validate --source` on a path that does not exist prints `no source plan at docs/plans/TEMPLATE.plan.toml; nothing to validate` and exits 0 until `validate-missing-source-exit` lands. Then:

```
./target/debug/agent-flow render --check docs/plans/TEMPLATE.plan.toml --strict
```

Pass: stdout is exactly `docs/plans/TEMPLATE.plan.toml: up to date`, exit 0. MEASURED, both hold with the placeholder values above.

4. THE SHIPPED PLACEHOLDERS REACH THE RENDERED TEMPLATE. In the same scaffolded directory:

```
grep -c -F -- '- problem: <the problem this step addresses>' docs/plans/TEMPLATE.md
```

```
grep -c -F -- '- approach: <how this step addresses it>' docs/plans/TEMPLATE.md
```

Pass: each prints exactly `1` on stdout and exits 0. Two commands, given once each, because a template that ships one placeholder and renders the other nowhere satisfies a single-field check. This is the pack-side form of increment 1 criterion 4, and it is stated because a required field that renders nowhere in the shipped template is the same defect one layer out.

5. EVERY TEMPLATE PAIR THIS INCREMENT TOUCHES STAYS BYTE-IDENTICAL, AND EACH `cmp` IS WRITTEN OUT. `plan-order-array-position` rule 3, which this criterion cites as its authority, reads "Every increment that touches either file runs the `cmp`", and the design pass states the same rule for the whole `docs/plans/TEMPLATE` family. This increment hand-edits BOTH SIDES OF THREE PAIRS. Three commands. Each prints nothing and exits 0.

```
cmp pack/plan-template.plan.toml docs/plans/TEMPLATE.plan.toml
```

```
cmp pack/plan-template.documentation-protocol.md docs/plans/TEMPLATE.documentation-protocol.md
```

```
cmp pack/plan-template.steps/example-step.md docs/plans/TEMPLATE.steps/example-step.md
```

`pack/pack.toml` maps each of the three sources to its destination with `ownership = "working"` and no `render = true`, so each pair is a verbatim copy and byte equality is the whole of the contract. AN EARLIER FORM RAN THE FIRST `cmp` ALONE, while this increment's own paragraph above says two rendered pairs are hand-edited here and no guard covers either. Under that form any divergence introduced anywhere else in either unchecked pair, a reflowed paragraph, a typo corrected on one side, a trailing-newline difference, passed criterion 5, passed criterion 6's greps for the one sentence, and passed criterion 9, which names the paths and proves nothing about their content. See `plan-order-array-position` rule 3 for the measurement that shows nothing else detects any of the three.

6. THE PACK PROSE RULE SHIPS, ITS COMMITTED COPY MATCHES, AND NEITHER COPY BURIES IT IN THE PLACEHOLDER. Two presence commands, written out in full rather than as one command plus a path to substitute, because the pack source and its committed copy are two files and a reader who substitutes once proves one file. Each prints exactly `1`.

```
grep -c -F -- 'must not repeat a `[[step]]` field' pack/plan-template.documentation-protocol.md
```

```
grep -c -F -- 'must not repeat a `[[step]]` field' docs/plans/TEMPLATE.documentation-protocol.md
```

THEN THE PLACEMENT, WHICH THE TWO PRESENCE COMMANDS CANNOT SEE. Each file's body below its heading is one angle-bracket placeholder note occupying a single unwrapped line, so a sentence written inside the note shares that line and a sentence written outside it starts its own:

```
grep -c -- '^<.*must not repeat a' pack/plan-template.documentation-protocol.md docs/plans/TEMPLATE.documentation-protocol.md
```

Pass: one row per named path, each row ending `:0`. The printed rows are the oracle and the exit status is not, because `grep -c` exits 1 when every count is zero, which is this command's pass case. Both paths are arguments of the one command, so neither is substituted in by the reader. MEASURED AGAINST THE WRONG PLACEMENT, with the sentence appended inside the brackets: both presence commands still print `1` and both rows here read `:1`. That placement ships a rule the first planner of every scaffolded project deletes on sight, because `pack/prompts/planner.md` directs it to delete the angle-bracket placeholder notes as it fills each part in, so the presence check alone cannot separate a rule that survives into the adopter's plan from one that does not.

7. THE MIGRATION RECORD IS GONE. `test -e docs/plans/step-intent-encoding.migration.tsv` exits 1, and `git diff --name-status` over the increment lists `D	docs/plans/step-intent-encoding.migration.tsv`. Both halves are the criterion: the `test` alone passes on a tree where the file never existed.

8. THE LIVE PROJECTION IS COMPLETE, ONE PAIR PER STEP. Run R4, the script the batch block states in full under its criterion 7.

Pass, all three clauses: `source` equals `steps` for both fields; `projected` minus `quoted` equals `source` for both fields; and the two halves of each pair are equal to each other. The first clause is the required flip landing on every step. The second is the projection being total rather than partial, and it is what catches a field that exists everywhere and renders nowhere. The third is the two fields moving together.

MEASURED on the untouched tree, before any of this is built, R4 prints `steps=105 source=0/0 quoted=1/1 projected=1/1`. A CRITERION THAT COMPARED THE PROJECTION AGAINST THE STEP COUNT DIRECTLY COULD NOT BE SATISFIED BY A CORRECT IMPLEMENTATION, because this sidecar's own fenced block under `render` in increment 1 carries a `- problem: ` line and a `- approach: ` line, and `render` inlines the sidecar verbatim into the document being counted. An earlier draft of this criterion did exactly that and stated `MEASURED at 101 steps, all three print 101`; the two projection counts print `1` today and cannot print a step count at any point in the migration, so nothing was measured. The step count itself moves and the outcome records what R4 prints on the day.

9. THE CHANGED PATH SET. `git diff --name-only` lists the 12 declaration-site files, plus `src/main.rs`, plus `docs/plans/agent-scaffold.md`, plus `docs/plans/TEMPLATE.md`, plus `pack/plan-template.documentation-protocol.md` and `docs/plans/TEMPLATE.documentation-protocol.md`, plus `pack/plan-template.steps/example-step.md` and `docs/plans/TEMPLATE.steps/example-step.md`, plus `CHANGELOG.md`, plus the deleted `docs/plans/step-intent-encoding.migration.tsv`. `docs/plans/agent-scaffold.plan.toml` appears only if a `[[step.increment]]` declaration changes, and its diff must touch no `problem` or `approach` value, because the batches own those.

THE PATHS AN EARLIER FORM OF THIS SET OMITTED ARE NAMED HERE WITH THEIR REASONS, because this criterion reads as an exact enumeration: an implementer who made any of those edits FAILED it, and one who obeyed it shipped the defect instead. `src/main.rs` carries the `status --step` fallback this increment changes, which WHAT CHANGES states and criterion 12 reads. `docs/plans/TEMPLATE.md` is the committed render of a source this increment edits twice, and nothing else in the repository detects a stale one. `pack/plan-template.steps/example-step.md` and its committed copy carry the pack's one how-to-add-a-step sentence, which the flip turns into a recipe for a plan that does not parse. `CHANGELOG.md` carries the entry this increment's DOCUMENTATION IMPACT owes. Every one of them is a file a CORRECT implementation must change, which is what makes the omission a defect in the criterion rather than in the implementation.

10. NO PLACEHOLDER-REJECTION RULE WAS ADDED. `grep -rn 'the problem this step addresses' src/ --include='*.rs'` prints nothing and exits 1. The rule is barred because it collides with criterion 3, and this criterion is what makes the bar checkable rather than a promise in prose.

11. THE SUITE, THE VALIDATORS AND ASCII. `cargo test` passes, `cargo clippy --all-targets -- -D warnings` exits 0, both `validate` invocations print their `valid` line and exit 0, and `LC_ALL=C grep -cP '[^\t\x20-\x7e]' <file>` prints `0` for every changed file.

12. `status --step` STILL REPORTS AN ABSENT FIELD ON THE MARKDOWN SUBSTRATE. This increment drops the `(not recorded)` fallback for a TOML source and KEEPS it for the Markdown one, and no other criterion here runs `status --step` at all. Run this from the repository root, against the Markdown plan this repository already commits:

```
./target/debug/agent-flow status --plan docs/plans/agent-scaffold.md --step core-assets
```

Pass: stdout is exactly the three lines `step: core-assets`, `problem: (not recorded)`, `approach: (not recorded)`, and the exit status is 0. `--source` is not supplied and it carries no default, so the projection is read from the Markdown Roadmap, which carries no such column: `steps_from_markdown` sets both fields to `None` and the fallback is the only correct output. ANY SLUG THE ROADMAP TABLE DECLARES WILL DO, and the outcome records which one was run. `core-assets` is named so the command is executable as printed, and it is the plan's first step.

WHY THE MARKDOWN SUBSTRATE CARRIES THIS AND THE TOML ONE NEEDS NO COMMAND. What the criterion holds is increment 1's sentence "For a field the substrate does not carry, the value prints as `(not recorded)`, so an absent field is never mistaken for an empty one". An implementation that drops the fallback OUTRIGHT rather than for the TOML source only satisfies every other criterion of this increment, because after the flip no TOML step can lack a field and nothing else here reads the Markdown substrate; it prints an empty value where this criterion requires `(not recorded)`. The TOML half needs no command of its own, because criterion 1's two parse checks already make a TOML step with a missing field unbuildable.

### DOCUMENTATION IMPACT

`CHANGELOG.md`, THE `## [Unreleased]` SECTION, WHICH INCREMENT 3 OPENS. `grep -n 'Unreleased' CHANGELOG.md` exits 1 today, so the entry means opening the section rather than appending to one. The entry belongs to increment 3 and not to the batches: the batches add data to this repository's own plan, and increment 3 is where the schema changes for everybody. It records that `[[step]]` gains two REQUIRED fields, `problem` and `approach`, and that a plan written against an earlier version no longer parses until each `[[step]]` carries both. `AGENTS.md` states the duty in this repository's own copy and in the shipped pack copy alike, and `validation-constraints.md` already names `CHANGELOG.md` and its `## [Unreleased]` section for a comparable pending step, which is the shape this section follows. `CHANGELOG.md` is in criterion 9's path set for that reason.

THE PACK GUIDANCE THE FLIP MAKES STALE IS NOT LEFT TO THIS SECTION, because it is a file edit rather than a note: `pack/plan-template.steps/example-step.md` and its committed copy are named in WHAT CHANGES and in criterion 9, and `pack/plan-template.plan.toml` and its committed copy ship the placeholder values.

`README.md` IS NOT MADE STALE, MEASURED. Its one description of the plan source names the Roadmap `[[step]]` entries and lists no field of them, so a field added to `[[step]]` makes nothing in it false. Its absence from the path set is a choice.

### THE RESIDUALS THIS STEP ACCEPTS RATHER THAN CLOSES

Four. Each is recorded so a later review round does not file it as a fresh finding, and each belongs in the eventual decision receipt. This is their single home; the design pass names them and points here.

RESIDUAL 1, INTENT-PROSE STALENESS. Nothing closes the case where the recorded intent is no longer what the step is for, and no check can. Prose in a TOML string goes stale exactly as prose in Markdown does. What the field removes is the SECOND copy, not the staleness.

RESIDUAL 2, MEANINGLESSNESS UNDER A REQUIRED FIELD. A required `String` needs a value, so `pack/plan-template.plan.toml` ships placeholder text and every scaffolded plan validates on day one with that text in place. The required field makes ABSENCE unrepresentable and leaves MEANINGLESSNESS fully representable and indistinguishable from real intent. `title` carries the same property today. A `validate` rule that rejects the shipped placeholder strings is REJECTED, because it collides head-on with increment 3's own criterion that a fresh scaffold validates, which is correct under Principle 3, Safe on existing projects, and Principle 4, Idempotent. Placeholder detection belongs in `audit`, which is advisory, and it is a separate step.

RESIDUAL 3, THE CITATION PROVES A DATE AND NOT A DERIVATION. Rule 4 makes the current sidecar the primary source and the batch block's criterion 6 requires the sentence to be MOVED, so the commit that satisfies the transcribed check is the commit that held the text before the move, by construction. WHAT RULE 6 DOES PROVE, AND AN EARLIER FORM OF THIS RESIDUAL DENIED IT. The earliest-commit arm of R2 dates the sentence: a value invented during the backfill has the backfill's own commit as its earliest, so a citation to an older commit proves the sentence predates the extraction. The human decided rule 6 on 2026-08-21 (`q_id:"Q-78-earliestcommit"`) on exactly that measurement, and the ledger records the pickaxe result that made it. So the assertion that NO criterion can distinguish provenance from the extraction's own commit is false, and it must not be restated. WHAT REMAINS OPEN is narrower: rule 6 proves the sentence is old, and it does not prove that the recorded field was DERIVED from that text rather than written afresh and matched to it. The human's 2026-08-19 requirement is answered in substance, because the recorded sentence IS the one the person with the context wrote. It is not answered as a mechanical proof of derivation. If the human wants genuine retroactive extraction tested, that is a different design and it must be put as one.

RESIDUAL 4, TWO OF THE FOUR SURFACES AN ADOPTER READS REPORT SUCCESS ON THE PLAN THE FLIP BREAKS. `validate --source` exits 1 on a plan that does not parse, correctly. MEASURED on today's unmodified binary against a two-step plan omitting the ALREADY-required `title`, `next --source` prints `note: --source <path> did not parse as a <task>.plan.toml; projecting from --plan` and then `no active review loop (no plan steps found)` and EXITS 0, and `status --source` prints `plan: not provided` and EXITS 0. So `next` gives the reason as no-plan-steps rather than as a parse failure, and neither command reports the parse failure at all. WHAT A WRONG IMPLEMENTATION COULD THEN SHIP: nothing this increment builds. The mechanism is pre-existing, it is measured against a field that is already required, and no increment of this step touches `next` or `status`'s resolution behaviour. What the residual admits is that WHAT THIS COSTS A SCAFFOLDED PROJECT, above, states an adopter cost that two of the four surfaces understate: an adopter who runs `next` or `status` after the flip is told the plan has no steps rather than that it no longer parses, and must run `validate` to learn why. `validate-missing-source-exit` excludes `next` under NOT IN SCOPE, and that exclusion is written for "EVERY OTHER SUBCOMMAND THAT SKIPS A MISSING PATH", which does not describe a path that exists and fails to parse, so no step in the pass covers it. The repair, if it is wanted, is a separate step of the `validate-missing-source-exit` kind, and the alternative is widening this pass into the product behaviour it deliberately excludes. The human accepted this on 2026-08-22 as residual risk, receipt `type:"decision"` `q_id:"Q-78-round4"` in `docs/metrics/workflow.jsonl`.

### NOT IN SCOPE, NAMED SO IT IS NOT DRAWN IN

- THE `order` DELETION. It belongs to `plan-order-array-position`, which BLOCKS this step.
- THE LEDGER'S `order` CITATIONS. `ledger-order-citation-currency` owns them.
- TYPED UMBRELLA MEMBERSHIP. It left the `Q-78` pass on 2026-08-21 and `Q-79` owns it. Nothing here waits on it.
- ANY CONTENT RULE OVER THE INTENT PROSE. `validate` checks presence, emptiness and the single-line bound. It does not check that a sentence is true, and this step does not pretend that a check can. The batch block's criterion 6 is a comparison between two fields of one plan and is not a content rule.
- PLACEHOLDER DETECTION IN `validate`. Rejected above. It belongs in `audit` and is a separate step.
- THE GENERATED STEP HEADING. `render` could own the `### <slug>: <title>` heading and every sidecar could lose its own. It rewrites every sidecar, which collides head-on with this step's backfill, so the design pass declines to schedule it.
- THE EMPTY QUESTION SIDECARS. All are 0 bytes and exist only to satisfy `render`'s existence check. The design pass records this under `Q-78` item (e) as a wart in the reader's contract rather than in this schema, and schedules nothing for it.
- THE `next` EXPLORATION-PHASE DEFECT, `Q-78` item (h). It keeps its own step and its own human decision.
