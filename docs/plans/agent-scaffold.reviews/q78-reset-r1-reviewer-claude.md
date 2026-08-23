# Q-78 reset round 1, Claude lens: fix verification, adoption, executability

Reviewer file. Worktree `.agents/worktrees/q78-reset-r1-claude`, branch `review/q78-reset-r1-claude`, tree at `77128ab`. Target: the five `Q-78` sidecars at their complete current contents. Repair commit under review: `70fd47b`.

METHOD. Every round 4 demonstration was rebuilt from the sidecar text rather than copied from another agent's fixture. Every criterion whose result is a command was run. Where a criterion claims a construction is refused, the construction was BUILT and the criteria were run against it. Fixtures live under the session scratchpad in `q78-reset-r1-claude/`, in `drift/`, `gb2/`, `ledger/` and `misc/`, all directories this review created and owns. A throwaway clone of this worktree lives at `drift/clone/` and is where `cargo build` and every mutation ran; nothing was written inside the repository and `git status --short` in this worktree reports only this findings file.

MEASUREMENT HAZARDS HONOURED. `grep` in this shell is a function wrapping `ugrep`, and `/usr/bin/grep` does not exist on this machine, so GNU grep is invoked by its absolute store path `/nix/store/gn94gpcp5q08x4v6g8mvw8v4r65rcjzk-gnugrep-3.12/bin/grep` (written `GG` below) wherever an escape or a `-P` pattern matters. Inside a `#!/usr/bin/env bash` script the function is not inherited, so the sidecars' own scripts get GNU grep; each finding below states which binary produced its numbers and, where the two differ, both were run. `grep -c` exits 1 on a zero count and that is data, not command failure. `validate` exits 0 on absent input, so every `validate` result pins its stdout line. Toolchain commands ran through `direnv allow && eval "$(direnv export bash)"`.

---

# Part 1. Verification of the mandated repairs

Each of the eleven repairs the reset fix brief mandated was attacked with the wrong implementation its finding named.

| Finding | Repair | Verdict |
| --- | --- | --- |
| `GB-1` | drift criterion 6, the `opening-anchors.tsv` provenance check | CLOSES on its anchor half. Both round 4 falsifiers rebuilt and run: the fabricating one (all 17 worklist openings replaced) and the probe-first one (whole opening line deleted on all 17) each print `checked=17 bad_anchor=17 added=0`. The correct bare strip prints `checked=17 bad_anchor=0 added=0`. The `added` half of the same criterion is inert; see `C-1`. |
| `GB-2` | increment 2 criterion 1's named-commit table plus criterion 2's two discriminating clauses | CLOSES. Table built with `git show HEAD:...`; a correct implementation over the live sidecar tree prints `rows=26 restated=25 wrong_slug=0 number_survives=1`, which is exactly `rows=R restated=R-E wrong_slug=0 number_survives=E` with `R=26` and `E=1`. The untouched tree prints `rows=26 restated=0 wrong_slug=0 number_survives=26`, so the criterion separates them. |
| `GB-3` | `src/plan/testdata/render-fixture.md` added to increment 3 criterion 9 | CLOSES. `step-intent-encoding.md:741` and `:743` now name it with its reason. Confirmed the collision it resolves is real: `src/plan/render.rs:660` holds the `GOLDEN` include and `:698` the equality assertion; `src/plan/testdata/render-fixture.plan.toml` holds 7 `slug` sites. |
| `GB-5` | increment 3 criterion 5's two content greps over both sides of the example-step pair | CLOSES. `pack/plan-template.steps/example-step.md` and `docs/plans/TEMPLATE.steps/example-step.md` are byte-identical (`cmp` exits 0) and carry the uncorrected sentence today, so the greps at `:704` and `:708` are the oracle criterion 5's `cmp` was not. A sentence naming only `problem` now fails. |
| `GB-6` | increment 1 criterion 8's content check | CLOSES. `$GG -rln 'entries with status and order' pack/ AGENTS.md .agents/` returns exactly `pack/AGENTS.md`, `AGENTS.md`, `.agents/AGENTS.reference.md` today, so the after-condition (empty stdout, exit 1) detects a mechanically green regeneration that keeps the clause. |
| `GB-7` | criterion 4's fourth disposition plus `vacated-order-to-slug.tsv` | CLOSES for the rows it reaches. The named historical commit exists and is not hypothetical: scanning all 142 commits that touched the plan TOML, exactly two carry both vacant values, `5fcd020` and `d39964f2` (2026-07-27 and 2026-07-28), each resolving `84` to `rename-to-agent-flow` and `91` to `exploring-item-actor-boundary`. With the historical table supplied, L1 on a correctly annotated ledger prints `drifting=117 annotated=117 bare=0 unknown_slug=0 wrong_slug=0`, so the forced `(no such step)` disposition is no longer the only one that passes. The criterion's search does not reach every vacated-value row; see `C-3`. |
| `GB-8` | criterion 8's red controls in a throwaway worktree | CLOSES. `validate-missing-source-exit.md:108-114` now mutates one branch family at a time and states in its own words that five correctly named `assert!(true)` stubs "fail this control because none reddens". The stub construction the finding named is refused. |
| `GB-10` | increment 1 criterion 10's frozen manifest, read by every batch | CLOSES. The batch identity check at `:326-338` now reads `declared.txt` from `docs/plans/step-intent-encoding.batches.tsv` and `:340` states "The live step count and a recomputed S do not appear anywhere in this identity check", so neither the shrink refusal nor the growth coverage hole can arise. Reproduced the partition at today's `N`: `steps=105 batches=6 size=18`, batches of 18/18/18/18/18/15, and `grep -c 'id = "step-intent-encoding-inc2'` prints 6, so `declared_loops` equals `manifest_batches`. |
| `GB-11` | both criteria abstracted to `<M> questions` | CLOSES. `plan-order-array-position.md:269` and `step-intent-encoding.md:141` now read `<N> steps, <M> questions, valid` with the outcome recording the complete line. `$GG -c '^\[\[question\]\]'` prints 80 today, and neither criterion depends on it. The two remaining literal `1 steps, 0 questions, valid` conditions (`step-intent-encoding.md:665`, `validate-missing-source-exit.md:94`) are over the one-step scaffold template, which is fixed data, and were verified to reproduce. |
| `F1` | criterion 2's explicit invocation with both arguments absolute | CLOSES. Run as printed, `bash <scratch>/h1.sh <scratch>/anchored.txt <scratch>/steps-copy > <scratch>/handover.txt` from the repository root, H1 produces a 19-row handover list from a 36-row selected set, leaving a 17-row worklist. Neither mode A (empty capture) nor mode B (whole selected set as handover) arises when the stated directory and argument form are used. |
| `T-1` | section `B`, criterion 5's exception and criterion 6's item all withdrawn | CLOSES. `$GG -n '^### ' docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md` shows no `### B` section; criterion 5 now carries only the `G-F9` numstat residual; `workflow-calibration` survives in the sidecar only as prose and as the named exclusion at `:112`, which states the reason the file is not opened. `workflow-calibration` is row 9 of the reproduced handover list, so the exclusion agrees with the measurement. |

BASE MEASUREMENTS RE-RUN AND REPRODUCING. Anchored selector 36 rows; H1 handover 19 rows; `comm -23` worklist 17 rows. Criterion 1's complement prints exactly the nine adjectival `deferred` openings the sidecar enumerates at `:22`. Increment 1 criterion 1's four before-values print 12 rows, `105`, 5 rows and `1`. The `slug` and `order` declaration-site searches each return 12 files and 69 sites; the `status` anchor returns 99. `for f in docs/plans/agent-scaffold.steps/*.md; do head -1 "$f" | grep -q '^#' || echo "$f"; done` prints `core-assets.md` alone. `render-fixture.plan.toml` validates as `7 steps, 5 questions, valid`. `next --source <live plan> | grep -cE '^    (problem|approach): '` prints `0` and exits 1, widened to the six slot names prints `4`. `--help | sed -n '/^Commands:/,/^$/p' | grep -cE '^  [a-z]+ '` prints `8`. `validate --source bogus.plan.toml` prints the unknown-field message with the exact nine-field expectation list quoted at `plan-order-array-position.md:113`. In an empty directory `validate --source docs/plans/TEMPLATE.plan.toml` prints both notes with the `; nothing to validate` tail and exits 0, and adding `--workflow` exits 1 carrying `--workflow requested but no plan source resolved`. `validate --help` is 11 lines and `grep -c -F -- 'must exist'` over it prints `0`. `grep -rnw 'order'` over the five front sidecars prints 8 rows across 5 files. R4 on the untouched tree prints `steps=105 source=0/0 quoted=1/1 projected=1/1`. Ledger totals are `137` and `117` against the sidecar's dated `135` and `116`, with 12 rows at or below 83 unchanged; the sidecar states at `:20` that both totals rise with every appended round and makes neither a pass condition, so the movement is inside its recorded boundary and is not a finding.

# Part 2. Verification of the four accepted residuals

Each residual was checked for identifier, severity, owning increment and criterion, accepted cost, and non-expansion boundary, and each cited receipt was confirmed to exist exactly once in `docs/metrics/workflow.jsonl`.

| Residual | Home | Severity | Owner named | Cost stated | Boundary stated | Receipt |
| --- | --- | --- | --- | --- | --- | --- |
| `GB-4` | `step-intent-encoding.md:170` | `low` | increment 1 criterion 3 and RULE 3 | the criterion exercises `""` and not a whitespace-only string | accepts only the whitespace-only distinction; does not waive the empty literal, the single-line rule, either field, or the flip | `Q-78-round4-low-residuals` x1, `Q-78-gb11-revision` x1 |
| `GB-9` | `validate-missing-source-exit.md:118` | `low` | increment 1 criterion 9 | `grep -c` counts lines, so the phrase can sit on three unrelated help lines | accepts only the attribution hole; does not waive criteria 2 to 5, criterion 8's tests and red controls, or any behaviour change | same pair |
| `F2` | `step-intent-encoding.md:731` | `low` | increment 3 criterion 6 | a sentence on its own line INSIDE the note prints `:0` too | accepts only that placement-oracle hole; does not waive presence, the byte-identical pair, or the how-to-add-step guidance | same pair |
| `F3` | `plan-order-array-position.md:413` and `step-intent-encoding.md:765` | `low` | increment 1 criterion 8 and increment 3 criterion 9, plus both DOCUMENTATION IMPACT duties | duplicate heading or a clobbered entry, with no content check | accepts only the sequencing ambiguity between the two declared duties; does not permit duplicate headings generally, does not waive either entry, does not alter either path set or the blocking edge | same pair |

All four are complete on every element the fix brief required, both `F3` copies agree, and none expands beyond its recorded boundary. `Q-78-loop-split`, `Q-78-risk-class-source` and `Q-78-foreclosure-enforcement` each occur exactly once as well. All thirteen `[[step.increment]]` entries are declared `risky` in `docs/plans/agent-scaffold.plan.toml:1537-1622`, so the two-clean-round requirement is a recorded property and not an assumption.

I did not re-raise `GB-4`, `GB-9`, `F2` or `F3`, and no finding below re-raises a settled item. `C-1` concerns a guard the repair for `GB-1` introduced and is new content; `C-2`, `C-3`, `C-4`, `C-5` and `C-6` were not raised in any earlier round, which was checked against `q78-r7-*` and `q78-r8-*`.

---

# Part 3. Findings

## `C-1`. Criterion 6's added-words arm can never fire, so the drift step's premise half has only one working oracle

- OWNING INCREMENT: `sidecar-status-opening-drift-inc1`.
- SEVERITY: `medium`.
- CLASS: class 1.

CLAIM. Criterion 6 (`sidecar-status-opening-drift.md:229`) filters its word-diff with `grep -E '^\+' | grep -v '^\+\+\+'`. The second pattern is a basic regular expression in which `\+` is the GNU repetition operator, so `^\+\+\+` matches EVERY line beginning with one or more `+`, not the `+++ b/<path>` header alone. `additions` is therefore always empty and `added` is always `0`. An implementation that makes the decided deletion AND authors new prose inside a worklist opening passes criteria 1, 4, 5, 6, 10 and 12 with output byte-identical to the correct implementation's, which falsifies the increment's PREMISE at `:39` ("authors no replacement line ... Any stale clauses later in that same line are removed by deletion rather than replaced with new prose") and the assertion at `:43` that criterion 6 "rejects every added word in those lines".

REPRODUCIBLE EVIDENCE.

The regex behaviour, minimally, under GNU grep and under ugrep alike (both print the warning `stray \ before +` and both drop the added-word line):

```
printf '+++ b/x\n+authored words\n' | grep -E '^\+' | grep -v '^\+\+\+'
```

prints NOTHING and exits 1. Changing only `-v` to `-vE` prints `+authored words` and exits 0, under both binaries.

The wrong implementation, built and run in the throwaway clone against the increment's own criteria. Base is `77128ab`; anchors are criterion 2's `opening-anchors.tsv` over the reproduced 17-file worklist. The implementation applies criterion 2's exact strip to all 17 worklist files and then REPLACES a stale clause in `decision-folder-currency.md`'s opening line, which `:97` names as a worked example, with 20 words of authored prose no reviewer has seen. `git diff --word-diff` shows the added words; the criterion does not:

| Criterion | Result on the authored-prose implementation |
| --- | --- |
| 1, anchored selector then `comm -3` against `handover.txt` | prints NOTHING. PASSES |
| 4, `git diff --name-only` | identical to `worklist.txt`, `diff` exits 0. PASSES |
| 5, `git diff --numstat` | 17 rows, none exceeding 2 added or 2 removed. PASSES |
| 6, the anchors-and-additions script | `checked=17 bad_anchor=0 added=0`. PASSES |
| 10, keyword scan | 8 rows, and `decision-folder-currency` is NOT among them, because the falsifier deleted the `still` that used to flag it. The authored sentence is not reachable by criterion 10's obligation at all |
| 12, first-character test | ZERO rows. PASSES |

The control, the same 17 files given the bare strip alone, prints `checked=17 bad_anchor=0 added=0` as well, so the two implementations are indistinguishable on every command the increment runs.

WHY CLASS 1. The increment's ground is stated at `:37` as a premise and a consequence, each half required to name the criterion that refuses it, and `:43` asserts "BOTH HALVES ARE REFUSED BY CONSTRUCTION". Criterion 6's anchor half does refuse the two round 4 falsifiers, verified above. Its addition half refuses nothing, so the premise clause "authors no replacement line" has no oracle. The wrong implementation also violates the human decision `Q-78-statusform` (`:13`), which chose DELETE over replace on reasoning that cites Principle 8 and Principle 1 by name, and the NOT IN SCOPE bullet at `:110`, "It does not review, re-scope, re-title or rewrite a single step."

IT ALSO WIDENS AN ACCEPTED RESIDUAL PAST ITS RECORDED BOUNDARY, which is why this is not merely a dead line of shell. The `G-F9` residual at `:213` accepts the loose 2-and-2 numstat bound and records "WHAT BOUNDS IT: criterion 6 forbids additions in the opening itself". It does not. The human accepted a cost bounded by a guard that cannot fire, so the accepted risk is larger than the record of it.

REQUIRED CORRECTION. Change the filter to `grep -vE '^\+\+\+'` (verified to work under GNU grep and ugrep), or drop the second `grep` and filter on `^\+[^+]` instead. State the corrected `added` behaviour as a MEASURED red: an implementation that authors any word inside a worklist opening prints a non-zero `added`. While the criterion is being edited, note that `added` is computed over the whole file diff rather than the opening line, which is stricter than `:213` describes; either narrow the diff to the opening line or correct `:213` to say what criterion 6 actually bounds.

## `C-2`. The citation search is case-sensitive, so four capitalised citations at or above 85 survive increment 2 and resolve to nothing

- OWNING INCREMENT: `plan-order-array-position-inc2`.
- SEVERITY: `medium`.
- CLASS: class 1.

CLAIM. Every instrument in increment 2 anchors on the lower-case words: criterion 1's capture (`:288`), P1's `actual` recomputation (`:336`), criterion 2's `post` sweep (`:367`) and criterion 6's ledger count (`:402`) all use `grep -rnoE '\b(order|step) [0-9]+\b'`, with no `-i`. Criterion 3's bare-word worklist searches five front sidecars only and needs no number. The sidecar states at `:281` that "The drift lives in both spellings. Do not search one", and names the two spellings as `order` and `step`; capitalisation is a third variant it does not name. Four citations written `Step <n>` at or above 85 sit inside the increment's own search set and are invisible to every one of its criteria, so a criteria-complete implementation leaves them, and after increment 1 deletes the field they resolve to nothing. That is increment 2's stated risk ground at `:275` verbatim: "a missed site leaves a citation that resolves to nothing, or worse, to the wrong step, which is the same class of miss that produced the drift this step exists to remove."

REPRODUCIBLE EVIDENCE.

The missed set, from the repository root under GNU grep (the same command with the lower-case alternation is criterion 1's own):

```
grep -rnoE '\b(Order|Step) [0-9]+\b' docs/plans/agent-scaffold.steps/ docs/plans/agent-scaffold.success-criteria.md docs/plans/agent-scaffold.documentation-protocol.md docs/plans/agent-scaffold._status-narrative.md | sort -u
```

prints exactly four rows, all at or above 85:

```
docs/plans/agent-scaffold.steps/checks-runner-worktree-name-collision.md:90:Step 85
docs/plans/agent-scaffold.steps/decision-folder-currency.md:3:Step 89
docs/plans/agent-scaffold.steps/decision-folder-currency.md:34:Step 89
docs/plans/agent-scaffold.steps/workflow-enforcement-tier.md:308:Step 92
```

All four name a real step at that `order` value: 85 is `drift-guard-test-hook-hygiene` (`docs/plans/agent-scaffold.plan.toml:1175`), 89 is `planner-folds-decisions`, 92 is `prompt-drift-guard`. The `checks-runner-worktree-name-collision.md:90` row is the sharpest, because that line carries NO lower-case citation at all, measured: `sed -n '90p' ... | grep -coE '\b(order|step) [0-9]+\b'` prints `0`. The whole line is outside every capture the increment makes, and the citation is bare: "Step 85 is a process-global panic-hook swap in `src/agents_md_drift.rs`".

The criteria-complete implementation, built on a copy of the sidecar tree at `gb2/tree` and restating every one of the 26 rows in `drift.txt` except the single enumerated quotation row. P1 run verbatim from that tree prints

```
NUMBER SURVIVES docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md:105 (was step 86)
rows=26 restated=25 wrong_slug=0 number_survives=1
```

which is `rows=R restated=R-E wrong_slug=0 number_survives=E`, all four clauses met. `diff` of the recomputed line counts against `lines-pre.txt` exits 0 and `exempt_lost=0`. Re-running the capitalised search over that same tree still prints the identical four rows, so nothing in the increment moved them.

WHY THIS IS NOT COVERED BY `GB-2`'S REPAIR. `GB-2` was about the resolution TABLE's source. That repair holds, verified above. This is the population, and the two are independent: the named-commit table resolves 85, 89 and 92 correctly, and no criterion ever asks it to.

REQUIRED CORRECTION. Anchor the searches on a case-insensitive alternation, `\b([Oo]rder|[Ss]tep) [0-9]+\b`, in criterion 1's capture, in P1's `actual` recomputation and in criterion 2's `post` sweep, so the three agree. State the four rows above as a MEASURED before-figure or, better, as a command whose output the outcome records, since the count moves as the sidecars are edited. RULE 4 or the SCOPE paragraph should say that the citation's leading word is matched without regard to case, so the omission is closed by a stated rule and not only by a regex.

## `C-3`. The same case-sensitivity leaves fourteen capitalised ledger citations unannotated while L1 prints a fully clean line

- OWNING INCREMENT: `ledger-order-citation-currency-inc1`.
- SEVERITY: `medium`.
- CLASS: class 1.

CLAIM. Criterion 1's population capture (`:79`), both loops of L1 (`:99` and `:112`) and criterion 4's vacated-value search (`:141`) all use a lower-case-only alternation. Fourteen occurrences written `Step <n>` or `Order <n>` at or above 85 sit in `docs/plans/agent-scaffold.ledger.md`, nine of them with no slug anywhere adjacent. An implementation that annotates every citation the capture prints leaves all fourteen bare and L1 reports `bare=0` with every clause met, because `drifting` never counted them. THE PROBLEM this step states at `:7` is then false of fourteen citations: "every such citation loses the thing it names". The increment's own ground at `:56` says "no validator reads the ledger, so nothing but this increment's own oracle catches it", and the oracle is blind to the class. Criterion 4 is affected independently: its search misses `Step 91` at ledger line 339, so one vacated-value row escapes the row-by-row disposal obligation that `:144` makes absolute ("no row may be left without one").

REPRODUCIBLE EVIDENCE.

The missed set, from the repository root under GNU grep:

```
grep -noE '\b(Order|Step) [0-9]+\b' docs/plans/agent-scaffold.ledger.md | awk -F: '{n=$NF; gsub(/[^0-9]/,"",n); if (n+0 >= 85) print}'
```

prints 14 occurrences at lines 339, 343 (twice), 363, 387, 931 (twice), 943, 1601, 1603, 1715 (twice) and 1731 (twice). Of those, the form `(Order|Step) <n> ` followed by a backticked slug accounts for 5 (339, 343, 363 and both at 931); the remaining NINE carry no slug at all and are exactly the rows this step exists to make followable. Samples, read in context rather than counted: line 343 "Step 92 has taken ZERO findings across rounds 2 and 3", line 943 "Step 92 spent SIX rounds and FIFTEEN findings on ONE coverage claim", line 1603 "Step 93's escalation reduces to ONE answerable question", line 1731 "Step 86 STAYS `in-progress` (inc1 of 4 done)" (twice on that line).

The criteria-complete implementation. A fixture at `ledger/fix/agent-scaffold.ledger.md` was built by annotating every occurrence the lower-case capture reaches, at or above 85 and at 84, from the pre-deletion table (`git show HEAD:...`) and the historical table (`git show 5fcd020:...`), skipping the single pre-existing annotation the criterion says to leave alone. L1 run verbatim against it prints

```
drifting=117 annotated=117 bare=0 unknown_slug=0 wrong_slug=0
```

against criterion 1's captured row count of `117`, so all four clauses of criterion 2 are met. Against the unedited ledger the same script prints `drifting=117 annotated=1 bare=116 unknown_slug=0 wrong_slug=0`, so it does detect the condition it was built for. Re-running the capitalised search over the annotated fixture still prints the same 14 occurrences.

The criterion 4 half, independently. `grep -noE '\b(order|step) (84|91)\b' docs/plans/agent-scaffold.ledger.md` prints 14 rows today; `grep -noE '\b(Order|Step) (84|91)\b'` prints one more, `339:Step 91`, and its narrative is a genuine citation: "Step 91 `exploring-item-actor-boundary` was authored during the round-1 fix pass and REMOVED again by the round-3 split". It is a row criterion 4 must dispose of and does not print.

WHY THIS IS DISTINCT FROM `C-2`. Same root cause, two increments, and neither repair reaches the other: the sidecar sweep restates and deletes the number where the ledger annotates and keeps it, the two run over disjoint file sets, the two use different scripts (P1 against L1), and this one additionally breaks criterion 4's vacated-value obligation, which has no counterpart in the sibling. The evidence above is measured entirely inside `docs/plans/agent-scaffold.ledger.md`.

REQUIRED CORRECTION. Make criterion 1's capture, both L1 loops and criterion 4's search case-insensitive on the leading word, `\b([Oo]rder|[Ss]tep) [0-9]+\b` and `\b([Oo]rder|[Ss]tep) (84|91)\b`. Keep the annotation form's `<word>` as the citation's own word so a capitalised citation is annotated `Step 92 (`prompt-drift-guard`)`, which the amended `annotated` regex must then also match. The five capitalised rows that already carry a bare backticked slug need a stated disposition, since they are resolvable but not in the parenthesised form L1 counts.

## `C-4`. Criterion 2's `post` clause omits the rows reading 84 that criterion 1's own relation names, so it refuses a correct implementation

- OWNING INCREMENT: `plan-order-array-position-inc2`.
- SEVERITY: `low`.
- CLASS: class 2, a criterion that refuses a correct implementation.

CLAIM. Criterion 1 states the relation at `:319`: "`pre` equals `exempt` plus `drift` plus the rows reading 84". Criterion 2's pass condition at `:371` reads "`post` equals `wc -l < exempt.txt` plus the enumerated `NUMBER SURVIVES` rows", which drops the 84 term. A row reading 84 is in neither `exempt.txt` (`<= 83`) nor `drift.txt` (`>= 85`), so P1 never reads it and no instruction in the increment restates it, yet it is still matched by the `post` sweep. `post` is therefore always `exempt + E + (rows reading 84)`, and the pass condition is unmet on every correct implementation for as long as any such row exists.

REPRODUCIBLE EVIDENCE. Measured on the live tree with the criterion's own commands:

```
pre=48 exempt=21 drift=26 eightyfour=1
```

and `21 + 26 + 1 = 48`, so criterion 1's relation reproduces. The single 84 row is `docs/plans/agent-scaffold.steps/ledger-order-citation-currency.md:24:order 84`, and it is prose explaining the vacancy itself ("the 84 rows name `rename-to-agent-flow` before it moved from order 84 to 100"), so restating it would destroy the sentence. It shares its line with no drifting citation, measured with `comm -12` over the line keys of `eightyfour.txt` and `drift.txt`, which prints nothing.

On the correct-implementation fixture at `gb2/tree`, criterion 2's second half prints

```
post=23 exempt_lost=0
```

against a required `post` of `21 + 1 = 22`. `comm -13 exempt.txt post.txt` names the two surplus rows: the enumerated quotation row `sidecar-status-opening-drift.md:105 step 86`, which the clause allows for, and `ledger-order-citation-currency.md:24 order 84`, which it does not. Removing only the 84 row from `post.txt` gives exactly `22`, so the 84 term is the whole of the discrepancy and the clause is otherwise sound.

REQUIRED CORRECTION. Restate the clause as "`post` equals `wc -l < exempt.txt`, plus the rows reading 84, plus the enumerated `NUMBER SURVIVES` rows", or capture the 84 rows into their own file in criterion 1 (as the sibling step does for its vacated values) and add that file's `wc -l` to the sum. Either form keeps the clause's discriminating power: a deleted or renumbered citation still moves `post` away from the sum.

## `C-5`. Increment 3 criterion 9 requires `docs/plans/agent-scaffold.md` in the diff, and no edit the increment specifies can change it

- OWNING INCREMENT: `step-intent-encoding-inc3`.
- SEVERITY: `medium`.
- CLASS: class 2, a criterion that refuses a correct implementation.

CLAIM. Criterion 9 (`step-intent-encoding.md:741`) enumerates the changed-path set and includes `docs/plans/agent-scaffold.md`, and `:745` states the enumeration is exact ("an implementer who made any of those edits FAILED it, and one who obeyed it shipped the defect instead"). By increment 3's own text no edit it makes can move that file. The same criterion forbids it: "its diff must touch no `problem` or `approach` value, because the batches own those". Every live step therefore already carries both fields when increment 3 opens, and increment 3's only render change is that `render` "emits both lines unconditionally" (`:552`), which is byte-identical output on a plan where every step carries both. No implementation can satisfy criterion 9 as written except by hand-editing the generated view, which the plan's convention forbids and which no criterion of this increment detects, since criterion 11 (`:749`) runs `cargo test`, clippy, the two `validate` invocations and the ASCII sweep, and does not run `render --check --strict` against the live plan at all.

REPRODUCIBLE EVIDENCE. The chain is settled by citation plus two measurements.

- `:741` requires the file; `:745` makes the enumeration exact.
- `:741` forbids touching any `problem` or `approach` value, and `:737` (criterion 8) requires `source` to equal `steps` for both fields, so the live plan is fully filled before this increment and unchanged by it.
- `:552` and `:554` list what increment 3 changes: two schema types, the two `if let Some` arms, `render`'s emission condition, `next`'s boundary wrapping, `src/main.rs`'s fallback, the inline declaration sites, the three pack pairs, and the two deleted TSVs. Only the pack pairs project into a rendered document, and that document is `docs/plans/TEMPLATE.md`, which criterion 9 also names.
- `render` does not project `[[step.increment]]`: `grep -n 'increment' src/plan/render.rs` returns only doc comments, a waiver-unit formatter at `:523-528` and test text, so the one plan-TOML change criterion 9 conditionally allows cannot move the document either.
- R4 on today's tree prints `steps=105 source=0/0 quoted=1/1 projected=1/1`, and criterion 8 requires `projected` minus `quoted` to equal `source` after the increment. With `source` at `105/105` from the batches, `projected` must already be `106/106` before increment 3 runs, which is the same statement from the other side: the projection is final before this increment opens.
- The convention that the outcome record does not count towards a path set is fixed by the sibling: `plan-order-array-position.md:257` requires that "no file under `docs/plans/agent-scaffold.steps/` must appear" and that `docs/plans/agent-scaffold.md` "must not appear", in an increment that also writes an outcome.

REQUIRED CORRECTION. Drop `docs/plans/agent-scaffold.md` from criterion 9's enumeration and add it to the criterion's stated must-not-appear list with its reason (the batches already produced the final projection and this increment's render change is a no-op over a fully filled plan), in the shape criterion 9 already uses for the paths it added. If the projection is expected to move for a reason not written down, state that reason and give the command that proves it. Separately, add `render --check --strict docs/plans/agent-scaffold.plan.toml` to criterion 11, so a hand-edit of the generated view is refused rather than merely discouraged.

## `C-6`. Four criteria that run outside the repository invoke the binary by a repository-relative path

- OWNING INCREMENT: `validate-missing-source-exit-inc1`.
- SEVERITY: `low`.
- CLASS: class 2, a criterion that refuses a correct implementation.

CLAIM. Criteria 2, 3, 4 (both commands) and 5 each state "In an empty directory outside the repository" or "In the same directory" and then invoke `./target/debug/agent-flow`. From that working directory the path does not resolve, so run verbatim against a CORRECT implementation each command exits 127 with empty stdout and no `error:` line, failing its own pass condition. This is the failure mode `F1` was upheld for, one level down: a command whose result depends on a working directory the sidecar names but does not reconcile with the paths inside the command. The step's own measurement paragraph at `:12` uses the bare `agent-flow` PATH form for the same command, so the file is inconsistent with itself about how the binary is reached.

REPRODUCIBLE EVIDENCE. From an empty directory outside the repository, criterion 2 run exactly as printed:

```
$ ./target/debug/agent-flow validate --source docs/plans/TEMPLATE.plan.toml
bash: ./target/debug/agent-flow: No such file or directory
exit=127
```

The same command with an absolute path to the built binary produces the behaviour the step measures:

```
no metrics log at docs/metrics/workflow.jsonl; nothing to validate
no source plan at docs/plans/TEMPLATE.plan.toml; nothing to validate
exit=0
```

so the criterion's substance is sound and only its invocation is unrunnable. Criterion 2's pass condition is "the exit status is 1"; the verbatim run gives 127, which is neither the pre-change 0 nor the post-change 1, so the criterion cannot distinguish anything.

NOT FILED SEPARATELY, AND NAMED SO THE SCOPE IS NOT SILENT. The same shape occurs at `plan-order-array-position.md:113` and `:174-186`, whose fixtures are written to "a scratch directory OUTSIDE the repository" and then addressed by bare relative filenames, and at `step-intent-encoding.md:656-668`, which scaffolds into an empty directory and then invokes `./target/debug/agent-flow`. I file one finding rather than four because the correction is identical everywhere and a single stated convention closes all of them; the other three increments are named here so the fix is not scoped to this one by omission.

REQUIRED CORRECTION. State the convention once, in the shape the drift step now uses for H1 ("run it under bash FROM THE REPOSITORY ROOT with BOTH arguments absolute"): either name the binary by an absolute path bound in the outcome, or keep the working directory at the repository root and give the fixture an absolute path. Criterion 4's first command already shows the second form works, because `:75` pins its working directory to the repository root and every path in it resolves there.

---

# Part 4. Recorded, not filed

Kept so the boundary of this review is visible rather than implied.

- CRITERION 6 CARRIES NO ABSENT-INPUT CLAUSE. Its pass condition is "`checked` equals the worklist row count", which is satisfied by `checked=0` on an empty worklist. Every other counting oracle in this pass carries a greater-than-zero clause and says why (R1's `rows > 0` at `step-intent-encoding.md:382`, R3's `checked` clause at `:467`, L1's absent-ledger sentence at `ledger-order-citation-currency.md:125`). NOT FILED because reaching an empty worklist now requires disobeying criterion 2's explicit invocation, which the `F1` repair pins, so no implementation that follows the text can get there.
- THE HOW-TO-ADD-A-STEP SENTENCE LIVES INSIDE THE ANGLE-BRACKET NOTE. Measured: `pack/plan-template.steps/example-step.md` is three lines and the whole of its body is one `<...>` placeholder that carries the sentence `GB-5`'s repair corrects. NOT FILED as an `F2` re-raise: `F2` concerns a RULE that must survive into the adopter's own plan, whereas this sentence is operator guidance read while the template is still fresh, so the planner's deletion of the note does not defeat it. Recorded because the two sites are one edit apart and a reader may expect the `F2` boundary to cover both; it does not.
- THE LEDGER TOTALS HAVE MOVED FROM `135`/`116` TO `137`/`117` since the sidecar was authored, and the count of vacated-value rows from 12 to 14, the new rows arriving with the 2026-08-23 resume block. NOT FILED: `ledger-order-citation-currency.md:20` and `:24` both state in advance that these move and make neither a pass condition, so the movement is inside the recorded boundary and confirms the no-figure-as-a-pass-condition rule is holding.
- `decision-folder-currency.md`'s opening line is a THIRD line collision between `sidecar-status-opening-drift` and `plan-order-array-position` increment 2, against RULE 5's "THERE ARE TWO LINE COLLISIONS" at `plan-order-array-position.md:31`. The line is on the drift step's worklist and carries `step 89` in `drift.txt`. NOT FILED as a separate defect because the two edits touch different parts of the line exactly as RULE 5's first collision does, and RULE 5's operative instruction ("Whichever step runs second must leave the other's edit intact") covers it; what is wrong is only the enumeration's count. Recorded so the count is corrected when `C-2` is fixed, since the case-insensitive search adds a fourth site on the same line.

---

# Part 5. Per-increment count and severity ceiling

| Increment | Raw findings | Severity ceiling |
| --- | --- | --- |
| `sidecar-status-opening-drift-inc1` | 1 | `medium` |
| `ledger-order-citation-currency-inc1` | 1 | `medium` |
| `plan-order-array-position-inc1` | 0 | none |
| `plan-order-array-position-inc2` | 2 | `medium` |
| `step-intent-encoding-inc1` | 0 | none |
| `step-intent-encoding-inc2a` | 0 | none |
| `step-intent-encoding-inc2b` | 0 | none |
| `step-intent-encoding-inc2c` | 0 | none |
| `step-intent-encoding-inc2d` | 0 | none |
| `step-intent-encoding-inc2e` | 0 | none |
| `step-intent-encoding-inc2f` | 0 | none |
| `step-intent-encoding-inc3` | 1 | `medium` |
| `validate-missing-source-exit-inc1` | 1 | `low` |

RAW TOTAL 6. Self-classed CLASS 1 three (`C-1`, `C-2`, `C-3`) against a required zero; CLASS 2 three (`C-4`, `C-5`, `C-6`) against a permitted three, all `low` or `medium`. Severity ceiling `medium`. The distinct count and the classes are the triager's to set.
