# Q-78 reset round 4 GPT review

## Scope and method

I reviewed only the three active risky loops named by the brief against `efce61a`: `sidecar-status-opening-drift-inc1`, `step-intent-encoding-inc1`, and `step-intent-encoding-inc3`. I did not read another reset-round-4 reviewer file. I treated I2, I6, I7, `GPT-R3-2`, T7a through T7f, D7, `GB-4`, `GB-9`, F2, and F3 as settled and did not re-raise them.

The round-3 repairs themselves are present: I1 adds the interior-line-whitespace row to the matrix, both fields of the render fixture, both human query surfaces, the independent formatter, and the per-line-trim mutation; I3 adds the outer-whitespace row and exact complete context to human `next`; I4 compares both CRLF fields on `status --step --json` with the parser oracle and names a red control; I5 adds `beta.md` to both exact path sets and specifies a no-heading fixture and test.

### Criterion map

| Increment | Criteria mapped to the governing rule, ground, or Principle |
| --- | --- |
| `sidecar-status-opening-drift-inc1` | C1-C4 select and bound the decided deletion population under Principle 8; C5-C6 enforce the risk ground's premise (opening-only, provenance-preserving, deletion-only); C7 enforces its rendered-projection consequence; C8-C9 are Principle 7 no-regression gates; C10-C12 enforce the semantic-reading ground and Principle 3. |
| `step-intent-encoding-inc1` | C1 maps to Rule 1; C2 maps to Rules 2 and 10; C3 and C13 map to Rule 3; C4-C8 map to Rule 10 and Principle 8; C9 maps to Principle 8's unchanged-live-projection boundary; C10 maps the batch/cap ground; C11 maps the increment scope; C12 maps to Principle 7. |
| `step-intent-encoding-inc3` | C1-C2 map to Rule 1 and both halves of the risky ground under Principle 3; C3-C6 map the fresh-scaffold, copied-template, and duty-(g) obligations under Principles 3, 4, and 8; C7 maps the migration-only lifetime in Rules 5-7; C8 and C12 map to Rule 10 and Principle 8; C9 maps the exact implementation and documentation scope; C10 maps the accepted placeholder boundary; C11 maps to Principle 7. |

### Reproduced current-tree evidence

All commands ran through the project direnv shell. The validators reported `445 records, valid`, `105 steps, 81 questions, valid`, and `workflow invariants hold`; strict render check reported the plan up to date. A scratch-only write render was byte-identical to the committed generated view. `cargo test` passed 470 tests, and `cargo clippy --all-targets --all-features -- -D warnings` exited 0. `git diff --check` passed; the `efce61a` product path set is exactly the step sidecar and generated plan view; both are ASCII-clean.

The drift selector reproduced 36 anchored rows, its 9-row adjectival complement, the 19-row handover, and the 17-row worklist. The TOML 0.8 scratch probe parsed all eight logical-value rows as both fields, including exact CRLF, bare-CR, outer-whitespace, continuation, and interior-line-whitespace bytes. The three named display mutations were independent: collapse-repeated-blank, leave-bare-CR, and per-line-trim each differed from the required output. The current declaration-site census reproduced 12 files and 69 sites, the six batch declarations reproduced, all three template pairs are byte-identical, and both strict template and live-plan render checks pass.

Runnable falsification output is in the authorised scratch child at `reviewer/inc1-falsify-output.txt`:

```text
human_status_named=12/12 outer_approach_violation=true
status_json_named=6/6 interior_approach_violation=true
named_red_mutations collapse=true bare_cr=true per_line=true
no_heading_named_range_same=true wrong_has_generated_heading=true
all_named_nonempty_fixture_shape_passes=true empty_body_with_fields_omitted=true
```

## Findings

### R4G-1 - `status --step` does not apply the full matrix to both fields and both output surfaces

- Owner: `step-intent-encoding-inc1`
- Severity: medium
- Proposed class: 1
- Governing contract: Rule 10 requires whole-value-only display trimming and unchanged JSON for both fields (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:53`); criterion 2 says every matrix case is exercised as both `problem` and `approach` and is the oracle for every projection (`:164`).
- Evidence: Human status explicitly runs only repeated-blank, interior-line-whitespace, CRLF, and bare-CR (`:290`), omitting the outer-whitespace row. JSON status runs the ordinary value and CRLF (`:292-304`); the only outer-whitespace JSON value is `problem` in the partial fixture, while the partial `approach` carries repeated blanks (`:306-334`). The scratch implementation leaves whole-value trimming out only for human `approach`: all 12 named human-status checks, including both partial checks, pass, but outer-whitespace `approach` is wrong. A second implementation changes only interior whitespace in JSON `approach`: all six named JSON checks pass, but the matrix's interior `approach` bytes are changed. These are surface-local wrong implementations; the full `next` matrix cannot detect them.
- Smallest correction: run every criterion-2 fixture through `status --step --json` for both fields, analogous to `next --json`; add the outer-whitespace fixture with both fields to the exact human-status matrix; add field-specific outer-trim and interior-whitespace red controls rather than only a shared-helper mutation.

### R4G-2 - The no-heading range starts after any fabricated heading

- Owner: `step-intent-encoding-inc1`
- Severity: low
- Proposed class: 1
- Governing contract: the step generates no heading (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:19`), and the Rule-10 render sub-rule says labelled intent is first when the body has no heading (`:98`).
- Evidence: Criterion 6's range searches for the first `**Problem**` after alpha and starts recording there (`:243-248`). A wrong no-heading branch can emit ``### `beta`: fabricated heading`` immediately before `**Problem**`; the source-side `grep -c '^#' beta.md` still prints zero, the per-field ownership test still finds each expected block once, and the prescribed range is byte-identical because it discards everything before `**Problem**`. The scratch probe reports `no_heading_named_range_same=true wrong_has_generated_heading=true`.
- Smallest correction: have `intent_precedes_a_body_without_a_heading` compare the entire private per-step fragment from byte zero, or start the golden range at the exact end of alpha's fragment, and assert the first beta byte is `*` with no preceding generated content.

### R4G-3 - A field-bearing step with an empty body has no increment-1 oracle

- Owner: `step-intent-encoding-inc1`
- Severity: low
- Proposed class: 1
- Governing contract: the render sub-rule requires a step with at least one intent field to contribute even when its body is empty (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:100`), implementing Rule 10 and Principle 8's structured-source-to-human-projection rule.
- Evidence: Every field-bearing render-fixture case in C4-C6 retains a non-empty body. The existing empty-body N1 fixture deliberately carries neither field until increment 3 (`:102`). Therefore a renderer that returns `None` whenever the sidecar body is empty passes the ownership, heading, partial, no-heading, golden, and mutation criteria in increment 1, while omitting present structured intent. The scratch probe reports `all_named_nonempty_fixture_shape_passes=true empty_body_with_fields_omitted=true`.
- Smallest correction: add an inline render unit test in `src/plan/render.rs` with an empty body and one present field, comparing the entire emitted Step Details fragment; keep it in increment 1 rather than waiting for the required flip.

### R4G-4 - Increment 3 preserves only the validation tests, not the projection contract it rewrites

- Owner: `step-intent-encoding-inc3`
- Severity: medium
- Proposed class: 1
- Governing contract: Rule 10 requires all projections, and increment 3 explicitly says `render` remains unconditional, `next` wraps both fields in `Some`, and TOML `status --step` keeps reporting both values (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:673`).
- Evidence: C2 explicitly protects only the four Rule-2/Rule-3 validation tests from deletion (`:768-772`). No increment-3 criterion runs TOML `next` at all; the sole status command in C12 is intentionally Markdown-only. A wrong flip can set `problem: None` in `steps_from_toml` (or omit one context slot), delete or weaken the increment-1 `next` tests, and still satisfy the six schema checks, declaration-site checks, fresh-scaffold checks, template checks, R4 render census, Markdown fallback check, exact path set, and the generic green suite. This violates Rule 10 and Principle 8 while passing the increment's stated criteria.
- Smallest correction: make increment 3 retain every named increment-1 render/next/status projection test by name and run them green, with no expectation weakening; additionally run the freshly scaffolded template through human and JSON `next` and TOML `status --step` so both required values are observed directly after the flip.

## Raw counts and outcome

| Active loop | Raw findings | Severity ceiling | Proposed class 1 / class 2 / neither | Round-4 outcome | Resulting streak | Converges / foreclosed |
| --- | ---: | --- | --- | --- | ---: | --- |
| `sidecar-status-opening-drift-inc1` | 0 | none | 0 / 0 / 0 | clean | 2 | converges |
| `step-intent-encoding-inc1` | 3 | medium | 3 / 0 / 0 | new_valid | 0 | convergence foreclosed before the cap |
| `step-intent-encoding-inc3` | 1 | medium | 1 / 0 / 0 | new_valid | 0 | convergence foreclosed before the cap |

Raw total: **4 findings**. Severity ceiling: **medium**. No high or critical dismissal is involved, so no backstop re-check is triggered by this review file.
