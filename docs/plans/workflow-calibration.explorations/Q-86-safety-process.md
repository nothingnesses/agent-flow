# Q-86: a safe bounded review process

## Prototype status after the capped synthesis review

Q-88 supersedes this proposal's proof-before-choice boundary. Q-86 later selected `B - Frozen obligations with sealed phase campaigns`, which maps to this proposal's M2 plus the state-machine proposal's sealed plan-review authority envelope. Q-91 selected floor `high`. The architecture descriptions and algebraic bounds remain design inputs, but the executable controller and replay scripts are adversarial prototypes rather than recommendation-eligibility proofs. Every later statement that calls the checker corrected or exhaustive, reports zero violations, or treats a run as establishing a safety property records the prototype's historical self-assessment and is not a current assurance claim. The round-5 triage at `docs/plans/agent-scaffold.reviews/q86-synthesis-r5-triage.md` demonstrates unsound arbitrary-finite composition, cross-family serious carry, scope and dismissal products, global family identity, and fresh-evidence handling. Selected Option B now requires the separate complete executable `bounded-convergence-option-b-proof` unit before implementation, and it must close every applicable Q-86 triage finding.

Explorer proposal for `Q-86`, written under a safety, human-process, finding-lineage and reviewer-allocation lens. Advisory design notes only. This document changes no workflow rule, no constant, no status and no code. Production implementation remains blocked on `bounded-convergence-option-b-proof` reaching `complete`, directly converging at its declared risky bar, carrying no step or increment convergence waiver, and receiving a later separate implementation decision. The future typed `complete-only-unwaived` dependency and its scheduler/validation enforcement are planned in `workflow-ready-frontier-scheduler`; `skipped`, every other non-complete state, roundless or below-streak `complete`, and waiver-backed `complete` remain blocking, and no production unit is added here.

The original exploration ran in worktree `.agents/worktrees/q86-explorer-safety`, branch `explore/q86-safety`, from `05142309`. The retained prototype no longer depends on that scratch directory. Appendix A points to the durable controller and replay artefacts and gives exact reproduction commands and historical outputs.

Evidence and recommendation are kept apart on purpose. Sections 1 and 2 are measurement. Sections 3 to 9 are design. Section 10 is the only place this proposal made its historical recommendation.

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

The disproof is parametric rather than sampled. Run:

```sh
for n in 1 2 10 100
do
    awk -v n="$n" 'BEGIN { print "resume_windows=" n, "review_rounds=" 5 * n, "state=active_after_resume" }'
    awk -v n="$n" 'BEGIN { print "acceptance_passes=" n, "repairs=" n, "state=awaiting_later_acceptance" }'
done
```

The values demonstrate the construction. The proof accepts every positive integer `n`, so no finite upper value exists.

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

**Non-resettability, and the anti-laundering rule.** No human resume, rename, new artefact identity, replan, or narrowing replenishes authority in a live family. The proposed controllers have no active transition named resume. Resume reconstructs the same state. Replan is a terminal non-delivery disposition and a materially different successor requires a new human receipt.

Section 3.4 handles the harder version of this question, which is whether the terminal choices smuggle the unbounded work back in.

### 3.2 Finding identity and lineage

A finding receives a **stable id at the moment a reviewer raises it**, scoped to the task and never reused. A controller carries the complete finite map from stable id to owner, severity, disposition, origin, and optional parent id. That map survives triage, repair, later rounds and later acceptance passes. Duplicate reports of one defect by two reviewers **merge onto one id** and debit nothing extra, which preserves the existing convention that per-reviewer valid counts may exceed the deduplicated round total. The full severity scale is `low`, `medium`, `high`, and `critical`.

One triaged batch is an atomic finite map from affected obligation owner to finding submap, plus a finite unowned set and one scheduled primary owner. Each entry carries its triage disposition, discovery phase, and canonical owner phase, so one batch may retain both a valid finding and a dismissed high or critical report across current and out-of-phase owners. Its reducer retains every affected finding and advances the initial attempt of only the scheduled primary owner. An absent or finding-bearing non-primary owner remains uncredited until its own scheduled initial batch; a batch cannot satisfy several initial attempts. `Open` and `AwaitingDismissalRecheck` remain distinct components. The attached re-check runs before a new repair without debiting authority. Upheld and overturned continuations preserve the valid repair component through normal progression and authority exhaustion. One joint repair moves the complete selected open set for one owner attempt to pending verification. Its named joint verification resolves the complete set, conservatively fails the complete set back to open, or leaves parents open while adding stable fix-induced children. A partial verification is failure unless every selected finding has named successful evidence. Completion and delivery quantify over the product of the complete map and every obligation state, so an unrelated result cannot replace an open parent or critical or close an affected owner.

Four lineages, kept strictly separate from severity.

- **`pre-existing`.** Present before this task's work. It counts fully against the stopping gate, because it is a real defect in the delivered artifact. The external experiment's blind R5 found six such defects that two informed reviews had missed, so a mechanism that discounted them would systematically miss what blind review is for.
- **`fix-induced`.** Introduced by a prior repair pass in this task. It counts fully. `calibration-analysis.md` measured 20 of 22 recorded injections as `class = prose`, and the 2026-08-13 audit measured self-reference at 49 per cent strict across 189 findings, so this lineage is the largest single population and discounting it would be the most consequential error available.
- **`scope-expanded`.** Not a violation of any frozen obligation. A low routes to a backlog obligation set for a future task. A medium routes to the terminal human scope decision. A proposed high or critical ruling first takes independent scope re-check. An upheld high then routes to the terminal human scope decision, while an overturned high returns in scope. A critical is always safety-blocking, so either re-check result enters `SeriousBlocked`. None enlarges the current family, and each debits the pass it arrived in because the pass ran.
- **`relitigated`.** An id already settled, re-raised without new evidence. The existing ledger rule dismisses it. It does not reopen an obligation and does not reset a streak.

**Reopening a settled finding** requires materially new evidence that beats the recorded verdict, in the existing `AGENTS.md` sense. A reopen consumes one of a per-finding allowance rather than being free, which is what makes section 5's bound finite.

**Severity is orthogonal to lineage.** A `pre-existing` critical and a `fix-induced` critical are both critical. A `scope-expanded` low is a backlog candidate. The two axes are recorded separately and neither is derived from the other.

### 3.3 The frozen rubric and the scope firewall

**When it freezes.** The acceptance rubric freezes when the plan review converges, before the first implementation step begins.

**Which durable sources define it.** The first implementation creates canonical finite `[[obligation]]` rows in the plan TOML. `O` is exactly those rows and is never inferred from prose. Each row has a stable id, one exact phase owner, a body reference or structured statement, and one source label from the closed enum `success_criterion`, `project_principle`, or `documentation_impact`. A principle label joins one numbered principle row. A documentation-impact label joins one Roadmap step. A success-criterion row is projected into the Success Criteria prose. Validation rejects duplicate ids, unknown labels, missing joins, missing owners, and digest changes after freeze. This restores the intended three-source boundary while making cardinality and membership mechanically enumerable.

**The distinguishing test.** A finding with a cited frozen obligation id follows the routine B-owned path. A finding is a **scope expansion** if the artefact can satisfy every frozen obligation without the proposed new capability, platform, quality threshold, or taste preference. A genuine violation of the common frozen invariant, boundary, or duty that no B obligation owns becomes `UnownedInScopeFinding(FindingId)`. That typed state blocks completion and routes to the human. It never defaults to backlog. This preserves the always-in-scope critical rule without pretending that the closed obligation source is complete.

**Three anti-abuse rules, because the firewall is the most abusable component here.**

- **An out-of-scope ruling on a `high` or above is treated exactly like a dismissal and takes the same independent backstop re-check.** An upheld high goes to the terminal human scope decision rather than backlog, and an overturned high returns in scope. This composes with the existing backstop rather than bypassing it.
- **A `critical` is always safety-blocking, regardless of whether it cites a frozen obligation.** A proposed out-of-scope label still takes independent re-check as an abuse control, but either result enters `SeriousBlocked` rather than backlog or delivery. Severity overrides the firewall at the top of the scale. This is the safety floor, and section 7 shows it is what makes the unresolved-critical invariant hold.
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
- The successor must carry a structured obligation or exclusion delta from the immutable predecessor, and the human receipt must attest that the delta is material.
- The successor id must be fresh against the predecessor id and every id in its ordered ancestry registry. The successor ancestry is exactly the predecessor ancestry followed by the predecessor id.
- Each replan writes a `decision` receipt bound to the exact predecessor and successor ids, both ancestry snapshots, both canonical scope digests, every presented option, the chosen successor, the predecessor spend snapshot, and the complete carried finding map.
- The successor preserves predecessor spend as lineage and names the new human receipt as the origin of its own authority. It cannot reinterpret predecessor spend as fresh authority.

This materially-different rule is the selected synthesis rule. The stricter proper-subset-or-disjoint rule is retained only as an unselected proposal alternative. No chain bound is claimed across materially different families. The finite controller and call bounds apply per immutable family. Validation rejects predecessor mutation, unchanged or reordered scope, a missing option set, wrong family or digest bindings, a missing carried finding, mismatched predecessor spend, and copied predecessor spend presented as fresh authority.

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

**A correction to the already-raised severity-trajectory candidate.** A trajectory predicate describes each pass's novel findings, while the safety invariant describes the open finding set across passes. A critical opened on one pass and never repaired remains open even if later passes contain only lows or no novel findings. The old proxy's count of twenty witnesses is withdrawn with that proxy. The logical counterexample remains. Any future M3 controller must retain explicit finding dispositions and require an empty serious open set in addition to its trajectory predicate before it can return to recommendation eligibility.

---

## 4. Mechanism M1: the sealed task budget

**The non-resettable task-budget design the brief requires.**

A task opens with an authorised budget `B = (Bp, Bw, Ba)` in review units. Rounds and acceptance passes debit per section 3.1. The terminal predicate is the existing consecutive-clean streak, scaled by risk class exactly as today. A loop converges at its required streak provided the complete finding map is settled and no serious dismissal is awaiting its re-check. Only a triage-valid high or critical, or an overturned serious dismissal, unlocks reserve. Referral to re-check does not unlock it, and an upheld dismissal preserves the prior reserve state. One remaining-clean-suffix calculation runs before every automatic review, repair, and verification. The controller forecloses before emitting the action when the remaining authorised path cannot attain the suffix. When any sub-budget reaches zero, the phase stops and the terminal menu is presented.

**A terminal severity floor `F`** governs which menu appears. With `F = critical`, `accept residual risk` and `narrow scope` are illegal only when a critical is open. With `F = high`, they are illegal when a high is open too. `F = critical` is the mandatory minimum. Section 7.1 shows the difference is large on the local data.

**What it is good at.** It bounds cost exactly and it is the smallest change from the current design, because the streak logic and the risk classes are untouched. **What it is bad at** is section 7.1.

---

## 5. Mechanism M2: frozen obligations with sealed phase campaigns

M2 is scope-bounded and count-bounded. Its plan review reuses M1's sealed controller unchanged. The inherited and still unapproved constants are five normal batches, two reserve batches, at most six grouped repairs, and reserve unlock only for a triage-valid high or critical or an overturned serious dismissal. Plan risk is declared once. The plan-review minimum `r_plan` is one clean batch at low risk and two consecutive clean batches at risky, with the complete map settled. The same remaining-clean-suffix foreclosure applies before any repair or review that can no longer attain completion. The maximum is seven batches. At convergence it freezes the canonical finite `O`, the set `P` of post-freeze phase identities, and one owner in `P` for every obligation. `P` contains each declared work loop and acceptance, so `p = m + 1`.

Each post-freeze phase has one `FrozenObligationCampaign(phase_id, scope_digest, obligations, findings, closure, spend, terminal)`. The `findings` field is the complete stable map, not a scalar. Each finding stores separate `discovery_phase` and `canonical_owner_phase` identities and a route derived from their positions in the frozen phase order. Within one phase, each obligation id is a schedulable owner key, distinct from its canonical phase identity. Each review reduction consumes an atomic finite owner map plus an unowned set and names one scheduled obligation owner. It retains every affected finding, but advances the initial attempt of only that scheduled owner; every other untested owner remains `Untested` until its own scheduled batch. An obligation has `Untested`, `OpenInitial(FindingMap)`, `InitialRepairPendingVerification(FindingMap)`, `Closed(reopen_unused)`, `OpenReopened(FindingMap)`, `ReopenRepairPendingVerification(FindingMap)`, and `Closed(reopen_used)` states. Initial review, initial verification, materially-new-evidence reopen discovery, and reopened verification each consume at most one review batch. One joint repair covers every owned finding in that attempt and consumes no review batch. Only named joint verification of the complete set closes it. A failed parent set or fix-induced child enters the terminal decision or serious block instead of creating another automatic attempt. Relitigation without new evidence cannot reopen. A dismissed high or critical uses the attached independent re-check.

Every obligation receives its scheduled initial attempt before any closed obligation may spend optional reopen authority. A cross-owner report against a closed owner in the current phase is retained as `DeferredReopen` with stable identity. An upheld incidental dismissal returns to `Closed(reopen_unused)`, while a valid or overturned report remains deferred. No active state may combine an `Untested` obligation with `OpenReopened`, reopened pending verification, or `Closed(reopen_used)`. Deferred work activates only after all initial attempts finish.

The phase route is explicit. A current-owner finding remains in the current campaign. A finding discovered after its canonical owner's campaign completed remains live under that immutable prior owner, with no authority transfer, reopening, or replenishment, and immediately routes the family to terminal non-delivery or receipted replan. A future-owner finding remains live without spend or initial credit until that campaign is scheduled. An unowned finding remains `UnownedInScopeFinding`. Thus acceptance-to-completed-work, early-work-to-future-owner, and atomic mixed current/prior/future/unowned products all have typed outcomes.

When every obligation and pre-closure current-owner component in one phase is settled, its non-transferable `BlindClosureDiscovery(phase_id)` stage runs one atomic triaged discovery batch. Closure is not awarded merely because the batch ran. Each component retains the full `OwnerRoute x ScopeDisposition x TriageDisposition` product under one stable finding id; no precedence shortcut or scalar state may discard an axis.

The scope disposition is complete. An in-scope triage-valid finding proceeds to its owner route. A low scope expansion becomes `ScopeBacklog` without current-family authority. A medium becomes `TerminalScopeDecision`. A high enters `AwaitingScopeRecheck`, which keeps closure pending; upheld goes to `TerminalScopeDecision`, while overturned returns the exact finding in scope and then takes its applicable current-, completed-prior-, future-, or unowned route. A critical also keeps closure pending while its scope re-check runs, but either upheld or overturned becomes `SeriousBlocked` regardless of owner or dismissal outcome.

The dismissal disposition composes rather than competes with that scope state. A high-or-critical dismissal enters `AwaitingDismissalRecheck` and keeps closure pending. If scope and dismissal re-checks are both pending, both per-id results must settle; resolving either one cannot clear the other or any sibling. An upheld dismissal settles only that axis and creates no owner component. An overturned dismissal makes the exact report triage-valid and follows its scope state: an in-scope or scope-overturned high takes its owner route, low remains backlog, medium or scope-upheld high remains a terminal scope decision, and critical remains `SeriousBlocked`.

The owner route then has these outcomes only for an admitted live in-scope finding:

- A current-owner finding becomes `ClosureCurrentOwnerBlock`. The only closure batch cannot serve as evidence about a later repair, so no automatic post-closure repair can lead to delivery; only terminal non-delivery or receipted replan remains.
- A completed-prior-owner finding remains live under the immutable prior owner and stays non-delivering, with only terminal non-delivery or receipted replan.
- A future-owner finding becomes `FutureOwnerPending`. The discovering phase may complete without spending or activating it; it remains live through intervening phases, activates only in its canonical campaign, and that later campaign supplies its own blind-closure discovery after the component settles.
- An unowned finding remains `UnownedInScopeFinding` and non-delivering; a serious case also takes the selected serious block.

After that phase's own obligations, current-owner components, and closure stage settle, the phase may complete while the family retains `FutureOwnerPending` components for later canonical campaigns. Those components remain live across the discovering phase and any intervening phase completions; phase completion cannot activate, resolve, drop, or spend them. The no-live-prior-or-future-route condition applies only to family delivery and construction of `Complete`, never to phase completion. Current-owner closure findings cannot deliver on stale closure evidence, while completed-prior and unowned closure routes remain non-delivering. A changed scope digest terminally replans the family, carries open findings, preserves old `O`, and requires the selected immutable-predecessor, receipt, and structured material scope-delta controls before a successor can review changed scope.

The selected proof's early-work fixture must close the discovering phase and an intervening phase while preserving the unchanged `FutureOwnerPending` identity, then activate it only when its canonical campaign is scheduled. Its paired mutations must fail if the pending route deadlocks phase completion, activates or disappears early, or permits family delivery before settlement. The completed-prior-owner fixture remains terminal and cannot be weakened into the future-owner continuation.

Blind-closure fixtures separately cover a valid current-owner finding, upheld and overturned current-owner serious dismissals, valid completed-prior and unowned findings, and a future-owner finding that survives the discovering phase and settles in its later campaign before that campaign's own closure. They also cover low backlog, medium terminal scope decision, high pending/upheld/overturned scope re-check with the overturned identity taking each applicable owner route, and critical `SeriousBlocked` after both scope outcomes. Atomic products include a scope referral plus a dismissal referral in one batch, every legal same-id scope/dismissal pair, simultaneous pending scope and dismissal re-checks, two scope referrals, and high plus critical outcomes. Killing mutations must reject post-closure repair followed by delivery on stale evidence, a skipped or misrouted serious-dismissal or scope re-check, either pending re-check counted as closure evidence, one re-check clearing the other, low owner fabrication, medium or upheld-high delivery, loss or misrouting of an overturned high before owner routing, critical escape from `SeriousBlocked`, atomic product erasure, accidental terminalisation or loss of the future component, premature activation or family delivery, delivery from prior or unowned routes, and completion without settled closure evidence.

For `n_q` obligations owned by phase `q`, the sealed allocation is `C_q = 4n_q + 1`. The final one is a minimum blind review even when `n_q = 0`. Freeze rejects a missing owner, duplicate owner, owner outside `P`, or mismatched allocation. Summing the phase partitions and adding plan review gives:

```text
R_M2 = 7 + sum(4n_q + 1)
     = 7 + 4|O| + p
     = 4|O| + m + 8
```

This proposed algebraic bound replaces `2|O| + 8`. One grouped repair per attempt leaves at most six plan repairs and at most two repairs per obligation, so the safe automated-agent upper bound remains `18|O| + 4m + 38`.

On an ordinarily delivering path that eventually constructs family `Complete`, a clean post-freeze phase has the unavoidable minimum `n_q + 1`, one scheduled initial-attempt batch per obligation plus blind closure. This phase minimum presupposes a valid freeze and exact ownership, a scheduled phase whose own obligations and blind closure settle, and no terminal or non-delivery transition before that closure; it still permits a `FutureOwnerPending` component that a later canonical campaign settles before family delivery. Atomic cross-owner retention cannot reduce that minimum because a non-scheduled owner receives no initial credit. The typed phase routes add no review authority: a completed-prior-owner route leaves the minimum domain by terminating delivery, and a future-owner route waits for its already-counted campaign. Therefore `C_q = 4n_q + 1` and the whole-family extrema remain unchanged. If `r_plan` is the inherited M1-controller plan-review minimum, the whole-family minimum over ordinarily delivering `Complete` paths with valid sealed review and freeze, all `p` phases scheduled and closed, and every delivery predicate settled is `r_plan + |O| + p = r_plan + |O| + m + 1` review batches and twice that number of reviewer calls. Legal early terminal and other non-delivery paths are outside both minimum domains and may stop earlier; the selected proof must test them separately rather than apply either minimum to them. A and C have cardinality-independent phase minima of one or two batches. `|O|` is a future frozen-row count, not a current prose-bullet count.

An active legacy task with no prospective `O` is the explicit `LegacyNoRubric` variant. It is historical and exempt from M2's obligation predicate, but it cannot enter a work or acceptance campaign with undefined authority. Its only paths are terminal preservation of a pinned legacy disposition, or a receipted new prospective plan review and freeze before B. The controller rejects direct `LegacyNoRubric -> FrozenObligationCampaign`, historical-round closure credit, and reinterpretation as a zero-obligation campaign.

M2 stops on verified complete-map and scope closure without reading historical outcome arrays. Its costs are canonical obligation authoring, cardinality-dependent clean review volume, completeness risk, and a terminal replan whenever structured frozen scope changes.

---

## 6. Mechanism M3: the severity-decay gate with a reserved blind pass

**Evidence-driven termination with a non-resettable ceiling as the backstop.**

Terminate when, for `k` consecutive passes, the maximum severity of **novel in-scope** valid findings is at or below a threshold `T`, the novel in-scope count is non-increasing, **no critical is open and no high dismissal awaits its re-check**, and at least one pass in the streak was **blind**. A non-resettable task ceiling `C3` bounds the process if the trajectory never decays.

`novel in-scope` excludes `relitigated` and `scope-expanded` per section 3.2, and includes `pre-existing` and `fix-induced` in full.

**What it is good at.** It is the only candidate whose terminal predicate reads the quantity that actually decayed in section 1.1, and it stops earlier than a count budget on a decaying sequence without stopping at all on a rising one. **What it is bad at** is that it reads `severities`, and section 1.5 shows the sibling fields of that record are demonstrably lossy.

---

## 7. EVIDENCE: proposed stopping bounds and adversarial prototype controls

### 7.1 Replay over the live Q-78 acceptance sequence

The selector in section 1.1 derives the sequence from the append-only log. The M1 and M3 tables apply their stated arithmetic to that selected sequence. The retained M2 replay has its own durable command below because its scope-digest assumptions are decision-material.

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

**Conditional M2 scope replay over all ten passes.** `docs/plans/workflow-calibration.explorations/q86-q78-scope-replay.sh` reads only task, phase, and artefact descriptions. It counts the first observation of each stable Q-58/Q-82, Q-83, Q-85/Q-86, and Q-87 fold identity. A repeated mention of Q-87 remains context within the same fold identity and does not mint another family. Historical records have no canonical B obligation rows or digests, so the mapping from each named fold to a material digest change is an explicit assumption. Under those four assumptions, passes 2, 4, 7, and 8 terminally replan, carry open findings, and require new receipts plus plan review and freeze before successor F2, F3, F4, or F5. The conditional result is ten passes across five families, four terminal replans, four additional receipts, and four additional plan-review and freeze campaigns. If a fold would not change canonical obligations or exclusions, its associated replan and cost disappear.

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

### 7.2 Adversarial transition prototype

The prior `statemachine.awk` result is withdrawn. Its M2 branch was a four-unit proxy without initial-attempt, repair, verification, reopen, phase, or blind-closure state. It did not derive the claimed bound. The retained adversarial prototype is `docs/plans/workflow-calibration.explorations/q86-controller-proof.py`.

Mode B is the retained prototype of the post-freeze `FrozenObligationCampaign` in section 5, not the selected proof. It keeps immutable phase identity, obligation stages, review spend, and a complete finite stable finding map. Mode A and mode C use the same map. One B batch is an atomic finite owner map plus unowned set. The sweep reaches same-owner and cross-owner low plus critical, mixed owned and unowned findings, and a parent plus fix-induced child. Joint repair and verification operate on the complete selected key set, and delivery universally quantifies over the map and obligations. Its reducer can award finding-bearing initial credit to several affected owners in one batch and its owner-state check forbids retaining a finding against an untested owner. Those prototype behaviours contradict scheduled-owner-only credit and future-owner retention, so the retained run does not establish `L_q = n_q + 1` or the selected phase routes.

Run the all-mode and B-sweep commands as adversarial evidence about the retained prototype. The output reports zero for the counters the prototype implements at both floors, but round 5 demonstrated that those counters omit required state products and cross-family behaviour. The current retained file's SHA-256 is `8a349c68dbe18df43d1d60d4110e11b3e216d97cdf4efb9f7e7328693d668175`.

The finite sweep caps the complete retained finding map at cardinality two. The earlier arbitrary-finite extension argument is withdrawn. Settled identities consume that cap and remove later fresh-finding, reopen, scope, and delivery transitions, so adding a component can make completion easier. A selected-option proof must separate finite batch-interaction coverage from arbitrary persistent history or establish another sound quotient and induction.

The proposed B family formula remains algebraic rather than a multi-phase enumeration. Each obligation is designed to have at most four review-consuming transitions, each post-freeze phase one blind-closure transition, and exact ownership no transfer. Under those unproved premises the post-freeze maxima sum to `4|O| + p`, and adding the proposed seven-batch plan campaign gives `4|O| + m + 8`. A selected B proof of concept must establish every premise before the formula can govern implementation.

M1's retained prototype controller is mode A in the same script. M3 remains outside the option set because its conceptual bound still needs a disposition controller and trustworthy prospective trajectory data.

### 7.3 Every required red-control path

| Path | M1 | Corrected M2 | M3 status. |
| --- | --- | --- | --- |
| **Repeated human resume** | Resume reconstructs spend and every phase ends by batch seven. | Resume reconstructs one immutable phase campaign. Bound `4n_q + 1`. | Excluded pending a corrected controller and instrumentation. |
| **Unbounded acceptance-repair sequence** | Every acceptance pass debits its slice and the final finding map is terminal. | Each obligation has at most one initial and one reopened grouped repair. Blind closure is an explicit discovery stage: a current-owner finding cannot repair and deliver on stale closure evidence; prior and unowned routes stay non-delivering; a future-owner component remains pending for its canonical later campaign and that campaign's own closure; upheld and overturned serious dismissals follow the explicit re-check routes. | Excluded. |
| **Multiple findings and dispositions in one batch** | The full map persists, including low plus critical, valid plus dismissed serious, and parent plus child. Both dismissal outcomes retain the repair component through exhaustion. | The atomic map retains same-owner, cross-owner, owned-plus-unowned, blind-closure, valid-plus-dismissed-serious, and scope-plus-dismissal products while advancing only the scheduled owner's initial attempt. Closure stays pending for either re-check, and one result cannot clear the other. | Excluded. |
| **Fix-induced high near exhaustion** | It consumes authorised verification and unlocks only unspent reserve. | Verification failure or a fix-induced child enters the terminal decision or serious block. | Excluded. |
| **Upheld serious dismissal** | It preserves the prior reserve state and cannot unlock reserve by itself. | It settles only through the attached re-check. | Excluded. |
| **Scope-expanded low at blind closure** | It is backlogged and cannot enlarge frozen scope. | It becomes `ScopeBacklog`, creates no owner authority, and cannot add an obligation. | Excluded. |
| **Scope-expanded medium at blind closure** | It enters the terminal human scope decision. | It becomes `TerminalScopeDecision` and cannot count as delivering closure evidence. | Excluded. |
| **Scope-expanded high at blind closure** | It takes independent scope re-check. Upheld goes to the terminal human scope decision and overturned returns in scope. | Closure remains pending; upheld becomes `TerminalScopeDecision`, while overturned takes the exact applicable owner route after any dismissal re-check settles. | Excluded. |
| **Scope-expanded critical at blind closure** | It takes independent scope re-check, but either result is `SeriousBlocked`. | Closure remains pending through re-check and both results are `SeriousBlocked` for every owner/dismissal product. | Excluded. |
| **Unowned in-scope critical** | The common map blocks delivery. | `UnownedInScopeFinding` enters `SeriousBlocked` and cannot complete or deliver residual. | Excluded. |
| **Relitigation without new evidence** | It preserves disposition and cannot reset spend. | It cannot take `MateriallyNewEvidence` or consume reopen authority. | Excluded. |
| **LegacyNoRubric** | Prospective adoption remains separate. | It terminally preserves legacy disposition or enters new prospective plan review and freeze, with no direct campaign, old-round credit, or zero-obligation reinterpretation. | Excluded. |
| **Narrowing or replan** | The family is terminal and no slice returns. | The family is terminal. A successor requires immutable predecessor, receipt, and structured material scope delta. | Excluded. |
| **Unresolved critical at exhaustion** | Delivery is unconstructible for the complete map. | Delivery is unconstructible at both floors for the complete map. | Excluded. |
| **Blind closure** | Every batch contains a blind seat. | Every phase owns one non-transferable closure seat, including an empty prospective phase. | Excluded. |
| **Early-work future-owner route** | The complete map retains the finding without fabricating delivery. | The discovering and intervening phases may complete after their own closure while the component remains `FutureOwnerPending`; only its canonical phase activates it, and family `Complete` remains blocked until it settles. | Excluded. |

M1 and M2 retain proposed finite bounds or terminal events for every required path. The retained prototype does not establish all of them. M3 remains design input rather than an offered architecture because its trajectory data is not trustworthy.

---

## 8. DESIGN: the candidates against all eight Project Principles by name

| Principle | M1 sealed budget. | Corrected M2 frozen obligations. | M3 severity decay. |
| --- | --- | --- | --- |
| **Prefer the cleaner long-term architecture over the smallest diff** | Keeps streak and budget as two stopping concepts. | Uses one obligation campaign for scope, attempts, closure, ownership, and bound. | Keeps a trajectory predicate plus an outer ceiling. |
| **Minimal by default** | Smallest migration from current semantics. | Largest schema, and the clean minimum `n_q + 1` scales with obligation count. | Middle, but prospective trajectory evidence is also new. |
| **Safe on existing projects** | A digest boundary can charge old spend and fail loudly. | `LegacyNoRubric` is exempt from B rather than falsely failed, but cannot start B before a prospective freeze. | Historical missing severity must never be treated as safe evidence. |
| **Idempotent** | Resume reconstructs monotone spend. | Phase, obligation, attempt, and spend replay deterministically. | A sealed ceiling prevents reset. |
| **Make illegal states unrepresentable** | Complete finding maps remove scalar erasure. | Closed variants and `UnownedInScopeFinding` prevent unverified closure, second reopen, phase transfer, and post-terminal action. | Needs the same explicit disposition controller before returning to eligibility. |
| **Ground decisions in evidence** | Preserves the measured five-round boundary, but reserve values are weakly calibrated. | Targets observed scope movement, while the conditional Q-78 scenario exposes four possible replans under stated digest assumptions. | The historical trajectory fields are not trustworthy enough for a gate. |
| **Reproducible** | Fixed arithmetic with an adversarial finite prototype whose limits are explicit. | `4\|O\| + m + 8` is an algebraic proposal requiring a complete selected-option proof. | The old proxy is withdrawn. |
| **Structured data first, project for humans** | Accounts, findings, and receipts are structured. | Obligation rows, owners, attempts, findings, and receipts are structured. | Prospective finding and trajectory state would need structure. |

The baseline assessment remains at section 2.3.

---

## 9. DESIGN: migration and enforcement

Common production surfaces move only after the selected proof passes and the human separately authorises implementation. Advisory guidance describes judgement. Mechanical enforcement exits non-zero on illegal state.

| Surface | What moves. | Authority. |
| --- | --- | --- |
| `.agents/workflow.toml` and `pack/workflow.toml` | Chosen controller constants and the human-selected terminal floor. | Data consumed by enforcement. |
| `src/workflow_spec.rs` | `WorkflowSpec` fields and drift-guard tests. | Enforced by tests. |
| Shared `ReviewProcess` reconstruction | Task family, phase controller, frozen scope, finding disposition, terminal state, and acceptance campaign. `SinglePass` remains one observation and does not acquire streak or cap fields. | Enforced. |
| `src/workflow.rs` and `src/next.rs` | One reconstruction supplies validation and the permitted next action. | Enforced state with advisory projection. |
| Metrics schema | Prospective scope, finding, evidence, disposition, brief, spend or stage, re-check, and terminal events. | Enforced by validation. |
| Plan source | Family, attempt, scope, phase, adoption, terminal, and B obligation rows. | Enforced structured source. |
| Ledger | Narrative and resume pointer only. No terminal fact lives only in the ledger. | Advisory projection. |
| Append-only history | No event is rewritten. A typed digest boundary separates legacy history. B adds `LegacyNoRubric`. | Enforced and fail-closed. |
| Canonical and generated guidance | `pack/AGENTS.md`, `pack/instrument.md`, role prompts, ledger and plan templates, their dogfood copies, README, and changelog. | Advisory text generated or byte-guarded where applicable. |

For a selected M2 implementation, validation would need to enforce finite canonical obligation rows, exact source labels, one phase owner, distinct discovery and canonical-owner phases, current/prior/future routes, `C_q = 4|O_q| + 1`, scheduled-owner-only initial credit, no transfer or replenishment, all initial attempts before optional reopen work, deferred early and future finding identity, explicit blind-closure discovery with per-owner and serious-dismissal routes, no current-owner delivery on stale closure evidence, phase completion after its own obligations and closure despite a retained future-owner route, the future campaign's own later closure, no family delivery while any prior- or future-owner route remains live, non-delivering completed-prior and unowned routes, complete finding maps and triage disposition products, grouped repair before grouped verification, `UnownedInScopeFinding`, typed scope-recheck state, scope-digest terminality, explicit legacy adoption, and critical legality. Successor validation binds the immutable terminal predecessor, its ordered ancestry registry, a successor id fresh against that registry, exact successor ancestry, both scope digests, every presented option, the chosen successor, predecessor spend, the complete carried finding map, and a non-empty structured obligation or exclusion delta attested as material. `next` reports the exact obligation and complete blind or informed brief permitted by state. It cannot prove that a reviewer was genuinely blind or that a human judgement was true.

The selected proof has no dependency on `review-loop-foreclosure-enforcement` or production typed reconstruction because it is an isolated executable specification. Any later production work may reuse the reviewed reconstruction where the proof shows that reuse is sound. Acceptance remains a campaign around disjoint `SinglePass` observations rather than adding convergence fields to a single pass.

---

## 10. HISTORICAL RECOMMENDATION BEFORE Q-86

**Before Q-86 was decided, this proposal provisionally recommended M2, frozen obligations with sealed phase campaigns, at low confidence.**

That recommendation rested on the conceptual architecture rather than the broken prototype. M2 gave scope, ownership, disposition, phase authority, and completion one structured source. It was advice prepared for the human choice and did not establish implementation eligibility. Q-86 has since selected synthesised Option B, while the separate proof gate below remains the condition for any later implementation authority.

- It addressed prospective scope movement by making a changed structured scope digest terminal rather than silently enlarging the accepted target.
- It completed from triage-backed obligation state and complete stable finding maps rather than broken historical outcome or severity arrays.
- Its proposed algebraic bound followed from a closed finite `O`, exact phase owners, and no transfer: `4|O| + m + 8` review batches per family. Those premises remain to be proved for the selected controller.
- Its prototype had exposed concrete delivery, composition, scope, legacy, priority, ancestry, and successor proof obligations across five adversarial rounds. The selected B proof must close them before implementation.

The recommendation had substantial costs.

- Under the stated counterfactual digest assumptions, Q-78 would have required four terminal replans, four additional human receipts, four additional plan-review and freeze campaigns, and five task families before all ten reviewer passes could run.
- A clean B phase costs at least `n_q + 1`, so ordinary review volume scales with obligation count.
- Canonical obligation authoring is the largest schema and migration burden.
- An incomplete obligation set is a new safety risk that mechanical cardinality cannot eliminate.
- The one-reopen design and its operational adequacy have no prospective calibration.

The human selected synthesised Option B, which includes M2. The separate complete executable proof of concept must close every applicable valid Q-86 synthesis finding, including arbitrary finite maps, cross-owner and mixed products, cross-family serious carry, scope and dismissal products, global family identity, fresh evidence, legacy adoption, both terminal floors, every terminal choice, and every M2 transition and bound. If it fails, implementation remains blocked and the architecture decision returns to the human. No fallback architecture or floor is selected automatically.

Evidence that would overturn M2 includes frozen-scope tasks that still need long repair sequences, systematic uncited genuine defects, any serious finding routed to backlog, or prospective evidence that M1 preserves materially more unique serious findings for acceptable cost. A change to the reopen count requires a new finite prospective value and cannot replenish a live campaign.

This historical recommendation did not claim that Q-78 diverged, that named folds caused later findings, that those folds certainly changed a counterfactual B digest, or that the evidence estimated a population rate.

---

## 11. YAGNI boundary

- Do not build a general issue tracker, project-wide defect database, mutable rubric editor, or autonomous obligation extractor.
- Do not build an autonomous risk, scope, severity, or residual-risk judge.
- Do not build probabilistic stopping, dynamic pricing, transferable credits, a reviewer marketplace, or a model optimiser.
- Do not rewrite or infer historical finding lineage, obligation membership, stage, or closure.
- Do not build a persistent workflow service, general workflow language, or new scheduler beyond the planned typed fleet.
- Do not create authority from rename, rebuild, replan, narrowing, scope change, or human resume.
- Do not implement selected Option B or floor `high` until the proof passes and the human separately authorises production implementation.

---

## 12. The human decisions and proof authority

The synthesis presented only A, B, and C as viable bounded architectures. Q-86 records recommendation and chosen value `B - Frozen obligations with sealed phase campaigns`. M3 remains excluded. Every controller constant remains unapproved, including the five-normal-plus-two-reserve slice inherited by selected B plan review and B's one reopen.

Q-91 records the serious-floor options `high`, `critical`, and `defer`, with recommendation and chosen value `high`. Ordinary residual acceptance and ordinary narrowing are unavailable while a high or critical is open. The selected proof models `critical` as a comparison so its residual-high difference remains executable.

At least one blind closure pass is structural in selected Option B. Instrument repair is required before any outcome or trajectory field becomes load-bearing, but the proof proceeds from prospective complete finding maps without waiting for a historical rewrite.

Q-85 decided only where this investigation belongs. Q-86 and Q-91 authorise only `bounded-convergence-option-b-proof`. Its gate is unwaived complete-only: a future production unit must use the typed `complete-only-unwaived` blocker policy planned in `workflow-ready-frontier-scheduler`, whose red controls keep that unit blocked when the proof is `skipped` or in any other non-`complete` status, lacks round-backed risky convergence, or carries a self-declared or record-backed step or increment convergence waiver, while ordinary blocker and generic waiver semantics remain unchanged. No production implementation is approved and no production unit exists.

---

## Appendix A: retained adversarial prototype and replay

### A.1 Controller prototype

The retained adversarial prototype is `docs/plans/workflow-calibration.explorations/q86-controller-proof.py`. Mode A exercises M1. Mode B exercises the proposed M2. Mode C exercises the fixed-depth synthesis option. Run from the repository root:

```sh
CHECKER=docs/plans/workflow-calibration.explorations/q86-controller-proof.py
export PYTHONDONTWRITEBYTECODE=1
nix shell --inputs-from . nixpkgs#python3 -c python3 "$CHECKER" --mode all --phase acceptance --risk risky --obligations 2 --floor high
nix shell --inputs-from . nixpkgs#python3 -c python3 "$CHECKER" --mode all --phase acceptance --risk risky --obligations 2 --floor critical
nix shell --inputs-from . nixpkgs#python3 -c python3 "$CHECKER" --mode A --phase plan_review --risk low_risk --floor high
nix shell --inputs-from . nixpkgs#python3 -c python3 "$CHECKER" --mode A --phase plan_review --risk risky --floor high
nix shell --inputs-from . nixpkgs#python3 -c python3 "$CHECKER" --mode A --phase work_review --risk risky --floor high
nix shell --inputs-from . nixpkgs#python3 -c python3 "$CHECKER" --mode C --phase acceptance --risk low_risk --floor high
for n in 0 1 2 3
do
    nix shell --inputs-from . nixpkgs#python3 -c python3 "$CHECKER" --mode B --phase work:example --obligations "$n" --floor high
done
sha256sum "$CHECKER"
```

The synthesis no longer retains a large exact stdout block. Run the commands below to reproduce the prototype's current output. Its zero-valued counters describe only implemented checks and do not show that all required controls passed. The B sweep declares design bounds `1`, `5`, `9`, and `13`, reaches smaller maxima under the retained-map cap in some cases, and reports clean minimums `1`, `2`, `3`, and `4`. The earlier arbitrary finite-map conclusion is withdrawn. The current retained checker SHA-256 is `8a349c68dbe18df43d1d60d4110e11b3e216d97cdf4efb9f7e7328693d668175`. Before the required in-file prototype caveat was added, the checker at historical commit `ad989b5f` had SHA-256 `d0dabe6da04fde2009a2baf22d0a3d9fabdfbd6bc96d2859d26043531aff579a`; that historical digest does not identify the current retained file.

### A.2 Q-78 scope replay

The durable replay is `docs/plans/workflow-calibration.explorations/q86-q78-scope-replay.sh`. It reads only task, phase, and artefact descriptions. It does not use outcome or severity arrays.

```sh
docs/plans/workflow-calibration.explorations/q86-q78-scope-replay.sh docs/metrics/workflow.jsonl
docs/plans/workflow-calibration.explorations/q86-q78-scope-replay.sh --self-test
```

Its summary is:

```text
summary passes=10 observed_named_folds=4 assumed_digest_changes=4 conditional_terminal_replans=4 conditional_families=5 conditional_additional_human_receipts=4 conditional_additional_plan_review_and_freeze_cycles=4
self_test selected_passes=9 summary passes=9 observed_named_folds=4 assumed_digest_changes=4 conditional_terminal_replans=4 conditional_families=5 conditional_additional_human_receipts=4 conditional_additional_plan_review_and_freeze_cycles=4
self_test selected_passes=11 summary passes=11 observed_named_folds=4 assumed_digest_changes=4 conditional_terminal_replans=4 conditional_families=5 conditional_additional_human_receipts=4 conditional_additional_plan_review_and_freeze_cycles=4
```

The four distinct named fold identities are observed. The repeated Q-87 mention in the eleven-pass fixture remains the same fourth identity. Their four digest changes are explicitly assumed. Under those assumptions, passes 2, 4, 7, and 8 terminally replan, carry unresolved findings, and require successor families F2 through F5. Historical obligation results remain explicitly unreconstructible.

---

## Appendix B: documentation and prompt staleness the recommended mechanism would create

This repair changes planning and proof artefacts only, so shipped product documentation is not stale now. Choosing B would require later implementation work across these surfaces:

- Update `pack/AGENTS.md`, `AGENTS.md`, and `.agents/AGENTS.reference.md` because convergence and acceptance would use sealed campaigns.
- Update planner, orchestrator, reviewer, triager, and implementer prompts in canonical and generated locations for obligation authoring, phase ownership, scope rulings, repair verification, and terminal choices.
- Update `pack/instrument.md` for scope, obligation, finding, evidence, disposition, spend, re-check, and terminal events.
- Update plan and ledger templates for obligation rows, phase campaigns, `LegacyNoRubric`, and resume projections.
- Update `.agents/workflow.toml`, `pack/workflow.toml`, and `WorkflowSpec` for the chosen constants and floor.
- Update README for the non-resettable campaign and changelog for the adoption break.
- Reconcile `review-loop-foreclosure-enforcement.md` and `workflow-driver-typed-fleet.md` through the reviewed shared reconstruction while preserving disjoint `SinglePass` observations.
