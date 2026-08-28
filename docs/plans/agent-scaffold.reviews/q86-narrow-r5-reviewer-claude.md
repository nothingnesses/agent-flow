# Narrowed Q-86 round 5 review (claude)

## Scope, method, and reproduction

I reviewed `main...HEAD` (`2c58cffd...4d0d737b`) as the risky narrowed Q-86 decision artefact, independently and in my own worktree. I read `AGENTS.md`, `.agents/prompts/reviewer.md`, the Q-86 and Q-88 structured records and sidecars, the owning `workflow-calibration` step sidecar, the Success Criteria, the narrowed synthesis, both retained proposals, the retained brief, both prototypes, the four prior narrowed triages, and the five Q-86 synthesis triages the proof gate names. I did not read the other round-5 reviewer. I changed nothing outside this file.

Baseline checks, both passing:

```sh
nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml
# docs/plans/agent-scaffold.plan.toml: up to date
nix develop -c cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow
# 489 records, valid; 114 steps, 88 questions, valid; workflow invariants hold
```

`git diff --stat main...HEAD` touches only `docs/metrics/workflow.jsonl`, `docs/plans/`, and the two exploration prototypes. No `src/`, `tests/`, `pack/`, `.agents/`, `README.md`, `CHANGELOG.md`, or workflow-spec path changed, so the artefact's own no-change claim at `Q-86-synthesis.md:7` holds and nothing in this pass alters shipped behaviour.

## Round-4 fixes: two verified closed, one closed only in part

- **T3 (human-facing formulas used undefined symbols).** Closed. `Q-86.md:7` now glosses `m` as the work-loop count "here and below", and `:8` defines `O`, `n_q = |O_q|`, and `r_plan` ("one at low risk and two at risky") before first use. The structured ask carries the same glosses at `agent-scaffold.plan.toml:2565-2566`, projected at `agent-scaffold.md:179` and `:5078-5079`. `render --check --strict` is up to date.
- **T2 (B's comparison and recommendation understated its inherited plan-review costs).** Closed on every surface the correction named. `Q-86-synthesis.md:169` now reads "while retaining A's sealed plan-review controller", `:170` "on top of A's plan-review account and reserve fields", `:174` "its inherited five-normal-plus-two-reserve values are weakly calibrated", `:182` "B does not replace A's plan machinery: it inherits A's sealed plan-review controller...", and `:184` adds the inherited constants to the low-confidence list. The qualification is propagated to `Q-86.md:8,15` and `agent-scaffold.plan.toml:2566,2569`. The added contrast "A keeps streak and budget as separate stopping concepts **throughout**" against B's "for post-freeze phases" is accurate given `:103`. No published bound changed (`git show 01dfe5d4`).
- **T1 (serious-floor recommendation lacked Principle-judged reasoning).** Closed in shape, not in substance. A rationale paragraph now exists on all three surfaces and is rendered, but its affirmative half names two principles that are not in the plan's Project Principle set. See finding 1.

## What else I re-derived and found sound

- **Every published number reproduces.** The authoritative selector returns ten passes and `[7,10,5,6,5,5,4,2,1,0]`. A stopping at pass seven leaves `2+1+0 = 3` shortfalls whose `severities` are all `low`; C stopping at pass three leaves `6+5+5+4+2+1+0 = 23`, with `high` present at passes 4, 5 and 6, so "including further highs" holds. The floor sentence's "passes three through six" names exactly the passes carrying a `high`. "Nineteen" reproduces as 19 clean-outcome records with `valid_findings > 0`, all with `consecutive_clean >= 1`. Six of the ten Q-78 triage files remain.
- **The algebra is internally consistent.** `sum(4n_q + 1)` over `p = m + 1` post-freeze phases is `4|O| + m + 1`; `+7` for the inherited plan slice gives `R_B = 4|O| + m + 8`. `L_B = r_plan + |O| + m + 1`. `I_B = 4R_B + 6 + 2|O| = 18|O| + 4m + 38`. A's `14 + 7 + 7 + 6 = 34`. Every figure agrees across `Q-86-synthesis.md`, `Q-86.md:7-9`, `agent-scaffold.plan.toml:2565-2567`, and `agent-scaffold.steps/workflow-calibration.md`.
- **The cost table survives the round-3 split.** Plan review is priced separately from post-freeze phases, B's plan rows reuse A's minima "reusing A's sealed plan controller", and every body row matches the header width with escaped `\|O\|`. The whole-family cells reconcile with the per-row minima for all three options.
- **Earlier documentation repairs still hold.** `n_a` (synthesis r5 T9) has no occurrence anywhere; the superseded state-machine graph counts (r5 T8) are gone; the published controller digest `8a349c68...` matches `sha256sum` of the retained file and the historical `d0dabe6d...` is bound to commit `ad989b5f` at `Q-86-safety-process.md:403,555` and `Q-86-state-machine.md:467`; both prototypes retain their in-file limitation notices; the retained brief is off `exploring` (`Q-86-convergence-mechanism-brief.md:5`).
- **The receipt is exact.** One `type:"decision"` record, `q_id:"Q-88"`, the six option labels in the recorded order, `recommendation` and `chosen` both `Narrow the proof scope`. It matches `Q-88.md:7-16` label for label, `Q-88` is `decided -> folded into workflow-calibration` (`agent-scaffold.plan.toml:2598-2600`), and W4 passes. `git diff main...HEAD -- docs/metrics/workflow.jsonl` adds exactly that one line, so `Q-86-synthesis.md:7` is accurate.
- **The prototype boundary is a faithful summary of round 5.** The six bullets at `Q-86-synthesis.md:49-55` map one-to-one onto `q86-synthesis-r5-triage.md` T1-T6 and `:56` covers T7. Nothing overstates what the prototypes established.
- **No hidden authority.** `Q-86-synthesis.md:188,199,207,223,246`, `Q-86.md:25,29,43`, `agent-scaffold.plan.toml:2573,2582`, and `agent-scaffold.success-criteria.md:41` all make the proof unit an explicit blocker for every production implementation unit, forbid an automatic fallback architecture or floor, and keep `defer` fail-closed by requiring a receipted floor decision before the proof can close. Gate item 8 forbids an unresolved critical reaching delivery under either floor. I found no path that grants implementation or architecture authority.
- **Currency.** The narrowing touches planning and prototype-status records only; the step sidecar, Success Criteria, brief, and both proposals are consistent with the narrowed gate, and no shipped prompt or product doc is made stale.

## Findings

Two findings, both `low`. **Zero critical, zero high, zero medium.**

### Finding 1 — the round-4 floor rationale names two principles that are not the plan's Project Principles

- **Severity:** low.
- **Evidence:** The round-4 repair (`01dfe5d4`) added this sentence to `Q-86-synthesis.md:217`, `Q-86.md:37`, and `agent-scaffold.plan.toml:2580`, projected at `agent-scaffold.md:179` and `:5108`:

  > `high` is recommended under **Make failure and absence explicit** and **Correctness before performance** ... Its cost under Ground decisions in evidence and Minimal by default is ...

  The plan declares exactly eight `[[principle]]` entries, and neither cited name is among them:

  ```sh
  grep -c '^\[\[principle\]\]' docs/plans/agent-scaffold.plan.toml
  # 8
  awk '/^\[\[principle\]\]/{p=1} p&&/^name = /{print; p=0}' docs/plans/agent-scaffold.plan.toml
  # "Prefer the cleaner long-term architecture over the smallest diff" / "Minimal by default" /
  # "Safe on existing projects" / "Idempotent" / "Make illegal states unrepresentable" /
  # "Ground decisions in evidence" / "Reproducible" / "Structured data first, project for humans"
  sed -n '2617,2656p' docs/plans/agent-scaffold.plan.toml \
    | grep -c 'Make failure and absence explicit\|Correctness before performance'
  # 0
  ```

  Both names come from the harness-agnostic list in `AGENTS.md:123,128` (items 10 and 15 of the numbered guidance principles), which is a different set from the plan's Project Principles. The cost half of the same sentence does name plan principles ("Ground decisions in evidence", "Minimal by default"), so the sentence half-satisfies the contract: the case *for* the recommended floor rests on no plan principle at all.

  Every other decision surface in this repository uses the plan set. The architecture recommendation in the same artefact names three plan principles for and three against (`Q-86-synthesis.md:182,184`); the Principle comparison table at `:167-176` uses all eight; `Q-88.md:27-36` judges itself against all eight; and the folded Q-83/Q-84/Q-85 decisions cite them by number and name (`agent-scaffold.md:176-178`, e.g. "Principle 5, Make illegal states unrepresentable").
- **Why this is a defect:** `AGENTS.md:41` settles the human-input contract once for every human-input point: the reasoning must be "judged against **the plan's Project Principles** by name". The floor is one of the two decisions Q-86 puts to the human, and `q86-narrow-r4-triage.md:15-20` ruled the missing rationale valid precisely on that contract, correcting it to "a concise Principle-named comparison and rationale". The repair supplies prose but not the named judgement the contract and the verdict require, so a human cannot check the safety case against the eight principles they own, and the round-4 verdict is not actually closed on its affirmative half. The round-4 reviewer's suggested wording used plan principles (`q86-narrow-r4-reviewer-claude.md:53`: "Make illegal states unrepresentable and Safe on existing projects"); the implemented wording substituted names from outside the set.
- **Why low:** the options, their consequences, and the `defer` escape remain stated and mutually consistent; `critical` is still correctly identified as the mandatory minimum; gate item 8 (`Q-86-synthesis.md:199,219`) still requires the selected proof to model both floors. No bound, count, or authority boundary changes, and the substantive argument (fail-closed on an open high, at an evidence and minimality cost) is present and correct on its merits.
- **Suggested correction:** restate the affirmative half against the plan's own principles — for example `high` under **Make illegal states unrepresentable** (an unresolved serious finding is structurally undeliverable rather than discretionary) and **Safe on existing projects** (the stricter floor fails closed on adoption) — keeping the existing cost half under Ground decisions in evidence and Minimal by default. Mirror the change to `Q-86.md:37` and `agent-scaffold.plan.toml:2580` and re-render.

### Finding 2 — Option C's per-phase automated-agent maximum is not derivable in the narrowed artefact, and the artefact's only stated composition contradicts it

- **Severity:** low.
- **Evidence:** `Q-86-synthesis.md:87` states the one per-batch composition the artefact carries, for Option A: "With two reviewer calls, at most one triage, at most one re-check, and at most six repairs per phase". Applied to A's seven batches this reproduces `I_A = 34(m + 2)` at `:90` exactly: `7*2 + 7*1 + 7*1 + 6 = 34`. (Only the per-batch reading works; reading all four rates as per-phase gives `2 + 1 + 1 + 6 = 10`.)

  Option C states no composition at all. `:139` says only "For each of the `m + 2` phases, the proposed maximum is four review batches and fifteen automated-agent calls", and `:143` publishes `I_C = 15(m + 2)`. Carrying A's stated rates onto C's four batches plus C's two repair generations (`:137`, "at most `Repair1` and `Repair2`") gives `4*(2 + 1 + 1) + 2 = 18`, not 15. The artefact never states the seat counts for `Verify1` and `Verify2`; `:146` states them only for the *minimum* path (Discovery two reviewers, BlindClosure one). At least two allocations reach 15 (`5 + 4 + 4 + 2` and `7 + 4 + 2 + 2`), so a reader cannot recover which, or tell whether 15 or 18 is intended.

  The derivation exists only in the mapped source: `Q-86-state-machine.md:312` gives Candidate B (= Option C, per the provenance map at `Q-86-synthesis.md:15`) "at most four review batches, five reviewer passes, four triage calls, four backstop calls, and two repair passes", i.e. `5 + 4 + 4 + 2 = 15`. The unexplained figure is a headline comparison number, republished at `Q-86.md:9`, `agent-scaffold.plan.toml:2567`, and `agent-scaffold.md:179,5080`, and it backs the claim at `Q-86-synthesis.md:163` that "C has the lowest fixed per-phase maximum".
- **No relitigation:** this is not narrowed round-1 T4, whose verdict and correction were scoped to C's *minimum* (two batches, three reviewer calls) and were applied at `:146`. This is the *maximum* at `:139,143`, which that repair did not touch. The new evidence is the arithmetic conflict: the only composition the narrowed artefact states yields 18 for C, so the gap is not merely an absence but an apparent contradiction on the artefact's own terms. It is the same class as narrowed round-2 T2 (A's acceptance allocation available only in the mapped source) and round-4 T3 (symbols defined only in the synthesis), both ruled valid and low.
- **Why low:** the figure does not change the ranking — at 15 or at 18, C's per-phase maximum is still the lowest of the three — no whole-family bound is wrong, and gate item 9 (`:200`) already requires the selected-option proof to "prove every selected-option transition and algebraic bound", so nothing here can reach implementation unchecked. The derivation is one hop away in the mapped proposal.
- **Suggested correction:** add C's per-batch allocation to `Q-86-synthesis.md:139` in the same form A already uses — four batches with five reviewer passes (two at Discovery, one each at `Verify1`, `Verify2`, and `BlindClosure`), four triage calls, four re-checks, and two repair passes, hence fifteen — so `I_C` reconstructs from the artefact. Do not change the published bound.

## Counts

**Zero critical, zero high, zero medium, two low.** I found nothing of critical, high, or medium severity: no surface grants implementation, architecture, or floor authority; every published bound, count, digest, and receipt reproduces; the proof gate, failure path, and no-decision boundary are fail-closed on all surfaces; and the prototypes remain correctly quarantined with their round-5 limitations stated. Neither finding re-raises a settled verdict without new evidence; round-1 T6 (the retained state-machine induction claim, ruled invalid) is untouched, and the deferred r1-r5 synthesis proof obligations are respected as deferred rather than re-raised.
