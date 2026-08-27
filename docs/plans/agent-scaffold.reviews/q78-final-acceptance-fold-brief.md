# Q-78 final acceptance fold brief

Act only as planner. The human accepted Q-78 after acceptance pass 10 returned zero shortfalls from both independent reviewers. Fold that final decision without changing the accepted design.

Append this exact closing decision receipt:

- `q_id`: `Q-78`.
- `task`: `step-intent-encoding`.
- Options: `Accept Q-78`, `Request revisions`.
- Recommendation and chosen: `Accept Q-78`.
- Date: `2026-08-26`.

Set Q-78 to `decided` and fold it into `step-intent-encoding`. Keep `receipt = "Q-78"`; the queue body already specifies that the closing receipt reuses the unsuffixed id and is distinguished from the route receipt by `chosen` and date. Update the Q-78 body so its live status, closing-receipt and review-pending statements describe the accepted state. Preserve the historical brief and sub-decisions rather than rewriting their at-the-time facts.

Remove `pending the review` from the titles and sidecar headings for `plan-order-array-position`, `ledger-order-citation-currency` and `step-intent-encoding`. Replace it with concise accepted-state wording only if context still needs it. Keep each TOML title and sidecar heading identical.

Add Q-78 to structured provenance for the three steps whose design it accepted:

- `plan-order-array-position`.
- `ledger-order-citation-currency`.
- `step-intent-encoding`, preserving Q-81.

Update the Q-78 exploration's live statement that no step cites Q-78 while it is open. Keep it as an explicitly dated review-stage fact and state that the final acceptance fold adds the now-valid provenance. Do not add Q-78 provenance to `validate-missing-source-exit`, which owns an independent defect.

Keep Q-86 `exploring`. Do not change any Roadmap status, increment, risk class, waiver, Success Criterion, workflow rule, code or pack asset. Do not add another acceptance obligation.

Render the generated plan. Run both validations, strict render, tests, Clippy, diff checks and ASCII checks. Do not run `agent-flow checks` in the container. The orchestrator will run it on the host. Commit with a docs subject. Do not push.
