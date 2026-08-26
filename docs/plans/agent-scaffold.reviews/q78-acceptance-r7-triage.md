# Q-78 acceptance pass 7 triage

## Scope and verification

I independently read the pass-7 reports, acceptance triages 1–6, Q-78/Q-84/Q-85/Q-86, the repaired plan product, and the ledger. I reproduced each pass-7 claim from the committed product rather than adopting a reviewer conclusion.

Using `/nix/store/4rayq0a6f1cq2cdcxm6cnhnlgqgbdjhk-source/target/debug/agent-flow`, I reproduced:

- `validate --source docs/plans/agent-scaffold.plan.toml`: 472 records and 114 steps / 86 questions valid.
- `validate --workflow --source docs/plans/agent-scaffold.plan.toml`: workflow invariants hold.
- `render --check --strict docs/plans/agent-scaffold.plan.toml`: up to date.
- `git diff --check`: passed.

All copy-and-mutation probes were under the authorised scratch mount. The product worktree remained clean. `agent-flow checks` was deliberately not run, because this container cannot see the complete worktree set.

## Deduplication

- Claude finding B and GPT R7-G2 are one post-Q-84 drift-measurement finding and are adjudicated once as R7-3.
- Claude finding A (the newly authored status token) is distinct from R7-3 (the changed selector populations it caused), despite their shared repair path.
- GPT R7-G1 and Claude finding C concern independent Q-86 design-contract and Q-85 provenance defects.

No finding is dismissed or accepted as residual, so no independent high/critical dismissal re-check is owed.

## Verdicts

### R7-1 — GPT R7-G1: valid, `medium`

The Q-86 brief itself establishes that the current mechanism has an unbounded path: a human resume resets the five-round window, and acceptance has no task-level pass cap (`docs/plans/workflow-calibration.explorations/Q-86-convergence-mechanism-brief.md:14-21`). It nevertheless calls that mechanism one of “more than one viable mechanism” (`:85`) while requiring a finite bound or exact terminal event for every path (`:89`) and a stopping-bound demonstration before recommendation (`:95`). Repeated resumes or acceptance repairs satisfy neither proof. Thus the current mechanism cannot both be an admissible viable candidate and meet the required stopping proof.

This blocks a truthful exploration result rather than merely using imprecise terminology: an explorer must either falsely prove the baseline bounded, omit the required baseline, or fail an explicit required output. It is `medium` because it is an unimplemented design-pass contract, not current workflow behaviour.

Smallest safe disposition: retain the current mechanism as a required, explicitly non-admissible comparison baseline. Require its proposal section to demonstrate the repeated-resume and acceptance countermodels and report that it fails the bounded-path property. Keep the finite-bound/exact-terminal and red-control obligations for every viable, recommendable bounded mechanism, and require more than one such viable mechanism as the existing wording intends. Do not treat Q-85 as selecting a mechanism.

### R7-2 — Claude A: valid, `medium`

The Q-85 fold changed `workflow-calibration` from `Not started (deferred). ...` to `In progress. ...` (`6c8847b8`, `docs/plans/agent-scaffold.steps/workflow-calibration.md:3`). That is a newly authored copy of the TOML-owned status, although the status protocol says Step Details “do not repeat the status label” (`docs/plans/agent-scaffold.documentation-protocol.md:5`). More importantly, the governing Q-78 record says the duplicated label is the defect even when accurate (`docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md:3-7`) and records the human choice to delete the token rather than replace it (`:13-15`). Q-85 chose where to schedule the investigation, not an exception to that form decision (`docs/plans/agent-scaffold.plan.toml:2537-2547`).

This is `medium`: it contravenes a recorded human decision and reintroduces the drift mechanism in a live sidecar, although the dynamic selector still makes the pending implementation executable.

Smallest safe disposition: remove only the leading `In progress. ` from this opening, leaving the grammatical `The scaffolded workflow...` opening, then re-render. Do not revise the historical fold brief: it is a transient, already-consumed instruction, and no live product rule depends on it.

### R7-3 — Claude B / GPT R7-G2: valid, `low`

The Q-84 decision records 44 relaxed selections, 35 anchored selections, 27 relaxed stripped openings, and 18 anchored handovers as the current measurement (`docs/plans/agent-scaffold.plan.toml:2524-2534`); the owning sidecar repeats that result as current (`docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md:19-28,119`) and the ledger repeats the 18 premise (`docs/plans/agent-scaffold.ledger.md:551`). Replaying its anchored/relaxed selectors and H1 token-strip test gives `44/35/26/17` on the current tree. Replacing the pre-Q-85 opening in an authorised scratch copy gives `44/35/27/18`; the only handover membership change is `workflow-calibration`. This is new evidence from the Q-85 fold, not a relitigation of the `workflow-driver` movement adjudicated in pass 6.

The R7-2 repair changes the selector populations again. Applying only the token deletion in scratch produces the required post-repair measurement: `43 relaxed`, `34 anchored`, `26 relaxed stripped openings`, and `17 anchored handover openings`. `workflow-calibration` leaves the anchored selector; no handover member changes in that second transition.

Q-84 chose specifically to continue with the measured set of 18, after its premise had changed from 19 (`agent-scaffold.plan.toml:2528-2534`). The newly measured handover is 17. Its selectors remain the implementation authority, so this does not make the implementation criteria fail, but the decision's explicit factual premise is no longer current. It is therefore `low`.

Smallest safe disposition: repair R7-2 first. Then the planner must run the sidecar's exact relaxed selector, anchored selector, and H1 strip test on the repaired tree; record all four values `43/34/26/17` plus the two membership deltas above; and present the changed Q-84 premise to the human. The human, not the planner or triager, must decide whether Q-84's selector-defined split carries forward to the measured 17 or whether it reopens the split/design. Preserve Q-84 as the accurate at-decision 18 snapshot and make every live “current” measurement unambiguous after that decision; do not put a moving count into an acceptance criterion.

### R7-4 — Claude C: valid, `low`

Success Criterion 41 expressly requires the in-progress `workflow-calibration` step to record Q-85's decision and exact receipt (`docs/plans/agent-scaffold.success-criteria.md:41`). The sidecar records only the decision in prose (`docs/plans/agent-scaffold.steps/workflow-calibration.md:18`), and its `[[step]]` block has no `[step.provenance]` (`docs/plans/agent-scaffold.plan.toml:473-481`). The exact receipt exists independently at `docs/metrics/workflow.jsonl:472`, while Q-85 resolves to this step in the queue (`agent-scaffold.plan.toml:2537-2547`). The data is not lost, but the owning Step Detail cannot provide the durable decision/receipt handle that the criterion requires.

This is `low`, because the exact receipt is present and Q-85 made only a scheduling decision, but the new work lacks the required provenance link.

Smallest safe disposition: add the valid structured provenance link `decisions = ["Q-85"]` to the `workflow-calibration` step and identify the exact Q-85 receipt in its sidecar with a stable committed source pointer, then re-render. Do not create another Roadmap step or change Q-86's `exploring` status.

## Result

Four distinct acceptance shortfalls are valid: two `medium` and two `low`. The required repair order is R7-1 independently, then R7-2 before R7-3's post-repair measurement and human decision, with R7-4 folded alongside the Q-85/Q-86 planning repair. No residual risk was accepted and no high/critical dismissal requires a re-check.
