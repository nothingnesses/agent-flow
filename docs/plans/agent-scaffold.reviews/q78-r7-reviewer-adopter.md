# Review: `Q-78` design pass, round 3 of the reset count, ADOPTER AND EXECUTABILITY lens

Reviewer worktree: `.claude/worktrees/q78-r7-adopter`, branch `review/q78-r7-adopter`.
Brief: `docs/plans/agent-scaffold.reviews/q78-r7-brief-adopter.md`.

## What this lens asked

1. THE ADOPTER QUESTION. What must a project that scaffolds from the new pack write before its plan parses? Answered by construction, against a real scaffolded tree.
2. THE EXECUTABILITY QUESTION. Can an implementer execute each increment as written, in the declared order, using only the commands the sidecar states? Answered by running them.

## Summary

Seven findings, all distinct, severity ceiling HIGH.

| Id | Severity | One line |
| --- | --- | --- |
| F1 | high | `pack/AGENTS.md:30` tells every scaffolded project a `[[step]]` carries `order`. No increment corrects it, and both that could have would fail their own path-set criterion for doing so. |
| F2 | medium | Increment 3's changed-path set forbids re-rendering `docs/plans/TEMPLATE.md`, which a correct implementation must re-render. |
| F3 | high | The pack's one how-to-add-a-step sentence becomes a recipe for a plan that does not parse, and no increment updates it. |
| F4 | medium | `next` and `status` report success and exit 0 on the plan the flip breaks. The mechanism is pre-existing but the pass makes the route routine, and no residual records it. |
| F5 | low | The pack prose rule increment 3 ships can land inside an angle-bracket placeholder the pack tells the adopter's planner to delete, and criterion 6 passes either way. |
| F6 | medium | The two increments that break every existing plan carry no documentation impact, against this plan's own per-change convention, and their exact path sets forbid a `CHANGELOG.md` entry. |
| F7 | medium | Rule 9 states a population of 45 that its own criterion 6 and the sibling sidecar both put at 36. Acting on the 45 mutilates nine legitimate problem statements and no criterion detects it. |

THE ANSWER TO QUESTION 1, in one line: a FRESH scaffold costs an adopter nothing, and everything else costs three edit passes and four `validate` runs, with the pack's own guidance still pointing at the old shape.

THE ANSWER TO QUESTION 2, in one line: every increment is executable as written and every stated figure reproduced exactly, with two exceptions that are both changed-path sets rather than criteria (F2 and F6) and one wrong population figure (F7).

FOUR OF THE SEVEN ARE THE SAME MISS. F1, F3, F5 and F6 are all pack or documentation surfaces that no `slug = ` or `order = ` search reaches, in a pass whose two schema steps establish their scope by exactly those searches.

## Method, so every measurement below is reproducible

Fixture root: the session scratchpad, subdirectory `adopter/`. Every scaffold used the command the brief names, never `just scaffold-self`.

THE POST-CHANGE BINARY WAS BUILT, NOT IMAGINED. A copy of the worktree at `adopter/postchange` carries the end state the five sidecars specify, applied minimally:

- `src/plan/source.rs`: `order: u64` deleted from `Step`, and `problem: String` and `approach: String` added immediately after `status`, both bare (no `serde` default), which is increment 3's PREMISE.
- `src/plan/render.rs`: the `sort_by(order, slug)` deleted so declaration order stands, and `step_details_section` splices the two `- problem:` / `- approach:` lines after the leading heading line, per increment 1's render rule.
- `src/next.rs`: `StepInfo.order` deleted, and the three `min_by_key` arms of `select_active_loop` became first-match.
- `pack/plan-template.plan.toml` and `docs/plans/TEMPLATE.plan.toml`: `order = 1` deleted, the two placeholder values added, per increment 3.

`cargo build` succeeds on that tree. Every "MEASURED" line below is output from that binary or from the worktree's own `target/debug/agent-flow`, quoted verbatim.

ONE FACT ABOUT THE BUILD, RECORDED BECAUSE IT COSTS AN IMPLEMENTER TIME. The pack is embedded into the binary at compile time, so an edit to `pack/plan-template.plan.toml` does not reach `scaffold` until the binary is rebuilt. A first attempt at the measurements below scaffolded the OLD template from a stale binary and produced a parse error that had nothing to do with the change.

## Findings

### F1. The shipped pack tells every scaffolded project that a `[[step]]` carries `order`, and no increment in the pass corrects it. Severity: HIGH

`pack/AGENTS.md:30` reads, of the plan source:

> the `<task>.plan.toml` skeleton holds the Roadmap (`[[step]]` entries with status and order)

That is the only enumeration of the `[[step]]` field set anywhere in the shipped pack. `pack/pack.toml:28-29` copies `pack/AGENTS.md` to `AGENTS.md`, and `pack/pack.toml:99-100` copies the same file to `.agents/AGENTS.reference.md`, so every scaffolded project receives TWO copies of the sentence. MEASURED on a fresh scaffold from the current pack:

```
$ /usr/bin/grep -c 'entries with status and order' AGENTS.md .agents/AGENTS.reference.md
AGENTS.md:1
.agents/AGENTS.reference.md:1
```

`plan-order-array-position` deletes `order`. After the deletion an agent that follows that sentence writes `order = N` and the project's plan stops parsing. MEASURED with the post-change binary, against a scaffolded tree whose one step carries `order = 1`:

```
error: could not render docs/plans/TEMPLATE.plan.toml: malformed `<task>.plan.toml`: TOML parse error at line 37, column 1
   |
37 | order = 1
   | ^^^^^
unknown field `order`, expected one of `slug`, `title`, `status`, `problem`, `approach`, `blocked_by`, `folds`, `provenance`, `increment`, `waiver`
```

`scaffold` itself exits 2 there and leaves the project WITHOUT `docs/plans/TEMPLATE.md`, measured by listing `docs/plans/` after the failed run.

NO INCREMENT IN THE PASS REACHES THE SENTENCE, and each exclusion is explicit rather than incidental:

- `plan-order-array-position` increment 1, criterion 8, gives an exact 16-path list. `pack/AGENTS.md` is not on it, and the only `pack/` entry is `pack/plan-template.plan.toml`.
- `plan-order-array-position` increment 2, criterion 5: "No file under `src/`, `tests/` or `pack/` appears."
- `step-intent-encoding` increment 3, criterion 9, lists the 12 declaration-site files plus `docs/plans/agent-scaffold.md` plus the two `documentation-protocol` files plus the deleted migration record. `pack/AGENTS.md` is not among them.
- `sidecar-status-opening-drift`, DOCUMENTATION IMPACT: "The pack is untouched by this step."

The declaration-site search each step uses cannot find it, and that is why it was missed. Both searches anchor on a TOML assignment (`(\\n|^)order = ` and `(\\n|^)slug = `). MEASURED, both return exactly the 12 files and the counts the two sidecars tabulate, so the searches are correct for what they search. The sentence is prose, and prose is outside them.

The fix is not a one-file edit either. `cmp AGENTS.md pack/AGENTS.md` exits 1 (they differ at line 41, by design), and `the_committed_scaffold_matches_a_fresh_render` in `src/agents_md_drift.rs:377` pins the committed root `AGENTS.md` against a fresh render of the pack source. So correcting `pack/AGENTS.md` forces a matching edit to the root `AGENTS.md`, and `cargo test` fails until both move. Two files, neither in any changed-path set in the pass, and both increments that could carry the edit have a criterion that would then fail the implementer for making it.

`step-intent-encoding` increment 3 already ships one pack prose edit for exactly this class of reason ("The rule rides in this increment rather than elsewhere because this increment already edits the pack"), so the pass has a home for the edit and did not use it.

### F2. Increment 3's changed-path set forbids re-rendering `docs/plans/TEMPLATE.md`, which a correct implementation must re-render. Severity: MEDIUM

`docs/plans/TEMPLATE.md` is committed (`git ls-files 'docs/plans/TEMPLATE*'` lists it) and is a rendered artefact: `pack/pack.toml:36-37` records that `scaffold` renders it rather than dropping it, and MEASURED on the untouched worktree, `render --check --strict docs/plans/TEMPLATE.plan.toml` prints `docs/plans/TEMPLATE.plan.toml: up to date` and exits 0.

`docs/plans/TEMPLATE.plan.toml` is site 1 of the 69 declaration sites increment 3 criterion 2 requires to carry both fields, and increment 3 states outright that it "ships placeholder values". Increment 1's render rule then puts two new lines into the Step Details body. So the committed `docs/plans/TEMPLATE.md` changes.

MEASURED on the post-change tree, before re-rendering:

```
$ ./target/debug/agent-flow render --check docs/plans/TEMPLATE.plan.toml --strict
error: docs/plans/TEMPLATE.md differs from a fresh render (a hand-edit, or a stale render after a source edit) (first difference at line 51: expected "- problem: <the problem this step addresses>", committed "<What this step does and how; once done, the outcome and the evidence. To add a ...")
exit=1
```

and after `render docs/plans/TEMPLATE.plan.toml`, `git diff --name-only` lists `docs/plans/TEMPLATE.md`.

Increment 3 criterion 9 enumerates the changed-path set and does not list it. An implementer who obeys criterion 9 commits a stale committed `docs/plans/TEMPLATE.md`. An implementer who re-renders fails criterion 9. Nothing else in the pass detects the stale state: MEASURED, `/usr/bin/grep -rn 'TEMPLATE' justfile .agents/checks.toml` prints nothing, so no recipe and no declared check renders or checks that pair, and `src/agents_md_drift.rs:60` names "the `docs/plans/TEMPLATE` family" as the worked example of what its guard does NOT cover.

THE ADOPTER IS NOT BROKEN BY THIS, and the finding is scoped accordingly: `scaffold` re-renders `TEMPLATE.md` into the target project rather than copying the committed one, MEASURED, so a fresh scaffold is correct either way. What ships stale is this repository's own committed copy, and what is unbuildable as written is criterion 9.

The sibling increment is right where this one is wrong. `plan-order-array-position` increment 1 also edits `docs/plans/TEMPLATE.plan.toml`, and its criterion 8 also omits `docs/plans/TEMPLATE.md`, correctly: `render` emits no order column and the template holds one step, so deleting `order` leaves the projection byte-identical. The two increments differ in whether the edit reaches the projection, and only increment 3's does.

### F3. The one shipped sentence that tells an adopter how to add a step becomes insufficient, and no increment updates it. Severity: HIGH

`pack/plan-template.steps/example-step.md:3` carries the whole of the pack's how-to-add-a-step guidance:

> To add a step, add a `[[step]]` entry to the `.plan.toml` and a matching `<slug>.md` body sidecar in this directory, then re-render.

MEASURED, that is the only such sentence in the pack: `/usr/bin/grep -rn 'add a step\|add a \[\[step\]\]\|new step' pack/` returns that one line and nothing else. `pack/pack.toml:84-85` copies the file to `docs/plans/TEMPLATE.steps/example-step.md`, and MEASURED on a fresh scaffold, `render` inlines it into `docs/plans/TEMPLATE.md` directly under the example step's own heading.

After increment 3 the sentence is not merely incomplete, it is a recipe that produces a plan that does not parse. THIS IS THE ADOPTER COST, MEASURED BY FOLLOWING THE SENTENCE LITERALLY. On a tree scaffolded from the updated pack with the post-change binary, appending a `[[step]]` block carrying `slug`, `title` and `status`, writing the matching sidecar, and re-rendering as instructed:

```
$ agent-flow render docs/plans/TEMPLATE.plan.toml
docs/plans/TEMPLATE.plan.toml: malformed `<task>.plan.toml`: TOML parse error at line 61, column 1
   |
61 | [[step]]
   | ^^^^^^^^
missing field `problem`

render exit=1
```

```
$ agent-flow validate --source docs/plans/TEMPLATE.plan.toml
no metrics log at docs/metrics/workflow.jsonl; nothing to validate
docs/plans/TEMPLATE.plan.toml: malformed `<task>.plan.toml`: TOML parse error at line 61, column 1
   |
61 | [[step]]
   | ^^^^^^^^
missing field `problem`

validate exit=1
```

The parse aborts on the first missing field, so the operator learns about `approach` only after supplying `problem` and re-running. Two edits, two runs.

`pack/plan-template.steps/example-step.md` is in no changed-path set in the pass. Increment 3's criterion 9 does not list it. `sidecar-status-opening-drift` reads this exact file in its DOCUMENTATION IMPACT block and concludes "no shipped guidance, prompt or template goes stale", which is true of the status-token deletion and false of the required-field flip, and that step declares "This step touches no file under `pack/`."

Increment 3 already knows the cost. Its own WHAT THIS COSTS A SCAFFOLDED PROJECT paragraph says "adding a step to any scaffolded plan requires two prose sentences before the plan parses". It states the cost and schedules no edit to the one shipped sentence that tells an adopter what to write, in the increment that already opens the pack and already carries a pack prose edit and a rendered-pair check for it.

### F4. `next` reports success on the plan the flip breaks, so the adopter's failure is silent on the surface the workflow reads. Severity: MEDIUM

Same tree, same non-parsing plan as F3, and the same command an agent runs to find its work:

```
$ agent-flow next --source docs/plans/TEMPLATE.plan.toml
note: --source docs/plans/TEMPLATE.plan.toml did not parse as a `<task>.plan.toml`; projecting from --plan
task: TEMPLATE
source: no plan source
metrics: no log found

no active review loop (no plan steps found)
exit=0
```

```
$ agent-flow next --source docs/plans/TEMPLATE.plan.toml --json
{
  "task": "TEMPLATE",
  "source": "no plan source",
  ...
  "no_active_loop_reason": "no-plan-steps"
}
exit=0
```

The plan has two steps. `next` reports none, gives the reason as `no-plan-steps` rather than as a parse failure, and exits 0.

THE MECHANISM IS PRE-EXISTING AND I AM NOT REPORTING IT AS NEW. MEASURED with the worktree's own unmodified `target/debug/agent-flow`, a plan whose step omits the already-required `title` produces the byte-identical shape: the same note, the same `no active review loop (no plan steps found)`, the same exit 0. What the pass changes is the frequency: it adds two required fields whose omission is the DEFAULT outcome of following the pack's own instruction (F3), so a route that previously needed a typo now needs only obedience.

IT IS ALSO NOT COVERED BY THE STEP THAT WOULD OTHERWISE OWN IT. `validate-missing-source-exit` excludes `next` under NOT IN SCOPE, and the exclusion is written for "EVERY OTHER SUBCOMMAND THAT SKIPS A MISSING PATH". This path is not missing. It exists, it is named explicitly, and it fails to parse, which is a case that exclusion does not describe. `validate` handles it correctly (exit 1, quoted above). `next` does not. The step's own governing rule, quoted from the product's `--workflow` help, is "a check that did not run must not report success".

I am not asking for this to be fixed in this pass. The finding is that the adopter cost the pass states is understated by the surface the cost lands on, and that the residual is not recorded anywhere. Increment 3's THE RESIDUALS block records three residuals and this is not one of them.

### F5. The pack prose rule increment 3 ships can be deleted by the first planner that follows the pack's own instruction, and criterion 6 passes either way. Severity: LOW

Increment 3 ships this sentence into `pack/plan-template.documentation-protocol.md`:

> A Step Detail below its own heading line must not repeat a `[[step]]` field. The heading line is the exception, and `render` takes it over later.

MEASURED, the entire body of that file is one angle-bracket placeholder note:

```
$ cat pack/plan-template.documentation-protocol.md
## Documentation Protocol

<How this plan is kept current during the work. The structured `<task>.plan.toml` is the single source of truth: ... Never hand-edit the generated view; edits are overwritten by the next render.>
```

and `pack/prompts/planner.md:5` directs the adopter's planner: "Delete the template's angle-bracket placeholder notes as you fill each part in."

So the sentence's fate turns on whether it lands inside the angle brackets or outside them, and increment 3 does not say which. Its criterion 6 is

```
grep -c -F -- 'must not repeat a `[[step]]` field' pack/plan-template.documentation-protocol.md
```

which prints `1` in both placements, so the criterion cannot separate a rule that survives into the adopter's plan from one the first planner deletes on sight. The same ambiguity carries into the paired check against `docs/plans/TEMPLATE.documentation-protocol.md`, since that file is a verbatim copy.

### F6. Two increments break every existing plan and neither carries a documentation impact, against this plan's own convention for exactly that. Severity: MEDIUM

MEASURED, of the five sidecars in scope only one carries a DOCUMENTATION IMPACT section:

```
$ for f in step-intent-encoding plan-order-array-position sidecar-status-opening-drift ledger-order-citation-currency validate-missing-source-exit; do printf '%s: ' "$f"; /usr/bin/grep -c 'DOCUMENTATION IMPACT' docs/plans/agent-scaffold.steps/$f.md; done
step-intent-encoding: 0
plan-order-array-position: 0
sidecar-status-opening-drift: 1
ledger-order-citation-currency: 0
validate-missing-source-exit: 0
```

The one that has it is the step that ships nothing. The two that break every previously valid plan in every scaffolded project have none, and so does the one that flips a shipped exit code.

THE CONVENTION IS THIS PLAN'S OWN, AND IT IS PER-CHANGE RATHER THAN PER-RELEASE. `docs/plans/agent-scaffold.steps/validation-constraints.md:171` names, in the documentation impact of a comparable pending step, "`CHANGELOG.md`, the `## [Unreleased]` section" and states why: "The narrowing is a behaviour change to `validate --workflow` and the population it affects must be named." Lines 177 and 181 repeat `CHANGELOG.md` for two further increments of the same step. `AGENTS.md:30` states the duty itself: "the planner also assesses that change's documentation impact: it identifies which docs and prompts the change will make stale, so keeping them current is planned work rather than an afterthought."

The changes at issue are strictly larger than the ones that convention covers. `CHANGELOG.md`'s own `[0.0.3]` entry documents a BREAKING rename with an explicit upgrade recipe and closes with "a project scaffolded by 0.0.2 needs no migration beyond the command name". The `Q-78` pass gives every scaffolded project a plan that no longer parses, which is a migration.

AND THE PATH SETS DO NOT MERELY OMIT THE ENTRY, THEY FORBID IT. `plan-order-array-position` increment 1 criterion 8 reads "`git diff --name-only` over the increment lists exactly:" followed by 16 paths. `step-intent-encoding` increment 3 criterion 9 enumerates its set the same way. An implementer who writes the CHANGELOG entry fails the criterion. One who satisfies the criterion ships the break undocumented.

Two narrowings, so this is not read as more than it is. `README.md` is NOT made stale: MEASURED, `/usr/bin/grep -n 'order\|\[\[step\]\]' README.md` returns no enumeration of the `[[step]]` field set, only ordinary uses of the word, so the README needs no edit. And MEASURED, `CHANGELOG.md` has no `## [Unreleased]` section today (`/usr/bin/grep -n 'Unreleased' CHANGELOG.md` exits 1), so the entry means opening one rather than appending to one.

ONE ROOT CAUSE UNDERLIES F1, F3 AND F6. Each of the two schema steps establishes its changed-path set by a search anchored on a TOML assignment, then treats that set as complete. The searches are correct: MEASURED, both reproduce the 12 files and the per-file counts the two sidecars tabulate exactly. What neither step then does is the second half of `AGENTS.md:30`, the prose sweep for what the change makes stale. Every one of F1, F3 and F6 is a file that no `slug = ` or `order = ` search can reach.

### F7. `step-intent-encoding` rule 9 states a population of 45 that its own criterion 6 and the sibling sidecar both put at 36, and acting on the 45 damages nine problem statements that no criterion checks. Severity: MEDIUM

`docs/plans/agent-scaffold.steps/step-intent-encoding.md:51` reads:

> RULE 9, NO INTENT VALUE OPENS WITH A ROADMAP STATUS TOKEN. 45 sidecars open with a status token and rule 4 makes that opening the first source, so a transcription that starts at the opening word writes the token into the TOML. That re-creates the duplicate `sidecar-status-opening-drift` deletes. The transcription starts after the token.

45 is the RELAXED selector's count, not the count of openings that carry a status LABEL. MEASURED on this tree, by running `sidecar-status-opening-drift` criterion 1's two commands verbatim:

- the relaxed form (a token followed by punctuation, a space, or end of line) selects 45.
- the anchored form (the form criterion 1 actually specifies, and the form `step-intent-encoding`'s own R3 regex uses at criterion 6) selects 36.
- the complement is exactly 9: `se-principle-namespace`, `classification-trivial-rename`, `drift-guard-optionality`, `instrument-magic-filename`, `module-spec-description-dead`, `checks-kind-skip`, `sidecar-ref-empty-string`, `sidecar-ref-symlink`, `repoint-resume-prompts`.

THE FILE CONTRADICTS ITSELF ACROSS TWO PARAGRAPHS, AND THE LATER ONE IS RIGHT. `step-intent-encoding.md:422`, under criterion 6, states that an earlier unanchored form of R3 "fired" on the sentence "Deferred cleanup from the `Q-44` audit (`architecture-audit`), raised there and scheduled here.", that this sentence "is the faithful opening of six sidecars in this plan and a legitimate problem statement", and that "the anchored form does not fire on it". `sidecar-status-opening-drift.md:22` agrees and goes further: those nine "are NOT in this step's scope at all", "in all nine the word names what the step IS", and a rule that reached them "would have rewritten nine correct sentences to satisfy a criterion whose own scope excludes them".

Rule 9 asserts of all 45 that transcribing from the opening word "re-creates the duplicate `sidecar-status-opening-drift` deletes". That is false of nine of them: the drift step deletes nothing in those nine, by its own explicit exclusion.

THE CONSEQUENCE IS A WRONG EDIT THAT NOTHING DETECTS. Rule 9's operative instruction is "The transcription starts after the token." Applied to the nine, it turns "Deferred cleanup from the `Q-44` audit (`architecture-audit`), raised there and scheduled here." into "cleanup from the `Q-44` audit ...", which is exactly the legitimate problem statement rule 9's own file calls it, mutilated. No criterion in the batch block catches it: R3's regex is the anchored one and stays silent either way, R3b prints only values that the relaxed form reaches AND the anchored form does not, which is the wrong direction for this case, and criterion 12 belongs to the other step and runs over that step's worklist. Criterion 8's reading is the only thing left, and the sidecar itself calls that "the weakest guard this pass uses".

THE FIGURE IS ALSO WRONG AT EXECUTION TIME, FOR A SECOND AND INDEPENDENT REASON. MEASURED, the five steps sit at declaration positions 101 to 105 with these dependencies:

```
pos=101 "sidecar-status-opening-drift"    status="not-started" blocked_by = []
pos=102 "validate-missing-source-exit"    status="not-started" blocked_by = []
pos=103 "plan-order-array-position"       status="not-started" blocked_by = []
pos=104 "ledger-order-citation-currency"  status="not-started" blocked_by = []
pos=105 "step-intent-encoding"            status="not-started" blocked_by = ["plan-order-array-position"]
```

`select_active_loop`'s ready-to-plan arm takes the lowest-order ready pending step, so `sidecar-status-opening-drift` runs FIRST and `step-intent-encoding` runs LAST. By the time the backfill reads a sidecar opening as its source, the drift step has already deleted the token from its own worklist, which that sidecar puts at 36 minus its 19 handover files, so 17. The openings that still carry a token when rule 9 applies are the 19 handover files plus the 9 adjectival ones, not 45 and not 36.

The correct edit is small: state 36 as the label population, or state 19 as the population rule 9 will actually meet, and exclude the nine adjectival openings by name as both sibling paragraphs already do. I checked for re-discovery: no file under `docs/plans/agent-scaffold.reviews/` mentions rule 9, and `/usr/bin/grep -n 'rule 9\|RULE 9\|45 sidecar' docs/plans/agent-scaffold.ledger.md` returns no round record about it.

## The adopter cost, measured

This section answers question 1 directly. Every line is output from the post-change binary.

WHAT AN EXISTING SCAFFOLDED PROJECT SEES ON UPGRADE. A tree scaffolded by today's `agent-flow`, run against the post-change binary, with no edits:

| Command | Exit | Result |
| --- | --- | --- |
| `validate --source docs/plans/TEMPLATE.plan.toml` | 1 | ``unknown field `order` ``, correct |
| `render --check docs/plans/TEMPLATE.plan.toml --strict` | 1 | same message, correct |
| `next --source docs/plans/TEMPLATE.plan.toml` | 0 | `no active review loop (no plan steps found)`, WRONG |
| `status --source docs/plans/TEMPLATE.plan.toml` | 0 | `plan: not provided`, WRONG |

Two of the four surfaces report success on a plan that does not parse (F4).

The `validate` error is better than the sidecars promise, and that is worth recording as a credit rather than a finding. Its `expected one of` list names the two new fields, so the operator discovers the whole migration from the first message:

```
unknown field `order`, expected one of `slug`, `title`, `status`, `problem`, `approach`, `blocked_by`, `folds`, `provenance`, `increment`, `waiver`
```

WHAT THE OPERATOR MUST TYPE, AND HOW MANY TIMES. MEASURED on a three-step plan written before the change, fixing each reported class in bulk:

- Run 1: ``unknown field `order` `` at the first step. Delete every `order = ` line.
- Run 2: `` missing field `problem` `` at the first `[[step]]`. Add a `problem` line to every step.
- Run 3: `` missing field `approach` `` at the first `[[step]]`. Add an `approach` line to every step.
- Run 4: `p.plan.toml: 3 steps, 0 questions, valid`, exit 0.

FOUR `validate` runs and three edit passes, independent of the plan's size, because the parser aborts on the first failure and the failure class is uniform across steps. Per step the edit is one line deleted and two lines added, so a plan of N steps costs 3N line edits. On this repository's own plan that is 315 line edits, and the pass schedules them as six reviewed batch increments plus one deletion increment.

TWO SENTENCES PER STEP, INCLUDING THE STEPS THAT ARE ALREADY FINISHED. The required flip does not distinguish by status. MEASURED on the three-step fixture, the `complete` step and the `not-started` step each fail with the same `` missing field `problem` `` until both fields are supplied. Increment 3's cost paragraph names one hard case, "for an exploratory step the problem statement is often the thing the step exists to find out", and does not name this one: an adopter upgrading a real project must author retrospective intent for every step it has already finished and closed. That is where the placeholder pressure residual 2 accepts will actually land, and residual 2 does not say so.

WHAT A FRESH SCAFFOLD COSTS: NOTHING, AND THAT HALF OF THE DESIGN HOLDS. MEASURED on a tree scaffolded from the pack with the two placeholder values in place, with no hand editing:

```
$ agent-flow validate --source docs/plans/TEMPLATE.plan.toml
docs/plans/TEMPLATE.plan.toml: 1 steps, 0 questions, valid
exit=0

$ agent-flow render --check docs/plans/TEMPLATE.plan.toml --strict
docs/plans/TEMPLATE.plan.toml: up to date
exit=0

$ grep -c -F -- '- problem: <the problem this step addresses>' docs/plans/TEMPLATE.md
1
$ grep -c -F -- '- approach: <how this step addresses it>' docs/plans/TEMPLATE.md
1

$ cmp pack/plan-template.plan.toml docs/plans/TEMPLATE.plan.toml
(no output, exit 0)
```

Increment 3's criteria 3, 4 and 5 all pass by construction. The cost falls entirely on the SECOND step an adopter adds, which is F3.

## Executability: what I ran, and what reproduced

Question 2 asked whether an implementer can execute each increment as written using only the commands the sidecar states. I ran every capture, measurement and reproduction command the five sidecars state that can run against the pre-increment tree. EVERY ONE REPRODUCED ITS STATED FIGURE EXACTLY. No increment in scope has a criterion that cannot be evaluated for want of a command, and I found no wrong figure.

| Sidecar and command | Stated | Measured |
| --- | --- | --- |
| `step-intent-encoding` inc1 crit 10, batch boundaries | `steps=105 batches=6 size=18` | `steps=105 batches=6 size=18` |
| same, declared batch increments | `6` | `6` |
| `step-intent-encoding` inc1, leading-heading reproduce | `core-assets.md` and nothing else | exactly that |
| `step-intent-encoding` inc1 crit 7, pre-change `next` slots | prints `0`, exits 1 | `0`, exit 1 |
| `step-intent-encoding` inc1 crit 8, subcommand count | `8` | `8` |
| `step-intent-encoding` inc3, declaration-site search | 12 files, 69 sites, per-file table | reproduced row for row |
| `step-intent-encoding` batch crit 7, R4 on the untouched tree | `steps=105 source=0/0 quoted=1/1 projected=1/1` | identical |
| `step-intent-encoding` batch crit 7, empty question sidecars | prints nothing | `find ... -size +0` printed nothing, and 80 sidecars, all 0 bytes |
| `plan-order-array-position` inc1, declaration-site search | 12 files, 69 sites, per-file table | reproduced row for row |
| `plan-order-array-position` inc1, the one data move | `rename-to-agent-flow` | `out of place: "rename-to-agent-flow"` |
| `ledger-order-citation-currency`, population | `135` and `116` | `135` and `116` |
| `sidecar-status-opening-drift` crit 1, anchored selector | 36 | 36 |
| same, relaxed selector | 45 | 45 |
| same, complement | 9 adjectival `deferred` openings, named | exactly those 9 slugs |
| `validate-missing-source-exit` crit 10, "the pack ships no `validate` invocation" | true | true, no `agent-flow validate` anywhere under `pack/` |
| `step-intent-encoding` inc3 crit 3, `scaffold --vcs none` | flag exists | `--vcs <VCS>` present in `scaffold --help` |
| `step-intent-encoding` inc1, `status --step` conflicts with `--resume` | buildable | `status --resume` exists, and `--ledger-fragment` already carries a clap `requires` relation |

## Gates, run from the worktree root

All six green on the pre-increment tree, so nothing below is confounded by a broken baseline.

| Gate | Result |
| --- | --- |
| `cargo test` | exit 0, no failures |
| `cargo clippy --all-targets -- -D warnings` | exit 0 |
| `validate --source ... --metrics ...` | `docs/plans/agent-scaffold.plan.toml: 105 steps, 80 questions, valid`, exit 0 |
| `validate --source ... --workflow` | `workflow invariants hold`, exit 0 |
| `render --check --strict docs/plans/agent-scaffold.plan.toml` | `up to date`, exit 0 |
| `LC_ALL=C grep -rcP '[^\t\x20-\x7e]' docs/plans/` | no file with a non-zero count |

Every gate line ran. `render --check --strict` runs correctly with the `<PLAN>` argument supplied, which is the form the brief gives.
