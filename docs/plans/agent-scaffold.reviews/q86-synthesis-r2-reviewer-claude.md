# Q-86 synthesis round 2 - reviewer (claude)

Lens: human-decision readiness, safety, and adoption. Reviewed range `main..66fb8dcf` (`62c6ddd9..66fb8dcf` is the repair), artifact treated as `risky`. Worktree `.agents/worktrees/q86-synthesis-r2-claude`. No reviewed product or prior findings file was edited; scratch scripts were written to `/tmp/q86scratch/` only.

## What I reproduced

Every published number in the repair reproduces exactly.

```sh
CHECKER=docs/plans/workflow-calibration.explorations/q86-controller-proof.py
nix shell nixpkgs#python3 -c python3 "$CHECKER" --mode all --phase acceptance --risk risky --obligations 2 --floor high
nix shell nixpkgs#python3 -c python3 "$CHECKER" --mode all --phase acceptance --risk risky --obligations 2 --floor critical
for n in 0 1 2 3; do nix shell nixpkgs#python3 -c python3 "$CHECKER" --mode B --phase work:example --obligations "$n" --floor high; done
nix shell nixpkgs#python3 -c python3 "$CHECKER" --mode A --phase work_review --risk risky --floor high
nix shell nixpkgs#python3 -c python3 "$CHECKER" --mode C --phase work_review --risk low_risk --floor high
sha256sum "$CHECKER"
docs/plans/workflow-calibration.explorations/q86-q78-scope-replay.sh docs/metrics/workflow.jsonl
jq -s 'map(select(.type == "round" and .task == "q78-design-pass" and .phase == "acceptance")) | {passes: length, valid_shortfalls: map(.valid_findings)}' docs/metrics/workflow.jsonl
jq -s 'map(select(.type=="round" and .outcome=="clean" and (.valid_findings // 0) > 0)) | length' docs/metrics/workflow.jsonl
nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml
nix develop -c cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow
```

All state/edge/terminal/acyclic/`max_reviews`/`bad_*` counts in `Q-86-synthesis.md:232-240`, `Q-86-safety-process.md:408-414`, and `Q-86-state-machine.md`'s reproduction block match byte for byte. The checker SHA-256 is `db2874d8654957582f18592ece030f344b60ca9657c127715fcc78d6987ef9a7` as claimed. The replay prints `summary passes=10 terminal_replans=4 families=5 additional_human_receipts=4 additional_plan_review_and_freeze_cycles=4`. The selector returns ten passes and `[7,10,5,6,5,5,4,2,1,0]`; the nineteen `clean`-with-findings rounds check returns `19`. Severities are `["high",...]` on passes 3-6, `["medium","medium","low","low"]` on pass 7, and low-only on 8-10, so the A and C replay statements at `:96` and `:191` are accurate. Strict render is `up to date` and `validate --workflow` reports 479 records, 114 steps, 87 questions, invariants hold. Arithmetic checks: `7 + 4|O| + p = 4|O| + m + 8`, `4R_B + 6 + 2|O| = 18|O| + 4m + 38`, A's `14+7+7+6 = 34`, C's `5+4+4+2 = 15`, and the T11 counterexample direction (at `m = 3, |O| = 1`, B = 68 < C = 75) all hold.

## Result

Ten findings: **one high, four medium, five low. No critical.** Five of the ten are new defects introduced by the repair itself (R2C-1, R2C-3, R2C-5, R2C-8, R2C-10). Two are partial-closure findings against round-1 verdicts, each carrying new evidence that the correction is incomplete (R2C-4 on T1, R2C-6 on T14). No settled round-1 finding is re-raised on its original evidence.

---

### R2C-1 (high). The repair deleted Option B's checkable successor-scope rule and its chain bound, leaving the source proposal self-contradictory and the enforcement inventory silent

**Evidence.**

The pre-repair synthesis carried a mechanical successor constraint. `git diff 62c6ddd9..66fb8dcf -- docs/plans/workflow-calibration.explorations/Q-86-synthesis.md` shows the removed line:

```
-- `Replan` ends the family, ... A successor needs a new human receipt and a strictly narrower or disjoint obligation set. It is not a resume transition.
+- `Replan` ends the family, ... A successor needs a new human receipt and materially different scope.
```

The replacement is at `Q-86-synthesis.md:73`, and `:127` matches it ("a differently scoped successor requires a new human receipt, plan review, and freeze").

The rule was not dropped from the cited source. `Q-86-safety-process.md:276` still states it formally: "`O_new` is a proper subset of `O_old` union the carry set, or `O_new` and `O_old` are disjoint", and `:279` derives the bound from it: "the chain of narrowing replans on a given original scope is bounded by `|O_initial|`".

That surviving rule now contradicts the replay the same repair added. `Q-86-safety-process.md:369` and `Q-86-synthesis.md:162-171` admit successors F2-F5 on Q-78 passes 2, 4, 7, and 8, and every one of those four events is a scope **addition** (`Q-58/Q-82`, `Q-83`, `Q-85/Q-86`, `Q-87`); reproduce the artifact strings with `jq -r '[inputs] | map(select(.type == "round" and .task == "q78-design-pass" and .phase == "acceptance")) | to_entries[] | "\(.key+1)\t\(.value.artifact)"' -n docs/metrics/workflow.jsonl`. An expanding successor is neither a proper subset of `O_old union carry` nor disjoint from `O_old`, so the new replay is illegal under the proposal's own `:276`.

The repair also deleted the red-control row that carried the chain bound. `git diff 62c6ddd9..66fb8dcf -- docs/plans/workflow-calibration.explorations/Q-86-safety-process.md | grep 'Chain of narrowing replans'` returns only the deletion (`-| **Narrowing or replan** | ... Chain of narrowing replans bounded by `|O_initial|`. ...`). The replacement rows at `Q-86-safety-process.md:429` and `Q-86-synthesis.md:251` state only the per-family terminal event.

Nothing replaces it. `Q-86-synthesis.md:259` enumerates what `validate --workflow` enforces - "exact ids, phase identity, monotone authority, repair-before-verification, finding dispositions, dismissal re-checks, no action after terminal state, and no delivery with an unresolved critical" - and contains no successor-scope check. `:47` forbids fresh authority only for "an **unchanged** replan", so a scope-changed replan grants a full fresh allowance by design, and `:127` makes that replan **automatic** on any scope-digest change.

**Consequence.** B's headline claim to the human is that it "makes scope movement terminal rather than invisible" (`:276`) and that the replay "is the exact mechanism by which B prevents a moving acceptance target from laundering authority" (`:173`). As now specified, a scope change is both the trigger for the replan and the sole qualification the successor needs, so the constraint is satisfied by its own trigger: for every positive integer `n`, `n` scope changes yield `n` receipted successors, each with a full fresh `4|O'| + m + 8` allowance and no bound on the chain and no mechanical check on `O'`. That is structurally the same shape as the baseline disproof at `:29` (which is also human-gated), differing only in that dispositions cannot be laundered. Additionally, an implementer working from `Q-86-safety-process.md` will find `:276` and `:369` mutually exclusive and cannot tell which rule B adopts.

**Smallest safe correction.** State in one sentence which successor-scope rule Option B adopts. If it is the state-machine proposal's "materially different obligation or exclusion set" (`Q-86-state-machine.md:97`), say so explicitly at `Q-86-synthesis.md:73`, note that it replaces the safety proposal's stricter rule and that the replan chain is consequently bounded only by human receipts, and correct `Q-86-safety-process.md:276` so it stops contradicting `:369`. If it is the strictly-narrower-or-disjoint rule, restore it at `:73` and state that the Q-78 replay's four expanding successors would then be illegal and delivery would stop at pass 2. Either way, add the chosen rule to the `validate --workflow` enforcement list at `:259` and restore a "chain of replans" entry to the red-control table at `:244-253`.

---

### R2C-2 (medium). Option B's minimum review cost scales with `|O|` and is never stated; the comparison and the human ask carry only upper bounds

**Evidence.**

B's transition table makes `InitialAttempt` consume one review batch **per obligation** (`Q-86-synthesis.md:120`), and `BlindClosure` is legal only once "All obligations closed" (`:126`). The durable proof implements exactly that: `q86-controller-proof.py:227-232` permits at most one obligation to act per batch, and `:304` gates blind closure on `b_all_closed`. So a phase's best case - every obligation clean on first attempt, no findings at all - still costs `n_q + 1` review batches.

Reproduce (script in `/tmp/q86scratch/mincost.py`, BFS for the smallest `reviews` at `control == "complete"`):

```text
A acceptance risky  min_reviews_to_complete = 1
A work_review risky min_reviews_to_complete = 2
C risky             min_reviews_to_complete = 2
C low_risk          min_reviews_to_complete = 1
B obligations=0 bound=1  min = 1
B obligations=1 bound=5  min = 2
B obligations=2 bound=9  min = 3
B obligations=3 bound=13 min = 4
B obligations=4 bound=17 min = 5
B obligations=5 bound=21 min = 6
```

The synthesis compares only maxima. `:150` says the bounds "cannot be ranked universally against C's `15(m + 2)` without parameter values"; `:197-204`'s "Minimal by default" row judges B on schema size ("Adds canonical obligation rows and the largest schema") and never on review volume; `docs/plans/agent-scaffold.plan.toml:2566` gives the human `C_q = 4|O_q| + 1` and `4|O| + m + 8` with no floor. The human is also given no way to estimate `|O|`: the three source labels at `:104-109` join Success Criteria, numbered principles, and Roadmap documentation-impact rows, and this plan has 39 Success-Criteria bullets (`grep -c "^- " docs/plans/agent-scaffold.success-criteria.md`) and 8 principle rows (`grep -c "^\[\[principle\]\]" docs/plans/agent-scaffold.plan.toml`), so an order of tens is the realistic range.

**Consequence.** On a clean, defect-free family, B costs `|O| + p` post-freeze review batches (two reviewer calls each) where A costs about `m + 2` and C about `2(m + 2)`, independent of `|O|`. At a modest `|O| = 20, m = 3`, B's best case is 24 post-freeze batches against A's 4 and C's 8 - a difference in ordinary running cost that is larger than any of the differences the comparison table does discuss, and it is the axis on which the recommended option is worst. A human weighing "Minimal by default" and adoption burden is not shown it.

**Smallest safe correction.** Add one sentence to the "Phase allocation, bound, and cost" section stating the per-phase minimum `n_q + 1` and the family minimum `|O| + p + (plan review)`, contrast it with A's and C's `|O|`-independent minimums, and carry the same fact into the `ARCHITECTURE OPTIONS` entry for B at `docs/plans/agent-scaffold.plan.toml:2566`.

---

### R2C-3 (medium). The B proof reaches a delivering terminal in two edges with zero reviews and every obligation untested

**Evidence.**

`q86-controller-proof.py:316` appends the `request_beyond_declared_authority` edge from **every** `active` state, with no guard on `state.reviews` against `limit`:

```python
edges.append(("request_beyond_declared_authority", BState(state.phase, state.obligations, state.reviews, exhausted_control, state.finding)))
```

From the resulting `exhausted` control, `:326-328` offers `accept_residual` whenever no outstanding serious finding and no pending re-check exist - which is trivially true when nothing has been reviewed. Reproduce (script in `/tmp/q86scratch/deliver.py`, shortest path to `control == "delivered_residual"`):

```text
B n=2 shortest path to delivered_residual: ['request_beyond_declared_authority', 'accept_residual']
   final state: reviews=0 obligations=('accepted_untested', 'accepted_untested')
   delivered_residual states=73, of which carry an untested obligation=19
B n=3 shortest path: same two edges; delivered_residual states=314, of which carry an untested obligation=142
```

**Consequence.** The reported `bad_delivery=0` is only a check that a delivering terminal carries no open critical and no pending re-check; the enumeration additionally contains 19 of 73 (`n=2`) delivering terminals in which an obligation was never tested, and permits the whole terminal menu from a state where no authority has been spent. So the proof does not establish two properties the synthesis leans on: that a terminal decision is reachable only at declared exhaustion or a genuine block (`:128`, "Declared authority exhausted | `AuthorityExhausted` ..."), and that delivery requires obligation closure - the basis for calling B "the strongest structured completion model" (`:177`) and for the "prevent unverified closure" claim at `:201`. The direction is conservative for the three invariants actually counted (a superset graph with zero violations still implies zero on the real graph), so this weakens the proof's coverage rather than falsifying its stated results.

**Smallest safe correction.** Guard the edge at `q86-controller-proof.py:316` with `if state.reviews >= limit` (or with "no other legal action exists"), add a `bad_undelivered_obligation` counter that flags any state in `delivery_controls` holding a non-`closed` obligation, re-run the published command block, and update the counts at `Q-86-synthesis.md:232-240` and `Q-86-safety-process.md:408-414`.

---

### R2C-4 (medium). T1's correction is partial: all three corrected controllers hold at most one outstanding finding, so the scenario T1 named is unreachable and untested

This is not a re-raise of T1 on its original evidence - the numeric `critical` scalar is genuinely gone and the disposition machine is real. The new evidence is that the replacement still cannot construct the case T1 was about.

**Evidence.**

`q86-controller-proof.py:36-43` gives `AState` a single `finding: str`; `:108-114` does the same for `CState`; and `:227-232` restricts B to `permitted = {active[0]}` whenever any obligation is outstanding. Reproduce (script in `/tmp/q86scratch/structure.py`):

```text
A reachable states: 104
A states with control=='active' and an outstanding finding: 0
A distinct finding values at control=='active': ['none']
C states in a review stage with an outstanding finding: 6   (verify1/verify2 holding the *named* repaired finding only)
B max simultaneously outstanding obligations: 1
```

So no A state and no C `discovery`/`blind_closure` state can run a review batch while a finding is open, and B never holds two outstanding obligations. The design text does contemplate that state: `Q-86-synthesis.md:88` says a verification may "leave the finding open, or open a fix-induced finding", but the model's `verify_fail_X` opens no new finding (`:87` in the checker) and `verify_pass_new_X` closes the old one (`:91`), so "old finding still open **and** fix-induced finding open" is unreachable.

**Consequence.** The properties the proof is cited for - `Q-86-synthesis.md:88` "A later unrelated clean batch cannot clear the finding", `:185` "A later clean observation outside the named verification cannot clear a critical", `:53` "A counter, clean observation, unrelated later finding ... never clears it", summarised as the checked control at `:213` - are exactly the multi-finding case the models cannot construct. `bad_critical_clear = 0` holds because the offending state is unreachable, not because a transition was tested and rejected. That is a materially weaker guarantee than the round-1 required correction asked for, and it is the same failure mode T1 identified one level up.

**Smallest safe correction.** Either permit a discovery batch from a state that already holds an outstanding finding (for A/C, add a second finding slot; for B, drop the `permitted = {active[0]}` serialisation) and re-run, or state plainly at `Q-86-synthesis.md:208` that the controllers serialise findings by construction, so the no-unrelated-clear property holds structurally and is not established by enumeration.

---

### R2C-5 (medium). Under Option B the shared in-scope test admits categories the closed obligation source cannot represent, and the controller has no transition for such a finding

**Evidence.**

The shared safety package at `Q-86-synthesis.md:49` defines the scope firewall for all three options: "A finding is in scope when it demonstrates a violation of a frozen obligation, **invariant, boundary, or duty**", and "A critical finding is always in scope."

Option B's closed source at `:104-110` admits exactly three labels - `success_criterion`, `project_principle`, `documentation_impact` - and states: "The first implementation does not infer obligations from unstructured **invariants, trust-boundary prose**, exclusions, or a reviewed baseline."

The source proposal uses the narrower test and does not carry `:49`'s wording: `Q-86-safety-process.md:249` says a finding "is **in scope** if and only if the reviewer can cite a specific frozen obligation by its stable id".

The controller has no home for such a finding. `Q-86-synthesis.md:116-131` routes every transition through an obligation id; the only non-obligation finding modelled is `open_blind_*` at blind closure (`q86-controller-proof.py:306-308`). The `:110` mitigation ("A reviewer who finds a genuine uncited defect sends uncertainty to the human") is prose, is absent from the transition table, and is absent from the `validate --workflow` list at `:259`.

**Consequence.** Under B, a reviewer applying `:49` rules an invariant or security-boundary violation in scope while `:104-110` denies it any obligation row, so the finding cannot be opened, repaired, or verified inside a phase campaign, and the phase's completion predicate ("all obligations closed" plus one blind batch) can be satisfied with it outstanding. Because `:49` also says "A critical finding is always in scope", the same gap applies to a critical discovered outside blind closure. The synthesis does price obligation incompleteness as a risk at `:110`, `:177`, and `:278`, but it does not disclose that the shared scope test and B's closed source disagree about which categories exist.

**Smallest safe correction.** Make `:49` conditional on the chosen option, or state at `:104` that under B the in-scope test is `Q-86-safety-process.md:249`'s "cites a frozen obligation id" plus the always-in-scope critical rule, and add one explicit transition (and one red-control row) for an in-scope finding that no obligation owns.

---

### R2C-6 (low). T14's `LegacyNoRubric` state has no replay or red control, which its round-1 correction required

Partial closure, with new evidence. The typed state itself is specified as required.

**Evidence.** T14's required correction ends: "Add validation and replay controls for that state." `Q-86-synthesis.md:153-154` specifies the state and asserts validation ("Validation rejects any direct `LegacyNoRubric -> FrozenObligationCampaign` edge"), but `grep -rn "LegacyNoRubric\|legacy" docs/plans/workflow-calibration.explorations/q86-controller-proof.py docs/plans/workflow-calibration.explorations/q86-q78-scope-replay.sh` returns nothing (exit 1), and the red-control table at `:244-253` has no row for it.

**Consequence.** The only population Principle "Safe on existing projects" protects under B - an active task already past plan review with no frozen `O` - is covered by an assertion, while every other B path now has an enumerated control. The principle table at `:199` nevertheless credits B's `LegacyNoRubric` under that principle.

**Smallest safe correction.** Add one `LegacyNoRubric` row to the red-control table at `:244-253` stating its exact terminal event, and either add the state to `q86-controller-proof.py` (asserting no edge into `FrozenObligationCampaign`) or say in the text that it is specified but not enumerated.

---

### R2C-7 (low). The no-decision boundary names A's and B's uncalibrated constants but omits C's

**Evidence.** `Q-86-synthesis.md:298` closes with: "The baseline, severity gate, A's five-plus-two values, B's one reopen, the serious floor, and any implementation are not silently approved by Q-85 or this synthesis." C's four-stage depth and two-repair limit (`:183`, `:187`) are as weakly calibrated as A's five-plus-two, and are absent from that list. This is not a re-raise of T6 (which concerned the serious floor and is closed); it is the same failure mode recurring for a different constant in text the repair rewrote.

**Consequence.** T6 was upheld on the reasoning that a reader treats the enumerated no-decision list as exhaustive. If the human chooses C, the enumeration reads as approving C's stage depth. `docs/plans/agent-scaffold.plan.toml:2578` does carry a blanket "no ... numeric constant ... is approved", so the human-facing ask is safe; the defect is confined to the synthesis's own boundary paragraph.

**Smallest safe correction.** Add "C's four-stage and two-repair depth" to the list at `:298`.

---

### R2C-8 (low). The status paragraph claims the pass changes no generated plan, in the same commit that changes it

**Evidence.** `Q-86-synthesis.md:5` reads: "It changes no workflow rule, cap, reset behaviour, metric, specification, pack file, prompt, template, README, changelog, **generated plan**, or Rust source." The repair added "generated plan" to that list (`git diff 62c6ddd9..66fb8dcf -- docs/plans/workflow-calibration.explorations/Q-86-synthesis.md`), and the same commit modifies the generated projection in four hunks: `git diff --stat 62c6ddd9..66fb8dcf -- docs/plans/agent-scaffold.md` reports `1 file changed, 12 insertions(+), 9 deletions(-)`.

**Consequence.** The sentence exists to fix the change boundary a reader or a later auditor checks the diff against. As written it is falsified by the diff it describes. No rule actually changed - the projection change is exactly what `render --check --strict` requires after the TOML edit - so this is a wording defect, not a boundary breach.

**Smallest safe correction.** Change "generated plan" to "generated plan beyond the required projection of the Q-86 question and Success Criteria edits", or drop the item.

---

### R2C-9 (low). The synthesis presents per-phase enumeration as evidence for whole-family bounds without stating the composition step

**Evidence.** Every published run is single-phase: `check_b` (`q86-controller-proof.py:446-449`) builds one phase and `state.phase` is inert on every edge; `check_c` (`:428-430`) ignores `--phase` entirely, which is why `C phase=acceptance risk=risky` and `C phase=work_review risk=risky` both return `states=79 edges=135`. The whole-family figures `7(m + 2)` (`Q-86-synthesis.md:92`), `4|O| + m + 8` (`:141`), and `4(m + 2)` (`:187`) are therefore algebra over per-phase results plus the asserted no-transfer rule at `:135`, which nothing enumerates. `:211` nonetheless lists "Review spend never exceeds the stated bound" among the checker's checks, immediately before the whole-family bounds. The source proposal is explicit where the synthesis is not: `Q-86-safety-process.md:416` says "The algebra proves the parameter not covered by the finite sweep."

**Consequence.** A reader takes the family bound in the human ask (`docs/plans/agent-scaffold.plan.toml:2566`) as enumerated when only its per-phase factor is.

**Smallest safe correction.** Add `Q-86-safety-process.md:416`'s sentence to `Q-86-synthesis.md:208-215`: the enumeration bounds one phase, and the family bound follows by summation under exact phase ownership and no transfer.

---

### R2C-10 (low). The durable proof artifact drops `medium` from its severity alphabet without saying so

**Evidence.** `q86-controller-proof.py:6` defines `SEVERITIES = ("low", "high", "critical")` and `:31-33` ranks `{"low": 1, "high": 2, "critical": 3}`. The project's scale is the four-level `low`/`medium`/`high`/`critical` (`AGENTS.md:21`, `:141`), and `medium` is the modal severity in the very sequence being replayed (passes 1-7 of Q-78). The superseded AWK checker documented the collapse explicitly ("`L` for a valid low or medium finding"); the deletion of that checker removed the note without replacing it. The omission is behaviourally harmless for the two floors on offer, since `medium` sorts below both `high` and `critical` and so behaves identically to `low`.

**Consequence.** The durable artifact an implementer will work from appears to omit a severity level of the production scale, and its safety conclusion silently depends on the floor never being set to `medium` - a value the co-decision at `:60-64` does not offer but also never rules out.

**Smallest safe correction.** Add one comment at `q86-controller-proof.py:6` stating that `low` stands for every below-floor severity including `medium`, and that the model is valid only for `FLOOR is `high` or `critical``.

---

## Round-1 closure verification

| Round-1 | Verdict | Closure |
| --- | --- | --- |
| T1 (high) | Corrected, **partially**. `AState`/`CState` now carry finding and disposition state and the numeric scalar is gone; the A and C models exhaust and report zero critical-clear violations. See **R2C-4** for the residual gap. | Partial |
| T2 (high) | Closed. `Q-86-synthesis.md:113-131` specifies one `FrozenObligationCampaign` with initial/reopen attempts, repair, verification, closure, re-check, blind closure, scope, exhaustion, and terminal transitions; `q86-controller-proof.py` mode B enumerates that controller and reaches `4n_q + 1` for `n = 0..3`. The disproved `2\|O\| + 8` is explicitly withdrawn at `:144`. | Closed |
| T3 (medium) | Closed. `docs/plans/agent-scaffold.success-criteria.md:41` now requires Q-86 `open` against the completed synthesis and keeps implementation blocked; strict render passes and the projection at `docs/plans/agent-scaffold.md:5114` agrees. | Closed |
| T4 (high) | Closed. `q86-q78-scope-replay.sh` plus the table at `:162-171` assign a typed transition and durable result to all ten passes, and the cost appears in the trade-off at `:173`, the ask at `plan.toml:2566`, the question sidecar, and the step sidecar. The four detected events match the four scope-bearing artifact strings. | Closed |
| T5 (medium) | Closed. A's pass-seven/three-low and C's pass-three/23 results are in `:96`, `:191`, and the ask; the "most bounded late discovery" universal is gone, replaced by the qualified `:96` comparison. | Closed |
| T6 (medium) | Closed. `:57-64` presents the floor as a named co-decision with its Q-78 consequence; `plan.toml:2571-2574` offers `high`/`critical`/`defer`; the floor appears in the no-decision boundary at `:298` and `plan.toml:2578`; the proof exhausts both values. | Closed |
| T7 (medium) | Closed. `:135` gives the source-owned allocation `C_q = 4n_q + 1` with a one-batch minimum at `n_q = 0`, freeze rejects a bad owner or allocation, bounds are recomputed, and the `n = 0` and `n = 1` red controls run in the published sweep. | Closed |
| T8 (medium) | Closed. `:104-110` restores a closed three-label source with exact joins and states the YAGNI boundary and the incompleteness risk. See **R2C-5** for a new inconsistency this created with the shared scope test. | Closed |
| T10 (medium) | Closed. `:278` sends a failed proof of concept back to the human with A as the recommendation and "No fallback architecture is pre-authorised"; the gate is in the ask and both sidecars. | Closed |
| T11 (low) | Closed. `plan.toml:2576` replaces the universal with a per-phase-depth claim and names the differing parameters; I confirmed B < C at `m = 3, \|O\| = 1` (68 vs 75), so the non-universality is real. | Closed |
| T12 (low) | Closed as an ownership boundary. The ledger is correctly outside `main..HEAD`, `docs/plans/agent-scaffold.ledger.md:535` now distinguishes `main` from the branch ("Q-86 remains `exploring` on `main`; branch `plan/q86-synthesis` proposes moving it to `open`"), and the same paragraph records "T12 remains the orchestrator's ledger move when the branch merges". No planner action was owed and none was taken. | Closed |
| T14 (medium) | Corrected, **partially**. `:153-154` specifies the typed `LegacyNoRubric` state, its exemption, its inability to mint authority, its two human paths, and the rejected direct edge. See **R2C-6** for the missing replay/red control. | Partial |
| T16 (low) | Closed. The label map is at `:13`. | Closed |
| T9, T13, T15, T17 | Ruled invalid in round 1; nothing in the repair changes that, and I raise no new evidence against those verdicts. | N/A |

## Decision-readiness checks

- **Recommendation follows from evidence:** mostly. B is recommended at medium-to-low confidence, gated on a schema and reconstruction proof of concept, with the overturning evidence named at `:280`. The cost side of the comparison is incomplete in two ways (**R2C-2**, **R2C-1**), so the human is choosing on an understated cost picture rather than on a wrong one.
- **All low-confidence constants unapproved:** yes in the human-facing ask (`plan.toml:2578` blankets "numeric constant"); one omission in the synthesis's own boundary paragraph (**R2C-7**).
- **Every option includes safe terminal choices:** yes. In the enumerated controllers, `terminal`, `exhausted`, and `serious_blocked` always offer the four non-delivery actions, `accept_residual` is offered only below the floor, and `bad_delivery = 0` at both floor values for all three modes.
- **No budget conceals an unresolved critical:** holds for every enumerated path at both floors, subject to **R2C-4**'s reachability limitation and **R2C-3**'s unguarded exhaustion edge.
- **Plan, Success Criteria, sidecars, generated projection agree:** yes. `render --check --strict` is `up to date` and `validate --workflow` passes; the Q-86 ask, question sidecar, step sidecar, and Success Criterion all carry the same architecture set, floor co-decision, `4|O| + m + 8` bound, four-replan cost, and proof-of-concept gate.
- **Documentation-impact claim:** the step sidecar's "changes planning records and proof artifacts only" is accurate - `treefmt` in `flake.nix` formats only nix/rust/toml and prettier's `*.md`/`*.yml`/`*.yaml`/`*.json`, so the new `.py` and `.sh` are untouched by `nix fmt` and the published SHA-256 is stable. The synthesis's own boundary sentence is the exception (**R2C-8**). No non-ASCII characters in any changed file.
- **Reproducibility gap:** `Q-86-synthesis.md:216-227` gives an exact command block, expected output, and SHA for the checker but no command for `q86-q78-scope-replay.sh`, whose four-replan result is a headline number in the human ask. The command exists only in `Q-86-safety-process.md:569`. Adding it to the synthesis's proof section would close the gap; folded here rather than raised separately.
