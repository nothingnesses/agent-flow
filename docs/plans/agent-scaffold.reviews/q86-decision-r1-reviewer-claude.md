# Q-86 decision-fold plan review, round 1 (reviewer `claude`)

## Scope and method

Artifact: the Q-86/Q-91 decision fold at tip `485443d9` against `main` (commits `af288707`, `45718b2c`, `c5880477`, `485443d9`), a 15-file planning diff. Reviewed against `AGENTS.md`, `.agents/prompts/reviewer.md`, the narrowed synthesis, the Q-86/Q-91 receipts, the five retained triages, the new proof sidecar, the plan sources, the Success Criteria and the generated plan. Lenses: executability of the new step by an implementer holding only the new sidecar; adoption into the existing plan machinery; and human-decision fidelity.

Verified green before looking for defects (built from `nix develop --command cargo build`):

```
./target/debug/agent-flow render --check docs/plans/agent-scaffold.plan.toml --strict   # up to date, exit 0
./target/debug/agent-flow validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl
# 496 records valid; 115 steps, 91 questions, valid; exit 0
./target/debug/agent-flow validate --source docs/plans/agent-scaffold.plan.toml --workflow  # invariants hold, exit 0
```

Checks that passed and are recorded here so they are not re-run:

- **Human-decision fidelity holds.** The Q-86 receipt records exactly the three architecture option strings the pre-fold ask presented, recommendation and chosen both `B - Frozen obligations with sealed phase campaigns`; the Q-91 receipt records exactly `["high","critical","defer"]`, recommendation and chosen both `high`; both carry `task:"bounded-convergence-option-b-proof"`, matching each question's `folded_into` (`docs/metrics/workflow.jsonl:495-496`, `docs/plans/agent-scaffold.plan.toml:2584-2586,2678-2681`). Both match the human's choices as the ledger records them (`docs/plans/agent-scaffold.ledger.md:535`).
- **The 51-verdict count is correct.** The sidecar's per-round valid-id lists (`bounded-convergence-option-b-proof.md:112-116`) reproduce exactly against the five retained triages: r1 13 valid (T9/T13/T15/T17 invalid), r2 12 (T13 invalid), r3 9 (all valid), r4 8 (T7/T9 invalid), r5 9 (all valid) = 51.
- **Current/open/decided prose is current.** `grep -rniE "after the human (selects|chooses)|the human (must|will) (choose|select)|remains? (open|undecided)"` over the questions, steps, explorations, Success Criteria and plan TOML returns no stale Q-86 hit. The two durable-text rows the fold claims to close are closed: r1 T3 (`success-criteria.md` no longer says `exploring`) and r4 T8 (`Q-86-convergence-mechanism-brief.md:6-8` now states `decided`).
- **The ledger anchor is genuinely current**, so `bounded-convergence-option-b-proof.md:120` is accurate: `docs/plans/agent-scaffold.ledger.md:535` is dated 2026-08-29 and describes this fold. The r1 T12 defect class did not recur.
- **The command form is real and matches project precedent.** `nix shell nixpkgs#python3 -c python3 <script> --suite all --floor high` was run against a stub and the flags reach the script (`ARGS ['--suite', 'all', '--floor', 'high']`, exit 0); it is the same form the retained explorations already use (`Q-86-safety-process.md:534-542`).
- **No hidden production work.** The diff touches only `docs/`; no `src/`, `pack/`, `README.md`, `CHANGELOG.md` or workflow-spec change. The algebra is internally coherent: `sum_q L_q = |O| + (m+1)` and `sum_q C_q = 4|O| + (m+1)`, which with `r_plan` and the separate seven-batch plan-review maximum give exactly the published `L_B = r_plan + |O| + m + 1` and `R_B = 4|O| + m + 8`.
- **Schema/adoption details are correct**, checked rather than assumed: `folds` is step-to-step (`src/plan/source.rs:142`), so `folds = []` alongside two questions whose `folded_into` names this step is right, not a missing back-link; the block's field ordering matches the `plan-order-array-position` precedent; all 15 changed files are ASCII-clean.

Severity summary: **0 critical, 0 high, 2 medium, 2 low.** I found nothing of critical or high severity, and say so explicitly rather than inflating.

---

## F1 (medium) - the new step duplicates an existing `order` value, so its Roadmap position rests on an alphabetical accident and the plan's order-to-position correspondence breaks for the 37-83 band

**Evidence.** The fold gives the new step `order = 36` (`docs/plans/agent-scaffold.plan.toml:490`), which `instrument-flag` already holds (`:513`). It is the plan's only duplicate:

```
awk '/^order = /{print $3}' docs/plans/agent-scaffold.plan.toml | sort -n | uniq -d
36
```

`render` sorts by `order` then slug (`src/plan/render.rs:177`), so the new row lands where the sidecar intends only because `b` sorts before `i`. Demonstrated by mutation in a scratch copy outside the repository (plan TOML plus sidecars copied to a tempdir, slug renamed `bounded-convergence-option-b-proof` -> `zzz-proof`, sidecar renamed with it, nothing else changed, then rendered):

```
| `workflow-calibration` | in progress | ...
| `instrument-flag` | complete |
| `zzz-proof` | not started | ...
```

The step now renders *after* `instrument-flag`, falsifying its own `bounded-convergence-option-b-proof.md:9` ("This step has Roadmap order 36, immediately after the active order-35 `workflow-calibration`") while the declared `order` is unchanged. The declared order does not determine the position; the slug does.

**Consequence 1, the citation is ambiguous.** `order 36` no longer names one step. The fold writes that ambiguous citation three times: `bounded-convergence-option-b-proof.md:9`, `workflow-calibration.md:30`, and `success-criteria.md:41` ("The separate order-36 Roadmap unit").

**Consequence 2, and the reason this is medium rather than low.** Inserting a second step at value 36 shifts every later step's rendered position by one while leaving its `order` value alone, so value and position no longer agree above 36:

```
slug                              value  rendered position
workflow-calibration                 35   35
bounded-convergence-option-b-proof   36   36
instrument-flag                      36   37
roles-findings-naming-slots          82   83
workflow-toml-rule-fragments         83   84
planner-folds-decisions              89   89
prompt-drift-guard                   92   91
```

That falsifies a measured, load-bearing premise in a decided-but-unstarted step. `docs/plans/agent-scaffold.steps/plan-order-array-position.md:279` reads: "A citation at or below 83 reads correctly as a position. A citation from 85 to 90 drifts by one. A citation at or above 92 drifts by two." All three clauses are now wrong: 37-83 drifts by one, 85-90 drifts by zero, 92+ drifts by one. That step (`plan-order-array-position`, `status = "not-started"`, `docs/plans/agent-scaffold.plan.toml:1589`) deletes the `order` field so position *becomes* the order, and its increment-2 criterion 1 builds `exempt.txt` from exactly that premise and leaves the exempt band un-restated. Nineteen citation rows now sit in the newly drifting 37-83 band and are scheduled to be left alone:

```
grep -rnoE '\b([Oo]rder|[Ss]tep) [0-9]+\b' docs/plans/agent-scaffold.steps/ docs/plans/agent-scaffold.success-criteria.md \
  docs/plans/agent-scaffold.documentation-protocol.md docs/plans/agent-scaffold._status-narrative.md \
  | awk -F: '{print $1"\t"$2"\t"$3}' | sort -u \
  | awk -F'\t' '{n=$3; gsub(/[^0-9]/,"",n); if (n+0 >= 37 && n+0 <= 83) print}' | wc -l
19
```

Worked example from that set: `generated-projection.md:7` cites "step `agents-md-drift-guard`, order 80". Order value 80 is `agents-md-drift-guard`; rendered position 80 is now `generated-projection` itself. After the `order` field is deleted the number resolves to the wrong step, which is precisely the "or worse, to the wrong step" hazard that `plan-order-array-position.md:275` names as its own risk ground.

The `success-criteria.md:41` citation is worse than merely stale: it is spelled `order-36` with a hyphen, which `plan-order-array-position`'s own capture regex `\b([Oo]rder|[Ss]tep) [0-9]+\b` cannot match, so it is invisible to that step's oracle and worklist entirely.

**Why this counts against this fold.** `AGENTS.md:30` makes documentation impact the planner's duty at fold time. The fold's assessment (`bounded-convergence-option-b-proof.md:170`) says "This step changes planning and proof records only. It makes no shipped product documentation stale because it changes no behaviour." That is true of shipped docs and false of planning docs: the fold made a decided step's specification stale and did not say so.

**Correction.** Either (a) restate the three new numeric citations by slug per `plan-order-array-position.md` RULE 4 (Principle 8, the slug is the stable identifier and the position is a projection) and add the drift-table correction to `plan-order-array-position.md:279` plus this fold's documentation-impact section; or (b) renumber `instrument-flag` and every following step by +1 so value and position agree again. (a) is the smaller and more principled fix; there is no free value between 35 and 36, so a distinct order number is not available without renumbering. Note the duplicate itself is legal and `render`'s equal-order tie-break is pinned by `ordering_is_numeric_for_questions_and_slug_tiebroken_for_equal_order_steps`, so this is a plan-data and currency defect, not a renderer bug.

---

## F2 (medium) - acceptance criterion 13 cannot be satisfied as written: it requires the five commands to run from clean temporary directories, while the commands block requires the repository root and pins repo-root-relative paths

**Evidence.** Two statements in the same sidecar, both load-bearing:

- `bounded-convergence-option-b-proof.md:130`: "Run these commands from the repository root. They use no machine-specific scratch path."
- `bounded-convergence-option-b-proof.md:158` (acceptance criterion 13): "All five exact commands pass twice from clean temporary directories and produce identical semantic summaries. They create no tracked or untracked artefact in the repository."

Every one of the five commands (`:133-137`) addresses its script by a repository-root-relative path, for example `docs/plans/workflow-calibration.proofs/q86-option-b-proof.py`. Run with a clean temporary directory as the working directory, that path does not resolve and Python exits non-zero before any property is checked, so criterion 13 fails by construction on a correct implementation. Reproduced now against the retained prototype, which does exist at such a path and takes the identical invocation form:

```sh
# from the repository root
nix shell nixpkgs#python3 -c python3 docs/plans/workflow-calibration.explorations/q86-controller-proof.py \
  --mode A --phase plan_review --risk risky --floor high
# -> A phase=plan_review risk=risky ... bad_foreclosure_state=0     exit 0

# from a clean temporary directory
T=$(mktemp -d); cd "$T"
nix shell nixpkgs#python3 -c python3 docs/plans/workflow-calibration.explorations/q86-controller-proof.py \
  --mode A --phase plan_review --risk risky --floor high
# -> python3: can't open file '/tmp/tmp.XXXXXXXXXX/docs/plans/workflow-calibration.explorations/q86-controller-proof.py':
#    [Errno 2] No such file or directory     exit 2
```

The second sentence of criterion 13 ("create no tracked or untracked artefact **in the repository**") shows the commands are meant to run against the repository, so "clean temporary directories" is not a fresh-clone instruction either. The two readings produce materially different work: under one, criterion 13 is the repeat-run determinism check plus the no-artefact check; under the other, the implementer must add a path-resolution or `--root` mechanism the commands block forbids ("no machine-specific scratch path"). A reviewer applying criterion 13 literally fails a correct implementation.

This is the same class of defect round 3 T8 raised against the prototype's advertised command ("contains a stale, machine-specific scratch path", `q86-synthesis-r3-triage.md:82-88`); the repair over-corrected into a contradiction rather than leaving it unresolved, so this is new evidence rather than a re-raise.

**Correction.** Keep `:130` as the invocation contract and restate criterion 13 as what it is actually testing, for example: "Each of the five commands is run twice from the repository root and produces an identical semantic summary on both runs. `git status --porcelain` is empty after all ten runs, so no tracked or untracked artefact is created. Any temporary state the proof needs is written under a directory the run creates and removes." That preserves the determinism and no-artefact obligations and drops the unsatisfiable working-directory clause.

---

## F3 (low) - the traceability gate can be closed by a checker that never reads the five triage files, an asymmetry with the anti-hard-coding rule the same sidecar imposes on the algebra command

**Evidence.** The traceability command is the only mechanical closure for 51 adversarial verdicts from five capped review rounds. Its contract is:

- `:21` "checks that the traceability matrix covers exactly the 51 valid triage verdicts, cites all five retained triages, resolves every named assertion or durable-text pointer, and leaves no applicable verdict open"
- `:140` "The traceability command reports `valid_findings=51` and `unresolved=0`"
- `:156` (criterion 11) "The traceability command covers exactly all 51 valid T-ids from the five retained triages"

Nothing requires the checker to *derive* the valid-verdict set from `docs/plans/agent-scaffold.reviews/q86-synthesis-r1-triage.md` through `-r5-triage.md`. A checker holding `EXPECTED = 51` and a hard-coded id list, counting only its own matrix rows, prints `valid_findings=51 unresolved=0` and satisfies `:21`, `:140` and criterion 11 in full while proving nothing about the triages; "cites all five retained triages" is satisfied by five path strings. The transcription from the triage files to the matrix, which is where a dropped or mis-assigned verdict would hide, is then unchecked.

The same sidecar states the correct standard 36 lines earlier for the other derived quantity, and does not apply it here: `:104` "Hard-coding the published formula without deriving every coefficient is a proof failure." Criterion 14 (`:159`, reviewers "inspect ... traceability ... rather than trusting green output") mitigates but does not close this, which is why it is low rather than medium.

**Correction.** State the derivation obligation in `:21` and criterion 11, mirroring `:104`: the checker parses the five retained triage files, extracts the valid verdict set from their verdict lines, and fails if that derived set differs from the matrix's row set or from the count it reports. Hard-coding the id list or the count 51 is then a proof failure on the same terms as hard-coding a bound coefficient.

---

## F4 (low) - the mutation contract requires the tag and mutation counts to be equal, which forbids a second mutation on a tag that carries two mandatory mutation classes

**Evidence.** Three statements that cannot all hold:

- `:122` "Every load-bearing transition and predicate is tagged in the reference model and appears in a manifest."
- `:126` "A mutation manifest entry without an exercised test fails. A load-bearing tag without a mutation fails. Any surviving mutation fails." (the correct coverage rule: at least one mutation per tag)
- `:140` "The mutation command reports `survived=0`, with the discovered tag and mutation counts equal." (a strict bijection: exactly one mutation per tag)

`:124` then names 24 mandatory mutation classes, and at least two of them land on the same transition. The sidecar itself puts both on one sentence at `:32`: "An upheld dismissal preserves the incoming clean streak and does not unlock reserve authority." The retained triages record them as two separate valid findings on that one upheld-dismissal re-check transition: r2 T4, "A's reserve is unlocked by an upheld serious dismissal" (`q86-synthesis-r2-triage.md:46-52`, tracing `review_dismissed_high -> recheck_upheld_high` with no valid serious finding) and r4 T4, "An upheld A dismissal loses the prior clean streak and forecloses one batch too early" (`q86-synthesis-r4-triage.md:50-56`). Criterion 2 (`:147`) requires the model to prove both. Killing both requires two mutations of that one tag, so the mutation count exceeds the tag count and the `:140` equality fails on the *more* thorough implementation. Conversely, an implementer who satisfies `:140` by writing exactly one mutation there leaves one of the two mandatory classes unexercised while the command still reports success.

**Correction.** Replace the equality in `:140` with the coverage relation `:126` already states, for example: "The mutation command reports `survived=0`, every discovered tag covered by at least one mutation, and every mandatory mutation class present; it fails on any tag with no mutation and on any manifest entry with no exercised test." That keeps the real guard (no untagged transition, no unexercised entry, no survivor) and drops the count identity that penalises covering two classes on one tag.

---

## Not raised

- Line length and prose wrapping (never a finding here).
- `nix shell nixpkgs#python3` resolving an unpinned registry `nixpkgs` rather than the repo's `flake.lock`: real, but it is the established convention of the retained explorations (`Q-86-safety-process.md:534-542`, `Q-86-state-machine.md:447-452`) and predates this fold, so it is not a defect introduced here.
- The two new decision receipts omitting the optional `ts` field: `ts` is optional per `AGENTS.md:139` and six prior receipts already omit it.
- The pre-existing staleness of `docs/plans/agent-scaffold._status-narrative.md`, which never mentioned Q-86 and is not touched or made worse by this fold.
