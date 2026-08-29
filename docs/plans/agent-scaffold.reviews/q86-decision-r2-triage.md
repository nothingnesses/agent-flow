# Q-86 decision-fold plan review, round 2 triage

## Scope and reproduction

I independently read `AGENTS.md`, `.agents/prompts/triager.md`, the Q-86 proof-step sidecar, the Q-86 synthesis and safety proposal, the round-1 triage, both round-2 reviews, the plan-order migration specification, the current plan and ledger, and the decision receipts. I judged the current decision-fold sources, not the retained controller prototype as a proof.

The mechanical plan gates reproduce cleanly:

```text
nix develop --command cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml
# docs/plans/agent-scaffold.plan.toml: up to date
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl
# docs/metrics/workflow.jsonl: 497 records, valid
# docs/plans/agent-scaffold.plan.toml: 115 steps, 91 questions, valid
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow
# docs/plans/agent-scaffold.plan.toml vs docs/metrics/workflow.jsonl: workflow invariants hold
git diff --check 1009ea82..HEAD
# exit 0
```

The reviewers raised five raw findings. Claude R2-C1 and GPT F2 are the same future-owner phase-progress contradiction, leaving four consolidated findings. All four are valid: three medium and one low. No finding is accepted as a residual.

## T1 — The unique `order = 117` repair creates a second declaration-order mismatch that the array-order migration denies

- **Sources:** GPT F1.
- **Verdict:** valid, **medium**.
- **Reproduced evidence:** `bounded-convergence-option-b-proof` is declaration position 36 but has `order = 117` in `docs/plans/agent-scaffold.plan.toml:486-513`; `rename-to-agent-flow` is the other decreasing transition. The migration's prescribed detector prints both:

  ```text
  out of place: "bounded-convergence-option-b-proof"
  out of place: "rename-to-agent-flow"
  ```

  Yet `docs/plans/agent-scaffold.steps/plan-order-array-position.md:9-17,87-91` says the declaration sequence differs at exactly one place and directs increment 1 to move only `rename-to-agent-flow`. Its byte-exact oracle depends on declaration order matching the current order-sorted render before `order` is removed. Removing `order` after only that specified move puts the proof row at position 36 rather than its current rendered position 115, shifting the old rows in between. The migration's position/citation partition at `:279-294` consequently retains a false premise about the positions that will result.
- **Reasoning:** Round 1 correctly removed the duplicate order and avoided moving any existing rendered row today, but it left the later order-to-array migration with an incomplete data move. The migration is a planned schema and sequencing change with a byte-exact projection gate; its current specification cannot produce the promised unchanged projection. This is a future-planning defect, not a current renderer defect, so it is medium rather than high.
- **Exact correction:** Make the proof block's declaration position agree with its unique final order before the migration, or revise `plan-order-array-position` to own and test the second move. In either case, update its “exactly one” claims, move set, red/green and changed-path contracts, and the positional citation/worklist reasoning to cover the proof block, then re-check the eventual declaration-order projection.

## T2 — The retained M2 completion wording deadlocks the required `FutureOwnerPending` path

- **Sources:** Claude R2-C1; GPT F2.
- **Verdict:** valid, **medium** (deduplicated; GPT's severity is retained).
- **Reproduced evidence:** The proof step requires `FutureOwnerPending` to remain live across intervening campaigns and activate only when its canonical phase is scheduled (`docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md:53-60`). The retained M2 proposal, which the synthesis maps to selected Option B (`docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:11`), says that after a phase's blind closure “a settled complete map with no prior- or future-owner route finishes the phase or family as applicable” (`docs/plans/workflow-calibration.explorations/Q-86-safety-process.md:330`).

  For ordered phases `work-1`, `work-2`, `acceptance`, an early `work-1` finding canonically owned by `work-2` must remain `FutureOwnerPending`. Reading the quoted completion predicate at phase scope prevents `work-1` from completing while that route is live, but `work-2` cannot be scheduled until `work-1` completes. The required early-work-to-future-owner fixture therefore has no progressing execution under that source. The proof sidecar instead places the no-live-prior/future-route predicate only on family `Complete` (`bounded-convergence-option-b-proof.md:37`), demonstrating the conflicting scopes.
- **Reasoning:** The selected proof is still gated and its required fixture should expose the deadlock, so the inconsistency does not yet authorize unsafe production behavior. But M2 remains selected-option provenance and its phase/family ambiguity contradicts the executable proof specification at the exact cross-phase route round 1 required. An implementer can otherwise encode a fail-closed but non-progressing model or weaken the future-owner route. That makes it medium, not low or high.
- **Exact correction:** In `Q-86-safety-process.md`, state separately that a phase may complete after its own obligations and blind closure settle while retaining `FutureOwnerPending` components for later campaigns; retain the no-prior-or-future-route condition solely for family delivery/`Complete`. Keep a completed-prior-owner route terminal, and align the future-owner fixture and mutation wording with that phase-versus-family rule.

## T3 — The stated minima include legal terminal paths outside their lower-bound domain

- **Source:** GPT F3.
- **Verdict:** valid, **medium**.
- **Reproduced evidence:** The proof presents `L_q = n_q + 1` and `L_B = r_plan + |O| + m + 1` as unqualified bounds at `docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md:104-120`, and acceptance criterion 10 repeats them at `:165`. The same transition model admits early `TerminalChoice` for an unowned finding or a completed-prior-owner finding (`:36,45,56`) and expressly requires checks of “early terminal paths” (`:120`). With one obligation, a first batch containing an unowned finding may terminally stop after one post-freeze batch, below `L_q = 2`; a pre- or post-freeze terminal route can likewise end before the published whole-family lower bound. The retained proposal correctly calls `n_q + 1` a **clean** post-freeze minimum (`Q-86-safety-process.md:342`), but the proof specification does not preserve that domain.
- **Reasoning:** A lower bound over all legal executions contradicts its own terminal transitions. The proof must distinguish ordinarily delivering completion paths from terminal non-delivery paths or its algebra oracle must silently reinterpret or reject legal states. This is a material soundness gap in the blocking proof design, hence medium.
- **Exact correction:** Define `L_q` and `L_B` explicitly as lower bounds over ordinarily delivering `Complete` paths, with the necessary preconditions for such a path. State that terminal/non-delivery paths are outside that minimum domain, and make the algebra oracle and criterion 10 assert both the scoped lower bounds and legal early-terminal behavior rather than applying the formulas to every execution.

## T4 — The proof-sidecar falsely claims the orchestrator-owned ledger resume anchor is already current

- **Source:** Claude R2-C2.
- **Verdict:** valid, **low**.
- **Reproduced evidence:** The proof sidecar says the fold “leaves the orchestrator-owned ledger to its already-current resume anchor” at `docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md:128`. The ledger's first current-looking Q-86 anchor at `docs/plans/agent-scaffold.ledger.md:535` says the fold has 496 metrics records and that plan-review round 1 is next. Both are stale: `wc -l docs/metrics/workflow.jsonl` and the metrics validator report 497 records, while the later ledger prose at `:551` itself says decision-fold round 2 is next and records 497. `agent-flow next --source ... --json` echoes both `496 metrics records` and `497 metrics records` from that resume material.
- **Reasoning:** The ledger is the durable resume source; contradictory counts and next actions are a real currency defect. Its current later paragraph contains the correct round, and the round-counting narrative is not endangered, limiting the impact to low. The sidecar must not declare currency for an artifact whose update belongs to the orchestrator rather than the planner.
- **Exact correction:** Remove the “already-current” assertion from the proof sidecar and state that advancing the ledger resume anchor is an orchestrator integration duty. When this round is recorded and the next action changes, the orchestrator must update the authoritative anchor and eliminate the stale count/action rather than asking the planner to edit the ledger.

## Outcome and backstop

**Outcome: `new_valid`.** Valid findings: **4** — **0 critical, 0 high, 3 medium, 1 low**. Invalid findings: **0**. Accepted residuals: **0**.

No high- or critical-severity finding was dismissed, so no independent dismissal backstop re-check is owed. This risky plan-review round cannot count as clean.
