# Q-78 reset round 3 GPT review

## Result

This review is not clean. I found 3 raw findings, with a severity ceiling of `medium`: 2 proposed class 1 findings and 1 proposed class 2 finding. No finding is `high` or `critical`.

I reviewed only the five active increments in the brief. I did not reopen T7a-T7f, D7, `GPT-R2-5`, or accepted residuals `GB-4`, `GB-9`, `F2`, and `F3`.

## Findings

### GPT-R3-1 - The projection matrix permits per-line whitespace trimming

- Owning increment: `step-intent-encoding-inc1`
- Severity: `medium`
- Proposed class: class 1
- Violated rule and ground: Rule 10 requires that human display trim only leading and trailing whitespace around the whole value (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:53`). The increment is `risky` because these exact projected bytes ship through `render`, `next`, and `status --step` to every scaffolded project (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:61`).

The matrix's only whitespace-bearing value is `"  paragraph one\nparagraph two  "` (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:164`). Per-line trimming and whole-value trimming produce the same bytes for that value. No row puts leading or trailing whitespace on an interior logical line. A wrong shared display helper can therefore trim every non-empty line independently, pass the complete seven-row matrix on all three human surfaces, and violate Rule 10 by deleting interior whitespace.

Reproduction source: `/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r3-gpt/gpt-review/per_line_trim.rs`.

```bash
S=/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r3-gpt/gpt-review
rustc "$S/per_line_trim.rs" -o "$S/per-line-trim"
"$S/per-line-trim"
```

Observed:

```text
listed_matrix=7 wrong_helper_passes=7 names=single,two_paragraphs,repeated_blanks,outer_whitespace,crlf,bare_cr,continuation_value
probe_parser_bytes="paragraph one\n  indented interior line  \nparagraph three"
required_probe="> paragraph one\n>   indented interior line  \n> paragraph three"
wrong_probe="> paragraph one\n> indented interior line\n> paragraph three"
interior_whitespace_preserved=false
```

The repeated-blank and bare-CR red mutations do not distinguish this implementation because it preserves blank multiplicity and normalises both carriage-return forms correctly.

Smallest correction: add a logical-value matrix row with leading and trailing whitespace on an interior non-empty line, exercise it as both fields, and require byte-exact preservation through `render`, human `next`, and human `status --step`. Include that row in the independent reference-formatter comparisons.

### GPT-R3-2 - Increment 2 omits structured question prose that cites the field it deletes

- Owning increment: `plan-order-array-position-inc2`
- Severity: `medium`
- Proposed class: class 1
- Violated rule and ground: Rule 4 requires prose to restate positional citations by stable slug and never renumber them (`docs/plans/agent-scaffold.steps/plan-order-array-position.md:29`). The increment's risk ground says a missed site leaves a citation resolving to nothing or to the wrong step (`docs/plans/agent-scaffold.steps/plan-order-array-position.md:275`).

Criterion 1 searches only step sidecars and four front sidecars (`docs/plans/agent-scaffold.steps/plan-order-array-position.md:288`), while criterion 5 expressly forbids `docs/plans/agent-scaffold.plan.toml` from changing (`docs/plans/agent-scaffold.steps/plan-order-array-position.md:403`). The structured question `ask` values nevertheless contain 11 citations at or above the drift boundary:

```bash
grep -noE '\b([Oo]rder|[Ss]tep) [0-9]+\b' docs/plans/agent-scaffold.plan.toml |
  awk -F: '{n=$NF; gsub(/[^0-9]/,"",n); if (n+0 >= 85) print}'
```

Observed:

```text
1977:order 94
2088:step 87
2095:step 89
2095:step 90
2095:step 89
2095:step 89
2095:order 90
2095:step 89
2111:step 90
2111:step 90
2123:order 91
```

One live example says `Folded into workflow-enforcement-tier (order 94)` at `docs/plans/agent-scaffold.plan.toml:1977`; render publishes it in the Q-55 queue item at `docs/plans/agent-scaffold.md:148`. An implementation can satisfy every declared increment-2 worklist and path criterion while leaving that `order 94` text in place after `[[step]].order` no longer exists.

Smallest correction: include structured question `ask` prose in the pre-edit citation worklist, dispose of each selected row by stable slug or an evidence-backed historical treatment, permit `docs/plans/agent-scaffold.plan.toml` in the increment-2 changed-path set, and keep the regenerated view in the existing projection check.

### GPT-R3-3 - The exact path set rejects the documentation update required by the new `status --step` surface

- Owning increment: `step-intent-encoding-inc1`
- Severity: `low`
- Proposed class: class 2
- Violated rule: planning must identify docs made stale by a change, and acceptance checks documentation currency (`AGENTS.md:30`, `AGENTS.md:33`).

Increment 1 adds a public `status --step <slug>` human and JSON query with known, partial, and unknown states (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:130-150`), but its exact changed-path set says no file beyond eight code, fixture, and batch-manifest paths may change (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:156`). `README.md:246` currently describes `status` only as the aggregate status/question/metrics projection, and its examples at `README.md:252-258` expose no per-step query. Once the flag lands, the unqualified sentence at line 246 is no longer a complete description of the command's modes.

A correct implementation that brings the command documentation current would fail the exact changed-path criterion, so this is the class-2 "criterion refuses a correct implementation" kind.

Smallest correction: add `README.md` to increment 1's path set and documentation impact, and document the `--step` human/JSON output and its known, partial, and unknown cases. Assess the public-surface change for the changelog in the same documentation-impact clause.

## Per-increment raw counts and proposed outcomes

All five increments remain `risky` and require two consecutive clean rounds.

| Increment | Raw findings | Severities | Proposed class 1 / class 2 / neither | Proposed outcome | Resulting streak |
| --- | ---: | --- | --- | --- | ---: |
| `sidecar-status-opening-drift-inc1` | 0 | none | 0 / 0 / 0 | clean | 1 |
| `ledger-order-citation-currency-inc1` | 0 | none | 0 / 0 / 0 | clean, converged | 2 |
| `plan-order-array-position-inc2` | 1 | medium | 1 / 0 / 0 | new_valid | 0 |
| `step-intent-encoding-inc1` | 2 | medium, low | 1 / 1 / 0 | new_valid | 0 |
| `step-intent-encoding-inc3` | 0 | none | 0 / 0 / 0 | clean | 1 |

Raw total: 3. Severity ceiling: `medium`.

## Baseline verification

All project commands ran through the project direnv environment with GNU grep 3.12. The current tree passed:

- source and metrics validation: 440 records, 105 steps, 81 questions;
- workflow validation;
- strict render check;
- the complete test suite (470 tests total);
- Clippy with all targets, all features, and warnings denied.
