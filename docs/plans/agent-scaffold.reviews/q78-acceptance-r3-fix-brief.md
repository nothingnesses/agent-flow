# Q-78 acceptance pass 3 repair brief

Act only as planner. Read AGENTS.md, both pass-3 reports, `q78-acceptance-r3-triage.md`, the current plan, Q-58/Q-82, the driver architecture, `structured-risk-class-source`, and ledger RESUME HERE.

Record the human risk-class decision as Q-83, decided and folded into `structured-risk-class-source`, with this exact receipt:

Options:

- `Make the plan increment authoritative`.
- `Make the first round authoritative`.
- `Add an authoritative loop-open event`.

Recommendation and chosen: `Make the plan increment authoritative`.

Decision: `[[step.increment]].risk_class` is declared at loop open and is authoritative. `round.risk_class` remains an auditable event snapshot. Every round must match its declared increment class, and missing declarations or mismatches fail closed. `next` reads the declared class before round one. This refines the earlier choice to retire the ledger prose duplicate.

Repair all five pass-3 findings:

1. R3-1: make the chosen authority model explicit throughout the step, Success Criteria, guidance impact and red controls. Include the reproduced `risky` TOML versus `low_risk` round false green and the pre-first-round case. The planned implementation must touch the necessary plan projection, workflow check and `next` paths. Do not claim no source change.
2. R3-2: preserve legal `ready-to-plan` and `blocked` actions in the typed carrier. Represent them directly or retain the current pending fallback until the scheduler replaces it. Pin human and JSON output plus red empty-carrier controls.
3. R3-3: add a question-scoped exploration variant keyed by a real `exploring` question id and independent of Roadmap status. Pin Q-68/Q-69-shaped fixtures and refuse a fake unrelated-step carrier.
4. R3-4: make the focused scheduler sidecar the implementation authority and align the canonical architecture. Define one eligible-step domain, the `skipped` blocker policy, task-action precedence over or beside the step frontier, and when selected-action membership applies. Pin skipped blockers, task acceptance with pending work, active review and serial fallback.
5. R3-5: replace the stale `CI-overlap for the knee` instruction with the frozen non-inferiority or equivalence procedure. Confidence intervals report uncertainty only.

Update dependencies, changed-path sets, documentation impact and Success Criteria. Keep the current Q-82 staging, settled residuals and converged increment identities. Do not implement code, edit pack, change existing Roadmap statuses, close Q-58 or Q-78, or invent another human decision.

Edit plan TOML, generated view, relevant sidecars and append the Q-83 decision receipt. Render and run both validations, strict render, tests, Clippy, diff and ASCII checks. Commit with a docs subject. Do not push.
