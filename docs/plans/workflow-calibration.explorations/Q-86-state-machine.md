# Q-86 bounded convergence by state and lineage

## Prototype status after the capped synthesis review

Q-88 supersedes this proposal's proof-before-choice boundary. The architecture descriptions and algebraic bounds remain design inputs, but the executable checker is an adversarial prototype rather than a recommendation-eligibility proof. Every later statement that calls the checker corrected or exhaustive, reports zero violations, or treats a graph run as establishing a safety property records the prototype's historical self-assessment and is not a current assurance claim. The round-5 triage at `docs/plans/agent-scaffold.reviews/q86-synthesis-r5-triage.md` demonstrates unsound arbitrary-finite composition, cross-family serious carry, scope and dismissal products, global family identity, and fresh-evidence handling. A complete executable proof is required only if the human later selects the corresponding architecture, and it must close every applicable Q-86 triage finding before implementation.

## Question and decision boundary

Q-86 asks how to bound repeated review, repair, acceptance, and human-resume cycles without hiding an unresolved critical finding. Q-85 authorised this design pass only. It did not authorise a mechanism. This proposal changes no workflow rule, constant, plan status, log record, prompt, pack file, generated copy, or Rust source.

The current mechanism is comparison evidence only. It is not an admissible option. This proposal compares two bounded candidates:

1. Candidate A is a non-resettable task budget with phase slices and a severity reserve.
2. Candidate B is a fixed-depth discovery, repair, verification, and blind-closure protocol.

The recommendation is Candidate A. The later human decision remains required.

## Evidence, separated from recommendation

### Local evidence

The current rules in `AGENTS.md` give plan and work review a five-round per-artefact window. A human resume resets both counters. Acceptance is one reviewers-then-triager pass, but a valid shortfall causes a repair and a later acceptance pass with no task-level cap. `.agents/workflow.toml` calls the five-round cap advisory. `docs/plans/agent-scaffold.steps/review-loop-foreclosure-enforcement.md` schedules enforcement of exact phase-bearing convergence windows. `docs/plans/agent-scaffold.steps/workflow-driver-typed-fleet.md` schedules disjoint `Convergence` and `SinglePass` process types.

The Q-78 selector in the brief has grown since the brief recorded six passes. On this tree it returns ten passes and the valid-shortfall sequence `[7,10,5,6,5,5,4,2,1,0]`. Maximum severity by pass is `[medium,medium,high,high,high,high,medium,low,low,clean]`. The six retained triages cover passes one through six and adjudicate every reported shortfall in those passes as valid. The records after pass six remain in the append-only metrics log even though their raw triage files are no longer retained in the tree.

The Q-78 sequence is evidence for two different claims. First, acceptance can continue well beyond the five-round convergence constant. Second, severity can decay before a clean pass, but it did not decay monotonically at first. High findings first appeared at pass three and remained through pass six. A severity-only stop before pass ten would either stop with valid findings or require an explicit residual-risk decision.

The retained triages also show why lineage must be prospective and structured. Pass two finding R2-C2 says a pass-one repair removed one bad record but left the reusable cause in shipped guidance. Pass three finding R3-1 establishes a high authority mismatch. Passes four through six find further migration and identity gaps as the design changes. Those observations are consistent with pre-existing defects, fix-induced defects, newly exposed defects, and scope movement. The files carry no stable cross-pass finding identity or required provenance field, so the evidence cannot distinguish those causes mechanically. This proposal does not infer a lineage that the records do not contain.

The calibration analysis treats clean-round evidence as censored by stopping. The later audit corrects one cap analysis, records one medium finding in the twenty-third enforced second round, and finds that changed prose repeatedly re-seeded findings. Both records argue against treating one observed clean pass, one defect count, or one severity count as a defect oracle. The audit also demonstrates that `validate --workflow` can validate hand-written round claims without proving that a review occurred. Mechanical enforcement can validate state consistency, not the truth of an external agent action.

The reviewer attribution data is useful but limited. Across the ten Q-78 acceptance passes, `gpt-5.6-sol` through `pi` has 26 raw and 26 credited-valid reports, while `claude-opus-5` through `claude-code` has 29 raw and 25 credited-valid reports. Per-reviewer credits can double-count one deduplicated finding. There is no stable finding join, so these totals cannot estimate marginal unique yield. They do show that both allocated model and harness paths contributed findings.

### External evidence

The article <https://kevinmahoney.co.uk/articles/ai-review-loops/> reports the linked experiment and cautions that opinion changes, scope creep, and false positives can prevent stabilisation. The detailed write-up at <https://gist.github.com/KMahoney/3098f0f12638d0a83a5ef3b91bef601d> reports 10, 12, and 17 defects over three reviews, with fixes creating defects and expanding public and review surface. Its machine-checkable core algorithm converged while open contract, conformance, and prose obligations did not.

Reviewer framing is load-bearing in that experiment. R1 and R3 received claimed properties or the prior change list. R5 was blind to that history and found six defects already present during R3. The write-up calls anchoring its strongest result. It also states that blindness is confounded with prompt breadth and that the sample is one artefact, one model family, one session, and three reviews. This supports reserving blind discovery separately from informed fix verification. It does not support a population rate.

The discussion at <https://lobste.rs/s/52povq/ai_review_loops_don_t_always_stabilise> supplies two bounded observations. An approval request to make a document better had no named defect and could be repeated indefinitely. Other comments identify the vague request for perfect code as an important confound. These observations support a frozen rubric and named defects. They do not prove that every review loop diverges.

### Recommendation derived from the evidence

The evidence supports a deterministic outer bound, a frozen acceptance rubric, prospective finding lineage, separate blind and informed seats, and an explicit critical-finding block. It does not support a probabilistic defect threshold, a severity-only declaration of cleanliness, or a measured optimum for the numeric budget. Candidate A is preferred because it keeps useful late discovery available through a small serious-finding reserve and makes every additional agent action spend a non-resettable typed seat. Candidate B is viable but reaches a terminal human decision much earlier on the local replay.

## Non-admissible baseline: resettable five-round windows and uncapped acceptance

### State and counterexamples

The convergence state is approximately `Active(loop_key, rounds_in_window, clean_streak)`. At round five, an unconverged loop enters `AwaitingHuman`. The current resume transition is `AwaitingHuman -> Active(loop_key, 0, 0)`. For any positive integer `n`, choose `new_valid` for five rounds and `resume` at each escalation. The process performs `5n` review rounds and remains active. Because `n` is arbitrary, no finite review bound exists.

Acceptance is approximately `AcceptancePass -> Repair -> AcceptancePass` whenever triage confirms a valid shortfall. For any positive integer `n`, choose one valid shortfall on each pass. The process performs `n` acceptance passes and remains active. The current Q-78 history supplies ten concrete passes, but the proof does not depend on ten.

Convergence-first precedence at the fifth round does not repair either counterexample. It closes only a path whose final round earns the required streak. The counterexample chooses `new_valid` every time. The baseline therefore receives no stopping proof and is not recommendation-eligible.

### Baseline against all eight Project Principles

| Project Principle | Assessment. |
| --- | --- |
| Prefer the cleaner long-term architecture over the smallest diff | The local counter is simple, but reset creates a second meaning for the same cap and leaves acceptance outside the architecture. |
| Minimal by default | The small rule is operationally expensive because it can author unlimited review, repair, and decision traffic. |
| Safe on existing projects | Human escalation is safe in isolation, but an unlimited default can consume cost indefinitely and can still end through an under-specified residual-risk choice. |
| Idempotent | Replaying one window is deterministic, but `resume` creates fresh authority from the same task state, so repeated application is not state-idempotent. |
| Make illegal states unrepresentable | An arbitrarily large number of spent rounds remains representable as an active task. Acceptance has no bounded campaign state. |
| Ground decisions in evidence | The cap is advisory and the reset is not justified by evidence that another identical window changes the process. |
| Reproducible | The counterexamples reproduce exactly. The mechanism fails the property they reproduce. |
| Structured data first, project for humans | Per-window counters discard task-level spend, while acceptance campaign state exists only as an inferred sequence of records. |

## Shared formal domain for both bounded candidates

### Typed identities

Display names never carry authority. The structured source defines these identities:

```text
TaskFamilyId
TaskAttemptId(TaskFamilyId, attempt_number)
ScopeId(TaskFamilyId, rubric_digest)
LoopId = PlanReview(TaskFamilyId)
       | WorkReview(TaskFamilyId, StepId, IncrementId)
       | AcceptanceCampaign(TaskFamilyId, ScopeId)
ArtifactVersionId(LoopId, TaskAttemptId, commit_or_content_digest)
ReviewBatchId(LoopId, one_based_index)
ReviewerPassId(ReviewBatchId, seat_index)
RepairId(LoopId, one_based_index)
ReportId(ReviewerPassId, local_report_index)
FindingId(TaskFamilyId, minted_sequence)
EvidenceId(FindingId, minted_sequence)
```

A rename changes display text only. A rebuild creates a new `TaskAttemptId` and `ArtifactVersionId` inside the same family. Neither creates a loop, budget, stage, or finding identity. A replan with unchanged obligations remains in the same exhausted `TaskFamilyId`. A terminal human decision can instead create a materially differently scoped successor family. The predecessor family remains terminal and its spent state is never copied as unspent state. Each successor id must be fresh against the predecessor id and its ordered ancestry registry. The successor ancestry is exactly that registry followed by the predecessor id, so same-family and ancestor reuse cannot mint authority.

### Frozen rubric and scope firewall

The rubric freezes when plan review completes and before implementation starts. During plan review, each immutable plan artefact version carries a proposed rubric rather than claiming that the rubric is already frozen. Its eventual single structured source is the plan TOML plus referenced Success Criteria, explicit invariants, security and trust boundaries, documentation-currency duty, exclusions, exact reviewed baseline, and the plan principles. The rendered Markdown plan is a projection. `ScopeId` is the digest of the canonical structured form and its referenced content digests.

A finding is in scope when it demonstrates, with reproducible evidence, a violation of a frozen Success Criterion, invariant, security or trust boundary, documentation-currency duty, or project-principle floor on the delivered artefact. A finding is scope-expanded only when the artefact can satisfy every frozen obligation without the proposed new capability, platform, quality threshold, or taste preference. Typed scope relation and scope-recheck state are part of both candidate transition relations, so scope routing is covered by their spend, identity, and delivery predicates rather than checked as a detached policy table. The triager must record the failed entailment, the cited frozen obligations, and the counterfactual compliant artefact. Uncertainty stays in scope or goes to the human. It never defaults to backlog.

A low scope-expanded improvement can become `Backlogged(scope_delta_id)` and does not keep the current task active. A medium scope expansion goes to the terminal human scope decision rather than silently joining the current task or being automatically backlogged. A proposed high or critical out-of-scope ruling first enters `AwaitingScopeRecheck`. An upheld high ruling then goes to the terminal human scope decision, while an overturned high returns in scope. A critical is always safety-blocking, so either critical re-check result enters `SeriousBlocked` and cannot backlog or deliver. A newly discovered violation of an existing obligation remains in scope regardless of when it is found. A security defect created or exposed by the shipped change is in scope even when the exact exploit was not named in the Success Criteria. The firewall therefore cannot relabel an in-scope defect merely by calling it optional.

Any change to frozen obligations, exclusions, or boundaries after freeze ends the current family as `Narrowed` or `Replanned`. A Roadmap edit that only schedules a repair without changing the frozen rubric is not a scope change. `ScopeId` never mutates. New optional work starts only through a separately authorised task family. An identical obligation set, renamed step, rebuild, changed baseline commit, or human resume resolves to the existing family and cannot obtain fresh state. A successor budget requires a human receipt and a materially different obligation or exclusion set, so an artefact rename or rebuild cannot alter a digest merely to launder spend.

### Finding identity, lineage, and severity

Lineage is a product type rather than one overloaded label:

```text
Origin = PreExisting(artifact_version)
       | FixInduced(repair_id, parent_finding_ids)
       | OriginIndeterminate
ScopeRelation = InScope(scope_id)
              | ScopeExpanded(scope_delta_id)
Continuity = New
           | DuplicateOf(finding_id)
           | Relitigated(finding_id)
           | Reopened(finding_id, evidence_id)
Severity = Low | Medium | High | Critical
```

The triager reduces every batch to a finite stable `FindingMap`, not one scalar. Each value records owner, severity, disposition, origin, and optional parent id. The map may hold several findings from one batch, including low plus critical and a parent plus fix-induced child. The triager mints one `FindingId` for each new proposition defined by the violated obligation, affected surface, and falsifying behaviour. Reviewer reports keep their own `ReportId` and point to those findings after deduplication. Duplicate reviewer reports consume the reviewer seats already used but create no extra finding, repair, or severity count. A demonstrably new defect caused by a repair receives a new child id whose parent remains in the map. A defect shown to exist before the repair is `PreExisting` even if detected later.

Relitigation without materially new evidence points to the settled `FindingId` and leaves its disposition unchanged. Materially new evidence creates a new `EvidenceId` and reopens the same finding root. It does not mint a fresh budget or reset a stage. Severity is orthogonal to every lineage axis. A pre-existing critical and a fix-induced critical are equally critical. A scope-expanded low can be backlogged only because of scope relation, not because low severity makes a genuine defect disappear.

The first implementation must permit `OriginIndeterminate`. The current corpus shows that provenance is often not recoverable. A forced confident label would turn missing evidence into false structure.

### Finding dispositions and critical legality

```text
Open
Dismissed
AwaitingDismissalRecheck
ResolvedPendingVerification
Resolved
Backlogged
AcceptedResidual
RemovedFromDelivery
RevertedWithArtifact
CarriedToSuccessor
```

`Complete` is constructible only when every in-scope finding in the complete map is `Resolved`, validly `Dismissed`, or otherwise removed from the delivered artefact, and the phase stopping rule is met. One grouped repair moves the complete selected open set to `ResolvedPendingVerification`. Its named joint verification resolves every selected id, conservatively fails the complete set back to open, or leaves parents open while adding fix-induced children. A partial verification is failure unless every selected finding has named successful evidence. An unrelated later observation, clean streak, budget boundary, child finding, or stage boundary cannot clear a parent. Terminal non-delivery instead records `RemovedFromDelivery`, `RevertedWithArtifact`, `CarriedToSuccessor`, or `UnresolvedAbandoned`. A dismissed high or critical follows `AwaitingDismissalRecheck -> Dismissed` only when the independent re-check upholds dismissal.

At exhaustion the machine enters `AwaitingTerminalDecision` or `CriticalBlocked` and spawns no reviewer or implementer. The human receives accept residual risk, narrow scope, revert, replan, and abandon through the human-input contract. The durable receipt records all options, the recommendation, the chosen option, the exact scope and budget or stage snapshot, and every open `FindingId`.

With no unresolved critical, all five terminal choices are legal. `AcceptedResidual` requires a record-backed waiver tied to the terminal-decision receipt. `Narrowed`, `Reverted`, `Replanned`, and `Abandoned` end the current attempt rather than resume it.

With an unresolved critical, `Complete` and accept residual risk are illegal. Narrow scope is legal only as a terminal declaration that the affected output will not be delivered by the current family, making the finding `RemovedFromDelivery` for that abandoned delivery. Revert is legal only to a named known-good artefact and records `RevertedWithArtifact`. Replan is legal only as terminal `CarriedToSuccessor`, keeps release blocked, and preserves the finding and evidence. Abandon is legal and ships nothing. Any authored removal or new repair occurs in a materially differently scoped successor rather than after the exhausted controller emits another implementer action. A successor may receive new authority only from a new explicit human decision and a changed obligation or exclusion set. Rename, rebuild, narrowing, replan, and resume do not replenish authority in the current family.

### Blind and informed reviewers

A blind reviewer receives the frozen artefact, rubric, and permitted tools, but no prior findings, repair claims, or change list. An informed reviewer receives named `FindingId` values, the repair claims, affected regions, and prior evidence. Blind review is priced as broad discovery. Informed review is priced as fix verification. The two inputs are distinct typed briefs.

Model and harness diversity are preferred when available because shared models and harnesses can share blind spots. The current Q-78 attribution shows useful output from two model and harness paths, but the missing finding join prevents a marginal-yield estimate. No candidate treats diversity as free. Candidate A spends two reviewer seats in every batch. Candidate B reserves two blind seats at discovery, one informed seat at each verification, and one blind seat at closure.

## Candidate A: non-resettable task budget with phase slices and a severity reserve

### Budget declaration and accounting

`TaskBudget` belongs to `TaskFamilyId` and is declared in two irreversible steps. Task opening declares the seven-batch plan slice. Plan convergence freezes `ScopeId`, the finite number `m` of work-loop identities, seven batches for each work loop, and seven acceptance batches. The second declaration occurs once. Later plan edits, scope changes, new artefact versions, attempts, renames, rebuilds, replans, and human decisions cannot append or restore seats in that family.

Each phase slice has five normal review batches and two red-reserve batches. A triage-valid high or critical, or an overturned serious dismissal, sets monotone `serious_seen = true` and unlocks the two reserve batches for that phase. Referral of a dismissal to re-check does not unlock reserve. An upheld dismissal preserves the prior value. Medium and low churn does not unlock reserve. Unlocking does not reset spent state. The reserve gives a risky plan or work loop enough room for two clean verification batches after valid serious evidence at normal batch five. It also gives acceptance one repair verification and one further blind sample if needed.

| Account in each plan, work, or acceptance slice | Initial authority. |
| --- | --- |
| Review batches | Five normal plus two red-reserve batches. |
| Reviewer passes | Fourteen seats, exactly two seats per executed batch. |
| Triage calls | At most seven, one attached to each finding-bearing batch. |
| Backstop re-check calls | At most seven, one independent re-check agent can adjudicate all high or critical dismissals from that batch. |
| Repair passes | At most six, and only when at least one review batch remains to verify the repair. |

The first batch uses one broad blind seat and one rubric-focused seat with no finding history. Every later batch uses one blind seat and one informed fix-verification seat in isolated contexts. A duplicate report still spends its seat. Triage and re-check do not spend reviewer seats, but they spend their own attached seats. A clean batch spends no triage seat. The final batch cannot author an unverified automatic repair. Its valid findings go to the terminal decision.

Acceptance remains a sequence of typed `SinglePassReview` values. A new `AcceptanceCampaign` owns the finite slice and ordered pass identities. `SinglePassReview` still has no risk class, streak, foreclosure, or cap field. This preserves the disjoint process requirement already scheduled in `workflow-driver-typed-fleet` while bounding the sequence around those single passes.

Post-escalation continuation has no special price because it does not exist. Exhaustion or foreclosure enters the terminal-decision state. A human can end the attempt or explicitly author a successor attempt, but cannot reopen the same slice.

### State machine and stopping

```text
TaskOpened
  -> PlanReviewActive
  -> RubricFrozen
  -> WorkReviewActive(loop_1)
  -> ...
  -> WorkReviewActive(loop_m)
  -> AcceptanceCampaignActive
  -> Complete

Any active phase
  -> AwaitingDismissalRecheck
  -> same active phase with spent seats unchanged

Any active phase
  -> Foreclosed
  -> AwaitingTerminalDecision

Any active phase at final authorised batch
  -> Complete when its completion predicate wins
  -> CriticalBlocked when an unresolved critical remains
  -> AwaitingTerminalDecision otherwise
```

Plan and work completion retain the current one-clean or two-consecutive-clean rule by declared risk class. Acceptance requires one pass with no valid in-scope shortfall after triage, every earlier in-scope finding settled, and every Roadmap step complete. Completion wins if it occurs on the final attainable batch. One remaining-clean-suffix calculation runs before every automatic review, repair, and verification. Foreclosure fires before that action when its remaining authorised verification path cannot attain the suffix. A high or critical dismissal blocks until re-check. Re-check preserves the incoming clean streak. An upheld dismissal advances that streak because its batch is clean after adjudication, while an overturned dismissal returns through the valid-finding path and resets the streak. Binary clean remains the release test. Novelty and severity affect routing and reserve access, not whether a genuine unresolved defect is called clean.

The state is `(phase_id, spent, serious_seen, clean_streak, FindingMap)`. A finding-bearing review unions every stable id from the triaged batch into that map. Joint repair moves the complete selected set to pending verification. The next informed verification can resolve the complete set, leave it open, or leave parents open while adding fix-induced children. The reserve and completion predicates universally quantify over the map rather than reading historical outcome or severity arrays. A falling severity trajectory raises confidence but never settles a finding. Stopping still censors what another review might have found.

### Finite bound

There are `m + 2` bounded phases, where `m` is frozen before implementation. Each phase has at most seven review batches. The task therefore has at most `7(m + 2)` review batches, `14(m + 2)` reviewer passes, `7(m + 2)` triage calls, `7(m + 2)` backstop calls, and `6(m + 2)` repair passes. The total number of automated agent invocations is at most `34(m + 2)`. Unused authority is not transferable. Any earlier convergence, foreclosure, or terminal choice reduces the realised total.

This is not another resettable cap. `spent` is monotone under every transition, belongs to immutable `TaskFamilyId` and `LoopId`, and has no decrement or reset transition. `resume` reconstructs the same value. Replan ends the family. A materially differently scoped successor receives authority only through a new human decision receipt and carries unresolved finding roots forward.

### Replay and red controls

| Required path | Exact bounded result. |
| --- | --- |
| Repeated human resume | `resume` is reconstruction only. A terminal state has no edge to an active state. |
| Unbounded acceptance repair | A low or medium only sequence reaches `AwaitingTerminalDecision` at pass five. Any sequence reaches a terminal state by pass seven. |
| Fix-induced high near exhaustion | `LLLLHCC` unlocks the reserve at pass five. Acceptance completes on clean pass six. A risky convergence loop completes on the two-clean streak at pass seven. |
| Upheld high dismissal at batch five | The re-check settles the dismissal but leaves reserve locked unless earlier valid serious evidence already unlocked it. |
| Low plus critical in one batch | Both stable ids remain in the map and the critical blocks delivery regardless of the low disposition. |
| Parent plus fix-induced child | Failed joint verification leaves the parent open and adds the child. Neither identity replaces the other. |
| Scope-expanded low | `O` records backlog and counts as no in-scope valid finding. |
| Scope-expanded medium | It enters the terminal human scope decision. |
| Scope-expanded high | It enters independent scope re-check. Upheld goes to the terminal human scope decision and overturned returns in scope. |
| Scope-expanded critical | It enters independent scope re-check, but either result is `SeriousBlocked` and cannot backlog or deliver. |
| Relitigation without new evidence | `R` preserves the settled finding and counts as no new valid finding. It cannot reset spend. |
| Narrowing or replan | Either choice is a terminal event for the current `TaskFamilyId`. No seat is restored. |
| Unresolved critical at exhaustion | `HLLLLLK` reaches `CriticalBlocked` at pass seven. Complete and accept residual risk are unconstructible. |

On the current Q-78 observation sequence, Candidate A stops at pass seven in `AwaitingTerminalDecision` with that pass carrying medium findings. It does not observe passes eight through ten, which contain three later valid shortfalls, all recorded low. This descriptive replay uses the pass-level adjudication summaries only to compare when a fixed controller would stop. The proposed algebra does not depend on those arrays, while the selected-option safety proof remains owed. On representative convergence histories, A completes `agents-md-drift-guard-inc1` at pass four and the low-risk `checks-runner-worktree-name-collision` plan review at pass four. `optional-modules-inc2cii` reaches pass five with one clean and an unlocked reserve, so one further clean could complete it. The low-only `prompt-drift-guard-inc1` and medium-only `step-intent-encoding-inc1` reach the normal boundary at pass five and terminally escalate rather than opening a new window.

The adversarial prototype explores stable finding maps only within its finite retained-map cap. Earlier exact graph counts in this paragraph became stale as the prototype changed and are deliberately removed. The retained output block in the Reproduction section records one historical run, not a safety proof. Round 5 showed that settled identities consume the global cap and remove later fresh-finding transitions, so the run does not establish arbitrary-finite delivery, critical, bound, dismissal, or foreclosure invariants.

### Candidate A against all eight Project Principles

| Project Principle | Assessment. |
| --- | --- |
| Prefer the cleaner long-term architecture over the smallest diff | One task budget owns plan, work, and acceptance spend while preserving typed per-pass process variants. The schema is larger than a cap patch but removes reset semantics. |
| Minimal by default | The first version uses fixed seats, two reviewer roles, and deterministic thresholds. It avoids probability, dynamic pricing, and a scheduler market. The cost is more structure than the baseline. |
| Safe on existing projects | Prospective adoption and explicit active-task snapshots preserve old append-only history. An adopted over-budget task can terminally escalate immediately, which is disruptive but loud. |
| Idempotent | Reconstructing the same ordered events yields the same spend. Duplicate event ids fail instead of charging twice. Resume has no state mutation. |
| Make illegal states unrepresentable | Phase slices, terminal states, and the critical block are disjoint variants. No reset method exists. Acceptance single passes cannot acquire convergence fields. |
| Ground decisions in evidence | Five normal batches preserve the current measured boundary. Two reserve batches respond only to serious evidence. The numeric defaults remain provisional because one project cannot calibrate an optimum. |
| Reproducible | The arithmetic is deterministic and the adversarial prototype is replayable, but a complete finite oracle remains owed for a selected architecture. |
| Structured data first, project for humans | Immutable ids, budget declarations, scope digests, finding events, and terminal receipts are structured sources. Ledger prose and human output are projections. |

### Candidate A migration and enforcement

`pack/workflow.toml`, the dogfood `.agents/workflow.toml`, and `WorkflowSpec::builtin()` gain normal batch count, red-reserve count, reviewer seats per batch, and repair-seat rules. `WorkflowSpec` parses and checks them once. The generated control fragment projects values into guidance without hand-copied numbers.

The shared `ReviewProcess` reconstruction gains `TaskBudget`, monotone phase accounts, `AcceptanceCampaign`, finding state, and terminal state. Existing `Convergence(LoopWindow)` remains the owner of streak and foreclosure. Existing `SinglePass(SinglePassHistory)` remains the owner of one acceptance or standalone review pass. The campaign composes single passes without adding convergence arithmetic to them. `next` and `validate --workflow` consume this one reconstruction.

The plan TOML schema and `pack/plan-template.plan.toml` gain immutable task-family and attempt ids, one budget declaration, the frozen rubric references, phase loop declarations, adoption metadata, and terminal receipts or references. The plan remains the durable state source. The ledger records a human narrative and resume pointer only. `pack/LEDGER.template.md` and `.agents/LEDGER.template.md` stop telling the orchestrator to count authority from prose and instead point to structured spend.

The metrics schema gains append-only `budget_declared`, `review_spend`, `repair_spend`, `finding`, `finding_evidence`, `finding_disposition`, `scope_frozen`, and `terminal_decision` events, or equivalent typed records with those meanings. A `round` gains exact task, attempt, scope, loop, batch, artefact-version, reviewer-pass, and blind-or-informed identities. Historical records are never rewritten. Pre-adoption rounds reconstruct as historical process variants and cannot satisfy a live budget. An active legacy task needs a digest-pinned adoption record that charges every matched prior action. If prior spend already exhausts a slice, adoption enters the terminal-decision state rather than minting a fresh window.

`validate --workflow` mechanically enforces exact identity joins, one declaration, monotone spend, phase isolation, reserve eligibility, repair-before-verification ordering, finding disposition legality, dismissal re-checks, no action after terminal state, no complete state with an open critical, and append-only adoption boundaries. It cannot prove that a human or model performed the action represented by a record. Help and diagnostics must state that limit.

`next` reports remaining normal and reserve seats, current scope digest, open finding ids, next blind or informed brief, foreclosure, and terminal choices. It never emits a reviewer or implementer action after exhaustion. The human and JSON projections come from the same typed state.

Canonical guidance changes are required in `pack/AGENTS.md`, `pack/instrument.md`, `pack/prompts/orchestrator.md`, `pack/prompts/reviewer.md`, `pack/prompts/triager.md`, and `pack/prompts/implementer.md`. Generated copies move through the normal pack path in `AGENTS.md`, `.agents/AGENTS.reference.md`, `.agents/prompts/`, `.agents/LEDGER.template.md`, and `.agents/workflow.toml`. `README.md` must replace reset arrows and document machine output. `CHANGELOG.md` must record the behavioural break and adoption rule. Resume, pause, compaction, kickoff, and review user prompts need edits only if their thin trigger text becomes false after the canonical guidance changes.

Advisory guidance includes the preference for cross-model and cross-harness diversity, the quality of a lineage explanation, and the human recommendation. Mechanical invariants include identities, spend, frozen scope, stage legality, terminality, and critical-finding legality. The implementation must not claim to enforce reviewer truth or reviewer independence beyond the structured identities it can inspect.

## Candidate B: fixed-depth verification protocol

### Phase-local protocol

Candidate B replaces fungible credits with one fixed graph per plan review, declared work loop, and acceptance campaign. Every phase has the same maximum depth but retains a distinct `LoopId`. No phase can consume or inherit another phase stage.

| Stage | Allocation and transition. |
| --- | --- |
| `Discovery` | Two blind reviewer seats inspect the frozen artefact and rubric. A settled low-risk plan or work observation completes. Every settled acceptance observation and every settled risky plan or work observation goes to `BlindClosure`. Any valid in-scope finding permits `Repair1` and goes to `Verify1`. |
| `Verify1` | One informed reviewer verifies named repairs and affected regions. A settled result goes to `BlindClosure`. Any valid in-scope finding permits `Repair2` and goes to `Verify2`. |
| `Verify2` | One informed reviewer verifies the second repair. A settled result goes to `BlindClosure`. Any valid in-scope finding goes directly to the terminal decision. |
| `BlindClosure` | One blind reviewer with no repair history samples the final artefact. A settled result completes. Any valid in-scope finding goes directly to the terminal decision. |

A finding-bearing stage may invoke one triager. A dismissed high or critical may invoke one independent re-check. `Repair1` and `Repair2` are the only automatic repair states. The closure stage is deliberately terminal on a finding even when an earlier path used fewer repairs. That fixed topology is what distinguishes Candidate B from a token budget.

Acceptance again remains a campaign around typed single passes. The stage belongs to `AcceptanceCampaign`, not to `SinglePassReview`. Plan and work risk class changes only the initial-clean route. A risky phase always receives the independent blind closure sample.

### State machine and stopping

```text
Discovery
  -> Complete for a settled low-risk plan or work phase
  -> BlindClosure for every acceptance phase or a settled risky plan or work phase
  -> Repair1 -> Verify1 for a valid in-scope finding

Verify1
  -> BlindClosure for a settled result
  -> Repair2 -> Verify2 for a valid in-scope finding

Verify2
  -> BlindClosure for a settled result
  -> AwaitingTerminalDecision for a valid noncritical finding
  -> CriticalBlocked for a valid critical finding

BlindClosure
  -> Complete for a settled result
  -> AwaitingTerminalDecision for a valid noncritical finding
  -> CriticalBlocked for a valid critical finding
```

A settled observation means no valid in-scope finding remains after triage. It may include a duplicate without new evidence or a scope-expanded low that was durably backlogged. It never includes a genuine unresolved defect. `Repair1` and `Repair2` jointly retain every selected identity and severity in `ResolvedPendingVerification`. Only named complete-set verification resolves them. A failed verification preserves every parent, and each fix-induced finding receives its own open child identity. Severity determines critical legality and backstop routing. Neither severity decay nor a clean count bypasses the complete map.

The protocol is deterministic. Confidence increases when informed verification reproduces a repair and when blind closure finds no in-scope defect. Stopping still censors any unrun future review. Candidate B accepts that censoring at a predeclared stage instead of estimating a probability from the current small and inconsistent dataset.

### Finite bound

For each of the `m + 2` phases, Candidate B has at most four review batches, five reviewer passes, four triage calls, four backstop calls, and two repair passes. The task has at most `4(m + 2)` review batches and `15(m + 2)` automated agent invocations. Every graph node is visited at most once. Resume reconstructs the current node. No transition points backwards.

### Replay and red controls

| Required path | Exact bounded result. |
| --- | --- |
| Repeated human resume | Terminal nodes have no edge to `Discovery`, `Verify1`, `Verify2`, or `BlindClosure`. |
| Unbounded acceptance repair | A third consecutive finding at `Verify2` enters the terminal decision. Any path is terminal by the fourth review batch. |
| Fix-induced high near exhaustion | `LHCC` uses `Repair1`, sees a high at `Verify1`, uses `Repair2`, verifies clean at `Verify2`, and completes after blind closure at batch four. |
| Scope-expanded low | `O` is backlogged and treated as settled. A low-risk plan or work phase may complete at discovery. Acceptance and risky plan or work still run blind closure. |
| Scope-expanded medium | It enters the terminal human scope decision. |
| Scope-expanded high | It enters independent scope re-check. Upheld goes to the terminal human scope decision and overturned returns in scope. |
| Scope-expanded critical | It enters independent scope re-check, but either result is `SeriousBlocked` and cannot backlog or deliver. |
| Relitigation without new evidence | `R` preserves the prior disposition and is settled. It creates no repair state and no new identity. |
| Narrowing or replan | Either choice is a terminal event for the current task family and preserves the visited stage history. |
| Unresolved critical at exhaustion | `LLK` reaches `CriticalBlocked` at `Verify2`, the third review batch. Accept residual risk and complete are illegal. |

On the Q-78 observation sequence, Candidate B stops at pass three with that pass carrying a high. At floor `high` it reaches `SeriousBlocked`. At floor `critical` it reaches `AwaitingTerminalDecision`, where residual acceptance of the open high is legal. Under both floors it does not observe passes four through ten, which contain 23 later valid shortfalls and include further highs. This descriptive replay is not the safety oracle. On the `agents-md-drift-guard-inc1` sequence it completes after `Verify2` and blind closure at pass four. It terminally escalates the low-risk `checks-runner-worktree-name-collision` plan review at pass three because `Verify2` finds another valid issue. The other selected long histories also stop by pass three or four.

The adversarial prototype exercises both grouped repair generations within its finite retained-map cap. Earlier exact graph counts in this paragraph became stale as the prototype changed and are deliberately removed. The retained output block records one historical run. It does not establish arbitrary-finite delivery, critical, or bound invariants because the round-5 findings identify missing fresh-history and transition products.

### Candidate B against all eight Project Principles

| Project Principle | Assessment. |
| --- | --- |
| Prefer the cleaner long-term architecture over the smallest diff | The stage graph is easier to reason about than fungible credits and makes blind closure structural. It is less adaptable to legitimate late repairs. |
| Minimal by default | Four stages and two repairs are a small closed protocol. The shared finding and scope model remains necessary. |
| Safe on existing projects | Prospective adoption is clear. Mapping an active historical loop to a stage is more disruptive because no reliable record says whether an old pass was discovery, informed verification, or blind closure. |
| Idempotent | Ordered replay returns the same node. Every node is single-use and duplicate event ids fail. |
| Make illegal states unrepresentable | Backward edges, a third repair, and completion with an open critical do not exist in the type graph. |
| Ground decisions in evidence | External anchoring evidence motivates separate blind stages. The exact depth of two repairs is a conservative design choice, not a calibrated optimum. |
| Reproducible | The fixed topology gives a proposed four-batch upper bound, while the adversarial prototype is not a complete transition proof. |
| Structured data first, project for humans | Stage, finding, scope, and terminal data are structured and projected. The stage graph needs fewer arithmetic fields than Candidate A. |

### Candidate B migration and enforcement

`pack/workflow.toml`, `.agents/workflow.toml`, and `WorkflowSpec::builtin()` gain protocol version, maximum two repair generations, the risky blind-closure requirement, and the permitted stage graph. They do not gain task credit arithmetic. The control fragment projects the protocol values.

The shared reconstruction gains phase-local `Discovery`, `Verify1`, `Verify2`, `BlindClosure`, `AwaitingTerminalDecision`, and `CriticalBlocked` variants. `Convergence` and `SinglePass` remain disjoint observations inside those phase controllers. The acceptance controller composes single passes without giving a single pass streak or cap fields. `next` and workflow validation consume the same stage reconstruction.

The plan schema and template gain immutable identities, frozen rubric references, one protocol declaration per phase loop, adoption metadata, and terminal receipts. The ledger remains narrative only and points to the structured stage. Metrics gain the same prospective finding, evidence, disposition, scope, reviewer-brief, and terminal events as Candidate A, plus `stage_entered` and `stage_completed` rather than spend events.

Append-only history is not rewritten. A new task starts at `Discovery`. An active legacy task cannot infer a blind or informed stage from old role labels. A human-reviewed adoption receipt must choose a stage no earlier than the number of already observed repair generations permits. Three or more unresolved finding-bearing historical passes enter the terminal-decision state immediately. Historical typed variants cannot satisfy a live stage.

`validate --workflow` enforces exact ids, forward-only stages, at most two repairs, required blind and informed brief types, no closure bypass for risky phases, finding dispositions, dismissal re-checks, terminality, and critical legality. `next` emits only the actor and brief permitted by the current node. It never recommends a third repair or a new discovery stage after resume.

The canonical and generated documentation surfaces are the same set as Candidate A. The content differs by describing stages rather than balances. Required canonical updates are `pack/AGENTS.md`, `pack/instrument.md`, `pack/LEDGER.template.md`, `pack/prompts/orchestrator.md`, `pack/prompts/reviewer.md`, `pack/prompts/triager.md`, `pack/prompts/implementer.md`, `pack/plan-template.plan.toml`, and `pack/workflow.toml`. Generated copies include `AGENTS.md`, `.agents/AGENTS.reference.md`, `.agents/LEDGER.template.md`, `.agents/prompts/`, `.agents/workflow.toml`, and newly scaffolded plan assets. `README.md` and `CHANGELOG.md` must change with the public workflow contract.

Advisory guidance includes model and harness diversity and the quality of human lineage reasoning. Mechanical enforcement includes exact stages, brief kind, scope digest, forward-only movement, critical legality, and terminal state. As with Candidate A, the tool validates claims recorded in structured events and must not claim that it observed an actual independent review.

## Direct comparison and recommendation

| Property | Candidate A | Candidate B. |
| --- | --- | --- |
| Bound | At most seven batches per phase and `34(m + 2)` automated agent invocations. | At most four batches per phase and `15(m + 2)` automated agent invocations. |
| Response to serious late finding | Unlocks two already-reserved batches without reset. | Permits repair only when the finding occurs before `Verify2` or closure. |
| Blind and informed allocation | One blind and one informed or rubric-focused seat in every batch. | Two blind seats at discovery, informed verification seats, then one blind closure seat. |
| Compatibility with current streak logic | Retains plan and work streaks and wraps acceptance passes in a budgeted campaign. | Replaces streak progression with a stage graph. |
| Q-78 replay | Terminal at pass seven with a medium finding. | Terminal at pass three with a high. It is `SeriousBlocked` at floor `high`, while residual acceptance is available at floor `critical`. |
| Main risk | Numeric seats can become policy knobs and the schema is larger. | Useful late repair is rejected even when unused earlier capacity exists. |

Recommendation: choose Candidate A, with medium confidence in the architecture and low confidence in the initial five-plus-two values. The reason is judged primarily against Prefer the cleaner long-term architecture over the smallest diff, Make illegal states unrepresentable, Ground decisions in evidence, and Structured data first, project for humans. Candidate A unifies task spend without collapsing typed phase semantics, removes every automatic reset, reserves bounded capacity for the serious tail observed in Q-78, and remains mechanically replayable. Candidate B is cleaner in isolation and cheaper, but the local replay shows that it terminally escalates before useful later evidence that Candidate A still admits.

Evidence that would overturn the recommendation includes prospective data showing that Candidate B catches the same medium-or-worse defects with materially fewer agent calls, stable finding lineage showing that Candidate A red-reserve batches mostly produce relitigation or optional scope expansion, a proof that task budget adoption cannot distinguish legitimate new scope from laundering, or an implementation proof that the stage graph composes with the scheduled typed fleet much more safely than budget accounts. Evidence that would change only the numeric values includes calibrated post-boundary probes, consistent per-finding severity data, and measured cost per unique valid finding.

## Later human decision required

The later synthesis should present only viable bounded options. This proposal contributes these two:

1. Choose Candidate A, the non-resettable task budget. Trade-off: it preserves more bounded late discovery and current streak semantics at the cost of a larger structured account model. This proposal recommends it because it best serves Prefer the cleaner long-term architecture over the smallest diff, Make illegal states unrepresentable, Ground decisions in evidence, and Structured data first, project for humans.
2. Choose Candidate B, the fixed-depth protocol. Trade-off: it has the smaller proposed graph and lower fixed maximum cost, but sends more late findings directly to a human terminal choice and replaces streak semantics.

The human must choose after the orchestrator synthesises every independent exploration. The current baseline must remain comparison evidence and must not appear as a viable option. Q-85 must not be treated as approval. A decision receipt must record the full option set, recommendation, chosen option, and principle-grounded reasoning before implementation is planned. Candidate A's five-plus-two values and Candidate B's four-stage and two-repair depth remain unapproved constants.

## YAGNI boundary

The first implementation must not build any of the following:

- A general issue tracker or project-wide defect database.
- An autonomous risk, scope, or residual-risk judge.
- A probabilistic defect oracle, Bayesian stop, capture-recapture estimator, or severity forecast.
- A reviewer marketplace, dynamic pricing system, or optimiser for model and harness selection.
- More than two reviewer seats in one batch for Candidate A, or more than the fixed Candidate B allocation.
- A rewrite, synthetic completion, or inferred provenance for historical findings and round records.
- Cryptographic proof that an external agent really reviewed the artefact.
- A persistent workflow service, general workflow language, or new scheduler beyond the already planned typed fleet.
- Automatic budget replenishment from rename, rebuild, replan, narrowing, or human resume.

The first implementation should build only typed identities, frozen scope, prospective finding lineage, the chosen bounded controller, append-only events, deterministic reconstruction, `validate --workflow` checks, `next` projection, terminal receipts, and the documentation migrations named above.

## Reproduction

The retained adversarial prototype can be run from the repository root and has no dependency on a session-specific scratch directory. The live plan and log were not mutated. Its output is reproducible evidence about that prototype only and is not a complete controller proof.

### Q-78 counts and reviewer attribution

Run from the repository root:

```sh
jq -s 'map(select(.type == "round" and .task == "q78-design-pass" and .phase == "acceptance")) | {passes: length, valid_shortfalls: map(.valid_findings), severity_trajectory: map(.severities)}' docs/metrics/workflow.jsonl

jq -s 'map(select(.type == "round" and .task == "q78-design-pass" and .phase == "acceptance")) as $r | $r | map(.reviewers[]?) | group_by([.model,.harness]) | map({model: .[0].model, harness: .[0].harness, passes: length, raw: (map(.raw_findings) | add), credited_valid: (map(.valid_findings) | add)})' docs/metrics/workflow.jsonl
```

The first command returned ten passes, `[7,10,5,6,5,5,4,2,1,0]`, and the severity arrays reported above. The second returned GPT totals `10,26,26` and Claude totals `10,29,25` for passes, raw reports, and credited-valid reports.

### Representative histories

```sh
jq -s 'map(select(.type == "round" and (.phase == "plan_review" or .phase == "work_review"))) | group_by(.increment // .task) | map({id: (.[0].increment // .[0].task), phase: .[0].phase, risk: .[0].risk_class, outcomes: map(.outcome), severities: map(.severities)}) | map(select(.id == "agents-md-drift-guard-inc1" or .id == "optional-modules-inc2cii" or .id == "prompt-drift-guard-inc1" or .id == "step-intent-encoding-inc1" or .id == "checks-runner-worktree-name-collision"))' docs/metrics/workflow.jsonl
```

### Parametric baseline replay

```sh
for n in 1 2 10 100
do
    awk -v n="$n" 'BEGIN { print "resume_windows=" n, "review_rounds=" 5 * n, "state=active_after_resume" }'
    awk -v n="$n" 'BEGIN { print "acceptance_passes=" n, "repairs=" n, "state=awaiting_later_acceptance" }'
done
```

The values of `n` are demonstrations. The counterexample is unbounded because the construction accepts every positive integer `n`.

### Exhaustive transition checker

The retained checker is the durable adversarial prototype `docs/plans/workflow-calibration.explorations/q86-controller-proof.py`. It models Candidate A as mode A and this proposal's fixed-depth Candidate B as mode C, matching the synthesis label map. It exercises a finite subset of finding, dismissal, scope, terminal, and non-delivery states. Its global retained-map cap and missing products make it incomplete, as the round-5 triage demonstrates. The command remains useful for reproducing the prototype and for mutation-driven development of a selected-option proof.

The cardinality-two graph checks the interactions a singleton cannot expose. For B, every triage-valid batch is an atomic finite map from affected obligation owner to finding submap plus an unowned set. Arbitrary finite maps follow by induction over the product of obligation state and finding state because transitions union fresh ids, advance every affected owner, preserve the bidirectional owner-state invariant, and make delivery a universal conjunction over ids and obligations. Adding an owner component cannot erase another identity, close an unaffected obligation, increase grouped calls, or make delivery easier.

Run:

```sh
CHECKER=docs/plans/workflow-calibration.explorations/q86-controller-proof.py
export PYTHONDONTWRITEBYTECODE=1
nix shell nixpkgs#python3 -c python3 "$CHECKER" --mode A --phase acceptance --risk risky --floor high
nix shell nixpkgs#python3 -c python3 "$CHECKER" --mode A --phase work_review --risk risky --floor high
nix shell nixpkgs#python3 -c python3 "$CHECKER" --mode C --phase acceptance --risk risky --floor high
nix shell nixpkgs#python3 -c python3 "$CHECKER" --mode C --phase acceptance --risk low_risk --floor high
nix shell nixpkgs#python3 -c python3 "$CHECKER" --mode C --phase work_review --risk low_risk --floor high
nix shell nixpkgs#python3 -c python3 "$CHECKER" --mode C --phase work_review --risk risky --floor high
sha256sum "$CHECKER"
```

The outputs are:

```text
A phase=acceptance risk=risky floor=high finding_cap=2 normal=5 reserve=2 required=1 states=1547 edges=1815 terminal=742 acyclic=true min_reviews=1 max_reviews=7 mixed_low_critical=40 parent_child=200 mixed_disposition=48 mixed_upheld=48 mixed_overturned=48 mixed_exhausted=8 mixed_exhaustion_cases=16 scope_routes=8 bad_delivery=0 bad_unverified_delivery=0 bad_critical_clear=0 bad_bound=0 bad_upheld_unlock=0 bad_upheld_streak=0 upheld_prior_streak_complete=0 upheld_batch5_complete=0 bad_mixed_preservation=0 bad_mixed_exhaustion=0 bad_scope_spend=0 bad_scope_identity=0 bad_scope_delivery=0 bad_foreclosure_state=0
A phase=work_review risk=risky floor=high finding_cap=2 normal=5 reserve=2 required=2 states=2351 edges=2756 terminal=1100 acyclic=true min_reviews=2 max_reviews=7 mixed_low_critical=34 parent_child=160 mixed_disposition=48 mixed_upheld=48 mixed_overturned=48 mixed_exhausted=0 mixed_exhaustion_cases=16 scope_routes=8 bad_delivery=0 bad_unverified_delivery=0 bad_critical_clear=0 bad_bound=0 bad_upheld_unlock=0 bad_upheld_streak=0 upheld_prior_streak_complete=43 upheld_batch5_complete=1 bad_mixed_preservation=0 bad_mixed_exhaustion=0 bad_scope_spend=0 bad_scope_identity=0 bad_scope_delivery=0 bad_foreclosure_state=0
C phase=acceptance risk=risky floor=high finding_cap=2 stages=4 repairs=2 states=1365 edges=1528 terminal=825 acyclic=true min_reviews=2 max_reviews=4 mixed_low_critical=16 parent_child=64 mixed_disposition=32 mixed_upheld=32 mixed_overturned=32 mixed_exhausted=16 mixed_exhaustion_cases=8 scope_routes=8 bad_delivery=0 bad_unverified_delivery=0 bad_critical_clear=0 bad_bound=0 bad_mixed_preservation=0 bad_mixed_exhaustion=0 bad_scope_spend=0 bad_scope_identity=0 bad_scope_delivery=0 bad_acceptance_blind_bypass=0
C phase=acceptance risk=low_risk floor=high finding_cap=2 stages=4 repairs=2 states=1365 edges=1528 terminal=825 acyclic=true min_reviews=2 max_reviews=4 mixed_low_critical=16 parent_child=64 mixed_disposition=32 mixed_upheld=32 mixed_overturned=32 mixed_exhausted=16 mixed_exhaustion_cases=8 scope_routes=8 bad_delivery=0 bad_unverified_delivery=0 bad_critical_clear=0 bad_bound=0 bad_mixed_preservation=0 bad_mixed_exhaustion=0 bad_scope_spend=0 bad_scope_identity=0 bad_scope_delivery=0 bad_acceptance_blind_bypass=0
C phase=work_review risk=low_risk floor=high finding_cap=2 stages=4 repairs=2 states=1107 edges=1235 terminal=640 acyclic=true min_reviews=1 max_reviews=4 mixed_low_critical=14 parent_child=64 mixed_disposition=24 mixed_upheld=24 mixed_overturned=24 mixed_exhausted=8 mixed_exhaustion_cases=8 scope_routes=8 bad_delivery=0 bad_unverified_delivery=0 bad_critical_clear=0 bad_bound=0 bad_mixed_preservation=0 bad_mixed_exhaustion=0 bad_scope_spend=0 bad_scope_identity=0 bad_scope_delivery=0 bad_acceptance_blind_bypass=0
C phase=work_review risk=risky floor=high finding_cap=2 stages=4 repairs=2 states=1365 edges=1528 terminal=825 acyclic=true min_reviews=2 max_reviews=4 mixed_low_critical=16 parent_child=64 mixed_disposition=32 mixed_upheld=32 mixed_overturned=32 mixed_exhausted=16 mixed_exhaustion_cases=8 scope_routes=8 bad_delivery=0 bad_unverified_delivery=0 bad_critical_clear=0 bad_bound=0 bad_mixed_preservation=0 bad_mixed_exhaustion=0 bad_scope_spend=0 bad_scope_identity=0 bad_scope_delivery=0 bad_acceptance_blind_bypass=0
```

The same commands with `--floor critical` also report zero for the prototype's implemented counters. Round 5 demonstrated that those counters omit required state products and cross-family behaviour, so zero is not evidence that every required control passed. This historical run used the checker at historical commit `ad989b5f`, whose SHA-256 is `d0dabe6da04fde2009a2baf22d0a3d9fabdfbd6bc96d2859d26043531aff579a`. The current retained file's SHA-256 is `8a349c68dbe18df43d1d60d4110e11b3e216d97cdf4efb9f7e7328693d668175`; its added in-file caveat changes no prototype output and grants no proof authority.
