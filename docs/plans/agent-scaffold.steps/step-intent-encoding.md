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

RULE 3, AN EMPTY VALUE IS ABSENCE SPELLED DIFFERENTLY, AND `validate` REJECTS IT. A required `String` accepts `""`, so a whole-plan backfill of empty strings survives the flip and satisfies any per-field presence check. `validate` therefore rejects a value that is empty after a trim. This is arithmetic over data the tool already loads and it asserts nothing about truth, so it sits on the admissible side of the line the design draws. MEASURED: with this rule, an empty backfill over the whole plan prints 202 problems and exits 1.

RULE 4, TRANSCRIBE BEFORE YOU PARAPHRASE. The problem and the approach for most steps are already written down, in the sidecar prose, by the person who had the context. The first source for each step is its own sidecar, and git history supplies the citation for that text rather than a fresh derivation of it.

RULE 5, NAME THE SOURCE FOR EVERY FIELD, AND MARK HOW IT WAS TAKEN, OUTSIDE THE PLAN. The migration record is `docs/plans/step-intent-encoding.migration.tsv`. It is a tab-separated file with a header line and one row per FIELD, not per step. Its columns are `slug`, `field`, `mark`, `source`. `field` is `problem` or `approach`. `mark` is `transcribed` or `paraphrased`. `source` is `<commit>:<path>` and nothing else, where `<path>` is the path AS OF THAT COMMIT. The record lives outside the schema because migration bookkeeping must not outlive the migration, and increment 3 deletes it.

THE BARE `<commit>` SOURCE FORM IS DELETED FROM THE GRAMMAR. A `transcribed` row that cites a bare commit cannot run the substring check that makes `transcribed` mean anything, and the transcribed count does not reveal it. Every row carries `<commit>:<path>`, `paraphrased` included. A decision receipt is reachable as `<commit>:docs/metrics/workflow.jsonl`, so the bare form buys nothing. Principle 5, Make illegal states unrepresentable, decides it: a format that cannot express the unprovable row beats a check that hunts for it. The human decided on 2026-08-21 (`q_id:"Q-78-backfillrecord"`) that the source reference and the mark do NOT enter the `[[step]]` schema, and this record is where they live instead.

THE CITED PATH IS THE PATH AT THAT COMMIT, NOT TODAY'S PATH. This is measured. The step sidecar tree did not exist until `0fadd90` (2026-07-19). For `ledger-template` the earliest commit that holds its opening sentence is `5e7ee58` (2026-07-14), and at that commit the sentence lives in `docs/plans/agent-scaffold.md` alone. A row that cites `5e7ee58:docs/plans/agent-scaffold.steps/ledger-template.md` fails `git show`, and criterion 4 of the batch block reports it as `UNRESOLVED SOURCE`. Most transcribed rows for the older steps will therefore cite `<commit>:docs/plans/agent-scaffold.md`.

RULE 6, THE SOURCE IS THE EARLIEST COMMIT THAT HOLDS THE SENTENCE. Any commit that contains a sentence satisfies a naive citation check, and the latest such commit is usually the tip, which proves nothing. `git log --oneline --reverse -S'<sentence>' -- .` returns the earliest across renames. MEASURED, the earliest commit for two live sidecar sentences is `5e7ee58` (2026-07-14) and `c44d8d1` (2026-07-28), and at `5e7ee58` the only file that holds the sentence is `docs/plans/agent-scaffold.md`, because the sidecar tree did not exist until `0fadd90` on 2026-07-19.

RULE 7, THE PARAPHRASE ROUTE IS AN OPT-OUT, SO IT IS BOUNDED AND MEASURED. A faithful paraphrase is trimmed or joined, so a substring test fails on correct work, and the substring test is therefore not applied to a `paraphrased` field. Each batch reports its transcribed and paraphrased counts, so an implementation that marks every field `paraphrased` is visible rather than silently compliant.

RULE 8, THE SENTENCE MOVES OUT OF THE SIDECAR. After a step is backfilled, its sidecar must not contain its own `problem` or `approach` string verbatim. This is a pure string comparison inside one plan, it needs no git resolution, and it catches the transcribe-then-forget-to-delete case. It is the guard duty (g) owes.

RULE 9, NO INTENT VALUE OPENS WITH A ROADMAP STATUS TOKEN. 45 sidecars open with a status token and rule 4 makes that opening the first source, so a transcription that starts at the opening word writes the token into the TOML. That re-creates the duplicate `sidecar-status-opening-drift` deletes. The transcription starts after the token.

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
- A STEP THAT CARRIES AT LEAST ONE FIELD CONTRIBUTES AN ENTRY EVEN WHEN ITS BODY IS EMPTY. A step with neither field and an empty body contributes nothing, which is today's behaviour unchanged.

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

2. THE SINGLE-LINE RULE FIRES ON ALL THREE WAYS A NEWLINE ARRIVES. Build three one-step plans in a scratch directory outside the repository, one with a `"""` block value, one with a `'''` block value, and one with a `\n` escape inside a basic string. Run `./target/debug/agent-flow validate --source <file>` on each. Each prints, on stderr, a line that ends `step \`a\` field \`problem\` must be a single line`, and exits 1. MEASURED on the `"""` form and the `\n` form, the stderr line is exactly `<file>: step \`a\` field \`problem\` must be a single line`, with nothing on stdout.

3. THE EMPTY-VALUE RULE FIRES PER FIELD. A one-step plan with `problem = ""` and `approach = ""` gives two stderr lines and exit 1:

```
<file>: step `a` field `problem` is empty
<file>: step `a` field `approach` is empty
```

MEASURED at whole-plan scale, `problem = ""` and `approach = ""` across every step of the live plan gives exactly 202 stderr lines for 101 steps and exit 1. This is the criterion that closes the measured trap where an empty backfill survives the required-field flip.

4. THE RENDER FORMAT IS PINNED IN THE GOLDEN. `src/plan/testdata/render-fixture.plan.toml` gains both fields on `alpha`, both on `gamma`, and BOTH on `eta` with only one of them filled, and the golden is regenerated. Then:

```
grep -c -F -- '- problem: The render golden pins no projected intent.' src/plan/testdata/render-fixture.md
```

Pass: stdout is exactly `1` and the exit status is 0. A missing golden file prints nothing on stdout and exits 2, so an absent input cannot pass.

THIS CRITERION IS THE ONE THAT CATCHES THE `title` TRAP. MEASURED against an implementation that adds both fields to the schema and emits neither, `cargo test` reports 0 failures, `validate --source` exits 0 and prints `7 steps, 5 questions, valid`, `render --check --strict` exits 0 and prints `up to date`, and `status --step alpha` prints both values correctly. This grep prints `0` and exits 1. Nothing else in the increment detects it.

5. THE LEADING-HEADING RULE IS PINNED BY A SIDECAR WITH PROSE ABOVE ITS HEADING. `src/plan/testdata/render-fixture.steps/gamma.md` takes a lead-in sentence above its own `###` heading, the `core-assets` shape. Then:

```
grep -A3 -F -- 'A lead-in sentence above the step' src/plan/testdata/render-fixture.md
```

Pass: the four printed lines are the lead-in sentence, a blank line, the `### \`gamma\`: The third step` heading, and a blank line, AND the two lines after those carry `- problem:` and `- approach:`. The failing implementation to look for emits the intent after line 1, which puts it above the heading.

6. THE PARTIAL CASE IS PINNED. `eta` carries `problem` and no `approach` in the fixture. `grep -A2 -F -- '### \`eta\`: The deferred step' src/plan/testdata/render-fixture.md` prints the heading, a blank line and a `- problem:` line, and no `- approach:` line follows it.

7. `next` CARRIES BOTH SLOTS. Build a one-step in-progress plan with both fields in a scratch directory, then:

```
./target/debug/agent-flow next --source intent.plan.toml --json | grep -oE '"(problem|approach)": "[^"]*"'
```

Pass: two lines on stdout, `"approach": "<value>"` then `"problem": "<value>"`, in that order, exit 0. MEASURED, the human-readable form prints the six context slots in the order `approach`, `isolation_tier`, `ledger`, `problem`, `review_findings`, `triage_findings`.

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

1. THE BATCH IS EXACTLY ITS DECLARED SLUG LIST. `git diff --name-only` over the increment lists exactly: `docs/plans/agent-scaffold.plan.toml`, `docs/plans/step-intent-encoding.migration.tsv`, `docs/plans/agent-scaffold.md`, and one file under `docs/plans/agent-scaffold.steps/` for each step in the batch that had a sentence to move. No step outside the batch gains a field, which is checked by comparing the pre and post outputs of:

```
grep -c '^problem = ' docs/plans/agent-scaffold.plan.toml
```

Pass: the post count minus the pre count equals the batch size. The outcome records both counts.

2. THE SIZING SAMPLE RUNS FIRST, IN BATCH a ONLY, AND IT REPORTS THE TWO FIELDS SEPARATELY. Before any field is filled, take the first ten steps of batch a, read each sidecar, and record in the outcome, for `problem` and for `approach` separately, how many of the ten yield a transcribable sentence and how many need a paraphrase. The design's own claim that most steps already state their intent is UNMEASURED, and this sample is the measurement. It is an acceptance criterion rather than a paragraph, because a named remedy that no criterion enforces is a remedy an implementer can skip. The recorded pair is what later batches are read against under criterion 8. One known case is named so the sample is not read as a formality: `file-dropper.md`, the shortest sidecar in the plan, states an approach and states no problem at all.

3. THE RECORD'S SHAPE AND ITS COVERAGE OF THE PLAN. Run:

```
#!/usr/bin/env bash
# R1: the migration record's shape, and its coverage of the filled fields.
REC="$1"; PLAN="$2"; AF="$3"
rows=0; bad=0
if [ "$(head -1 "$REC" 2>/dev/null)" != "$(printf 'slug\tfield\tmark\tsource')" ]; then
  echo "BAD HEADER"; bad=$((bad+1))
fi
while IFS=$'\t' read -r slug field mark source; do
  rows=$((rows+1))
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
filled=$(grep -c '^\(problem\|approach\) = ' "$PLAN")
printf 'rows=%d filled=%d bad=%d\n' "$rows" "$filled" "$bad"
```

Pass: the printed line reads `rows=<n> filled=<n> bad=0`, with the two counts EQUAL and `bad` zero. The oracle is the printed line and not the exit status, which is 0 in every case. MEASURED against four defective records:

- The record ABSENT prints `BAD HEADER` and `rows=0 filled=4 bad=1`. This closes the measured trap where the record's absence satisfied the stated pass condition.
- A record with only `slug` and `field` columns prints `BAD HEADER` and eight `BAD` rows, `rows=4 filled=4 bad=9`.
- A `transcribed` row that cites a bare commit prints `BAD SOURCE row 1: 5e7ee58` and `bad=2`.
- A filled field with no row prints `rows=2 filled=4 bad=0`, which fails on `rows != filled` rather than on `bad`. Both halves of the pass condition are therefore load-carrying and both are stated.

4. EVERY SOURCE RESOLVES, EVERY TRANSCRIBED SENTENCE IS AT ITS SOURCE, AND THAT SOURCE IS THE EARLIEST COMMIT THAT HOLDS IT. Run:

```
#!/usr/bin/env bash
# R2: source resolution, the transcribed substring test, and the earliest-commit rule.
REC="$1"; PLAN="$2"; AF="$3"
rows=0; tr=0; pa=0; bad=0
while IFS=$'\t' read -r slug field mark source; do
  rows=$((rows+1))
  if ! git show "$source" > /dev/null 2>&1; then
    echo "UNRESOLVED SOURCE row $rows: $slug $field $source"; bad=$((bad+1)); continue
  fi
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

Pass: the printed line ends `bad=0` and its `rows` equals criterion 3's `rows`. The full commit hashes are compared through `git rev-parse`, because the abbreviated `%h` width varies with repository size. MEASURED against three defective citations:

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
    case "$value" in
      "Not started"*|"In progress"*|Complete*|Skipped*|Next[.\;,:\ ]*|Optional*|Deferred*)
        echo "STATUS TOKEN $slug $field: $(printf '%s' "$value" | cut -c1-40)"; token=$((token+1));;
    esac
  done
done
printf 'checked=%d duplicated=%d status_token=%d\n' "$checked" "$dup" "$token"
```

Pass: the printed line reads `checked=<2m> duplicated=0 status_token=0`, where `m` is the number of steps filled so far across all batches. MEASURED, a transcribed sentence left in its sidecar prints `SIDECAR REPEATS checks-runner-worktree-name-collision approach` and `duplicated=1`, and a value that opens `Next. Decided (...` prints `STATUS TOKEN ledger-template problem: Next. Decided (\`Q-2\`, human). Make the r` and `status_token=1`. A correct batch prints `checked=4 duplicated=0 status_token=0` on the same fixture.

7. THE PROJECTION IS REGENERATED AND THE DIFF IS THE BATCH. `./target/debug/agent-flow render docs/plans/agent-scaffold.plan.toml` then `render --check --strict`, which prints `docs/plans/agent-scaffold.plan.toml: up to date` and exits 0. Then:

```
grep -c '^- problem: ' docs/plans/agent-scaffold.md
```

Pass: stdout equals the running total of filled steps, and the outcome records it. The same command with `approach` in place of `problem` is run separately and its count must match. The two commands are given as two commands because a reader who substitutes once checks one field, and a batch that fills `problem` and forgets `approach` passes a single-field check.

```
grep -c '^- approach: ' docs/plans/agent-scaffold.md
```

8. EVERY PARAPHRASED FIELD IS DISPOSED OF IN THE OUTCOME. This is NOT a pass-or-fail oracle and it is a bounded worklist. For every row this batch marks `paraphrased`, the outcome quotes the source sentence and the recorded sentence side by side. A row left without that pair is the batch not finished. The criterion exists because no command can test a paraphrase, criterion 4 deliberately exempts it, and a batch that marks every field `paraphrased` otherwise satisfies every mechanical check in this block. Read the count against the sizing sample recorded in batch a.

9. THE CHANGED PATH SET AND THE UNCHANGED REST. `git diff --name-only` matches criterion 1. No file under `src/`, `tests/` or `pack/` appears. `docs/metrics/workflow.jsonl` does not appear.

10. THE VALIDATORS, THE SUITE AND ASCII. Both `validate` invocations print their `valid` line and exit 0. `cargo test` passes. `LC_ALL=C grep -cP '[^\t\x20-\x7e]' <file>` prints `0` for every changed file, the migration record included.

### Increment 3, `step-intent-encoding-inc3`: the required flip, the pack, and the record deletion

RISK CLASS `risky` (two consecutive clean review rounds). THE GROUND: the increment makes both fields required, so every previously valid scaffolded plan fails to parse until its author edits it. That is squarely Principle 3, Safe on existing projects, and it is hard to roll back once a downstream author has edited. It also changes `pack/plan-template.plan.toml`, `pack/plan-template.documentation-protocol.md` and their committed copies under `docs/plans/`, which every scaffolded project inherits.

THE HUMAN DECISION THIS INCREMENT WAITED ON IS TAKEN (2026-08-21, receipt `q_id:"Q-78-requiredfields"`). `problem` AND `approach` ARE REQUIRED, IN THE SHIPPED PACK AS WELL AS HERE, over an optional field with a validation warning. The human rejected a third option, required here and optional in the pack. The human weighed the cost this increment states below, and accepted the residual that a placeholder satisfies a required field forever. So this increment builds what it already specifies, and it waits only on the review the whole step waits on.

WHAT CHANGES. `Option<String>` becomes `String` on both fields and the two `if let Some` arms in `validate` become direct reads. `render` emits both lines unconditionally. `next` wraps both in `Some` at the `steps_from_toml` boundary, so `StepInfo` keeps its `Option` for the Markdown substrate, which carries no such column. `status --step` drops the `(not recorded)` fallback for a TOML source and keeps it for the Markdown one.

Every inline `[[step]]` declaration in `src/`, `tests/` and the two template files gains both fields.

`pack/plan-template.plan.toml` and `docs/plans/TEMPLATE.plan.toml` ship placeholder values of the form `problem = "<the problem this step addresses>"` and `approach = "<how this step addresses it>"`.

`pack/plan-template.documentation-protocol.md` gains the duty (g) sentence, scoped so it does not break on the template that carries it:

```
A Step Detail below its own heading line must not repeat a `[[step]]` field. The heading line is the exception, and `render` takes it over later.
```

`docs/plans/step-intent-encoding.migration.tsv` is deleted.

WHY THE SENTENCE IS SCOPED. The unqualified form must not ship, because `pack/plan-template.steps/example-step.md:1` restates `slug` and `title` on its own first line, and so does almost every sidecar in this repository. The rule rides in this increment rather than elsewhere because this increment already edits the pack, so it already owes the rendered-pair check below.

TWO RENDERED PAIRS ARE HAND-EDITED HERE AND NO GUARD COVERS EITHER. `pack/pack.toml` maps `plan-template.plan.toml` to `docs/plans/TEMPLATE.plan.toml` and `plan-template.documentation-protocol.md` to `docs/plans/TEMPLATE.documentation-protocol.md`, both as verbatim copies with no `render = true`, so each pair is byte-identical today. `src/agents_md_drift.rs` names "the `docs/plans/TEMPLATE` family" as UNGUARDED in its own coverage block, and `.agents/checks.toml` declares only `render-check`. Criterion 5 is the guard and it is `cmp`, not `just scaffold-self`: that recipe's second command is `nix fmt`, which formats the whole tree, and this tree is not formatter-clean, so the recipe reformats files this increment did not intend and breaks criterion 9, the changed-path set, until the implementer re-renders.

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

THE ANCHOR IS THE `slug` LINE AND NOT THE `status` LINE. A `status` line also belongs to every `[[question]]` and to some waivers, so a substitution anchored on `status` over-patches. MEASURED, a `status`-anchored substitution patches 92 sites rather than 69 and produces 33 test failures from `deny_unknown_fields`.

WHY THE MIGRATION RUNS THIS WAY. The alternative, land the fields as required and backfill every step in the same commit, has no optional window at all, which Principle 5 prefers. It is rejected because one review loop would then carry every step in the plan against a cap of five rounds, which is the reason the backfill splits into six batch increments in the first place. The window in which absence is legal is six batches long, and this increment closes it, so the end state makes absence unrepresentable and no `[meta]` exemption field is needed. An exemption boundary of the `[meta].w4_baseline` kind is right for a rule that will always have exempt members and wrong for a migration that finishes.

WHAT THIS COSTS A SCAFFOLDED PROJECT, STATED HERE AND WEIGHED BY THE HUMAN. After this increment, adding a step to any scaffolded plan requires two prose sentences before the plan parses, and for an exploratory step the problem statement is often the thing the step exists to find out. The pack template must ship placeholder values, because a required `String` needs one, so every scaffolded plan validates on day one carrying placeholder intent. The required field therefore makes ABSENCE unrepresentable and leaves MEANINGLESSNESS fully representable. A `validate` rule that rejects the placeholder strings is REJECTED: it would break criterion 3 below, which is correct under Principle 3, Safe on existing projects, and Principle 4, Idempotent. Placeholder detection, if wanted, belongs in `audit` and is a separate step.

ACCEPTANCE, EACH EXECUTABLE.

1. THE FIELDS ARE REQUIRED. `grep -c 'pub(crate) problem: String,' src/plan/source.rs` prints `1`, and `grep -c 'problem: Option<String>' src/plan/source.rs` prints `0` and exits 1. A `[[step]]` that omits either field fails to parse, which is checked directly: run `validate --source` against a one-step plan with no `problem`, and it prints, on stderr, a line that carries `missing field \`problem\``, and exits 1.

2. THE 69 DECLARATION SITES ALL CARRY BOTH FIELDS. `cargo test` passes and `cargo build` reports no error. MEASURED, a flip that leaves the sites unpatched still BUILDS with 0 errors and gives 54 test failures, so the suite is a real oracle here. The path set in criterion 9 is what proves the enumeration was complete rather than lucky.

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

Pass: stdout is exactly `1`, exit 0. This is the pack-side form of increment 1 criterion 4, and it is stated because a required field that renders nowhere in the shipped template is the same defect one layer out.

5. THE TEMPLATE PAIR STAYS BYTE-IDENTICAL. `cmp pack/plan-template.plan.toml docs/plans/TEMPLATE.plan.toml` prints nothing and exits 0. See `plan-order-array-position` rule 3 for the measurement that shows nothing else detects this.

6. THE PACK PROSE RULE SHIPS AND ITS RENDERED COPY MATCHES. `grep -c -F -- 'must not repeat a \`[[step]]\` field' pack/plan-template.documentation-protocol.md` prints `1`, and the same command against `docs/plans/TEMPLATE.documentation-protocol.md` prints `1`. Two commands, given once each, because the pack source and its committed copy are two files and only the pair check proves both.

7. THE MIGRATION RECORD IS GONE. `test -e docs/plans/step-intent-encoding.migration.tsv` exits 1, and `git diff --name-status` over the increment lists `D	docs/plans/step-intent-encoding.migration.tsv`. Both halves are the criterion: the `test` alone passes on a tree where the file never existed.

8. THE LIVE PROJECTION IS COMPLETE, ONE PAIR PER STEP.

```
grep -c '^- problem: ' docs/plans/agent-scaffold.md
```

```
grep -c '^- approach: ' docs/plans/agent-scaffold.md
```

```
grep -c '^\[\[step\]\]' docs/plans/agent-scaffold.plan.toml
```

Pass: all three print the SAME number. MEASURED at 101 steps, all three print `101`. This is the criterion that proves the projection is total rather than partial, and it is the one that catches a field that exists everywhere and renders nowhere.

9. THE CHANGED PATH SET. `git diff --name-only` lists the 12 declaration-site files, plus `docs/plans/agent-scaffold.md`, plus `pack/plan-template.documentation-protocol.md` and `docs/plans/TEMPLATE.documentation-protocol.md`, plus the deleted `docs/plans/step-intent-encoding.migration.tsv`. `docs/plans/agent-scaffold.plan.toml` appears only if a `[[step.increment]]` declaration changes, and its diff must touch no `problem` or `approach` value, because the batches own those.

10. NO PLACEHOLDER-REJECTION RULE WAS ADDED. `grep -rn 'the problem this step addresses' src/ --include='*.rs'` prints nothing and exits 1. The rule is barred because it collides with criterion 3, and this criterion is what makes the bar checkable rather than a promise in prose.

11. THE SUITE, THE VALIDATORS AND ASCII. `cargo test` passes, `cargo clippy --all-targets -- -D warnings` exits 0, both `validate` invocations print their `valid` line and exit 0, and `LC_ALL=C grep -cP '[^\t\x20-\x7e]' <file>` prints `0` for every changed file.

### THE RESIDUALS THIS STEP ACCEPTS RATHER THAN CLOSES

Three. Each is recorded so a later review round does not file it as a fresh finding, and each belongs in the eventual decision receipt. This is their single home; the design pass names them and points here.

RESIDUAL 1, INTENT-PROSE STALENESS. Nothing closes the case where the recorded intent is no longer what the step is for, and no check can. Prose in a TOML string goes stale exactly as prose in Markdown does. What the field removes is the SECOND copy, not the staleness.

RESIDUAL 2, MEANINGLESSNESS UNDER A REQUIRED FIELD. A required `String` needs a value, so `pack/plan-template.plan.toml` ships placeholder text and every scaffolded plan validates on day one with that text in place. The required field makes ABSENCE unrepresentable and leaves MEANINGLESSNESS fully representable and indistinguishable from real intent. `title` carries the same property today. A `validate` rule that rejects the shipped placeholder strings is REJECTED, because it collides head-on with increment 3's own criterion that a fresh scaffold validates, which is correct under Principle 3, Safe on existing projects, and Principle 4, Idempotent. Placeholder detection belongs in `audit`, which is advisory, and it is a separate step.

RESIDUAL 3, THE CITATION PROVES PROVENANCE AND NOT DERIVATION. Rule 4 makes the current sidecar the primary source and the batch block's criterion 6 requires the sentence to be MOVED, so the commit that satisfies the transcribed check is the commit that held the text before the move, by construction. No criterion distinguishes that from a retroactive extraction, and the design cannot change to make one unless it abandons rule 4. The human's 2026-08-19 requirement is answered in substance, because the recorded sentence IS the one the person with the context wrote, and the citation names the earliest commit that holds it. It is not answered as a mechanical proof. If the human wants genuine retroactive extraction tested, that is a different design and it must be put as one.

### NOT IN SCOPE, NAMED SO IT IS NOT DRAWN IN

- THE `order` DELETION. It belongs to `plan-order-array-position`, which BLOCKS this step.
- THE LEDGER'S `order` CITATIONS. `ledger-order-citation-currency` owns them.
- TYPED UMBRELLA MEMBERSHIP. It left the `Q-78` pass on 2026-08-21 and `Q-79` owns it. Nothing here waits on it.
- ANY CONTENT RULE OVER THE INTENT PROSE. `validate` checks presence, emptiness and the single-line bound. It does not check that a sentence is true, and this step does not pretend that a check can. The batch block's criterion 6 is a comparison between two fields of one plan and is not a content rule.
- PLACEHOLDER DETECTION IN `validate`. Rejected above. It belongs in `audit` and is a separate step.
- THE GENERATED STEP HEADING. `render` could own the `### <slug>: <title>` heading and every sidecar could lose its own. It rewrites every sidecar, which collides head-on with this step's backfill, so the design pass declines to schedule it.
- THE EMPTY QUESTION SIDECARS. All are 0 bytes and exist only to satisfy `render`'s existence check. The design pass records this under `Q-78` item (e) as a wart in the reader's contract rather than in this schema, and schedules nothing for it.
- THE `next` EXPLORATION-PHASE DEFECT, `Q-78` item (h). It keeps its own step and its own human decision.
