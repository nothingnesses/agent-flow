# Q-78 post-escalation round 2 GPT review

## Verdict

FR1-2's state axis is repaired: the new seam test specifies all nine current `LoopState` variants, exact values for both intent keys, a compile-forced future-variant update, the complete five-state negative control, and increment-3 retention. I found no class 1 defect.

I found one low class 2 second-guard hole in increment 1: every `next` oracle supplies both optional fields together, so paired-only insertion passes while a present field disappears when the other field is absent. This is distinct from settled FR1-1, which concerns render's empty-body branch.

Under the foreclosure rule, both loops are clean. Increment 1 advances from streak 0 to 1. Increment 3 advances from streak 1 to 2 and converges.

## Finding GPT-R2-1: the `next` guards do not make independent optional-field presence load-bearing

- **Owner:** `step-intent-encoding-inc1`
- **Severity:** low
- **Class:** 2, second-guard hole
- **Evidence:** The contract requires `build_context` to insert each slot "when the field is present" (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:112`). The projection matrix exercises every logical value as both fields (`:164`, `:260`, `:294`), and the new all-state seam row likewise always supplies `Some` for both fields (`:320`). The state-restriction mutation also supplies both (`:324`). A paired-only implementation therefore satisfies the exhaustive nine-state exact-value table and produces the required ten failures under the sampled-state mutation, while violating the per-field clause for a valid increment-1 partial step.

  Reproduce with the reviewer-owned countermodel:

  ```text
  rustc /tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-foreclosure-r2-gpt/reviewer-gpt/fr1-2-proof.rs -o /tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-foreclosure-r2-gpt/reviewer-gpt/fr1-2-proof
  /tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-foreclosure-r2-gpt/reviewer-gpt/fr1-2-proof
  ```

  Output:

  ```text
  all-state-both-fields failures=[]
  sampled-red-control failures=["Blocked:problem", "Blocked:approach", "Converged:problem", "Converged:approach", "Escalate:problem", "Escalate:approach", "RiskClassConflict:problem", "RiskClassConflict:approach", "Done:problem", "Done:approach"]
  partial-present-field result=problem:None approach:None
  ```

  This is class 2 rather than class 1: it leaves an unnumbered per-field projection clause without a second guard, and the exposure ends when increment 3 makes both fields required.
- **Correction:** In `build_context_carries_intent_in_every_loop_state`, retain the both-fields exact-value row for every state and add problem-only and approach-only cases for every state, asserting the present key's exact value and the other key's absence. Retain those assertions in increment 3 at the `LoopFacts`/formatter seam, as the existing partial-status retention clause already does for its now-unparseable TOML fixtures.

## FR1-2 falsification results

- The sidecar's nine named variants at `step-intent-encoding.md:320` exactly match the current enum at `src/next.rs:273-303`.
- The prescribed single-list macro construction is feasible. Adding a tenth `Future` variant without updating the macro list failed compilation with `E0004: non-exhaustive patterns: LoopState::Future not covered`; the proof is `future-growth-proof.rs` beside the countermodel above.
- The sampled-state mutation reports both missing keys on exactly `Blocked`, `Converged`, `Escalate`, `RiskClassConflict`, and `Done`, while the restored all-state exact-value table has no failure.
- The named test is present in the authoritative increment-1 list (`step-intent-encoding.md:402`) and in increment 3's no-weakening retention clause (`:824`).
- The 12-file / 69-declaration-site figure still reproduces, so no changed evidence reopens the settled increment-3 declaration-site boundary.

## Validation

All commands ran through the project direnv environment with `CARGO_TARGET_DIR` under the authorised reviewer scratch child.

- Source and metrics validation: 452 records, 105 steps, 81 questions, valid.
- Workflow validation: invariants hold.
- `render --check --strict`: up to date.
- `cargo test`: 470 tests passed across all binaries; zero failed.
- `cargo clippy --all-targets --all-features -- -D warnings`: passed.
- `git diff --check c54a0b9^..c54a0b9`: passed.
- Both changed product files contain zero bytes outside tab and printable ASCII.
- Product paths in `c54a0b9`: only the intent sidecar and its rendered plan projection. Round-2 briefs were excluded.

## Per-loop count table

| Loop | Entering streak | Raw findings | Distinct findings | Severity | Class 1 | Class 2 | Neither | Outcome | Resulting streak | Converged |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- | ---: | --- |
| `step-intent-encoding-inc1` | 0 | 1 | 1 | low | 0 | 1 | 0 | clean | 1 | no |
| `step-intent-encoding-inc3` | 1 | 0 | 0 | none | 0 | 0 | 0 | clean | 2 | yes |

No waiver is authorised or used. No high or critical finding was raised, so no dismissal backstop is implicated.
