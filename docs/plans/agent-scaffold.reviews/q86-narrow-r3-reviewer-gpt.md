# Narrowed Q-86 round 3 review — decision scope and provenance

Reviewed risky artefact `main...152e316e` with `main` at `8fb6454a`. I read `AGENTS.md`, the reviewer prompt, the Q-86 and Q-88 structured records and sidecars, the narrowed synthesis, the owning step and Success Criteria, both retained proposals and prototype headers, both prior narrowed triages, and all five synthesis triages. I treated the executable scripts as deferred adversarial prototypes, not as controller proofs.

## Finding

### Finding 1 — the retained controller's published SHA-256 no longer identifies the retained file

- **Severity:** low.
- **Evidence:** `sha256sum docs/plans/workflow-calibration.explorations/q86-controller-proof.py` at tip returns `8a349c68dbe18df43d1d60d4110e11b3e216d97cdf4efb9f7e7328693d668175`, while `docs/plans/workflow-calibration.explorations/Q-86-safety-process.md:403` says in the present tense that its SHA-256 is `d0dabe6da04fde2009a2baf22d0a3d9fabdfbd6bc96d2859d26043531aff579a`. The exact-command block still includes `sha256sum "$CHECKER"` at `Q-86-safety-process.md:552`, followed by the old hash at `:555`; `Q-86-state-machine.md:453,467` repeats the command and old hash. The provenance is reproducible from history: `git show ad989b5f:docs/plans/workflow-calibration.explorations/q86-controller-proof.py | sha256sum` returns the documented `d0dabe...`, while `git show d20a4af9:docs/plans/workflow-calibration.explorations/q86-controller-proof.py | sha256sum` returns the current `8a349c...` after the required in-file prototype caveat was added.
- **Consequence:** A reader running the retained exact reproduction command cannot match the published digest to the retained evidence file, and the present-tense claim at `Q-86-safety-process.md:403` is false. This is low severity because the narrowed synthesis correctly quarantines the script from recommendation eligibility and no architecture, bound, or implementation authority relies on the digest.
- **Correction:** Identify `8a349c...` as the current retained-file digest. If `d0dabe...` is worth preserving as the historical executable-body digest, bind it explicitly to commit `ad989b5f` rather than presenting it as the current file's hash. This correction must not expand the deferred selected-option proof.

## Round-2 fix verification

All three round-2 fixes are closed:

1. `docs/plans/agent-scaffold.questions/Q-86.md:7` now gives A's pass-seven result and its three later low shortfalls, symmetric with C's quantified tail. The authoritative Q-78 selector still returns ten passes and `[7,10,5,6,5,5,4,2,1,0]`; passes eight and nine contain exactly three low findings and pass ten is empty.
2. `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:79` now states A's one broad blind seat plus one rubric-focused or informed seat and explains that the blind seat supplies closure evidence, deriving the one-batch/two-call acceptance minimum without changing the bound.
3. `docs/plans/agent-scaffold.questions/Q-88.md:1` now names Q-88 before `## Decision`. The generated Question Details block has a local identity boundary, and the outside-fence H1 scan of `docs/plans/agent-scaffold.md` returns only the plan title at line 3.

## Fresh decision-scope sweep

- **Provenance:** The synthesis maps A to state-machine Candidate A and safety M1, B to safety M2 plus the sealed authority envelope, C to state-machine Candidate B, and keeps M3 excluded. The one digest defect above is the only reproducible provenance problem found.
- **Bounds:** A's `7(m + 2)` and `34(m + 2)`, B's post-freeze `n_q + 1` / `4n_q + 1`, family `r_plan + |O| + m + 1` / `4|O| + m + 8`, and `18|O| + 4m + 38`, and C's `4(m + 2)` / `15(m + 2)` are consistently presented as proposed algebraic consequences whose premises remain for the selected-option proof. I found no false arithmetic or universal ranking claim.
- **Gate:** The synthesis, Q-86 sidecar, owning step, and Success Criterion all require a separate risky reviewed proof-of-concept Roadmap unit for only the selected architecture, make its completion an explicit blocker for every production implementation unit, require all applicable round-1-through-round-5 verdicts to be traced, and return failure to the human with no automatic architecture or floor fallback.
- **Status and receipt:** Q-86 is `open`; Q-88 is `decided`, folded into `workflow-calibration`, with receipt `Q-88`; `workflow-calibration` remains `in-progress`. Exactly one Q-88 decision record exists. Its six labels match the sidecar in order, recommendation and chosen are exactly `Narrow the proof scope`, and its task matches the folded-into slug.
- **Projection and documentation:** `render --check --strict` reports the plan up to date. `validate --source ... --workflow` reports 487 valid metrics records, 114 valid steps, 88 valid questions, and workflow invariants holding. Q-88's heading hierarchy is valid, the generated projection is current, and the shipped-documentation impact is explicitly deferred until a selected proof passes.
- **No implementation authority:** The diff contains planning, exploration, prototype, metrics-receipt, and generated-plan files only; no `src/`, `tests/`, `pack/`, `.agents/`, README, changelog, workflow-spec, or production-code path changed. Every current surface says the architecture/floor choice authorises proof only, not production implementation.

## Counts

Critical: 0. High: 0. Medium: 0. Low: 1. **Total: 1.**
