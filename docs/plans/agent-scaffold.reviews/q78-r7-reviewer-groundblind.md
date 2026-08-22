# Findings: `Q-78` design pass, round 3 of the reset count, GROUND-BLIND FALSIFICATION lens

Reviewer worktree: `.claude/worktrees/q78-r7-groundblind`, branch `review/q78-r7-groundblind`, base `e788baa`.

Lens: split each stated ground into its premise and its consequence, then build a wrong implementation for each half. A criterion is ground-blind (class 1) when a wrong implementation passes it while it falsifies the premise, even though the consequence still holds by another cause.

Scope: five step sidecars under `docs/plans/agent-scaffold.steps/`, 13 increments, all `risky`.

Findings are appended as they are confirmed. Counts are at the end.

---

## Gate results

All six gate lines ran. None was worked around.

| Gate | Result |
| --- | --- |
| `cargo test` | 0 failures |
| `cargo clippy --all-targets -- -D warnings` | exit 0 |
| `validate --source ... --metrics ...` | `docs/plans/agent-scaffold.plan.toml: 105 steps, 80 questions, valid`, exit 0 |
| `validate --source ... --workflow` | `workflow invariants hold`, exit 0 |
| `render --check --strict <PLAN>` | `up to date`, exit 0 |
| `LC_ALL=C grep -rcP '[^\t\x20-\x7e]' docs/plans/` | every file `0`, exit 1 (the PASS case for a sweep) |

The plan carries 105 steps and 80 questions, which is the tree every figure below is measured against.

---

## Findings

### F1. `step-intent-encoding` increment 1: no command anywhere tests the single-line rule on `approach`, so half of RULE 2 is unguarded

CLASS 1. Severity: medium.

RULE 2 (`step-intent-encoding.md:31`) reads: "`validate` therefore rejects a newline in EITHER field, as a pure function over the deserialised string. That catches all three ways a newline arrives: a `"""` block, a `'''` block, and a `\n` escape inside a basic string. Principle 5, Make illegal states unrepresentable, decides it." RULE 1 (`:29`) reads "Both are single-line TOML strings". Increment 1's schema block states all four rejection strings and says (`:87`) "The four strings are given once each rather than as one string with a field name to substitute."

Criterion 2 (`:141`) is the only criterion that exercises the single-line rule. It builds three one-step plans, each carrying a multi-line **`problem`**, and pins one output string:

```
step `a` field `problem` must be a single line
```

The string `step \`a\` field \`approach\` must be a single line` appears nowhere in any criterion of any increment of this step.

THE WRONG IMPLEMENTATION. Apply the newline rejection to `problem` and not to `approach`. The premise of the increment's own risk ground ("it adds a new `validate` rejection rule", `:61`) is then false of half the rule, while the consequence ("It changes product behaviour and it ships to every scaffolded project") still holds in full, because the other four surfaces still ship.

EVERY COMMAND IN INCREMENT 1, AND WHY EACH PASSES. This is the whole acceptance block, enumerated:

| Criterion | Command's input | Reaches a multi-line `approach`? |
| --- | --- | --- |
| 1 | live plan; `grep -c 'problem: Option<String>'` | No, and the grep names `problem` only |
| 2 | three plans with a multi-line `problem` | No |
| 3 | `problem = ""`, `approach = ""` | No, this is the empty rule |
| 4 | `grep -F '- problem: ...'` on the golden | No |
| 5 | `grep -A5` on the golden | No |
| 6 | `grep -A3` on the golden | No |
| 7 | one-step plan, both fields single-line | No |
| 8 | four `status --step` runs, single-line values | No |
| 9 | `render --check --strict` on the live plan | No |
| 10 | batch-boundary arithmetic | No |
| 11 | `git diff --name-only` | No |
| 12 | `cargo test`, `clippy`, two `validate` runs on the live plan, ASCII | No; and see F2, no suite test is required |

No later increment reaches it either. Increment 3 criterion 1's four greps read `String` against `Option<String>` and say nothing about the newline check. The batch block's R1, R2, R3 and R4 read values that a correct batch authors, never a rejected one.

WHY THE STEP KNOWS THIS HAZARD AND MISSED IT HERE. The same sidecar applies the two-commands-per-field rule in three other places, each with the reason stated: the batch block criterion 1 (`:283`) "Both fields are counted because a batch that fills `problem` and forgets `approach` satisfies a single-field check"; increment 3 criterion 1 (`:556`) "a reader who substitutes once proves one field"; increment 3 criterion 4 (`:628`) "Two commands, given once each, because a template that ships one placeholder and renders the other nowhere satisfies a single-field check". Increment 1 criterion 3 also runs both fields for the EMPTY rule. Criterion 2 is the one place the pattern is dropped.

WHAT IT COSTS. The bound is what resolves the pass's central tension. `Q-78.md:87` and `step-intent-encoding.md:23` both argue that two single-line fields add exactly two lines to a `[[step]]` block whatever its length, which is what keeps the reprioritisation cost of `plan-order-array-position` unchanged. With the rule half-implemented, `approach = """..."""` across ten lines parses and validates, in this repository and in every scaffolded project, and the plan's own criteria never notice.

THE FIX SHAPE, stated so the finding is actionable and not a puzzle: criterion 2 needs its `approach` twin written out, not a substitution instruction, in the shape criterion 8 and increment 3 criterion 1 already use.

---

### F2. `step-intent-encoding`: RULE 2 and RULE 3 are pinned nowhere in the suite, and increment 3 rewrites the arms that implement them

CLASS 1. Severity: medium.

RULE 2 encodes the single-line bound and RULE 3 (`:33`) encodes the empty-value rejection, both decided by Principle 5, Make illegal states unrepresentable. Increment 1 is the increment that builds them. Its only oracles for both are hand-run commands in a scratch directory: criterion 2 and criterion 3. Criterion 11 (`:253`) fixes the changed-path set and requires no test file. Criterion 12 (`:255`) says only "`cargo test` passes". No criterion of increment 1 requires a single unit or integration test for either rule.

Increment 3 then rewrites exactly that code. `:505`: "`Option<String>` becomes `String` on both fields and the two `if let Some` arms in `validate` become direct reads."

THE WRONG IMPLEMENTATION. Make both fields required and turn the two `if let Some` arms into direct reads that drop the check bodies. The premise and the consequence of increment 3's own ground both stay TRUE of it (both fields are required; every previously valid scaffolded plan fails to parse). What it falsifies is RULE 2, RULE 3 and Principle 5.

EVERY CRITERION OF INCREMENT 3, AND WHY EACH PASSES:

- 1. Four greps on `src/plan/source.rs` plus two parse checks. Both parse failures are serde's `missing field`, raised before any `validate` rule runs. Pass.
- 2. `cargo test` and `cargo build`. No test exists for either rule, because increment 1 required none. Pass.
- 3. Fresh scaffold validates. The shipped placeholders `<the problem this step addresses>` and `<how this step addresses it>` are non-empty and single-line, so neither rule is exercised. Pass.
- 4. Two `grep -c -F` on `docs/plans/TEMPLATE.md`. Pass.
- 5. `cmp` on the template plan pair. Pass.
- 6. Two greps for the pack prose sentence. Pass.
- 7. `test -e` and `git diff --name-status` on the migration record. Pass.
- 8. R4, which counts filled and projected fields on a correctly backfilled plan. Pass.
- 9. `git diff --name-only`. Pass.
- 10. `grep -rn 'the problem this step addresses' src/`. Pass.
- 11. `cargo test`, `clippy`, two `validate` runs on the live plan, ASCII. The live plan's values are correct, so neither rejection fires. Pass.

The batch increments do not reach it either: their criterion 10 (`:487`) runs `validate` on the live plan and requires the `valid` line, which a correct backfill produces whether or not the rules exist.

THE PASS ALREADY STATES THE RULE THIS BREAKS, IN THIS SAME REVIEW SET. `validate-missing-source-exit.md:98`, criterion 8: "A criterion that only runs by hand does not survive the increment, which is why the pair lives in the suite as well as in criteria 4 and 5." That step pins five branches in the integration suite for a change one tenth the size. `step-intent-encoding` pins none for two rules its own design pass calls the thing that resolves its central tension (`Q-78.md:89`, "THE BOUND IS ENCODED, NOT LEFT AS A CONVENTION ... The claim that resolves the pass's central tension must not rest on an author's habit (Principle 5)").

THE EVIDENCE IS THE CRITERIA TEXT, NOT A GREP OF TODAY'S TREE. The increment is unbuilt, so "no test exists today" is trivially true and proves nothing. What proves the finding is that neither increment obliges one. Increment 1's twelve criteria are enumerated in F1 above and none names a test. Increment 3's eleven are enumerated here and none exercises either rule. For contrast, the pattern the repository already uses for a validator rule is a named assertion in the suite: `/usr/bin/grep -rn "field \`.*\` is empty" src/ tests/` returns 13 rows in `src/metrics.rs`, six of them `assert_eq!` lines in unit tests pinning the metrics log's own empty-field rejections. The `[[step]]` rules this step adds get no equivalent, by specification.

F1 and F2 are separate defects with separate fixes. F1 is a missing command in increment 1 criterion 2. F2 is a missing suite obligation across increments 1 and 3, and it stands even if F1 is fixed, because a hand-run criterion-2 command at increment 1 says nothing about the state of the code after increment 3.

---

### F3. The batch block's identity check reads `problem` alone, so a batch can fill `approach` on steps outside its declared slug list

CLASS 1. Severity: medium.

The batch increments' shared risk ground (`:259`) reads: "a batch authors two prose sentences for up to 18 steps and MOVES the source text out of those sidecars, so a mistake spreads across the published plan document and is not reversible by one revert once a later batch lands on top."

PREMISE: two sentences, for the up-to-18 steps of THIS batch.
CONSEQUENCE: prose ships into the published plan and is not one-revert reversible.

Criterion 1 (`:275`) is the criterion that carries the premise. Its own heading is "THE BATCH IS EXACTLY ITS DECLARED SLUG LIST", and it splits deliberately into a count check and an identity check, because "MEASURED, a count-only check passes on a batch that fills the right NUMBER of steps from the wrong part of the plan, and `outside` is what reports that" (`:295`).

The identity check keys on `problem` and on nothing else (`:291`):

```
awk '/^slug = /{s=$0} /^problem = /{print s}' docs/plans/agent-scaffold.plan.toml | sed -n 's/^slug = "\(.*\)"$/\1/p' | sort > filled-post.txt
```

`declared`, `gained`, `outside` and `missing` are all computed from that one set. The count check runs both fields, but a count cannot name a step.

THE WRONG IMPLEMENTATION. In batch a, fill `problem` on the 18 declared slugs, and fill `approach` on 18 steps belonging to a LATER batch, marking those 18 `paraphrased` so no sidecar sentence has to move. The premise is false: this is one sentence each for 36 steps, not two sentences for 18. The consequence is untouched: 36 authored sentences ship into `docs/plans/agent-scaffold.md`, and once batch b lands on top, no single revert takes them out.

CRITERION BY CRITERION:

- 1, count half. Post `problem` minus pre = 18. Post `approach` minus pre = 18. Both equal the batch size, and `problem` and `approach` totals are equal to each other. Pass.
- 1, name-only half. The diff lists the plan TOML, the record, the rendered plan, and one sidecar per in-batch step that had a sentence to move. The out-of-batch fields are paraphrased, so they move no sentence and add no path. Pass.
- 1, identity half. `filled-post.txt` reads `problem` only, so `gained` is exactly the 18 declared slugs. `outside=0`, `missing=0`. Pass.
- 3, R1. `rows=36`, `filled=36`, `dupes=0`, `bad=0`; each row's field really is filled, so `NO SUCH FILLED FIELD` never fires. Pass.
- 4, R2. Every out-of-batch row is `paraphrased`, so R2 runs resolution and relevance only, and `docs/plans/agent-scaffold.steps/<slug>.md` is admissible for each of them. Pass.
- 5. Counts are reported, not bounded. Pass.
- 6, R3. `checked=36`, `duplicated=0` (nothing was transcribed out of place), `status_token=0`. Pass.
- 7, R4. `source=18/18`, both halves equal, `projected - quoted` equals `source`. Pass.
- 8. The paraphrased rows are disposed of side by side. The criterion requires a source-versus-recorded comparison and says nothing about whether the slug belongs to this batch. Pass.
- 9, 10. Path set and validators. Pass.

The hole is exactly the one the criterion's own text warns about, applied to the other field: the sidecar wrote "Both fields are counted because a batch that fills `problem` and forgets `approach` satisfies a single-field check" for the COUNT half, then built the IDENTITY half on a single field.

ONE CLAUSE IS AMBIGUOUS AND MAY REFUSE IT, STATED SO THE FINDING IS NOT OVERSOLD. Criterion 7's R4 pass condition ends "and both halves of `source` are equal to each other and to the running total of filled steps". Read as steps carrying BOTH fields, the wrong implementation gives 0 against `source=18/18` and the clause refuses it. Read as the running batch total, which is how criterion 6's `checked=<2m>` uses `m`, it gives 18 and the clause passes. The criterion does not say which, and criterion 1, whose own heading is the batch identity, is the criterion that should not depend on the answer.

THE FIX SHAPE. `filled-post.txt` needs an `approach` twin, and `gained`, `outside` and `missing` need computing for both, in the two-commands-given-once-each shape the sidecar uses elsewhere.

---

### F4. `step-intent-encoding` increment 3 claims criterion 5 guards two hand-edited template pairs, and criterion 5 `cmp`s one

CLASS 1. Severity: medium.

`:521` states the hazard and names its guard:

"TWO RENDERED PAIRS ARE HAND-EDITED HERE AND NO GUARD COVERS EITHER. `pack/pack.toml` maps `plan-template.plan.toml` to `docs/plans/TEMPLATE.plan.toml` and `plan-template.documentation-protocol.md` to `docs/plans/TEMPLATE.documentation-protocol.md`, both as verbatim copies with no `render = true`, so each pair is byte-identical today. `src/agents_md_drift.rs` names 'the `docs/plans/TEMPLATE` family' as UNGUARDED in its own coverage block, and `.agents/checks.toml` declares only `render-check`. Criterion 5 is the guard and it is `cmp`".

Criterion 5 (`:630`) reads, in full: "THE TEMPLATE PAIR STAYS BYTE-IDENTICAL. `cmp pack/plan-template.plan.toml docs/plans/TEMPLATE.plan.toml` prints nothing and exits 0."

One pair. The documentation-protocol pair gets no `cmp` anywhere in the increment.

THE FACTS REPRODUCE:

```
$ /usr/bin/grep -n 'plan-template' pack/pack.toml
...
59:source = "plan-template.documentation-protocol.md"
$ sed -n '57,61p' pack/pack.toml
[[asset]]
source = "plan-template.documentation-protocol.md"
dest = "docs/plans/TEMPLATE.documentation-protocol.md"
ownership = "working"
$ cmp pack/plan-template.documentation-protocol.md docs/plans/TEMPLATE.documentation-protocol.md
(no output, exit 0)
$ cat .agents/checks.toml | /usr/bin/grep -c '^\[\[check\]\]'
1
$ /usr/bin/grep -n 'TEMPLATE' src/agents_md_drift.rs
60://! the `.toml` copies under `.agents/`, and the `docs/plans/TEMPLATE` family illustrate the
```

So: verbatim copy, no `render = true`, byte-identical today, and unguarded by the drift module and by `.agents/checks.toml` alike.

THE WRONG IMPLEMENTATION. Add the duty (g) sentence to `pack/plan-template.documentation-protocol.md` and to `docs/plans/TEMPLATE.documentation-protocol.md`, and let the two copies diverge anywhere else in the file: a reflowed paragraph, a corrected typo applied to one side, a trailing-newline difference. The premise of `plan-order-array-position` RULE 3, which increment 3 criterion 5 cites by name ("See `plan-order-array-position` rule 3 for the measurement that shows nothing else detects this"), is then false of this increment: RULE 3 (`plan-order-array-position.md:27`) says "Every increment that touches either file runs the `cmp`", and `Q-78.md:255` says "EVERY INCREMENT THAT TOUCHES THIS FAMILY CARRIES THE PAIR CHECK, which is `cmp`". The consequence still holds, because criterion 5 does run a `cmp` and does keep the other pair honest.

CRITERION BY CRITERION for the divergence:

- 5. `cmp` on the plan pair only. Pass.
- 6. Two `grep -c -F` for `must not repeat a \`[[step]]\` field`. Both print `1`, because both files carry the sentence. A grep for one sentence cannot see a difference anywhere else in the file. Pass.
- 9. The path set lists both files by name. Naming a path proves nothing about its content. Pass.
- Everything else in the increment reads `src/`, the plan TOML, the rendered plan or the scaffolded output, none of which reads either documentation-protocol file.

`plan-order-array-position` criterion 7 records what this costs, measured: "an implementation that updates the pack source and leaves the committed copy stale gives `cargo test` 0 failures, `render --check --strict` exit 0 and `validate` exit 0, and this `cmp` prints `... differ: byte 1511, line 37`". The same measurement applies to the second pair, and increment 3 runs no `cmp` on it.

THE FIX SHAPE. Criterion 5 needs its second `cmp` written out as its own command, for the reason increment 3 criterion 4 gives for its own pair of greps.

---

### F5. `step-intent-encoding` increment 3 criterion 6 breaks the sidecar's own written-out-once-each rule, on the one pair no `cmp` covers

CLASS 2 (second-guard hole). Severity: low.

Criterion 6 (`:632`) reads: "THE PACK PROSE RULE SHIPS AND ITS RENDERED COPY MATCHES. Run this, and then the same command against `docs/plans/TEMPLATE.documentation-protocol.md`. Two commands, given once each, because the pack source and its committed copy are two files and only the pair check proves both. Each prints `1`."

It then gives ONE fenced block, against `pack/plan-template.documentation-protocol.md`, and instructs the reader to substitute the second path. That is the substitution instruction the same sidecar refuses four times over, with the reason stated each time: `:556` "a reader who substitutes once proves one field"; `:628` "Two commands, given once each"; `plan-order-array-position.md:181` "The three commands are given once each rather than as one command with a substitution instruction, because the three fixtures are three different files and a reader who substitutes once proves one arm"; `validate-missing-source-exit.md:65` "This command is given on its own rather than as a substitution into criterion 2, because a reader who substitutes once proves one flag".

The criterion's own sentence "Two commands, given once each" is therefore false of the text under it. This is class 2 rather than class 1 because a reader who follows the instruction does reach both files. It is reported because criterion 6 is the ONLY content check on the pair F4 shows has no `cmp`, so a reader who proves one file here proves nothing about the other on either axis.

---

### F6. `plan-order-array-position` increment 2: every mechanical clause of the increment, criterion 2's oracle included, is satisfied by a tree on which nothing was done

CLASS 1. Severity: medium.

Increment 2's risk ground (`plan-order-array-position.md:254`) reads: "Criterion 2 is a mechanical oracle over the numbered citations, and criterion 3 is a bounded worklist that a reviewer disposes of row by row, so one half of the increment carries a reading." Criterion 7 (`:382`) repeats it: "None of the three reads sidecar prose, so they are the no-regression check rather than the oracle. Criterion 2 is the oracle." RULE 4 (`:29`) reads: "THE PROSE FIX RESTATES BY SLUG AND NEVER RENUMBERS. A renumbered citation is still a positional citation and it drifts again on the next reorder. Principle 8, Structured data first, project for humans, decides it. Criterion 2 of increment 2 detects a renumbering."

Criterion 2's stated pass condition (`:326`) is three clauses: "`rows` equals `wc -l < drift.txt`, `wrong_slug=0`, and `restated` plus the count of `NUMBER SURVIVES` rows equals `rows`."

Clauses 1 and 3 are identities of the P1 script and cannot fail. The loop reads `drift.txt` line by line and increments `rows` once per line, so clause 1 holds by construction. Every row then takes exactly one of three exits (`residual`, `restated`, `wrong`), so `rows = restated + wrong + residual` always, and clause 3 is clause 2 restated. The only substantive clause is `wrong_slug=0`, and an untouched tree has no annotations to be wrong about.

MEASURED, THREE TREES AGAINST P1 AS WRITTEN. Fixture at `<scratchpad>/groundblind/p1`, a copy of `docs/plans/agent-scaffold.steps/` plus the three front sidecars criterion 1 names, with `pre.txt`, `exempt.txt`, `drift.txt` and `order-to-slug.tsv` built by criterion 1's own commands. `pre=47 exempt=21 drift=26 table=105`.

```
UNTOUCHED (nothing done at all)
rows=26 restated=0 wrong_slug=0 number_survives=26

RENUMBERED (every drifting citation rewritten to its rendered position, +1 in 85..90, +2 at or above 92)
rows=26 restated=0 wrong_slug=0 number_survives=26

RESTATED BY SLUG, INCLUDING THE ONE QUOTATION ROW
rows=26 restated=26 wrong_slug=0 number_survives=0
```

All three satisfy all three stated clauses. The untouched tree and the renumbered tree print a byte-identical line.

THE THREE WRONG IMPLEMENTATIONS AND WHAT EACH VIOLATES:

1. NOTHING DONE. Violates the increment itself. It also passes every other mechanical criterion: criterion 4's numstat equality holds at 0 = 0; criterion 5's path set is a subset of the empty set; criterion 2's second half prints `post=47 exempt_lost=0` and `post` equals `exempt` (21) plus the 26 `NUMBER SURVIVES` rows; criteria 6 and 7 are a recorded exclusion and a no-regression check.
2. RENUMBER EVERY DRIFTING CITATION. Violates RULE 4 by name, and Principle 8, which RULE 4 cites. RULE 4's own sentence "Criterion 2 of increment 2 detects a renumbering" is false of the pass condition, measured above.
3. RESTATE THE ONE QUOTATION ROW TOO. Violates the human decision `Q-78-quotationrow` (2026-08-21), which chose to leave that row over restating it, on Principle 8, because "A restatement makes the quotation stop matching the text it quotes, and `render` publishes both files" (`:336`). The row is `docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md:105`, found with the criterion's own `grep -n 'opens "Next (built first' ...`. This implementation prints `number_survives=0` and passes all three clauses.

WHAT THE CRITERION ALREADY KNOWS AND DOES NOT PUT IN ITS PASS CONDITION. The criterion's own MEASURED table (`:350`) states the discriminating equality twice: "A CORRECT IMPLEMENTATION prints `rows=R restated=R-E wrong_slug=0 number_survives=E`", and the paragraph at `:328` states "a correct implementation prints `number_survives=1` rather than `0`". Neither `restated = R - E` nor `number_survives = E` appears in the Pass clause. The sidecar then asserts (`:353`) "That is why the pass condition reads `restated` rather than a before-and-after diff", and the pass condition reads `restated` only inside the identity, so it reads it in no discriminating way.

THE BACKSTOPS, STATED SO THE FINDING IS NOT OVERSOLD. Criterion 2's next sentence is a reading: every `NUMBER SURVIVES` row must be enumerated in the outcome as a verbatim quotation whose restatement would falsify it, and exactly one row today qualifies. A reviewer who runs that reading refuses trees 1 and 2, and the `number_survives=1` sentence refuses tree 3. What is defeated is the increment's own claim about which half is mechanical: the ground says one half carries a reading, and measured, both halves do.

THE FIX SHAPE. Move `number_survives` equals the enumerated quotation count, and `restated` equals `rows` minus that count, into the Pass clause, where the MEASURED table already puts them.

---

### F7. `sidecar-status-opening-drift` criterion 2: `handover.txt` is not executable as written, and the executable reading of it produces an EMPTY handover list

CLASS 1. Severity: medium.

Criterion 2 (`sidecar-status-opening-drift.md:167`) names three capture files "because criterion 1's pass condition reads two of them by name". The middle one:

"`handover.txt` is criterion 12's command run over a throwaway copy of `docs/plans/agent-scaffold.steps/` in which every selected file's opening line has lost its leading token."

Criterion 12's command (`:213`) hard-codes the live path and takes the worklist that does not exist yet:

```
for slug in $WORKLIST; do
  line=$(sed -e '/^#/d' -e '/^[[:space:]]*$/d' "docs/plans/agent-scaffold.steps/$slug.md" | head -1)
  ...
```

Three gaps, all in the one command criterion 1's pass condition consumes by name. The path is fixed to the working tree, so "run over a throwaway copy" needs a substitution the criterion never states. `WORKLIST` is defined at `:196` as "THIS STEP'S WORKLIST from criterion 2", and this step's worklist is `comm -23 anchored handover`, so the definition is circular in command terms; criterion 2's prose resolves it to the SELECTED set but the command text does not. And nothing states the strip.

MEASURED, THE COMMAND RUN VERBATIM. `anchored.txt` from criterion 1's anchored selector against the live tree gives 36 slugs. Criterion 12's command, run exactly as printed with `WORKLIST` set to those 36:

```
rows=0
```

Zero. Every one of the 36 openings begins with an uppercase status token, so every one matches `[A-Z]*` and none is printed. `handover.txt` is empty.

MEASURED, THE COMMAND RUN AS INTENDED. The same 36 slugs, over a throwaway copy of `docs/plans/agent-scaffold.steps/` in which the leading token and its trailing delimiter have been removed from each opening line:

```
rows=19
include-all-visible, state-schema, workflow-viz, optional-modules, greenfield-flake,
later-enhancements, git-url-fetch, tui-authoring, workflow-calibration, instrument-flag,
escalation-exempt, waiver-model, structured-skeleton, test-driven, mutation,
workflow-driver, task-entry-regrounding, reviewer-reproducible-evidence,
workflow-audit-followups
```

Nineteen, which reproduces the figure at `:23` exactly. The two readings of one criterion differ by the whole handover list.

WHAT THE EMPTY READING DOES TO THE REST OF THE STEP. With `handover.txt` empty, `worklist.txt` becomes `comm -23 anchored handover` = all 36. Criterion 1's pass condition becomes `comm -3 <(post-anchored) <(empty)` prints nothing, which requires the post-increment anchored selector to print nothing, which requires the token deleted from all 36. Criterion 12 then runs over all 36 and refuses a bare strip, because it prints the 19 fragments. So the implementation the criteria jointly endorse is: delete the token from all 36 AND author replacement openings for the 19.

THE WRONG IMPLEMENTATION AND WHAT IT VIOLATES. Doing both steps' work inside this step falsifies the premise of this increment's own risk ground (`:39`): "The increment DELETES the leading status token from the opening LINE of every file on THIS STEP'S WORKLIST, and it authors no replacement line ... The handover files keep their token and this step does not open them." The consequence (`:41`) is untouched: `render` still inlines every edited line into the published plan. It also violates the human decisions `Q-78-driftsplit` and `Q-78-drifthandover`, and the WHERE THE SPLIT CUTS ground at `:29`, which cites Principle 3, Safe on existing projects, Principle 1, Prefer the cleaner long-term architecture over the smallest diff, and Principle 5, Make illegal states unrepresentable, by name.

Criterion by criterion, that implementation passes: criterion 1's `comm -3` prints nothing; criterion 4's changed path set is `worklist.txt`, which is all 36; criterion 5's per-file numstat bound of 2 and 2 accommodates a one-line rewrite; criterion 12 prints nothing because the 19 were authored; criteria 3, 6, 7, 8, 9 are unaffected. Criteria 10 and 11 are readings over the worklist, which now contains all 36, so they do not refuse it either.

The other executable reading, a bare strip across all 36, is refused by criterion 12, which prints the 19. That is the outcome `Q-78-drifthandover` was decided to avoid, and it is caught. The scope-collapsing outcome is not.

THE FIX SHAPE. Criterion 2 needs the handover capture written out as a command of its own: the copy, the strip, the path root, and the selected-set slug list, in the shape criterion 1 already uses for the anchored selector.

---

### F8. `validate-missing-source-exit` criterion 8's verification command cannot run, and prints `0` whatever the suite contains

CLASS 2 (second-guard hole). Severity: low.

Criterion 8 (`validate-missing-source-exit.md:98`) is the durability guard for the whole increment. Its own text states why: "A criterion that only runs by hand does not survive the increment, which is why the pair lives in the suite as well as in criteria 4 and 5." It requires five integration tests and says: "Verify with `grep -c 'fn .*missing_.*_path' tests/`, whose count the outcome records."

MEASURED, from the worktree root:

```
$ /usr/bin/grep -c 'fn .*missing_.*_path' tests/
/usr/bin/grep: tests/: Is a directory
0
exit=2
```

There is no `-r`. GNU grep refuses the directory, prints `0` on stdout and exits 2. The count it prints is `0` whether the suite holds five such tests, one, or none, so the command is inert in both directions: it cannot show the tests are present, and it cannot show they are absent. An outcome that "records the count" records `0` for a correct implementation.

This is the same class as the brief's known defect that `render --check --strict` exits 2 without its `<PLAN>` argument: a criterion line that does not run. It is class 2 rather than class 1 because criterion 8's prose obligation ("The integration tests gain one test per branch ... FIVE TESTS, because five branches") is explicit and a reviewer reads it, and because `cargo test` in criterion 11 runs whatever tests do exist.

---

### F9. `sidecar-status-opening-drift` criterion 5's diff bound is one line per file looser than its own stated justification

CLASS 2 (second-guard hole). Severity: low.

Criterion 5 (`:181`) reads: "For each file on the worklist, `git diff --numstat` reports at most 2 added and 2 removed lines, since each opening is one line in an unwrapped file and the fix rewrites that line in place rather than splitting it."

The stated justification supports 1 added and 1 removed. The bound is 2 and 2, which is exactly one further line-pair per file. These sidecars do not hard-wrap (`no-wrap-convention`), so one line is one paragraph: the slack admits one silent, unrelated paragraph rewrite in every worklist file, and no other criterion reads below the opening line. Criteria 1, 10, 11 and 12 all read the first non-blank non-heading line only. Criterion 4 checks path names, not content. Criterion 7 re-renders whatever is there.

The step's own scope says the opposite twice. `:9`: "It changes nothing else about any step." `:112`, under NOT IN SCOPE: "ANY SIDECAR TEXT BELOW THE OPENING LINE, with the single exception specified as item `B` below." And item `B`'s own argument (`:122`) is that the 2026-08-13 audit measured steps generated by the process itself rising from 8.3% to 54.2%, so "'while you are in the file anyway' is the exact habit that produced that number". The slack is the size of exactly that habit, once per file.

It is class 2 rather than class 1 because the property it fails to bound is a scope statement rather than a stated risk ground, a numbered RULE or a cited Principle, and because the whole-diff read a reviewer does at merge would show the extra part.

---

### F10. `validate-missing-source-exit`: the `error:` prefix the messages block specifies is pinned by no criterion

CLASS 1. Severity: low. This is the weakest of the class 1 items and it is stated as such.

THE MESSAGES block (`validate-missing-source-exit.md:37`) reads: "Each keeps its current wording and takes an error prefix, so an existing reader recognises the line", and gives the three strings with the prefix:

```
error: no source plan at <path>
error: no plan at <path>
error: no metrics log at <path>
```

Split it. PREMISE: each message keeps its current wording AND takes an `error:` prefix. CONSEQUENCE: an existing reader recognises the line.

The consequence has another cause. Keeping the current wording is on its own sufficient for recognition, so an implementation that keeps the wording and adds no prefix satisfies the consequence while falsifying half the premise.

Criteria 2, 3 and 4 pin the messages as "stderr carries a line ENDING `no source plan at docs/plans/TEMPLATE.plan.toml`" and the two equivalents. The lines end with the path, so "ending" pins everything except the prefix. Criterion 1 quotes the PRE-change stderr, which has no prefix. Criterion 7 pins the `--workflow` message, which is a different string. Criterion 9 reads `--help`. No criterion anywhere reads the head of the three new lines.

MEASURED, the current unprefixed wording, from an empty directory outside the repository:

```
$ agent-flow validate --source docs/plans/TEMPLATE.plan.toml
no metrics log at docs/metrics/workflow.jsonl; nothing to validate
no source plan at docs/plans/TEMPLATE.plan.toml; nothing to validate
exit=0
```

An implementation that changes only the exit path, leaving both lines byte-identical, satisfies criteria 2 and 4 as written (each line ends with the required string) and exits 1. The distinction between a note and an error then exists only in the exit code, which is the thing this step exists to make readable.

---

### F11. `step-intent-encoding` increment 1: criterion 4 and criterion 6 specify incompatible `eta` fixtures

CLASS 2. The fit to the brief's two sub-kinds is arguable: it is a contradiction between two acceptance criteria rather than a second-guard hole or a figure. Severity: low.

Criterion 4 (`step-intent-encoding.md:158`): "`src/plan/testdata/render-fixture.plan.toml` gains both fields on `alpha`, both on `gamma`, and BOTH on `eta` with only one of them filled".

Criterion 6 (`:176`): "THE PARTIAL CASE IS PINNED. `eta` carries `problem` and no `approach` in the fixture." Its pass condition is four printed lines, "the heading, a blank line, a `- problem:` line and a BLANK line. THE FOURTH LINE IS THE CRITERION."

Under criterion 4's literal reading, `eta` carries `approach` present and empty. Two consequences, both bad. RULE 3 (`:33`) rejects a value that is empty after a trim, so the fixture would carry a value the step's own rule forbids. And the render sub-rule at `:100`, "A STEP THAT CARRIES ONLY ONE FIELD emits only that line", no longer applies to `eta`, which carries two, so `render` emits a `- approach: ` line and criterion 6's fourth line is that line rather than a blank. Criterion 6 then fails on a fixture criterion 4 requires.

Criterion 6 is the one that states the intent unambiguously and it is the one the render sub-rule needs a fixture for. Criterion 4's "BOTH on `eta`" reads as a slip for "one of them on `eta`".

---

### F12. `step-intent-encoding` increment 3 changes `status --step` and runs no `status --step` command, and `src/main.rs` is absent from its changed-path set

CLASS 1. Severity: low.

Increment 3's WHAT CHANGES (`:505`) states a behaviour change to the CLI surface increment 1 added: "`status --step` drops the `(not recorded)` fallback for a TOML source and keeps it for the Markdown one."

Increment 1 grounds that fallback (`:123`): "For a field the substrate does not carry, the value prints as `(not recorded)`, so an absent field is never mistaken for an empty one." Split it. PREMISE: a field the substrate does not carry prints `(not recorded)`. CONSEQUENCE: an absent field is never mistaken for an empty one.

After increment 3 the consequence holds vacuously on the TOML substrate, because a TOML plan can no longer carry an absent field at all. The premise survives only on the Markdown substrate, and nothing tests it there.

Increment 3's acceptance block contains no `status --step` command. Increment 1's criterion 8 ran four, all against a TOML source, and the third of them (`status --source no-intent.plan.toml --step a`, expecting two `(not recorded)` lines) becomes unrunnable after the flip, because `no-intent.plan.toml` no longer parses. So of the four commands that pinned the flag, one is dead and three are never re-run. As in F2, increment 1 requires no suite test, so `cargo test` in criterion 11 has nothing to run.

THE WRONG IMPLEMENTATION. Drop the `(not recorded)` fallback outright rather than for the TOML source only. Every criterion of increment 3 passes, and `status --plan <markdown> --step <slug>` then prints an empty value where the step's own ground requires the absence to be visible.

A SECOND, RELATED TENSION IN THE SAME INCREMENT. `run_status` lives in `src/main.rs:1233` and `StatusArgs` at `src/main.rs:496`, which increment 1's own risk ground cites. `step_views()` (`src/plan/source.rs:416`) projects only `slug` and `status`, so `status --step` cannot read the intent through `PlanProjection`; it must read a type that carries the fields, and increment 1's changed-path set includes `src/main.rs` for exactly that reason. Increment 3's criterion 9 lists "the 12 declaration-site files" and four more, and `src/main.rs` is in neither group, measured:

```
$ for f in $(/usr/bin/grep -rlE '(\\n|^)slug = ' src tests pack docs/plans/TEMPLATE.plan.toml | sort); do printf '%s\t%s\n' "$(/usr/bin/grep -oE '(\\n|^)slug = ' "$f" | wc -l)" "$f"; done
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

Twelve files, 69 sites, no `src/main.rs`. Either the WHAT CHANGES sentence describes an edit criterion 9's exact path list then refuses, or the sentence describes no edit at all and its wording is wrong. One of the two is a defect and the criteria do not say which.

---

### F13. `sidecar-status-opening-drift` criterion 11's enlarged-word-list measurement reproduces on neither scope

CLASS 2 (non-reproducing measurement inside an acceptance criterion). Severity: low.

Criterion 11 (`:208`) states: "That silence survives an enlarged word list: adding `remains`, `awaiting`, `planned`, `to do`, `not done`, `when built`, `blocked`, `paused`, `will be` and `yet to` picks up `doc-redundancy-cleanup` (on `when built`) and `reviewer-reproducible-evidence` (on `paused`) and still does not reach it."

Criterion 11 runs over THIS STEP'S WORKLIST, which criterion 2 defines as `comm -23 anchored handover`. MEASURED, that worklist is 17 slugs, and the enlarged list over it picks up ONE:

```
doc-redundancy-cleanup	when built
```

`reviewer-reproducible-evidence` is on the HANDOVER list, so criterion 11 never reads it. Over the SELECTED set of 36 instead, the enlarged list picks up FOUR:

```
structured-skeleton	blocked
doc-redundancy-cleanup	when built
task-entry-regrounding	to do
reviewer-reproducible-evidence	paused
```

The named pair matches neither scope. The claim the sentence exists to support does hold on both: `planner-folds-decisions` is on the worklist (criterion 11's own witness) and the enlarged list does not reach it.

The neighbouring measurements in the same criteria all reproduce and are recorded here so the reviewer's own scope is checkable: the anchored selector prints 36, the unanchored 45, the complement 9 (all nine `Deferred <noun>` openings on `deferred` steps), a bare token strip over the 36 leaves 19 that criterion 12 flags, the worklist is 17, and criterion 10's word list over the worklist prints one row per worklist file, 17 of them.

---

## Figures inside an increment block that DO reproduce

Recorded so the triager can see the sweep was total rather than selective, and so a later round does not re-measure them. Every one below sits inside an acceptance criterion, a risk-class ground or a numbered RULE, which is the brief's test for a class 2 figure, and every one reproduced exactly on this tree. The plan carries 105 steps.

`step-intent-encoding`:

- RULE 3 and increment 1 criterion 3, the empty-backfill line count. `2 x 105 = 210`, and `2 x 101 = 202` for the earlier tree.
- Increment 1 criterion 4, the render fixture. `grep -c '^\[\[step\]\]'` prints 7 and `grep -c '^\[\[question\]\]'` prints 5 on `src/plan/testdata/render-fixture.plan.toml`, so `7 steps, 5 questions, valid` is right.
- Increment 1 criterion 7. `next --source <live plan> | grep -cE '^    (problem|approach): '` prints `0` and exits 1; the same command widened to all six slot names prints `4` and exits 0.
- Increment 1 criterion 8. `--help | sed -n '/^Commands:/,/^$/p' | grep -cE '^  [a-z]+ '` prints `8`.
- Increment 1 criterion 10. The batch rule prints `steps=105 batches=6 size=18`, and `grep -c 'id = "step-intent-encoding-inc2'` prints `6`. The K-from-101-to-120 claim holds by arithmetic: `ceil(120/6)=20` and `ceil(121/6)=21`.
- Increment 1's render sub-rule. `grep -nE '(\\n|^)slug = ' src/plan/render.rs` prints three sites, and the first, line 877, is the `N1` fixture inside `empty_details_sections_emit_no_bare_heading` (`src/plan/render.rs:872`).
- Batch criterion 7 and increment 3 criterion 8. R4 on the untouched tree prints `steps=105 source=0/0 quoted=1/1 projected=1/1`. The one quoted pair is `docs/plans/agent-scaffold.steps/step-intent-encoding.md:92` and `:93`, rendered at `docs/plans/agent-scaffold.md:3521` and `:3522`. The eight named sidecars are exactly the seven `[meta.sidecars].front` entries plus the one `tail` entry. `find docs/plans/agent-scaffold.questions -type f -size +0 | wc -l` prints 0.

`plan-order-array-position`:

- Increment 1 criterion 1, all four pre-change commands: 12 rows, `105`, 5 rows, `1`. The quoted schema error reproduces byte for byte, including the field list: ``unknown field `bogus`, expected one of `slug`, `title`, `status`, `order`, `blocked_by`, `folds`, `provenance`, `increment`, `waiver` ``.
- Increment 1 criterion 6. The awk on `src/plan/testdata/render-fixture.md` prints `zeta=1 epsilon=1 roadmap zeta<epsilon=0 details zeta<epsilon=0`.
- Increment 2 criterion 3. `grep -rnw 'order'` over the five front sidecars prints 8 rows across 5 files, and the three named rows are at the line numbers given.
- Increment 2 criterion 1's stated relation. `pre=47`, `exempt=21`, `drift=26`, rows reading 84 = 0, so `pre = exempt + drift + 84-rows` holds. `raw_sites=35 worklist_rows=26 surplus=9`.

`sidecar-status-opening-drift`: the anchored selector prints 36, the unanchored 45, the complement 9, a bare strip leaves 19 flagged, the worklist is 17, criterion 10's list prints one row per worklist file, `workflow-calibration.explorations/` holds 12 entries, and `validate --source <absent> --workflow` exits 1 carrying `--workflow requested but no plan source resolved`.

`ledger-order-citation-currency`: every figure reproduced, as the brief said. `135` and `116` for the population, `12` at or below 83, `12` rows on 84 or 91 splitting `7` and `5`, the busiest line carrying 8 drifting citations across four values with one value repeated three times, the dedup surplus of `20`, the single pre-existing annotation `1`, and `14` citations in `docs/metrics/workflow.jsonl` of which `13` are at or above 85. Criterion 2's four MEASURED lines are arithmetically consistent with all of it: `116 - 1 = 115`, `116 - 111 = 5`.

## Notes that do not bear on cleanliness

- The brief's known defect that `validate` exits 0 on an absent input is live and reproduced: from an empty directory, `validate --source docs/plans/TEMPLATE.plan.toml` prints two notes on stderr, nothing on stdout, and exits 0. No criterion in this review set treats a bare exit 0 as proof except `sidecar-status-opening-drift` criterion 8's first command, which the sidecar already records as an accepted residual with the `--workflow` arm as the blocker. That is correct: the `--workflow` arm exits 1 on the same tree, measured.
- All six gate lines ran. `render --check --strict` was given its `<PLAN>` argument and exited 0.
- No fixture was built with mode 000 or 600, so none needed restoring. Every fixture lives under `<scratchpad>/groundblind/`, in `po/`, `p1/`, `throwaway/` and `emptydir/`. Nothing outside that directory was written or deleted.

## Counts

| | |
| --- | --- |
| Total findings | 13 |
| Distinct findings | 13 |
| CLASS 1 | 8 (F1, F2, F3, F4, F6, F7, F10, F12) |
| CLASS 2 | 5 (F5, F8, F9, F11, F13) |
| Severity ceiling | medium |
| Non-reproducing figures inside an increment block | 1 (F13) |

Against the stop condition, the class 1 count is 8 where zero keeps the round clean, and the class 2 count is 5 where three or fewer keeps it clean. The round is not clean on either arm.

WHERE THE CLASS 1 ITEMS CLUSTER. Six of the eight are one shape: a criterion that proves a property on one of two symmetric surfaces. F1 proves the single-line rule on `problem` and not `approach`. F3 proves the batch identity on `problem` and not `approach`. F4 `cmp`s one template pair of two. F12 pins `status --step` on the TOML substrate and not the Markdown one. F2 and F10 are the same shape one level out: a rule proved once, at the increment that builds it, and never re-proved at the increment that rewrites it. Only F6 and F7 are structural rather than symmetric.

The pattern is the one the sidecars themselves name four times over, in the words "a reader who substitutes once proves one field", "one flag", "one arm". The rule is stated; it is applied at eight sites and dropped at six.

THE THREE RULES THE CLEAN SIDECAR OBEYS, TESTED AGAINST THE OTHER FOUR. The brief names them, and they held. `ledger-order-citation-currency` states every figure as a command's output and none as a pass condition, and every figure reproduced. The two sidecars whose search set contains themselves, `plan-order-array-position` and `sidecar-status-opening-drift`, both now refuse to write a concrete example into themselves and both state relations rather than counts inside their criteria; that is why F6 and F13 are about what the criteria FAIL TO PIN rather than about a figure that moved. Rule 3 is the one that still bites: `plan-order-array-position` increment 2's pass condition is three clauses of which two are identities, so the oracle it names has no measured value in it at all.
