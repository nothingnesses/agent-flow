# Q-78 acceptance pass 6 triage

## Scope and verification

I independently read both pass-6 reports, acceptance triages 1–5, Q-81 and Q-83 in the TOML plan source, the repaired planning product, the live ledger, and `AGENTS.md`. This triage judges the planning product and its executable migration requirements, not an unimplemented schema change.

Using `/nix/store/4rayq0a6f1cq2cdcxm6cnhnlgqgbdjhk-source/target/debug/agent-flow`, I reproduced:

- `validate --source docs/plans/agent-scaffold.plan.toml`: 468 records and 114 steps / 83 questions valid.
- `validate --workflow --source docs/plans/agent-scaffold.plan.toml`: workflow invariants hold.
- `render --check --strict docs/plans/agent-scaffold.plan.toml`: up to date.
- `agent-flow checks` through a scratch-only `PATH` shim: 1 passed, 0 failed, 0 skipped.
- `git diff --check` and `git diff --check f79c92a7..HEAD`: passed.

All probes that copied or mutated data used `/tmp/q78-r6-triage.c5Ce5G`; the reviewed tree stayed clean.

## Deduplication

- Claude A and GPT R6-G1 both concern the new phase-bearing migration, but are distinct. Claude A finds three currently retained identities with no authorised declaration route; GPT R6-G1 finds a future-delivery collision for the thirteen Q-81 identities even if their historical plan-review records are represented.
- GPT R6-G2 is new evidence outside R5-4's adjudicated `r2-requirements-scope.md` sites.
- The stale drift measurement and the ledger queue omission are independent documentation-currency defects.

## Verdicts

### R6-G1 — GPT: valid, `high`

The thirteen Q-81 records at log lines 387–430 reproduce as thirteen exact `(step, increment, plan_review)` identities. Their five owning Roadmap steps are all `not-started`. `structured-risk-class-source.md:11,34,60` requires each of those retained ids to be declared `phase = "plan_review"`, gives an increment only one phase, and requires a new identity to change phase. In contrast, `workflow-loop-visibility.md:11-12,33` requires the exact increment that enters implementation and work review to be declared `work_review`, retaining the same `(step, increment)` identity across that delivery lifecycle.

Thus every Q-81 id is consumed by its preserved plan-review history and cannot enter its stated delivery path: switching it to `work_review` rejects history, while retaining `plan_review` rejects implementation/work review. This is a high-severity failure of the proposed fail-closed state model for all thirteen scheduled delivery increments. It is not critical because the intended implementation rejects the conflict rather than silently accepting it.

Smallest safe disposition: preserve the Q-81 append-only plan-review histories in a bounded typed historical Roadmap-increment-plan-review representation, leaving the existing delivery increments declared `work_review`. Update the migration prose and fixtures so the 41 records, their phases, classes, and escalation segmentation remain exact, but cannot consume the live delivery declaration. The alternative—new delivery ids—requires reopening Q-81 and updating every affected step, criterion, and waiver, so it is not the smallest safe repair.

### A — Claude: valid, `medium`

The complete log population reproduces as 99 `plan_review` records: 63 Roadmap-resolving records over 18 identities and 36 non-Roadmap records. Three identities have no route in the proposed migration:

- Lines 210–214 are `step = "decision-folder-currency"`, no `increment`, and `task = "decision-folder-currency-fold"`; the plan declares only `decision-folder-currency-inc1` (`agent-scaffold.plan.toml:1259`). The exact-match mapping in `structured-risk-class-source.md:16` therefore cannot join these records.
- `q77-fold` appears at lines 358, 361, 362, and 364, and `step-intent-fold` at lines 368, 369, 370, 373, 374, and 376. Neither is in `[meta].orphan_tasks` (`agent-scaffold.plan.toml:1-24`), so neither can receive the exact `[[task_loop]]` required by `structured-risk-class-source.md:12,16`.

The assertion that all sixteen increment identities retain existing declarations is consequently false for `decision-folder-currency-fold`, and the changed-plan-source worklist's restriction to *registered* task histories omits the two task identities. These records either fail the promised fail-closed implementation or remain accepted and unjoined. This is a medium shortfall: the classes are unambiguous (`low_risk`) and the repair has a clear, bounded route, but the current migration plan cannot implement its claimed complete history coverage.

Smallest safe disposition: author an exact `decision-folder-currency-fold` plan-review declaration with its observed class; register `q77-fold` and `step-intent-fold` and add exact task-plan-review declarations; and extend the current-history criterion to cover all 99 plan-review records, including a red unregistered-task control. Reconcile this work with R6-G1's required historical Q-81 representation rather than preserving the now-invalid instruction that all sixteen increment declarations are live `plan_review` declarations.

### B — Claude: valid, `low`

The dated measurement in `sidecar-status-opening-drift.md:19-25,29,116,205` claims 45 / 36 / 28 / 19. Running its selectors and H1-style scratch copy now produces 44 unanchored selections, 35 anchored selections, 27 unanchored stripped openings requiring authoring, and 18 anchored handover openings. The historical `f05c3678` tree produces the old shape; the current difference includes `workflow-driver`, whose opening was changed by the acceptance repair from the stale status claim to the delivered-foundation wording.

The criteria deliberately do not hard-code those totals, so implementation remains executable, but the sidecar's explicitly dated human-decision evidence is stale. The decision was previously re-put when this measurement moved; leaving its current value unsupported defeats that established safeguard.

Smallest safe disposition: remeasure and correct the dated paragraph, identify the `workflow-driver` movement, and re-put the changed handover-size premise through the existing Q-78 decision path (or durably record the human-approved reason it does not reopen the decision). Do not convert a moving count into an acceptance pass condition.

### R6-G2 — GPT: valid, `low`

The repaired Stage-3 bullet correctly says Q-82 lifts the former real-parallelism gate for the typed fleet and read-only scheduler (`r2-architecture-build-path.md:234`). The same detailed architecture still says the near-term path stops at Stage 2 and that “3/4/5/6 stay behind their evidence gates” (`:239`), calls the scheduler gated (`:253`), and recommends holding all of 3–6 (`:264`). The focused sidecars and Q-82 schedule Stage 3, so these retained directives contradict the document's own later Q-82 statement.

This is low severity because the focused scheduler sidecar and the corrected Stage-3 bullet provide the executable authority, but it is a stale contradictory architecture source and fails the acceptance documentation-currency requirement.

Smallest safe disposition: mark the pre-Q-82 Stage-3 recommendation as superseded history and limit the remaining evidence gates to Stages 4–6, preserving the distinct write-path and authoritative-driving gates.

### R6-G3 — GPT: valid, `low`, orchestrator-owned

The current resume anchor records Q-83 and its selected authority rule (`agent-scaffold.ledger.md:541`); the plan has Q-83 as decided and folded into `structured-risk-class-source` (`agent-scaffold.plan.toml:2503-2508`), with its receipt at `workflow.jsonl:468`. Yet the checkpoint inventory at `agent-scaffold.ledger.md:549` says it names the queue while listing only decided Q-80 through Q-82 and describing branch-only state as Q-79 through Q-82.

This is stale durable resume state. It is low severity because the plan remains authoritative and the immediate action is unchanged, but a resumer is directed to an incomplete queue inventory.

Smallest safe disposition: the orchestrator should update the ledger inventory and branch-only range to include Q-83, or replace the duplicated inventory with an accurate pointer to the structured queue. This is an orchestrator ledger correction, not planner-owned product work.

## Result

Five distinct acceptance shortfalls are valid: one `high`, one `medium`, and three `low`. No finding is invalid or accepted as residual. The high finding is upheld, not dismissed, so no independent high/critical dismissal re-check is owed. Acceptance cannot settle until the valid planning and ledger dispositions are repaired and verified in a later acceptance pass.
