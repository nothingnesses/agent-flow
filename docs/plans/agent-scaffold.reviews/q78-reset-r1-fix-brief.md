# Q-78 reset round 1 fix brief

## Task

Repair D1, D2, D3 and D5 from reset round 1.

Revise the complete intent design for the human's paragraph-value decision.

Record the request intake and the decision receipt.

## Human decision

The human decided on 2026-08-23 that `problem` and `approach` can contain one or more paragraphs.

This decision concerns the logical values, not source-line wrapping alone.

Both fields remain required and non-empty.

Support TOML multiline strings.

Preserve paragraph breaks in `render`, `next` and `status --step` under clear labels.

Do not impose a sentence, line or character cap.

This decision supersedes the single-line and one-sentence design clauses.

It does not supersede `Q-78-requiredfields` or the two-field choice.

Judge the revision against these Project Principles:

- Prefer the cleaner long-term architecture over the smallest diff.
- Minimal by default.
- Make illegal states unrepresentable.
- Ground decisions in evidence.
- Structured data first, project for humans.

The accepted trade-off is that paragraph values make `[[step]]` blocks and reorder diffs larger.

## Authoritative sources

Read these sources before any edit:

- `docs/plans/agent-scaffold.reviews/q78-reset-r1-triage.md`.
- `docs/plans/agent-scaffold.ledger.md`, from the current `RESUME HERE` line.
- `docs/plans/agent-scaffold.steps/step-intent-encoding.md`.
- `docs/plans/step-intent-encoding.explorations/Q-78.md`.
- `docs/plans/agent-scaffold.questions/Q-78.md`.
- The other four Q-78 step sidecars.
- `docs/plans/agent-scaffold.plan.toml`.
- `docs/metrics/workflow.jsonl`.

Treat the triage verdict as authoritative over both reviewer files.

Treat the later human decision as authoritative over D4 and D6.

## Round 1 corrections

Fix these findings:

- D1, repair the inert opening-additions filter.
- D2, include uppercase ledger citations.
- D3, include uppercase sidecar citations.
- D5, include all 84 post-sweep rows in the guard.

Decision 26 supersedes D4's single-line premise.

Decision 26 also supersedes D6's false refusal.

D7 remains valid and clean under the class 2 threshold.

Do not repair D7 in this pass.

## Intent design revision

Revise every affected clause, rule, cost statement and criterion.

Do not patch only the D4 and D6 paragraphs.

Apply these requirements:

- Define each field as non-empty prose with one or more paragraphs.
- Allow single-paragraph values.
- Allow multiline basic strings, multiline literal strings and escaped newline values.
- Reject only an absent value or a value that is empty after trim.
- Preserve paragraph boundaries on all three projections.
- Use deterministic labels and spacing on all three projections.
- Remove the `one_line` projection requirement for these values.
- Remove every one-sentence rule.
- Remove every physical-line cost claim.
- Remove every single-line error and test.
- Keep the migration record outside the plan.
- Keep per-field source citations and marks.
- Keep the scope boundary between intent and decision evidence.

Inspect the current projection helpers and fixtures before you specify exact output.

Use a small proof against the current code to check each proposed format.

State exact output and executable criteria after that proof.

If no format preserves paragraphs on one projection, stop and report the conflict.

Update the exploration so it no longer recommends the superseded design.

Preserve the historical fact that the earlier pass chose a single-line design.

Mark that rationale as superseded by decision 26 rather than silently deleting the history.

Update the `Q-78` question body with decision 26 and its fold into `step-intent-encoding`.

Do not close `Q-78`.

## Instrumentation records

Append one intake record to `docs/metrics/workflow.jsonl`:

```json
{"type":"intake","task":"q78-design-pass","classification":"non_trivial","replanned":false,"ts":"2026-08-23"}
```

Append one decision record to `docs/metrics/workflow.jsonl`:

```json
{"type":"decision","task":"step-intent-encoding","q_id":"Q-78-intent-paragraphs","options":["Allow one or more paragraphs in each logical value","Allow multiline TOML source but keep one sentence per logical value"],"recommendation":"Allow one or more paragraphs in each logical value","chosen":"Allow one or more paragraphs in each logical value","ts":"2026-08-23"}
```

Do not alter any earlier JSONL record.

Do not append a round record.

## Scope

Edit only these product sources:

- `docs/metrics/workflow.jsonl`.
- `docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md`.
- `docs/plans/agent-scaffold.steps/ledger-order-citation-currency.md`.
- `docs/plans/agent-scaffold.steps/plan-order-array-position.md`.
- `docs/plans/agent-scaffold.steps/step-intent-encoding.md`.
- `docs/plans/step-intent-encoding.explorations/Q-78.md`.
- `docs/plans/agent-scaffold.questions/Q-78.md`.
- `docs/plans/agent-scaffold.md` through `agent-flow render` only.

Do not edit `docs/plans/agent-scaffold.plan.toml`.

Do not edit `src/`, `Cargo.toml`, `pack/`, `AGENTS.md`, `.agents/` or the ledger.

Do not edit an existing review file.

Do not add a new `[[question]]`.

Do not close `Q-80`.

Do not add the successor drift step.

Do not reconfirm the expanded decision set.

Do not edit this brief.

Do not push.

## Loop state

Keep all thirteen loops at `risky`.

The human request changes all eight `step-intent-encoding` increments.

Their active clean streak is zero after this scope change.

Their reset round 1 record still counts against the round cap.

Do not change the five other loop streaks.

Do not record the next review round in this pass.

## Validation

Run every command through the project direnv environment.

Run both validation modes and read their output.

Run `render --check --strict docs/plans/agent-scaffold.plan.toml`.

Run the test suite.

Run Clippy with warnings denied.

Check that no forbidden path changed.

Check that D1, D2, D3 and D5 reproduce before the correction and close after it.

Check that no live design clause requires a single-line or one-sentence value.

Check that the intake id and decision id each occur exactly once.

Check every changed technical file for non-ASCII text.

Do not run `nix fmt`.

Do not run `just scaffold-self`.

## Commit

Commit the source files and generated plan view together.

Use a conventional `docs:` commit subject.

Do not add attribution trailers.

If a requirement conflicts with an authoritative source, stop and report the conflict.
