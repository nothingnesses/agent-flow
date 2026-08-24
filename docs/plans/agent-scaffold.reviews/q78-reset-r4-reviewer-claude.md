# Q-78 reset round 4 Claude review

Independent reviewer, adoption / executability / fix-verification lens. One raw finding.

## Method and gates

I read `AGENTS.md`, the ledger from its current `RESUME HERE` (2026-08-24, after reset round 3), `q78-reset-r3-triage.md`, `q78-reset-r3-fix-brief.md`, the reset round 1 and 2 triages (for the settled set), the plan TOML, the generated view, the `Q-78` exploration and the three active sidecars. I read no reset round 4 reviewer file.

Every toolchain command ran through the project direnv environment (`direnv allow && eval "$(direnv export bash)"`, dev shell actually loaded; `cargo` resolves to `/nix/store/76jaab43a2l7n7fiifxjngp68kk167vm-rust-mixed/bin/cargo`). GNU-regex claims used GNU grep 3.12 at `/nix/store/gn94gpcp5q08x4v6g8mvw8v4r65rcjzk-gnugrep-3.12/bin/grep`; the interactive `grep` on this host is a shell function that dispatches to ugrep, so the absolute path is used throughout. All fixtures live in my own child directory of the authorised scratch path:

```text
/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r4-claude/reviewer-claude
```

No bare `/tmp` path was used and no wildcard deletion was run.

Baseline gates on the reviewed tree (`71fbd9c`, the round 3 repair `efce61a` plus the committed briefs):

- `validate --source ... --metrics ...`: `docs/metrics/workflow.jsonl: 445 records, valid`; `docs/plans/agent-scaffold.plan.toml: 105 steps, 81 questions, valid`; exit 0.
- `validate ... --workflow`: `workflow invariants hold`; exit 0.
- `render --check --strict docs/plans/agent-scaffold.plan.toml`: `up to date`; exit 0.
- `cargo test`: 470 passed, 0 failed, across 12 test binaries; exit 0.
- `cargo clippy --all-targets -- -D warnings`: exit 0.

## Figures reconciled on the current tree

Every figure I could re-run reproduced exactly. Nothing below is a finding; it is the reconciliation the brief asks for.

| Claim | Site | Re-run result |
| --- | --- | --- |
| Relaxed selector reaches 45 sidecars | `sidecar-status-opening-drift.md:21` | 45 |
| Bare strip over the 45 leaves 28 flagged | `:21` | 28 |
| Anchored selector reaches 36 | `:23` | 36 |
| Bare strip over the 36 leaves 19; handover population is 19 | `:23` | 19 |
| Nine relaxed-only rows, all adjectival, all `deferred` | `:22`, criterion 1 complement | 9 rows, all nine declared `status = "deferred"` |
| This step's worklist | criterion 2 | 17 slugs (36 - 19) |
| Criterion 10 prints one row per worklist file pre-fix | `:264` | 17 rows |
| Enlarged word list picks up `doc-redundancy-cleanup` on `when built` and never reaches `planner-folds-decisions` | `:266` | reproduces exactly |
| Roadmap header is three columns | `:31` | `docs/plans/agent-scaffold.md:178` reads `\| Step \| Status \| Notes \|` |
| `documentation-protocol.md:5` ends "do not repeat the status label" | `:3` | reproduces; rendered at `agent-scaffold.md:26` |
| Ledger `:46`, `:62`, `:99`, `:101` carry G1, its `high` verdict, L1 and the eight-valid line | `:5` | all four reproduce |
| `45 step sidecars` / `21 of them contradict` | `step-intent-encoding.md:21` | 45 reproduces; the by-slug enumeration at `sidecar-status-opening-drift.md:59` totals 21 |
| `2 x $(grep -c '^\[\[step\]\]' ...)` is 210 | `:31`, `:198` | 105 steps, 210 |
| 12 files and 69 declaration sites, per-file table | `:705-720` | 12 files, 69 sites, every row identical |
| `status` anchor reaches 99 against `slug`'s 69 | `:722` | 99 and 69 |
| `grep -nE '(\\n\|^)slug = ' src/plan/render.rs` prints three sites, N1 first | `:102` | 3 sites (877, 1047, 1227); `empty_details_sections_emit_no_bare_heading` owns 877 |
| The no-heading sweep prints only `core-assets`, whose heading sits at line 9 | `:107-110` | reproduces |
| Batch sizing: 105 steps, 6 batches, size 18; declared loops equal manifest batches | criterion 10 | `steps=105 batches=6 size=18`; `declared_loops=6 manifest_batches=6` |
| R4 on the current tree | batch criterion 7 / inc3 criterion 8 | `steps=105 source=0/0 quoted=1/1 projected=1/1`; `projected - quoted = source` holds |
| The eight named front/tail sidecars are `[meta.sidecars]` | `:647` | 7 front + 1 tail, names identical |
| `StatusArgs` at `src/main.rs:496`, `--source` has no default | `:61`, inc3 criterion 12 | `struct StatusArgs {` is line 496; `source: Option<PathBuf>` with no default |
| `status --source <plan> --plan /nonexistent.md` notes and exits 0 | `:154` | `note: --plan /nonexistent.md does not exist`, exit 0 |
| The subcommand census prints `8` before the change | criterion 8 | 8 |
| Fresh scaffold validates and renders | inc3 criterion 3 | `docs/plans/TEMPLATE.plan.toml: 1 steps, 0 questions, valid`; `up to date` |
| The three pack pairs are byte-identical, `ownership = "working"`, no `render = true` | inc3 criterion 5 | all three `cmp`s silent; `pack/pack.toml:39-41`, `:59-61`, `:84-86` |
| `pack/prompts/planner.md` tells the adopter's planner to delete the placeholder notes | inc3 `:685` | `pack/prompts/planner.md:5` |
| `grep -cE 'fn validate_(rejects\|accepts)_a' src/plan/source.rs` is 0 today | criterion 13 | 0, so the required `4` is reachable |
| `Step` fields are declared `pub(crate) <name>: <Type>,` | inc3 criterion 1 | `src/plan/source.rs:129-158` |
| GB-11 is repaired: no criterion hard-codes `80 questions` | ledger decision (25) | GNU grep for `80 questions` over the sidecars and the plan TOML returns nothing; `<N> steps, <M> questions` is the surviving form |

Clap's conflict message shape, which increment 1 criterion 8 pins verbatim, also reproduces on this clap 4: `agent-flow audit --dir . --out X --json` prints `error: the argument '--out <OUT>' cannot be used with '--json'` and exits 2, so `'--step <STEP>' cannot be used with '--resume'` is the exact text this clap emits for the criterion's argument order.

## Round 3 fix verification

I attacked each of the four class 1 repairs with the wrong implementation its finding named.

**I1, the interior-line-whitespace matrix row -- closed.** Case (h) is added at `step-intent-encoding.md:164`, its display bytes are pinned at `:187`, it reaches `render` through `beta` (`:202`), human `next` (`:282`) and human `status --step` (`:290`), and the third red mutation at `:350` reddens all three named tests on that row. The mutation is correctly specific: for case (d) (`  paragraph one\nparagraph two  `) per-line trim and whole-value trim agree, which is why (d) could not carry this control and (h) can. The premise reproduces on this toolchain: a TOML value carrying interior leading and trailing spaces round-trips unchanged through this crate's `toml = "0.8"` and out through JSON, measured with the existing `[[question]].ask` path, which is an ordinary `String` on the same parser:

```text
"ask": "paragraph one\n  indented interior line  \nparagraph three"
```

**I3, the outer-whitespace human `next` row -- closed.** `:254` adds the fixture to the named list and `:267-280` pins its complete expected six-key context block. I checked the arithmetic: `"  approach paragraph one\napproach paragraph two  "` under whole-value trim and the `> ` prefix is exactly the block written, and the block's key set and order match `build_context`'s live `BTreeMap` output (`src/next.rs:993-1021`), which I confirmed against the running binary.

**I4, CRLF through `status --step --json` -- closed.** `:298-304` adds the run, the `jq -j` plus `cmp` comparison and the named test `status_step_json_preserves_the_crlf_parser_value`, and `:252` extends the normalising red control to the `status --step --json` insertion. The whole chain is executable on this toolchain: a CRLF TOML value comes back through JSON and `jq -j` byte-for-byte, `cmp` silent against a `printf 'problem one\r\nproblem two'` oracle.

**I5, the no-heading render case -- closed, and the new range check works.** `beta.md` is now permitted in both changed-path statements (`:156` and criterion 11 at `:388`), the fixture shape is pinned at `:236-248`, and `beta` carries the interior row so the two repairs share one fixture. I built the golden both ways and ran the criterion's `awk` verbatim. Against a correct render it prints exactly `**Problem**` first, both quoted blocks with the interior spaces intact, one blank line, then the unchanged body. Against the wrong implementation the finding named -- intent placed after the first body line in the unrepresented no-heading case -- it prints nothing, so the criterion's "the first printed line is `**Problem**`" refuses it. `beta.md`'s current body is byte-identical to the fenced block the criterion says the file retains.

I also confirmed the repair is inert elsewhere: nothing in `src/` or `tests/` asserts on `beta`'s sidecar heading (`grep -rn 'beta' src/ tests/ --include='*.rs'`), `step_details_section` (`src/plan/render.rs:573-584`) inlines the body verbatim and requires no heading, and `src/plan/testdata/render-fixture*` is excluded from treefmt (`flake.nix`), so the trailing spaces the new golden must carry are not at risk from the repo formatter -- empirically confirmed by `alpha.md`'s body still being hard-wrapped under `proseWrap: never`.

## Executability simulation of `sidecar-status-opening-drift-inc1`

I ran the increment end to end on a throwaway copy of `docs/plans`, applying the bare token deletion to the 17 worklist files and nothing else:

- criterion 12 over this step's worklist printed nothing;
- criterion 1's anchored selector on the post tree printed 19 rows;
- criterion 1's pass condition, `comm -3` on the first columns against the captured `handover.txt`, printed nothing;
- criterion 6's anchor arm printed `checked=17 bad_anchor=0`.

The H1 handover script ran verbatim from the repository root with both arguments absolute and produced the 19-row list; run against the relaxed 45-row selected set it produces 28, which is the relation the sidecar states. I found no new defect in this increment.

## Findings

### C4-1 -- `next` carries the intent slots in one loop state and no criterion varies the state

- **Owner:** `step-intent-encoding-inc1`
- **Severity:** medium
- **Proposed class:** 1 (a wrong implementation passes while violating a numbered rule and the increment's own stated risk ground). If the triager reads RULE 10 as governing byte format only, the fallback reading is class 2, a second-guard hole in criterion 7, the only guard on `next`.

**The stated obligation.** `docs/plans/agent-scaffold.steps/step-intent-encoding.md:112`: "`LoopFacts` carries both, and `build_context` inserts a `problem` slot and an `approach` slot when the field is present, **in every loop state**." RULE 10 (`:53`) makes increment 1 the increment that pins this: "Increment 1 pins `render`, human and JSON `next`, and human and JSON `status --step` against paragraph fixtures before the first batch." The increment's own risk ground (`:61`) singles this surface out: "the `context` block that `next` hands an agent as an instruction rather than a report (`src/next.rs`) ... `workflow-enforcement-tier.md` is the plan's own precedent that `next`'s output being an instruction rather than a report is a blast-radius argument."

**The obligation is not vacuous: the slot set really is state-dependent.** `build_context` (`src/next.rs:993-1021`) inserts `ledger` and `isolation_tier` unconditionally at `:999-1000`, then adds per-state slots inside a `match state` at `:1003-1019`. Measured on the current binary against one-step scratch plans:

```text
{"state":"ready-to-plan","ctx":["isolation_tier","ledger"]}
{"state":"awaiting-first-review","ctx":["isolation_tier","ledger","review_findings","triage_findings"]}
{"state":"awaiting-fixes","ctx":["isolation_tier","ledger","triage_findings"]}
{"state":"blocked","ctx":["blocked_by","isolation_tier","ledger"]}
```

Each row is one `agent-flow next --source <plan> --json` run piped through `jq -c '{state:.active_loop.state, ctx:(.active_loop.next_instruction.context|keys)}'`, over a one-step plan that is `not-started` (ready-to-plan), `in-progress` with an empty round log (awaiting-first-review), `in-progress` with one `outcome: "new_valid"` round record (awaiting-fixes), and `not-started` with an unmet `blocked_by` (blocked).

The human surface differs the same way; at `awaiting-fixes` the live binary prints a three-key `context:` block with no `review_findings`.

**Every `next` criterion is blind to that axis.** Criterion 7 (`:250`) runs `next --json` on "every criterion 2 fixture" and names no state. Its human arm (`:254`) "fixes the four non-intent values to `worktree`, `ledger.md`, `reviews/reviewer.md` and `reviews/triage.md`", which is the four-slot `AwaitingFirstReview`/`AwaitingReviewers` shape, and both new blocks restate it: `:267-280` shows six keys, and `:282` requires the interior-line fixture to keep "the same six keys and order". So all six named human fixtures are pinned to one state. GNU grep over the whole sidecar, `grep -nE 'AwaitingFirstReview\|AwaitingFixes\|AwaitingReviewers\|ReadyToPlan\|LoopState\|Converged\|Escalate' docs/plans/agent-scaffold.steps/step-intent-encoding.md`, returns exactly one line, `:112`, and its only state name is `AwaitingFirstReview`. Criteria 4 to 6 are `render` and criterion 8 is `status --step`, so neither reaches `next`. No NOT-IN-SCOPE bullet covers it either: `:19` excludes only `next`'s loop **selection**, and `:913` excludes only the exploration-phase defect.

**The wrong implementation that passes.** Put the two inserts inside the `LoopState::AwaitingFirstReview | LoopState::AwaitingReviewers` arm at `src/next.rs:1004-1007` instead of beside the unconditional inserts at `:999-1000`. Every criterion 2 fixture, every criterion 7 byte comparison on both surfaces, both `next` red controls, and every other increment-1 criterion pass unchanged, because all of them observe only the four-non-intent-slot state. Meanwhile `agent-flow next` at `AwaitingFixes` -- the state whose whole purpose is to hand an implementer its instruction -- at `Blocked`, and at `ReadyToPlan` emits an instruction carrying no `problem` and no `approach`. That is the increment's stated `next` contract falsified in three of the states it names, on the surface its risk ground calls an instruction rather than a report, and nothing in increments 2a to 2f or increment 3 reads `next` at all (the batch scripts R1, R2 and R3 use `status --step --json`; increment 3 criterion 12 uses `status --step`), so no later increment catches it.

**Smallest correction.** Add one clause to criterion 7 requiring the human and JSON `next` comparisons to be repeated on at least one non-review loop state, and state that fixture's complete expected context range -- `awaiting-fixes` is the cheapest, reachable from a one-step in-progress plan plus a single `outcome: "new_valid"` round record, and its correct five-key block is `approach`, `isolation_tier`, `ledger`, `problem`, `triage_findings`. Then name the placement in the red-control list: record that moving the two inserts inside the review-state arm reddens `human_next_preserves_the_display_matrix` and `next_json_preserves_the_parser_value_matrix` on that row and leaves every existing row green. No path joins the changed-path set, because `src/next.rs` is already in it.

## Raw counts

| Increment | Raw findings | Severities | Proposed class 1 / class 2 / neither |
| --- | ---: | --- | --- |
| `sidecar-status-opening-drift-inc1` | 0 | none | 0 / 0 / 0 |
| `step-intent-encoding-inc1` | 1 | medium | 1 / 0 / 0 |
| `step-intent-encoding-inc3` | 0 | none | 0 / 0 / 0 |

- **Raw total:** 1.
- **Severity ceiling:** medium.
- No finding is assigned to any of the eleven converged loops.
- I re-raised nothing settled: I2, I6 and I7 are untouched, and `GPT-R3-2`, T7a through T7f, D7, `GB-4`, `GB-9`, `F2` and `F3` are not reopened. C4-1 is new; it is not a re-raise of T1, T2, T8, D4 or I1 through I5, all of which are defects on the logical-value axis, while C4-1 is a defect on the loop-state axis, which no round of this pass has examined.
