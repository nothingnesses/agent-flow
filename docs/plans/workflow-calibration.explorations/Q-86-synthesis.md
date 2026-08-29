# Q-86 narrowed synthesis: bounded convergence options

## Status and decision boundary

Q-86 is `decided -> folded into bounded-convergence-option-b-proof`. The exact architecture options were `A - Sealed phase budget`, `B - Frozen obligations with sealed phase campaigns`, and `C - Fixed-depth verification protocol`. The recommendation and human choice were both Option B. Q-91 separately records the exact terminal-floor options `high`, `critical`, and `defer`, with recommendation and chosen value `high`.

The five-round review loop on the earlier proof-before-choice synthesis ended at its cap with valid findings in every round. Q-88 records the human decision to narrow the proof scope rather than open a sixth ordinary review round. The narrowed decision artefact then reached its own five-round cap with valid findings in every round and two low findings in round 5. Q-89 records the human choice `Fix, verify once, then close`. It retired the capped narrowed counters and authorised focused mixed-model verification of the two low fixes. That verification found one valid low current-state wording defect in the structured Q-86 ask and returned it to the human as Q-89 required. Q-90 records the human choice `Fix and merge`. It authorised the exact correction and merge without another review. The narrowed decision artefact is closed.

This narrowed decision artefact retains all three bounded architecture proposals and their algebraic finite bounds as decision provenance. It does not present the executable controller or replay scripts as recommendation-eligibility proofs. Those scripts are adversarial prototypes that exposed proof obligations. Selected Option B must receive a complete executable proof of concept before implementation. No workflow or production behaviour changes in this decision fold. Q-86 and Q-91 each append exactly one `type: "decision"` event to the metrics log without changing the metrics schema or behaviour. The generated plan remains only a projection of the Q-86, Q-88, Q-89, Q-90, and Q-91 planning sources.

The source proposal labels map as follows. Option A maps to state-machine Candidate A in `Q-86-state-machine.md` and safety M1 in `Q-86-safety-process.md`. Selected Option B maps to safety M2 plus the state-machine proposal's sealed authority envelope. Option C maps to state-machine Candidate B. Safety M3 remains excluded. These proposals remain design inputs under the prototype caveats below, and this provenance map does not revive any proof or recommendation-eligibility claim.

No controller constant or production implementation has been selected. Q-85 authorised the design pass. Q-88 changed only the proof timing and gate. Q-89 retired the capped narrowed counters and authorised only the two low repairs plus one focused mixed-model verification. Q-90 authorised only the exact current-state wording correction and merge without another review. Q-86 selects Option B and Q-91 selects floor `high`, but both authorise proof work only.

## Evidence that constrains the choice

### Current mechanism and Q-78

The current mechanism remains comparison evidence and is not an admissible bounded option. For every positive integer `n`, five `new_valid` rounds followed by human `resume` can repeat `n` times and leave the loop active after `5n` rounds. An acceptance pass with a valid shortfall can likewise route through repair to another acceptance pass for every `n`. Neither path has a finite forced bound.

The authoritative Q-78 selector is:

```sh
jq -s 'map(select(.type == "round" and .task == "q78-design-pass" and .phase == "acceptance")) | {passes: length, valid_shortfalls: map(.valid_findings)}' docs/metrics/workflow.jsonl
```

At this decision point it returns ten passes and `[7,10,5,6,5,5,4,2,1,0]`. The run closed at pass ten. It demonstrates high review cost, late serious findings, scope movement, and eventual closure. It does not demonstrate divergence.

The four named Q-78 folds are observed in artefact descriptions, but the historical log has no prospective Option B obligation rows or scope digests. Treating those four folds as four material digest changes is a counterfactual assumption, not a reconstructed fact.

### Instrument and evidence limits

Nineteen historical round records say `outcome: "clean"` while `valid_findings` is greater than zero and advance `consecutive_clean`. Historical outcome and streak fields are therefore unsuitable as proof inputs for a new controller. Historical findings also lack stable cross-review identity, and only six of the ten Q-78 triage files remain in the tree.

The local and external evidence supports distinct blind discovery and informed fix-verification briefs. It does not establish a causal yield estimate because blindness, model, harness, lens, and prompt breadth are confounded.

The architecture decision must therefore use the algebraic design, trade-offs, observed costs, and explicit uncertainty. It must not infer proof from a prototype reporting zero counters.

## Prototype boundary and known limitations

`docs/plans/workflow-calibration.explorations/q86-controller-proof.py` and `q86-q78-scope-replay.sh` are retained as evidence. They are useful because adversarial review found concrete missing states and unsound proof claims. They are not complete proofs of A, B, or C.

The controller prototype has at least these known limitations from `docs/plans/agent-scaffold.reviews/q86-synthesis-r5-triage.md`:

- Its global two-finding cap includes settled identities, so adding settled history removes fresh-finding transitions and invalidates the claimed arbitrary-finite composition.
- Its published scope-route counter does not establish the high and critical overturn paths by transition identity.
- It does not soundly carry a serious finding into a successor campaign as a delivery-blocking state.
- It does not enumerate the product of scope re-check and dismissal re-check states, and a seeded product can escape `SeriousBlocked`.
- Successor freshness is local to one ancestry chain rather than global across the append-only family registry.
- `MateriallyNewEvidence` neither requires nor records a fresh evidence identity.

The replay prototype also undercounts when one artefact description repeats a known fold identity and introduces a new one in the same record. Its four-replan output is a conditional scenario over the current ten-pass sample, not a proof of prospective Option B behaviour.

Earlier rounds exposed additional obligations around complete finite finding maps, cross-owner batches, owner-state products, legacy adoption, unowned in-scope findings, terminal floors, blind closure, reserve and foreclosure semantics, scope routing, successor receipts, and cost vocabulary. The selected-option proof gate below treats every applicable valid finding from rounds 1 through 5 as open until a traceability matrix and executable assertion close it.

## Shared proposed safety package

These are architecture requirements, not established prototype results.

- Stable finding identity must survive reviewers, triage, repairs, verification, later phases, replans, and successor families.
- One atomic triaged batch must carry an arbitrary finite map of owners to finding maps plus an unowned set. Each entry must retain severity, lineage, scope relation, disposition, evidence identity, and any parent identity.
- Duplicate reviewer reports must join one finding identity without erasing reviewer attribution.
- Joint repair and verification must name the complete selected set. Partial verification must not silently resolve unverified findings.
- A valid critical may leave the blocking set only after named repair and verification or a terminal non-delivery disposition. A dismissed high or critical requires the independent re-check.
- The acceptance rubric freezes after plan review and before implementation. A genuine violation of a frozen obligation, invariant, boundary, or duty remains in scope. Optional low scope expansion may be backlogged. Medium goes to a terminal human scope decision. High goes through independent scope re-check and then either returns in scope or goes to the terminal human scope decision. Either critical scope result remains safety-blocking.
- Resume, rename, rebuild, and unchanged replan reconstruct the same authority. A materially different successor requires a terminal immutable predecessor, a globally fresh family identity, a human receipt, an exact structured scope delta, predecessor spend, and the complete carried finding set.
- A successor must treat carried serious findings as live delivery blockers until resolved or given a terminal non-delivery disposition.
- Blind and informed reviewer briefs remain distinct. Every ordinarily completing acceptance path reserves blind closure evidence.
- Backstop re-checks do not debit review authority.

## Option A - Sealed phase budget

### Proposed controller and algebraic bound

A declares a non-resettable budget over plan review, each of `m` work loops, and acceptance. Each of the `m + 2` phase slices has five normal review batches and two already-declared reserve batches. Reserve unlock is proposed only after a triage-valid high or critical or an overturned serious dismissal. Plan and work retain their risk-scaled clean suffix. Acceptance requires one settled pass after every earlier in-scope finding and Roadmap step is settled. That single settled acceptance batch has one broad blind seat and one rubric-focused or informed seat; the blind seat supplies the required closure evidence. A remaining-clean-suffix check forecloses an action that can no longer complete within authority.

The proposed maximum is:

```text
R_A = 7(m + 2) review batches
```

With two reviewer calls, at most one triage, at most one re-check, and at most six repairs per phase, the proposed conservative automated-agent maximum is:

```text
I_A = 34(m + 2)
```

The clean whole-family minimum is `r_plan + sum(r_work_q) + 1`, where each plan or work `r` is one at low risk and two at risky. The formulas follow algebraically from the proposed fixed slices. The selected-option proof of concept must establish every transition, reserve rule, foreclosure rule, finding-map invariant, and terminal path before these formulas can govern implementation.

### Trade-off

A is closest to current streak semantics and preserves more bounded late discovery than C on the Q-78 descriptive replay. It adds a substantial account model and makes five-plus-two a policy knob with weak calibration. On the Q-78 replay it would reach a terminal decision at pass seven, leaving three later low shortfalls undiscovered.

## Option B - Frozen obligations with sealed phase campaigns

### Proposed controller and algebraic bound

B reuses A's sealed controller for plan review. Plan convergence freezes a finite canonical set `O` of obligation rows, a finite set of `m` work-loop identities, acceptance, and one exact post-freeze phase owner for every obligation. A genuine in-scope finding with no canonical owner enters `UnownedInScopeFinding` and blocks ordinary completion.

For post-freeze phase `q`, let `n_q = |O_q|`. Each obligation has at most an initial attempt and verification, one materially-new-evidence reopen attempt and verification, while the phase has one non-transferable blind-closure batch. The proposed per-phase maximum and clean minimum are:

```text
C_q = 4n_q + 1
L_q = n_q + 1
```

With `p = m + 1` post-freeze phases, exact ownership and no transfer give the proposed whole-family bounds:

```text
R_B = 7 + sum(4n_q + 1)
    = 4|O| + m + 8

L_B = r_plan + |O| + m + 1
```

The proposed conservative automated-agent maximum is:

```text
I_B = 18|O| + 4m + 38
```

These are algebraic design bounds. The controller prototype does not prove their safety premises. In particular, the selected-option proof must show arbitrary finite batch handling, exact owner-state composition, fresh-evidence reopen, globally unique successor identity, serious carry into successors, legacy adoption, blind closure, every floor outcome, and terminality without relying on the prototype's global finding cap.

### Trade-off

B gives scope, ownership, finding disposition, and completion one structured architecture. It also has the largest authoring and adoption burden, a clean review cost that scales with `|O|`, and a real risk that canonical obligation rows omit a genuine defect. Under the explicit counterfactual assumption that each of the four observed Q-78 folds changes the structured obligation or exclusion digest, B would require four terminal replans, four additional human receipts, four additional plan-review and freeze campaigns, and five families. If one assumed fold would not change the canonical digest, its associated replan and cost disappear.

## Option C - Fixed-depth verification protocol

### Proposed controller and algebraic bound

C gives each plan review, work loop, and acceptance campaign forward-only `Discovery`, `Verify1`, `Verify2`, and `BlindClosure` review nodes, with at most `Repair1` and `Repair2`. A valid finding at `Verify2` or blind closure goes to a terminal human state rather than another automatic repair. Risky plan and work paths and every ordinarily completing acceptance path require blind closure.

For each of the `m + 2` phases, the proposed maximum is four review batches and fifteen automated-agent calls. Across those four batches, the maximum comprises five reviewer passes (two at Discovery and one each at Verify1, Verify2, and BlindClosure), four triage calls, four backstop calls, and two repair passes, so `5 + 4 + 4 + 2 = 15`. The whole-family maxima are:

```text
R_C = 4(m + 2)
I_C = 15(m + 2)
```

For a risky plan or work phase and for acceptance, the proposed minimum is a Discovery batch with two reviewers plus a BlindClosure batch with one reviewer, hence two review batches and three reviewer calls. The clean whole-family minimum is `c_plan + sum(c_work_q) + 2`, where each plan or work `c` is one at low risk and two at risky. The selected-option proof of concept must establish phase typing, every forward transition, both repair generations, mandatory acceptance blind closure, arbitrary finite finding products, scope and dismissal products, terminal floors, and all delivery blocks.

### Trade-off

C has the smallest fixed phase graph and lowest fixed per-phase maximum. It rejects useful late repair even when earlier stages were cheap. On the Q-78 descriptive replay it stops at pass three, leaving 23 later shortfalls undiscovered, including further highs. At floor `high` it is `SeriousBlocked`. At floor `critical` residual acceptance of the open high is available.

## Cost comparison

| Unit | A minimum | B minimum | C minimum |
| --- | --- | --- | --- |
| Low-risk plan review | One batch and two reviewer calls | One batch and two reviewer calls, reusing A's sealed plan controller | One batch and two reviewer calls |
| Risky plan review | Two batches and four reviewer calls | Two batches and four reviewer calls, reusing A's sealed plan controller | Two batches and three reviewer calls |
| Low-risk post-freeze work phase | One batch and two reviewer calls | `n_q + 1` batches and `2(n_q + 1)` reviewer calls | One batch and two reviewer calls |
| Risky post-freeze work phase | Two batches and four reviewer calls | `n_q + 1` batches and `2(n_q + 1)` reviewer calls | Two batches and three reviewer calls |
| Post-freeze acceptance phase | One batch and two reviewer calls | `n_q + 1` batches and `2(n_q + 1)` reviewer calls, with `q = acceptance` | Two batches and three reviewer calls |
| Whole family | `r_plan + sum(r_work_q) + 1` batches | `r_plan + \|O\| + m + 1` batches | `c_plan + sum(c_work_q) + 2` batches |

C has the lowest fixed per-phase maximum. Whole-family costs cannot be universally ranked across all three options because B additionally scales with `|O|`.

## Project Principle comparison

| Project Principle | Option A | Option B | Option C |
| --- | --- | --- | --- |
| Prefer the cleaner long-term architecture over the smallest diff | Unifies task spend but layers a budget over existing streaks | Unifies scope, ownership, disposition, phase authority, and completion while retaining A's sealed plan-review controller | Uses the smallest fixed graph but replaces streak progression |
| Minimal by default | Reuses current semantics but adds account and reserve fields | Adds canonical obligations and the largest schema on top of A's plan-review account and reserve fields | Uses four review nodes and two repair generations |
| Safe on existing projects | Prospective adoption can charge prior spend and fail loudly | `LegacyNoRubric` can fail closed before prospective freeze | Historical stage adoption is ambiguous and must route to a human |
| Idempotent | Ordered replay preserves monotone spend | Frozen owner and obligation state reconstruct without reset | Every stage is forward-only and single-use |
| Make illegal states unrepresentable | Typed accounts can remove reset and unsafe completion paths | Typed obligations can make unverified closure, phase transfer, and unowned completion illegal | The graph can make a third automatic repair and backward movement illegal |
| Ground decisions in evidence | Keeps the measured five-round boundary, but reserve values are weakly calibrated | Addresses observed scope movement, but obligation cost and completeness lack prospective evidence and its inherited five-normal-plus-two-reserve values are weakly calibrated | Matches anchoring evidence, but Q-78 shows the cost of early terminality |
| Reproducible | Fixed arithmetic is reproducible once the transition model is proved | Finite rows and exact ownership make the algebra reproducible once the controller is proved | A fixed graph is reproducible once every transition product is proved |
| Structured data first, project for humans | Accounts, findings, and receipts are structured | Obligations, owners, attempts, findings, scope deltas, and receipts are structured | Stages, briefs, findings, and terminal state are structured |

## Selected architecture and confidence boundary

The recommendation and human choice are both `B - Frozen obligations with sealed phase campaigns`.

The decision does not rely on the controller prototype. It rests on the conceptual architecture. B gives frozen scope, exact obligation ownership, finding disposition, phase authority, and completion one structured source for post-freeze phases, where A keeps streak and budget as separate stopping concepts throughout and C discards bounded late repair earlier. B does not replace A's plan machinery. It inherits A's sealed plan-review controller, including its account and reserve model and weakly calibrated five-normal-plus-two-reserve values. That reasoning is strongest under Prefer the cleaner long-term architecture over the smallest diff, Make illegal states unrepresentable, and Structured data first, project for humans.

Confidence remains low under Minimal by default, Safe on existing projects, and Ground decisions in evidence. B has the largest schema, its clean cost scales with `|O|`, its inherited plan-review account and reserve values are weakly calibrated, an incomplete obligation set is a new safety risk, and five proof rounds found serious omissions in the prototype. The decision therefore authorises only the blocking proof and does not establish eligibility for production implementation.

## Blocking selected Option B proof of concept

The decision fold materialises `bounded-convergence-option-b-proof` as the complete executable proof of concept for selected Option B. Its completion is an explicit blocker for every later production implementation unit for bounded convergence. The proof of concept is a blocking specification test, not production controller code, and it must converge through the ordinary risky review loop.

The proof of concept must:

1. Define the selected architecture's complete typed state and every legal transition, including plan review, work review, acceptance, repair, verification, re-check, exhaustion, terminal decision, resume reconstruction, narrowing, replan, revert, abandonment, and completion where the option permits them.
2. Model arbitrary finite finding maps soundly. A finite interaction sweep may support the proof, but it must not cap persistent history in a way that removes fresh-finding, reopen, scope, or delivery transitions. The executable oracle must include settled history followed by fresh valid, serious-dismissal, and scope batches.
3. Model atomic cross-owner batches, mixed owned and unowned findings, low plus critical, parent plus fix-induced child, valid plus serious-dismissal, scope plus dismissal, and multiple simultaneous scope re-checks without scalar erasure or bulk rewriting unrelated identities.
4. Preserve serious findings across terminal replan and successor families as live delivery blockers until verified or given a terminal non-delivery disposition.
5. Enforce a global append-only family identity registry, fresh successor identity across predecessors, ancestors, siblings, and unrelated existing families, one authorised successor per terminal predecessor, exact ancestry, and exact receipt binding.
6. Require materially fresh evidence for reopen, retain the old evidence and root finding identity, and reject same-evidence relitigation.
7. Model prospective and legacy adoption separately. A legacy task must not receive prospective authority, closure credit, a zero-obligation reinterpretation, or an inferred stage without an explicit legal adoption path.
8. Model the `high` and `critical` terminal floors, every residual-delivery and non-delivery choice, every high-or-critical dismissal re-check, and every selected-option scope route. No unresolved critical may reach delivery under either floor.
9. Prove every selected-option transition and algebraic bound, including reserve and clean-suffix foreclosure for A, the inherited plan controller, obligation ownership and blind campaigns for B, or fixed stages and mandatory acceptance blind closure for C.
10. Carry a traceability matrix for every valid verdict in `docs/plans/agent-scaffold.reviews/q86-synthesis-r1-triage.md` through `q86-synthesis-r5-triage.md`. Every valid finding must be marked applicable and closed by a named executable assertion, or inapplicable with a cited architecture-specific reason. Planning and documentation findings must point to their corrected durable text rather than being silently omitted.
11. Include mutation controls that remove each load-bearing transition or predicate and demonstrate that the proof fails.
12. State the exact finite-domain assumptions, the composition or induction argument for arbitrary finite data, the commands, the expected output, and the limitations that remain outside the model.

### Failure path

If the selected architecture cannot satisfy every applicable triage verdict, cannot establish its stated bound, or admits a delivery path that violates the selected safety package, the proof of concept fails. Implementation remains blocked. The planner records the new evidence, Q-86 returns to the human, and the human may revise the selected architecture, choose another architecture and commission its own proof of concept, or abandon the redesign. No fallback architecture or terminal floor is selected automatically, and a failed proof never grants production authority.

## Selected serious terminal floor

Q-91 records the three options `high`, `critical`, and `defer`. The recommendation and human choice are both `high`.

At selected floor `high`, ordinary residual acceptance and ordinary narrowing are unavailable while a high or critical is open. The retained Q-78 triages show that this restriction would apply on passes three through six. At comparison floor `critical`, an open critical blocks those choices while a high may reach a receipted residual-risk or narrowing choice.

`high` is selected under Make illegal states unrepresentable because an unresolved serious finding has no ordinary delivery state, and Safe on existing projects because the stricter boundary fails closed on adoption. Its cost under Ground decisions in evidence and Minimal by default is that Q-78 supplies only descriptive, not prospective, evidence for the stricter boundary, which removes residual-acceptance and narrowing choices on passes three through six.

The selected Option B proof must model both floor values so the safety difference remains executable. Only `high` is selected.

## Migration and documentation impact after proof

Only after the selected proof of concept passes may the implementation plan schedule changes to `.agents/workflow.toml`, `pack/workflow.toml`, `WorkflowSpec`, shared `ReviewProcess` reconstruction, metrics, plan state, ledger projection, `validate --workflow`, `next`, pack guidance, prompts, templates, generated copies, README, and changelog. Historical records remain append-only and receive explicit legacy treatment rather than inferred structure.

The Q-90 closure correction changes planning and prototype-status records only. It makes no shipped product documentation stale because no workflow behaviour changes.

## YAGNI boundary

- Do not complete production-ready controller proofs for all three architectures before the human selects one.
- Do not build a general issue tracker, project-wide defect database, mutable rubric editor, or autonomous obligation extractor.
- Do not build an autonomous risk, scope, severity, material-delta, or residual-risk judge.
- Do not build probabilistic stopping, dynamic pricing, transferable credits, a reviewer marketplace, or a model optimiser.
- Do not infer historical finding lineage, obligation membership, scope digest, stage, or closure.
- Do not build a persistent workflow service, general workflow language, or new scheduler beyond the planned typed fleet.
- Do not create authority from rename, rebuild, replan, narrowing, scope change, or human resume.
- Do not implement selected Option B, floor `high`, or any controller constant before the selected proof gate passes and the human separately authorises production implementation.

## Decisions and authority

Q-86 records the exact architecture options `A - Sealed phase budget`, `B - Frozen obligations with sealed phase campaigns`, and `C - Fixed-depth verification protocol`, with recommendation and chosen value Option B. Q-91 records the exact floor options `high`, `critical`, and `defer`, with recommendation and chosen value `high`.

Both receipts use `task:"bounded-convergence-option-b-proof"`. The decisions authorise only that proof-of-concept unit. They do not authorise production implementation.
