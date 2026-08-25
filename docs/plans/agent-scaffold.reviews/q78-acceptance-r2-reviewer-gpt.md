# Q-78 acceptance pass 2 - GPT reviewer

## Verdict

Five acceptance shortfalls: four `medium`, one `low`. T1 through T7 are closed, all thirteen original Q-78 increment identities retain their convergence evidence or authorised waiver, and Q-78 remaining `open` is not a finding.

The repaired step-intent product is internally consistent. The remaining shortfalls are in the newly scheduled Q-58/Q-82 work and the durable documentation that should describe the current branch.

## Shortfalls

### R2-G1 - `medium`: the phase field cannot represent legal plan-review or acceptance states

The new Success Criterion requires `next` to distinguish exploration, implementation, review and acceptance (`docs/plans/agent-scaffold.success-criteria.md:39`). The owning step puts the phase field on an `in-progress` Roadmap step, requires it exactly in that status, forbids it on every other status, and constructs `active_loops` only from in-progress steps (`docs/plans/agent-scaffold.steps/workflow-loop-visibility.md:7-9`, `:17`).

That representation has no legal carrier for two phases it promises. Plan review occurs before phase-4 Roadmap implementation begins, and acceptance begins only when no pending Roadmap step remains (`AGENTS.md:32-35`). In the ordinary acceptance state every implementation step is complete; the proposed field is forbidden on all of them, and the proposed `active_loops` collection therefore has no acceptance unit. A plan-review fixture can only be made to pass by falsely marking an implementation step in progress. The criterion fixture covers exploration, implementation and two review rows, but never constructs plan review or acceptance from their legal task-level states (`workflow-loop-visibility.md:18-22`). The later fleet nevertheless promises an acceptance fixture (`workflow-driver-typed-fleet.md:22`), so it inherits the impossible input.

This is ground-blind: an implementation can enforce every status/field combination and pass every named visibility criterion while returning no active unit during acceptance. It then fails the Success Criterion and can emit no acceptance action. The phase source must represent task-scoped plan review and acceptance separately from step-scoped implementation/work review (or use another typed active-work carrier that represents both), define who advances it, and test every phase from a workflow-legal state.

### R2-G2 - `medium`: two steps own the same shared loop reconstruction without a dependency or reuse boundary

`review-loop-foreclosure-enforcement` explicitly owns extraction of the one ordered reconstruction shared by `validate --workflow` and `next`, including rounds, escalation segments, streak, cap and foreclosure (`docs/plans/agent-scaffold.steps/review-loop-foreclosure-enforcement.md:7`, `:17-22`). The later typed-fleet step again says to extract the W3/`next` reconstruction and again owns a `reconstruct_loop(rounds, escalations, spec)` family covering streak, cap/reset segments and convergence (`docs/plans/agent-scaffold.steps/workflow-driver-typed-fleet.md:7`, `:17`).

The Roadmap puts foreclosure earlier but does not connect those owners: the fleet is blocked only by visibility and the resume-state currency signal (`docs/plans/agent-scaffold.plan.toml:1718-1724`), not by foreclosure enforcement. Thus reuse is implicit in today's mutable array order rather than encoded in the typed dependency graph, and the plan never tells the fleet implementer to consume the function the earlier step lands. Following both scopes literally permits two reconstructions or a second extraction/refactor over the first, contrary to the one-arithmetic architecture and Q-82's claim that its dependencies make the sequence durable (`agent-scaffold.plan.toml:2485`).

Make `workflow-driver-typed-fleet` depend on `review-loop-foreclosure-enforcement`, and change its scope and criteria from extracting the arithmetic again to reusing and extending the already reviewed reconstruction for the Stage-2 fleet. The driver architecture should remain the single design source; this correction needs no duplicate design note.

### R2-G3 - `medium`: the reopened Q-58 experiment still has no predeclared statistical decision rule

The retained design defines the knee as a score within an unspecified `epsilon` of V0 with overlapping confidence intervals (`docs/plans/code-value-audit.explorations/Q-58-ablation-design.md:62-67`). It specifies neither epsilon, confidence level/interval method nor a rule for resolving disagreement between the per-model results it requires (`:53-60`, `:88`). Overlapping confidence intervals are also not, by themselves, a predeclared equivalence or non-inferiority test.

The reopened step predeclares the trial count and score, requires confidence intervals, and asks for a reproducible plateau, but does not close any of those selection degrees of freedom (`docs/plans/agent-scaffold.steps/q58-output-ablation.md:7`, `:19-21`). A result can run every required trial and then choose an epsilon that places V3 on the plateau; the same aggregate data with a smaller post-hoc epsilon selects V2 or V0. Both reports can satisfy the present criteria, so the experiment does not deterministically produce the evidence on which the carrier decision is meant to rest.

Before results are read, require the result protocol to fix the non-inferiority/equivalence margin, confidence level and interval/test method, aggregation/weighting across states, and the decision rule when model classes disagree. Those values and the trial count must be recorded in a committed pre-run protocol. This preserves the retained oracle-circularity limit while making the carrier comparison falsifiable.

### R2-G4 - `medium`: the ledger RESUME HERE still instructs a resumer to redo the completed planner repair

The live resume anchor says "Q-78 ACCEPTANCE SHORTFALLS READY FOR PLANNER REPAIR," says T1 still requires deleting the JSONL waiver, and names the immediate next action as a planner pass repairing T1 through T7 (`docs/plans/agent-scaffold.ledger.md:535`, `:539`, `:545`). It also reports Q-80 as open (`:549`). At the reviewed tip, commit `866d793` has completed that planner repair, the JSONL has no waiver record, and Q-80 is `decided -> review-loop-class-inheritance` (`docs/plans/agent-scaffold.plan.toml:2442-2459`). This second acceptance pass is the actual in-flight action.

A resumer obeying the required plan/ledger reconstruction would spawn the wrong role, redo reviewed planning work and treat a decided item as open. Move the old anchor under a clearly historical heading and write a current RESUME HERE that names the repair commit and this acceptance pass. This is the durable-state counterpart of T5, not a re-raise of its fixed receipt-total claim.

### R2-G5 - `low`: the canonical workflow-driver sidecar remains stale and contradictory after its Q-82 edit

The changed architecture sidecar still says the step is not started and has no increments (`docs/plans/agent-scaffold.steps/workflow-driver.md:3`), while its TOML source says `in-progress` and declares stages 0a, 0b and 1 (`docs/plans/agent-scaffold.plan.toml:681-700`). It also says Stage 3 remains gated on real parallel execution and that work is still serial (`workflow-driver.md:15`, `:21`), then says Q-82 has authorised the Stage-3 scheduler (`:23`). Q-82's option set expressly distinguishes scheduling the scheduler from leaving it behind the prior evidence gate, and chose the former (`agent-scaffold.plan.toml:2479-2485`).

The Roadmap and child sidecars still make the intended work discoverable, so this is `low`, but the canonical architecture now gives opposite answers about whether Stage 3 is actionable. Update only the canonical status/staging prose: mark completed/declared stages accurately and state explicitly how Q-82 disposes of the former scheduler gate. Keep implementation criteria in the focused child sidecars so the correction does not duplicate the architecture.

## T1-T7 repair verification

| Item | Result |
| --- | --- |
| T1 | Closed. The sole JSONL waiver row is gone; the log now contains only 310 rounds, 17 escalations, 133 decisions, 2 intakes and 1 dismissal recheck. The TOML `step-intent-encoding-w1` waiver and its decision escalation remain, and W5 passes. |
| T2 | Closed. Rule 5, R1, R2, criterion 8, the exploration and Q-78 ask agree on `<commit>:docs/metrics/workflow.jsonl#L<line>`. R2 reads one line, validates a decision object, requires `task == slug`, exposes only its decision strings, rejects the unqualified log and retains the earliest-receipt check. |
| T3 | Closed. Focused Roadmap owners now exist for structured risk class, Q-80/class inheritance, foreclosure/cap enforcement and authored drift openings. Q-80 is decided with an exact alias of `Q-78-classinherit`; the alias options, recommendation and choice compare equal. Q-81 remains owned only by its existing typed provenance. |
| T4 | Closed. The live Q-78 recommendation and cost permit one or more paragraphs with no sentence, line or character cap. No live single-line/one-sentence recommendation remains. |
| T5 | Closed in the plan product. The Q-78 ask maintains selectors rather than a receipt total or six-plus-six partition. R2-G4 is a later resume-anchor currency defect, not the fixed inventory-total claim. |
| T6 | Closed. `validate-missing-source-exit` owns an Unreleased changelog entry and admits `CHANGELOG.md` in its exact path set while preserving the measured README exclusion. |
| T7 | Closed. The exploration, Q-78 ask and owning step consistently call the four-item block the complete *design*-residual set and leave separately owned review residuals outside it. |

## Decisions, loops and live probes

- Q-58 is genuinely reopened: the new 2026-08-25 receipt chooses the ablation, `q58-output-ablation` is a risky Roadmap step, `resume-state-currency-signal` is blocked on it, and Q-58 remains `exploring` pending the result and carrier decision. A current read-only run emitted 730209 human-output bytes (the reviewed branch has grown since the recorded 727754-byte run); JSON still falsely projected `workflow-calibration` as `awaiting-first-review`, with 728204 bytes in `resume_state`, reproducing the motivating defect rather than assuming it.
- Q-80's alias receipt exactly matches `Q-78-classinherit`; Q-81's original eight identities and no-scope-reset choice remain; Q-82's staged choice, receipt and three focused Roadmap steps exist.
- Twelve Q-78 increments retain peak streak 2 under `risky`. `step-intent-encoding-inc1` retains peak 1 and the correctly scoped record-backed TOML waiver. The 13 identities, round counts and risk classes are unchanged by `866d793`.
- The event-only JSONL invariant is restored: zero `type:"waiver"` rows.

## Gates

The configured `direnv` executable was unavailable in this harness (its PATH entry names a missing store path), so I could not honestly claim a direnv-loaded run. I used the available Nix-store Rust 1.95.0 toolchain and GCC wrapper directly; the crate's MSRV is 1.88.

- source + metrics validation: `463 records, valid`; `113 steps, 82 questions, valid`;
- workflow validation: `workflow invariants hold`;
- `render --check --strict`: `up to date`;
- tests: 470 passed, 0 failed;
- `cargo clippy --all-targets --all-features -- -D warnings`: passed;
- `git diff --check 866d793^..HEAD`: passed;
- changed-file ASCII sweep: zero non-ASCII rows.

No high or critical finding is raised, so no dismissal backstop is implicated by this reviewer report.
