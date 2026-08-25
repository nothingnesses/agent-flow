### `sidecar-status-authored-openings`: author phase-neutral openings for the handover left by `sidecar-status-opening-drift`

This is the successor `Q-78-driftsplit` promised and `sidecar-status-opening-drift` deliberately did not author. It starts only after that predecessor converges. The predecessor deletes status labels only where the remaining prose is already grammatical and leaves every authored-replacement opening, token intact, for this step.

THE INPUT IS A PROPERTY, NOT A FROZEN SLUG COUNT. At this step's base, rerun the predecessor's anchored selector over the generated Roadmap and capture its complete output. Because the predecessor has removed its own worklist, the remaining rows are this step's handover. Record the list in the outcome before editing. The 2026-08-21 decision was taken against the then-current measured set; later plan edits may move that set, so no implementation criterion hard-codes its old count.

THE APPROACH. Read each selected opening against the step's current TOML status and complete sidecar, then author one phase-neutral opening that states the enduring problem, approach or sequencing fact without restating any Roadmap status. Delete the leading token in the same edit. Preserve every unrelated edit already made to that line, especially a slug-restatement from `plan-order-array-position`; do not recover an old line wholesale from git.

### Increment 1, `sidecar-status-authored-openings-inc1`

RISK CLASS `risky` (two consecutive clean review rounds). Every changed opening is authored prose published verbatim into the plan, and correctness requires a reading rather than a complete mechanical oracle. The work ships no product code and reverts cleanly, but the breadth and semantic review obligation set the class.

ACCEPTANCE.

1. Capture the predecessor's anchored selector at the increment base as `handover-before.tsv`. Every selected slug resolves to one current Roadmap step and one sidecar. An empty capture is valid only if the outcome demonstrates that intervening reviewed work already closed every row.
2. For every captured row, the outcome quotes the before and after opening and states what enduring fact the new opening carries. A generic replacement sentence or a new phase/status synonym does not satisfy the reading.
3. Rerun the anchored selector after the edit. It prints no row from `handover-before.tsv`; any newly selected row is disposed of rather than ignored.
4. A bounded vocabulary scan over each changed opening reports status labels and adjacent phrases (`not started`, `in progress`, `complete`, `next`, `optional`, `deferred`, `pending`, `not yet`). Every hit is either removed or justified as referring to an external object rather than this step's state.
5. Diff each changed opening against the increment base. Changes are confined to the first non-heading, non-blank line, and a reviewer verifies that concurrent citation/title edits on that line survive. A red mutation restoring one old token makes the selector fail.
6. Regenerate `docs/plans/agent-scaffold.md` and run strict render. Its numstat equals the sum of the changed sidecar lines plus renderer framing; the generated file is never hand-edited.
7. The changed-path set is exactly the captured sidecars plus `docs/plans/agent-scaffold.md`. No Roadmap status, plan TOML, metrics, source, test or pack file changes.
8. Both validation modes, strict render, tests, Clippy, diff checks and ASCII checks pass.

### Documentation impact

No shipped documentation changes. Authoring this step made the predecessor's future-tense handover stale, so the planning fold updates `sidecar-status-opening-drift` to name this slug while preserving why an early stub was refused. The implementation step itself makes existing plan prose comply with `agent-scaffold.documentation-protocol.md`; it changes neither that rule nor the scaffolded template. Its only projection is the generated plan. The dynamic handover and review outcome are the durable documentation of which openings moved.
