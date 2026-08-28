# Q-86 synthesis round 1: REVIEWER, safety / adoption / evidence / human-choice lens

Independent reviewer. I did not author the synthesis and did not read another reviewer's worktree or findings file. Lens: whether a human can make the Q-86 decision safely from what this fold puts in front of them.

## Artifact and method

- Worktree `/home/jessea/Documents/projects/agent-scaffold/.agents/worktrees/q86-synthesis-r1-claude`, branch `review/q86-synthesis-r1-claude`, tip `77345e88`. Reviewed `git diff main..HEAD`: 5 files, 268 insertions, 9 deletions.
- Read in full: `AGENTS.md`, `.agents/prompts/reviewer.md`, `Q-86-convergence-mechanism-brief.md`, `Q-86-state-machine.md`, `Q-86-safety-process.md`, `Q-86-synthesis.md`, the `[[question]] Q-86` TOML entry and `agent-scaffold.questions/Q-86.md`, `agent-scaffold.steps/workflow-calibration.md`, and the generated projection `docs/plans/agent-scaffold.md`.
- Treated as `risky`, per the ledger's classification of this artifact. This is a decision-readiness review, not an implementation review.
- No review ledger of settled findings was handed to me, so nothing below is a re-raise.
- `cargo` is not on PATH in this box, so `render --check` and `validate --workflow` could not be run. I verified the projection by re-deriving it from the source instead (see PROOF COMMANDS below); every other claim rests on a `jq`/`grep`/`sed` command or a `file:line` citation.

## Findings

16 findings: 3 high, 6 medium, 7 low. No critical.

---

### CR-1 (high). Option B's obligation accounting is self-contradictory, so the recommended option's headline bound is unproved and the option may be unable to complete a task at all.

`Q-86-synthesis.md:126` defines the post-freeze controller:

> each obligation has its initial closure attempt and at most one prospective reopen, so `r = 1`. Every post-freeze review batch must settle one active obligation attempt, consume that obligation's one reopen after materially new evidence, or execute the one reserved blind closure batch. A batch that cannot make one of those typed transitions goes to the terminal decision rather than authoring more review.

`Q-86-synthesis.md:130` then constrains the reopen:

> A finding against a closed obligation can use its one reopen.

The two sentences do not describe the same machine, and the difference decides both the bound and whether the mechanism works.

- Reading 1, "reopen = the second closure attempt on an obligation that failed its first attempt". Then `|O| * (r + 1)` attempt-batches is right and `C_O = 2|O| + 1` follows. But it contradicts `:130` and the source rule at `Q-86-safety-process.md:234` ("Reopening a settled finding requires materially new evidence that beats the recorded verdict"), because a first-attempt failure is neither settled nor materially new evidence.
- Reading 2, taking `:130` literally: the reopen is only available against an *already closed* obligation. Then an obligation whose first attempt raises a valid finding is open, unmet, and has no further attempt allocated. It can never become `Met`, and `:130` makes `Met` or `AcceptedResidual` a completion requirement for every obligation. Under this reading no task in which any obligation fails one review can ever complete, and every such task goes terminal.

Neither explorer's exhaustive check covers this. `Q-86-safety-process.md:626-640` (`statemachine.awk`, `MECH=m2`) runs with `CAP = 4` and the streak predicate `nc >= REQ && noc == 0 && noh == 0 && nob == 0`; it never evaluates `C2 = |O| * (r + 1) + 1`. The synthesis concedes this at `:144` ("the safety proposal exhaustively checked the obligation controller, while the sealed outer ceiling supplies a direct finite fallback") but the fallback is not independent: `C_O` is computed from the same attempt count the ambiguity governs, so a wrong attempt rule makes the ceiling wrong by the same factor. The claim at `:220` that Option B's ceiling stops "malformed or stalled obligation progress" is therefore not defence in depth.

Consequence: `2|O| + 1` and `2|O| + 8` are the recommended option's central quantitative claims and they are carried verbatim into the human-facing ask (`docs/plans/agent-scaffold.plan.toml:2566`, projected at `docs/plans/agent-scaffold.md:179`). A human approving Option B is approving a bound derived from a rule the document states two incompatible ways, one of which makes the mechanism uncompletable.

Smallest safe correction: in `Q-86-synthesis.md`, state in one sentence how many closure attempts an obligation receives after a failing attempt, keep "attempt" and "reopen" as distinct named transitions, and either re-derive `C_O` from that stated rule or mark `2|O| + 1` as unproved pending the proof of concept `:228` already requires.

---

### CR-2 (high). The recommended option is never replayed against the Q-78 history that is its stated justification, and under its own rules that history would have been blocked or terminated four times.

The recommendation at `Q-86-synthesis.md:226` rests on the moving-scope diagnosis:

> The safety proposal is right that the local sequence grew a moving acceptance target ... It therefore addresses both the observed scope problem and the formal unbounded-path problem.

The diagnosis reproduces. Run from the repository root:

```sh
jq -r '[inputs] | map(select(.type == "round" and .task == "q78-design-pass" and .phase == "acceptance")) | to_entries[] | [ (.key + 1), .value.valid_findings, ( if (.value.artifact | test("\\bfold\\b|(after|and) Q-8[0-9]")) then "scope-added" else "-" end ), ( if (.value.artifact | test("expanded")) then "expanded" else "-" end ) ] | @tsv' -n docs/metrics/workflow.jsonl
```

Passes 2, 4, 7 and 8 add scope; passes 2 through 10 describe the target as expanded. Those four folds were Q-58/Q-82, Q-83, Q-85/Q-86 and Q-87 - human decisions the project had to record into the plan while the plan was the artifact under acceptance.

Now apply Option B to that history using only the synthesis's own text. The rubric "freezes after plan review and before implementation" (`:56`), and `validate --workflow` for Option B "mechanically enforces a finite frozen set ... [and] no scope mutation" (`:151`). Each of the four folds is therefore either (a) rejected as a scope mutation, or (b) admitted into the delivered artifact while sitting outside `O` - where nothing in `:130`'s completion predicate requires it to be reviewed at all, because completion is closure of `O`. Under `Q-86-state-machine.md:97` the same event ends the family. The synthesis nowhere states which of these Option B does.

Consequence: the single measured sequence the recommendation is built on is also the sequence on which Option B's adoption cost is largest, and the synthesis reports the diagnosis while omitting the consequence. A human choosing B is not told that on this project's own demonstrated working pattern B forces a terminal replan (or an unreviewed artifact) roughly every second acceptance pass. That is the difference between "B addresses the measured problem" and "B forbids the way this project measured it".

Smallest safe correction: add a short Option B replay over the ten Q-78 acceptance passes stating, for each of the four folds, which typed transition B takes and what the resulting durable state is, and carry that result into the TRADE-OFF SUMMARY at `docs/plans/agent-scaffold.plan.toml:2571`.

---

### CR-3 (high). Both explorers' per-option Q-78 replays - the only local measurement of what each option would fail to discover - are dropped, and the human-facing summary asserts a late-discovery ranking without them.

Both proposals produced directly comparable replay results, and the synthesis carries neither as a number.

- `Q-86-state-machine.md:221` and `:357`: Candidate A (= synthesis Option A) is "Terminal at pass seven with a medium finding"; Candidate B (= synthesis Option C) is "Terminal at pass three with a high finding".
- `Q-86-safety-process.md:345-352` tabulates the same thing as undiscovered defects. `Ba = 4` (Option C's acceptance depth of four batches, `Q-86-synthesis.md:169`, `:205`) stops at pass 4 with an open `high` and **17 valid shortfalls never discovered, worst never discovered `high`**. `Ba = 7` (Option A's five-plus-two, `:87`) stops at pass 7 with an open `medium` and **3 never discovered, worst `low`**. The arithmetic checks against the live log: cumulative shortfalls through pass 4 are 7+10+5+6 = 28 of 45, leaving 17; through pass 7, 42 of 45, leaving 3.

The synthesis retains one clause of this, buried in a principles-table cell for Option C (`:182`, "Q-78 would have escalated on pass three before its later decay"), and no number for A or B. Meanwhile the ask the human reads asserts a ranking:

> TRADE-OFF SUMMARY: Option A preserves the most bounded late discovery ... (`docs/plans/agent-scaffold.plan.toml:2571`, projected at `docs/plans/agent-scaffold.md:179`)

Consequence: the runner-level requirement that the options "preserve useful late defect discovery" is exactly the property these numbers measure, and they are the only local measurement of it that exists. Removing them leaves a comparative superlative resting on nothing, and hides that Option C would have terminated on a `high`-bearing pass with 17 real shortfalls unfound.

Smallest safe correction: add the two explorer replay lines (A: terminal pass 7, open medium, 3 undiscovered; C: terminal pass 4, open high, 17 undiscovered) to the red-control comparison table at `:202-211`, and either support or drop "the most bounded late discovery".

---

### CR-4 (medium). The serious terminal floor `F = high` is packaged into all three options and omitted from both the no-decision boundary and the human-facing ask, although the explorer that produced it named it a human-owned decision.

`Q-86-synthesis.md:65`:

> The first implementation uses `high` as the conservative serious terminal floor. This packages the safety proposal's local Q-78 control rather than asking the human to decide a second policy toggle.

`Q-86-safety-process.md:516-518` lists it as the first of "Three sub-decisions the human owns whichever option is chosen", and says of it: "This is a safety-appetite decision and is not derivable from the data."

The synthesis's own no-decision boundary at `:236` enumerates what is *not* approved - "The baseline, the excluded severity gate, the five-plus-two values of Option A, and the one-reopen value of Option B" - and `F` is absent from that list. The NO-DECISION BOUNDARY paragraph in the ask (`docs/plans/agent-scaffold.plan.toml:2573`) does not mention the floor either, and neither does `docs/plans/agent-scaffold.questions/Q-86.md`. By the synthesis's own construction, everything not named there is approved by the human's choice.

The floor is conservative, so this is not a safety hole; it is an undisclosed cost. At `F = high`, `Accept residual risk` and ordinary `Narrow scope` become illegal whenever any high is open (`:65`, `:69`, `:70`). On the measured Q-78 sequence that is passes 3 through 6 - four of ten - where the human would have been refused both options (`Q-86-safety-process.md:345-352`, last two columns).

Consequence: a low-confidence policy constant that an explorer explicitly reserved to the human is approved silently by any of the three choices, and the human is not shown the terminal-menu restriction it buys.

Smallest safe correction: add `the serious terminal floor of high` to the not-silently-approved list at `Q-86-synthesis.md:236` and to the NO-DECISION BOUNDARY paragraph of the ask, or surface it as a named sub-decision with its Q-78 cost.

---

### CR-5 (medium). Option B partitions its derived ceiling across every work loop and acceptance with no rule relating `|O|` to the number of loops, so an increment can receive one or zero review batches.

`Q-86-synthesis.md:128`:

> It is partitioned at freeze across declared work loops and acceptance, with no transfer and no later increase. ... Any exhausted sub-account reaches the terminal decision even when another sub-account has unused authority.

`C_O = 2|O| + 1` is a whole-task quantity, and the sub-accounts number `m + 1` (the `m` work loops of `:85` plus acceptance). Nothing constrains `|O|` relative to `m`. When `2|O| + 1 < m + 1` at least one sub-account receives zero batches; with the partition unspecified, even a comfortable total can allocate one batch to a step. A zero-batch sub-account is exhausted on creation, so by the sentence above the family goes terminal at that step before any reviewer runs.

Neither explorer proposed this. `Q-86-safety-process.md:317` keeps `C2` as a task-level ceiling; `Q-86-state-machine.md:155` partitions but guarantees seven batches to *every* declared loop. The synthesis introduced the partition and inherited neither guarantee.

Consequence: Option A guarantees 7 review batches per phase and Option C guarantees 4; the recommended option guarantees nothing, and can foreclose a step before it is reviewed once. This is not in the trade-off summary, which lists B's costs only as "the largest authoring and migration burden and risks an incomplete frozen set".

Smallest safe correction: state the partition rule and a per-sub-account minimum, or drop the partition and keep `C_O` task-level as `Q-86-safety-process.md:317` specified.

---

### CR-6 (medium). The frozen-rubric source was widened from three enumerated committed artifacts to an eight-category union, which inflates and de-mechanises `|O|` - the very quantity Option B's bound is derived from.

`Q-86-safety-process.md:242` fixes the source deliberately and narrowly:

> **Which durable artifacts define it.** Exactly three, and no others: the plan's Success Criteria sidecar ..., the plan's `[[principle]]` set, and each step sidecar's documentation-impact statement. All three are already committed, already single-sourced and already rendered, so the freeze adds a boundary rather than a new artifact.

`Q-86-synthesis.md:56` replaces this with a union of both proposals:

> Its structured source cites the plan's Success Criteria, numbered Project Principles, explicit invariants, security and trust boundaries, documentation-currency duties, exclusions, reviewed baseline, and step documentation-impact obligations.

Five of those eight categories are not enumerated as discrete rows anywhere in this plan today, so they must be authored at freeze. Option B is the only option whose bound is a function of `|O|`, so widening the source both grows the ceiling and makes it less mechanically derivable - while the risk the synthesis already names for B ("risks an incomplete frozen set", ask line 2571) is precisely the risk that grows with the number of categories a planner must enumerate by hand.

Consequence: `2|O| + 8` is presented to the human as Option B's bound, but `|O|` is unknowable at decision time and the synthesis has just enlarged the space it is drawn from. The human is asked to prefer B partly because "its bound is derived rather than chosen" while being unable to evaluate the derived value.

Smallest safe correction: either restore the three-source enumeration for the obligation set (keeping the wider list as scope-relevance guidance for reviewers rather than as obligation rows), or state an order-of-magnitude `|O|` for this plan so `2|O| + 8` becomes a number the human can weigh.

---

### CR-7 (medium). The severity-decay gate is excluded on an instrumentation ground the synthesis does not apply to its own serious floor, removing a mechanism the safety explorer proved viable.

`Q-86-synthesis.md:218` excludes it because "it makes severity instrumentation load-bearing when that instrumentation is incomplete and the sample is sparse."

But the shared safety package makes severity load-bearing in all three options. `:65`: "An open `high` or `critical`, or a pending high-or-critical dismissal re-check, prevents completion and prevents ordinary residual-risk acceptance." The serious floor is the synthesis's primary guarantee that no budget conceals a critical, and it is a severity predicate. If severity classification is too unreliable to gate stopping, it is too unreliable to gate completion; if it is reliable enough for the floor, the stated exclusion reason does not hold.

The excluded mechanism was eligible under the brief. `Q-86-safety-process.md:388` records `m3` with P1 BOUND `HOLDS` and P2 CRITICAL `HOLDS` over 38 reachable states, and `:416` states all three of that proposal's mechanisms meet the brief's eligibility condition. The exclusion is within the orchestrator's synthesis remit; the inconsistent justification is not.

Consequence: the human's option set is narrowed from four explorer-viable mechanisms to three on a rationale that, taken at face value, also undermines the safety property the remaining three depend on.

Smallest safe correction: one sentence at `:218` distinguishing prospective triage-assigned severity on a single finding (which the serious floor reads, and which `:59` already types) from the multi-pass historical `severities` trajectory the decay gate reads, and rest the exclusion on the missing trajectory history rather than on severity being load-bearing.

---

### CR-8 (medium). Stale Success Criterion: the plan still requires `workflow-calibration` to keep Q-86 `exploring` and to schedule the brief.

```sh
grep -n "keeps Q-86" docs/plans/agent-scaffold.success-criteria.md docs/plans/agent-scaffold.md
```

`docs/plans/agent-scaffold.success-criteria.md:41`, projected at `docs/plans/agent-scaffold.md:5111`:

> The in-progress `workflow-calibration` step records Q-85's decision and exact receipt, keeps Q-86 `exploring`, and schedules the tracked `docs/plans/workflow-calibration.explorations/Q-86-convergence-mechanism-brief.md` design pass with a later human decision required before any cap, acceptance, reset, pack, or code change.

This fold sets `status = "open"` (`docs/plans/agent-scaffold.plan.toml:2561`) and repoints the step from the brief to the synthesis (`docs/plans/agent-scaffold.steps/workflow-calibration.md:20`). The criterion is now false as written, and cannot be satisfied by the tree it measures.

This is not cosmetic in context: the synthesis's own shared safety package makes the plan's Success Criteria the first-named source of the frozen acceptance rubric (`Q-86-synthesis.md:56`), so a Success Criterion that contradicts the plan is exactly the failure mode Option B is being recommended to prevent.

Consequence: the next acceptance pass over this plan measures the tree against a criterion the tree cannot meet, and the discrepancy is in the plan's own single source rather than in a transient file.

Smallest safe correction: the later planner fold updates that criterion to require the step to record Q-85's receipt, hold Q-86 `open` against the completed synthesis, and keep implementation blocked until the Q-86 choice is receipted. (Out of scope for me to edit: I am not permitted to touch the plan.)

---

### CR-9 (medium). A pre-authorised fallback makes the human's "choose exactly one" conditional, and the fallback is absent from the ask.

`Q-86-synthesis.md:228`:

> A focused schema and reconstruction proof of concept must validate that obligations remain finite, precise, and non-duplicative before implementation proceeds. If that proof fails, choose `A - Sealed phase budget` rather than weakening the obligation invariant.

The proof-of-concept requirement is right and follows Principle 6. The fallback is the problem: it converts a failed PoC directly into a different architecture without returning to the human. The ask says the opposite - "The human must choose exactly one viable option through the human-input contract" (`docs/plans/agent-scaffold.plan.toml:2573`) - and never mentions the fallback, so a human who reads the queue line does not know their choice of B carries a conditional A. `AGENTS.md:41` is explicit: "The human decides; the agent advises and never decides for them."

Consequence: a hidden second decision rides on the first, and it is exactly the impasse case Principle 6 says to raise ("If the candidates are exhausted, raise the impasse for a decision rather than forcing through an unvalidated approach").

Smallest safe correction: change `:228` to route a failed proof of concept back to the human with A as the recommendation, and name the proof-of-concept gate in the ask.

---

### CR-10 (low). The cross-option cost claim in the ask mixes per-phase and whole-task bounds and is falsifiable as stated.

`docs/plans/agent-scaffold.plan.toml:2571`, projected at `docs/plans/agent-scaffold.md:179`:

> Option C has the smallest proof and lowest maximum cost ...

Option A and Option C bounds are per phase and scale with `m`; Option B's is whole-task and scales with `|O|` (`Q-86-synthesis.md:91`, `:128`, `:169`). Option C's automated-call bound is `15(m + 2)`; Option B's is `5(7 + C_O) - 1 = 10|O| + 39`. At `m = 3, |O| = 3` that is C = 75 against B = 69, so the claim is false for reachable parameter values. Nothing in the synthesis states that the three bounds are not directly comparable.

Consequence: a cost-sensitive human is given a ranking that does not hold, on the one line of the plan they are most likely to read.

Smallest safe correction: qualify the sentence with the parameter each bound scales in, or restate it as "Option C has the smallest proof and the lowest per-phase depth".

---

### CR-11 (low). The ledger's RESUME STATE anchor still says Q-86 is `exploring`, and this fold is what made that false.

```sh
grep -n 'Q-86 remains `exploring`' docs/plans/agent-scaffold.ledger.md
```

`docs/plans/agent-scaffold.ledger.md:535` ("RESUME HERE (2026-08-28 ...)") states "Q-86 remains `exploring`, and its tracked brief is `docs/plans/workflow-calibration.explorations/Q-86-convergence-mechanism-brief.md`", while `:551` in the same file records that the synthesis planner "moved Q-86 from `exploring` to `open`". The RESUME HERE claim was true on `main` and is false at `77345e88`.

The ledger is orchestrator-owned and outside this diff, and the runner forbids me from editing it, so this is reported rather than fixed. It matters because `AGENTS.md:61` makes RESUME STATE the pointer a resumed session reads first, and it now points at a retired status and a superseded document.

Smallest safe correction: the orchestrator moves the resume anchor to `Q-86 open, synthesis at .../Q-86-synthesis.md, awaiting the human choice` when it merges this round.

---

### CR-12 (low). Option B's per-batch call list reads as denying triage and the mandatory backstop re-check on the final authorised batch, contradicting the shared safety package.

`Q-86-synthesis.md:128`:

> With exactly two reviewer seats and at most one triage, one mandatory batched re-check, and one repair per non-final batch, automated calls are bounded by `5(7 + C_O) - 1`.

The natural reading attaches "per non-final batch" to all three items, which would leave the final authorised batch with no triage and no backstop re-check. That contradicts `:75`: "The call is structurally available even at exhaustion, so the budget cannot ration the safety check." Only the arithmetic disambiguates it in the safe direction - `5(7 + C_O) - 1` subtracts exactly one call, so only the repair is denied - and the arithmetic is not where a reader looks for a safety rule.

Consequence: the sentence that a reader would quote back as Option B's exhaustion behaviour states the opposite of the shared package's central backstop guarantee.

Smallest safe correction: move the qualifier - "at most one triage and one mandatory batched re-check per batch, and one repair per non-final batch".

---

### CR-13 (low). Option B drops the explorer's rule that a tree with no frozen rubric must be exempt rather than failed, and defines no `C_O` for such a tree.

`Q-86-safety-process.md:426` (Principle 3 row, M2 column): "Needs care. A tree with no frozen rubric must be exempt, not failed."

`Q-86-synthesis.md:140` keeps only the general part - "Historical findings remain untouched and active legacy work adopts at a digest boundary. An incomplete frozen set is a new safety risk, so uncertain or serious uncited defects fail closed to the human" - and `:149` inherits Option A's migration wholesale. Option A's adoption rule is "An active legacy task that has already spent its slice must terminally escalate rather than receive a fresh window" (`:99`), which presupposes a declared slice. Option B has no slice until `O` exists, and an active legacy task has no `O`, so `C_O` is undefined for exactly the population Principle 3 protects.

Consequence: the recommended option's Principle 3 story is incomplete in the direction the explorer warned about, and the two available default readings (undefined ceiling, or fail closed) are respectively unbounded and a hard break on existing trees.

Smallest safe correction: carry the exemption rule into `:140` - a task with no frozen obligation set adopts as exempt from the obligation predicate and bounded by the plan-review ceiling alone until its next plan review freezes an `O`.

---

### CR-14 (low). `pack/plan-template.success-criteria.md` is missing from the migration inventory, while the step sidecar claims the inventory is complete per mechanism.

`docs/plans/agent-scaffold.steps/workflow-calibration.md:22` asserts:

> The completed synthesis inventories the pack guidance, prompts, templates, generated copies, README, changelog, workflow spec, plan and ledger state, and instrumentation surfaces that each viable mechanism would make stale.

Option B's obligations "cite the plan's Success Criteria" with "stable ids [and] source references" (`Q-86-synthesis.md:56`, `:149`), so the Success Criteria template must carry those ids. `Q-86-safety-process.md:454` and `:738` name `pack/plan-template.success-criteria.md` for exactly this. The synthesis names only "the ledger and plan templates" (`:110`) and "The plan schema and template" (`:149`). The file exists (`ls pack/plan-template.success-criteria.md`) and is a canonical pack source with a generated counterpart, so omitting it leaves a generated copy that would drift.

Smallest safe correction: name `pack/plan-template.success-criteria.md` in Option B's migration surface at `:149`.

---

### CR-15 (low). "Option B" in the synthesis is the opposite of "Candidate B" in the proposal the synthesis cites as its source, with no mapping between the two label sets.

`Q-86-state-machine.md:9-12` names its two options Candidate A (non-resettable task budget) and Candidate B (fixed-depth protocol), and recommends Candidate A. In the synthesis, Candidate A becomes Option A and Candidate B becomes Option C, while Option B is a new composition built on the *other* proposal's M2. `Q-86-safety-process.md` uses a third label set, M1/M2/M3.

`Q-86-synthesis.md:5` and `:47` direct the reader to both proposals as the authoritative detail, and `:124` describes Option B as adopting "the state-machine proposal's sealed non-resettable authority envelope" - but nowhere maps Option A/B/C onto Candidate A/B and M1/M2/M3.

Consequence: a human who follows the synthesis's own pointers reads "Recommendation: choose Candidate A" in one source and "Choose B" in the other, with "Candidate B" describing the option the synthesis calls C. The most likely misreading is that the state-machine explorer rejected the recommended option, which is not what it did.

Smallest safe correction: one mapping line near `:47` - Option A = Candidate A + M1, Option B = M2 + the sealed envelope, Option C = Candidate B; M3 excluded.

---

### CR-16 (low). The shared package silently reverses the safety proposal's deliberate rule that review breadth is never rationed.

`Q-86-safety-process.md:282` states it as a design intent, not an incidental: "Model and harness diversity is free under section 3.1, because a round costs one unit however many reviewers run. This is a deliberate incentive: the cost control should ration review *rounds* and never review *breadth*." Its YAGNI repeats it at `:499`: "No per-reviewer or per-token budget accounting. One unit per round, deliberately, so diversity stays free."

The synthesis fixes "exactly two reviewer seats" per batch in Options A and B (`:87`, `:128`) and makes it a YAGNI prohibition in Option A: "Do not build ... more than two reviewer seats per batch" (`:118`). Under those options a third diverse reviewer on a risky artifact is structurally unavailable. The reversal is not noted, and `Q-86-synthesis.md:79` still presents reviewer allocation as though only blindness were constrained.

This does not conflict with the scheduled `reviewer-diversity` step, which generalises a *preference* to models-or-harnesses rather than setting a count, and it matches what the project runs today (all ten Q-78 acceptance passes ran exactly two reviewers). It is a finding because a stated explorer design rule was inverted without being surfaced to the human.

Smallest safe correction: note at `:79` that the first version caps seats at two per batch and that this trades the safety proposal's free-diversity incentive for a simpler account, so the human sees the exchange.

---

## What I checked and did not find a problem with

Stated explicitly so the absence is a result rather than a gap.

- **The ten-pass evidence is exact.** `jq -s 'map(select(.type == "round" and .task == "q78-design-pass" and .phase == "acceptance")) | {passes: length, valid_shortfalls: map(.valid_findings)}' docs/metrics/workflow.jsonl` returns 10 passes and `[7,10,5,6,5,5,4,2,1,0]`, matching `Q-86-synthesis.md:25`. Both explorers corrected the brief's dated six-pass snapshot and the synthesis carries the correction, including the honest reading at `:25` that the sequence closed rather than diverged.
- **The baseline non-admissibility argument is sound and correctly separated from the run.** `:27` argues from the rule, not the observation, and both explorer state-machine checks reproduce both cycles (`Q-86-state-machine.md:46-50`; `Q-86-safety-process.md:160-183`). The baseline is kept out of the option set in the plan, the sidecar and the ask.
- **The instrumentation caveats reproduce.** `jq -s 'map(select(.type == "round" and .outcome == "clean" and .valid_findings > 0)) | {rounds: length, streaks_advanced: (map(select(.consecutive_clean > 0)) | length)}' docs/metrics/workflow.jsonl` returns 19 and 19; the critical/re-check selector returns 1 critical round, 1 `dismissal_recheck`, result `overturned`. `:31`, `:32` and `:34` state these accurately, including the sparse-sample limit. The synthesis does not overstate the external experiment: `:35` and `:36` carry the four-way confound and the one-artifact caveat, and `:37` states the enforcement limit that no tool can prove a review was blind or independent.
- **Reviewer-allocation limits are honestly bounded.** `:79` keeps blindness and independence advisory and does not claim mechanical enforcement, consistent with both proposals and with `Q-86-safety-process.md:459`. CR-16 is about seat count, not about an overclaim.
- **Append-only migration holds.** `git diff --stat main..HEAD -- docs/metrics/` is empty; no historical record is rewritten. `:61` states the no-rewrite and digest-pinned-boundary rule, and each option's migration repeats it.
- **The dependency sequencing survives the synthesis.** `Q-86-safety-process.md:501` requires the mechanism to land after `review-loop-foreclosure-enforcement`; `Q-86-synthesis.md:236` carries it ("must sequence the chosen mechanism after the shared typed review reconstruction"). I checked the apparent conflict with `docs/plans/agent-scaffold.steps/workflow-driver-typed-fleet.md:12` and `review-loop-foreclosure-enforcement.md:10`, which forbid `SinglePass` from holding a cap or round counter: every option places the acceptance counter on a campaign or controller rather than on `SinglePass` (`:89`, `:149`, `:188`), so the disjointness contract is preserved and those two sidecars do not become stale. The safety proposal's contrary claim at its `:445` and `:742` is the one that is wrong, and the synthesis was right not to carry it.
- **Plan status and projection are coherent.** `Q-86` is `open` in `docs/plans/agent-scaffold.plan.toml:2561`, and the rendered queue line is an exact projection of the TOML ask: reconstructing it by the renderer's own rule (`src/plan/render.rs:442` with `one_line` at `:555`, newlines to spaces) reproduces `docs/plans/agent-scaffold.md:179` byte for byte. Both edited sidecars appear verbatim in the generated view. `Q-44` and `Q-56` are also `open` with no principle-named reasoning in their asks, so Q-86's ask format is consistent with the plan's convention and I do not raise it.
- **The no-change claim is accurate.** `:5` claims the synthesis changes no workflow rule, cap, reset behaviour, status outside Q-86, metric, spec, pack file, prompt, template, README, changelog or Rust source; the diff is five planning files and nothing else.
- **The Q-85 receipt citation is still exact.** `sed -n '472p' docs/metrics/workflow.jsonl | jq -c '{type,task,q_id,chosen}'` returns the `Q-86`-adjacent `Q-85` decision with `chosen: "Add a design pass to workflow-calibration"`, so the line-anchored citation in the step sidecar has not drifted (the log is 478 records).
- **All eight Project Principles are priced by name for each option.** `:95-104`, `:136-145`, `:175-184` cover all eight in the plan's exact wording, and none of the three tables is a copy of another. The rows are not uniformly favourable - `:98`, `:139`, `:143` and `:179` each concede real costs - so the tables are not advocacy. CR-3 and CR-6 concern what the "Ground decisions in evidence" rows omit, not their existence.
- **Documentation impact is present and mostly complete.** Each option names canonical pack sources and generated copies together (`:108-110`, `:147-151`, `:186-190`), and the step sidecar correctly says nothing is stale *now*. CR-14 is the one omission I found; CR-8 is a staleness this fold created elsewhere rather than a gap in the inventory.
- **Terminal choices are defined and the critical invariant is stated correctly.** `:67-73` fixes the legal effect of all five choices, `:70` blocks ordinary narrowing with an open serious finding and represents removal as an explicit `RemovedFromDelivery` disposition rather than as a resolved finding, and `:72` makes replan terminal with `CarriedToSuccessor` rather than a renamed resume. `:75` keeps the backstop outside the budget. I found no path in the synthesis text by which a budget alone converts an unresolved critical into a completion.
- **No finding on line length, wrapping, or style.** Per `AGENTS.md:108` and `.agents/prompts/reviewer.md:15`.

## Proof commands

Run from the repository root. Every one was executed in this worktree.

```sh
git diff --stat main..HEAD
git diff --stat main..HEAD -- docs/metrics/

jq -s 'map(select(.type == "round" and .task == "q78-design-pass" and .phase == "acceptance")) | {passes: length, valid_shortfalls: map(.valid_findings)}' docs/metrics/workflow.jsonl
jq -s 'map(select(.type == "round" and .outcome == "clean" and .valid_findings > 0)) | {rounds: length, streaks_advanced: (map(select(.consecutive_clean > 0)) | length)}' docs/metrics/workflow.jsonl
jq -s '{critical_rounds: (map(select(.type == "round" and ((.severities // []) | index("critical")))) | length), dismissal_rechecks: (map(select(.type == "dismissal_recheck")) | length), results: map(select(.type == "dismissal_recheck") | .result)}' docs/metrics/workflow.jsonl
jq -r '[inputs] | map(select(.type == "round" and .task == "q78-design-pass" and .phase == "acceptance")) | to_entries[] | [ (.key + 1), .value.valid_findings, ( if (.value.artifact | test("\\bfold\\b|(after|and) Q-8[0-9]")) then "scope-added" else "-" end ) ] | @tsv' -n docs/metrics/workflow.jsonl
sed -n '472p' docs/metrics/workflow.jsonl | jq -c '{type,task,q_id,chosen}'

grep -n "keeps Q-86" docs/plans/agent-scaffold.success-criteria.md docs/plans/agent-scaffold.md
grep -n 'Q-86 remains `exploring`' docs/plans/agent-scaffold.ledger.md
grep -n 'RECOMMENDATION: `B\|TRADE-OFF SUMMARY\|NO-DECISION BOUNDARY' docs/plans/agent-scaffold.plan.toml
ls pack/plan-template.success-criteria.md
```

Projection check (no `cargo` in this box, so the renderer's rule at `src/plan/render.rs:442` and `:555` was applied by hand):

```sh
# collapse the Q-86 TOML ask's newlines to spaces and compare with the rendered queue line
sed -n '179p' docs/plans/agent-scaffold.md > /tmp/rendered.txt
# reconstructed line from plan.toml lines 2560-2573 matched /tmp/rendered.txt exactly (diff empty)
diff <(sed -n '5063,5069p' docs/plans/agent-scaffold.md) docs/plans/agent-scaffold.questions/Q-86.md   # empty
```
