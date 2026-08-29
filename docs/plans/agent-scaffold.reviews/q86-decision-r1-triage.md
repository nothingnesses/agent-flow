# Q-86 decision-fold plan round 1 triage

## Scope and reproduction

I independently read `AGENTS.md`, `.agents/prompts/triager.md`, the decision fold, its rendered projection, Q-86/Q-91 source and JSONL receipts, the new proof sidecar, the five retained synthesis triages, the plan-order decision material, and both reviewer reports. I judged the current decision-fold sources, not the historical prototype as an implementation: the requested proof files do not exist yet.

The source and projection are mechanically current:

```text
nix develop --command cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml
# docs/plans/agent-scaffold.plan.toml: up to date
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl
# 496 records, valid; 115 steps, 91 questions, valid
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow
# workflow invariants hold
git diff --check 8dff38e2..HEAD
# exit 0
```

I independently derived the retained valid-verdict set from the verdict lines: round 1 has 13 (`T1`–`T8`, `T10`–`T12`, `T14`, `T16`), round 2 has 12, round 3 has 9, round 4 has 8 (`T1`–`T6`, `T8`, `T10`), and round 5 has 9, for 51 total. The Q-86 and Q-91 JSONL decision receipts exactly match their structured question records and both name `bounded-convergence-option-b-proof` as their task/fold target.

Eight raw findings consolidate to seven: Claude F1 and GPT Finding 3 are the same duplicate-order and historical-position defect. Six consolidated findings are valid: one high, three medium, and two low. Claude F4 is invalid. No finding is accepted as a residual risk.

## T1 — Duplicate order 36 makes the new proof unit's position and the historical citation map ambiguous

- **Sources:** Claude F1; GPT Finding 3.
- **Verdict:** valid, **medium**.
- **Reproduced evidence:** `docs/plans/agent-scaffold.plan.toml:487-513` assigns `order = 36` to both `bounded-convergence-option-b-proof` and `instrument-flag`; `awk '/^order = /{print $3}' ... | sort -n | uniq -d` prints `36`. The renderer sorts equal values by slug (`src/plan/render.rs:177`), so the current rendered positions are 36 for `bounded-convergence-option-b-proof` and 37 for `instrument-flag` only because `bounded...` lexically precedes `instrument...`. `docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md:9`, `workflow-calibration.md:30`, and `agent-scaffold.success-criteria.md:41` all make a position/order-36 claim. More importantly, `plan-order-array-position.md:279` declares the obsolete position mapping that citations through 83 are safe, 85–90 drift one, and 92+ drift two. Inserting the duplicate shifts the rendered positions from 37 onward, invalidating that premise and leaving `order-36` outside the step's space-separated citation matcher.
- **Reasoning:** This is not a renderer defect: equal-order slug tie-breaking is intentional. It is a plan-data and documentation-currency defect introduced by the fold. It makes the new numerical identifier non-unique and invalidates a load-bearing historical map used by the planned order-field migration; that migration can otherwise preserve the wrong citations after `order` is removed.
- **Exact correction:** Make the proof step's ordering unambiguous rather than relying on the slug tie-break. If immediate position after 35 is required, use a unique ordering representation and update the affected subsequent ordering/citation map; otherwise choose a unique existing position and replace the immediate-position claim with the actual structured sequencing rule. In either case, update all new order references, correct the `plan-order-array-position` historical mapping and worklist boundary for the inserted row, make the `order-36` spelling visible to that migration or restate it by slug now, then re-render and re-run the plan-order evidence commands.

## T2 — The temporary-directory acceptance condition contradicts the exact root-relative commands

- **Source:** Claude F2.
- **Verdict:** valid, **medium**.
- **Reproduced evidence:** The sidecar says to run the five commands from the repository root at `bounded-convergence-option-b-proof.md:130`, and every command at `:133-137` names a repository-relative `docs/plans/workflow-calibration.proofs/...` path. Criterion 13 at `:158` instead requires the commands to pass twice “from clean temporary directories.” The retained prototype demonstrates the path property: its root invocation exited 0, while the identical invocation from a new `mktemp -d` directory exited 2 with `python3: can't open file .../docs/plans/workflow-calibration.explorations/q86-controller-proof.py`. The planned paths have the same relative form.
- **Reasoning:** A clean temporary working directory contains no repository-relative proof path. A temporary checkout could make the command work, but the criterion does not say that; the root-only contract and its no-repository-artifact clause point to a different intended test. An implementer cannot tell whether to add a prohibited/unstated path-resolution mechanism or merely prove repeatability.
- **Exact correction:** Define one execution environment. Keep the exact commands root-relative and require each to run twice from the repository root, with any temporary state created under a fresh temporary directory and removed, followed by an explicit no-new-artifact check. If a temporary checkout is intended instead, say so explicitly and provide commands whose repository root is that checkout. Do not leave a bare temporary working directory as an acceptance environment.

## T3 — The traceability checker is not required to derive its claimed 51-verdict input set

- **Source:** Claude F3.
- **Verdict:** valid, **low**.
- **Reproduced evidence:** The retained triage verdicts derive to 51 valid IDs, and the sidecar lists the same set at `bounded-convergence-option-b-proof.md:112-116`. But the required checker is only stated to report the fixed values `valid_findings=51` and `unresolved=0` at `:140`; its contract at `:21` and acceptance criterion 11 at `:156` never require parsing the five triages to derive that set. Thus a checker can compare a matrix against a hard-coded list/count while merely storing five path strings, and its prescribed output does not distinguish that from a checker that actually validates the retained verdicts.
- **Reasoning:** The traceability gate is the sole mechanical closure for 51 adversarial verdicts. Review of the matrix remains required, but it does not make a checker that claims to check the triages without reading them an adequate mechanical gate. This is a low assurance gap in a future proof specification, not evidence that any current matrix is wrong.
- **Exact correction:** Require `q86-option-b-traceability.py` to parse all five retained triage files, derive valid T-ids from their verdict records, and fail if that derived set differs from the matrix row set, the reported count, or the applicable/inapplicable resolution set. A hard-coded expected count or ID list must not substitute for the derived source set.

## T4 — Equal tag and mutation counts are not shown to forbid the required mutation coverage

- **Source:** Claude F4.
- **Verdict:** invalid.
- **Reproduced evidence:** The cited wording requires every load-bearing **transition and predicate** to be tagged (`bounded-convergence-option-b-proof.md:124`), and separately requires every mandatory mutation class, including reserve unlock and clean-streak preservation. The earlier retained findings concern two distinct semantic predicates on an upheld dismissal (`q86-synthesis-r2-triage.md:46-52` and `q86-synthesis-r4-triage.md:50-56`). No manifest or reference model exists yet, and nothing requires both predicates to share one tag.
- **Reasoning:** A manifest can tag the upheld-dismissal transition and its independent reserve and streak predicates separately, then provide one exercised, killed mutation for each tag while its tag and mutation counts remain equal. The reviewer's asserted collision assumes a single tag must cover both predicates; the sidecar says the opposite granularity is available. The equality may be a rigid design choice, but the supplied evidence does not establish an unsatisfiable requirement or a loss of either retained control.
- **Correction:** none.

## T5 — The proof omits a typed route for findings whose canonical owner is in a different phase

- **Source:** GPT Finding 1.
- **Verdict:** valid, **high**.
- **Reproduced evidence:** The selected synthesis requires stable finding identity through “later phases” and permits an atomic owner-to-finding map (`docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:60-61`). The proof sidecar instead defines `PhaseCampaign(q)` as owning exactly `O_q` (`bounded-convergence-option-b-proof.md:35`), mentions incidental cross-owner work only within “that phase” (`:47`), and requires cross-owner fixtures without a discovery-phase/owner-phase relation (`:51-66`, `:106`). Searching the sidecar for `cross-phase`, `prior phase`, `future phase`, `closed phase`, or a phase reopening route finds no such rule. A finding discovered in acceptance that canonically belongs to an already completed work phase, or in an early phase for a future owner, therefore has no typed route that preserves it while respecting non-transferable authority.
- **Reasoning:** Declaring those legal review observations out of model scope would silently weaken the selected safety package. This hole can leave a later serious finding outside the delivery proof, so its impact is high if left unfixed. It is new evidence about the selected-proof specification, not relitigation of a settled prototype verdict.
- **Exact correction:** Add distinct discovery-phase and canonical-owner-phase state, and define the route for current-, prior-, and future-phase owners. A completed owner must retain the finding without authority transfer or replenishment and reach a named legal disposition (continued existing authority where available, or a terminal non-delivery/replan path); a future owner must retain it until its campaign. Add atomic fixtures and killing mutations for acceptance-to-completed-work, early-work-to-future-owner, and mixed current/out-of-phase batches, and re-derive any affected bounds.

## T6 — Permitting several initial-owner advances in one batch contradicts the published phase minimum

- **Source:** GPT Finding 2.
- **Verdict:** valid, **medium**.
- **Reproduced evidence:** The proof sidecar says one atomic batch may advance several initial owners (`bounded-convergence-option-b-proof.md:47`) while giving the post-freeze phase minimum as `L_q = n_q + 1` (`:97`, also acceptance criterion 10 at `:155`). With two untested owners, one legal batch that advances both initial attempts plus the blind-closure batch takes two batches, not the claimed three. The selected synthesis repeats the same formula and calls it the clean minimum (`Q-86-synthesis.md:101-105,154-156`).
- **Reasoning:** The plan may not call an exact minimum a minimum while its own legal transition relation admits a lower cost. The contradiction affects the decision comparison and the algebraic proof gate; the maximum may still be safe, but is not established by this minimum claim.
- **Exact correction:** Choose one model and make the transition relation, formulas, and fixtures agree. Either allow a cross-owner batch to retain extra findings but give initial-attempt credit only to the scheduled owner, preserving `L_q = n_q + 1`; or permit multi-owner initial credit and replace `L_q` and `L_B` with the correctly derived minima. Exercise zero, one, and multiple-owner cases, including the atomic multi-owner case, in the algebra oracle.

## T7 — The retained safety proposal still frames the completed choice as pending advice

- **Source:** GPT Finding 4.
- **Verdict:** valid, **low**.
- **Reproduced evidence:** The proposal says “Provisional recommendation” and “advice for the human choice” at `docs/plans/workflow-calibration.explorations/Q-86-safety-process.md:476-478`, yet the same section records that the human selected synthesised Option B at `:493`; Q-86 is now decided in `agent-scaffold.plan.toml:2583-2586`.
- **Reasoning:** The proposal is retained as decision provenance, so it should preserve its historical recommendation without describing a receipted decision as currently awaiting a human choice. This is documentation currency only and does not reopen Q-86.
- **Exact correction:** Relabel that section as the historical/provisional recommendation that preceded Q-86, use past tense for the advice, and retain the low-confidence and blocking-proof boundaries.

## Outcome and backstop

**Outcome: `new_valid`.** Valid findings: **6** — **1 high, 3 medium, 2 low**. Invalid findings: **1**. Accepted residuals: **0**.

No high- or critical-severity finding was dismissed, so no independent dismissal backstop re-check is owed. The valid high finding returns to the planner for correction; this risky plan-review round cannot count as clean.
