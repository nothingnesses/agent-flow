# Q-78 reset round 3 Claude review

Independent reviewer, adoption / executability / fix-verification lens. Target: `plan/q78-design-pass` after `bf13e6f`, judged at branch tip `9c62277`, with the round 3 review briefs excluded from the product. No reset round 3 reviewer file was read.

## Method

I read `AGENTS.md`, the ledger from `RESUME HERE` (`docs/plans/agent-scaffold.ledger.md:535`), `q78-reset-r2-triage.md`, `q78-reset-r2-fix-brief.md`, the plan TOML, the generated view, the `Q-78` exploration, the `Q-78` and `Q-81` question items, and the five active increment sidecars. I then re-ran every command those sidecars cite that is runnable on today's tree, rebuilt the `Q-78` matrix against the workspace `toml` crate, and rebuilt criterion 6 of the drift step against a throwaway git repository.

All fixtures live under the brief's scratch root, in the reviewer-owned child directory `.../q78-reset-r3-claude/`. No bare `/tmp` path was used and no wildcard deletion was run.

TOOLCHAIN DEVIATION, DISCLOSED RATHER THAN PAPERED OVER. The brief requires the project direnv environment. `direnv` is present in this session (`/nix/store/1majrhkds58pykw8syjsgwdk022ncmxk-direnv-2.37.1/bin/direnv`, version 2.37.1) and loads `.envrc`, but it then reports `nix-direnv: Could not find Nix binary, please add Nix to PATH`: no `nix` binary exists in this sandbox and `/nix/var/nix/profiles/default` is absent, so the flake devShell cannot be instantiated. I therefore ran every toolchain command against a pinned store toolchain, `rustc`/`cargo` 1.94.0 from `/nix/store/91ay3rkmph1sc7avfwmj0f9v26wk9jy5-rust-default-1.94.0`, with `CARGO_HOME` and `CARGO_TARGET_DIR` inside the scratch root so nothing was written into the worktree. GNU grep 3.12 was invoked by absolute path (`/nix/store/gn94gpcp5q08x4v6g8mvw8v4r65rcjzk-gnugrep-3.12/bin/grep`), because in this harness the bare name `grep` is a shell function that dispatches to `ugrep`; every GNU-behaviour claim below was measured with GNU grep. The gates ran green on that toolchain, which is evidence about this tree and not a substitute for the project shell: `cargo test` 470 passed / 0 failed across 12 suites, `cargo clippy --all-targets -- -D warnings` exit 0, `validate --source ... --metrics ...` printing `440 records, valid` and `105 steps, 81 questions, valid`, `validate ... --workflow` printing `workflow invariants hold`, and `render --check --strict` printing `up to date`. A reviewer with the project shell should re-run them there.

## Findings

Six findings. Four are class 1 and all four sit in `step-intent-encoding-inc1`. Severity ceiling `medium`.

### `C3-1` -- RULE 10's whole-value trim clause is unfalsifiable across the entire criterion 2 matrix

- OWNING INCREMENT: `step-intent-encoding-inc1`.
- SEVERITY: `medium`. PROPOSED CLASS: 1.
- RULE VIOLATED: RULE 10 (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:53`), "only leading and trailing whitespace around the whole value is trimmed for display", restated for the render helper at `:95` ("trims only the whole value for display").

THE HOLE. Criterion 2's matrix is (a) single paragraph, (b) two paragraphs, (c) `paragraph one\n\n\nparagraph two`, (d) `  paragraph one\nparagraph two  `, (e) CRLF, (f) bare CR, (g) an escaped continuation (`:164`). Case (d) is the only case carrying whitespace, and it carries it at the two outer extremities of the value, which is exactly where a whole-value trim and a per-line trim agree. No matrix case carries whitespace at the start or end of an INTERIOR logical line, so an implementation that trims EVERY logical line rather than only the whole value produces byte-identical output on every row of the matrix, on all three human surfaces, and against the criterion 4 reference formatter built from the same matrix.

MEASURED. A scratch crate deserialised the complete matrix with the workspace's `toml` dependency and ran two helpers over each value: `rule10` (normalise CRLF and CR to LF, trim the whole value, prefix each non-empty logical line with `> ` and each blank one with `>`) and `perline` (identical except it trims every logical line). Source and run under `<scratch>/trimproof`:

```
case (a) identical=true bytes_rule10=18 bytes_perline=18
case (b) identical=true bytes_rule10=33 bytes_perline=33
case (c) identical=true bytes_rule10=35 bytes_perline=35
case (d) identical=true bytes_rule10=31 bytes_perline=31
case (e) identical=true bytes_rule10=31 bytes_perline=31
case (f) identical=true bytes_rule10=31 bytes_perline=31
case (g) identical=true bytes_rule10=25 bytes_perline=25
matrix_rows=7 rows_that_discriminate=0
```

The same run shows the two helpers DO separate on a value with interior indentation, `"The problem is X.\n\n  - an indented sub point"`:

```
rule10:                            perline:
> The problem is X.                > The problem is X.
>                                  >
>   - an indented sub point         > - an indented sub point
interior_identical=false
```

WHY IT MATTERS RATHER THAN BEING A CURIOSITY. RULE 4 makes each step's own sidecar the first source and the batches transcribe that prose, and sidecar prose in this repository carries indented list content (`docs/plans/agent-scaffold.steps/core-assets.md` opens with a bullet list above its heading). A per-line-trimming helper silently reflows such a value in `render`, in the `next` context block an agent is handed as an instruction, and in `status --step`, while every criterion of this increment passes. The two required red mutations at `:313` do not reach it: they collapse blank runs and normalise CRLF only, and both leave the trim scope untouched.

THIS IS NOT INSIDE `GB-4`'s BOUNDARY. `GB-4` (`:200`) accepts only that criterion 3 exercises `""` and not a whitespace-only string, so `value.is_empty()` can stand in for `value.trim().is_empty()` in RULE 3's `validate` rejection. That is a different rule, a different surface and a different value class; `GB-4`'s stated non-expansion boundary does not reach RULE 10's display trim.

SMALLEST CORRECTION. Add one matrix case to criterion 2 whose value carries whitespace at the start or end of an interior logical line (for example `"first line\n  indented second line"`), state its expected human bytes beside the existing three blocks at `:170-185`, require it on all three human surfaces in criteria 4, 7 and 8, and add a third red mutation at `:313`: temporarily trim every logical line in the shared display helper, and require all three named display tests to fail that row.

### `C3-2` -- criterion 7's human `next` arm omits the outer-whitespace row, so that surface has no trim coverage at all

- OWNING INCREMENT: `step-intent-encoding-inc1`.
- SEVERITY: `low`. PROPOSED CLASS: 1.
- RULE VIOLATED: RULE 10 (`step-intent-encoding.md:53`), the same trim clause, and criterion 2's own promise at `:187` that "Case (d) keeps its internal newline and trims only the two outer runs for human display".

THE HOLE. Criterion 7's human arm names its fixtures explicitly: "Then run the human form on the single-paragraph, repeated-blank, CRLF and bare-CR fixtures and compare the complete fixed context range byte-for-byte" (`:240`). That is matrix cases (a), (c), (e) and (f). Case (d), the outer-whitespace value, is not run on this surface. The other two human surfaces do run it: criterion 4 puts outer whitespace into the render fixture (`:202`), and criterion 8 runs it through `problem-only.plan.toml`, whose value is `"  problem one\rproblem two  "` (`:269`). So `next` is the one human surface where an implementation that applies the quoted-line helper WITHOUT the whole-value trim, or with no trim at all, passes every byte comparison the criteria specify.

WHY A SURFACE-LOCAL SLIP IS THE REALISTIC ONE HERE. Criterion 7's JSON arm requires the untrimmed bytes to survive into `next --json` ("the outer-whitespace value retains both outer runs", `:236`), so the trim cannot happen at the `build_context` insertion point and must be applied at the human display step in `render_active_loop` (`src/next.rs:1219-1222`). That is a `next`-only code path, and it is the one path the human matrix does not exercise for this case. The `:313` red mutations are described as acting on "the shared display helper" and test blank-run collapse and CRLF-only normalisation, so they do not catch an omitted trim in the `next` display path either.

SMALLEST CORRECTION. Add the outer-whitespace fixture to criterion 7's human list at `:240`, so it reads "the single-paragraph, repeated-blank, outer-whitespace, CRLF and bare-CR fixtures", and state its expected context block beside the single-paragraph block at `:242-251`.

### `C3-3` -- `status --step --json` is never run against a CRLF value, so a CRLF-normalising JSON projection passes

- OWNING INCREMENT: `step-intent-encoding-inc1`.
- SEVERITY: `low`. PROPOSED CLASS: 1.
- RULE VIOLATED: RULE 10 (`step-intent-encoding.md:53`), "JSON keeps the deserialised string unchanged".

THE HOLE. Criterion 8 is the only criterion that runs `status --step --json` at all (`:255-305`). Its JSON assertions run against exactly three value-bearing fixtures, and their representations are:

| Fixture | Citation | Representations carried |
| --- | --- | --- |
| `good.plan.toml` | `:255`, `:267` | two paragraphs, LF only |
| `problem-only.plan.toml` | `:269` | outer whitespace, bare CR |
| `approach-only.plan.toml` | `:280` | two consecutive blank logical lines |

No CRLF value reaches this surface. An implementation whose `status --step --json` path applies `value.replace("\r\n", "\n")` therefore satisfies "each JSON prose string equals its parser value" on `good.plan.toml`, leaves the bare CR in `problem-only` untouched (CRLF-only normalisation does not touch a lone `\r`), leaves `approach-only`'s LF runs untouched, and violates RULE 10's JSON clause. Nothing else reaches it: criterion 7's byte-for-byte matrix and its normalising red control are both scoped to `next --json` (`:236-238`), and the two red mutations at `:313` are display-helper mutations checked against three HUMAN tests.

THIS IS THE SAME DEFECT `T2` CLOSED ON THE OTHER JSON SURFACE. The reset round 2 triage ruled `T2` class 1 for `next --json` on exactly this ground (`q78-reset-r2-triage.md:59`); the repair gave `next --json` the whole matrix plus a normalising red control and gave `status --step --json` three fixtures with no CRLF row and no red control.

SMALLEST CORRECTION. Add criterion 2's CRLF fixture to criterion 8's JSON arm with a `jq -j` byte comparison against the parser value, and extend the red control at `:238` so the temporary normalising insertion must also redden a named `status --step --json` test.

### `C3-4` -- the "body with no heading line" render sub-rule has no fixture and no criterion

- OWNING INCREMENT: `step-intent-encoding-inc1`.
- SEVERITY: `low`. PROPOSED CLASS: 1.
- RULE VIOLATED: RULE 10 (`step-intent-encoding.md:53`), "Increment 1 pins `render` ... against paragraph fixtures before the first batch", against the sub-rule stated at `:98`.

THE HOLE. The render format states four sub-rules (`:97-100`). Three are pinned: the leading-heading rule by criterion 5's `gamma` range (`:220-226`), the one-field case by criterion 6's `eta` range (`:228-234`), and the empty-body case by increment 3 criterion 2's re-pointing of `empty_details_sections_emit_no_bare_heading` (`:733`). The fourth, "A BODY WITH NO HEADING LINE takes the labelled intent first, then one blank line, then the body" (`:98`), is pinned by nothing, because no fixture and no live sidecar exercises it.

MEASURED, on today's tree:

```
for f in src/plan/testdata/render-fixture.steps/*.md; do printf '%s headings=%s\n' "$(basename "$f")" "$(grep -c '^#' "$f")"; done
alpha.md headings=1   beta.md headings=1   delta.md headings=1   epsilon.md headings=1
eta.md headings=1     gamma.md headings=1  zeta.md headings=1

for f in docs/plans/agent-scaffold.steps/*.md; do grep -q '^#' "$f" || echo "$f"; done
(prints nothing: every one of the 105 live sidecars carries a heading line)
```

Criterion 5 makes `gamma.md` carry "a lead-in sentence above its own `###` heading" (`:220`), which is `core-assets`'s shape, a heading that is not on line 1. It is not the no-heading shape. Criterion 4's per-step test checks that each present field's fragment CONTAINS exactly one label line and one expected block (`:204`); it does not read position, so a renderer that files the intent after the first body line when the body has no heading passes it, passes criteria 5 and 6 (both steps have headings), and passes criterion 9's strict render check on the live plan (all 105 sidecars have headings). The golden `render-fixture.md` is regenerated by the same implementer, so it is not an independent oracle for a case no fixture contains.

WHY IT IS NOT MERELY THEORETICAL. `render` places no constraint on sidecar content, and the shipped pack ships this format to every scaffolded project, whose planners author sidecars this repository's conventions do not police.

SMALLEST CORRECTION. Give one existing render-fixture step a sidecar body with no heading line at all (`beta.md` is free, since criterion 4's red control uses `beta` only as a duplication target), and add one `awk` range to criterion 6 in the shape criteria 5 and 6 already use, asserting the labelled intent first, one blank line, then the body.

### `C3-5` -- the narrowed numstat residual is one class short: a wordless in-line edit below the opening passes criteria 5 and 6

- OWNING INCREMENT: `sidecar-status-opening-drift-inc1`.
- SEVERITY: `low`. PROPOSED CLASS: 2, a second-guard hole. See the note on the alternative reading below.
- RULE / GROUND: `docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md:213`, the reset round 2 `T9` repair, which states "THE COST ACCEPTED is only those deletion-only or wordless line-count changes below the opening that criterion 5 admits and criterion 6 cannot see", against criterion 5's bound at `:211` and criterion 6's additions arm at `:229` and `:239`.

WHAT THE REPAIR GOT RIGHT, VERIFIED FIRST. I rebuilt criterion 6's script verbatim against a throwaway repository (`<scratch>/driftrepo`) holding one worklist file whose opening carries `Deferred. `, and ran the correct fix plus four mutations. The repaired residual's two named exposures reproduce exactly, and its central claim, that the word-diff arm covers authored prose below the opening, reproduces too:

| Case | `git diff --numstat` | criterion 6 | criterion 5 admits? |
| --- | --- | --- | --- |
| correct token deletion only | `1 1` | `checked=1 bad_anchor=0 added=0` | yes |
| whole paragraph deleted below the opening | `1 2` | `added=0` | yes (named by the residual) |
| blank line added below the opening | `2 1` | `added=0` | yes (named by the residual) |
| authored sentence appended below the opening | `2 1` | `OPENING ADDS WORDS demo`, `added=1` | rejected |
| clause deleted inside a line below the opening | `2 2` | `OPENING ADDS WORDS demo`, `added=1` | rejected |

THE ROW THE RESIDUAL DOES NOT NAME. A whitespace-only edit inside a line below the opening changes no words and changes no line count, so it is neither "deletion-only" nor a "line-count change":

```
# in the throwaway repo, after the correct token deletion:
sed -i '3s/second paragraph/second  paragraph/' docs/plans/agent-scaffold.steps/demo.md
git diff --numstat -- docs/plans/agent-scaffold.steps/demo.md
2	2	docs/plans/agent-scaffold.steps/demo.md
bash c6.sh anchors.tsv "$BASE"
checked=1 bad_anchor=0 added=0
```

`2 2` is exactly criterion 5's bound at `:211` ("at most 2 added and 2 removed lines"), so criterion 5 admits it, and the word-diff emits the changed line as a context row with no `+` or `-` word entries, so criterion 6 reports `added=0`:

```
@@ -3 +3 @@ Deferred. This is a defect fix in `src/`, not a design change.
 A second  paragraph that the step keeps.
~
```

CONSEQUENCE. The residual's "only" is false as written, so the boundary the human weighed on 2026-08-22 is one class wider than the sentence records. The extra admitted edit is cosmetic (whitespace inside published prose, no claim changes), which is why this is `low` and not higher.

ALTERNATIVE READING, STATED SO THE TRIAGER CAN RULE RATHER THAN RE-DERIVE. Criterion 6's word-diff arm is explicitly the second guard over criterion 5's looseness (`:239`, "criterion 5's loose numstat bound cannot hide an addition below the opening"), which is why I propose class 2. A triager who instead reads this as an inaccurate accepted-risk boundary, the kind reset round 2 ruled `T9` to be, would place it outside both permitted classes.

SMALLEST CORRECTION. At `:213`, delete the two words "line-count", so the sentence reads "only those deletion-only or wordless changes below the opening that criterion 5 admits and criterion 6 cannot see". No other text moves and the acceptance does not widen.

### `C3-6` -- the dedup-surplus and busiest-line figures inside criterion 1 no longer reproduce under the repaired selector

- OWNING INCREMENT: `ledger-order-citation-currency-inc1`.
- SEVERITY: `low`. PROPOSED CLASS: 2, an in-increment non-reproducing figure.
- RULE / GROUND: `docs/plans/agent-scaffold.steps/ledger-order-citation-currency.md:82`, inside criterion 1 (`:76-86`) of the increment declared at `:52`, against that same criterion's own rule at `:86` ("NO ROW COUNT IS WRITTEN INTO THIS CRITERION. The first number moves with every appended round").

THE FIGURE. `:82` reads: "MEASURED, the busiest single ledger line carries eight drifting citations across four values, three of them repeats of one value, and a deduplicating form collapses 20 sites across the file", and it instructs the reader to "Reproduce the surplus by running the command above with and without `sort -u` and subtracting".

MEASURED ON THE REVIEWED TREE, with GNU grep, using criterion 1's own command at `:79`:

```
grep -noE '\b([Oo]rder|[Ss]tep) [0-9]+\b' docs/plans/agent-scaffold.ledger.md \
  | awk -F: '{n=$NF; gsub(/[^0-9]/,"",n); if (n+0 >= 85) print}' > pre-ledger.txt
no sort -u: 131
with sort -u: 109
surplus: 22
```

The busiest line is 1735, and it carries TEN drifting citations across four values, not eight, and the repeat shape is not "three of them repeats of one value":

```
      2 1735:Step 86
      2 1735:step 86
      3 1735:step 87
      1 1735:step 88
      2 1735:step 89
```

WHY IT BROKE, WHICH IS THE PART THAT MAKES THE FIX OBVIOUS. The figure was authored at `b4eb7f6` when every selector in this sidecar was lower-case-only, and it is still exact under that selector: at `HEAD`, `\b(order|step) [0-9]+\b` gives raw 117, dedup 97, surplus 20. Reset round 1's `D2` repair replaced the selector with the case-insensitive `([Oo]rder|[Ss]tep)` form at `c7b5a56` (`git log -S'[Oo]rder|[Ss]tep' -- docs/plans/agent-scaffold.steps/ledger-order-citation-currency.md`), and `git log -S'collapses 20 sites across the file'` on the same path returns only `b4eb7f6`, so the sentence was never re-measured against the selector it now sits beside. The figure is not merely stale with the ledger's growth: it is stale against this sidecar's own repair, and it has been wrong on every tree since `c7b5a56`.

WHY THIS IS NOT A RE-RAISE. Reset round 1 raised the selector itself (`D2`, `q78-reset-r1-triage.md:49`) and reset round 2 re-measured this sidecar and filed nothing on this loop (`q78-reset-r2-reviewer-claude.md:227`, `q78-reset-r2-triage.md:96`). Neither round measured the surplus under the repaired selector.

SMALLEST CORRECTION. At `:82`, replace the two figures with the relation the rest of the criterion already uses: state that a deduplicating form collapses the repeats a single ledger line can carry, that the surplus is what the two runs differ by, and that the outcome records the pair on the day. No number is needed for the sentence to carry its point, and `:86` already says none belongs here.

## Checked and NOT filed

- THE `one of those records` CLAIM AT `ledger-order-citation-currency.md:43`. Measured, three `round` records carry the slug beside the number (`docs/metrics/workflow.jsonl` lines 210, 211 and 217), not one. NOT FILED, on the same ground the reset round 2 review recorded: the sentence sits at `:43`, above the increment block that opens at `:52`, so the figure rule excludes it, and it is an existential claim that understates rather than overstates its own evidence.
- `plan-order-array-position-inc2` CRITERION 2's `expect`/`actual` DEDUP ASYMMETRY. `expect` is read from the `sort -u`'d `pre.txt` and `actual` is recomputed raw from the line (`:336-337`), so a line carrying a drifting citation AND the same exempt citation twice would be refused on a correct implementation. NOT FILED: measured over all 30 rows of `drift.txt`, no such line exists on this tree (the scan printed no `ASYMMETRY` row), so the refusal is unreachable and filing it would be a prediction rather than a measurement.
- `plan-order-array-position.md:432`, "which is why every question sidecar is 0 bytes", which is false now that `docs/plans/agent-scaffold.questions/Q-78.md` is 1295 bytes. NOT FILED against an active loop: the sentence sits in that step's NOT IN SCOPE list, outside either increment block, and `Q-78.md:5`, `step-intent-encoding.explorations/Q-78.md:219` and the batch block's own note at `step-intent-encoding.md:610` all record the supersession, so no criterion or rule of an active increment rests on it. Recorded here so the successor pass can retire the last copy.
- THE WORDING OF "THE COMPLETE ACCEPTED-RESIDUAL SET HAS ONE HOME" (`docs/plans/agent-scaffold.plan.toml:2288`, mirrored at `step-intent-encoding.explorations/Q-78.md:324`). The phrase collides with the term of art `ACCEPTED RESIDUAL` used by `GB-4` (`step-intent-encoding.md:200`), `F2` (`:815`), `F3` (`:849`), `GB-9` (`validate-missing-source-exit.md:118`) and the two drift-step residuals (`sidecar-status-opening-drift.md:213`, `:247`), none of which lives under the named heading. NOT FILED: each of those carries its own `Q-78-round4-low-residuals` or `Q-78-residuals` acceptance receipt, so the eventual `Q-78` closing receipt owes only the four the section defines, the substance the `T9`/`T6` repair was asked for is correct, and the residue is wording rather than a boundary defect.
- THE INCREMENT 3 MEASUREMENTS AGAINST BUILT WRONG IMPLEMENTATIONS (`step-intent-encoding.md:628`, `:727-729`, `:731`). These describe binaries built from an increment 1 that does not exist yet, so they cannot be re-run on this tree. I verified their internal arithmetic and their command shapes instead, and I record the limit rather than claiming a reproduction I did not make.

## Reproductions

Every runnable figure and command inside an active increment block reproduced exactly, except the two named in `C3-6`.

`sidecar-status-opening-drift-inc1`. Anchored selector 36 rows; complement 9 rows, and all nine slugs (`se-principle-namespace`, `classification-trivial-rename`, `drift-guard-optionality`, `instrument-magic-filename`, `module-spec-description-dead`, `checks-kind-skip`, `sidecar-ref-empty-string`, `sidecar-ref-symlink`, `repoint-resume-prompts`) are declared `status = "deferred"`, matching the enumeration at `:22`; unanchored selector 45 rows; `h1.sh` run verbatim gives 19 handover rows from the anchored set and 28 from the unanchored set, matching `:21` and `:23`; worklist 36 - 19 = 17, matching `:29`; criterion 12 run verbatim over the whole selected set against the live tree prints zero rows, matching `:166`. Every slug in the contradicting enumeration at `:59` checks out: ten `complete` steps open "Not started", seven `complete` open "Next", two `complete` open "Deferred", two `in-progress` open "Not started", and `code-value-audit-static` opens "Build the Tier-0 slice ..." with no token. The criterion 6 red control at `:241` reproduces (`OPENING ADDS WORDS demo`, `added=1`).

`ledger-order-citation-currency-inc1`. The corrected selector prints 155 total and 131 at or above 85; the capitalized selector's delta at `:20` is exactly `131 - 117 = 14`; `order` values 84 and 91 are absent from the plan; the four dated commits at `:29-35` print `then=8 agreeing=8`, `then=11 agreeing=11`, `then=12 agreeing=12` and `then=18 agreeing=18`; `docs/metrics/workflow.jsonl` carries 14 citation hits, 13 of them at or above 85; the single pre-existing ledger annotation is `1735:step 88 (\`reviewer-reproducible-evidence\`)`; `next --source` prints `RESUME STATE (verbatim from the ledger):`; the ledger's ASCII sweep prints `0`.

`plan-order-array-position-inc2`. `pre=52 exempt=21 eightyfour=1 drift=30`, so criterion 1's stated relation `pre = exempt + eighty-four + drift` holds; `raw_sites=39 worklist_rows=30 surplus=9`; the bare-word worklist prints 8 rows across 5 files, matching `:395`; `grep -n 'opens "Next (built first'` returns exactly one row, matching `:354`; `grep -rl '\`order\`' docs/plans/agent-scaffold.steps/` returns five files, four of them `Q-78` sidecars, matching `:428`.

`step-intent-encoding-inc1`. `core-assets.md` is the only sidecar whose first line is not a heading; `src/plan/render.rs` has three `slug` sites and the `N1` fixture at `:877` is the first, with `empty_details_sections_emit_no_bare_heading` at `:872`; `--help` prints `8`; the batch sizing prints `steps=105 batches=6 size=18` against six declared `inc2` entries; RULE 3's `2 x $(grep -c '^\[\[step\]\]' ...)` is `2 x 105 = 210`; `StatusArgs` is at `src/main.rs:496`. The clap 4.6.1 conflict message shape the criterion pins is correct: `agent-flow scaffold --write --dry-run` prints `error: the argument '--write' cannot be used with '--dry-run'`, so `--step <STEP>` before `--resume` yields the string `:311` states.

`step-intent-encoding-inc3`. The declaration-site search returns 12 files and 69 sites, row for row as tabulated at `:671-683`, against the `status` anchor's 99; `grep -rn 'the problem this step addresses' src/ --include='*.rs'` prints nothing and exits 1; `grep -n 'Unreleased' CHANGELOG.md` exits 1; all three template pairs are byte-identical today and `pack/pack.toml` maps each with `ownership = "working"` and no `render = true` (lines 39-41, 59-61, 84-86); `.agents/checks.toml` declares one check naming `docs/plans/agent-scaffold.plan.toml`; a fresh `scaffold --output-dir . --write --vcs none` outside the repository gives `docs/plans/TEMPLATE.plan.toml: 1 steps, 0 questions, valid` and `docs/plans/TEMPLATE.plan.toml: up to date`; the how-to-add-a-step sentence at `pack/plan-template.steps/example-step.md:3` reads verbatim as quoted at `:650`. Criterion 6's placement measurement reproduces both ways: with the sentence as its own paragraph outside the note, both presence greps print `1` and the placement command prints `pack/...:0` and `docs/...:0` exiting 1; with it appended inside the brackets, the presence greps still print `1` and both rows read `:1`. R4 run verbatim prints `steps=105 source=0/0 quoted=1/1 projected=1/1`, and its question-sidecar clause at `:610` is correct: the steps and questions directories hold 105 and 81 files against 105 declared steps and 81 declared questions.

`Q-81` AND THE EVENTUAL `Q-78` RECEIPT DO NOT CONFLICT. `Q-81` is registered `decided`, `folded_into = "step-intent-encoding"`, `receipt = "Q-81"`, with the three option labels, their trade-offs, the chosen option and reasoning against plan Principles 6, 8 and 2, whose names in this plan's `[[principle]]` table are exactly "Ground decisions in evidence", "Structured data first, project for humans" and "Minimal by default". One matching `type:"decision"` receipt was appended with `q_id:"Q-81"` and `task:"step-intent-encoding"`, matching the `folded_into` convention, and `[step.provenance].decisions = ["Q-81"]` was added to the step. W4 keys on `d.q_id == question.id`, so `Q-81`'s receipt and the `q_id:"Q-78"` receipt the `Q-78` item rules on at `docs/plans/agent-scaffold.plan.toml:2290` join to different items and neither can satisfy the other. `validate --source --metrics --workflow` passes on all three arms. The empty `docs/plans/agent-scaffold.questions/Q-81.md` follows the project's own question-sidecar convention and is not a defect.

FIX VERIFICATION OF RESET ROUND 2. `T1` (repeated blanks, CRLF and bare CR on all three human surfaces, with two red mutations at `:313`), `T2` (`next --json` compared byte-for-byte across the whole matrix with a normalising red control), `T3` (both partial `status --step` states as separate fixtures, with the exact human blocks and the `found`/null contract), `T4` (per-step render reconciliation with `each_intent_field_projects_once_inside_its_own_step_details` and the offsetting red control, the global census demoted to a secondary), `T6` (the four-item residual set stated once and pointed at from the structured ask and the exploration, with the eventual receipt required to cover all four) and `T8` (the conditional `multiline` wording removed at `:112`, and the single-paragraph human `next` shape pinned with the inline form forbidden at `:253`) are all present and internally consistent, and I could not construct a wrong implementation that defeats any of the six as repaired. `T9` is repaired and its central claim reproduces; `C3-5` is the one row its narrowed sentence does not name. `C3-1` through `C3-4` are holes the repaired matrix did not close rather than regressions the repair introduced. `GPT-R2-5` was not re-raised. `T7a` through `T7f` and `D7` were not re-opened. The accepted residuals `GB-4`, `GB-9`, `F2` and `F3` were not filed as new, and `Q-81`'s recorded reasoning was not reopened. The reset round 2 repair touched only the paths its fix brief allowed, `git diff main...HEAD -- src/ Cargo.toml pack/ tests/` for `bf13e6f` is empty, and every file it changed sweeps ASCII-clean at `0`.

## Per-increment raw counts

| Increment | Raw findings | Severities | Proposed class 1 / class 2 / neither |
| --- | ---: | --- | --- |
| `sidecar-status-opening-drift-inc1` | 1 | `low` | 0 / 1 / 0 |
| `ledger-order-citation-currency-inc1` | 1 | `low` | 0 / 1 / 0 |
| `plan-order-array-position-inc2` | 0 | none | 0 / 0 / 0 |
| `step-intent-encoding-inc1` | 4 | `medium`, `low`, `low`, `low` | 4 / 0 / 0 |
| `step-intent-encoding-inc3` | 0 | none | 0 / 0 / 0 |

## Totals

- RAW FINDINGS: 6.
- SEVERITY CEILING: `medium` (`C3-1`).
- PROPOSED CLASSES: 4 class 1, 2 class 2, 0 in neither class.
- ZERO-FINDING LOOPS, STATED PLAINLY: `plan-order-array-position-inc2` and `step-intent-encoding-inc3` are clean on this review. I found nothing to file in either after re-running every runnable command they cite and attacking their criteria with the wrong implementations each is written to refuse.
- The four class 1 findings are all in `step-intent-encoding-inc1` and all bear on one region, the RULE 10 projection freeze and the matrix that is supposed to falsify it. A single fix pass over criterion 2's matrix, criteria 4, 7 and 8's per-surface fixture lists, and the red-mutation block at `:313` closes all four.
