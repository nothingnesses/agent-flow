### `structured-risk-class-source`: make the plan increment declaration the authoritative review-loop risk-class source

Decision `Q-78-risk-class-source` retired the ledger prose duplicate in favour of structured data. Q-83 now resolves the two structured homes that the earlier decision left ambiguous: the human chose `Make the plan increment authoritative`, over making the first round authoritative or adding an authoritative loop-open event. This is a refinement of the earlier choice, not a restoration of ledger authority.

THE REPRODUCED DEFECT. `[[step.increment]].risk_class` is already required and documented as setting an increment's convergence streak, but `PlanToml::step_views` drops increments, W3 reads the first round's class, and `next` reports no class before round one. A scratch TOML declaring `dangerous-inc1` as `risky` plus one clean round that snapshots `low_risk` currently exits zero from `validate --workflow`; the cheaper one-round bar wins over the declared two-round bar. Before the first round, the same declared increment reaches `next` with `risk_class` and `required_streak` null. Those are the two red cases this step must close.

THE AUTHORITY MODEL. The orchestrator declares `[[step.increment]].risk_class` in the plan at loop open, before spawning the first reviewer. That declaration is authoritative for the increment's whole loop. `round.risk_class` remains required as an auditable event snapshot, but it never chooses or lowers the convergence threshold. Every round joined to a Roadmap increment must resolve to exactly one declared increment and match its declared class; a missing declaration, unresolved join, or mismatch fails closed. `next` reads the declaration before round one and continues to report that declared class and its required streak after rounds exist. No reader recovers a missing declaration from the ledger or the first round.

The plan-source projection, workflow check and forward driver use one declared-increment view. `src/plan/source.rs` must retain each increment id, owner step and class instead of normalising them away; `src/workflow.rs` uses that view for W3 and the shared reconstruction; `src/next.rs` uses it for pre-first-round output and rejects conflicting snapshots rather than selecting either value. Existing Roadmap work-review histories are migrated by declaring their exact retained increment identities and observed classes in the plan before enforcement is switched on; the append-only round log is not rewritten. Task-scoped single-pass records and other records that are not Roadmap increments remain event snapshots and must not be misjoined to a Roadmap declaration.

The ledger narrative keeps the review evidence a resuming human needs, but points at the plan declaration and joined round records rather than restating class or required count. Narrative round/streak history remains until the separately open structured-ledger design settles its own scope; this step removes only the prose duplicate and settles the relationship between the two structured values.

### Increment 1, `structured-risk-class-source-inc1`

RISK CLASS `risky` (two consecutive clean review rounds), declared here in the plan before this loop opens. The increment changes the convergence bar every reviewer loop and downstream scaffold follows. A false green can reduce a declared risky loop to the low-risk bar, so the blast radius is wide.

WHAT CHANGES.

- `src/plan/source.rs`, `src/workflow.rs` and `src/next.rs`: carry the declared increment map through the plan projection, make it W3/shared-reconstruction authority, and make `next` use it before and after the first round.
- The current plan source: add any missing historical Roadmap increment declarations without renaming converged increment identities, changing statuses or rewriting the event log.
- `pack/AGENTS.md` and its committed renders `AGENTS.md` and `.agents/AGENTS.reference.md`: classify once at loop open, declare the increment class in the plan before review, repeat it as a snapshot on every round, and remove the instruction to copy class or required count into ledger prose.
- `pack/prompts/orchestrator.md` and `.agents/prompts/orchestrator.md`: at point of action, declare/read the plan increment and reject a missing or conflicting declaration instead of deriving from round one.
- `pack/LEDGER.template.md` and `.agents/LEDGER.template.md`: point to the declared increment and joined rounds without an independent class value.
- `pack/instrument.md`: describe `round.risk_class` as the required event snapshot that must equal the plan declaration, not the authoritative loop-open value.
- `pack/plan-template.plan.toml` and the committed `docs/plans/TEMPLATE.plan.toml`: teach the loop-open increment declaration without forcing a class before a loop exists.
- `README.md` and `CHANGELOG.md`: document fail-closed workflow validation, pre-round `next` output and the migration/authority change.

ACCEPTANCE.

1. The plan parser exposes a typed `(step, increment, declared risk_class)` projection used by W3, the shared reconstruction and `next`; a red mutation that drops increments from that projection fails the workflow and next suites.
2. The reproduced downgrade is red: a `risky` `dangerous-inc1` declaration plus one `low_risk` clean round fails `validate --workflow`, identifies both values and the increment, and never reports convergence. Mutating the round to `risky` leaves one clean round short of the two-round bar.
3. A round for a Roadmap increment with no declaration fails closed. A later round whose snapshot differs from the declaration also fails even when every round agrees with that later value; neither a waiver nor a historical cap-adoption boundary suppresses a missing declaration or mismatch.
4. Before round one, human and JSON `next` output for a declared `risky` increment reports `risk_class = risky` and `required_streak = 2`. Red controls that restore nulls or derive the value only after a round fail. After rounds exist, both surfaces retain the declaration and a conflicting snapshot produces a typed data-fault action rather than ordinary reviewer advice.
5. Strict metrics validation still rejects a round with no `risk_class`. Round snapshots remain required and auditable; they are checked against the declaration rather than becoming optional or authoritative.
6. Current-history migration preserves every existing converged Roadmap increment id and class, adds no new round/escalation/waiver event, changes no Roadmap status, and leaves task-scoped non-increment records out of the Roadmap join.
7. Fixed-string and drift-guard controls cover the pack guidance, committed AGENTS copies, orchestrator prompts, ledger templates, instrumentation guidance and plan templates. No surface instructs an orchestrator to recover class from prose or from the first round.
8. Both validation modes, strict render, tests including all red controls, Clippy, diff checks and ASCII checks pass.

### Documentation impact

This semantic change makes the convergence guidance, point-of-action orchestrator prompt, ledger template, instrumentation schema explanation, starter plan template, README workflow-check description and changelog stale; all are explicit implementation paths above. The generated AGENTS and starter-template copies move with their pack sources. `.agents/workflow.toml` still owns only the class-to-required-streak constants and needs no value change: Q-83 changes which plan value selects a class, not what each class requires. The Q-80 inheritance sidecar is updated in this planner fold so a rebuild writes the inherited class into the new increment declaration rather than its first round.
