# Q-78 second foreclosure verification, Claude reviewer

## Verdict

**Zero findings** on `step-intent-encoding-inc1`.

`GPT-R4-1` is closed. I verified it independently against a countermodel I authored from RULE 10 and criteria 2 and 7 alone; I read no reviewer file from this round or any earlier one, and no GPT report at any point.

## Scope and gates

Lens: adoption and executability. Artifact: increment 1 of `docs/plans/agent-scaffold.steps/step-intent-encoding.md` at the branch tip `8bf318b`, after the pending-transfer fix `469a5bb`. I read `AGENTS.md`, the ledger from `RESUME HERE` (`agent-scaffold.ledger.md:535-543`), `q78-second-foreclosure-fix-brief.md`, `q78-foreclosure-r4-triage.md`, and increment 1 in full (`:59-508`) plus the step-level RULES it depends on (`:25-57`) and the step's `DOCUMENTATION IMPACT` and residual sections. To establish which findings are settled I read the seven prior triage files' verdict tables and the round-1 and round-3 fix briefs; I did not read any reviewer file.

Scratch: `.../scratchpad/q78-second-foreclosure-claude/reviewer`. Nothing was written to bare `/tmp` and nothing outside that directory and the one committed findings file.

**The Nix development environment is unavailable in this harness, so I make no claim about the validators, the test suite, Clippy or the strict render check.** `direnv` resolves onto `PATH` but its store path is absent (`/nix/store/...-direnv-2.37.1/bin`: no such file or directory), so `direnv exec . true` exits 127; `cargo`, `nix` and `agent-flow` are also absent. This matches what the round-4 triage recorded for its own harness.

GNU grep 3.12 IS available and every `grep` figure below was reproduced with it. This needs recording because the interactive shell defines `grep` as a function wrapping **ugrep 7.5.0**, whose `-c`, `-o` and `-P` behaviour is not GNU's; `command grep` bypasses the function and is GNU grep 3.12. A reviewer who runs bare `grep` in this harness is not running the selector the sidecar's figures were measured with.

Direct checks that DID run, all green: `git diff --check 469a5bb^ 469a5bb` exit 0; the non-ASCII sweep `LC_ALL=C grep -cP '[^\t\x20-\x7e]'` printing `0` for both the sidecar and the generated projection; the fix's changed-path set being exactly the two permitted files; and a partial render-currency surrogate, `cmp` of the sidecar's rewritten region `:320-382` against `docs/plans/agent-scaffold.md:3884-3946`, which is byte-identical. That surrogate is not `render --check --strict` and does not stand in for it.

## GPT-R4-1: independently verified as closed

The finding was that every listed pending oracle used one-line literals (`"ready problem"`, `"blocked approach"`), so a `build_pending_loop` transfer that truncated a value at a paragraph boundary satisfied all of them while violating RULE 10's unchanged-JSON contract (`:53`) and the `next` contract at `:112`.

I modelled the seam from the specification text only: the eight criterion-2 logical cases in both fields, RULE 10's display formatter, the two mutations the fix now demands, and four oracle sets (the pre-fix pending oracle recovered from `git show 051f83b`, the post-fix pending oracle, criterion 7's in-progress matrices, and the direct `build_context` seam). No product code and no reviewer fixture supplies an expected value. Script at `.../scratchpad/q78-second-foreclosure-claude/reviewer/model.sh`.

```text
== mutant: pending transfer keeps only the text before the first blank line ==
   (this is exactly GPT-R4-1's countermodel)
   pre-fix  pending oracle (one-line literals): PASS
   post-fix pending oracle (eight-row matrix) : FAIL
       pending JSON mismatch: row(b) problem
       pending human mismatch: row(b) problem
       pending JSON mismatch: row(b) approach
       pending human mismatch: row(b) approach
       pending JSON mismatch: row(c) problem
       pending human mismatch: row(c) problem
       pending JSON mismatch: row(c) approach
       pending human mismatch: row(c) approach
   criterion 7 in-progress matrices            : PASS
   direct all-state build_context seam         : PASS

== mutant: pending transfer trims each non-empty logical line ==
   pre-fix  pending oracle (one-line literals): PASS
   post-fix pending oracle (eight-row matrix) : FAIL
       pending JSON mismatch: row(d) problem
       pending JSON mismatch: row(d) approach
       pending JSON mismatch: row(e) problem
       pending JSON mismatch: row(e) approach
       pending JSON mismatch: row(h) problem
       pending human mismatch: row(h) problem
       pending JSON mismatch: row(h) approach
       pending human mismatch: row(h) approach
   criterion 7 in-progress matrices            : PASS
   direct all-state build_context seam         : PASS

== control: unmutated transfer ==
   post-fix pending oracle: PASS
```

The wrong implementation GPT-R4-1 named now reddens both pending tests on both surfaces for both fields, and it reddens nothing else. That is precisely what `:379` claims for the paragraph-truncation control, and `:380`'s claim reproduces too: the interior-line-whitespace row (h) fails on BOTH surfaces, because whole-value display trimming preserves the two leading and two trailing interior spaces that per-line trimming destroys. The one detail the sidecar understates rather than overstates is that per-line trimming also reddens rows (d) and (e) on the JSON surface; naming only row (h) is a floor, not a ceiling, so the control still holds.

The five obligations the fix brief set are all met and all internally consistent: the complete eight-row two-field matrix through both pending constructors (`:320-321`), exact JSON and exact human display bytes for every row (`:333`, `:335`, `:347`, `:361`, `:374`), complete pinned context keys for both states (`:322-331`, `:349-359`), the two new pending-only red controls (`:379`, `:380`), and the retained absence-only mutation (`:378`). Nothing was weakened: the single old control became three, and `:382`'s isolation clause is wider than the sentence it replaced. The increment-3 retention clause at `:890` gained the new obligations and dropped none.

I also checked the fix's setup claims against the real code rather than taking them:

- `:322` gives step `a` `status = "next"` and expects `ReadyToPlan`. `StepPhase::is_pending()` covers `NotStarted | Next` (`src/next.rs:500`) and `select_active_loop` rule 2 reaches `build_pending_loop(..., ReadyToPlan, ...)` (`src/next.rs:720-726`). Correct.
- `:349` makes `dep` a declared `deferred` step so nothing pre-empts the blocked path. `Deferred` is terminal (`src/next.rs:508`), so `dep` is never selected, and `is_complete` is false for it (`src/next.rs:753-758`), so `a` falls to rule 3 with `blockers = ["dep"]`. Correct on both halves.
- The pinned key sets are exactly what `build_context` emits: `ledger` and `isolation_tier` unconditionally, the `ReadyToPlan` arm adding nothing (four keys with intent) and the `Blocked` arm adding `blocked_by` (five keys), in `BTreeMap` order (`src/next.rs:998-1020`). The `awaiting-fixes` five-key set at `:294-304` matches the `AwaitingFixes` arm, `review_findings` absent. Correct.
- `:335`'s human range boundary -- starting at the two spaces before `context:` and ending immediately before the two spaces of `reminders:`, final byte the LF after the last context line -- is exactly the renderer's shape (`src/next.rs:1219-1223`). Correct.

## Executability sweep of increment 1

Every figure and command in increment 1 that this harness can run reproduces exactly. Reproduced with GNU grep 3.12 at the branch tip:

| Site | Claim | Reproduced |
| --- | --- | --- |
| `:31`, `:198` | RULE 3 / criterion 3: `2 x $(grep -c '^\[\[step\]\]' ...)` is 210 | `105` steps, so `210` |
| `:102` | `grep -nE '(\\n\|^)slug = ' src/plan/render.rs` prints three sites, the `N1` fixture first | three sites at `877`, `1047`, `1227`; `empty_details_sections_emit_no_bare_heading` is at `872` |
| `:107-110` | the leading-heading loop prints `core-assets.md` and nothing else; its heading sits at line 9 | exactly one file; heading at line 9 |
| `:158` | 69 inline `[[step]]` declaration sites | the `:818-820` selector returns 12 files and 69 sites, every row of the `:826-837` table matching |
| `:239` | criterion 5's `gamma` awk range | runs, selects heading through `The gamma step body` |
| `:247` | criterion 6's `eta` awk range | runs, selects heading through `The eta step body` |
| `:255`, `:258` | `beta`'s retained body, and `grep -c '^#' beta.md` printing `0` after the heading is deleted | body byte-identical; `beta.md` has exactly one `#` line today, so deletion yields `0` |
| `:202` | the fixture declares `alpha`, `gamma`, `eta`, `beta` | all four present, plus `delta`, `zeta`, `epsilon` for the remaining matrix rows |
| `:471` | the Clap set `["scaffold", "validate", "status", "next", "checks", "render", "audit", "help"]` | the `Command` enum's declaration order at `src/main.rs:412-425` is exactly those seven |
| `:61` | `src/main.rs:496` for the new flag's home | `struct StatusArgs {` |
| `:483-489` | criterion 10's sizing script | `steps=105 batches=6 size=18`, 105 TSV rows |
| `:497-502` | `declared_loops` equals `manifest_batches` | `declared_loops=6 manifest_batches=6` |
| `:466` | each of the thirteen authoritative test names resolves | all thirteen occur inside increment 1; `render_is_deterministic_and_matches_the_golden` is the one pre-existing test and it is at `src/plan/render.rs:698` |

Two figures I could not run are recorded as unrun rather than passed: criterion 1's `grep -c 'problem: Option<String>'` and criterion 8's exact Clap conflict message both describe post-implementation state. The conflict message's form (`error: the argument '--step <STEP>' cannot be used with '--resume'`, exit 2) is consistent with Clap 4's `ArgumentConflict` rendering and with `--step`'s derived `STEP` value name, but the repository contains no existing assertion of a Clap conflict string to pin it against, so it is unverified rather than verified.

## Adoption

Increment 1 costs an existing project nothing, and it states and tests that property rather than asserting it. Both fields land as `Option<String>` with `skip_serializing_if` (`:65`), so an existing plan deserialises to `None` and re-serialises to nothing; the empty-value rule fires only on a present field (`:67-77`); `render` contributes an entry only for a step carrying at least one field, and the neither-field empty-body case is explicitly preserved as today's behaviour (`:100`) with the named `N1` regression test staying green at this increment and inverting only at increment 3 (`:102`). `docs/plans/TEMPLATE.md` and `pack/plan-template.plan.toml` are correctly absent from the changed-path set, because neither gains a field until increment 3 (`:807`). Criterion 9's two-part live-projection check (`:478`) is the executable form of the same property for this repository. The `status --step` flag and the two `next` context slots are purely additive. The whole adopter cost of this step falls on increment 3, which is where the ledger's measured figures put it.

## Considered and not filed

**Settled findings I did not re-raise, per the brief.** `C4-1` (Markdown `status --step`), `R3-3` (Markdown `next --plan` boundary), `R3-4` (the `:158` declaration-site scope claim, which does include `render-fixture.plan.toml`'s seven sites of which criterion 4 changes four), `FR1-4` (criterion 7 pinning `reviews/reviewer.md` and `reviews/triage.md` at `:273-274`, `:288-289`, `:302`, `:315`, which `findings_naming::review_findings_path` cannot emit for any `task`/`step`, since `DIR_TEMPLATE` always prefixes `docs/plans/` -- `src/findings_naming.rs:31-63`), `FR1-1`, `I2` (the README exclusion for the new public flag; `:1021`'s substitute measurement is itself true -- README has exactly one `[[step]]` description, at `README.md:199`, listing no field -- but it answers a question about the schema field rather than about the flag, and that does not change I2's class, severity or measured boundary, so it is not the new evidence the fix briefs require), `I6`, `I7`, `D7`, `T7a`-`T7f`, `GB-4`, `GB-9`, `F2`, `F3`, and the dismissals `GPT-R2-5`, `GPT-R3-2` and `PE1C-3`. I confirmed the fix commit introduced no fresh instance of any of these: it rewrote only `:317-382` and `:890`, leaving the `status --step` region and every settled literal untouched.

**One residual exposure, weighed and judged below the bar.** `build_context_carries_intent_in_every_loop_state` (`:384`) covers all nine states but with the single-line values `"all-state problem"` and `"all-state approach"`, which carry no blank line, no outer whitespace, no interior whitespace and no carriage return. A complete matrix now reaches only four states -- `ReadyToPlan` and `Blocked` through `build_pending_loop`, `AwaitingFirstReview` and `AwaitingFixes` through the two in-progress `LoopFacts` sites -- so a value-corrupting normalisation applied inside `build_context` for only the other five states would pass every listed oracle while violating RULE 10. I did not file this. The three `LoopFacts` construction sites (`src/next.rs:770`, `:802`, `:836`) are each now reached by a complete matrix, which is what closed GPT-R4-1's defect class; the remaining exposure needs a compound and unmotivated deviation, since `build_context`'s state `match` adds only state-specific extra keys and the natural intent insertion is one unconditional statement beside `ledger` and `isolation_tier`, and the existing loop-state red control at `:388` already forces state-conditional insertion to redden. Recorded so the triager can overrule this judgement on the evidence rather than have to rediscover it.

## Totals

- Raw findings: 0.
- Severity ceiling: none.
- Class 1: 0. Class 2: 0.
- Backstop re-check: not owed (nothing dismissed at any severity).
