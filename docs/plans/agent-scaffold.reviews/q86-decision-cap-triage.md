# Q-86 decision-fold cap verification triage

## Scope and reproduction

I independently read `AGENTS.md`, `.agents/prompts/triager.md`, Q-92, the round-5 triage, the proof and scheduler authorities, and both focused reviews. The reviewed planning artefact is content-identical to focused-review tip `9555d64d` for the proof step, scheduler sidecar, plan source/projection, and Q-92.

The ordinary gates reproduce on this tip:

```text
nix develop --command cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml
# docs/plans/agent-scaffold.plan.toml: up to date
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl
# docs/metrics/workflow.jsonl: 503 records, valid
# docs/plans/agent-scaffold.plan.toml: 115 steps, 92 questions, valid
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow
# workflow invariants hold
git diff --check 30e5246e..HEAD
# exit 0
```

Those gates do not exercise the future proof programs. The focused Claude review raised two low findings; focused GPT raised zero.

## Verdicts

### T1 — The mutation-result join is not observable through the specified traceability contract

- **Source:** Claude Finding 1.
- **Verdict:** valid, **low**.
- **Reproduction:** The required join says the traceability checker resolves every executable row to one manifest entry *and that run's* exercised-and-killed result (`docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md:184`). Its prescribed command receives only the matrix and five triages, not a manifest or result source (`:206`); the separately invoked mutation runner follows it (`:207`). Each invocation has fresh external state, both states are removed, and no repository artifact may be created (`:212-214`). The pinned traceability summary exposes only `valid_findings=51` and `unresolved=0`, while the mutation summary exposes only `survived=0` and tag counts (`:210`). Although `:194` requires mutations of the checker, it does not define a result handoff or an observable traceability assertion for this join.
- **Reasoning:** The specification states the intended safety property, but it does not make the checker’s consumption of a real mutation result or the result of that join independently checkable. A checker can retain the stipulated parser summary while omitting the result join; a separate later runner cannot supply it across the required isolated invocations. An in-process shared runner would be a viable design, but it is not selected or required, and no required traceability result identifies the resolved/exercised/killed rows. This leaves the round-5 T2 repair without the observable verification required by Principles 6 and 11. The impact is limited to traceability attribution because manifest-wide mutation coverage remains separately required, so low is proportionate.
- **Required correction:** Specify one result flow for the checker—either a named result input produced and consumed in the same temporary invocation, or an explicit shared in-process runner—and require the traceability command to report and assert the resolved/exercised/killed row result. The checker mutation controls must exercise that flow and fail for unknown, surviving, and unexercised names.

### T2 — The scheduler provenance entry is not task-relative

- **Source:** Claude Finding 2.
- **Verdict:** valid, **low**.
- **Reproduction:** The Q-92-authored scheduler provenance entry is `"docs/plans/agent-scaffold.reviews/q86-decision-r5-triage.md"` (`docs/plans/agent-scaffold.plan.toml:1782`), while the same evidence on the proof step is `"agent-scaffold.reviews/q86-decision-r5-triage.md"` (`:1806`). `Provenance.findings` is documented and diagnosed as a task-relative path (`src/plan/source.rs:245-247,643-649`). From `docs/plans/`, the scheduler spelling points at the absent `docs/plans/docs/plans/agent-scaffold.reviews/q86-decision-r5-triage.md`; the proof spelling points at the existing retained finding. In a temporary copy, replacing the scheduler entry with another safe but nonexistent task-relative path still made `validate --source` exit 0, confirming that validation shape-checks rather than resolves this historical pointer.
- **Reasoning:** The safe-path check properly permits a contained string but does not change the field’s documented resolution convention. This directly applies, rather than reopens, round-5 T4’s settled convention. The entry was authored as part of the Q-92 repair, so correcting its form is direct residue; the older sibling spellings are outside this focused scope. It is a durable evidence-navigation defect, not an execution defect, so low is proportionate.
- **Required correction:** Change `docs/plans/agent-scaffold.plan.toml:1782` to `agent-scaffold.reviews/q86-decision-r5-triage.md` and re-render the projection. Normalising the pre-existing sibling entries is separate scope.

## Outcome, counts, and backstop

**Round outcome: `new_valid`.** Raw reviewer findings: **2** from Claude and **0** from GPT. Deduplicated triage verdicts: **2 valid low** findings; **0** invalid; **0** critical, high, or medium; no residual risk accepted.

No high- or critical-severity finding was dismissed, so the independent dismissal backstop is **not owed**.

Q-92 authorises closure only if the focused verification reports no new valid finding (`docs/plans/agent-scaffold.questions/Q-92.md:34`). It therefore **does not close**: its one focused verification has produced two valid direct-residue findings and must return to the human for a decision; do not merge or start another focused verification under Q-92 automatically.
