### `workflow-loop-visibility`: make `next` distinguish exploration from review and project every active loop while selecting one next action (`Q-82`)

Q-82 chose `Schedule visibility and scheduling in stages`. This step is the first stage only: repair phase correctness and visibility. It gives `next` no authority to schedule parallel work and does not build the Stage-2 typed fleet.

THE PROBLEM. Stage 1 deliberately selects one lowest-order `in-progress` step and models it as a review loop. A current run therefore presents an exploration as `awaiting-first-review`, hides other active loops, and emits 727754 bytes around one selected block. Status alone cannot distinguish exploration, implementation, review and acceptance, so a different sort cannot repair the false phase.

THE APPROACH. Add one typed, mutable workflow-phase field for an `in-progress` Roadmap step, with a closed enum covering at least `exploration`, `implementation`, `plan_review`, `work_review` and `acceptance`. The field is required exactly when status is `in-progress` and forbidden otherwise; parse the combination at the plan boundary so an active step with no phase cannot reach `next`. Backfill every currently in-progress step from durable evidence during this increment without changing any status. This is the smallest durable source that lets the driver distinguish phases without heuristically parsing sidecars or ledger prose.

`next` projects every in-progress step as an ordered `active_loops` collection on JSON and human surfaces. Review phases retain their W3-derived review-loop state. Exploration and implementation receive phase-correct actions and roles and never masquerade as `awaiting-first-review` merely because they have no round records. The existing singular `active_loop` remains as the deterministically selected loop/action for compatibility and one-action focus; it must be one member of `active_loops`, not a separately reconstructed answer.

### Increment 1, `workflow-loop-visibility-inc1`

RISK CLASS `risky` (two consecutive clean review rounds). The increment changes the plan schema and the machine output agents act on, and a phase error can dispatch the wrong authority. It is read-only and introduces no scheduler, which bounds the risk without making it low.

ACCEPTANCE.

1. Source validation rejects an `in-progress` step with no workflow phase, rejects an unknown phase, and rejects a terminal/not-started step carrying one. Each error names the slug and illegal combination. Fresh templates remain valid because their initial step is not in progress.
2. A fixture with one exploration, one implementation loop and two review loops projects all four exactly once in declaration order on both surfaces. A red mutation restoring the single-step filter drops three and fails.
3. The exploration row emits the explorer role/action and no reviewer action, review streak or false `awaiting-first-review`; the implementation row likewise emits its writer action. A red mutation mapping every in-progress step through review reconstruction fails phase-specific tests.
4. `active_loop` equals one member of `active_loops` byte-for-byte after JSON decoding. Selection stays deterministic and preserves one next action; changing visibility never implies permission to spawn the whole collection.
5. Existing Stage-1 review-state fixtures keep their state, streak, cap, transitions and output. JSON adds `active_loops` without silently renaming or repurposing `active_loop`; human output labels the selected row.
6. The current plan's in-progress steps receive explicit phases from cited durable evidence, with no status change. The migration is reviewed as plan data and re-rendered.
7. Output size is measured on the motivating plan. The result reports the contribution of loop visibility separately from the Q-58 resume carrier and does not claim this step solves carrier bloat.
8. No `src/driver/` fleet, DAG scheduler, write command, worktree spawn or parallel execution enters this increment. A changed-path review rejects those scopes.
9. README documents the plural JSON/human projection and singular selected action; `CHANGELOG.md` records the schema/output addition. Pack plan guidance and templates document the workflow-phase rule if the schema field ships to scaffolded projects.
10. Both validation modes, strict render, tests including red controls, Clippy, diff checks and ASCII checks pass.

### Documentation impact

Update README's `next` JSON vocabulary and examples, the plan-source field documentation in the pack guidance/template if required by the schema, their committed copies and drift guards, and `CHANGELOG.md`. The retained Stage-1 build plan remains historical and is not rewritten; `workflow-driver.md` points to this corrective successor. Q-58 carrier work remains independent and owns resume-echo documentation.
