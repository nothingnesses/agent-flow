# Q-78 second foreclosure GPT verification

## Scope

I reviewed only `step-intent-encoding` increment 1 at the current branch tip and independently verified the correction for `GPT-R4-1`. I did not read the Claude verification report and did not re-open `C4-1` or any earlier settled class-2 finding.

## Ground-blind falsification

I built an independent pending-transfer countermodel under the authorised `scratchpad/q78-second-foreclosure-gpt` child. It models the eight logical parser values without using a reviewer fixture or a product projection as its oracle, applies each defect only at the pending transfer, and compares unchanged JSON values plus independently formatted human values across both fields and both pending states.

The old one-line pending oracle admitted paragraph truncation, per-line whitespace trimming and line-ending normalisation with zero mismatches. The repaired matrix produced these results:

```text
baseline_mismatches=0
old_single_truncation_mismatches=0 new_matrix_truncation_mismatches=16
old_single_whitespace_mismatches=0 new_matrix_whitespace_mismatches=12
old_single_line_ending_mismatches=0 new_matrix_line_ending_mismatches=8
new_matrix_absence_mismatches=64
in_progress_and_direct_seam_mismatches=0 (pending-only mutants do not enter those paths)
```

The plan now requires the independent eight-row parser-value matrix to enter both pending paths through TOML, with distinct values for both fields (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:320-322`, `:347-349`). `ReadyToPlan` fixes the complete four-key JSON object and exact human range for every row (`:322-347`); `Blocked` independently fixes the complete five-key object and exact human range (`:349-374`). Both use parser-oracle bytes rather than `StepInfo`, `LoopFacts`, or product formatting as expected values (`:320`, `:335`, `:361`). This closes the original counterexample against RULE 10's unchanged JSON and paragraph-preserving human contract (`:53`).

The three pending-only controls are separate rather than composite: absence is retained, paragraph truncation must redden both fields on both surfaces in both states, and per-line whitespace normalisation must do the same while the in-progress matrices and direct all-state seam stay green (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:376-382`). The complete matrix additionally exposes pending-only CRLF or bare-CR normalisation through exact JSON comparisons (`:333`, `:361`). I could not construct a pending-transfer implementation that loses or normalises a covered parser value while satisfying these obligations.

## Verification

Using the direnv-loaded project shell:

- `render --check --strict` reported the plan up to date.
- Both source validation and workflow validation passed: 105 steps, 81 questions, 457 metric records, invariants hold.
- `cargo test` passed all 470 tests.
- `cargo clippy --all-targets -- -D warnings` passed.
- `git diff --check 469a5bb^..469a5bb` passed; the fix commit changes only `docs/plans/agent-scaffold.steps/step-intent-encoding.md` and generated `docs/plans/agent-scaffold.md`, and both files are ASCII-clean.

## Findings

Zero findings. `GPT-R4-1` is closed by the pending-transfer matrix and its isolated red controls.
