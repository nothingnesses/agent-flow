# Q-86 decision-fold plan round 2 review - GPT

## Findings

### F1 - The order repair leaves a second declaration-order mismatch that breaks the already-planned array-order migration

- **Severity:** medium.
- **Evidence:** `docs/plans/agent-scaffold.plan.toml:486-513` declares `bounded-convergence-option-b-proof` physically between `workflow-calibration` and `instrument-flag`, but assigns it `order = 117` while `instrument-flag` remains `order = 36`. The future migration says declaration position will become order and claims only `rename-to-agent-flow` is out of place, so it will move only that one block (`docs/plans/agent-scaffold.steps/plan-order-array-position.md:9-17,87-91`). Re-running that migration's own prescribed detector now reports a second mismatch:

  ```sh
  awk '/^slug = /{s=$3} /^order = /{sub(/order = /,""); if ($0+0 < p) print "out of place:", ps; p=$0+0; ps=s}' docs/plans/agent-scaffold.plan.toml
  # out of place: "bounded-convergence-option-b-proof"
  # out of place: "rename-to-agent-flow"
  ```

  The same migration still classifies every numbered citation at or below 83 as safe because it assumes order equals eventual array position there (`plan-order-array-position.md:279-294`). Once `order` is deleted, the proof block becomes position 36 and shifts the old order-36-through-83 blocks by one, invalidating that exemption set.
- **Impact:** Round-1 T1 is not fully closed. Increment 1's byte-exact projection oracle will fail unless it performs an unplanned second move; if that mismatch is instead allowed through, increment 2 can preserve numerical citations that now resolve to the wrong step.
- **Required correction:** Put the proof block at the declaration position corresponding to its unique final order, or update `plan-order-array-position`'s move set, position map, worklist partitions, changed-path contract, and red/green oracle for the second mismatch.

### F2 - The retained selected-M2 source deadlocks a legal future-owner finding

- **Severity:** medium.
- **Evidence:** The repaired proof specification says `FutureOwnerPending` stays live across intervening campaigns and activates only when its canonical campaign is scheduled (`docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md:53-60`). The simultaneously repaired retained M2 source says a phase finishes only with "no prior- or future-owner route" (`docs/plans/workflow-calibration.explorations/Q-86-safety-process.md:330`). For a frozen order `[work-1, work-2, acceptance]`, a finding discovered in `work-1` for a `work-2` obligation is therefore required to wait for `work-2`, while `work-1` is forbidden to finish while that route is live. `work-2` can never be scheduled.
- **Impact:** The cross-phase repair for round-1 T5 has incompatible transition rules in two current decision-fold sources. The retained proposal admits no progression for the exact early-work-to-future-owner fixture that the proof and acceptance criteria require, so an implementer must either drop/terminalise the finding or violate the phase-finish rule.
- **Required correction:** State that a current phase may finish with retained `FutureOwnerPending` components and that only family delivery/`Complete` requires all future routes to have activated and settled. Keep prior-owner routes terminal.

### F3 - The published minimum formulas are not scoped away from legal early-terminal paths

- **Severity:** medium.
- **Evidence:** The proof publishes `L_q = n_q + 1` and `L_B = r_plan + |O| + m + 1` as minima (`docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md:104-120`) while also making unowned findings and completed-prior-owner findings immediate terminal routes (`:45,56`) and requiring the oracle to check early terminal paths (`:120`). With `n_q = 1`, the first scheduled batch can retain an unowned finding and enter `TerminalChoice` after one post-freeze batch, which is less than `L_q = 2`; a material-scope or plan-review terminal can end still earlier than `L_B`. The retained safety proposal calls `n_q + 1` a **clean** phase minimum (`docs/plans/workflow-calibration.explorations/Q-86-safety-process.md:342`), but that qualifier is absent from the executable proof's definitions and acceptance criterion 10 (`bounded-convergence-option-b-proof.md:165`).
- **Impact:** A conforming oracle cannot simultaneously compute these as minima over every legal execution and admit the required early terminal paths. It must silently reinterpret the formulas or reject legal states, weakening the algebra gate that authorises later implementation.
- **Required correction:** Define `L_q` and `L_B` explicitly as minima over ordinarily delivering `Complete` paths (and state that terminal/non-delivery paths are outside the lower-bound domain), or publish separate lower bounds for terminal executions. Make the algebra oracle and acceptance criterion assert the same domain.

## Counts

- Critical: 0
- High: 0
- Medium: 3
- Low: 0
- Total: 3
