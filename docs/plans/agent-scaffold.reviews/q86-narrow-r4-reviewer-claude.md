# Narrowed Q-86 round 4 review (claude)

## Scope, method, and reproduction

I reviewed `main...HEAD` (`b6fb2ff6...392712ac`) as the risky narrowed Q-86 decision artefact, independently and in my own worktree. I read `AGENTS.md`, `.agents/prompts/reviewer.md`, the Q-86 and Q-88 structured records and sidecars, the owning `workflow-calibration` step sidecar, the Success Criteria, the narrowed synthesis, both retained proposals, the retained brief, both prototypes, and the three prior narrowed triages. I did not read the other round-4 reviewer. I changed nothing outside this file.

Baseline checks, both passing:

```sh
nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml
# docs/plans/agent-scaffold.plan.toml: up to date
nix develop -c cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow
# 488 records, valid; 114 steps, 88 questions, valid; workflow invariants hold
```

`git diff --name-only main...HEAD` contains only `docs/metrics/workflow.jsonl`, `docs/plans/`, and the two exploration prototypes. No `src/`, `tests/`, `pack/`, `.agents/`, `README.md`, `CHANGELOG.md`, or workflow-spec path changed, so nothing in this pass alters shipped behaviour and the artefact's own no-change claim at `Q-86-synthesis.md:7` holds.

## Round-3 fixes: all four verified closed

- **T1 (unescaped table delimiters discard decision content).** Every body row in both repaired tables now matches its header width. `nix run nixpkgs#cmark-gfm -- --extension table` on `Q-86-synthesis.md:152-177` renders the whole-family row with all four cells and the B cell as `r_plan + |O| + m + 1`; `Q-86-safety-process.md:445` is escaped the same way and its M3 cell survives. I re-scanned every table row in `Q-86-synthesis.md`, `Q-86-safety-process.md`, `Q-86-state-machine.md`, `Q-86-convergence-mechanism-brief.md`, `Q-86.md` and `Q-88.md` for unescaped pipes; no row is now off its header width.
- **T2 (B's cost table applied a post-freeze symbol to plan review).** `Q-86-synthesis.md:156-160` now splits plan review from post-freeze work and acceptance, prices B's plan review as A's one-batch/two-call and two-batch/four-call minima "reusing A's sealed plan controller", and keeps `n_q + 1` / `2(n_q + 1)` only for post-freeze phases. That matches `:103`, `:105` and the unchanged whole-family algebra at `:112-119`.
- **T3 (the Q-86 sidecar omitted B's qualified Q-78 consequence).** `Q-86.md:8` now carries the counterfactual four-replan statement with its "if one assumed fold would not change the canonical digest" qualifier, and it is projected at `agent-scaffold.md:5079`. All three option bullets now carry a Q-78 consequence.
- **T4 (published controller digest did not identify the retained file).** `sha256sum docs/plans/workflow-calibration.explorations/q86-controller-proof.py` returns `8a349c68dbe18df43d1d60d4110e11b3e216d97cdf4efb9f7e7328693d668175`, which is now published at `Q-86-safety-process.md:403,555` and `Q-86-state-machine.md:467`. `git show ad989b5f:...q86-controller-proof.py | sha256sum` returns `d0dabe6d...`, which is now labelled as the historical pre-caveat digest at that named commit rather than as the current file's.

## What else I re-derived and found sound

- **Every published number reproduces.** The authoritative selector returns ten passes and `[7,10,5,6,5,5,4,2,1,0]`. A stopping at pass seven leaves `2+1+0 = 3` low shortfalls; C stopping at pass three leaves `6+5+5+4+2+1+0 = 23`, with `high` in the `severities` of passes 4, 5 and 6. The floor-`high` restriction sentence at `:213` names exactly the passes whose severities contain a `high` (3-6), and the retained triages for those four passes each carry an upheld valid `high` (`q78-acceptance-r3-triage.md:21`, `-r4-:29,37`, `-r5-:31`, `-r6-:25`). "Nineteen" reproduces as 19, and all 19 carry `consecutive_clean >= 1`. Six of the ten Q-78 triage files remain.
- **The algebra is internally consistent.** `sum(4n_q + 1)` over `p = m + 1` post-freeze phases is `4|O| + m + 1`, `+7` for the inherited plan phase gives `R_B = 4|O| + m + 8`; `4R_B + 6 + 2|O| = 18|O| + 4m + 38 = I_B`; `L_B = r_plan + |O| + m + 1`; A's `14 + 7 + 7 + 6 = 34`; C's `5 + 4 + 4 + 2 = 15`. Every figure agrees across `Q-86-synthesis.md`, `Q-86.md:7-9`, `agent-scaffold.plan.toml:2565-2567` and `agent-scaffold.steps/workflow-calibration.md:22`.
- **Both prototypes reproduce their published output, with their caveats intact.** The replay prints `summary passes=10 observed_named_folds=4 assumed_digest_changes=4 conditional_terminal_replans=4 conditional_families=5 conditional_additional_human_receipts=4 conditional_additional_plan_review_and_freeze_cycles=4` and both self-test fixtures, exactly as `Q-86-safety-process.md:569-571` states. The B sweep declares bounds `1,5,9,13` with `min_reviews` `1,2,3,4` and `max_reviews` `1,5,9,11`, so the "reaches smaller maxima under the retained-map cap" caveat at `:555` is accurate. Both files carry the in-file limitation notice added for round-1 T5.
- **The prototype-boundary list is a faithful summary of round 5.** The six bullets at `Q-86-synthesis.md:49-55` map one-to-one onto `q86-synthesis-r5-triage.md` T1-T6, and `:56` covers T7. Nothing overstates what the prototypes established.
- **The receipt is exact.** One `type:"decision"` record with `q_id:"Q-88"`, the six option labels in the recorded order, `recommendation` and `chosen` both `Narrow the proof scope`. It matches `Q-88.md:7-16` and `agent-scaffold.plan.toml:2600-2609` label for label. Round-5's counts (`4 high, 2 medium, 3 low`) match `q86-synthesis-r5-triage.md:89`, `Q-88.md:23` and `workflow-calibration.md:20`.
- **The proof gate, failure path, and no-decision boundary hold across all surfaces** (`Q-86-synthesis.md:186-207,225-244`, `Q-86.md:23-29,39-41`, `agent-scaffold.plan.toml:2573,2580`, `workflow-calibration.md:26,28`, `agent-scaffold.success-criteria.md:41`). Each makes the proof unit an explicit blocker for every production implementation unit, requires the r1-r5 traceability matrix, and returns a failed proof to the human with no automatic fallback. I found no path that grants implementation authority, and the round-3 valid findings were all repaired in-pass rather than deferred, so the traceability scope still drops nothing.
- **Currency.** The retained brief (`Q-86-convergence-mechanism-brief.md:5-11,91-105`) was updated off `exploring` and onto the narrowed gate, so no surface still calls Q-86 an open design pass or points at the brief as the decision artefact.

## Findings

Three findings, all `low`. **Zero critical, zero high, zero medium.** None re-raises a settled verdict: round-1 T6 (the retained state-machine induction claim) is untouched, and the deferred r1-r5 proof obligations are respected as deferred rather than re-raised.

### Finding 1 — the serious terminal-floor co-decision carries a recommendation with no reasoning and no Principle-named judgement

- **Severity:** low.
- **Evidence:** The floor is one of the two decisions Q-86 puts to the human (`Q-86-synthesis.md:244`, `agent-scaffold.plan.toml:2580`). Its presentation is `Q-86-synthesis.md:209-217`, copied to `Q-86.md:31-37`, `agent-scaffold.plan.toml:2575-2578`, and projected into the Open-Questions queue at `agent-scaffold.md:179`. Each surface gives three options, a consequence sentence per option, and the bare word "recommended" on `high`. None gives a reason for that recommendation, and none names a Project Principle:

  ```sh
  sed -n '209,217p' docs/plans/workflow-calibration.explorations/Q-86-synthesis.md \
    | grep -cE 'Prefer the cleaner|Minimal by default|Safe on existing|Idempotent|Make illegal states|Ground decisions|Reproducible|Structured data first'
  # 0
  ```

  The same grep returns `0` for `Q-86.md:31-37` and for `agent-scaffold.plan.toml:2575-2578`. The gap is specific to the floor: the architecture recommendation in the same artefact names three Principles for and three against (`Q-86-synthesis.md:182,184`), the Principle comparison table at `:167-176` covers all eight by name for A, B and C only, and Q-88's own decision judges itself against all eight (`Q-88.md:27-36`, `agent-scaffold.plan.toml:2611`). The reasoning is not merely relocated: the mapped source proposal's floor bullets (`Q-86-safety-process.md:521-525`) also give only consequences, so no durable surface carries it.
- **Why this is a defect:** `AGENTS.md:41` settles the human-input contract once for every human-input point: the orchestrator presents "the viable options or approaches, the trade-offs of each, a recommendation, and the reasoning, with the reasoning judged against the plan's Project Principles by name". The floor is a safety co-decision that determines whether an open `high` may ever be shipped as residual risk, so it is not the "trivial confirmation" the contract lets you scale down to a one-line recommendation and reason — and even that reduced form requires a reason, which is absent. The human is asked to choose the stricter of two safety floors on an unstated basis.
- **Why low:** the options, their consequences, and the `defer` escape are all stated and mutually consistent, `critical` is correctly identified as the mandatory minimum, and gate item 8 (`:199`) requires the selected proof to model both floors, so no floor outcome can hide an untested transition. Nothing here changes a bound or grants authority.
- **Suggested correction:** give the floor recommendation one short reasoning paragraph judged against the Project Principles by name (for example: `high` under Make illegal states unrepresentable and Safe on existing projects, because it makes an unresolved serious finding structurally undeliverable rather than discretionary; against it, Minimal by default and Ground decisions in evidence, because the Q-78 replay shows the restriction would have bound on passes three through six with no prospective evidence on its cost). Mirror it into `Q-86.md` and the structured ask, and re-render.

### Finding 2 — B's Principle comparison and recommendation reasoning omit the plan-review controller B inherits from A

- **Severity:** low.
- **Evidence:** B is not a whole-family replacement for A. `Q-86-synthesis.md:103` states that "B reuses A's sealed controller for plan review"; `:112-116` derives `R_B = 7 + sum(4n_q + 1)`, where the `7` is A's five-normal-plus-two-reserve slice; `L_B = r_plan + |O| + m + 1` at `:118` carries A's plan term; and the round-3 repair now prices B's two plan-review rows identically to A's, annotated "reusing A's sealed plan controller" (`:156-157`). The mapped source says the same twice — `Q-86-safety-process.md:324` ("Its plan review reuses M1's sealed controller unchanged") and `:515`, which lists "the five-normal-plus-two-reserve slice used by A **and inherited by B plan review**" among the unapproved controller constants.

  The comparison surfaces do not carry that inheritance across:

  - `:169` prices A as "Unifies task spend but layers a budget over existing streaks" and B as "Unifies scope, ownership, disposition, phase authority, and completion", though one of B's `m + 2` phases *is* that layered budget over streaks.
  - `:170` charges A with "adds account and reserve fields" and B only with "canonical obligations and the largest schema", though B adds the obligation schema *on top of* A's account and reserve fields.
  - `:174`, the "Ground decisions in evidence" row, charges A alone with "reserve values are weakly calibrated" and gives B "obligation cost and completeness lack prospective evidence" — but B inherits precisely those weakly calibrated reserve values, as `Q-86-safety-process.md:515` says.
  - `:182` states the recommendation's core differentiator as "B gives ... one structured source, while A keeps streak and budget as separate stopping concepts", unqualified; `:184`'s list of low-confidence reasons for B omits the inherited constants entirely. The same unqualified contrast is copied to `Q-86.md:13` and `agent-scaffold.plan.toml:2569`.
- **Why this is a defect:** every A-side cost the reasoning cites is a cost B also pays for its plan-review phase, and the omission runs one way — it understates the recommended option in the table and paragraph that justify recommending it. This is a distinct surface from round-3 T2, whose correction was explicitly scoped to the cost table and directed not to change the published bounds; the Principle table and the recommendation paragraph were not in that repair.
- **Why low:** the inheritance is stated plainly three times in the same document, and after the round-3 repair the cost table itself now says it, so a reader who works through the cost model can recover it. No bound is wrong and the proof gate is untouched.
- **Suggested correction:** qualify B's cells at `:169`, `:170` and `:174` to note that B inherits A's sealed plan-review controller with its account, reserve fields and weakly calibrated five-plus-two values, and add that inherited constant to the low-confidence list at `:184` and to the recommendation text in `Q-86.md` and the structured ask. Do not change any published bound.

### Finding 3 — the human-facing Q-86 surfaces state B's cost formulas with symbols they never define

- **Severity:** low.
- **Evidence:** `Q-86.md:8` prices B as "clean post-freeze phase minimum `n_q + 1`, maximum `4n_q + 1`, whole-family minimum `r_plan + |O| + m + 1`, whole-family maximum `4|O| + m + 8`, and automated-agent maximum `18|O| + 4m + 38`". None of `m`, `n_q`, `O` or `r_plan` is defined anywhere in that file, and `m` also appears undefined in the A and C bullets at `:7` and `:9`. The structured ask glosses only `m` ("each of `m` work loops", `agent-scaffold.plan.toml:2565`) and leaves `n_q`, `O` and `r_plan` unglossed at `:2566`; that ask is what the Open-Questions queue projects at `agent-scaffold.md:179`, which is the human-decision queue `AGENTS.md:71` designates as the single queue of decisions the human owns. The definitions exist only in the synthesis: `m` at `Q-86-synthesis.md:79`, `O` and `n_q = |O_q|` at `:103,105`, and `r` ("one at low risk and two at risky") at `:93`. `r_plan` is the sharpest case, because unlike `|O|` it is not inferable from surrounding prose, so a reader of the queue cannot evaluate B's whole-family minimum at all.
- **Why this is a defect:** cost is the axis on which B is most exposed, and these are the surfaces a human reads when the queue is pushed at a checkpoint. This is the same class of defect as round-5 T9, where `n_a` undefined against the table's vocabulary was ruled valid and low, and the round-3 T2 verdict rested on the same reasoning ("a reader cannot price B's low- or risky-plan review from that table").
- **Why low:** `Q-86.md:1` names the synthesis as the narrowed decision artefact in its first line, so every definition is one hop away, and the formulas themselves are correct and consistent across all four surfaces.
- **Suggested correction:** add one glossing clause to `Q-86.md:8` and the structured ask — `O` is the frozen canonical obligation set, `n_q = |O_q|` is the obligation count owned by post-freeze phase `q`, and `r_plan` is the plan-review clean-batch count, one at low risk and two at risky — and gloss `m` as the work-loop count where it is first used. Re-render.

## Counts

**Zero critical, zero high, zero medium, three low.** I found nothing of critical, high, or medium severity: no surface grants implementation or architecture authority, no published bound or count is wrong, no floor outcome can bypass the proof gate, and the prototypes are correctly quarantined.
