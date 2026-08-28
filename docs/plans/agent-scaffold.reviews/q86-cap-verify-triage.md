# Q-86 cap-verification triage

## Scope and reproduction

I independently triaged only the human-authorised Q-89 focused verification at `1419a2de`: the two narrowed-round-5 low repairs and their direct closure-path residue. I read `AGENTS.md`, the triager prompt, Q-89, `q86-narrow-r5-triage.md`, and both cap-verification reviews. I did not reopen the deferred selected-option proof obligations, architecture or floor choice, or any settled narrowed-round finding.

I reproduced GPT's cited text. The authoritative Q-86 `ask` says that “Q-89 ended the capped narrowed artefact through two low fixes and one focused mixed-model verification,” then makes closure conditional on that same verification finding nothing new (`docs/plans/agent-scaffold.plan.toml:2562`). The Q-89 decision instead states that the verification occurs after the repairs and closes the artefact only if it finds nothing new (`docs/plans/agent-scaffold.questions/Q-89.md:19,38`); the narrowed synthesis has the same ordering (`docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:7`).

`nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml` and `nix develop -c cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` both pass. Those structural checks do not resolve the contradictory current-state wording.

## Verdicts

### GPT finding 1 — Q-86's structured ask prematurely says the capped narrowed artefact ended

**Verdict: valid, low.**

The source of truth presents the verification as both already part of an ended artefact and the condition that later closes that artefact. Q-89 authorises the latter ordering: its capped counters retire, but the artefact closes only after a focused verification finds nothing new. The Q-86 ask is direct residue of the Q-89 closure fold and can misstate the current human-facing state; it should use Q-89's conditional ordering. This is new post-round-5 wording, not relitigation of T1, T2, or a deferred proof obligation.

### Claude zero findings

**No finding to adjudicate.** Claude correctly verified the two named round-5 repairs, their local derivation and receipt/closure evidence, but its zero-finding report does not rebut the independently reproducible Q-86 structured-ask contradiction above.

## Outcome, counts, and backstop

**Outcome: `new_valid`.** The two reviewer files contain one raw low claim from GPT and zero claims from Claude. Triaged counts: critical 0, high 0, medium 0, low 1; valid 1, invalid 0.

No high- or critical-severity finding was dismissed. The independent dismissal backstop is not owed. Under Q-89's authorised path, this new valid finding returns the capped narrowed artefact to the human rather than closing it as clean.
