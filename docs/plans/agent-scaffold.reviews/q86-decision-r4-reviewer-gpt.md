# Q-86 decision-fold plan round 4 review — GPT

## Scope and verification

I independently reviewed `main...6dce497b` after reading `AGENTS.md`, `.agents/prompts/reviewer.md`, the proof step, Q-86/Q-88–Q-91, the synthesis, state-machine and safety proposals, all five retained synthesis triages, all three prior decision-fold triages, the ledger retention record, the TOML source, and the generated projection.

The round-3 repairs are present: the lower-bound domain no longer assumes scheduled-owner credit and keeps the two-owner mutant in-domain; the ledger records retention of the five synthesis triages; the selected sources qualify `L_q` and `L_B` as ordinary-delivery minima; and blind closure now has explicit owner/dismissal routes. The closure repair is still incomplete in the fresh scope-product case below.

These gates passed:

```text
nix develop --command cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml
# docs/plans/agent-scaffold.plan.toml: up to date
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl
# 499 records, 115 steps, 91 questions, valid
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow
# workflow invariants hold
git diff --check main...HEAD
# exit 0
```

The Q-86 and Q-91 receipts exactly match their structured decisions. The generated projection is current, and the retained ledger record identifies the five live synthesis triages and their 51 valid verdict identities.

## Findings

### F1 — Blind closure's “exhaustive” route product omits the selected scope-recheck axis

- **Severity:** medium.
- **Evidence:** The selected safety policy distinguishes four scope outcomes: optional low is backlogged, medium goes to a terminal human scope decision, high waits for an independent scope re-check and then goes terminal or returns in scope, and either critical scope result remains safety-blocking (`docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:65`). `BlindClosureDiscovery(q)` accepts an atomic triaged finding map (`docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md:74`) and calls its table the “one exhaustive route product” (`:76`), but the table at `:78-85` covers only canonical-owner position and valid/upheld/overturned dismissal outcomes. It has no state for `AwaitingScopeRecheck`, backlogged scope-low, terminal scope-medium, overturned scope-high returning through an owner route, or either critical scope result. The closure-specific fixtures at `:99` and closure Acceptance criterion at `:191` repeat only owner and dismissal outcomes; generic scope fixtures at `:102` can therefore be satisfied in a non-closure campaign without testing their conjunction with closure.
- **Impact:** A proof can satisfy the stated closure acceptance while never establishing whether a scope referral discovered by the sole blind-closure batch keeps closure pending. In the serious case, that leaves room for the exact failure the selected policy forbids: treating a proposed scope-expanded critical as settled closure evidence rather than retaining its per-id re-check and safety block.
- **Required correction:** Extend the closure route product, fixtures, acceptance, and killing mutations across the scope axis. At minimum cover low/medium/high/critical scope outcomes, upheld and overturned high/critical scope re-checks, owner routing after overturn, and an atomic closure batch containing both scope- and dismissal-recheck components. Closure must remain pending while either re-check is pending, and either critical scope result must remain non-delivering.

### F2 — `blocked_by` is not a durable proof-completion gate under the already-planned scheduler semantics

- **Severity:** high.
- **Evidence:** The proof step says completion is the gate and requires every later bounded-convergence production unit to declare only `blocked_by = ["bounded-convergence-option-b-proof"]` (`docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md:21`); on proof failure the step remains incomplete and every production implementation remains blocked (`:206`). The accepted scheduler Success Criterion, however, defines its frontier using `complete/skipped` blockers (`docs/plans/agent-scaffold.success-criteria.md:40`). That scheduler is Roadmap order 116 and the proof is order 117 (`docs/plans/agent-scaffold.plan.toml:1767-1788`). Thus an implementation of the scheduler exactly as planned will treat a `skipped` proof step as satisfying the only dependency the later production unit is required to carry. The current fallback implementation is stricter—it checks only `Complete` at `src/next.rs:736-756`—which demonstrates the semantic drift rather than repairing the future gate.
- **Impact:** The plan claims a failed or abandoned proof has no path to production, but its required dependency representation admits that path once the proof row is `skipped`. This bypasses the blocking safety proof for a widely depended-on workflow mechanism.
- **Required correction:** Give this dependency an enforced complete-only meaning: for example a typed `requires_complete` gate, a non-skippable proof-gate status validated against every bounded-convergence production unit, or a global blocker rule that does not count `skipped` as completion. Add a red control showing that `skipped` and every other non-`complete` proof status keep a production unit blocked.

### F3 — The exact proof commands do not use the repository's pinned Python toolchain

- **Severity:** low.
- **Evidence:** All five exact commands resolve `nixpkgs#python3` through the caller's Nix registry (`docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md:173-177`). Reproduction on this worktree:

  ```text
  nix registry list | grep 'flake:nixpkgs'
  # ... global flake:nixpkgs github:NixOS/nixpkgs/nixpkgs-unstable

  jq -r '.nodes.root.inputs.nixpkgs as $k | .nodes[$k].locked.rev' flake.lock
  # d407951447dcd00442e97087bf374aad70c04cea
  ```

  The command's mutable registry target is not the repository pin. Two same-machine passes can agree while another machine or a later run resolves a different Python, and the plan states no supported Python version.
- **Impact:** This weakens the durable exact-command and cross-environment reproducibility claim, although it does not by itself show a property-oracle error.
- **Required correction:** Run Python from the repository-locked development shell, or resolve `python3` with `--inputs-from .`/an equivalent lock-bound command. State any minimum Python version the scripts require.

## Counts

- Critical: 0
- High: 1
- Medium: 1
- Low: 1
- Total: 3
