# Q-78 acceptance pass 3 - GPT reviewer

## Verdict

Four acceptance shortfalls: one `high`, two `medium`, and one `low`. No `critical` finding.

The pass-2 repairs close their named dispositions: task-scoped plan-review/acceptance representation exists; the typed fleet now depends on and reuses the foreclosure reconstruction; the Q-58 protocol freezes its statistical degrees of freedom before trials; the ledger anchor is current; the workflow-driver handover is current; the historical cap adoption is typed and digest-pinned; TOML waiver guidance has focused ownership; the historical output measurement has exact provenance; the changed-path count is corrected; and the authored-openings successor is named. The remaining findings are defects in the expanded design or in those repairs, not re-raises of settled findings.

Q-78 remaining `open` pending this acceptance pass is deliberate and is not a finding.

## Shortfalls

### R3-G1 - `high`: the structured-risk repair leaves two authoritative classes and preserves a false green that lowers a declared `risky` bar

`structured-risk-class-source` says each loop's round records become the **only** authoritative class and that no product source change is needed (`docs/plans/agent-scaffold.steps/structured-risk-class-source.md:1`, `:7`, `:22-25`). But the plan schema still requires `[[step.increment]].risk_class` and documents it as the increment's convergence class that sets the required streak (`src/plan/source.rs:257-265`). Every newly scheduled increment, including this repair's own, declares that TOML value. Nothing in the repair removes, demotes, or reconciles it with `round.risk_class`.

The existing checker reads only the first round's class and checks agreement only among that increment's round records (`src/workflow.rs:496-505`); `PlanToml::step_views` drops the declared increment data entirely (`src/plan/source.rs:416-430`). The repair explicitly plans no source change, so the following false green remains after it lands. Run from an authorised scratch directory with the built binary:

```bash
S=<authorised-scratch>/risk-source-mismatch
mkdir -p "$S/docs/plans" "$S/docs/metrics"
cat > "$S/docs/plans/risk.plan.toml" <<'EOF'
[meta]
title = "risk"
primary = "toml"

[[step]]
slug = "dangerous"
title = "Dangerous"
status = "complete"
order = 1
blocked_by = []
folds = []
waiver = []

[[step.increment]]
id = "dangerous-inc1"
risk_class = "risky"
EOF
cat > "$S/docs/metrics/workflow.jsonl" <<'EOF'
{"type":"round","task":"dangerous-inc1","step":"dangerous","increment":"dangerous-inc1","artifact":"dangerous","phase":"work_review","changed_since_prev":true,"outcome":"clean","valid_findings":0,"severities":[],"consecutive_clean":1,"risk_class":"low_risk"}
EOF
agent-flow validate --workflow --source "$S/docs/plans/risk.plan.toml" --metrics "$S/docs/metrics/workflow.jsonl"
```

Observed: exit 0 and `workflow invariants hold`. The TOML says `risky` (two clean rounds), while one `low_risk` clean round completes it. This directly defeats the expanded Success Criterion that rebuilding cannot silently buy a cheaper bar (`docs/plans/agent-scaffold.success-criteria.md:37`). It also leaves no durable authoritative class at loop-open if the TOML field is truly ignored: before the first completed round, `next` represents `risk_class` and `required_streak` as null (`src/next.rs:225-232`), while the repair removes the ledger copy.

Resolve the two structured homes explicitly. The chosen design needs a durable loop-open class and a fail-closed relationship between that value and every round; merely declaring the completed round authoritative leaves the pre-round state unrecorded and permits the demonstrated downgrade.

### R3-G2 - `medium`: the phase carrier removes the existing ready-to-plan and blocked actions before the scheduler exists

The new step-scoped carrier accepts only `in-progress` steps (`docs/plans/agent-scaffold.steps/workflow-loop-visibility.md:9-12`, criterion 1 at `:24`). With no carrier row, `selected_action` is absent (`:16`). Thus a fresh plan whose first step is `not-started`, or a plan whose pending step is blocked, cannot be represented at all.

Those are existing Stage-1 states, not future scheduler features: `LoopState::ReadyToPlan` and `Blocked` are explicit (`src/next.rs:273-279`), and `select_active_loop` currently selects a ready pending step or a blocked pending step after checking in-progress work (`src/next.rs:704-731`). A one-step fresh plan currently yields `state: ready-to-plan`, role `planner`, and transition `start-plan`. The proposed compatibility criterion preserves only "review-state fixtures" (`workflow-loop-visibility.md:29`), so it does not catch this regression.

The later Stage-3 scheduler cannot make an independently shipped first stage correct, especially because Stage 2 and Stage 3 are blocked on the Q-58/Q-59 and foreclosure chain. Add typed pending/blocked representation or retain the existing pending fallback until the scheduler replaces it, and pin both legal states on human and JSON surfaces.

### R3-G3 - `medium`: the focused Stage-3 scheduler contradicts the canonical architecture it says it reuses

The focused step says it reuses `workflow-driver` Stage 3 (`docs/plans/agent-scaffold.steps/workflow-ready-frontier-scheduler.md:3`), but the two specifications define different functions:

- The canonical architecture schedules only `NotStarted`/`Next` steps and treats blockers in either `Complete` or `Skipped` as satisfied (`docs/plans/mealy-workflow-driver.explorations/r2-architecture-build-path.md:153-161`).
- The focused step instead uses an undefined "nonterminal/current state permits work" population and requires every blocker to be strictly complete (`workflow-ready-frontier-scheduler.md:7`, `:17-19`). It also requires review and acceptance candidates in the frontier (`:20`), although Q-82's corrected carrier makes acceptance task-scoped (`workflow-loop-visibility.md:9`) and the scheduler calls itself step-granularity.
- Criterion 5 requires `selected_action` to be a frontier member whenever the step frontier is non-empty (`workflow-ready-frontier-scheduler.md:21`), but the preceding visibility stage selects from task- and step-scoped active units (`workflow-loop-visibility.md:16`); a task-scoped acceptance action can therefore be selected while an independent step frontier is non-empty.

An implementer cannot preserve the canonical scheduler, satisfy the focused blocker rule, and include task-scoped acceptance in a step-only frontier simultaneously. Define one eligibility domain, one `skipped`-blocker policy, and precedence between task actions and the step frontier, then make the focused sidecar and canonical architecture agree.

### R3-G4 - `low`: the retained Q-58 design still instructs CI-overlap selection after forbidding it

The repaired pre-run protocol correctly says interval overlap alone is not evidence of equivalence/non-inferiority and requires the frozen test and margin (`docs/plans/code-value-audit.explorations/Q-58-ablation-design.md:80-95`). The later, still-live Agent-variance guidance nevertheless says to use "CI-overlap for the knee" (`:116`). That is the superseded selection rule pass 2 was meant to remove.

The mandatory protocol and owning step are strong enough that this is `low`, but it is contradictory experiment guidance on the exact degree of freedom R2-G3 closed. Replace the stale phrase with the frozen non-inferiority/equivalence procedure and retain confidence intervals as reported uncertainty, not the decision rule.

## Verification of pass-2 dispositions

- Legal task phases: the task/step union now represents plan review and acceptance without faking implementation status. R3-G2 is new evidence about pending states omitted by that repair.
- Reconstruction reuse: `workflow-driver-typed-fleet` is blocked by `review-loop-foreclosure-enforcement` and explicitly consumes its reviewed result.
- Pre-run ablation protocol: margin, confidence/test method, state/model aggregation, disagreement, tie rule and analysis command are frozen before results. R3-G4 is the one stale contrary sentence.
- Historical cap adoption: record 386 is a `q78-design-pass` `plan_review` round, and SHA-256 over its raw JSON bytes without the line ending is `4e7aed64e77ca228347de1cfbcf620ca2d6b6f3d8550b606212b3b448d0e95c6`, matching the planned boundary.
- TOML waiver guidance, measurement provenance, the seven-plus-changelog path count, the canonical workflow-driver wording, and the authored-openings handover are all repaired as triaged.
- The event log has 464 valid records: 311 rounds, 17 escalations, 133 decisions, 2 intakes and 1 dismissal recheck, with zero waiver records. Q-80/Q-81/Q-82 receipts resolve and Q-80 exactly aliases `Q-78-classinherit`.

## Gates

The flake development shell was not usable in this container, so I used the available Nix-store Rust 1.95.0 toolchain and GCC wrapper directly, with `HOME`, `TMPDIR`, `CARGO_HOME`, and `CARGO_TARGET_DIR` under the authorised reviewer scratch.

- `validate --source docs/plans/agent-scaffold.plan.toml`: `464 records, valid`; `114 steps, 82 questions, valid`.
- `validate --workflow --source docs/plans/agent-scaffold.plan.toml`: `workflow invariants hold`.
- `render --check --strict docs/plans/agent-scaffold.plan.toml`: `up to date`.
- `cargo test --locked`: 470 passed, 0 failed across all test binaries.
- `cargo clippy --all-targets --locked -- -D warnings`: passed.
- `git diff --check`: passed.

Totals: 4 findings; severity ceiling `high`; 0 critical, 1 high, 2 medium, 1 low.
