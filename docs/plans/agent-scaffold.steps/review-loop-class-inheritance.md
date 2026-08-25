### `review-loop-class-inheritance`: make a rebuilt artefact's reopened loop inherit the retired loop's risk class (`Q-80`)

Q-80 is decided without a new choice. The existing `Q-78-classinherit` receipt records the exact option the human chose: `Name the rebuild branch in AGENTS.md and make a re-opened loop inherit the retired loop's class`. The `Q-80` receipt is an explicit W4 alias carrying the same options, recommendation and chosen value.

THE COUNT AND CLASS ARE SEPARATE. Existing guidance already resets counters after an escalation whether the decision resumes the loop or closes it and opens a rebuilt artefact in a fresh loop. Both readings start the rebuilt work at zero. The missing rule is the convergence class: classifying every new loop afresh permits a rebuild to buy a cheaper clean-round bar even when its scope and blast radius did not narrow.

THE RULE. A human-directed rebuild closes the old loop and opens a new one with counters at zero. At loop open, its new `[[step.increment]].risk_class` declaration inherits the retired loop's declared class unless the rebuild narrowed the artefact's scope. A lower class is permitted only when the durable rebuild brief names the narrowed scope and grounds the lower class against the risk test; repair, rewrite or changed implementation shape alone is not narrowing. The inherited or justified replacement is authoritative under Q-83; every later `round.risk_class` is an auditable snapshot that must match it.

### Increment 1, `review-loop-class-inheritance-inc1`

RISK CLASS `risky` (two consecutive clean review rounds). The change governs whether rebuilding a safety-relevant artefact can reduce its convergence bar. It is guidance rather than product code, but every scaffolded review loop inherits it and a permissive ambiguity directly weakens review evidence.

WHAT CHANGES.

Update the canonical convergence rule in `pack/AGENTS.md`, its committed renders, the canonical orchestrator prompt and its committed copy, and the ledger template pair after `structured-risk-class-source` has removed the duplicate prose class and `toml-primary-waiver-guidance` has regenerated the overlapping committed guidance copies. Record the Q-80 decision in `CHANGELOG.md` under `## [Unreleased]`. Do not add a new event type or alter counter arithmetic; the existing escalation record is the durable boundary.

ACCEPTANCE.

1. The convergence text names a human-directed rebuild as a loop-closing decision, says the old counters retire and the new loop starts at zero, and states class inheritance with the narrowed-scope exception.
2. The narrowed-scope exception requires a durable cited ground; a silent reclassification or a lower class justified only by "rewritten" is forbidden.
3. The orchestrator prompt gives the same instruction at point of action. Before a first reviewer is spawned, the new increment declaration exists and `next` projects its class and required streak. The ledger template points at that inherited declaration without asking for a prose copy.
4. A content test or drift-guard assertion fails when the inheritance sentence is deleted from the pack source and when either committed render is stale. A red fixture that inherits only in the first round while declaring a lower plan class fails the Q-83 mismatch check. Existing counter-reset wording remains byte-equivalent in meaning.
5. No `src/` change or workflow-log schema change appears. The exact changed-path review covers the pack/committed guidance, prompt and ledger-template families plus `CHANGELOG.md`.
6. Both validation modes, strict render, tests, Clippy, diff checks and ASCII checks pass.

### Documentation impact

The workflow guidance, orchestrator prompts and ledger templates are the stale surfaces and move together after `structured-risk-class-source` establishes plan-declaration authority. The Roadmap dependency on `toml-primary-waiver-guidance` serialises their overlapping generated copies so neither reviewed pack edit is silently lost. README's diagram says only that cap escalation returns to the workflow and carries no rebuild/class rule, so it stays current. The changelog records the inherited-class rule because scaffolded projects receive it.
