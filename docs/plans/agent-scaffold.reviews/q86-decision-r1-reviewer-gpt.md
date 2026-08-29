# Q-86 decision-fold plan round 1 review — plan soundness and proof obligations

Reviewed `main...485443d9` as a risky plan artifact. I verified the Q-86 and Q-91 question records and their unique JSONL receipts, the five retained triages, the narrowed synthesis, the new proof step, the TOML sources, Success Criteria, and generated plan. The retained valid-verdict sets total 51 (`13 + 12 + 9 + 8 + 9`), and the declared increment is `risky`. Strict render and workflow validation pass, but they do not detect the findings below.

## Finding 1 — High: the proof can omit findings discovered in one phase against obligations owned by another phase

**Evidence.** The selected synthesis requires stable finding identity to survive “later phases” and defines an atomic batch as an arbitrary finite owner-to-findings map (`docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:60-61`). The proof plan instead says `PhaseCampaign(q)` owns exactly `O_q` (`docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md:35`), discusses incidental cross-owner work only in terms of obligations receiving initial attempts “in that phase” (`:47`), and requires merely “several owners” in states “where they are legal” (`:55-57`). Neither the fixtures, mutation list, nor acceptance criteria require the decisive cases where acceptance discovers a critical owned by an already-closed work phase, or an early work phase discovers a finding owned by a future phase. Reproduce the omission with:

```sh
rg -n -i 'cross-phase|later phase|prior phase|future phase|closed phase|phase.*reopen|reopen.*phase' docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md
```

The command finds no cross-phase routing obligation; its only reopen/phase matches describe per-phase ownership and priority. Because the plan also makes blind closure non-transferable and single-use (`:35`), an implementation can declare out-of-phase owner events illegal, satisfy the same-phase “several owners” fixtures, and never prove whether a later serious finding re-enters the old campaign, uses remaining authority, or terminally blocks the family. That is silently weaker than the selected synthesis and can leave a late critical outside the proved delivery predicate.

**Correction.** Define the owner-map domain across all of `O`, not only `O_q`, and specify the typed route for a finding discovered in phase `q` whose canonical owner is in a prior, current, or future phase. State how an already blind-closed owner campaign behaves without transferring or replenishing authority and re-derive the family bounds. Require fixtures and killing mutations for at least: acceptance critical -> completed work owner, early-work finding -> future owner, and one atomic batch mixing current- and out-of-phase owners; each must preserve the finding and block delivery or reach an explicit non-delivery terminal.

## Finding 2 — Medium: multi-owner initial advancement contradicts the formulas called minimums

**Evidence.** The proof plan explicitly permits one atomic batch to advance several initial owners and says this “can lower observed cost” (`docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md:47`). It nevertheless requires the proof to derive `L_q = n_q + 1` and `L_B = r_plan + |O| + m + 1` as minima (`:92-106`, acceptance criterion 10 at `:155`). For `n_q = 2`, the allowed one batch advancing both initial owners followed by the separate blind-closure batch costs two review batches, while the claimed minimum is three. This is the exact unresolved branch of round-3 T1, whose correction required recomputing the minimum if one batch can satisfy several initial attempts (`docs/plans/agent-scaffold.reviews/q86-synthesis-r3-triage.md:32`). The same stale minima remain in the selected synthesis (`docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:101-115`) and Q-86 decision sidecar (`docs/plans/agent-scaffold.questions/Q-86.md:21`).

**Correction.** Choose one coherent model before proof implementation: either charge/permit exactly one initial review batch per obligation, so an atomic cross-owner finding does not advance other owners' initial attempts, or retain multi-owner advancement and replace `L_q`, `L_B`, the cost table, Q-86 durable wording, and acceptance outputs with correctly qualified lower bounds/minima (including `n_q = 0`, `1`, and `>1`). Keep `C_q` only after independently proving it remains a safe upper bound.

## Finding 3 — Low: the new step does not have a unique Roadmap priority

**Evidence.** The proof step and the already-existing `instrument-flag` step both have `order = 36` at `docs/plans/agent-scaffold.plan.toml:490` and `:513`, while the new sidecar and Success Criterion claim a distinct order-36 step immediately after order 35 (`docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md:9`; `docs/plans/agent-scaffold.success-criteria.md:41`). Reproduce the only duplicate with:

```sh
awk '/^order = /{c[$0]++; lines[$0]=lines[$0] " " FNR} END{for(k in c)if(c[k]>1)print k, c[k], lines[k]}' docs/plans/agent-scaffold.plan.toml
```

It prints `order = 36 2  490 513`. `agent-flow validate --source ... --workflow` still passes, so the structural gate does not supply uniqueness.

**Correction.** Assign the proof a unique priority and align every order claim in the sidecar, workflow-calibration fold, Success Criteria, and generated plan. If “immediately after 35” is load-bearing, renumber safely rather than relying on declaration-order tie-breaking; otherwise remove that claim and encode the real sequencing mechanism explicitly.

## Finding 4 — Low: the retained safety proposal still presents a completed decision as provisional advice

**Evidence.** The safety proposal's updated status says Q-86 selected Option B (`docs/plans/workflow-calibration.explorations/Q-86-safety-process.md:5`), and the same recommendation section later acknowledges the human selection (`:493`). But that section still says “Provisional recommendation” and “advice for the human choice” in present tense (`:474-478`). This is stale decision-state wording inside a retained source that the proof traceability matrix must cite.

**Correction.** Relabel the section and sentences as the historical recommendation/input that preceded Q-86, while retaining the low-confidence reasoning and proof boundary. Do not describe an already-receipted choice as pending advice.

## Counts

- Critical: 0
- High: 1
- Medium: 1
- Low: 2
- Total: 4
