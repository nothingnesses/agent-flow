# Q-86: a safe bounded review process

Explorer proposal for `Q-86`, written under a safety, human-process, finding-lineage and reviewer-allocation lens. Advisory design notes only. This document changes no workflow rule, no constant, no status and no code, and implementation remains blocked on the later human decision that section 12 sets out.

Worktree `.agents/worktrees/q86-explorer-safety`, branch `explore/q86-safety`, from `05142309`. Scratch scripts in `/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q86-safety-process/`, reproduced in full in Appendix A so every count and every state-machine claim below can be re-derived without that directory.

Evidence and recommendation are kept apart on purpose. Sections 1 and 2 are measurement. Sections 3 to 9 are design. Section 10 is the only place a recommendation is made.

---

## 0. What the reader needs first: the brief's own snapshot has moved

The brief records that its selector "returns six passes and `[7,10,5,6,5,5]`" and states that "the selector is the authority if the log grows". The log has grown. Run today, the brief's own command returns **ten passes and `[7,10,5,6,5,5,4,2,1,0]`**.

The sequence therefore **terminated**. The tenth acceptance pass returned zero shortfalls from both reviewers and is recorded `clean`. Three consequences follow, and the synthesis must carry all three.

- The local acceptance sequence is not an observation of divergence. It is an observation of a **decaying sequence that closed at ten passes**, and any proposal that treats it as a runaway is arguing against evidence that no longer exists.
- The baseline is nonetheless still non-admissible, because non-admissibility is a property of the **rule**, not of the run. The rule places no counter on later acceptance passes, so it permits `n + 1` passes for every `n`. Section 2.2 disproves the bound mechanically. Observed termination was contingent, not forced.
- Only six triage files survive on disk (`q78-acceptance-triage.md` and `-r2-` through `-r6-`). The adjudications for passes 7 to 10 are named in the log's `artifact` strings but have been cleaned up, so the lineage evidence for the decaying tail is weaker than for the rising head. Section 1.7 states what that costs.

---

## 1. EVIDENCE

Every figure in this section is derived from `docs/metrics/workflow.jsonl` at `05142309` by the commands shown. The log holds 478 records, of which 319 are `round` records.

### 1.1 The Q-78 acceptance sequence, with severities and scope movement

```sh
jq -s 'map(select(.type == "round" and .task == "q78-design-pass" and .phase == "acceptance")) | {passes: length, valid_shortfalls: map(.valid_findings)}' docs/metrics/workflow.jsonl
```

```sh
jq -r '[inputs] | map(select(.type == "round" and .task == "q78-design-pass" and .phase == "acceptance")) | to_entries[] | [ (.key + 1), .value.valid_findings, ( .value.severities | map({critical:4, high:3, medium:2, low:1}[.]) | if length == 0 then "none" else (max | {"4":"critical","3":"high","2":"medium","1":"low"}[tostring]) end ), ( if (.value.artifact | test("\\bfold\\b|(after|and) Q-8[0-9]")) then "scope-added" else "-" end ), ( if (.value.artifact | test("expanded")) then "expanded" else "-" end ), .value.outcome ] | @tsv' -n docs/metrics/workflow.jsonl
```

| Pass | Valid shortfalls | Max severity | Scope added this pass | Target described as | Outcome |
| --- | --- | --- | --- | --- | --- |
| 1 | 7 | medium | - | - | new_valid |
| 2 | 10 | medium | scope-added | expanded | new_valid |
| 3 | 5 | **high** | - | expanded | new_valid |
| 4 | 6 | **high** | scope-added | expanded | new_valid |
| 5 | 5 | **high** | - | expanded | new_valid |
| 6 | 5 | **high** | - | expanded | new_valid |
| 7 | 4 | medium | scope-added | expanded | new_valid |
| 8 | 2 | low | scope-added | expanded | new_valid |
| 9 | 1 | low | - | expanded | new_valid |
| 10 | 0 | none | - | expanded | clean |

Three facts carry most of the design weight in this document.

- **Severity rose before it fell.** Four consecutive passes, 3 through 6, each surfaced a `high`. Late discovery was not noise on this artifact, it was the most serious material the whole sequence produced, and it arrived after two passes that had found nothing above `medium`. The triages confirm the content: `R3-1` (a silent downgrade from a two-clean-round bar to one), `R4-1` and `R4-2` (a migration with no legal state, and a task-loop identity that preserves the exact silent downgrade), `R5-1` (63 plan-review records that neither declaration arm can represent) and `R6-G1` (thirteen identities consumed by their own history).
- **The acceptance target was enlarged during the acceptance sequence.** Passes 2, 4, 7 and 8 each folded new material into the artifact under acceptance, namely the Q-58 and Q-82 scheduling fold, Q-83, the Q-85 and Q-86 convergence-investigation fold, and the Q-87 dynamic-selector decision. Every pass from the second onward describes its own target as "expanded". Acceptance was measuring a moving artifact against a moving rubric.
- **The regex used above is deliberate.** A bare `fold` matches `agent-scaf**fold**` inside the triage path on nine of ten passes and reports the whole sequence as scope-added. The word-boundary form is required. This is recorded because the false positive is easy to reproduce and would invert the reading.

The co-occurrence of the four folds with the four `high`-bearing passes is **suggestive and not causal**. One task, ten passes, one project. It is reported as an association, and section 1.7 states the limit.

### 1.2 The repeated-resume history, observed rather than hypothesised

```sh
jq -r '[inputs] | map(select(.task == "step-intent-encoding-inc1" or .increment == "step-intent-encoding-inc1")) | to_entries[] | [ (.key + 1), .value.type, (.value.phase // "-"), (.value.outcome // "-"), (.value.valid_findings // "-" | tostring), (.value.consecutive_clean // "-" | tostring), (.value.human_decision // "-") ] | @tsv' -n docs/metrics/workflow.jsonl
```

One artifact identity, `step-intent-encoding-inc1`, a `risky` plan-review loop with a required streak of 2 and a cap of 5, carries eleven ordered records: nine rounds and two escalations. The first escalation is `human_decision: "resume"` and the second is `human_decision: "decision"`. Rounds continue after each. **Three counter windows on one artifact identity.**

This is the repeated-resume path running in this repository, not a thought experiment. It is the exact branch the brief asks the baseline section to demonstrate.

Two honest qualifications. The retained records begin mid-window, and the first record's `artifact` string refers to "the round 4 fix pass" while the following escalation calls itself a "reset round 4 foreclosure", so the origin of window one is not recoverable from the retained records alone. That ambiguity is itself an instance of the point `review-loop-foreclosure-enforcement` already makes at line 19 of its sidecar, that prose inside a round record is not a `type:"escalation"` event and cannot segment an ordered reconstruction. The structural fact does not depend on resolving it: two escalations on one identity, one of them a resume, with rounds after both.

### 1.3 The escalation population, and a trigger that has now fired

```sh
jq -s 'map(select(.type == "escalation")) | {total: length, decision: (map(select(.human_decision == "decision")) | length), resume: (map(select(.human_decision == "resume")) | length)}' docs/metrics/workflow.jsonl
```

17 escalations: 15 `decision` and 2 `resume`.

`calibration-analysis.md` recorded that all five escalations then in the log carried `decision`, argued from that that "escalation is the product, not the friction", and pre-registered the reversal condition: "If the escalation records ever start carrying `human_decision: "resume"` at a material rate, that is the signal that the cap is firing too early and creating friction rather than decisions, and it should trigger an immediate re-look." Two of seventeen, at 11.8 per cent, is the first evidence on that trigger. Whether 2 of 17 is "material" is a judgement the human owns and this document does not make. It is reported because the analysis asked for it to be watched.

### 1.4 The safety instruments are almost entirely unexercised

```sh
jq -s '{rounds: (map(select(.type == "round")) | length), rounds_with_a_critical: (map(select(.type == "round" and ((.severities // []) | index("critical")))) | length), dismissal_recheck_records: (map(select(.type == "dismissal_recheck")) | length), recheck_outcomes: (map(select(.type == "dismissal_recheck") | .result))}' docs/metrics/workflow.jsonl
```

- **One round out of 319 carries a `critical`**, on `workflow-invariants` work review.
- **One `dismissal_recheck` record exists in the whole log, and its result is** `overturned`.

The second figure is the single most important safety datum available. The one time the high-or-above dismissal backstop was exercised and recorded, it **caught a real finding that a triager had waved away**. A rate of one out of one proves nothing about the population, but it is the only local evidence there is, and it points one way. The design consequence is stated in section 3.1: **the backstop re-check must never be rationed by any budget.**

### 1.5 The stopping signal the current log actually carries is defective

```sh
jq -s 'map(select(.type == "round" and .outcome == "clean" and .valid_findings > 0)) | {rounds: length, streaks_advanced: (map(select(.consecutive_clean > 0)) | length), tasks: (map(.task) | unique)}' docs/metrics/workflow.jsonl
```

**19 rounds are recorded `outcome: "clean"` while carrying `valid_findings > 0`, and all 19 advanced a consecutive-clean streak**, across 17 distinct tasks.

`calibration-analysis.md` and the 2026-08-13 audit each reported six such rounds. The count has grown to 19. The analysis drew the correct conclusion at six and it applies with more force at 19: "`valid_findings` and `severities` are the two fields I just showed to be inconsistently written, and building a convergence rule on top of them without fixing them first would encode the defect into the gate. Fix the instrument, then revisit."

This is decisive for mechanism selection. Any stopping rule keyed on `outcome` inherits a field that disagrees with its own finding count 19 times, and any rule keyed on `severities` inherits a field whose completeness is unverified. Section 10 selects on this basis.

### 1.6 Reviewer allocation as this project actually runs it

```sh
jq -s 'map(select(.type == "round" and .task == "q78-design-pass" and .phase == "acceptance")) | map(.reviewers[]) | group_by(.model) | map({model: .[0].model, harness: .[0].harness, passes: length, raw: (map(.raw_findings) | add), valid: (map(.valid_findings) | add)})' docs/metrics/workflow.jsonl
```

Every one of the ten acceptance passes ran exactly two reviewers, one on each of two models and two harnesses.

| Lens | Model | Harness | Passes | Raw findings | Valid findings | Precision |
| --- | --- | --- | --- | --- | --- | --- |
| ground-blind falsification, then closure verification | `gpt-5.6-sol` | `pi` | 10 | 26 | 26 | 100 per cent. |
| adoption and executability, then fresh-adopter closure | `claude-opus-5` | `claude-code` | 10 | 29 | 25 | 86.2 per cent. |

The round-level deduplicated total is 45 valid shortfalls against a per-reviewer sum of 51, so 6 findings were raised by both lenses.

The blind lens reached zero raw findings at pass 9 and stayed there. The adoption lens still raised 3 raw and 1 valid at pass 9. The two lenses did not stop at the same time, and the blind one stopped first.

Across the whole log, `harness` now records 360 `claude-code` reviewer passes, 51 `pi` passes and 30 absent, over 441 reviewer passes and 7 distinct model strings. **This supersedes the 2026-08-13 audit's finding that "277 reviewer passes recorded `claude-code`, 30 recorded nothing, and ZERO recorded any other harness".** Harness diversity is no longer a standing rule that has never been exercised.

### 1.7 The external experiment, and what it does and does not license

Read directly. The article states the setup as asking a model "to generate a small amount of 'perfect, non-trivial' code" and passing it "through three review-fix loops", and notes "the defect count _increases_ with each review". The linked gist gives the structure: R0 generation, R1 informed review given seven claimed properties, R2 fix, R3 informed review given the R2 change list, R4 fix, R5 blind review given the files only.

Defect counts: **R1 10, R3 12, R5 17.** The gist attributes roughly 6 self-inflicted and 2 pre-existing at R3, and roughly 5 self-inflicted and 6 pre-existing at R5. The load-bearing result is that "informed reviewers verified the claims they were handed and found almost nothing in untouched code", while the blind reviewer found six defects that had been present throughout R3 and that both informed reviews had missed.

The Lobsters discussion contributes two bounded observations. One commenter describes an approval cycle in which reviewers repeatedly asked a model to "make it better" with "no particular issue" named, which can continue indefinitely. Another argues that requesting "perfect" code is itself a confound that makes a model "10x as neurotic". A third names the missing control directly, that without "scope, constraints, and satisfaction criteria ... the risk of never converging is high".

What this licenses: pricing blind artifact-wide discovery separately from informed fix verification, and treating an unnamed open-ended improvement request as an unbounded process. What it does not license: a population estimate. One artifact, one model family, one session. The author's own caveat, that blindness is confounded with prompt breadth, applies to this project's data as well, because the `pi` lens differs from the `claude-code` lens in model, harness, blindness and brief simultaneously.

### 1.8 Limits of the evidence, stated once

- **One task, ten passes.** The acceptance sequence is a single observation. Nothing here estimates a rate.
- **The severity-decay tail is thinly evidenced.** Triages survive for passes 1 to 6 only. The decay from `medium` to `low` to `none` across passes 7 to 10 rests on the log's `severities` field alone, and section 1.5 shows that field's siblings are unreliable.
- **"Ground-blind" is a role label, not a verified information barrier.** Nothing in the log proves what the reviewer was or was not shown. The triages record that the **triager** read all preceding triages, which is a different agent.
- **The blind-versus-informed comparison is confounded four ways** and cannot separate blindness from model, harness or brief.
- **Correlated raters persist.** Six of the seven distinct model strings are Claude-family, and the only non-Claude string is `gpt-5.6-sol`, so all cross-family evidence in the log rests on the 51 `pi` passes.
- **The critical path is untested.** One critical finding and one re-check in the project's entire history. Every claim below about `critical` handling is a design claim, not an empirical one.

---

## 2. EVIDENCE: the baseline, and its mechanical disproof

The current mechanism is a required comparison and is **not recommendation-eligible**. Per the brief, it is not subjected to eligibility criteria. Instead both counterexamples are demonstrated.

The disproof is mechanical. `statemachine.awk` in Appendix A enumerates the entire reachable state set under the full input alphabet and looks for a cycle. Run:

```sh
awk -v MECH=b0 -f statemachine.awk </dev/null
awk -v MECH=b0acc -f statemachine.awk </dev/null
```

### 2.1 Counterexample one: repeated human resume

The model is faithful to `AGENTS.md` rather than convenient. A resume is a legal input **only** at an escalated state, and a review round is legal only at a non-escalated one. Allowing a resume everywhere would manufacture the cycle rather than derive it.

Result, over 12 reachable states and 58 edges:

```
P1 BOUND: DISPROVED - a cycle is reachable
  4,0,0,0,1 --human_resume--> 0,0,0,0,0 (revisits an earlier or equal depth)
  4,1,0,0,1 --human_resume--> 0,0,0,0,0 (revisits an earlier or equal depth)
  4,0,0,0,1 --human_resume--> 0,0,0,0,0   measure 1 -> 16
```

The state `(rounds_used = cap, streak = 0, escalated)` returns to the initial state `(0, 0, not escalated)` and the well-founded measure jumps from 1 back to 16. No measure decreases across the resume edge, so the graph is not well-founded and **no finite bound and no guaranteed terminal event exist**. This is the same shape as the observed `step-intent-encoding-inc1` history in section 1.2.

### 2.2 Counterexample two: the later-acceptance sequence

Acceptance is a single reviewers-then-triager pass with no streak, no round loop and no cap. A valid shortfall routes to planning or implementation and a later acceptance pass verifies the repair. Nothing counts those later passes.

Result, over 1 reachable state and 8 edges:

```
P1 BOUND: DISPROVED - a cycle is reachable
  0,0,0,0,0 --round_low--> 0,0,0,0,0 (revisits an earlier or equal depth)
  0,0,0,0,0 --round_medium--> 0,0,0,0,0
  0,0,0,0,0 --round_high_upheld--> 0,0,0,0,0
  0,0,0,0,0 --round_high_dismissed--> 0,0,0,0,0
```

Every shortfall-bearing acceptance pass is a self-loop, because no component of the state changes. The rule permits `n + 1` passes for every `n`.

The observed run terminated at ten. That termination came from the artifact ceasing to grow and the reviewers ceasing to find, not from the rule. **The counterexample stands, and the ten-pass observation bounds the cost rather than the rule.**

### 2.3 The baseline against the eight Project Principles

- **Prefer the cleaner long-term architecture over the smallest diff.** Fails. Two different bounding stories, a resettable per-artifact cap and no acceptance counter at all, coexist for one concern.
- **Minimal by default.** Passes, and this is its genuine strength. It adds no machinery, and the cost of every candidate below is measured against this.
- **Safe on existing projects.** Passes. It is what the repository already runs, so it invalidates no existing tree.
- **Idempotent.** Fails. Running the loop twice does not produce the same result as running it once, which is precisely what the resume branch encodes.
- **Make illegal states unrepresentable.** Fails. "Accepted with an unresolved critical" is representable, because acceptance settles on a single pass and the dismissal re-check is advisory in `.agents/workflow.toml` rather than enforced.
- **Ground decisions in evidence.** Mixed. The constants are calibrated in `calibration-analysis.md`, but the acceptance branch has no constant to calibrate.
- **Reproducible.** Fails on the branch that matters. Two runs of the same task can differ by an unbounded number of passes.
- **Structured data first, project for humans.** Partly. Rounds and escalations are structured, but the acceptance sequence has no structured budget or terminal at all.

---

## 3. DESIGN: what the three candidates share

The design space items the brief enumerates split into decisions that are common to any bounded mechanism and decisions that distinguish the candidates. Settling the common ones once keeps sections 4 to 6 about the actual differences.

### 3.1 Budget identity, and exactly what debits it

A **review unit** is debited **once per review round or acceptance pass opened**, from the sub-budget of the phase that opened it. Nothing else debits.

| Activity | Debits? | Why. |
| --- | --- | --- |
| A round's reviewers, however many | No, the round is one unit | Charging per reviewer would price diversity, and section 1.6 shows the second lens carried real independent value. |
| Triage | No, part of its round | Triage is not optional and rationing it would push a round toward no adjudication. |
| Backstop re-check on a high or critical dismissal | **Never** | Section 1.4: the one recorded re-check overturned. A rationed safety net is not a safety net. |
| Repair pass | No | The repair is the response to a round, and the round that verifies it debits. |
| Acceptance pass | Yes, one unit from `Ba` | This is the branch the baseline leaves uncounted. |
| Post-escalation continuation | Yes, normally | The escalation replenishes nothing. |

**Phase sub-budgets.** The task budget is a strict partition `B = (Bp, Bw, Ba)` over plan review, work review and acceptance, with **no transfer between phases**, so one phase cannot consume the whole allowance accidentally. The human may re-partition once at a checkpoint, and a re-partition may never increase the total, so the bound is invariant under it.

**Non-resettability, and the anti-laundering rule.** No human resume, no rename, no new artifact identity, no replan and no narrowing replenishes a budget. In the state machine, `human_resume` is **not a legal input at any state** of any bounded mechanism, and the run reports it rejected 22 times for M1 and M3 and 56 times for M2. There are no counters to reset, so the transition does not exist rather than being a no-op that could quietly recur.

Section 3.4 handles the harder version of this question, which is whether the terminal choices smuggle the unbounded work back in.

### 3.2 Finding identity and lineage

A finding receives a **stable id at the moment a reviewer raises it**, scoped to the task and never reused. That id survives triage, repair, later rounds and later acceptance passes. Duplicate reports of one defect by two reviewers **merge onto one id** and debit nothing extra, which preserves the existing convention that per-reviewer valid counts may exceed the deduplicated round total.

Four lineages, kept strictly separate from severity.

- **`pre-existing`.** Present before this task's work. It counts fully against the stopping gate, because it is a real defect in the delivered artifact. The external experiment's blind R5 found six such defects that two informed reviews had missed, so a mechanism that discounted them would systematically miss what blind review is for.
- **`fix-induced`.** Introduced by a prior repair pass in this task. It counts fully. `calibration-analysis.md` measured 20 of 22 recorded injections as `class = prose`, and the 2026-08-13 audit measured self-reference at 49 per cent strict across 189 findings, so this lineage is the largest single population and discounting it would be the most consequential error available.
- **`scope-expanded`.** Not a violation of any frozen obligation. It routes to a backlog obligation set for a future task and never enlarges the current one. It debits the pass it arrived in, because the pass ran.
- **`relitigated`.** An id already settled, re-raised without new evidence. The existing ledger rule dismisses it. It does not reopen an obligation and does not reset a streak.

**Reopening a settled finding** requires materially new evidence that beats the recorded verdict, in the existing `AGENTS.md` sense. A reopen consumes one of a per-finding allowance rather than being free, which is what makes section 5's bound finite.

**Severity is orthogonal to lineage.** A `pre-existing` critical and a `fix-induced` critical are both critical. A `scope-expanded` low is a backlog candidate. The two axes are recorded separately and neither is derived from the other.

### 3.3 The frozen rubric and the scope firewall

**When it freezes.** The acceptance rubric freezes when the plan review converges, before the first implementation step begins.

**Which durable artifacts define it.** Exactly three, and no others: the plan's Success Criteria sidecar (`docs/plans/<task>.success-criteria.md`), the plan's `[[principle]]` set, and each step sidecar's documentation-impact statement. All three are already committed, already single-sourced and already rendered, so the freeze adds a boundary rather than a new artifact.

**The distinguishing test.** A finding is **in scope** if and only if the reviewer can cite a specific frozen obligation by its stable id **and** give `file:line` or command evidence that the artifact as frozen fails it. A finding is a **scope expansion** if the reviewer must first author a new criterion for the finding to be a violation at all. The test is mechanical in the sense that matters: it asks whether the obligation existed before the finding did.

**Three anti-abuse rules, because the firewall is the most abusable component here.**

- **An out-of-scope ruling on a `high` or above is treated exactly like a dismissal and takes the same independent backstop re-check.** This composes with the existing backstop rather than bypassing it, and it is the specific answer to the brief's requirement that the firewall must not become a way to relabel an in-scope defect as optional.
- **A `critical` is always in scope, by rule, regardless of whether it cites a frozen obligation.** Severity overrides the firewall at the top of the scale. This is the safety floor, and section 7 shows it is what makes the unresolved-critical invariant hold.
- **The triager rules on scope, never the orchestrator.** The orchestrator owns convergence and cost and is therefore biased toward ruling findings out of scope, which is the same argument `AGENTS.md` already makes for never collapsing the triager into the orchestrator.

The frozen rubric is also the direct answer to the Lobsters observation. An approval process that can ask for "better" without naming a defect has no frozen obligation to cite, so under this firewall it produces no in-scope finding at all.

### 3.4 Terminal human choices, and the honest treatment of replan

At exhaustion the human receives the terminal menu through the human-input contract, with options, trade-offs, a recommendation and Principle-judged reasoning.

| Choice | Durable state | Receipts and waivers | Does the task end? |
| --- | --- | --- | --- |
| Accept residual risk | Each open finding recorded `accepted-residual` with id, severity, lineage and evidence retained | `type: "decision"` receipt, plus a `waiver` with `reason: "accepted-at-escalation"` and `evidence_tier: "record-backed"` | Yes. |
| Narrow scope | Named obligations removed from the frozen set, each with the finding ids it carried | `decision` receipt naming the removed obligation ids | Yes, and a backlog task holds the removed obligations. |
| Revert | Artifact restored to its pre-task state, open findings recorded `moot-by-revert` with evidence retained | `decision` receipt | Yes. |
| Replan | Task terminally closed, open findings recorded **`carried`, never `resolved`** | `decision` receipt naming the carry set | Yes, and a differently scoped task begins. |
| Abandon | Every open finding recorded `unresolved-abandoned` with identity and evidence retained | `decision` receipt | Yes. |

**"Resume with reset counters" is not on the menu under any name.** It is not a legal input at any state.

**Why replan is not the reset branch wearing a hat.** This is the hardest requirement in the brief and it deserves a direct answer rather than an assertion. Replan grants a new budget, so on its face it is a laundering vector. Three rules close it.

- The old task **terminally closes** and its open findings are permanently recorded `carried`, not `resolved`. A replan cannot change any finding's disposition, so it cannot launder the safety question even though it grants review capacity.
- The new task's frozen obligation set must be **strictly narrower than, or disjoint from**, the old one. Formally, `O_new` is a proper subset of `O_old` union the carry set, or `O_new` and `O_old` are disjoint.
- Each replan writes a `decision` receipt naming the full option set and the human's choice, so the chain is visible rather than implicit.

The second rule gives an actual bound. `|O|` is a positive integer, and a narrowing replan strictly decreases it, so **the chain of narrowing replans on a given original scope is bounded by `|O_initial|`**. A disjoint replan is a genuinely different task, and unbounded capacity to start different tasks is not a review-loop pathology, it is what a project is. The distinction is stated plainly rather than blurred: this design bounds relitigation of one scope, and it does not bound, and should not bound, a human's willingness to begin new work.

### 3.5 Reviewer allocation

- **A blind reviewer** receives the frozen artifact and the frozen rubric, and no prior findings, no fix claims and no change list.
- **An informed reviewer** verifies a named fix and its affected region, with lineage available.
- **At least one blind artifact-wide pass is reserved for the terminal streak**, so a task is never declared done on informed fix-verification evidence alone. This is priced directly from the external result, where the blind R5 found six defects present throughout R3 that both informed reviews had missed, and it is consistent with this project's own pattern in section 1.6, where the blind lens both had the higher precision and stopped first.
- **Informed passes are the right allocation immediately after a repair**, where the question is whether a named fix worked and where a blind reviewer would waste its breadth re-reading untouched material.
- **Model and harness diversity is free under section 3.1**, because a round costs one unit however many reviewers run. This is a deliberate incentive: the cost control should ration review *rounds* and never review *breadth*.

The limits from section 1.7 and 1.8 apply and are not repeated in the recommendation.

### 3.6 Sequential and severity-aware stopping

Carrying forward the sequential and survival framing that `calibration-analysis.md` established: a clean-round rule is censored by stopping, and the cap must be analysed jointly with the streak bar rather than as an isolated constant. Two consequences for every candidate here.

- **What updates confidence** is the joint distribution of the terminal predicate and the ceiling, not either alone. `calibration-analysis.md` showed that moving the bar from 2 to 1 cuts predicted escalation from 23.4 per cent to 2.9 per cent at the same cap, which is the same point in this setting: the terminal predicate moves the number that the ceiling is blamed for.
- **What censoring remains** is unchanged and unfixable by design alone. Every mechanism here stops, and none observes what the pass it did not run would have found. Only the forward experiment that `calibration-analysis.md` specifies at item 5 addresses that, and it is out of scope for this question.

**A correction to the already-raised severity-trajectory candidate.** The brief asks that it be compared rather than silently adopted. Comparing it exposes a defect that is easy to miss and that section 7.2 demonstrates mechanically: **a severity-trajectory predicate does not entail the unresolved-critical invariant.** The predicate is a statement about each pass's *novel* findings, whereas the invariant is a statement about the *open* finding set across passes. A critical raised at pass 3 and never fixed does not make pass 5's novel-severity predicate false. Without an explicit open-finding conjunct the gate accepts with an open critical, in 20 reachable ways. The conjunct is required, and the trajectory idea is safe only with it.

---

## 4. Mechanism M1: the sealed task budget

**The non-resettable task-budget design the brief requires.**

A task opens with an authorised budget `B = (Bp, Bw, Ba)` in review units. Rounds and acceptance passes debit per section 3.1. The terminal predicate is the existing consecutive-clean streak, scaled by risk class exactly as today. A loop converges at its required streak provided no critical is open and no high dismissal is awaiting its re-check. When any sub-budget reaches zero, the phase stops and the terminal menu is presented.

**A terminal severity floor `F`** governs which menu appears. With `F = critical`, `accept residual risk` and `narrow scope` are illegal only when a critical is open. With `F = high`, they are illegal when a high is open too. `F = critical` is the mandatory minimum. Section 7.1 shows the difference is large on the local data.

**What it is good at.** It bounds cost exactly and it is the smallest change from the current design, because the streak logic and the risk classes are untouched. **What it is bad at** is section 7.1.

---

## 5. Mechanism M2: the frozen-obligation ledger

**Scope-bounded rather than count-bounded, and the mechanism that attacks the cause section 1.1 measured.**

At plan-review convergence the rubric freezes into a finite enumerated obligation set `O` from the three sources in section 3.3, and `|O|` is recorded in the plan. Each obligation carries a disposition: `open`, `met`, or `residual-accepted`.

**Termination.** The task is done when every obligation is `met` or `residual-accepted`, no obligation carries an open in-scope defect, no critical is open, and no high dismissal awaits its re-check. Stopping is a statement about **scope closure**, not about round outcomes, which matters because section 1.5 shows the round-outcome field disagrees with its own finding count 19 times.

**The bound is derived rather than chosen.** Each obligation may be reopened at most `r` times, so the total number of repair cycles is at most `|O| * (r + 1)` and the ceiling is `C2 = |O| * (r + 1) + 1`. This is the sharpest distinction from M1: M1's ceiling is a policy number that a human picks, and M2's is a function of the frozen rubric, so a larger task earns a proportionally larger allowance automatically and a small one cannot hide behind a generous constant.

**Scope expansion routes to a backlog obligation set**, under the three anti-abuse rules of section 3.3.

**What it is good at.** It bounds the thing that actually grew. Passes 2, 4, 7 and 8 each enlarged the acceptance target, and under a frozen rubric each of those folds would have been a new task rather than an extension of the one under acceptance. It also converts the open-ended part of review, the part the external experiment found did not converge while the machine-checkable core did, into a named finite set. **What it is bad at** is that it depends on the obligation set being authored honestly and completely at freeze time, which is a new failure mode that does not exist today.

---

## 6. Mechanism M3: the severity-decay gate with a reserved blind pass

**Evidence-driven termination with a non-resettable ceiling as the backstop.**

Terminate when, for `k` consecutive passes, the maximum severity of **novel in-scope** valid findings is at or below a threshold `T`, the novel in-scope count is non-increasing, **no critical is open and no high dismissal awaits its re-check**, and at least one pass in the streak was **blind**. A non-resettable task ceiling `C3` bounds the process if the trajectory never decays.

`novel in-scope` excludes `relitigated` and `scope-expanded` per section 3.2, and includes `pre-existing` and `fix-induced` in full.

**What it is good at.** It is the only candidate whose terminal predicate reads the quantity that actually decayed in section 1.1, and it stops earlier than a count budget on a decaying sequence without stopping at all on a rising one. **What it is bad at** is that it reads `severities`, and section 1.5 shows the sibling fields of that record are demonstrably lossy.

---

## 7. EVIDENCE: stopping proofs and red controls

### 7.1 Replay over the live Q-78 acceptance sequence

`replay.sh` derives the sequence from the log rather than hard-coding it, so it tracks the append-only log if it grows. Run `sh replay.sh` from the repository root.

**M1, a pure count budget, at every acceptance sub-budget `Ba`:**

| `Ba` | Stops at pass | Max severity open at stop | Valid shortfalls never discovered | Worst never discovered | `accept residual` legal at `F = critical` | at `F = high` |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 3 | high | 23 | high | **yes** | NO |
| 4 | 4 | high | 17 | high | **yes** | NO |
| 5 | 5 | high | 12 | high | **yes** | NO |
| 6 | 6 | high | 7 | medium | **yes** | NO |
| 7 | 7 | medium | 3 | low | yes | yes |
| 9 | 9 | low | 0 | none | yes | yes |

The reading is unfavourable to a pure count budget and is stated plainly. **Any acceptance sub-budget below 7 stops on a pass that itself carried a `high`.** At `Ba = 6` the task would have terminated with an open high and 7 further valid shortfalls undiscovered, and **with the terminal floor at `critical` the human would have been offered `accept residual risk` as a legal option in that state.** Setting `F = high` refuses it. This is the strongest local argument for setting the terminal severity floor above `critical` on risky work, and it is an argument the brief's mandatory-minimum requirement permits but does not compel.

**M3, the decay gate, across thresholds `T` and windows `k`:**

| `T` | `k` | Fires at pass | Worst severity still found at or after firing |
| --- | --- | --- | --- |
| low | 1 | 8 | low. |
| low | 2 | 9 | low. |
| low | 3 | 10 | none. |
| medium | 1 | **1** | **high.** |
| medium | 2 | 8 | low. |
| medium | 3 | 9 | low. |
| high | 1 | **1** | **high.** |
| high | 2 | **6** | **high.** |
| high | 3 | 7 | medium. |

Two red controls fall out. At `T = medium, k = 1` the gate fires on **pass 1**, before all four high-bearing passes, because passes 1 and 2 both had a maximum of `medium`. At `T = high, k = 2` it fires on **pass 6**, a pass that itself carried a high. At `T = low` it never fires while a high is outstanding. The calibration is therefore not a matter of taste: **`T` must sit strictly below the severity that would not be shipped, and `k` must be at least 2.**

### 7.2 Exhaustive transition check

`statemachine.awk` enumerates the complete reachable state set under the twelve-input alphabet and checks two properties. **P1 BOUND**: every non-terminal edge strictly decreases the well-founded measure `(CAP - u) * 4 + oc + oh + ob`, so every path terminates. **P2 CRITICAL**: no terminal labelled `converged` or `accepted` is reachable with an open critical or a pending backstop re-check.

```sh
for m in b0 b0acc m1 m2 m3 m3nogate
do awk -v MECH=$m -f statemachine.awk </dev/null
done
```

| Mechanism | Reachable states | Edges | Longest path | P1 BOUND | P2 CRITICAL |
| --- | --- | --- | --- | --- | --- |
| `b0` baseline convergence | 12 | 58 | 4 | **DISPROVED, cycle reachable** | holds. |
| `b0acc` baseline acceptance | 1 | 8 | 0 | **DISPROVED, cycle reachable** | holds. |
| `m1` sealed budget | 38 | 203 | 4 | HOLDS | HOLDS. |
| `m2` obligation ledger | 107 | 505 | 4 | HOLDS | HOLDS. |
| `m3` decay gate | 38 | 203 | 4 | HOLDS | HOLDS. |
| `m3nogate` red control | 36 | 184 | 4 | HOLDS | **VIOLATED, 20 reachable.** |

The red control is the point of the exercise. `m3nogate` is M3 with the open-finding conjunct removed, leaving the pure severity-trajectory rule that section 3.6 warned about. It remains bounded, and it accepts with an open critical in 20 reachable ways:

```
2,1,1,0,0 --round_clean--> 3,2,1,0,0 terminal=converged open_critical=1 pending_recheck=0
2,1,0,1,0 --round_clean--> 3,2,0,1,0 terminal=converged open_critical=0 pending_recheck=1
```

Read the first witness: two units spent, decay streak 1, a critical open from an earlier pass. A clean pass advances the streak to 2 and the gate fires. The critical never entered the predicate, because the predicate only ever read the current pass. **The trajectory rule is bounded and unsafe until the conjunct is added, and boundedness and safety are genuinely independent properties here.**

`human_resume` is rejected as an illegal input 22 times for `m1` and `m3` and 56 times for `m2`, at every state, which is the mechanical form of the non-resettability claim.

The parameters are deliberately small (`CAP = 4`, `REQ = 2`, `k = 2`, `|O| = 2`) so the enumeration is genuinely exhaustive rather than sampled. Nothing in either property depends on the values.

### 7.3 Every required red-control path

| Path | M1 | M2 | M3 |
| --- | --- | --- | --- |
| **Repeated human resume** | Not a legal input. No transition exists, so the ceiling is untouched. Bound: `B`. | Same. Bound: `\|O\| * (r + 1) + 1`. | Same. Bound: `C3`. |
| **Unbounded acceptance-repair sequence** | Every acceptance pass debits `Ba`. Bound: `Ba`. Terminal: exhaustion menu. | Every pass must close an obligation or spend a reopen. Bound: `\|O\| * (r + 1)`. Terminal: scope closure or ceiling. | Every pass debits `C3`. Bound: `C3`. Terminal: decay streak or ceiling. |
| **Fix-induced high near exhaustion** | Counts fully, resets the streak, debits. Terminal: `exhausted_restricted` when `F = high`, `exhausted_full` when `F = critical`. | Reopens its obligation and spends one reopen allowance. Terminal: as M1. | Counts fully as novel in-scope, resets the decay streak. Terminal: as M1. |
| **Scope-expanded low** | Debits its pass, counts as clean for the streak. Bound unchanged. | Routed to the backlog obligation set. `\|O\|` unchanged, so the bound is unchanged. | Excluded from `novel in-scope`, so the decay streak advances. Bound unchanged. |
| **Relitigation without new evidence** | Dismissed by the ledger rule, counts as clean. Bound unchanged. | Does not reopen an obligation, so no reopen allowance is spent. Bound unchanged. | Excluded from `novel in-scope`. Bound unchanged. |
| **Narrowing or replan** | New budget, old task terminally closed with findings `carried`. Chain of narrowing replans bounded by `\|O_initial\|`. | Same, and narrowing strictly decreases `\|O\|`, which **is** the bound, so the chain bound is exact. | Same as M1. |
| **Unresolved critical at exhaustion** | Menu restricted to revert, replan-with-carry, abandon. `accept residual` and `narrow scope` illegal. Terminal: `exhausted_restricted`. Verified over 38 states. | Same, and a critical is always in scope by the section 3.3 severity floor so it cannot be routed to backlog. Verified over 107 states. | Same, and the terminal predicate additionally cannot fire. Verified over 38 states. |

All three mechanisms therefore have a finite bound or an exact terminal event on every required path, which is the eligibility condition the brief sets.

---

## 8. DESIGN: all three against all eight Project Principles by name

| Principle | M1 sealed budget | M2 obligation ledger | M3 decay gate |
| --- | --- | --- | --- |
| **Prefer the cleaner long-term architecture over the smallest diff** | Weakest. It keeps two stopping stories, a streak and a budget, layered on one concern. | Strongest. One concept, scope closure, replaces the streak, the cap and the uncounted acceptance branch. | Middle. Replaces the streak with a better predicate but keeps a separate ceiling. |
| **Minimal by default** | Strongest. Streak logic and risk classes are untouched, and only a counter is added. | Weakest. It requires a new authored artifact, the frozen obligation set. | Middle. New predicate, no new artifact. |
| **Safe on existing projects** | Good. A budget can be absent and default to unbounded on a legacy tree. | Needs care. A tree with no frozen rubric must be exempt, not failed. | Good, if `severities` is absent-tolerant. |
| **Idempotent** | Holds. No reset transition exists, so two runs of one task give one result. | Holds, and more strongly, because closure is a property of the artifact rather than of the run. | Holds. |
| **Make illegal states unrepresentable** | Partial. The open-critical conjunct is a guard on the terminal, not a property of the type. | Strong. An obligation's disposition is a closed enum and "done with an open obligation" is not constructible. | Partial, and section 7.2 shows how easy the mistake is to make. |
| **Ground decisions in evidence** | Poor here. Section 7.1 shows no value of `Ba` below 7 is defensible on the local data, and the local data is one task. | Good. It targets the enlargement that section 1.1 measured. | Good in principle, undermined in practice by section 1.5. |
| **Reproducible** | Holds. The bound is a constant. | Holds, and the bound is derivable from committed data. | Holds given the ceiling. |
| **Structured data first, project for humans** | Good. A budget is a `[meta]` integer triple. | Strongest. Obligations become structured rows projected into the rendered plan, which is the pattern `Q-78` and `Q-83` already chose. | Good, but it makes `severities` load-bearing, which section 1.5 argues against today. |

The baseline's assessment is at section 2.3.

---

## 9. DESIGN: migration and enforcement

Common to all three. **Advisory** means prose guidance an agent may follow. **Enforced** means `validate --workflow` exits non-zero.

| Surface | What moves | Advisory or enforced |
| --- | --- | --- |
| `.agents/workflow.toml` and `pack/workflow.toml` | New constants beside `[convergence]` and `[rounds]`. M1 adds the budget triple. M2 adds the reopen allowance `r`. M3 adds `T` and `k`. All add the terminal severity floor `F`. | Data, consumed by an enforced check. |
| `src/workflow_spec.rs` | `WorkflowSpec` gains the fields, and the existing drift-guard test that parses the TOML and asserts equality extends to them. | Enforced by the existing test. |
| `ReviewProcess` reconstruction | The single largest dependency. `review-loop-foreclosure-enforcement` is already scheduled to deliver the shared typed reconstruction with `Convergence` and `SinglePass` disjoint. **All three mechanisms need `SinglePass` to gain a task-scoped counter, which today it deliberately has none of.** M2 additionally needs an obligation join. This work must land after that step, never beside it. | Enforced. |
| `src/workflow.rs` | A new check in the W-series. Convergence-or-waiver precedence in W3 is untouched. | Enforced. |
| `src/next.rs` | New reasons distinguishing budget exhaustion from foreclosure and from cap, and the terminal menu. Read-only and advisory authority is unchanged. | Advisory output of an enforced state. |
| `src/metrics.rs` and the record schema | `round` gains the debited phase and the running spend. M2 adds obligation ids and dispositions. M3 makes `severities` load-bearing. A new terminal-choice record, or an extension of `escalation` with the terminal option chosen. | Enforced by `validate`. |
| Plan and ledger state | M2's frozen obligation set is plan-resident structured data, projected into the rendered view. The ledger's round-records narrative gains the running spend. The ledger is still deleted at task close, so **no terminal record may live only in the ledger.** | Mixed. |
| **Append-only history** | **Nothing is rewritten.** The mechanism adopts the same honest device `review-loop-foreclosure-enforcement` already established: a typed, digest-pinned adoption boundary in the plan TOML that retires pre-adoption history for the new check only. Existing waivers, the `q78-design-pass` `[[task_loop]]` declaration and the Q-81 historical rows are untouched. A tree with no boundary enforces from its first round. | Enforced, fail-closed. |
| `pack/AGENTS.md`, `AGENTS.md`, `.agents/AGENTS.reference.md` | The Convergence and Accept sections. Acceptance stops being described as unbounded. Rendered from the single source, so copies cannot drift. | Advisory text, byte-guarded. |
| `pack/instrument.md` | The new record fields and the semantics of the terminal record. | Advisory. |
| `pack/prompts/orchestrator.md`, `reviewer.md`, `triager.md`, and the `.agents/` copies | Reviewer prompts gain the blind-versus-informed brief. **The triager prompt gains the scope ruling and the rule that an out-of-scope ruling at `high` or above takes the backstop re-check.** | Advisory, and the highest-leverage change for M2. |
| `pack/plan-template.plan.toml`, `pack/plan-template.success-criteria.md` | M2 adds the obligation rows. | Data. |
| `pack/LEDGER.template.md` and `.agents/LEDGER.template.md` | The spend line in the round-records narrative. | Advisory. |
| `README.md` | The cap-labelled diagram must stay value-free and become budget-accurate. | Advisory. |
| `CHANGELOG.md` | Records that a previously valid tree may now fail. | Advisory. |

**What is enforced versus advised, stated sharply.** The bound itself must be enforced, because an advisory bound is the current cap and section 1.2 shows what an advisory bound does. The **terminal severity floor must be enforced**, because it is the only thing standing between a budget and a concealed critical. Reviewer allocation stays **advisory**, because a machine cannot verify that a reviewer was genuinely blind, and section 1.8 records that "ground-blind" is a label rather than a proven barrier.

---

## 10. RECOMMENDATION

**Recommended: M2, the frozen-obligation ledger.** Selected only from the viable bounded mechanisms, per the brief.

Four reasons, in descending weight.

- **It bounds the thing that actually grew.** Section 1.1 measures four scope folds into an artifact already under acceptance, and every pass from the second onward describing its own target as "expanded". M1 and M3 both bound the *response* to a growing artifact. Only M2 bounds the growth. Given a choice between rationing the review of a moving target and freezing the target, the second is the cleaner architecture and the one that addresses the measured cause.
- **Its termination predicate does not read the fields that are broken.** Section 1.5 shows 19 rounds recorded `clean` while carrying valid findings, all 19 advancing a streak. M1's predicate is the streak, which is computed from `outcome`. M3's predicate is `severities`, whose sibling fields are demonstrably lossy. M2's predicate is a per-obligation disposition authored by a triager, which is the one judgement in this system that is already produced by an independent agent and already committed to a findings file.
- **Its bound is derived rather than chosen.** Section 7.1 shows that no defensible value of a count budget exists on the local data, because every value below 7 stops on a `high`-bearing pass and 7 is a sample of one. `|O| * (r + 1) + 1` requires no such guess and scales with the task.
- **It answers the external evidence most directly.** The experiment found that the machine-checkable core converged while open-ended contract, conformance and prose obligations did not, and the Lobsters thread names missing "scope, constraints, and satisfaction criteria" as the root cause. A frozen finite obligation set is exactly the conversion of the second category into the first.

**Confidence: MEDIUM.**

It is not higher for three reasons. The evidence is one task and ten passes. M2 introduces a genuinely new failure mode that does not exist today, namely an obligation set authored incompletely at freeze time, and the `critical`-always-in-scope rule is the only backstop against it, which is a design claim with one supporting observation in the whole log. And M2 is the weakest of the three on **Minimal by default**, which is a real cost that section 8 does not hide.

It is not lower because the two mechanical results are direct enumerations rather than inferences: the baseline cycle at section 2, and P1 and P2 over 107 reachable states at section 7.2.

**Evidence that would overturn this recommendation.**

- **A second acceptance sequence that grows long with a frozen rubric.** If a task whose scope demonstrably did not move still needed many acceptance passes, the diagnosis in section 1.1 is wrong and M3 becomes the better answer.
- **A repaired `outcome` and `severities` instrument.** Section 1.5 is the main argument against M3. `calibration-analysis.md` item 2 specifies the repair. If it lands and the fields become trustworthy, M3's predicate reads the quantity that actually decayed and its case strengthens considerably.
- **An obligation set found to be systematically incomplete at freeze.** If in-scope defects routinely fail to cite any frozen obligation, the firewall is filtering real defects and M1's blunter instrument is safer.
- **Any recorded case of a `critical` routed to backlog.** That would falsify the severity-floor rule directly and would make M2 unsafe as specified.
- **A material rise in `human_decision: "resume"`.** Section 1.3 records the first two. If resumes become common under any mechanism, the terminal menu is not being taken seriously and the problem is human process rather than mechanism.

**What this recommendation does not claim.** It does not claim the Q-78 sequence diverged, and section 0 corrects the record. It does not claim the folds caused the highs. It does not claim a rate for anything.

---

## 11. YAGNI boundary: what not to build first

- **No general issue tracker.** The backlog obligation set is a list of obligation ids in the plan TOML, and nothing more. No priorities, no assignment, no lifecycle beyond `open` and `folded into <task>`.
- **No autonomous risk judge.** Severity and scope stay triager judgements entering through typed inputs. Nothing infers a risk class, and the existing rule that no transition manufactures a triage verdict holds unchanged.
- **No probabilistic defect oracle.** No survival model, no threshold fitted from the log, no confidence interval in a gate. Section 1.8 explains why the sample cannot support one, and `calibration-analysis.md` already declined to build one on the same grounds.
- **No reviewer marketplace.** Allocation stays advisory prompt guidance. Do not build reviewer scoring, selection or routing from the attribution data.
- **No rewriting of historical findings or records.** The append-only log stays append-only, and adoption uses the digest-pinned boundary device that already exists.
- **No per-reviewer or per-token budget accounting.** One unit per round, deliberately, so diversity stays free.
- **No new phase and no new role.** M2 reuses the planner for the freeze, the triager for the scope ruling and the orchestrator for the terminal menu.
- **Do not build the mechanism before `review-loop-foreclosure-enforcement` lands.** Every candidate needs the shared typed reconstruction and needs `SinglePass` to acquire a task-scoped counter. Building beside that step would create the second loop formula it exists to prevent.
- **Do not implement anything until the human decides.** `Q-85` scheduled this investigation and decided nothing about the mechanism.

---

## 12. The later human decision that implementation needs

Presented through the human-input contract at synthesis time. Only the viable bounded options go to the human. The baseline is comparison evidence and is not an option.

**The question.** Which bounded convergence mechanism should replace the current resettable per-artifact cap and the uncounted acceptance-repair sequence?

**The options.** M1 the sealed non-resettable task budget, M2 the frozen-obligation ledger, M3 the severity-decay gate with a reserved blind pass. Trade-offs at sections 4 to 6, Principle assessment at section 8, migration at section 9.

**The recommendation.** M2, at MEDIUM confidence, for the reasons at section 10.

**Three sub-decisions the human owns whichever option is chosen.**

- **The terminal severity floor `F`.** The mandatory minimum is `critical`. Section 7.1 shows that at `F = critical` the human would have been offered `accept residual risk` on a pass carrying an open `high`, with seven further shortfalls undiscovered. Setting `F = high` for `risky` artifacts refuses that. This is a safety-appetite decision and is not derivable from the data.
- **Whether at least one blind artifact-wide pass is reserved in the terminal streak.** It costs one pass per task. The external result and the local precision figures both support it, and both are confounded.
- **Whether the instrument repair precedes the mechanism.** Section 1.5's 19 rounds argue that a gate built on `outcome` or `severities` today would encode a known defect. M2 is the least exposed to this, which is part of why it is recommended, but the question is worth putting explicitly.

**What must not be inferred.** `Q-85` decided only where this investigation belongs. Nothing in it approves a mechanism.

---

## Appendix A: scripts

All three are read-only and mutate no tracked file. Run from the repository root.

### A.1 `evidence.sh`

Every count in section 1. The individual `jq` commands are reproduced inline in sections 1.1 to 1.6, so this script is a convenience wrapper over them.

### A.2 `replay.sh`

Derives the acceptance sequence from the log rather than hard-coding it, then replays the baseline, M1 at every sub-budget, and M3 at every threshold and window. Produces the tables at section 7.1. Its final block replays the `step-intent-encoding-inc1` window arithmetic from section 1.2.

### A.3 `statemachine.awk`

The exhaustive transition check behind section 7.2.

```awk
# Usage: awk -v MECH=<b0|b0acc|m1|m2|m3|m3nogate> -f statemachine.awk </dev/null
#
# State: u  review units spent
#        c  streak (clean streak for m1/b0, decay streak for m3)
#        oc open critical outstanding
#        oh high dismissal awaiting the backstop re-check
#        ob open frozen-rubric obligations (m2), or the escalated flag (b0)
#
# Input alphabet, applied at EVERY reachable non-terminal state:
#   1 round_clean          no novel in-scope valid finding
#   2 round_low            novel in-scope, max severity low
#   3 round_medium
#   4 round_high_upheld    triager ruled it valid, so it must be repaired
#   5 round_high_dismissed triager dismissed it, so a re-check is owed
#   6 round_critical
#   7 round_scope_expanded ruled out of the frozen rubric, routed to backlog
#   8 round_relitigated    re-raised with no new evidence, dismissed by ledger
#   9 recheck_upheld       backstop upholds the dismissal
#  10 recheck_overturned   backstop overturns it, the finding is valid
#  11 fix_closes_critical  a repair pass closes the open critical
#  12 human_resume         the baseline reset branch

function enc(u, c, oc, oh, ob) { return u "," c "," oc "," oh "," ob }
function measure(u, c, oc, oh, ob) { return (CAP - u) * 4 + oc + oh + ob }

BEGIN {
  if (MECH == "") { print "set -v MECH"; exit 1 }
  CAP = 4; REQ = 2; K = 2; OBL0 = 2

  NIN = 12
  nm[1]="round_clean";          nm[2]="round_low";            nm[3]="round_medium"
  nm[4]="round_high_upheld";    nm[5]="round_high_dismissed";  nm[6]="round_critical"
  nm[7]="round_scope_expanded"; nm[8]="round_relitigated"
  nm[9]="recheck_upheld";       nm[10]="recheck_overturned";   nm[11]="fix_closes_critical"
  nm[12]="human_resume"

  start = enc(0, 0, 0, 0, (MECH == "m2" ? OBL0 : 0))
  q[1] = start; seen[start] = 1; depth[start] = 0; qh = 1; qt = 1
  edges = 0; badmeasure = 0; cycles = 0; violations = 0; maxdepth = 0; rejected = 0

  while (qh <= qt) {
    s = q[qh++]
    if (term[s] != "") continue
    split(s, f, ",")
    u = f[1] + 0; c = f[2] + 0; oc = f[3] + 0; oh = f[4] + 0; ob = f[5] + 0

    for (i = 1; i <= NIN; i++) {
      if (i == 9 || i == 10) { if (oh == 0) { rejected++; continue } }
      if (i == 11)           { if (oc == 0) { rejected++; continue } }
      if (i == 12 && MECH != "b0" && MECH != "b0acc") {
        # In every bounded mechanism a human resume is NOT a legal input:
        # there are no counters to reset. Recorded as rejected, not a no-op.
        rejected++; illegal_resume++; continue
      }
      # In the baseline, a resume is legal ONLY at an escalated state, and a
      # review round is legal only at a NON-escalated one. Modelling it this
      # way matters: allowing a resume anywhere would manufacture the cycle
      # instead of deriving it from the rule as written.
      if (MECH == "b0") {
        if (i == 12 && ob != 1) { rejected++; continue }
        if (i != 12 && ob == 1) { rejected++; continue }
      }

      nu = u; nc = c; noc = oc; noh = oh; nob = ob; lab = ""

      if (MECH == "b0") {
        if (i >= 1 && i <= 8) {
          nu = u + 1
          if (i == 1 || i == 7 || i == 8) nc = c + 1; else nc = 0
          if (nc >= REQ) lab = "converged"
          else if (nu >= CAP) nob = 1        # escalated, and NOT terminal
        } else if (i == 12) {
          nu = 0; nc = 0; nob = 0; lab = ""  # the reset branch
        } else { rejected++; continue }
      }

      else if (MECH == "b0acc") {
        if (i >= 1 && i <= 8) {
          nu = 0                             # nothing counts an acceptance pass
          if (i == 1) lab = "accepted"; else nc = 0
        } else { rejected++; continue }
      }

      else if (MECH == "m1" || MECH == "m2") {
        if (i >= 1 && i <= 8) {
          nu = u + 1
          if (i == 1 || i == 7 || i == 8) nc = c + 1; else nc = 0
          if (i == 6) noc = 1
          if (i == 5) noh = 1
          if (MECH == "m2" && (i == 1 || i == 2 || i == 3)) nob = (ob > 0 ? ob - 1 : 0)
          converged = (nc >= REQ && noc == 0 && noh == 0)
          if (MECH == "m2") converged = (converged && nob == 0)
          if (converged) lab = "converged"
          else if (nu >= CAP) lab = (noc == 1 || noh == 1) ? "exhausted_restricted" : "exhausted_full"
        } else if (i == 9)  { noh = 0 }
        else if (i == 10) { noh = 0; nc = 0 }
        else if (i == 11) { noc = 0 }
      }

      else if (MECH == "m3" || MECH == "m3nogate") {
        if (i >= 1 && i <= 8) {
          nu = u + 1
          # the decay streak advances only on a pass whose NOVEL in-scope
          # findings are at or below the low threshold
          if (i == 1 || i == 2 || i == 7 || i == 8) nc = c + 1; else nc = 0
          if (i == 6) noc = 1
          if (i == 5) noh = 1
          if (MECH == "m3") converged = (nc >= K && noc == 0 && noh == 0)
          else              converged = (nc >= K)     # RED CONTROL: gate omitted
          if (converged) lab = "converged"
          else if (nu >= CAP) lab = (noc == 1 || noh == 1) ? "exhausted_restricted" : "exhausted_full"
        } else if (i == 9)  { noh = 0 }
        else if (i == 10) { noh = 0; nc = 0 }
        else if (i == 11) { noc = 0 }
      }

      t = enc(nu, nc, noc, noh, nob)
      edges++

      if (lab == "") {
        if (measure(nu, nc, noc, noh, nob) >= measure(u, c, oc, oh, ob)) {
          badmeasure++
          if (badlist[s "->" t] == 0) {
            badlist[s "->" t] = 1
            if (nbad < 6) { nbad++; badshow[nbad] = "  " s " --" nm[i] "--> " t \
              "   measure " measure(u,c,oc,oh,ob) " -> " measure(nu,nc,noc,noh,nob) }
          }
        }
        if (seen[t] && depth[t] <= depth[s]) {
          cycles++
          if (ncyc < 4) { ncyc++; cycshow[ncyc] = "  " s " --" nm[i] "--> " t " (revisits an earlier or equal depth)" }
        }
      } else {
        # P2: an accepting terminal must never carry an open critical or a
        # pending high re-check.
        if ((lab == "converged" || lab == "accepted") && (noc == 1 || noh == 1)) {
          violations++
          if (nvio < 6) { nvio++; vioshow[nvio] = "  " s " --" nm[i] "--> " t \
            " terminal=" lab " open_critical=" noc " pending_recheck=" noh }
        }
        term[t] = lab
      }

      if (!seen[t]) {
        seen[t] = 1; depth[t] = depth[s] + 1
        if (depth[t] > maxdepth) maxdepth = depth[t]
        q[++qt] = t
      }
    }
  }

  nstates = 0; for (k in seen) nstates++
  print "MECHANISM: " MECH
  print "  parameters: ceiling=" CAP "  required_streak=" REQ "  decay_window=" K "  obligations=" OBL0
  print "  reachable states: " nstates "    edges explored: " edges "    inputs rejected as illegal: " rejected
  print "  longest path from the initial state: " maxdepth
  print ""
  if (MECH == "b0" || MECH == "b0acc") {
    print "  P1 BOUND: " (cycles > 0 || badmeasure > 0 ? "DISPROVED - a cycle is reachable" : "no cycle found")
    for (i = 1; i <= ncyc; i++) print cycshow[i]
    for (i = 1; i <= nbad; i++) print badshow[i]
    print "  A reachable cycle means no finite bound and no guaranteed terminal event."
  } else {
    print "  P1 BOUND: " (badmeasure == 0 ? "HOLDS" : "FAILED") \
          " - every non-terminal edge strictly decreases the measure (CAP-u)*4+oc+oh+ob."
    for (i = 1; i <= nbad; i++) print badshow[i]
    print "           the measure starts at " (CAP * 4 + (MECH == "m2" ? OBL0 : 0)) \
          " and is bounded below by 0, so every path terminates."
    print "  human_resume rejected as an illegal input at every state: " illegal_resume " times."
  }
  print ""
  print "  P2 CRITICAL INVARIANT: " (violations == 0 ? "HOLDS - no accepting terminal carries an open critical or a pending re-check." : "VIOLATED (" violations " reachable)")
  for (i = 1; i <= nvio; i++) print vioshow[i]
  print ""
  for (k in term) { tcount[term[k]]++ }
  printf "  terminal states by label:"
  for (k in tcount) printf "  %s=%d", k, tcount[k]
  print ""
  print "-------------------------------------------------------------"
}
```

---

## Appendix B: documentation and prompt staleness the recommended mechanism would create

Inventoried per the brief's documentation-impact requirement. This design pass itself changes only a planning record, so nothing is stale now.

- `AGENTS.md`, `pack/AGENTS.md` and `.agents/AGENTS.reference.md`, the Convergence and Accept sections, because acceptance would cease to be an uncounted single pass.
- `pack/prompts/triager.md` and `.agents/prompts/triager.md`, which would gain the scope ruling and the rule that an out-of-scope ruling at `high` or above takes the backstop re-check.
- `pack/prompts/reviewer.md` and `.agents/prompts/reviewer.md`, which would gain the requirement to cite a frozen obligation id.
- `pack/prompts/orchestrator.md` and `.agents/prompts/orchestrator.md`, for the terminal menu and the freeze point.
- `pack/prompts/planner.md` and `.agents/prompts/planner.md`, because the planner would author the frozen obligation set.
- `pack/instrument.md`, for the new record fields and the terminal record.
- `pack/LEDGER.template.md` and `.agents/LEDGER.template.md`, for the spend line.
- `pack/plan-template.plan.toml` and `pack/plan-template.success-criteria.md`, for the obligation rows.
- `.agents/workflow.toml` and `pack/workflow.toml`, and the `src/workflow_spec.rs` comments that currently call the cap and the backstop advisory.
- `README.md`, whose cap-labelled diagram must remain value-free and become budget-accurate.
- `CHANGELOG.md`, recording that a previously valid tree may now fail.
- `docs/plans/agent-scaffold.steps/review-loop-foreclosure-enforcement.md` and `workflow-driver-typed-fleet.md`, whose `SinglePass` contract states that acceptance has no round count for cap purposes and would need a reviewed contract migration.
