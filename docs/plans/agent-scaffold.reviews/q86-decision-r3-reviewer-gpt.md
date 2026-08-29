# Q-86 decision-fold plan round 3 review — GPT

Reviewed `main...5845ece6` independently as a risky plan artifact. I read `AGENTS.md`, the reviewer prompt, Q-86/Q-91 decisions and receipts, Q-88 through Q-90, the narrowed synthesis and retained proposals, all five synthesis triages, both prior decision-fold triages, the proof step, structured plan source, Success Criteria, ledger resume anchor, and generated projection.

The four round-2 repairs reproduce as landed:

- Declaration order now agrees with unique `order = 117`; the migration detector reports only the pre-existing `rename-to-agent-flow` exception, and the duplicate-order detector reports nothing.
- `FutureOwnerPending` explicitly permits the discovering and intervening phases to complete while blocking family delivery.
- `L_q` and `L_B` are scoped to ordinarily delivering `Complete` paths, with early terminal and non-delivery paths tested separately.
- The false ledger-currency assertion is gone; the proof sidecar assigns the resume-anchor move to orchestrator integration.

The ordinary gates pass:

```text
nix develop --command cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml
# docs/plans/agent-scaffold.plan.toml: up to date
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl
# 498 records, 115 steps, 91 questions, valid
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow
# workflow invariants hold
git diff --check main...5845ece6
# exit 0
```

## F1 — Blind-closure findings have contradictory terminal and continuation routes

- **Severity:** medium.
- **Evidence:** The selected M2 provenance says unqualifiedly that “A blind-closure finding is terminal” (`docs/plans/workflow-calibration.explorations/Q-86-safety-process.md:420`). The proof specification instead routes every finding against a closed current-phase owner to deferred reopen work (`docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md:49,55`) and routes every future-owner finding, without a blind-closure exception, to `FutureOwnerPending` so the phase may complete (`:57`). The proof requires only one blind-closure batch (`:35,161`), and neither its named fixtures (`:68-76`) nor its mandatory mutation classes (`:134`) specifies the disposition of a finding raised by that batch. Reproduce the missing proof-level terminal rule with:

  ```sh
  rg -n -i 'blind[- ]closure.*(finding|valid|terminal)|finding.*blind[- ]closure|closure finding|closure.*terminal' \
    docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md
  ```

  It finds closure/exhaustion mentions but no rule or fixture saying which blind-closure findings terminalise. A concrete legal trace exposes the ambiguity: one obligation receives a clean initial attempt and becomes closed with reopen unused; its phase then runs blind closure, as the selected M2 source requires after all obligations close (`Q-86-safety-process.md:326,330`); that batch raises a valid current-owner finding. Applying the proof sidecar's general current-owner rule defers and then spends reopen authority, after which the family may complete without another blind pass. Applying the retained red-control rule terminalises the same event. A future-owner finding from the same blind batch creates the opposite conflict: the repaired cross-phase rule requires it to survive to the future campaign, while the unqualified red-control sentence says it is terminal.
- **Impact:** An implementer cannot construct one transition relation that follows both current sources. Choosing deferred current-owner repair permits delivery after a repair performed later than the only blind-closure evidence; choosing the universal terminal rule breaks the newly repaired future-owner progress path. The generic `blind closure` mutation requirement can pass by proving that a closure batch exists without detecting either wrong routing choice.
- **Required correction:** Define blind closure as an explicit discovery stage and state its route product by owner and disposition. At minimum, say whether a valid current-owner finding is terminal rather than reopenable, preserve the repaired `FutureOwnerPending` continuation where intended, retain prior/unowned terminal blocks, and define serious-dismissal re-check outcomes. Align the retained red-control wording, add current- and future-owner blind-closure fixtures, and require killing mutations for post-closure repair, accidental terminalisation/loss of a future-owner component, and delivery without fresh closure evidence.

## Counts

- Critical: 0
- High: 0
- Medium: 1
- Low: 0
- Total: 1
