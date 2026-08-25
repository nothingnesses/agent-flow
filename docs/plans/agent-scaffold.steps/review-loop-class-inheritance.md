### `review-loop-class-inheritance`: make a rebuilt artefact's reopened loop inherit the retired loop's risk class (`Q-80`)

Q-80 is decided without a new choice. The existing `Q-78-classinherit` receipt records the exact option the human chose: `Name the rebuild branch in AGENTS.md and make a re-opened loop inherit the retired loop's class`. The `Q-80` receipt is an explicit W4 alias carrying the same options, recommendation and chosen value.

THE COUNT AND CLASS ARE SEPARATE. Existing guidance already resets counters after an escalation whether the decision resumes the loop or closes it and opens a rebuilt artefact in a fresh loop. Both readings start the rebuilt work at zero. The missing rule is the convergence class: classifying every new loop afresh permits a rebuild to buy a cheaper clean-round bar even when its scope and blast radius did not narrow.

THE RULE. A human-directed rebuild closes the old loop and opens a new one with counters at zero. Its first structured round record inherits the retired loop's `risk_class` unless the rebuild narrowed the artefact's scope. A lower class is permitted only when the durable rebuild brief names the narrowed scope and grounds the lower class against the risk test; repair, rewrite or changed implementation shape alone is not narrowing. The inherited or justified replacement value then follows `structured-risk-class-source` as the only authority.

### Increment 1, `review-loop-class-inheritance-inc1`

RISK CLASS `risky` (two consecutive clean review rounds). The change governs whether rebuilding a safety-relevant artefact can reduce its convergence bar. It is guidance rather than product code, but every scaffolded review loop inherits it and a permissive ambiguity directly weakens review evidence.

WHAT CHANGES.

Update the canonical convergence rule in `pack/AGENTS.md`, its committed renders, the canonical orchestrator prompt and its committed copy, and the ledger template pair after `structured-risk-class-source` has removed the duplicate prose class. Record the Q-80 decision in `CHANGELOG.md` under `## [Unreleased]`. Do not add a new event type or alter counter arithmetic; the existing escalation record is the durable boundary.

ACCEPTANCE.

1. The convergence text names a human-directed rebuild as a loop-closing decision, says the old counters retire and the new loop starts at zero, and states class inheritance with the narrowed-scope exception.
2. The narrowed-scope exception requires a durable cited ground; a silent reclassification or a lower class justified only by "rewritten" is forbidden.
3. The orchestrator prompt gives the same instruction at point of action. The ledger template points at the inherited structured class without asking for a prose copy.
4. A content test or drift-guard assertion fails when the inheritance sentence is deleted from the pack source and when either committed render is stale. Existing counter-reset wording remains byte-equivalent in meaning.
5. No `src/` change or workflow-log schema change appears. The exact changed-path review covers the pack/committed guidance, prompt and ledger-template families plus `CHANGELOG.md`.
6. Both validation modes, strict render, tests, Clippy, diff checks and ASCII checks pass.

### Documentation impact

The workflow guidance, orchestrator prompts and ledger templates are the stale surfaces and move together. README's diagram says only that cap escalation returns to the workflow and carries no rebuild/class rule, so it stays current. The changelog records the inherited-class rule because scaffolded projects receive it.
