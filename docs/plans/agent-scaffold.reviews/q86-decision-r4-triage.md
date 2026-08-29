# Q-86 decision-fold plan review, round 4 triage

## Scope and reproduction

I independently read `AGENTS.md`, the triager prompt, the Q-86 proof step, Q-86/Q-91 decision sources, the retained synthesis and safety proposal, the prior decision-fold triages, both round-4 reviews, the proof prototypes, the ledger retention record, the scheduler specification, and the current plan source and projection. The reviewed artifact remains planning-only; no proof artefact or production bounded-convergence unit exists.

The current mechanical gates reproduce:

```text
nix develop --command cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml
# docs/plans/agent-scaffold.plan.toml: up to date
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl
# docs/metrics/workflow.jsonl: 499 records, valid
# docs/plans/agent-scaffold.plan.toml: 115 steps, 91 questions, valid
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow
# docs/plans/agent-scaffold.plan.toml vs docs/metrics/workflow.jsonl: workflow invariants hold
git diff --check main...HEAD
# exit 0
```

Five raw reports consolidate to four findings: Claude Finding 1 and GPT F1 identify the same missing closure scope-product. All four consolidated findings are valid. None re-raises a prior settled finding without new evidence.

## T1 - Blind closure must compose the scope disposition with the owner/dismissal route product

- **Sources:** Claude Finding 1; GPT F1.
- **Verdict:** valid, **medium**.
- **Reproduced evidence:** The proof calls its table the one "exhaustive route product" at `docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md:76`, but rows `:78-85` cover owner route and serious-dismissal disposition only. A finding still carries an independent scope relation (`:91`), and the required product fixtures apply in every legal authority state (`:95-104`), including scope-plus-dismissal and high-plus-critical scope cases. The same step requires a critical scope result to remain delivery-blocking while its attached re-checks settle (`:106`). The selected safety package has distinct scope outcomes: low backlog, medium human scope decision, high scope re-check then terminal or in-scope, and critical `SeriousBlocked` regardless of re-check result, at `Q-86-safety-process.md:242,255-260` and `Q-86-synthesis.md:61-67`. Neither the closure table nor its closure-specific fixtures, acceptance criterion, or mutations says how that axis composes at `BlindClosureDiscovery(q)`.
- **Reasoning:** Treating the owner table as exhaustive leaves a closure-discovered scope component unmatched; coercing it to `UnownedInScopeFinding` changes the defined scope policy. In particular, the existing acceptance wording can be satisfied without testing that a pending high scope re-check holds closure open or that either critical scope result remains non-delivering. This is a blocking proof-specification hole around an explicit safety invariant, but the proof still fails closed before any production authority, so medium is proportionate.
- **Required correction:** Define scope disposition before or as a product with the owner routes for closure. Cover low backlog, medium terminal scope decision, high pending/upheld/overturned scope re-check behavior, and critical `SeriousBlocked`; closure must remain pending for either scope or dismissal re-check, and an overturned high must then take its applicable owner route. Add closure-state fixtures, an atomic scope-plus-dismissal fixture, killing mutations, and acceptance wording; align the retained synthesis and safety proposal with the selected choice.

## T2 - A skipped proof satisfies the planned generic scheduler dependency and bypasses the claimed completion gate

- **Source:** GPT F2.
- **Verdict:** valid, **high**.
- **Reproduced evidence:** The proof requires every later bounded-convergence production unit to use `blocked_by = ["bounded-convergence-option-b-proof"]` and says that completion is its gate (`docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md:21,206`). The accepted scheduler specification instead treats a blocker with either `complete` or `skipped` status as satisfied (`docs/plans/agent-scaffold.steps/workflow-ready-frontier-scheduler.md:7,28-31`). `Skipped` explicitly means "is this step done?" is answered no and is not an exemption (`src/plan/source.rs:175`). The current `next` implementation is stricter, checking only `Complete` (`src/next.rs:742-760`), but the earlier scheduler unit is planned to replace that behavior and explicitly tests skipped blockers as ready. Thus a later production step with the only required proof dependency can become scheduler-ready after the proof is skipped.
- **Reasoning:** A proof that is incomplete because it failed is held by the present wording, but one that is skipped is not. That violates the selected decision's explicit "completed proof" boundary and creates a future path around the safety proof for a widely used workflow mechanism. No production unit exists now, but leaving the representation unchanged would authorize the bypass when the planned scheduler and later production units land. The impact is high.
- **Required correction:** Preserve the generic scheduler's intentional `complete`-or-`skipped` behavior, but represent this proof dependency as an explicit complete-only gate (for example a typed blocker policy) and enforce it in scheduler/validation selection. Require red controls that a skipped proof, and every other non-`complete` proof state, keeps a bounded-convergence production unit blocked; update the proof step, future scheduler authority, and the production-unit planning contract together.

## T3 - The proof commands select Python through a mutable global registry rather than the repository lock

- **Source:** GPT F3.
- **Verdict:** valid, **low**.
- **Reproduced evidence:** Each prescribed command uses `nix shell nixpkgs#python3` (`bounded-convergence-option-b-proof.md:173-177`). On this worktree, `nix registry list` resolves global `flake:nixpkgs` to mutable `nixpkgs-unstable` channels, whereas this repository's lock pins `nixpkgs` at `d407951447dcd00442e97087bf374aad70c04cea` (`flake.lock`). Nothing in the command binds `nixpkgs#python3` to that lock.
- **Reasoning:** The proof is required to be exactly reproducible across runs and machines. A registry-selected interpreter can change independently of the repository and can therefore change proof behavior despite identical source. This is an assurance/reproducibility defect in a future proof command, not evidence of a current proof-oracle failure, so low is proportionate.
- **Required correction:** Bind the five commands to the repository lock, for example with `nix shell --inputs-from . nixpkgs#python3 -c python3 ...`, or add the selected Python to a lock-bound development shell. A separately stated minimum Python version is useful only if the proof relies on a compatibility range; lock-bound resolution is the required part.

## T4 - The owning `workflow-calibration` sidecar still states Option B minima without their delivery domain

- **Source:** Claude Finding 2.
- **Verdict:** valid, **low**.
- **Reproduced evidence:** `docs/plans/agent-scaffold.steps/workflow-calibration.md:26` calls `n_q + 1` and `r_plan + |O| + m + 1` minima without qualifying their clean, ordinarily delivering `Complete` domains. The proof step defines those domains and admits shorter legal early-terminal/non-delivery paths at `bounded-convergence-option-b-proof.md:136-152`; the selected synthesis, Q-86 sidecar, structured ask, and Success Criteria carry the qualification (`Q-86-synthesis.md:101-123,161`, `questions/Q-86.md:21`, and `success-criteria.md:41`).
- **Reasoning:** The proof gate remains correct, so this cannot make a conforming proof unsound. But the active owning calibration step leaves the formula in a form its own selected proof rejects, which is a documentation-currency defect.
- **Required correction:** Qualify both minima in `workflow-calibration.md` as clean, ordinarily delivering `Complete`-domain minima and state that legal early-terminal and non-delivery paths may be shorter. Re-render the generated plan rather than editing it directly.

## Outcome, counts, and backstop

**Outcome: `new_valid`.** Raw findings: **5**. Deduplicated valid findings: **4** - **0 critical, 1 high, 1 medium, 2 low**. Invalid findings: **0**. Accepted residual risks: **0**.

No high- or critical-severity finding was dismissed; the high finding is upheld. **No independent dismissal backstop re-check is owed.** This risky plan-review round is not clean, so its consecutive-clean streak remains zero.
