# Q-78 reset round 2 triage

## Method

I read both merged reviewer findings, the controlling round-1 and round-8 records, the current ledger resume state, and the reviewed product sources. I rebuilt every behavioural demonstration under `/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r2-triage`; no reviewer fixture directory was read. Project commands ran through the project direnv environment and GNU grep.

The independent reproduction helper showed that a helper which passes the presently named single-value, one-blank-line, and continuation cases fails repeated blanks and bare CR on `render`, human `next`, and human `status --step`, while normalising CRLF. It also showed a normalising `next --json` implementation passing the named JSON shape, and a status projection that passes all-present, all-absent, and unknown cases while turning either partial state into `Unknown`.

The reconstructed R4 fixture printed `source=2/2 projected=2/2 global_relation=pass` while `alpha_problem=0 beta_problem=2`. The reconstructed criterion-6 guard printed `OPENING ADDS WORDS demo` and `checked=1 bad_anchor=0 added=1` after an addition below the opening. GNU grep with R3's exact anchor matched a `Next.` at the start of a second paragraph, and R3b printed a second-paragraph `Next up` complement row. The one-line citations for C2-2 reproduce at `step-intent-encoding.md:112`, `:215`, and `:218`.

The complete test suite passed, Clippy passed with warnings denied, source-plus-metrics validation reported `426 records, valid` and `105 steps, 80 questions, valid`, workflow validation held, and strict render check reported `up to date`.

## Raw verdicts

| Raw finding | Verdict | Loop finding(s) | Severity | Class |
| --- | --- | --- | --- | --- |
| GPT-R2-1 | valid | T1 | medium | 1 |
| GPT-R2-2 | valid | T2 | medium | 1 |
| GPT-R2-3 | valid | T3 | medium | 1 |
| GPT-R2-4 | valid | T4 | medium | 1 |
| GPT-R2-5 | dismissed | — | medium as filed | — |
| GPT-R2-6 | valid | T6 | low | neither class |
| C2-1 | valid | T7a through T7f | medium each | 2 each |
| C2-2 | valid | T8 | low | 1 |
| C2-3 | valid | T9 | low | neither class |

No finding is accepted as residual risk.

`GPT-R2-5` is dismissed. The structured `Q-78` ask explicitly says the paragraphs from the pass outcome record what happened and supersede present-tense claims in the retained brief, while the retained body stays in its original tense (`docs/plans/agent-scaffold.plan.toml:2226`). The two cited single-line and sentence phrases are inside that marked historical recommendation, not a live implementation constraint. The current decision is stated in `Q-78.md:1-5`; its status remains open. This is not a high or critical dismissal.

## Deduplication and fan-out

| Loop finding | Raw source | Owning increment | Required correction |
| --- | --- | --- | --- |
| T1 | GPT-R2-1 | `step-intent-encoding-inc1` | Add exact-byte repeated-blank, CRLF, and bare-CR fixtures to all three human surfaces, plus a mutation that collapses a blank run or leaves bare CR. |
| T2 | GPT-R2-2 | `step-intent-encoding-inc1` | Compare `next --json` values byte-for-byte with parser values across the logical-value matrix, including outer whitespace, CRLF, and bare CR; add a normalising red mutation. |
| T3 | GPT-R2-3 | `step-intent-encoding-inc1` | Exercise both partial states in human and JSON `status --step`, requiring `found: true`, exact preservation of the present field, and `(not recorded)` or `null` only for the absent field. |
| T4 | GPT-R2-4 | `step-intent-encoding-inc1` | Reconcile each source field with exactly one correctly quoted labelled block inside its own generated Step Details section; retain aggregate counts only as a secondary census. |
| T6 | GPT-R2-6 | `step-intent-encoding-inc3` | Make the structured ask and exploration either point to the sidecar without a residual count or state all four, and require the eventual receipt to cover all four. |
| T7a | C2-1 | `step-intent-encoding-inc2a` | Test only the first logical line for R3 and both R3b arms, and print only that line in a status-token report. |
| T7b | C2-1 | `step-intent-encoding-inc2b` | Same shared correction as T7a. |
| T7c | C2-1 | `step-intent-encoding-inc2c` | Same shared correction as T7a. |
| T7d | C2-1 | `step-intent-encoding-inc2d` | Same shared correction as T7a. |
| T7e | C2-1 | `step-intent-encoding-inc2e` | Same shared correction as T7a. |
| T7f | C2-1 | `step-intent-encoding-inc2f` | Same shared correction as T7a. |
| T8 | C2-2 | `step-intent-encoding-inc1` | Remove the conditional `multiline` wording and add a single-paragraph human-`next` fixture that requires the label-own-line quoted form. |
| T9 | C2-3 | `sidecar-status-opening-drift-inc1` | Reconcile the accepted-residual text at `sidecar-status-opening-drift.md:213` with criterion 6's whole-file word-diff guard, retaining only exposure the repaired guard does not cover. |

T7 is one textual defect but six loop findings: the shared batch block independently governs each of the six declared batch increments. A single correction closes all six, but the fan-out must remain visible in loop accounting.

## Findings and evidence

### T1 — human projection matrix omits repeated blanks and bare CR

Rule 10 requires every internal blank line to survive and CRLF and CR to normalise to LF (`step-intent-encoding.md:53`). Criteria 5, 7, and 8 exercise only a single blank separator. The rebuilt helper passes all named shapes, normalises CRLF, and reports `repeated=false bare_cr=false` for every human surface. A wrong helper can therefore pass the criteria while violating Rule 10. Class 1, medium.

### T2 — `next --json` is not held to unchanged deserialised bytes

Criterion 7's only `next --json` fixture is the two-paragraph value at `step-intent-encoding.md:215-226`. The rebuilt normalising projection preserved that fixture but changed `"  paragraph one\rparagraph two  "` to `"paragraph one\nparagraph two"`. This violates Rule 10's unchanged JSON requirement. Class 1, medium.

### T3 — both partial status states are untested

Criterion 8 tests all-present, all-absent, and unknown, but neither one-field permutation (`step-intent-encoding.md:227-260`). The rebuilt projection passed the three named states and returned `Unknown` for both `problem`-only and `approach`-only known steps. This violates the declared field-wise `found`/string-or-null contract. Class 1, medium.

### T4 — R4 permits an offsetting omission and duplicate

R4 compares global source and labelled projection counts (`step-intent-encoding.md:523-555`). The rebuilt two-step projection passed the global relation while losing alpha's labels and duplicating beta's. It violates Rule 10's per-step labelled projection requirement. Class 1, medium.

### T6 — the eventual-receipt residual set has two incompatible counts

The plan and exploration each require three residuals in the eventual receipt (`agent-scaffold.plan.toml:2285`, `step-intent-encoding.explorations/Q-78.md:324`), while the owning sidecar declares four and defines residual 4 (`step-intent-encoding.md:801-809`). This is new evidence narrowing the recorded boundary of an accepted residual, not a re-raise of residual 4's accepted behaviour.

It is valid but neither permitted class: it is not a wrong implementation that violates a stated risk ground, numbered rule, or cited plan Principle, and it is neither a second-guard hole, an in-increment non-reproducing figure, nor a criterion refusing a correct implementation. Its unpermitted kind prevents a clean `step-intent-encoding-inc3` loop.

### T7a–T7f — R3 and R3b anchor at every line, not the logical value

GNU grep's `^` anchors each input line. The exact R3 expression matched a valid value whose second paragraph begins `Next.`, while the same prose with `Next.` on the first logical line is the only shape Rule 9 forbids. R3b likewise printed a second-paragraph `Next up` complement row. This rejects a correct paragraph value, so it is the class-2 criterion-refuses-a-correct-implementation kind, medium. The fan-out assigns one such finding to every batch increment.

### T8 — single-paragraph human `next` has two admissible shapes

Rule 10 makes quoted lines unconditional (`step-intent-encoding.md:53`), but the `next` prose limits the label-own-line form to a “multiline context slot” (`:112`). Criterion 7 only runs a two-paragraph pair (`:215-226`). Thus an inline single-paragraph context slot can pass every stated criterion while violating Rule 10. Class 1, low.

### T9 — the accepted residual overstates what no criterion reads

The repaired criterion 6 explicitly scans the whole changed file for authored words (`sidecar-status-opening-drift.md:218-241`). The independent throwaway repository added a sentence below the opening and the rebuilt guard reported it, contrary to the residual's claim at `:213` that no criterion reads such a rewrite. This is new evidence changing the accepted residual's measured boundary.

It is valid but neither class: it is an inaccurate accepted-risk boundary, not one of the three class-2 kinds and not a wrong implementation passing while violating the specified class-1 grounds. Its unpermitted kind prevents a clean `sidecar-status-opening-drift-inc1` loop.

## Per-increment outcome

All increments remain `risky`; this is their second round, so every loop has used two rounds and none exceeds the cap. `other` counts valid findings in neither permitted class.

| Increment | Valid | Severities | Class 1 / Class 2 / other | Outcome | Resulting streak |
| --- | ---: | --- | --- | --- | ---: |
| `sidecar-status-opening-drift-inc1` | 1 | low | 0 / 0 / 1 | new_valid | 0 |
| `ledger-order-citation-currency-inc1` | 0 | none | 0 / 0 / 0 | clean | 1 |
| `plan-order-array-position-inc1` | 0 | none | 0 / 0 / 0 | clean, converged | 2 |
| `plan-order-array-position-inc2` | 0 | none | 0 / 0 / 0 | clean | 1 |
| `step-intent-encoding-inc1` | 5 | medium, medium, medium, medium, low | 5 / 0 / 0 | new_valid | 0 |
| `step-intent-encoding-inc2a` | 1 | medium | 0 / 1 / 0 | clean | 1 |
| `step-intent-encoding-inc2b` | 1 | medium | 0 / 1 / 0 | clean | 1 |
| `step-intent-encoding-inc2c` | 1 | medium | 0 / 1 / 0 | clean | 1 |
| `step-intent-encoding-inc2d` | 1 | medium | 0 / 1 / 0 | clean | 1 |
| `step-intent-encoding-inc2e` | 1 | medium | 0 / 1 / 0 | clean | 1 |
| `step-intent-encoding-inc2f` | 1 | medium | 0 / 1 / 0 | clean | 1 |
| `step-intent-encoding-inc3` | 1 | low | 0 / 0 / 1 | new_valid | 0 |
| `validate-missing-source-exit-inc1` | 0 | none | 0 / 0 / 0 | clean, converged | 2 |

The six class-2 T7 findings are within the permitted per-increment threshold of three and have no high severity, so those six loops are clean. T6 and T9 are valid unpermitted kinds, so their loops are `new_valid` despite no class-1 finding.

## Totals and backstop

- Raw findings received: 9.
- Raw verdicts: 8 valid, 1 dismissed, 0 accepted risk.
- Distinct loop findings: 13 after required T7 fan-out.
- Class counts: 5 class 1, 6 class 2, 2 valid findings in neither class.
- Severity ceiling: medium.
- Required high/critical dismissal re-checks: none. The only dismissal is medium.
