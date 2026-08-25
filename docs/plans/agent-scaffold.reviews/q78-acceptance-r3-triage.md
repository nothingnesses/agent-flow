# Q-78 acceptance pass 3 triage

## Scope and verification

I independently read both pass-3 reports, both preceding acceptance triages and repair briefs, the current TOML-primary plan and Success Criteria, Q-58 and Q-82, the driver architecture, the affected sidecars, and `AGENTS.md`.

Using the available `agent-flow 0.0.4` binary, I reproduced `validate --source docs/plans/agent-scaffold.plan.toml` (464 records and 114 steps / 82 questions valid), `validate --workflow --source docs/plans/agent-scaffold.plan.toml` (`workflow invariants hold`), and `render --check --strict docs/plans/agent-scaffold.plan.toml` (`up to date`). `git diff --check 5b28975..7f10acc` also exits zero.

I reproduced GPT's structured-risk demonstration in authorised scratch with the exact one-step TOML fixture: it declares `dangerous-inc1` as `risky`, supplies one `low_risk` clean round, and `validate --workflow` exits zero with `workflow invariants hold`. This is not a tooling failure. `Increment.risk_class` is documented as setting the convergence streak in `src/plan/source.rs:256-265`, but `PlanToml::step_views` drops increments (`src/plan/source.rs:416-430`) and W3 selects and checks only the round-record class (`src/workflow.rs:495-506`).

I also reproduced the existing phase selection in scratch: a one-step `not-started` plan emits `state: ready-to-plan`, `next: spawn a planner to draft the step plan`, and `role: planner`; a pending step blocked by a deferred prerequisite emits `state: blocked` and `next: resolve the unmet blockers before starting`. This follows the current selection code at `src/next.rs:709-734`.

## Deduplication

- GPT R3-G4 and Claude finding B are the same stale `CI-overlap for the knee` instruction and are adjudicated once as R3-4.
- Claude finding A and GPT R3-G2 share the overly narrow step carrier, but are not duplicates. R3-2 concerns pending ready/blocked Roadmap work; R3-3 concerns question-scoped exploration that deliberately has no Roadmap step.
- No finding re-raises a settled pass-1 or pass-2 disposition without new evidence.

## Verdicts

### R3-1 — GPT R3-G1: valid, `high`

`structured-risk-class-source` promises that a round record is the only authoritative class (`docs/plans/agent-scaffold.steps/structured-risk-class-source.md:1,7`), while the shipped source and current plan retain a second field described as the increment's convergence class. The reproduced fixture proves that the existing validator accepts a one-round `low_risk` convergence despite a `risky` TOML declaration. The planned step explicitly excludes source work unless a reader still reads prose (`structured-risk-class-source.md:25`); this demonstrated disagreement is instead between two structured values, so that exception cannot repair it.

This violates Success Criterion 37's promise that a rebuild cannot silently obtain a cheaper bar (`docs/plans/agent-scaffold.success-criteria.md:37`). It is `high`: it permits a systemic downgrade from the declared two-clean-round bar to one clean round while all validators report success. It is not `critical`, because it is bounded to workflow review evidence rather than directly compromising safety, money, or data.

Smallest safe disposition: reconcile or remove the TOML increment class before calling round records the only authority. If the TOML field remains, its relation to the loop-opening record must be explicit and fail closed; otherwise it must be demoted/removed rather than described as the convergence class. Add the reproduced disagreeing pair as a red control, including the pre-first-round case, and update Criterion 37 and the sidecar to state the one chosen model. No high finding was dismissed, so no dismissal re-check is owed.

### R3-2 — GPT R3-G2: valid, `medium`

The proposed carrier accepts a step only when it is `in-progress` and says no carrier means no selected action (`docs/plans/agent-scaffold.steps/workflow-loop-visibility.md:9-16,24-29`). Its compatibility promise retains review-state fixtures only. That removes the currently legal `ready-to-plan` and `blocked` actions reproduced above: a fresh or dependency-blocked plan has neither a legal `[[active_work]]` row nor a selected action. The existing selection is deliberately broader, not dead code.

This is a `medium` workflow regression: it leaves a normal fresh or blocked plan without the planner/orchestrator instruction needed to start or unblock work, but it does not itself mutate or lose data.

Smallest safe disposition: represent pending-ready and pending-blocked work in the typed model, or retain the existing pending fallback until the scheduler deliberately supersedes it. Pin both states on JSON and human surfaces and add red fixtures proving that an empty carrier cannot erase a legal pending action.

### R3-3 — Claude finding A: valid, `medium`

The carrier's only exploration representation is a step-scoped row whose step must be `in-progress` (`docs/plans/agent-scaffold.steps/workflow-loop-visibility.md:9-10,24-25`). Design exploration is instead a question-scoped entry mode: `AGENTS.md:45` records an `exploring` question and then spawns explorers, and `AGENTS.md:65` places their notes under a task exploration path. The plan has concrete legal examples: Q-68 and Q-69 are `exploring`, and Q-69 explicitly states “NO STEP YET” and that Q-68 has the same shape (`docs/plans/agent-scaffold.plan.toml:2238-2263`).

An `exploring` question is not necessarily an explorer currently in flight, so the report's “active twice right now” wording overstates the current runtime state. The defect remains: when either owed question-scoped pass runs, no union arm can represent it, contrary to Success Criterion 40's all-active-unit projection (`docs/plans/agent-scaffold.success-criteria.md:40`). This is distinct from R3-2 and is `medium` because it can hide live work and emit no phase-correct instruction.

Smallest safe disposition: add a legal question-scoped exploration variant, keyed by a resolving Open-Questions id and independent of Roadmap status, or explicitly revise the workflow and Success Criterion to forbid pre-step exploration. Add fixtures for Q-68/Q-69-shaped work and the rejected alternative. Do not fake a carrier by changing an unrelated step's status.

### R3-4 — GPT R3-G3: valid, `medium`

The focused Stage-3 sidecar says its step-granularity frontier contains nonterminal steps whose blockers are strictly complete (`docs/plans/agent-scaffold.steps/workflow-ready-frontier-scheduler.md:7,17-21`). The canonical architecture it says it reuses instead defines the function over `NotStarted`/`Next` steps and treats `Complete` or `Skipped` blockers as satisfied (`docs/plans/mealy-workflow-driver.explorations/r2-architecture-build-path.md:157-161`). The focused sidecar additionally requires exploration, implementation, review, and acceptance candidates plus makes `selected_action` a frontier member, while the prior stage selects from task- and step-scoped active units in declaration order (`workflow-loop-visibility.md:9-16`). A task-scoped acceptance action cannot be an element of a pure `Vec<StepMachine>` frontier.

These are contradictory implementation contracts, not harmless terminology. An implementer cannot both preserve the stated canonical architecture and satisfy the focused criteria. The impact is `medium`: scheduler advice can wrongly block skipped dependencies or misstate authority/selection, but the scheduler remains read-only.

Smallest safe disposition: make one sidecar the explicit authority and align the other. Define one eligibility domain, the skipped-blocker rule, and precedence between a task action and a step frontier. If the frontier remains step-only, task actions must be outside it and the selected-action membership invariant must be conditioned accordingly. Add fixtures for skipped blockers, task acceptance with pending work, active review, and serial fallback.

### R3-5 — GPT R3-G4 / Claude finding B: valid, `low`

The retained Q-58 design rejects interval overlap as evidence and requires the frozen test/interval (`docs/plans/code-value-audit.explorations/Q-58-ablation-design.md:88-95`); the owning step repeats that rule (`docs/plans/agent-scaffold.steps/q58-output-ablation.md:21`). The later Agent-variance bullet still directs `CI-overlap for the knee` (`Q-58-ablation-design.md:116`). The reports are duplicate evidence of one contradictory experiment instruction.

This is `low`: the newer protocol and acceptance criterion prevent the stale sentence from becoming an acceptable completed run, but it can still send an experimenter toward a wasted invalid protocol.

Smallest safe disposition: replace that phrase with the frozen non-inferiority/equivalence procedure while retaining confidence intervals as reported uncertainty, not the decision rule.

## Result

Five distinct acceptance shortfalls are valid: one `high`, three `medium`, and one `low`. No finding is invalid or accepted as residual. The high finding is upheld, not dismissed, so the independent high/critical dismissal re-check is not required. Q-78 cannot settle acceptance until these dispositions are planned and repaired.