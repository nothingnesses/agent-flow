# Q-78 acceptance pass 4 triage

## Scope and verification

I independently read both pass-4 reports, all three earlier acceptance triages, Q-83, the repaired TOML-primary plan product and affected sidecars. The pass-3 repair is the product under acceptance; this triage does not reopen an earlier disposition without new evidence.

Using the available prebuilt `agent-flow` at `/nix/store/4rayq0a6f1cq2cdcxm6cnhnlgqgbdjhk-source/target/debug/agent-flow`, I reproduced these non-mutating gates on this tree:

- `validate --source docs/plans/agent-scaffold.plan.toml`: 466 metrics records and 114 steps / 83 questions valid.
- `validate --workflow --source docs/plans/agent-scaffold.plan.toml`: workflow invariants hold.
- `render --check --strict docs/plans/agent-scaffold.plan.toml`: up to date.
- `git diff --check` and `git diff --check main...HEAD`: pass.

The three required scratch demonstrations also reproduce:

1. A `round-log-core` declaration retaining `round-log-core-incA` and `round-log-core-incB` exits 1 because each id is not a well-formed kebab-case id. Those are the actual retained, fieldless historical identities: `round-log-core` has no declarations (`docs/plans/agent-scaffold.plan.toml:511-519`), while the five records retain the upper-case ids. The source deliberately distinguishes uppercase-capable well-formed orphan/task tokens from lowercase increment ids (`src/plan/source.rs:452-470`).
2. A zero-step TOML plan with its title as a task-level `plan_review` and one `low_risk` clean round validates under `validate --workflow`. It has no possible task-loop class declaration. The repository likewise has 15 fieldless task-level plan-review identities, including seven `risky` `q78-design-pass` rounds. This is material because the foreclosure design makes task-level plan review a convergence-loop identity (`docs/plans/agent-scaffold.steps/review-loop-foreclosure-enforcement.md:7,13-15,28`).
3. A scratch in-progress `multi` step declaring `multi-inc1` (`low_risk`) and `multi-inc2` (`risky`), with only a clean `multi-inc1` round, makes `next --json` report `multi-inc1`, `converged`, `low_risk`, and required streak 1. This follows the present selector, which derives candidates from rounds and returns the first un-converged round group or latest recorded group (`src/next.rs:782-885`); neither the declarations nor the planned step active-work arm name the newly open increment (`docs/plans/agent-scaffold.steps/workflow-loop-visibility.md:9-11`).

## Deduplication

- Claude A and no GPT finding are the same uppercase historical-increment migration defect.
- Claude B and GPT R4-G1 are one task-scoped convergence-loop authority defect. GPT's `high` severity is correct; this is not two independent findings.
- Claude C, D, GPT R4-G2, and GPT R4-G3 concern distinct selection, scheduler-currency, statistical-protocol, and fleet-currency defects respectively.
- No pass-4 finding merely relitigates a settled pass-1 through pass-3 verdict. The two high findings are upheld, not dismissed; no independent dismissal re-check is owed.

## Verdicts

### R4-1 — Claude A: valid, `high`

`structured-risk-class-source` requires migration to preserve every existing Roadmap increment identity without renaming it or rewriting the append-only log (`docs/plans/agent-scaffold.steps/structured-risk-class-source.md:9,20,35`). It also makes a missing declaration a non-waivable, pre-arithmetic data fault (`:32`). The two retained `round-log-core` identities cannot be declared under the current increment-id contract, as reproduced above and as the source's own uppercase-id test confirms (`src/plan/source.rs:1217-1224`). The requested migration therefore has no legal state for this repository: declaration fails, lowercasing breaks the join, and log rewriting is forbidden.

This is `high`, not a documentation nit: it blocks the Q-83 enforcement migration or forces an implementer to choose an unplanned identity policy on the fail-closed path. It fails loudly today, so it is not `critical`.

Smallest safe disposition: make the increment identity policy explicit in `structured-risk-class-source` and test it against both retained upper-case ids. Prefer a narrow, typed compatibility rule that preserves the exact historical string through parsing and joining; if declared increment ids instead adopt the existing `is_well_formed_token` contract, explicitly state the resulting scope rather than silently weakening a kebab-case invariant. Pin that the migrated history joins and validates without renamed ids, new log events, status changes, or a rewritten log.

### R4-2 — Claude B / GPT R4-G1: valid, `high`

Q-83 and Success Criterion 37 promise one structured authoritative home at loop open and forbid recovery from the first round (`docs/plans/agent-scaffold.steps/structured-risk-class-source.md:7`; `docs/plans/agent-scaffold.success-criteria.md:37`). The repair supplies that home only for `[[step.increment]]`. A task-level plan-review loop is explicitly a different convergence identity, and is still subject to cap/foreclosure enforcement (`docs/plans/agent-scaffold.steps/review-loop-foreclosure-enforcement.md:7,15,28`). `[meta].orphan_tasks` is only `Vec<String>` and does not carry a class (`src/plan/source.rs:106-110`), while the planned task active-work arm has task and phase but no declaration/class (`docs/plans/agent-scaffold.steps/workflow-loop-visibility.md:9-10`).

The scratch validation and live `q78-design-pass` population show this is a live branch, not a hypothetical one. A future risky task-level plan-review loop can still receive a `low_risk` first snapshot and take a one-round bar with no structured declaration or mismatch check. That preserves the exact silent downgrade Q-83 was chosen to eliminate, so `high` is warranted rather than Claude's `medium`.

Smallest safe disposition: add one typed, plan-resident task-loop declaration keyed by task and convergence phase, usable for `[meta].title` and registered orphan tasks, with a class fixed before round one. Make task active-work and the reconstruction resolve it, require every task-loop snapshot to match it, and extend rebuild/inheritance rules if they can reopen task loops. Add pre-round, mismatch, and existing `q78-design-pass` fixtures. Do not treat task loops as single-pass records: acceptance and standalone review are single-pass, but plan review is expressly not.

### R4-3 — Claude C: valid, `medium`

The acceptance criterion requires pre-round output for *the* declared risky increment (`docs/plans/agent-scaffold.steps/structured-risk-class-source.md:33`), yet more than one increment can be declared before any corresponding loop opens. The current plan has multi-increment steps, and the reproduced fixture establishes that the extant selector necessarily reports the old converged increment. The proposed active-work step variant identifies only a step and phase, not an increment (`docs/plans/agent-scaffold.steps/workflow-loop-visibility.md:9-11`), so it cannot supply the missing selection fact. Choosing declaration order or latest round would invent a selection rule and can return the wrong class exactly at loop open.

This is `medium`: it makes the required pre-round output unimplementable for a routine multi-increment shape and can misstate the convergence bar, but it does not itself silently mutate or lose durable data.

Smallest safe disposition: define one durable open-increment selection operation before `next` reads the declaration, and make the later active-work carrier reuse it rather than create a second selector. It may be an explicit resolving increment identity or a genuinely enforced declare-only-at-open lifecycle, but it must distinguish a newly opened increment from predeclared or converged siblings. Pin a multi-increment fixture where a converged low-risk sibling exists and a newly selected risky sibling reports streak 2 before round one, plus a red control that selects the sibling by declaration order or latest round.

### R4-4 — Claude D: valid, `low`

The pass aligns the current scheduler authority to Q-82 (`docs/plans/agent-scaffold.steps/workflow-ready-frontier-scheduler.md:1-9`), but two retained design records still say that scheduler work is gated on real parallelism: `docs/plans/mealy-workflow-driver.explorations/r2-requirements-scope.md:127,170` and `docs/plans/agent-scaffold.explorations/Q-64-delivery-fsm.md:76`. The first is a requirements-scope record, not merely an immutable transcript, and neither location labels the condition as superseded history.

This is `low` because the focused sidecar remains the implementation authority, but the contradictory records fail the acceptance documentation-currency check and can mislead a reader about whether Stage 3 is authorised.

Smallest safe disposition: update both sites with the same bounded Q-82 supersession note, or clearly label them as frozen pre-Q-82 history and point to the focused scheduler sidecar. Preserve the distinct gates for the write path and authoritative driving.

### R4-5 — GPT R4-G2: valid, `low`

The retained protocol permits an exact, precommitted paired interval *or* test to implement the non-inferiority/equivalence procedure (`docs/plans/code-value-audit.explorations/Q-58-ablation-design.md:80-95`). The new criterion instead says confidence intervals “report uncertainty only” while the procedure decides admission (`docs/plans/agent-scaffold.steps/q58-output-ablation.md:21`; repeated in Success Criterion 35). That wording prohibits the allowed interval-based procedure, not only the intentionally banned interval-overlap heuristic.

This is `low`: a hypothesis-test choice can avoid the contradiction, and the frozen protocol still prevents post-hoc selection, but the plan offers two incompatible methods to the experimenter.

Smallest safe disposition: distinguish descriptive marginal/per-arm intervals and interval overlap (never decision rules) from a precommitted paired confidence-bound procedure that may implement the frozen non-inferiority/equivalence rule. Apply the clarification consistently to the retained design, owning step, and Success Criterion.

### R4-6 — GPT R4-G3: valid, `low`

`workflow-driver-typed-fleet` names the Stage-2 paragraph in `workflow-driver.md` as its authoritative scope (`docs/plans/agent-scaffold.steps/workflow-driver-typed-fleet.md:1`). That paragraph still promises only nested `StepMachine`/`TaskMachine` and a task/step fleet (`docs/plans/agent-scaffold.steps/workflow-driver.md:20`), whereas the repaired architecture and focused criteria require `QuestionMachine` and task/question/step coverage (`docs/plans/mealy-workflow-driver.explorations/r2-architecture-build-path.md:134-149`; `docs/plans/agent-scaffold.steps/workflow-driver-typed-fleet.md:17-20`).

This is `low` because the focused acceptance criteria would reject a question-less implementation, but the explicitly authoritative scope document is stale and conflicts with the repaired question carrier.

Smallest safe disposition: update the Stage-2 paragraph to name `QuestionMachine` and the full task/question/step fleet, while preserving the focused sidecar as the detailed implementation authority.

## Result

Six deduplicated shortfalls remain: two `high`, one `medium`, and three `low`. No finding is invalid or accepted as residual. The two upheld high findings need planning before acceptance can settle; none was dismissed, so no high/critical dismissal re-check is pending.
