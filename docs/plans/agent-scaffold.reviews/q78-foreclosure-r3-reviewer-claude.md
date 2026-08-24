# Q-78 post-escalation round 3 Claude review

## Scope, method and gates

I reviewed `step-intent-encoding-inc1` only, in my own worktree on `review/q78-foreclosure-r3-claude`, whose tree is identical to `plan/q78-design-pass` at `44ab967` (`git diff --stat plan/q78-design-pass HEAD` is empty). I did not read the GPT round 3 review. I edited no product.

I read `AGENTS.md`, the ledger from `RESUME HERE` (`docs/plans/agent-scaffold.ledger.md:535-543`), `q78-foreclosure-r2-triage.md`, the round 1 triage and fix brief for the settled set, and the complete `step-intent-encoding-inc1` block (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:59-454`), plus the rules and increment 3 material it cross-references.

Every project command ran through `direnv exec .` with the project's Nix development environment. My build target, fixtures, countermodel plans and command output are all under the authorised child directory `/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-foreclosure-r3-claude/reviewer`, with `CARGO_TARGET_DIR` inside it. I used no bare `/tmp` path and deleted nothing. GNU grep 3.12 served every GNU-regex claim.

Baseline gates, all green on `44ab967`:

- `validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl`: 454 records, 105 steps, 81 questions, valid, exit 0.
- The same with `--workflow`: `workflow invariants hold`, exit 0.
- `render --check docs/plans/agent-scaffold.plan.toml --strict`: `up to date`, exit 0. Same for `docs/plans/TEMPLATE.plan.toml`.
- `cargo test`: 470 passed, 0 failed.
- `cargo clippy --all-targets --all-features -- -D warnings`: exit 0.
- `git status --short` empty; `git diff --check` exit 0.

## Product state and fix verification

There was no intervening product change, as the ledger directs: `git diff c54a0b9 HEAD -- docs/plans/agent-scaffold.steps/step-intent-encoding.md` is empty, so this round judges the same sidecar bytes round 2 judged. `R2-1` and `R2-2` therefore stand unfixed as permitted class 2 findings; I did not re-raise them and found no evidence that moves either boundary.

I re-verified the round 1 fix (`FR1-2`) against the current tree rather than taking round 2's word for it. The `LoopState` enum has exactly the nine variants the seam table names, `ReadyToPlan`, `Blocked`, `AwaitingFirstReview`, `AwaitingFixes`, `AwaitingReviewers`, `Converged`, `Escalate`, `RiskClassConflict` and `Done` (`src/next.rs:273-304`), matching `step-intent-encoding.md:320`. `build_context` (`src/next.rs:993-1021`) is a `BTreeMap` with a no-wildcard `match` over all nine, so the macro-generated exhaustive match at `:322` does force a compile error on a new variant. The state-restriction control at `:324` names the five omitted states correctly.

I reproduced the two `next` states the criteria depend on with a triager-style scratch fixture rather than reasoning about them. A one-step `in-progress` TOML source with no round records gives `state: awaiting-first-review` with exactly the four non-intent context keys `isolation_tier`, `ledger`, `review_findings`, `triage_findings`, so criterion 7's six-key claim (`:112`) holds. The same source plus exactly one joined `new_valid` round record gives `state: awaiting-fixes` with exactly `isolation_tier`, `ledger`, `triage_findings`, so criterion 7's "exactly five keys" claim (`:294`) holds.

## Current-tree reconciliation

Every checkable claim inside the increment 1 block reproduced. Recorded so the triager can see what was measured rather than read.

| Claim | Site | Measured result |
| --- | --- | --- |
| Only `core-assets` opens without a `#` line; its heading sits at line 9 | `:107`, `:110` | The loop prints `docs/plans/agent-scaffold.steps/core-assets.md` and nothing else; `grep -n '^#'` gives line 9; the file opens "Decisions carried from the resolved open questions:" |
| The `N1` fixture is the first of three `slug = ` sites in `render.rs` | `:102` | `grep -nE '(\\n\|^)slug = ' src/plan/render.rs` prints lines 877, 1047, 1227; `empty_details_sections_emit_no_bare_heading` begins at 872 and its fixture is line 877 |
| `src/main.rs:496` is the new flag's declaration site | `:61` | Line 496 is `struct StatusArgs {`; `resume: bool` is declared there, so `conflicts_with = "resume"` resolves |
| `next`'s output is an instruction rather than a report, per `workflow-enforcement-tier.md` | `:61` | `docs/plans/agent-scaffold.steps/workflow-enforcement-tier.md:302` carries that exact blast-radius argument |
| `2 x $(grep -c '^\[\[step\]\]' ...)` is 210 | `:31`, `:198` | 105 steps, so 210 |
| A failing `validate --source` prints only its problem lines on stderr, prefixed `<path>: `, exit 1 | `:77`, `:191` | Two-error fixture: stdout empty, stderr exactly the problem lines, exit 1. So criterion 3's "exactly 2N stderr lines" is reachable |
| `--help` prints 8 command rows today | `:410` | The stated pipeline prints `8` |
| The clap conflict message and exit 2 | `:396` | The existing `--out`/`--json` pair prints `error: the argument '--out <OUT>' cannot be used with '--json'` and exits 2, first-provided argument named first, so `--step a --resume` yields the stated string |
| Criterion 10's sizing and manifest equality | `:414-436` | `steps=105 batches=6 size=18`; `declared_loops=6 manifest_batches=6`; 105 `^slug = ` lines equal 105 `^[[step]]` lines, so the `sed`/`awk` partition is total |
| The 69-site census | `:158` via `:749-772` | Reproduced exactly: 12 files, 69 sites, every row identical |
| `toml = "0.8"` is a normal dependency, so criterion 2's parser oracle is available | `:189` | `Cargo.toml:19` |
| The schema position "immediately after `status`" is available and has precedent | `:65` | `Step` declares `status` at `src/plan/source.rs:135`; `provenance` already uses `#[serde(default, skip_serializing_if = "Option::is_none")]` at `:151` |

## Findings

One finding, class 2, `low`. No class 1. No finding outside both classes.

### `R3C-1`. The increment says no `[[step]]` declaration site changes here, and its own criterion 4 changes at least six of them

- OWNER: `step-intent-encoding-inc1`.
- SEVERITY: `low`.
- CLASS: 2, in-increment claim that does not reproduce.

EVIDENCE. Two sentences of the increment's scope boundary assert that no `[[step]]` block gains a field in increment 1.

`:158` reads: "The 69 inline `[[step]]` declaration sites do NOT change in this increment, because both fields are optional. They all change in increment 3."

Acceptance criterion 11 (`:440`) repeats it: "`docs/plans/agent-scaffold.plan.toml` does NOT appear, because the six batch increments are declared in the plan pass rather than here, and no `[[step]]` field changes in this increment."

The 69 is not a loose figure. It is the census the same sidecar establishes by search at `:749-772`, and I reproduced it on this tree:

```text
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

12 files, 69 sites, every row identical to `:760-771`. Seven of the 69 are the `[[step]]` blocks of `src/plan/testdata/render-fixture.plan.toml`, which I confirmed carries exactly seven steps, `alpha`, `beta`, `gamma`, `delta`, `zeta`, `epsilon` and `eta`.

Increment 1's own criterion 4 (`:202`) requires those blocks to gain the fields: "`src/plan/testdata/render-fixture.plan.toml` gains both single-paragraph fields on `alpha`, both two-paragraph multiline fields on `gamma`, `problem` ALONE on `eta`, ... and both interior-line-whitespace fields on `beta` ... Its other existing steps retain the remaining shared-matrix cases so the fixture includes two consecutive blank logical lines, outer whitespace, CRLF and bare CR". Four sites are named outright. The remaining four matrix cases need two field slots each per step, so at least two of `delta`, `zeta` and `epsilon` must take fields too: at least six of the seven sites change in this increment, not in increment 3.

The contradiction is two lines wide. `:156` lists `src/plan/testdata/render-fixture.plan.toml` in the changed-path set, and `:158` immediately follows it saying the declaration sites do not change; criterion 11 lists the same path and then carries the same clause. So the sentence "They all change in increment 3" is false of at least six sites, and the criterion 11 clause is false unless the reader silently narrows it to `docs/plans/agent-scaffold.plan.toml` alone, which its wording does not do.

CONSEQUENCE, stated so it is not read as more. Nothing passes or fails wrongly. Criterion 11's pass condition is the exact `git diff --name-only` list, which includes the fixture, and criteria 4, 5 and 6 all require the fixture edit, so a correct implementation is not refused and a wrong one is not admitted. What is defective is the scope boundary as a readable statement, which is exactly what the "future changed-path boundary" audit consults: a later increment, or a reviewer checking whether a declaration site was already touched, is told here that increment 1 left all 69 alone.

CLASS, and why it is class 2 rather than outside both classes. This is the shape the round 2 triage gave `R2-2` and `R2-3`: an in-increment claim about a measured population whose measurement does not reproduce (`q78-foreclosure-r2-triage.md:54`, "a low class-2 in-increment non-reproducing figure"; `:60`, the `TEMPLATE.md` undercount). The clause also sits inside acceptance criterion 11, one of the three locations the figure test admits (ledger `:675`). Severity `low` on the same calibration: no criterion outcome moves, and the cost is a false statement in the increment's own enumeration of what it does and does not touch.

SMALLEST CORRECTION. Scope both sentences to the live plan, which is what they are actually about. At `:158`: say that no site in `docs/plans/agent-scaffold.plan.toml`, `pack/`, `src/` (outside the render fixture) or `tests/` changes here, that criterion 4 fills the seven render-fixture sites, and that the remaining 62 change in increment 3. At `:440`: change "no `[[step]]` field changes in this increment" to "no `[[step]]` field of `docs/plans/agent-scaffold.plan.toml` changes in this increment".

## Checked and deliberately not raised

Recorded so the triager can see these were examined and dismissed on their merits, not missed.

- THE `one_line` STRUCTURE CONTRACT AND THE NEW MULTILINE SITE. `src/plan/render.rs:539-553` states an invariant, "Every site that writes a free-text value onto a generated line passes through here", and names two trailing spaces as "a CommonMark hard break, which is a structure change of its own"; `one_line_neutralizes_every_line_ending_and_trims` (`src/plan/render.rs:1112`) pins it. Increment 1 opts out explicitly ("A dedicated multiline helper, not `one_line`", `:95`) and criterion 2 case (h) plus criteria 4, 6 and 8 require an interior line's two trailing spaces to survive into the golden, which is a hard break. I do not raise it. The same doc comment carves out exactly this case: the opaque multi-line blobs spliced verbatim are excluded because they are "not values on a generated line", and the intent block is a multi-line block, quoted more strictly than the sidecar bodies beside it. The purpose the comment states, that a value cannot fabricate a heading, a principle, a queue item or a table row, is fully served by the `> ` prefix, which no matrix row can escape. Nothing wrong passes and nothing correct is refused.
- INCREMENT 3'S CHANGELOG ENTRY DOES NOT MENTION INCREMENT 1'S USER-FACING SURFACE. The step's single DOCUMENTATION IMPACT section (`:947-949`) assigns one `## [Unreleased]` entry to increment 3 and enumerates its content as three schema facts. It names neither the new `status --step <slug>` flag and its JSON contract, nor `render`'s two new labelled blocks, nor the new `validate` empty-after-trim rejection, all of which increment 1 ships, and increment 1's criterion 11 forbids `CHANGELOG.md`. This is the closest call I made. I do not file it because its owner is increment 3's documentation-impact section and criterion 9, which this round's brief puts out of scope, and because it sits inside the area settled finding `FR1-3` already covers, that criterion 9 proves only that `CHANGELOG.md` changed and not what it contains. I claim no waiver and none is authorised; I record it here so the triager can overrule me if it reads the ownership differently.
- CRITERION 1 GREPS ONE FIELD AND NOT THE OTHER. `:162` is headed "THE SCHEMA CARRIES BOTH FIELDS" and runs `grep -c 'problem: Option<String>'` with no `approach` counterpart, which is the substitute-once shape increment 3's criterion 1 was rebuilt to refuse (`:782`). I could construct no implementation that survives it: an implementation missing `approach` from the schema fails criterion 3's per-field empty message and criteria 4, 6, 7 and 8's two-field matrices, and one defaulting `approach` to a bare `String` trips RULE 3 on the live plan and fails criterion 1 itself. An inconsistency in form, not a hole.
- CRITERION 12'S `grep -c` EXIT STATUS. `LC_ALL=C grep -cP '[^\t\x20-\x7e]' <file>` prints `0` and exits 1 on a clean file, which I confirmed on all eight changed source paths. Criterion 12 attaches its exit-0 requirements to `clippy` and `validate` and asks only that the grep "prints `0`", so the printed value is the oracle, as increment 3 criterion 6 says explicitly for its own grep. Not a defect, though the `&&`-chain trap is unremarked here.
- `jq` IS NOT IN THE DEV SHELL. `flake.nix`'s `devShells.default` does not list it; the `jq` that resolves under `direnv exec .` is inherited from the ambient environment. Criteria 7 and 8 name `jq -j` with no alternative. I do not raise it: both criteria make a named Rust test the real oracle for the same bytes, criterion 2 offers "a Rust string comparison" as an alternative outright, and `validation-constraints.md` already uses `jq` in this plan, so this is a project-wide convention rather than something this increment introduces.
- CRITERION 5'S LEAD-IN CLAUSE SITS OUTSIDE ITS OWN RANGE. The pass condition includes "The lead-in sentence remains above the heading and no intent label appears between them", but the `awk` range starts at the `gamma` heading and cannot show anything above it. The failure mode the criterion exists to refuse is still caught: a first-line insertion leaves the heading followed directly by the body, which fails the range. Wording only.
- TRAILING WHITESPACE IN THE REGENERATED GOLDEN. Criteria 4, 6 and 8 put lines ending in two spaces into `src/plan/testdata/render-fixture.md`, which `git diff --check` flags by default. No committed check refuses it: `.agents/checks.toml` declares only `render-check`, there is no `.gitattributes`, and `flake.nix` excludes `src/plan/testdata/render-fixture*` from treefmt so prettier cannot strip it back out. No criterion of this increment runs `git diff --check`.
- THE FIFTH INTERPOLATION SITE AND `F1`. `every_interpolated_free_text_site_stays_on_one_generated_line` (`src/plan/render.rs:1218`) is commented as covering "all four interpolation sites"; increment 1 adds a fifth into the same generated document. I could construct no implementation that both satisfies the byte-exact quoted-line criteria and fabricates a line, because every logical line takes a `> ` or `>` prefix, so the guard's property holds by construction. The stale "four" in a code comment lives in `src/plan/render.rs`, which is already in the changed-path set.
- SETTLED ITEMS. I did not re-open `R2-1`, `R2-2`, `R2-3`, `FR1-1`, `FR1-3`, `FR1-4`, `PE1C-3`, `I2`, `I6`, `I7`, `D7`, `T7a` through `T7f`, `GPT-R2-5`, `GPT-R3-2`, `GB-4`, `GB-9`, `F2` or `F3`. In particular criterion 7's `reviews/...` context literals (`FR1-4`) and the empty-versus-whitespace-only distinction (`GB-4`) are untouched here; I found no evidence that moves either settled boundary. No waiver is claimed and none is authorised.

## Per-loop outcome

`step-intent-encoding-inc1` is `risky` (`docs/plans/agent-scaffold.plan.toml:1596-1597`), entered this round at streak one, and converges on a clean round. Applying the brief's stop condition, clean means zero class 1, at most three `low` or `medium` class 2 findings, and no finding outside those classes:

| Loop | Entering streak | Findings | Severities | Class 1 / class 2 / neither | Outcome | Resulting streak | Converged |
| --- | ---: | ---: | --- | --- | --- | ---: | --- |
| `step-intent-encoding-inc1` | 1 | 1 (`R3C-1`) | low | 0 / 1 / 0 | clean | 2 | yes |

This is a reviewer's report, not a verdict: the triager owns the class, the severity and the outcome.

## Totals and backstop

- Raw findings: 1.
- Distinct findings: 1 (no duplicates within this file).
- Class totals: 0 class 1, 1 class 2, 0 outside both classes.
- Severity ceiling: `low`.
- Dismissals proposed: none, so no backstop re-check is owed from this file.
- Residual acceptance or waiver proposed: none.
