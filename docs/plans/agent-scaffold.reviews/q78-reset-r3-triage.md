# Q-78 reset round 3 triage

## Method and gates

I read the committed brief, both merged round-3 reviewer files, reset round 2 triage, the ledger from its current `RESUME HERE`, the relevant current plan source including Q-78 and Q-81, the Q-78 exploration, and all five active-increment sidecars. I did not read any reviewer fixture directory. I rebuilt the demonstrations in the authorised child directory `/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r3-triage/triager`.

All toolchain commands used `direnv allow && eval "$(direnv export bash)"` with the project dev shell actually loaded; no fallback toolchain was used. The baseline gates passed:

- source-plus-metrics validation: `440 records, valid`; `105 steps, 81 questions, valid`;
- workflow validation: `workflow invariants hold`;
- strict render check: `docs/plans/agent-scaffold.plan.toml: up to date`;
- tests: 470 passed and 0 failed across 12 test binaries;
- `cargo clippy --all-targets -- -D warnings`: exit 0.

## Raw verdicts

| Raw finding | Verdict | Distinct finding | Owner | Final severity | Final class | Smallest correction |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-R3-1 | valid | I1 | `step-intent-encoding-inc1` | medium | 1 | Add an interior-line-whitespace row to the logical-value matrix, run it through all three human projections and the independent formatter, and add a per-line-trim red mutation. |
| GPT-R3-2 | dismissed | — | — | medium as filed | — | None; its cited TOML question prose is outside increment 2's declared scope and changed-path set. |
| GPT-R3-3 | valid | I2 | `step-intent-encoding-inc1` | low | 2 | Permit and require the README update describing `status --step` human and JSON known, partial, and unknown output; record that documentation impact. |
| C3-1 | valid (duplicate of GPT-R3-1) | I1 | `step-intent-encoding-inc1` | medium | 1 | Same I1 correction. |
| C3-2 | valid | I3 | `step-intent-encoding-inc1` | low | 1 | Add the outer-whitespace row to criterion 7's human `next` fixtures and exact expected context block. |
| C3-3 | valid | I4 | `step-intent-encoding-inc1` | low | 1 | Run the CRLF row through `status --step --json`, compare decoded bytes with the parser oracle, and extend the JSON-normalising red control to it. |
| C3-4 | valid | I5 | `step-intent-encoding-inc1` | low | 1 | Permit a second fixture sidecar in the path set, give it a body with no heading, and pin the labelled-intent, blank-line, body order with an exact range check. |
| C3-5 | valid | I6 | `sidecar-status-opening-drift-inc1` | low | 2 | Correct the residual to cover wordless changes, not only wordless line-count changes. |
| C3-6 | valid | I7 | `ledger-order-citation-currency-inc1` | low | 2 | Remove the stale numeric illustration from criterion 1 and retain only the command-derived surplus relation. |

No finding is accepted as residual risk in this triage.

## Deduplication

| Distinct finding | Raw source(s) | Reason |
| --- | --- | --- |
| I1 | GPT-R3-1, C3-1 | Both show that the seven-row matrix cannot distinguish whole-value trimming from per-line trimming. |
| I2 | GPT-R3-3 | The exact increment-1 path set rejects the README update required to document the new public flag. |
| I3 | C3-2 | A distinct no-trim implementation passes the four human-`next` rows because outer whitespace is absent from that surface. |
| I4 | C3-3 | A distinct CRLF-only JSON normaliser passes every current `status --step --json` value-bearing fixture. |
| I5 | C3-4 | The no-heading render sub-rule has no fixture or criterion. |
| I6 | C3-5 | The residual's stated boundary omits a wordless in-line whitespace edit that both guards admit. |
| I7 | C3-6 | Criterion 1 contains figures that no longer reproduce under its own corrected selector. |

I1 is one defect with two raw reports. No other reports describe the same wrong implementation, so no further collapse is warranted.

## Reproduced evidence

### I1 — whole-value trim is not distinguished from per-line trim

Rule 10 requires whole-value-only trimming (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:53`), while criterion 2's matrix is at `:164`. I independently compiled and ran a scratch-only probe:

```text
matrix_rows=7 per_line_trim_indistinguishable=7
interior_whole="> paragraph one\n>   indented interior line  \n> paragraph three"
interior_per_line="> paragraph one\n> indented interior line\n> paragraph three"
```

Thus every named row passes an implementation that destroys interior indentation and trailing spaces. This is a class-1 wrong implementation passing while violating Rule 10. It independently reproduces both GPT-R3-1 and C3-1.

### GPT-R3-2 — dismissed: the cited rows are deliberately outside increment 2

The claimed source rows reproduce under the stated GNU grep selector: 11 matches at plan TOML lines 1977, 2088, 2095, 2111 and 2123. The live `workflow-enforcement-tier` record currently has `order = 94` (`docs/plans/agent-scaffold.plan.toml:1307-1310`). But increment 2 scopes itself to numbered citations in step sidecars and five named front sidecars (`plan-order-array-position.md:277`), and its exact changed-path criterion expressly forbids a plan-TOML change (`:403`). Rule 4's prose rule is consequently bounded by that scope. The question `ask` values are not an implementation obligation of this increment, so leaving them untouched does not violate the increment's stated risk ground or Rule 4. The demonstration reproduces; the claimed defect does not. Dismissed.

### I2 — the public `status --step` documentation is forbidden

Increment 1 adds `status --step` with human and JSON known, partial, and unknown states (`step-intent-encoding.md:130-150`), but its exact path set at `:156` permits only eight code, fixture, and manifest files. GNU grep found no `--step` mention in `README.md`; its only command description says that `status` projects aggregate step status, questions, and metrics (`README.md:246`). A correct implementation that makes that public command documentation current must edit the README and therefore fails the criterion. This is the class-2 correct-implementation-refusal kind, low. It also satisfies the planning and acceptance documentation-currency duties (`AGENTS.md:30,33`).

### I3 — human `next` has no outer-whitespace trim test

Criterion 7 names only the single-paragraph, repeated-blank, CRLF, and bare-CR human fixtures (`step-intent-encoding.md:240`). The independent probe printed:

```text
next_human_named_rows=4 untrimmed_passes=4
outer_whitespace_whole="> paragraph one\n> paragraph two"
outer_whitespace_untrimmed=">   paragraph one\n> paragraph two  "
```

A `next`-local display path that does no whole-value trimming passes all named human rows but violates Rule 10. This is a separate class-1 defect from I1 because its wrong implementation is no trim, not per-line trim.

### I4 — `status --step --json` has no CRLF value

Criterion 8's value-bearing JSON fixtures are LF-only `good`, bare-CR `problem-only`, and repeated-LF `approach-only` (`step-intent-encoding.md:255-305`). The independent probe printed:

```text
status_json_named_rows=3 crlf_normaliser_passes=3
status_json_crlf_raw="problem one\r\nproblem two"
status_json_crlf_normalised="problem one\nproblem two"
```

A CRLF-only JSON normaliser therefore passes each listed `status` JSON fixture while violating Rule 10's unchanged-deserialised-string requirement. Class 1, low.

### I5 — the no-heading render case is unpinned

The sub-rule is explicit at `step-intent-encoding.md:98`. My GNU-grep census of `src/plan/testdata/render-fixture.steps/*.md` printed one heading for each of `alpha`, `beta`, `delta`, `epsilon`, `eta`, `gamma`, and `zeta`; every live sidecar also had at least one heading. The two shape criteria instead pin a lead-in above a heading (`gamma`, `:220`) and a partial field case with a heading (`eta`, `:228`). No fixture or criterion reaches a body with no heading at all. A renderer that puts intent after the first body line only in that unrepresented case passes the specified fixtures while violating the stated format. Class 1, low.

### I6 — a wordless in-line edit escapes both drift guards

I independently created and committed a tiny scratch git repository, removed the leading `Deferred. ` token, then changed `second paragraph` to `second  paragraph` below the opening. The reconstructed criterion-6 script printed:

```text
2	2	docs/plans/agent-scaffold.steps/demo.md
checked=1 bad_anchor=0 added=0
```

The porcelain word diff contained only the token deletion and the whitespace-only context row. Thus the edit fits criterion 5's `2/2` numstat allowance and is invisible to criterion 6's added-word arm. The current accepted-residual text limits the cost to deletion-only or wordless line-count changes (`sidecar-status-opening-drift.md:213`), which does not include this wordless in-line edit. It is a low class-2 second-guard hole. The correction narrows no implementation requirement and merely records the actual accepted boundary.

### I7 — criterion 1's figures are stale under its own selector

Using GNU grep and criterion 1's exact case-insensitive selector, I reproduced:

```text
corrected_raw=131 corrected_unique=109 corrected_surplus=22
lower_raw=117 lower_unique=97 lower_surplus=20
```

The busiest line, 1735, has ten hits: two `Step 86`, two `step 86`, three `step 87`, one `step 88`, and two `step 89`. Criterion 1 instead says eight hits and a 20-site surplus (`ledger-order-citation-currency.md:82`). The lower-case historical calculation still yields 20, proving the stale number survived the later selector correction. This is an in-increment non-reproducing figure, class 2 and low.

## Per-increment outcome

This is reset round 3. Every active loop is `risky`, has used three of five rounds after this round, and requires two consecutive clean rounds. A class-2 finding at low or medium remains recorded without resetting the streak.

| Increment | Distinct valid | Severities | Class 1 / class 2 / neither | Outcome | Resulting streak | Converges | Cap forecloses convergence |
| --- | ---: | --- | --- | --- | ---: | --- | --- |
| `sidecar-status-opening-drift-inc1` | 1 | low | 0 / 1 / 0 | clean | 1 | no | no |
| `ledger-order-citation-currency-inc1` | 1 | low | 0 / 1 / 0 | clean | 2 | yes | no |
| `plan-order-array-position-inc2` | 0 | none | 0 / 0 / 0 | clean | 2 | yes | no |
| `step-intent-encoding-inc1` | 5 | medium, low, low, low, low | 4 / 1 / 0 | new_valid | 0 | no | no |
| `step-intent-encoding-inc3` | 0 | none | 0 / 0 / 0 | clean | 1 | no | no |

The two remaining rounds can still supply the needed clean streak to every non-converged loop. If a loop reaches a converging clean round at round five, convergence is checked before the cap escalation, so no current loop is foreclosed.

## Totals, backstop, and cap

- Raw findings: 9.
- Raw verdicts: 8 valid, 1 dismissed, 0 accepted risk.
- Distinct valid findings: 7.
- Raw class totals: 5 class 1, 3 class 2, 0 neither.
- Distinct class totals: 4 class 1, 3 class 2, 0 neither.
- Severity ceiling: medium.
- Backstop: none owed. The sole dismissal, GPT-R3-2, is medium; no high or critical finding was dismissed.
- Cap status: no active loop is presently foreclosed; `ledger-order-citation-currency-inc1` and `plan-order-array-position-inc2` converge this round.
