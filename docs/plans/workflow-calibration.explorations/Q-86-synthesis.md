# Q-86 synthesis: bounded convergence options

## Status and decision boundary

Q-86 is ready for a human decision. This synthesis reconciles `Q-86-state-machine.md` and `Q-86-safety-process.md`. It changes no workflow rule, cap, reset behaviour, status outside Q-86, metric, specification, pack file, prompt, template, README, changelog, or Rust source.

The exact later decision is to choose one bounded architecture from this set:

- `A - Sealed phase budget`.
- `B - Frozen obligations with a sealed derived budget`.
- `C - Fixed-depth verification protocol`.

The recommendation is `B - Frozen obligations with a sealed derived budget`. The current mechanism is comparison evidence and is not an option. No mechanism has been chosen, Q-85 authorised only this design pass, and implementation remains blocked until the human decides Q-86 and the decision is folded into `workflow-calibration` with a receipt.

## Evidence that constrains the decision

### Corrected Q-78 acceptance history

The brief's selector is authoritative and has grown. Run:

```sh
jq -s 'map(select(.type == "round" and .task == "q78-design-pass" and .phase == "acceptance")) | {passes: length, valid_shortfalls: map(.valid_findings)}' docs/metrics/workflow.jsonl
```

It now returns ten passes and `[7,10,5,6,5,5,4,2,1,0]`. The observed sequence closed on pass ten. It is evidence of a costly sequence with late serious findings and eventual decay, not evidence that this particular run diverged.

The baseline remains non-admissible because the rule, rather than this run, has reachable unbounded paths. For every positive integer `n`, five `new_valid` rounds followed by human `resume` can repeat `n` times and leave the loop active after `5n` rounds. For every positive integer `n`, an acceptance pass with a valid shortfall can route through repair to another acceptance pass and leave the campaign active after `n` passes. Convergence-first precedence closes neither construction. Both explorer state-machine checks reproduce these cycles. The baseline therefore has no finite bound or exact forced terminal event and cannot be chosen.

### Evidence limitations that every option must respect

- Nineteen logged rounds have `outcome: "clean"` while `valid_findings` is greater than zero, and all nineteen advance `consecutive_clean`. Raw `outcome` and its derived streak are not safe load-bearing inputs until repaired or replaced by triage-backed finding dispositions.
- Severity instrumentation is not trustworthy enough for a severity-trajectory gate. Only six of the ten Q-78 triage files remain, so the recorded decay across passes seven to ten depends on the log's severity arrays without retained adjudication files.
- Historical findings have no stable cross-review identity. The current records cannot mechanically distinguish `pre-existing`, `fix-induced`, `scope-expanded`, and `relitigated` findings or estimate marginal unique reviewer yield.
- The log contains one round with a `critical` finding and one `dismissal_recheck` record. That re-check was overturned. Critical legality and re-check behaviour are therefore safety design requirements with sparse empirical support, not calibrated rates.
- Q-78 used two model and harness paths, but blindness, model, harness, lens, and brief differed together. The local and external blind-versus-informed evidence cannot isolate a causal advantage for blindness.
- The external experiment covers one artefact, one model family, one session, and three reviews. Its blind review found six defects present during an informed review, but blindness was confounded with prompt breadth. It supports distinct blind discovery and informed verification seats, not a population estimate.
- `validate --workflow` can validate structured claims but cannot prove that an external agent performed an independent or genuinely blind review. Mechanical enforcement must state that limit.
- The Q-78 acceptance target grew during the sequence. The association between those folds and later findings does not prove that scope movement caused the findings.

Reproduce the broken stopping signal and sparse safety record with:

```sh
jq -s 'map(select(.type == "round" and .outcome == "clean" and .valid_findings > 0)) | {rounds: length, streaks_advanced: (map(select(.consecutive_clean > 0)) | length)}' docs/metrics/workflow.jsonl
jq -s '{critical_rounds: (map(select(.type == "round" and ((.severities // []) | index("critical")))) | length), dismissal_rechecks: (map(select(.type == "dismissal_recheck")) | length), results: map(select(.type == "dismissal_recheck") | .result)}' docs/metrics/workflow.jsonl
```

The design brief is `docs/plans/workflow-calibration.explorations/Q-86-convergence-mechanism-brief.md`. The formal state and reproduction scripts are in `Q-86-state-machine.md`. The process, evidence audit, and obligation proof are in `Q-86-safety-process.md`. The sequential and censoring inputs are `calibration-analysis.md` and `2026-08-13-audit-when-the-loop-turned.md` in the same directory. External design inputs are <https://kevinmahoney.co.uk/articles/ai-review-loops/>, <https://gist.github.com/KMahoney/3098f0f12638d0a83a5ef3b91bef601d>, and <https://lobste.rs/s/52povq/ai_review_loops_don_t_always_stabilise>.

## Shared safety package

The human decision is about architecture, not a matrix of avoidable safety toggles. Every viable option includes this package.

### Identity, scope, and lineage

- Authority belongs to an immutable `TaskFamilyId`, typed phase and loop identities, and ordered review batch identities. A rename, rebuild, new display name, human resume, or unchanged replan cannot create fresh authority.
- The acceptance rubric freezes after plan review and before implementation. Its structured source cites the plan's Success Criteria, numbered Project Principles, explicit invariants, security and trust boundaries, documentation-currency duties, exclusions, reviewed baseline, and step documentation-impact obligations. The rendered plan remains a projection.
- A finding is in scope when it demonstrates a violation of a frozen obligation, invariant, boundary, or duty. A genuinely optional new capability or preference is `ScopeExpanded` and is backlogged without enlarging the current family. Uncertainty stays in scope or goes to the human.
- A triager, never the orchestrator, rules on scope. An out-of-scope ruling at `high` or `critical` requires the same independent re-check as a dismissal. A `critical` finding is always in scope.
- Prospective finding state separates `Origin`, `ScopeRelation`, `Continuity`, and `Severity`. It supports `PreExisting`, `FixInduced`, `OriginIndeterminate`, `ScopeExpanded`, `DuplicateOf`, `Relitigated`, and `Reopened` without deriving lineage from severity.
- One stable `FindingId` survives reviewer reports, triage, repairs, re-checks, later review, and acceptance. Duplicate reports keep their report identities but join one finding. Relitigation without materially new evidence does not reopen it. New evidence adds an evidence identity and reopens the same finding root.
- Historical records are not rewritten and historical provenance is not invented. A digest-pinned adoption boundary separates legacy evidence from prospective structured state.

### Serious findings and terminal choices

The first implementation uses `high` as the conservative serious terminal floor. This packages the safety proposal's local Q-78 control rather than asking the human to decide a second policy toggle. An open `high` or `critical`, or a pending high-or-critical dismissal re-check, prevents completion and prevents ordinary residual-risk acceptance.

At exhaustion the human sees all five named choices through the human-input contract. Their legal effects are fixed:

- `Accept residual risk` is legal only below the serious floor. It ends the current family and requires a decision receipt plus a record-backed accepted-at-escalation waiver naming every accepted finding.
- `Narrow scope` ends the current family and never replenishes it. With an open serious finding, ordinary narrowing is illegal. Removal of the affected output from delivery is legal only as a terminal `RemovedFromDelivery` disposition with an exact exclusion and no delivery of that output.
- `Revert` is legal only to a named known-good artefact. It ends the family and records each affected finding as `RevertedWithArtifact`.
- `Replan` ends the family, preserves every unresolved finding as `CarriedToSuccessor`, and keeps release blocked. A successor needs a new human receipt and a strictly narrower or disjoint obligation set. It is not a resume transition.
- `Abandon` ends the family, ships nothing, and preserves every unresolved finding and its evidence.

Backstop re-checks never debit a review budget. Each possible finding-bearing batch has one mandatory independent re-check call that can adjudicate all high-or-critical dismissals from that batch. The call is structurally available even at exhaustion, so the budget cannot ration the safety check.

### Reviewer allocation

Blind and informed briefs remain distinct. A blind reviewer receives the frozen artefact and rubric without prior findings, repair claims, or change lists. An informed reviewer receives named finding identities, repair claims, affected regions, and prior evidence. Every option reserves blind artefact-wide closure evidence and uses informed seats for named repair verification. Different models or harnesses remain preferred where available, but genuine blindness and independence are advisory properties that the tool cannot prove.

## Option A - Sealed phase budget

### State, allocation, and stopping bound

Option A reconciles the two proposals' sealed-budget mechanisms. A non-resettable `TaskBudget` is declared in two irreversible steps. Task opening authorises the plan slice. Plan convergence freezes the rubric, the finite number `m` of work-loop identities, one work slice for each identity, and the acceptance slice. Authority is partitioned and cannot transfer between phases.

Each of the `m + 2` slices has five normal review batches and two red-reserve batches. A triager-valid `high` or `critical` sets monotone `serious_seen` and unlocks that slice's two already-declared reserve batches. Unlocking does not restore spent authority. Every executed batch has exactly two reviewer seats, at most one triage call, and at most one mandatory batched re-check call. A slice has at most six repair calls, and a repair is legal only when an authorised review batch remains to verify it.

The first batch uses a broad blind seat and a rubric-focused seat without finding history. Later batches use one blind seat and one informed verification seat. Plan and work completion retain the declared one-clean or two-clean requirement, but cleanliness is reconstructed from triage-backed finding dispositions rather than trusting the broken historical `outcome` field. Acceptance completes on a settled pass after all prior in-scope findings are settled and all Roadmap steps are complete. Foreclosure fires when fewer batches remain than the required clean streak. Completion wins on the final authorised batch.

The finite task bound is at most `7(m + 2)` review batches, `14(m + 2)` reviewer passes, `7(m + 2)` triage calls, `7(m + 2)` backstop calls, and `6(m + 2)` repair calls. The resulting automated-agent bound is `34(m + 2)`. Resume reconstructs spent state. No transition decrements, resets, transfers, or appends authority.

### Trade-offs against all eight Project Principles

| Project Principle | Option A trade-off. |
| --- | --- |
| Prefer the cleaner long-term architecture over the smallest diff | A single task budget unifies plan, work, and acceptance spend while preserving typed phase processes. It is cleaner than resettable windows, but it still layers a numeric ceiling over a clean-streak predicate. |
| Minimal by default | Fixed five-plus-two slices and two seats avoid dynamic pricing and probability. The account schema is larger than a cap patch and repeats one slice per work identity. |
| Safe on existing projects | Prospective adoption and a digest-pinned boundary preserve history. An active legacy task that has already spent its slice must terminally escalate rather than receive a fresh window. |
| Idempotent | Ordered replay yields the same spend and duplicate event identities fail. Resume is reconstruction rather than mutation. |
| Make illegal states unrepresentable | Disjoint active, foreclosed, terminal, and serious-blocked variants remove reset and post-terminal action edges. Acceptance single passes still remain distinct from convergence windows. |
| Ground decisions in evidence | Five normal batches preserve the current boundary and two reserve batches protect serious late discovery. The architecture is supported, but the five-plus-two values are not calibrated by more than one project. |
| Reproducible | The arithmetic and state replay are deterministic, and exhaustive enumeration proved termination by seven batches per phase without critical completion. |
| Structured data first, project for humans | Typed identities, declarations, spend, findings, and receipts are authoritative. Ledger prose and human output are projections. |

### Migration and enforcement surface

`pack/workflow.toml`, `.agents/workflow.toml`, and `WorkflowSpec` gain normal and reserve batch counts, reviewer seats, repair legality, and the serious floor. The shared `ReviewProcess` reconstruction gains task and phase accounts, an `AcceptanceCampaign`, finding state, and terminal variants while retaining disjoint `Convergence` and `SinglePass` observations. The plan TOML and template gain family, attempt, scope, loop, budget, and adoption declarations. Metrics gain prospective budget, spend, finding, evidence, disposition, scope-freeze, and terminal-decision events. `validate --workflow` enforces identity joins, monotone spend, phase isolation, reserve eligibility, repair-before-verification ordering, terminality, and serious-finding legality. `next` reports balances and emits no action after foreclosure or exhaustion.

Canonical guidance and generated copies must move together through `pack/AGENTS.md`, `pack/instrument.md`, the planner, orchestrator, reviewer, triager, and implementer prompts, the ledger and plan templates, `AGENTS.md`, `.agents/AGENTS.reference.md`, `.agents/prompts/`, `.agents/LEDGER.template.md`, `.agents/workflow.toml`, `README.md`, and `CHANGELOG.md`. Existing append-only events remain unchanged. Reviewer diversity, lineage quality, and actual blindness remain advisory. State, spend, joins, the serious floor, and terminal legality are mechanical.

### Confidence and reversal evidence

Confidence is medium in the architecture and low in the five-plus-two values. Prefer another option if prospective lineage shows that reserve batches mostly produce relitigation or optional scope expansion, if fixed slices terminally reject important repairs at a material rate, if active-task adoption cannot prevent authority laundering, or if the account model cannot compose cleanly with the scheduled typed review fleet. Better post-boundary probes could change the values without overturning the architecture.

### YAGNI boundary

Do not build transferable credits, dynamic pricing, per-token accounting, a reviewer marketplace, probabilistic stopping, automatic budget replenishment, or more than two reviewer seats per batch. Build only immutable identities, fixed accounts, prospective findings, deterministic reconstruction, terminal receipts, validation, `next`, and required documentation migration.

## Option B - Frozen obligations with a sealed derived budget

### State, allocation, and stopping bound

Option B reconciles the proposals' recommendations rather than choosing one concern and discarding the other. It adopts the state-machine proposal's sealed non-resettable authority envelope and the safety proposal's frozen-obligation completion predicate. This is not a cosmetic budget variant. Option A stops on a triage-backed clean streak under fixed phase slices. Option B stops on closure of a finite obligation set and derives its post-freeze ceiling from that set.

Plan review has the same sealed maximum of seven batches needed to reach a frozen rubric. Plan convergence freezes a finite structured obligation set `O`. For the first implementation each obligation has its initial closure attempt and at most one prospective reopen, so `r = 1`. Every post-freeze review batch must settle one active obligation attempt, consume that obligation's one reopen after materially new evidence, or execute the one reserved blind closure batch. A batch that cannot make one of those typed transitions goes to the terminal decision rather than authoring more review.

The post-freeze ceiling is `C_O = |O| * (r + 1) + 1`, which is `2|O| + 1` with the packaged first-version value. It is partitioned at freeze across declared work loops and acceptance, with no transfer and no later increase. The whole task therefore has at most `7 + C_O`, or `2|O| + 8`, review batches. With exactly two reviewer seats and at most one triage, one mandatory batched re-check, and one repair per non-final batch, automated calls are bounded by `5(7 + C_O) - 1`. Any exhausted sub-account reaches the terminal decision even when another sub-account has unused authority.

Each obligation has a closed disposition. Completion requires every obligation to be `Met` or validly `AcceptedResidual`, no open in-scope finding, no open serious finding, no pending re-check, one reserved blind artefact-wide closure pass, and completion of every Roadmap step. A scope-expanded low is backlogged and does not enlarge `O`. A finding against a closed obligation can use its one reopen. A serious finding that cannot attach safely to a frozen obligation enters `SeriousBlocked` rather than minting a new obligation or new authority.

Reviewer allocation uses two blind or rubric-focused seats for initial discovery, informed seats after named repairs, and two seats including at least one blind reviewer for the reserved closure batch. The structured brief records blind or informed intent, while guidance admits that the tool cannot verify the information barrier.

### Trade-offs against all eight Project Principles

| Project Principle | Option B trade-off. |
| --- | --- |
| Prefer the cleaner long-term architecture over the smallest diff | One finite obligation model explains scope, completion, reopen, and the derived ceiling. It addresses the moving target measured in Q-78, but introduces a larger plan schema. |
| Minimal by default | It reuses existing plan sources and adds one reopen allowance rather than a general tracker. It is the least minimal option because every acceptance obligation must be enumerated and maintained. |
| Safe on existing projects | Historical findings remain untouched and active legacy work adopts at a digest boundary. An incomplete frozen set is a new safety risk, so uncertain or serious uncited defects fail closed to the human. |
| Idempotent | Obligation dispositions, reopen use, and spend reconstruct deterministically. Repeating resume or rendering cannot create an obligation or restore an allowance. |
| Make illegal states unrepresentable | A closed enum prevents completion with an open obligation, a second reopen, an open serious finding, or a pending re-check. The sealed ceiling prevents malformed obligation progress from creating an unbounded campaign. |
| Ground decisions in evidence | It directly addresses the four observed Q-78 scope folds and avoids the broken `outcome` predicate. The evidence is still one task, and `r = 1` is a conservative first value rather than a measured optimum. |
| Reproducible | The bound is derived from committed `O` and a fixed `r`. The safety proposal exhaustively checked the obligation controller, while the sealed outer ceiling supplies a direct finite fallback. |
| Structured data first, project for humans | Obligation identities and dispositions become structured plan state projected for readers. This is the strongest fit, at the cost of more authoring discipline. |

### Migration and enforcement surface

All common identity, finding, terminal, history, guidance, README, changelog, and generated-copy migrations named for Option A still apply. `WorkflowSpec` adds the plan-review ceiling, reopen allowance, closure-seat rule, serious floor, and no-transfer rule rather than fixed work and acceptance slices. `ReviewProcess` gains `FrozenObligationCampaign` and typed obligation attempts. The plan schema and template gain obligation rows with stable ids, source references, phase ownership, disposition, and reopen state. Metrics gain exact obligation joins and disposition events. The ledger points to structured obligation state and does not become its source.

`validate --workflow` mechanically enforces a finite frozen set, exact source and phase joins, at most one reopen, monotone phase spend, the reserved blind-brief record, no scope mutation, no completion with open obligations or findings, and no action after terminal state. `next` reports open obligations, remaining attempts, phase balances, and the permitted blind or informed brief. It cannot prove obligation completeness or reviewer blindness, so the planner, reviewer, and triager prompts must state those advisory duties and fail uncertain scope to the human.

### Confidence and reversal evidence

Confidence is medium in the architecture and low in the initial one-reopen value. The recommendation is overturned if a proof of concept cannot make obligations precise without duplicating the whole plan, if frozen-rubric tasks still need long review sequences without scope movement, if valid in-scope defects routinely cannot cite a frozen obligation, if obligation sets are systematically incomplete, if any serious finding is routed to backlog, or if the obligation joins make the typed fleet materially less coherent than sealed phase accounts. Evidence that one reopen is too strict changes the constant only if a new finite value is declared prospectively and cannot replenish live work.

### YAGNI boundary

Do not build a general issue tracker, autonomous obligation extractor, theorem prover for scope, project-wide defect database, priority or assignment workflow, historical lineage rewrite, or mutable rubric editor. The first version stores only finite obligation ids, source references, dispositions, one reopen bit, phase ownership, the sealed ceiling, findings, receipts, validation, `next`, and documentation changes.

## Option C - Fixed-depth verification protocol

### State, allocation, and stopping bound

Option C replaces fungible credits and clean streaks with a forward-only phase graph. Each plan review, declared work loop, and acceptance campaign has its own `Discovery`, `Verify1`, `Verify2`, and `BlindClosure` nodes. No node can be revisited and no phase can inherit another phase's unused stage.

`Discovery` uses two blind reviewer seats. A settled low-risk result completes because the discovery itself is blind. A settled risky result advances to `BlindClosure`. A valid in-scope finding permits `Repair1` and one informed `Verify1` seat. A finding at `Verify1` permits `Repair2` and one informed `Verify2` seat. A settled verification advances to one blind closure seat. A finding at `Verify2` or `BlindClosure` enters the terminal decision, or `SeriousBlocked` when it is high or critical. The closure node never authors another automatic repair.

For each of `m + 2` phases, the exact maximum is four review batches, five reviewer passes, four triage calls, four mandatory batched re-check calls, and two repair calls. The task bound is `4(m + 2)` batches and `15(m + 2)` automated calls. Resume reconstructs the current node. A replan terminates the family. No transition points backwards.

A settled result is derived from finding dispositions, not raw `outcome`. It may include a duplicate without new evidence or a triaged scope-expanded low, but never an unresolved in-scope defect. The blind closure requirement and serious terminal floor use the shared safety package.

### Trade-offs against all eight Project Principles

| Project Principle | Option C trade-off. |
| --- | --- |
| Prefer the cleaner long-term architecture over the smallest diff | The graph is the smallest formal proof and makes blind closure structural. It replaces current streak semantics and may terminally reject a useful third repair despite unused project capacity. |
| Minimal by default | Four named nodes and two repairs form a small closed protocol. Prospective scope and finding state are still required. |
| Safe on existing projects | New tasks are clear. Historical adoption is hardest because old records do not establish whether a reviewer was blind, informed, or at a particular verification generation. |
| Idempotent | Every node is single-use, ordered replay returns the same node, and duplicate events fail. |
| Make illegal states unrepresentable | Backward edges, a third automatic repair, closure bypass for risky work, post-terminal action, and serious completion do not exist in the graph. |
| Ground decisions in evidence | Separate blind and informed nodes fit the external anchoring observation. The exact depth of two repairs is a conservative design choice, and Q-78 would have escalated on pass three before its later decay. |
| Reproducible | Exhaustive enumeration proved every path terminal by batch four with no critical completion. The topology has less arithmetic than either budget option. |
| Structured data first, project for humans | Stage, brief kind, finding state, and terminal state are structured and projected. Fewer numeric fields are needed, but stage migration needs explicit adoption data. |

### Migration and enforcement surface

The common surfaces still move. `WorkflowSpec` gains a protocol version, two-repair maximum, risky closure requirement, serious floor, and permitted graph. `ReviewProcess` gains the four forward-only phase-controller variants around disjoint `Convergence` and `SinglePass` observations. Plan and template state gain immutable identities, scope references, phase protocol declarations, current stage, and adoption metadata. Metrics gain stage-entry, stage-completion, reviewer-brief, finding, and terminal events rather than budget-spend events.

`validate --workflow` enforces exact ids, forward-only movement, at most two repairs, valid blind or informed brief types, risky closure, finding dispositions, mandatory re-checks, terminality, and serious legality. `next` emits only the actor and brief allowed at the current node. Active legacy work needs a human-reviewed adoption receipt at a stage no earlier than its evidenced repair history. If the stage cannot be established, adoption fails closed to the terminal decision.

### Confidence and reversal evidence

Confidence is high in the finite-state proof and low to medium in operational adequacy. Prefer another option if prospective runs show that a third bounded repair often resolves serious defects without churn, if terminal escalations become common at `Verify2` or closure, if stage adoption loses too much existing work, or if blind closure adds little unique valid yield. Prefer this option over the others if it catches the same medium-or-worse defects with materially fewer calls and fewer ambiguous states.

### YAGNI boundary

Do not build an extensible workflow language, adaptive stage insertion, dynamic repair depth, stage transfer, reviewer optimiser, or historical stage inference. Build only the four nodes, fixed seats, prospective findings and briefs, terminal receipts, validation, `next`, and documentation migration.

## Red-control comparison

| Required path | A - Sealed phase budget | B - Frozen obligations with a sealed derived budget | C - Fixed-depth verification protocol |
| --- | --- | --- | --- |
| Repeated human resume | Resume reconstructs spend. Every phase terminates by batch seven. | Resume reconstructs obligation and spend state. The task terminates by `2|O| + 8` batches. | Resume reconstructs one forward-only node. Every phase terminates by batch four. |
| Unbounded acceptance repair | Acceptance has five normal and at most two serious-reserve batches. The final finding goes to the terminal decision. | Every pass settles an attempt, consumes the one reopen, or uses blind closure. Post-freeze work ends by `2|O| + 1` batches. | A finding at `Verify2` or closure is terminal. Acceptance has at most four batches and two repairs. |
| Fix-induced high near exhaustion | It unlocks any unspent declared reserve and consumes a batch. Exhaustion enters `SeriousBlocked` without reset. | It consumes the parent's one reopen if available. Otherwise it enters `SeriousBlocked` without enlarging `O`. | It can use the next fixed repair only before `Verify2`. At `Verify2` or closure it enters `SeriousBlocked`. |
| Scope-expanded low | It is backlogged after triage, consumes its opened batch, and does not unlock reserve or enlarge scope. | It is backlogged, consumes its opened batch, and cannot add an obligation or reopen allowance. | It is settled for stage movement, consumes the stage, and cannot add a node. |
| Relitigation without new evidence | It preserves the finding disposition, consumes the opened batch, and cannot reset spend or streak. | It cannot reopen an obligation, consumes the opened batch, and cannot change `O` or the bound. | It preserves the disposition, consumes the stage, and cannot point backwards. |
| Narrowing or replan | The family becomes terminal and no slice is restored. A successor needs a new receipt and materially different scope. | The family becomes terminal with open findings carried. Strictly narrower or disjoint successor scope cannot mutate `O`. | The family becomes terminal and no stage is restored. A successor begins at its own discovery only after a new receipt. |
| Unresolved critical at exhaustion | `SeriousBlocked` makes complete, residual acceptance, and ordinary narrowing illegal. Re-check remains available outside the review debit. | The same block applies. A critical cannot be backlogged or used to mint an obligation. | The same block applies at any stage, including discovery and blind closure. |
| Blind closure | Every batch includes a blind seat, including the final authorised batch. | One final blind artefact-wide batch is reserved inside `C_O`. | `BlindClosure` is a required node for risky work and follows every settled repair path. |

All three mechanisms pass the brief's finite-bound or exact-terminal-event proof and every red control when implemented with the shared safety package. Their stopping observations remain censored because no mechanism can observe a review it does not run.

## Excluded candidates

- The current baseline is excluded because repeated resume and later acceptance repair each contain a reachable cycle.
- A severity-decay gate is excluded from the current decision set. Its bounded version needs a non-resettable ceiling and an explicit open-finding conjunct, but it makes severity instrumentation load-bearing when that instrumentation is incomplete and the sample is sparse. It can return only after the outcome and severity records are repaired and prospective evidence supports a threshold and window.
- A probabilistic or survival-threshold gate is excluded because the sample and lineage data cannot support a safe stopping probability. Sequential and survival analysis remains useful for later calibration, not as the first enforcement mechanism.
- A pure frozen-obligation rule without a sealed ceiling is excluded. Option B includes the ceiling so malformed or stalled obligation progress cannot recreate an unbounded path.

## Recommendation

Choose `B - Frozen obligations with a sealed derived budget`.

The plain reason is that the two explorers identified different necessary layers. The state-machine proposal is right that authority must be sealed, typed, monotone, and non-resettable. The safety proposal is right that the local sequence grew a moving acceptance target and that the current `outcome` and severity fields are unsafe stopping inputs. Option B uses frozen obligations to define what done means and a sealed derived budget to force a terminal event when obligation progress stalls. It therefore addresses both the observed scope problem and the formal unbounded-path problem.

The recommendation is judged mainly against Prefer the cleaner long-term architecture over the smallest diff, Make illegal states unrepresentable, Ground decisions in evidence, and Structured data first, project for humans. Its real cost is against Minimal by default and Safe on existing projects because obligation authoring and migration are larger than a counter or fixed graph. Confidence is medium in the architecture and low in `r = 1`. A focused schema and reconstruction proof of concept must validate that obligations remain finite, precise, and non-duplicative before implementation proceeds. If that proof fails, choose `A - Sealed phase budget` rather than weakening the obligation invariant.

## Exact human decision and no-decision boundary

The orchestrator must ask: "Which bounded convergence architecture should Q-86 fold into `workflow-calibration`: `A - Sealed phase budget`, `B - Frozen obligations with a sealed derived budget`, or `C - Fixed-depth verification protocol`?"

The presentation must state the trade-offs above, recommend Option B, state the medium architecture confidence and low confidence in the first reopen value, and state that Option B's main unresolved design risk is whether a finite obligation schema can be precise and complete without duplicating the plan or filtering genuine defects.

Until the human chooses, Q-86 remains `open` and implementation is blocked. The choice does not author code by itself. It authorises a later planner fold that must sequence the chosen mechanism after the shared typed review reconstruction, include the instrumentation and documentation migrations, record the decision receipt, and review the resulting plan before implementation. The baseline, the excluded severity gate, the five-plus-two values of Option A, and the one-reopen value of Option B are not silently approved by Q-85 or by this synthesis.
