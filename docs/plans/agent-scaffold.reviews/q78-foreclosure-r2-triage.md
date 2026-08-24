# Q-78 post-escalation round 2 triage

## Scope and gates

I independently triaged the four raw reports against `c54a0b9`. I read no reviewer fixture. My countermodel, copied template family, build target and command output are all under the authorised child directory `/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-foreclosure-r2-triage/triager`. Every project command ran through `direnv exec .` with the project's Nix development environment; `CARGO_TARGET_DIR` was inside that child.

The baseline gates are green:

- `validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl`: 452 records, 105 steps and 81 questions valid.
- The same validation with `--workflow`: workflow invariants hold.
- Strict render checks for `agent-scaffold.plan.toml` and `TEMPLATE.plan.toml`: up to date.
- `cargo test`: 470 passed, zero failed.
- `cargo clippy --all-targets --all-features -- -D warnings`: passed.
- `git diff --check c54a0b9^ c54a0b9`: passed. GNU grep found zero non-ASCII bytes in the changed sidecar and its projection.

## Raw verdicts

| Raw finding | Verdict | Distinct finding | Owner | Severity | Class | Evidence and correction |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-R2-1 | valid; duplicate | R2-1 | `step-intent-encoding-inc1` | low | 2 | E1. Add problem-only and approach-only `LoopFacts` rows across every loop state, asserting the present exact value and absence of the other key. |
| R2C-1 | valid | R2-1 | `step-intent-encoding-inc1` | low | 2 | E1. Same correction as GPT-R2-1. |
| R2C-2 | valid | R2-2 | `step-intent-encoding-inc1` | low | 2 | E2. Retain only actually sampled projection states in the red-control allow-list, or state another true reason for the wider list; the former makes the control fail on both keys for the other seven states. |
| R2C-3 | valid | R2-3 | `step-intent-encoding-inc3` | low | 2 | E3. Say that `docs/plans/TEMPLATE.md` changes three times and name the documentation-protocol front-sidecar edit as the third cause. |

`FR1-2` is not re-opened. The new all-state seam at `step-intent-encoding.md:320` covers all nine declared `LoopState` variants, and its state-restriction control at `:324` catches the five states that were missing from the earlier state-axis coverage. The R2-1 defect is narrower and different: its inputs always carry both optional fields, so it does not test the per-field presence contract at `:112`.

## Deduplication

| Distinct finding | Raw reports | Defect |
| --- | --- | --- |
| R2-1 | GPT-R2-1, R2C-1 | `next` has no test input where exactly one optional intent field is present. |
| R2-2 | R2C-2 | The red-control rationale falsely calls `AwaitingReviewers` an already projection-sampled state. |
| R2-3 | R2C-3 | The required-flip prose undercounts independent causes that re-render `docs/plans/TEMPLATE.md`. |

## Reproduced evidence

### E1 — R2-1: both-field inputs do not prove conditional insertion

The contract says `build_context` inserts each key when its field is present (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:112`). The ordinary `next` matrices use each logical case as both `problem` and `approach` (`:164`, `:260`, `:294`), and the new exhaustive seam supplies `Some` for both fields (`:320`). Increment 3's fresh-scaffold surface likewise has both required placeholders (`:729`, `:851-852`). No `next` oracle supplies exactly one field.

I compiled a triager-authored nine-state countermodel, not a reviewer fixture. Both a pair-only implementation and one that inserts an empty string for a missing field pass the all-state both-present table and produce the ten state-restriction mismatches required by the red control. They fail the omitted partial contract in different ways:

```text
pair-only: paired-all-states=pass ... problem-only=[problem=<absent> approach=<absent>] approach-only=[problem=<absent> approach=<absent>]
empty-for-absent: paired-all-states=pass ... problem-only=[problem=problem approach=] approach-only=[problem= approach=approach]
```

The first loses the present key; the second fabricates the absent key. Each passes every specified `next` input because every such input has both fields. The `status --step` partial fixtures do not cure this: they exercise `status`, not `next` (`:354-378`). This is a low class-2 second-guard hole, not class 1: it violates the unnumbered per-field sentence, not a risk ground, numbered RULE or cited Principle.

### E2 — R2-2: the red-control coverage claim does not reproduce

The control says its retained set consists of states “the projection checks already sample” (`step-intent-encoding.md:324`). GNU grep over the complete sidecar found both `ReadyToPlan`/`ready-to-plan` and `AwaitingReviewers`/`awaiting-reviewers` only on lines 320 and 324—the newly authored seam and its control. The actual `next` projection matrices name `AwaitingFirstReview` and `awaiting-fixes` at `:260` and `:294`; independently, the current template command reports `state: ready-to-plan`, which is the fresh-scaffold state increment 3 later exercises. Nothing projects an intent-bearing `AwaitingReviewers` case before the new seam itself does.

The restored seam still catches an implementation omitting either key in that state, so this does not reopen FR1-2 or create a class-1 hole. It makes the control's stated premise false and leaves its retained `AwaitingReviewers` row without the claimed independent projection guard. That is a low class-2 in-increment non-reproducing figure.

### E3 — R2-3: the template projection has a third independent input

Increment 3 requires the new documentation-protocol duty in the committed `docs/plans/TEMPLATE.documentation-protocol.md` (`step-intent-encoding.md:737`). That file is a `front` sidecar (`docs/plans/TEMPLATE.plan.toml:20-28`). Yet the same increment says the committed template projection changes “twice over” (`step-intent-encoding.md:741`), naming only the required placeholder values and the changed example-step sentence.

I copied the complete `TEMPLATE` family into triager scratch, changed only the committed documentation-protocol sidecar by adding the exact proposed duty, and rendered the scratch plan. The generated `TEMPLATE.md` changed independently, inserting the duty between the protocol placeholder and the next front-sidecar heading. Thus the documentation-protocol edit is a third cause, separate from the two named ones. The path and strict-render criteria still require a correct implementation to regenerate the projection, so this is a low class-2 in-increment figure error rather than a false green.

## Per-loop outcome

Both active loops remain `risky` under the foreclosure decision; the clean bar is zero class 1, at most three low or medium class 2 findings, and none outside those classes.

| Loop | Entering streak | Raw / distinct findings | Severities | Class 1 / class 2 / neither | Outcome | Resulting streak | Converged |
| --- | ---: | ---: | --- | --- | --- | ---: | --- |
| `step-intent-encoding-inc1` | 0 | 3 / 2 | low, low | 0 / 2 / 0 | clean | 1 | no |
| `step-intent-encoding-inc3` | 1 | 1 / 1 | low | 0 / 1 / 0 | clean | 2 | yes |

The valid class-2 findings are within the specified clean allowance, so they do not reset either loop. Increment 1 needs one further clean round; increment 3 has converged.

## Totals and backstop

- Raw findings: 4.
- Raw verdicts: 4 valid, 0 dismissed.
- Distinct valid findings: 3.
- Distinct classes: 0 class 1, 3 class 2, 0 outside both classes.
- Severity ceiling: low.
- Waiver or residual acceptance: none authorised or used.
- Backstop: not owed. No high or critical report was dismissed.
