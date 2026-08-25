### `review-loop-foreclosure-enforcement`: report and enforce review-loop foreclosure and the total-round cap

Decision `Q-78-foreclosure-enforcement` chose `Report and enforce foreclosure plus the round cap`, over report-only and keeping both advisory. The choice already exists in the event log; this step gives it focused Roadmap ownership after the structured class and rebuild-boundary rules land.

THE PROBLEM. `WorkflowSpec` carries `round_cap`, and `next` reports escalation only after a loop reaches it. `validate --workflow` does not enforce the cap. More sharply, a loop can become unable to reach its required consecutive-clean streak before the cap: with rounds used `r`, current clean streak `c`, cap `k` and required streak `q`, foreclosure holds when `k - r < q - c`. Running another review in that state spends a round without any possible converging outcome.

THE APPROACH. Extract one ordered loop-window reconstruction used by `validate --workflow` and `next`. Round and escalation records retain their JSONL line numbers. A scoped escalation is a segment boundary: later rounds for that unit start a new counter window, while prior rounds remain history. Within the active window, compute rounds used, current clean streak, required streak, cap and foreclosure from the structured records and `WorkflowSpec`. Convergence is checked first, then foreclosure, then cap, preserving the existing precedence.

ENFORCEMENT BOUNDARY. `next` reports `escalate` as soon as the active window is foreclosed or reaches the cap without convergence, with a reason that distinguishes the two. `validate --workflow` rejects: a foreclosed active window with no following scoped escalation; a cap-reached unconverged window with no following scoped escalation; and any window containing more rounds than the cap. A joined escalation closes that violation and resets the next segment. Historical rounds before the boundary never count against the new segment.

### Increment 1, `review-loop-foreclosure-enforcement-inc1`

RISK CLASS `risky` (two consecutive clean review rounds). This turns an advisory safety limit into a hard workflow invariant and can make trees that validate today fail, a cost the human explicitly accepted. It touches the checker and the action a driver recommends, so a defect either blocks valid work or permits review beyond the authorised cap.

ACCEPTANCE.

1. A shared typed reconstruction consumes ordered rounds and escalations plus `WorkflowSpec`; `next` and the workflow validator do not maintain separate formulas. A differential test compares both consumers over the same fixtures.
2. Table tests cover: converging on the cap (convergence wins); exactly enough rounds remaining (not foreclosed); one fewer round remaining than needed (foreclosed); cap reached unconverged; a sixth round without escalation (invalid); a scoped escalation followed by a fresh valid segment; and an escalation for another unit (no reset).
3. Risk-class inconsistency remains a data fault and is evaluated before foreclosure arithmetic. A waiver cannot suppress it, foreclosure or an over-cap segment.
4. Human and JSON `next` outputs distinguish `foreclosed` from `cap reached`, preserve one actionable escalation, and carry the human-input-contract reminder. Neither state spawns another reviewer.
5. `validate --workflow` messages name the step/increment, segment round count, current/required streak and cap. A malformed or unjoined escalation cannot reset a window.
6. Existing Q-78 and other historical multi-segment loops validate by joining their recorded escalation boundaries; no test deletes or rewrites history to make the check green.
7. `src/workflow_spec.rs` no longer calls the cap advisory-only. README's cap-labelled diagram remains value-free and accurate; help text and JSON docs change if their stated contracts now omit a new reason/state.
8. `CHANGELOG.md` records the new enforcement and that a previously valid over-cap or foreclosed active history may fail until its real escalation boundary is recorded.
9. Both validation modes, strict render, all tests including red mutations, Clippy, diff checks and ASCII checks pass.

### Documentation impact

Update the `WorkflowSpec` code comments, CLI/help or README JSON vocabulary that enumerates `next` reasons, the pack guidance if it describes cap handling without the new early-foreclosure branch, and `CHANGELOG.md`. The README Mermaid diagram already names a cap-triggered escalation without duplicating the numeric value; keep that correct summary and add only the foreclosure edge if omission would make the diagram materially false. `pack/instrument.md` already documents rounds and escalations and needs a semantic note about a scoped escalation resetting the enforced window, not a new record type.
