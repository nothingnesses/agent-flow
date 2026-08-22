# Triage: `Q-78` design pass, round 3 of the reset count

Adjudicates `q78-r7-reviewer-groundblind.md` (13 findings) and `q78-r7-reviewer-adopter.md` (7 findings). Nothing else is re-adjudicated. `r6-triage.md` (round 2 of the reset count) and the ledger were read for the carried-forward routing list and for the recorded question, not to re-open their rulings.

Worktree `.claude/worktrees/q78-r7-triage`, branch `triage/q78-r7`, head `5c53016`. Every fixture lives under the session scratchpad in `triage-r7/`, a directory this triage created and owns. Nothing outside it was written or deleted. No fixture took mode 000 or 600, so none needed restoring.

MEASUREMENT HAZARD HONOURED. `grep` in this shell dispatches to `ugrep`, which recurses by default and prints per-file counts. Every regex-bearing or count-bearing command below ran as `/usr/bin/grep` by absolute path. Where the difference changes a result, it is stated.

KNOWN PRODUCT DEFECT HONOURED. `validate` exits 0 on an absent input. Every `validate` result below pins the stdout line rather than the exit code.

## Gates, run from the worktree root on the triage tree

| Gate | Result |
| --- | --- |
| `cargo test` | exit 0, no failures |
| `cargo clippy --all-targets -- -D warnings` | exit 0 |
| `validate --source ... --metrics ...` | `395 records, valid` and `docs/plans/agent-scaffold.plan.toml: 105 steps, 80 questions, valid`, exit 0 |
| `validate --source ... --workflow` | `workflow invariants hold`, exit 0 |
| `render --check --strict <PLAN>` | `docs/plans/agent-scaffold.plan.toml: up to date`, exit 0 |
| `LC_ALL=C grep -rcP '[^\t\x20-\x7e]' docs/plans/` | every file `0` |

All six ran. `render --check --strict` was given its `<PLAN>` argument. Both reviewers reported the same six results, and both reproduce here.

---

# Part 0. How I classified, stated before the rulings so it is checkable

The stop condition's literal wording, which my brief states and which `ledger:595` records, is:

- CLASS 1, a ground-blind criterion: a wrong implementation PASSES while it violates A STATED RISK GROUND, A NUMBERED RULE OR A CITED PRINCIPLE. Clean count zero.
- CLASS 2: a second-guard hole or a non-reproducing figure. Three or fewer, all `low` or `medium`, and the round is clean.
- A figure counts as class 2 if and only if it sits inside a step sidecar's increment block.

ROUND 2'S TRIAGE APPLIED A BROADER OPERATIVE TEST, and the difference is worth naming rather than silently picking one. `r6-triage.md` Part 1 states class 1 as "a criterion that a constructed wrong implementation PASSES, where that wrong implementation violates A GROUND THE INCREMENT STATES IN ITS OWN TEXT". That reaches any specification sentence, not only a risk ground, a numbered RULE or a Principle.

I CLASSIFY ON THE LITERAL WORDING, and for every finding where the broader test would give a different answer I say so in the ruling. The primary counts below are the literal wording's. The round is not clean under either, so nothing in the outcome turns on the choice, but a fix pass and a human reading this need to know which findings sit on the boundary.

ONE GAP IN THE CONDITION, FOUND WHILE APPLYING IT, AND IT IS ROUTED IN PART 5. The condition has two buckets and this round produced a defect kind that fits neither: A CRITERION THAT REFUSES A CORRECT IMPLEMENTATION. `A-F2`, `A-F6` and `G-F11` are all of that kind. They are not ground-blind, because nothing wrong passes; they are not a second-guard hole or a figure. I placed all three in class 2, which is the closer of the two buckets, and I flag the choice because at a class 2 limit of three the bucket assignment can decide a round.

---

# Part 1. Rulings on the GROUND-BLIND lens, `q78-r7-reviewer-groundblind.md`

## G-F1. UPHELD. CLASS 1. Severity `medium`.

The single-line rule is proved on `problem` and never on `approach`.

REPRODUCED. `/usr/bin/grep -n 'must be a single line' docs/plans/agent-scaffold.steps/step-intent-encoding.md` prints three rows: `:80` and `:84`, which are the two strings in the schema block, and `:144`, which is criterion 2's pinned string and names `problem`. `/usr/bin/grep -rn 'field \`approach\` must be a single line' docs/plans/` reaches the sidecar's schema block at `:84` and its rendered copy at `docs/plans/agent-scaffold.md:3513`, and no acceptance criterion anywhere.

WHAT IT VIOLATES. RULE 2 (`:31`) is a numbered RULE and it reads "`validate` therefore rejects a newline in EITHER field". An implementation that applies the rejection to `problem` alone satisfies every criterion of increment 1 and of increment 3, and RULE 2 is false of it on half its subject. Principle 5, which RULE 2 cites by name, is equally false of it.

I AGREE WITH THE REVIEWER'S ARGUMENT AND ITS ENUMERATION. Its twelve-row table of increment 1's criteria is correct: criterion 3 runs both fields for the EMPTY rule and criterion 2 is the one place the pattern is dropped.

FIX SHAPE. Criterion 2 gains its `approach` twin, written out as its own command in the shape criterion 3 and increment 3 criterion 1 already use. A substitution instruction does not close it, for the reason the same sidecar states four times.

## G-F2. UPHELD. CLASS 1. Severity `medium`.

Neither RULE 2 nor RULE 3 is pinned by any test the increments oblige, and increment 3 rewrites the code that implements both.

REPRODUCED. Increment 1's criterion 11 fixes the changed-path set and names no test file. Its criterion 12 says only "`cargo test` passes". Increment 3's criterion 2 says `cargo test` passes and `cargo build` reports no error. Neither increment obliges a single unit or integration test for either rule. The reviewer's contrast measurement also reproduces: `/usr/bin/grep -rn 'field \`.*\` is empty' src/ tests/` returns 13 rows, all in `src/metrics.rs`, six of them `assert_eq!` lines pinning the metrics log's own empty-field rejections. The `[[step]]` rules this step adds get no equivalent, by specification.

WHAT IT VIOLATES. The wrong implementation is increment 3's own stated edit taken literally: turn the two `if let Some` arms into direct reads and drop the check bodies. Increment 3's ground survives whole, in both halves, because both fields are still required and every previously valid plan still fails to parse. RULE 2, RULE 3 and Principle 5 are all false of it.

THE REVIEWER'S EVIDENCE DISCIPLINE IS RIGHT AND I RECORD IT. It refused to argue from "no test exists today", which is trivially true of an unbuilt increment, and argued from what the criteria oblige. That is the correct form for this finding.

G-F1 AND G-F2 ARE NOT THE SAME FINDING. G-F1 is a missing command in one criterion. G-F2 is a missing suite obligation across two increments, and it stands after G-F1 is fixed, because a hand-run command at increment 1 says nothing about the state of the code after increment 3 rewrites it.

## G-F3. UPHELD. CLASS 1. Severity `medium`. THE SUPPORTING ARGUMENT IS INCOMPLETE AND I CORRECT IT.

The batch block's identity check keys on `problem` alone.

REPRODUCED, from the criterion's own text at `:291`: `filled-post.txt` is built by `awk '/^slug = /{s=$0} /^problem = /{print s}'`, and `declared`, `gained`, `outside` and `missing` are all computed from that one set. The count half runs both fields. The identity half runs one.

WHAT IT VIOLATES. The batch increments' shared risk ground (`:259`) is "a batch authors TWO PROSE SENTENCES FOR UP TO 18 STEPS and MOVES the source text out of those sidecars". A batch that fills `problem` on its 18 declared slugs and `approach` on 18 steps of a later batch falsifies that premise, and the consequence, prose shipping into the published plan and not reversible by one revert, holds in full.

WHERE THE REVIEWER OVERSTATES, AND IT MATTERS TO THE FIX. It flags criterion 7's R4 clause as ambiguous and does not notice that CRITERION 6 CARRIES THE SAME AMBIGUITY. R3's pass condition reads `checked=<2m>`, "where `m` is the number of steps filled so far across all batches". On the wrong implementation `checked` is 36. Read `m` as the batch's running step total, 18, and `2m` is 36 and the clause PASSES. Read `m` as the number of steps carrying any filled field, 36, and `2m` is 72 and the clause REFUSES it. The criterion does not say which. So TWO clauses, not one, decide the wrong implementation, and both are ambiguous.

THE FINDING SURVIVES THE CORRECTION, and the correction makes it sharper. A criterion set in which a wrong implementation is refused only by whichever reading a reader happens to take of an undefined referent has not failed that implementation. The criterion whose own heading is THE BATCH IS EXACTLY ITS DECLARED SLUG LIST, and which was deliberately split into a count half and an identity half for this exact hazard, does not refuse it at all.

FIX SHAPE, LARGER THAN THE REVIEWER'S. `filled-post.txt` gains an `approach` twin and `gained`, `outside` and `missing` are computed for both. AND `m` is defined once, in criterion 6 and criterion 7 alike, so neither clause depends on a reader's choice.

## G-F4. UPHELD. CLASS 1. Severity `medium`.

Increment 3 states that two rendered pairs are hand-edited and that criterion 5 is the guard, and criterion 5 `cmp`s one pair.

REPRODUCED, all of it. `pack/pack.toml:59-61` maps `plan-template.documentation-protocol.md` to `docs/plans/TEMPLATE.documentation-protocol.md` with `ownership = "working"` and no `render = true`, so the copy is verbatim. `cmp pack/plan-template.documentation-protocol.md docs/plans/TEMPLATE.documentation-protocol.md` prints nothing and exits 0, so the pair is byte-identical today. `.agents/checks.toml` declares one `[[check]]`, `render-check`, over `docs/plans/agent-scaffold.plan.toml` alone. `src/agents_md_drift.rs:56-61` names "the `docs/plans/TEMPLATE` family" inside a COMPLEMENT, AS A RULE block whose subject is what the module does NOT guard. Criterion 5 (`:630`) reads in full: "`cmp pack/plan-template.plan.toml docs/plans/TEMPLATE.plan.toml` prints nothing and exits 0."

WHAT IT VIOLATES. Criterion 5 cites `plan-order-array-position` rule 3 by name as its own authority. RULE 3 is a numbered RULE and it reads "Every increment that touches either file runs the `cmp`". `Q-78.md:255` states the same rule for the whole family: "EVERY INCREMENT THAT TOUCHES THIS FAMILY CARRIES THE PAIR CHECK, which is `cmp`". Increment 3 touches both pairs and `cmp`s one. Its own paragraph at `:521` says the quiet part out loud: "TWO RENDERED PAIRS ARE HAND-EDITED HERE AND NO GUARD COVERS EITHER ... Criterion 5 is the guard and it is `cmp`".

THE WRONG IMPLEMENTATION IS ORDINARY, WHICH IS WHY THE SEVERITY IS NOT LOW. The increment hand-edits both sides of the pair to add one sentence. Any divergence introduced anywhere else in either file, a reflowed paragraph, a corrected typo applied to one side, a trailing-newline difference, passes criterion 5, passes criterion 6's two greps for the one sentence, and passes criterion 9, which names both paths and proves nothing about their content.

FIX SHAPE. Criterion 5 gains its second `cmp`, written out as its own command.

## G-F5. UPHELD. CLASS 2, second-guard hole. Severity `low`.

Criterion 6 says "Two commands, given once each" and gives one fenced block plus a substitution instruction.

REPRODUCED at `:632-636`: the sentence and one block against `pack/plan-template.documentation-protocol.md`, with the second path named only in prose. The same sidecar refuses that construction four times with the reason stated each time (`:556`, `:628`, `plan-order-array-position.md:181`, `validate-missing-source-exit.md:65`).

CLASS 2 AND NOT CLASS 1, AND I AGREE WITH THE REVIEWER'S OWN REASONING. A reader who follows the instruction does reach both files, so nothing wrong passes by construction. It is reported because criterion 6 is the ONLY content check on the pair G-F4 shows has no `cmp`, so this is the second guard on that pair and it has a hole in it.

## G-F6. UPHELD. CLASS 1. Severity `medium`. REPRODUCED INDEPENDENTLY, NOT ACCEPTED FROM THE REPORT.

Increment 2 criterion 2's stated pass condition is satisfied by an untouched tree and by a renumbered tree alike.

I REBUILT THE FIXTURE AND RAN P1 MYSELF. Criterion 1's own capture commands, run verbatim against this tree, print `pre=47 exempt=21 drift=26 table=105`, which matches the reviewer exactly. I then built three trees from the captured drift set, each a copy of every file `pre.txt` names, and ran P1 as printed in the sidecar:

```
UNTOUCHED   rows=26 restated=0  wrong_slug=0 number_survives=26
RENUMBERED  rows=26 restated=0  wrong_slug=0 number_survives=26
RESTATED    rows=26 restated=26 wrong_slug=0 number_survives=0
```

The untouched tree and the renumbered tree print a byte-identical line. All three satisfy all three stated clauses: `rows` equals `wc -l < drift.txt`, `wrong_slug=0`, and `restated` plus the `NUMBER SURVIVES` count equals `rows`.

THE MECHANISM, WHICH I CHECKED RATHER THAN INFERRED. Clause 1 is an identity of the loop, which increments `rows` once per line of `drift.txt`. Every row takes exactly one of three exits, so `rows = restated + wrong + residual` always, and clause 3 is clause 2 restated. The only substantive clause is `wrong_slug=0`, and neither an untouched tree nor a renumbered one has an annotation to be wrong about. A renumbering cannot escape the residual arm in either direction, because `expect` holds only the citations at or below 83 on that line and `actual` holds every citation still on it, so any surviving number sends the row to `NUMBER SURVIVES`.

WHAT IT VIOLATES. RULE 4 (`:29`) is a numbered RULE, it cites Principle 8 by name, and its own last sentence is "Criterion 2 of increment 2 detects a renumbering." Measured, the pass condition does not. Increment 2's risk ground (`:254`) says "Criterion 2 is a mechanical oracle over the numbered citations, and criterion 3 is a bounded worklist ..., so ONE HALF of the increment carries a reading", and criterion 7 repeats it. Measured, both halves carry a reading.

THE BACKSTOP IS REAL AND THE REVIEWER STATED IT AGAINST ITS OWN FINDING, WHICH I ENDORSE. Criterion 2's next sentence obliges the outcome to enumerate every `NUMBER SURVIVES` row as a verbatim quotation whose restatement would falsify it, and exactly one row qualifies today. An implementer who discharges that reading refuses the untouched and renumbered trees, and the `number_survives=1` sentence refuses the restate-everything tree. What is defeated is the pass condition and the ground's claim about which half is mechanical, not the criterion's every last line.

FIX SHAPE. Move the two discriminating equalities the criterion's own MEASURED table already states, `restated = rows - E` and `number_survives = E`, into the Pass clause.

## G-F7. UPHELD AS A DEFECT. CLASS OVERRULED, FROM CLASS 1 TO CLASS 2. Severity `medium`. ONE OF ITS THREE STATED GAPS IS FALSE.

Criterion 2's `handover.txt` capture is not executable as printed.

BOTH MEASUREMENTS REPRODUCE, AND I RAN BOTH. With `WORKLIST` set to the 36 slugs criterion 1's anchored selector prints, criterion 12's command run VERBATIM against the live tree prints `rows=0`, because every one of the 36 openings still begins with an uppercase status token and so matches `[A-Z]*`. Run against a throwaway copy in which each of those 36 opening lines has lost its leading token and delimiter, the same command prints `rows=19`, and the 19 slugs are exactly the 19 the reviewer lists and exactly the 19 the sidecar's own paragraph at `:23` names. The worklist is then 17.

THE THIRD STATED GAP IS FALSE AND I OVERRULE IT. The reviewer writes "and nothing states the strip". Criterion 2 states it, in the same sentence it names the file: "`handover.txt` is criterion 12's command run over a throwaway copy of `docs/plans/agent-scaffold.steps/` IN WHICH EVERY SELECTED FILE'S OPENING LINE HAS LOST ITS LEADING TOKEN." That sentence also fixes the input set as the SELECTED set, which is the other half of what the reviewer says is missing.

WHAT SURVIVES, AND IT IS A REAL DEFECT. Criterion 12's command hard-codes `docs/plans/agent-scaffold.steps/$slug.md`, so pointing it at the throwaway copy needs a substitution the sidecar never writes out, and its `$WORKLIST` is defined at `:196` as "THIS STEP'S WORKLIST from criterion 2", which criterion 2 defines as `anchored` minus `handover`, so the command text is circular for the one capture that produces `handover.txt`. Only criterion 2's prose breaks the circle. An implementer who copies the command rather than reading the sentence gets an empty `handover.txt`, and from there the worklist becomes all 36 and the criteria jointly endorse doing the successor step's work inside this step, which falsifies this increment's own risk-ground premise and the human decisions `Q-78-driftsplit` and `Q-78-drifthandover`.

WHY CLASS 2 AND NOT CLASS 1. Class 1 requires a wrong implementation to PASS. This one passes only for a reader who takes half of criterion 2's sentence (the selected set) and discards the other half (the strip) in the same breath. That is an executability defect in a capture command and a hole in the guard that fixes the split, which is the class 2 shape. The reviewer reached class 1 by way of the false third gap, and with that gap removed the class does not hold.

FIX SHAPE, UNCHANGED FROM THE REVIEWER'S. Criterion 2 writes the handover capture out as a command of its own: the copy, the strip, the path root and the selected-set slug list, in the shape criterion 1 already uses for the anchored selector.

## G-F8. UPHELD. CLASS 2, second-guard hole. Severity `low`.

Criterion 8's verification command cannot run.

REPRODUCED, from the worktree root:

```
$ /usr/bin/grep -c 'fn .*missing_.*_path' tests/
/usr/bin/grep: tests/: Is a directory
0
exit=2
```

There is no `-r`. GNU grep refuses the directory, prints `0` on stdout and exits 2, so the count the outcome is told to record is `0` whether the suite holds five such tests, one, or none. I ALSO MEASURED THE SHELL'S OWN `grep`, WHICH THE REVIEWER DID NOT, and it does not save the criterion either: `ugrep` recurses by default and prints one `<path>:0` row per test file, which is not a count and is not what the criterion asks the outcome to record.

WHY IT MATTERS MORE THAN ITS SEVERITY SUGGESTS. Criterion 8 is the durability guard for the whole increment, and its own text is the argument for it: "A criterion that only runs by hand does not survive the increment, which is why the pair lives in the suite as well as in criteria 4 and 5." The prose obligation, five tests for five branches, is explicit and a reviewer reads it, and `cargo test` in criterion 11 runs whatever tests exist, which is why this is class 2 rather than class 1.

FIX SHAPE. `grep -rc` over `tests/`, or name the test file.

## G-F9. UPHELD. CLASS 2, second-guard hole. Severity `low`.

Criterion 5's diff bound is one line-pair per file looser than its own justification.

REPRODUCED by reading `:181`: "at most 2 added and 2 removed lines, since each opening is one line in an unwrapped file and the fix rewrites that line in place rather than splitting it." A one-line in-place rewrite is one added and one removed. The named exception, `workflow-calibration.md`, is given 4 and 4 for two edits, so the doubling is consistent rather than a slip.

WHAT THE SLACK ADMITS. These sidecars are not hard-wrapped, so one line is one paragraph, and no other criterion reads below the opening line: criteria 1, 10, 11 and 12 all read the first non-blank non-heading line only, criterion 4 checks path names, and criterion 7 re-renders whatever is there. The step's own NOT IN SCOPE bullet at `:112` excludes "ANY SIDECAR TEXT BELOW THE OPENING LINE" with one named exception, and item `B`'s own argument at `:122` is that "while you are in the file anyway" is the habit the 2026-08-13 audit measured.

CLASS 2 AND NOT CLASS 1, WHICH IS THE REVIEWER'S OWN CALL AND IT IS RIGHT. What the bound fails to hold is a scope statement rather than a risk ground, a numbered RULE or a cited Principle.

## G-F10. UPHELD. CLASS OVERRULED, FROM CLASS 1 TO CLASS 2. Severity `low`. THE STATED WRONG IMPLEMENTATION DOES NOT REPRODUCE AND I REPLACE IT.

No criterion reads the head of the three new error lines, so the `error:` prefix is pinned nowhere.

THE CORE CLAIM REPRODUCES. Criteria 2, 3 and 4 each require "stderr carries a line ENDING" with the message tail. Criterion 1 quotes the pre-change stderr, which has no prefix. Criterion 7 pins a different string. Criterion 9 reads `--help`. Nothing reads the head of the line.

THE REVIEWER'S OWN WRONG IMPLEMENTATION FAILS, AND ITS OWN EVIDENCE SHOWS IT. It writes that "an implementation that changes only the exit path, leaving both lines byte-identical, satisfies criteria 2 and 4 as written". Measured in an empty directory outside the repository with today's binary:

```
no metrics log at docs/metrics/workflow.jsonl; nothing to validate
no source plan at docs/plans/TEMPLATE.plan.toml; nothing to validate
exit=0
```

Those lines END `; nothing to validate`, not with the path. A byte-identical implementation therefore FAILS criteria 2, 3 and 4, which require the line to end with the path. The reviewer quotes exactly these two lines and then draws the opposite conclusion from them.

THE FINDING SURVIVES WITH A DIFFERENT CONSTRUCTION. Drop the `; nothing to validate` tail, which the criteria force, add no prefix, and change the exit path. That implementation satisfies criteria 2, 3 and 4 and exits 1, and the MESSAGES block's premise, "each keeps its current wording AND takes an error prefix", is false of it while its consequence, "an existing reader recognises the line", still holds because the wording is kept.

WHY CLASS 2 UNDER THE LITERAL WORDING. The MESSAGES block at `:37` is a specification sentence with a justification clause. It is not the increment's risk-class ground, not a numbered RULE and not a cited Principle. UNDER ROUND 2'S BROADER OPERATIVE TEST, "a ground the increment states in its own text", THIS IS CLASS 1, and I record that plainly so the boundary is visible rather than buried.

## G-F11. UPHELD. CLASS 2. Severity `low`. THE FIT TO THE BUCKET IS BY RESIDUE AND I SAY SO.

Criterion 4 and criterion 6 specify incompatible `eta` fixtures.

REPRODUCED by reading. Criterion 4 (`:158`): the render fixture "gains both fields on `alpha`, both on `gamma`, and BOTH on `eta` with only one of them filled". Criterion 6 (`:176`): "`eta` carries `problem` and no `approach` in the fixture", and its pass condition is four printed lines whose fourth is a BLANK line.

WHY THE TWO CANNOT BOTH HOLD. Under criterion 4's plain reading `eta` carries `approach` present and empty. RULE 3 (`:33`) rejects a value that is empty after a trim, so the fixture would carry a value the step's own numbered RULE forbids. And the render sub-rule at `:100`, "A STEP THAT CARRIES ONLY ONE FIELD emits only that line", no longer applies to `eta`, so `render` emits an `- approach: ` line and criterion 6's fourth line is that line rather than a blank.

WHICH ONE IS RIGHT. Criterion 6, and I agree with the reviewer. It states the intent unambiguously and it is the criterion the render sub-rule needs a fixture for. Criterion 4's "BOTH on `eta`" reads as a slip for "one of them on `eta`".

THE CLASS. This is not ground-blind, because nothing wrong passes: it is two criteria that cannot both be satisfied, so it refuses a correct implementation instead. It is not a figure. I place it in class 2 as the closer bucket and flag the condition's missing bucket in Part 5.

## G-F12. UPHELD. CLASS OVERRULED, FROM CLASS 1 TO CLASS 2. Severity `low`.

Increment 3 changes `status --step` and runs no `status --step` command, and `src/main.rs` is absent from its changed-path set.

BOTH HALVES REPRODUCE. Increment 3's WHAT CHANGES (`:505`) states "`status --step` drops the `(not recorded)` fallback for a TOML source and keeps it for the Markdown one", and increment 3's acceptance block contains no `status --step` command at all. `StatusArgs` is at `src/main.rs:496` and `run_status` at `src/main.rs:1233`. `step_views` (`src/plan/source.rs:416`) projects `slug` and `status` and nothing else, so `status --step` cannot read the intent through `PlanProjection`. The declaration-site search reproduces row for row on this tree, 12 files and 69 sites, and `src/main.rs` is in neither that group nor criterion 9's four further paths:

```
1  docs/plans/TEMPLATE.plan.toml        1  pack/plan-template.plan.toml
2  src/next.rs                          3  src/plan/render.rs
32 src/plan/source.rs                   7  src/plan/testdata/render-fixture.plan.toml
3  src/plan/testdata/skeleton.plan.toml 13 src/workflow.rs
1  tests/metrics_and_ledger_anchor_to_the_plan_source.rs
4  tests/unsafe_pairings_are_refused_and_omitted.rs
1  tests/validate_toml_primary_skips_markdown_plan.rs
1  tests/validate_workflow_toml_source_needs_no_plan.rs
```

SO THE INCREMENT EITHER DESCRIBES AN EDIT ITS OWN PATH-SET CRITERION REFUSES, OR IT DESCRIBES NO EDIT AND ITS WORDING IS WRONG. The criteria do not say which, and that is the finding.

WHY CLASS 2 UNDER THE LITERAL WORDING. The wrong implementation the reviewer names, dropping the fallback outright rather than for the TOML source only, does pass every criterion. What it falsifies is increment 1's sentence at `:123`, "For a field the substrate does not carry, the value prints as `(not recorded)`, so an absent field is never mistaken for an empty one". That is a specification sentence, not a risk ground, a numbered RULE or a cited Principle. UNDER ROUND 2'S BROADER TEST THIS IS CLASS 1, and the path-set half is the same defect kind as `A-F2` in the same criterion.

FIX SHAPE, AND IT IS ONE EDIT SHARED WITH `A-F2`. Criterion 9's path set is settled once, covering `src/main.rs` and `docs/plans/TEMPLATE.md`, and increment 3 gains one `status --step` command against the Markdown substrate.

## G-F13. UPHELD. CLASS 2, non-reproducing measurement inside an acceptance criterion. Severity `low`.

Criterion 11's enlarged-word-list claim reproduces on neither scope.

I MEASURED BOTH SCOPES MYSELF. Criterion 11 runs over THIS STEP'S WORKLIST, which criterion 2 defines as `anchored` minus `handover`, and which I computed at 17 from my own captures. Over that worklist the enlarged list picks up ONE row:

```
doc-redundancy-cleanup	when built
```

Over the SELECTED set of 36 it picks up FOUR:

```
doc-redundancy-cleanup		when built
reviewer-reproducible-evidence	paused
structured-skeleton		blocked
task-entry-regrounding		to do
```

The criterion names the pair `doc-redundancy-cleanup` (on `when built`) and `reviewer-reproducible-evidence` (on `paused`). `reviewer-reproducible-evidence` is on the HANDOVER list, so criterion 11 never reads it. The named pair matches neither scope.

THE CLAIM THE SENTENCE EXISTS TO SUPPORT DOES HOLD, and the reviewer says so, which is the right way to file this. `planner-folds-decisions` is on the worklist, measured, and the enlarged list does not reach it.

THE FIGURE QUALIFIES AS CLASS 2 UNDER THE BRIEF'S TEST, because it sits inside an acceptance criterion of a step sidecar's increment block, which is one of the three admitted locations.

---

# Part 2. Rulings on the ADOPTER AND EXECUTABILITY lens, `q78-r7-reviewer-adopter.md`

BOTH `high` FINDINGS ARE UPHELD. No dismissal at or above `high` occurred, so NO BACKSTOP RE-CHECK IS OWED and convergence is not blocked on one.

## A-F1. UPHELD. CLASS 1. Severity `high`.

The shipped pack tells every scaffolded project that a `[[step]]` carries `order`, and no increment in the pass corrects it.

REPRODUCED. `pack/AGENTS.md:30` reads "the `<task>.plan.toml` skeleton holds the Roadmap (`[[step]]` entries with status and order)". `/usr/bin/grep -rn 'entries with status and order'` returns exactly three files: `pack/AGENTS.md`, the committed root `AGENTS.md` and `.agents/AGENTS.reference.md`. `pack/pack.toml:27-31` and `:98-102` copy `pack/AGENTS.md` to both destinations with `render = true`, so every scaffolded project receives two copies of the sentence. `cmp AGENTS.md pack/AGENTS.md` exits 1, differing at line 41, so the root copy is a render rather than a byte copy, and `the_committed_scaffold_matches_a_fresh_render` at `src/agents_md_drift.rs:377` pins it. Correcting the pack source therefore forces the two committed copies to move with it or `cargo test` fails.

NO INCREMENT REACHES THE SENTENCE, AND EACH EXCLUSION IS EXPLICIT. `plan-order-array-position` increment 1 criterion 8 gives an exact 16-path list whose only `pack/` member is `pack/plan-template.plan.toml`. Its increment 2 criterion 5 reads "No file under `src/`, `tests/` or `pack/` appears." `step-intent-encoding` increment 3 criterion 9 lists the 12 declaration-site files plus four more, and `pack/AGENTS.md` is in neither group. `sidecar-status-opening-drift`'s DOCUMENTATION IMPACT reads "The pack is untouched by this step."

WHY THE SEARCHES MISS IT, WHICH THE REVIEWER DIAGNOSES CORRECTLY. Both steps establish their scope by a search anchored on a TOML assignment, `(\\n|^)order = ` and `(\\n|^)slug = `. I reproduced both and they return exactly the 12 files and the per-file counts the two sidecars tabulate, so the searches are right for what they search. The sentence is prose, and prose is outside them.

WHAT IT VIOLATES. `plan-order-array-position` increment 1's stated risk ground is that the deletion means "every previously valid plan in every scaffolded project fails to parse until edited" and that this is "widely depended on". An implementation that satisfies every criterion of that increment ships, to every one of those projects, the instruction to write the field that now makes the plan fail to parse. The criteria are blind to the consequence their own risk ground names, and criterion 8's exact path list REFUSES the correction rather than merely omitting it.

I CORRECT THE FIX SHAPE, BECAUSE THE REVIEWER'S WOULD BREACH THE PASS'S OWN CONSTRAINT. The `Q-78` pass authors plan content only and must not touch `src/`, `Cargo.toml` or `pack/`, which the ledger records and which measures true: `git log a6e1d7f..HEAD -- pack/` on this branch is EMPTY. So the fix is NOT to edit `pack/AGENTS.md` in this pass. It is to add `pack/AGENTS.md`, the root `AGENTS.md` and `.agents/AGENTS.reference.md` to the changed-path set of whichever increment ships the deletion, and to state the edit in that increment's WHAT CHANGES, so the implementer makes it and the path-set criterion admits it. That edit is plan content and this pass can make it.

## A-F2. UPHELD. CLASS 2. Severity `medium`. THE FIT TO THE BUCKET IS BY RESIDUE, AS FOR `G-F11`.

Increment 3's changed-path set forbids re-rendering `docs/plans/TEMPLATE.md`, which a correct implementation must re-render.

REPRODUCED. `git ls-files 'docs/plans/TEMPLATE*'` lists `docs/plans/TEMPLATE.md` as committed. `./target/debug/agent-flow render --check docs/plans/TEMPLATE.plan.toml --strict` prints `docs/plans/TEMPLATE.plan.toml: up to date` and exits 0 on the untouched tree, so the committed file is a current render of that source. `docs/plans/TEMPLATE.plan.toml` is one of the 12 declaration sites increment 3 requires to carry both fields, and increment 3 states at `:509` that it ships placeholder values. Increment 1's render rule (`:89-94`) emits the two lines into the Step Details body immediately after the leading heading line, and `docs/plans/TEMPLATE.md:49` is that heading. So the committed projection changes, necessarily.

CRITERION 9 DOES NOT LIST IT. Its enumeration is the 12 declaration-site files, `docs/plans/agent-scaffold.md`, the two `documentation-protocol` files and the deleted migration record, with one stated conditional member. An implementer who obeys it commits a stale `docs/plans/TEMPLATE.md`; one who re-renders fails it.

NOTHING ELSE DETECTS THE STALE STATE. `.agents/checks.toml` declares one check and it names `docs/plans/agent-scaffold.plan.toml`. `src/agents_md_drift.rs:60` names the `docs/plans/TEMPLATE` family as outside its coverage.

THE REVIEWER'S SCOPING IS CORRECT AND I ENDORSE IT. A fresh scaffold is unaffected, because `scaffold` re-renders `TEMPLATE.md` into the target project rather than copying the committed one. What ships stale is this repository's own committed copy, and what is unbuildable as written is criterion 9.

THE SIBLING CONTRAST IS ALSO CORRECT, AND IT IS THE REASON THIS IS NOT A GENERAL RULE. `plan-order-array-position` increment 1 also edits `docs/plans/TEMPLATE.plan.toml` and its criterion 8 also omits `docs/plans/TEMPLATE.md`, correctly, because `render` emits no order column and the template holds one step, so that edit leaves the projection byte-identical. Only increment 3's edit reaches the projection.

FIX SHAPE. Shared with `G-F12`: criterion 9's path set is settled once, adding `docs/plans/TEMPLATE.md` and `src/main.rs`.

## A-F3. UPHELD. CLASS 1. Severity `high`.

The pack's one how-to-add-a-step sentence becomes a recipe for a plan that does not parse, and no increment updates it.

REPRODUCED. `pack/plan-template.steps/example-step.md:3` is the whole of the pack's guidance: "To add a step, add a `[[step]]` entry to the `.plan.toml` and a matching `<slug>.md` body sidecar in this directory, then re-render." `/usr/bin/grep -rn 'add a step\|new step' pack/` returns that one line and nothing else. `pack/pack.toml:84-85` copies the file to `docs/plans/TEMPLATE.steps/example-step.md`, and `render` inlines it into `docs/plans/TEMPLATE.md` under the example step's own heading.

THE FAILURE THE REVIEWER MEASURED IS THE EXPECTED ONE AND ITS SHAPE IS CONFIRMED HERE ON TODAY'S BINARY. A `[[step]]` block that omits an already-required field aborts the parse on the FIRST missing field:

```
$ agent-flow validate --source notitle.plan.toml
notitle.plan.toml: malformed `<task>.plan.toml`: TOML parse error at line 5, column 1
missing field `title`
exit=1
```

So after the flip an operator following the shipped sentence learns about `approach` only after supplying `problem` and re-running. Two edits, two runs, per the reviewer's measurement against its post-change build.

WHAT IT VIOLATES. Increment 3's own WHAT THIS COSTS A SCAFFOLDED PROJECT paragraph (`:552`) states the cost the human weighed and cites Principle 3, Safe on existing projects, and Principle 4, Idempotent, by name in the same paragraph. Shipping, to every scaffolded project, an instruction whose literal execution produces a plan that no longer parses is exactly what Principle 3 is cited to prevent, and every criterion of increment 3 passes over it. `sidecar-status-opening-drift`'s DOCUMENTATION IMPACT reads this exact file and concludes "no shipped guidance, prompt or template goes stale", which is true of the status-token deletion and false of the required-field flip.

THE AGGRAVATING FACT THE REVIEWER NAMES IS RIGHT. Increment 3 already carries one pack prose edit, on the stated ground that "this increment already edits the pack", so the pass has a home for this edit and did not use it.

FIX SHAPE, CORRECTED AS FOR `A-F1`. Not a pack edit in this pass. Add `pack/plan-template.steps/example-step.md` and its committed copy to increment 3's changed-path set and state the edit in WHAT CHANGES.

## A-F4. UPHELD AS VALID. CLASS NONE: it bears on the arithmetic and not on this round's cleanliness. Severity `medium`.

`next` and `status` report success and exit 0 on the plan the flip breaks.

REPRODUCED WITH THE WORKTREE'S OWN UNMODIFIED BINARY, on a two-step plan omitting the already-required `title`:

```
$ agent-flow next --source notitle.plan.toml
note: --source notitle.plan.toml did not parse as a `<task>.plan.toml`; projecting from --plan
no active review loop (no plan steps found)
exit=0

$ agent-flow status --source notitle.plan.toml
plan: not provided
exit=0
```

`validate` exits 1 on the same file, correctly. So two of the four surfaces an adopter reads report success on a plan that does not parse, and `next` gives the reason as no-plan-steps rather than as a parse failure.

THE REVIEWER'S SCOPING IS EXACTLY RIGHT AND IS WHY THE CLASS IS NONE. The mechanism is pre-existing, the reviewer says so, and it does not ask for a fix in this pass. The finding is that the adopter cost this pass states is understated by the surface it lands on, and that increment 3's THE RESIDUALS block records three residuals and not this one. `validate-missing-source-exit` excludes `next` under NOT IN SCOPE, and the exclusion is written for "EVERY OTHER SUBCOMMAND THAT SKIPS A MISSING PATH", which does not describe a path that exists and fails to parse.

WHY IT IS NOT CLASS 1 OR CLASS 2. It is not a criterion defect of any kind. No criterion is blind and no guard has a hole; the specification omits a residual. Under the stop condition as written it does not bear on cleanliness. It IS a valid finding, so it counts for the arithmetic, and it is my first-choice residual in Part 6.

## A-F5. UPHELD. CLASS 2, second-guard hole. Severity `low`.

The pack prose rule increment 3 ships can land inside the placeholder the pack tells the adopter's planner to delete.

REPRODUCED. The entire body of `pack/plan-template.documentation-protocol.md` below its heading is one angle-bracket placeholder note, verified by reading the whole file. `pack/prompts/planner.md:5` directs the adopter's planner: "Delete the template's angle-bracket placeholder notes as you fill each part in." Increment 3 says the file "gains the duty (g) sentence, scoped so it does not break on the template that carries it", and does not say whether the sentence lands inside the brackets or outside them. Criterion 6's `grep -c -F` prints `1` in both placements.

SO THE CRITERION CANNOT SEPARATE A RULE THAT SURVIVES INTO THE ADOPTER'S PLAN FROM ONE THE FIRST PLANNER DELETES ON SIGHT. The same ambiguity carries into the paired check against the committed copy, since that copy is verbatim.

## A-F6. UPHELD. CLASS 2. Severity `medium`. THE FIT TO THE BUCKET IS BY RESIDUE, AS FOR `A-F2`.

Two increments break every existing plan and neither carries a documentation impact, and the path sets forbid the entry.

REPRODUCED. Of the five sidecars in scope, exactly one carries a DOCUMENTATION IMPACT section:

```
step-intent-encoding: 0        plan-order-array-position: 0
sidecar-status-opening-drift: 1  ledger-order-citation-currency: 0
validate-missing-source-exit: 0
```

The one that has it is the step that ships nothing to a scaffolded project. `docs/plans/agent-scaffold.steps/validation-constraints.md:171` names, for a comparable pending step, "`CHANGELOG.md`, the `## [Unreleased]` section" and states why, and repeats it for two further increments. `AGENTS.md:30` states the duty itself, in this repository's own copy and in the shipped pack copy alike. `/usr/bin/grep -n 'Unreleased' CHANGELOG.md` exits 1, so the entry means opening a section rather than appending to one.

AND THE PATH SETS DO NOT MERELY OMIT THE ENTRY. `plan-order-array-position` increment 1 criterion 8 reads "lists exactly" followed by 16 paths, and `step-intent-encoding` increment 3 criterion 9 enumerates its set the same way. An implementer who writes the CHANGELOG entry fails the criterion.

THE REVIEWER'S TWO NARROWINGS ARE CORRECT AND I KEEP THEM. `README.md` is not made stale, measured, and the CHANGELOG entry means opening `## [Unreleased]`.

WHY CLASS 2 AND NOT CLASS 1. What the omission violates is `AGENTS.md:30`, a workflow duty, rather than a risk ground, a numbered RULE or a cited Principle of the increment. The path-set half is the same defect kind as `A-F2`: a criterion that refuses a correct implementation.

## A-F7. UPHELD. CLASS 1. Severity `medium`.

RULE 9 states a population of 45 that the same file's criterion 6 paragraph and the sibling sidecar both put at 36, and acting on the 45 damages nine legitimate problem statements that no criterion checks.

I RAN ALL THREE SELECTORS MYSELF, VERBATIM FROM `sidecar-status-opening-drift` CRITERION 1:

```
relaxed  45
anchored 36
complement 9: checks-kind-skip, classification-trivial-rename, drift-guard-optionality,
              instrument-magic-filename, module-spec-description-dead, repoint-resume-prompts,
              se-principle-namespace, sidecar-ref-empty-string, sidecar-ref-symlink
```

So RULE 9's "45 sidecars open with a status token" is the RELAXED count, and the anchored form, which is the form `step-intent-encoding`'s own R3 regex uses at criterion 6, reaches 36.

THE FILE CONTRADICTS ITSELF AND THE LATER PARAGRAPH IS RIGHT. `step-intent-encoding.md:422` states that an unanchored form fired on "Deferred cleanup from the `Q-44` audit ...", that this sentence "is the faithful opening of six sidecars in this plan and A LEGITIMATE PROBLEM STATEMENT", and that "the anchored form does not fire on it". `sidecar-status-opening-drift.md:22` agrees and says those nine "are NOT in this step's scope at all". RULE 9 asserts of all 45 that transcribing from the opening word "re-creates the duplicate `sidecar-status-opening-drift` deletes", which is false of nine of them.

WHAT IT VIOLATES, AND WHY IT IS CLASS 1 RATHER THAN A STALE FIGURE. RULE 9 is a numbered RULE and its operative instruction is "The transcription starts after the token." Applied to the nine, it turns a legitimate problem statement into a mutilated fragment, and I checked each guard that might catch it. R3's regex is the anchored one and stays silent on "cleanup from the `Q-44` audit ...". R3b prints only values the relaxed form reaches AND the anchored form does not, which is the wrong direction for a value that has lost its leading word. R2's transcribed substring test PASSES, because the mutilated sentence really is a substring of the cited blob. Criterion 12 belongs to the other step and runs over that step's worklist. Criterion 8's reading is the only thing left, and the sidecar itself calls that "the weakest guard this pass uses". So a wrong implementation, and it is the implementation RULE 9 directs, passes every mechanical criterion in the batch block.

THE SECOND, INDEPENDENT HALF ALSO REPRODUCES. The five steps sit at declaration positions 101 to 105, all `not-started`, and `step-intent-encoding` at 105 is the only one with a `blocked_by`, naming `plan-order-array-position`:

```
101 sidecar-status-opening-drift   102 validate-missing-source-exit
103 plan-order-array-position      104 ledger-order-citation-currency
105 step-intent-encoding  blocked_by = ["plan-order-array-position"]
```

`select_active_loop` takes the lowest-order ready pending step, so the drift step runs FIRST and the backfill runs LAST. By the time RULE 9 applies, the drift step has deleted the token from its 17 worklist files, so the openings that still carry one are the 19 handover files plus the 9 adjectival ones, and neither 45 nor 36 is the population RULE 9 will meet.

FIX SHAPE, THE REVIEWER'S AND I AGREE. State 36 as the label population or 19 as the population RULE 9 will actually meet, and exclude the nine adjectival openings by name, as both sibling paragraphs already do.

---

# Part 3. The deduplicated count

TWENTY RAW, TWENTY DISTINCT, ZERO DISMISSED. The two lenses overlap at three REMEDY SITES and at no finding. I looked for duplicates deliberately, because 20 distinct from 20 raw is an unusual result and the brief warns against it.

WHY THERE ARE NO DUPLICATES. The ground-blind lens attacks the criteria from inside the specification; the adopter lens has never been run and attacks the shipped pack and the executability of the increments. Their subject matter barely intersects: no adopter finding is against a criterion's falsification coverage, and no ground-blind finding is against a file under `pack/`. Round 2 of the reset count returned 27 raw and 25 distinct valid from two lenses that shared more ground than these two do.

THE THREE SHARED REMEDY SITES, so the fix pass treats each once rather than three times:

1. INCREMENT 3 CRITERION 9, THE CHANGED-PATH SET: `G-F12` (`src/main.rs`) and `A-F2` (`docs/plans/TEMPLATE.md`). Two files, two different reasons, one criterion, one edit. `G-F12` carries a second half, that no criterion of increment 3 runs `status --step` at all, which survives the path-set fix.
2. INCREMENT 3 CRITERION 6, THE PACK PROSE RULE: `G-F5` (one command with a substitution instruction) and `A-F5` (the grep passes in both placements of the sentence). Two different defects in one criterion.
3. THE PACK PROSE SURFACES NO DECLARATION-SITE SEARCH REACHES: `A-F1`, `A-F3` and `A-F6`. One root cause, three files, three separate consequences and three separate edits. Counted three times, routed together, in the same treatment round 2's triage gave `R6-G1` and `R6-C11`.

FOUR FINDINGS SHARE ONE SHAPE AND ARE NOT ONE FINDING. `G-F1` proves a rule on `problem` and not `approach`; `G-F3` proves the batch identity on `problem` and not `approach`; `G-F4` `cmp`s one pair of two; `G-F12` pins one substrate of two. The reviewer names the pattern and does not merge them, correctly: each has its own site and its own one-command remedy.

## Counts

| | Literal wording | Round 2's broader test |
| --- | --- | --- |
| Distinct valid | 20 | 20 |
| Dismissed | 0 | 0 |
| CLASS 1 | 8 | 11 |
| CLASS 2 | 11 | 8 |
| CLASS NONE | 1 | 1 |
| Severity ceiling | `high` | `high` |

CLASS 1, LITERAL WORDING (8): `G-F1`, `G-F2`, `G-F3`, `G-F4`, `G-F6`, `A-F1` (`high`), `A-F3` (`high`), `A-F7`.

CLASS 2, LITERAL WORDING (11): `G-F5`, `G-F7`, `G-F8`, `G-F9`, `G-F10`, `G-F11`, `G-F12`, `G-F13`, `A-F2`, `A-F5`, `A-F6`.

CLASS NONE (1): `A-F4`.

THE THREE THAT MOVE BETWEEN THE TWO TESTS: `G-F10`, `G-F12` and `A-F2`, all class 2 on the literal wording and class 1 on round 2's broader one.

SEVERITIES: 2 `high` (`A-F1`, `A-F3`), 10 `medium` (`G-F1`, `G-F2`, `G-F3`, `G-F4`, `G-F6`, `G-F7`, `A-F2`, `A-F4`, `A-F6`, `A-F7`), 8 `low` (`G-F5`, `G-F8`, `G-F9`, `G-F10`, `G-F11`, `G-F12`, `G-F13`, `A-F5`). I changed no severity. I changed three classes: `G-F7` down from 1 to 2, `G-F10` down from 1 to 2, `G-F12` down from 1 to 2, and I raised no reviewer's class, though three adopter findings the reviewer did not class at all fall in class 1.

MY CLASS 1 SET IS NOT THE REVIEWER'S. The ground-blind reviewer filed 8 class 1 and I uphold 5 of them, moving `G-F7`, `G-F10` and `G-F12` to class 2. The other three class 1 items are adopter findings the ground-blind reviewer never saw. The arithmetic arrives at the same number by a different route, which is worth stating so the count is not read as agreement.

---

# Part 4. The round outcome

ROUND 3 IS NOT CLEAN. It fails both limbs of the stop condition.

- CLASS 1 is EIGHT where ZERO keeps the round clean. It is ELEVEN under round 2's broader test. Neither is zero, so the choice of test does not change the outcome.
- CLASS 2 is ELEVEN where THREE OR FEWER keeps the round clean. Every class 2 item is `low` or `medium`, so the severity half of that limb is satisfied and the count half is not.
- The severity ceiling is `high`, on two findings, both from the adopter lens, both UPHELD.

## The arithmetic

- The pass is classed `risky`, so it needs TWO CONSECUTIVE CLEAN ROUNDS. The class is under `Q-80`, which is `open`; see Part 5.
- The streak was ZERO and STAYS ZERO.
- This was round THREE of a cap of FIVE in the reset count. THREE ROUNDS ARE NOW USED and TWO REMAIN.
- Convergence therefore requires ROUNDS 4 AND 5 TO BOTH BE CLEAN. A single new valid finding in round 4 forecloses convergence and forces an escalation at the cap. That is arithmetic, not judgement.

CONVERGENCE IS NOT YET FORECLOSED, and I say that against my own expectation rather than for it. Two clean rounds remain arithmetically available. What is gone is every unit of slack.

THE ONE COUNTER-DATUM IN THIS ROUND'S FAVOUR, MEASURED. The round 2 fix pass and its follow-up authored 214 insertions and 35 deletions across six files (`git diff --stat ae3d037 e788baa`), and exactly ONE finding this round is against text those two commits authored: `G-F7`, class 2, `medium`. Every other finding's site predates them. That is the best fix-pass-to-next-round ratio this loop has recorded, and it is the strongest available evidence that a round 4 clean is reachable rather than nominal.

THE FACTS THAT ARGUE THE OTHER WAY, STATED WITH IT. The round 3 fix is much larger than round 2's: eight class 1 remedies and eleven class 2 ones, against round 2's two class 1 items and its six authorised fixes plus record repairs. And three of this round's findings (`A-F1`, `A-F3`, `A-F6`) are in a region no round has ever reviewed and that this pass is forbidden to edit, so their fix is a promise of an edit rather than the edit, and round 4 will be the first review of that promise.

I DO NOT RULE ON WHETHER TO RUN ROUND 4 OR ESCALATE NOW. That is the orchestrator's call to put and the human's to take, and it is routed in Part 5 with the arithmetic above as its input.

---

# Part 5. What must route to the human

## 5a. CARRIED FORWARD: routed by an earlier adjudication and NOT discharged

The brief names this loop's own defect: a decision routed by one adjudication and not carried by the next disappears silently. I read `r6-triage.md` Part 6 and the ledger's live `Q-78` region for every routed item, and checked each against the tree. FOUR ARE UNDISCHARGED. THE ANSWER IS NOT NONE.

CARRIED 1. `Q-80` IS `open`. Measured: `docs/plans/agent-scaffold.plan.toml:2312-2313` declares `id = "Q-80"` and `status = "open"`. It asks whether a rebuilt artefact's RISK CLASS is re-derived when the rebuilt artefact enters review. `AGENTS.md:56` says classify once at loop open, and under the loop-closing branch a new loop opens on the rebuilt artefact, so nothing mechanically binds this pass's `risky` class. THIS BEARS DIRECTLY ON PART 4'S ARITHMETIC: the whole two-clean-rounds requirement rests on a class the orchestrator asserted and no rule warrants. Its own item recommends option (a) and nothing has been decided.

CARRIED 2. THE ROUTED-DECISION-TRACKING DEFECT OWES A QUESTION AND HAS NONE. The ledger records it twice, at the round 1 record of the reset count ("NOTHING IN THIS WORKFLOW TRACKS A DECISION FROM THE MOMENT IT IS TAKEN TO THE MOMENT IT IS DISCHARGED") and at the fifth-decision paragraph ("That is a workflow defect and it owes its own question"). Measured: no `[[question]]` in the plan covers it. `Q-80` is about round counters and risk class and does not reach it. This triage's Part 5a exists only because I was told to compensate for it by hand, which is not a mechanism.

CARRIED 3. ROUND 2'S NOTIFICATION 1 IS DISCHARGED ON ITS RECORD HALF AND NOT ON ITS CONFIRMATION HALF. Measured: all sixteen 2026-08-21 `Q-78` sub-decision ids now carry receipts in `docs/metrics/workflow.jsonl`, including the four the round 2 fix pass wrote (`Q-78-drifthandover`, `Q-78-residuals`, `Q-78-driftclass`, `Q-78-quotationrow`). So the ledger-to-receipt reconciliation is done. What is NOT done is what the notification actually asked: "Only the human can confirm the set is what they took." Four of the sixteen receipts were written by an AGENT after the fact, from the ledger's prose. The ask is now small, show the human the sixteen ids and ask whether that is the set, and it is still open.

CARRIED 4. THE SECOND LOST ROUTED DECISION WAS NEVER PUT, AND IS PROBABLY NOW MOOT. The ledger records that the original round 2's triage required both a class change and a separate ROUTING of that mid-loop class change to the human, and that the orchestrator applied the change and dropped the routing. Measured: no receipt names a class decision for `step-intent-encoding`, and `Q-78-driftclass` covers the drift step alone. MY ANALYSIS, so the human is not asked to re-litigate a dead item: the specification rebuild re-declared all eight `step-intent-encoding` increments `risky` at authoring time (`docs/plans/agent-scaffold.plan.toml:1592-1621`), none of those increments has opened a review loop, and `AGENTS.md:56` classifies at loop open, so there is no longer a mid-loop change to ratify. I carry it because it was routed and never put, and I recommend closing it as moot rather than re-putting it.

DISCHARGED, RECORDED SO THE NEXT ADJUDICATION DOES NOT RE-CARRY THEM. Round 2's five residuals became human decision (14), its DECISION 1 became (15), its DECISION 2 became (16), and all three carry receipts. Its NOTIFICATION 2, that the drift step's `title` promised a closure the plan does not deliver, is discharged: the title now reads "DELETE the duplicated status label from every SELECTED step sidecar whose opening strips to prose, and HAND THE REST to a successor step" and names five receipts including `Q-78-driftsplit` and `Q-78-driftsize`.

ONE ITEM FROM THE LEDGER'S OWED LIST THAT PREDATES THIS PASS, carried because it meets the brief's test and not because this round found it: "A QUESTION IS OWED TO THE HUMAN AND HAS NO `[[question]]` YET: whether the `AGENTS.md:93` rebase rule should be mechanically enforced". Measured: still no `[[question]]` mentions a merge-base or rebase rule.

## 5b. NEW, raised by this round

NEW 1. THE ARITHMETIC DECISION, and it is the one that cannot wait. Round 3 is not clean, the streak is zero, three of five rounds are used, and convergence now needs rounds 4 AND 5 both clean. The options are to fix and run round 4 knowing a single valid finding forecloses convergence; to accept residuals now under `AGENTS.md:57` so that round 4 starts against zero outstanding items; or to escalate at once on the ground that a 20-finding round with two `high` items in a never-reviewed region is not one fix away from clean. I recommend FIX AND RUN ROUND 4, WITH THE TWO RESIDUALS IN PART 6 ACCEPTED FIRST, on Principle 6, Ground decisions in evidence: the measured fix-pass-to-next-round ratio in Part 4 is the only direct evidence available about whether the next round can come back clean, and it is good. This is genuinely open because the arithmetic leaves no slack and the human has already escalated this pass twice.

NEW 2. THE STOP CONDITION HAS NO BUCKET FOR A CRITERION THAT REFUSES A CORRECT IMPLEMENTATION. `A-F2`, `A-F6` and `G-F11` are that kind: nothing wrong passes, so they are not ground-blind, and they are neither a second-guard hole nor a figure. I put all three in class 2. At a class 2 limit of three, that choice can decide a round on its own, and round 4 will be reviewed under the same condition. The options are to widen class 2's definition to name this kind, to add a third class with its own count, or to leave the condition as it stands and let each triager place them. Recommended: WIDEN CLASS 2 EXPLICITLY, under Principle 5, Make illegal states unrepresentable, because a condition whose buckets do not partition the defect space lets the bucket assignment decide cleanliness. Genuinely open because it changes the bar the next two rounds are measured against.

NEW 3. THE PACK EDITS `A-F1`, `A-F3` AND `A-F6` REQUIRE ARE OUTSIDE WHAT THIS PASS MAY TOUCH, AND I HAVE RULED ON THE FIX RATHER THAN ROUTING IT. Recording it here so the ruling is visible and can be overturned. The pass authors plan content only and must not touch `pack/`, measured true: `git log a6e1d7f..HEAD -- pack/` is empty. So the fix is to add the pack files to the relevant increments' changed-path sets and WHAT CHANGES, which IS plan content. If the human would rather widen the pass to make the pack edits now, that reverses my ruling and needs saying.

---

# Part 6. Residuals I would put to the human

Two, plus one I explicitly recommend AGAINST accepting. For each: what accepting it means a wrong implementation could then ship.

RESIDUAL 1, `A-F4`, `next` and `status` reporting success on a plan that does not parse. ACCEPTING IT MEANS: the pass ships knowing that two of the four surfaces an adopter reads exit 0 on the plan the flip breaks, and that increment 3's THE RESIDUALS block gains a fourth entry saying so. WHAT COULD SHIP: nothing this pass builds. The mechanism is pre-existing, measured on today's unmodified binary against an already-required field, and no increment in the pass touches `next` or `status`'s resolution behaviour. THE COST ACCEPTED is that the pass states an adopter cost while two surfaces understate it, and the repair, if wanted, is a separate step of the `validate-missing-source-exit` kind. THIS IS THE CLEANEST RESIDUAL IN THE SET, because the alternative is widening the pass into product behaviour it deliberately excluded.

RESIDUAL 2, `G-F9`, the numstat bound of 2 and 2 against a justification supporting 1 and 1. ACCEPTING IT MEANS: criterion 5 admits one silent, unrelated paragraph rewrite in each of the 17 worklist files. WHAT COULD SHIP: one changed paragraph per file that no criterion of that step reads, in text `render` publishes into every reader's copy of the plan. IT IS BOUNDED by the whole-diff read a reviewer does at merge, and by the step's own NOT IN SCOPE bullet, which a reviewer reads. THE COST ACCEPTED is that the bound stops being the guard the step says it is. I put this one second because its remedy is also one character, changing 2 to 1 and 4 to 2, so accepting it buys very little.

DO NOT ACCEPT `G-F13`, and I name it because it looks like the cheapest residual in the set and is not. Its remedy is one sentence, replacing a wrong pair of slugs with the measurement over the worklist, which I have already run and printed in Part 1. Accepting a wrong measurement inside an acceptance criterion when the right one costs one line is the trade this loop has been burned by repeatedly, and the ledger records the pattern under the heading that a fix which deletes the count beats a fix that corrects it.

---

# Part 7. The recorded question: regression, or first contact with a sharpened obligation?

THE QUESTION. Class 1 went from TWO in round 2 to EIGHT in round 3 under the same lens name, and round 3 is the first round ever run under the third form of the falsification obligation. I was told to rule on which event this is and to give the measurement rather than rule from the numbers.

MY RULING: THIS IS FIRST CONTACT, NOT A REGRESSION, and the decisive measurement is where the defective text came from.

MEASUREMENT 1, THE ORIGIN OF EVERY CLASS 1 SITE. A regression means the last fix pass made the artefact worse. I traced each class 1 finding's site with `git log -S` over the branch history:

| Finding | Site | Introduced by |
| --- | --- | --- |
| `G-F1` | inc 1 criterion 2 | `9990bc0`, the specification rebuild |
| `G-F2` | inc 1 criterion 12 | `9990bc0` |
| `G-F3` | batch criterion 1's identity check | `ae3d037`, the round 1 fix pass |
| `G-F4` | inc 3 criterion 5 | `9990bc0` |
| `G-F6` | inc 2 criterion 2's pass condition | `ae3d037` |
| `A-F1` | `pack/AGENTS.md:30` | `deda349`, `structured-skeleton` Inc 6 |
| `A-F3` | `pack/plan-template.steps/example-step.md:3` | `97d5997`, `structured-skeleton` Inc 6 |
| `A-F7` | RULE 9 | `9990bc0` |

NOT ONE CLASS 1 SITE WAS AUTHORED BY THE ROUND 2 FIX PASS. Every one predates `5c39ca0` and `e788baa`. Two of the eight predate the `Q-78` pass entirely, by months. The round 2 fix cannot have regressed text it did not write.

MEASUREMENT 2, THE ONE EXCEPTION, AND IT IS THE OPPOSITE OF A REGRESSION. Exactly one finding this round is against text the round 2 fix pass authored: `G-F7`, whose site is criterion 2's three named capture files, introduced by `e788baa` ("docs: name the drift step's three capture files, which criterion 1 reads"). That commit exists BECAUSE round 2's adjudication asked for those files to be named. So the single post-round-2 finding is a NEW GUARD THAT IS INCOMPLETE, not a repaired guard that broke, and it is class 2, `medium`.

MEASUREMENT 3, THE LENS SPLIT, WHICH THE QUESTION'S FRAMING HIDES. The question compares 2 against 8 "under the same lens name". Of my eight class 1 findings, FIVE are from the ground-blind lens and THREE (`A-F1`, `A-F3`, `A-F7`) are from the ADOPTER lens, which has never been run on this artefact. Round 2's comparable figure was 2 from ground-blind plus 0 from currency. So the same-lens comparison is 2 to 5, not 2 to 8, and 3 of the 8 say nothing at all about the ground-blind stream.

MEASUREMENT 4, WHAT THE THIRD FORM REACHES THAT THE SECOND DOES NOT. Four of the five ground-blind class 1 findings are premise-and-consequence splits that the second form of the obligation does not produce. In each, the whole-ground attack IS caught and only the half-attack passes: `G-F1` (attack half of RULE 2's subject, the other half still ships four surfaces), `G-F2` (drop the check bodies while both halves of increment 3's ground stay true), `G-F3` (one sentence each for 36 steps while the prose still ships irreversibly), `G-F4` (diverge the pair the criterion does not `cmp` while the pair it does `cmp` stays honest). The fifth, `G-F6`, WAS reachable under the second form, because RULE 4 names criterion 2 as the detector of a renumbering and a per-ground attacker would test exactly that. I record that against my own ruling: one of the five is a plain miss by round 2's lens rather than a new reach.

MEASUREMENT 5, THE REGION. Both `high` findings are in `pack/`, and this branch has never touched `pack/`: `git log a6e1d7f..HEAD -- pack/` is empty. No lens in six review rounds read the shipped pack against this pass's changes. Round 2's own triage recorded the principle, that findings on first contact with a region are evidence the region is unreviewed rather than evidence the artefact is nearly done, and this round supplies the region.

WHAT THE RULING DOES NOT SAY. It does not say the artefact is closer to clean than the count suggests. Eight ground-blind holes that survived two rounds of a lens with the same name are eight real holes, and `G-F6` shows at least one of them was reachable a round earlier. It says only that the rise is the obligation and the lens reaching further, not the last repair breaking what it touched, and the arithmetic in Part 4 stands whichever way this question is answered.

---

# Part 8. File safety

Every fixture built by this triage lives under the session scratchpad in `triage-r7/`: `anchored.txt`, `relaxed.txt`, `complement.txt`, `selected.txt`, `handover.txt`, `worklist.txt`, `steps-stripped/`, `p1/` (with its `untouched`, `renumbered` and `restated` trees), `emptydir/`, `nofix/`, and the four scripts `c12.sh`, `enlarged.sh`, `p1.sh` and `build_trees.py`. Nothing outside that directory was written or deleted, no wildcard glob was used in any delete, and no fixture was created with mode 000 or 600, so none needed restoring. `git status --short` in the worktree shows only this file.
