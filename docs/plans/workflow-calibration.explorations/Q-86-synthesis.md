# Q-86 synthesis: bounded convergence options

## Status and decision boundary

Q-86 is `open` for a human decision. This synthesis reconciles the corrected proofs in `Q-86-state-machine.md` and `Q-86-safety-process.md`. It changes no workflow rule, cap, reset behaviour, metric, specification, pack file, prompt, template, README, changelog, or Rust source. It changes generated-plan content only through the separately required projection of the Q-86 planning sources.

The human decision is between three bounded architectures:

- `A - Sealed phase budget`.
- `B - Frozen obligations with sealed phase campaigns`.
- `C - Fixed-depth verification protocol`.

The source labels map as follows. Option A is the state-machine proposal's Candidate A and the safety proposal's M1. Option B is the safety proposal's corrected M2 plus the state-machine proposal's sealed authority envelope. Option C is the state-machine proposal's Candidate B. The safety proposal's M3 remains excluded.

The recommendation remains `B - Frozen obligations with sealed phase campaigns`, at medium to low confidence. The corrected proof establishes its controller and finite per-family bound. The conditional Q-78 replay also exposes its substantial cost if the four observed named folds are treated as material obligation-digest changes. No mechanism, serious terminal floor, or controller constant has been chosen. Q-85 authorised only this design pass. Implementation remains blocked until the human decides Q-86 and the decision is receipted and folded into `workflow-calibration`.

## Evidence that constrains the decision

### Corrected Q-78 acceptance history

Run:

```sh
jq -s 'map(select(.type == "round" and .task == "q78-design-pass" and .phase == "acceptance")) | {passes: length, valid_shortfalls: map(.valid_findings)}' docs/metrics/workflow.jsonl
```

It returns ten passes and `[7,10,5,6,5,5,4,2,1,0]`. The run closed at pass ten. It demonstrates high review cost, late serious findings, four observed named folds, and eventual closure. It does not demonstrate divergence.

The baseline remains non-admissible because its rules have reachable unbounded paths. For every positive integer `n`, five `new_valid` rounds followed by human `resume` can repeat `n` times and leave the loop active after `5n` rounds. For every positive integer `n`, an acceptance pass with a valid shortfall can route through repair to another acceptance pass and leave the campaign active after `n` passes. Convergence-first precedence closes neither construction. The baseline has no finite bound or exact forced terminal event and cannot be chosen.

### Evidence limitations

- Nineteen logged rounds have `outcome: "clean"` while `valid_findings` is greater than zero, and all nineteen advance `consecutive_clean`. Raw outcome and streak fields are not safe completion inputs.
- Only six of the ten Q-78 triage files remain. The severity tail in passes seven to ten depends on append-only summary records and is not used to establish any controller invariant.
- Historical findings have no stable cross-review identity. The Q-78 history cannot reconstruct which prospective B obligation a finding would have joined, whether a verification closed its parent, or whether a later report was pre-existing, fix-induced, duplicate, relitigated, or materially new evidence.
- The four named Q-78 folds are observed in artefact descriptions. Their mapping to four counterfactual B obligation-digest changes is an explicit assumption because no historical obligation rows or digests exist. The four-replan cost is conditional on that assumption, not a reconstructed historical fact.
- The log contains one critical-bearing round and one dismissal re-check. That re-check was overturned. Critical legality and re-check behaviour are safety requirements with sparse empirical support, not calibrated rates.
- Q-78's two reviewer paths confound blindness, model, harness, lens, and brief. The local and external evidence supports separate blind discovery and informed verification briefs, not a causal yield estimate.
- `validate --workflow` can validate structured claims but cannot prove that an external agent performed an independent or genuinely blind review.
- The association between Q-78's named folds and later findings is not evidence that the folds caused the findings.

The controllers do not use the broken outcome or severity arrays. They consume prospective triage-backed stable finding maps, dispositions, and per-finding severity. The historical arrays appear only in descriptive replay evidence.

## Shared safety package

### Stable finding maps and joint batch semantics

Every controller carries a finite `FindingMap` keyed by immutable `FindingId`. Each value records owner, severity, disposition, origin, typed `ScopeRelation`, and an optional parent id. `ScopeRelation` is either `InScope(ScopeId)` or `ScopeExpanded(ScopeDeltaId)`. The severity alphabet is the full project scale `low`, `medium`, `high`, and `critical`. Origin distinguishes `pre_existing`, `fix_induced`, `reopened`, and `origin_indeterminate`. A fix-induced child keeps a pointer to its parent while both identities remain in the map.

One triaged review batch is an atomic `ReviewBatch(primary_owner, findings_by_owner, unowned_findings)`. Every entry carries its triage disposition, so the same batch may contain a triage-valid finding and a dismissed high or critical report. `findings_by_owner` is a finite map from each affected obligation owner to that owner's finite finding map, and `unowned_findings` is a finite set. Duplicate reviewer reports join one stable id. A review batch costs one review unit regardless of finding count. Triage adjudicates the whole batch, and the reducer updates every affected obligation and the complete finding map in one transition. The primary owner is the scheduled rubric target. An absent finding settles only that primary target, not every obligation absent from the map. A batch can therefore satisfy several finding-bearing initial attempts, but it cannot claim several clean initial attempts.

A mixed-disposition reduction retains both components as `Open` and `AwaitingDismissalRecheck`. The attached independent re-check runs before a new repair and does not debit review authority. If it upholds dismissal, that component becomes `Dismissed` while the valid component remains `Open`. If it overturns dismissal, the stable dismissed-report id joins the existing `Open` repair set. At authority exhaustion both continuations retain the repair component and route it to the correct terminal state rather than dropping either component. One joint repair action moves every `Open` finding selected for one owner attempt to `PendingVerification`. Its named joint verification must cover that complete selected set. It either resolves every selected finding, fails the complete set conservatively back to `Open`, or fails the parents while adding one or more `FixInduced` children. A partial real-world verification is represented by the conservative failure branch unless every selected finding has named successful evidence. This makes the review and repair bounds independent of batch cardinality.

Completion and every delivering terminal quantify over the complete map. Ordinary completion requires every in-scope finding to be `Resolved`, validly `Dismissed`, backlogged only where the scope rule permits it, or removed from the delivered artefact. Residual delivery changes every permitted outstanding below-floor finding to `AcceptedResidual`. It is illegal if any finding is still `Open`, `PendingVerification`, or `AwaitingDismissalRecheck` after the terminal disposition is applied. No reducer selects only the latest or most severe finding.

A valid critical therefore follows `Open -> PendingVerification -> Resolved`, or reaches a terminal non-delivery disposition. A dismissed critical follows `AwaitingDismissalRecheck -> Dismissed` only after an independent upheld re-check. A counter, unrelated clean observation, child finding, scope label, or human resume never removes the parent identity or clears it.

### Finite exhaustive model and arbitrary finite batches

The durable checker exhausts every severity multiset whose complete live map has cardinality at most two. This includes all four singleton severities, all ten two-finding severity multisets, the required simultaneous low-plus-critical case under one owner and under two different owners, mixed owned and unowned batches, multiple findings at blind closure, a parent plus fix-induced child that remain outstanding together, and every valid-severity by serious-dismissal product. B covers same-owner, cross-owner, owned-plus-unowned, and blind-closure disposition products. The finite cardinality is deliberately two because that is the smallest interaction model that can expose scalar erasure, cross-owner state mismatch, mixed-floor mistakes, mixed triage disposition loss, and parent-child replacement.

The proof composes to every arbitrary finite batch over the product of obligation state, finding state, triage disposition, and scope relation. The atomic batch reducer unions fresh stable ids, updates every affected obligation, and preserves the bidirectional owner invariant: every owned outstanding finding has a matching non-closed obligation state of the same disposition kind, and every open, pending-verification, dismissal-recheck, or scope-recheck obligation state has a matching outstanding owned finding. Every safety or delivery predicate is a universal conjunction over ids and obligations. Joint repair and verification take the complete finite selected key set for one owner attempt as one typed argument. Attached dismissal and scope re-checks preserve the whole map and consume no review authority. Adding another finite owner or disposition component neither removes nor rewrites an existing component, cannot close an unaffected obligation, does not increase phase spend, and can only make the universal delivery predicate harder to satisfy. By induction on finite owner-map cardinality and then each finite finding and disposition submap, the lifecycle, owner-product, and universal terminal invariants hold for any finite union. The cardinality-two sweep checks the non-pointwise interactions, namely two owners with low plus critical, valid plus dismissed-serious reports, a mixed owned and unowned batch, and a parent-child relation. The phase bounds remain cardinality-independent because one atomic batch can consume one attempt for each owner it affects but is charged once, while each affected owner still has at most its existing verification and reopen transitions.

### Identity, scope, and successor families

Authority belongs to an immutable `TaskFamilyId`, typed phase and loop identities, and ordered review-batch identities. Rename, rebuild, a new display name, human resume, or an unchanged replan cannot create fresh authority.

The acceptance rubric freezes after plan review and before implementation. A finding is in scope when it demonstrates a violation of a frozen obligation, invariant, boundary, or duty. The typed scope relation and `AwaitingScopeRecheck` are part of every A, B, and C phase state and transition relation, rather than a detached policy lookup. Their transitions consume the review batch that found the report, preserve stable identity and evidence through re-check, debit no authority for the re-check itself, and remain subject to each controller's spend and delivery predicates. The selected scope-expansion policy is severity-sensitive. A genuinely optional `low` capability or preference becomes `Backlogged`. A `medium` scope expansion goes directly to the terminal human scope decision. A proposed `high` or `critical` out-of-scope ruling first enters `AwaitingScopeRecheck`. If the re-check overturns a high ruling, the finding returns to the in-scope controller. If it upholds the high ruling, the finding still goes to the terminal human scope decision rather than backlog. A critical is always safety-blocking, so either critical re-check outcome enters `SeriousBlocked` and cannot backlog or deliver. Uncertainty stays in scope or goes to the human. A triager, never the orchestrator, rules on scope. This deliberately selects the state-machine proposal's stricter policy over all-severity automatic backlog because it limits abuse of the scope firewall under Safe on existing projects and Make illegal states unrepresentable.

Option B narrows the routine owned path to its canonical obligation ids. If the common scope rule identifies a genuine in-scope finding that no B obligation owns, the controller creates `UnownedInScopeFinding(FindingId)` and terminally routes the phase to the human. It cannot satisfy all-obligations-closed, become backlog automatically, or disappear at blind closure. An unowned critical enters `SeriousBlocked` and cannot reach completion or residual delivery.

The selected successor rule for B is materially different structured scope, not the safety proposal's stricter proper-subset-or-disjoint alternative. The stricter rule remains an unselected proposal alternative and no narrowing-chain bound is claimed for selected B. A successor requires all of the following:

- The predecessor family is terminal and immutable and carries its ordered ancestry registry.
- The successor id is fresh against the predecessor id and every recorded ancestor id. Its ancestry is exactly the predecessor ancestry followed by the predecessor id, so same-family reuse and ancestor reuse are illegal.
- A human decision receipt binds the exact predecessor and successor ids, both ancestry snapshots, both canonical obligation and exclusion digests, all presented options, and the chosen successor.
- A structured scope delta shows that the obligation or exclusion set differs from the predecessor, and the receipt records the human judgement that the difference is material.
- The receipt and successor both bind the predecessor's monotone review spend and the complete carried finding map. Every unresolved predecessor finding remains `CarriedToSuccessor` with stable identity and evidence.
- The successor names `new_human_receipt` as the origin of its own authority. It cannot relabel predecessor spend as unspent authority.

Scope additions are therefore permitted, as required by the conditional Q-78 scenario, but they are new receipted families rather than reset edges. There is no finite claim across a human's sequence of materially different projects. The finite proof and cost bound apply to each immutable family. Validation must reject the same or reordered scope, same-family reuse, reuse of any ancestor id, malformed or mismatched ancestry, a missing receipt or option set, a wrong family or digest, a missing carried finding, predecessor mutation, a mismatched predecessor-spend snapshot, and any attempt to copy spent predecessor authority as fresh authority.

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
- `Replan` ends the family, preserves unresolved findings as `CarriedToSuccessor`, and keeps delivery blocked. A successor needs the receipt and structured material scope delta above.
- `Abandon` ends the family, ships nothing, and preserves each unresolved finding and its evidence.

Backstop re-checks do not debit review authority. A finding-bearing batch carries one attached independent re-check call that can adjudicate all its high-or-critical dismissals even at exhaustion.

### Reviewer allocation

Blind and informed briefs are distinct. A blind reviewer receives the frozen artefact and rubric without prior findings, repair claims, or change lists. An informed reviewer receives named finding identities, the complete joint repair claim, affected regions, and prior evidence. Every option reserves blind closure evidence and uses informed seats for named joint repair verification. Different models or harnesses remain preferred where available. Genuine blindness and independence remain advisory properties that the tool cannot prove.

## Option A - Sealed phase budget

### Controller, reserve rule, and bounds

A non-resettable `TaskBudget` is declared in two irreversible steps. Task opening authorises plan review. Plan convergence freezes the rubric, `m` work-loop identities, one work slice per loop, and the acceptance slice. Each of the `m + 2` slices has five normal review batches and two already-declared reserve batches.

Only a triage-valid high or critical, or a serious dismissal that the independent re-check overturns, sets monotone `serious_seen` and unlocks that slice's reserve. Merely referring a high or critical dismissal does not unlock reserve. An upheld dismissal preserves the prior value and the clean streak that entered re-check. The upheld result advances that incoming streak because the triaged batch is clean after its required re-check. An overturned dismissal returns through the valid-finding path, resets the streak to zero, and unlocks reserve only when its established severity is high or critical. Unlocking never restores spent authority.

Each result updates the complete finding map under the shared joint semantics. The final authorised batch cannot spawn an unverified repair. Plan and work review retain the declared one-clean or two-clean requirement, reconstructed from the complete triage-backed map rather than raw outcome. Acceptance requires one settled pass after all earlier in-scope findings and Roadmap steps are settled. A single remaining-clean-suffix calculation runs before every automatic review, repair, and verification. If the remaining authorised verification path is shorter than the clean suffix still required, the slice forecloses before emitting that action. Completion still wins if it occurs on the final attainable batch.

The task maximum is `7(m + 2)` review batches, `14(m + 2)` reviewer calls, at most `7(m + 2)` triage calls, at most `7(m + 2)` re-check calls, and at most `6(m + 2)` grouped repair calls. A safe automated-agent upper bound remains `34(m + 2)`. Joint maps do not increase it.

A's minimum is one batch for acceptance. For plan and work review it is the required clean streak `r_plan` or `r_work_q`, which is one batch at low risk and two consecutive batches at risky. Its whole-family minimum is `r_plan + sum(r_work_q) + 1` review batches and twice that many reviewer calls. It does not scale with finding or obligation cardinality.

### Evidence and trade-off

On the Q-78 observation sequence, A reaches its terminal decision at pass seven with that pass carrying medium findings. It does not observe passes eight through ten, which contain three later valid shortfalls, all recorded low. A therefore preserves more bounded late discovery than C on this run. Its cost is a larger account model and numeric five-plus-two values supported by one project rather than a calibrated optimum.

## Option B - Frozen obligations with sealed phase campaigns

### Closed source for `O` and unowned findings

`O` is exactly the finite set of canonical `[[obligation]]` rows frozen in the plan TOML. No prose scan, broad category union, reviewer inference, or generated Markdown contributes a row. Each row has a stable id, one phase owner, a body sidecar reference or structured statement, and one source label from this closed enum:

- `success_criterion`, for a criterion made canonical as an obligation row and projected into Success Criteria prose.
- `project_principle`, with an exact join to one numbered `[[principle]]` row.
- `documentation_impact`, with an exact join to one Roadmap step slug and its obligation body.

The row is the source of membership and cardinality. The label records why it exists. Validation enforces unique ids, finite rows, exact source joins, one owner, and a frozen digest. The first implementation does not infer obligations from unstructured invariants, trust-boundary prose, exclusions, or a reviewed baseline. The `UnownedInScopeFinding` path is the fail-closed bridge from the common in-scope rule to this narrow source.

### One `FrozenObligationCampaign` controller

B's plan review reuses A's sealed phase controller unchanged. Its inherited and still unapproved constants are five normal batches, two reserve batches, at most six grouped repairs, and reserve unlock only after a triage-valid high or critical or an overturned serious dismissal. Plan risk is the once-declared plan-artifact risk class. Its clean requirement `r_plan` is one batch for low risk and two consecutive batches for risky plan review. Completion requires that clean suffix and the complete map settled. The same remaining-suffix foreclosure prevents an unverified repair or review whose remaining path cannot complete. The plan maximum is seven batches. Plan convergence then freezes `O`, the finite post-freeze phase set `P`, and an exact owner for every obligation. `P` contains each declared work loop and acceptance, so `p = |P| = m + 1`.

Each phase `q` owns `O_q` and one non-transferable blind-closure seat. Its controller is `FrozenObligationCampaign(phase_id, scope_digest, obligations, findings, closure, spend, terminal)`. The complete stable finding map is part of this one controller.

| Obligation state | Legal transition and result. |
| --- | --- |
| `Untested` | `InitialAttempt` consumes one review batch and atomically reduces `findings_by_owner` plus `unowned_findings`. The primary owner enters `Closed(reopen_unused)` only when its result is settled. Every `Untested` owner named by a valid finding enters `OpenInitial`, so one cross-owner batch can satisfy several finding-bearing initial attempts. A serious dismissal enters `AwaitingDismissalRecheck`. An upheld incidental dismissal against a non-primary untested owner retains that owner as `Untested`, while an overturned dismissal establishes valid initial work and enters `OpenInitial`. An unowned in-scope finding terminally routes to the human. |
| `OpenInitial` | `RepairInitialJoint` records one repair over the complete owned open set and enters `InitialRepairPendingVerification`. It consumes no review batch and is legal only because the phase has its declared verification seat. |
| `InitialRepairPendingVerification` | `VerifyInitialJoint` consumes one informed batch. Named success for the complete set enters `Closed(reopen_unused)`. A failed parent set, fix-induced child, or overturned new dismissal exhausts that automatic attempt and enters `AwaitingTerminalDecision` or `SeriousBlocked`. |
| `Closed(reopen_unused)` | After every obligation has received its initial attempt, `MateriallyNewEvidence` may consume the one optional reopen-discovery batch. It reopens stable roots where available. A valid result enters `OpenReopened`. Relitigation without new evidence cannot take this transition. |
| `OpenReopened` | `RepairReopenedJoint` records one repair over the complete reopened set and enters `ReopenRepairPendingVerification`. |
| `ReopenRepairPendingVerification` | `VerifyReopenedJoint` consumes one informed batch. Named success for the complete set enters `Closed(reopen_used)`. Failure or a fix-induced child is terminal. |
| All obligations closed | `BlindClosure` consumes the phase's one blind batch. A settled result completes the phase. Any valid owned or unowned finding enters `AwaitingTerminalDecision` or `SeriousBlocked`. Blind closure never authors another automatic repair. |
| Any active state with a changed scope digest | `ScopeDigestChanged` terminally enters `Replanned`. Unresolved findings become `CarriedToSuccessor`, old `O_q` stays immutable, and the selected successor rule requires a receipt and structured material scope delta. |
| Declared authority exhausted | `AuthorityExhausted` enters `AwaitingTerminalDecision` or `SeriousBlocked`. No reviewer or implementer action follows. |

Initial attempts have priority over optional reopen discovery. A valid incidental report against `Closed(reopen_unused)` while another obligation is still `Untested` enters `DeferredReopen(FindingMap)`. Its stable identity remains in the map, but it cannot become `OpenReopened`, `ReopenRepairPendingVerification`, or `Closed(reopen_used)` until no obligation remains `Untested`. An incidental serious dismissal may take its attached re-check immediately because that re-check debits no authority. An upheld dismissal returns the owner to `Closed(reopen_unused)`. An overturned dismissal retains the report in `DeferredReopen`. The controller then activates deferred reopen work without another discovery batch only after every initial attempt has finished. The priority oracle is a state predicate that rejects any active state containing both `Untested` and generation-one work. It does not infer priority from action names. `AcceptResidual` is not constructible while any obligation remains `Untested`. The proof's `bad_unverified_delivery` check applies to the complete finding map and to this obligation condition.

### Phase allocation, maximum, minimum, and calls

For `n_q = |O_q|`, one obligation can consume at most four review batches: initial attempt, initial verification, one materially-new-evidence reopen discovery, and reopen verification. The phase also has one blind-closure batch. Its sealed maximum is therefore `C_q = 4n_q + 1`, including a minimum of one blind review when `n_q = 0`. Freeze rejects an owner outside `P`, a missing owner, a duplicate owner, or any allocation not equal to that formula. No phase can consume another phase's authority.

A clean B phase still costs at least `n_q + 1` review batches, one clean primary initial attempt per obligation plus blind closure. A cross-owner finding batch may satisfy several initial attempts, but that is not the all-settled clean path and cannot claim clean evidence for an absent non-primary owner. If `r_plan` is the inherited A-controller plan-review minimum, one for low-risk plan review and two for risky plan review, the whole-family minimum is:

```text
L_B = r_plan + |O| + p
    = r_plan + |O| + m + 1
```

With two reviewer calls per batch, the clean whole-family reviewer-call minimum is `2L_B`. Unlike A and C, B's ordinary minimum scales with `|O|`. `|O|` is the future frozen-row count and cannot be estimated by counting current prose bullets.

Summing the post-freeze maxima and adding the seven-batch plan campaign gives:

```text
R_B = 7 + 4|O| + p
    = 4|O| + m + 8
```

Each review batch has exactly two reviewer calls, at most one triage call, and at most one re-check call. Plan review has at most six grouped repairs. Post-freeze campaigns have at most two grouped repairs per obligation. A safe whole-family automated-agent upper bound remains:

```text
4R_B + 6 + 2|O| = 18|O| + 4m + 38
```

The multi-finding repair semantics do not change these bounds because one repair call covers the complete finite finding set for one obligation attempt. If a joint repair or verification cannot cover that set, the attempt fails terminally rather than minting another call.

### `LegacyNoRubric`

An active legacy task already past plan review has no prospective `O`, no defined `C_q`, and no legal B work or acceptance campaign. It reconstructs as the explicit `LegacyNoRubric` variant. Its only legal paths are a human terminal that preserves its pinned legacy disposition, or a receipted transition into a new prospective plan review and freeze. Only the latter may then enter a B campaign.

The controller rejects direct `LegacyNoRubric -> FrozenObligationCampaign`, historical-round closure credit, and reinterpretation as a prospective zero-obligation campaign. A legitimate new prospective task may still freeze an actual zero-obligation phase and receive its one blind-closure batch. That state is distinct from legacy adoption.

### Conditional Q-78 scope replay

The durable replay reads only task, phase, and artefact descriptions. It observes the named Q-58/Q-82, Q-83, Q-85/Q-86, and Q-87 fold identities. It counts the first observation of each stable identity and treats a later mention of the same identity as context rather than another fold. It does not reconstruct prospective obligation rows or digests. Its mapping of each distinct named fold to a material B scope-digest change, and each other pass to an unchanged digest, is an explicit counterfactual assumption.

Under those four assumptions, passes 2, 4, 7, and 8 terminally replan and successors F2 through F5 require receipts, structured scope deltas, plan review, and freeze. The conditional cost is four terminal replans, five families, four additional human receipts, and four additional plan-review and freeze campaigns. If any fold would not have changed the canonical obligation or exclusion set, its associated replan and cost must be removed. If the human refused any successor, delivery would stop at that fold. Historical obligation outcomes remain unreconstructible and receive no B closure credit.

### Evidence and trade-off

B defines done without raw outcome or severity trajectories and makes prospective scope movement explicit. It has the strongest structured completion model and a proved per-family bound. It also has the largest authoring and adoption burden, a real obligation-completeness risk, a clean cost that scales with `|O|`, and the conditional four-replan Q-78 scenario. Its derived maximum is not necessarily smaller than A or C.

## Option C - Fixed-depth verification protocol

### Controller, bounds, and minimum

Each plan review, work loop, and acceptance campaign has forward-only `Discovery`, `Verify1`, `Verify2`, and `BlindClosure` review nodes plus explicit `Repair1` and `Repair2` grouped actions. Phase is part of the controller state. `Discovery` uses two blind seats. A valid batch enters the complete stable finding map. `Repair1` jointly enters `PendingVerification`, and `Verify1` can clear the selected map only through named complete success. A failure or fix-induced child may use `Repair2` and `Verify2`. A valid finding at `Verify2` or blind closure is terminal. A risky settled path always reaches blind closure, and every ordinarily completing acceptance path reaches blind closure regardless of risk. No node can be revisited.

For each of `m + 2` phases, C has at most four review batches, five reviewer calls, four triage calls, four re-check calls, and two grouped repair calls. The task maximum remains `4(m + 2)` batches and a safe `15(m + 2)` automated-agent calls.

A low-risk plan or work phase can complete in one discovery batch and two reviewer calls. A risky plan or work phase and acceptance require at least discovery plus blind closure, two batches and three reviewer calls. C's whole-family minimum is `c_plan + sum(c_work_q) + 2` batches, where each `c` is one for low risk and two for risky. It does not scale with `|O|`.

### Evidence and trade-off

On Q-78, C stops at pass three because `Verify2` carries a high. With terminal floor `high` it enters `SeriousBlocked`, so residual acceptance is unavailable. With floor `critical` it enters the ordinary terminal state, where the human may accept that open high as residual risk. Under either floor it does not observe passes four through ten, which contain 23 later valid shortfalls, including further highs. C has the lowest fixed per-phase review depth and the smallest graph. It does not have a universally lowest whole-task call bound because B scales in different parameters. Its main cost is terminal rejection of useful late repairs, compounded at the critical floor by the option to deliver before those later shortfalls are known.

## Minimum-cost comparison

| Unit | A minimum. | B minimum. | C minimum. |
| --- | --- | --- | --- |
| Low-risk plan or work phase | One batch and two reviewer calls. | `n_q + 1` batches and `2(n_q + 1)` reviewer calls. | One batch and two reviewer calls. |
| Risky plan or work phase | Two batches and four reviewer calls. | `n_q + 1` batches and `2(n_q + 1)` reviewer calls. | Two batches and three reviewer calls. |
| Acceptance phase | One batch and two reviewer calls. | `n_a + 1` batches and `2(n_a + 1)` reviewer calls. | Two batches and three reviewer calls. |
| Whole family | `r_plan + sum(r_work_q) + 1` batches. | `r_plan + |O| + m + 1` batches. | `c_plan + sum(c_work_q) + 2` batches. |

A and C minima depend on phase count and risk. B additionally depends on the future canonical obligation count. These are lower bounds for a settled clean path, not expected costs.

## Project Principle comparison

| Project Principle | Option A. | Option B. | Option C. |
| --- | --- | --- | --- |
| Prefer the cleaner long-term architecture over the smallest diff | Unifies task spend but layers a ceiling over streaks. | Unifies scope, disposition, phase ownership, and bound in one controller. | Has the smallest graph but replaces present streak semantics. |
| Minimal by default | Fixed slices and two seats avoid dynamic policy. | Adds canonical obligation rows, the largest schema, and an ordinary minimum that scales with `|O|`. | Four nodes and two repairs are compact. |
| Safe on existing projects | Digest adoption can charge old spend and fail loudly. | `LegacyNoRubric` fails closed and requires a prospective freeze before B starts. | Historical stage adoption is ambiguous and must fail to a human. |
| Idempotent | Ordered replay preserves monotone spend. | Obligation state, phase identity, finding map, and spend reconstruct without reset. | Every node is single-use. |
| Make illegal states unrepresentable | Stable finding maps and terminal variants remove scalar erasure and reset. | Closed obligation variants prevent unverified closure, second reopen, phase transfer, unowned completion, and post-terminal action. | Forward-only stages prevent a third repair and closure bypass. |
| Ground decisions in evidence | Preserves the measured five-round boundary, but reserve values are weakly calibrated. | Targets observed scope movement, while the conditional replay exposes the possible cost of four replans. | Blind and informed stages fit anchoring evidence, but Q-78 shows early loss. |
| Reproducible | Fixed arithmetic and an exhaustive cardinality-two controller. | Per-phase bound derives from finite `O`, exact owners, and exhaustive cardinality-two controller, then composes algebraically. | Fixed graph and exhaustive cardinality-two controller. |
| Structured data first, project for humans | Identities, spend, finding maps, and receipts are structured. | Obligation rows, attempts, finding maps, ownership, scope deltas, and receipts are structured. | Stage, brief, finding map, and terminal state are structured. |

## Corrected proof and red controls

The durable proof is `docs/plans/workflow-calibration.explorations/q86-controller-proof.py`. It enumerates the actual A, B, and C phase controllers with a complete live finding-map cardinality of two. It explicitly models medium, all severity multisets up to that cardinality, valid-plus-dismissed-serious disposition products, joint repair and verification, same-owner and cross-owner low plus critical, parent plus fix-induced child, mixed owned and unowned batches, B's deferred initial-attempt priority, A's upheld-dismissal streak and reserve controls, B legacy adoption, fresh successor identity against ancestry, typed scope relations inside every controller, and acceptance blind closure.

The checker establishes each post-freeze B phase factor, while B plan review is the separately identified A controller with its inherited constants. It does not enumerate a multi-phase family. The whole-family formulas follow algebraically by summing disjoint exact phase owners under the enforced no-transfer rule. The arbitrary finite-finding result follows from the owner-product compositional argument in the shared package, not from claiming that a cardinality-two graph enumerates every finite map.

Its checks are:

- Every reachable phase graph is acyclic.
- Review spend never exceeds that phase's stated bound.
- No delivering terminal carries an outstanding finding or pending re-check.
- B residual delivery carries no `Untested` obligation.
- Every B owned outstanding finding and obligation state agree in both directions, including the cross-owner low-plus-critical batch.
- A reserve remains locked after an upheld serious dismissal unless earlier valid serious evidence had already unlocked it.
- A forecloses before a repair or review whose remaining path cannot attain its required clean suffix.
- A valid critical can leave the outstanding map only on its named verification after joint repair, an upheld dismissal re-check, or a terminal non-delivery transition.
- No active B state with an `Untested` obligation contains generation-one work. Early cross-owner findings against a closed owner remain in `DeferredReopen` with stable identity until every initial attempt finishes.
- An unowned B critical reaches the controller and cannot reach completion or residual delivery.
- `LegacyNoRubric` cannot enter B directly, reuse historical rounds, or become a zero-obligation campaign.
- A B successor binds exact family ids, both ancestry snapshots, both scope digests, presented options, chosen successor, predecessor spend, and the complete carried finding map. Same-family reuse, ancestor reuse, malformed ancestry, wrong-family, wrong-digest, missing-carry, and fresh-authority cases fail.
- Scope-expanded low, medium, high, and critical findings enter the A, B, and C transition relations with typed scope state. Their referral continuations preserve identity, debit no re-check authority, and remain covered by controller delivery and spend predicates.
- Every completing C acceptance path, including low-risk acceptance, visits `BlindClosure`.

Run exactly:

```sh
CHECKER=docs/plans/workflow-calibration.explorations/q86-controller-proof.py
export PYTHONDONTWRITEBYTECODE=1
nix shell nixpkgs#python3 -c python3 "$CHECKER" --mode all --phase acceptance --risk risky --obligations 2 --floor high
nix shell nixpkgs#python3 -c python3 "$CHECKER" --mode all --phase acceptance --risk risky --obligations 2 --floor critical
nix shell nixpkgs#python3 -c python3 "$CHECKER" --mode A --phase plan_review --risk low_risk --floor high
nix shell nixpkgs#python3 -c python3 "$CHECKER" --mode A --phase plan_review --risk risky --floor high
nix shell nixpkgs#python3 -c python3 "$CHECKER" --mode A --phase work_review --risk risky --floor high
nix shell nixpkgs#python3 -c python3 "$CHECKER" --mode C --phase acceptance --risk low_risk --floor high
for n in 0 1 2 3
do
    nix shell nixpkgs#python3 -c python3 "$CHECKER" --mode B --phase work:example --obligations "$n" --floor high
done
sha256sum "$CHECKER"
```

The exact two all-mode outputs are:

```text
A phase=acceptance risk=risky floor=high finding_cap=2 normal=5 reserve=2 required=1 states=1547 edges=1815 terminal=742 acyclic=true min_reviews=1 max_reviews=7 mixed_low_critical=40 parent_child=200 mixed_disposition=48 mixed_upheld=48 mixed_overturned=48 mixed_exhausted=8 mixed_exhaustion_cases=16 scope_routes=8 bad_delivery=0 bad_unverified_delivery=0 bad_critical_clear=0 bad_bound=0 bad_upheld_unlock=0 bad_upheld_streak=0 upheld_prior_streak_complete=0 upheld_batch5_complete=0 bad_mixed_preservation=0 bad_mixed_exhaustion=0 bad_scope_spend=0 bad_scope_identity=0 bad_scope_delivery=0 bad_foreclosure_state=0
B phase=acceptance obligations=2 floor=high finding_cap=2 bound=9 states=33951 edges=36002 terminal=24380 acyclic=true min_reviews=3 max_reviews=9 mixed_low_critical=210 parent_child=300 cross_owner_low_critical=37 atomic_cross_owner_low_critical=28 multi_initial_batch=46 mixed_disposition=580 mixed_same_owner=196 mixed_cross_owner=104 mixed_owned_unowned=224 mixed_blind_closure=216 mixed_upheld=580 mixed_overturned=580 mixed_exhausted=0 mixed_exhaustion_cases=144 deferred_early_findings=0 scope_routes=8 unowned_critical=442 bad_owner_state=0 bad_unowned_critical_delivery=0 bad_reopen_before_initial=0 bad_deferred_identity=0 bad_mixed_preservation=0 bad_mixed_exhaustion=0 bad_scope_spend=0 bad_scope_identity=0 bad_scope_delivery=0 bad_delivery=0 bad_unverified_delivery=0 bad_critical_clear=0 bad_bound=0
B legacy states=5 edges=4 legal_start_paths=2 bad_direct_campaign=0 bad_historical_credit=0 bad_zero_obligation=0
B successor structured_cases=14 accepted_different=true bad_same_scope=0 bad_reordered_scope=0 bad_missing_receipt=0 bad_missing_options=0 bad_wrong_family=0 bad_wrong_predecessor_digest=0 bad_wrong_successor_digest=0 bad_missing_carry=0 bad_fresh_authority=0 bad_same_family=0 bad_ancestor_reuse=0 bad_ancestry_binding=0 bad_receipt_ancestry=0 bad_predecessor_mutation=0
C phase=acceptance risk=risky floor=high finding_cap=2 stages=4 repairs=2 states=1365 edges=1528 terminal=825 acyclic=true min_reviews=2 max_reviews=4 mixed_low_critical=16 parent_child=64 mixed_disposition=32 mixed_upheld=32 mixed_overturned=32 mixed_exhausted=16 mixed_exhaustion_cases=8 scope_routes=8 bad_delivery=0 bad_unverified_delivery=0 bad_critical_clear=0 bad_bound=0 bad_mixed_preservation=0 bad_mixed_exhaustion=0 bad_scope_spend=0 bad_scope_identity=0 bad_scope_delivery=0 bad_acceptance_blind_bypass=0
A phase=acceptance risk=risky floor=critical finding_cap=2 normal=5 reserve=2 required=1 states=1568 edges=1836 terminal=763 acyclic=true min_reviews=1 max_reviews=7 mixed_low_critical=40 parent_child=200 mixed_disposition=48 mixed_upheld=48 mixed_overturned=48 mixed_exhausted=8 mixed_exhaustion_cases=16 scope_routes=8 bad_delivery=0 bad_unverified_delivery=0 bad_critical_clear=0 bad_bound=0 bad_upheld_unlock=0 bad_upheld_streak=0 upheld_prior_streak_complete=0 upheld_batch5_complete=0 bad_mixed_preservation=0 bad_mixed_exhaustion=0 bad_scope_spend=0 bad_scope_identity=0 bad_scope_delivery=0 bad_foreclosure_state=0
B phase=acceptance obligations=2 floor=critical finding_cap=2 bound=9 states=35010 edges=37061 terminal=25439 acyclic=true min_reviews=3 max_reviews=9 mixed_low_critical=210 parent_child=300 cross_owner_low_critical=37 atomic_cross_owner_low_critical=28 multi_initial_batch=46 mixed_disposition=580 mixed_same_owner=196 mixed_cross_owner=104 mixed_owned_unowned=224 mixed_blind_closure=216 mixed_upheld=580 mixed_overturned=580 mixed_exhausted=0 mixed_exhaustion_cases=144 deferred_early_findings=0 scope_routes=8 unowned_critical=442 bad_owner_state=0 bad_unowned_critical_delivery=0 bad_reopen_before_initial=0 bad_deferred_identity=0 bad_mixed_preservation=0 bad_mixed_exhaustion=0 bad_scope_spend=0 bad_scope_identity=0 bad_scope_delivery=0 bad_delivery=0 bad_unverified_delivery=0 bad_critical_clear=0 bad_bound=0
B legacy states=5 edges=4 legal_start_paths=2 bad_direct_campaign=0 bad_historical_credit=0 bad_zero_obligation=0
B successor structured_cases=14 accepted_different=true bad_same_scope=0 bad_reordered_scope=0 bad_missing_receipt=0 bad_missing_options=0 bad_wrong_family=0 bad_wrong_predecessor_digest=0 bad_wrong_successor_digest=0 bad_missing_carry=0 bad_fresh_authority=0 bad_same_family=0 bad_ancestor_reuse=0 bad_ancestry_binding=0 bad_receipt_ancestry=0 bad_predecessor_mutation=0
C phase=acceptance risk=risky floor=critical finding_cap=2 stages=4 repairs=2 states=1403 edges=1566 terminal=863 acyclic=true min_reviews=2 max_reviews=4 mixed_low_critical=16 parent_child=64 mixed_disposition=32 mixed_upheld=32 mixed_overturned=32 mixed_exhausted=16 mixed_exhaustion_cases=8 scope_routes=8 bad_delivery=0 bad_unverified_delivery=0 bad_critical_clear=0 bad_bound=0 bad_mixed_preservation=0 bad_mixed_exhaustion=0 bad_scope_spend=0 bad_scope_identity=0 bad_scope_delivery=0 bad_acceptance_blind_bypass=0
```

The exact inherited B plan-controller, risky-work foreclosure, and low-risk C acceptance outputs are:

```text
A phase=plan_review risk=low_risk floor=high finding_cap=2 normal=5 reserve=2 required=1 states=1547 edges=1815 terminal=742 acyclic=true min_reviews=1 max_reviews=7 mixed_low_critical=40 parent_child=200 mixed_disposition=48 mixed_upheld=48 mixed_overturned=48 mixed_exhausted=8 mixed_exhaustion_cases=16 scope_routes=8 bad_delivery=0 bad_unverified_delivery=0 bad_critical_clear=0 bad_bound=0 bad_upheld_unlock=0 bad_upheld_streak=0 upheld_prior_streak_complete=0 upheld_batch5_complete=0 bad_mixed_preservation=0 bad_mixed_exhaustion=0 bad_scope_spend=0 bad_scope_identity=0 bad_scope_delivery=0 bad_foreclosure_state=0
A phase=plan_review risk=risky floor=high finding_cap=2 normal=5 reserve=2 required=2 states=2351 edges=2756 terminal=1100 acyclic=true min_reviews=2 max_reviews=7 mixed_low_critical=34 parent_child=160 mixed_disposition=48 mixed_upheld=48 mixed_overturned=48 mixed_exhausted=0 mixed_exhaustion_cases=16 scope_routes=8 bad_delivery=0 bad_unverified_delivery=0 bad_critical_clear=0 bad_bound=0 bad_upheld_unlock=0 bad_upheld_streak=0 upheld_prior_streak_complete=43 upheld_batch5_complete=1 bad_mixed_preservation=0 bad_mixed_exhaustion=0 bad_scope_spend=0 bad_scope_identity=0 bad_scope_delivery=0 bad_foreclosure_state=0
A phase=work_review risk=risky floor=high finding_cap=2 normal=5 reserve=2 required=2 states=2351 edges=2756 terminal=1100 acyclic=true min_reviews=2 max_reviews=7 mixed_low_critical=34 parent_child=160 mixed_disposition=48 mixed_upheld=48 mixed_overturned=48 mixed_exhausted=0 mixed_exhaustion_cases=16 scope_routes=8 bad_delivery=0 bad_unverified_delivery=0 bad_critical_clear=0 bad_bound=0 bad_upheld_unlock=0 bad_upheld_streak=0 upheld_prior_streak_complete=43 upheld_batch5_complete=1 bad_mixed_preservation=0 bad_mixed_exhaustion=0 bad_scope_spend=0 bad_scope_identity=0 bad_scope_delivery=0 bad_foreclosure_state=0
C phase=acceptance risk=low_risk floor=high finding_cap=2 stages=4 repairs=2 states=1365 edges=1528 terminal=825 acyclic=true min_reviews=2 max_reviews=4 mixed_low_critical=16 parent_child=64 mixed_disposition=32 mixed_upheld=32 mixed_overturned=32 mixed_exhausted=16 mixed_exhaustion_cases=8 scope_routes=8 bad_delivery=0 bad_unverified_delivery=0 bad_critical_clear=0 bad_bound=0 bad_mixed_preservation=0 bad_mixed_exhaustion=0 bad_scope_spend=0 bad_scope_identity=0 bad_scope_delivery=0 bad_acceptance_blind_bypass=0
```

The exact B sweep output is:

```text
B phase=work:example obligations=0 floor=high finding_cap=2 bound=1 states=180 edges=188 terminal=135 acyclic=true min_reviews=1 max_reviews=1 mixed_low_critical=2 parent_child=0 cross_owner_low_critical=0 atomic_cross_owner_low_critical=0 multi_initial_batch=0 mixed_disposition=8 mixed_same_owner=0 mixed_cross_owner=0 mixed_owned_unowned=0 mixed_blind_closure=8 mixed_upheld=8 mixed_overturned=8 mixed_exhausted=8 mixed_exhaustion_cases=8 deferred_early_findings=0 scope_routes=8 unowned_critical=13 bad_owner_state=0 bad_unowned_critical_delivery=0 bad_reopen_before_initial=0 bad_deferred_identity=0 bad_mixed_preservation=0 bad_mixed_exhaustion=0 bad_scope_spend=0 bad_scope_identity=0 bad_scope_delivery=0 bad_delivery=0 bad_unverified_delivery=0 bad_critical_clear=0 bad_bound=0
B phase=work:example obligations=1 floor=high finding_cap=2 bound=5 states=6678 edges=6999 terminal=4893 acyclic=true min_reviews=2 max_reviews=5 mixed_low_critical=56 parent_child=100 cross_owner_low_critical=0 atomic_cross_owner_low_critical=0 multi_initial_batch=0 mixed_disposition=156 mixed_same_owner=60 mixed_cross_owner=0 mixed_owned_unowned=64 mixed_blind_closure=64 mixed_upheld=156 mixed_overturned=156 mixed_exhausted=0 mixed_exhaustion_cases=64 deferred_early_findings=0 scope_routes=8 unowned_critical=148 bad_owner_state=0 bad_unowned_critical_delivery=0 bad_reopen_before_initial=0 bad_deferred_identity=0 bad_mixed_preservation=0 bad_mixed_exhaustion=0 bad_scope_spend=0 bad_scope_identity=0 bad_scope_delivery=0 bad_delivery=0 bad_unverified_delivery=0 bad_critical_clear=0 bad_bound=0
B phase=work:example obligations=2 floor=high finding_cap=2 bound=9 states=33951 edges=36002 terminal=24380 acyclic=true min_reviews=3 max_reviews=9 mixed_low_critical=210 parent_child=300 cross_owner_low_critical=37 atomic_cross_owner_low_critical=28 multi_initial_batch=46 mixed_disposition=580 mixed_same_owner=196 mixed_cross_owner=104 mixed_owned_unowned=224 mixed_blind_closure=216 mixed_upheld=580 mixed_overturned=580 mixed_exhausted=0 mixed_exhaustion_cases=144 deferred_early_findings=0 scope_routes=8 unowned_critical=442 bad_owner_state=0 bad_unowned_critical_delivery=0 bad_reopen_before_initial=0 bad_deferred_identity=0 bad_mixed_preservation=0 bad_mixed_exhaustion=0 bad_scope_spend=0 bad_scope_identity=0 bad_scope_delivery=0 bad_delivery=0 bad_unverified_delivery=0 bad_critical_clear=0 bad_bound=0
B phase=work:example obligations=3 floor=high finding_cap=2 bound=13 states=98023 edges=104837 terminal=69460 acyclic=true min_reviews=4 max_reviews=11 mixed_low_critical=519 parent_child=548 cross_owner_low_critical=177 atomic_cross_owner_low_critical=120 multi_initial_batch=198 mixed_disposition=1420 mixed_same_owner=396 mixed_cross_owner=464 mixed_owned_unowned=480 mixed_blind_closure=512 mixed_upheld=1420 mixed_overturned=1420 mixed_exhausted=0 mixed_exhaustion_cases=256 deferred_early_findings=530 scope_routes=8 unowned_critical=901 bad_owner_state=0 bad_unowned_critical_delivery=0 bad_reopen_before_initial=0 bad_deferred_identity=0 bad_mixed_preservation=0 bad_mixed_exhaustion=0 bad_scope_spend=0 bad_scope_identity=0 bad_scope_delivery=0 bad_delivery=0 bad_unverified_delivery=0 bad_critical_clear=0 bad_bound=0
```

The declared B bounds are `1`, `5`, `9`, and `13`. The clean minimums remain `1`, `2`, `3`, and `4`. An upheld incidental dismissal against a non-primary untested owner does not substitute for that owner's initial attempt. The cardinality-two sweep reaches maxima `1`, `5`, `9`, and `11` because its global two-finding interaction cap cannot populate every finding-bearing attempt at three obligations. The arbitrary finite compositional argument supplies the cardinality-independent `4n_q + 1` maximum. `mixed_exhausted` counts mixed states reached from the canonical initial graph after automatic repair authority is exhausted, using the numeric authority boundary for A and B and the terminal `Verify2` or `BlindClosure` stages for C. `mixed_exhaustion_cases` additionally seeds each controller's legal last-batch boundary and exhausts both re-check continuations there. It is therefore non-zero for A, B, and C even where the canonical cardinality-two start reaches no mixed state on its last batch. `scope_routes=8` means that low, medium, high referral, high upheld, high overturned, critical referral, critical upheld, and critical overturned are all reachable inside that controller. The zero scope-spend, identity, delivery, and bound counters are evaluated over those same graph edges. The checker SHA-256 is `d0dabe6da04fde2009a2baf22d0a3d9fabdfbd6bc96d2859d26043531aff579a`.

Run the conditional Q-78 scenario and its selected-length controls exactly:

```sh
docs/plans/workflow-calibration.explorations/q86-q78-scope-replay.sh docs/metrics/workflow.jsonl
docs/plans/workflow-calibration.explorations/q86-q78-scope-replay.sh --self-test
```

The live summary is:

```text
summary passes=10 observed_named_folds=4 assumed_digest_changes=4 conditional_terminal_replans=4 conditional_families=5 conditional_additional_human_receipts=4 conditional_additional_plan_review_and_freeze_cycles=4
```

The exact selected-length control output is:

```text
self_test selected_passes=9 summary passes=9 observed_named_folds=4 assumed_digest_changes=4 conditional_terminal_replans=4 conditional_families=5 conditional_additional_human_receipts=4 conditional_additional_plan_review_and_freeze_cycles=4
self_test selected_passes=11 summary passes=11 observed_named_folds=4 assumed_digest_changes=4 conditional_terminal_replans=4 conditional_families=5 conditional_additional_human_receipts=4 conditional_additional_plan_review_and_freeze_cycles=4
```

## Required red-control paths

| Path | A. | B. | C. |
| --- | --- | --- | --- |
| Repeated human resume | Resume reconstructs spend. Every phase ends by batch seven. | Resume reconstructs phase, obligation, and complete finding-map state. Every phase ends within `4n_q + 1`. | Resume reconstructs one forward-only node. Every phase ends by batch four. |
| Unbounded acceptance repair | The final finding map routes to a terminal decision by batch seven. | Each obligation has at most one initial and one reopened grouped repair. Blind-closure findings are terminal. | A finding at `Verify2` or closure is terminal. |
| Multiple findings and dispositions in one batch | Every severity map up to cardinality two is exhausted, including valid plus dismissed serious reports. Upheld and overturned re-check continuations retain the open repair component through normal authority and exhaustion. | The atomic owner map covers same-owner, cross-owner, owned-plus-unowned, blind-closure, and valid-plus-dismissed-serious products. Every affected obligation advances with the complete stable map. | Every severity map and valid-plus-dismissed-serious product up to cardinality two is exhausted through both re-check outcomes and exhaustion. |
| Parent plus fix-induced child | Failed joint verification keeps the parent open and adds the child under a new stable id. | The attempt terminally preserves both parent and child. | The next fixed repair jointly owns both only when a repair stage remains. |
| Fix-induced high near exhaustion | It consumes an authorised verification batch and unlocks only unspent reserve. | It is added to the attempt map and cannot create another attempt. | It uses the next fixed repair only before `Verify2`. |
| Upheld serious dismissal | It does not unlock A reserve without earlier valid serious evidence. | It settles only through the attached re-check. | It settles only through the attached re-check. |
| Scope-expanded low | It is backlogged, consumes its opened batch, and cannot enlarge frozen scope. | It is backlogged and cannot add an obligation. | It is backlogged and cannot add a node. |
| Scope-expanded medium | It enters the terminal human scope decision. | It enters the terminal human scope decision without adding an obligation. | It enters the terminal human scope decision. |
| Scope-expanded high | A proposed out-of-scope ruling waits for independent re-check. Upheld goes to the terminal human scope decision and overturned returns in scope. | The same re-check route applies before any scope terminal. | The same re-check route applies before any scope terminal. |
| Scope-expanded critical | A proposed out-of-scope ruling waits for re-check, but either result is `SeriousBlocked` and cannot backlog or deliver. | The same always-safety-blocking route applies to an owned or unowned critical. | The same always-safety-blocking route applies. |
| Unowned in-scope critical | The common finding map blocks delivery. | `UnownedInScopeFinding` enters `SeriousBlocked` and cannot complete or deliver residual. | The common finding map blocks delivery. |
| Relitigation without new evidence | It preserves disposition and cannot reset spend. | It cannot take `MateriallyNewEvidence` or consume a reopen. | It preserves disposition and cannot point backwards. |
| Legacy task without rubric | Prospective budget adoption remains separate. | It terminally preserves legacy disposition or enters new prospective plan review and freeze. No direct campaign or historical credit exists. | Prospective stage adoption remains separate. |
| Narrowing or replan | The family becomes terminal and no slice returns. | The family becomes terminal. A successor requires immutable predecessor, receipt, and structured material scope delta. | The family becomes terminal and no stage returns. |
| Unresolved critical at exhaustion | Completion and residual delivery are unconstructible. | Completion and residual delivery are unconstructible. | Completion and residual delivery are unconstructible. |
| Blind closure | Every batch has a blind seat. | Each phase has one non-transferable blind-closure seat. | `BlindClosure` is a required node on risky and repaired plan or work paths and on every ordinarily completing acceptance path. |

## Migration and enforcement

All options move the same core surfaces. `.agents/workflow.toml`, `pack/workflow.toml`, and `WorkflowSpec` gain the chosen controller constants. The shared `ReviewProcess` reconstruction gains task-family, phase, finite finding map, scope, terminal, and acceptance-campaign state while preserving disjoint `Convergence` and `SinglePass` observations. The plan schema and pack plan template gain immutable identities, freeze and adoption data, and terminal receipts. Metrics gain prospective scope, finding, evidence, disposition, review-brief, spend or stage, and terminal events. Historical events remain append-only.

`validate --workflow` enforces exact ids, phase identity, monotone authority, repair-before-verification, complete-map terminal predicates, dismissal re-checks, no action after terminal state, and no delivery with an unresolved critical. `next` reports only the actor and brief allowed by reconstructed state. It does not manufacture a finding, verdict, human decision, or proof of an external review.

B additionally moves canonical obligation rows and exact phase ownership into the plan source, validates `C_q = 4|O_q| + 1`, enforces initial-attempt priority, implements `UnownedInScopeFinding` and `LegacyNoRubric`, and enforces the selected successor test. That test binds a terminal immutable predecessor, its ancestry registry, a successor id fresh against that whole registry, the exact successor ancestry, both scope digests, every presented option, the chosen successor, predecessor spend, the complete carried finding map, and a non-empty structured obligation or exclusion delta attested as material. A adds fixed accounts and reserve eligibility, including the upheld-dismissal control. C adds forward-only stage events and adoption state.

Canonical guidance and generated copies must move together through `pack/AGENTS.md`, `pack/instrument.md`, planner, orchestrator, reviewer, triager, and implementer prompts, ledger and plan templates, `AGENTS.md`, `.agents/AGENTS.reference.md`, `.agents/prompts/`, `.agents/LEDGER.template.md`, `.agents/workflow.toml`, README, and changelog. The chosen work must land after the shared typed review reconstruction. Reviewer diversity, the quality of a lineage judgement, material scope judgement, and actual blindness remain advisory. Identity, authority, disposition, phase, terminality, and critical legality are mechanical.

## Excluded candidates

- The current mechanism is excluded because repeated resume and later acceptance repair each contain a reachable cycle.
- A severity-decay gate is excluded because its multi-pass trajectory needs trustworthy prospective sequence data that does not exist. This differs from the per-finding prospective severity used by the serious floor.
- A probabilistic or survival-threshold gate is excluded because the sample and lineage data cannot support a safe stopping probability.
- A pure frozen-obligation rule without sealed phase campaigns is excluded because malformed or stalled progress could otherwise recreate an unbounded path.
- The strict-narrower-or-disjoint B successor rule remains an unselected proposal alternative. Selected B permits receipted material additions and makes no cross-family chain bound.

## Recommendation

Choose `B - Frozen obligations with sealed phase campaigns`, with medium to low confidence.

B is the cleaner long-term architecture under Prefer the cleaner long-term architecture over the smallest diff, Make illegal states unrepresentable, and Structured data first, project for humans. Its corrected controller gives each obligation, finding, and phase one typed source, derives a finite per-family bound without trusting broken outcome arrays, fails closed on unowned findings, and makes scope movement terminal rather than invisible.

The recommendation is not high confidence under Minimal by default, Safe on existing projects, and Ground decisions in evidence. B's clean minimum scales with `|O|`. Its canonical obligation source can omit a genuine defect. Its legacy adoption requires a prospective freeze. The Q-78 four-replan cost is conditional on unreconstructible digest assumptions rather than a measured fact. A focused schema and reconstruction proof of concept must therefore show that the closed obligation rows remain finite, precise, non-duplicative, and able to route genuine uncited findings through `UnownedInScopeFinding`. If that proof fails, the human decision reopens with A as the recommendation. No fallback architecture is pre-authorised and a new receipt is required.

Evidence that would overturn B includes obligation sets that routinely omit genuine in-scope defects, frozen-scope tasks that still require long repair sequences, a serious finding routed to backlog, ordinary clean costs dominated by `|O|`, or prospective evidence that A preserves materially more unique serious findings for acceptable cost. Evidence that changes only a constant includes prospective distributions of initial verification failures and materially-new-evidence reopens.

## YAGNI boundary

- Do not build a general issue tracker, project-wide defect database, mutable rubric editor, or autonomous obligation extractor.
- Do not build an autonomous risk, scope, severity, material-delta, or residual-risk judge.
- Do not build probabilistic stopping, dynamic pricing, transferable credits, a reviewer marketplace, or a model optimiser.
- Do not infer historical finding lineage, obligation membership, scope digest, stage, or closure.
- Do not build a persistent workflow service, general workflow language, or new scheduler beyond the planned typed fleet.
- Do not create automatic authority from rename, rebuild, replan, narrowing, scope change, or human resume.
- Do not implement a mechanism, floor, or controller constant until the human decides and the planner records the receipt and fold.

## Exact human decision and no-decision boundary

The orchestrator must ask which architecture Q-86 should fold into `workflow-calibration`: A, B, or C. It must also ask whether the serious terminal floor is `high` or `critical`, or record that the floor is deferred to a separate pre-implementation decision.

The presentation must state A's pass-seven Q-78 terminal and three undiscovered low shortfalls, B's post-freeze `n_q + 1` phase minimum, its inherited plan controller, and its `4|O| + m + 8` per-family maximum, the conditional four-replan scenario under its named-fold digest assumptions, and C's pass-three outcome under both floors. At floor `high` C is `SeriousBlocked`. At floor `critical` residual acceptance of the open high is available. Both C outcomes leave 23 later shortfalls undiscovered, including further highs. The presentation must also state the different bound parameters, the B proof-of-concept gate, and the recommendation above.

Until the human chooses, Q-86 remains `open` and implementation is blocked. The choice does not author code. A later planner fold must sequence the chosen mechanism after the shared typed review reconstruction, include instrumentation and documentation migrations, and record the decision receipt. The baseline, severity gate, the five-normal-plus-two-reserve slice used by A and inherited by B plan review, B's one reopen, C's four-stage and two-repair depth, the serious floor, every other controller constant, and any implementation remain unapproved by Q-85 and this synthesis.
