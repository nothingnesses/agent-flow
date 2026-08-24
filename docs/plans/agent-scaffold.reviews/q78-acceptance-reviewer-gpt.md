# Q-78 acceptance review — GPT

## Verdict

Five acceptance shortfalls: four `medium`, one `low`. I did not treat `Q-78` remaining `open` as a shortfall.

I reviewed the plan product, excluding review briefs and transient findings, against the Success Criteria, the Q-78/Q-81 decisions, Project Principles, documentation currency, and the thirteen per-increment review identities.

## Findings

### A1 — `medium`: the accepted-at-escalation waiver was written into both substrates, contrary to Q-46 and the plan Success Criteria

The authoritative waiver exists where Q-46 put TOML-primary waivers, as `[[step.waiver]]` `step-intent-encoding-w1` in `docs/plans/agent-scaffold.plan.toml:1626-1633`. The same waiver was also appended as a `type:"waiver"` JSONL record at `docs/metrics/workflow.jsonl:459`.

That duplicate contradicts the live Success Criterion at `docs/plans/agent-scaffold.success-criteria.md:20`, which says exemption waivers are nested on their steps and the JSONL holds only genuine events—rounds, escalations, decisions, intakes, and dismissals. It also contradicts the recorded Q-46 consequence at `docs/plans/agent-scaffold.md:139`: the TOML owns waivers, the JSONL keeps only genuine events, and W5 joins the TOML waiver to the retained JSONL escalation. This is not merely historical residue: `jq -r 'select(.type=="waiver") | .task' docs/metrics/workflow.jsonl` prints exactly the newly added `step-intent-encoding-inc1` row, while the plan contains 30 nested waivers.

The workflow validator stays green because the TOML-primary path reads `waivers_from_toml`; the JSONL copy is not the waiver W3/W5 consume. Leaving it creates two records for one exemption and regresses the event-only log invariant under Principle 8, Structured data first, project for humans. Keep the TOML waiver and its decision-scoped escalation, and remove the duplicate JSONL waiver.

### A2 — `medium`: the historical-intent design permits decision-receipt sources that its mandatory R2 check rejects

Rule 5 explicitly says a decision receipt is an admissible source at `<commit>:docs/metrics/workflow.jsonl` (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:37`). The design exploration is stronger: when a sidecar states neither value, “the source is the commit or the decision receipt that does” (`docs/plans/step-intent-encoding.explorations/Q-78.md:118`).

The mandatory R2 source-relevance arm admits only `docs/plans/agent-scaffold.md` or the step's own sidecar; every other path, including `docs/metrics/workflow.jsonl`, increments `bad` and continues (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:636-640`). Its pass condition requires `bad=0` (`:664`). Criterion 8 calls such rows visible exceptions to dispose of (`:767`), but that prose cannot clear R2's nonzero `bad`, so no decision-receipt row can pass the batch.

An independent scratch model of the specified `case` arm produced:

```text
docs/plans/agent-scaffold.md                         bad=0
docs/plans/agent-scaffold.steps/example-step.md      bad=0
docs/metrics/workflow.jsonl                          bad=1
```

The design therefore false-refuses one of its own promised historical-recovery routes. Either make receipt sources executable with a bounded relevance oracle, or remove that route consistently from Rule 5 and the exploration.

### A3 — `medium`: several recorded Q-78 decisions are still not folded into actionable plan state

The metrics log records final human choices for class inheritance, structured-only risk-class authority, and foreclosure/cap enforcement (`docs/metrics/workflow.jsonl:449`, `:453-454`). The drift split also requires a successor step for the authored replacement openings (`docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md:116`).

The current ledger expressly says the two enforcement decisions each still need their own step, `Q-80` needs closing rather than re-deciding, and the successor drift step still needs a planner (`docs/plans/agent-scaffold.ledger.md:549`). The structured queue confirms `Q-80` remains `open` (`docs/plans/agent-scaffold.plan.toml:2323-2324`), and no Roadmap step owns the other two decisions or the successor work.

This fails the acceptance brief's requirement to judge all recorded Q-78 decisions and the workflow rule that a resolved non-trivial decision is recorded in the queue and folded into the step it affects. It is distinct from the deliberately open status of Q-78 itself. Route a planner pass to close/fold Q-80 and author the missing Roadmap ownership before final acceptance.

### A4 — `medium`: the structured Q-78 ask still presents the superseded one-sentence design as the current recommendation

The paragraph-value decision says each field may contain one or more paragraphs and applies no sentence, line, or character cap (`docs/plans/agent-scaffold.questions/Q-78.md:1-3`; `docs/plans/agent-scaffold.steps/step-intent-encoding.md:1-29`). The structured Q-78 ask nevertheless labels “two required single-line fields ... one sentence each” as `THE RECOMMENDATION` and later says a new step needs “two prose sentences” (`docs/plans/agent-scaffold.plan.toml:2269`, `:2279`).

Those are not explicitly marked historical at their source sites. The ask's opening says the post-`THE PASS RAN` paragraphs are the authoritative outcome (`:2236`), and both stale statements occur in that later outcome section. Although the supplemental question sidecar says decision 26 supersedes them, the generated queue still publishes the contradictory structured ask at `docs/plans/agent-scaffold.md:171`.

This leaves the central value shape stale on a human-facing source-of-truth surface. Update the Q-78 ask to state the paragraph design or mark the old recommendation locally as superseded, then re-render.

### A5 — `low`: the durable decision inventory contradicts itself and the metrics log

The Q-78 ask says “NO TOTAL IS WRITTEN HERE” (`docs/plans/agent-scaffold.plan.toml:2236`, `:2299`) but also says the human decided exactly twelve times on 2026-08-21 and divides them into six plus six (`:2271`). The prescribed metrics query returns sixteen distinct Q-78 ids for that date:

```text
jq -r 'select(.type=="decision" and .ts=="2026-08-21" and (.q_id|startswith("Q-78"))) | .q_id' docs/metrics/workflow.jsonl | sort -u | wc -l
# 16
```

The current `RESUME HERE` block has a second contradiction: it says the expanded set was confirmed on 2026-08-24 (`docs/plans/agent-scaffold.ledger.md:545`), then four lines later says that confirmation is stale and must be re-put (`:549`). These stale statements do not erase any receipt, but they make the durable decision and resume records unreliable. Remove the fixed total and retire the already-superseded confirmation item.

## Convergence and waiver check

All thirteen declared Q-78 increment identities are `risky`. Twelve reached a peak consecutive-clean streak of two: `sidecar-status-opening-drift-inc1`, `validate-missing-source-exit-inc1`, both `plan-order-array-position` increments, `ledger-order-citation-currency-inc1`, all six `step-intent-encoding-inc2*` batches, and `step-intent-encoding-inc3`.

`step-intent-encoding-inc1` ended at streak one after the second-foreclosure verification. Its TOML waiver is increment-scoped, record-backed, and joins the decision escalation at `docs/metrics/workflow.jsonl:429`; W5 passes. A1 concerns the redundant JSONL waiver record, not the validity of the TOML waiver-to-escalation join.

## Verification

Run through the direnv-loaded project toolchain:

- source plus metrics validation: 459 records; 105 steps and 81 questions valid;
- workflow validation: invariants hold;
- strict render check: up to date;
- tests: 470 passed, 0 failed;
- `cargo clippy --all-targets --all-features -- -D warnings`: passed;
- `git diff --check main...HEAD`: passed.
