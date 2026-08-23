# Q-78 reset fix pass brief

## Task

Repair the eleven round 4 findings that remain after the human decisions.

Record the four accepted residuals.

Append one decision receipt for each of decisions 21 through 25.

## Authoritative sources

Read these sources before any edit:

- `docs/plans/agent-scaffold.reviews/q78-r8-triage.md`.
- `docs/plans/agent-scaffold.ledger.md`, from the line that starts `RESUME HERE (2026-08-23)`.
- The five Q-78 step sidecars.
- `docs/plans/agent-scaffold.plan.toml`.
- `docs/metrics/workflow.jsonl`.

Treat the triage verdict as authoritative over both reviewer files.

Use each triage correction instead of a reviewer demonstration that did not reproduce.

## Finding disposition

Fix these findings:

- `GB-1`.
- `GB-2`.
- `GB-3`.
- `GB-5`.
- `GB-6`.
- `GB-7`.
- `GB-8`.
- `GB-10`.
- `GB-11`.
- `F1`.
- `T-1`.

Record these accepted residuals without a repair:

- `GB-4`.
- `GB-9`.
- `F2`.
- `F3`.

Keep `GB-1` and `GB-2` as mandatory fixes.

Do not revive the superseded choice that accepted `GB-11`.

Put each residual beside the increment and criterion that own it.

State its identifier, severity, accepted cost, and non-expansion boundary.

## Decision receipts

Append five `type: "decision"` records to `docs/metrics/workflow.jsonl`.

Use `task: "q78-design-pass"` for each record.

Use the following receipt payloads:

1. `Q-78-loop-split`.
   - Options: `Thirteen per-increment loops`, `Five per-sidecar loops`, `One shared loop`.
   - Recommendation: `Thirteen per-increment loops`.
   - Chosen: `Thirteen per-increment loops`.
2. `Q-78-round4-low-residuals`.
   - Options: `Accept the five low findings`, `Fix the five low findings`.
   - Recommendation: `Accept the five low findings`.
   - Chosen: `Accept the five low findings`.
3. `Q-78-risk-class-source`.
   - Options: `Use structured risk_class only`, `Keep structured risk_class and ledger prose`, `Keep ledger prose only`.
   - Recommendation: `Use structured risk_class only`.
   - Chosen: `Use structured risk_class only`.
4. `Q-78-foreclosure-enforcement`.
   - Options: `Report and enforce foreclosure plus the round cap`, `Report foreclosure without enforcement`, `Keep both advisory`.
   - Recommendation: `Report and enforce foreclosure plus the round cap`.
   - Chosen: `Report and enforce foreclosure plus the round cap`.
5. `Q-78-gb11-revision`.
   - Options: `Fix GB-11 and retain four residuals`, `Keep GB-11 as an accepted residual`.
   - Recommendation: `Fix GB-11 and retain four residuals`.
   - Chosen: `Fix GB-11 and retain four residuals`.

Omit `ts` when the exact decision date is not recoverable from a durable source.

Do not reuse an existing `q_id`.

Do not alter any earlier JSONL record.

## Scope

Edit only these product sources:

- `docs/metrics/workflow.jsonl`.
- `docs/plans/agent-scaffold.plan.toml` when a source change requires it.
- The five Q-78 step sidecars.
- `docs/plans/agent-scaffold.md` through `agent-flow render` only.

Do not edit `src/`, `Cargo.toml`, `pack/`, `AGENTS.md`, or `.agents/`.

Do not edit the ledger or any existing review file.

Do not add a new `[[question]]` in this pass.

Do not close `Q-80` in this pass.

Do not add the steps required by decisions 23 and 24 in this pass.

Do not add the successor drift step in this pass.

Do not reconfirm the expanded decision set in this pass.

Do not change the notification cadence or GitHub subscription.

Do not edit this brief.

Do not push.

## Constraints

Keep all thirteen future review loops at `risky`.

Keep the new loop count at zero.

Do not append a `round` record in this fix pass.

Keep future loop identity in structured `step` and `increment` fields.

Keep migration evidence outside the plan.

Preserve array position as the priority source.

Preserve both required intent fields and their three projections.

Keep `pack/` work as a documented future change.

Keep every command and criterion executable from repository root.

Use a named commit for any historical resolution table.

Do not make a changing figure a pass condition.

## Validation

Run every command through the project direnv environment.

Run both validation modes and read their output.

Run `render --check --strict` with `docs/plans/agent-scaffold.plan.toml`.

Run the test suite.

Run Clippy with warnings denied.

Check that no file under `src/`, `pack/`, or `Cargo.toml` changed.

Check that `GB-11` no longer depends on the current question count.

Check that all five new receipt identifiers occur exactly once.

Check every changed technical file for non-ASCII text.

Do not run `nix fmt`.

Do not run `just scaffold-self`.

## Commit

Commit the source files and generated plan view together.

Use conventional `docs:` commit subjects.

Do not add attribution trailers.

If a requirement conflicts with an authoritative source, stop and report the conflict.
