# Triage: `Q-78` design pass, round 4 of the reset count

Triager file. Worktree `.claude/worktrees/q78-r8-triage`, branch `triage/q78-r8`. Written and committed verdict by verdict, so a context loss loses at most one verdict.

INPUTS. `q78-r8-reviewer-groundblind.md`, 11 findings, self-classed 6 class 1 and 5 class 2, ceiling `high`. `q78-r8-reviewer-fixverify.md`, 3 findings, self-classed 1 class 1 and 2 class 2, ceiling `medium`.

METHOD. Every testable claim was rebuilt from the sidecar text rather than copied from the reviewer's fixture directory, and a claim that did not reproduce was to be dismissed. No reviewer class was accepted without a reason of my own. Fixtures live under the session scratchpad in `triage-r8/`, a directory this triage created and owns.

MEASUREMENT HAZARDS HONOURED. `grep` in this shell is `ugrep`, so `/usr/bin/grep` is used by absolute path wherever an escape or a `-P` pattern matters. `grep -c` exits 1 on zero matches and that is the PASS case for a sweep. `validate` exits 0 on an absent input, so every `validate` result below pins its stdout line rather than its exit code.

---

# Verdicts, ground-blind lens

## `GB-1`. UPHELD. CLASS 1. Severity `high`.

REPRODUCED IN FULL, both falsifiers, rebuilt from the sidecar text.

The base measurements hold on this tree: criterion 1's anchored selector prints 36 rows, `H1` prints 19 handover rows, and `comm -23` leaves a 17-file worklist.

FALSIFIER ONE, the fabricating one. Each of the 17 worklist openings replaced by "This work was scheduled from an earlier review round and is recorded here.", the handover files untouched. Measured against the criteria run verbatim:

| Criterion | Result |
| --- | --- |
| 1, anchored selector then `comm -3` against `handover.txt` | 19 rows, `comm -3` prints NOTHING. PASSES |
| 4, `git diff --name-only` | exactly the 17 worklist files, no handover file. PASSES |
| 5, `git diff --numstat` | 1 added and 1 removed on every file, inside the 2-and-2 bound. PASSES |
| 10, keyword scan | ZERO rows. PASSES |
| 12, first-character test | ZERO rows. PASSES |
| 11, the reading | the fabricated sentence makes no claim about state, so no claim any declared `status` contradicts. PASSES |

THE "PASSES MORE CLEANLY" CLAIM ALSO REPRODUCES, and it is the part that makes this finding `high` rather than `medium`. The CORRECT implementation, the bare token deletion the sidecar specifies, prints NINE criterion 10 rows the implementer must then dispose of one by one: `agents-worktree-planner-scope`, `decision-folder-currency`, `decision-receipt`, `doc-currency-guidance`, `reviewer-diversity`, `reviewer-harness-field`, `round-log-core`, `state-queries` and `workflow-invariants`. The fabricating implementation prints zero. So the criteria do not merely fail to refuse the wrong implementation, they reward it.

FALSIFIER TWO, the destructive one, ALSO REPRODUCES, and my first build of it did not, which is worth recording. An implementation that deletes the whole opening line everywhere is caught, because on 8 of the 17 it leaves a non-prose opening. An implementation that probes first, deletes the whole line where criterion 12 stays silent and falls back to the specified bare strip elsewhere, is caught by NOTHING. Measured: it destroys the opening paragraph of exactly the nine files `GB-1` names, `checks-runner-worktree-name-collision`, `decision-folder-currency`, `human-input-gate-reinforce`, `planner-folds-decisions`, `prompt-drift-guard`, `review-mode`, `round-log-core`, `session-preflight` and `workflow-invariants`, each at 0 added and 1 removed, and criterion 1's `comm -3` prints 0 rows, criterion 12 prints 0 rows, criterion 4's changed set is IDENTICAL to the worklist, and no file exceeds criterion 5's bound. Nine paragraphs of design prose are deleted from the published plan and every criterion is green.

WHY CLASS 1. The increment block at `:37` states its ground as a premise and a consequence and asserts at `:43` that "BOTH HALVES ARE REFUSED BY CONSTRUCTION, AND BOTH CONSTRUCTIONS WERE BUILT AND RUN". That assertion is false. The construction that was built rewrites all 36 selected openings and so destroys the 19 handover rows criterion 1 requires; confining the same rewrite to the 17 worklist files leaves those rows untouched and no criterion sees it. A wrong implementation passes while violating the increment's own stated risk ground, which is the class 1 definition exactly.

IT ALSO VIOLATES, independently: `Q-78-statusform`, the human decision at `:13` that chose DELETE over replace, whose accepted reasoning cites Principle 8 and Principle 1 by name; and the NOT IN SCOPE bullet at `:110`, "It does not review, re-scope, re-title or rewrite a single step."

WHERE I DISAGREE WITH THE REVIEWER'S ARGUMENT. `GB-1` presents the second falsifier as passing "criteria 1, 5 and 12 with the same zero output as the correct implementation". The variant that only deletes, with no fallback, does NOT: it leaves 8 files carrying their token and criterion 1 prints 8 surplus rows. The falsifier has to pair the whole-line deletion with the specified strip on the other 8 to go undetected. The finding stands on the rebuilt form.

## `GB-2`. UPHELD, AND ITS CLASS IS RAISED. CLASS 1, not the reviewer's class 2. Severity `high`.

THE CORE MEASUREMENT REPRODUCES EXACTLY.

- The resolution-table `awk` against the committed plan prints `105` rows.
- Against a copy with every `^order = ` line removed, which is what increment 1 leaves behind and what increment 1 criterion 1 (`:115`) requires, it prints `0`.
- `plan-order-array-position-inc1` and `-inc2` are declared in that order under one step in `docs/plans/agent-scaffold.plan.toml:1563` and `:1567`, and increment 2 exists only because increment 1 deleted the field, so increment 2 cannot run on a tree that still carries `order`.

THE CONSEQUENCE FOR CRITERION 2 REPRODUCES, on a fixture holding one correctly restated drifting citation:

```
rows=1 restated=1 wrong_slug=0 number_survives=0        # table built before the deletion
WRONG SLUG f.md:2 (was step 86) wants ``
rows=1 restated=0 wrong_slug=1 number_survives=0        # table built after increment 1, the real tree
```

So criterion 2's `wrong_slug=0` clause and its `restated` clause both refuse a correct implementation, on every row, on the only tree the increment can run on. That is the class 2 third kind, and the reviewer stopped there.

I WENT FURTHER, AND THE FINDING IS WORSE THAN CLASSED. The specification gives the implementer no runnable table source, so the implementer must invent one. The obvious substitute on a post-deletion tree is the array position the step has just made authoritative. MEASURED, the order-value table and the declaration-position table DISAGREE ON FOURTEEN ROWS, every value from 92 to 105, because 84 and 91 are vacant and two values run past 105:

```
92  prompt-drift-guard          vs  checks-runner-worktree-name-collision
95  test-tmpdir-repo-assumption vs  status-resume-ignores-json
100 rename-to-agent-flow        vs  user-prompts-pointer-and-drift-coverage
105 plan-order-array-position   vs  step-intent-encoding
```

MEASURED, a citation reading `step 95` restated to `status-resume-ignores-json`, which is the WRONG step, and judged against the position-derived table the implementer had to invent, prints:

```
rows=1 restated=1 wrong_slug=0 number_survives=0
```

It PASSES. P1 checks the implementation against whatever table the implementer built, so it cannot separate a right substitution from a wrong one, and the same fixture judged against the true pre-deletion table prints `WRONG SLUG ... wants `test-tmpdir-repo-assumption``.

WHY THAT MAKES IT CLASS 1. A wrong implementation passes while violating increment 2's own stated risk ground at `:267`, "a missed site leaves a citation that resolves to nothing, or worse, to the wrong step, which is the same class of miss that produced the drift this step exists to remove". The criterion's own text at `:371` says "THE WRONG-SLUG CASE IS WHY THE RESOLUTION TABLE EXISTS", and the table is the half that does not survive the increment it runs after. It also violates Principle 7, Reproducible, cited by name by the sibling sidecar for this exact trap.

THE SIBLING'S RULE IS CONFIRMED VERBATIM. `ledger-order-citation-currency.md:60` reads "THE RESOLUTION TABLE IS BUILT FROM A NAMED COMMIT, NOT FROM THE WORKING TREE, so the increment is reproducible whether it runs before or after `plan-order-array-position` deletes the field (Principle 7, Reproducible)", and `:5` records that the human removed the blocking edge partly because "the resolution table below reads the working tree directly while `order` is present and needs `git show` once the field is gone". The trap was identified, named and solved in the sibling, and the sibling's own text says the sibling step may run either side of the deletion. `plan-order-array-position` increment 2 has no such freedom, it always runs after, and it carries the unqualified working-tree form.

COUNTED ONCE, AS CLASS 1. It is class 2 third kind as well, and I count the more severe limb rather than both.

## `GB-3`. UPHELD. CLASS 2, a criterion that refuses a correct implementation. Severity `medium`.

EVERY LINK IN THE CHAIN REPRODUCES.

- `src/plan/testdata/render-fixture.plan.toml` holds SEVEN `slug` sites, and it is one of the 12 declaration-site files criterion 2 requires to carry both fields. Its seven steps are `alpha`, `beta`, `gamma`, `delta`, `zeta`, `epsilon` and `eta`.
- Increment 1 criterion 4 (`:170`) gives `alpha` both fields, `gamma` both, and `eta` `problem` ALONE. So `beta`, `delta`, `zeta` and `epsilon` carry nothing after increment 1.
- Increment 1's `render` rule emits a `- problem:` line and an `- approach:` line immediately after the leading heading line for a step carrying a field.
- Increment 3 criterion 2 requires all 69 sites to carry BOTH fields, so four steps gain two projected lines each and `eta` gains one. The golden MUST change.
- `src/plan/render.rs:660` holds `const GOLDEN: &str = include_str!("testdata/render-fixture.md");` and `render_is_deterministic_and_matches_the_golden` (`:698`) asserts `first == GOLDEN`. Increment 3 criterion 11 requires `cargo test` to pass.
- Increment 3 criterion 9's enumeration does NOT name `src/plan/testdata/render-fixture.md`, and `:721` states the enumeration is exact: "an implementer who made any of those edits FAILED it, and one who obeyed it shipped the defect instead."

SO NO IMPLEMENTATION SATISFIES BOTH CRITERION 9 AND CRITERION 11. That is the class 2 third kind exactly.

THE SIDECAR KNOWS THE RULE AND APPLIES IT TWICE ELSEWHERE. `step-intent-encoding`'s OWN increment 1 puts `src/plan/testdata/render-fixture.md` in its changed-path set, at `:135` and again in criterion 11 at `:265`. The sibling does the same, at `plan-order-array-position.md:245`. Increment 3 is the one place the file is dropped.

SEVERITY `medium` IS RIGHT AND I CHECKED THE CASE FOR RAISING IT. The contradiction fails loudly: an implementer meets either a red `cargo test` or a path-set mismatch at build time, so nothing wrong ships silently. It is `medium` rather than `low` because criterion 9 is written as an exact enumeration whose own paragraph tells the implementer that obeying it ships a defect, so the implementer has no way to resolve the conflict from the text.

## `GB-4`. UPHELD. CLASS 1. Severity `low`.

REPRODUCED BY EXHAUSTIVE SEARCH OF THE SIDECAR RATHER THAN BY BUILDING THE BINARY, which is the right instrument here because the claim is about what the criteria REACH.

- RULE 3 (`:33`) states the premise: "`validate` therefore rejects a value that is empty after a trim." The `validate` block at `:69` repeats it: "An empty-after-trim value gives".
- The consequence, also `:33`: "with this rule, an empty backfill over the whole plan prints TWO PROBLEMS PER STEP and exits 1".
- Increment 1 criterion 3 (`:161`) supplies `problem = ""` and `approach = ""`, and its whole-plan measurement at `:168` is the same literal repeated.
- MEASURED, `/usr/bin/grep -nP '(problem|approach)\s*=\s*"[ \t]+"'` over the whole sidecar exits 1: NO whitespace-only field value appears anywhere in the file. The only field assignments of an empty value are the two at `:161` and `:168`, both the literal `""`.
- Criterion 13 names `validate_rejects_an_empty_problem` and `validate_rejects_an_empty_approach` and says each "builds a one-step plan carrying the defect its name states". "Empty" written as `""` passes on an untrimmed implementation.
- Criterion 13's RED measurement DELETES the check outright, so both tests fail under the deletion whether the check trims or not. The RED half does not separate the two implementations either.

So `value.is_empty()` falsifies RULE 3's premise while every criterion that exercises the rule stays green. A numbered RULE is class 1 material under the stop condition, and RULE 3 is numbered.

SEVERITY `low` UPHELD, and the reviewer's ground for it is sound. RESIDUAL 2 (`:751`) already concedes that "The required field makes ABSENCE unrepresentable and leaves MEANINGLESSNESS fully representable", so what a trim buys over `is_empty()` is one character of shortcut, not a class of defect.

## `GB-5`. UPHELD. CLASS 1. Severity `medium`.

REPRODUCED. `/usr/bin/grep -n 'example-step'` over the sidecar returns `:538`, `:558`, `:560`, `:564`, `:566`, `:688`, `:719`, `:721` and `:741`. The reviewer's list omits `:560`, which is prose like the rest, so the substance is unchanged. Only `:688` is a command, and it is criterion 5's third `cmp`, which compares the pack source against its committed copy. NOTHING READS THE SENTENCE.

THE WRONG IMPLEMENTATION PASSES, checked criterion by criterion against a sentence corrected to name `problem` alone.

- CRITERION 5's third `cmp`: both sides of the pair carry the same bytes, so it passes on any content whatever.
- CRITERION 9: both paths appear in `git diff --name-only`. The increment says so itself at `:691`, criterion 9 "names the paths and proves nothing about their content".
- CRITERION 4: MEASURED, its two strings are `- problem: <the problem this step addresses>` and `- approach: <how this step addresses it>` over `docs/plans/TEMPLATE.md`. Those are the PROJECTED field lines rendered from `plan-template.plan.toml`, not this sidecar body's prose, so criterion 4 cannot see the sentence.
- CRITERION 3: a fresh scaffold validates, because the placeholder values come from `plan-template.plan.toml`.

WHAT IT VIOLATES. `:558` states the ground and cites the Principle by name: "Shipping that instruction to every scaffolded project is what Principle 3, Safe on existing projects, is cited to prevent in this increment's own cost paragraph, and every criterion below would otherwise pass over it." The last clause is still true. A wrong implementation passes while violating a cited Principle, which is class 1.

THE ASYMMETRY IS INSIDE ONE INCREMENT AND IT IS STARK, confirmed by reading all three:

| What ships | Its guard |
| --- | --- |
| The two placeholder values | criterion 4, TWO commands, one per field, with the reason stated |
| The documentation-protocol sentence | criterion 6, TWO presence commands PLUS a placement command, with the reason stated |
| The how-to-add-a-step sentence, which the flip turns into a recipe for a plan that does not parse | a `cmp` that compares it against a copy of itself, and a path name |

## `GB-6`. UPHELD. CLASS 1. Severity `medium`.

THE SUBSTANCE REPRODUCES, THOUGH THE REVIEWER'S QUOTED COMMAND DOES NOT, AND I RECORD BOTH.

`GB-6` writes that `grep -n 'status and order' docs/plans/agent-scaffold.steps/plan-order-array-position.md` returns `:80`, `:259`, `:383` and `:403`. MEASURED, that command returns TWO rows, `:80` and `:383`, under `/usr/bin/grep` and under ugrep alike. The four rows come from `grep -n 'and order'`, the shorter string. The reviewer transposed the two search strings. The claim the rows support is unaffected: `:80` is the only occurrence of the shipped clause in the sidecar, and it sits in the WHAT CHANGES prose.

THE LOAD-CARRYING CLAIMS ALL HOLD.

- The clause ships in three files today. `/usr/bin/grep -rln 'entries with status and order' pack/ AGENTS.md .agents/` returns exactly `pack/AGENTS.md`, `AGENTS.md` and `.agents/AGENTS.reference.md`, so the command reproduces.
- It is stated at `:80` as a BEFORE measurement, "MEASURED OVER THE SHIPPED SURFACES, ... returns exactly those three paths", and NEVER as an after-condition. Criterion 1's own four commands each carry a stated post-change value; this one does not.
- Criterion 8 is a path-name enumeration and nothing else.
- Criterion 1's four commands are anchored on a TOML assignment, on `.order` in `src/`, and on `slug, status, order` in `src/plan/render.rs`. None reaches pack prose, and `:78` says so: "The sentence below is PROSE, so no anchored search reaches it".
- The drift test exists and pins the pair. `the_committed_scaffold_matches_a_fresh_render` is at `src/agents_md_drift.rs:377`, and `pack/pack.toml:28-31` and `:99-103` map `AGENTS.md` to both destinations with `render = true`. So an implementer who edits `pack/AGENTS.md` ANYWHERE and re-renders gets all three paths into the diff and a green suite.

WHAT IT VIOLATES. `:83` states the ground: "An implementation that satisfies every other criterion here ships, to every one of those projects, the instruction to write the field that now makes the plan fail to parse: the criteria would be blind to the consequence their own risk ground names." That is the increment's own stated risk ground, and the criteria are still blind to it. CLASS 1.

THE REPAIR IS ONE LINE, and the increment already wrote the command.

## `GB-7`. UPHELD. CLASS 1. Severity `medium`. THE MODEL SIDECAR IS BROKEN, AND THE RULING ON WHAT THAT MEANS IS BELOW.

CRITERION 4'S TWELVE ROWS REPRODUCE. Its command prints exactly 12 rows, splitting 7 reading `84` and 5 reading `91`, at ledger lines 341 (twice), 347, 749 (twice), 1309, 1383, 1537, 1587, 1589, 1601 and 1605.

I READ ALL TWELVE IN CONTEXT RATHER THAN TAKING THE REVIEWER'S SUMMARY. Every one is a fourth kind the trichotomy does not name.

- THE SEVEN `84` ROWS all cite `rename-to-agent-flow` at the order it then held. Line 749 says it outright: "The planner also moved `rename-to-agent-flow` from order 84 to 100 and set `blocked_by = [\"audit-user-prompt\"]`, because decision 2 orders the prompt before the rename and order 84 said the opposite." Line 1309 reads "`rename-to-agent-flow` itself (order 84, `deferred`, `blocked_by = []`)". Lines 1383 and 1601 read "THEN the rename, step 84 `rename-to-agent-flow`". Lines 1587 and 1589 read "THEN the rename, step 84" and "then the rename (step 84)". Verified against the source: `rename-to-agent-flow` holds `order = 100` today.
- THE FIVE `91` ROWS all cite a step that existed at order 91 and was deleted. Line 341: "step 90 owns branch 2 and step 91 owns branch 3". Line 347: "step 91 REMOVED (committed deletion) because its content implemented an undecided choice". Line 1537: "step 91 built on those options had to be DELETED". Line 1605: "nothing would have caught an orphan left by step 91's removal".

NONE is a rendered position, NONE is a false positive of the search, and NONE is a mistake in the original entry. Every one was correct on the day it was written.

THE WRONG IMPLEMENTATION PASSES, AND I RAN IT RATHER THAN REASONING ABOUT IT. `L1` was rebuilt verbatim from `:83-105` and run against a fixture holding two ordinary drifting citations correctly annotated plus all twelve absent-value rows given the forced `(no such step)` disposition:

```
drifting=7 annotated=2 bare=5 unknown_slug=0 wrong_slug=0
```

`bare=5` is exactly what criterion 2's fourth clause requires, because criterion 4's twelve rows split 7 and 5 and only the five at or above 85 can contribute. Criterion 4's obligation is discharged, because every row carries one of the three. Confirmed mechanically: `(no such step)` does not match L1's `annotated` regex ``\b(order|step) [0-9]+ \(`[a-z0-9-]+`\)``, and a row reading `84` never enters `drifting` at all, which criterion 2's own fourth clause states in its own words.

I FOUND IT WORSE THAN THE REVIEWER DID. Running the SAME fixture with the twelve rows left completely BARE, no disposition made at all, prints the IDENTICAL line:

```
drifting=7 annotated=2 bare=5 unknown_slug=0 wrong_slug=0
```

So criterion 2 is not merely neutral on WHICH disposition is chosen, it is blind to whether one was made. The whole of criterion 4's obligation rests on the outcome's prose, and criterion 4 offers that prose no true option.

WHAT IT VIOLATES. Principle 6, Ground decisions in evidence, cited by this step at `:11` and again at `:43`, where the sentence is exactly on point: "the evidence must survive the correction that makes it readable." Annotating twelve historically correct citations `(no such step)` writes a false statement into the artefact `:54` calls the one "that every convergence count, every round total and every re-raise ruling in this project reads", and makes twelve citations permanently unfollowable while recording that there was never anything to follow. It also defeats the step's own APPROACH at `:9`, "Resolve each citation to the slug it always meant". A wrong implementation passes while violating a cited Principle. CLASS 1.

THE DEEPER REASON, WHICH THE REVIEWER FILES AS NOT BEARING AND WHICH I THINK IS THE HEART OF IT. The step's whole safety argument is the append-only measurement at `:26` and `:37`: "an `order` value, once assigned, kept its slug", so "a resolution taken from today's plan is the resolution the entry meant". That argument is TRUE for the range it measures and FALSE for `84`, which `rename-to-agent-flow` vacated, and the four-date `awk` cannot see the falsification because it filters `>=85`. Criterion 4 is the one place in the step where the central measured ground does not apply, and it is the place whose rows were never measured. The reviewer is right that nothing downstream is affected, because the drifting set is `>=85`; the reviewer is wrong to file it as separate from `GB-7`, because it is the same defect seen from the other end.

---

### RULING: is `ledger-order-citation-currency.md` still the model?

THE ORCHESTRATOR'S STATED GROUND HOLDS. I re-ran every figure the sidecar states, and every one reproduces on this tree:

| Figure | Stated | Measured |
| --- | --- | --- |
| ledger citations, total and drifting (`:20`) | `135`, `116` | `135`, `116` |
| citations at or below 83 (`:22`) | `12` | `12` |
| the 84/91 split (`:24`) | `7` and `5` | `7` and `5` |
| dedup surplus (`:74`) | `20` | `116` against `96`, surplus `20` |
| busiest line (`:74`) | 8 drifting citations across four values, three of them repeats of one | line 1701, values 86, 87, 88, 89, with 87 appearing three times |
| pre-existing annotation (`:119`) | `annotated=1` | one, `` step 88 (`reviewer-reproducible-evidence`) `` at line 1701 |
| append-only, four dates (`:37`) | `8/8`, `11/11`, `12/12`, `18/18` | `8/8`, `11/11`, `12/12`, `18/18` |

SO THE FRAMING'S GROUND WAS TRUE AND ITS CONCLUSION WAS NOT. "Every figure it stated reproduced" is a claim about FIGURE CURRENCY. "It is the model the other four are measured against" is a claim about CRITERION SOUNDNESS. They are different properties and the first does not imply the second: a sidecar can state nothing but reproducing figures and still carry a criterion set that admits a wrong implementation, which is precisely what `GB-7` demonstrates.

WHAT THE LEDGER MUST RECORD, stated so the entry is accurate rather than merely self-critical. The orchestrator did not state a false figure. It drew an unsupported inference from a true measurement, and it carried that inference into three briefs. The correction is to the inference.

THE MODEL FRAMING SURVIVES ON THE THREE RULES IT WAS ACTUALLY USED FOR, and this matters because `GB-2` rests on one of them. `GB-7` reaches criterion 4's disposition trichotomy. It does not touch the named-commit resolution table (`:60`), the no-figure-as-a-pass-condition rule (`:20`, `:78`), or the no-`sort -u` rule (`:74`). All three still hold in this sidecar and all three are still the right measure for the other four. What must stop is the blanket claim.

## `GB-8`. UPHELD, AND ITS CLASS IS LOWERED. CLASS 2, second-guard hole, not the reviewer's class 1. Severity `medium`.

THE MEASUREMENT REPRODUCES. A `tests/validate_refuses_a_missing_explicit_path.rs` holding five correctly named tests whose bodies are `assert!(true)` gives `/usr/bin/grep -c 'fn missing_.*_path'` stdout `5` and exit 0, which is the WHOLE of criterion 8's pass condition. `cargo test` passes on such a file by construction.

THE ASYMMETRY REPRODUCES. `/usr/bin/grep -n 'RED'` over `validate-missing-source-exit.md` returns `:49` only, and `:49` is criterion 1's RED CONTROL, a before-the-change exit-code capture, not a red measurement over the tests. The two siblings both carry one, and both carry the identical framing sentence: `plan-order-array-position.md:194` and `:212`, and `step-intent-encoding.md:273` and `:281`. Criterion 8 has the grep and nothing else.

WHY I LOWER THE CLASS. Class 1 requires a wrong implementation to pass while violating a stated risk ground, a numbered RULE or a cited Principle. Applying that test strictly:

- The increment's stated risk ground (`:33`) is the exit-code flip reaching every scaffolded project on upgrade. Five stub tests do not falsify it. The reviewer concedes this in its own words: "The exit-code repair itself is pinned by criteria 2 to 5 at build time, so the increment lands correctly."
- The step declares no numbered RULEs.
- The Principles it cites, 1 at `:17`, 3 at `:19`, 5 at `:21` and 6 at `:29`, are all about the shipped behaviour, which is correct on this implementation.

What IS defeated is criterion 8's own stated purpose, which is to carry criteria 4 and 5's refusal into the suite so it survives increment 3's rewrite. That is a guard behind a guard, and its pass condition has a hole. That is the class 2 first kind by definition. The reviewer's own strongest sentence describes a FUTURE regression passing, not this increment's implementation passing, and durability against a future regression is exactly what "second guard" names.

I KEEP `medium`. Nothing wrong ships from this increment, which argues for `low`, and both siblings closed the identical hole in themselves after the same analysis, which makes the omission a real and avoidable inconsistency rather than an oversight of a rule nobody had stated.

## `GB-9`. UPHELD ON A REBUILT FALSIFIER. ITS STATED FALSIFIER DOES NOT REPRODUCE, and I record that. CLASS 2, second-guard hole. Severity `low`.

THE MECHANICAL CORE REPRODUCES. `grep -c` counts LINES containing the string, not occurrences: `printf 'a must exist b must exist c\nmust exist\n' | /usr/bin/grep -c -F -- 'must exist'` prints `2` against three occurrences. So the criterion cannot attribute a hit to a flag. The bound is "at least `3`", which is looser again. The unchanged state is detected: today's binary prints `0`.

THE REVIEWER'S FALSIFIER FAILS ITS OWN CRITERION. `GB-9` writes that "An implementation that writes 'must exist' three times inside the `--source` help alone ... prints `3`". MEASURED, `validate --help` renders each flag's help as ONE unwrapped line, so three occurrences inside `--source` sit on one line and `grep -c` prints `1`. That implementation FAILS the criterion. The reviewer's own construction does not reproduce.

THE REBUILT FALSIFIER WORKS AND IS WORSE. `validate --help` is 11 lines, one per flag plus the about and the usage. Put "must exist" on the about line, the `--plan` line and the `--source` line, and the command prints `3` and PASSES, while `--metrics` documents nothing. MEASURED on a fixture of that shape: `3`. `--metrics` is the one flag whose behaviour SPLITS, and `:35` says so in the increment's own words: "the current `--metrics` help documents the defaulting rule and now has to document the split". So the falsifier that passes is the one that leaves undocumented exactly the flag the increment says most needs documenting.

WHY CLASS 2 AND `low`. Criterion 9 is a documentation guard behind the behavioural criteria, and it has a hole, which is the second-guard shape. `low` is right: the shipped behaviour is unaffected and the cost is a help text that is short on one flag.

THE STEP FOLDS ITS FLAGS TOGETHER HERE AND NOWHERE ELSE, confirmed: criterion 3 (`:67`) is run separately with the reason stated, criterion 4 (`:69`) separately, criterion 8 (`:100`) "FIVE TESTS, because five branches."

## `GB-10`. UPHELD, WITH ITS MECHANISM CORRECTED. CLASS 2. Severity `medium`.

THE ARITHMETIC REPRODUCES EXACTLY, run from the sidecar's own rule:

```
steps=101 batches=6 size=17 last_batch=16 coverage=102
steps=105 batches=6 size=18 last_batch=15 coverage=108
steps=110 batches=6 size=19 last_batch=15 coverage=114
steps=120 batches=6 size=20 last_batch=20 coverage=120
```

K IS 6 FOR EVERY N FROM 101 TO 120 AND S MOVES FROM 17 TO 20 INSIDE THAT RANGE. The only guard is on K: `grep -c 'id = "step-intent-encoding-inc2'` prints `6` and the `batches` field must equal `6`, MEASURED, it does. So the guard cannot fire in the range it covers, and the quantity that moves is unguarded. Today's plan is at 105 steps, and this pass still owes the drift step's successor (`sidecar-status-opening-drift.md:116`, "a planner's to author"), so N moves before batch a runs.

THE INTERNAL CONTRADICTION IS REAL. The criterion says "The batch letter and its slug list come from increment 1 criterion 10", which CAPTURES them, and then supplies a command that RE-DERIVES them from the live plan. The two agree only while N is unchanged.

I CORRECT THE REVIEWER ON WHICH READING BREAKS WHICH WAY, because I simulated both cumulatively and the finding's stated mechanism holds in only one direction.

- N SHRINKS, `$S` recomputed. Batches a and b ran at N=110 with S=19 and filled 1-38; a step is deleted, N=105 and S=18, and batch c's re-derived `declared.txt` is 37-54. MEASURED: `declared=18 gained=16 outside=0 missing=2`. A CORRECT batch c is REFUSED, on both field rows. This is the reviewer's stated mechanism and it reproduces.
- N GROWS, `$S` recomputed. Batches at S=18, then 19, then 20 give declared sets 1-18, 20-38, 41-60. MEASURED: `declared=20 gained=20 outside=0 missing=0`, so batch c PASSES, while positions 19, 39 and 40 sit in NO batch. This is a SILENT COVERAGE HOLE, not a refusal, and growth is the likely direction.
- N GROWS, `$S` held at the captured value. Six batches cover `K*S` = 108 positions of 110, so two steps fall outside every batch, and nothing reads them until increment 3 criterion 8 six increments later, whose `source` equals `steps` clause fails with no indication which batch owed the remainder.

`GB-10` states the refusal as following from the partition shifting "under the batches already done" when the plan GROWS. It does not: growth moves the boundaries later and opens gaps. The refusal needs N to shrink. Both consequences are real and both are class 2, one as a criterion that refuses a correct implementation and one as a hole in the per-batch identity guard, so the class is unaffected and `medium` stands.

## `GB-11`. UPHELD. CLASS 2, a criterion that refuses a correct implementation. Severity `low`.

REPRODUCED. `plan-order-array-position.md:261` and `step-intent-encoding.md:141` both state the pass condition as `<N> steps, 80 questions, valid`: a placeholder for the step count and a literal for the question count, in one sentence.

THE FIGURE REPRODUCES TODAY, so this is correctly NOT a non-reproducing-figure finding. MEASURED, `/usr/bin/grep -c '^\[\[question\]\]'` prints `80`, and the gates print `docs/plans/agent-scaffold.plan.toml: 105 steps, 80 questions, valid`.

IT IS NEARER THAN "LATENT" SUGGESTS, and this is where I go further than the reviewer. It becomes a refusal on the first `[[question]]` the plan gains, and THIS TRIAGE'S OWN ROUTED LIST ALREADY OWES ONE: the routed-decision-tracking defect carried forward from round 3 has no `[[question]]`, and registering it takes the count to 81 and breaks both criteria the same day. The defect is not waiting on a hypothetical future edit, it is waiting on an action this loop already owes.

THE RULE IT BREAKS IS ONE BOTH FILES ADOPT FOR THE OTHER HALF OF THE SAME LINE. `plan-order-array-position.md:3` and `step-intent-encoding.md:3` carry the identical sentence about the step count, and `ledger-order-citation-currency.md:20` states the general form: "no criterion below states either figure as a pass condition."

`low` is right. The repair is two characters in each file and nothing wrong can ship from it.

---

# Verdicts, fix-verification lens

## `F1`. UPHELD. CLASS 1. Severity `medium`.

BOTH MODES REPRODUCE EXACTLY, with `H1` saved verbatim from `:176-192` and run twice.

```
MODE A, run from the repository root as :173 directs, anchored.txt in the scratch directory
  exit=0   handover.txt rows = 0
  stderr:  cut: anchored.txt: No such file or directory   (twice)

MODE B, run from the scratch directory where anchored.txt lives
  exit=0   handover.txt rows = 36, every row a slug with an EMPTY second column
  stderr:  cp: cannot stat 'docs/plans/agent-scaffold.steps': No such file or directory
```

Confirmed that `anchored.txt` is NOT at the repository root, because criterion 2 at `:167` sends the three captures "to a scratch directory OUTSIDE the repository", while `:173` says "Run it under bash, from the repository root". `H1` reads `cut -f1 anchored.txt` as a bare relative path in both of its loops. NEITHER MODE RETURNS A NON-ZERO EXIT STATUS. The only signal is text on stderr, and the script's stdout is the artefact.

THE MODE A WRONG IMPLEMENTATION PASSES, AND I BUILT IT RATHER THAN REASONING ABOUT IT. With `handover.txt` empty, the worklist becomes all 36. The implementation strips the 17 that strip cleanly and AUTHORS a replacement opening for the other 19. Measured against the criteria run verbatim:

| Criterion | Result |
| --- | --- |
| 1, post-increment anchored selector | 0 rows; `comm -3` against the empty `handover.txt` prints 0 rows. PASSES |
| 4, changed set | IDENTICAL to `worklist.txt`, and no handover file can appear because the list is empty. PASSES |
| 5, numstat | no file exceeds 2 added or 2 removed. PASSES |
| 12, first-character test over the 36 | 0 rows. PASSES |

AND IT AUTHORS OPENINGS FOR NINETEEN HANDOVER FILES, measured by intersecting the changed set with the true handover list: 19.

WHAT IT VIOLATES. The increment's stated PREMISE at `:39`: "The increment DELETES the leading status token from the opening LINE of every file on THIS STEP'S WORKLIST, and it authors no replacement line ... The handover files keep their token and this step does not open them." It authors 19 replacement lines and opens all 19 handover files, while the CONSEQUENCE at `:41` holds whole. It defeats `Q-78-driftsplit` and `Q-78-drifthandover`, and it ships 19 authored openings from a step that carries no acceptance criterion for an authored opening. CLASS 1.

MODE B IS THE MIRROR AND ALSO REPRODUCES: `handover.txt` becomes all 36 slugs, the worklist is empty, and a step that does nothing satisfies criteria 1, 4 and 7.

`medium` RATHER THAN `high` IS RIGHT, and this is where it differs from `GB-1`. Both defeat the same premise half, but this one prints two lines on stderr and an empty capture file, so an attentive implementer has a signal. `GB-1`'s falsifiers produce no error at all and pass more cleanly than the correct implementation.

I AGREE WITH THE REVIEWER AGAINST THE ROUND 3 TRIAGE ON THE CLASS. Round 3 ruled `G-F7` class 2 on the ground that the defect "passes only for a reader who takes half of criterion 2's sentence and discards the other half". No half-reading is involved now. A reader who follows both halves of criterion 2 in full, and runs the command in the directory criterion 2 names, gets the empty capture.

## `F2`. UPHELD. CLASS 2, second-guard hole. Severity `low`.

REPRODUCED, three fixtures built from the live pack file and run through both presence commands and the placement command:

```
                                                       presence   placement
CORRECT   sentence after the closing `>`, own paragraph      1       0 (exit 1)
WRONG-A   sentence appended inside the note, SAME line       1       1 (exit 0)
WRONG-B   sentence inside the note, OWN line, blank line     1       0 (exit 1)
```

WRONG-B AND CORRECT ARE BYTE-IDENTICAL ON ALL THREE COMMANDS. Confirmed by inspecting the tails: WRONG-B's sentence sits on its own line and is followed by the note's closing `>`, so it is inside the brackets AND starts its own line. That falsifies the criterion's stated premise at `:703`, "a sentence written inside the note shares that line and a sentence written outside it starts its own". The live file is 3 lines and its last line ends `>`, as the premise assumes, and the premise is still a claim about how the implementer writes rather than about the file.

WHY WRONG-B IS THE LIKELY WRITING RATHER THAN THE EXOTIC ONE, and I think this is the finding's strongest point. Increment 3's own instruction at `:556` is "THE SENTENCE LANDS AS ITS OWN PARAGRAPH BELOW THE ANGLE-BRACKET PLACEHOLDER NOTE AND OUTSIDE IT". WRONG-B honours "as its own paragraph" and "below the note" and breaks only "outside it", and every command in the criterion certifies it.

THE CONSEQUENCE IS THE ONE `A-F5` NAMED. `pack/prompts/planner.md` directs the adopter's planner to delete the angle-bracket placeholder notes as it fills each part in, so the rule never reaches the adopter's own plan. Criterion 5's `cmp` only proves the two copies agree about it.

CLASS 2 IS RIGHT. The placement command is the second guard the `A-F5` repair installed behind the two presence commands, and it has a hole. `low` is right: one rule fails to reach adopters, and nothing in this repository breaks.

## `F3`. UPHELD. CLASS 2, second-guard hole. Severity `low`. I ALSO RULE ON THE REVIEWER'S OWN CLASS-NONE ALTERNATIVE.

EVERY CLAIM REPRODUCES.

- Both sentences exist and are the same sentence with a different increment named. `plan-order-array-position.md:401` reads "WHICH INCREMENT 1 OPENS"; `step-intent-encoding.md:739` reads "WHICH INCREMENT 3 OPENS". Both carry the identical "`grep -n 'Unreleased' CHANGELOG.md` exits 1 today" measurement.
- The plan decides the order mechanically: `plan-order-array-position` has `blocked_by = []`, `step-intent-encoding` has `blocked_by = ["plan-order-array-position"]`. Both are `not-started`.
- `/usr/bin/grep -n 'Unreleased' CHANGELOG.md` exits 1 on this tree, so the shared measurement reproduces and is measured on the wrong tree: what matters for increment 3 is the tree `plan-order-array-position` leaves behind, where the section EXISTS.
- The precedent is real. `user-prompts-pointer-and-drift-coverage.md:71` states as an acceptance criterion that "`CHANGELOG.md` carries one `## [Unreleased]` section above `## [0.0.3] - 2026-08-15`".
- NO CRITERION DETECTS A DUPLICATE. `/usr/bin/grep -n 'CHANGELOG'` over both sidecars returns six rows: two path-set entries, two reasons paragraphs and the two DOCUMENTATION IMPACT sentences. Every one names the PATH. Nothing reads the file's content.

I RULE AGAINST CLASS NONE. The reviewer offers it on the ground that this is "neither a criterion nor a figure inside an increment block". The class 2 first kind, a second-guard hole, is not worded as a restriction to criteria, and it should not be read as one here: the DOCUMENTATION IMPACT sections did not exist before this fix pass, they were authored as the whole of the `A-F6` repair, and they now direct an action that produces a defect nothing reads. Reading the bucket narrowly would let a defect the fix pass itself introduced escape the count on a technicality, which is the opposite of what the widening was for. CLASS 2.

`low` IS RIGHT. The worst outcome is a duplicate heading or one clobbered entry in a changelog, visible to any reviewer reading the diff.

## `T-1`. ADOPTED FROM THE FIX-VERIFY LENS'S RECORDED-BUT-NOT-FILED LIST, AND UPHELD. CLASS 2, a criterion that refuses a correct implementation. Severity `medium`.

The fix-verification lens recorded this with its measurement and wrote "so a triager can overrule". Overruling a not-filed decision is a triage act, so I take it rather than leave it.

REPRODUCED. `workflow-calibration` IS ON THE HANDOVER LIST, row 9 of the `H1` capture, because its opening strips to "(deferred). The scaffolded workflow's round co...", which `sidecar-status-opening-drift.md:81` already names as one of the seven that need an authored opening. It is therefore NOT on this step's worklist, measured: 0 occurrences in `worklist.txt`.

THE CRITERIA ARE THEN UNSATISFIABLE AS A SET.

- CRITERION 4 requires that "NO FILE ON THE HANDOVER LIST APPEARS" in `git diff --name-only`.
- CRITERION 5 names `docs/plans/agent-scaffold.steps/workflow-calibration.md` as its ONE exception, at "at most 4 and 4", which presupposes it IS in the diff.
- CRITERION 6 requires item `B`'s correction inside that same file.
- The whole `### B` section directs the edit and argues at length that it is in scope.

An implementer who edits the file fails criterion 4. One who does not fails criterion 6. No implementation satisfies both.

THE CAUSE IS THE SAME AS `F3`'S. The handover split landed on 2026-08-21 and moved `workflow-calibration` out of this step's reach, and nothing reconciled section `B`, criterion 5's exception or criterion 6 against it. A repair or a re-scope authored without reconciling it against a dependency the same document declares is now the second instance of one failure mode in this round.

I AGREE WITH THE REVIEWER'S OTHER TWO NOT-FILED ITEMS AND RECORD WHY.

- THE `69` DECLARATION-SITE FIGURE. It measures at exactly 69 today, so it is not a non-reproducing figure, and the increment instructs at `:593` "Re-run the two anchors rather than copying the pair, because both move as the plan and the suite grow". Correctly not filed.
- `docs/plans/TEMPLATE.md` CHANGING THREE WAYS RATHER THAN "TWICE OVER". `:560` sits in the WHAT CHANGES prose, not in an acceptance criterion, not in a risk-class ground and not in a numbered RULE, so the figure rule's "if and only if" excludes it. Correctly not filed. It is a real inaccuracy and it is recorded here as NOT BEARING.

---

# The deduplicated count

THE FIX-VERIFICATION LENS DID AVOID DUPLICATING THE GROUND-BLIND LENS. I checked each pair rather than assuming it, and the two closest pairs are distinct.

- `F1` AGAINST `GB-1`, the closest pair. Both attack `sidecar-status-opening-drift` increment 1's premise half, and they are different defects with different repairs. `GB-1` operates on a CORRECTLY captured 17-file worklist and shows the criteria cannot see a rewrite or a probe-first deletion confined to it; its repair is a criterion that reads the opening line's provenance. `F1` shows the capture command itself is unrunnable as directed, so the worklist is wrong before any criterion runs; its repair is a working directory or a `SELECTED` argument. NEITHER SUBSUMES THE OTHER: `GB-1`'s repair does not reach `F1`'s mode B, where the step does nothing and passes, and `F1`'s repair does not reach `GB-1`'s falsifiers at all. COUNTED SEPARATELY.
- `F2` AGAINST `GB-5`. Both concern `step-intent-encoding` increment 3 pack prose, and they are different sentences in different files: `GB-5` is the how-to-add-a-step sentence in `example-step.md`, `F2` is the duty (g) sentence in `documentation-protocol.md`. COUNTED SEPARATELY.
- `F3` and `T-1` touch nothing the ground-blind lens raised.
- Within the ground-blind set: `GB-2` and `GB-6` are different increments of one step; `GB-3`, `GB-4`, `GB-5` and `GB-10` are different increments and rules of one step; `GB-8` and `GB-9` are different criteria of one step. `GB-11` is ONE defect appearing in two files and is counted ONCE, as the reviewer did.

DISMISSED: NONE. Every finding put to me reproduced, on its own terms or on a rebuilt form, and I record the three where the reviewer's own demonstration failed and I rebuilt it: `GB-1`'s second falsifier, `GB-6`'s quoted search string, and `GB-9`'s falsifier.

| | Count |
| --- | --- |
| Findings received | 14 (11 ground-blind, 3 fix-verification) |
| Adopted from the not-filed list | 1 (`T-1`) |
| DISTINCT UPHELD | 15 |
| Dismissed | 0 |
| CLASS 1 | 7 |
| CLASS 2 | 8 |
| Severity ceiling | `high` |

CLASS 1, seven: `GB-1`, `GB-2`, `GB-4`, `GB-5`, `GB-6`, `GB-7`, `F1`.
CLASS 2, eight: `GB-3`, `GB-8`, `GB-9`, `GB-10`, `GB-11`, `F2`, `F3`, `T-1`.
SEVERITIES: `high` 2 (`GB-1`, `GB-2`), `medium` 8 (`GB-3`, `GB-5`, `GB-6`, `GB-7`, `GB-8`, `GB-10`, `F1`, `T-1`), `low` 5 (`GB-4`, `GB-9`, `GB-11`, `F2`, `F3`).

TWO CLASSES MOVED AGAINST THE REVIEWERS. `GB-2` up, from class 2 to class 1, because it admits a wrong implementation as well as refusing a correct one. `GB-8` down, from class 1 to class 2, because the wrong implementation it names does not violate a risk ground, a numbered RULE or a cited Principle, only criterion 8's own purpose. The net class 1 count is unchanged by the pair.

THE BACKSTOP IS NOT TRIGGERED. Both `high` findings, `GB-1` and `GB-2`, are UPHELD. I dismissed nothing at any severity, so no independent re-check is owed and convergence is not blocked on one.

BY SIDECAR, because it decides one of the escalation options:

| Sidecar | Findings | Worst |
| --- | --- | --- |
| `step-intent-encoding.md` | 6 (`GB-3`, `GB-4`, `GB-5`, `GB-10`, `F2`, share of `GB-11`) | `medium` |
| `sidecar-status-opening-drift.md` | 3 (`GB-1`, `F1`, `T-1`) | `high` |
| `plan-order-array-position.md` | 3 (`GB-2`, `GB-6`, share of `GB-11`) | `high` |
| `validate-missing-source-exit.md` | 2 (`GB-8`, `GB-9`) | `medium`, and neither ships anything |
| `ledger-order-citation-currency.md` | 1 (`GB-7`) | `medium` |

---

# The round outcome, the arithmetic, and the foreclosure ruling

## Gates

All six pass, run from the worktree root through the project toolchain. Both reviewers' gate tables reproduce.

| Gate | Result |
| --- | --- |
| `cargo test` | exit 0, no failures |
| `cargo clippy --all-targets -- -D warnings` | exit 0 |
| `validate --source ... --metrics ...` | `docs/metrics/workflow.jsonl: 405 records, valid` and `docs/plans/agent-scaffold.plan.toml: 105 steps, 80 questions, valid`, exit 0 |
| `validate --source ... --workflow` | `workflow invariants hold`, exit 0 |
| `render --check --strict <PLAN>` | `docs/plans/agent-scaffold.plan.toml: up to date`, exit 0 |
| `LC_ALL=C grep -rcP '[^\t\x20-\x7e]' docs/plans/` | no path reports a non-zero count |

## The outcome

ROUND 4 IS NOT CLEAN, on both limbs of the widened stop condition.

- CLASS 1 must be ZERO. It is SEVEN.
- CLASS 2 must be THREE OR FEWER, all `low` or `medium`. It is EIGHT.

ONE THING IMPROVED AND IT IS WORTH STATING. Raising `GB-2` to class 1 leaves NO class 2 finding at `high`, so the class 2 limb's severity half is satisfied for the first time. The limb still fails on the count, eight against three.

## The arithmetic

The required count is confirmed in two places rather than assumed: `AGENTS.md:56` requires "consecutive clean rounds ... scaled to the stakes by the artifact's risk class", and `src/workflow.rs:450` encodes it as "`low_risk` 1, `risky` 2".

```
required consecutive clean rounds (risky)   2
streak entering round 4                     0
round 4 outcome                             NOT CLEAN
streak after round 4                        0
rounds used                                 4
cap                                         5
rounds remaining                            1
rounds needed to converge                   2
2 > 1
```

## THE RULING: CONVERGENCE IS FORECLOSED, and the loop escalates now rather than after round 5.

FORECLOSED WITHIN THE CURRENT RESET COUNT. Two consecutive clean rounds cannot fit in the one round that remains. Convergence is decided by arithmetic and not by judgement, which is the same foreclosure that forced this pass's second escalation.

AND THE ESCALATION IS ALREADY CERTAIN, WHICH IS WHY IT SHOULD HAPPEN NOW. `AGENTS.md:57` escalates when the total rounds reach the cap, "whatever the clean-versus-new-valid mix", with one proviso: "If a round both reaches the cap and is the converging clean round, the convergence check applies first, so the loop converges rather than escalating." Round 5 would reach the cap, and it CANNOT be the converging clean round, because a clean round 5 takes the streak to 1 against a required 2. So the proviso cannot apply and the escalation fires on round 5 whatever round 5 finds. Running it first buys one round's cost and no information that changes the decision.

THE FORECLOSURE IS NOT TERMINAL, and this half matters for the options. `AGENTS.md:57` continues: "When the human's decision is applied and the loop resumes, reset the artifact's round counters (both the consecutive-clean count and the total-round count) so the cap does not immediately re-fire on the next round." So the human's decision restores a full budget. The question put to the human is not whether the pass can continue. It is what to change so that the next budget ends differently from the last two.

AN ACCEPTED RISK DOES NOT SAVE A ROUND. `AGENTS.md:57` says an accepted risk "does not block convergence", not that it makes a round clean. The human has used that route twice in this pass, both times for `low`-severity items with one-character repairs.

---

# Options for the escalation

Five, each with its trade-offs and Principle-judged reasoning. The `AGENTS.md:57` reset applies to all of them, so each option starts from a full budget; they differ in what changes before that budget is spent.

## OPTION 1, RESET AND SPLIT THE PASS INTO PER-STEP LOOPS. RECOMMENDED.

WHAT IT IS. Apply the reset, then run the remaining review as five independent loops, one per sidecar, each with its own round budget and its own consecutive-clean streak.

IT MATCHES THE MACHINERY THE PROJECT ALREADY HAS. `src/workflow.rs:507` records that "The streak is per loop (per increment), not per artifact", and `:923` shows a real step, `round-log-core`, converging as two separate loops at two different classes. The round records already model per-increment loops. The five-sidecar single loop is the thing that is out of step with the data model, not the split.

THE EVIDENCE FOR IT IS THIS ROUND'S OWN DISTRIBUTION. `validate-missing-source-exit` carries two findings, both second-guard holes, neither shipping anything; it could plausibly go two rounds clean quickly. `ledger-order-citation-currency` carries one. Under a single loop those three sidecars have their streak reset for four rounds running by defects in the other two, which is the mechanism that has held the streak at zero since the count reset.

TRADE-OFFS. More total rounds across the project and five loops to track instead of one. Against that, each loop's surface is small enough for a clean round to be reachable, and the two sidecars carrying the `high` findings get concentrated attention instead of sharing a budget with three that are nearly done.

PRINCIPLES. Principle 6, Ground decisions in evidence: four rounds say the repair process works and the surface is too large, so act on the surface. Principle 2, Minimal by default: rounds are spent where the defects are. Principle 8, Structured data first, project for humans: the split matches the per-increment identity the round records already carry, rather than maintaining a loop shape the data does not represent.

## OPTION 2, RESET AND CONTINUE ON THE SAME SURFACE.

WHAT IT IS. Apply the reset, fix the 15 findings, run a fresh count against all five sidecars together.

TRADE-OFFS. Simplest, changes nothing, keeps the `risky` guarantee whole. Against it: this would be the third such reset, and rounds 1 to 4 each produced valid findings. The strongest argument for it is the fix-pass evidence, and that argument is weaker than it looks: 16 of 18 fixes closed, yet the fix pass ITSELF introduced `F3` and left `F2` as a repair that does not close, so two of this round's 15 findings are the previous repair's own output.

PRINCIPLES. Principle 6 argues against: the same input has produced the same output four times.

## OPTION 3, LOWER THE REQUIRED STREAK TO ONE FOR THIS PASS.

TRADE-OFFS. Cheapest, and it fits inside the remaining budget without a reset. Against it: two consecutive clean rounds is what `risky` MEANS in this project, stated at `AGENTS.md:56` and encoded at `src/workflow.rs:450`, and `w5_problems` reports a short streak unless a waiver covers it, so the change has to be made in the constants or waived rather than simply done. Round 4 found two `high` class 1 defects, so this is the worst available moment to accept the weakest evidence.

PRINCIPLES. Against Principle 1, Prefer the cleaner long-term architecture over the smallest diff: it is the smallest diff and it degrades the meaning of `risky` for every future pass. Against Principle 3, Safe on existing projects: `GB-5` and `GB-6` each ship a defect to every scaffolded project.

## OPTION 4, ACCEPT THE OUTSTANDING FINDINGS AS RESIDUAL RISK AND CONVERGE.

TRADE-OFFS. `AGENTS.md:57` permits it and an accepted risk does not block convergence, so this is the only option that reaches convergence without another round. Against it: accepting a class 1 finding means accepting that a wrong implementation passes, which is not what the residual route is shaped for. Seven of the 15 are class 1, two are `high`, and `GB-5` and `GB-6` ship to adopters. The two residuals the human has already accepted, `A-F4` and `G-F9`, are `low` items with one-character repairs, which is a different kind of ask.

PRINCIPLES. Against Principle 3, Safe on existing projects, and Principle 5, Make illegal states unrepresentable.

A NARROW FORM OF THIS OPTION IS DEFENSIBLE AND IS WORTH PUTTING SEPARATELY: accept the five `low` findings (`GB-4`, `GB-9`, `GB-11`, `F2`, `F3`) so the next round starts against ten rather than fifteen. That does not save a round and it does not converge anything, but it reduces what the next fix pass carries.

## OPTION 5, RE-CLASSIFY SOME INCREMENTS TO `low_risk`.

TRADE-OFFS. Some increments genuinely ship nothing outside `docs/plans/`, and `plan-order-array-position` increment 2 is a prose sweep whose own ground says "It ships nothing to a scaffolded project and it is reversible in a single revert". Against it: the human RE-CONFIRMED the drift step's `risky` class on 2026-08-21 over a drop to `low_risk`, receipt `q_id:"Q-78-driftclass"`, and re-opening classes because the budget is tight fits the classification to the arithmetic rather than to the risk.

PRINCIPLES. Against Principle 6, Ground decisions in evidence.

## RECOMMENDATION

OPTION 1, RESET AND SPLIT, with two qualifications.

- `GB-1` AND `GB-2` ARE NOT ACCEPTABLE AS RESIDUALS under any option. Both are `high`, both are class 1, and both sit in the two sidecars that would get their own loops.
- TAKE THE NARROW FORM OF OPTION 4 ALONGSIDE IT: accept the five `low` findings so the split loops open against ten items rather than fifteen.

## A SIXTH ITEM, NOT AN OPTION, BECAUSE IT OUTLIVES THIS PASS

MAKE THIS FORECLOSURE UNREPRESENTABLE. The control constants are already data: `validate --workflow-spec` supplies "the convergence streaks, round cap, and backstop severity", and `validate --workflow` already recomputes the per-increment streak and reports a disagreement. Nothing reports the state this triage had to derive by hand, which is `cap - rounds_used < required_streak - current_streak`. A check for it would report the dead end at the round it becomes unreachable rather than at the cap, one round later, and would have fired on this pass at round 4 without a triager working it out. Principle 5, Make illegal states unrepresentable. It is not this pass's to build and it owes its own `[[question]]` or step.

---

# What must route to the human

## Carried forward from round 3, and NOT discharged

I checked all of round 3's items against the tree rather than taking the brief's count. THE BRIEF SAYS TWO REMAIN OWED. FOUR DO. That undercount is itself an instance of the defect item C names.

CARRIED A. `Q-80` IS STILL `open`, AND IT IS NOW ANSWERED IN SUBSTANCE BUT NOT CLOSED. Measured: `docs/plans/agent-scaffold.plan.toml` declares `id = "Q-80"` with `status = "open"`. It asks whether a rebuilt artefact's risk class is re-derived when the rebuilt artefact enters review. A receipt now settles the general rule: `q_id:"Q-78-classinherit"` (2026-08-22) chose "Name the rebuild branch in AGENTS.md and make a re-opened loop inherit the retired loop's class". THE ACTION OWED is to close `Q-80` against that receipt, or to say why it is not covered. It bears on the arithmetic above, because the two-clean-rounds requirement rests on the class.

CARRIED B. THE ROUTED-DECISION-TRACKING DEFECT STILL HAS NO `[[question]]`. Measured: no `[[question]]` in the plan mentions routed-decision tracking in any form. The ledger records the defect twice. This section exists only because a triager compensates for it by hand, which is not a mechanism, and the undercount at the head of this list is what that costs.

CARRIED C. ROUND 2'S NOTIFICATION 1 IS STILL UNDISCHARGED ON ITS CONFIRMATION HALF, AND THE ASK HAS GROWN. Round 3 measured sixteen 2026-08-21 `Q-78` sub-decision ids and asked the human to confirm the set is what they took, because four of the receipts were written by an agent after the fact. MEASURED TODAY, there are TWENTY-FOUR distinct `Q-78-` sub-decision receipts. No receipt confirms the set. The ask is unchanged in kind and larger in size.

CARRIED D. THE `AGENTS.md:93` REBASE-RULE QUESTION IS STILL UNREGISTERED. Measured: no `[[question]]` in the plan mentions a rebase, a merge base or a merge-back rule. `AGENTS.md:93` is the worktree lifecycle and merge-back rule and it is unenforced.

DISCHARGED SINCE ROUND 3, recorded so the next adjudication does not re-carry them. Round 3's NEW 1 by `q_id:"Q-78-round4"`, its NEW 2 by `q_id:"Q-78-stopwiden"`, and its NEW 3 by `q_id:"Q-78-packruling"`, all with receipts dated 2026-08-22. Round 3's CARRIED 4, the unratified `step-intent-encoding` class change, is MOOT and I close it: `q_id:"Q-78-classinherit"` now settles the rule it would have been decided under, and no `step-intent-encoding` increment has opened a loop.

## New, raised by this round

NEW 1. THE ARITHMETIC DECISION, which is the escalation itself. Convergence is foreclosed and the five options are above. Recommended: OPTION 1, reset and split, with `GB-1` and `GB-2` named as must-fix and the five `low` findings accepted.

NEW 2. THE MODEL-SIDECAR FRAMING WAS WRONG AND THE LEDGER MUST RECORD IT. `ledger-order-citation-currency.md` was briefed to three agents as the model the other four are measured against. Its FIGURES all reproduce, verified row by row above, so the stated ground was true. The INFERENCE from figure currency to criterion soundness was not, and `GB-7` is a class 1 finding against its criterion 4. This needs no human decision; it needs a ledger entry that records the correction to the inference rather than to the measurement, and it needs the three briefs' framing withdrawn. I raise it here because the brief directs that the ledger record it.

NEW 3. `GB-11` AND CARRIED B COLLIDE, AND WHOEVER FIXES ONE MUST FIX THE OTHER. `plan-order-array-position.md:261` and `step-intent-encoding.md:141` both hard-code `80 questions` as a pass condition. Registering the `[[question]]` that CARRIED B owes takes the count to 81 and makes both criteria unsatisfiable the same day. The repair is two characters in each file. Flagged so the two are not scheduled independently.

NEW 4. A DEFECT CLASS THIS ROUND SAW TWICE AND HAS NO GUARD FOR. `F3` and `T-1` are the same failure: a section authored or re-scoped without reconciling it against a dependency the same document declares. `F3` is the `A-F6` repair writing "WHICH INCREMENT N OPENS" into two sidecars whose `blocked_by` makes one false. `T-1` is the 2026-08-21 handover split moving `workflow-calibration` out of the drift step's worklist while criterion 5's exception, criterion 6 and the whole `### B` section still direct an edit to it. Both passed every criterion of their increments. Whether this owes its own rule is a judgement above my role; I record it because two instances in one round is a pattern rather than a coincidence.

THERE ARE NO OTHERS. I checked round 3's Part 5 in full, the ledger's live `Q-78` region, and the receipt set, and every item is either listed above or recorded as discharged.

---

# File safety

Every fixture built by this triage lives under the session scratchpad in `triage-r8/`, a directory this triage created and owns: `drift/` (with `anchored.txt`, `handover.txt`, `worklist.txt`, `anchored.sh`, `h1.sh`, `root/`, `wrongB2/`, `wrongA2/`, `wrongA3/` and `correct/`), `gb2/`, `gb7/`, `gb8/`, `gb9/`, `gb10/`, `f1/`, `f2/`, `c4rows.txt`, `then.txt` and `gates.log`. Nothing was written inside the repository, nothing outside `triage-r8/` was deleted, no wildcard glob was used in any delete, and no fixture was created with mode 000 or 600, so none needed restoring. The `gb-r8/`, `fixverify/`, `adopter/`, `triage-r7/` and `planner-fixpass/` directories were not written to and not read from: every reviewer claim was rebuilt from the sidecar text rather than taken from another agent's fixture.

Measuring `F1`'s mode A required running `H1` from the repository root, which reads `anchored.txt` from its working directory. That file was deliberately NOT placed there, because its absence IS the measurement. `git status --short` in this worktree reports only this findings file.
