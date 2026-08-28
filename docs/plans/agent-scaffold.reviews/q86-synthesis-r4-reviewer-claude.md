# Q-86 synthesis round 4 reviewer report (claude)

## Scope and reproduction

Reviewed exact product tip `a7ea4f4b` against `main` (`f696e8b1`), treated as `risky`. Lens: final human decision, executability, and adoption. I read `AGENTS.md`, `.agents/prompts/reviewer.md`, the Q-86 brief, both current proposals, the synthesis, the durable checker and replay scripts, the Q-86 plan fold and its sidecars, the Success Criterion, the generated projection, the ledger resume anchor, and the round-1, round-2 and round-3 reviewer reports and triages. I edited no reviewed product, no prior finding, no metric, and no ledger.

Everything the artefacts publish as evidence reproduces byte for byte in this worktree:

- `Q-86-synthesis.md:281-292` (both `--mode all` runs at `floor=high` and `floor=critical`), `:298-301` (inherited plan controller, risky work foreclosure, low-risk C acceptance) and `:307-310` (B sweep `n = 0..3`) — `diff` against my captured output is empty for all three blocks.
- `Q-86-state-machine.md:455-460`'s six outputs and `Q-86-safety-process.md:553-564`'s two all-mode blocks — reproduce exactly.
- `sha256sum` on the checker returns `b00662359b70139bb1ea670d8ed511caf8a727e6b773b385ab1a31ffd8f8f73c`, matching all three artefacts.
- `q86-q78-scope-replay.sh docs/metrics/workflow.jsonl` returns the published summary at `:325`; `--self-test` returns the two published control lines at `:331-332`.
- The Q-78 selector returns ten passes and `[7,10,5,6,5,5,4,2,1,0]`. Per-pass severities are `medium, medium, high, high, high, high, medium, low, low, none`, so A's "pass seven, three later low shortfalls" (`2+1+0`) and C's "pass three, 23 later shortfalls including further highs" (`6+5+5+4+2+1+0`) are both arithmetically correct.
- The evidence-limitation bullets at `:33-40` check out at `HEAD`: 19 `clean` rounds with `valid_findings > 0`, all 19 advancing `consecutive_clean`; one critical-bearing round; one `dismissal_recheck`, `overturned`; six retained Q-78 triage files. `Q-86-safety-process.md`'s figures pinned at `05142309` also verify at that commit (478 records, 319 rounds, 441 reviewer passes, 360/51/30 harness split, 7 model strings), as do the current 17 escalations (15 decision, 2 resume) and the `26/26` and `29/25` Q-78 attribution totals.
- `nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml` — passed (`up to date`).
- `nix develop -c cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` — passed (481 records; 114 steps; 87 questions; workflow invariants hold).
- `git diff --check main...a7ea4f4b` — clean. No non-ASCII in any changed planning doc.

I verified every round-3 correction landed. T1: cross-owner atomic batches (`b_valid_batches`, `b_reduce_valid_batch`), with `cross_owner_low_critical`, `atomic_cross_owner_low_critical`, `multi_initial_batch` and a bidirectional `bad_owner_state` counter. T2: `SuccessorReceipt` now carries both family ids, both digests, options, chosen successor, spend and carried findings, with ten structured cases and nine negatives. T3: B's plan review explicitly reuses A's controller, `r_plan` is defined, and the ask and sidecar now scope `4n_q + 1` to post-freeze phases. T4: one selected scope policy plus `check_scope_controls`. T5: `CState.phase`, `c_settled`'s acceptance exception and `bad_acceptance_blind_bypass`; `--mode C --phase acceptance --risk low_risk` now reports `min_reviews=2`. T6: `a_cannot_complete` centralises the clean-suffix calculation and `bad_foreclosure_state=0`. T7: both floor outcomes for C are stated in the synthesis, sidecar and ask. T8: no `TMPDIR` export or session scratch path remains in any Q-86 artefact. T9: the replay computes counters in-process and emits exactly one end-of-input summary, with nine- and eleven-pass self-tests.

I also re-derived the arithmetic independently. `R_B = 7 + (4|O| + p) = 4|O| + m + 8`; `4R_B + 6 + 2|O| = 18|O| + 4m + 38`; A's `7(m+2)` batches and `2+1+1` calls per batch plus six repairs give `34(m+2)`; C's `5+4+4+2` gives `15(m+2)`. All four are internally consistent. An independent adversarial sweep of my own (not the shipped assertions) over A at four phase/risk settings, C at three, and B at `n = 0..3`, at both floors, found **zero** reachable `complete` or `delivered_residual` state carrying an outstanding finding, an `untested` obligation, or a non-closed obligation, and confirmed B's `min_complete = n + 1` and `max_reviews <= 4n + 1` at every `n`.

I re-raise no settled finding. Each finding below cites text or code that the round-2 or round-3 repair introduced and that no prior round adjudicated; provenance is given per finding.

## Result

**Six findings: zero critical, zero high, two medium, four low.**

There are **no `critical` findings and no `high` findings**. The controllers, their bounds, the unresolved-critical invariant, the successor and legacy controls, the conditional replay, and the reproducibility of every published command all survive adversarial re-execution.

---

### R4C-1 — B's stated initial-attempt-priority invariant is falsified by the shipped controller, and the counter presented as establishing it is blind to the path the round-3 repair added

- **Severity:** medium.
- **Provenance:** `bad_reopen_before_initial` was added by `3db0f2bd`; cross-owner batches (`b_valid_batches`) were added by `7905237c`, the round-3 repair. The interaction is new in this round's tip.
- **Evidence:** `Q-86-synthesis.md:153` asserts two things: "Initial attempts have priority over optional reopen discovery. **Every obligation therefore receives its initial authority before a closed obligation can spend reopen authority.**" `Q-86-safety-process.md:323` repeats it: "Every obligation receives its initial attempt before any closed obligation may spend optional reopen authority." The shipped controller permits the opposite. `b_reduce_valid_batch` at `q86-controller-proof.py:388-390` moves any batch-named owner sitting at `closed0` to `open1` with `origin = "reopened"`, and `b_attempt_edges` at `:421` builds those batches from `b_valid_batches(state, index)`, which at `:347` defaults `owner_indices` to **every** obligation, not just untested ones. So an initial batch whose primary is `Untested` can reopen an already-`Closed` obligation while a third obligation has never been examined.

  The shipped `bad_reopen_before_initial` counter at `:952` matches only actions containing `material_new_evidence`, `reopen_clean` or `reopen_batch`. The offending action is named `o2_initial_batch_owned_o1-low_unowned_none`, so the counter cannot see it and reports `0`. Reproduce from the repository root:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3 - <<'PY'
  import importlib.util
  from collections import deque
  p='docs/plans/workflow-calibration.explorations/q86-controller-proof.py'
  sp=importlib.util.spec_from_file_location('q',p); q=importlib.util.module_from_spec(sp); sp.loader.exec_module(q)
  start=q.BState('work:probe',('untested',)*3,0,'active',())
  prev={start:None}; todo=deque([start]); seen={start}; edges=[]
  while todo:
      s=todo.popleft()
      for a,t in q.b_edges(s):
          edges.append((s,a,t))
          if t not in seen: seen.add(t); prev[t]=(s,a); todo.append(t)
  hits=[(s,a,t) for s,a,t in edges if 'verify1_' in a and 'untested' in s.obligations]
  print('reopen-generation verification batches spent while an obligation is Untested:', len(hits))
  print('shipped bad_reopen_before_initial:',
        sum(1 for s,a,t in edges
            if ('material_new_evidence' in a or 'reopen_clean' in a or 'reopen_batch' in a)
            and 'untested' in s.obligations))
  s,a,t=sorted(hits,key=lambda e:e[0].reviews)[0]
  path=[]; n=s
  while prev[n] is not None:
      src,act=prev[n]; path.append(act); n=src
  print(' -> '.join(reversed(path)), '->', a)
  print('source obligations', s.obligations, 'reviews', s.reviews)
  PY
  ```

  It prints:

  ```text
  reopen-generation verification batches spent while an obligation is Untested: 324
  shipped bad_reopen_before_initial: 0
  o1_initial_clean -> o2_initial_batch_owned_o1-low_unowned_none -> o1_repair1_joint -> o1_verify1_pass_joint
  source obligations ('pending1', 'closed0', 'untested') reviews 2
  ```

  The same walk finds 70 `initial_batch` edges at `n = 3` that reopen a `closed0` owner while another obligation is still `Untested`, and 1358 reachable states holding an active generation-1 obligation alongside an `Untested` one. On that four-step path `o1` — an already-closed obligation — is reopened, repaired, and consumes its generation-1 **verification review batch**, exhausting its single reopen allowance, before `o3` has received any attempt at all.
- **Consequence:** three separate claims are wrong or unsupported. (1) `Q-86-synthesis.md:153` sentence two and `Q-86-safety-process.md:323` are false against the artefacts' own durable proof. (2) `Q-86-synthesis.md:253` ("B optional reopen discovery never precedes all initial attempts") and `Q-86-safety-process.md:398` (which lists "reopen-priority" among the controls the checker establishes at both floors) rest on a counter that is structurally incapable of observing the path, so the property is asserted rather than established for the transition relation as it now stands. (3) `Q-86-synthesis.md:362` schedules "enforces initial-attempt priority" as a mechanical `validate --workflow` rule, and the same claim is carried into four human-facing surfaces — `docs/plans/agent-scaffold.plan.toml:2571` ("gives initial attempts priority over optional reopen work"), `docs/plans/agent-scaffold.questions/Q-86.md:10`, `docs/plans/agent-scaffold.steps/workflow-calibration.md:20`, and `docs/plans/agent-scaffold.success-criteria.md:41` — plus the generated projection at `docs/plans/agent-scaffold.md:179`. An implementer told to enforce strict priority would build a scheduler the reference controller contradicts, and would reject a batch the model calls legal. A second, quieter effect for the human: a valid finding raised incidentally against a closed obligation silently burns that obligation's one reopen, outside the `MateriallyNewEvidence` gate that `:146` presents as the only route into a reopen. The per-family bound is unaffected (`4n_q + 1` is exactly four transitions per obligation plus blind closure, so no obligation can starve another, and my independent sweep confirms `bad_bound = 0` and no unsafe delivery), which is why this is medium and not high.
- **Smallest correction:** decide and state which is true. Either (a) restrict `b_valid_batches` in `b_attempt_edges` generation 0 to owners that are not yet `Closed`, so a cross-owner batch can only satisfy other **initial** attempts, and keep the prose as written; or (b) keep the broader batch and correct `Q-86-synthesis.md:153` and `Q-86-safety-process.md:323` to say that only the *discretionary* reopen-discovery batch is deferred, while an incidental cross-owner finding may open a closed obligation's reopen generation early and consume it. Either way, widen `bad_reopen_before_initial` to a state predicate — no state with an `untested` obligation may hold any generation-1 obligation stage — rather than an action-name filter, republish the affected outputs and hash, and align the four human-facing surfaces and the `validate --workflow` inventory with whichever rule is selected.

---

### R4C-2 — The Q-78 late-discovery comparison is quantified for A and C and left blank for the recommended option B

- **Severity:** medium.
- **Provenance:** the A and C figures were added by the round-1 repair; the B replay was added by the same repair but only ever reported as cost. Nothing in rounds 1-3 adjudicated the asymmetry.
- **Evidence:** the ask gives Option A "On Q-78 A stops at pass seven and leaves three later low shortfalls undiscovered" (`docs/plans/agent-scaffold.plan.toml:2565`) and Option C "On Q-78 C stops at pass three and leaves 23 later shortfalls undiscovered, including further highs" (`:2567`). Option B's Q-78 sentence at `:2566` reports only cost: "four terminal replans, four additional receipts, and four additional plan-review and freeze campaigns." The question sidecar repeats exactly the same three-way shape at `docs/plans/agent-scaffold.questions/Q-86.md:8`, and `Q-86-synthesis.md:398` bakes the asymmetry into the mandated presentation: it requires A's pass-seven terminal and three shortfalls, C's pass-three outcome under both floors, and for B only "the conditional four-replan scenario".

  The durable replay supplies the missing side and is not published. `docs/plans/workflow-calibration.explorations/q86-q78-scope-replay.sh docs/metrics/workflow.jsonl` emits fourteen event lines before its summary; every one of the ten passes carries `conditional_review=admitted` or `review=admitted`, and no pass emits a foreclosure or exhaustion event. `Q-86-synthesis.md:322-326` and `Q-86-safety-process.md:578-584` publish only the one-line summary, so the per-pass admissions never reach the reader. `Q-86-synthesis.md:193` does record the countervailing condition — "If the human refused any successor, delivery would stop at that fold" — but that sentence appears in neither the ask nor the sidecar.
- **Consequence:** the artefact's own decisive axis, how much late discovery each architecture forecloses, is priced for two options and blank for the third, which happens to be the recommendation. A human reading the ask sees "A loses 3, C loses 23, B costs four replans" and cannot tell that under the same stated assumptions B forecloses no pass at all, nor that B's full admission is contingent on the human approving four successors and collapses to a stop-at-the-fold if any one is refused. Both halves matter: the first is the strongest argument for the recommended option and is missing, the second is the recommendation's sharpest conditional risk and is also missing. This is a decision-adequacy defect in the presentation the orchestrator is instructed to give, not an error in the underlying replay.
- **Smallest correction:** add one sentence to Option B in `docs/plans/agent-scaffold.plan.toml:2566` and to `Q-86.md:8` stating B's Q-78 discovery outcome on the same axis as A and C — under the four stated digest assumptions B forecloses none of the ten passes, at the price of four human successor decisions, and delivery stops at the first fold whose successor the human refuses — and add the same requirement to the presentation list at `Q-86-synthesis.md:398`. Publishing the replay's per-pass `admitted` lines beside the existing summary would make the claim reproducible from the artefact rather than only from the script.

---

### R4C-3 — The scope-expansion "red control" is a self-referential test of a function no controller calls

- **Severity:** low.
- **Provenance:** `check_scope_controls` and `scope_expanded_route` were added by `7905237c`, the round-3 repair for T4. T4 settled *which* policy is selected; this is new evidence about how the repair proves it.
- **Evidence:** `grep -n 'scope_expanded_route' docs/plans/workflow-calibration.explorations/q86-controller-proof.py` returns the definition at `:650` and exactly eight call sites, all inside `check_scope_controls` at `:925-932`. There is no call site in `a_edges`, `b_edges` or `c_edges`, no scope-expanded finding ever enters a `Finding` tuple, and no `awaiting_scope_recheck` or scope-derived `serious_blocked` state is reachable in any of the three graphs. `check_scope_controls` at `:933-936` compares the function's eight return values against a hard-coded `expected` tuple that restates the function's own four branches, then asserts the difference is zero.
- **Consequence:** `Q-86-synthesis.md:239` says the checker "explicitly models ... scope-expansion routing" and `:257` lists "Scope-expanded low, medium, high, and critical cases follow the selected severity policy" among the checks; `Q-86-safety-process.md:398` lists "scope-route" among the controls established at both floors. What is actually established is that a four-branch lookup table returns the four values the same file expects it to. The per-option red-control rows at `Q-86-synthesis.md:345-348` go further and claim behaviour the test cannot reach: "either result is `SeriousBlocked` and **cannot backlog or deliver**", "cannot add an obligation", "cannot add a node". Because no scope-expanded finding is ever represented in a controller's finding map, no delivery predicate in the checker ever sees one, and the interaction between an out-of-scope critical and a phase that is otherwise completable is unmodelled — the graphs still reach `complete` with such a finding notionally outstanding. This differs from the vacuity round-2 T13 accepted: those counters are zero because the enumerated transition relation excludes the edge, whereas here there is no scope transition in any relation to restrict.
- **Smallest correction:** either wire the routing into the controllers, so a scope-expanded finding enters the finding map with a scope relation and the existing `bad_delivery` / `bad_critical_clear` predicates cover the always-safety-blocking critical rule; or, if the routing is deliberately kept outside the phase models, say so at `Q-86-synthesis.md:239` and `:257` and at `Q-86-safety-process.md:398` — the checker encodes the selected policy table and does not exercise it against any A, B or C delivery predicate — and mark the three "cannot backlog or deliver" cells in the red-control table as design claims rather than checked ones.

---

### R4C-4 — Moving Q-86 to `open` left the design brief asserting `exploring` and removed its last pointer from the plan

- **Severity:** low.
- **Provenance:** the step sidecar's brief pointer was dropped by `604c9578`, the first synthesis commit; the status became false in the same commit. Never raised.
- **Evidence:** `docs/plans/workflow-calibration.explorations/Q-86-convergence-mechanism-brief.md:5` still reads "Q-86 is `exploring`. ... the orchestrator synthesises them, moves Q-86 to `open`, and presents the viable options to the human." This change set sets `status = "open"` at `docs/plans/agent-scaffold.plan.toml:2561` and updates the question sidecar, the step sidecar and the Success Criterion to match, so the brief is the one surviving statement of the superseded status. Separately, `grep -rn "Q-86-convergence-mechanism-brief" docs/plans/agent-scaffold.plan.toml docs/plans/agent-scaffold.questions/ docs/plans/agent-scaffold.steps/ docs/plans/agent-scaffold.success-criteria.md docs/plans/agent-scaffold.md` now returns nothing, where `git show main:docs/plans/agent-scaffold.plan.toml | grep -c` returns `1` and `git show main:docs/plans/agent-scaffold.md | grep -c` returns `4`. The only remaining reference anywhere under `docs/` is inside `q86-synthesis-r1-reviewer-claude.md`, a transient findings file on the commit-before-delete path. This is not a case of a frozen historical record: the same change set rewrote both explorer proposals (`Q-86-state-machine.md`, `Q-86-safety-process.md`) rather than leaving them at their authored state, so exploration artefacts here are maintained, and `AGENTS.md:65` only lapses the *pointer* obligation when the item leaves `exploring`, not the currency obligation on the file itself.
- **Consequence:** the brief remains the criteria source against which this design pass's required outputs, proof obligations, red controls and YAGNI boundary are judged — this round's own reviewer instruction names it — yet it is now reachable only by directory listing, and the first thing it tells a reader is a status the same change made false. `docs/plans/agent-scaffold.steps/workflow-calibration.md:22` asserts "no shipped prompt or product documentation becomes stale now", which is true as written and leaves this planning-record staleness unaccounted for.
- **Smallest correction:** update `Q-86-convergence-mechanism-brief.md:5` to record that Q-86 is now `open` against `Q-86-synthesis.md` and that the design pass it specifies is complete, and restore one path reference to the brief in `docs/plans/agent-scaffold.steps/workflow-calibration.md:20` so the criteria source stays reachable from the plan until the orchestrator's cleanup decision is taken.

---

### R4C-5 — The ask's cost paragraph denies a whole-task ranking that does hold between A and C

- **Severity:** low.
- **Provenance:** the COST LIMIT wording was introduced by `3db0f2bd`. Round-1 T11 settled that the *previous* wording ("Option C has the lowest maximum cost") over-claimed a universal; this is new evidence that the replacement over-corrects in the other direction.
- **Evidence:** `docs/plans/agent-scaffold.plan.toml:2578` (projected verbatim at `docs/plans/agent-scaffold.md:179`) states: "Whole-task costs cannot be universally ranked because B scales with both `|O|` and the number `m` of work loops, while A and C scale with `m` and phase risk." Both halves of the A-versus-C comparison are in fact universal. From `Q-86-synthesis.md:115` and `:205`, A's family maximum is `7(m + 2)` and C's is `4(m + 2)`, so C's ceiling is strictly lower for every `m >= 0`. From `:117` and `:207`, A's family minimum is `r_plan + sum(r_work_q) + 1` and C's is `c_plan + sum(c_work_q) + 2`, and `:117` and `:207` give the `r` and `c` values the same definition (one at low risk, two at risky), so C's floor is exactly one batch higher than A's for every risk profile. The synthesis body's own sentence is correctly narrow and does not make this mistake: `:211` says C "does not have a universally lowest whole-task call bound **because B scales in different parameters**".
- **Consequence:** the human is told no whole-task cost ranking exists, when in fact the only genuinely incomparable pairs are the two involving B, and the crisp A-versus-C fact — C is always cheaper at the ceiling and always one batch dearer at the floor — is available and useful for exactly the ceiling-versus-floor trade-off the ask is asking them to make. The ask also omits A's `7(m + 2)` and C's `4(m + 2)` family maxima entirely while giving B's `4|O| + m + 8`, so a reader working only from the ask cannot recover the comparison for themselves.
- **Smallest correction:** in `docs/plans/agent-scaffold.plan.toml:2578`, narrow the claim to the pairs it is true of and state the A-versus-C ranking, for example: "C's family maximum `4(m + 2)` is below A's `7(m + 2)` for every `m`, while C's family minimum is one batch above A's; only the pairs involving B are unrankable, because B's `4|O| + m + 8` scales in `|O|` as well as `m`." Then re-render.

---

### R4C-6 — A's minimum-cost sentence uses an undefined symbol `r_q`

- **Severity:** low.
- **Provenance:** introduced by `3db0f2bd`. Never raised.
- **Evidence:** `Q-86-synthesis.md:117` reads "A's minimum is one batch for acceptance and the required clean streak `r_q`, one for low-risk plan or work review and two for risky plan or work review, for every other phase." `grep -n 'r_q\|r_work_q\|r_plan' docs/plans/workflow-calibration.explorations/Q-86-synthesis.md` shows `r_q` occurring exactly once, at `:117`, and never being defined; the family formula in the very next clause and the minimum-cost table at `:220` both use `r_plan` and `r_work_q` for the same quantities.
- **Consequence:** the one sentence that defines A's per-phase minimum introduces a symbol that appears nowhere else and is not the symbol the published formula uses, so a reader pricing A cannot join the sentence to `r_plan + sum(r_work_q) + 1`. B's corresponding definition at `:159` is explicit ("If `r_plan` is the inherited A-controller plan-review minimum, one for low-risk plan review and two for risky plan review"), which makes the A side the odd one out in the same comparison.
- **Smallest correction:** replace `r_q` at `:117` with `r_work_q`, and rephrase so the acceptance value and the per-phase value are separable, for example: "A's minimum is one batch for acceptance, and for every plan or work phase the required clean streak `r_plan` or `r_work_q`, which is one at low risk and two at risky."

---

## Checks that found nothing

Run and recorded so the triager can see the covered surface.

- Every published proof and replay output, the checker hash, strict render and workflow validation reproduce exactly, as listed in the scope section. `git diff --check main...a7ea4f4b` is clean and no changed planning doc contains non-ASCII.
- An **independent** adversarial delivery sweep, using my own predicate rather than the shipped assertions, over A (`acceptance/risky`, `plan_review/risky`, `plan_review/low_risk`, `work_review/risky`), C (`acceptance/risky`, `acceptance/low_risk`, `work_review/low_risk`) and B (`n = 0..3`), at **both** floors: zero reachable `complete` or `delivered_residual` state carries an outstanding finding, an `untested` obligation, or a non-closed obligation. B's `min_complete` is exactly `n + 1` at every `n` and `max_reviews` never exceeds `4n + 1`. C's acceptance `min_complete` is 2 at both risks with zero completions that skipped `BlindClosure`; C's low-risk work review reaches six such completions, which is the documented low-risk discovery exit, not a defect.
- A's foreclosure repair is sound, not merely non-violating: `a_clean_needed` correctly returns the full `need` at `repair` and `verify` (where the streak is always zero by construction) and `need - streak` at `active`, and `a_open`/`a_settled` divert to `terminal` before constructing an unattainable state, which is why `bad_foreclosure_state = 0` and the `foreclose_before_*` edges are unreachable. That is an implementation choice, not a gap.
- Backstop re-checks debit no authority in any mode and remain reachable at exhaustion: `a_edges`'s `recheck` branch and `b_edges`'s `recheck` dispatch both bypass every `reviews < limit` gate and reuse `state.reviews`, matching `Q-86-synthesis.md:99`.
- A's reserve control holds in both directions: dismissal referral preserves `serious_seen` (`:169`), `recheck_upheld` preserves it (`:199`), `recheck_overturned` sets it (`:201`); `bad_upheld_unlock = 0` at both floors.
- The `4n_q + 1` allocation is exactly attainable and exactly sufficient: each obligation has precisely four review-consuming transitions and no second reopen (`closed1` targets go to `open_exhausted` and terminate), so cross-owner batches can only reduce realised spend. I traced a completing `n = 1` path that reaches the full five batches.
- `accept_residual` is unconstructible for B while any obligation is `Untested` (`:550-553`), and `legal_critical_clear` (`:670-679`) omits `accept_residual`, so an outstanding critical can leave the map only via named verification, an upheld re-check, or a non-delivery terminal — `bad_critical_clear = 0` throughout.
- The successor oracle is now substantive rather than tautological: `successor_authorised` (`:622-647`) conjoins eighteen conditions and `check_successor` publishes nine negative cases (same scope, reordered scope, missing receipt, missing options, wrong family, wrong predecessor digest, wrong successor digest, missing carry, fresh authority) plus a predecessor-immutability check. All reproduce.
- The replay's R3C-7 repair is real: `replay_rows` reads from a here-document rather than a pipeline, so the counters survive the loop, and the summary is emitted once after EOF from the actual `passes` and `family` values (`q86-q78-scope-replay.sh:14-43`). The nine- and eleven-pass self-tests assert exactly one summary line via `awk`.
- Source map at `Q-86-synthesis.md:13` is correct against both proposals, including that `Q-86-state-machine.md:369` still recommends its own Candidate A while the synthesis recommends B, and that M3 is excluded in `Q-86-safety-process.md:404`.
- Every path in the migration inventory at `:358-364` exists: `pack/{AGENTS.md,instrument.md,workflow.toml,LEDGER.template.md,plan-template.plan.toml}`, `pack/prompts/{planner,orchestrator,reviewer,triager,implementer}.md`, `AGENTS.md`, `.agents/{AGENTS.reference.md,LEDGER.template.md,workflow.toml,prompts/}`, `README.md`, `CHANGELOG.md`, `src/workflow_spec.rs`.
- The no-behaviour-change boundary at `:5` is accurate against the reviewed diff: the only changed files are five planning sources, the generated plan, three exploration artefacts and two proof scripts. No pack file, prompt, template, README, changelog, metric record or Rust source changed.
- The ledger resume anchor at `docs/plans/agent-scaffold.ledger.md:535` remains true on `main` ("Q-86 remains `exploring` on `main`; branch ... proposes moving it to `open` and is under review"); the status move there is the orchestrator's merge-time job, which round-1 T12 already assigned.
- Implementation sequencing is coherent: `Q-86-synthesis.md:400` defers ordering to a later planner fold and requires the chosen mechanism to land after the shared typed reconstruction; `review-loop-foreclosure-enforcement` (order 112) and `workflow-driver-typed-fleet` (order 115, blocked on it) both exist and are `not-started`, so the constraint is expressible when that fold is authored. I did not raise the fact that the owning `workflow-calibration` step is order 35 and unblocked, because no implementation step exists yet to order.
- I considered, and did not raise, the thinness of A's and C's legacy-adoption treatment relative to B's. The synthesis compresses the sources' fuller adoption paragraphs (`Q-86-state-machine.md:252` and `:350`) into one principle-table cell each plus one red-control row each, but "Digest adoption can charge old spend and fail loudly" and "Historical stage adoption is ambiguous and must fail to a human" (`:230`) do carry the decision-relevant risk without being false, and B needs the extra `LegacyNoRubric` machinery precisely because it needs a frozen `O` that A and C do not.
- I did not re-raise the structural vacuity of `bad_direct_campaign`, `bad_historical_credit`, `bad_zero_obligation`, or the obligation-index symmetry reduction (`untested[0]`, `closed0[0]`, `special[0]`). Round-2 T13 settled that a restriction of the enumerated transition relation is legitimate enforcement, the reduction is permutation-sound for the properties checked, and I have no new evidence against either verdict. R4C-3 is raised as distinct because `scope_expanded_route` is not a restriction of any transition relation — no controller calls it.
