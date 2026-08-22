# Review: `Q-78` design pass, round 4 of the reset count, FIX-VERIFICATION AND DIVERGENCE lens

Worktree `.claude/worktrees/q78-r8-fixverify`, branch `review/q78-r8-fixverify`, tree head `2c0ff99`.

This lens does not re-attack every ground. It asks three questions:

1. Did each of the 18 repaired findings close the finding it names? For each, the wrong implementation the finding named is rebuilt and the repaired criterion runs against it.
2. Are the five divergences, where the fix pass overrode its triager, sound? The claim each rests on is reproduced.
3. Are the two new criteria, `step-intent-encoding` increment 1 criterion 13 and increment 3 criterion 12, sound? Both are unreviewed content and are attacked as any criterion is.

MEASUREMENT HAZARD HONOURED. `grep` in this shell dispatches to `ugrep`. Every regex-bearing or count-bearing command below ran as `/usr/bin/grep` by absolute path, and where the two differ the difference is stated. `validate` exits 0 on an absent input, so every `validate` result pins the stdout line rather than the exit code.

Every fixture lives under the session scratchpad in `fixverify/`, a directory this review created and owns.

---

## Gates, run from the worktree root through the project toolchain

| Gate | Result |
| --- | --- |
| `cargo test` | exit 0, no failures |
| `cargo clippy --all-targets -- -D warnings` | exit 0 |
| `validate --source ... --metrics ...` | `docs/metrics/workflow.jsonl: 405 records, valid` and `docs/plans/agent-scaffold.plan.toml: 105 steps, 80 questions, valid`, exit 0 |
| `validate --source ... --workflow` | `workflow invariants hold`, exit 0 |
| `render --check --strict <PLAN>` | `docs/plans/agent-scaffold.plan.toml: up to date`, exit 0 |
| `LC_ALL=C grep -rcP '[^\t\x20-\x7e]' docs/plans/` | every file `0` |

All six ran, with the `<PLAN>` argument supplied. Each `validate` result pins its stdout line rather than its exit code.

---

# Findings

## F1. The `G-F7` repair reproduces the defect it closes, by a different route. CLASS 1. Severity `medium`.

`sidecar-status-opening-drift` criterion 2's new `H1` script is directed to run from a directory in which the file it reads does not exist. Run as printed, in the directory the criterion names, it produces the EMPTY `handover.txt` that the whole repair exists to prevent.

THE TWO DIRECTIONS THAT CONFLICT, both inside criterion 2 and eight lines apart.

- `:167` "Write them to a scratch directory OUTSIDE the repository", of `anchored.txt`, `handover.txt` and `worklist.txt`.
- `:173` "Run it under bash, from the repository root, with `COPY` a path in the same scratch directory that does not yet exist."

`H1`'s two loops both read `cut -f1 anchored.txt`, a BARE RELATIVE PATH, which resolves against the working directory. The working directory the criterion names is the repository root. `anchored.txt` is, by the same criterion, not there.

MEASURED, BOTH WAYS ROUND, with `anchored.txt` the 36 rows criterion 1's anchored selector prints on this tree.

```
MODE A, run from the repository root as :173 directs, anchored.txt in the scratch directory
  exit=0   handover.txt rows = 0
  stderr:  cut: anchored.txt: No such file or directory   (twice)

MODE B, run from the scratch directory where anchored.txt lives
  exit=0   handover.txt rows = 36, every row a slug with an EMPTY second column
  stderr:  cp: cannot stat 'docs/plans/agent-scaffold.steps': No such file or directory
```

`cp -r docs/plans/agent-scaffold.steps "$COPY"` is itself a bare relative path, so mode B cannot be the intended reading either. Neither mode returns a non-zero exit status. The only signal is text on stderr, and the script's stdout is the artefact.

MODE A IS THE DEFECT `G-F7` NAMED, WORD FOR WORD. The criterion's own paragraph at `:173` states the consequence: "an implementer who copies the command rather than reading the prose gets an EMPTY `handover.txt`. From there the worklist becomes the whole selected set and the criteria jointly endorse doing the successor step's work inside this step, which falsifies this increment's premise half and the human decisions `Q-78-driftsplit` and `Q-78-drifthandover`." That is what running the printed command in the printed directory produces.

WHY THIS IS CLASS 1 WHERE THE TRIAGE RULED `G-F7` CLASS 2. The triage's ground for class 2 was that the earlier defect "passes only for a reader who takes half of criterion 2's sentence (the selected set) and discards the other half (the strip) in the same breath". No half-reading is involved now. A reader who follows both halves of criterion 2 in full, and runs the command in the directory criterion 2 names, gets the empty capture.

THE WRONG IMPLEMENTATION PASSES EVERY CRITERION, checked one by one against mode A, where `handover.txt` is empty, `worklist.txt` is all 36, and the implementer strips 17 openings and AUTHORS replacements for the other 19.

- Criterion 1's pass condition is `comm -3` between the POST-increment anchored selector's slug column and `handover.txt`'s. Post-increment the anchored selector prints nothing, `handover.txt` is empty, and `comm -3` on two empty inputs prints nothing. PASSES.
- Criterion 4 requires the changed set to be exactly the worklist and that NO FILE ON THE HANDOVER LIST APPEARS. The worklist is all 36 and the handover list is empty, so both clauses hold. PASSES.
- Criterion 5's numstat bound of 2 and 2 holds for a one-line authored replacement. PASSES.
- Criterion 12 runs over the worklist and prints nothing once every opening begins as prose, which an authored replacement guarantees. PASSES.
- Criterion 3's RED-then-GREEN reads "criterion 1 prints that one row IN ADDITION TO THE HANDOVER LIST", which an empty handover list satisfies trivially. PASSES.

WHAT IT VIOLATES. The increment's own stated PREMISE at `:39`: "The increment DELETES the leading status token from the opening LINE of every file on THIS STEP'S WORKLIST, and it authors no replacement line ... The handover files keep their token and this step does not open them." The implementation above authors 19 replacement lines and opens all 19 handover files, so the premise is false of it, while the CONSEQUENCE at `:41` holds whole, because every edited line still ships into `docs/plans/agent-scaffold.md`. It also defeats the two human decisions the same paragraph names, `Q-78-driftsplit` and `Q-78-drifthandover`, and it ships 19 authored openings from a step whose criteria contain no acceptance criterion for an authored opening at all.

MODE B IS THE MIRROR AND IS AS BAD. `handover.txt` becomes all 36 slugs, so `worklist.txt` is EMPTY, the step changes nothing, criterion 4's changed set is empty and satisfied, criterion 7's `render --check --strict` is up to date on an untouched tree, and criterion 1's `comm -3` compares the same 36 slugs against themselves and prints nothing. A step that does nothing passes.

REPRODUCE. Capture `anchored.txt` with criterion 1's anchored selector into a scratch directory, save `H1` verbatim from `:176-192`, then run it once with `cwd` at the repository root and once with `cwd` at the scratch directory.

FIX SHAPE, NOT MINE TO MAKE. The two other capture files are read by `worklist.txt`'s definition and by criterion 1's pass condition, both of which name no working directory, so `H1` is the one command where the conflict is explicit. Either give `H1` a `SELECTED` argument in the shape it already gives `COPY`, or state one working directory for the whole criterion and make the repository paths absolute.


## F2. The `A-F5` repair does not fail its own attack: the sentence can still land inside the placeholder note. CLASS 2, second-guard hole. Severity `low`.

`step-intent-encoding` increment 3 criterion 6's new placement command separates only ONE of the two ways the duty (g) sentence lands inside the angle-bracket note the adopter's planner deletes. The other way passes every command in the criterion, byte for byte identical to a correct implementation.

THE COMMAND, at `:706`:

```
grep -c -- '^<.*must not repeat a' pack/plan-template.documentation-protocol.md docs/plans/TEMPLATE.documentation-protocol.md
```

Pass: one row per named path, each row ending `:0`.

ITS STATED JUSTIFICATION, at `:703`: "Each file's body below its heading is one angle-bracket placeholder note occupying a single unwrapped line, so a sentence written inside the note shares that line and a sentence written outside it starts its own."

THAT PREMISE IS A CLAIM ABOUT HOW THE IMPLEMENTER WRITES, NOT ABOUT THE FILE. The note opens with `<` on the body line and closes with `>` at the very end of it, measured: `pack/plan-template.documentation-protocol.md` is 3 lines and its last line ends `>`. A sentence appended BEFORE that closing `>` and on its own line is inside the brackets AND starts its own line, so it satisfies both halves of the premise's supposed dichotomy at once.

MEASURED, three fixtures built from the live pack file, all three run through both of criterion 6's presence commands and its placement command:

```
                                                       presence   placement
CORRECT   sentence after the closing `>`, own paragraph      1       0 (exit 1)
WRONG-A   sentence appended inside the note, SAME line       1       1 (exit 0)
WRONG-B   sentence inside the note, OWN line, blank line     1       0 (exit 1)
                                                                    before it
```

WRONG-B AND CORRECT ARE BYTE-IDENTICAL ON ALL THREE COMMANDS. The criterion's own MEASURED sentence at `:709` reports only WRONG-A, "with the sentence appended inside the brackets: both presence commands still print `1` and both rows here read `:1`", so the repair was measured against the one placement it catches.

WHY WRONG-B IS THE MORE LIKELY WRITING, NOT THE MORE EXOTIC ONE. Increment 3's own instruction at `:556` is "THE SENTENCE LANDS AS ITS OWN PARAGRAPH BELOW THE ANGLE-BRACKET PLACEHOLDER NOTE AND OUTSIDE IT". An implementer who honours "as its own paragraph" and "below the note" by appending a blank line and the sentence before the closing `>` has followed two of the three clauses and broken the third, and every command in the criterion certifies the result. The project's own house style forbids hard-wrapping prose, so writing a new paragraph on its own line is the normal act.

THE CONSEQUENCE IS THE ONE `A-F5` NAMED, UNCHANGED. `pack/prompts/planner.md:5` directs the adopter's planner to "Delete the template's angle-bracket placeholder notes as you fill each part in". The note runs from the `<` to the `>`, so a planner deleting the note deletes the rule with it, and the rule never reaches the adopter's own plan. The same holds for the committed copy, because `pack/pack.toml:59-61` maps the pair verbatim and criterion 5's `cmp` only proves the two copies agree about it.

REPRODUCE. Take `pack/plan-template.documentation-protocol.md`, strip its final `>`, append a blank line, the duty (g) sentence and the `>`, then run the two presence commands and the placement command against that file and against the correct placement. All three outputs match.

FIX SHAPE, NOT MINE TO MAKE. The placement test has to read the note's CLOSING bracket rather than its opening one, for instance by requiring the sentence's line to follow the line that ends `>`, or by requiring the file's last line to be the sentence.

## F3. The `A-F6` repair writes the same "which increment OPENS the section" claim into two sidecars, and the plan's own `blocked_by` makes one of them false. CLASS 2, second-guard hole. Severity `low`.

Both new DOCUMENTATION IMPACT sections carry the identical sentence, and only one of them can be true.

- `plan-order-array-position.md:401`: "`CHANGELOG.md`, THE `## [Unreleased]` SECTION, WHICH INCREMENT 1 OPENS. `grep -n 'Unreleased' CHANGELOG.md` exits 1 today, so the entry means opening the section rather than appending to one."
- `step-intent-encoding.md:739`: "`CHANGELOG.md`, THE `## [Unreleased]` SECTION, WHICH INCREMENT 3 OPENS. `grep -n 'Unreleased' CHANGELOG.md` exits 1 today, so the entry means opening the section rather than appending to one."

THE PLAN DECIDES THE ORDER MECHANICALLY, so this is not a scheduling guess. Measured in `docs/plans/agent-scaffold.plan.toml`:

```
slug = "plan-order-array-position"   status = "not-started"  blocked_by = []
slug = "step-intent-encoding"        status = "not-started"  blocked_by = ["plan-order-array-position"]
```

`step-intent-encoding.md:5` states the same relation in prose and gives its ground. So `plan-order-array-position` increment 1 necessarily lands first and opens `## [Unreleased]`. By the time `step-intent-encoding` increment 3 runs, the section EXISTS, and its entry appends. The shared "exits 1 today" measurement reproduces on this tree, `/usr/bin/grep -n 'Unreleased' CHANGELOG.md` exits 1, and it is the wrong tree to measure: what matters is the tree increment 3 runs against, which is the tree `plan-order-array-position` left behind.

WHAT AN IMPLEMENTER WHO OBEYS IT SHIPS. A second `## [Unreleased]` heading, or an overwrite of the entry `plan-order-array-position` wrote. That the project treats a duplicate heading as a defect is its own precedent: `user-prompts-pointer-and-drift-coverage.md:71` states as an acceptance criterion that "`CHANGELOG.md` carries one `## [Unreleased]` section".

NO CRITERION OF EITHER INCREMENT DETECTS IT. `/usr/bin/grep -n 'CHANGELOG' ` over both sidecars returns four rows: increment 3's criterion 9 path set, its explanatory paragraph, its DOCUMENTATION IMPACT, and the same three in the sibling. Every one of them names the PATH. Nothing reads the file's content, so a duplicated heading or a clobbered sibling entry passes criterion 9, passes criterion 11's suite and validator sweep, and passes every other criterion in the increment.

WHY THIS IS A DEFECT IN THE REPAIR AND NOT A PRE-EXISTING ONE. Neither sentence existed before this fix pass. `A-F6` was upheld precisely because neither increment carried a documentation impact, and the repair authored both sections in the same commit pair, from the same finding, without reconciling them against the dependency the plan declares.

WHY CLASS 2. `A-F6`'s violation is `AGENTS.md:30`, a workflow duty, which the triage ruled is not a risk ground, a numbered RULE or a cited Principle, so it is not class 1. The DOCUMENTATION IMPACT section is the guard the repair installed against the missing entry, and it directs an action that produces a defect no criterion reads, which is the second-guard-hole shape. A triager who reads the class 2 buckets strictly may prefer CLASS NONE, on the ground that this is neither a criterion nor a figure inside an increment block, and the finding is valid either way.

FIX SHAPE, NOT MINE TO MAKE. One of the two sentences states the append case, or both state the condition rather than the answer, in the shape the sibling paragraph already uses for its own figures.

---

# Question 1. Did each of the 18 fixes close its finding?

SIXTEEN OF THE EIGHTEEN CLOSE. Two do not, and they are `F1` and `F2`. One of the sixteen closed its finding and introduced a new defect while doing so, which is `F3`.

| Fix | Verdict | How it was checked |
| --- | --- | --- |
| `G-F1` | CLOSES | Criterion 2 now builds SIX plans and gives the `approach` string its own fenced block. The `problem`-only implementation leaves the three `approach` files exiting 0 with no such line, and the criterion requires all six to exit 1. |
| `G-F2` | CLOSES | New criterion 13. Attacked in full under question 3. |
| `G-F3` | CLOSES | Fixture built and run, below. |
| `G-F4` | CLOSES | Three `cmp`s, one per copied pair. `pack/pack.toml:39`, `:59` and `:84` map all three with `ownership = "working"` and no `render = true`, and all three pairs are byte-identical today, measured. Divergence 2. |
| `G-F5` | CLOSES | Criterion 6 now carries two fenced presence commands, one per path, with no substitution instruction. |
| `G-F6` | CLOSES | Measured, below. |
| `G-F7` | DOES NOT CLOSE | `F1`. |
| `G-F8` | CLOSES | Criterion 8 names the file. Measured, `grep -c '<pattern>' <absent file>` prints nothing on stdout and exits 2, so an absent suite cannot print `5`. Divergence 4. |
| `G-F10` | CLOSES | Criteria 2, 3 and 4 now require the line to be EXACTLY `error: no source plan at <path>` and its two siblings. Measured on today's binary, the tail-dropped no-prefix implementation prints `no source plan at docs/plans/TEMPLATE.plan.toml`, which is not that line. |
| `G-F11` | CLOSES | Criterion 4's fixture now gives `eta` `problem` ALONE, which is what criterion 6's four-line pass condition needs. The two are satisfiable together. |
| `G-F12` | CLOSES | `src/main.rs` joins criterion 9's set and increment 3 gains criterion 12. Attacked in full under question 3. |
| `G-F13` | CLOSES | Both scopes reproduced, below. Divergence 5. |
| `A-F1` | CLOSES | The three shipped surfaces join criterion 8's path set and the edit is stated in WHAT CHANGES. Divergence 3, and the file check is below. |
| `A-F2` | CLOSES | `docs/plans/TEMPLATE.md` joins criterion 9's set. Measured: it is committed (`git ls-files`), it is a current render (`render --check --strict` prints `up to date`), and it inlines both files the increment edits. |
| `A-F3` | CLOSES | Both `pack/plan-template.steps/example-step.md` and its committed copy join criterion 9's set, WHAT CHANGES and criterion 5. File check below. |
| `A-F5` | DOES NOT CLOSE | `F2`. |
| `A-F6` | CLOSES, and introduces `F3` | Both increments gain a DOCUMENTATION IMPACT section and `CHANGELOG.md` joins both path sets, so both halves of the finding are closed. The new sections then carry `F3`. |
| `A-F7` | CLOSES | RULE 9 no longer directs the damaging transcription. Measured, below. Divergence 1. |

## `G-F3`, measured against the wrong implementation the finding named

Six-step plan, batch size 3, batch 1 declared as `s1 s2 s3`. The wrong implementation fills `problem` on the three declared slugs and `approach` on three steps of the LATER batch. Criterion 1's count half and its repaired identity half, run verbatim:

```
COUNT     problem=3 approach=3           both rise by the batch size and are equal: PASSES
IDENTITY  problem declared=3 gained=3 outside=0 missing=0
          approach declared=3 gained=3 outside=3 missing=3   REFUSED

CONTROL, the correct batch
COUNT     problem=3 approach=3
IDENTITY  problem declared=3 gained=3 outside=0 missing=0
          approach declared=3 gained=3 outside=0 missing=0   PASSES
```

The `approach` row is what refuses it, and the earlier `problem`-only form had no such row. `m` is now defined once, in criterion 1, as the POST count of `^problem = `, and criteria 6 and 7 read it from there rather than restating it, so neither clause depends on a reader's choice of referent.

## `G-F6`, measured against the untouched tree

Criterion 1's captures reproduce on this tree at `pre=47 exempt=21 drift=26`, the same three the triage measured, so the fix pass's own sidecar edits added no drifting citation. `P1` run verbatim against the untouched tree prints:

```
rows=26 restated=0 wrong_slug=0 number_survives=26
```

The earlier three clauses all held on that line. The repaired pass condition requires `restated` to equal `rows` MINUS `E` and `number_survives` to EQUAL `E`, and the criterion pins `E` at one today by naming the row: `/usr/bin/grep -n 'opens "Next (built first' docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md` returns `:105`, and that row is in `drift.txt`. So the untouched tree is refused at 26 against a required 1, and a renumbered tree prints the same line and is refused with it. RULE 4's last sentence, "Criterion 2 of increment 2 detects a renumbering", is now true of the pass condition.

## `G-F13`, both scopes reproduced

The enlarged word list, run over the two scopes on this tree:

```
THIS STEP'S WORKLIST (17 files)
  doc-redundancy-cleanup        when built

THE SELECTED SET (36 files)
  structured-skeleton           blocked
  doc-redundancy-cleanup        when built
  task-entry-regrounding        to do
  reviewer-reproducible-evidence paused
```

Criterion 11's stated row is the worklist row and it reproduces exactly. Its load-carrying clause reproduces too: `planner-folds-decisions` IS on the worklist, the enlarged list does not reach it, and with its leading token stripped criterion 10's base word list finds nothing in its opening either, so the criterion's "goes silent while every assertion is still false" argument holds as printed.

## `A-F7`, measured

The three selectors on this tree print `relaxed 45`, `anchored 36`, and a complement of exactly the nine adjectival openings `sidecar-status-opening-drift.md:22` enumerates by slug. RULE 9 now reads "NO INTENT VALUE OPENS WITH A ROADMAP STATUS LABEL" and its next paragraph makes the anchored selector the thing that separates a label from an adjective, so the rule no longer directs a transcription that mutilates the nine. The paragraph's remaining claim also reproduces: `sidecar-status-opening-drift` is declared at position 101 and `step-intent-encoding` at 105, with `blocked_by = ["plan-order-array-position"]` on the latter, so the drift step does run first.

## `A-F1` and `A-F3`, whether the promise names the right files and the right changes

Both promises are complete on this tree, measured rather than read.

- `A-F1`. `/usr/bin/grep -rniw 'order' pack/ --include='*.md'` returns ten rows and `pack/AGENTS.md:30` is the only one that names `order` as a `[[step]]` field; every other row is "in this order" or "in order" in the sequencing sense. The three named paths are the pack source and its two committed renders, and `pack/pack.toml:28-31` and `:99-103` map both with `render = true`, so `cmp` correctly does not apply and `the_committed_scaffold_matches_a_fresh_render` (`src/agents_md_drift.rs:377`) is the guard the sidecar names. Its own comment confirms what it asserts: the committed `AGENTS.md` and `.agents/AGENTS.reference.md` must match a fresh render of the built-in pack.
- `A-F3`. `/usr/bin/grep -rn 'add a step\|new step\|adding a step' pack/` returns exactly one row, `pack/plan-template.steps/example-step.md:3`, so the promise names the pack's only how-to-add-a-step sentence. Its committed copy is in the path set with it, `pack/pack.toml:84-86` maps the pair verbatim, and criterion 5's third `cmp` covers it. `render` does inline that file into `docs/plans/TEMPLATE.md`, measured, so the projection listed in criterion 9 is the right one.

---

# Question 2. Are the five divergences sound?

ALL FIVE ARE SOUND. Each rests on a claim that reproduces.

## Divergence 1, `A-F7`: the figure DELETED rather than restated as 36 or 19

SOUND. The triage's own second half is what defeats every restatement. It records that the drift step runs first and deletes the label from its 17 worklist files, so the population RULE 9 meets is neither 45 nor 36. Its remaining candidate, 19, is contingent on a step that does not exist yet: the successor step that owns the 19 handover files is, by `sidecar-status-opening-drift.md:116`, "a planner's to author", so it carries no declaration position and nothing fixes whether it lands before or after the backfill. A restated 19 is therefore a figure whose truth depends on an undeclared schedule. The fix pass's brief also directs, in terms, "WHERE A FIX CAN DELETE RATHER THAN CORRECT, PREFER THE DELETION".

The half of the triage's remedy that survived is honoured by a pointer rather than a copy: the new paragraph says the sibling sidecar "enumerates by slug the adjectival openings it excludes", and it does, at `:22`, all nine, every one declared `deferred`, verified. The nine are excluded by MECHANISM here, through the anchored selector, which is stronger than a name list because it also reaches a tenth such opening the list would not name.

## Divergence 2, `G-F4`: THREE `cmp`s rather than the second the triage asked for

SOUND, and forced. The triage asked for a second `cmp` while adjudicating `G-F4` alone. The `A-F3` fix, adjudicated separately, adds `pack/plan-template.steps/example-step.md` and its committed copy to the same increment. Measured, `pack/pack.toml:84-86` maps that pair `ownership = "working"` with no `render = true`, exactly as it maps the other two, and `cmp` on all three pairs prints nothing and exits 0 today. `plan-order-array-position` rule 3 reads "Every increment that touches either file runs the `cmp`", and increment 3 now touches three pairs, so three is what the rule requires. Running two would leave the pair `A-F3` introduced unguarded, which is the defect `G-F4` was.

## Divergence 3, `A-F1`: the triage's `grep -rln` does not reproduce, and the search is scoped

SOUND. VERIFIED BOTH FORMS.

The triage wrote that `/usr/bin/grep -rln 'entries with status and order'` "returns exactly three files". It does not, and it did not on the triage's own tree. Measured with `git grep -ln` against the pre-fix tree `064fffc^`, the phrase is in SIX files:

```
.agents/AGENTS.reference.md
AGENTS.md
pack/AGENTS.md
docs/plans/agent-scaffold.reviews/q78-r7-reviewer-adopter.md
docs/plans/agent-scaffold.reviews/q78-r7-triage.md
docs/plans/agent-scaffold.reviews/q78-r8-brief-fixverify.md
```

The three surplus files are this pass's own review records, and two of them are the triage file itself and the adopter findings file it adjudicates, both of which were in the triage's working tree when it ran the command.

THE SCOPED FORM THE FIX WROTE REPRODUCES EXACTLY. `/usr/bin/grep -rln 'entries with status and order' pack/ AGENTS.md .agents/` returns `pack/AGENTS.md`, `AGENTS.md` and `.agents/AGENTS.reference.md`, three rows, under GNU grep 3.12 and under ugrep 7.5.0 alike.

THE SIDECAR'S OWN JUSTIFYING SENTENCE ALSO REPRODUCES, on the tree it now sits on. `/usr/bin/grep -rln 'entries with status and order'` over the whole worktree returns eight files: the three shipped surfaces, the three review records, `docs/plans/agent-scaffold.steps/plan-order-array-position.md` and `docs/plans/agent-scaffold.md`. The last two are the sidecar itself and the rendered plan, which is what the sentence names, and they became matches because the fix quoted the sentence in order to state the edit. So the scoping is not merely defensible, it is now necessary.

## Divergence 4, `G-F8`: `grep -rc` prints one row per file, so the file is named instead

SOUND. VERIFIED UNDER BOTH GREPS. `/usr/bin/grep -rc 'fn ' tests/` prints 11 rows of the form `<path>:<count>` and exits 0; the shell's `grep`, which is ugrep 7.5.0, prints the same 11 rows. Neither yields the single total the outcome is told to record, so the triage's first option was not available.

The fix took the triage's SECOND option, "or name the test file", which the triage offered in the same sentence, so this is a rejection of one of two offered remedies rather than an override of the verdict. The criterion's own MEASURED sentence reproduces as well: `/usr/bin/grep -c 'fn .*missing_.*_path' tests/` prints `/usr/bin/grep: tests/: Is a directory` on stderr, `0` on stdout, and exits 2.

## Divergence 5, `G-F13`: the one worklist row stated, the four-row selected-set count dropped

SOUND. Criterion 11 runs over THIS STEP'S WORKLIST, which the triage itself established, so the selected-set count is not a fact the criterion needs and stating it would put a second expiring figure inside an acceptance criterion. The triage's own remedy sentence asked for exactly what was written: "replacing a wrong pair of slugs with the measurement over the worklist". Both scopes were reproduced above and the fix's row is the correct one for the criterion's scope. The dropped row that matters most, `reviewer-reproducible-evidence` on `paused`, is on the HANDOVER list and criterion 11 never reads it, which the new text now says in its own words.

---

# Question 3. Are the two new criteria sound?

BOTH HOLD.

## `step-intent-encoding` increment 1, criterion 13

ITS GREP HALF IS CLEAN. `/usr/bin/grep -c 'fn validate_rejects_a' src/plan/source.rs` prints nothing and exits 1 on this tree, so no existing test name inflates the count, and all four required names begin `validate_rejects_a`, `validate_rejects_an_empty_problem` included, so a correct implementation prints exactly `4`.

ITS RED MEASUREMENT IS RUNNABLE AS PRINTED. `agent-flow` is a bin-only crate with no `src/lib.rs` and `plan` is a module of the bin (`src/main.rs:22`), so `cargo test --bin agent-flow validate_rejects_a` reaches unit tests inside `src/plan/source.rs`. Smoke-tested: `cargo test --bin agent-flow` runs the bin's 409 unit tests and accepts a substring filter.

THE THREE CONSTRUCTIONS THE CRITERION MUST REFUSE, ALL REFUSED.

- Four correctly named tests that assert nothing. The grep prints `4` and PASSES. Under the deletion they still pass, so the RED measurement's "ALL FOUR FAIL" is false and REFUSES them. The criterion says this itself.
- Four tests pinning `problem` on both rules with the two `approach` names stubbed. The grep PASSES. Under the deletion two fail and two pass, so "ALL FOUR" REFUSES them. This is why the pass condition is all four rather than a count.
- A build that swaps the two fields' message strings. `validate_source` takes a `&str` and returns `Vec<String>` (`src/plan/source.rs:518`), and each test is required to assert "that field's own string", so the swapped build shows red on the GREEN half.

A CORRECT IMPLEMENTATION IS NOT REFUSED. The four named tests exist, the grep prints `4`, the deletion makes all four fail because `validate_source` then returns no problem for either defect at increment 1, and restoring shows four green. Criterion 11's changed-path set already holds `src/plan/source.rs`, so criterion 13 adds no path, which it states correctly.

## `step-intent-encoding` increment 3, criterion 12

ITS PREMISE HOLDS ON TODAY'S BINARY. `StatusArgs.source` is `Option<PathBuf>` with a bare `#[arg(long)]` and no default (`src/main.rs`), and `status --help` confirms it, so `--plan docs/plans/agent-scaffold.md` with no `--source` really does read the Markdown Roadmap. That Roadmap declares `core-assets`, at `docs/plans/agent-scaffold.md:179`, and `status --plan docs/plans/agent-scaffold.md` parses it today, printing `plan: 105 steps ...` and exiting 0.

IT REFUSES BOTH WRONG IMPLEMENTATIONS IT NEEDS TO.

- Dropping the `(not recorded)` fallback OUTRIGHT rather than for the TOML source only. The command then prints an empty value where the criterion requires `(not recorded)`. REFUSED. This is the construction the criterion names.
- Resolving `--step` from a TOML source only, so a Markdown-only plan declares no steps. The command then prints the single line `step: core-assets not in this plan`, which increment 1's own `status` block specifies for an unknown slug, against a required three lines. REFUSED. The criterion does not name this one and catches it anyway.

IT DOES NOT REFUSE A CORRECT IMPLEMENTATION. Increment 1's `status` block already specifies that `--step` prints exactly three lines and that an absent field prints `(not recorded)`, and increment 1 criterion 8 already requires "stdout is exactly the three lines" for the `--source` form, so the three-line shape is settled before criterion 12 uses it rather than invented by it. `steps_from_markdown` setting both fields to `None` is stated in increment 1's `next` block, and criterion 12 names it as the mechanism.

ITS SCOPE HEDGE IS CORRECT. "ANY SLUG THE ROADMAP TABLE DECLARES WILL DO" makes the named slug an example rather than a pass condition, so the criterion does not expire if `core-assets` moves, and `core-assets` is `complete` and stays in the table in any case.

---

# The two accepted residuals: does either recorded statement UNDERSTATE?

NEITHER DOES. Both were checked against the brief's test rather than accepted as recorded, and neither is re-filed.

## `A-F4`, RESIDUAL 4 in `step-intent-encoding.md:755`

ITS MEASUREMENT REPRODUCES ON TODAY'S BINARY, run against a two-step plan omitting the already-required `title`:

```
validate --source notitle.plan.toml   missing field `title`, exit 1
next --source notitle.plan.toml       note: --source ... did not parse ...; projecting from --plan
                                      no active review loop (no plan steps found), exit 0
status --source notitle.plan.toml     plan: not provided, exit 0
```

ITS SCOPING CLAIM HOLDS. "No increment of this step touches `next` or `status`'s resolution behaviour" is true as stated: increment 1 adds `StepInfo` fields and `build_context` slots and increment 3 changes the `(not recorded)` fallback in `run_status`, and neither changes how a plan source is resolved when it fails to parse. The receipt it cites exists, `q_id:"Q-78-round4"`, `ts:"2026-08-22"`, with `chosen` reading "Fix and run round 4, with the two residuals accepted first".

## `G-F9`, beside criterion 5 of `sidecar-status-opening-drift.md:206`

ITS ENUMERATION OF WHAT DOES NOT READ THE SLACK IS COMPLETE, checked criterion by criterion. Criteria 1, 10, 11 and 12 each build their input with `sed -e '/^#/d' -e '/^[[:space:]]*$/d' ... | head -1`, so all four read the opening line only. Criterion 4 checks path names. Criterion 7 re-renders. Criterion 9's ASCII sweep reads every byte and passes on ASCII prose. Criterion 3 is criterion 1 run twice. Criterion 8 runs the validators, none of which reads sidecar prose.

IT ALSO STATES THE HALF THE TRIAGE DID NOT. The triage's residual named the in-place rewrite; the recorded statement adds "it admits an added line that is not balanced by a removed one", which reaches the append case the numstat pair also buys. Nothing that a slack of one added and one removed line admits is left unstated.

---

# Checked and recorded, not filed

Three things this lens hit and judged NOT findings. Each is recorded with its measurement so a triager can overrule.

1. CRITERION 13 MOVES THE `69` DECLARATION-SITE FIGURE, AND NOTHING WRONG SHIPS. `validate_source` takes a `&str` (`src/plan/source.rs:518`), so each of criterion 13's four tests must carry a `[[step]]` TOML fixture, and each fixture carries a `slug = ` line the increment 3 anchor counts. The site count today measures at exactly 69 across 12 files, reproduced row for row, and rises to 73 once increment 1 builds, against increment 3 criterion 2's "THE 69 DECLARATION SITES". It is not filed because the same increment instructs at `:593` "Re-run the two anchors rather than copying the pair, because both move as the plan and the suite grow", criterion 9's path set is by path rather than by count, and an implementer who patches 69 and leaves the four new fixtures short of `approach` gets test failures from `cargo test`, which criterion 2 requires to pass.

2. `docs/plans/TEMPLATE.md` CHANGES THREE WAYS, NOT "TWICE OVER". `step-intent-encoding.md:560` says "the committed projection changes twice over, once from the placeholder values and once from the corrected example-step sentence". Measured, `docs/plans/TEMPLATE.md` also inlines `TEMPLATE.documentation-protocol.md`, which the same increment edits with the duty (g) sentence, so it changes three ways. Not filed: the path is in criterion 9's set either way and no criterion turns on the count.

3. `workflow-calibration.md` IS ON THE HANDOVER LIST, SO CRITERION 5's NAMED EXCEPTION AND ITEM `B` REACH A FILE CRITERION 4 FORBIDS. Measured, the `H1` capture prints `workflow-calibration` among the 19, because its opening strips to "(deferred). The scaffolded workflow's ...", which `sidecar-status-opening-drift.md:81` already names as one of the seven that need an authored opening. Criterion 4 requires that NO FILE ON THE HANDOVER LIST APPEARS in the diff, while criterion 5's `4 and 4` exception, criterion 6 and the whole `### B` section all direct an edit to it. This text predates the fix pass and is a ground-blind finding against the sidecar as it now reads, so it is noted here and not built out, per this lens's brief.

---

# Counts

| | |
| --- | --- |
| Total findings | 3 |
| Distinct findings | 3 |
| CLASS 1 | 1 (`F1`) |
| CLASS 2 | 2 (`F2`, `F3`) |
| Severity ceiling | `medium` |

SEVERITIES: 1 `medium` (`F1`), 2 `low` (`F2`, `F3`).

AGAINST THE WIDENED STOP CONDITION. Class 1 must be ZERO and it is ONE, so this lens does not return clean. Class 2 is TWO, which is inside the limit of three, and both are `low`, so the class 2 limb is satisfied on both halves.

WHAT IS CLEAN, STATED BECAUSE A CLEAN ANSWER IS AS USEFUL AS A FINDING. Sixteen of the eighteen fixes close the finding they name, all five divergences are sound and every claim they rest on reproduces, and both new criteria hold under attack. The two failures are `G-F7`, where the repaired capture command reproduces its own defect from the working directory the criterion names, and `A-F5`, where the new placement command separates only one of the two ways the sentence lands inside the placeholder note.

---

# File safety

Every fixture built by this review lives under the session scratchpad in `fixverify/`: `drift/` (with `anchored.txt`, `handover.txt`, `worklist.txt`, `h1.sh`, `steps-copy/`, `copyA/`, `copyB/` and the two stderr captures), `inc2/` (`pre.txt`, `exempt.txt`, `drift.txt`, `order-to-slug.tsv`, `p1.sh`), `gf3/` (`pre.plan.toml`, `wrong.plan.toml`, `correct.plan.toml`, `ident.sh`), `af5/` (`correct.md`, `wrongA.md`, `wrongB.md`), `gf8/`, `gf10/`, `res4/` and `gates.log`. Nothing outside that directory was written or deleted, no wildcard glob was used in any delete, and no fixture was created with mode 000 or 600, so none needed restoring.

`H1` reads `anchored.txt` from its working directory, so measuring mode A required that file to exist at the repository root for the length of one command. It was removed in the same command, and `git status --short` in the worktree shows only this findings file.
