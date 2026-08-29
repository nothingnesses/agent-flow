# Q-86 decision-fold plan review, round 2, reviewer `claude-opus-5` (`claude-code`)

Target: `main` (`1009ea82`) through branch tip `aaaa2e7c` on `review/q86-decision-r2-claude`. Criteria: `AGENTS.md`, `.agents/prompts/reviewer.md`, the plan's Project Principles, and the six valid verdicts in `docs/plans/agent-scaffold.reviews/q86-decision-r1-triage.md`.

## Scope and method

I read `AGENTS.md`, `.agents/prompts/reviewer.md`, the round-1 triage, the new proof sidecar `docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md`, the Q-86/Q-88/Q-89/Q-90/Q-91 question sidecars and their `[[question]]` sources, the two new `type:"decision"` receipts, `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md` and the three retained proposals, the five retained `q86-synthesis-r*-triage.md` triages, `workflow-calibration.md`, the Success Criteria, the plan TOML and the rendered projection. I did not read either reviewer's round-1 findings file or any peer round-2 worktree; the round-1 triage is the settled ledger I worked from.

Gates, run in this worktree after `nix develop --command cargo build`:

```text
./target/debug/agent-flow render --check --strict docs/plans/agent-scaffold.plan.toml
# docs/plans/agent-scaffold.plan.toml: up to date                     (exit 0)
./target/debug/agent-flow validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl
# docs/metrics/workflow.jsonl: 497 records, valid
# docs/plans/agent-scaffold.plan.toml: 115 steps, 91 questions, valid (exit 0)
./target/debug/agent-flow validate --source docs/plans/agent-scaffold.plan.toml --workflow
# docs/plans/agent-scaffold.plan.toml vs docs/metrics/workflow.jsonl: workflow invariants hold (exit 0)
git diff --check main...HEAD                                          # exit 0
for f in $(git diff --name-only main...HEAD); do LC_ALL=C grep -cP '[^\t\x20-\x7e]' "$f"; done
# 0 for all 14 changed files
```

Append-only history holds: `caa6cd90`->`ba0da096`->`57e1e211` moves `docs/metrics/workflow.jsonl` 494 -> 495 -> 497 lines with no line rewritten, and the two appended records are the Q-86 and Q-91 receipts.

## The six round-1 fixes, each verified

**T1, duplicate order 36 - fixed.** `order = 117` at `docs/plans/agent-scaffold.plan.toml:490`. `grep '^order = ' docs/plans/agent-scaffold.plan.toml | awk '{print $3}' | sort -n | uniq -d` prints nothing; `main`'s maximum was 116, so nothing collides and nothing moves. The rendered Roadmap confirms it: `docs/plans/agent-scaffold.md:304` is the 115th and last data row (rows run 190-304), so no pre-existing row changed position. The `plan-order-array-position` historical map survives, because its premise is that 84 and 91 are the only absent `order` values (`docs/plans/agent-scaffold.steps/plan-order-array-position.md:279`); `comm` against `seq 1 117` still yields exactly `84` and `91`, so a citation at or above 92 still drifts by two and 117 still resolves to position 115. The immediate-position claim is gone and replaced by a structured sequencing rule at `bounded-convergence-option-b-proof.md:9`, which is the second branch the triage's exact correction allowed. No new `order <n>` or `step <n>` citation was introduced, so the `plan-order-array-position` worklist grep is unaffected.

**T2, temporary-directory contradiction - fixed.** `bounded-convergence-option-b-proof.md:150` now requires two passes over the five root-relative commands with a fresh temporary state directory created *outside* the repository per invocation and an explicit "do not change the working directory", plus a before/after `git status --porcelain=v1 --untracked-files=all` and a whole-tree path/type/content manifest asserted byte-identical after the tenth invocation. Criterion 13 (`:168`) matches that prose exactly, and `:152` was strengthened from "must not modify a tracked file" to "a tracked or untracked repository file". The bare-temporary-directory acceptance environment the triage rejected is gone.

**T3, traceability checker must derive its set - fixed.** `:21`, `:124`, `:148` and criterion 11 (`:166`) all require the checker to parse all five triages, pair each `### T<n>` heading with its verdict record, derive round-qualified valid ids, and fail on any row-set, row-count, disposition-set or summary mismatch, with "No hard-coded expected set or count can satisfy this criterion." The five triage paths are now arguments of command 4 (`:144`), so the parse is structurally forced. I re-derived the source set independently and it matches the sidecar's `valid_findings=51`:

```sh
for n in 1 2 3 4 5; do awk '/^### T/{t=$2} /^- \*\*Verdict/{ if ($0 ~ /valid/ && $0 !~ /invalid/) print t }' \
  docs/plans/agent-scaffold.reviews/q86-synthesis-r$n-triage.md | sort -u | wc -l; done
# 13 12 9 8 9  -> 51
```

The verdict label differs across files (`- **Verdict and severity:**` in r1, `- **Verdict:**` in r2-r5); a parser keyed on only one form leaves 17 unconsumed T sections in r1, which `:124`'s "unconsumed T section fails closed" turns into a failure rather than a silent pass.

**T5, cross-phase routing - fixed.** All six sub-requirements of the exact correction are present: distinct `DiscoveryPhase`/`CanonicalOwnerPhase` state (`:34`, `:53`, `:64`); the four derived routes (`:55-58`); a completed prior owner that retains the finding with no transfer, reopen or replenishment and reaches a named terminal disposition (`:56`); a future owner that retains it until its own campaign (`:57`); atomic fixtures for acceptance-to-completed-work, early-work-to-future-owner and mixed out-of-phase batches (`:71`) with matching mandatory mutation classes (`:132`) and acceptance criteria 4, 5 and 12; and the bounds re-derived (`:118`). `:60` closes the two named cases explicitly.

**T6, multi-owner initial credit versus `L_q` - fixed, and the algebra re-checks out.** The old "Atomic batches may advance several initial owners at once" is replaced by scheduled-owner-only credit at `:35`, `:47`, `:49` and criterion 10, with the two ownership axes separated at `:47`. I re-derived every published bound from the repaired transition relation: `sum_q L_q = |O| + (m+1)`, so `L_B = r_plan + |O| + m + 1`; `sum_q C_q = 4|O| + (m+1)`, plus the separate seven-batch sealed plan review, so `R_B = 4|O| + m + 8`; and `I_B = 4(4|O| + m + 8) + 2|O| + 6 = 18|O| + 4m + 38` at four agents per batch plus two repairs per obligation and six plan repairs. The `n_q = 0` edge is consistent (`L_q = C_q = 1`, the blind-closure batch). The same values appear unchanged in `Q-86.md:21`, `plan.toml:2591`, `workflow-calibration.md:30`, `Q-86-synthesis.md:104-120` and `Q-86-safety-process.md:342`.

**T7, stale recommendation framing - fixed.** `Q-86-safety-process.md` section 10 is now "HISTORICAL RECOMMENDATION BEFORE Q-86", every clause is past tense, and both the low-confidence rating and the blocking-proof boundary are retained, which is what the correction asked for. Section 12 and the state-machine proposal's parallel sections were moved to past tense the same way.

## Implementer simulation

Reading the sidecar as instructions: create `docs/plans/workflow-calibration.proofs/` with the five named artefacts plus `fixtures/`; run the five commands from the repository root twice with `TMPDIR`/cache redirected to a fresh external directory per invocation; bracket the ten invocations with the two snapshots. The command form matches established repo precedent (`Q-86-safety-process.md:534`), `PYTHONDONTWRITEBYTECODE=1` suppresses the one repository write Python would otherwise make, every path is repository-root-relative and every referenced input exists today. The mutation runner is confined to an in-memory model or a temporary copy (`:134`), so it cannot collide with the manifest assertion. Every body requirement has a matching acceptance criterion, and every criterion traces back to body text; the failure return (`:174-176`) agrees verbatim in intent with `Q-86.md:39`, `Q-86-synthesis.md:203` and `workflow-calibration.md:32`, and none of them pre-authorises a fallback. The blocking-gate direction holds: no step declares `blocked_by = ["bounded-convergence-option-b-proof"]` because no production unit was authored, and `review-loop-foreclosure-enforcement` enforces the *current* cap and foreclosure, which Q-86 explicitly leaves unchanged, so it is correctly not gated.

No production authority leaks. `grep -rn 'Q-86\|Q-91' README.md CHANGELOG.md pack/ .agents/ src/ tests/` returns nothing, the diff touches no file outside `docs/`, and criterion 15 restates the boundary. Documentation currency holds for the status change: `agent-scaffold.success-criteria.md` no longer contains `exploring` (0 matches), and every sidecar that previously said Q-86 was open now says so in the past tense at its own decision point.

## Findings

Two valid findings, both **low**. No critical, no high, no medium.

### R2-C1 - the repaired M2 phase-completion predicate deadlocks the future-owner route it introduces (low)

- **Evidence.** `ae0b74c7` added, in the same paragraph that introduces the phase routes, `docs/plans/workflow-calibration.explorations/Q-86-safety-process.md:330`: "A future-owner finding remains live without spend or initial credit until that campaign is scheduled. ... A settled complete map **with no prior- or future-owner route** finishes the phase or family as applicable." Applied to a phase, the second sentence makes a live future-owner route block phase completion, while the first sentence makes that route live until a later phase runs. The authoritative step sidecar does not have this problem: it attaches the identical condition only to the family-level stage 6, `bounded-convergence-option-b-proof.md:37` ("`Complete` is constructible only after ... no prior-owner or future-owner route remains live"), and states the future-owner rule at `:57`.
- **Reproduction.** Freeze the phase order `<w1, w2, acceptance>` with obligation `X` owned by `acceptance`. A `w1` batch discovers a finding for `X`; `:330` and sidecar `:57` both route it `FutureOwnerPending` and keep it live. `w1` may then finish only on "a settled complete map with no prior- or future-owner route", which cannot clear before `acceptance` is scheduled, and `acceptance` is scheduled only after `w1` and `w2` finish. No legal continuation exists. This is not a hypothetical corner: sidecar criterion 5 (`:160`) makes an "early-work-to-future-owner" fixture mandatory, and `:132` makes "early-work-to-future-owner activation or loss" a mandatory mutation class.
- **Reasoning.** The two documents now disagree about where the no-live-route predicate applies, and the exploration is the document the synthesis names as the mapping source for the selected option (`Q-86-synthesis.md:11`: "Selected Option B maps to safety M2 plus the state-machine proposal's sealed authority envelope"), so an implementer building the reference model from M2 encodes the deadlock. It fails closed rather than admitting an unsafe delivery, and the mandatory fixture would surface it, which is why this is low rather than higher; but the likelier repair path is the quiet one, narrowing early cross-phase discovery out of the model and silently weakening the T5 fix.
- **Exact correction.** In `Q-86-safety-process.md:330`, scope the no-prior-or-future-route condition to family completion only, and state the phase-completion condition separately as a settled complete map for that phase's own obligations with no live prior-owner route, matching `bounded-convergence-option-b-proof.md:37`.

### R2-C2 - the fold asserts the ledger resume anchor is current, and it is not (low)

- **Evidence.** `docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md:128` closes the planning and documentation traceability rows partly by "leaves the orchestrator-owned ledger to its already-current resume anchor". That anchor, `docs/plans/agent-scaffold.ledger.md:535`, says the gates "pass with 496 metrics records, 115 steps, and 91 questions" and that "The immediate next action is plan-review round 1". Both are wrong at this tip, and the ledger contradicts itself in the same section: `docs/plans/agent-scaffold.ledger.md:551` says "497 metrics records, 115 steps, and 91 questions" and "THE IMMEDIATE NEXT ACTION IS DECISION-FOLD ROUND 2".
- **Reproduction.**

  ```text
  ./target/debug/agent-flow validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl
  # docs/metrics/workflow.jsonl: 497 records, valid
  wc -l docs/metrics/workflow.jsonl                       # 497
  git show 57e1e211:docs/metrics/workflow.jsonl | wc -l   # 497, i.e. wrong when the anchor was written too
  ./target/debug/agent-flow next --source docs/plans/agent-scaffold.plan.toml --json | grep -o '49[67] metrics records'
  # 496 metrics records
  # 497 metrics records
  ```

  Lines 535 and 551 are both inside the single `## RESUME STATE` block (`:329`-`:1742`) that `next` echoes verbatim, so the contradiction is what tooling actually hands a resuming orchestrator.
- **Reasoning.** The resume anchor is the durable reconstruction source named by `AGENTS.md:99-100`, and a resuming agent that compares "496" against `validate`'s 497 has to decide whether a record was appended out of process. The counting the convergence rule depends on is safe, because `AGENTS.md:61` puts it in the round-records narrative, which is the correct half at `:551`. That is why this is low and not higher. It is still a false verifiable claim inside the reviewed diff.
- **Exact correction.** The planner may not edit the ledger (`AGENTS.md:91` reserves the resume anchor for the orchestrator), so either drop the unverified "already-current" clause from `bounded-convergence-option-b-proof.md:128` and name the ledger move as an orchestrator integration duty, as the retained `q86-synthesis-r1-triage.md` T12 disposition did, or have the orchestrator correct the count and next-action sentence when it moves the anchor for round 2.

## Severities with nothing to report

No **critical** and no **high** findings. No **medium** findings: I specifically tried and failed to break the repaired algebra (`L_q`, `C_q`, `L_B`, `R_B`, `I_B` all re-derive from the transition relation as written), the four-route reducer in the step sidecar, the derived 51-verdict traceability gate, the mutation-class coverage against criterion 12, the command/path set, and the production-authority boundary.

## Considered and deliberately not raised

- **`57e1e211` and `ae0b74c7` commit a source edit without its regenerated view** (`render --check --strict` exits 1 at both, 0 at `d7660671` and `aaaa2e7c`), which reads against `AGENTS.md:30` "commit the source and the generated view together". This is the repository's established fold-then-render pattern, not something this branch introduced: `b3e53951` / `c9b4e866` on `main` are the same pair. The tip is clean.
- **The five retained triages are not mechanically pinned against the findings-file cleanup rule** (`AGENTS.md:67`), and `src/plan/source.rs:236-239` documents that `[step.provenance].findings` are shape-checked, not existence-checked. Not a defect: the project's practice is to carve named evidence out of cleanup by naming it in the plan, and `061a0166` did exactly that, deleting the narrow-round triages and the synthesis reviewer files while keeping these five.
- **`docs/plans/workflow-calibration.proofs/` is a new directory suffix** not named in `AGENTS.md`, and it sits under the `workflow-calibration` prefix rather than the owning step's slug. It is internally consistent across the artefact list and all five commands, it keeps the proof beside the retained prototypes it must supersede, and no tooling enumerates `docs/plans/*` by suffix.
- **The removal of the explicit per-round T-id enumeration** (`57e1e211`'s `:87-93`) is the correct direction under Principle 16, since the retained triages become the single source the checker derives from.
- **A `CompletedPriorOwner` finding blocks delivery at any severity**, which is stricter than selected floor `high`. It is stated consistently in the sidecar (`:56`, criterion 4), the synthesis (`:99`) and M2 (`:330`), and follows from non-transferable authority rather than from the floor, so it is a design property, not an inconsistency.
- **Equal discovered tag and mutation counts** (`:148`). The round-1 triage settled this as T4-invalid, and the expanded `:132` class list gives me no new evidence that a single tag provably needs two mutations.
- **`agent-flow next` reports the `workflow-calibration` loop at 12 rounds against a cap of 5.** Identical on `main`; the fold appends no `round` record, so it neither caused nor changed this.
- Prose line length and formatter reflow, per `AGENTS.md:108` and the reviewer prompt.

## Summary

Valid findings: **2**. 0 critical, 0 high, 0 medium, 2 low. All six round-1 fixes verified as correct and complete, with the two lows arising from the round-2 repair itself (R2-C1) and from a currency claim it makes about an out-of-diff durable source (R2-C2).
