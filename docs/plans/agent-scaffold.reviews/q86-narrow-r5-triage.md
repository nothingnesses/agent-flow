# Narrowed Q-86 round 5 triage

## Scope and reproduction

I independently triaged the risky narrowed Q-86 decision artefact at `main...HEAD` (`2c58cffd...4d0d737b`). I read `AGENTS.md`, the triager prompt, the Q-86/Q-88 structured records and sidecars, the narrowed synthesis, the mapped state-machine proposal, the workflow-calibration record, the narrowed round-1 through round-4 triages and records, and both round-5 reviews. I did not change the reviewed product, plan, metrics, or earlier findings.

`nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml` passed. `nix develop -c cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` passed with 489 valid metric records, 114 steps, 88 questions, and workflow invariants holding.

I reproduced all three raw low claims. The two floor reports name the same defect: the eight `[[principle]]` entries at `docs/plans/agent-scaffold.plan.toml:2617-2657` do not contain `Make failure and absence explicit` or `Correctness before performance`, while the three live floor-recommendation surfaces use both names at `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:217`, `docs/plans/agent-scaffold.questions/Q-86.md:37`, and `docs/plans/agent-scaffold.plan.toml:2580`. For C, the narrowed synthesis states only the four-batch/fifteen-call maximum at `Q-86-synthesis.md:139`; its local two-reviewer allocation is expressly a minimum at `:146`. The provenance map at `:15` points C to state-machine Candidate B, whose five reviewer passes, four triages, four backstops, and two repairs total fifteen at `Q-86-state-machine.md:312`.

## Deduplication and no-relitigation

There are three raw low reports and two unique findings. Claude finding 1 and GPT finding 1 are duplicates. Claude finding 2 is distinct.

The floor finding is post-round-4 evidence from the applied repair, not a re-raise of round-4 T1's former absence of any Principle-named rationale. The C finding concerns the maximum allocation. Narrowed round-1 T4 required only C's three-reviewer minimum; it did not adjudicate the maximum. The earlier triages contain no settled maximum-allocation verdict, so neither valid finding reopens a settled result without new evidence.

## Verdicts

### T1 — the serious-floor rationale uses names outside the plan's Project-Principle set

- **Source IDs:** Claude finding 1; GPT finding 1.
- **Verdict:** valid, **low**.
- **Reasoning:** The human-input contract requires the recommendation to be judged against the plan's Project Principles by name. The recommendation's cost half does that with Ground decisions in evidence and Minimal by default, but its affirmative case cites two AGENTS guidance principles outside the plan's authoritative eight-principle set. The options, fail-closed consequence, proof gate, and human authority remain clear, so this is a decision-material defect rather than a safety or implementation-authority defect.
- **Correction:** State the affirmative case using applicable plan principles, for example Make illegal states unrepresentable (an open high has no delivery state) and Safe on existing projects (the stricter boundary fails closed), preserve the existing evidence/minimality cost, mirror the corrected rationale to all three source surfaces, and render the projection.

### T2 — C's maximum lacks a local allocation derivation

- **Source ID:** Claude finding 2.
- **Verdict:** valid, **low** (with one evidentiary correction).
- **Reasoning:** The mapped proposal does establish the published fifteen-call maximum as `5 + 4 + 4 + 2`, but the narrowed decision artefact itself supplies only C's result and its minimum allocation. A reader therefore cannot reconstruct the headline maximum without following the provenance map. That is the same self-contained decision-material gap as the earlier accepted allocation and symbol fixes. The reviewer's claimed contradiction does not reproduce: A's two-reviewer/one-triage/one-re-check composition at `Q-86-synthesis.md:87` is explicitly Option A's allocation, not a generic rate that C must inherit. The valid defect is the local omission, not a false `15` bound. Its impact remains low because the mapped source supplies the correct derivation, the option ranking is unchanged, and the selected-option proof gate separately requires every selected bound to be proved.
- **Correction:** Add C's maximum allocation beside `Q-86-synthesis.md:139`: four batches with five reviewer passes (two at Discovery and one each at Verify1, Verify2, and BlindClosure), four triage calls, four backstop calls, and two repair passes, hence fifteen. Do not change the published bound.

## Outcome, cap, and backstop

**Outcome: `new_valid`.** Three raw low reports deduplicate to **two valid low findings**. Counts: critical 0, high 0, medium 0, low 2, invalid 0.

This is narrowed round 5. The artifact is recorded as risky, so it requires two consecutive clean rounds; rounds 1 through 4 were all `new_valid` with clean streak zero, and this round is also `new_valid`. The total reaches the five-round cap and cannot converge. Under the recorded cap rule, the orchestrator must escalate to the human; no sixth ordinary review round is legal before that decision.

No high- or critical-severity finding was dismissed. **No independent dismissal backstop re-check is owed.**
