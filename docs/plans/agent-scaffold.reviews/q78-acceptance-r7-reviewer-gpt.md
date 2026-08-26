# Q-78 acceptance pass 7 GPT review

## Result

Two acceptance shortfalls: one `medium`, one `low`. No `critical` or `high` shortfalls.

## Findings

### R7-G1 - `medium`: the Q-86 brief requires the known-unbounded baseline to satisfy a bounded-path proof

The design question exists because the current workflow permits indefinitely repeated resume windows and acceptance passes (`docs/plans/workflow-calibration.explorations/Q-86-convergence-mechanism-brief.md:11,19-21`). The required proposal output nevertheless includes the current mechanism among "viable" mechanisms (`:85`) and requires a finite bound or exact terminal event for *every path* (`:89`), with a stopping-bound demonstration before recommendation (`:95`). The current baseline has a path consisting of repeated human resumes, and another consisting of repeated acceptance repairs, for which it deliberately has neither a finite bound nor a forced terminal event. An explorer therefore cannot satisfy all three requirements as written: either it falsely calls the current baseline bounded, omits it, or reports the required no-bound result while violating item 5.

This is an internal design-contract contradiction, not an objection to retaining the current mechanism as a control. Make the current mechanism an explicitly non-admissible baseline that may fail the stopping proof, or require more than one viable bounded alternative in addition to that baseline. Keep the finite-bound/exact-terminal obligation for candidate mechanisms that may be recommended.

### R7-G2 - `low`: Q-85's fold made Q-84's freshly repaired 44/35/27/18 measurement stale again

Q-84 and its owning sidecar state that the current commands produce 44 relaxed selections, 35 anchored selections, 27 relaxed stripped openings needing authoring, and 18 anchored handover openings (`docs/plans/agent-scaffold.plan.toml:2528-2534`; `docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md:19-28`). Re-running the sidecar's selectors and exact H1 token-strip/uppercase test in the authorised scratch mount now prints:

```text
relaxed=44 anchored=35 relaxed_handover=26 anchored_handover=17
```

The new evidence postdates pass 6: commit `222fba5a` changed `docs/plans/agent-scaffold.steps/workflow-calibration.md:3` from `Not started (deferred). ...` to `In progress. ...`. Both selectors still select that line, but H1 now strips it to the grammatical uppercase opening `The scaffolded workflow...`, removing exactly that slug from both handover sets. This is not a re-raise of pass-6 finding B on the same tree; the Q-85 fold changed the selector input after Q-84 was decided.

The dynamic selectors remain valid implementation authority, so the defect is stale decision evidence rather than a broken handover. Correct the dated figures and identify `workflow-calibration` as the second movement, without hard-coding the new totals as acceptance conditions or reopening the selector design merely because its input changed.

## Required gates

All required gates passed using the project Nix development environment and only the authorised scratch mount for Cargo state and destructive checks:

- `agent-flow validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl`: `472 records, valid`; `114 steps, 86 questions, valid`.
- `agent-flow validate --source docs/plans/agent-scaffold.plan.toml --workflow`: `workflow invariants hold`.
- `agent-flow render --check --strict docs/plans/agent-scaffold.plan.toml`: `up to date`.
- `agent-flow checks`: 1 passed, 0 failed, 0 skipped.
- `cargo test --locked --offline`: 470 passed, 0 failed.
- `cargo clippy --all-targets --locked --offline -- -D warnings`: passed.
- `git diff --check` passed for the complete product and the pass-6/pass-7 repair ranges.
- ASCII check over all 103 files changed from `main` to `plan/q78-design-pass`: 0 non-ASCII files.
