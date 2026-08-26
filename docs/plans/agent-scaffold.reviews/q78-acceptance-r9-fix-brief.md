# Q-78 acceptance pass 9 repair brief

Act only as planner. Read AGENTS.md, both pass-9 reports, `q78-acceptance-r9-triage.md`, the complete product and the ledger. Repair only finding A. Do not act on findings B or C, which triage dismissed.

At both live sites below, preserve the sidecar-existence reasoning but replace the false universal that every question sidecar is empty:

- `docs/plans/agent-scaffold.steps/plan-order-array-position.md`.
- `docs/plans/umbrella-membership.explorations/Q-79.md`.

State that question sidecars must exist and most are empty. Make `find docs/plans/agent-scaffold.questions -type f -size +0` the sole authority for the current non-empty set. Do not write a count or enumerate paths. Match the de-counted wording already used by the accepted pass-8 repair. Re-render after changing the Step Detail source.

Do not change questions, receipts, Success Criteria, Roadmap statuses, workflow rules, code, packs or other historical claims. Run both validations, strict render, tests, Clippy, diff checks and ASCII checks. Do not run `agent-flow checks` inside the container. The orchestrator will run it on the host. Commit with a docs subject. Do not push.
