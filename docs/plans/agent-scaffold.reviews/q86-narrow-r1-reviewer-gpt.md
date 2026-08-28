# Narrowed Q-86 round 1 review — scope fidelity and safety gate

Reviewed `main...aec61700` as a risky decision artifact. I checked the narrowed brief and synthesis, Q-88 decision and exact receipt, all five prior Q-86 triages, the structured plan sources and generated projection, the blocking/failure paths, the retained proposals and prototype boundaries, and documentation currency.

## Finding 1 — The retained state-machine proposal still asserts the invalid arbitrary-finite proof in the present tense

- **Severity:** medium
- **Evidence:** `docs/plans/workflow-calibration.explorations/Q-86-state-machine.md:438` correctly says the retained checker exercises only a finite subset and is incomplete because of its global retained-map cap and missing products. Two lines later, `docs/plans/workflow-calibration.explorations/Q-86-state-machine.md:440` still says “Arbitrary finite maps follow by induction” and asserts that adding an owner cannot make delivery easier. That is the exact composition claim invalidated by `docs/plans/agent-scaffold.reviews/q86-synthesis-r5-triage.md` T1 and contradicted again within the proposal at `Q-86-state-machine.md:233`, which records that settled identities consume the cap, remove later transitions, and can make completion easier. Reproduce the contradiction with `rg -n 'Arbitrary finite maps follow|does not establish arbitrary-finite' docs/plans/workflow-calibration.explorations/Q-86-state-machine.md`.
- **Consequence:** A human following the retained proposal reaches an affirmative proof claim immediately before the executable commands even though the narrowed decision artifact says the prototype is not proof. The document-level historical-status disclaimer mitigates the risk but does not make this mutually contradictory, present-tense derivation safe decision material. It breaches the narrowed requirement that no human-facing claim treat the prototype as proof.
- **Correction:** Replace line 440 with the finite-subset limitation and the withdrawn-composition result, pointing arbitrary-finite composition to the mandatory selected-option proof obligation. Do not complete or demand proofs for the unselected controllers now.

## Finding 2 — The narrowed synthesis falsely says the generated plan did not change

- **Severity:** low
- **Evidence:** `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:7` says no “generated plan” changes in this pass. `git diff --name-only main...aec61700` includes `docs/plans/agent-scaffold.md`, and `nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml` confirms that file is the current generated projection. The same diff also appends the Q-88 event to `docs/metrics/workflow.jsonl`, so the broad “metric” wording is at least ambiguous even though no metrics schema or behavior changed.
- **Consequence:** The decision boundary inaccurately describes its own artifact and weakens documentation-currency accounting. This does not alter workflow behavior, but it repeats the generated-plan boundary error previously adjudicated in round 2.
- **Correction:** State that no current workflow or production behavior changes, while explicitly allowing the planning-source edits, Q-88 event append, and required generated-plan projection.

## Counts

- Critical: 0
- High: 0
- Medium: 1
- Low: 1
- Total: 2

I found no unresolved high-severity claim that still changes the architecture choice rather than belonging to the explicitly deferred selected-option controller proof. Q-88 has exactly one receipt with the six labels in the recorded order and exact recommendation/chosen value. Q-86 is `open`, Q-88 is `decided -> folded into workflow-calibration`, `workflow-calibration` remains `in progress`, the Success Criterion carries the blocking proof gate and failure path, no fallback architecture or floor is automatic, no production or pack path changed, strict render passes, and workflow validation passes with 485 records, 114 steps, and 88 questions.
