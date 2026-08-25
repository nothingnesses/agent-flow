# Q-78 acceptance pass 4 - GPT reviewer

## Verdict

Three acceptance shortfalls: one `high` and two `low`. No `critical` or `medium` finding.

The pass-3 repairs close the pending-ready/blocked fallback, the question-scoped exploration carrier, the focused scheduler's eligibility/precedence rules, and the stale CI-overlap instruction on their intended paths. The remaining findings are an uncovered non-Roadmap plan-review branch of Q-83, one contradictory Q-58 statistical-method instruction introduced by the repair, and one stale Stage-2 architecture sentence left by the question-carrier repair.

Q-78 remaining `open` pending acceptance is deliberate and is not a finding.

## Shortfalls

### R4-G1 - `high`: task-scoped plan-review loops still have no authoritative loop-open risk class

Success Criterion 37 promises one authoritative structured home for every review-loop class, available before round one (`docs/plans/agent-scaffold.success-criteria.md:37`). The Q-83 repair supplies that home only for Roadmap increments: `structured-risk-class-source` makes `[[step.increment]].risk_class` authoritative, migrates Roadmap work-review histories, and explicitly leaves non-increment records as event snapshots (`docs/plans/agent-scaffold.steps/structured-risk-class-source.md:7-9,30-36`).

The expanded design also has convergence loops that cannot own a `[[step.increment]]`. The shared reconstruction defines a task-level `plan_review` loop separately from a Roadmap work loop, but states the declared-class rule only for the Roadmap increment window (`docs/plans/agent-scaffold.steps/review-loop-foreclosure-enforcement.md:7`). Its typed task carrier contains only `task` and phase, with no class or declaration reference (`docs/plans/agent-scaffold.steps/workflow-loop-visibility.md:9`). The driver then instantiates `ReviewLoop` for plan review while claiming its `risk_class` and `Open.declared_risk_class` come from a resolving plan increment (`docs/plans/mealy-workflow-driver.explorations/r2-architecture-build-path.md:100-120`). Those contracts cannot all hold for an orphan task.

The repository's own task that motivated foreclosure proves this is a live shape. Run:

```bash
jq -s -r '
  to_entries[]
  | select(.value.type == "round"
      and .value.task == "q78-design-pass"
      and .value.phase == "plan_review")
  | [(.key + 1), .value.task, (.value.step // "<none>"),
     (.value.increment // "<none>"), .value.risk_class]
  | @tsv
' docs/metrics/workflow.jsonl
```

It prints records 380 through 386, each as `q78-design-pass <none> <none> risky`. The design itself confirms that task has no Roadmap step (`docs/plans/agent-scaffold.steps/review-loop-foreclosure-enforcement.md:11`). It is also the exact rebuild shape Q-80 is meant to govern, yet the inheritance step requires the rebuilt loop to write a new `[[step.increment]]` declaration (`docs/plans/agent-scaffold.steps/review-loop-class-inheritance.md:7`), which this task has nowhere to put.

Consequently a fresh task-level plan-review loop has no durable class before its first completed round. Afterward an implementation must either recover authority from `round.risk_class`, preserving the same silent low-risk downgrade Q-83 closed for work reviews, or fail to reconstruct a legal task plan review at all. This is `high` for the same reason as pass-3 R3-1: it can reduce a risky convergence loop from two clean rounds to one while leaving the task-level branch outside the new mismatch controls.

Add an authoritative task-loop declaration (or another explicit representation consistent with Q-83), make the task carrier reference it before round one, require every task plan-review snapshot to match it, and apply Q-80 inheritance to it. Red fixtures should cover a pre-round risky orphan task, a risky task declaration plus one low-risk snapshot, and the existing `q78-design-pass` shape.

### R4-G2 - `low`: Q-58 both permits a confidence-interval decision procedure and says confidence intervals cannot decide

The retained Q-58 protocol explicitly permits an exact interval method, requires its confidence level, and directs the analysis to interpret the score delta through that frozen interval/test (`docs/plans/code-value-audit.explorations/Q-58-ablation-design.md:81,88,95`). A valid paired non-inferiority procedure can therefore decide admission by comparing a one-sided confidence bound with the frozen margin.

The repaired owning criterion instead says confidence intervals "report uncertainty only" while another procedure decides plateau membership (`docs/plans/agent-scaffold.steps/q58-output-ablation.md:21`); the retained design repeats that restriction (`docs/plans/code-value-audit.explorations/Q-58-ablation-design.md:116`), as does Success Criterion 35 (`docs/plans/agent-scaffold.success-criteria.md:35`). This is stronger than the intended and correctly stated ban on **interval overlap**: it also appears to forbid the paired interval procedure that lines 81, 88, and 95 expressly allow.

This is `low` because a protocol can avoid the conflict by choosing a hypothesis test, and the frozen-protocol controls still prevent post-hoc selection. Clarify that marginal/per-arm confidence intervals and their overlap are descriptive only while a precommitted paired confidence bound may implement the non-inferiority rule, or remove the interval-method option and require a test.

### R4-G3 - `low`: the paragraph named as Stage 2's authority still omits the repaired question machine

The focused fleet step calls the Stage 2 paragraph in `workflow-driver.md` its authoritative scope (`docs/plans/agent-scaffold.steps/workflow-driver-typed-fleet.md:3`). That paragraph still specifies only nested `StepMachine`/`TaskMachine` and a "full task/step active-unit fleet" (`docs/plans/agent-scaffold.steps/workflow-driver.md:20`).

The repaired architecture and executable criterion now require three scopes: `QuestionMachine` appears beside task and step machines and in `Fleet.questions` (`docs/plans/mealy-workflow-driver.explorations/r2-architecture-build-path.md:134-149`), and the focused acceptance criterion requires every task-, question-, and step-scoped unit including Q-68/Q-69-shaped exploration (`docs/plans/agent-scaffold.steps/workflow-driver-typed-fleet.md:20`).

The focused criteria prevent a question-less implementation from passing, so the impact is `low`, but the document explicitly named as authoritative is stale on the pass-3 question-carrier disposition and fails the acceptance documentation-currency check. Update the Stage 2 paragraph to name `QuestionMachine` and the task/question/step fleet.

## Pass-3 disposition verification

- R3-1 is closed for Roadmap increments: the plan declaration is authoritative, mismatch/missing-declaration cases fail closed, and pre-round human/JSON output is pinned. R4-G1 is new evidence for the separately specified task-level convergence branch.
- R3-2 is closed: absent/empty carriers retain typed `ready-to-plan` and `blocked` fallback actions on human and JSON surfaces, with red empty-selection controls.
- R3-3 is functionally closed: a real `exploring` question has its own Roadmap-independent carrier and Q-68/Q-69 fixtures. R4-G3 is the stale architecture sentence left behind, not a claim that the focused criteria omit the variant.
- R3-4 is closed: the focused scheduler is authoritative, its domain is exactly `not-started`/`next`, `complete` and `skipped` satisfy blockers, explicit task/question/step actions take precedence, and frontier membership is conditional on origin.
- R3-5's stale `CI-overlap for the knee` phrase is gone. R4-G2 concerns the newly authored broader confidence-interval restriction, not the removed overlap rule.
- Q-80, Q-81, Q-82, and Q-83 are registered as decided with matching receipts; Q-80 aliases the earlier class-inheritance choice, Q-81 retains the existing increment identities, and Q-82's staged dependencies remain structured.

## Gates

I used Rust/Cargo 1.95.0 and the GCC wrapper from the Nix store, with `HOME`, `TMPDIR`, `CARGO_HOME`, and `CARGO_TARGET_DIR` under `/tmp/q78-acceptance-r4-gpt`; the advertised `direnv` and `nix` PATH entries were not realised in this container.

- `validate --source docs/plans/agent-scaffold.plan.toml`: `466 records, valid`; `114 steps, 83 questions, valid`.
- `validate --workflow --source docs/plans/agent-scaffold.plan.toml`: `workflow invariants hold`.
- `render --check --strict docs/plans/agent-scaffold.plan.toml`: `up to date`.
- `cargo test --locked`: 470 passed, 0 failed.
- `cargo clippy --all-targets --locked -- -D warnings`: passed.
- `git diff --check` and `git diff --check main...HEAD`: passed.
- The changed-file ASCII sweep with `grep -nP '[^\t\x20-\x7e]'`: zero files reported.

Totals: 3 findings; severity ceiling `high`; 0 critical, 1 high, 0 medium, 2 low.
