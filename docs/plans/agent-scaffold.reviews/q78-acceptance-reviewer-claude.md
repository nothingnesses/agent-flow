# Q-78 acceptance review, Claude reviewer

## Verdict

**Four shortfalls: three `medium`, one `low`.** Three unmet criteria and one inaccurate claim. None of them touches the design's substance: the encoding, the array-position authority, the cited backfill, the paragraph-value shape and the migration record all hold, and every executable figure I could run reproduces. All four shortfalls are bookkeeping around the design rather than the design, and all four are repairable by plan edits inside this pass.

`Q-78`'s `open` status is not filed as a shortfall, per the brief.

## Scope

Artifact: the complete `plan/q78-design-pass` product at the branch tip, which is `review/q78-acceptance-claude` at `6d9ba59`. Measured against the plan's Success Criteria (`docs/plans/agent-scaffold.success-criteria.md`), the recorded `Q-78` decision set, the eight Project Principles and documentation currency.

Read in full: `AGENTS.md`; `docs/plans/agent-scaffold.plan.toml` and the generated `docs/plans/agent-scaffold.md`; `docs/plans/agent-scaffold.questions/Q-78.md` and the `Q-78` `[[question]]` ask; `docs/plans/step-intent-encoding.explorations/Q-78.md`; all five step sidecars (`step-intent-encoding`, `plan-order-array-position`, `ledger-order-citation-currency`, `validate-missing-source-exit`, `sidecar-status-opening-drift`); the ledger from `RESUME HERE` (`agent-scaffold.ledger.md:535-593`); the latest triages and both second-foreclosure verification reports; `Q-79`, `Q-80` and `Q-81`; and the `round`, `escalation`, `decision` and `waiver` records in `docs/metrics/workflow.jsonl`.

Review briefs and transient findings files are excluded from the product, per the brief.

Product scope confirmed clean: `git diff --stat main...HEAD -- src/ Cargo.toml Cargo.lock pack/ tests/ build.rs` is EMPTY. The pass touched plan content only, as decision (20) requires.

## Harness, stated rather than glossed

**The Nix development environment is unavailable in this container, so I could not use `direnv` as the brief directs.** `direnv`'s store path is on `PATH` but absent from the filesystem (`/nix/store/...-direnv-2.37.1/bin`: no such file or directory), and `nix` is absent entirely. Rather than report the gates as unrun, I built directly against a toolchain already in the store: `cargo`/`rustc` 1.95.0 from `/nix/store/9l9lclxjw8ns5q4k13lxld7pl90paa3g-rust-mixed`, with `cc` from `gcc-wrapper-15.3.0` and a readable CA bundle (the one `SSL_CERT_FILE` names is a dangling symlink). The crate declares `rust-version = "1.88"`, so 1.95.0 stable satisfies the MSRV; the flake pins fenix `latest`, so this is not byte-identical to the project toolchain and the gate results below should be read with that caveat. `CARGO_HOME` and `CARGO_TARGET_DIR` were both inside the authorised scratch.

GNU grep 3.12 was used for every figure, at `/nix/store/gn94gpcp5q08x4v6g8mvw8v4r65rcjzk-gnugrep-3.12/bin/grep`. This needs recording: bare `grep` in this harness resolves to **ugrep 7.5.0**, whose `-c`, `-o` and `-r` behaviour is not GNU's, so a reviewer running bare `grep` is not running the selector the sidecars' figures were measured with.

Scratch: `.../scratchpad/q78-acceptance-claude`. Nothing was written to bare `/tmp`, and nothing outside that directory and this one committed file. `git status --porcelain` is empty apart from this file.

## Gates, all green

| Gate | Result |
| --- | --- |
| `validate --source docs/plans/agent-scaffold.plan.toml` | `459 records, valid`; `105 steps, 81 questions, valid`; exit 0 |
| `validate --workflow --source docs/plans/agent-scaffold.plan.toml` | `workflow invariants hold`; exit 0 |
| `render --check --strict docs/plans/agent-scaffold.plan.toml` | `up to date`; exit 0 |
| `cargo test` | 470 passed, 0 failed |
| `cargo clippy --all-targets -- -D warnings` | exit 0 |

## The thirteen loops

Thirteen declared `[[step.increment]]` entries across the five steps (8 + 2 + 1 + 1 + 1), and thirteen loop identities in the round records. Peak `consecutive_clean` per increment, computed from the log rather than from the ledger's prose:

| Increment | Rounds | Peak streak | Bar (`risky`) | Result |
| --- | --- | --- | --- | --- |
| `ledger-order-citation-currency-inc1` | 3 | 2 | 2 | converged |
| `plan-order-array-position-inc1` | 2 | 2 | 2 | converged |
| `plan-order-array-position-inc2` | 3 | 2 | 2 | converged |
| `sidecar-status-opening-drift-inc1` | 4 | 2 | 2 | converged |
| `step-intent-encoding-inc1` | 9 | 1 | 2 | SHORT, waived |
| `step-intent-encoding-inc2a` .. `inc2f` | 2 each | 2 each | 2 | converged |
| `step-intent-encoding-inc3` | 6 | 2 | 2 | converged |
| `validate-missing-source-exit-inc1` | 2 | 2 | 2 | converged |

Twelve converged on their own evidence. The thirteenth is covered by `step-intent-encoding-w1`, and **the waiver is well-formed, correctly scoped and load-bearing, which I falsified rather than read.** All five W5 conditions hold: it names a real Roadmap step, its increment is declared under that step, the `accepted-at-escalation` / `record-backed` pairing is consistent, and its `evidence` joins to `{"type":"escalation","task":"step-intent-encoding-inc1",...,"human_decision":"decision","step":"step-intent-encoding","increment":"step-intent-encoding-inc1","ts":"2026-08-24"}`.

The falsification, run in scratch: `step-intent-encoding` is `not-started` today, so W3 (which gates on `status == "complete"`, `src/workflow.rs:469`) does not reach any of the thirteen loops yet, and the waiver is therefore inert on the live tree. Flipping the step to `complete` in a scratch copy keeps `validate --workflow` green; deleting ONLY the seven-line `[[step.waiver]]` block from that same copy turns it red with exactly

```
Roadmap step `step-intent-encoding` increment `step-intent-encoding-inc1` reached a consecutive-clean streak of 1 but its `risky` risk class needs 2
```

So the exemption is real and precisely scoped, and it will bind at the moment it is supposed to.

Backstop: every one of the eight `Q-78` triage files records its backstop status explicitly and none was owed; no `high` or `critical` finding was dismissed anywhere in the pass. The two escalations account for `inc1`'s nine rounds against a cap of five: the first (`human_decision: "resume"`) resets the counters per `AGENTS.md:57`, the second (`human_decision: "decision"`) ends the loop with the waiver.

## Shortfalls

### 1. A `type:"waiver"` record was appended to the round log, which the criterion forbids and which nothing reads (`medium`)

**The criterion**, verbatim at `docs/plans/agent-scaffold.success-criteria.md:20`:

> ... and (per Q-46) the exemption waivers nested on their step and the W4 baseline in `[meta]`; the append-only `docs/metrics/workflow.jsonl` holds only genuine events (rounds, escalations, decisions, intakes, dismissals).

A waiver is not one of the five listed event types, and Q-46's cutover deliberately MOVED all sixteen historical `waiver` lines into `[[step.waiver]]` and pruned them from the log.

**Measured.** `jq -r '.type' docs/metrics/workflow.jsonl | sort | uniq -c` returns `1 waiver` on this branch and `0` on `main`. It is the only `waiver` record in the file, and it duplicates `[[step.waiver]] id = "step-intent-encoding-w1"` (`docs/plans/agent-scaffold.plan.toml:1626-1632`) field for field.

**It is dead data, not a second reader.** This repo is `[meta].primary = "toml"`, so `check_workflow_toml` sources waivers from `waivers_from_toml(plan)` (`src/workflow.rs:192`) and never from `metrics::parse_waivers`. Falsified in scratch: deleting the JSONL line and re-running `validate --workflow` gives `458 records, valid` and `workflow invariants hold` at exit 0, with no output change at all. The converse probe above shows the TOML copy is the one that binds.

**What it costs.** Two hand-maintained copies of one exemption, one of which no check on this substrate reads, in the file whose stated job is to hold only genuine events. That is the duplication Principle 8 ("Structured data first, project for humans", which the plan itself says sharpens one-source-of-truth thinking) exists to remove, and it re-creates exactly the state Q-46's cutover removed. A future edit to either copy leaves the other stale and silent.

**Provenance, so the fix lands in the right place.** `docs/plans/agent-scaffold.reviews/q78-waiver-fold-brief.md` directed it: "Append the matching `type:"waiver"` metrics record with task and increment `step-intent-encoding-inc1` ...". The planner did as instructed; the instruction is what breaches the criterion. Note the log is append-only, so the repair is a deliberate one-time prune of the kind Q-46 already sanctioned, not an ordinary edit, and it needs the human's ruling rather than a silent deletion.

### 2. `Q-81` declares a fold into `step-intent-encoding` that never happened (`medium`)

**The rule.** `AGENTS.md:41`: "A resolved decision is recorded in the plan's Open Questions section and folded into the step it affects." `Q-81` itself closes with "Keep every existing increment id, add no scope-reset event, and fold this decision into `step-intent-encoding`", and carries `status = "decided"`, `folded_into = "step-intent-encoding"` (`docs/plans/agent-scaffold.plan.toml:2340-2342`).

**Measured.** `grep -c 'Q-81' docs/plans/agent-scaffold.steps/step-intent-encoding.md` returns `0`. Neither the id, nor "scope change", nor the accepted cost appears anywhere in that sidecar.

**This is anomalous, not the plan's convention.** Of the 26 decided queue items carrying a `folded_into`, `Q-81` is the ONLY one whose target step sidecar never names it; the other 25 all do. Reproduce by extracting each `(id, folded_into)` pair from the `[[question]]` blocks and grepping the named sidecar for the id.

**What it costs, and it is not merely clerical.** `Q-81` is the decision that authorises counting reset round 1's clean outcomes through the 2026-08-23 `Q-78-intent-paragraphs` scope change, and its accepted cost is stated in its own words: "only reset round 2 reviewed paragraph values". Six of the thirteen loops converged on precisely that shape - `step-intent-encoding-inc2a` through `inc2f` each reached peak streak 2 from one clean round dated 2026-08-23 and one dated 2026-08-24, so the FIRST clean round of every one of those six streaks reviewed the pre-paragraph artifact. The limitation that qualifies half the convergence evidence for six loops is recorded only in the queue item, and nowhere in the step whose convergence it qualifies. `validate --source` cannot catch this: it checks only that `folded_into` resolves to a real slug, which it does.

### 3. `validate-missing-source-exit` ships a breaking exit-code change with no documentation impact, and its exact path set forbids the entry (`medium`)

**The criterion**, at `docs/plans/agent-scaffold.success-criteria.md`:

> Documentation currency is a core cross-cutting part of the workflow: the planner assesses which docs and prompts a folded change makes stale ..., the implementer updates them, the reviewer verifies, and acceptance carries a doc-currency check that a shipped change leaves no doc or prompt stale.

**Measured.** `docs/plans/agent-scaffold.steps/validate-missing-source-exit.md` contains zero occurrences of `DOCUMENTATION IMPACT` and zero of `CHANGELOG`.

**The change is squarely changelog-worthy by the step's own account.** Its risk ground (`:33`) reads: "the increment changes the exit code of a shipped subcommand that every scaffolded project's checks and CI read, so a project that names a stale path flips from passing to failing on upgrade ... the flip reaches every downstream project at once rather than this repository alone." `:23` adds: "A scaffolded project whose `.agents/checks.toml` passes a path that has since moved flips from green to red on upgrade." `CHANGELOG.md` already records a strictly smaller instance of the same class, at 0.0.2: a `principles.toml` the tool cannot read "produced an empty principle set at exit 0 with empty stderr in 0.0.1; it now exits 2 naming the file".

**The path set forecloses the fix.** Criterion 10 (`:120`) is an exact enumeration: "`git diff --name-only` lists `src/main.rs` and `tests/validate_refuses_a_missing_explicit_path.rs`, the file criterion 8 adds, **and nothing else**." It names only `docs/plans/` and `pack/` as considered exclusions and is silent on `CHANGELOG.md`. So an implementer who obeys criterion 10 cannot write the entry, and one who writes it fails the criterion.

**This is the defect class the round-3 adopter lens already filed, reproduced in the third step.** The ledger records that lens finding "the two schema-breaking steps carry no documentation impact and their exact path sets forbid a `CHANGELOG.md` entry" (`agent-scaffold.ledger.md:559`). It was repaired for both: `plan-order-array-position` increment 1 and `step-intent-encoding` increment 3 each gained a `DOCUMENTATION IMPACT` section opening `## [Unreleased]`, each names `CHANGELOG.md` in its path set, and each records verbatim that omitting such a path is "a defect in the criterion rather than in the implementation". `validate-missing-source-exit` carries the same property and got neither repair. I found no triage verdict, ledger passage or receipt that accepts the omission.

`README.md` is NOT made stale by this step, measured: its `validate` section (`README.md:225-242`) documents path resolution and never states the note-and-skip behaviour, so nothing in it becomes false.

### 4. The exploration's "complete accepted-residual set" claim is false of the pass (`low`)

`docs/plans/step-intent-encoding.explorations/Q-78.md:324` states: "The complete accepted-residual set lives once in `docs/plans/agent-scaffold.steps/step-intent-encoding.md` under `THE RESIDUALS THIS STEP ACCEPTS RATHER THAN CLOSES`. It contains four numbered items ...", under a section headed "What this pass ACCEPTS rather than fixes".

Four FURTHER residuals this pass accepts rather than fixes live at five other sites, none of them in that block: `GB-4` (`step-intent-encoding.md:200`), `F2` (`:983`), `F3` (`:1017`, and again at `plan-order-array-position.md:419`), and `GB-9` (`validate-missing-source-exit.md:118`).

The consequence is bounded and I state it as such: each of those four is recorded with an owner, a non-expansion boundary and its own human receipt (`Q-78-round4-low-residuals`, revised by `Q-78-gb11-revision`), so nothing is lost or unowned. Only the word "complete" overreaches, and it overreaches in the document a human will read when building the closing receipt. The fix is one qualifier: the block is the complete set of the DESIGN residuals, not of the pass's accepted residuals.

## Two stale figures, recorded but not filed

`ledger-order-citation-currency.md:82` states, present tense, "MEASURED, the busiest single ledger line carries eight drifting citations across four values ... and a deduplicating form collapses 20 sites across the file." Reproduced today: the worklist is 131 rows, `sort -u` gives 109, so the surplus is **22**, and the busiest line (ledger line 1735) carries **10** citations across four values. Both moved because the ledger is append-only and every appended round adds citations, which the same paragraph predicts and instructs the reader to re-derive by running the command with and without `sort -u`.

I am not filing these. The paragraph carries its own selector, no criterion pins either number as a pass condition, and the step's own line 20 already dates the comparable pair ("THE EARLIER LOWER-CASE-ONLY MEASUREMENT printed `135` and `116` ... Both totals rise with every appended review round"). Nothing wrong can ship from them. They are recorded so the triager can overrule this judgement on the evidence rather than have to rediscover it, and because line 82 not being dated the way line 20 is dated is an inconsistency inside one file.

## What I verified and found sound

Executability is the strongest part of this pass. Every figure and command I could run reproduced exactly, several of them byte-for-byte:

- **The array-position migration oracle, which is the central claim of `plan-order-array-position`.** `order` gaps fall after 83 and after 90; `rename-to-agent-flow` is the single out-of-place declaration, standing 84th and rendering 98th. Moving that one slug from declaration index 84 to 98 makes the declaration sequence **identical** to the rendered Roadmap sequence over all 105 steps (`diff` prints nothing). The byte-exact criterion is achievable as specified.
- **The declaration-site table** (`step-intent-encoding.md:818-837`): 12 files and 69 sites, every row of the table matching, including the `(\\n|^)slug = ` anchor that reaches inline TOML inside Rust string literals.
- **The shipped-surface path set**: `grep -rln 'entries with status and order' pack/ AGENTS.md .agents/` returns exactly `pack/AGENTS.md`, `AGENTS.md`, `.agents/AGENTS.reference.md`, as `plan-order-array-position.md:80` states.
- **The bare-word worklist** (`plan-order-array-position.md` increment 2 criterion 3): 8 rows across 5 files, as measured.
- **The drift selector**: the anchored form selects 36, the complement prints 9, and all nine are declared `deferred` with adjectival `Deferred <noun>` openings, exactly as the sidecar claims.
- **The batch sizing** (`step-intent-encoding.md:483-502`): `steps=105 batches=6 size=18`, and `declared_loops` equals `manifest_batches` at 6.
- **The empty-value rule arithmetic**: `2 x $(grep -c '^\[\[step\]\]' ...)` is 210 today, as RULE 3 states.
- **The cited code line**: `src/main.rs:954` is `eprintln!("no source plan at {}; nothing to validate", ...)`, the exact site `validate-missing-source-exit` names.
- **`GB-7`'s repair is executable, which I checked because a class 1 finding once landed there.** `ledger-order-citation-currency.md:66-72` now requires a historical-resolution table taken from "a commit at which both currently vacant values were assigned". Such a commit exists: scanning all 144 commits that touch the plan TOML, `d39964f` (2026-07-28) and `5fcd020` (2026-07-27) each resolve `84 -> rename-to-agent-flow` and `91 -> exploring-item-actor-boundary`, matching the ledger's own narrative that step 91 `exploring-item-actor-boundary` was removed on 2026-07-28. The criterion is satisfiable and the fourth disposition class is now admitted.

Also sound:

- **Every receipt cited resolves.** All 22 distinct `Q-78-<suffix>` ids cited across the five sidecars, the exploration and the `Q-78` question sidecar appear in `docs/metrics/workflow.jsonl`; the set difference is empty.
- **The residual bookkeeping is complete and located.** The four design residuals carry non-expansion boundaries and a receipt obligation; the four round-4 accepted residuals each carry an owner, a boundary and a receipt. Subject to shortfall 4, nothing is unowned.
- **Pack promises are exact where they were made.** `pack/AGENTS.md`'s `and order` clause and its two drift-guarded renders are named in `plan-order-array-position` increment 1's path set with the measured search that finds them; `pack/plan-template.plan.toml` and `pack/plan-template.steps/example-step.md` and their committed copies are named in `step-intent-encoding` increment 3's, so the placeholder values and the how-to-add-a-step sentence both have owners.
- **The successor drift step is a clean handover, not a dangling reference.** `sidecar-status-opening-drift.md:116` names no slug and says so deliberately: "THIS SIDECAR IS THE POINTER AND NOT THE STEP ... a planner's to author against this sidecar as its input."
- **Paragraph values are feasible on the live substrate.** The `Q-78` `[[question]].ask` is already a multiline basic string carrying 28 blank lines that parse and render today, so `toml = "0.8"` handles the shape decision 26 requires. RULE 10's block-quote projection is a genuine addition rather than existing behaviour: `render` currently FLATTENS a multi-paragraph `ask` into a single queue bullet (`agent-scaffold.md:174` joins `Q-81`'s paragraphs with two spaces), which is why pinning the three projection formats before the first value lands is the right call.

## Readiness

The design is ready for the human's accept/revise decision, with the four shortfalls above put alongside it.

None of the four attacks a recommendation. The encoding, the two required fields, the array-position authority, the migration record outside the plan, the cited backfill in six bounded batches and the paragraph-value shape all survive this pass unscathed, and the parts of the specification I could execute are unusually strong: measured figures that reproduce byte-for-byte, criteria that name the wrong implementations they refuse, and red controls that are separate rather than composite. Shortfalls 1, 2 and 4 are plan-content edits of a few lines each. Shortfall 3 needs a planner to add a `DOCUMENTATION IMPACT` section and one path to one criterion, which is the same repair already made twice in this pass.

What the human should know when deciding, drawn from the ledger's own list of what is owed and not filed here because none of it is this pass's product: decisions (23) and (24) each still owe their own step; the routed-decision-tracking defect and the `AGENTS.md:93` rebase rule each still owe a `[[question]]`; `Q-80` still reads `open` although `Q-78-classinherit` answers it in substance; and the successor drift step still owes its planner.

## Totals

- Raw findings: 4.
- Severity ceiling: `medium`.
- By severity: 0 critical, 0 high, 3 medium, 1 low.
- Backstop re-check: not owed (nothing dismissed at any severity).
- Recorded but not filed: 2 stale figures in `ledger-order-citation-currency.md:82`.
