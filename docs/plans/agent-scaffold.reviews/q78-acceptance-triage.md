# Q-78 acceptance triage

## Scope and verification

I independently read the two acceptance reports, the current TOML-primary plan and generated projection, the Q-78 design and affected step sidecars, Success Criteria, the live ledger `RESUME HERE` block, the relevant decisions, and `AGENTS.md`.

The required executable gates could not run in this worktree: `direnv`, `cargo`, and `agent-flow` are absent from `PATH`; source validation, workflow validation, and strict render each exited 127 before invoking a project tool. I therefore do not adopt the reviewers' reported green gates. The static probes below reproduced the cited source facts, and `git diff --check` exited 0.

No high or critical finding was dismissed, so no dismissal re-check is owed. The later Q-58 / phase-aware scheduling interrupt is deliberately outside this adjudication, as the brief requires.

## Verdicts

### T1 — A1 / Claude 1: valid, `medium`

The current `step-intent-encoding-w1` waiver has the required TOML-primary home at `docs/plans/agent-scaffold.plan.toml:1626`, but its duplicate remains a JSONL `type:"waiver"` at `docs/metrics/workflow.jsonl:460`. The Success Criterion requires TOML-nested waivers and an event-only JSONL (`docs/plans/agent-scaffold.success-criteria.md:20`). The TOML check consumes `waivers_from_toml(plan)` while it consumes JSONL only for rounds, decisions, and escalations (`src/workflow.rs:180-193`), so the duplicate is not load-bearing.

This is live contradictory guidance/data, not frozen Q-46 migration history: the original cutover deliberately pruned the old JSONL waiver rows, while commit `5c920e9` newly added this one. Remove only the duplicate JSONL record; retain the nested waiver and its decision escalation, then re-run both validator modes.

### T2 — A2: valid, `medium`

Rule 5 explicitly permits a decision receipt as `<commit>:docs/metrics/workflow.jsonl` (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:37`), and the design says a receipt may be the source where neither sidecar has the value (`docs/plans/step-intent-encoding.explorations/Q-78.md:118`). R2 subsequently permits only the rendered plan or the target step sidecar and rejects every other path (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:637-641`). A receipt source therefore fails the required check.

Make the promised receipt route executable with a precise receipt identity and a bounded relevance check, or remove that route consistently from Rule 5 and the exploration. Merely allowing the entire metrics log as relevant would weaken the source-relevance property.

### T3 — A3 / Claude 2: partly valid, `medium`

The missing-fold claim is valid for the outstanding decisions and successor work: the log records the structured-risk source and foreclosure-enforcement decisions (`docs/metrics/workflow.jsonl:454-455`), the ledger records that each needs its own step, Q-80 needs closure rather than re-decision, and the successor drift step still needs a planner (`docs/plans/agent-scaffold.ledger.md:551`). The successor is expressly only a pointer, not an authored step (`docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md:116`). These are unclosed plan obligations, not merely historical notes.

The Q-81 portion is invalid. Q-81 has `folded_into = "step-intent-encoding"` (`docs/plans/agent-scaffold.plan.toml:2340-2343`) and that step owns it through `[step.provenance].decisions = ["Q-81"]` (`docs/plans/agent-scaffold.plan.toml:1591-1592`). The absent prose repetition in the sidecar does not negate those typed ownership links.

A planner should author ownership for the two unstepped enforcement decisions and the successor, and fold/close Q-80 using the already taken decision without reopening it. Do not add a redundant Q-81 fold.

### T4 — A4: valid, `medium`

The live Q-78 ask still calls the superseded shape two single-line, one-sentence fields (`docs/plans/agent-scaffold.plan.toml:2269`) and repeats the two-sentence cost (`:2279`). The supplemental Q-78 decision instead says each field supports one or more paragraphs with no sentence, line, or character cap and explicitly supersedes the old form (`docs/plans/agent-scaffold.questions/Q-78.md:1-3`). Because the ask declares its post-pass text authoritative (`docs/plans/agent-scaffold.plan.toml:2236`), this is live contradictory guidance.

Replace the stale recommendation and cost with the paragraph-value decision, or explicitly mark them historical at their source; then render the projection.

### T5 — A5: valid, `low`

The prescribed 2026-08-21 receipt selector returns 16 unique Q-78 ids, while the same live ask says the human decided twelve times, split six plus six (`docs/plans/agent-scaffold.plan.toml:2271`). That conflicts with the ask's own no-fixed-total rule (`:2236`, `:2299`). The ledger also states the 2026-08-24 confirmation and then says that confirmation has become stale (`docs/plans/agent-scaffold.ledger.md:547`, `:551`).

Remove fixed totals from the live inventory and label the old confirmation as historical, retaining only the reproducible selector and the current-state instruction.

### T6 — Claude 3: valid, `medium`

`validate-missing-source-exit` changes a shipped subcommand's exit behavior for downstream checks and CI (`docs/plans/agent-scaffold.steps/validate-missing-source-exit.md:33`), yet it has no documentation-impact assessment. Its exact changed-path condition permits only `src/main.rs` and one test, “and nothing else” (`:120`), which forecloses the required changelog documentation. This is the same documentation-currency defect class already repaired in sibling schema-breaking steps.

Add the documentation-impact work, including the appropriate changelog entry, and revise the exact path set so a correct implementation can make it. Keep the stated exclusion of stale README changes if it still reproduces.

### T7 — Claude 4: valid, `low`

The exploration calls the four-item block the complete accepted-residual set of the pass (`docs/plans/step-intent-encoding.explorations/Q-78.md:324`), but additional accepted residuals live outside that block, including `GB-4` (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:200`), `F2` (`:983`), `F3` (`:1017`), and `GB-9` (`docs/plans/agent-scaffold.steps/validate-missing-source-exit.md:118`). The four-item block is complete only for the design residuals it names.

Qualify the exploration and Q-78 pointer as the complete *design* residual set, rather than claiming it inventories every accepted residual in the pass.

## Result

Seven distinct acceptance shortfalls are valid: five `medium` and two `low`. One overlapping subclaim, that Q-81 lacks a fold, is invalid because the structured question and step ownership already provide that fold. No residual risk was newly accepted by this triage.
