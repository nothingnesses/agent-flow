# Option B proof work review round 1 triage

## Scope and reproduction

I independently read `AGENTS.md`, `.agents/prompts/triager.md`, the `bounded-convergence-option-b-proof` sidecar, all 13 proof artefacts and eight fixtures, the retained Q-86 synthesis triages `q86-synthesis-r1-triage.md` through `q86-synthesis-r5-triage.md`, and both round-1 reviewer reports. The reviewed product is `main...848de2c3` (the 13 new files under `docs/plans/workflow-calibration.proofs/`). `git diff --check main...HEAD` passes.

I ran the five exact sidecar commands twice from the repository root, each invocation with a distinct external temporary directory for temporary and cache variables. The two passes had byte-identical stdout, stderr, and exit status: high all-suite `0`, critical all-suite `0`, algebra `0`, traceability `1`, and manifest-wide mutations `0`. The traceability failure was `ValueError: unresolved durable pointer: R1-T12`; the other outputs reported zero suite failures and `discovered_tags=129 mutations=129 unexercised=0 survived=0`. `git status --porcelain=v1 --untracked-files=all` and a complete non-Git path/type/content manifest were byte-identical before and after all ten invocations.

Every source mutation and scratch demonstration below was run in a fresh `git archive HEAD` extract outside the repository, using the locked Nix Python already resolved by the exact commands. Those extracts were removed after testing.

## Deduplication and verdicts

### T1 — R1-T12 makes the required traceability command fail and ties it to mutable ledger text

- **Source IDs:** Claude F1; GPT F1.
- **Verdict and severity:** valid, **high**.
- **Reproduced evidence:** The matrix row at `docs/plans/workflow-calibration.proofs/q86-option-b-traceability.md:19` names `docs/plans/agent-scaffold.ledger.md#OPTION B PROOF IMPLEMENTATION IN PROGRESS`; the current ledger anchor at `docs/plans/agent-scaffold.ledger.md:535` contains `OPTION B PROOF WORK REVIEW ROUND 1 READY` instead. Both exact traceability passes consequently exit 1 at `q86-option-b-traceability.py:277`. Replacing only that scratch matrix pointer with the stable sidecar sentence beginning `Advancing the ledger's authoritative resume anchor is an orchestrator integration duty` makes the exact command pass with `valid_findings=51 executable_rows=30 resolved_rows=30 exercised_rows=30 killed_rows=30 unresolved=0`.
- **Reasoning:** Criteria 11 and 13 require this gate to pass. The ledger resume anchor is orchestrator-owned transient state, so simply updating the needle to its current wording would recreate the same breakage.
- **Exact correction:** Point R1-T12 to the stable planning-sidecar statement that records the ledger duty, not a live ledger-anchor phrase; optionally reject the ledger as a `durable-text` target in the checker. Rerun the ten-command repeatability check and update the ledger's false all-green summary.

### T2 — The family delivery gate trusts forgeable campaign summaries and does not exercise its finding-map blocks

- **Source IDs:** Claude F2; GPT F3.
- **Verdict and severity:** valid, **critical**.
- **Reproduced evidence:** `FrozenFamily.complete` at `q86-option-b-proof.py:831-849` checks only phase names plus each supplied campaign's `completed` and `blind_closure_spent` flags. A scratch source mutation replacing the finding-map predicate at `:845` with `allowed = exact and all_closed` leaves the full all-suite green. A separate scratch caller constructs empty `PhaseCampaign` instances with those two flags set for each frozen phase; `family.complete(...)` returns `Complete` with three frozen obligations and zero campaign owner keys. A source mutation that makes live completed-prior, future, and unowned routes non-blocking also leaves the suite green.
- **Reasoning:** The sidecar and spec require completion to reject unexamined frozen obligations and every live out-of-phase, unowned, carried, or pending-recheck component. The executable delivery constructor accepts a fabricated product instead. This is the core safety property that the proof is intended to establish.
- **Exact correction:** Bind a campaign to its family/freeze identity and have `complete` verify exact owner-key equality, legal settled attempt state for every frozen obligation, closure evidence, and merged-history delivery blocks rather than trusting public booleans. Add independent negative family-completion cases and mutations for live current, completed-prior, future, unowned, carried, scope-pending, and dismissal-pending components; each must reach the delivery constructor and be rejected.

### T3 — The algebra formulas, witnesses, and algebra output are disconnected from bounded transition execution

- **Source IDs:** Claude F3, Claude F8; GPT F2.
- **Verdict and severity:** valid, **high**.
- **Reproduced evidence:** `derive_bounds` assigns `l_q = n_q + 1` and `c_q = 4 * n_q + 1` directly at `q86-option-b-proof.py:1233-1234`; `clean_delivering_phase` at `:1262-1277` is a string/list counter, not a `PhaseCampaign` execution. Activating `mut-algebra-cross-credit` shortens that helper to two batches but leaves a real two-owner `PhaseCampaign.initial_batch` with B still `Untested`. The required in-domain campaign/family witness is absent. More seriously, a real one-obligation campaign can perform 100 empty `verify(())` transitions, then verify the selected finding and blind-close: it constructs `Complete` with `batches=103` although the published `C_q` is 5. Repeated repair calls are also accepted while the finding remains `REPAIR_PENDING`. The actual initial/verify/reopen/verify/blind-closure lifecycle instead records four batches because `reopen` itself does not spend one. Finally, changing the literal algebra output from `formula L_q=n_q+1` to `formula L_q=bogus` leaves the algebra suite green, confirming that the printed contract is not derived output.
- **Reasoning:** A claimed maximum cannot be established by a helper that is disconnected from transitions while the actual transition API admits arbitrarily many no-op verification batches. This violates the sidecar's explicit requirement to derive every coefficient and to retain the two-owner cross-credit witness inside the ordinary-delivery domain.
- **Exact correction:** Make repair and verification consume only legal, non-empty, exact selected work and reject no-op/repeated spending; count every review-bearing transition consistently, including reopen if it is a review batch. Derive minima and maxima from actual campaign executions that construct `Complete`, including the specified two-owner cross-credit mutant. Compute the printed formulas, premise list, and early-path report from those checks rather than hard-coded strings; withdraw any coefficient the transition model cannot establish.

### T4 — The replay oracle is self-comparison rather than independent reconstruction

- **Source IDs:** Claude F4.
- **Verdict and severity:** valid, **high**.
- **Reproduced evidence:** `replay_view` at `q86-option-b-proof.py:1172-1193` invokes the same `reduce_replay(events)` for every named view and only changes which self-injected mutation tag it applies. `check_replay` at `:1861-1869` compares those results to another `reduce_replay(events)` result. Replacing the replay fixture's ten events with `[]` in scratch leaves the full suite green. The reported field/replenishment mutations are killed because they deliberately alter the result immediately before equality with an unaltered copy, not because resume, rename, rebuild, or unchanged replan reconstruct authority independently.
- **Reasoning:** The proof does not establish that any actual reconstruction view preserves family identity, spend, evidence, routes, terminal state, or non-replenishment. This is a required acceptance property, not a presentation-only issue.
- **Exact correction:** Implement distinct baseline, serialized-resume, rename, rebuild, and unchanged-replan reconstruction paths over the canonical event stream. Derive the compared fields from state/events rather than constants and compare cross-path results. Make unchanged replan exercise the actual successor/no-new-authority rule; keep a mutation only when that independent comparison kills it.

### T5 — The named fixtures are largely labels or scalar mirrors, not executable inputs

- **Source IDs:** Claude F5.
- **Verdict and severity:** valid, **medium**.
- **Reproduced evidence:** In independent scratch copies, removing every `scheduled_owner` and `findings` body from `products.json`, every `obligations` body from `campaigns.json`, `families` from `successors.json`, or `forbidden` from `legacy.json` each leaves the all-suite green. The corresponding checks consume only names, attempt-list lengths, or hand-built Python values (`q86-option-b-proof.py:1391-1394`, `:1427-1475`, `:1659-1718`, and `:1772-1804`).
- **Reasoning:** This does not prove the fixture claims in the sidecar, especially its named atomic/product cases. A future fixture addition or correction can have no executable effect.
- **Exact correction:** Parse and drive the fixture bodies through the real model, asserting the resulting owner, finding, route, and terminal states. Extend those data-driven cases to every named sidecar product. Remove any fixture field that deliberately has no semantic role instead of presenting it as proof input.

### T6 — `--floor` does not run a critical-floor family model

- **Source IDs:** Claude F6.
- **Verdict and severity:** valid, **medium**.
- **Reproduced evidence:** `run_suite` accepts only `suite` at `q86-option-b-proof.py:2167`; `main` uses the parsed floor only to select its printed label. `FreezePending.freeze` hard-codes `selected_floor=Floor.HIGH` at `:805`. A scratch mutation that reverses the label predicate reverses `selected_floor` and `comparison_floor` in output while both all-suites remain green. Thus no `FrozenFamily` or `Complete` is constructed under `critical`.
- **Reasoning:** The second exact all-suite command presently adds only a label, while the sidecar requires the `critical` comparison model to execute. This does not invalidate the separately tested terminal-choice table, but it leaves the stated full-model comparison unproved.
- **Exact correction:** Thread the parsed floor through model construction and suite execution. Exercise a normally completing critical-floor family and critical-specific terminal choices; preserve the selected high default. Do not make a live carried finding deliver merely to create a floor distinction: the selected model requires carried components to remain live until settled.

### T7 — Deferred reopen and one-reopen controls are write-only or untested

- **Source IDs:** Claude F7.
- **Verdict and severity:** valid, **medium**.
- **Reproduced evidence:** `deferred_reopens` is written in `PhaseCampaign.initial_batch` at `q86-option-b-proof.py:653,688-697` but is never read by a transition or assertion. Replacing its accumulation with `set()` in scratch leaves the all-suite green. Replacing the second-reopen `raise ValueError` at `:751` with `pass` also leaves it green; no manifest tag covers that guard.
- **Reasoning:** The sidecar makes deferred discovery and at-most-one fresh-evidence reopen load-bearing authority rules. The manifest's comment census cannot detect a load-bearing untagged branch.
- **Exact correction:** Drive a closed-owner incidental finding into an asserted deferred-reopen state, require its later transition to honor that state after all initial attempts, and add a named mutation. Add a distinct second-reopen rejection oracle/mutation, or remove the field only if the sidecar is revised through planning to select a different authority model.

### T8 — Routing is falsely advertised as arbitrary finite phase composition

- **Source IDs:** GPT F4.
- **Verdict and severity:** valid, **high**.
- **Reproduced evidence:** `freeze_sources` accepts arbitrary `work_loops`, but `derive_owner_route` indexes the fixed `PHASE_ORDER = ("work-build", "work-check", "acceptance")` at `q86-option-b-proof.py:472-482`. Freezing `design/build/verify/ship` succeeds but routing a `design -> ship` finding raises `ValueError: tuple.index(x): x not in tuple`. The freeze also accepts duplicate phases `("same", "same", "same")`; the owner projection reports only one row.
- **Reasoning:** Exact ownership, cross-phase routing, and algebra are claimed for arbitrary finite frozen registries, but execute only for the one fixed fixture registry. Duplicate phase identity is an invalid frozen product accepted at the boundary.
- **Exact correction:** Carry the unique ordered `FreezeResult.phases` registry into routing and validate discovery/current/owner membership against it. Reject duplicate work-loop and acceptance identities. Parameterize transition and algebra tests over zero, one, and several arbitrary phase names.

### T9 — Blind-closure re-checks have no campaign continuation, and a route-specific critical escape survives all declared mutations

- **Source IDs:** GPT F5.
- **Verdict and severity:** valid, **high**.
- **Reproduced evidence:** `PhaseCampaign.blind_closure` computes `completed` once at `q86-option-b-proof.py:755-784`; `resolve_scope_in_history` and `resolve_dismissal_in_history` at `:548-575` return only history. After a high dismissal is upheld, the phase remains `blind_closure_spent=True, completed=False`; a second closure raises, and repair/verify leave it incomplete. In a separate scratch mutation, critical scope stays `SeriousBlocked` only for `CurrentOwner` and becomes `InScope` for other routes. Both the all-suite and the full 129-mutation run remain green, while a future-owner critical with upheld dismissal becomes `dismissal-settled` and does not block delivery.
- **Reasoning:** The model lacks a legal post-closure re-check settlement transition and its product tests fail to cover critical scope across routes. It therefore neither represents all required legal outcomes nor protects the selected `SeriousBlocked` invariant.
- **Exact correction:** Model scope and dismissal re-checks as typed campaign transitions keyed by stable finding id; re-evaluate closure settlement without minting a second closure batch and forbid repair of upheld dismissals. Generate every legal owner/scope/triage product, including critical scope for all routes and same-id dual-axis orderings, and make delivery/non-delivery assertions kill coordinate-specific mutations.

### T10 — The public mutation-runner contract can write bytecode into the planning tree

- **Source IDs:** Claude F9.
- **Verdict and severity:** valid, **low**.
- **Reproduced evidence:** Importing `q86-option-b-mutations.py` by path and calling `run_manifest("q86-option-b")` in a scratch extract without `PYTHONDONTWRITEBYTECODE` creates three files in `docs/plans/workflow-calibration.proofs/__pycache__/`. The exact commands avoid this only because their caller supplies that environment variable.
- **Reasoning:** The sidecar expressly exposes this in-process contract and requires proof scripts not to modify repository state. The standalone caller should not have to remember an environmental safety precondition.
- **Exact correction:** Set `sys.dont_write_bytecode = True` before loading sibling proof/checker modules (and preserve the external-cache exact-command setup); add a direct-contract cleanliness regression.

### T11 — The manifest runner silently omits mandatory checker controls when the checker file is absent

- **Source IDs:** Claude F10.
- **Verdict and severity:** valid, **low**.
- **Reproduced evidence:** `q86-option-b-mutations.py:50` loads the traceability checker only when `checker_path.exists()`. Deleting that file in a scratch extract lets `--all` exit 0 with `discovered_tags=111 mutations=111 unexercised=0 survived=0`, silently dropping all 18 checker control classes.
- **Reasoning:** The sidecar makes those traceability controls mandatory. A reduced tag count with a green survivor total is not manifest-wide assurance.
- **Exact correction:** Require the checker module and fail before discovery if it is absent; add a negative missing-checker test.

## Outcome and counts

- **Raw reviewer findings adjudicated:** 15.
- **Deduplicated findings:** 11.
- **Valid:** 11 — 1 critical, 5 high, 3 medium, 2 low.
- **Invalid:** 0.
- **Accepted residual risk:** 0.
- **Outcome:** `new_valid`.

## Backstop obligation

No high- or critical-severity finding was dismissed. Therefore no independent dismissal re-check is owed. The valid critical and high findings return to implementation and prevent this risky proof increment from counting as a clean review round.
