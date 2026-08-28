# Q-86 synthesis round 4 triage

## Scope and reproduction

I independently read `AGENTS.md`, the triager prompt, the Q-86 brief, both current proposals, the synthesis, the controller proof, the Q-78 replay, the Q-86 plan fold and sidecars, the ledger anchor, every prior Q-86 triage, and both round-4 reviews. The reviewed product is `f696e8b1...976793d1` (product tip `a7ea4f4b` before the round-4 review records), a risky decision artifact. I did not edit product, prior findings, the ledger, or the metrics log.

I reproduced the cited controller paths with `nix shell nixpkgs#python3 -c python3`, including `same_family_successor_authorised=True`; zero transitions that add both `open` and `awaiting_recheck` findings in A, B, or C; the three-obligation initial-priority trace; and A's upheld-dismissal trace. The published all-mode controller run, the live Q-78 replay, and its self-test reproduce. `render --check --strict`, `validate --workflow`, and `git diff --check f696e8b1...HEAD` pass. The passing general checks do not cover the defects below.

The no-relitigation rule is observed. T1 exercises a same-successor-family case absent from round 3's receipt-binding review. T2 adds the valid-plus-dismissed disposition product not covered by the round-3 cross-owner repair. T3, T4, and T5 test behavior introduced by the respective round-3 repairs. T6 concerns repeated fold identity rather than the round-3 selected-length summary defect. T8 and T10 were not previously adjudicated.

## Deduplication and outcome

Twelve raw reports consolidate to ten findings:

- `R4C-1` and `Q86-R4-GPT-3` are T3, B initial-attempt priority.
- `R4C-3` and `Q86-R4-GPT-5` are T5, detached scope routing.

Eight consolidated findings are valid: **two high, three medium, and three low**. Two reports are invalid. No finding is accepted as residual.

**Round outcome: `new_valid`.**

No high- or critical-severity finding was dismissed. **No independent dismissal backstop re-check is owed.**

## Consolidated verdicts

### T1 — B accepts a successor that reuses the immutable predecessor family id

- **Source IDs:** `Q86-R4-GPT-1`.
- **Verdict:** valid, **high**.
- **Reproduced evidence:** The synthesis says scope additions become new receipted families and applies its bound to an immutable `TaskFamilyId` (`Q-86-synthesis.md:64-78`). `successor_authorised` checks receipt bindings but never requires a distinct successor id (`q86-controller-proof.py:622-647`). Constructing terminal predecessor `F1` and a materially different successor also named `F1`, with the receipt bound to `F1`, prints `same_family_successor_authorised=True`. `check_successor`'s advertised wrong-family case changes the receipt predecessor id, not a successor id reused from the predecessor (`:887-921`).
- **Reasoning:** A material successor may receive receipt-origin authority while retaining the identity whose per-family budget is meant to be immutable. This is a reset/laundering edge inside the claimed bounded identity, so the published successor control does not establish a core property of the recommended architecture. It is new evidence beyond round-3 T2's receipt-field repair.
- **Exact correction:** Require every successor id to be fresh relative to its predecessor and all recorded ancestors/family identities, represent the necessary ancestry or no-reuse registry in the prospective rule, and reject reuse mechanically. Add same-family and ancestor-reuse negative cases to `check_successor`; then align the synthesis, human-facing proof claim, and output with the strengthened invariant.

### T2 — The complete-map proof omits a triage batch containing both a valid finding and a serious dismissal

- **Source IDs:** `Q86-R4-GPT-2`.
- **Verdict:** valid, **high**.
- **Reproduced evidence:** The shared package requires an atomic triaged `ReviewBatch` and preserves dismissed serious findings as `AwaitingDismissalRecheck` (`Q-86-synthesis.md:46-60,99`). The checker instead creates valid profiles and dismissal profiles on mutually exclusive edges: A at `q86-controller-proof.py:163-169,192-196`, C at `:267-272`, and B at `:345-362,419-424`. Exhausting the shipped graphs found zero transition that newly adds both dispositions: `A 0`, `B 0`, `C 0`.
- **Reasoning:** A real batch may uphold one report while dismissing a high or critical report in that same batch. The claimed cardinality-two complete-map proof therefore omits a required disposition product, including the interaction between an open repair path and an attached independent re-check. The existing delivery predicates cannot establish preservation of a component the transition relation cannot construct. This is distinct from prior same-owner/cross-owner valid-finding repairs.
- **Exact correction:** Make batch entries carry their triage dispositions and add atomic transitions that retain valid and awaiting-recheck findings together, including owner products and blind closure. Define the permitted follow-on ordering without dropping either component, and exhaust upheld/overturned continuations at both floors and at authority exhaustion for A, B, and C. Extend the arbitrary-finite composition argument to the disposition product.

### T3 — B's initial-attempt-priority control misses an early cross-owner reopen

- **Source IDs:** `R4C-1`, `Q86-R4-GPT-3`.
- **Verdict:** valid, **medium**.
- **Reproduced evidence:** The synthesis promises that every obligation receives its initial authority before a closed one spends reopen authority (`Q-86-synthesis.md:153`). In an initial attempt, `b_valid_batches` defaults to every owner (`q86-controller-proof.py:345-362,421`), and its reducer turns an already `closed0` owner into `open1` (`:371-403`). From three untested obligations, the shipped graph produces `o1_initial_clean -> o2_initial_batch_owned_o1-low_unowned_none -> o1_repair1_joint -> o1_verify1_pass_joint`; immediately before the last action the state is `('pending1', 'closed0', 'untested')` at two reviews. The walk found 324 generation-one verification edges whose source still has an untested obligation, while the action-name filter used for `bad_reopen_before_initial` reports zero (`:952-960`).
- **Reasoning:** A valid incidental finding can consume an already closed owner's one reopen before another frozen obligation receives an initial attempt. The controller therefore contradicts the stated priority rule, and its green counter is structurally blind to the violating edge. The finite spend and no-residual-delivery controls still hold, so this is medium rather than high.
- **Exact correction:** Choose and state one policy. To preserve the published strict priority, defer or terminally route a cross-owner finding against a closed owner until all initial attempts finish, without losing its identity; assert that no state with an `Untested` obligation carries generation-one work. Alternatively retain early incidental reopen as an explicit exception, remove the strict-priority claim from every human-facing surface, and measure that exception with a state predicate rather than action names.

### T4 — An upheld A dismissal loses the prior clean streak and forecloses one batch too early

- **Source IDs:** `Q86-R4-GPT-4`.
- **Verdict:** valid, **medium**.
- **Reproduced evidence:** A all-dismissed, upheld batches are clean under the project convergence rule, but `review_dismissed_*` creates `AState("recheck", reviews, 0, ...)` (`q86-controller-proof.py:163-169`) and `recheck_upheld` then advances only from zero (`:197-201`). The reproduced risky trace ends `review_dismissed_high recheck 5 0` and `recheck_upheld terminal 5 1`, after batch four had already established the first clean batch. It should complete with the second clean batch rather than foreclose.
- **Reasoning:** The green foreclosure check proves consistency with the erased streak, not A's stated complete triage-backed clean-suffix semantics. It affects A risky plan/work review and B's inherited risky plan controller, although not the one-clean acceptance path.
- **Exact correction:** Preserve the incoming streak in a re-check state and advance it only on an upheld dismissal; an overturned dismissal must reset it through the valid-finding path. Add the reproduced batch-five risky trace as a regression requiring `complete`, and rerun A plus inherited B plan review at both serious floors.

### T5 — Scope routing is a detached lookup rather than a controller red-control path

- **Source IDs:** `R4C-3`, `Q86-R4-GPT-5`.
- **Verdict:** valid, **medium**.
- **Reproduced evidence:** `rg -n 'scope_expanded_route|check_scope_controls' q86-controller-proof.py` finds the route function at `:650` and calls only inside `check_scope_controls` (`:924-937`), never from `a_edges`, `b_edges`, or `c_edges`. The check compares its own eight return values to a hard-coded tuple; no scope-expanded finding enters any controller finding map or delivery predicate. This contradicts the claim that the checker explicitly models scope-expansion routing (`Q-86-synthesis.md:239,257`) and the table's controller outcomes (`:345-348`).
- **Reasoning:** The table establishes the selected policy labels, not that a low consumes an opened batch without scope growth, a medium stops the relevant graph, an overturned high returns in scope, or either critical outcome is non-delivering. The selected severity policy from round-3 T4 remains settled; this is new evidence that the round-3 table-only repair does not exercise the policy in a phase controller.
- **Exact correction:** Put a typed scope relation and scope-recheck state into the shared finding/controller transitions and exercise each low/medium/high/critical outcome against A, B, and C delivery and spend predicates. If scope routing is deliberately outside the phase models, narrow the synthesis and red-control claims to a checked policy table and explicitly mark the controller outcomes as unexercised design requirements.

### T6 — The conditional replay counts a repeated reference to one fold as a new family

- **Source IDs:** `Q86-R4-GPT-6`.
- **Verdict:** valid, **low**.
- **Reproduced evidence:** `replay_rows` increments family and replan count for every matching artefact substring without preserving seen fold identities (`q86-q78-scope-replay.sh:18-43`). Its eleven-pass fixture repeats `Q-87 dynamic-selector decision` at passes eight and eleven (`:62-64`) and `--self-test` consequently reports five observed folds and five replans (`Q-86-synthesis.md:330-332`). The live ten-pass result remains correctly four because all four current matches are distinct.
- **Reasoning:** The replay claims to count observed named folds, not mentions. A later append-only record can repeat contextual Q-87 prose, so the current self-test encodes a future overcount of conditional replans, receipts, and families.
- **Exact correction:** Deduplicate stable fold identities before charging a successor (or parse an explicit identity where one is available); a repeated mention must leave the count unchanged. Change the eleven-pass control to expect four folds and use a distinct named fold if testing a fifth.

### T7 — B's Q-78 comparison is not missing from the decision material

- **Source IDs:** `R4C-2`.
- **Verdict:** invalid.
- **Reproduced evidence:** The live replay prints admitted processing for all ten selected passes, with terminal replan plus admitted successor processing at passes two, four, seven, and eight. The synthesis states those four replans and their condition, including that a human refusal stops delivery (`Q-86-synthesis.md:189-193`); the plan and question sidecar link the synthesis and present the conditional cost.
- **Reasoning:** An explicit sentence saying “no selected pass is foreclosed if every successor is approved” would improve scanability, but the cited behavior and the refusal condition are already published and reproducible. The review does not establish a false or decision-blocking omission.
- **Correction:** none required.

### T8 — The retained Q-86 design brief still states the superseded `exploring` status

- **Source IDs:** `R4C-4`.
- **Verdict:** valid, **low**.
- **Reproduced evidence:** The brief's status boundary says “Q-86 is `exploring`” and describes moving it to `open` (`Q-86-convergence-mechanism-brief.md:5`), while the structured question is now `status = "open"` (`agent-scaffold.plan.toml:2560-2562`) and the current planning surfaces point to the completed synthesis. Searching the live plan sources finds no remaining plan pointer to the brief.
- **Reasoning:** The brief is retained as the design-pass criteria source, so its unqualified present-tense status is stale. The lack of a plan pointer after leaving `exploring` is not independently invalid: the workflow only requires that pointer while a question is exploring. It is nevertheless reasonable to retain a provenance link if the brief remains live.
- **Exact correction:** Update the brief's status boundary to record the completed design pass and current `open` decision against `Q-86-synthesis.md`. Optionally restore a provenance link from the owning step while the brief is retained; do not claim that post-exploration linkage is a separate policy violation.

### T9 — The cost-limit wording does not falsely deny the A-versus-C pairwise ranking

- **Source IDs:** `R4C-5`.
- **Verdict:** invalid.
- **Reproduced evidence:** A's maximum is `7(m + 2)` and C's is `4(m + 2)` (`Q-86-synthesis.md:115,205`), while their stated family minima differ by one batch. B's whole-family maximum additionally depends on `|O|`. The reviewer’s arithmetic is correct.
- **Reasoning:** “Whole-task costs cannot be universally ranked” in the ask (`agent-scaffold.plan.toml:2578`) accurately means that no universal ordering across all three options exists because B changes the parameter space. It does not state that A and C are incomparable. Adding the pairwise fact would be useful exposition, but no false human-facing cost claim is established.
- **Correction:** none required.

### T10 — A's minimum-cost explanation introduces undefined `r_q`

- **Source IDs:** `R4C-6`.
- **Verdict:** valid, **low**.
- **Reproduced evidence:** `Q-86-synthesis.md:117` uses `r_q` once, without definition; the immediately following formula and minimum-cost table use `r_plan` and `r_work_q`.
- **Reasoning:** The prose definition cannot be joined unambiguously to its own formula. This is a localized documentation/formula defect.
- **Exact correction:** Replace `r_q` with the appropriate `r_plan` or `r_work_q` terminology and state separately that acceptance is one batch while plan/work use the risk-scaled clean streak; keep the formula and table aligned.

## Verification record

- Reproduced the successor-reuse, mixed-disposition, initial-priority, A streak, detached-scope, and replay-identity evidence cited above.
- Reproduced the live replay and its selected-length self-test; current live result remains four distinct named folds.
- `nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml` — passed.
- `nix develop -c cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` — passed.
- `git diff --check f696e8b1...HEAD` — passed before this triage file was authored.
