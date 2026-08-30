# Option B proof work review round 2 triage

## Scope and reproduction

I independently read `AGENTS.md`, `.agents/prompts/triager.md`, the `bounded-convergence-option-b-proof` sidecar, the proof product, the round-1 triage, and both round-2 reviews. The reviewed product is `main...b8d64178` (the 13 authorised files under `docs/plans/workflow-calibration.proofs/`); the product tree is the same one reviewed as `main...a167d71a`. `git diff --check main...HEAD` passes.

I ran each of the five exact commands in `docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md` from the repository root with an external temporary/cache state directory. All exited 0: both all-suite runs reported nine zero failure counters, algebra printed its five formulas, traceability reported `valid_findings=51 executable_rows=30 resolved_rows=30 exercised_rows=30 killed_rows=30 unresolved=0`, and the manifest reported `discovered_tags=151 mutations=151 unexercised=0 survived=0`. The working tree was unchanged.

For every behavioral claim below, I used a fresh `git archive HEAD` extract under `/tmp`, made only the stated scratch mutation, ran the applicable exact sidecar command(s), and removed the extract. “All five” means the five exact sidecar commands, including the in-process traceability join and manifest-wide mutation command.

## Deduplication and verdicts

### T1 — Completion accepts forged receipt order and state (GPT F1)

- **Verdict and severity:** valid, **critical**.
- **Evidence:** `FrozenFamily._campaign_is_legal` checks summary fields and membership only (`q86-option-b-proof.py:1047-1084`); `complete` consumes that predicate at `:1086-1127` without replaying receipts. In a scratch extract, I constructed each exact phase campaign with `ClosedReopen`, then receipts `blind-closure` followed by `initial-review`. `family.complete(...)` printed `Complete 3`, with every phase receipt order `('blind-closure', 'initial-review')`. Thus no initial verification or reopen/verification receipt was needed for `ClosedReopen`. This reproduces GPT’s command and result.
- **Reasoning:** The product claims receipts derive legal attempt state (`q86-option-b-spec.md:116`), while the central delivery constructor accepts a contradictory product. This can falsely prove the complete-only safety gate.
- **Correction:** Replay a sufficient receipt algebra from the exact campaign initial state and require its derived states, history, closure position, and spend to equal the supplied campaign. Add killing controls for closure-before-initial, closed-reopen-without-reopen/verification, missing/duplicate receipts, and unsupported history changes.

### T2 — Replay equality cannot detect a shared reducer defect (Claude F1)

- **Verdict and severity:** valid, **high**.
- **Evidence:** `check_replay` makes its expected snapshot with `reduce_replay(events)` at `q86-option-b-proof.py:2586-2599`; that is the baseline `reconstruct_replay` path (`:1616-1617`), whose state reducer is also used by every view (`:1591-1613`). Scratch-removing only `self.remaining_authority -= spend` at `:1452` left all five exact commands green, including `151/151` killed mutations. The replay mutations instead drift the already returned snapshot at `:1620-1640`.
- **Reasoning:** Equal results from one faulty reducer do not establish authority conservation or non-replenishment across reconstruction views, contrary to the sidecar’s replay requirement (`bounded-convergence-option-b-proof.md:158,194`). This is new evidence beyond the round-1 self-comparison finding.
- **Correction:** Add an independently computed event-spend/conservation oracle and mutations that alter reduction before snapshot construction. Keep view equality, but do not use it as the only authority derivation.

### T3 — Initial-batch serious referrals are forced through stale closure and have no overturned-repair continuation (GPT F2)

- **Verdict and severity:** valid, **high**.
- **Evidence:** Both campaign re-check methods reject calls before closure (`q86-option-b-proof.py:943-951`), while blind-closure readiness ignores pending scope/dismissal axes (`:955-963`). I reproduced the supplied one-owner high-dismissal scenario: it printed `ClosedInitial AwaitingDismissalRecheck`; pre-closure re-check raised `ValueError: closure dismissal re-check requires closure evidence`; after blind closure and overturn it printed `after True ClosedInitial`; repair raised `ValueError: repair has no unspent attempt authority`; and family completion rejected the live finding. The same construction applies to a high scope referral overturned to `InScope`.
- **Reasoning:** A prior current-owner finding must settle before blind closure, not be terminalised by a closure batch that is stale for it. The missing legal continuation conflicts with the required current-owner/re-check model and named products (`bounded-convergence-option-b-proof.md:84,112,221`).
- **Correction:** Distinguish earlier-batch referrals from closure discoveries. Permit their per-id re-check before closure, open the matching attempt on overturn, require repair and verification, and make blind closure reject every unresolved earlier referral. Retain the non-delivering closure-discovery rule only for `closure_discovery=True` findings.

### T4 — Unchanged replan is not a load-bearing replay check (Claude F2)

- **Verdict and severity:** valid, **medium**.
- **Evidence:** The only distinguishing operation is `unchanged_replan_rejected(state)` at `q86-option-b-proof.py:1610`. Replacing that call with `pass` in scratch left all five exact commands green. The ten view mutations are applied after reconstruction (`:1620-1640`), so none reaches this registry call.
- **Reasoning:** The sidecar requires unchanged replan to exercise the actual no-successor/no-new-authority rule; equality with the baseline cannot cover an omitted operation.
- **Correction:** Make the registry-rejection result an asserted input to the unchanged-replan view and add a mutation that removes or misbinds that call before the snapshot is produced.

### T5 — The CLI floor boundary is observationally inert (Claude F3, GPT F3)

- **Verdict and severity:** valid, **medium**.
- **Evidence:** `run_suite` only assigns `EXECUTION_FLOOR` at `q86-option-b-proof.py:3053-3056`; its meaningful consumer is the complete-gate oracle at `:2650-2671`, which also constructs a critical family unconditionally. Scratch-replacing that assignment with `EXECUTION_FLOOR = "high"` left all five commands green. Separately, replacing `run_suite(args.suite, Floor(args.floor))` at `:3151` with `run_suite(args.suite, Floor.HIGH)` left `--suite all --floor critical` reporting `comparison_floor=critical` with zero counters and left the `151/151` manifest green.
- **Reasoning:** Both command labels are produced from CLI text, but the critical invocation does not independently demonstrate a critical-floor complete model. This fails the stated critical-command contract (`q86-option-b-spec.md:9`).
- **Correction:** Test the CLI-to-suite handoff through `main` or an equivalent boundary oracle, observe a floor-sensitive model made only through that path, and add a mutation for substituting `Floor.HIGH` at the handoff.

### T6 — Arbitrary-history coverage discards the required serious and scope semantics (Claude F4)

- **Verdict and severity:** valid, **medium**.
- **Evidence:** `check_arbitrary_history` extends raw `HistoryQuotient` records and then asserts only count and three ids (`q86-option-b-proof.py:2300-2329`). Changing every `products.json` `history_extensions` row to low/in-scope/valid left all five commands green. No post-history `PhaseCampaign` transition, scope re-check, dismissal re-check, repair, verification, reopen, or delivery check runs.
- **Reasoning:** This does not establish the specified settled-history composition with fresh valid, serious-dismissal, and scope batches (`q86-option-b-spec.md:63-71`; sidecar line 130).
- **Correction:** Drive the parsed extension rows through campaign transitions after settled history and assert their independent route, scope, dismissal, and delivery effects. Add mutations for erasing each mandatory semantic coordinate.

### T7 — Algebra’s required dynamic fixture partition is optional (GPT F4)

- **Verdict and severity:** valid, **medium**.
- **Evidence:** `check_algebra` merely iterates `fixture["finite_cases"]` (`q86-option-b-proof.py:2605-2637`). Setting it to `[]` in scratch left all five exact commands green, while still printing the published formulas and `151/151` mutations.
- **Reasoning:** Zero, one, and several arbitrary named registries are expressly required proof cases, not optional examples. The executable oracle neither requires nor records their semantic coordinates.
- **Correction:** Require and record a semantic partition covering zero obligations/work loops, one loop, several dynamic names, empty/non-empty owners, and nonuniform owner distributions; kill removal of each required coordinate family.

### T8 — The delivery predicate assumes the published maximum bound (Claude F6)

- **Verdict and severity:** valid, **low**.
- **Evidence:** `_campaign_is_legal` embeds `campaign.batches <= 4 * len(expected_keys) + 1` and the related repair cap at `q86-option-b-proof.py:1077-1078`. Removing only those two clauses in scratch left all five commands green. The code therefore does not exercise whether the eligibility bound is independently derived; it makes over-bound traces illegal before a maximum oracle can measure them.
- **Reasoning:** The sidecar requires the `C_q` coefficient to be derived rather than hard-coded. This is a proof-structure defect, but the shipped transition tests still reject no-op/repeated work, so the direct impact is lower than T1.
- **Correction:** Remove the published formula from delivery legality, or derive the constraint from an independently tested transition accounting relation with a dedicated mutation and witness.

### T9 — The cross-credit mutation is killed by an earlier driver crash, not its mandated witness (Claude F7)

- **Verdict and severity:** valid, **low**.
- **Evidence:** Running `run_mutation("mut-algebra-cross-credit")` in scratch returned `(True, True, 'ValueError: scheduled owner is not untested')`, from `drive_maximum_family` re-scheduling an owner already cross-credited. Under the same active mutation, direct `clean_delivering_phase(2)` returned `(2, True, ('O-0-0', 'O-0-1'))`, the required in-domain witness, but it is never reached by `check_algebra` after the driver error. The claimed witness lives at `q86-option-b-proof.py:2634-2637`.
- **Reasoning:** The property exists, but the reported manifest kill proves only a driver failure, not the required `L_q < n_q + 1` assertion.
- **Correction:** Run the witness before the maximum driver or have that driver skip owners already credited, so this mutation dies at the stated minimum assertion.

### T10 — `campaigns.json` attempt names are decorative duplicated literals (Claude F8)

- **Verdict and severity:** valid, **low**.
- **Evidence:** The fixture names `fresh-evidence-reopen`, but the model emits `reopen-review` (`q86-option-b-proof.py:667,906,940`); the fixture is only compared with a duplicated source literal at `:2008-2014`. In scratch, changing all fixture names and that duplicate literal together left the all-suite command and `151/151` manifest green. No `CampaignTransition` can emit the fixture’s original label.
- **Reasoning:** The data is presented as a semantic lifecycle fixture but is not joined to the actual transition model.
- **Correction:** Assert the actual per-obligation transition sequence against the fixture using model transition names, or remove this fixture field and the duplicated assertion.

### T11 — Several specified state fields/helpers are dead (Claude F5)

- **Verdict and severity:** valid, **low**.
- **Evidence:** `history_digest` (`q86-option-b-proof.py:671`) and `maximum_phase_witness` (`:1855`) have no call site; `owner_digest` is set only at `:324`; and `phase_accounts` is written at `:1007` and then only declared at `:1018`. In one scratch extract I renamed both helpers, replaced `owner_digest` with a constant, and replaced phase accounts with `(("DEAD", -999),)`; the all-suite and manifest remained green. `SourceFinding.title` is likewise parsed at `q86-option-b-traceability.py:49,117` but not consumed.
- **Reasoning:** This leaves the specification’s canonical digest, phase-account, and parsed-title claims unproved. It is not a current delivery escape.
- **Correction:** Either remove unused representation from the product/specification or make each claimed authority-bearing value participate in an equality/invariant oracle with a tagged mutation.

### T12 — The public runner deletes caller-owned pre-existing bytecode (GPT F5)

- **Verdict and severity:** valid, **low**.
- **Evidence:** `run_manifest` calls `remove_runner_bytecode` (`q86-option-b-mutations.py:23-31,89-97`). In a fresh scratch archive with `PYTHONDONTWRITEBYTECODE` unset, importing the runner printed `before_call True q86-option-b-mutations.cpython-313.pyc`; a second import followed by `run_manifest("q86-option-b")` printed `after_call False entries 151`. Thus the runner deletes a pre-existing repository artifact before its own before/after check.
- **Reasoning:** The exact commands remain clean because they set the environment flag, but the exposed in-process contract mutates caller-owned planning-tree state, contrary to the no-repository-mutation requirement.
- **Correction:** Do not unlink a caller-owned cache file. Establish bytecode suppression before public-module loading or make the caller-owned loader/cache location explicit and external; add a regression with a pre-existing cache and exact before/after state equality.

## Outcome and counts

- **Raw reviewer findings adjudicated:** 13.
- **Deduplicated findings:** 12 (Claude F3 and GPT F3 are one floor-boundary finding).
- **Valid:** 12 — 1 critical, 2 high, 4 medium, 5 low.
- **Invalid:** 0.
- **Accepted residual risk:** 0.
- **Outcome:** `new_valid`.

## Backstop obligation

No high- or critical-severity finding was dismissed. No independent dismissal re-check is owed. The valid critical and high findings prevent this risky proof increment from counting as a clean review round.
