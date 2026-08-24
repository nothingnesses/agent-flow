# Q-78 post-escalation round 4 GPT review

## Scope and gates

I reviewed only `step-intent-encoding-inc1` at the current `plan/q78-design-pass` tip, excluding the round-4 briefs from the product under review. I independently verified R3-1 and R3-2, treated R3-3 and R3-4 as settled permitted class-2 findings, and did not read the Claude round-4 report.

All scratch evidence and the Cargo target are under the authorised child `/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-foreclosure-r4-gpt/reviewer`. Every project command ran through the loaded `direnv` flake environment.

Baseline gates pass:

- `validate --source ... --metrics ...`: 455 records, 105 steps and 81 questions valid.
- The same validation with `--workflow`: workflow invariants hold.
- Strict render checks for `agent-scaffold.plan.toml` and `TEMPLATE.plan.toml`: up to date.
- `cargo test`: 470 passed, zero failed.
- `cargo clippy --all-targets --all-features -- -D warnings`: passed.
- `git diff --check`: passed; both changed product files are ASCII-clean.

## Findings

### GPT-R4-1 - the pending oracles permit paragraph loss during the transfer - medium, class 1

Numbered RULE 10 requires JSON to keep the deserialised string unchanged, including paragraph boundaries (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:53`), and the `next` contract repeats that its context values are unchanged and that human output supports one or several paragraphs (`:112`). The R3-1 repair does close a complete omission, but both new pending-constructor tests use only single-paragraph sentinel values (`:320-366`). The full parser-value matrices still enter through the in-progress constructors (`:260-318`), while the all-state seam still injects its one-line values below the pending transfer (`:370`).

A wrong `build_pending_loop` can therefore copy only the first paragraph of each field. The new `ReadyToPlan` and `Blocked` complete-object assertions remain green because `"ready problem"`, `"ready approach"`, `"blocked problem"` and `"blocked approach"` contain no second paragraph. The prescribed drop-only mutation remains non-vacuous: replacing that wrong transfer with `None` makes both pending tests red while the in-progress matrices and direct seam stay green. Yet an actual pending value `"paragraph one\n\nparagraph two"` reaches both human and JSON context as only `"paragraph one"`.

Reproduction:

```text
rustc .../reviewer/pending_transfer_countermodel.rs -o .../reviewer/pending_transfer_countermodel
.../reviewer/pending_transfer_countermodel
in-progress parser-value matrix: pass
direct all-state build_context seam: 9/9 pass
ReadyToPlan one-paragraph oracle: pass
Blocked one-paragraph oracle: pass
drop-only pending mutation: both pending oracles red; matrices and seam green
wrong pending multiline value: "paragraph one"
required parser value: "paragraph one\n\nparagraph two"
```

The complete source and output are `.../reviewer/pending_transfer_countermodel.rs` and `.../reviewer/pending_transfer_countermodel.out` under the authorised scratch child above. This is class 1 because the wrong implementation satisfies the repaired acceptance and red-control obligations while violating numbered RULE 10 and the step's decided one-or-more-paragraph contract. It is medium because a planner or blocker-resolution instruction can silently lose part of both the problem and the approach on both output surfaces.

Run the independent parser-value matrix through both pending constructors, or at minimum give each pending oracle byte-distinct multi-paragraph/non-normalised values and require a pending-only truncation or normalisation mutation to make the affected oracle red. Keep the existing drop-only mutation as a separate control.

## R3-2 verification

R3-2 is closed. I reproduced Clap 4.6's materialisation behavior with the specified `CommandFactory` sequence: the current vector is exactly `scaffold, validate, status, next, checks, render, audit, help`; adding an `IntentQuery` variant exposes `intent-query`, changes the collected vector, and makes the exact-vector assertion exit 101; restoring it returns green. Evidence is in `.../reviewer/clap-probe/`, `clap-hyphenated-red.out`, and `clap-restored-green.out` under the authorised scratch child.

## Outcome

One distinct finding: one medium, class 1. Under the controlling foreclosure condition this round is not clean, so the two-clean-round requirement can no longer be reached within the remaining reset-round budget. No waiver is authorised or used.
