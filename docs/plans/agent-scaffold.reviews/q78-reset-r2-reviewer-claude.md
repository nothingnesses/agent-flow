# Q-78 reset round 2, independent Claude reviewer: fix verification, adoption and executability

Reviewer file. Worktree `.agents/worktrees/q78-reset-r2-claude`, branch `review/q78-reset-r2-claude`. Product reviewed at `f5260c6`; the repair inspected as `47984a0..f5260c6`. Every product source named in the brief was read whole, not only as a diff.

THREE FINDINGS. Ceiling `medium`. Self-classed one class 1 and two class 2. The four round 1 corrections this pass owed all reproduce before the repair and all close after it.

## Method and evidence environment

Every toolchain command ran through the project's flake environment. `direnv` is not on `PATH` inside this isolated worktree, so the environment was materialised with `nix --extra-experimental-features 'nix-command flakes' print-dev-env` and sourced; it yields the same `cargo 1.98.0-nightly (a335d47ff 2026-06-26)` and `rustc 1.98.0-nightly (f46ec5218 2026-06-30)` the flake pins. `cargo build --offline` FAILS in a fresh worktree (`no matching package named clap found`, no vendored registry), so `./target/debug/agent-flow` was built with network access; it reports `agent-flow 0.0.4`.

`grep` in this shell is a function shimming to ugrep, so GNU grep was invoked by absolute path, `/nix/store/gn94gpcp5q08x4v6g8mvw8v4r65rcjzk-gnugrep-3.12/bin/grep`, wherever an escape, an ERE or an exit status mattered. `grep -c` exiting 1 on zero matches was read as data. Every `validate` result below pins its stdout line rather than its exit code, because `validate` exits 0 on an absent input until `validate-missing-source-exit` lands.

Every fixture lives under the authorised scratch directory `/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r2-claude`, in the subdirectories `d1/`, `l1/`, `p1/`, `r3/`, `wd/`, `pickaxe/` and `toml/`, all of which this review created and owns. Nothing was written inside the repository except this file. No wildcard deletion was used. Nothing was pushed. No reviewer or triager fixture directory from an earlier round was read: every reproduction below was rebuilt from the sidecar text.

## Part 1: fix verification, D1, D2, D3 and D5

Each was reproduced against the reviewed tree before the repaired clause was applied, then re-measured against the repaired clause. All four CLOSE.

### D1, the inert opening-additions filter. CLOSED.

REPRODUCED. The two filter forms were run over a synthetic word-diff porcelain fragment holding one `+++ b/x` header row and one `+authored words` row:

```
BRE (the superseded form)   grep -v '^\+\+\+'    warning: stray \ before +   0 rows, exit 1
ERE (the repaired form)     grep -vE '^\+\+\+'   +authored words             1 row,  exit 0
```

So the superseded filter removed the authored word along with the header and `added` could never rise, and the repaired filter at `sidecar-status-opening-drift.md:229` retains it.

VERIFIED AGAINST A REBUILT CRITERION 6. Criterion 6's script was saved verbatim from `:218-237` and run in a throwaway git repository holding one worklist-shaped sidecar, against the increment's base commit:

```
(i)  correct increment, token deletion only                     checked=1 bad_anchor=0 added=0
(ii) token deletion plus one silent paragraph rewrite below     OPENING ADDS WORDS demo
     the opening                                                +the implementer silently replaced.
                                                                checked=1 bad_anchor=0 added=1
```

The red control the correction required is present at `:241` and it names the ERE as load-carrying. The third clause of the round 1 correction, reconciling `:213`, is NOT discharged; see finding `C2-3`.

### D2, uppercase ledger citations. CLOSED.

REPRODUCED on `docs/plans/agent-scaffold.ledger.md` at `f5260c6`:

```
selector                    total   at or above 85
lower case only             137     117
[Oo]rder|[Ss]tep            155     131
capitalized only                     14
```

The 14 capitalized rows sit at ledger lines 339, 343 (twice), 363, 387, 933 (twice), 945, 1603, 1605, 1717 (twice) and 1733 (twice). Criterion 4's vacated-value search moves from 14 rows to 15 under the repaired selector, the extra row being `339:Step 91`, exactly as the round 1 triage measured.

VERIFIED. L1 was saved verbatim from `ledger-order-citation-currency.md:91-116` and run against three ledgers: the unedited file, a correct case-insensitive case-preserving additive annotation of every citation at or above 85 plus the two vacated values, and that annotation with one capitalized annotation stripped.

```
criterion 1 worklist rows                        131
before the edit        drifting=131 annotated=1   bare=130 unknown_slug=0 wrong_slug=0
correct additive edit  drifting=131 annotated=131 bare=0   unknown_slug=0 wrong_slug=0
capitalized red control drifting=131 annotated=130 bare=1  unknown_slug=0 wrong_slug=0
```

`drifting` equals criterion 1's captured row count on both edited trees, so the additive clause holds, and criterion 3's new capitalized red control produces exactly the one-row delta it specifies.

THE RED CONTROL IS LOAD-CARRYING, WHICH IS THE HALF THAT MATTERS. Run under the SUPERSEDED lower-case-only L1, the correct tree and the capitalized mutation print a byte-identical line:

```
drifting=117 annotated=117 bare=0 unknown_slug=0 wrong_slug=0    (correct tree)
drifting=117 annotated=117 bare=0 unknown_slug=0 wrong_slug=0    (capitalized citation left bare)
```

So the mutation is invisible to the old selector and visible to the new one, which is what the correction asked for.

CRITERION 4 IS SATISFIABLE, AND THAT WAS NOT PREVIOUSLY SHOWN. The criterion needs a named commit at which BOTH currently vacant values were assigned. Searching all 142 commits that touch `docs/plans/agent-scaffold.plan.toml`, two qualify, `d39964f` and `5fcd020`, and both resolve `84 rename-to-agent-flow` and `91 exploring-item-actor-boundary`, which are the two slugs `:24` names.

THE NEW DISPOSITION SENTENCE AT `:41` DESCRIBES A REAL POPULATION. Capitalized rows that already carry a bare slug exist and were read in context: `Step 91 exploring-item-actor-boundary` (line 339), `Step 92 prompt-drift-guard` (343), `Step 93 checks-runner-worktree-name-collision` (363), `Order 94 workflow-enforcement-tier` and `Order 86 code-value-audit-static` (933).

### D3, uppercase sidecar citations. CLOSED.

REPRODUCED over the stated source set (`docs/plans/agent-scaffold.steps/`, `agent-scaffold.success-criteria.md`, `agent-scaffold.documentation-protocol.md`, `agent-scaffold._status-narrative.md`):

```
selector                  pre   exempt   84   drift
lower case only            48       21     1      26
[Oo]rder|[Ss]tep           52       21     1      30
```

The four capitalized rows are `decision-folder-currency.md:3`, `:34` (both `Step 89`), `checks-runner-worktree-name-collision.md:90` (`Step 85`) and `workflow-enforcement-tier.md:308` (`Step 92`). All four are at or above 85 and all four were outside the superseded worklist.

VERIFIED ON A BUILT CORRECT IMPLEMENTATION. A copy of the sidecar tree and the three front sidecars took a slug restatement of all 30 drifting citations except the enumerated quotation row at `sidecar-status-opening-drift.md:105`, using the pre-deletion `order`-to-slug table. P1, saved verbatim from `plan-order-array-position.md:327-347`, prints:

```
NUMBER SURVIVES docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md:105 (was step 86)
rows=30 restated=29 wrong_slug=0 number_survives=1
```

which is the criterion's stated `rows=R restated=R-E wrong_slug=0 number_survives=E` for `R=30`, `E=1`. The `lines-pre.txt` diff prints nothing.

THE CAPITALIZED RED CONTROL AT `:385` IS LOAD-CARRYING. Restoring `Step 85` at `checks-runner-worktree-name-collision.md:90` on that correct tree gives, under the repaired selector, `NUMBER SURVIVES ... (was Step 85)` and a post sweep of 24 against the required 23. Under a lower-case-only pre-capture the same tree prints `rows=26 restated=25 wrong_slug=0 number_survives=1`, which is the correct-implementation line: the mutation is invisible.

### D5, the omitted 84 rows in the post sweep. CLOSED.

REPRODUCED. The 84 population is one row, `docs/plans/agent-scaffold.steps/ledger-order-citation-currency.md:24:order 84`. It is neither exempt nor drifting and it survives a correct implementation, so the superseded relation `post = exempt + enumerated NUMBER SURVIVES` demanded 22 where a correct tree gives 23.

VERIFIED. On the built correct implementation the repaired post sweep prints:

```
post=23 exempt_lost=0 eighty_four_lost=0
required: exempt(21) + eighty-four(1) + E(1) = 23
```

and the only post row outside `exempt.txt` and `eighty-four.txt` is the enumerated quotation row. Criterion 1 now captures `eighty-four.txt` (`:293`), the outcome records its `wc -l` (`:320`), the relation is restated as a disjoint union (`:320`), and `H` is defined and correctly excluded from P1's own input (`:377`).

## Part 2: divergences from the round 1 correction, judged

- D6 WAS REPAIRED THOUGH THE FIX BRIEF SAID DECISION 26 SUPERSEDED IT. `docs/plans/agent-scaffold.md` moved out of increment 3 criterion 9's must-appear set and into an explicit must-not-appear clause with the batches named as the producer of the final projection (`step-intent-encoding.md:769`), and criterion 11 gained `render --check --strict docs/plans/agent-scaffold.plan.toml` (`:777`). SOUND. Decision 26 does not in fact touch whether increment 3 alters the generated view, so the fix brief's supersession claim was the weaker reading; applying the round 1 triage's stated correction removes a contradiction that would otherwise have stood. The repair matches the correction clause for clause.
- D4 IS FULLY MOOT AND WAS DISPOSED OF BY REMOVAL RATHER THAN BY A GUARD. RULE 1 (`:27`) no longer prohibits `"""` or `'''` blocks and RULE 2 (`:29`) states positively that continuation escaping which collapses physical lines is valid, with `:77` recording that neither `\n` nor `\r` is an error and that no physical representation is inspected. SOUND, and it is the branch the round 1 triage offered as the alternative to a physical-representation guard.
- GB-11 WAS REPAIRED RATHER THAN ACCEPTED, per `Q-78-gb11-revision`. Both sites now read `<N> steps, <M> questions, valid` (`step-intent-encoding.md:162`, `plan-order-array-position.md:269`), so registering an eighty-first `[[question]]` no longer breaks either criterion. SOUND.
- D7 WAS NOT REPAIRED, as the fix brief directed. Criteria 2 to 5 of `validate-missing-source-exit.md` still invoke `./target/debug/agent-flow` from a directory outside the repository (`:54`, `:64`, `:80`, `:91`). NOT RE-RAISED: no evidence found in this round changes its class, severity or measured boundary, and the round 1 correction already folded the analogous invocations in the other sidecars into D7's own repair.
- THE ROUND 1 CORRECTION FOR D1 HAS THREE CLAUSES AND ONLY TWO ARE DISCHARGED. The reconciliation the correction demanded was written inside criterion 6 rather than in the paragraph it named. Filed as `C2-3`.

## Part 3: findings

### `C2-1`. R3's status-token arm anchors per LINE, so a correct paragraph value is refused

**Owning increment:** `step-intent-encoding-inc2a`. **Severity:** `medium`. **Candidate class:** class 2, third kind, a criterion that refuses a correct implementation.

WHAT IS VIOLATED. `step-intent-encoding.md:495` states, as the ground for criterion 6's status-token arm, "EVERY ARM IS ANCHORED ON THE START OF THE LOGICAL VALUE, AND THE ANCHOR IS THE SAME ONE `sidecar-status-opening-drift` USES." That sentence was changed by this repair, from "ANCHORED ON A SENTENCE BOUNDARY" to "ANCHORED ON THE START OF THE LOGICAL VALUE", in the same pass that made a logical value hold one or more paragraphs. It is false of a multi-paragraph value: the arm at `:485` is `printf '%s' "$value" | grep -qE '^(Not started|...)...'`, and `grep`'s `^` anchors at the start of every LINE, not at the start of the value. The pass condition at `:493` is `status_token=0`, so the false positive is a refusal. It also defeats rule 9's own scope at `:49`, which forbids only a value that OPENS with a status label.

REPRODUCED. The exact regex from `:485` was run against a two-paragraph value whose SECOND paragraph opens with a status label:

```
value:  The plan carries no field stating why a step exists.
        <blank>
        Next. A reader must open the sidecar to learn it.
result: FIRES
```

Then R3's body was rebuilt verbatim from `:468-490` (only the `status --step --json | jq` value source replaced by a file, since the subcommand does not exist yet) over a two-step fixture:

```
value written as TWO paragraphs   STATUS TOKEN alpha problem: ...   checked=4 duplicated=0 status_token=1
same prose joined into ONE        (no row)                          checked=4 duplicated=0 status_token=0
```

THE SAME PROSE PASSES AS ONE PARAGRAPH AND FAILS AS TWO. That is the shape that matters: the criterion's only visible remedy is to reshape a valid paragraph value into the single-paragraph form decision 26 removed, which is the outcome criterion 2 at `:361` was written to detect ("Also record how many selected values use more than one paragraph, so later batches are not silently pushed back toward the superseded one-sentence design").

A SECOND, SMALLER MANIFESTATION OF THE SAME ROOT CAUSE IS IN THE REPORT ITSELF. `:486` truncates with `cut -c1-40`, which is line-oriented, so a multi-paragraph hit prints one row PER LINE of the value, blank lines included, instead of the one `STATUS TOKEN <slug> <field>: <40 chars>` row the criterion describes. The output above shows three lines for one hit.

R3b INHERITS THE ANCHOR. Its two greps at `:508` and `:509` carry the identical `^`, so a value whose later paragraph begins with a status word plus a connective outside the closed list is printed as a complement row the outcome must dispose of, though it is not a rule 9 candidate at all.

WHY IT IS NOT CLASS 1. The defect is strictly over-selective on rule 9's target: no value that opens with a label escapes. Nothing wrong ships; a batch fails loudly.

SMALLEST REQUIRED CORRECTION. Anchor both arms on the first logical line rather than on every line, for example by testing `printf '%s' "$value" | head -1 | grep -qE ...` in R3 and in both R3b greps, and restate `:495` to say the anchor is the value's FIRST LINE. Change `cut -c1-40` to a first-line-then-truncate form so one hit stays one row. Add a red control: a value whose second paragraph opens `Next. ` must print `status_token=0`, and the same value with `Next. ` moved to the front must print `status_token=1`.

FAN-OUT NOTE, STATED SO IT IS NOT UNDER-COUNTED. The batch block states its criteria once and runs them once per batch (`:315`), so the identical defect text governs `step-intent-encoding-inc2b` through `-inc2f` as well. One repair closes all six. It is filed once, against the first batch, because there is one defective sentence and one correction; the triager owns whether to fan it out to six.

### `C2-2`. `next`'s human form is specified conditionally, so a single-paragraph value has two admissible shapes and no criterion separates them

**Owning increment:** `step-intent-encoding-inc1`. **Severity:** `low`. **Candidate class:** class 1, a wrong implementation passes while violating a numbered RULE.

WHAT IS VIOLATED. RULE 10 (`:53`) states the projection contract without a condition: "All human forms use deterministic labels and a quoted-line representation: each non-empty logical line is prefixed by `> `, each blank logical line by `>`". Increment 1's `next` paragraph (`:112`) states it WITH one: "In human output a multiline context slot is labelled on its own line and uses the same quoted-line helper, indented beneath the map key." For a single-paragraph value the two disagree. Under RULE 10 the slot must render as `    problem:` followed by `      > <value>`; under `:112`'s literal reading a single-line slot is not "multiline" and keeps `render_active_loop`'s existing `    problem: <value>` form (`src/next.rs:1220-1222`).

REPRODUCED BY CITATION, WHICH SETTLES IT WITHOUT A FIXTURE. No criterion in the step runs `next` on a single-paragraph value:

- Criterion 7 is the only criterion that runs `next` at all. `grep -n 'agent-flow next' docs/plans/agent-scaffold.steps/step-intent-encoding.md` returns one row, `:218`, inside criterion 7.
- Criterion 7's fixture is stated at `:215`: "Build a one-step in-progress plan whose `problem` and `approach` each have two paragraphs". Its human clause at `:225` reads only that two-paragraph range.
- `render --check --strict` is a byte compare over the rendered document and reaches no `next` output; the golden at `src/plan/render.rs:660` likewise.
- Increment 3 runs `status --step` (criterion 12) and never `next`.

So an implementation that emits the inline form for a single-paragraph slot passes criteria 7, 11, 12 and 13 and the whole suite, while RULE 10's "each non-empty logical line is prefixed by `> `" is false of it. RULE 10's own heading is "THE THREE PROJECTION FORMATS ARE FROZEN BEFORE THE LIVE PLAN GAINS ONE VALUE", and its stated reason is that the first implementer's choice otherwise becomes the standard, which is exactly what an unpinned case leaves open. The sibling surfaces do not carry the ambiguity: `status --step` is stated unconditionally at `:130` and its single-line case is pinned by criterion 8's `no-intent.plan.toml` five-line block at `:251`, and `render`'s single-paragraph case is pinned by criterion 6's `eta` range at `:207-213`.

SEVERITY. `low`. Both shapes are readable and the divergence is visible on the first run, but `next`'s human output is handed to an agent as an instruction rather than as a report, which is this increment's own stated blast-radius argument (`:61`), so a slot whose shape varies with the value's paragraph count is worth one clause to remove.

SMALLEST REQUIRED CORRECTION. Delete the word "multiline" at `:112` so every `problem` and `approach` context slot takes the label-on-its-own-line and quoted-line form regardless of paragraph count, matching RULE 10 and `status --step`. Add one clause to criterion 7: run the human form once against a SINGLE-paragraph pair and require `    problem:` on its own line followed by one `      > ` line.

### `C2-3`. The D1 repair falsified the accepted residual's own statement of what bounds it, and `:213` was not reconciled

**Owning increment:** `sidecar-status-opening-drift-inc1`. **Severity:** `low`. **Candidate class:** class 2. The triager owns the kind; it is a contract inconsistency inside the increment block rather than a criterion that admits or refuses an implementation.

WHAT IS VIOLATED. The round 1 triage's D1 correction has three clauses, and its third reads: "Reconcile `:213` with the implementation: either limit the word-diff to the opening or say clearly that the guard is stricter and scans the whole changed file." The repair took the second branch but wrote it at `:239`, inside criterion 6, and left `:213` unchanged. The two now contradict each other about the same criterion:

- `:239` (added by this repair): "The word-diff guard is deliberately stricter than the opening-only obligation: it scans the whole changed file and rejects any authored word, so criterion 5's loose numstat bound cannot hide an addition below the opening."
- `:213` (unchanged): "WHAT A WRONG IMPLEMENTATION COULD THEN SHIP: one silent, unrelated paragraph rewrite in each file on the worklist, in text `render` publishes into every reader's copy of the plan, THAT NO CRITERION OF THIS STEP READS. Criteria 1, 6, 10, 11 and 12 READ THE OPENING LINE ... WHAT BOUNDS IT: criterion 6 forbids additions IN THE OPENING ITSELF".

REPRODUCED. Criterion 6's script, saved verbatim from `:218-237`, was run in a throwaway git repository against exactly the wrong implementation `:213` describes, a correct token deletion plus one silent rewrite of a paragraph BELOW the opening:

```
correct increment (token deletion only)                       checked=1 bad_anchor=0 added=0
token deletion + one paragraph rewrite below the opening       OPENING ADDS WORDS demo
                                                               +the implementer silently replaced.
                                                               checked=1 bad_anchor=0 added=1
git diff --numstat                                             2  2   (inside criterion 5's bound)
```

So criterion 6 DOES read it, and the residual's stated cost, "that no criterion of this step reads", does not reproduce. This is new evidence rather than a re-raise of the accepted residual itself: the residual `Q-78-round4` was accepted on 2026-08-22 against a criterion 6 whose additions arm was inert, and this repair made that arm live, which moved the boundary the human weighed.

SMALLEST REQUIRED CORRECTION. Rewrite the two clauses of `:213` that name criterion 6: state that criterion 6's additions arm reads the WHOLE changed file, and narrow the residual's stated cost to what the numstat bound alone still admits, which is a pure DELETION below the opening line and an added line not balanced by a removed one, neither of which the word-diff arm reports. The accepted residual survives in that narrowed form; only its overstated half goes.

## Part 4: adoption boundaries checked

Each boundary the brief names, with what was measured.

| Boundary | Result |
| --- | --- |
| Existing projects can express paragraphs without source-format restrictions | HOLDS. All four RULE 2 source forms parse: multiline basic, escaped `\n\n` in a basic string, a continuation-escaped multiline basic, and a multiline literal. Each prints `1 steps, 0 questions, valid` and exits 0 on the current binary. |
| The optional migration phase remains parseable | HOLDS, same measurement, plus `deny_unknown_fields` is not reached because the fields land in the schema in increment 1. |
| The final required-field phase rejects absence and emptiness only | HOLDS. Increment 3 criterion 1's four greps and two parse checks separate the asymmetric and the defaulted builds; `:580` keeps only the empty-after-trim rejections; `:816` bars every content rule. |
| Human and JSON output contracts are unambiguous | FAILS for `next` on a single-paragraph value. Finding `C2-2`. JSON is unambiguous on all three surfaces. |
| Exact labels, indentation and blank lines agree across prose and criteria | HOLDS for `render` (`:79-95` against criteria 4, 5, 6) and for `status --step` (`:130-150` against criterion 8, including the five-line `(not recorded)` block). The `next` block at `:112-128` agrees with criterion 7 on the two-paragraph case only; see `C2-2`. |
| Render fixture work can implement the specified heading placement | HOLDS. `src/plan/testdata/render-fixture.steps/gamma.md` and `eta.md` both open with a `###` heading and the golden carries "The gamma step body" and "The eta step body", so both awk ranges in criteria 5 and 6 resolve. A first-line insertion puts the labels above the heading and leaves criterion 5's range showing the body straight after the heading, so the criterion does discriminate. |
| `next` human formatting does not corrupt unrelated context slots | HOLDS. `build_context` (`src/next.rs:993`) yields exactly the six slots `:112` names at `AwaitingFirstReview`, in the stated `BTreeMap` order, and the specified change touches only the `problem` and `approach` slots. |
| `status --step --json` composes with the current CLI `--json` contract | HOLDS as specified. Today `status --json` emits a `plan`/`questions`/`metrics` projection; `:144` states `--step --json` prints a DEDICATED object with `step`, `found`, `problem`, `approach`, and every consumer in the criteria (criterion 8, R1, R2, R3) reads that dedicated shape. The `--resume` conflict is real: clap 4 prints `error: the argument '--step <STEP>' cannot be used with '--resume'` and exits 2 for this argument order, verified against the live `scaffold --write --dry-run` conflict. |
| Unknown, absent and present intent states remain distinguishable | HOLDS. `found` separates unknown from known and `null` versus string separates absent from present; the human form separates them by `not in this plan` versus `  > (not recorded)`. |
| Multiline values survive every shell script in the batch criteria | HOLDS. Against a plan text carrying one two-paragraph step and one single-paragraph step, criterion 1's count prints `problem=2 approach=2` and its per-field identity awk yields `alpha beta` for both fields; R4's source counts print `steps=2 source=2/2`. The `$'\034'` sentinel in R2 and R3 preserves trailing newlines through command substitution. The one script that does NOT survive is R3's status-token arm; that is `C2-1`. |
| Earliest-commit searches and substring checks work for newline values | HOLDS, measured rather than assumed. In a throwaway repository, `git log --reverse --format=%H -S"$val"` with `$val` spanning a blank line returns the earliest commit, and `[[ "$blob" == *"$val"* ]]` on a `git show` blob captured through the sentinel matches. RULE 6's claim at `:41` reproduces. |
| No command substitution silently removes meaningful trailing newlines | HOLDS. R2 (`:431`, `:437`) and R3 (`:474`, `:479`) both append `\034` inside the substitution and strip it after, and `jq -j` is used rather than `jq -r`. |
| The rendered reconciliation reaches question, front and tail sidecars correctly | HOLDS. R4's eight named front and tail sidecars are exactly `[meta.sidecars].front` (seven) plus `tail`, and the question directory is included. There are 80 question sidecars for 80 `[[question]]` entries, so no orphan file can over-count. Measured today: `quoted_problem=1 quoted_approach=1 projected_problem=1 projected_approach=1`, so `projected - quoted = source = 0` holds on the pre-increment tree. |
| The pack and changelog impact remains scheduled in increment 3 | HOLDS. Three hand-edited pack pairs with a `cmp` each (criterion 5), the duty (g) sentence with two presence commands and a placement command (criterion 6), the how-to-add-a-step sentence checked on both sides of its pair, and `CHANGELOG.md` in criterion 9's set with the DOCUMENTATION IMPACT section owning it. `grep -n 'Unreleased' CHANGELOG.md` still exits 1, so the stated premise reproduces. |
| The changed-path sets permit every promised edit and forbid unrelated edits | HOLDS. Increment 1's eight paths cover the schema, the three projections, the fixture plan, the golden, `gamma.md` and the batch manifest, and criterion 13's four unit tests land in `src/plan/source.rs`, already in the set. Increment 3's set now carries `src/main.rs`, `render-fixture.md`, `TEMPLATE.md`, both documentation-protocol copies, both example-step copies, `CHANGELOG.md` and the two deletions, and excludes `docs/plans/agent-scaffold.md`. |
| The exploration and registered `Q-78` item reflect the human decision | HOLDS. `docs/plans/step-intent-encoding.explorations/Q-78.md:7`, `:9`, `:85`, `:91` and `:301` carry decision 26 and mark the earlier single-line recommendation and its physical-line cost rationale as superseded rather than deleting the history. `docs/plans/agent-scaffold.questions/Q-78.md` gained a three-paragraph body recording the decision, its fold into `step-intent-encoding`, what it does NOT supersede, and that `Q-78` stays `open`. |
| The intake and decision records match the presented options and choice | HOLDS. Both appended records are byte-identical to the fix brief's specified JSON, each occurs exactly once, and the decision receipt's `chosen` is a member of its `options`. `validate --metrics` reports `426 records, valid`. |

## Part 5: currency of the product

- NO LIVE DESIGN CLAUSE RESTORES THE SUPERSEDED DESIGN. A case-insensitive sweep for `one sentence`, `single line`, `one-line`, `sentence cap`, `character cap`, `line cap` and `physical line` over the five sidecars, the exploration and the question body returns only explicit negations (`step-intent-encoding.md:19`, `:23`, `:816`), RULE 2's permission list (`:29`), the exploration's marked-superseded history (`:9`, `:301`), and unrelated prose about file line counts. `one_line` survives only as the helper the design now REFUSES to use (`:95`).
- EVERY CITED FIGURE AND SELECTOR RE-MEASURED REPRODUCES: shortest sidecar 54 words (`file-dropper.md`); one sidecar with no leading heading (`core-assets.md`); 12 declaration-site files and 69 sites, matching the table at `:615-626` row for row; three `slug` sites in `src/plan/render.rs` with the `N1` fixture at `:877` first and `empty_details_sections_emit_no_bare_heading` at `:872`; 105 `[[step]]` entries, so RULE 3's `2 x $(grep -c ...)` is 210; six `step-intent-encoding-inc2` declarations against six manifest batches; `--help` prints 8 commands; `grep -n 'Unreleased' CHANGELOG.md` exits 1; no placeholder-rejection rule in `src/`; `GOLDEN` at `src/plan/render.rs:660` and its test at `:698`; `StatusArgs` at `src/main.rs:496`; the metrics-log form evidence at `ledger-order-citation-currency.md:43` prints 14 hits with 13 at or above 85 under both the old and the repaired selector; the 14-citation delta at `:20` is exactly `131 - 117`. All 13 increments are declared in the plan TOML.
- THE GENERATED PLAN IS A CURRENT PROJECTION. `render --check --strict docs/plans/agent-scaffold.plan.toml` prints `up to date` and exits 0.
- ASCII. `LC_ALL=C grep -cP '[^\t\x20-\x7e]'` prints `0` for all eight changed files.

## Part 6: settled items, not re-raised

`GB-4`, `GB-9`, `F2` and `F3` were read at their recorded homes (`step-intent-encoding.md:185`, `validate-missing-source-exit.md:118`, `step-intent-encoding.md:759`, `step-intent-encoding.md:793`). Each still carries its acceptance receipt and its non-expansion boundary, and none is re-raised; no evidence found in this round changes any of them. D7 is not re-raised. D6 is disposed of in Part 2 as a repaired divergence rather than as a finding.

## Part 7: recorded, not filed

Each carries its measurement so a triager can take it if it disagrees with my reason for leaving it.

- CRITERION 6's `checked` CLAUSE IS AN IDENTITY OF ITS OWN LOOP. `sidecar-status-opening-drift.md:239` requires `checked` to equal the worklist row count, and the loop increments `checked` once per line of `opening-anchors.tsv`, which criterion 2 generates one row per worklist slug. This is the same shape round 4 raised against P1's `rows` clause and the repair fixed in the sibling. NOT FILED: it is pre-existing, this repair did not touch it, and the reset round 1 triage did not reach it.
- A NON-WORD-ALIGNED DELETION FAILS CRITERION 6's ADDITIONS ARM. Measured: deleting a mid-sentence clause whose boundary strands a comma turns `rule,` into `rule.` and the word diff prints `+rule.`, so `added` rises on a deletion-only edit. NOT FILED as a refusal of a correct implementation, because I could not demonstrate that any file on the 17-slug worklist forces it. Both false-clause deletions the sidecar names, `decision-folder-currency.md:3`'s FOUR-passages clause and `planner-folds-decisions.md:3`'s three assertions, are removable at whole-word boundaries, and each was built and measured at `added=0`. Recorded because the correction for `C2-3` touches the same paragraph and could state the boundary while it is open.
- CRITERION 5's awk RANGE CANNOT SHOW THE LEAD-IN IT ASKS THE READER TO VERIFY. `step-intent-encoding.md:202` starts printing AT the `### \`gamma\`` heading, while `:205`'s pass condition includes "The lead-in sentence remains above the heading". NOT FILED: the discriminating half of the criterion, that a first-line insertion puts the labels above the heading, is fully carried by the printed range, and the lead-in half is a fixture the same criterion authors.
- THE `one of those records` FIGURE AT `ledger-order-citation-currency.md:43` UNDERSTATES. Measured, three `round` records in `docs/metrics/workflow.jsonl` carry the slug beside the number (lines 210, 211 and 217), not one. NOT FILED: the sentence sits above the increment block, in the FORM argument rather than in a criterion, a numbered rule or a risk-class ground, so the figure rule excludes it, and it understates rather than overstates its own evidence. This follows the round 4 triage's own ruling on the `docs/plans/TEMPLATE.md` "twice over" figure.
- EXECUTABILITY NOTE FOR A FUTURE IMPLEMENTATION WORKTREE, NOT A PRODUCT DEFECT. `direnv` is absent from `PATH` in an isolated worktree and `cargo build --offline` fails there for want of a vendored registry, so an implementer must either materialise the flake environment through `nix print-dev-env` or run with network access before any criterion that invokes `./target/debug/agent-flow` can run at all.

## Part 8: loop identity

| Increment | Findings | Severities | Class |
| --- | ---: | --- | --- |
| `sidecar-status-opening-drift-inc1` | 1 | `low` | 0 class 1 / 1 class 2 |
| `ledger-order-citation-currency-inc1` | 0 | none | none |
| `plan-order-array-position-inc1` | 0 | none | none |
| `plan-order-array-position-inc2` | 0 | none | none |
| `step-intent-encoding-inc1` | 1 | `low` | 1 class 1 / 0 class 2 |
| `step-intent-encoding-inc2a` | 1 | `medium` | 0 class 1 / 1 class 2 |
| `step-intent-encoding-inc2b` | 0 | none | none (see `C2-1`'s fan-out note) |
| `step-intent-encoding-inc2c` | 0 | none | none (see `C2-1`'s fan-out note) |
| `step-intent-encoding-inc2d` | 0 | none | none (see `C2-1`'s fan-out note) |
| `step-intent-encoding-inc2e` | 0 | none | none (see `C2-1`'s fan-out note) |
| `step-intent-encoding-inc2f` | 0 | none | none (see `C2-1`'s fan-out note) |
| `step-intent-encoding-inc3` | 0 | none | none |
| `validate-missing-source-exit-inc1` | 0 | none | none |

Self-classed totals: 3 findings, 1 class 1 and 2 class 2, ceiling `medium`. The triager sets the final class, the deduplicated count and each loop's outcome.

## Part 9: gates

All six run from this worktree through the flake environment.

| Gate | Result |
| --- | --- |
| `cargo test` | exit 0, 470 tests across 12 binaries, 0 failed |
| `cargo clippy --all-targets -- -D warnings` | exit 0 |
| `validate --source ... --metrics ...` | `docs/metrics/workflow.jsonl: 426 records, valid` and `docs/plans/agent-scaffold.plan.toml: 105 steps, 80 questions, valid`, exit 0 |
| `validate --source ... --workflow` | `docs/plans/agent-scaffold.plan.toml vs docs/metrics/workflow.jsonl: workflow invariants hold`, exit 0 |
| `render --check --strict <PLAN>` | `docs/plans/agent-scaffold.plan.toml: up to date`, exit 0 |
| `LC_ALL=C grep -cP '[^\t\x20-\x7e]'` over the eight changed files | `0` for every path |

## File safety

Every fixture built by this review lives under the authorised scratch directory named in the Method section, in `d1/`, `l1/`, `p1/` (with `work/` and `red/`), `r3/`, `wd/` (with two throwaway git repositories), `pickaxe/` and `toml/`, plus the build and gate logs. Nothing was written inside the repository other than this findings file. No product, plan, ledger, metrics, brief or existing review file was edited. No wildcard glob was used in any delete. Bare `/tmp` was never written to. Nothing was pushed. `git status --short` in this worktree reports only this file.
