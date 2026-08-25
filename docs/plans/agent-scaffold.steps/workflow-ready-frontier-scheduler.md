### `workflow-ready-frontier-scheduler`: add the workflow driver's read-only ready-frontier scheduler after the typed fleet (`Q-82`, Stage 3)

This is the later scheduler stage authorised by Q-82. It reuses `workflow-driver` Stage 3 and the typed fleet; it does not combine scheduler authority with the first phase/visibility repair.

THE PROBLEM. Once every active unit is visible and typed, choosing only the lowest-order action serialises independent work and leaves the existing `blocked_by` graph unused. Choosing every non-blocked step naively is also wrong: it can schedule dependencies together, include terminal work or turn a read-only adviser into an executor.

THE APPROACH. Implement the Stage-3 pure step-granularity graph function in `driver/schedule.rs`. Given the typed task fleet and `blocked_by`, return the declaration-ordered ready frontier: the maximal set of nonterminal steps whose blockers are complete and whose current typed states permit work. Project that frontier as advice in JSON and human output. Preserve one selected next action for a serial harness; expose the remaining frontier as parallel candidates. The tool never spawns, reserves or mutates work.

No increment-level DAG, resource allocator, priority score, daemon, persisted lease or automatic merge enters this step. The plan's step graph is the only scheduling graph.

### Increment 1, `workflow-ready-frontier-scheduler-inc1`

RISK CLASS `risky` (two consecutive clean review rounds). Agents act on scheduler advice, so an invalid frontier can start work before its dependency or fan out conflicting authority. The function is pure and read-only, which makes exhaustive fixture testing possible but does not reduce the consequence of wrong advice.

ACCEPTANCE.

1. Table fixtures cover independent ready steps, a dependency chain, a diamond, blocked/deferred dependencies, terminal steps, simultaneous active review loops and no-ready-work. Every frontier is declaration ordered and contains no duplicate.
2. For every returned step, every `blocked_by` slug resolves and is complete. A mutation that treats merely scheduled or in-progress blockers as complete fails.
3. The frontier is maximal over eligible steps: a mutation that returns only the first ready step fails, and a mutation that returns all nonterminal steps fails on the dependency fixtures.
4. Phase authority is preserved. Exploration, implementation, review and acceptance candidates retain the actor/action emitted by the typed fleet; the scheduler does not rewrite them into a generic worker action.
5. JSON carries a typed `ready_frontier` and one `selected_action` that is a member when the frontier is non-empty. Human output names parallel candidates separately from the one action to take in a serial harness.
6. Determinism holds across runs and machines. No wall clock, filesystem lock, model capacity or worktree availability changes the pure frontier.
7. No command writes the plan, metrics, ledger or worktree; no spawn/merge API is added. Red path review rejects `driver/record.rs`, a daemon or an increment-level scheduler.
8. Existing Stage-1/visibility/typed-fleet fixtures remain green. Differential tests show a one-ready-step fixture yields the same selected action as before this step.
9. README documents advisory frontier semantics and serial fallback, and `CHANGELOG.md` records the new output. Pack guidance changes only if it currently says the orchestrator may run exactly one ready step.
10. Both validation modes, strict render, tests including red mutations, Clippy, diff checks and ASCII checks pass.

### Documentation impact

Update README's `next` human/JSON contract, the driver architecture summary and `CHANGELOG.md`. If the pack guidance's checkpoint cadence or worktree lifecycle wording assumes strict serial execution, revise it and its committed copies to distinguish a proposed frontier from authority to spawn. No new scheduling policy document is created; `workflow-driver` remains the architecture source.
