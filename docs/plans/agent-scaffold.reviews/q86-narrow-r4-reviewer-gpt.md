# Narrowed Q-86 round 4 review — scope, provenance, rendering, bounds, gate, and authority

I independently reviewed `main..392712ac` with `main` at `b6fb2ff6`. I read `AGENTS.md`, `.agents/prompts/reviewer.md`, the Q-86 and Q-88 structured records and sidecars, all three prior narrowed triages, all five synthesis triages, the narrowed synthesis, retained proposals and prototype boundaries, the owning step, Success Criteria, generated plan, ledger Q-86/Q-88 record, and Q-88 receipt. I treated the scripts as deferred adversarial prototypes and did not require proof for any unselected architecture.

## Round-3 fix verification

All four round-3 fixes are closed.

1. **GFM tables:** rendering the synthesis cost table and safety-process Principle table with `cmark-gfm --extension table` now preserves every four-column row and both `|O|` formulas. A fresh parser sweep over every changed Markdown file found no table whose body-row width differs from its header.
2. **B phase scope:** `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:156-161` now separates low- and risky-plan review from post-freeze work and acceptance. B's plan rows explicitly reuse A's sealed plan controller; `n_q + 1` is confined to post-freeze rows.
3. **B replay consequence:** `docs/plans/agent-scaffold.questions/Q-86.md:8` now carries the qualified four-fold counterfactual and states that a non-changing assumed fold removes its associated replan and cost. The generated copy is verbatim.
4. **Prototype provenance:** `sha256sum docs/plans/workflow-calibration.explorations/q86-controller-proof.py` returns `8a349c68dbe18df43d1d60d4110e11b3e216d97cdf4efb9f7e7328693d668175`; `git show ad989b5f:docs/plans/workflow-calibration.explorations/q86-controller-proof.py | sha256sum` returns the separately labelled historical `d0dabe6da04fde2009a2baf22d0a3d9fabdfbd6bc96d2859d26043531aff579a`. The safety and state-machine records distinguish the two.

## Fresh sweep

- `nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml` passed. The generated plan has one non-fenced H1, and each Q-86/Q-88 sidecar occurs verbatim once. `validate --source docs/plans/agent-scaffold.plan.toml --workflow` passed with 488 valid records, 114 steps, and 88 questions.
- The proposal-label map is present, the Q-88 receipt is unique and exactly matches all six presented labels in order, and the current and historical prototype digests reproduce.
- I independently re-derived A's `7(m + 2)` / `34(m + 2)`, B's post-freeze and family formulas including `18|O| + 4m + 38`, and C's `4(m + 2)` / `15(m + 2)` from the stated finite topologies and call allocations. I found no arithmetic defect; these remain proposed algebraic consequences, not proof claims.
- The selected-option gate remains blocking and architecture-specific, requires risky convergence, traceability, assertions and mutation controls, returns failure to the human, and selects no fallback. No production, pack, prompt, workflow-spec, Rust, or test path changes; no Roadmap step is added or completed; Q-86 remains human-owned and `open`.

## Finding

### Finding 1 — the recommended serious floor is not judged against any Project Principle

- **Severity:** low.
- **Evidence:** `AGENTS.md:41` requires every human-input recommendation to carry reasoning judged against the plan's Project Principles by name, and `AGENTS.md:65` requires an exploration document to apply that contract to its options. The synthesis's architecture comparison and recommendation do this at `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:165-184`, but its separate floor decision at `:209-217` recommends `high` using only the operational restriction and Q-78 pass range. Its `critical` and `defer` alternatives likewise have no Principle-judged trade-off. The human-facing Q-86 detail repeats the same ungrounded recommendation at `docs/plans/agent-scaffold.questions/Q-86.md:31-37`. Reproduce the omission with:

  ```sh
  sed -n '209,217p' docs/plans/workflow-calibration.explorations/Q-86-synthesis.md |
    rg 'Prefer the cleaner|Minimal by default|Safe on existing|Idempotent|Make illegal states|Ground decisions|Reproducible|Structured data'
  # exit 1
  ```

- **Consequence:** The floor is a real human-owned policy decision: it determines whether an open high can be accepted as residual risk or ordinarily narrowed. The decision material provides the operational difference and useful evidence, but the `high` recommendation does not satisfy the project's mandatory presentation contract. This is low because the floor remains unselected, the human retains authority, and the proof/implementation gates remain intact.
- **Correction:** Add a concise Principle-named comparison and rationale for the floor recommendation to the synthesis and Q-86 human-facing plan sources, then re-render. This needs no controller proof and must not alter the deferred selected-option gate.

## Counts

Critical: 0. High: 0. Medium: 0. Low: 1. **Total: 1.**
