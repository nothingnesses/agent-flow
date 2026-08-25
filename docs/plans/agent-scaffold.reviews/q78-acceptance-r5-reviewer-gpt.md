# Q-78 acceptance pass 5 - GPT reviewer

## Verdict

Three acceptance shortfalls remain: one `high`, one `medium`, and one `low`. No `critical` finding.

The pass-4 repair closes the named lowercase/uppercase increment-id incompatibility, supplies a task-loop declaration for the live orphan `q78-design-pass`, makes active Roadmap increment selection explicit, aligns the Q-58 paired-interval rule, restores `QuestionMachine`, and updates the main Q-82 scheduler authorities. The remaining defects are a historical plan-review shape outside the new two-arm declaration model, an impossible single-pass state in the authoritative Stage-2 type sketch, and one stale scheduler gate left in the requirements YAGNI boundary.

Q-78 remaining `open` pending acceptance is deliberate and is not a finding.

## Shortfalls

### R5-G1 - `high`: Roadmap-owned historical `plan_review` loops fit neither authoritative declaration arm

The repaired model has exactly two convergence declaration/selection arms: a Roadmap arm carrying `(step, increment)` for `work_review`, and a task arm carrying `(task, plan_review)` whose task must be the plan title or a registered orphan (`docs/plans/agent-scaffold.steps/structured-risk-class-source.md:7-13`; `docs/plans/agent-scaffold.steps/review-loop-foreclosure-enforcement.md:7-9`). Missing or ambiguous declaration joins fail closed, the event log is not rewritten, and current-history migration must preserve every identity (`docs/plans/agent-scaffold.steps/structured-risk-class-source.md:9,15,43-44`).

This repository has a third historical shape: `plan_review` records whose task is itself a real Roadmap step slug, with no increment. Reproduce it directly:

```bash
jq -s -r '
  to_entries[]
  | select(.value.type == "round"
      and .value.phase == "plan_review"
      and (.value.increment == null)
      and (.value.task == "structured-skeleton"
           or .value.task == "checks-runner-worktree-name-collision"))
  | [(.key + 1), .value.task, (.value.step // "<none>"),
     (.value.increment // "<none>"), .value.risk_class, .value.outcome]
  | @tsv
' docs/metrics/workflow.jsonl
```

The result is records 98, 99, 115, 217, 219, 220, and 221. All have phase `plan_review`, no increment, and task `structured-skeleton` or `checks-runner-worktree-name-collision`; those are real Roadmap slugs at `docs/plans/agent-scaffold.plan.toml:582` and `:1287`. They cannot use the declared Roadmap arm because that arm requires an exact increment and `work_review`. They cannot use the task arm either: it requires the title or an orphan, while the existing source contract deliberately rejects an orphan task equal to a Roadmap slug (`src/plan/source.rs:755-769`).

The larger Q-81 population reinforces that phase and owner cannot be inferred casually: records 387-430 contain 41 `plan_review` rounds over 13 exact structured increments. Those task strings happen to equal their increment strings, but Q-81 expressly preserves the increment identities; the repaired criteria name only the seven fieldless `q78-design-pass` records as the task-loop history fixture.

This is `high` for the same reason as pass-4 R4-1: implementing the stated fail-closed migration has no legal state for committed append-only history. A literal implementation either makes this repository permanently fail validation, rewrites historical phase/identity fields, or invents an unreviewed compatibility arm on the safety-relevant authority path.

Add a typed declaration/reconstruction rule for Roadmap-owned plan-review history, or a narrowly specified legacy mapping that preserves its exact phase and identity without weakening the orphan invariant. Pin the seven step-slug records and the 41 Q-81 increment-scoped records as current-history fixtures, including their real escalation segmentation.

### R5-G2 - `medium`: the authoritative Stage-2 type requires a convergence class for phases forbidden to have one

`workflow-driver-typed-fleet` names the Stage-2 paragraph and detailed architecture build path as its authority (`docs/plans/agent-scaffold.steps/workflow-driver-typed-fleet.md:3`). The repaired architecture says one reusable `ReviewLoop` is instantiated for plan review, work review, and a degenerate single-pass acceptance/review variant, but the shown type makes `risk_class` mandatory, includes `Acceptance | Review` in the same `Phase`, and can open only with `Open { declared_risk_class }` (`docs/plans/mealy-workflow-driver.explorations/r2-architecture-build-path.md:100-129`). Its total transition function then applies required-streak and cap arithmetic from that class (`:132`).

The same repaired document says acceptance/review never borrow a convergence declaration and reconstruct without a declaration lookup (`:142,152`). The focused acceptance criteria likewise require acceptance and standalone review to remain single passes without convergence arithmetic (`docs/plans/agent-scaffold.steps/workflow-driver-typed-fleet.md:18-20`). No `SinglePass` type, constructor, or transition table is defined, so the shown supposedly total type cannot represent the required state without fabricating a risk judgment or storing a meaningless class.

This is `medium`: the focused output criteria should catch a behavioural implementation that gives acceptance a streak or cap, but an implementer cannot follow the authoritative type design as written and must silently redesign a load-bearing control/judgment boundary.

Represent convergence and single-pass review as distinct typed variants, for example a `ReviewProcess::{Convergence(ReviewLoop), SinglePass(SinglePassReview)}` union, and pin that the single-pass variant has no constructible risk class, streak, foreclosure, or cap state.

### R5-G3 - `low`: the retained requirements YAGNI boundary still forbids the Q-82 work

Q-82 chose to schedule the typed fleet and then the read-only scheduler (`docs/plans/agent-scaffold.plan.toml:2491-2501`), and the current workflow-driver authority says the former real-parallelism gate is superseded for that scheduler (`docs/plans/agent-scaffold.steps/workflow-driver.md:21`). The pass-4 repair added matching supersession notes to the two sites the prior finding cited.

However, the same retained requirements record still ends with the live imperative: "Do NOT build the fleet + scheduler before parallel units actually run" (`docs/plans/mealy-workflow-driver.explorations/r2-requirements-scope.md:175`). That directly forbids both newly scheduled steps and is not marked as historical or superseded.

This is `low` because the focused sidecars and Roadmap remain unambiguous implementation authorities, but pass-4 R4-4 is not fully closed and the acceptance documentation-currency check still fails. Mark this YAGNI bullet as superseded by Q-82 for the typed fleet/read-only scheduler while preserving the separate write-path and authoritative-driving gates.

## Pass-4 disposition verification

- R4-1 is closed for `round-log-core-incA`/`incB`: the compatibility grammar is owner-matching, byte-preserving, and does not widen unrelated slug classes. R5-G1 is a different historical phase/owner shape.
- R4-2 is closed for the orphan-task `q78-design-pass` branch: it has a task-loop declaration design, pre-round authority, mismatch controls, and a digest-pinned cap-adoption boundary. R5-G1 covers Roadmap-owned plan-review histories that cannot enter that registry.
- R4-3 is closed: the exact active `(step, increment)` selection is durable, used before round one, retained across implementation/review transitions, and tested against sibling/order/recency guesses.
- R4-4 is only partially closed: the two previously cited sites carry Q-82 notes, but R5-G3 identifies another still-operative prohibition in the same requirements record.
- R4-5 is closed: the retained design, owning step, and Success Criterion consistently distinguish descriptive marginal/per-arm intervals from a precommitted paired confidence-bound or paired-test decision procedure.
- R4-6 is closed for the question scope: `QuestionMachine` and the task/question/step fleet now appear in the authoritative Stage-2 paragraph and detailed architecture. R5-G2 concerns the separately inconsistent acceptance/review single-pass type.
- Q-80, Q-81, Q-82, and Q-83 remain registered as decided with matching receipts. Q-58 remains correctly reopened and `exploring`; its experiment precedes the dependent carrier work.

## Gates and evidence

All configured gates ran from scratch under `/tmp/q78-r5-gpt`, using Cargo/Rust 1.95.0 and the Nix GCC wrapper. The current tree was never modified.

- `validate --source docs/plans/agent-scaffold.plan.toml`: `467 records, valid`; `114 steps, 83 questions, valid`.
- `validate --source docs/plans/agent-scaffold.plan.toml --workflow`: `workflow invariants hold`.
- `render --check --strict docs/plans/agent-scaffold.plan.toml`: `up to date`.
- `agent-flow checks`: 1 passed, 0 failed, 0 skipped.
- `cargo test --locked --offline`: 470 passed, 0 failed.
- `cargo clippy --all-targets --locked --offline -- -D warnings`: passed.
- `git diff --check`, `git diff --check main...HEAD`, and the changed-file ASCII sweep passed.
- The record-386 SHA-256 reproduces as `4e7aed64e77ca228347de1cfbcf620ca2d6b6f3d8550b606212b3b448d0e95c6`.

An extra `cargo fmt --check` probe was not treated as a configured gate: the directly assembled stable-rustfmt environment ignores this repository's nightly-only rustfmt options and reports repo-wide differences in unchanged Rust files. It changed nothing; the configured check runner is the authoritative format/lint surface here.

Totals: 3 findings; severity ceiling `high`; 0 critical, 1 high, 1 medium, 1 low.
