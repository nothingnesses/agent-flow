# Q-78 post-escalation round 2 Claude review

## Scope, method and gates

I reviewed `plan/q78-design-pass` at `a8cf6da`, product content through `c54a0b9`, as an independent reviewer in the isolated worktree `.agents/worktrees/q78-foreclosure-r2-claude`. I read `AGENTS.md`, the ledger from `RESUME HERE (2026-08-24, AFTER POST-ESCALATION ROUND 1)`, `q78-foreclosure-r1-triage.md`, `q78-foreclosure-r1-fix-brief.md` and the current `docs/plans/agent-scaffold.steps/step-intent-encoding.md`. I did not read the GPT round 2 review; it is absent from this tree in any case. I read only my own brief among the round 2 briefs.

Only two loops are in scope: `step-intent-encoding-inc1` (entering streak 0) and `step-intent-encoding-inc3` (entering streak 1). Both are `risky`. I edited no product file.

The product diff under review is `c54a0b9`, which touches exactly `docs/plans/agent-scaffold.steps/step-intent-encoding.md` and its rendered view `docs/plans/agent-scaffold.md` (18 insertions, 6 deletions). `git diff --check c54a0b9^..c54a0b9` exits 0, and `LC_ALL=C grep -cP '[^\t\x20-\x7e]'` prints `0` for both files.

All project commands ran through the project direnv environment. Every reconstructed artifact is under my own child of the authorised scratch root, `/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-foreclosure-r2-claude`. I used GNU grep 3.12 by absolute store path for every GNU-regex claim, because the interactive `grep` on this container's `PATH` is a shell function wrapping ugrep 7.5.0 and its regex dialect is not GNU's. I never used bare `/tmp` and never used a wildcard deletion.

Baseline gates, all green on the reviewed tree:

```text
validate --source ... --metrics ...            452 records, valid; 105 steps, 81 questions, valid; exit 0
validate ... --workflow                        workflow invariants hold; exit 0
render --check --strict agent-scaffold.plan.toml   up to date; exit 0
render --check --strict TEMPLATE.plan.toml         up to date; exit 0
cargo test                                     12 binaries, 470 passed, 0 failed
cargo clippy --all-targets --all-features -- -D warnings   exit 0
git status --porcelain                         empty
```

## FR1-2 verification, done independently

The brief requires FR1-2 to be verified rather than accepted. I verified it by construction, not by reading.

### The state axis is the real one

`LoopState` is declared at `src/next.rs:273-304` with exactly nine fieldless variants: `ReadyToPlan`, `Blocked`, `AwaitingFirstReview`, `AwaitingFixes`, `AwaitingReviewers`, `Converged`, `Escalate`, `RiskClassConflict`, `Done`. It carries no `#[non_exhaustive]` (`:271-272`), so a no-wildcard match inside the crate is exhaustiveness-checked. The nine names in the new table (`step-intent-encoding.md:320`) match the enum name for name, with nothing omitted and nothing invented. `build_context` is at `src/next.rs:993-1021`, private to the module, and `mod tests` is a child module at `src/next.rs:1231`, so the seam is callable from the required test. `LoopFacts` (`src/next.rs:649-657`) and `LoopContext` (`:639-645`) are plain structs a test constructs directly.

### The construction compiles, passes, and reddens exactly as specified

I built an independent replica of those three shapes in `seamproof/` under my scratch child, importing no product code, and implemented the criterion literally: one local `macro_rules!` invocation whose variant list generates both the table rows and a no-wildcard `match state { LoopState::<variant> => (), ... }`, with that generated match called for every row, and per-row `problem`/`approach` comparisons accumulated rather than short-circuited. Restored (unconditional) insertion runs green over all nine rows.

Applying the specified negative control, insertion only for `ReadyToPlan`, `AwaitingFirstReview`, `AwaitingReviewers` and `AwaitingFixes`, the test printed exactly the required set and nothing else:

```text
ROWS=9
MISMATCH blocked problem: absent
MISMATCH blocked approach: absent
MISMATCH converged problem: absent
MISMATCH converged approach: absent
MISMATCH escalate problem: absent
MISMATCH escalate approach: absent
MISMATCH risk-class-conflict problem: absent
MISMATCH risk-class-conflict approach: absent
MISMATCH done problem: absent
MISMATCH done approach: absent
```

Both keys on each of the five named states, no entry for the four retained rows. The control is recordable exactly as written.

### Future enum growth really does force the update

In a second copy, `growthproof/`, I added a tenth variant to the enum and left the macro invocation alone. `cargo test` refused to compile, and the diagnostic points at the macro invocation itself:

```text
error[E0004]: non-exhaustive patterns: `LoopState::AwaitingSecondTriage` not covered
  |                         ^^^^^ pattern `LoopState::AwaitingSecondTriage` not covered
121 | /     all_loop_states!(
    | |_____- in this macro invocation
```

So the "exhaustive by construction, not by a hand-maintained count" clause (`:322`) is satisfiable and load-bearing, and the refused shape it names (a separate `ALL_STATES` array plus an unrelated match) is genuinely weaker.

### Test retention and the contract list

`build_context_carries_intent_in_every_loop_state` joined the single authoritative increment-1 list (`:402`), which now holds ten names, and increment 3's retention clause gained "exhaustive all-`LoopState` `build_context` table" (`:824`). No count of that list is stated anywhere, so adding a name broke nothing. The new test needs no increment-3 setup adaptation: it supplies `Some(...)` through `LoopFacts` rather than through a partial TOML `Step`, and increment 3 keeps `StepInfo`'s `Option` for the Markdown substrate (`:725`), so it survives the required flip unchanged. `src/next.rs` was already in increment 1's changed-path set (`:440`), so criterion 11 needed no edit either.

VERDICT: FR1-2 is closed. The all-loop-state requirement now has a witness that fails on every omitted state, reports the whole omitted set, and cannot silently miss a future variant. The five previously unwitnessed states (`Blocked`, `Converged`, `Escalate`, `RiskClassConflict`, `Done`) are covered.

## Current-tree reconciliation

Every command either increment states that is runnable today reproduces. Nothing in this section is a finding.

| Command or figure | Cited at | Result |
| --- | --- | --- |
| `grep -c '^\[\[step\]\]' docs/plans/agent-scaffold.plan.toml` | `:31`, `:198` | `105`; `2 x 105 = 210`, the stated pair |
| leading-heading sweep over the step sidecars | `:107` | prints `docs/plans/agent-scaffold.steps/core-assets.md` and nothing else |
| `--help` subcommand census | `:407` | `8` |
| batch sizing script | `:417-423` | `steps=105 batches=6 size=18` |
| `declared_loops` vs `manifest_batches` | `:431-433` | `declared_loops=6 manifest_batches=6` |
| declaration-site search | `:752-772` | 12 files, 69 sites, row for row as printed |
| `grep -n 'Unreleased' CHANGELOG.md` | `:949` | no output, exit 1 |
| three template `cmp` pairs | `:874-883` | all byte-identical, exit 0 |
| documentation-protocol placement command | `:912` | one row per path, each ending `:0`, exit 1 |
| how-to-add-a-step sentence as it reads today | `:739` | `pack/plan-template.steps/example-step.md:3`, verbatim |
| `grep -rn 'the problem this step addresses' src/ --include='*.rs'` | `:933` | no output, exit 1 |
| `render --check --strict` on both plan sources | `:412`, `:935` | both `up to date`, exit 0 |
| R4 reconciliation on today's tree | `:668-693` | `steps=105 source=0/0 quoted=2/2 projected=2/2`; `projected - quoted = source` holds |
| `src/main.rs:496` as the `StatusArgs` site | `:61`, `:725` | `struct StatusArgs {` |
| `status --help` best-effort sentence | `:154` | present verbatim |
| `status --source <plan> --plan /nonexistent.md` | `:154` | prints the note, exit 0 |
| residual 4's three measurements | `:967` | all three reproduce, exit 0 in both cases |
| `awaiting-fixes` recipe | `:294` | reaches `awaiting-fixes` with the three stated non-intent context values |
| clap conflict message and exit code | `:396` | `--step` before `--resume` yields `the argument '--step <STEP>' cannot be used with '--resume'`, exit 2, confirmed against the two existing `conflicts_with` sites |
| fresh scaffold `validate`, `render --check`, `next` both surfaces | `:828-857` | all exit 0, stderr empty, state is `ready-to-plan` |
| `core-assets` in the Markdown Roadmap | `:943` | `docs/plans/agent-scaffold.md:180` |

The two `validate` wordings are a deliberate and correct distinction, not a slip: increment 3 criterion 3 says stdout "carries exactly" the `valid` line, because `validate --source` on a fresh scaffold also prints a metrics preamble, while the render check says stdout "is exactly", and that command really does print one line.

## Findings

Three findings, all class 2, all `low`. No class 1. No finding outside both classes.

### `R2C-1`. `next` never sees an absent intent field, on either surface, in either increment

- OWNER: `step-intent-encoding-inc1`.
- SEVERITY: `low`.
- CLASS: 2, second-guard hole.

EVIDENCE. Increment 1 specifies the `next` seam as conditional on presence: "`build_context` inserts a `problem` slot and an `approach` slot WHEN THE FIELD IS PRESENT, in every loop state" (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:112`). I enumerated every `next` invocation and every `build_context` obligation in both increments under review, by extracting lines 59-455 and 709-945 and matching on `agent-flow next`, `` `next` `` and `build_context`. The complete set is: criterion 7's `AwaitingFirstReview` pass (`:260`), criterion 7's `awaiting-fixes` repeat (`:294`), the new seam test (`:320`), and increment 3 criterion 3's two fresh-scaffold commands (`:851-852`). Criterion 7 runs "every criterion 2 fixture", and criterion 2 requires every matrix case to be exercised "as both `problem` and `approach`" (`:164`), so every fixture carries both. The seam test supplies `Some(...)` for both (`:320`). The fresh scaffold carries both required placeholders (`:729`). So no check in either increment ever runs the seam or either surface with either field absent.

The consequence: an implementation that inserts both slots unconditionally, filling an absent field with `""` rather than omitting the key, passes every criterion in both increments. It passes the seam test and its negative control unchanged, because both are driven from a `LoopFacts` carrying `Some` on both fields; it passes criterion 7 for the same reason; criterion 9 (`:412`) touches the live no-intent plan but reads only `render --check` and the changed-path set; and increment 3 criterion 12 (`:937`) pins the analogous absence contract for `status --step` on the Markdown substrate but runs no `next` at all.

The only thing standing in that implementation's way is unnamed. `golden_human_text` (`src/next.rs:2130`) and `golden_json` (`src/next.rs:2135`) byte-compare a whole projection built from `test_step("core-assets", ...)` with no intent (`src/next.rs:2028-2047`), in state `awaiting-reviewers`, and their expected context blocks (`src/next.rs:2050`, `src/next.rs:2075`) list four keys with no `problem` or `approach`. Those two goldens would redden; but neither is in the increment-1 authoritative list (`:402`), neither is protected the way `empty_details_sections_emit_no_bare_heading` (`:822`) and the four rule 2 and rule 3 tests (`:826`) are protected, and increment 1 criterion 12 (`:442`) asks only that `cargo test` passes. Editing two expected constants to add `"approach": ""` and `"problem": ""` satisfies it.

The asymmetry is inside one increment and it is deliberate everywhere else. `render` guards the absent case: `:100` states that a step with neither field and an empty body contributes nothing, and `:102` names `empty_details_sections_emit_no_bare_heading` as the increment-1 fixture that holds it. `status --step` guards it twice: `no-intent.plan.toml` (`:387-390`) and `status_step_preserves_both_partial_states` (`:354-378`), with the stated reason at `:144`, "so absence is never mistaken for an empty value". `next` is the one projection of the three with no absent-field check, and it is the one the increment's own risk ground singles out as "the `context` block that `next` hands an agent as an instruction rather than a report" (`:61`). The exposure is the whole optional window, increment 1 plus the six batch increments, during which most steps of this repository's own plan carry no intent.

The current wording makes the wrong implementation the easy one rather than a perverse one: the red control paragraph says "Temporarily replace THE UNCONDITIONAL INTENT INSERTION" and "Restore UNCONDITIONAL insertion" (`:324`), which reads as a licence to insert without testing presence.

CLASS, and why it is not class 1. What the wrong implementation falsifies is the specification sentence at `:112`, not a risk ground, a numbered RULE or a cited Principle. That is the exact boundary the round 7 triage drew for the structurally identical `status --step` hole: "What it falsifies is increment 1's sentence ... That is a specification sentence, not a risk ground, a numbered RULE or a cited Principle" (`q78-r7-triage.md:218`), verdict class 2, severity `low`. I apply the same rule and reach the same class. Severity `low` on the same calibration the round 8 triage used for `GB-4`: the defect substitutes an empty quoted slot for an absent one on an advisory surface, and increment 3 closes the window for TOML sources outright.

SMALLEST CORRECTION. Add one absent-field row to the seam obligation at `:320`: with a second `LoopFacts` carrying `None` for both fields, assert for every `LoopState` that neither `problem` nor `approach` is a key of the returned map. Replace "unconditional intent insertion" with "presence-conditional intent insertion" in both sentences of `:324`. Optionally name `golden_json` and `golden_human_text` in the increment-1 authoritative list so the goldens cannot be relaxed to accommodate a fabricated slot.

### `R2C-2`. The red control's retained set names two states no projection check in either increment samples

- OWNER: `step-intent-encoding-inc1`.
- SEVERITY: `low`.
- CLASS: 2, in-increment claim that does not reproduce.

EVIDENCE. The new control says: "Temporarily replace the unconditional intent insertion with insertion only for THE STATES THE PROJECTION CHECKS ALREADY SAMPLE: `ReadyToPlan`, `AwaitingFirstReview`, `AwaitingReviewers` and `AwaitingFixes`" (`:324`). Two of those four are not sampled.

GNU grep over the whole sidecar for `ReadyToPlan|ready-to-plan` and for `AwaitingReviewers|awaiting-reviewers` returns lines `320` and `324` and nothing else. Both tokens occur only inside the two paragraphs the fix added; no criterion anywhere in the file names either state. Increment 1's projection checks sample two states and name them: `AwaitingFirstReview` (`:260`) and `awaiting-fixes` (`:294`). `ReadyToPlan` is reached only by increment 3 criterion 3, which is a different increment and does not say so; I confirmed the state empirically by running `next --source docs/plans/TEMPLATE.plan.toml` in a fresh scaffold, which reports `state: ready-to-plan`. `AwaitingReviewers` is reached by no command and no named test in either increment.

The round 1 triage's own measured enumeration says the same thing in its E2 evidence: "Criterion 7 exercises review and fixes states (`step-intent-encoding.md:260-318`), while increment 3's fresh-scaffold check adds only ready-to-plan (`:842-851`)" (`q78-foreclosure-r1-triage.md:50`). The new sentence asserts a coverage claim its own triage record contradicts.

This is not a hole in the seam test: the restored run asserts all nine rows, `AwaitingReviewers` included, so an implementation that omitted intent there still fails. What it costs is control strength and reader trust. Because two states sit in the retained set on a false premise, no red control anywhere reddens on them, and `AwaitingReviewers` is precisely the state that no other check in either increment reaches, so it is the row whose load-bearingness is least demonstrated. A reader who takes the sentence at face value concludes there is a second guard on `AwaitingReviewers` when there is none.

SMALLEST CORRECTION. Restate the retained set as the two states increment 1's own criterion 7 samples, `AwaitingFirstReview` and `AwaitingFixes`, and require the control to redden on both keys for each of the other seven variants. That is strictly stronger, costs nothing, and removes the false claim. If the four-state set is kept for any other reason, drop the "the states the projection checks already sample" justification and name the set outright.

### `R2C-3`. `docs/plans/TEMPLATE.md` changes three times over, not twice; the third cause is unnamed

- OWNER: `step-intent-encoding-inc3`.
- SEVERITY: `low`.
- CLASS: 2, in-increment figure that does not reproduce.

EVIDENCE. `:741` reads: "So the committed projection changes TWICE OVER, once from the placeholder values and once from the corrected example-step sentence." The enumeration is short by one. The same increment adds the duty (g) sentence to `pack/plan-template.documentation-protocol.md` and requires "The same placement ... in the committed copy `docs/plans/TEMPLATE.documentation-protocol.md`" (`:737`). That committed copy is a front sidecar of the template plan: `docs/plans/TEMPLATE.plan.toml` lists `TEMPLATE.documentation-protocol.md` in `[meta.sidecars].front`, and `render` splices it into `docs/plans/TEMPLATE.md`, where its body is present today.

I demonstrated the third cause in isolation. I copied the whole `docs/plans/TEMPLATE` family into my scratch child, confirmed `render --check TEMPLATE.plan.toml --strict` reports `up to date` on the copy, appended ONLY the duty (g) sentence to `TEMPLATE.documentation-protocol.md`, re-rendered, and diffed against the committed projection:

```text
@@ -16,6 +16,8 @@
 <How this plan is kept current during the work. ... edits are overwritten by the next render.>

+A Step Detail below its own heading line must not repeat a `[[step]]` field. The heading line is the exception, and `render` takes it over later.
+
 ## Repository Layout and Current Architecture
```

One edit, neither of the two named causes, and the committed projection moves.

Nothing passes or fails wrongly because of this: `docs/plans/TEMPLATE.md` is in criterion 9's path set (`:927`), and criterion 11 (`:935`) requires `render --check --strict docs/plans/TEMPLATE.plan.toml` to print `up to date`, so a correct implementation regenerates it whatever the cause count says. The defect is that the paragraph exists to justify why the path is not optional and to name every reason it moves, and `:931` promises that the omitted paths "ARE NAMED HERE WITH THEIR REASONS". A reader auditing the path set against the stated reasons finds one reason missing, which is the same class of gap the paragraph was written to close.

SMALLEST CORRECTION. Change "twice over" to "three times over" and add the third cause: the duty (g) sentence added to `docs/plans/TEMPLATE.documentation-protocol.md`, which `render` splices into `docs/plans/TEMPLATE.md` as a front sidecar.

## Checked and deliberately not raised

Recorded so the triager can see these were examined and dismissed on their merits, not missed.

- THE HOW-TO-ADD-A-STEP SENTENCE STAYS INSIDE THE ANGLE-BRACKET NOTE. `pack/plan-template.steps/example-step.md:3` carries the sentence inside the one placeholder note the adopter's planner is told to delete (`pack/prompts/planner.md:5`), and criterion 5 (`:890-894`) pins its content on both sides of the pair but not its placement, unlike criterion 6, which pins both for the documentation-protocol sentence. I do not raise this. The two files differ in purpose: the documentation-protocol sentence is a standing rule that must survive into the adopter's own plan, which is why `:737` specifies its placement, whereas the example-step body IS the placeholder and is meant to be replaced wholesale. I could construct no wrong implementation that both passes and violates a risk ground, a numbered RULE or a cited Principle, and I will not file a finding I cannot place in either class.
- `context["problem"]` VERSUS THE ACCUMULATING TRAVERSAL. `:320` writes the comparison as an index expression, while `:324` requires the test to accumulate a mismatch for each absent key rather than stop at the first failure; a literal `Index` on a `BTreeMap` panics on an absent key and would make the control's required record unobtainable. A `get`-based read satisfies both readings, which is what my replica used, and the accumulation sentence plainly governs. Wording tension only; it neither admits a wrong implementation nor refuses a correct one.
- STRUCTURAL CLAUSES WITH NO COMMAND. `:322`'s "the macro invocation is the only state list in the test" is checked by reading a diff rather than by a command. Every prose criterion in this sidecar shares that property, and the clause explicitly names the shape it refuses, so a reviewer can apply it.
- SETTLED ITEMS. I did not re-open FR1-1, FR1-3, FR1-4, `I2`, `I6`, `I7`, `D7`, `T7a` through `T7f`, `PE1C-3`, `GB-4`, `GB-9`, `F2` or `F3`. In particular criterion 7's `reviews/...` context literals (FR1-4) and the changelog content gap (FR1-3) are untouched here; I found no evidence that moves either settled boundary. No waiver is claimed and none is authorised.

## Per-loop outcome

Both loops entered this round with the full two-clean-round bar under the human foreclosure decision, option A. Applying the brief's stop condition (clean means zero class 1, at most three `low` or `medium` class 2 findings, and no finding outside both classes):

| Loop | Entering streak | Findings | Severities | Class 1 / class 2 / neither | Outcome | Resulting streak | Converged |
| --- | ---: | ---: | --- | --- | --- | ---: | --- |
| `step-intent-encoding-inc1` | 0 | 2 (`R2C-1`, `R2C-2`) | low, low | 0 / 2 / 0 | clean | 1 | no |
| `step-intent-encoding-inc3` | 1 | 1 (`R2C-3`) | low | 0 / 1 / 0 | clean | 2 | yes |

Increment 1 is clean: FR1-2 is closed by construction and both of my findings are `low` class 2, within the three permitted. It reaches streak 1 and needs one further consecutive clean round. Increment 3 is clean with one `low` class 2 finding, reaches streak 2 and converges. Three reset rounds would remain for increment 1 after this round.

This is a reviewer's report, not a verdict: the triager owns the classes, the severities and both outcomes.

## Totals and backstop

- Raw findings: 3.
- Distinct findings: 3 (no duplicates within this file).
- Class totals: 0 class 1, 3 class 2, 0 outside both classes.
- Severity ceiling: `low`.
- Dismissals proposed: none, so no backstop re-check is owed from this file.
- Residual acceptance or waiver proposed: none.
