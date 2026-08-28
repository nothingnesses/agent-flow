# Q-86 synthesis round 3 reviewer report (claude)

## Scope and reproduction

I independently read `AGENTS.md`, `.agents/prompts/reviewer.md`, the Q-86 brief, both explorer proposals, the synthesis, the durable proof and replay artefacts, the Q-86 plan fold and its sidecars, the Success Criteria source, the generated projection, the round-1 and round-2 triages, and the ledger resume anchor. The reviewed change is `main..HEAD`, that is `a4905603..bc680ebe`, treated as `risky`. Lens: executability, human choice, and adversarial adoption.

Everything published as evidence reproduces exactly in this worktree:

- `q86-controller-proof.py --mode all ... --floor high` and `--floor critical`: both four-line outputs match `Q-86-synthesis.md:273-282` byte for byte.
- The `--mode B --phase work:example --obligations 0..3 --floor high` sweep matches `Q-86-synthesis.md:288-291`, including the declared bounds `1,5,9,13` and the reached maxima `1,5,9,11`.
- `Q-86-state-machine.md:449-453`'s five outputs (A acceptance/work_review, C acceptance/work_review at both risks) reproduce exactly.
- `sha256sum` on the checker returns `937c714a483b583eaa66222adf4fc2e50e4764924568a5d435cbbf3078349260`, matching all three artefacts.
- `q86-q78-scope-replay.sh docs/metrics/workflow.jsonl` returns the published fourteen event lines and the exact summary at `Q-86-synthesis.md:305`.
- The Q-78 selector returns ten passes and `[7,10,5,6,5,5,4,2,1,0]`. Pass 7's `severities` is `["medium","medium","low","low"]` and passes 8-10 are `["low","low"]`, `["low"]`, `[]`, so A's "pass seven, three later low shortfalls" and C's "pass three, 23 later shortfalls including highs" are both arithmetically correct against the log. The six retained Q-78 triages confirm highs on passes three, four, five and six and none on passes one and two, so the floor rationale at `Q-86-synthesis.md:83` is supported.
- `nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml` — passed (`up to date`).
- `nix develop -c cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` — passed (480 records; 114 steps; 87 questions; workflow invariants hold).

I verified each of the twelve valid round-2 findings landed: T1 complete `FindingMap` with a cardinality-two sweep plus a compositional argument, T2 conditional replay wording throughout (`:36`, `:190-192`, `:350`), T3 `LegacyNoRubric` with three red controls, T4 `serious_seen` preserved on referral plus `bad_upheld_unlock`, T5 the selected successor rule with the stricter rule marked unselected at `:342`, T6 the minimum-cost table, T7 `bad_unverified_delivery` plus the `no_untested` guard, T8 `UnownedInScopeFinding`, T9 C's constants added to the no-decision list at `:370`, T10 the projection-qualified boundary sentence at `:5`, T11 the phase-factor-versus-algebra split at `:240`, and T12 `medium` in `SEVERITIES` at `q86-controller-proof.py:7`. I re-derived the arithmetic behind `R_B = 4|O| + m + 8`, `18|O| + 4m + 38`, `34(m + 2)` and `15(m + 2)` and all four are internally consistent. I also independently derived why the n=3 sweep stops at 11 rather than 13 (with a global two-finding cap only two obligations can reach four review-consuming transitions; the third reaches two, giving 4+4+2+1 = 11), which confirms the explanation at `:294`.

I did not re-raise any settled finding. No finding below repeats a round-1 or round-2 verdict; each cites new evidence in text or code that the round-2 repair introduced or left unaddressed.

## Result

**Seven findings: zero critical, zero high, three medium, four low.**

There are no `critical` findings and no `high` findings. The corrected controller, its bounds, the conditional replay and the reproducibility of every published command all hold up under adversarial re-execution.

---

### R3C-1 — The human-facing ask states a per-phase B maximum that contradicts the published whole-family maximum

- **Severity:** medium.
- **Evidence:** the Q-86 ask at `docs/plans/agent-scaffold.plan.toml:2566` says of Option B: "Each phase has a clean minimum `n_q + 1` and maximum `4n_q + 1`. The whole-family minimum is `r_plan + |O| + m + 1`, while the maximum is `4|O| + m + 8`." The same two sentences appear in the question sidecar at `docs/plans/agent-scaffold.questions/Q-86.md:6` and in both generated projections at `docs/plans/agent-scaffold.md:179` and `:5068`. The synthesis body is correct and different: `Q-86-synthesis.md:136` says "Plan review has the same sealed maximum of seven batches as A", and `:156` scopes `C_q = 4n_q + 1` to the post-freeze set `P` only.
- **Consequence:** the two numbers in the same paragraph cannot both be right. Summing the stated per-phase maximum over all `m + 2` phases, with plan review carrying no obligations, gives `4|O| + (m + 2)`, not `4|O| + m + 8`; the gap is exactly the six extra batches of the seven-batch plan campaign. A human pricing B from the per-phase formula the ask gives them under-counts B's family maximum by six review batches, and cannot tell from the ask alone which figure governs. This is a cost input in a decision whose stated purpose includes comparing maxima.
- **Smallest correction:** in the plan TOML ask and the `Q-86.md` sidecar, scope the formula the way the synthesis body already does, for example "Each post-freeze phase has a clean minimum `n_q + 1` and maximum `4n_q + 1`, while plan review keeps a sealed seven-batch maximum", then re-render.

---

### R3C-2 — Option B's plan-review campaign is never specified, so `r_plan` is undefined for B and A's constants are inherited silently

- **Severity:** medium.
- **Evidence:** `Q-86-synthesis.md:136` gives B's plan review a maximum ("the same sealed maximum of seven batches as A") and `:174` gives it A's repair allowance ("Plan review has at most six grouped repairs"), but nothing in the Option B section states B's plan-review completion predicate, its normal/reserve split, or its reserve-unlock rule. `:158` then writes the published family minimum as "If `r_plan` is the declared plan-review minimum, the whole-family minimum is `L_B = r_plan + |O| + m + 1`", and the minimum-cost table at `:219` places the same symbol `r_plan` in both the A and the B column. `r_plan` is defined for A by `:112` and `:116` (one clean for low risk, two for risky); it is defined for C by `:206`; it is defined nowhere for B. The checker's mode B starts post-freeze (`q86-controller-proof.py:729-731`) and never models a B plan-review campaign, so the seven and the six come from mode A's graph, not from any B-specific evidence.
- **Consequence:** two things follow. First, B's published whole-family minimum contains a term the document never defines for B, so a planner or validator cannot compute it and the A-versus-B minimum comparison in the table silently assumes the two `r_plan` values are the same quantity. Second, choosing B in fact adopts A's five-plus-two plan-review budget and its six-repair allowance, while both the synthesis no-decision list at `:370` and the ask's NO-DECISION BOUNDARY at `docs/plans/agent-scaffold.plan.toml:2580` present "A's five-plus-two" as an A-specific constant. A human choosing B is not told that A's plan-review constants come with it.
- **Smallest correction:** add one sentence to the Option B controller section stating that B's plan-review phase reuses Option A's phase controller unchanged, so `r_plan` and the seven-batch maximum are A's and are established by the published mode-A run; and change "A's five-plus-two" to "the five-plus-two plan and phase slice values used by A and by B's plan review" in the two no-decision lists.

---

### R3C-3 — The shared scope rule drops the state-machine proposal's human routing for medium-or-worse scope expansions, with no reconciliation recorded

- **Severity:** medium.
- **Evidence:** the shared package at `Q-86-synthesis.md:66` says "A genuinely optional new capability or preference is `ScopeExpanded` and is backlogged without enlarging the current family", with no severity qualification; the only severity-sensitive controls in that paragraph are the re-check for a high or critical out-of-scope ruling and the always-in-scope critical rule. Its mapped source is explicit and stricter at `Q-86-state-machine.md:95`: "A low scope-expanded improvement can become `Backlogged(scope_delta_id)` ... A medium, high, or critical scope-expansion proposal goes to the terminal human scope decision rather than silently joining the current task or being automatically backlogged." The synthesis records no such reconciliation: its "Excluded candidates" section at `:336-342` records only the stricter B successor rule as an unselected proposal alternative, and its red-control table exercises only the "Scope-expanded low" row at `:318`, so the medium-and-above case is untested for all three options. The checker models no scope-expansion transition at all.
- **Consequence:** under the synthesis as written, a triager may backlog a medium scope-expansion with neither a re-check nor a human terminal decision, and a high one with a re-check but still no human decision, in a design whose own safety source calls the scope firewall "the most abusable component here" (`Q-86-safety-process.md:253`). This is a real loosening of a control that one source proposal deliberately installed, and because it lives in the shared package it applies to A, B and C alike. Round-1 T17 accepted an express reconciliation of a source disagreement; this one is not express, so a human cannot see that a proposed control was dropped.
- **Smallest correction:** state once in the shared package which rule is selected. Either adopt the source rule ("a medium, high or critical scope-expansion ruling goes to the terminal human scope decision; only a low may be backlogged") or keep the current rule and record the state-machine's severity-escalated variant in "Excluded candidates" as an unselected proposal alternative with its reason. In either case replace the "Scope-expanded low" red-control row with one that also names the medium-and-above path.

---

### R3C-4 — Mode C never reads `--phase`, so C's acceptance factor is asserted rather than established

- **Severity:** low.
- **Evidence:** `q86-controller-proof.py:666-668` passes `phase` to `print` only; `c_edges` and `c_settled` receive `risk` alone, and `c_settled` at `:209-215` requires blind closure purely on `risk != "low_risk"`. By contrast `check_a` at `:638` keys its completion requirement off the phase (`need = 1 if phase == "acceptance" or risk == "low_risk" else 2`). Two consequences reproduce. The published `C phase=acceptance risk=risky` line and the `C phase=work_review risk=risky` line at `Q-86-state-machine.md:451` and `:453` are identical apart from the label: both are `states=794 edges=863 terminal=485 min_reviews=2 max_reviews=4`. And a legal invocation of the published checker, `--mode C --phase acceptance --risk low_risk --floor high`, returns `states=659 edges=711 terminal=387 acyclic=true min_reviews=1 max_reviews=4 ... bad_bound=0`, that is one review batch for an acceptance phase.
- **Consequence:** `Q-86-synthesis.md:218` asserts C's acceptance minimum as "Two batches and three reviewer calls" and `:206` derives the family minimum `c_plan + sum(c_work_q) + 2` from it, while `:240` says "The checker establishes each phase factor". For C the checker establishes a risk factor, not a phase factor, and the acceptance row rests on an unstated premise that an acceptance phase is always risky. The premise happens to hold in the log, so the published numbers are not wrong, but the cited evidence does not support the acceptance-specific claim and a reader can construct a contradicting run from the document's own instructions.
- **Smallest correction:** either state the premise once ("acceptance is always risky, so C's acceptance minimum is the risky value of two batches"), or key `c_settled`'s blind-closure requirement off the phase as `check_a` already does and re-publish the affected outputs and hash.

---

### R3C-5 — C's Q-78 terminal is presented as floor-independent when it is not

- **Severity:** low.
- **Evidence:** `Q-86-synthesis.md:210` states without qualification: "On Q-78, C reaches `SeriousBlocked` at pass three because `Verify2` carries a high." `SeriousBlocked` is reached only when the open finding is at or above the floor: `terminal_control` at `q86-controller-proof.py:110-111` returns `serious_blocked` only when `outstanding_at_floor`, and `at_floor` at `:30-31` compares against the selected `FLOOR`. With `F = critical`, an open high is below the floor, so pass three instead reaches `terminal`, from which `c_edges:264-267` makes `accept_residual` legal. The synthesis presents the floor as an independent co-decision at `:79-86`, and the safety proposal makes exactly this floor-dependence explicit for its own count-budget replay at `Q-86-safety-process.md:371` ("with the terminal floor at `critical` the human would have been offered `accept residual risk` as a legal option in that state").
- **Consequence:** the architecture replay that argues hardest against C is quietly conditioned on the floor the human has not yet chosen. At `F = critical` the same pass-three stop permits shipping with an open high and 23 later valid shortfalls unobserved, which is a materially different and worse outcome than `SeriousBlocked`, and it is invisible in both the synthesis and the ask. The floor recommendation at `:83` is argued from A-shaped evidence only.
- **Smallest correction:** state C's pass-three terminal for both floor values in the same sentence, as the safety proposal's table already does for M1, and carry the `F = critical` variant into the ask's SERIOUS-FLOOR CO-DECISION so the interaction between the two choices is visible.

---

### R3C-6 — The published "Run exactly" blocks export a machine- and session-specific `TMPDIR` that does not exist

- **Severity:** low.
- **Evidence:** `Q-86-synthesis.md:260` and `Q-86-state-machine.md:437` both contain `export TMPDIR=/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q86-synthesis-r2-fix` inside a block introduced by "Run exactly". `ls` on that path returns `No such file or directory` in this worktree. `git log -S 'export TMPDIR=' -- docs/plans/workflow-calibration.explorations/Q-86-synthesis.md` returns exactly `db2ac673 docs: repair Q-86 multi-finding proofs`, so the line is fix-induced in this diff and was not present at the round-2 review. The third published block, `Q-86-safety-process.md:530-539`, has no such export, and `Q-86-safety-process.md:5` asserts "The corrected proof no longer depends on that scratch directory" while `Q-86-state-machine.md:394` says the opposite: "The corrected proof rerun used `/tmp/claude-1000/.../q86-synthesis-r2-fix`".
- **Consequence:** the reproduction instruction a second party is told to run "exactly" points at a per-session scratchpad that exists on no other machine and on this one no longer exists, and two of the three artefacts disagree about whether the proof depends on it. I confirmed the export is currently harmless here (both the checker and a cold `nix shell nixpkgs#hello` still succeed with it set), so this is a durability and hygiene defect in a decision artefact rather than a broken command.
- **Smallest correction:** delete the `export TMPDIR=...` line from `Q-86-synthesis.md:260` and `Q-86-state-machine.md:437`, matching the clean block in `Q-86-safety-process.md`, and drop the scratch-directory sentence at `Q-86-state-machine.md:394` so it agrees with `Q-86-safety-process.md:5`.

---

### R3C-7 — The Q-78 replay emits its summary on a hard-coded pass number rather than at end of input

- **Severity:** low.
- **Evidence:** `q86-q78-scope-replay.sh:37-40` guards the summary with `if [ "$pass" -eq 10 ]`, inside a `while` loop that runs in a pipeline subshell, so the counters cannot be used after the loop. Two reproductions on synthetic logs of the same shape: an eleven-pass input prints `summary passes=10 observed_named_folds=1 ... conditional_families=2` and then continues with `pass=11 ... conditional_terminal=Replanned ... successor=F3` lines that the summary does not count; a nine-pass input prints no summary at all (`grep -c summary` returns `0`).
- **Consequence:** the durable artefact silently produces a mid-stream, undercounted summary if the append-only log ever gains another `q78-design-pass` acceptance record, and no summary at all if the selector ever returns fewer. The synthesis publishes that summary line verbatim at `:305` as the evidence for the conditional four-replan cost, and `Q-86-safety-process.md:13` records that this same selector has already grown once from six passes to ten, so the failure mode is the one the evidence section itself warns about.
- **Smallest correction:** compute the counts in the same process as the summary, for example by dropping the pipeline (`while ... done <<EOF` or a `jq` output captured to a variable) and printing the summary after the loop ends, so it reflects the actual number of selected passes rather than a hard-coded ten.

---

## Checks that found nothing

These were run and produced no finding, and are recorded so the triager can see the covered surface:

- Every published proof and replay output, the checker hash, and the strict render and workflow validation reproduce exactly, as listed above.
- The Option B controller bound holds under adversarial reading: `b_attempt_edges`, `b_repair_edges`, `b_verify_edges` and `b_blind_edges` are each gated on `state.reviews < 4n + 1`, no obligation can take a second reopen (`b_attempt_edges` generation 1 is offered only from `closed0`), and `bad_bound=0` at every published parameter.
- Backstop re-checks debit no review authority in any mode (`a_edges` recheck branch reuses `state.reviews`; `b_recheck_edges` and the `recheck_blind` branch do the same), matching `Q-86-synthesis.md:98`.
- A's reserve control is correct in both directions: dismissal referral preserves `serious_seen` (`q86-controller-proof.py:158-160`), an upheld re-check preserves it (`:183-184`), and an overturned one sets it (`:186`); `bad_upheld_unlock=0`.
- Residual delivery is unconstructible with an outstanding at-or-above-floor finding, a pending re-check, or an `Untested` B obligation, at both floor values; `bad_delivery`, `bad_unverified_delivery` and `bad_critical_clear` are zero throughout.
- The four `19`-rounds, `six retained triages`, `one critical-bearing round` and `one overturned re-check` evidence-limitation bullets at `:33-40` all check out against the log.
- The migration inventory at `:328-334` names only paths that exist: `pack/AGENTS.md`, `pack/instrument.md`, `pack/workflow.toml`, `pack/prompts/{planner,orchestrator,reviewer,triager,implementer}.md`, `.agents/AGENTS.reference.md`, `.agents/LEDGER.template.md`, `.agents/workflow.toml`, `src/workflow_spec.rs::WorkflowSpec`, README and changelog. The plan TOML has eight `[[principle]]` rows, so B's `project_principle` join target exists; it has zero `[[obligation]]` rows, which is correct for an unimplemented schema.
- The no-behaviour-change boundary at `:5` is accurate against the reviewed diff: the only changed files are five planning sources plus the generated plan and the three exploration artefacts. No pack file, prompt, template, README, changelog, metric or Rust source changed.
- The label map at `:13`, the round-1 T16 requirement, is correct against both proposals, including that `Q-86-state-machine.md` still recommends its own Candidate A while the synthesis recommends Option B.
- The ledger resume anchor at `docs/plans/agent-scaffold.ledger.md:535` is current: it records Q-86 as `exploring` on `main` with this branch proposing `open` and under review, which is true.
- I did not raise the structural vacuity of the `bad_direct_campaign`, `bad_historical_credit`, `bad_zero_obligation` and `bad_reopen_before_initial` counters. Each is zero because the transition relation excludes the edge rather than because a mutation was rejected, but round-2 T13 settled that a restriction of the enumerated transition relation is legitimate enforcement, and I have no new evidence against that verdict.
