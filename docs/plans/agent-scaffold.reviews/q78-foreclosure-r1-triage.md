# Q-78 post-escalation round 1 triage

## Scope and gates

I independently triaged the seven raw reports against the repaired design at `7120d94`. I read no reviewer fixture. All reconstructed inputs and countermodels are under `/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-foreclosure-r1-triage/triager-independent`, and every project command used the project `direnv` environment.

The repaired product diff contains only `docs/plans/agent-scaffold.steps/step-intent-encoding.md` and its rendered view. `git diff --check 7120d94^..7120d94` passed, and GNU grep found zero non-ASCII bytes in both files.

Baseline gates passed: source-plus-metrics validation reported 450 valid records and 105 valid steps / 81 questions; workflow validation held; strict render was up to date; `cargo test` passed 470 tests; and `cargo clippy --all-targets --all-features -- -D warnings` exited zero.

## Raw verdicts

| Raw finding | Verdict | Distinct finding | Owner | Final severity | Final class | Evidence | Smallest correction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-FR1-1 | valid | FR1-1 | `step-intent-encoding-inc1` | low | 2 | E1 | Extend the empty-body unit oracle with independently constructed problem-only and approach-only cases, each asserting its complete fragment and absence of the other label. |
| GPT-FR1-2 | valid | FR1-2 | `step-intent-encoding-inc1` | medium | 1 | E2 | At the `build_context` seam, table-test every production `LoopState` for both populated intent slots and their values; retain the existing per-surface matrices. |
| GPT-FR1-3 | valid | FR1-3 | `step-intent-encoding-inc3` | medium | 2 | E5 | Add a content oracle for the Unreleased entry requiring both required fields, paragraph support with no cap, and the earlier-plan parse break / per-step migration. |
| PE1C-1 | valid; duplicate | FR1-2 | `step-intent-encoding-inc1` | medium | 1 | E2 | Same as FR1-2. |
| PE1C-2 | valid | FR1-4 | `step-intent-encoding-inc1` | medium | 2 | E3 | Pin the actual deterministic `docs/plans/<task>.reviews/...` values from the fixture task and step, including the intentional reviewer `<disambiguator>` token. |
| PE1C-3 | dismissed | - | `step-intent-encoding-inc1` | - | - | E4 | None required. Optionally say "all eight" in the review-state human-matrix sentence for readability. |
| PE1C-4 | valid; duplicate | FR1-1 | `step-intent-encoding-inc1` | low | 2 | E1 | Same as FR1-1. |

The final classes follow the brief rather than the reporters' labels. FR1-1 is a second-guard hole: the violated statement is an unnumbered render sub-rule, not a risk ground, numbered RULE, or cited plan Principle. FR1-3 is likewise a second-guard hole: criterion 9 proves only that `CHANGELOG.md` changed, not that it contains the documentation-impact duty. FR1-2 is class 1 because it admits an implementation that violates the explicit all-loop-state instruction requirement on the risky instruction surface.

## Deduplication

| Distinct finding | Raw reports | Defect |
| --- | --- | --- |
| FR1-1 | GPT-FR1-1, PE1C-4 | The empty-body oracle exercises both fields but not either one-field branch. |
| FR1-2 | GPT-FR1-2, PE1C-1 | The all-loop-state requirement has no witness for five production states. |
| FR1-3 | GPT-FR1-3 | The changelog path / heading checks do not prove the migration notice. |
| FR1-4 | PE1C-2 | Criterion 7 pins findings paths that `build_context` cannot emit. |

PE1C-3 is not a defect. Its claimed six-versus-eight contradiction has a satisfying implementation, so it neither permits a wrong implementation nor rejects a correct one.

## Reproduced evidence

### E1 - FR1-1: one-field empty bodies evade the oracle

The render contract says that at least one field contributes an entry even with an empty body (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:100`). The repaired oracle constructs only the both-fields case (`:218-232`); the existing partial fixture has a body (`:244-250`). I independently evaluated the admitted predicate `body is non-empty OR (problem is present AND approach is present)` in scratch. It produced:

```text
empty-body: both-fields-oracle=pass body-bearing-partial=pass problem-only-empty=fail approach-only-empty=fail
```

Thus the predicate passes the named oracle and the bodied partial case while violating the at-least-one quantifier. The result is a low class-2 second guard, not class 1.

### E2 - FR1-2: the all-state requirement remains unrefused

Increment 1 requires `build_context` to insert both slots "in every loop state" (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:112`) on a surface whose risk ground calls `next` an instruction (`:61`). The production enum has ready, blocked, two reviewer states, fixes, converged, escalate, risk-class-conflict, and done (`src/next.rs:273-303`); its current context match likewise has distinct blocked and empty/control arms (`src/next.rs:1003-1018`). Criterion 7 exercises review and fixes states (`step-intent-encoding.md:260-318`), while increment 3's fresh-scaffold check adds only ready-to-plan (`:842-851`).

My independent countermodel inserted both values only for ready-to-plan, both reviewer states, and awaiting-fixes. Every named increment-1 row and the increment-3 fresh-scaffold row remained covered, but it printed:

```text
every-state: inc1-rows=pass inc3-ready-to-plan=pass omitted=blocked,converged,done,escalate,risk-class-conflict
```

The omission violates the stated all-state requirement on the instruction surface, so FR1-2 is medium class 1. It is owned by increment 1; increment 3 retains increment 1's contract but does not add coverage for the omitted states.

### E3 - FR1-4: fixed context literals cannot be emitted

Criterion 7 fixes the review and fix context paths to `reviews/...` (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:264-274`, `:294-315`). The implementation derives paths from `docs/plans/<task>.reviews` (`src/findings_naming.rs:28-71`). Using a triager-authored one-step fixture with task `t`, step `example-step`, `--ledger-fragment ledger.md`, and `--isolation-tier worktree`, the current binary emitted:

```text
{"state":"awaiting-first-review","context":{"isolation_tier":"worktree","ledger":"ledger.md","review_findings":"docs/plans/t.reviews/example-step-reviewer-<disambiguator>.md","triage_findings":"docs/plans/t.reviews/example-step-triage.md"}}
{"state":"awaiting-fixes","context":{"isolation_tier":"worktree","ledger":"ledger.md","triage_findings":"docs/plans/t.reviews/example-step-triage.md"}}
```

No CLI input can turn the literal `docs/plans/` prefix into `reviews/`, and the reviewer path intentionally retains `<disambiguator>`. A correct implementation therefore fails criterion 7's complete literal comparison. FR1-4 is a medium class-2 false refusal.

### E4 - PE1C-3: the claimed matrix contradiction does not reproduce

The review-state human text names six fixtures (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:264`); the fixes text requires every fixture (`:306`); and the following sentence requires the same named tests to own both state families (`:318`). I independently constructed the alleged mismatch and assigned all eight matrix rows to both state families. It satisfied the six named review rows, the eight fix rows, and the pairing rule:

```text
human-matrix: six-named-review-rows=pass eight-fix-rows=pass paired-eight-by-eight=pass
```

The six-item list is not an exclusive constraint. Since an eight-by-eight implementation satisfies every stated clause, PE1C-3's false-refusal claim is dismissed.

### E5 - FR1-3: a heading and changed path do not prove the notice

Criterion 9 only requires `CHANGELOG.md` in the changed-path set (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:921-925`). The documentation-impact duty requires the Unreleased entry to record both required fields, uncapped paragraph support, and the migration parse break (`:941-945`). I confirmed the current tree has no Unreleased heading, then constructed a scratch changelog containing only `## [Unreleased]` and an unrelated housekeeping entry. The path / heading predicates passed while every required migration-content predicate failed:

```text
documentation: changed-path-set=pass heading=pass required-migration-content=fail
```

This is a medium class-2 second-guard hole. The accepted F3 residual concerns heading collision or clobbering; it does not waive the required entry content.

## Per-loop outcome

Both loops were reset to round zero before this post-escalation round and remain risky, so each needs two consecutive clean rounds.

| Loop | Distinct valid findings | Severities | Class 1 / class 2 / neither | Outcome | Resulting streak | Converged |
| --- | ---: | --- | --- | --- | ---: | --- |
| `step-intent-encoding-inc1` | 3 | medium, medium, low | 1 / 2 / 0 | new valid | 0 | no |
| `step-intent-encoding-inc3` | 1 | medium | 0 / 1 / 0 | clean | 1 | no |

Increment 1 is not clean because FR1-2 is class 1. Increment 3 is clean under the foreclosure rule: its only finding is a medium class 2. It still needs one further consecutive clean round. Four rounds remain under the reset cap for each loop.

## Totals and backstop

- Raw findings: 7.
- Raw verdicts: 6 valid, 1 dismissed.
- Distinct valid findings: 4.
- Distinct class totals: 1 class 1, 3 class 2, 0 outside both classes.
- Severity ceiling: medium.
- Residual acceptance and waiver: none.
- Backstop: not owed. The only dismissal is PE1C-3 at proposed low severity; no high or critical finding was dismissed.
