# Narrowed Q-86 round 4 triage

## Scope, reproduction, and no-relitigation

I independently triaged the risky narrowed Q-86 decision artefact. I read `AGENTS.md`, `.agents/prompts/triager.md`, Q-86/Q-88 and their structured records, the narrowed synthesis, both retained proposals and prototypes, the ledger's narrowed-Q-86 record, all three prior narrowed triages, and both round-4 reviewer reports. I did not change the reviewed product, plan, metrics, or earlier review records.

`nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml` passed. `nix develop -c cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` passed with 488 valid metrics records, 114 steps, 88 questions, and workflow invariants holding. `git diff --check b6fb2ff6...HEAD` passed.

I reproduced the four raw low-severity claims. The floor blocks at `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:209-217` and `docs/plans/agent-scaffold.questions/Q-86.md:31-37` each return zero matches for all eight Project-Principle names. The structured Q-86 ask has the same bare floor recommendation at `docs/plans/agent-scaffold.plan.toml:2575-2578`. B explicitly inherits A's plan controller at `Q-86-synthesis.md:103`, while the comparison and recommendation omit the inherited account/reserve and weakly calibrated five-plus-two cost at `:169-184`; the retained source identifies those inherited constants at `Q-86-safety-process.md:324,515`. Finally, the human-facing sidecar uses `n_q`, `r_plan`, `|O|`, and `m` at `Q-86.md:7-9` without defining them; the structured ask likewise leaves `n_q`, `O`, and `r_plan` unglossed at `agent-scaffold.plan.toml:2565-2566`. Their definitions are only in the synthesis at `Q-86-synthesis.md:79,93,103-105`.

The two floor reports are duplicates. None of the three consolidated findings re-raises a settled verdict without new evidence: synthesis round-1 T6 made the floor visible; this is the distinct current failure to supply the required Principle-judged recommendation. Narrowed round-3 T2 corrected B's plan/post-freeze cost-table classification; this is the distinct, still-unreviewed comparison and recommendation rationale. The current sidecar/queue-symbol omission is direct evidence that the earlier controller-definition repair was not made self-contained on the human-facing decision path.

## Verdicts

### T1 — serious-floor recommendation lacks Principle-judged reasoning

- **Source IDs:** Claude finding 1; GPT finding 1.
- **Verdict:** valid, **low**.
- **Reasoning:** `AGENTS.md:41` requires every human-input point to provide a recommendation and reasoning judged against Project Principles by name; `AGENTS.md:65` applies that contract to the decision artefact. The serious floor is an explicit human co-decision, not a trivial confirmation. Its options and operational consequences are clear, and the selected-option proof still models both floors, so the omission cannot grant implementation authority or hide an untested transition. It does, however, leave the `high` recommendation's safety/cost trade-off unexplained.
- **Correction:** Add a concise Principle-named comparison and rationale for `high` to the synthesis, Q-86 sidecar, and structured Q-86 ask, then re-render. It should explain both the safety case for making an open high non-deliverable and the evidence/minimality cost of restricting the Q-78 pass-three-through-six cases.

### T2 — B's comparison and recommendation understate its inherited plan-review costs

- **Source ID:** Claude finding 2.
- **Verdict:** valid, **low**.
- **Reasoning:** B does not replace A's plan-review controller; it reuses it. The Principle table charges the account/reserve model and weakly calibrated five-plus-two values only to A, and the recommendation contrasts B with A as though B did not retain that controller. This is a one-sided omission in the material offered to justify the recommendation. The inheritance and correct cost bounds are stated elsewhere, so no bound is wrong and the impact is documentation/decision-readiness only.
- **Correction:** In B's relevant Principle-table cells and recommendation/confidence rationale, state that B inherits A's sealed plan-review controller, including its account/reserve model and weakly calibrated five-plus-two values. Propagate the concise qualification to the Q-86 sidecar and structured ask without changing published bounds.

### T3 — Q-86 human-facing formulas use undefined symbols

- **Source ID:** Claude finding 3.
- **Verdict:** valid, **low**.
- **Reasoning:** The Q-86 sidecar and queue projection are the human decision path, but neither lets a reader evaluate B's minimum and maximum costs without opening the synthesis. `r_plan` is particularly opaque; `n_q`, `O`, and `m` are also not formally glossed there. This is the same self-contained decision-material class as prior cost-vocabulary corrections, but on the current sidecar and structured ask. The formulae agree with the synthesis and no calculation is false, limiting the severity to low.
- **Correction:** Define the terms at their first human-facing use in Q-86 and the structured ask: `m` as the work-loop count; `O` as the frozen canonical obligation set; `n_q = |O_q|` as the count owned by post-freeze phase `q`; and `r_plan` as the inherited plan-review clean-batch count (one low-risk, two risky). Re-render the generated projection.

## Outcome and counts

**Outcome: `new_valid`.** Four raw low findings deduplicate to **three valid low findings**: critical 0, high 0, medium 0, low 3, invalid 0. No residual risk was accepted. This risky narrowed artefact remains at a clean streak of 0 of 2; the orchestrator records the round total and next action in the ledger.

## Backstop

No high- or critical-severity finding was dismissed. **No independent dismissal backstop re-check is owed.**
