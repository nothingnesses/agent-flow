# Q-86 decision-fold plan review, round 4 - reviewer (Claude)

## Scope and method

Independent review of the Q-86/Q-91 decision fold and the `bounded-convergence-option-b-proof` Roadmap unit at branch tip `6dce497b` against `main` (`b3fc80ef`); the reviewed range is the eight commits `9e921190..6dce497b`, fifteen changed files. I read `AGENTS.md`, `pack/prompts/reviewer.md`, the proof-step sidecar, `docs/plans/agent-scaffold.plan.toml`, the rendered projection, the Q-86/Q-88/Q-89/Q-90/Q-91 question sidecars, the JSONL decision receipts, the retained synthesis, safety-process, state-machine and design-brief explorations, the five retained Q-86 synthesis triages, the round-1/2/3 decision-fold triages, and the orchestrator-owned ledger retention record. I did not read the other round-4 reviewer's output.

The specified proof artefacts do not exist yet, so every claim below is about the specification. I simulated an implementer building `docs/plans/workflow-calibration.proofs/` from the step and reported only what an exact citation, a command, or a derivation an implementer must follow can settle.

## Mechanical reproduction

```text
nix develop --command cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml
# docs/plans/agent-scaffold.plan.toml: up to date                                       (exit 0)
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl
# docs/metrics/workflow.jsonl: 499 records, valid
# docs/plans/agent-scaffold.plan.toml: 115 steps, 91 questions, valid                   (exit 0)
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow
# docs/plans/agent-scaffold.plan.toml vs docs/metrics/workflow.jsonl: workflow invariants hold  (exit 0)
git diff --check main...HEAD
# exit 0
```

ASCII check over all fifteen changed files: `LC_ALL=C grep -cP '[^\t\x20-\x7e]' <file>` prints `0` for every one.

Order uniqueness and position:

```text
awk '/^order = /{print $3}' docs/plans/agent-scaffold.plan.toml | sort -n | uniq -d
# (empty)
awk '/^\[\[step\]\]/{n++} /^slug = /{s=$3} /^order = /{print n"\t"$3"\t"s}' docs/plans/agent-scaffold.plan.toml | tail -1
# 115  117  "bounded-convergence-option-b-proof"
```

Traceability source set derived from the retained verdict records:

```text
for r in 1 2 3 4 5; do
  awk '/^### T/{h=1} /^- \*\*Verdict/{if(h && $0 ~ /valid/ && $0 !~ /invalid/) c++; h=0} END{print c}' \
    docs/plans/agent-scaffold.reviews/q86-synthesis-r$r-triage.md
done
# 13 12 9 8 9   -> 51
```

This matches the step's published `valid_findings=51` (`bounded-convergence-option-b-proof.md:180`).

## Round-3 fix verification

All four round-3 upheld findings are repaired.

- **T1 (scheduled-owner credit embedded in the `L_q` domain) - fixed.** `bounded-convergence-option-b-proof.md:136` now defines the domain by independently observable conditions only and states explicitly that "Whether every member of `O_q` received a separate scheduled-owner batch is not a domain-membership test". `:148` derives the per-owner batch requirement from the transition relation ("only the named scheduled owner can leave `Untested`"), and `:152` puts the two-owner cross-credit witness *inside* the domain and requires the mutant to report `L_q < n_q + 1`, calling the old filter a proof failure. Criterion 10 (`:197`) and the mutation class list (`:164`) match. The correction propagated to `Q-86-safety-process.md:356`, `Q-86-synthesis.md:123` and `:200`, and `agent-scaffold.success-criteria.md:41`.
- **T2 (no retention contract for the five traceability inputs) - fixed.** The proof-start precondition is stated at `bounded-convergence-option-b-proof.md:11-19` and re-stated as the gate at `:156` and criterion 11 (`:198`), including "Provenance entries do not satisfy this precondition or enforce retention." The orchestrator-owned action is recorded in `docs/plans/agent-scaffold.ledger.md:551` ("RETENTION RECORD: `q86-synthesis-r1-triage.md` through `q86-synthesis-r5-triage.md` are a fixed evidence sample exempt from routine cleanup until `bounded-convergence-option-b-proof` completes"), which lands on `main` at `b3fc80ef`, i.e. before this step can start. All five paths exist and parse today.
- **T3 (blind-closure findings had no coherent disposition) - fixed for the cases it names.** A new "Blind-closure discovery and routing" section (`:72-87`) makes closure an explicit one-batch discovery stage with a route table for current-, completed-prior-, future- and unowned owners plus upheld and overturned serious dismissals, plus fixtures (`:99`), mutation classes (`:164`) and criterion 4 (`:191`). `Q-86-safety-process.md:332-344` and `Q-86-synthesis.md:125` carry the same reconciliation, so M2's former unqualified "terminal" wording no longer conflicts with the future-owner continuation. Finding 1 below is the residue of this repair, not a re-raise of T3.
- **T4 (minimum-domain qualification did not reach the decision sources) - fixed in three of the four surfaces that carry the claim.** `Q-86-synthesis.md:101-123,161`, `docs/plans/agent-scaffold.questions/Q-86.md:21` and the structured ask at `agent-scaffold.plan.toml:2591` are now qualified. Finding 2 below is the surface the repair missed.

I also re-checked the round-1 and round-2 repairs and found no regression: order 117 is unique and last in both declaration order and sort order; the root-relative command contract and its temporary-state protocol are internally consistent (`:170-184`, criterion 13); the source-derived traceability gate is required rather than a hard-coded count (`:31`, `:156`); the cross-phase route model is present (`:61-70`); the ledger-currency assertion is now framed as an orchestrator integration duty (`:160`); and the historical recommendation tense is corrected (`Q-86-safety-process.md:491-514`).

I independently re-derived every published bound from the step's own typed costs and all five hold: `C_q = 4n_q + 1` (4 batches per obligation plus one closure); `R_B = 7 + sum(4n_q + 1) = 7 + 4|O| + (m+1) = 4|O| + m + 8`; `L_q = n_q + 1`; `L_B = r_plan + sum(n_q + 1) = r_plan + |O| + m + 1`; `I_B = 34 + 18|O| + 4(m+1) = 18|O| + 4m + 38` at 2 reviewers + 1 triage + 1 re-check per batch, 6 plan repairs and 2 repairs per obligation. The `n_q = 0` edge (`L_q = C_q = 1`, closure only) is consistent with `Q-86-safety-process.md:346`.

## Findings

### Finding 1 - the blind-closure "exhaustive route product" omits the scope disposition the step separately requires and makes delivery-blocking

**Severity: medium.**

**Evidence.** `bounded-convergence-option-b-proof.md:76` states "The stage has one exhaustive route product:" and the table at `:78-85` enumerates exactly six rows: the four owner routes, plus upheld and overturned high-or-critical dismissals. No row carries a scope-referred component, and neither does the "Delivery consequence" column.

Scope referral is a live, orthogonal disposition axis in the same model, not an owner route:

- `:91` records "scope relation" and "triage disposition" as separate fields on every finding, alongside "its derived owner route".
- `:106` requires that "A critical scope result remains delivery-blocking while any attached scope or dismissal re-check settles. No later repair, verification, or upheld dismissal may clear that block accidentally."
- `:95` requires named product fixtures "in every authority state where they are legal", and `:102` lists "scope referral plus dismissal referral, two simultaneous scope referrals, and high plus critical scope outcomes" among them. `BlindClosureDiscovery(q)` is an authority state, and nothing in `:72-87` or anywhere else in the step makes a scope referral illegal in that batch.
- The selected scope firewall itself is severity-routed with four distinct outcomes (`Q-86-safety-process.md:255-259`): low to backlog, medium to a terminal human scope decision, high through independent re-check, and a critical to `SeriousBlocked` "regardless of whether it cites a frozen obligation".

The closure fixture bullet (`:99`) lists only valid current-owner, upheld and overturned current-owner serious dismissals, completed-prior, unowned, and future-owner closure findings. Criterion 4 (`:191`) says only "The closure route table covers valid findings and upheld or overturned serious dismissals for all four owner routes", and the closure mutation classes at `:164` name stage bypass, stale-evidence delivery, future-component terminalisation/loss/early activation, prior-and-unowned delivery, skipped re-check, overturned-as-upheld, and completion without settled closure evidence - none of them scope. `grep -n scope docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md` returns no hit between `:72` and `:90`. The same omission is in both retained decision sources: `Q-86-safety-process.md:332-338` lists the same five closure routes with no scope bullet, and `Q-86-synthesis.md:125` likewise. So this is a specification gap, not a projection mismatch.

**Failure an implementer reaches.** Build the closure reducer from the table as instructed and feed it the batch the step's own fixture list requires: `BlindClosureDiscovery(q)` returns one triaged component whose scope relation is scope-expanded and whose severity is `critical`. Two readings are available and the step does not choose between them.

1. Treat the table as exhaustive. The component matches no row, so the reducer has no route for it. If it drops the component, closure settles clean and the family can construct `Complete` (`:47`) with an unresolved critical scope result live, which directly violates `:106` and the `SeriousBlocked` rule at `Q-86-safety-process.md:257`. If it fails closed instead, the required fixture at `:102` is unconstructible in this authority state and the proof cannot satisfy `:95`.
2. Force it into the `Unowned` row. That is wrong in the other direction: `:55` reserves `UnownedInScopeFinding` for "A later genuine violation with no canonical owner", and a scope expansion is by construction not a violation of any frozen obligation (`Q-86-safety-process.md:255`). It also silently converts a low scope expansion, which the shared package permits to be backlogged, into a delivery blocker.

The pending-re-check question is equally unstated. Row 5 makes closure stay in `AwaitingDismissalRecheck` for a serious *dismissal*, but a high scope ruling takes "the same independent backstop re-check" (`Q-86-safety-process.md:257`) and nothing says whether that pending re-check holds closure open the same way.

**Why this severity.** The proof is still a blocking gate that fails closed before any production authority, and the general scope machinery exists elsewhere in the model, so this cannot ship an unsafe controller today. But one branch of the missing routing touches the unresolved-critical invariant that the whole selected safety package rests on, the table asserts an exhaustiveness it does not have, and no fixture or mutation class would catch a reducer that got it wrong. That is the same class and impact as the round-3 T3 verdict, so medium is proportionate; it is not high because delivery of the defect is still gated behind two clean review rounds on the proof itself.

**Suggested correction.** Either state explicitly in `:72-87` that a scope-referred component is illegal in a blind-closure batch and add a mutation that kills a reducer accepting one, or extend the route product so scope composes with the owner routes: give the table a severity-routed scope row (low backloggable and non-blocking, medium to the terminal scope decision, high held in the closure-pending state until its independent re-check settles and then routed as valid-in-scope or terminal, critical into `SeriousBlocked` and never closure evidence), add the closure scope fixtures to `:99` and the matching killing mutations to `:164`, and extend criterion 4 to name the scope outcomes. Mirror the choice into `Q-86-safety-process.md:332-338` and `Q-86-synthesis.md:125` so the decision sources and the executable specification agree.

### Finding 2 - the owning step still publishes Option B's minima without the ordinarily-delivering domain the round-3 repair added everywhere else

**Severity: low.**

**Evidence.** `docs/plans/agent-scaffold.steps/workflow-calibration.md:26` reads:

> The proposed Option B bounds remain post-freeze phase minimum `n_q + 1`, post-freeze phase maximum `4n_q + 1`, whole-family minimum `r_plan + |O| + m + 1`, whole-family maximum `4|O| + m + 8`, and automated-agent maximum `18|O| + 4m + 38`. They are proof obligations, not controller constants.

Both minima are unqualified. Every other surface this fold touches carries the domain:

```text
grep -rn 'n_q + 1' docs/plans --include=*.md | grep -v agent-scaffold.reviews/
# questions/Q-86.md:21          "minimum over clean, ordinarily delivering family paths that eventually construct `Complete`"
# success-criteria.md:41        "`L_q` and `L_B` apply only to explicitly preconditioned clean, ordinarily delivering `Complete` paths"
# Q-86-synthesis.md:101,123,161 "clean, ordinarily-delivering `Complete`-domain minimum" + the explicit domain paragraph
# Q-86-safety-process.md:356    "On an ordinarily delivering path that eventually constructs family `Complete` ..."
# steps/workflow-calibration.md:26   (no qualifier)
```

The structured ask carries it too (`agent-scaffold.plan.toml:2591`). The gap reaches the human-facing projection unchanged at `docs/plans/agent-scaffold.md:730`.

`git log` confirms the omission is a miss rather than a deliberate exception: the sentence was authored by the fold commit `9e921190` and the round-3 domain repair `bc04f67f` touched `plan.toml`, `questions/Q-86.md`, the proof step, `success-criteria.md`, `Q-86-safety-process.md` and `Q-86-synthesis.md` but not `workflow-calibration.md`.

**Why this matters.** As round-3 T4 established, an unqualified `L_q`/`L_B` contradicts the model's own transition relation: the same step admits early `TerminalChoice` for an unowned or completed-prior-owner finding (`bounded-convergence-option-b-proof.md:46,66,68`) and legal non-delivery paths that finish below both numbers, which `:136` now says explicitly lie outside the minimum domains. `workflow-calibration` is the owning step for the whole Q-86 design pass and the surface a resuming reader reaches first, so it should not state the one formula the proof is required to derive in a form the proof would reject.

**Why low.** The authoritative proof step and the algebra criterion are correct and are what gates implementation, so a conforming proof cannot be made unsound by this sentence. It is documentation currency only, exactly as round-3 T4 was rated.

**Suggested correction.** In `docs/plans/agent-scaffold.steps/workflow-calibration.md:26`, label the two minima as clean, ordinarily delivering `Complete`-domain minima and add the sentence that legal early-terminal and non-delivery paths lie outside those domains and may be shorter, matching `questions/Q-86.md:21`. Re-render; do not hand-edit `docs/plans/agent-scaffold.md`.

## Severities with no findings

- **critical: none.** I found no path by which this planning fold authorises production behaviour, a controller constant, a floor, a pack or code change, or an implementation unit. `bounded-convergence-option-b-proof.md:3,21,202,212`, `Q-86.md:45-47`, the plan's `AUTHORITY BOUNDARY`, and criterion 15 all hold the line, no step declares `blocked_by = ["bounded-convergence-option-b-proof"]` because no production unit exists yet, and the two JSONL receipts (records 498 and 499) match their structured questions exactly on options, recommendation, chosen value and `task`.
- **high: none.** The published algebra is self-consistent and each coefficient is derivable from the step's own typed costs; the traceability gate derives its 51-identity source set rather than asserting it; the retention precondition is genuinely recorded before the step can start; and the `L_q` lower-bound argument is now a conclusion of the transition relation with an in-domain killing witness, which is what round 3 required.

## Things I checked that are not findings

- **The new `docs/plans/workflow-calibration.proofs/` directory does not disturb the drift-guard population.** That selector reads the first non-blank non-heading line of each Roadmap step sidecar (`sidecar-status-opening-drift.md:58`); the new sidecar opens "Q-86 selected ...", which carries no status label, so the human-confirmed 43/34/26/17 snapshot (Q-84, Q-87) is unchanged and no criterion needed updating.
- **Provenance path form.** The step's `findings` entries are task-relative (`agent-scaffold.reviews/...`), which matches the documented convention in `src/plan/source.rs:246-249` ("task-relative paths") and existing entries such as `agent-scaffold.plan.toml:777`. The mixed full-path entries elsewhere in the file predate this fold.
- **The `nix shell nixpkgs#python3 -c python3 <script> --flag` command form.** Reproduced against a stub in round 1; `-c` consumes the remaining arguments, so the flags reach the script. `PYTHONDONTWRITEBYTECODE=1` on all five commands forecloses the `__pycache__` artefact the mutation runner's import would otherwise leave for criterion 13's manifest to flag. Registry-versus-locked `nixpkgs` resolution is the established convention of the retained explorations and predates this fold.
- **The `ClosureCurrentOwnerBlock` versus deferred-reopen tension.** `:59` would make a finding against a closed current-phase owner a live deferred reopen, while the closure table sends it to `ClosureCurrentOwnerBlock`. The closure section scopes itself explicitly to `BlindClosureDiscovery(q)` results and states the reason (stale closure evidence, `:87`), so the specific rule governs and this is not ambiguous.
- **Acceptance as the last frozen phase.** `:70` implies it without asserting it as an invariant, which is what keeps a future-owner route out of the final phase's closure. It is implied consistently by every route example and by `Q-86-safety-process.md:324`, so I did not raise it.
- **The ledger record names the five files by range rather than by five full paths** (`ledger.md:551`) where `bounded-convergence-option-b-proof.md:156` says "five exact paths". The filenames are unique in the tree and `success-criteria.md:41` uses the same range form, so the precondition is satisfied in substance; not worth a finding.

## Counts

- Findings: **2** - **0 critical, 0 high, 1 medium, 1 low**.
