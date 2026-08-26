# Q-78 acceptance pass 7 repair brief

Act only as planner in this isolated worktree. Read AGENTS.md, both pass-7 reviewer reports, `q78-acceptance-r7-triage.md`, Q-78/Q-84/Q-85/Q-86, the complete product, and the ledger. Repair exactly R7-1 through R7-4. Do not add optional scope.

## R7-1

Keep the current convergence mechanism as a required comparison baseline, but name it explicitly non-admissible because repeated resume windows and later acceptance passes provide unbounded counterexamples. Require the baseline section to demonstrate and report those counterexamples. Require more than one viable bounded alternative. Apply the finite-bound or exact-terminal-event proof, red controls, and recommendation eligibility only to viable bounded mechanisms. Preserve Q-85 as a scheduling decision, Q-86 as `exploring`, and the later human mechanism decision.

## R7-2

Delete only the leading `In progress. ` token from `docs/plans/agent-scaffold.steps/workflow-calibration.md`. Leave the grammatical `The scaffolded workflow...` opening. Do not edit the consumed `convergence-investigation-fold-brief.md`.

## R7-3 and Q-87

Record Q-87 as decided and folded into `sidecar-status-opening-drift`, with this exact receipt.

Options:

- `Follow the selector automatically`.
- `Pin the previous set of 18`.
- `Reopen the cleanup design`.

Recommendation and chosen: `Follow the selector automatically`.

The decision means that the selector-defined worklist follows the selector without another human decision when already-approved edits cause expected membership movement. Record the current counts as dated evidence: 43 relaxed selections, 34 anchored selections, 26 relaxed stripped openings and 17 anchored handover openings. Preserve Q-84 as an accurate 18-member snapshot at the time of that decision rather than rewriting its history as if it had selected 17. Make live references distinguish Q-84's historical snapshot from Q-87's current snapshot. Record both membership movements: `workflow-driver` reduced the handover from 19 to 18, and the token-free `workflow-calibration` opening reduced it from 18 to 17. Require a new human decision only if the selector or ownership split changes, or evidence shows that an expected movement changes the design premise. Do not put a moving count in an acceptance criterion.

Add Q-87 to the owning step's structured provenance without dropping Q-84. Update the Success Criterion only if its current wording would otherwise freeze a moving number.

## R7-4

Add `decisions = ["Q-85"]` as structured provenance for `workflow-calibration`. Identify the exact Q-85 receipt in the step sidecar with a stable path and selector or line pointer into the committed append-only metrics log. Preserve all existing provenance if present.

## Boundaries and gates

Do not change Roadmap statuses, current workflow constants, code, pack assets, loop identities, waivers or the historical fold brief. Do not close Q-58, Q-78 or Q-86.

Run both validation modes, strict render, tests, Clippy, diff checks and ASCII checks. Do not run `agent-flow checks` inside the container because its view of host worktrees is incomplete. The orchestrator will run that gate on the host after your commit. Commit with a docs subject. Do not push.
