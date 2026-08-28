# Narrowed Q-86 round 5 review — decision contract and scope

Reviewed risky artefact `main...4d0d737b` with `main` at `2c58cffd`. I read `AGENTS.md`, the reviewer prompt, Q-86/Q-88 and their structured records and sidecars, the narrowed synthesis and retained proposal boundaries, all four prior narrowed triages, all five synthesis triages, the owning step, Success Criteria, ledger record, receipt, and generated plan. I respected Q-88's deferred selected-option proof boundary.

The round-4 inheritance and definition fixes are closed. Strict render and workflow validation pass with 489 metrics records, 114 steps, and 88 questions; Q-88's one receipt exactly matches its six presented labels and fold; Q-86 remains `open`, Q-88 remains `decided`, and `workflow-calibration` remains `in-progress`. I found no changed production, pack, prompt, workflow-spec, Rust, or test path and no implementation authority.

## Finding 1 — the repaired serious-floor rationale uses two names that are not Project Principles in this plan

- **Severity:** low.
- **Evidence:** The human-input contract requires recommendation reasoning to be judged against “the plan's Project Principles by name” (`AGENTS.md:41`). The round-4 repair now says that `high` is recommended under **Make failure and absence explicit** and **Correctness before performance** in the authoritative synthesis (`docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:217`), Q-86 sidecar (`docs/plans/agent-scaffold.questions/Q-86.md:37`), and structured ask (`docs/plans/agent-scaffold.plan.toml:2580`). Neither name exists among this plan's eight `[[principle]]` rows at `docs/plans/agent-scaffold.plan.toml:2617-2657`; the relevant typed principle is instead **Make illegal states unrepresentable**. Reproduce the namespace mismatch with:

  ```sh
  rg -n '^name = "(Make failure and absence explicit|Correctness before performance)"' docs/plans/agent-scaffold.plan.toml
  # no output
  awk '/^\[\[principle\]\]/{p=1;next} p&&/^name =/{print; p=0}' docs/plans/agent-scaffold.plan.toml
  # prints the plan's eight names, including Make illegal states unrepresentable, but not the two cited names
  ```

- **Reasoning:** This is post-round-4 evidence from the applied fix, not a re-raise of the prior absence of rationale. The repair now provides a real safety/cost argument and correctly uses the plan principles **Ground decisions in evidence** and **Minimal by default** for its cost side, but presents its affirmative recommendation as Principle-judged under a different principle namespace. The human therefore still does not receive the positive floor rationale judged against the plan's actual Project Principles as the contract requires. The options, operational consequences, proof gate, and human authority remain intact, so impact is low.
- **Correction:** Replace the two affirmative grounds with applicable names from the plan's `[[principle]]` set (for example, **Make illegal states unrepresentable**) and preserve the existing safety/evidence/minimality argument on all three source surfaces; re-render the plan.

## Counts

Critical: 0. High: 0. Medium: 0. Low: 1. **Total: 1.**
