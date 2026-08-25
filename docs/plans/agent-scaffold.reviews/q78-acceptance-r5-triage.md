# Q-78 acceptance pass 5 triage

## Scope and verification

I independently read both pass-5 reports, all four preceding acceptance triages, the Q-83 decision, the repaired plan sidecars and Success Criteria, the current source, and `AGENTS.md`. This triage judges the repaired planning product, not an implementation of its proposed schema.

Using `/nix/store/4rayq0a6f1cq2cdcxm6cnhnlgqgbdjhk-source/target/debug/agent-flow`, I reproduced:

- `validate --source docs/plans/agent-scaffold.plan.toml`: 467 records and 114 steps / 83 questions valid.
- `validate --workflow --source docs/plans/agent-scaffold.plan.toml`: workflow invariants hold.
- `render --check --strict docs/plans/agent-scaffold.plan.toml`: up to date.
- `agent-flow checks` through a scratch-only `PATH` shim: 1 passed, 0 failed, 0 skipped.
- `git diff --check`: passed.

The historical phase/identity population reproduces by resolving a round's step as its structured `step`, or `task` with a trailing `-inc<alnum>` removed, then testing it against the current Roadmap: 63 Roadmap-owned `plan_review` rounds, 202 Roadmap-owned `work_review` rounds, 36 non-Roadmap `plan_review` rounds, eight non-Roadmap `work_review` rounds, and four non-Roadmap `acceptance` rounds. The 63 Roadmap-owned plan-review rounds have 18 exact task identities. In particular, `structured-skeleton` has three and `checks-runner-worktree-name-collision` has four; both task tokens are current Roadmap step slugs. The eight non-Roadmap work-review rounds span `workflow-hardening`, `metrics-fields`, `q59-backlog-fold`, `decision-fold-q60-q62`, `q64-capture`, `q65-capture`, and `ship-v0-0-4`.

A scratch TOML plan declaring both a `real-step` Roadmap step and `orphan_tasks = ["real-step"]` fails source validation with `meta orphan task \`real-step\` is also a step slug, so it is not orphan`. This reproduces the claimed inability to register the two colliding plan-review identities as task loops without weakening the orphan invariant.

I also reproduced the Stage-2 contradiction by reading the authoritative type sketch. Its sole displayed `ReviewLoop` has mandatory `risk_class`, `round`, and `consecutive_clean`, takes `Open { declared_risk_class }`, and includes `Acceptance | Review` in `Phase` (`docs/plans/mealy-workflow-driver.explorations/r2-architecture-build-path.md:103-130`). The same document requires acceptance and standalone review to be single-pass and to reconstruct without a declaration lookup (`:142-152`). Thus the shown type has no legal single-pass state: it requires exactly the class and convergence fields the surrounding contract forbids.

No high or critical finding is dismissed, so an independent dismissal re-check is not owed.

## Deduplication

- Claude finding A and GPT R5-G1 are one high-severity migration/identity-coverage defect.
- Claude finding C and GPT R5-G3 are one low-severity stale-Q-82-gate defect. Claude supplies three remaining sites; GPT independently establishes the live YAGNI contradiction.
- Claude finding B, GPT R5-G2, and Claude finding D are distinct: respectively non-Roadmap work-review coverage, the Stage-2 single-pass type, and stale current-history evidence.

## Verdicts

### R5-1 — Claude A / GPT R5-G1: valid, `high`

The repaired two-arm model covers Roadmap `work_review` and registered-task `plan_review` only (`docs/plans/agent-scaffold.steps/structured-risk-class-source.md:7-13`; `docs/plans/agent-scaffold.steps/review-loop-foreclosure-enforcement.md:7-9`). It promises fail-closed joins and preservation of current Roadmap and task-loop identity/class without rewriting the log (`structured-risk-class-source.md:9,15,43-44`). The reproduced 63 Roadmap-resolving `plan_review` records are neither arm as written. The seven `structured-skeleton` and `checks-runner-worktree-name-collision` records cannot use the task arm: their task is a real step slug, while the source rejects a step slug in `orphan_tasks` (`src/plan/source.rs:755-769`). They cannot honestly be made Roadmap `work_review` histories either, because their recorded phase is `plan_review` and phase is load-bearing in the proposed reconstruction.

This is new evidence, not a re-raise of R4-2: R4-2 established an authority home for the genuine orphan `q78-design-pass` task loop. This finding demonstrates a different live phase/owner shape that the two homes cannot represent. It is high because the promised append-only, fail-closed migration has no legal state for existing converged history; it must either fail permanently or force an implementer to invent an identity policy on the authority path. It is not critical because the proposed implementation fails loudly rather than silently accepting a weaker bar.

Smallest safe disposition: specify and test a phase-preserving mapping for every Roadmap-resolving `plan_review` identity before implementation. That mapping must cover the two step-slug identities and the declared-increment population, preserve exact phase, identity, and class, and neither admit a Roadmap step into `orphan_tasks` nor relabel plan review as work review. Add a phase-blind-grouping red control and current-history fixtures for `structured-skeleton`, `checks-runner-worktree-name-collision`, and `workflow-enforcement-tier-fold`.

### R5-2 — Claude B: valid, `medium`

The repaired contract closes `TaskConvergencePhase` to `plan_review` and expressly rejects task-level `work_review` (`structured-risk-class-source.md:7,39`), while Roadmap increments necessarily belong to a `[[step]]`. The reproduced eight non-Roadmap work-review records therefore resolve to neither declaration arm. Current W3 iterates Roadmap steps only (`src/workflow.rs:466-497`), so the existing shape is invisible to convergence enforcement rather than being rejected.

The plan may choose to treat a non-Roadmap work review as invalid workflow input rather than add another convergence declaration arm, but it cannot leave the choice implicit. As written, its broad fail-closed and future-enforcement claims do not say how these retained records are classified, migrated, or prohibited, and a future event of the same shape can still evade the proposed declaration check. The impact is medium: this is a real unrepresented loop shape and a silent enforcement gap, but it does not itself make a Roadmap step converge incorrectly or lose data.

Smallest safe disposition: either add a typed non-Roadmap work-review declaration/selection arm, or explicitly make that shape invalid in workflow validation, state the bounded historical treatment for the eight records, and pin a record-379-shaped fixture plus a red future record. A prose-only exclusion that leaves a new record accepted and unjoined is insufficient.

### R5-3 — GPT R5-G2: valid, `medium`

The architecture's concrete `ReviewLoop` type cannot implement its own single-pass contract. It requires an authoritative class at `Open` and stores streak/cap-relevant state for every `Phase`, including acceptance and standalone review, while the repaired architecture and `workflow-driver-typed-fleet` require those phases to have no declaration lookup or convergence arithmetic (`r2-architecture-build-path.md:103-152`; `docs/plans/agent-scaffold.steps/workflow-driver-typed-fleet.md:17-20`). Calling the single pass “degenerate” does not make its forbidden risk class or counters unconstructible.

This is distinct from R4-6, which corrected the omitted `QuestionMachine` and full fleet scope. It is a medium design contradiction: an implementer must invent a load-bearing state variant or fabricate a meaningless risk class, but the product has not yet implemented the engine.

Smallest safe disposition: model convergence and single-pass processing as disjoint typed variants. The single-pass variant must have no constructible risk class, streak, foreclosure, or cap state while retaining the required high/critical dismissal re-check.

### R5-4 — Claude C / GPT R5-G3: valid, `low`

R4-4's two cited sites were repaired, but the retained requirements record still contains the same active real-parallelism gate at `docs/plans/mealy-workflow-driver.explorations/r2-requirements-scope.md:34,67,175`. The last is a YAGNI imperative that directly forbids the fleet and scheduler that Q-82 schedules. The focused sidecars remain clear enough that this does not block implementation, but the acceptance documentation-currency criterion is not met.

Smallest safe disposition: add the same bounded Q-82 supersession at all three sites, preserving the separate write-path and authoritative-driving gates. One documented, clearly scoped historical note is acceptable only if it unambiguously covers all three live directives.

### R5-5 — Claude D: valid, `low`

The current-history paragraph says acceptance records 432 and 433 are the separate single-pass records (`docs/plans/agent-scaffold.steps/review-loop-foreclosure-enforcement.md:13`), but the log has four such records at `docs/metrics/workflow.jsonl:432-435`. The rule the paragraph is meant to establish remains correct, so this is low severity, but the claimed current-history fixture was already stale when the repair edited that paragraph.

Smallest safe disposition: replace the growing ordinal enumeration with the durable selector `task == "q78-design-pass" && phase == "acceptance"`, and retain the assertion that those selected records do not enter the task's plan-review convergence window.

## Result

Five distinct shortfalls are valid: one `high`, two `medium`, and two `low`. No finding is invalid or accepted as residual. Q-78 cannot settle acceptance until the high migration gap is planned and repaired; the remaining valid dispositions should be folded with it rather than silently scoped away.
