### `q58-output-ablation`: run the existing Q-58 output-content ablation and select the compact resume carrier

This is the reopened Q-58 experiment, not a product implementation. The human chose `Reopen Q-58 and run the ablation` on 2026-08-25 after a current `next` run emitted 727754 bytes. The earlier 2026-07-24 shelf decision was conditional on the source-side boundary holding output near 6 KB; that premise is now historical. Q-58 remains `exploring` while this step runs.

THE INPUT DESIGN HAS ONE HOME. Run `docs/plans/code-value-audit.explorations/Q-58-ablation-design.md`; do not replace it with a second variant or scoring design here. Before execution, reconcile its cited `src/next.rs` anchors and its old byte baselines with the current tree, recording every moved anchor and current measurement in the result rather than rewriting the retained design as though it had been run today. Keep its oracle-circularity limit: the experiment can measure the resume carrier's value, not independently prove the ACTIVE LOOP action that supplies its own Tier-A oracle.

THE OUTPUT. Write the durable result to `docs/plans/code-value-audit.explorations/Q-58-ablation-result.md`. It records the sampled states, fresh-agent/model matrix, trial count selected before results are read, raw output/token costs, oracle scores, confidence intervals, per-state deltas, the Pareto frontier, threats to validity and the cheapest carrier on the task-success plateau that carries Q-59's currency signal. Raw experimental fixtures and scripts stay in owned scratch unless a result depends on them for reproduction; any retained data file is named from the result.

THE DECISION BOUNDARY. The experiment produces an option set for the human; it does not silently pick a carrier in code. Before this step completes, Q-58 moves from `exploring` to `open`, the options are presented through the human-input contract, and the human decides the compact carrier. That later receipt, not this planning pass, authorises product implementation. `resume-state-currency-signal` and `workflow-driver-typed-fleet` remain blocked until the chosen carrier is durable.

### Increment 1, `q58-output-ablation-inc1`

RISK CLASS `risky` (two consecutive clean review rounds). The increment changes no product code, but its result selects the carrier used by resume, the currency signal and the typed driver. A false result commits several later steps to the wrong substrate and is expensive to unwind; the high-leverage decision, not code blast radius, sets the class.

ACCEPTANCE.

1. The result reproduces the 727754-byte motivating run or explains, with the exact command, source commit and input paths, why the current measurement differs. It reports bytes, lines and tokens; no old 6 KB or 150145-byte figure is used as a current pass condition.
2. Every design variant that remains representable is run. A dropped or changed variant is named with evidence from the current source. V4 remains the oracle-circularity control unless the result demonstrates a stronger independent control.
3. Each comparison uses fresh consuming agents, a fixed structured response request, a predeclared scoring rule, stratified derivable and transient states, and at least two model classes as the retained design requires. The result reports trial count and variance rather than one draw.
4. Tier-B truth comes from git reality and not from the resume prose under test. The Q-59 currency gate is scored on every carrier candidate.
5. The selected knee is reproducible from retained aggregate data, and the result states what the experiment cannot conclude. A carrier is not declared superior when its confidence interval does not support that claim.
6. No file under `src/`, `tests/`, `pack/` or `Cargo.toml` changes. The changed paths are the result and any explicitly retained experiment data, followed by the planner-authored Q-58 question/step/dependency updates and decision receipt needed to open and decide Q-58.
7. Both validation modes, strict render check, tests, Clippy, diff checks and ASCII checks pass after the result and decision fold.

### Documentation impact

The experiment updates Q-58's structured ask, its durable result, the selected-carrier language in `resume-state-currency-signal`, the Stage-2 gate in `workflow-driver-typed-fleet`, and the corresponding Success Criteria. It changes no shipped behaviour, so it owes no README or changelog entry. The later carrier implementation owns those product-doc updates.
