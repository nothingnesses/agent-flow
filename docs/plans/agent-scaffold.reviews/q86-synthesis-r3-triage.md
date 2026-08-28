# Q-86 synthesis round 3 triage

## Scope and reproduction

I independently read `AGENTS.md`, the triager prompt, the Q-86 brief, both current proposals, the synthesis, the controller proof and Q-78 replay scripts, the Q-86 planning fold, the round-1 and round-2 triages, and both round-3 reviewer reports. The reviewed product is `main...bc680ebe`; this is a risky decision artifact. I did not edit reviewed product, prior findings, the metrics log, or the ledger.

The published controller commands reproduce at both floors. The B sweep reports declared bounds `1`, `5`, `9`, and `13`, observed cardinality-two maxima `1`, `5`, `9`, and `11`, and the advertised zero counters. The checker hash is `937c714a483b583eaa66222adf4fc2e50e4764924568a5d435cbbf3078349260`. The live Q-78 selector returns ten passes, `[7,10,5,6,5,5,4,2,1,0]`, and the published conditional replay returns four observed named folds, four assumed digest changes, four conditional replans, and five families.

I also reproduced every new claim below in this worktree. Scratch mutation and synthetic-log tests were created in a worktree-local temporary directory and removed before authoring this file. The no-relitigation rule is observed: the two round-2 partial closures carry new evidence about the corrected transition relation, rather than restating the prior scalar-map or successor-rule claims.

## Deduplication and outcome

Eleven raw reports consolidate to nine findings:

- `Q86-R3-GPT-3` and `R3C-4` are one acceptance-blind-closure defect.
- `R3C-1` and `R3C-2` are one Option B plan-campaign definition and arithmetic defect.

All nine consolidated findings are valid: **one high, four medium, and four low**. There are no invalid findings and no accepted residual risks.

**Round outcome: `new_valid`.**

No high- or critical-severity report was dismissed. **No independent dismissal backstop re-check is owed.**

## Consolidated verdicts

### T1 — B's finite-map proof omits cross-owner findings from one review batch

- **Source IDs:** `Q86-R3-GPT-1`
- **Verdict:** valid, **high**.
- **New evidence / reproduced evidence:** The repaired checker now retains multiple findings for one owner, but `b_valid_from_attempt` assigns a profile to exactly one selected owner at `q86-controller-proof.py:317-324`, and `b_edges` serializes one `untested` or special obligation at `:435-460`. Exhausting the shipped two-obligation graph yields zero states with outstanding findings for two owned obligations. I then reproduced the reviewer's scratch-only mutation: an `o1` initial low batch also adds an `o2` critical. The shipped assertion fails with `bad_delivery != 0`. Independently, starting the unmodified reducer from the resulting post-`o1` verification state (`o1` closed, `o2` untested, `o2` critical still open) reaches `o2_initial_clean -> blind_closure_clean`; `walk` reports `bad_delivery=29` and `bad_unverified_delivery=29`.
- **Reasoning:** `Q-86-synthesis.md:50-61` permits any finite batch and claims the arbitrary-cardinality result composes. A broad review batch can contain findings mapped to several frozen obligations. The current composition argument covers finding-map union and pointwise dispositions, but not the product with the obligation-state tuple. It therefore cannot establish B's claimed complete-map delivery invariant for a legal mixed-owner batch. This is distinct from round-2 T1, which concerned scalar erasure and was repaired for same-owner and blind-closure maps.
- **Exact correction:** Model batch reductions as a finite map keyed by owner plus an optional unowned set, atomically advancing every affected obligation state. Add the `o1` low plus `o2` critical cardinality-two case to the shipped proof. Extend the composition proof to preserve the invariant that every owned outstanding finding has a matching non-closed obligation state, and make blind completion quantify over both that state and the full finding map. State whether a batch can satisfy initial attempts for several owners and recompute B's minimum accounting if so; retain `4n_q + 1` only after showing it remains an upper bound.

### T2 — B's successor oracle does not model receipt binding, finding carry, or spend preservation

- **Source IDs:** `Q86-R3-GPT-2`
- **Verdict:** valid, **medium**.
- **New evidence / reproduced evidence:** `Q-86-synthesis.md:70-77` requires a receipt naming the predecessor and proposed scope, plus carried unresolved findings. The proof's `SuccessorReceipt` contains only `present` and `materially_different` booleans, while `Predecessor` contains only family id, obligations, exclusions, and terminality (`q86-controller-proof.py:505-520`). I imported the checker and confirmed that `SuccessorReceipt(True, True)` authorizes a successor for `F1` despite containing no family, digest, options, chosen successor, findings, or spend. `check_successor` tests same/reordered scope and a missing receipt only (`:711-726`).
- **Reasoning:** the proof result labelled `B successor structured_cases=4` cannot establish the anti-laundering and carried-critical controls attributed to it. This is new evidence about the successor proof added after round-2 T5; it does not reopen the settled prose choice of materially different scope.
- **Exact correction:** Give the receipt exact predecessor and successor identities, proposed obligation/exclusion digests, presented options, and chosen successor. Model predecessor spend and the complete carried finding map in the successor relation. Reject wrong-family and wrong-digest receipts, missing carried findings, and a successor that treats predecessor spend as fresh authority; publish those negative cases with the existing scope tests.

### T3 — Option B's plan-review campaign is under-specified and its human-facing arithmetic misstates the phase boundary

- **Source IDs:** `R3C-1`, `R3C-2`
- **Verdict:** valid, **medium**.
- **New evidence / reproduced evidence:** The human ask says every B phase has maximum `4n_q + 1` while also stating the family maximum is `4|O| + m + 8` (`agent-scaffold.plan.toml:2566` and `questions/Q-86.md:6`). The synthesis correctly scopes the former to post-freeze phases and separately gives plan review a seven-batch maximum (`Q-86-synthesis.md:136,156`); treating plan review as another `4n_q + 1` phase undercounts the family by six batches. Further, B uses an undefined `r_plan` in its minimum (`:158-162`), but specifies neither B's plan-review completion predicate nor whether it reuses A's five-normal-plus-two-reserve controller. Mode B starts only a post-freeze campaign (`q86-controller-proof.py:729-731`).
- **Reasoning:** the same omission causes both the misleading per-phase sentence and an uncomputable B minimum. It silently imports A's seven-batch maximum and six repair allowance while presenting five-plus-two as A-specific and unapproved. This is a new plan-phase problem after the round-2 allocation and minimum-cost corrections.
- **Exact correction:** Define B's plan-review controller, including its completion predicate, risk treatment, budget/reserve rule, and repair bound, or explicitly state that B reuses A's plan controller and identify all inherited constants as B plan-review constants too. Change the ask and question sidecar to say that only each post-freeze phase has `n_q + 1` / `4n_q + 1`, while B plan review has its separately defined maximum. Define `r_plan` from that controller, then re-render the plan.

### T4 — The synthesis leaves the severity routing for scope-expanded findings unreconciled

- **Source IDs:** `R3C-3`
- **Verdict:** valid, **medium**.
- **Reproduced evidence:** The shared synthesis rule backlogs every genuinely optional scope expansion, subject only to a high-or-critical out-of-scope re-check (`Q-86-synthesis.md:66`), and its red-control matrix tests only `Scope-expanded low` (`:318`). The state-machine proposal instead sends medium, high, and critical scope expansions to a terminal human scope decision and backlogs only low (`Q-86-state-machine.md:95`). Neither the synthesis's selected-rule discussion nor its excluded-alternatives section records which policy it chose or why, and the checker has no scope-expanded transition.
- **Reasoning:** this is a real policy choice at the scope firewall, not merely a terminology difference between proposals. The synthesis must either retain the stricter routing or deliberately choose the broader backlog route and expose its trade-off. Leaving it implicit lets a triager backlog a medium finding without the human routing the state-machine proposal regarded as a protection against firewall abuse. The brief requires scope expansion to be controlled rather than silently enlarging the task; it does not authorize an unrecorded severity policy.
- **Exact correction:** State one shared selected policy. Either permit automatic backlog only for low and route medium-or-above scope expansions to a terminal human decision, or explicitly retain the all-severity backlog rule, explain why against the Project Principles, and list the severity-escalated route as an unselected alternative. Add red controls for low, medium, high, and critical scope-expanded results, including the high-or-critical re-check.

### T5 — C's executable acceptance controller can bypass mandatory blind closure

- **Source IDs:** `Q86-R3-GPT-3`, `R3C-4`
- **Verdict:** valid, **medium**.
- **Reproduced evidence:** The synthesis says acceptance requires discovery plus blind closure (`Q-86-synthesis.md:206,218-219`). But `check_c` passes phase only to output and `c_settled` completes every low-risk discovery (`q86-controller-proof.py:209-215,666-669`). Running the legal command `--mode C --phase acceptance --risk low_risk --floor high` reports `min_reviews=1`, rather than the stated two. The round-3 reports differ only in initial severity; the defect is one acceptance-specific control failure.
- **Reasoning:** the phase-local proof does not establish C's acceptance factor or reserved blind closure for every accepted invocation. A one-batch acceptance can deliver without the independent sample that C presents as structural.
- **Exact correction:** Carry phase into C state/transitions and permit one-batch discovery completion only for a non-acceptance low-risk phase, or explicitly forbid a low-risk acceptance invocation. Add the low-risk acceptance case to the published proof matrix with `min_reviews=2` and assert every completing acceptance path visited `BlindClosure`.

### T6 — A's controller does not implement its stated foreclosure timing

- **Source IDs:** `Q86-R3-GPT-4`
- **Verdict:** valid, **low**.
- **Reproduced evidence:** A says foreclosure fires when remaining batches cannot satisfy the required clean streak (`Q-86-synthesis.md:112`). In the risky-work graph I reached `repair` at review six with streak zero, limit seven, one review remaining, and two clean rounds required. `a_edges` still offers `repair_joint -> verify`; `a_open` tests only the absolute limit, not the clean suffix (`q86-controller-proof.py:138-143`).
- **Reasoning:** the maximum remains bounded, but this path spends an automatic repair and verification after the declared convergence predicate is impossible. That contradicts the decision artifact's stated foreclosure semantics and needlessly changes its bounded cost behavior.
- **Exact correction:** Centralize the remaining-clean-suffix calculation and foreclose before repair or review when the remaining authorized verification path cannot attain it. Add a risky-work assertion that an active, repair, or verify state is not retained when its remaining reviews are fewer than its required clean suffix.

### T7 — C's Q-78 pass-three result is incorrectly presented as independent of the serious floor

- **Source IDs:** `R3C-5`
- **Verdict:** valid, **low**.
- **Reproduced evidence:** The synthesis says C reaches `SeriousBlocked` at Q-78 pass three because that pass carries a high (`Q-86-synthesis.md:210`). `terminal_control` makes an open finding serious only at or above the selected floor (`q86-controller-proof.py:110-111`). With `F=critical`, I reproduced `review_findings_high -> terminal`, and `accept_residual` is legal from that state; it is not `SeriousBlocked`.
- **Reasoning:** floor choice is explicitly still human-owned. The strongest Q-78 comparison against C therefore has materially different outcomes under the two offered floors, and the critical-floor outcome is absent from the architecture/floor decision framing.
- **Exact correction:** state C's pass-three outcome for both floors in the synthesis and human ask: `SeriousBlocked` at `high`, and terminal with residual acceptance available at `critical`. Explain the corresponding 23 undiscovered shortfalls in both cases.

### T8 — The proof's advertised exact command contains a stale, machine-specific scratch path

- **Source IDs:** `R3C-6`
- **Verdict:** valid, **low**.
- **Reproduced evidence:** `Q-86-synthesis.md:260` and `Q-86-state-machine.md:437` export a fixed `/tmp/claude-1000/.../q86-synthesis-r2-fix` `TMPDIR`. The path does not exist in this worktree. The checker happens to pass with that nonexistent `TMPDIR`, so this is not a false proof result, but a reader told to run the command exactly receives a stale session path. `Q-86-safety-process.md:5` says the corrected proof does not depend on the old scratch directory, while the state-machine document still records it as a corrected rerun location.
- **Reasoning:** a machine- and session-specific scratch path in a durable exact reproduction command violates the design pass's reproducibility boundary and creates contradictory documentation about a dependency the proof does not have.
- **Exact correction:** remove the fixed `TMPDIR` export from both exact-command blocks and remove or reword the stale state-machine scratch-directory claim to match the safety proposal.

### T9 — The Q-78 scope replay summary is hard-coded to pass ten rather than the selected input length

- **Source IDs:** `R3C-7`
- **Verdict:** valid, **low**.
- **Reproduced evidence:** `q86-q78-scope-replay.sh:37-40` emits the summary only when `pass == 10`. On a synthetic nine-pass selected log, it emits no summary. On an eleven-pass selected log with a second named fold at pass eleven, it emits a pass-ten summary with one replan and two families, then emits the pass-eleven replan to F3 after that stale summary. The live replay currently works only because it currently selects ten passes.
- **Reasoning:** the Q-86 brief makes the selector authoritative if the append-only log grows. The durable replay must preserve that property; its current summary silently becomes incomplete on exactly the expected future change.
- **Exact correction:** process the selected rows without a pipeline-subshell counter loss and print one summary after EOF, using the actual pass and family counters. Add nine- and eleven-pass synthetic regression fixtures or equivalent commands proving the summary is always emitted once and reflects all selected records.

## Verification record

- Published all-mode proof commands at `high` and `critical`, B `n=0..3` sweep, checker hash, live Q-78 replay, and authoritative Q-78 selector — reproduced.
- Direct checker-state searches, the cross-owner scratch mutation, low-risk C acceptance run, floor-critical C high trace, and risky A foreclosure trace — reproduced as cited above.
- Dynamic replay tests used synthetic nine- and eleven-pass JSONL inputs in a removed worktree-local scratch directory.
- `git diff --check main...bc680ebe` — passed before this triage file was authored.
