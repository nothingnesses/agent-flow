# Q-78 reset shared review brief, GPT lens

## Role

Review the repaired Q-78 design independently from the planner and the other reviewer.

Use a ground-blind and paragraph-projection falsification lens.

Assume that a wrong implementation can satisfy the criteria until evidence rules that out.

## Reviewed product

Review the product at commit `f5260c6`.

Read the complete current files, not only the diff.

Use `47984a0..f5260c6` to inspect the latest repair.

Review these product sources:

- `docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md`.
- `docs/plans/agent-scaffold.steps/ledger-order-citation-currency.md`.
- `docs/plans/agent-scaffold.steps/plan-order-array-position.md`.
- `docs/plans/agent-scaffold.steps/step-intent-encoding.md`.
- `docs/plans/agent-scaffold.steps/validate-missing-source-exit.md`.
- `docs/plans/step-intent-encoding.explorations/Q-78.md`.
- `docs/plans/agent-scaffold.questions/Q-78.md`.
- `docs/plans/agent-scaffold.plan.toml` and its generated Markdown view.
- The two appended records in `docs/metrics/workflow.jsonl`.

## Controlling records

Read these files before review:

- `docs/plans/agent-scaffold.reviews/q78-reset-r1-triage.md`.
- `docs/plans/agent-scaffold.reviews/q78-reset-r1-fix-brief.md`.
- `docs/plans/agent-scaffold.reviews/q78-r8-triage.md`.
- `docs/plans/agent-scaffold.ledger.md`, from the current `RESUME HERE` line.

The later human paragraph-value decision supersedes D4 and D6.

The authoritative intent contract is:

- Both fields are required and non-empty at the final state.
- Each logical value can contain one or more paragraphs.
- A single paragraph is valid.
- TOML multiline forms and escaped newlines are valid.
- Human projections preserve paragraph boundaries under clear labels.
- JSON projections preserve the deserialised strings.
- No sentence, line or character cap applies.

## Primary duties

Try to construct wrong implementations that satisfy every criterion.

Test the full premise and consequence of each risk ground.

Check these boundaries:

- D1 detects an authored word anywhere in a selected file.
- D2 reaches lower-case and capitalized ledger citations.
- D3 reaches lower-case and capitalized sidecar citations.
- D5 preserves every value-84 row in the post-sweep relation.
- Multiline TOML values survive validation and every projection.
- Single-paragraph values gain no invented paragraph break.
- Repeated blank lines remain distinct on human projections.
- CRLF and CR handling matches the stated human format.
- JSON values stay unchanged while human values use display formatting.
- Partial optional fields remain distinct from unknown steps.
- The required-field flip retains paragraph acceptance and empty rejection.
- The migration scripts handle newlines without shell truncation or sentinel loss.
- A transcribed multi-paragraph value resolves at its cited source.
- Sidecar duplicate detection compares complete multiline values.
- Render reconciliation counts labelled blocks without false matches.
- The changed-path sets include every implementation and documentation site.

Check that no live clause restores the superseded one-sentence or single-line design.

Check the exploration, question body and step sidecar for one coherent decision.

Check that the generated plan is a current projection.

## Settled items

Do not re-raise these accepted residuals without new evidence:

- `GB-4`.
- `GB-9`.
- `F2`.
- `F3`.

Do not re-raise D7 without evidence that changes its class, severity or measured boundary.

D6 is moot because the human removed its premise.

A finding about a settled item must identify the new evidence.

## Loop identity

Assign every finding to exactly one increment:

- `sidecar-status-opening-drift-inc1`.
- `ledger-order-citation-currency-inc1`.
- `plan-order-array-position-inc1`.
- `plan-order-array-position-inc2`.
- `step-intent-encoding-inc1`.
- `step-intent-encoding-inc2a`.
- `step-intent-encoding-inc2b`.
- `step-intent-encoding-inc2c`.
- `step-intent-encoding-inc2d`.
- `step-intent-encoding-inc2e`.
- `step-intent-encoding-inc2f`.
- `step-intent-encoding-inc3`.
- `validate-missing-source-exit-inc1`.

If one defect independently breaks two increments, file two findings.

Use the question body and exploration under the increment whose implementation contract they change.

## Finding requirements

For each finding, include:

- A stable identifier.
- The owning increment.
- Severity on the `low`, `medium`, `high`, `critical` scale.
- A candidate class under the Q-78 stop condition.
- The violated rule, criterion, decision or risk ground.
- Reproducible evidence.
- The smallest required correction.

Use a mutation for a behavioural or correctness claim.

Use an exact command or `file:line` citation when that settles the claim.

Do not file a style preference.

Do not file lack of evidence as proof of a defect.

Report zero findings explicitly when the review is clean.

## Stop-condition classes

Class 1 means a wrong implementation passes while it violates a stated risk ground, numbered rule or cited Project Principle.

Class 2 contains:

- A second-guard hole.
- A non-reproducing figure inside an increment block.
- A criterion that refuses a correct implementation.

The triager decides the final class and round outcome.

## Evidence environment

Run every project command through direnv.

Use GNU grep when ugrep differs.

Pin stdout when `validate` can exit zero on absent input.

Treat zero-match `grep -c` exit 1 as data.

Write fixtures only under:

`/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r2-gpt`.

Do not write into bare `/tmp`.

Do not use wildcard deletion.

## File safety

Do not edit product, plan, ledger, metrics, brief or existing review files.

Write findings only to:

`docs/plans/agent-scaffold.reviews/q78-reset-r2-reviewer-gpt.md`.

Do not push.

Commit only the findings file with a conventional `docs:` subject.

Do not add attribution trailers.
