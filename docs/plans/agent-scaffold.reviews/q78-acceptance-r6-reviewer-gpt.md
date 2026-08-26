# Q-78 acceptance pass 6 - GPT reviewer

## Verdict

Three acceptance shortfalls remain: one `high` and two `low`. No `critical` or `medium` finding.

The pass-5 repair correctly digest-pins the exact-step plan-review and unowned-work-review histories, separates convergence from single-pass processing in the concrete type design, and replaces the growing acceptance-ordinal list with a durable selector. The principal remaining defect is an interaction the repair does not disposition: it permanently assigns the thirteen Q-81 implementation increment identities to `plan_review`, while the delivery state machine requires those same not-yet-built increments to be declared for `work_review`.

Q-78 remaining `open` pending acceptance is deliberate and is not itself a finding.

## Shortfalls

### R6-G1 - `high`: the phase-preserving migration consumes all thirteen Q-81 delivery increment identities as plan-review-only

The new declaration contract gives each Roadmap increment exactly one phase and requires a new identity to change phase (`docs/plans/agent-scaffold.steps/structured-risk-class-source.md:9-14`). The migration then assigns all sixteen retained increment identities their observed `plan_review` phase, including all thirteen Q-81 identities, and promises to retain every id and class (`docs/plans/agent-scaffold.steps/structured-risk-class-source.md:34,45,59-60`). This is internally consistent for reconstructing history.

It is not executable for the work those increments still own. All thirteen Q-81 identities belong to five `not-started` Roadmap steps (`docs/plans/agent-scaffold.plan.toml:1524-1624`), and their sidecars define future delivery under those exact ids: the status-opening prose edit, ledger edit, two order-deletion increments, eight intent implementation/backfill increments, and missing-source code repair (`docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md:33-39`; `docs/plans/agent-scaffold.steps/ledger-order-citation-currency.md:52-58`; `docs/plans/agent-scaffold.steps/plan-order-array-position.md:41,273`; `docs/plans/agent-scaffold.steps/step-intent-encoding.md:61,524,825`; `docs/plans/agent-scaffold.steps/validate-missing-source-exit.md:31-35`). Q-81 expressly keeps the eight intent ids (`docs/plans/agent-scaffold.plan.toml:2482-2488`).

The active-work design, however, permits `implementation` and `work_review` only on an increment declared for `work_review`, retains that exact `(step, increment)` across the delivery transition, and rejects a phase mismatch (`docs/plans/agent-scaffold.steps/workflow-loop-visibility.md:11-18,30-33`). After the planned migration, none of the thirteen can legally enter implementation: changing one to `work_review` makes its retained plan-review rounds mismatch, while leaving it `plan_review` makes the delivery active row invalid.

Reproduce the collision directly from the retained Q-81 window:

```bash
sed -n '387,430p' docs/metrics/workflow.jsonl \
  | jq -r 'select(.type=="round") | [.step,.increment,.phase] | @tsv' \
  | sort -u
```

This prints thirteen rows, all `plan_review`, for exactly the increment declarations at `docs/plans/agent-scaffold.plan.toml:1536-1624`; their five owners are all `not-started`. The output includes no separate work-review delivery identity.

This is `high` because the fail-closed implementation reaches no legal state for the very work Q-78 is meant to schedule. An implementer must either weaken the one-phase invariant, relabel append-only history, or invent and propagate thirteen new delivery identities through the plan, sidecars, Q-81, and the existing waiver. None is planned or authorised. It is not `critical` because the specified parser should reject the conflict loudly rather than produce a false green.

Disposition: separate these completed plan-review histories from the live delivery declarations. For example, give the thirteen Q-81 windows a bounded typed historical plan-review representation and leave their existing implementation increments declared for `work_review`; alternatively, explicitly plan new delivery ids and update every owning criterion and waiver. Preserve the recorded phases and do not make one id silently carry both phases.

### R6-G2 - `low`: the authoritative architecture still says Stage 3 is gated after Q-82 schedules it

The repaired architecture now says Q-82 supersedes the real-parallelism gate and schedules the typed fleet and read-only scheduler (`docs/plans/mealy-workflow-driver.explorations/r2-architecture-build-path.md:233-234`). The same authoritative document still says Stage 3 remains behind its evidence gate, calls the scheduler gated, and recommends holding Stage 3 (`:239,253,264`). `workflow-driver-typed-fleet` points implementers to this detailed build path as an authority (`docs/plans/agent-scaffold.steps/workflow-driver-typed-fleet.md:3`), while Q-82 and the Roadmap unambiguously schedule the scheduler (`docs/plans/agent-scaffold.plan.toml:1752-1756,2495-2501`).

This is new evidence beyond R5-4's three `r2-requirements-scope.md` sites, which are repaired. It is `low` because the focused scheduler sidecar and the adjacent corrected architecture paragraph resolve the implementation direction, but the documentation-currency criterion is still unmet. Mark the stale ordering/recommendation sentences as historical and Q-82-superseded, while retaining the distinct write-path and authoritative-driving gates.

### R6-G3 - `low`: the live pass-6 checkpoint omits Q-83 from the queue it claims to name

The current ledger anchor explicitly records Q-83 and its chosen authority rule (`docs/plans/agent-scaffold.ledger.md:541`), but its current queue paragraph lists decided Q-80 through Q-82 only and says branch-only product state ends at Q-82 (`docs/plans/agent-scaffold.ledger.md:549`). The structured source has Q-83 `decided`, folded into `structured-risk-class-source`, with receipt `Q-83` (`docs/plans/agent-scaffold.plan.toml:2503-2508`; decision record 468 in `docs/metrics/workflow.jsonl`).

This does not change the immediate pass-6 action and the plan remains authoritative, so severity is `low`. It is nevertheless stale durable resume state in the checkpoint that says it names the queue rather than counting it. Add Q-83 or replace the duplicated inventory with a pointer/query over the structured queue.

## Pass-5 disposition verification

- R5-1's historical representability repair is accurate on its stated data: the current log contains 63 Roadmap-resolving `plan_review` rounds over 18 identities, including the seven exact-step records and the 41 Q-81 rounds. All seven pinned exact-step SHA-256 values reproduce. R6-G1 is the new delivery-lifecycle collision created by treating the thirteen still-unbuilt Q-81 increment identities as single-phase live plan-review declarations.
- R5-2 is closed for the retained non-Roadmap work reviews. Records 1, 47, 48, 164, 173, 177, 178, and 379 have the stated tasks/classes, and all eight pinned digests reproduce. The proposed exact historical rows cannot satisfy W3, and a future unowned work review is specified to fail.
- R5-3 is closed. `ReviewProcess::{Convergence, SinglePass}` is disjoint throughout the focused sidecar and detailed type sketch; single pass has no constructible class, streak, foreclosure, or cap and retains the dismissal re-check.
- R5-4's three cited requirements/YAGNI sites are closed. R6-G2 identifies uncured contradictory statements in the separate detailed architecture authority.
- R5-5 is closed. Every `task == "q78-design-pass" && phase == "acceptance"` record is selected independently of ordinal and remains outside the records-380-through-386 plan-review window; the current log has five such acceptance records.
- Q-58 remains correctly reopened and `exploring`, with a frozen pre-result protocol and mechanical non-inferiority/equivalence rule required before carrier selection. Q-80/Q-81/Q-82/Q-83 are registered as decided with matching receipts.

## Gates and evidence

All build/test outputs were written under `/tmp/q78-r6-gpt-*`; the reviewed tree remained clean until this findings file was authored.

- `validate --source docs/plans/agent-scaffold.plan.toml`: `468 records, valid`; `114 steps, 83 questions, valid`.
- `validate --source docs/plans/agent-scaffold.plan.toml --workflow`: `workflow invariants hold`.
- `render --check --strict docs/plans/agent-scaffold.plan.toml`: `up to date`.
- `agent-flow checks`: 1 passed, 0 failed, 0 skipped.
- `cargo test --locked --offline`: 470 passed, 0 failed.
- `cargo clippy --all-targets --locked --offline -- -D warnings`: passed.
- `git diff --check` passed for the pass-5 repair and pass-6 brief commits. The 16 pass-5 repair files are ASCII-clean.
- The record-386 adoption digest reproduces as `4e7aed64e77ca228347de1cfbcf620ca2d6b6f3d8550b606212b3b448d0e95c6`; all 15 other historical digests introduced by the pass-5 repair also reproduce.

Totals: 3 findings; severity ceiling `high`; 0 critical, 1 high, 0 medium, 2 low.
