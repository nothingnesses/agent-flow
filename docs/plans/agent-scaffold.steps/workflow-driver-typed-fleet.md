### `workflow-driver-typed-fleet`: build the workflow driver's typed per-unit fleet on the compact Q-58 carrier (`Q-82`, Stage 2)

This step implements the existing Stage-2 architecture; it does not redesign it. The authoritative scope is the Stage 2 paragraph in `docs/plans/agent-scaffold.steps/workflow-driver.md`, with the detailed build path in `docs/plans/mealy-workflow-driver.explorations/r2-synthesis.md` and `r2-architecture-build-path.md`. Q-82 schedules it after the independent visibility repair.

DEPENDENCIES ARE LOAD-BEARING. `workflow-loop-visibility` must first establish phase-correct plural projection. `q58-output-ablation` must select the compact carrier, and `resume-state-currency-signal` must add Q-59's currency value to it. This step consumes that decided carrier; it does not assume structured-only before the experiment or restore a prose echo by convenience.

THE SCOPE. Extract the loop reconstruction shared by W3 and `next` into one typed function. Add the Stage-2 `src/driver/` fleet: a total `ReviewLoop` Mealy transition, nested step/task machines, full reconstruction of every per-unit loop, and instruction emission from typed state. Judgments enter only through typed inputs; no transition manufactures a triage verdict, risk class or human decision. Preserve `workflow-loop-visibility`'s complete active-loop collection and one selected action.

THE BOUNDARY. No ready-frontier scheduling, parallel fan-out, record/write commands, persistent FSM store or workflow DSL. `workflow-ready-frontier-scheduler` owns the first item; the others retain the YAGNI boundary in `workflow-driver`.

### Increment 1, `workflow-driver-typed-fleet-inc1`

RISK CLASS `risky` (two consecutive clean review rounds). The typed engine becomes the common source for checker and driver state and controls the instruction an agent receives. A divergence can either waive required review or deadlock legal work.

ACCEPTANCE.

1. W3 and the driver call one `reconstruct_loop(rounds, escalations, spec)`-family implementation for streak, class, cap/reset segment and convergence state. A differential suite replays logs and compares forward state with the backward validator verdict.
2. The transition table is total at compile time: every `(state, input)` pair has a defined result or typed rejection, and adding a state/input variant makes the exhaustive test fail to compile until handled.
3. Every output requiring judgment is reachable only from an input carrying that judgment. Red mutations that synthesize a clean verdict, risk class or human choice fail.
4. Reconstruction returns every active unit and preserves each phase established by `workflow-loop-visibility`. No lowest-order filter sits below the fleet; the singular selected action is derived from the fleet afterwards.
5. The selected Q-58 carrier supplies non-derivable `awaiting`, artifact/diff and currency data through a typed boundary. Missing, stale and dirty states are explicit; heuristic prose parsing is forbidden unless the Q-58 decision explicitly selected and bounded a parser, in which case that exact parser is the typed boundary.
6. Golden human and JSON fixtures cover exploration, implementation, first review, fixes, reviewer continuation, convergence, foreclosure/cap escalation, risk conflict, acceptance and terminal states, including multiple simultaneous units.
7. Existing W3/W4/W5 tests and Stage-1 output fixtures remain green or receive reviewed, documented contract migrations. No scheduler or write path appears in the diff.
8. README documents typed reconstruction and the unchanged advisory/read-only authority; `CHANGELOG.md` records the Stage-2 engine. Any pack guidance made stale by emitted-state vocabulary moves with its committed copies.
9. Both validation modes, strict render, tests and differential/red controls, Clippy, diff checks and ASCII checks pass.

### Documentation impact

Update README's driver architecture and machine-output vocabulary, `CHANGELOG.md`, and any generated or pack guidance whose phase/state names change. Do not duplicate the Stage-2 design in a new durable design note; this sidecar records implementation obligations and points to the existing architecture. The Q-58 result remains the source for the carrier choice.
