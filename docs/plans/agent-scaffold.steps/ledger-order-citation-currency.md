### `ledger-order-citation-currency`: resolve the ledger's numbered step citations by slug, so they survive the `order` deletion (`Q-78-ledgersplit`, decided 2026-08-21, pending the review)

THIS STEP MUST NOT BUILD UNTIL THE `Q-78` REVIEW LOOP CONVERGES, AND IT IS BLOCKED BY NOTHING. The direction is decided: the human chose on 2026-08-21 to give the ledger's citations their own step, over keeping them inside `plan-order-array-position` increment 2 and over leaving them alone, receipt `type:"decision"` `q_id:"Q-78-ledgersplit"` in `docs/metrics/workflow.jsonl`.

AN EARLIER DRAFT DECLARED THIS STEP BLOCKED BY `plan-order-array-position` AND THE HUMAN REMOVED THAT EDGE ON 2026-08-21, receipt `type:"decision"` `q_id:"Q-78-ledgeredge"`. Its stated ground was a file collision, and the two steps share no file: criterion 6 below lists exactly `docs/plans/agent-scaffold.ledger.md` and excludes the plan TOML, the steps directory and the rendered plan by name, while `plan-order-array-position` names the ledger in neither increment's changed-path set and excludes it explicitly. The edge also inverted the cost, because the resolution table below reads the working tree directly while `order` is present and needs `git show` once the field is gone. NO CORRECTNESS ARGUMENT SUPPORTS AN EDGE IN EITHER DIRECTION: Principle 7, Reproducible, holds both ways, since the named-commit form works after the deletion as well as before. RUNNING THIS STEP FIRST IS CHEAPER AND THAT PREFERENCE LIVES HERE RATHER THAN IN `blocked_by` (Principle 2, Minimal by default).

THE PROBLEM. `docs/plans/agent-scaffold.ledger.md` cites steps by their `order` value, and `plan-order-array-position` deletes that field, so every such citation loses the thing it names.

THE APPROACH. Resolve each citation to the slug it always meant, additively, so the historical text survives and a reader can follow the citation without the deleted field.

WHY THIS IS NOT `plan-order-array-position` INCREMENT 2. That increment's oracle is an enumerated diff against the rendered plan: it edits sidecars, regenerates `docs/plans/agent-scaffold.md`, and checks that the projection's diff equals the sum of the sidecar diffs. `render` never inlines the ledger, because the ledger is not a sidecar and does not appear in `[meta.sidecars]`. So that oracle cannot reach a single ledger row, and an increment that carried the ledger would claim a coverage it cannot deliver. This step therefore carries its own oracle, built for an artefact `render` does not touch (Principle 6, Ground decisions in evidence).

THE POPULATION, MEASURED. Run:

```
grep -noE '\b(order|step) [0-9]+\b' docs/plans/agent-scaffold.ledger.md | wc -l
grep -noE '\b(order|step) [0-9]+\b' docs/plans/agent-scaffold.ledger.md | awk -F: '{n=$NF; gsub(/[^0-9]/,"",n); if (n+0 >= 85) print}' | wc -l
```

MEASURED on the tree this step was authored against, the two print `135` and `116`. Both numbers rise with every appended review round, so the outcome records what the commands print on the day and no criterion below states either figure as a pass condition.

THE DRIFT ARITHMETIC IS THE SIBLING STEP'S. The `order` values 84 and 91 are absent from the range, so a citation at or below 83 reads correctly as an array position and needs no edit, a citation from 85 to 90 drifts by one, and a citation at or above 92 drifts by two. MEASURED, 12 of the 135 sit at or below 83.

TWO CITED VALUES NAME NO STEP AT ALL, and they are named so the implementer does not hunt for them. 84 and 91 are the absent values, and the ledger cites both. MEASURED, 7 hits read `84` and 5 read `91`. Each is either a citation of a RENDERED POSITION rather than an `order` value, or a false positive of the search, or a mistake in the original entry. Criterion 4 disposes of each one by hand and forbids a guess.

THE RESOLUTION IS PROVABLE, WHICH IS WHAT MAKES THIS SAFE. The ledger spans 2026-07-09 to today and the plan grew throughout, so a reader might expect a citation's referent to depend on its date. It does not. The plan grew by APPENDING, and an `order` value, once assigned, kept its slug. MEASURED at four dated commits against today, every order-to-slug row at or above 85 that existed then agrees with today:

```
today=$(awk '/^slug = /{s=$3} /^order = /{sub(/order = /,""); if ($0+0>=85) print $0"\t"s}' docs/plans/agent-scaffold.plan.toml | sort -n)
for d in 2026-07-29 2026-08-05 2026-08-12 2026-08-19; do
  c=$(git log --until="$d" --format=%H -1)
  git show "$c:docs/plans/agent-scaffold.plan.toml" | awk '/^slug = /{s=$3} /^order = /{sub(/order = /,""); if ($0+0>=85) print $0"\t"s}' | sort -n > then.txt
  printf '%s then=%d agreeing=%d\n' "$d" "$(wc -l < then.txt)" "$(comm -12 <(sort then.txt) <(echo "$today" | sort) | wc -l)"
done
```

MEASURED, the four dates print `then=8 agreeing=8`, `then=11 agreeing=11`, `then=12 agreeing=12` and `then=18 agreeing=18`. So the mapping is append-only and a resolution taken from today's plan is the resolution the entry meant when it was written. Without that measurement the whole step would be a guess, which is why it is stated before the criteria rather than inside one.

### The form: ANNOTATE, and do not rewrite

EACH CITATION KEEPS ITS NUMBER AND GAINS THE SLUG, in the form ``<word> <n> (`<slug>`)`` where `<word>` is the citation's own `order` or `step`. The number stays and the slug is added after it. THE FORM IS GIVEN METASYNTACTICALLY AND NOT AS A CONCRETE PAIR, because a concrete pair in this file is itself a numbered citation that `plan-order-array-position` increment 2 then has to restate. One real instance already exists in the ledger, the single pre-existing annotation criterion 2 counts, and it is the worked example.

WHY ADDITIVE RATHER THAN SUBSTITUTIVE, MEASURED RATHER THAN ASSERTED. The ledger is the project's evidence base: every convergence count, every round total and every "do not re-raise without new evidence" ruling reads it, and escalation records quote its narrative. AN EXTERNAL QUOTATION OF THAT NARRATIVE EXISTS AND IT IS COUNTED. `grep -oE '\b(order|step) [0-9]+\b' docs/metrics/workflow.jsonl` returns 14 hits, 13 of them at or above 85, every one inside an `artifact` field quoting ledger narrative, and one of those records already carries the slug beside the number, which is this form arrived at independently. Under a substitutive edit a reader matching a metrics record's citation against the ledger finds nothing, and under an additive edit the substring still matches. Those 13 rows are the evidence for the FORM, and they are the only measurement in this file that distinguishes the two forms. `AGENTS.md` also treats the ledger as a record rather than a projection, so nothing can re-derive it once its text is changed. Principle 6, Ground decisions in evidence, decides it: the evidence must survive the correction that makes it readable.

THE TWO REJECTED ALTERNATIVES, RECORDED SO A REVIEW ROUND DOES NOT RE-RAISE THEM.

- RESTATE BY SLUG AND DELETE THE NUMBER, which is what `plan-order-array-position` RULE 4 prescribes for the sidecars. It is right there, because a sidecar is a live claim and the rendered plan re-derives it. It is wrong here, because the ledger holds frozen round narratives and deleting the number rewrites quoted evidence. The two artefacts differ in kind, and this is the ground for treating them differently.
- LEAVE THE CITATIONS AND ADD ONE DATED CONVENTION NOTE at the head of the ledger. Cheapest by far, and the human rejected it on 2026-08-21. It also fails the reader it is meant to serve: a note at line 1 does not help someone who lands on line 341 from a search.

THIS FORM IS A PLANNER JUDGEMENT AND NOT A HUMAN DECISION. The human decided that the ledger becomes its own step. The annotate-versus-restate choice was left to be decided on its own evidence, and the 13 external quotations counted above are that evidence. A reviewer who disagrees must argue against that measurement. THE APPEND-ONLY MEASUREMENT BELOW IS NOT EVIDENCE FOR THE FORM and an earlier draft pointed at it as though it were: it establishes that a resolution taken from today's plan is the resolution each entry meant, which is a precondition for ANY correction here and is exactly as true under a substitution as under an annotation.

### Increment 1, `ledger-order-citation-currency-inc1`: annotate every drifting citation

RISK CLASS `risky` (two consecutive clean review rounds). THE GROUND: the increment edits most of the drifting set in the artefact that every convergence count, every round total and every re-raise ruling in this project reads, and `next` echoes part of the same file verbatim to an agent as an instruction rather than as a report.

NO EDIT COUNT IS WRITTEN INTO THIS GROUND, AND AN EARLIER FORM STATED THE WRONG ONE. It gave the size of the drifting SET as the number of edits. Criterion 2's own correct-outcome line shows the two differ: the edit count is `drifting` minus `bare`, and `bare` is the rows whose value names no step. That earlier figure was the only figure in this sidecar that was not the output of a stated command, and it was the only one that failed to reproduce. The human accepted the finding on 2026-08-21 as residual risk, receipt `type:"decision"` `q_id:"Q-78-residuals"` in `docs/metrics/workflow.jsonl`, and the record here is the disposition. THE CONSEQUENCE THE HUMAN WEIGHED: nothing wrong can ship, because criterion 2's `bare` clause names those rows explicitly and criterion 4 disposes of each by hand. The cost accepted is that a reviewer of the outcome must re-derive them. A wrong slug on a round narrative misattributes a finding to the wrong step, and no validator reads the ledger, so nothing but this increment's own oracle catches it. The edit is additive and one revert undoes it, and the file ships to no scaffolded project, which argues the other way. The volume and the evidence-base role decide it, and the classification matches `plan-order-array-position` increment 2, which is `risky` for a smaller sweep of the same kind.

WHAT IT DOES. For every citation at or above 85, append the resolved slug in parentheses after the number. Change nothing else in the file. Do not reflow, do not reword the surrounding sentence and do not correct any other claim, however tempting, because a second kind of edit in this diff makes the oracle below unreadable.

THE RESOLUTION TABLE IS BUILT FROM A NAMED COMMIT, NOT FROM THE WORKING TREE, so the increment is reproducible whether it runs before or after `plan-order-array-position` deletes the field (Principle 7, Reproducible). When this step runs first the named commit is the increment's own base commit, and `git show` reads it exactly as it reads any earlier one. Record the commit in the outcome and build the table with:

```
git show <pre-deletion-commit>:docs/plans/agent-scaffold.plan.toml | awk '/^slug = /{s=$3} /^order = /{sub(/order = /,""); print $0"\t"s}' | sort -n > order-to-slug.tsv
```

ACCEPTANCE, EACH EXECUTABLE.

1. THE WORKLIST IS CAPTURED BEFORE THE EDIT. Write the drifting set to a scratch file OUTSIDE the repository:

```
grep -noE '\b(order|step) [0-9]+\b' docs/plans/agent-scaffold.ledger.md | awk -F: '{n=$NF; gsub(/[^0-9]/,"",n); if (n+0 >= 85) print}' > pre-ledger.txt
```

THERE IS NO `sort -u` IN THAT PIPELINE AND ITS ABSENCE IS THE POINT. A ledger line can carry the same citation more than once, and each occurrence is a separate edit site that this increment owes. MEASURED, the busiest single ledger line carries eight drifting citations across four values, three of them repeats of one value, and a deduplicating form collapses 20 sites across the file. Such a form would hand the implementer a worklist 20 short of the population criterion 2 counts and make the cross-check between the two unsound. Reproduce the surplus by running the command above with and without `sort -u` and subtracting.

No concrete value-and-slug pair is written into this sidecar as an example, for the reason the form paragraph above records: a concrete pair here is itself a drifting citation that the sibling step then has to restate.

The outcome records `wc -l` of that file and the resolution table's own `wc -l`. NO ROW COUNT IS WRITTEN INTO THIS CRITERION. The first number moves with every appended round and the second with every added step, which is why the criterion pins the commands, and the paragraph at THE POPULATION, MEASURED, above the increment block, is the one dated statement of them.

2. EVERY DRIFTING CITATION IS ANNOTATED, AND EVERY SLUG NAMES A REAL STEP. Run this under bash, from the repository root:

```
#!/usr/bin/env bash
# L1: annotation coverage, and slug resolution against the pre-deletion table.
LEDGER="$1"; TABLE="$2"; PLAN="$3"
drifting=0; annotated=0; bare=0; unknown=0; wrong=0
while IFS= read -r hit; do
  n=${hit##* }
  [ "$n" -ge 85 ] || continue
  drifting=$((drifting+1))
done < <(grep -oE '\b(order|step) [0-9]+\b' "$LEDGER")
while IFS= read -r hit; do
  n=$(printf '%s' "$hit" | sed -E 's/^(order|step) ([0-9]+) .*/\2/')
  [ "$n" -ge 85 ] || continue
  annotated=$((annotated+1))
  slug=$(printf '%s' "$hit" | sed -E 's/.*\(`([a-z0-9-]+)`\)$/\1/')
  grep -q "^slug = \"$slug\"\$" "$PLAN" || { echo "UNKNOWN SLUG: $hit"; unknown=$((unknown+1)); }
  want=$(awk -F'\t' -v n="$n" '$1==n {print $2}' "$TABLE" | tr -d '"')
  if [ -n "$want" ] && [ "$want" != "$slug" ]; then
    echo "WRONG SLUG: $hit wants $want"; wrong=$((wrong+1))
  fi
done < <(grep -oE '\b(order|step) [0-9]+ \(`[a-z0-9-]+`\)' "$LEDGER")
bare=$((drifting - annotated))
printf 'drifting=%d annotated=%d bare=%d unknown_slug=%d wrong_slug=%d\n' \
  "$drifting" "$annotated" "$bare" "$unknown" "$wrong"
```

Pass, all four clauses:

- `drifting` EQUALS THE ROW COUNT CRITERION 1 RECORDED. This clause is what makes the edit additive rather than substitutive, and it is stated first because it is the one a cheaper implementation breaks.
- `unknown_slug=0`.
- `wrong_slug=0`.
- `bare` equals the count of rows criterion 4 disposes of as non-citations AND whose value is at or above 85. The qualifier is load-carrying: `bare` is `drifting - annotated` and `drifting` counts only hits at or above 85, so a row reading `84` can never reach `bare`, and without the qualifier a correct implementation that disposes of an `84` row as a non-citation fails a condition it cannot satisfy. MEASURED, criterion 4's twelve rows split 7 reading `84` and 5 reading `91`, so at most 5 of them can contribute.

The oracle is the printed line and not the exit status, which is 0 in every case. An absent ledger prints `drifting=0`, which fails the first clause, so an absent input cannot pass.

MEASURED, four ledgers against this script:

- BEFORE THE EDIT it prints `drifting=116 annotated=1 bare=115 unknown_slug=0 wrong_slug=0`, so it detects the condition rather than merely staying silent. The single pre-existing annotation is real and is left as it is.
- A CORRECT ADDITIVE EDIT prints `drifting=116 annotated=111 bare=5 unknown_slug=0 wrong_slug=0`, and the five are the `91` rows, which name no step.
- AN IMPLEMENTATION THAT SUBSTITUTES THE SLUG FOR THE NUMBER at every drifting site, which is the rejected alternative recorded above and which falsifies the form's own ground, prints `drifting=5 annotated=0 bare=5 unknown_slug=0 wrong_slug=0`.
- A MIXED IMPLEMENTATION that annotates ten sites correctly and substitutes the other 101 prints `drifting=15 annotated=10 bare=5 unknown_slug=0 wrong_slug=0`, which keeps criterion 3's red-then-green executable.

BOTH SUBSTITUTIONS SATISFY THE OTHER THREE CLAUSES IN FULL. Only the `drifting` clause separates them from the correct edit, which is why this criterion states it first and why criterion 1 records the number it compares against.

3. RED THEN GREEN ON ONE ANNOTATION. Take one annotated citation, strip its parenthesised slug, run criterion 2's script and record that `bare` rises by one and `annotated` falls by one. Restore it and show the pair back at their passing values. The red output lands as evidence in the outcome.

4. THE TWO ABSENT VALUES ARE DISPOSED OF ROW BY ROW, AND NO ROW IS GUESSED. The `order` values 84 and 91 name no step, so no annotation is possible for a hit on either. List them with:

```
grep -noE '\b(order|step) (84|91)\b' docs/plans/agent-scaffold.ledger.md
```

MEASURED, that prints 12 rows. THE OBLIGATION: the outcome records, for every row it prints, which of three things the row is, and no row may be left without one. Either the row cites a RENDERED POSITION rather than an `order` value, in which case it is annotated with the slug at that position and the outcome says so; or the row is a false positive of the search, in which case the outcome quotes enough of the sentence to show it; or the row is an error in the original entry, in which case it is annotated `(no such step)` and left otherwise untouched. A row disposed of by a guess at the intended step is this criterion failed.

5. NOTHING BUT ANNOTATIONS CHANGED. The diff of the ledger adds text and removes none:

```
git diff --numstat -- docs/plans/agent-scaffold.ledger.md
```

Pass: the deleted-line count and the added-line count are EQUAL, because the file does not hard-wrap prose and every edited line is rewritten in place. Then confirm no wording changed outside the annotations:

```
git diff -U0 -- docs/plans/agent-scaffold.ledger.md | grep -E '^[+-]' | grep -v '^[+-][+-]' | wc -l
```

The outcome records that number and the reviewer reads the diff. A hunk that changes a sentence rather than adding a parenthesis is this criterion failed.

6. THE CHANGED PATH SET. `git diff --name-only` lists exactly `docs/plans/agent-scaffold.ledger.md`. No file under `src/`, `tests/`, `pack/` or `docs/plans/agent-scaffold.steps/` appears. `docs/plans/agent-scaffold.plan.toml` does not appear, because no `status` flips in this increment. `docs/plans/agent-scaffold.md` does not appear, and its absence is the point: `render` never inlines the ledger, which is why this step exists.

7. `next` STILL READS ITS RESUME BLOCK. `./target/debug/agent-flow next --source docs/plans/agent-scaffold.plan.toml` exits 0 and prints a `RESUME STATE (verbatim from the ledger)` section. The section's text changes where an annotation lands inside it, which is expected, and the outcome records the diff of that section. This criterion exists because `next` hands that text to an agent as an instruction, so a truncation there is a real defect that no other criterion here reaches.

8. THE SUITE, THE VALIDATORS AND ASCII. `cargo test` passes. `cargo clippy --all-targets -- -D warnings` exits 0. `./target/debug/agent-flow validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl` prints its `<N> steps, <M> questions, valid` line on stdout and exits 0. `./target/debug/agent-flow validate --source docs/plans/agent-scaffold.plan.toml --workflow` prints `workflow invariants hold` and exits 0. `LC_ALL=C grep -cP '[^\t\x20-\x7e]' docs/plans/agent-scaffold.ledger.md` prints `0`. The `valid` line is pinned as well as the exit code, because `validate` exits 0 on a source that is not there until `validate-missing-source-exit` lands.

### NOT IN SCOPE, NAMED SO IT IS NOT DRAWN IN

- THE SIDECAR AND FRONT-SIDECAR CITATIONS. `plan-order-array-position` increment 2 owns them, and it restates them by slug rather than annotating them, for the reason recorded above.
- EVERY OTHER STALE CLAIM IN THE LEDGER. The file holds superseded transient blocks by design, each marked as frozen history. This increment corrects citations and corrects nothing else.
- THE LEDGER'S EVENTUAL DELETION. `AGENTS.md` says a ledger is deleted when its task closes. This plan's ledger outlived several tasks, which is its own question and not this step's.
