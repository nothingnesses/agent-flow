### `bounded-convergence-option-b-proof`: prove selected Option B before any bounded-convergence implementation

Q-86 selected `B - Frozen obligations with sealed phase campaigns` from the exact three architecture options recorded in its decision receipt. Q-91 selected terminal floor `high` from `high`, `critical`, and `defer`. These decisions authorise this proof of concept and nothing more. They do not authorise workflow behaviour, controller code, pack changes, production documentation, or any production implementation unit.

This step is the blocking specification test promised by Q-88, Q-89, and Q-90. The retained `q86-controller-proof.py` and `q86-q78-scope-replay.sh` scripts remain adversarial prototypes and evidence of missing obligations. They are not extended into production code and their zero counters, finite retained-map cap, and conditional Q-78 replay are not proof inputs.

### Sequence, dependencies, and authority

The structured sequencing rule is that this step is the next bounded-convergence build after the `workflow-calibration` decision fold and no bounded-convergence production unit may precede it. Its unique Roadmap order is placed after the pre-existing maximum so no existing Roadmap row moves and no historical position citation changes. Its `blocked_by` list remains empty because every input needed for the proof is already durable in Q-86, Q-88, Q-89, Q-90, Q-91, the narrowed synthesis, and the five retained synthesis triages; there is no unfulfilled proof dependency to add. It must not wait for `review-loop-foreclosure-enforcement`, the typed driver fleet, or any production controller substrate because the proof is an isolated executable specification, not implementation.

The one declared increment is `bounded-convergence-option-b-proof-inc1`, classified `risky`. An unsound proof could authorise a widely used stopping and delivery mechanism, so the increment requires two consecutive clean review rounds. Completion of this increment is the gate. Every later production implementation unit for bounded convergence must declare `blocked_by = ["bounded-convergence-option-b-proof"]`. No such production unit is authored by this fold.

### Proof artefacts and boundary

The increment creates only planning and proof artefacts under `docs/plans/workflow-calibration.proofs/`:

- `q86-option-b-spec.md` is the mathematical and typed-state specification, finite-domain statement, composition or induction argument, algebraic derivation, limitations, and terminal-choice table.
- `q86-option-b-proof.py` is the executable reference model and property oracle. It uses no production controller module and writes no live plan, log, ledger, workflow spec, pack, or generated product documentation.
- `q86-option-b-mutations.py` imports the reference model and applies the named mutation manifest. It fails if a load-bearing transition or predicate has no mutation, if a mutation is not exercised, or if any mutation survives.
- `q86-option-b-traceability.md` maps every source-derived, round-qualified valid T-id from `agent-scaffold.reviews/q86-synthesis-r1-triage.md` through `q86-synthesis-r5-triage.md` to a named executable assertion, a corrected durable planning statement, or a cited Option-B-specific inapplicability reason.
- `q86-option-b-traceability.py` parses all five retained triages, derives each valid T-id from its finding heading and verdict record, and then checks the matrix. It rejects a missing, duplicate, malformed, or unparsed triage; any difference between the derived source set and the matrix rows; any duplicate row or count mismatch; any overlap, omission, or disagreement in the matrix's applicable and Option-B-inapplicable disposition sets; an unresolved named assertion or durable-text pointer; and any applicable verdict left open. A hard-coded expected T-id set or count is not a substitute for parsing and deriving the source set.
- `fixtures/` contains only synthetic prospective fixtures for arbitrary finite batches, obligation freezes, phase campaigns, legacy adoption, successor registries, receipts, and terminal choices. Historical Q-78 data may appear only as explicitly descriptive or counterfactual evidence and cannot satisfy a safety assertion.

The proof may use the Python standard library and repository-local proof data. It must not add a runtime dependency, alter the metrics schema, rewrite append-only history, infer historical finding lineage, or import production workflow reconstruction. The reference model is disposable after it has served as an independently reviewed specification.

### Selected state and typed authority

The executable entry state fixes `Architecture = FrozenObligationsWithSealedPhaseCampaigns` and records `selected_floor = high`. A comparison-only invocation models `critical`, but no command, fixture, or receipt may silently change the selected floor. Reconstruction of the same ordered events yields the same selected architecture, floor, family, authority, findings, and terminal state.

The state model is a closed sum of these stages:

1. `SealedPlanReview` owns one immutable plan-review campaign. It models five normal review batches, two reserve batches unlocked only by a triage-valid high or critical or an overturned high-or-critical dismissal, the declared one- or two-clean suffix, clean-suffix foreclosure, repairs, verification, independent dismissal re-checks, and terminal exhaustion. An upheld dismissal preserves the incoming clean streak and does not unlock reserve authority. Resume reconstructs the account and never replenishes it.
2. `FreezePending` can be entered only by a converged sealed plan review. It deterministically extracts a finite canonical obligation set `O`, a finite ordered set of `m` work-loop identities, acceptance, exact post-freeze phase ownership for every obligation, a frozen exclusion set, and their canonical digests.
3. `FrozenFamily` holds one immutable family id, the freeze digest, `O`, exact owners, the ordered post-freeze phase registry, all finding and evidence history, phase accounts, predecessor spend, and the append-only global family and receipt registry. Every finding records distinct `DiscoveryPhase` and `CanonicalOwnerPhase` values and a typed owner route derived from them.
4. `PhaseCampaign(q)` owns exactly `O_q`. Every obligation has one initial attempt and verification plus at most one reopen attempt and verification on materially fresh evidence. Every phase has one non-transferable blind-closure batch. An atomic batch may retain findings for several owners, but initial-attempt credit is awarded only to the one scheduled owner; no batch transfers authority or advances another owner's attempt.
5. `TerminalChoice` represents exhaustion, an unowned finding, a finding discovered after its canonical owner's campaign completed, material scope change, serious blockage, legacy adoption refusal, revert, replan, narrowing, residual-risk request, abandonment, and non-delivery outcomes without fabricating completion.
6. `Complete` is constructible only after every frozen obligation is examined and has a permitted terminal disposition, every live in-scope or carried finding is resolved or has a permitted non-delivery disposition, no prior-owner or future-owner route remains live, exact owner campaigns and blind closure are complete, every serious dismissal re-check is settled, and the selected floor permits delivery.

Illegal stage products are unconstructible. In particular, a legacy task cannot construct `FrozenFamily`, a terminal predecessor cannot regain active authority, a post-freeze phase cannot change its owner set, and no delivery variant carries an unresolved critical under either floor.

### Frozen obligations and phase ownership

`O` is a canonical finite set of rows extracted only from closed structured sources fixed by the converged plan review. Each row contains stable `ObligationId`, source kind, exact source locator, source digest, normative text digest, exact post-freeze phase owner, and disposition state. The accepted source kinds are finite structured Success Criteria, Project Principles, and documentation-impact duties. Any selected invariant, boundary, trust duty, or exclusion needed for in-scope routing must first become one of those structured rows during sealed plan review. Free-form prose does not silently add an obligation at freeze.

The freeze fails rather than guessing when a source is missing, duplicated, unstable, unparseable, or ownerless. A later genuine violation with no canonical owner becomes `UnownedInScopeFinding`, blocks ordinary completion, and routes to a terminal human choice. It is never backlogged merely because `O` omitted it. Exact ownership is non-transferable and the sum of all `O_q` equals `O` with no duplicate or absent row.

The proof keeps two ownership axes distinct. `CanonicalOwnerPhase` is the exact post-freeze phase `q` assigned by the obligation row. Within `PhaseCampaign(q)`, each `ObligationId` in `O_q` is a schedulable owner key for initial-attempt accounting, and `ScheduledOwner` is the one such key named by the current initial-review batch. Thus `n_q` counts schedulable obligation owners inside one canonical phase; a batch cannot turn findings for other keys or phases into their initial-attempt credit.

All obligations receive their initial authority before any closed obligation spends reopen authority. Each initial-review batch names exactly one scheduled owner. The batch may retain cross-owner findings atomically, but only that scheduled owner receives initial-attempt credit; every other untested owner remains `Untested` until its own scheduled batch. An incidental finding against a closed current-phase owner is retained immediately as a live deferred reopen, but its reopen work waits until every obligation in that phase has received its scheduled initial attempt.

### Discovery phase and canonical-owner routing

The frozen phase registry gives every post-freeze phase a stable identity and total order. Every finding separately records the phase whose batch discovered it and the exact phase that canonically owns its obligation. The reducer derives, rather than accepts, one of these routes from those two fields and the current campaign:

- `CurrentOwner` retains the finding in the current campaign. The scheduled owner alone receives initial-attempt credit; another current-phase owner remains uncredited until its scheduled batch, or remains a deferred reopen when it had already closed.
- `CompletedPriorOwner` retains the live finding under its canonical owner after that owner's campaign has completed. The completed campaign stays immutable: authority is not transferred to the discovery phase, reopened, or replenished. This route immediately blocks delivery and permits only a terminal non-delivery choice or a receipted replan whose successor carries the finding.
- `FutureOwnerPending` retains the live finding without spending or advancing the future campaign. It stays live across intervening campaigns and activates only when its canonical owner's campaign is scheduled; that owner must still take its own initial-attempt batch.
- `UnownedInScopeFinding` has no fabricated owner and follows its existing terminal human-choice route.

Acceptance is a phase in the same frozen order. A finding discovered during acceptance for a completed work owner therefore takes `CompletedPriorOwner`, not acceptance authority. A finding discovered in an early work phase for a later work or acceptance owner takes `FutureOwnerPending`. Resume reconstructs the same route from immutable phase identities and cannot reclassify, drop, transfer, or replenish it.

### Arbitrary finite findings and mixed products

One atomic triaged batch is an arbitrary finite map from optional owner ids to finite finding maps, plus a finite unowned set. Every finding retains stable `FindingId`, root and optional parent ids, severity from the full `low`, `medium`, `high`, `critical` scale, scope relation, triage disposition, evidence identity, reviewer attribution, predecessor lineage, carried status, `DiscoveryPhase`, `CanonicalOwnerPhase`, and its derived owner route.

The executable proof must not bound persistent retained history. It establishes arbitrary finite handling through a documented quotient and composition or induction argument whose extension relation preserves fresh discovery, reopen, scope, re-check, and delivery transitions after any settled history. A finite interaction sweep is supporting evidence only. The oracle must include settled history followed by fresh valid, serious-dismissal, and scope batches.

Named product fixtures cover at least these cases in every authority state where they are legal:

- findings for several owners in one batch, findings for one owner, and mixed owned plus unowned findings; zero-, one-, and multiple-owner batches prove that only the scheduled owner receives initial-attempt credit
- acceptance discovery for a completed work owner, early-work discovery for a future owner, and an atomic mix of current-, completed-prior-, future-, and unowned routes
- low plus critical, high plus critical, parent plus fix-induced child, and duplicate reports that retain attribution without duplicating identity
- valid plus high-or-critical dismissal in one batch
- scope referral plus dismissal referral, two simultaneous scope referrals, and high plus critical scope outcomes
- joint repair and verification of an exact selected finding set, with partial verification leaving every unselected identity live
- settled history followed by a fresh finding, fresh scope referral, or fresh serious dismissal

Every re-check reducer acts on one stable finding id and never bulk-rewrites unrelated entries. A critical scope result remains delivery-blocking while any attached scope or dismissal re-check settles. No later repair, verification, or upheld dismissal may clear that block accidentally.

### Serious carry, global family identity, and fresh evidence

A terminal replan or material scope change makes the predecessor immutable. A successor requires a human decision receipt that binds the exact predecessor id, globally fresh successor id, exact predecessor and successor digests, complete carried finding map, predecessor spend, presented options, and chosen successor. The global append-only registry rejects predecessor, ancestor, sibling, and unrelated existing-id reuse, rejects a second chosen successor for one predecessor, and reconstructs exact ancestry without omitted links.

Every carried finding enters the successor as a live component. A carried high or critical remains a delivery blocker according to the selected floor until named repair and verification or a terminal non-delivery disposition. Successor authority does not erase or reset predecessor spend, evidence, findings, or receipt history.

A reopen requires a globally fresh `EvidenceId` attached to an exact settled root. The old evidence and root remain in history. Same-evidence relitigation is rejected and consumes no reopen authority. Fresh evidence reopens only the named roots and cannot bulk-reopen or erase siblings.

### Legacy adoption

The proof models prospective and legacy entry separately. `LegacyNoRubric` has no `O`, owner map, phase, stage credit, or prospective authority. It can terminate under a pinned legacy disposition or obtain a human adoption receipt that starts a new sealed plan review and prospective freeze. It cannot enter a post-freeze campaign directly, reinterpret missing obligations as `O = {}`, infer a stage from historical role labels, or use historical clean rounds as closure credit.

Mutation and fixture controls reject direct legacy-to-campaign entry, zero-obligation reinterpretation, inferred stage, historical authority, and a successor receipt presented as an adoption receipt.

### Terminal floors and choices

Both floors are executable and the selected `high` floor is the default proof entry.

At floor `high`, an unresolved high or critical makes ordinary residual acceptance and ordinary narrowing unavailable. Repair and verification, a successor that carries the live blocker, revert, abandonment, and explicit non-delivery remain representable. None grants delivery authority.

At floor `critical`, an unresolved critical has the same restriction. An unresolved high may reach a receipted residual-risk or narrowing terminal choice, but only that comparison model exposes those edges. It does not change the selected `high` state.

Under either floor, an unresolved critical can never deliver. A high-or-critical dismissal always waits for an independent re-check. Exhaustion cannot itself change finding disposition. Replan, rebuild, rename, narrowing, or human resume cannot replenish authority. Every accept-residual, narrow, revert, replan, abandon, and continue-to-repair choice has a distinct durable state and receipt requirement.

### Algebraic proof obligations

Let `n_q = |O_q|`, `|O| = sum(n_q)`, `m` be the frozen work-loop count, and `r_plan` be one clean batch for low-risk sealed plan review or two for risky sealed plan review.

The proof derives rather than repeats these selected Option B bounds:

```text
L_q = n_q + 1
C_q = 4n_q + 1
L_B = r_plan + |O| + m + 1
R_B = 4|O| + m + 8
I_B = 18|O| + 4m + 38
```

`L_q` and `C_q` apply only to post-freeze phase `q`. Sealed plan review has its separate seven-batch maximum. `L_q = n_q + 1` is preserved because each of the `n_q` obligation-owner keys must receive its own scheduled initial-attempt batch and no cross-owner observation awards extra initial credit; blind closure contributes the final batch. The discovery/owner routing adds no review authority: a completed-prior-owner route terminates delivery, while a future-owner finding remains live and is handled inside that future owner's already-counted campaign. The whole-family formulas therefore still follow from one sealed plan-review campaign, exactly `m + 1` post-freeze phases, exact ownership, and no transfer. The automated-agent maximum must be independently derived from typed reviewer, triage, re-check, repair, and proof-step costs. Hard-coding the published formula without deriving every coefficient is a proof failure.

The proof checks zero and one obligation, empty and non-empty owners, zero-, one-, and multiple-owner atomic batches, scheduled-owner-only initial credit, each out-of-phase owner route, early terminal paths, maximum-spend paths, and symbolic sums for arbitrary finite `O`. It distinguishes a safe upper bound from an observed finite-sweep maximum. A mutation that grants initial credit to a non-scheduled owner must falsify `L_q`; a mutation that transfers, replenishes, drops, or activates out-of-phase authority must falsify the phase or delivery oracle. If the transition model does not establish any published coefficient or premise, the published bound is withdrawn and the step fails.

### Retained-triage traceability gate

The checker must parse each of the five retained triages section by section, pair every `### T<n>` heading with that section's verdict record, and derive the valid identities as round-qualified keys. A malformed, absent, duplicate, or unconsumed T section fails closed. The matrix must then cover that derived set exactly. A row marked executable must name a property and at least one mutation that kills it. A row marked durable-text must cite the corrected planning source. A row marked Option-B-inapplicable must give an architecture-specific reason and identify any shared invariant that remains executable. Executable plus durable-text rows form the applicable disposition set; Option-B-inapplicable rows form the inapplicable set. Those sets must be disjoint, their union and row count must equal the source-derived identities, and any matrix summary of their sets or counts must equal the parser's computed values. No hard-coded expected identity list or count may replace this derivation, and no row may cite a prototype zero counter as closure.

The matrix must close the B controller, bounds, conditional-replay boundary, terminal-floor receipt, allocation, finite source, legacy state, simultaneous findings, reserve and clean-streak inheritance, successor contract, minimum cost, unverified delivery, unowned findings, phase-to-family algebra, full severity scale, cross-owner batches, carried finding and spend preservation, scope policy, clean-suffix foreclosure, reproducible commands, family freshness, mixed dispositions, initial priority, integrated scope routes, persistent arbitrary history, scope-route identity, serious carry, scope and dismissal products, global registry, and fresh evidence findings. A- or C-specific proof claims may be Option-B-inapplicable only where the row cites the exact selected-B boundary and preserves any shared serious-delivery, blind-closure, floor, or reproducibility invariant.

The planning and documentation rows are closed only by their durable sources. This fold makes Q-86 decided, records Q-91, updates the Success Criteria, synthesis, design brief, proposal status boundaries, and historical Q-88 to Q-90 wording, and leaves the orchestrator-owned ledger to its already-current resume anchor. Retained prototype replay and stale-count findings remain historical limitations and cannot become selected-proof premises.

### Mutation controls

Every load-bearing transition and predicate is tagged in the reference model and appears in a manifest. The mutation runner must remove, invert, weaken, or misbind each tag one at a time and show that a named oracle fails. The mandatory mutation classes include persistent-history discovery, finite-map reduction, cross-owner atomicity, scheduled-owner-only initial credit, discovery-phase/canonical-owner-phase misbinding, acceptance-to-completed-work current-authority fabrication, completed-prior-owner transfer, replenishment or delivery, early-work-to-future-owner activation or loss, mixed out-of-phase component erasure or bulk rerouting, unowned blocking, parent-child lineage, mixed valid and dismissed products, per-id scope reduction, integrated scope routing, serious carry, global family freshness, one-successor authority, exact receipt binding, fresh evidence identity, legacy gating, untested-obligation completion, initial-before-reopen priority, no phase transfer, blind closure, reserve unlock, clean-streak preservation, clean-suffix foreclosure, high-floor residual restriction, critical delivery prohibition, traceability-source parsing and disposition partitioning, and algebraic coefficient derivation.

A mutation manifest entry without an exercised test fails. A load-bearing tag without a mutation fails. Any surviving mutation fails. Mutation controls may operate on an imported in-memory model or a temporary copy, never on the live planning tree.

### Exact commands and expected contract

Run these commands from the repository root. They use no machine-specific scratch path.

```sh
PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3 docs/plans/workflow-calibration.proofs/q86-option-b-proof.py --suite all --floor high
PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3 docs/plans/workflow-calibration.proofs/q86-option-b-proof.py --suite all --floor critical
PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3 docs/plans/workflow-calibration.proofs/q86-option-b-proof.py --suite algebra --floor high
PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3 docs/plans/workflow-calibration.proofs/q86-option-b-traceability.py docs/plans/workflow-calibration.proofs/q86-option-b-traceability.md docs/plans/agent-scaffold.reviews/q86-synthesis-r1-triage.md docs/plans/agent-scaffold.reviews/q86-synthesis-r2-triage.md docs/plans/agent-scaffold.reviews/q86-synthesis-r3-triage.md docs/plans/agent-scaffold.reviews/q86-synthesis-r4-triage.md docs/plans/agent-scaffold.reviews/q86-synthesis-r5-triage.md
PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3 docs/plans/workflow-calibration.proofs/q86-option-b-mutations.py --all
```

Each command exits non-zero on any unmet property. The two all-suite runs identify Option B, distinguish `selected_floor=high` from `comparison_floor=critical`, and report zero safety, transition, authority, delivery, legacy, identity, evidence, product, and bound failures. The algebra run prints the five formulas above from the model and reports every premise checked. The traceability command reports its parser-derived `valid_findings=51` and `unresolved=0`; changing a retained verdict, omitting a triage input, or adding, deleting, duplicating, or changing a matrix row or disposition must change or fail the derived comparison rather than pass against an embedded expected set. The mutation command reports `survived=0`, with the discovered tag and mutation counts equal.

Run two passes over the five exact commands from the repository root. Before each individual invocation, create a fresh temporary state directory outside the repository and point its temporary/cache environment there; do not change the working directory. Capture that invocation's semantic summary in its temporary state, compare it with the corresponding command's other pass, and remove both states after the comparison. Before the first invocation, capture both `git status --porcelain=v1 --untracked-files=all` and a path/type/content manifest of the complete working tree, including ignored paths but excluding Git's administrative path. Assert both snapshots are byte-identical after the tenth invocation, so no tracked, untracked, or ignored repository artefact is created, removed, or changed.

The implementation review also runs the ordinary repository gates over only the changed proof and planning files. The orchestrator owns rendering the generated plan and final integration gates. The proof scripts must not modify a tracked or untracked repository file when any command runs.

### Acceptance

1. Q-86 and Q-91 remain exact receipted decisions folded into this step. The selected state is Option B with floor `high`, while `critical` is comparison-only and both floors pass the complete model.
2. The sealed plan-review model proves reserve unlock, streak preservation, clean-suffix foreclosure, reconstruction without replenishment, high-or-critical dismissal re-checks, all terminal paths, and the separate seven-batch maximum.
3. The freeze deterministically produces finite `O`, exact source locators and digests, exact non-transferable phase ownership, finite work-loop identities, acceptance, and exclusions. Missing, duplicate, unstable, unowned, or free-form-only rows fail closed.
4. The post-freeze model represents every selected Option B state and legal transition, distinct discovery and canonical-owner phases, current-, completed-prior-, future-, and unowned routes, all scheduled initial attempts before reopen spend, one fresh-evidence reopen per obligation, grouped repair and exact verification, one blind closure per phase, unowned and completed-prior-owner delivery blocks, and completion over obligations plus the complete finding map. A completed prior campaign neither transfers nor regains authority, and a future-owner finding stays live until that owner's campaign.
5. The arbitrary-finite argument does not cap persistent history. Executable interaction controls and the composition or induction proof cover fresh events after settled history, acceptance-to-completed-work, early-work-to-future-owner, mixed current/out-of-phase products, cross-owner and mixed dispositions, parent-child lineage, per-id re-checks, and partial verification.
6. Successor tests enforce immutable predecessors, global family uniqueness, one authorised successor, exact ancestry and receipt binding, predecessor spend, and complete carried findings. Carried serious findings stay live and block delivery.
7. Fresh-evidence tests retain old evidence and exact roots, reject same-evidence relitigation, and prevent sibling erasure or bulk reopen.
8. Legacy tests admit no inferred authority, zero-obligation reinterpretation, historical closure credit, or direct campaign entry. Only a pinned terminal legacy disposition or a receipted new sealed plan review is legal.
9. Floor tests exercise every terminal choice at `high` and `critical`. No unresolved critical delivers under either floor, and no unresolved high reaches residual acceptance or ordinary narrowing under selected floor `high`.
10. The algebra command derives `L_q`, `C_q`, `L_B`, `R_B`, and `I_B` from typed costs and exact ownership. Zero, one, and arbitrary finite obligation cases, including atomic multiple-owner batches, satisfy the formulas without treating a finite sweep as the proof. Cross-owner findings are retained, but only the scheduled owner receives initial-attempt credit, preserving `L_q = n_q + 1`; out-of-phase routing grants no additional authority, so the remaining bounds are either re-derived unchanged or withdrawn.
11. The traceability command parses all five retained triages and derives their round-qualified valid T-ids before reading the matrix. It rejects every row-set, row-count, applicable/inapplicable disposition-set, or summary mismatch; resolves every applicable row; and supplies specific reasons for every Option-B-inapplicable row. No hard-coded expected set or count can satisfy this criterion.
12. The mutation manifest covers every load-bearing tag and every mandatory mutation class, including scheduled-owner-only credit and all three owned phase routes. Every mutation is exercised and killed.
13. From the repository root, all five exact commands pass twice, each invocation using a fresh external temporary state directory, and produce identical semantic summaries. The working directory never changes to a bare temporary directory. Both the repository status and complete non-Git path/type/content manifests are identical before and after all ten invocations, proving that no tracked, untracked, or ignored repository artefact was created, removed, or changed.
14. The proof step converges as `risky` work with two consecutive clean review rounds. Reviewers inspect the mathematical argument, executable model, traceability, mutation adequacy, and planning-only boundary rather than trusting green output.
15. No production file, workflow rule, controller, pack source, generated pack copy, README, changelog, metrics schema, live ledger state, or append-only historical event changes in this proof unit.

### Failure and return to the human

Any unresolved applicable triage verdict, surviving mutation, unproved transition, invalid floor path, unsafe delivery path, unmodelled legacy, successor, or out-of-phase owner state, non-finite authority premise, or failed algebraic coefficient makes the proof fail. The step remains incomplete and every production implementation remains blocked.

The planner records the new evidence against Q-86 and returns the architecture decision to the human through the human-input contract. The human may revise Option B and commission a new proof identity, choose A or C and commission that option's own proof, or abandon the redesign. No fallback architecture, terminal floor, bound, controller constant, production step, or implementation authority is selected automatically.

### Documentation impact

This step changes planning and proof records only. It makes no shipped product documentation stale because it changes no behaviour. A successful proof permits a later planner, after a separate human-authorised implementation decision, to turn the synthesis inventory into production steps for `.agents/workflow.toml`, `pack/workflow.toml`, `WorkflowSpec`, review reconstruction, metrics, plan state, ledger projection, validation, `next`, pack guidance, prompts, templates, generated copies, README, and changelog. Those production steps do not exist yet and must all be blocked by this proof step.
