### `toml-primary-waiver-guidance`: make the shipped waiver instructions follow the active plan substrate

This is the focused documentation repair for the reusable cause behind the removed JSONL waiver. Fresh scaffolds are TOML-primary, but `pack/instrument.md` still presents `type: "waiver"` as their live exemption record. The TOML workflow checker instead consumes waivers nested under their owning step. Following the shipped prose therefore appends an inert non-event and leaves the intended exemption unavailable, a loud but confusing failure of the event-only-log contract.

THE ONE CANONICAL EXPLANATION. Correct `pack/instrument.md`, then regenerate its committed copies. For `[meta].primary = "toml"`, an authorised waiver lives only as nested `[[step.waiver]]` in `<task>.plan.toml`; its owning step comes from the enclosing `[[step]]`, an increment-unit waiver names a declared increment, and a record-backed accepted-at-escalation waiver still points across substrates to the real decision-scoped escalation event in JSONL. A `type:"waiver"` JSONL object is legacy input only for a Markdown-primary plan. It is not emitted for a TOML-primary plan, and a fresh TOML-primary event log contains only genuine round, escalation, decision, intake and dismissal-recheck events. Point to the existing commented waiver shape in `pack/plan-template.plan.toml` rather than hand-copying a second field schema.

This step changes documentation, not waiver parsing, W3/W5 arithmetic or historical records. It does not add a JSONL waiver, move an existing TOML waiver, or rewrite the append-only log.

### Increment 1, `toml-primary-waiver-guidance-inc1`

RISK CLASS `risky` (two consecutive clean review rounds). The edit is prose-only and reversible, but it ships to every scaffolded project and controls how a convergence exemption is recorded. The stale instruction has already produced a medium acceptance defect, so its process blast radius sets the class.

ACCEPTANCE.

1. The canonical `pack/instrument.md` waiver section states that TOML-primary waivers live only as nested `[[step.waiver]]`, explains the enclosing-step ownership and increment reference, and points to `pack/plan-template.plan.toml` for the field shape. It states that JSONL waiver records are legacy Markdown-primary input only.
2. The same section preserves the cross-substrate rule for `accepted-at-escalation`: TOML owns the waiver while its `record-backed` evidence joins a real decision-scoped JSONL escalation. Nothing says the escalation itself moves into TOML.
3. A fixed-string/semantic sweep over `pack/instrument.md`, `AGENTS.md` and `.agents/AGENTS.reference.md` finds no unqualified instruction to append a waiver to JSONL for a TOML-primary plan. A red control restoring the old unqualified bullet fails.
4. The committed copies are regenerated through the normal pack path and the existing drift guards prove they match the canonical source. The commented nested example in `pack/plan-template.plan.toml` remains valid and need not change unless the wording audit finds an actual schema mismatch.
5. Strict validation still accepts the live nested `step-intent-encoding-w1`, W5 still joins its escalation evidence, and the event-type inventory of `docs/metrics/workflow.jsonl` contains no waiver. No metrics history is appended, deleted or rewritten by this increment.
6. The changed-path set is `pack/instrument.md`, `AGENTS.md`, `.agents/AGENTS.reference.md` and `CHANGELOG.md`, unless a failing existing drift test demonstrates another generated copy; any widening is evidence-backed and reviewed. No source/parser/test change is allowed merely to make the documentation edit easier.
7. `CHANGELOG.md` records the corrected TOML-primary waiver home and the legacy Markdown qualification under `## [Unreleased]`.
8. Both validation modes, strict render, tests, Clippy, diff checks and ASCII checks pass.

### Documentation impact

The canonical instrumentation guidance and its generated copies are the stale shipped surfaces and are the body of this increment. `pack/plan-template.plan.toml` is an already-correct schema example and is a referenced verification input, not a second prose authority. README does not teach waiver authoring and remains unchanged unless the implementation finds contrary text by citation.
