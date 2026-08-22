# `Q-78` round 4 of the reset count, GROUND-BLIND FALSIFICATION lens, findings

Reviewer file. Read-only with respect to the plan and the code. Written as the work proceeded, so ordering is discovery order and not severity order.

METHOD. For each stated ground in the five sidecars, split the sentence into its PREMISE and its CONSEQUENCE, then build a wrong implementation for each half. A criterion set is ground-blind when the implementation that falsifies the premise, while the consequence still holds, passes every criterion.

CLASSES, as the brief widens them.

- CLASS 1: a ground-blind criterion. A wrong implementation passes while it violates a stated risk ground, a numbered RULE or a cited Principle.
- CLASS 2, three kinds: a second-guard hole, a non-reproducing figure INSIDE an increment block, and a criterion that REFUSES a correct implementation.
- NOT BEARING: currency defects, stale counts outside an increment block, missing receipts.

Fixtures live under the session scratchpad in `gb-r8/`. No fixture was built inside the repository.

## Findings

### GB-1, CLASS 1, `high`. `sidecar-status-opening-drift` increment 1: the premise half is refused only for a falsifier that reaches the handover files, and every falsifier confined to the worklist passes every criterion.

THE GROUND, `docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md:39`. THE PREMISE: "The increment DELETES the leading status token from the opening LINE of every file on THIS STEP'S WORKLIST, and it authors no replacement line". THE CONSEQUENCE, `:41`: "`render` inlines every one of those opening lines verbatim into `docs/plans/agent-scaffold.md`, so every edit ships into the published plan."

THE SIDECAR CLAIMS THE PREMISE HALF IS REFUSED, at `:43`: "BOTH HALVES ARE REFUSED BY CONSTRUCTION, AND BOTH CONSTRUCTIONS WERE BUILT AND RUN. An implementation that rewrites ALL the selected openings falsifies the premise while the consequence still holds ... MEASURED on a throwaway copy given that implementation, criterion 1 prints ZERO rows against the handover list it requires". That construction rewrites all 36 SELECTED files, so it destroys the 19 handover rows criterion 1 requires. A REWRITE CONFINED TO THE 17 WORKLIST FILES LEAVES THOSE 19 ROWS EXACTLY WHERE THEY ARE, and criterion 1 cannot see it.

THE WRONG IMPLEMENTATION, BUILT AND RUN. On each of the 17 worklist files, replace the whole opening line with one fabricated, status-neutral sentence, "This work was scheduled from an earlier review round and is recorded here." No status token is left anywhere, so nothing contradicts any declared `status` and criterion 11's reading is satisfied as well.

Reproduce from the fixture directory (`gb-r8/wrongB2`, built by `gb-r8/build-wrong2.sh` from a copy of `docs/plans/agent-scaffold.md` and `docs/plans/agent-scaffold.steps/`):

```
bash gb-r8/check-variant.sh gb-r8/wrongB2
```

MEASURED, against the criteria run verbatim:

- CRITERION 1: the anchored selector prints 19 rows, and `comm -3` of its slug column against `handover.txt`'s slug column prints NOTHING. PASSES.
- CRITERION 12: ZERO rows. PASSES.
- CRITERION 10: ZERO rows, so there is nothing for the outcome to dispose of. PASSES, and it passes MORE CLEANLY than the correct implementation, which prints 9 rows the implementer then has to argue about one by one (`gb-r8/wrongC`, the specified bare token deletion, measured).
- CRITERION 5: every worklist file reports 1 added and 1 removed, inside the 2-and-2 bound. PASSES.
- CRITERION 4: `git diff --name-only` lists exactly the 17 worklist files. PASSES.
- CRITERION 11: the reading finds no claim any declared `status` contradicts, because the fabricated sentence makes no claim about state at all. PASSES.
- Criteria 7, 8 and 9 are a re-render, the validators and an ASCII sweep, and none of them reads sidecar prose.

WHAT IT VIOLATES. The increment's own PREMISE, which says it authors no replacement line. `Q-78-statusform`, the human decision recorded at `:13`, which chose DELETE the state token over replace it. The NOT IN SCOPE bullet at `:110`: "This step corrects a stale claim about state. It does not review, re-scope, re-title or rewrite a single step." THE CONSEQUENCE HOLDS WHOLE: all 17 fabricated lines ship into `docs/plans/agent-scaffold.md`.

A SECOND FALSIFIER OF THE SAME PREMISE, ALSO BUILT AND RUN, IS DESTRUCTIVE RATHER THAN FABRICATING. The premise says the increment deletes the leading status TOKEN from the opening line. An implementation that deletes THE WHOLE OPENING LINE is caught on 8 of the 17 files only, and only incidentally: those 8 sidecars hold nothing below the opening line, so criterion 12 reads an empty string (`gb-r8/wrongA`, measured, criterion 12 prints 8 rows). An implementation that probes first and deletes the whole line only where criterion 12 stays silent (`gb-r8/wrongA2`, measured) destroys the opening paragraph of 9 sidecars, `checks-runner-worktree-name-collision`, `decision-folder-currency`, `human-input-gate-reinforce`, `planner-folds-decisions`, `prompt-drift-guard`, `review-mode`, `round-log-core`, `session-preflight` and `workflow-invariants`, each at 0 added and 1 removed, and passes criteria 1, 5 and 12 with the same zero output as the correct implementation.

WHY NO CRITERION REACHES EITHER. Criterion 1 tests only for a LEADING TOKEN, and the sidecar says so itself at `:163`: "A DELETION SATISFIES IT BY CONSTRUCTION, since a line with no leading status token cannot print one". Criterion 12 tests only the first character. Criterion 10 is a keyword scan whose empty output the sidecar explicitly refuses to treat as a target. Criterion 5's bound is a line-pair count and cannot tell a deletion from a rewrite. Criterion 11 is a reading about state claims and says nothing about whether the line is the one that was there.

### GB-2, CLASS 2 (a criterion that refuses a correct implementation), `high`. `plan-order-array-position` increment 2 criterion 1 builds its resolution table from the working tree, and increment 1 has already deleted the field that table is made of.

`docs/plans/agent-scaffold.steps/plan-order-array-position.md:289`, inside criterion 1 of increment 2:

```
awk '/^slug = /{s=$3} /^order = /{sub(/order = /,""); print $0"\t"s}' docs/plans/agent-scaffold.plan.toml | tr -d '"' | sort -n > order-to-slug.tsv
```

Increment 1 of the same step deletes every `order` line from that file, and its own criterion 1 (`:115`) requires `grep -c '^order = ' docs/plans/agent-scaffold.plan.toml` to print `0`. Increment 2 runs after increment 1. So on the tree increment 2 actually runs on, that `awk` matches nothing and `order-to-slug.tsv` is EMPTY.

MEASURED. Against a copy of the live plan with every `^order = ` line removed, which is what increment 1 leaves behind, the table has 0 rows against 105 before the deletion:

```
grep -v '^order = ' docs/plans/agent-scaffold.plan.toml > postinc1.plan.toml
awk '/^slug = /{s=$3} /^order = /{sub(/order = /,""); print $0"\t"s}' postinc1.plan.toml | tr -d '"' | sort -n | wc -l
```

prints `0`. The same command against the committed plan prints `105`.

THE CONSEQUENCE FOR CRITERION 2. P1 sets `want` from that table, so `want` is the empty string on every row, and the slug test becomes `grep -qF -- '``'`. MEASURED on a two-line fixture holding one CORRECTLY restated drifting citation and one exempt citation (`gb-r8/p1fix`), P1 prints:

```
rows=1 restated=1 wrong_slug=0 number_survives=0        # table built before the deletion
WRONG SLUG f.md:2 (was step 86) wants ``
rows=1 restated=0 wrong_slug=1 number_survives=0        # table built after increment 1, the real tree
```

So criterion 2's `wrong_slug=0` clause and its `restated` clause both refuse a correct implementation, on every row, on the only tree the increment can run on.

THIS IS THE ONE RULE THE CLEAN SIDECAR STATES AND THIS ONE DOES NOT FOLLOW. `ledger-order-citation-currency.md:60` names the same trap and solves it: "THE RESOLUTION TABLE IS BUILT FROM A NAMED COMMIT, NOT FROM THE WORKING TREE, so the increment is reproducible whether it runs before or after `plan-order-array-position` deletes the field (Principle 7, Reproducible)", and its command is `git show <pre-deletion-commit>:docs/plans/agent-scaffold.plan.toml | awk ...`. The sibling step's increment 2 carries the unqualified working-tree form.

### GB-3, CLASS 2 (a criterion that refuses a correct implementation), `medium`. `step-intent-encoding` increment 3 criterion 9 omits the render golden that its own criterion 2 forces to change.

`docs/plans/agent-scaffold.steps/step-intent-encoding.md:719` enumerates the changed-path set as "the 12 declaration-site files, plus `src/main.rs`, plus `docs/plans/agent-scaffold.md`, plus `docs/plans/TEMPLATE.md`, ..." and `:721` states that the enumeration is exact: "an implementer who made any of those edits FAILED it, and one who obeyed it shipped the defect instead."

The 12 declaration-site files are listed at `:579`. `src/plan/testdata/render-fixture.plan.toml` is one of them, with 7 sites, and criterion 2 (`:639`) requires all 69 sites to carry both fields. `src/plan/testdata/render-fixture.md` is NOT in the list.

That file is the render golden. `src/plan/render.rs:660` reads `const GOLDEN: &str = include_str!("testdata/render-fixture.md");` and `render_is_deterministic_and_matches_the_golden` (`src/plan/render.rs:697`) compares a fresh render of `render-fixture.plan.toml` against it. Increment 1's render rule (`:91`) emits a `- problem:` and an `- approach:` line for every step carrying a field, and increment 1 criterion 4 leaves `beta`, `delta`, `epsilon` and `zeta` with no field and `eta` with `problem` alone. Criterion 2 fills all five. So the golden MUST change.

NO IMPLEMENTATION SATISFIES BOTH CRITERIA. One that updates the golden fails criterion 9's exact enumeration. One that obeys criterion 9 fails criterion 11, which requires `cargo test` to pass. The sibling step gets this right: `plan-order-array-position.md:245` puts `src/plan/testdata/render-fixture.md` in its own increment 1 path set for the same reason.

### GB-4, CLASS 1, `low`. RULE 3's trim clause is not reachable by any criterion, so a `is_empty()` implementation passes while the rule says `trim`.

`docs/plans/agent-scaffold.steps/step-intent-encoding.md:33`, RULE 3. THE PREMISE: "`validate` therefore rejects a value that is empty after a trim." THE CONSEQUENCE: "MEASURED: with this rule, an empty backfill over the whole plan prints TWO PROBLEMS PER STEP and exits 1".

An implementation that tests `value.is_empty()` rather than `value.trim().is_empty()` falsifies the premise while the consequence still holds, because every criterion that exercises the rule supplies the literal empty string.

- Increment 1 criterion 3 (`:161`) supplies `problem = ""` and `approach = ""`, and its whole-plan measurement is the same value repeated.
- Increment 1 criterion 13 (`:269`) names `validate_rejects_an_empty_problem` and `validate_rejects_an_empty_approach`, and each "builds a one-step plan carrying the defect its name states". Written with `""`, both pass on the untrimmed implementation, and both still FAIL under criterion 13's RED measurement, which deletes the check entirely.
- No other criterion in the step supplies a whitespace-only value. Verified: the string `" "` as a field value appears nowhere in the sidecar, and criterion 3 is the only criterion that supplies an empty value at all.

WHAT SHIPS. `problem = " "` on every step of a whole-plan backfill, which is the shortcut RULE 3's own ground names ("a whole-plan backfill of empty strings survives the flip and satisfies any per-field presence check"), one character away from the form the criterion tests. Severity is `low` because RESIDUAL 2 already concedes that meaninglessness is representable under a required field, so the extra ground a trim buys is narrow.

THE REPAIR IS ONE FIXTURE: give criterion 3 a second one-step plan carrying `problem = " "` and `approach = "\t"`, or state the whitespace form in criterion 13's test names.

### GB-5, CLASS 1, `medium`. `step-intent-encoding` increment 3: the pack's how-to-add-a-step sentence is guarded by a path name and by nothing that reads it, and the increment's own ground says a path name proves nothing about content.

THE GROUND, `docs/plans/agent-scaffold.steps/step-intent-encoding.md:558`: "After the flip its literal execution produces a plan that no longer parses, and the parser aborts on the FIRST missing field, so an operator following it learns about `approach` only after supplying `problem` and re-running. Shipping that instruction to every scaffolded project is what Principle 3, Safe on existing projects, is cited to prevent in this increment's own cost paragraph, and every criterion below would otherwise pass over it. The corrected sentence names `problem` and `approach` as required entries of the `[[step]]` block."

THE PREMISE: the corrected sentence names BOTH `problem` and `approach`. THE CONSEQUENCE: the pack stops shipping a recipe for a plan that does not parse, and `pack/plan-template.steps/example-step.md` and its committed copy change.

EVERY MENTION OF THAT FILE IN THE INCREMENT IS PROSE. Measured, `grep -n 'example-step' docs/plans/agent-scaffold.steps/step-intent-encoding.md` returns `:538`, `:558`, `:564`, `:566`, `:688`, `:719`, `:721` and `:741`. Only `:688` is a command, and it is criterion 5's third `cmp`, which compares the pack source against its committed copy. Criterion 9 (`:719`) names the two paths. NOTHING READS THE SENTENCE.

THE WRONG IMPLEMENTATION. Correct the sentence to name `problem` alone: "To add a step, add a `[[step]]` entry to the `.plan.toml` with its `problem` field and a matching `<slug>.md` body sidecar in this directory, then re-render." Then:

- CRITERION 5's third `cmp` passes, because both sides of the pair carry the same bytes.
- CRITERION 9 passes, because both paths appear in `git diff --name-only`.
- CRITERION 3 passes, because the shipped `pack/plan-template.plan.toml` carries both placeholder values and the scaffolded plan still validates.
- CRITERION 4 passes, because it reads `docs/plans/TEMPLATE.md` for the two PLACEHOLDER lines, which come from `plan-template.plan.toml` and not from this sentence.
- Criteria 1, 2, 6, 7, 8, 10, 11 and 12 read the schema, the declaration sites, the documentation-protocol sentence, the migration record, R4, a `grep` over `src/`, the suite and `status --step`. None reaches it.

WHAT SHIPS: to every scaffolded project, the one how-to-add-a-step sentence the pack carries, naming one of the two fields a `[[step]]` now needs, so the operator meets `missing field \`approach\`` on the second run. That is exactly the state `:558` cites Principle 3 to prevent.

THE ASYMMETRY IS INSIDE THIS ONE INCREMENT. The documentation-protocol sentence gets criterion 6, which is two `grep -c -F` presence commands PLUS a placement command, written out per file "because the pack source and its committed copy are two files and a reader who substitutes once proves one file". The placeholder values get criterion 4, which is two commands, one per field, "because a template that ships one placeholder and renders the other nowhere satisfies a single-field check". The sentence that turns the pack into a recipe for an unparseable plan gets neither. The increment states the principle it then does not apply, at `:691`: criterion 9 "names the paths and proves nothing about their content".

THE REPAIR IS TWO COMMANDS OF THE SHAPE CRITERION 4 ALREADY USES, one per field, over `docs/plans/TEMPLATE.md`, which `render` inlines this file into.

### GB-6, CLASS 1, `medium`. `plan-order-array-position` increment 1: the shipped `and order` clause is guarded by a path name only, and the increment states the command that would prove it as a BEFORE measurement and never as a pass condition.

THE GROUND, `docs/plans/agent-scaffold.steps/plan-order-array-position.md:83`: "Increment 1 ships the deletion, and this increment's own risk ground is that 'every previously valid plan in every scaffolded project fails to parse until edited' and that this is widely depended on. An implementation that satisfies every other criterion here ships, to every one of those projects, the instruction to write the field that now makes the plan fail to parse: the criteria would be blind to the consequence their own risk ground names."

THE PREMISE, `:80`: "`pack/AGENTS.md`, the phase 2 sentence reading 'the `<task>.plan.toml` skeleton holds the Roadmap (`[[step]]` entries with status and order)'. The `and order` clause goes."

THE INCREMENT'S REPAIR WAS TO PUT THE THREE PATHS IN CRITERION 8, and criterion 8 is a path-name enumeration. Measured, `grep -n 'status and order' docs/plans/agent-scaffold.steps/plan-order-array-position.md` returns `:80`, `:259`, `:383` and `:403`. `:383` is a different sentence in a front sidecar. The other three are prose. No acceptance criterion of increment 1 reads the clause. Criterion 1's four commands are `grep -rlE '(\\n|^)order = '`, `grep -c '^order = '`, `grep -rn '\.order' src/` and `grep -c 'slug, status, order' src/plan/render.rs`, and the anchored search is stated at `:78` to be incapable of reaching prose: "The sentence below is PROSE, so no anchored search reaches it".

THE WRONG IMPLEMENTATION. Change `pack/AGENTS.md` anywhere other than that clause, for instance rewrite the same sentence's tail, and re-render its two committed copies. `AGENTS.md` and `.agents/AGENTS.reference.md` move with it because `the_committed_scaffold_matches_a_fresh_render` in `src/agents_md_drift.rs` pins them, so `cargo test` stays green. All three paths then appear in `git diff --name-only`, criterion 8's enumeration is satisfied exactly, and `entries with status and order` still ships to every scaffolded project.

THE STEP ALREADY WROTE THE COMMAND THAT CLOSES THIS, at `:80`: `grep -rln 'entries with status and order' pack/ AGENTS.md .agents/`. MEASURED TODAY it returns exactly the three named paths, so it reproduces. It is stated as a BEFORE measurement and never as an after-condition. Every other before-measurement in this increment is paired with one: criterion 1 states "MEASURED BEFORE THE CHANGE, the four print 12 rows, `105`, 5 rows and `1`, so each detects the condition rather than merely staying silent", and each of those four has a stated post-change value. This one does not.

THE REPAIR IS ONE LINE IN CRITERION 1: after the change, that same `grep -rln` prints nothing and exits 1.

### GB-7, CLASS 1, `medium`. `ledger-order-citation-currency` criterion 4 offers three dispositions and all twelve rows it governs are a fourth kind, so the disposition that passes is false of every one of them.

THE GROUND, `docs/plans/agent-scaffold.steps/ledger-order-citation-currency.md:24`: "TWO CITED VALUES NAME NO STEP AT ALL ... Each is either a citation of a RENDERED POSITION rather than an `order` value, or a false positive of the search, or a mistake in the original entry. Criterion 4 disposes of each one by hand and forbids a guess."

Criterion 4 (`:134`) makes that trichotomy an executable obligation: "the outcome records, for every row it prints, which of three things the row is, and no row may be left without one ... A row disposed of by a guess at the intended step is this criterion failed."

MEASURED, ALL TWELVE ROWS ARE A FOURTH KIND THE TRICHOTOMY DOES NOT NAME: a value that named a real step when the entry was written, and was later vacated. Run:

```
grep -noE '.{0,60}\b(order|step) (84|91)\b.{0,40}' docs/plans/agent-scaffold.ledger.md
```

- THE SEVEN `84` ROWS cite `rename-to-agent-flow`, which held `order = 84` when they were written and holds `order = 100` today. The ledger says so in its own narrative, on line 749: "The planner also moved `rename-to-agent-flow` from order 84 to 100 and set `blocked_by = [\"audit-us..." Verified against the source: `awk '/^slug = "rename-to-agent-flow"/{f=1} f&&/^order = /{print; exit}' docs/plans/agent-scaffold.plan.toml` prints `order = 100`.
- THE FIVE `91` ROWS cite a step that existed at `order = 91` and was deleted. Line 347 reads "step 91 REMOVED (committed deletion) because it...", and line 1605 reads "nothing would have caught an orphan left by step 91's removal".

None of these is a rendered position, none is a false positive of the search, and none is a mistake in the original entry. Every one was correct on the day it was written.

THE WRONG IMPLEMENTATION THAT PASSES. Forced to pick one of three, an implementer picks "a mistake in the original entry" and annotates all twelve `(no such step)`. MEASURED against criterion 2's own script, that disposition is invisible to it: `(no such step)` does not match the `annotated` regex ``\b(order|step) [0-9]+ \(`[a-z0-9-]+`\)``, so the five `91` rows stay in `bare`, and the seven `84` rows never enter `drifting` at all, which criterion 2's fourth clause states in its own words ("a row reading `84` can never reach `bare`"). The printed line is `bare=5`, which is the value criterion 2's MEASURED bullet gives for A CORRECT ADDITIVE EDIT. Criterion 4's obligation is discharged, because every row carries one of the three. Criteria 1, 3, 5, 6, 7 and 8 are a worklist capture, a red-then-green, a numstat, a path set, `next`, and the suite, and none reads a disposition.

WHAT IT VIOLATES. `(no such step)` is a false statement about twelve rows of the artefact this increment's own ground calls the one "that every convergence count, every round total and every re-raise ruling in this project reads" (`:54`). The step exists to make a citation followable without the deleted field (`:9`, "Resolve each citation to the slug it always meant, additively, so the historical text survives and a reader can follow the citation"), and this disposition makes twelve of them permanently unfollowable while recording that there was never anything to follow. Principle 6, Ground decisions in evidence, is the principle this step cites twice (`:11`, `:43`), and the evidence for what those rows mean is in the same file, two lines away.

THE SAME DEFECT REFUSES THE CORRECT DISPOSITION, which is the class 2 third kind and is recorded here rather than filed separately. The right annotation for the seven `84` rows is `` order 84 (`rename-to-agent-flow`) ``, taken from the ledger's own line 749 rather than guessed. Criterion 4 has no slot for it, and criterion 4's last sentence makes an annotation that is not one of the three read as the guess it forbids. Criterion 2 is neutral on it either way, for the reason its fourth clause records.

THE REPAIR IS A FOURTH DISPOSITION: the row cites an `order` value that was correct when written and has since been vacated by a move or a deletion, in which case it is annotated with the slug the ledger's own narrative names, and the outcome quotes the ledger line that establishes it.

NOTE, NOT BEARING, ON THE APPEND-ONLY GROUND. `:26` states "The plan grew by APPENDING, and an `order` value, once assigned, kept its slug." That is false of `order = 84`, which `rename-to-agent-flow` vacated. The four-date measurement does not see it because its `awk` filters `>=85`. The ground as USED is sound, because the drifting set is `>= 85` and the measurement covers exactly that range, so nothing downstream is affected. The sentence overstates its own measurement by one value.

### GB-8, CLASS 1, `medium`. `validate-missing-source-exit` criterion 8 counts five test NAMES and has no red measurement, so five tests that pin nothing satisfy the criterion whose stated purpose is that they pin the branches.

THE GROUND, `docs/plans/agent-scaffold.steps/validate-missing-source-exit.md:19`: "The rule is therefore one rule with one condition, not three special cases: an explicitly supplied path that does not exist is a violation", and `:100`, criterion 8's own purpose: "The fourth and the fifth are a pair over the same path string, and only the flag differs, so together they pin explicitness to `is_some()` rather than to a path comparison. The fifth is also the one that fails if the fix is written too wide. A criterion that only runs by hand does not survive the increment, which is why the pair lives in the suite as well as in criteria 4 and 5."

THE PREMISE: the five tests pin the five branches, and the fourth-and-fifth pair pins explicitness to `is_some()`. THE CONSEQUENCE: five functions with those names exist in `tests/validate_refuses_a_missing_explicit_path.rs` and `cargo test` passes.

THE WHOLE OF THE CRITERION IS A NAME COUNT:

```
grep -c 'fn missing_.*_path' tests/validate_refuses_a_missing_explicit_path.rs
```

Pass: "stdout is exactly `5`".

MEASURED, five correctly named tests whose bodies are `assert!(true)` print exactly `5` and exit 0 (`gb-r8/c8`), so the whole pass condition is satisfied by a file that pins nothing. `cargo test` passes on them by construction. Criteria 2, 3, 4 and 5 are hand-run commands against the binary, so they are green on a correct implementation whatever the suite contains, and criterion 8's own sentence says exactly why that is not enough: "A criterion that only runs by hand does not survive the increment."

THE TWO SIBLING SIDECARS BOTH CLOSED THIS SAME HOLE IN THEMSELVES, AND THIS ONE DID NOT. `plan-order-array-position.md:194` states the split and the repair: "THE GROUND SPLITS INTO A PREMISE AND A CONSEQUENCE ... A grep set can only reach the consequence, so a RED measurement carries the premise", then adds three greps and a RED measurement that flips the arms and requires all three named tests to FAIL. `step-intent-encoding.md:273` states the identical sentence for its own four tests and adds a RED measurement that deletes the two checks and requires all four to FAIL. `validate-missing-source-exit` criterion 8 has the grep and no red measurement of any kind.

WHAT SHIPS. The exit-code repair itself is pinned by criteria 2 to 5 at build time, so the increment lands correctly. What is not pinned is the state AFTER the increment: a later change that decides explicitness by comparing the resolved path against the derived default passes `cargo test`, because no test in the suite separates the fourth branch from the fifth. That implementation is the one the step's own `:85` paragraph identifies as the premise-half falsifier and builds criterion 4's second command to refuse, and criterion 8 exists to carry that refusal into the suite.

THE REPAIR IS THE SHAPE BOTH SIBLINGS ALREADY USE: change the explicitness test from `args.metrics.is_some()` to a comparison against the derived default, run `cargo test --test validate_refuses_a_missing_explicit_path`, and require `missing_explicit_metrics_path_equal_to_the_default` to FAIL while `missing_defaulted_metrics_path` stays green.

### GB-9, CLASS 2 (second-guard hole), `low`. `validate-missing-source-exit` criterion 9 aggregates three flags into one count, in a step whose stated discipline everywhere else is one command per flag.

`docs/plans/agent-scaffold.steps/validate-missing-source-exit.md:108`: "THE HELP TEXT STATES THE RULE. `./target/debug/agent-flow validate --help` describes, for each of the three flags, that a path the user supplies must exist. `grep -c -F -- 'must exist' <(./target/debug/agent-flow validate --help)` prints at least `3`."

`grep -c` counts LINES containing the string across the whole help output, so it cannot attribute a hit to a flag. An implementation that writes "must exist" three times inside the `--source` help alone, or once in `--source` and twice in the subcommand's about text, prints `3` and passes while `--plan` and `--metrics` document nothing. That falsifies the criterion's own header and `:35`, "The `--help` text of all three flags states the new behaviour". The bound is "at least `3`", which is looser again.

THIS IS THE ONE PLACE THE STEP FOLDS ITS FLAGS TOGETHER. Criterion 3 (`:67`): "This command is given on its own rather than as a substitution into criterion 2, because a reader who substitutes once proves one flag and the two arms are two pieces of code." Criterion 4 (`:69`): run separately. Criterion 8 (`:100`): "FIVE TESTS, because five branches."

MEASURED, the string is absent today: `./target/debug/agent-flow validate --help | grep -c -F -- 'must exist'` prints `0`, so the criterion does detect the unchanged state.

THE REPAIR IS THREE COMMANDS, one per flag, each reading that flag's own help block, in the shape criteria 3 and 4 already use.

SECOND, NOT BEARING: criterion 9 is the only command in the five sidecars that uses process substitution without saying so. The pass states the warning at `step-intent-encoding.md:301` ("Each uses process substitution, so it cannot run in nu") and at `ledger-order-citation-currency.md:80` ("Run this under bash"). This shell replaces `grep` with `ugrep` and is nu, so criterion 9 as printed does not run.

### GB-10, CLASS 2 (a criterion that refuses a correct implementation), `medium`. The batch partition is recomputed from the live plan at every batch, the batch SIZE moves whenever the plan grows, and only the batch COUNT is guarded.

`docs/plans/agent-scaffold.steps/step-intent-encoding.md:255` defines the split: "K is the smallest batch count whose batch size is 20 or less, and the batch size S is `ceil(N/K)`. Batch i covers declaration positions `(i-1)*S+1` to `min(i*S, N)`."

The batch block's criterion 1 (`:320`) then recomputes the partition from the LIVE plan at each batch:

```
sed -n 's/^slug = "\(.*\)"$/\1/p' docs/plans/agent-scaffold.plan.toml | awk -v s="$S" -v b="$B" '{if (int((NR-1)/s)+1 == b) print}' | sort > declared.txt
```

THE ONLY GUARD IS ON K, at `:263`: "`grep -c 'id = \"step-intent-encoding-inc2' docs/plans/agent-scaffold.plan.toml` prints `6`, and the `batches` field of the printed line equals `6`. A disagreement means the plan grew past 120 steps and the declarations need a planner pass before any batch runs." K IS 6 FOR EVERY N FROM 101 TO 120, which the sidecar states, so that guard never fires in the range it covers. S IS NOT GUARDED AND S MOVES INSIDE THAT RANGE.

MEASURED, running the sidecar's own rule:

```
steps=101 batches=6 size=17 last_batch=16 coverage=102
steps=105 batches=6 size=18 last_batch=15 coverage=108
steps=110 batches=6 size=19 last_batch=15 coverage=114
steps=120 batches=6 size=20 last_batch=20 coverage=120
```

THE SIDECAR'S OWN RECORD SHOWS THIS HAPPENING. Criterion 10 states "MEASURED at N=101, the rule gives `steps=101 batches=6 size=17`" and then "MEASURED AGAIN at N=105, the tree this sidecar was spliced into, the rule prints `steps=105 batches=6 size=18`". S moved by one while the design pass ran, and the plan is verified at `grep -c '^\[\[step\]\]'` = 105 today. This pass alone still owes the successor step for the drift handover, so N moves again before batch a runs.

THE TWO READINGS BOTH BREAK, AND THE SIDECAR PICKS NEITHER.

- `$S` HELD AT THE VALUE INCREMENT 1 CAPTURED. Six batches then cover `K*S` positions. At N=110 with S=18 that is 108, so two steps fall outside every batch. Nothing detects it until increment 3 criterion 8, six increments later, whose `source` equals `steps` clause fails with no indication of which batch owed the remainder.
- `$S` RECOMPUTED AT EACH BATCH. The partition shifts under the batches already done, so batch c's `declared.txt` contains steps batch a already filled. Those steps are in `declared.txt` and not in `gained-<field>.txt`, which is a `comm -13` of the pre and post filled sets, so criterion 1's identity check prints `missing` greater than zero on both rows and REFUSES a correct batch.

The criterion says "The batch letter and its slug list come from increment 1 criterion 10" and then supplies a command that derives them afresh. The two are the same thing only while N is unchanged.

THE REPAIR IS TO CAPTURE THE SLUG LISTS RATHER THAN THE RULE. Increment 1 criterion 10 already prints the per-batch slug list; recording it as the six batches' declared sets, and having criterion 1 read that capture instead of re-partitioning, makes the partition immune to N. That is the shape `sidecar-status-opening-drift` criterion 2 already uses for its own three capture files.

### GB-11, CLASS 2 (a criterion that refuses a correct implementation, latent), `low`. Two sidecars hard-code `80 questions` as a pass condition in the same sentence where they refuse to hard-code the step count.

`docs/plans/agent-scaffold.steps/plan-order-array-position.md:261` and `docs/plans/agent-scaffold.steps/step-intent-encoding.md:141` both state the pass condition as a `docs/plans/agent-scaffold.plan.toml: <N> steps, 80 questions, valid` line. The step count is a placeholder and the question count is a literal, in one sentence.

The question count moves exactly as the step count does. MEASURED today, `grep -c '^\[\[question\]\]' docs/plans/agent-scaffold.plan.toml` prints `80`, and `validate` prints `docs/plans/agent-scaffold.plan.toml: 105 steps, 80 questions, valid`, SO THE FIGURE REPRODUCES AND THIS IS NOT A NON-REPRODUCING-FIGURE FINDING. It becomes a refusal on the first `[[question]]` the plan gains, at which point both criteria pin a line no correct implementation can print. `Q-79` is already registered (`id = "Q-79"` at `docs/plans/agent-scaffold.plan.toml:2296`), so the highest registered id is 80 and the next one is 81.

THIS IS THE THIRD RULE OF THE ONE CLEAN SIDECAR, and both files adopt it for the other half of the same line. `plan-order-array-position.md:3` and `step-intent-encoding.md:3` carry the identical sentence: "It states no count of the plan's steps, because such a count expires and the plan's own standing cure, recorded in the ledger against orchestrator defect (12), is to carry the selecting command instead." `plan-order-array-position.md:115` says it again: "The `105` is the plan's step count on the day and it rises as the plan grows, so the outcome records what the command prints rather than this number." `ledger-order-citation-currency.md:20` states the general form: "no criterion below states either figure as a pass condition."

THE REPAIR IS TWO CHARACTERS IN EACH FILE: `<M> questions`.

## Verdict and counts, as measured

ELEVEN findings, all distinct. CLASS 1: six (GB-1, GB-4, GB-5, GB-6, GB-7, GB-8). CLASS 2: five (GB-2, GB-3, GB-9, GB-10, GB-11). SEVERITY CEILING: `high` (GB-1, GB-2).

THE ROUND IS NOT CLEAN ON EITHER HALF OF THE STOP CONDITION. Class 1 must be zero and is six. Class 2 must be three or fewer and all `low` or `medium`; it is five, and GB-2 is `high`.

BY SIDECAR:

- `step-intent-encoding.md`: four (GB-3, GB-4, GB-5, GB-10), plus a share of GB-11.
- `plan-order-array-position.md`: two (GB-2, GB-6), plus a share of GB-11.
- `validate-missing-source-exit.md`: two (GB-8, GB-9).
- `sidecar-status-opening-drift.md`: one (GB-1), and it is the round's joint-highest.
- `ledger-order-citation-currency.md`: one (GB-7).

EVERY FIGURE IN ALL FIVE SIDECARS THAT CAN BE REPRODUCED TODAY REPRODUCES EXACTLY. There is no non-reproducing-figure finding in this round, inside an increment block or outside one. Reproduced: the ledger's `135`, `116`, `12` at or below 83, the dedup surplus of `20`, the busiest line's eight citations across four values, `drifting=116 annotated=1 bare=115 unknown_slug=0 wrong_slug=0`, criterion 4's twelve rows splitting `7` and `5`, the four-date append-only pairs `8/8`, `11/11`, `12/12` and `18/18`, and the metrics `14` hits of which `13` are at or above 85; the plan-order declaration table of 12 files and 69 sites, `105`, five `.order` rows, `1` stale doc comment, the `unknown field \`bogus\`` message with its full expected-fields list, `old.plan.toml: 1 steps, 0 questions, valid`, the render-fixture `zeta=1 epsilon=1 roadmap zeta<epsilon=0 details zeta<epsilon=0`, the bare-word worklist's 8 rows across 5 files, and the single quotation row; the drift step's anchored `36`, complement `9` all declared `deferred`, handover `19`, and criterion 12 printing zero rows verbatim against the live tree; and step-intent's `core-assets` as the sole non-heading-first sidecar, the N1 fixture as the first of three `slug` sites in `src/plan/render.rs`, the `slug` anchor's 12 files and 69 sites against the `status` anchor's `99`, `8` subcommands, `0` and `4` for the two `next` context counts, `steps=105 batches=6 size=18` with six declared `inc2` entries, R4's `steps=105 source=0/0 quoted=1/1 projected=1/1`, and the RULE 5 and RULE 6 commits `5e7ee58` (2026-07-14, holds the plan document and not the sidecar), `0fadd90` (2026-07-19, the first commit holding the steps tree) and `c44d8d1` (2026-07-28).

THE THREE RULES OF THE ONE CLEAN SIDECAR, applied to the other four.

- RULE A, the search set does not contain itself. `validate-missing-source-exit` holds it. `plan-order-array-position` increment 2 breaks it, knows it (`:309`, "A specification whose search set contains itself cannot state a snapshot that survives its own edit") and pays by stating no snapshot. `step-intent-encoding`'s R4 breaks it and pays with the `quoted` reconciliation term, which is measured and reproduces. `sidecar-status-opening-drift` breaks it benignly, because its own opening carries no token, and says so.
- RULE B, refuse a concrete example inside the file. `plan-order-array-position` adopts it by name (`:311`). `step-intent-encoding` breaks it, with the fenced `- problem:` and `- approach:` pair under `render` in increment 1, and pays the whole `quoted` term for it. `sidecar-status-opening-drift` breaks it by quoting `reviewer-reproducible-evidence`'s opening line verbatim with its numbered citation, and pays a human decision (`Q-78-quotationrow`) plus a permanent `number_survives=1` exception in another step's oracle.
- RULE C, every figure is a command's output and never a pass condition. Held everywhere except the `80 questions` literal, which is GB-11.

GATES, run through the project toolchain from the worktree root.

- `cargo test`: PASS, exit 0.
- `cargo clippy --all-targets -- -D warnings`: PASS, exit 0.
- `validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl`: exit 0, `docs/plans/agent-scaffold.plan.toml: 105 steps, 80 questions, valid`.
- `validate --source docs/plans/agent-scaffold.plan.toml --workflow`: exit 0, `docs/plans/agent-scaffold.plan.toml vs docs/metrics/workflow.jsonl: workflow invariants hold`.
- `render --check --strict docs/plans/agent-scaffold.plan.toml`: exit 0, `docs/plans/agent-scaffold.plan.toml: up to date`.
- `LC_ALL=C grep -rcP '[^\t\x20-\x7e]' docs/plans/`: clean, no path reports a non-zero count.

FIXTURE HYGIENE. Everything was built under the session scratchpad in `gb-r8/`, in `wrongA`, `wrongA2`, `wrongB`, `wrongB2`, `wrongC`, `p1fix`, `c8`, `bogus`, `empty`, `h1run`, `appendrun` and `postinc1`. No fixture was written inside the repository, no fixture was created with mode 000 or 600, and nothing outside `gb-r8/` was deleted. One stray file was created in the worktree root during setup and removed immediately; `git status --porcelain` reports only this findings file.

