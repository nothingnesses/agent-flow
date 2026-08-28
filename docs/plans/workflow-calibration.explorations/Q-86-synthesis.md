# Q-86 synthesis: bounded convergence options

## Status and decision boundary

Q-86 is `open` for a human decision. This synthesis reconciles the corrected proofs in `Q-86-state-machine.md` and `Q-86-safety-process.md`. It changes no workflow rule, cap, reset behaviour, metric, specification, pack file, prompt, template, README, changelog, generated plan, or Rust source.

The human decision is between three bounded architectures:

- `A - Sealed phase budget`.
- `B - Frozen obligations with sealed phase campaigns`.
- `C - Fixed-depth verification protocol`.

The source labels map as follows. Option A is the state-machine proposal's Candidate A and the safety proposal's M1. Option B is the safety proposal's corrected M2 plus the state-machine proposal's sealed authority envelope. Option C is the state-machine proposal's Candidate B. The safety proposal's M3 remains excluded.

The recommendation is `B - Frozen obligations with sealed phase campaigns`, at medium to low confidence. The corrected proof establishes its controller and finite bound. The Q-78 replay also establishes its substantial cost on moving scope. No mechanism or serious terminal floor has been chosen. Q-85 authorised only this design pass. Implementation remains blocked until the human decides Q-86 and the decision is receipted and folded into `workflow-calibration`.

## Evidence that constrains the decision

### Corrected Q-78 acceptance history

Run:

```sh
jq -s 'map(select(.type == "round" and .task == "q78-design-pass" and .phase == "acceptance")) | {passes: length, valid_shortfalls: map(.valid_findings)}' docs/metrics/workflow.jsonl
```

It returns ten passes and `[7,10,5,6,5,5,4,2,1,0]`. The run closed at pass ten. It demonstrates high review cost, late serious findings, four scope additions, and eventual closure. It does not demonstrate divergence.

The baseline remains non-admissible because its rules have reachable unbounded paths. For every positive integer `n`, five `new_valid` rounds followed by human `resume` can repeat `n` times and leave the loop active after `5n` rounds. For every positive integer `n`, an acceptance pass with a valid shortfall can route through repair to another acceptance pass and leave the campaign active after `n` passes. Convergence-first precedence closes neither construction. The baseline has no finite bound or exact forced terminal event and cannot be chosen.

### Evidence limitations

- Nineteen logged rounds have `outcome: "clean"` while `valid_findings` is greater than zero, and all nineteen advance `consecutive_clean`. Raw outcome and streak fields are not safe completion inputs.
- Only six of the ten Q-78 triage files remain. The severity tail in passes seven to ten depends on append-only summary records and is not used to establish any controller invariant.
- Historical findings have no stable cross-review identity. The Q-78 replay cannot infer which obligation a finding belongs to, whether a verification closed its parent, or whether a later report was pre-existing, fix-induced, duplicate, relitigated, or materially new evidence.
- The log contains one critical-bearing round and one dismissal re-check. That re-check was overturned. Critical legality and re-check behaviour are safety requirements with sparse empirical support, not calibrated rates.
- Q-78's two reviewer paths confound blindness, model, harness, lens, and brief. The local and external evidence supports separate blind discovery and informed verification briefs, not a causal yield estimate.
- `validate --workflow` can validate structured claims but cannot prove that an external agent performed an independent or genuinely blind review.
- The association between Q-78's scope additions and later findings is not evidence that the additions caused the findings.

The controllers do not use the broken outcome or severity arrays. They consume prospective triage-backed finding identities, dispositions, and per-finding severity. The historical arrays appear only in descriptive replay evidence.

## Shared safety package

### Identity, scope, and lineage

Authority belongs to an immutable `TaskFamilyId`, typed phase and loop identities, and ordered review-batch identities. Rename, rebuild, a new display name, human resume, or an unchanged replan cannot create fresh authority.

The acceptance rubric freezes after plan review and before implementation. A finding is in scope when it demonstrates a violation of a frozen obligation, invariant, boundary, or duty. A genuinely optional new capability or preference is `ScopeExpanded` and is backlogged without enlarging the current family. Uncertainty stays in scope or goes to the human. A triager, never the orchestrator, rules on scope. An out-of-scope ruling at `high` or `critical` requires the same independent re-check as a dismissal. A critical finding is always in scope.

Prospective finding state separates origin, scope relation, continuity, severity, and disposition. One stable `FindingId` survives reviewer reports, triage, repair, verification, re-check, later review, and acceptance. Duplicate reports retain report identities but join one finding. Relitigation without materially new evidence leaves the finding settled. Materially new evidence adds an evidence identity and may reopen the same finding root only where the chosen controller has declared reopen authority.

A valid critical has an explicit `Open -> ResolvedPendingVerification -> Resolved` path. `Repair` creates `ResolvedPendingVerification` but does not clear the open safety obligation. Only a named successful verification clears it. The other legal paths are terminal non-delivery dispositions such as `RemovedFromDelivery`, `RevertedWithArtifact`, `CarriedToSuccessor`, or `UnresolvedAbandoned`. A counter, clean observation, unrelated later finding, scope label, or human resume never clears it. A dismissed critical instead follows `AwaitingDismissalRecheck -> Dismissed` only after the independent re-check upholds dismissal.

Historical records are not rewritten and historical provenance is not invented. A digest-pinned adoption boundary separates legacy evidence from prospective controller state.

### Human co-decision on the serious terminal floor

The architecture choice does not settle the serious terminal floor `F`.

- `F = high` blocks ordinary residual-risk acceptance and ordinary narrowing while an open high or critical remains. This is the recommendation because the retained Q-78 triages show highs on passes three through six. If exhaustion had occurred on any of those passes, those two terminal choices would have been unavailable.
- `F = critical` is the mandatory safety minimum. It blocks those choices only for an open critical and leaves the human able to accept a high as residual risk. It preserves more human discretion at greater safety risk.

Both values retain the invariant that no unresolved critical can be delivered. The proof exhausts both values. The human must choose the floor with the architecture, or explicitly defer it to a second decision before implementation. It is not silently approved by choosing A, B, or C.

### Terminal choices

At exhaustion the human receives accept residual risk, narrow scope, revert, replan, and abandon through the human-input contract.

- `Accept residual risk` is legal only below `F`. It ends the current family and records a decision receipt plus a record-backed waiver naming every accepted finding.
- `Narrow scope` ends the family. With an open finding at or above `F`, ordinary narrowing is illegal. Removing the affected output from delivery is legal only as terminal `RemovedFromDelivery` with an exact exclusion.
- `Revert` ends the family at a named known-good artefact and records `RevertedWithArtifact`.
- `Replan` ends the family, preserves unresolved findings as `CarriedToSuccessor`, and keeps delivery blocked. A successor needs a new human receipt and materially different scope.
- `Abandon` ends the family, ships nothing, and preserves each unresolved finding and its evidence.

Backstop re-checks do not debit review authority. A finding-bearing batch carries one attached independent re-check call that can adjudicate its high-or-critical dismissals even at exhaustion.

### Reviewer allocation

Blind and informed briefs are distinct. A blind reviewer receives the frozen artefact and rubric without prior findings, repair claims, or change lists. An informed reviewer receives named finding identities, repair claims, affected regions, and prior evidence. Every option reserves blind closure evidence and uses informed seats for named repair verification. Different models or harnesses remain preferred where available. Genuine blindness and independence remain advisory properties that the tool cannot prove.

## Option A - Sealed phase budget

### Controller and bound

A non-resettable `TaskBudget` is declared in two irreversible steps. Task opening authorises plan review. Plan convergence freezes the rubric, `m` work-loop identities, one work slice per loop, and the acceptance slice. Each of the `m + 2` slices has five normal review batches and two already-declared reserve batches. A valid high or critical sets monotone `serious_seen` and unlocks that slice's reserve. Unlocking never restores spent authority.

Each review result updates explicit finding dispositions. A valid finding enters `Open`. A repair enters `ResolvedPendingVerification`. The next authorised informed verification either enters `Resolved`, leaves the finding open, or opens a fix-induced finding. A later unrelated clean batch cannot clear the finding. The final authorised batch cannot spawn an unverified repair.

Plan and work review retain the declared one-clean or two-clean requirement, reconstructed from triage-backed dispositions rather than raw outcome. Acceptance requires one settled pass after all earlier in-scope findings and Roadmap steps are settled. Foreclosure fires when fewer batches remain than the required clean streak. Completion wins if it occurs on the final batch.

The task bound is `7(m + 2)` review batches, `14(m + 2)` reviewer calls, at most `7(m + 2)` triage calls, at most `7(m + 2)` re-check calls, and at most `6(m + 2)` repair calls. A safe automated-agent upper bound is `34(m + 2)`. Resume reconstructs spend. No transition decrements, transfers, resets, or appends authority.

### Evidence and trade-off

On the Q-78 observation sequence, A reaches its terminal decision at pass seven with that pass carrying medium findings. It does not observe passes eight through ten, which contain three later valid shortfalls, all recorded low. A therefore preserves more bounded late discovery than C on this run, but no B comparison follows from finding arrays because B needs stable obligation identities.

A keeps current streak semantics and offers the most room for late repair among the fixed-depth candidates. Its cost is a larger account model and numeric five-plus-two values supported by one project rather than a calibrated optimum.

## Option B - Frozen obligations with sealed phase campaigns

### Closed source for `O`

`O` is exactly the finite set of canonical `[[obligation]]` rows frozen in the plan TOML. No prose scan, broad category union, reviewer inference, or generated Markdown contributes a row. Each row has a stable id, one phase owner, a body sidecar reference or structured statement, and one source label from this closed enum:

- `success_criterion`, for a criterion made canonical as an obligation row and projected into Success Criteria prose.
- `project_principle`, with an exact join to one numbered `[[principle]]` row.
- `documentation_impact`, with an exact join to one Roadmap step slug and its obligation body.

The row is the source of membership and cardinality. The label records why it exists. Validation enforces unique ids, finite rows, exact source joins, one owner, and a frozen digest. The first implementation does not infer obligations from unstructured invariants, trust-boundary prose, exclusions, or a reviewed baseline. A reviewer who finds a genuine uncited defect sends uncertainty to the human rather than silently backlogging it. This narrow source is the YAGNI boundary and the incompleteness risk remains explicit.

### One `FrozenObligationCampaign` controller

Plan review has the same sealed maximum of seven batches as A. Plan convergence freezes `O`, the finite post-freeze phase set `P`, and an exact owner for every obligation. `P` contains each declared work loop and acceptance, so `p = |P| = m + 1`.

Each phase `q` owns `O_q` and one non-transferable blind-closure seat. Its controller is `FrozenObligationCampaign(phase_id, scope_digest, obligations, closure, spend, terminal)`. Obligations are processed by stable id and have these transitions:

| State | Legal transition and result. |
| --- | --- |
| `Untested` | `InitialAttempt` consumes one review batch. A settled result enters `Closed(reopen_unused)`. A valid finding enters `OpenInitial(FindingId)`. A high-or-critical dismissal enters `AwaitingDismissalRecheck`. |
| `OpenInitial` | `RepairInitial` records the repair and enters `InitialRepairPendingVerification`. It consumes no review batch and is legal only because the phase has its declared verification seat. |
| `InitialRepairPendingVerification` | `VerifyInitial` consumes one informed batch. A named pass closes the finding and enters `Closed(reopen_unused)`. A failed verification or fix-induced valid finding exhausts that automatic attempt and enters `AwaitingTerminalDecision` or `SeriousBlocked`. |
| `Closed(reopen_unused)` | `MateriallyNewEvidence` consumes the one reopen-discovery batch and preserves the finding root. An upheld dismissal enters `Closed(reopen_used)`. A valid finding enters `OpenReopened(FindingId, EvidenceId)`. Relitigation without new evidence does not take this transition. |
| `OpenReopened` | `RepairReopened` records the repair and enters `ReopenRepairPendingVerification`. |
| `ReopenRepairPendingVerification` | `VerifyReopened` consumes one informed batch. A named pass enters `Closed(reopen_used)`. A failure or fix-induced finding enters `AwaitingTerminalDecision` or `SeriousBlocked`. |
| All obligations closed | `BlindClosure` consumes the phase's one blind batch. A settled result completes the phase. Any valid finding enters `AwaitingTerminalDecision` or `SeriousBlocked`. Blind closure never authors another automatic repair. |
| Any active state with a changed scope digest | `ScopeDigestChanged` terminally enters `Replanned`. Unresolved findings become `CarriedToSuccessor`, old `O_q` stays immutable, and a differently scoped successor requires a new human receipt, plan review, and freeze. |
| Declared authority exhausted | `AuthorityExhausted` enters `AwaitingTerminalDecision` or `SeriousBlocked`. No reviewer or implementer action follows. |
| Terminal decision | Accept below `F`, remove output, revert, replan, or abandon enters the durable disposition described in the shared package. There is no edge back to an active state. |

A re-check is attached to the batch that created `AwaitingDismissalRecheck` and consumes no review authority. An upheld dismissal applies the settled transition for that attempt. An overturned dismissal applies its valid-finding transition. The phase identity is immutable on every edge.

### Phase allocation, bound, and cost

For `n_q = |O_q|`, one obligation can consume at most four review batches: initial attempt, initial verification, one materially-new-evidence reopen discovery, and reopen verification. The phase also has one blind-closure batch. Its sealed allocation is therefore `C_q = 4n_q + 1`, including a minimum of one blind review when `n_q = 0`. Freeze rejects an owner outside `P`, a missing owner, a duplicate owner, or any allocation not equal to that formula. No phase can consume another phase's authority.

Summing over all post-freeze phases gives `4|O| + p`. Adding the seven-batch plan campaign gives the whole-family review bound:

```text
R_B = 7 + 4|O| + p
    = 4|O| + m + 8
```

This replaces the disproved `2|O| + 8` claim. Each review batch has exactly two reviewer calls, at most one triage call, and at most one re-check call. Plan review has at most six repairs. Post-freeze campaigns have at most two repairs per obligation. A safe whole-family automated-agent upper bound is therefore:

```text
4R_B + 6 + 2|O| = 18|O| + 4m + 38
```

The review and call bounds scale in both `|O|` and `m`. They cannot be ranked universally against C's `15(m + 2)` without parameter values.

### Legacy no-rubric state

An active legacy task already past plan review has no prospective `O`, no defined `C_q`, and no legal B work or acceptance campaign. It reconstructs as `LegacyNoRubric`, which is historical and exempt from B's obligation-completion predicate rather than falsely failed or falsely complete. It cannot mint review authority or treat old rounds as obligation transitions. The human may terminally finish that legacy task under its adopted pre-B rule, or author a receipt that sends it through a new prospective plan review and freeze before B starts. The next normal plan review creates `O`. Validation rejects any direct `LegacyNoRubric -> FrozenObligationCampaign` edge.

### Q-78 scope replay

`q86-q78-scope-replay.sh` runs B's scope-digest guard over all ten recorded passes without using outcome or severity arrays. The old records lack obligation ids, so their finding transitions are explicitly `historically_unreconstructible` and receive no B closure credit.

| Pass | B scope transition. | Durable result. |
| --- | --- | --- |
| 1 | `ScopeDigestMatched -> ReviewBatch`. | F1 remains active. Obligation result is not reconstructible. |
| 2 | `ScopeDigestChanged(Q-58/Q-82) -> Replanned`, then a human-authorised F2 freezes before the pass is admitted. | F1 is terminal and open findings are `CarriedToSuccessor`. |
| 3 | `ScopeDigestMatched -> ReviewBatch`. | F2 remains subject to prospective obligation state that history cannot reconstruct. |
| 4 | `ScopeDigestChanged(Q-83) -> Replanned`, then F3 freezes before admission. | F2 is terminal and open findings are carried. |
| 5 | `ScopeDigestMatched -> ReviewBatch`. | F3 remains active subject to unreconstructible obligation state. |
| 6 | `ScopeDigestMatched -> ReviewBatch`. | F3 remains active subject to unreconstructible obligation state. |
| 7 | `ScopeDigestChanged(Q-85/Q-86) -> Replanned`, then F4 freezes before admission. | F3 is terminal and open findings are carried. |
| 8 | `ScopeDigestChanged(Q-87) -> Replanned`, then F5 freezes before admission. | F4 is terminal and open findings are carried. |
| 9 | `ScopeDigestMatched -> ReviewBatch`. | F5 remains active subject to unreconstructible obligation state. |
| 10 | `ScopeDigestMatched -> ReviewBatch`. | F5 receives the historical observation, but prior obligation closure still cannot be inferred. |

The counterfactual cost is four terminal replans, five task families, four additional human receipts, and four additional plan-review and freeze campaigns before all ten reviewer passes could occur. If the human refused any successor, delivery would stop at that scope addition. This is B's largest measured cost. It is also the exact mechanism by which B prevents a moving acceptance target from laundering authority.

### Evidence and trade-off

B defines done without raw outcome or severity trajectories and makes a moving scope explicit. It has the strongest structured completion model and a proved per-family bound. It also has the largest authoring and adoption burden, a real obligation-completeness risk, and the Q-78 replay's four forced replans. Its derived bound is not necessarily smaller than A or C.

## Option C - Fixed-depth verification protocol

### Controller and bound

Each plan review, work loop, and acceptance campaign has forward-only `Discovery`, `Verify1`, `Verify2`, and `BlindClosure` review nodes plus explicit `Repair1` and `Repair2` actions. `Discovery` uses two blind seats. A valid finding enters `Open`, `Repair1` enters `ResolvedPendingVerification`, and `Verify1` can clear that finding only through a named pass. A valid finding at `Verify1` may use `Repair2` and `Verify2`. A valid finding at `Verify2` or blind closure is terminal. A risky settled path always reaches blind closure. No node can be revisited.

The finding identity and severity remain in state across repair and verification. A later clean observation outside the named verification cannot clear a critical. A dismissed high or critical follows the attached re-check path. Terminal non-delivery dispositions are explicit.

For each of `m + 2` phases, C has at most four review batches, five reviewer calls, four triage calls, four re-check calls, and two repair calls. The task bound is `4(m + 2)` batches and a safe `15(m + 2)` automated-agent calls. Resume reconstructs the current node. No transition points backwards.

### Evidence and trade-off

On Q-78, C reaches `SeriousBlocked` at pass three because `Verify2` carries a high. It therefore does not observe passes four through ten, which contain 23 later valid shortfalls and further highs. C has the lowest fixed per-phase review depth and the smallest graph. It does not have a universally lowest whole-task call bound because B scales in different parameters. Its main cost is terminal rejection of useful late repairs.

## Project Principle comparison

| Project Principle | Option A. | Option B. | Option C. |
| --- | --- | --- | --- |
| Prefer the cleaner long-term architecture over the smallest diff | Unifies task spend but layers a ceiling over streaks. | Unifies scope, disposition, phase ownership, and bound in one controller. | Has the smallest graph but replaces present streak semantics. |
| Minimal by default | Fixed slices and two seats avoid dynamic policy. | Adds canonical obligation rows and the largest schema. | Four nodes and two repairs are compact. |
| Safe on existing projects | Digest adoption can charge old spend and fail loudly. | `LegacyNoRubric` avoids invented history, but adoption requires a new freeze before B starts. | Historical stage adoption is ambiguous and must fail to a human. |
| Idempotent | Ordered replay preserves monotone spend. | Obligation state, phase identity, and spend reconstruct without reset. | Every node is single-use. |
| Make illegal states unrepresentable | Explicit findings and terminal variants remove scalar erasure and reset. | Closed obligation variants prevent unverified closure, second reopen, phase transfer, and post-terminal action. | Forward-only stages prevent a third repair and closure bypass. |
| Ground decisions in evidence | Preserves the measured five-round boundary, but reserve values are weakly calibrated. | Targets the observed scope movement, while the replay exposes four forced replans. | Blind and informed stages fit anchoring evidence, but Q-78 shows early loss. |
| Reproducible | Fixed arithmetic and exhaustive controller. | Bound derives from finite `O`, exact phase owners, and exhaustive controller. | Fixed graph and exhaustive controller. |
| Structured data first, project for humans | Identities, spend, findings, and receipts are structured. | Obligation rows, attempts, findings, ownership, and receipts are structured. | Stage, brief, finding, and terminal state are structured. |

## Corrected proof and red controls

The durable proof is `docs/plans/workflow-calibration.explorations/q86-controller-proof.py`. It enumerates the actual A, B, and C controllers rather than observation-only proxies. It retains explicit open, repaired, pending-recheck, closed, terminal, and non-delivery states. Its checks are:

- Every reachable graph is acyclic.
- Review spend never exceeds the stated bound.
- No delivery terminal carries an open critical or pending re-check.
- A valid critical can leave the open set only on a named verification after repair or a terminal non-delivery transition.
- Re-check-upheld is the only separate dismissal path.

Run:

```sh
CHECKER=docs/plans/workflow-calibration.explorations/q86-controller-proof.py
nix shell nixpkgs#python3 -c python3 "$CHECKER" --mode all --phase acceptance --risk risky --obligations 2 --floor high
nix shell nixpkgs#python3 -c python3 "$CHECKER" --mode all --phase acceptance --risk risky --obligations 2 --floor critical
for n in 0 1 2 3
do
    nix shell nixpkgs#python3 -c python3 "$CHECKER" --mode B --phase work:example --obligations "$n" --floor high
done
sha256sum "$CHECKER"
```

The first two commands return:

```text
A phase=acceptance risk=risky floor=high normal=5 reserve=2 required=1 states=104 edges=220 terminal=43 acyclic=true max_reviews=7 bad_delivery=0 bad_critical_clear=0 bad_bound=0
B phase=acceptance obligations=2 floor=high bound=9 states=1680 edges=3785 terminal=892 acyclic=true max_reviews=9 bad_delivery=0 bad_critical_clear=0 bad_bound=0
C phase=acceptance risk=risky floor=high stages=4 repairs=2 states=79 edges=135 terminal=42 acyclic=true max_reviews=4 bad_delivery=0 bad_critical_clear=0 bad_bound=0
A phase=acceptance risk=risky floor=critical normal=5 reserve=2 required=1 states=105 edges=221 terminal=44 acyclic=true max_reviews=7 bad_delivery=0 bad_critical_clear=0 bad_bound=0
B phase=acceptance obligations=2 floor=critical bound=9 states=1744 edges=3963 terminal=938 acyclic=true max_reviews=9 bad_delivery=0 bad_critical_clear=0 bad_bound=0
C phase=acceptance risk=risky floor=critical stages=4 repairs=2 states=82 edges=138 terminal=45 acyclic=true max_reviews=4 bad_delivery=0 bad_critical_clear=0 bad_bound=0
```

The B parameter sweep returns bounds `1`, `5`, `9`, and `13` for zero through three obligations. Every run is acyclic, reaches its bound, and reports zero bad delivery, critical-clear, and bound states. The checker SHA-256 is `db2874d8654957582f18592ece030f344b60ca9657c127715fcc78d6987ef9a7`.

The required paths resolve as follows:

| Path | A. | B. | C. |
| --- | --- | --- | --- |
| Repeated human resume | Resume reconstructs spend. Every phase ends by batch seven. | Resume reconstructs phase and obligation state. Every phase ends by `4n_q + 1`. | Resume reconstructs one forward-only node. Every phase ends by batch four. |
| Unbounded acceptance repair | The final finding routes to a terminal decision by batch seven. | Each obligation has at most initial repair and one reopened repair. Blind-closure findings are terminal. | A finding at `Verify2` or closure is terminal. |
| Fix-induced high near exhaustion | It consumes an authorised verification batch and unlocks only unspent reserve. | It uses the current attempt's finding transition and cannot create another attempt. | It uses the next fixed repair only before `Verify2`. |
| Scope-expanded low | It is backlogged, consumes its opened batch, and cannot enlarge frozen scope. | It cannot add an obligation. A changed scope digest terminally replans the family. | It is settled for stage movement and cannot add a node. |
| Relitigation without new evidence | It preserves disposition and cannot reset spend. | It cannot take `MateriallyNewEvidence` or consume a reopen. | It preserves disposition and cannot point backwards. |
| Narrowing or replan | The family becomes terminal and no slice returns. | The family becomes terminal, with findings carried and `O` immutable. | The family becomes terminal and no stage returns. |
| Unresolved critical at exhaustion | Delivery and residual acceptance are unconstructible. | Delivery and residual acceptance are unconstructible. | Delivery and residual acceptance are unconstructible. |
| Blind closure | Every batch has a blind seat. | Each phase has one non-transferable blind-closure seat. | `BlindClosure` is a required node on risky and repaired paths. |

## Migration and enforcement

All options move the same core surfaces. `.agents/workflow.toml`, `pack/workflow.toml`, and `WorkflowSpec` gain the chosen controller constants. The shared `ReviewProcess` reconstruction gains task-family, phase, finding, scope, terminal, and acceptance-campaign state while preserving disjoint `Convergence` and `SinglePass` observations. The plan schema and pack plan template gain immutable identities, freeze/adoption data, and terminal receipts. Metrics gain prospective scope, finding, evidence, disposition, review-brief, spend or stage, and terminal events. Historical events remain append-only.

`validate --workflow` enforces exact ids, phase identity, monotone authority, repair-before-verification, finding dispositions, dismissal re-checks, no action after terminal state, and no delivery with an unresolved critical. `next` reports only the actor and brief allowed by reconstructed state. It does not manufacture a finding, verdict, human decision, or proof of an external review.

B additionally moves canonical obligation rows and exact phase ownership into the plan source, validates `C_q = 4|O_q| + 1`, and implements `LegacyNoRubric`. A adds fixed accounts and reserve eligibility. C adds forward-only stage events and adoption state.

Canonical guidance and generated copies must move together through `pack/AGENTS.md`, `pack/instrument.md`, planner, orchestrator, reviewer, triager, and implementer prompts, ledger and plan templates, `AGENTS.md`, `.agents/AGENTS.reference.md`, `.agents/prompts/`, `.agents/LEDGER.template.md`, `.agents/workflow.toml`, README, and changelog. The chosen work must land after the shared typed review reconstruction. Reviewer diversity, the quality of a lineage judgement, and actual blindness remain advisory. Identity, authority, disposition, phase, terminality, and critical legality are mechanical.

## Excluded candidates

- The current mechanism is excluded because repeated resume and later acceptance repair each contain a reachable cycle.
- A severity-decay gate is excluded because its multi-pass trajectory needs trustworthy prospective sequence data that does not exist. This differs from the per-finding prospective severity used by the serious floor.
- A probabilistic or survival-threshold gate is excluded because the sample and lineage data cannot support a safe stopping probability.
- A pure frozen-obligation rule without sealed phase campaigns is excluded because malformed or stalled progress could otherwise recreate an unbounded path.

## Recommendation

Choose `B - Frozen obligations with sealed phase campaigns`, with medium to low confidence.

B is the cleaner long-term architecture under Prefer the cleaner long-term architecture over the smallest diff, Make illegal states unrepresentable, and Structured data first, project for humans. Its corrected controller gives each obligation and phase one typed source, derives a finite bound without trusting broken outcome arrays, and makes scope movement terminal rather than invisible. The exhaustive proof now checks that controller rather than the old four-unit proxy.

The recommendation is not high confidence under Minimal by default, Safe on existing projects, and Ground decisions in evidence. The Q-78 replay shows that B would have forced four terminal replans and four additional plan-review campaigns. A finite obligation set can also omit a genuine defect. A focused schema and reconstruction proof of concept must therefore show that the closed obligation rows remain precise and non-duplicative. If that proof fails, the human decision reopens with A as the recommendation. No fallback architecture is pre-authorised and a new receipt is required.

Evidence that would overturn B includes obligation sets that routinely omit genuine in-scope defects, frozen-scope tasks that still require long repair sequences, a serious finding routed to backlog, or prospective evidence that A preserves materially more unique serious findings for acceptable cost. Evidence that changes only a constant includes prospective distributions of initial verification failures and materially-new-evidence reopens.

## YAGNI boundary

- Do not build a general issue tracker, project-wide defect database, mutable rubric editor, or autonomous obligation extractor.
- Do not build an autonomous risk, scope, severity, or residual-risk judge.
- Do not build probabilistic stopping, dynamic pricing, transferable credits, a reviewer marketplace, or a model optimiser.
- Do not infer historical finding lineage, obligation membership, stage, or closure.
- Do not build a persistent workflow service, general workflow language, or new scheduler beyond the planned typed fleet.
- Do not create automatic authority from rename, rebuild, replan, narrowing, scope change, or human resume.
- Do not implement a mechanism or floor until the human decides and the planner records the receipt and fold.

## Exact human decision and no-decision boundary

The orchestrator must ask which architecture Q-86 should fold into `workflow-calibration`: A, B, or C. It must also ask whether the serious terminal floor is `high` or `critical`, or record that the floor is deferred to a separate pre-implementation decision.

The presentation must state A's pass-seven Q-78 terminal and three undiscovered low shortfalls, B's four forced scope replans and corrected `4|O| + m + 8` bound, C's pass-three terminal and 23 undiscovered shortfalls including highs, the different bound parameters, the B proof-of-concept gate, and the recommendation above.

Until the human chooses, Q-86 remains `open` and implementation is blocked. The choice does not author code. A later planner fold must sequence the chosen mechanism after the shared typed review reconstruction, include instrumentation and documentation migrations, and record the decision receipt. The baseline, severity gate, A's five-plus-two values, B's one reopen, the serious floor, and any implementation are not silently approved by Q-85 or this synthesis.
