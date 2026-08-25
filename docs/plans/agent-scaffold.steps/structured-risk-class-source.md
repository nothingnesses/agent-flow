### `structured-risk-class-source`: make each structured round record the only authoritative review-loop risk-class source

Decision `Q-78-risk-class-source` chose `Use structured risk_class only`, over keeping the class in both the JSONL and ledger prose and over keeping ledger prose alone. The choice already exists in `docs/metrics/workflow.jsonl`; this step gives it durable Roadmap ownership without inventing a new numbered question or human choice.

THE PROBLEM. Every `round` record already requires `risk_class`, W3 rejects inconsistent values within an increment, and `next` reads the same structured field. The scaffolded guidance, orchestrator prompt and ledger template nevertheless instruct the orchestrator to author the class again in the ledger narrative and make core counting depend on that prose. Two hand-maintained values can disagree, and the tool can validate only one.

THE APPROACH. The first round record of a loop records its class, every later record for that loop repeats the same structured value, and the existing inconsistency check fails closed. The ledger narrative keeps the review evidence a resuming human needs, but points at the joined round records for class and required streak rather than restating them. Narrative round/streak history remains until the separately open structured-ledger design settles its own scope; this step removes only the duplicated class authority.

### Increment 1, `structured-risk-class-source-inc1`

RISK CLASS `risky` (two consecutive clean review rounds). The text defines the convergence bar every reviewer loop applies and every scaffolded project inherits. Although the structured checker already follows the target design, stale guidance can make an orchestrator write or trust a conflicting class, so the process blast radius is wide.

WHAT CHANGES.

- `pack/AGENTS.md` and its committed renders `AGENTS.md` and `.agents/AGENTS.reference.md`: classify once at loop open, write that class on the first `round` record, repeat it consistently, and treat those records as authority. Remove the requirement to copy the class or required count into the ledger narrative.
- `pack/prompts/orchestrator.md` and `.agents/prompts/orchestrator.md`: round recording and convergence read the structured class; the prompt no longer tells the orchestrator to author or recompute it in prose.
- `pack/LEDGER.template.md` and `.agents/LEDGER.template.md`: the narrative points to the joined round identity and records reviewers, verdicts, outcome and reasoning, but carries no independent class value.
- `CHANGELOG.md`: under `## [Unreleased]`, record that structured `round.risk_class` is authoritative and the prose duplicate is retired.

ACCEPTANCE.

1. A fixed-string sweep over `pack/AGENTS.md`, `AGENTS.md`, `.agents/AGENTS.reference.md`, both orchestrator prompts and both ledger templates finds no instruction to record the risk class or required clean count in the ledger narrative.
2. The same surfaces state that every loop-opening `round` record carries the classification and later records for that loop must agree. No text implies that a missing structured class may be recovered from prose.
3. Existing strict metrics validation still rejects a round with no `risk_class`, and W3/`next` still reject inconsistent classes. Red controls delete the first class and mutate a later one; both remain red.
4. The committed pack/render pairs stay current through the repository's existing drift guards. The changed-path set is exactly the eight guidance/template files named above plus `CHANGELOG.md`; no product source changes are needed unless a failing test demonstrates that a supposedly structured reader still reads prose, in which case the source path is added with that evidence and reviewed as scope expansion.
5. Both validation modes, strict render, tests, Clippy, diff checks and ASCII checks pass.

### Documentation impact

The pack guidance, orchestrator prompt, ledger template and their committed copies are the documentation this semantic change makes stale, and they are the body of the increment. `pack/instrument.md` already defines `risk_class` as required structured data and needs no wording change unless the implementation sweep finds a prose-fallback promise. README describes neither risk-class storage location, so it remains unchanged. The changelog entry makes the externally scaffolded workflow change visible.
