# Q-78 acceptance pass 2 triage

## Scope and verification

I independently read both pass-2 reports, the current TOML plan and relevant sidecars, the first acceptance triage and repair brief, Q-58/Q-80/Q-82, the retained Q-58 design, Success Criteria, and the live ledger anchor. The reviewed planner repair is `ef20d87`, an ancestor of this branch.

Using an isolated Rust 1.95.0 toolchain and scratch-only target/Cargo directories, I reproduced these gates:

- `validate --source docs/plans/agent-scaffold.plan.toml`: `463 records, valid`; `113 steps, 82 questions, valid`.
- `validate --workflow --source docs/plans/agent-scaffold.plan.toml`: `workflow invariants hold`.
- `render --check --strict docs/plans/agent-scaffold.plan.toml`: `up to date`.
- `next --source docs/plans/agent-scaffold.plan.toml`: 730209 human-output bytes; JSON is 733192 bytes and still selects `workflow-calibration` as `in progress` / `awaiting-first-review`.
- `git diff --check main...HEAD`: passed.

I found no duplicate finding between the reports: their two reconstruction findings concern different defects (future reuse/dependency versus the historical over-cap record). No finding is invalid or accepted as residual. No high or critical finding is dismissed, so no independent dismissal re-check is owed.

## Verdicts

### R2-G1 — valid, `medium`: the proposed phase carrier cannot represent legal plan-review or acceptance states

`workflow-loop-visibility` requires `workflow_phase` only on an `in-progress` Roadmap step and forbids it otherwise, while it promises `plan_review` and `acceptance` among the phases (`docs/plans/agent-scaffold.steps/workflow-loop-visibility.md:7,17`). It projects only `in-progress` steps (`:9`). A plan review occurs before an implementation step need be in progress, and acceptance occurs after implementation work is complete; neither legal task-level state has the required carrier. The fixture requirements consequently cover neither state despite Success Criterion 39 requiring all four phase families (`docs/plans/agent-scaffold.success-criteria.md:39`).

This can dispatch no phase-correct action during acceptance, rather than merely omitting a display detail. Add a typed task-scoped carrier (or an equivalent typed active-work union) for plan review and acceptance, state who advances it, and test every phase from a workflow-legal state. Do not fake either phase by changing an implementation step's status.

### R2-G2 — valid, `medium`: the typed fleet is not required to reuse the earlier loop reconstruction

The foreclosure step owns extraction of the ordered reconstruction shared by `validate --workflow` and `next` (`docs/plans/agent-scaffold.steps/review-loop-foreclosure-enforcement.md:7,17`); the later fleet says it will extract the same W3/`next` reconstruction again (`docs/plans/agent-scaffold.steps/workflow-driver-typed-fleet.md:7,17`). Yet `workflow-driver-typed-fleet` is blocked only by visibility and currency, not foreclosure (`docs/plans/agent-scaffold.plan.toml:1719-1723`). Array order is not a reuse contract.

Add the foreclosure step as a load-bearing dependency and change the fleet scope/criteria to consume and extend that reviewed reconstruction. This is separate from R2-C1: it prevents future duplicate arithmetic even after the historic-cap policy is made satisfiable.

### R2-G3 — valid, `medium`: the Q-58 carrier-selection rule remains under-specified before results

The retained design defines the knee with an unspecified `epsilon` and overlapping confidence intervals (`docs/plans/code-value-audit.explorations/Q-58-ablation-design.md:62-67`). It leaves the confidence method/level, cross-model aggregation, and disagreement rule unspecified despite requiring per-model results (`:55-60,88`). The reopened step requires a predeclared scoring rule and variance but does not bind those degrees of freedom (`docs/plans/agent-scaffold.steps/q58-output-ablation.md:17-21`).

Without a committed pre-run margin, interval/test method, aggregation/weighting rule, and model-disagreement rule, the same results can select different carriers post hoc. Keep the retained design and its oracle-circularity boundary, but require those values in a committed pre-run protocol (the result file may be opened and committed before the first trial) and make the knee mechanically reproducible from its retained aggregate data.

### R2-G4 — valid, `medium`, orchestrator-owned: `RESUME HERE` is stale after the completed planner repair

The live anchor still directs a planner to repair T1–T7 and describes Q-80 as open (`docs/plans/agent-scaffold.ledger.md:535-545,549`). The repair is already an ancestor of this branch; T1's JSONL waiver is absent, and Q-80 is `decided -> review-loop-class-inheritance` (`docs/plans/agent-scaffold.plan.toml:2442-2459`). A resumer following the required plan-and-ledger reconstruction would repeat reviewed planner work rather than continue this acceptance pass.

This is a durable-state failure, not planner-owned product content. The orchestrator must directly replace the live anchor with the completed-repair/current-acceptance state, identify the current pass and triage action, and make the obsolete planner instructions explicitly historical. Do not send this disposition to a planner or create a Roadmap step for it.

### R2-G5 — valid, `low`: the canonical workflow-driver architecture contradicts the scheduled Q-82 stages

`workflow-driver` still claims the umbrella is not started and has no increments (`docs/plans/agent-scaffold.steps/workflow-driver.md:3`), despite its TOML entry being `in-progress` with Stage 0a/0b/1 increments (`docs/plans/agent-scaffold.plan.toml:681-700`). It also leaves Stage 3 behind a real-parallel-execution gate (`workflow-driver.md:15,21`) while its Q-82 handover schedules the Stage-3 scheduler (`:23`) and Q-82 chose staged scheduling (`agent-scaffold.plan.toml:2479-2485`).

Correct the canonical architecture to use phase-neutral current wording and state how Q-82 replaces the former scheduler gate. Keep detailed implementation requirements in the focused successor sidecars; this is a documentation-currency correction, not a second architecture.

### R2-C1 — valid, `medium`: the new over-cap rule would reject unrepaired current history

The foreclosure step promises to reject any window with more rounds than the cap and says existing Q-78 history validates through recorded escalation boundaries (`docs/plans/agent-scaffold.steps/review-loop-foreclosure-enforcement.md:9,22`). I replayed the log: `q78-design-pass` has eight rounds, including seven `plan_review` rounds at `docs/metrics/workflow.jsonl:380-386`, and zero escalation records. It has no Roadmap step either. The round artifacts themselves describe escalations, but there is no `type:"escalation"` event to join. The cap is five.

Therefore the proposed "any window" enforcement makes its own criterion 6 false. Before implementation, define the treatment of non-Roadmap/historical loops and either append evidence-backed records for the real historical escalation boundaries or state a justified scope that excludes them. Do not silently narrow the implementation or delete history merely to obtain a green test.

### R2-C2 — valid, `medium`: shipped instrumentation guidance still tells TOML-primary projects to write JSONL waivers

`pack/instrument.md:11` presents `type:"waiver"` as a live JSONL record and is shipped into `AGENTS.md` and `.agents/AGENTS.reference.md`. A fresh scaffold is TOML-primary (`pack/plan-template.plan.toml:13-15`), and the TOML workflow path consumes waivers from `waivers_from_toml(plan)` while it reads JSONL only for rounds, decisions, and escalations (`src/workflow.rs:171-193`). Thus a scaffolded orchestrator following the current text writes an inert JSONL waiver, contrary to the event-only log Success Criterion (`docs/plans/agent-scaffold.success-criteria.md:18`).

T1 removed one bad record but not this reusable cause. Give the TOML waiver home and the legacy/Markdown qualification one canonical, shipped explanation; update its committed copies through the normal pack path. The disposition needs focused Roadmap ownership (or an explicit documented extension), not another JSONL waiver.

### R2-C3 — valid, `low`: the precise 727754-byte premise has no reproducible provenance

The exact value is repeated as a current measurement in Q-58, Q-82 and their owning sidecars (`docs/plans/agent-scaffold.plan.toml:2139,2479,2485`; `docs/plans/agent-scaffold.steps/q58-output-ablation.md:3,17`). The current reproduction instead yielded 730209 bytes with `next --source docs/plans/agent-scaffold.plan.toml`; no cited command, commit, working directory, or input paths identify the earlier 727754-byte run. The later ablation criterion correctly anticipates a changed measurement, but that does not source the present-tense decision evidence.

This does not block the experiment once its own criterion 1 remeasures the output, but it fails the grounding/documentation-currency bar now. Cite the historical measurement precisely, or replace the exact current claim with a bounded historical statement and a pointer to the reproducible current measurement. Keep a single source for the measured premise rather than copying a new fixed total.

### R2-C4 — valid, `low`: the structured-risk changed-path criterion has an impossible count

`structured-risk-class-source` enumerates seven guidance/template files plus `CHANGELOG.md` (`docs/plans/agent-scaffold.steps/structured-risk-class-source.md:15-18`), eight paths total. Criterion 4 calls this "the eight guidance/template files named above plus `CHANGELOG.md`" (`:25`), yielding a nonexistent ninth path. This is the exact-path false-refusal class the preceding acceptance repair was intended to eliminate.

Correct the count to seven guidance/template files plus `CHANGELOG.md` (or otherwise make the enumeration and criterion match). No scope expansion is required.

### R2-C5 — valid, `low`: the predecessor handover still says its successor is un-authored

The predecessor says the successor is "a planner's to author" (`docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md:116`), but `sidecar-status-authored-openings` is present with an increment and a declared dependency (`docs/plans/agent-scaffold.plan.toml:1689-1700`; `docs/plans/agent-scaffold.steps/sidecar-status-authored-openings.md:1-22`). The forward link is therefore stale, and the successor's documentation-impact statement does not notice it.

Replace the obsolete future-tense handover with the successor slug and preserve the historical rationale for refusing a stub. This is distinct from R2-G5: it repairs the Q-78 handover, not the driver architecture.

## Result

All ten deduplicated pass-2 findings are valid: six `medium` and four `low`. R2-G4 is an orchestrator-owned direct ledger correction; the other nine return to planning for a focused revision before the next acceptance pass. No residual risk was accepted.
