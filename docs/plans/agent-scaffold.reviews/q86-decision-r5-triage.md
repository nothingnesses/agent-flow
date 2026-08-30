# Q-86 decision-fold plan review, round 5 triage

## Scope, reproduction, and deduplication

I independently read `AGENTS.md`, `.agents/prompts/triager.md`, the selected proof step, the waiver model, the scheduler authority, Q-86/Q-91, the four earlier decision-fold triages, both round-5 reviews, and the retained Q-86 synthesis triages.

The ordinary gates reproduce cleanly:

```text
nix develop --command cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml
# docs/plans/agent-scaffold.plan.toml: up to date
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl
# 500 records, valid; 115 steps, 91 questions, valid
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow
# workflow invariants hold
git diff --check main...e1d8a767
# exit 0
```

The reviewers supplied six raw reports: five from Claude and one from GPT. The scheduler-comment report is duplicated, leaving five findings. Four are valid: one high and three low. The provenance-path report is invalid. No finding is accepted as residual risk.

## Verdicts

### T1 — A convergence waiver can make the safety proof `complete` without its required reviews

- **Sources:** Claude Finding 1.
- **Verdict:** valid, **high**.
- **Reproduction:** I copied `docs/` to a temporary project root, changed only the proof step to `status = "complete"`, and ran the workflow validator. With no waiver it exited 1 with `Roadmap step 'bounded-convergence-option-b-proof' is 'complete' but has no round records and no covering waiver`. I then replaced that step's empty waiver list with a nested step waiver:

  ```toml
  [[step.waiver]]
  id = "bounded-convergence-option-b-proof-w1"
  unit = "step"
  reason = "review-skipped"
  evidence_tier = "self-declared"
  ```

  The same `validate --source <scratch>/docs/plans/agent-scaffold.plan.toml --workflow` exited 0 and reported workflow invariants hold. This follows the deliberately generic W3 rule in `src/workflow.rs:436-486`: a step-level waiver is sufficient when a complete step has no rounds, while W5 permits the stated self-declared `review-skipped` pairing. The proof requires two clean risky rounds at `bounded-convergence-option-b-proof.md:21` and acceptance criterion 14, but the planned complete-only scheduler gate tests only target status (`workflow-ready-frontier-scheduler.md:17,35`).
- **Reasoning:** This is distinct from round 4's skipped-status bypass. The complete-only policy correctly rejects `skipped`, but it inherits every route that can produce `complete`; the generic waiver route permits the blocking proof to reach that status with no proof work or review. The result can unlock a future broadly used bounded-convergence implementation without its required proof, so high is proportionate.
- **Required correction:** The selected proof needs an explicit no-waiver completion invariant. The future complete-only policy and workflow validation must require both `status == complete` and round-backed, unwaived convergence for this proof; reject a production dependent when its proof target has a step or increment convergence waiver. Add red controls for the self-declared no-round route and every other waiver route. Do not weaken the generic waiver model for ordinary steps.

### T2 — Traceability does not bind an executable row's named mutation to the mutation manifest

- **Sources:** Claude Finding 2.
- **Verdict:** valid, **low**.
- **Reproduction:** The traceability contract requires each executable matrix row to name both a property and a mutation that kills it (`bounded-convergence-option-b-proof.md:180`). Its stated rejection list resolves a named assertion or durable-text pointer, but not a named mutation (`:39,180,222`). Separately, the mutation runner requires each manifest tag to have an exercised, killed mutation (`:37,188-190`); it does not bind a matrix row's mutation name to that manifest entry.
- **Reasoning:** A matrix can therefore claim a per-verdict mutation name that is missing, unexercised, or tests another assertion while both planned tools satisfy their stated checks. The general manifest still requires mutation coverage for load-bearing tags, limiting the impact to traceability attribution rather than eliminating mutation coverage altogether.
- **Required correction:** Require the traceability checker to resolve every executable row's named mutation against the manifest and verify that it was exercised and killed, failing unknown, surviving, or unexercised names.

### T3 — The aligned scheduler pseudocode retains a universal ordinary-blocker claim

- **Sources:** Claude Finding 3; GPT Finding 1.
- **Verdict:** valid, **low**.
- **Reproduction:** `r2-architecture-build-path.md:188` says a blocker is satisfied exactly by `Complete` or `Skipped`, while `:191` correctly limits that rule to ordinary `blocked_by` and says a typed complete-only blocker requires `Complete`. The scheduler sidecar names this architecture document as an aligned summary to update (`workflow-ready-frontier-scheduler.md:46-48`).
- **Reasoning:** The focused scheduler sidecar remains authoritative, so this is not another completion-gate bypass. It is nevertheless a stale implementation-shaped comment in an explicitly aligned document and can mislead a reader into applying the ordinary predicate to the exceptional policy.
- **Required correction:** Qualify the comment as ordinary `blocked_by` behavior and state the complete-only exception, or remove the redundant comment.

### T4 — The proof's structured provenance paths are correctly task-relative

- **Sources:** Claude Finding 4.
- **Verdict:** invalid.
- **Reproduction:** The proof provenance entries use `agent-scaffold.reviews/q86-synthesis-r<n>-triage.md`; each resolves from the plan directory `docs/plans/` to the retained file. This is the schema's documented convention: `Provenance.findings` holds task-relative paths (`src/plan/source.rs:233-249`) and validation requires a safe task-relative reference (`:609-649`). A repository-root prefix is neither required by the provenance schema nor by task-entry re-grounding.
- **Reasoning:** The sidecar's prose uses repository-root paths because it is run from the repository root; that does not make the structured, plan-relative references defective. The neighboring full-root-looking reference does not establish a different schema contract. No new evidence shows that the proof provenance cannot be used through its declared resolution base.

### T5 — Post-freeze resume reconstruction is specified but not acceptance-tested explicitly

- **Sources:** Claude Finding 5.
- **Verdict:** valid, **low**.
- **Reproduction:** The proof requires replay of the same ordered events to reconstruct identical selected state (`bounded-convergence-option-b-proof.md:46`), specifies route reconstruction on resume (`:78`), and forbids replenishment on resume, rename, rebuild, replan, and narrowing (`:154`). Acceptance criterion 2 requires reconstruction without replenishment only for `SealedPlanReview` (`:213`). Criterion 4 requires the post-freeze state and routes, but does not require an event-replay equality fixture or a resume/rebuild/rename/replan mutation for those post-freeze components (`:215`); the mandatory mutation list likewise does not make that replay assertion explicit (`:188`).
- **Reasoning:** A proof could cover the named static post-freeze routes and still omit the reconstruction property that prevents a resumed family from reclassifying or replenishing authority. The property is stated repeatedly and the proof remains blocking, so this is a low specification-to-acceptance gap rather than current unsafe behavior.
- **Required correction:** Extend the post-freeze acceptance and mutation requirements to replay identical ordered events and compare architecture, floor, family id, spend/authority, finding map, owner routes, and terminal state. Cover resume, rename, rebuild, and unchanged replan without replenishment.

## Outcome, cap, and backstop

**Round outcome: `new_valid`.** Deduplicated findings: **4 valid** — **1 high, 3 low** — and **1 invalid**. There are no critical or medium valid findings and no accepted residual risk.

This risky decision-fold artifact has reached review round **5 of 5** with a consecutive-clean streak of **0 of 2**. Because valid findings reset the streak, the convergence-first exception cannot apply. The total-round cap therefore requires escalation to the human under the human-input contract; do not open a sixth ordinary review round.

No high- or critical-severity finding was dismissed: T1 is valid and all other valid findings are low. The independent high/critical dismissal backstop is therefore **not owed** for this round.
