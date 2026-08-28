# Q-86 synthesis round 5 triage

## Scope, reproduction, and no-relitigation

I read `AGENTS.md`, the triager prompt, the Q-86 brief, both proposals, the synthesis, the plan fold and sidecars, the ledger's Q-86 history, the durable controller and replay scripts, both round-5 reviews, and all four prior Q-86 triages. The reviewed product is `55a58b5e...2bdd3213`; it is a risky decision artifact. I did not edit product, prior records, the ledger, or metrics.

The published all-mode checker succeeds at SHA-256 `d0dabe6da04fde2009a2baf22d0a3d9fabdfbd6bc96d2859d26043531aff579a`. I also reproduced every demonstration below with `PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3`, using only ephemeral shell input or temporary files that were removed.

The prior-findings rule is observed. T1 is the new evidence that the round-4 complete-map repair counts retained settled identities against the interaction cap. T2 and T4 test the round-4 scope integration rather than re-raising detached scope routing. T5 is sibling/global family-id reuse, not the settled same-predecessor or ancestor reuse case. The other findings concern previously untested replan, evidence, replay, and documentation paths.

Ten raw reports deduplicate to nine findings: `R5C-3` and `Q86-R5-GPT-1` are one global-cap/composition defect. Every other source ID below is distinct.

## Verdicts

### T1 — The complete-map cap invalidates the arbitrary-finite proof

- **Source IDs:** `R5C-3`, `Q86-R5-GPT-1`.
- **Verdict:** valid, **high**.
- **Evidence:** The synthesis calls the bound a cardinality of the “complete live map” and derives arbitrary-finite composition from extension monotonicity (`Q-86-synthesis.md:60-62,242-244`). The checker instead has one global `FINDING_CAP = 2` (`q86-controller-proof.py:14`) and subtracts `len(state.findings)` to mint any subsequent valid, mixed-disposition, or scope finding (`:147,224,254,261,283,288,298,374,408,413,428,434,509-521,644,695,701,711,809`). Settled identities remain in that map. I followed the reported legal paths that resolve a low-plus-medium pair, then enumerated outgoing actions. A offers only `review_settled`, C only `review_settled`, and B's blind closure only `blind_closure_clean`; no later finding can be represented. This also confirms the narrower documentation claim: the checker bounds the complete retained map, not a live/outstanding map.
- **Reasoning:** Adding a settled component removes discovery transitions, so it can make completion easier and is not the extension relation the induction claims. The finite graph therefore does not establish the advertised arbitrary-finite finding-map invariant or its recommendation-eligibility conclusion. This is a core safety-proof gap, not merely a mislabeled cap.
- **Correction:** Separate a per-batch interaction bound from persistent retained identities, or prove a sound finite quotient that preserves fresh-discovery, reopen, scope, and delivery transitions after arbitrary settled history. Add reachable regressions for two settled findings followed by fresh valid, serious-dismissal, and scope batches in A, B, and C. Correct `complete live map` to the actual boundary while withholding the arbitrary-finite claim until the extension proof holds.

### T2 — `scope_routes=8` does not observe the high/critical overturn routes it claims

- **Source ID:** `R5C-1`.
- **Verdict:** valid, **medium**.
- **Evidence:** Routes five and eight in `scope_control_metrics` only ask for an ordinary in-scope high `open` finding or an in-scope critical in `serious_blocked` (`q86-controller-proof.py:1188,1191`); neither predicate requires a source `scope_recheck_overturned` edge. I replaced `update_scope` with an identity function, eliminating the asserted return-to-in-scope behavior. A, B, and C still passed their checks with `scope_routes=8` and all published zero scope counters. Conversely, removing every scope-producing/recheck edge from each graph leaves two asserted routes in each graph. The synthesis nevertheless says all eight named routes are reachable inside the controller (`Q-86-synthesis.md:314`).
- **Reasoning:** The underlying singleton return behavior exists, but its published red control cannot detect removal. The counter consequently overstates what it proves about the scope-firewall abuse control.
- **Correction:** Measure the routes over edges: require a source finding with `ScopeExpanded` and `AwaitingScopeRecheck`, the named re-check action, and the same finding/evidence id in the required target state. In particular, an overturned high must be the source of the in-scope open finding, and an overturned critical must be the source of the in-scope `SeriousBlocked` finding. Keep mutations of `update_scope` as regressions and require the route count to fall when that transition is removed.

### T3 — A carried serious finding can be delivered by the unmodelled successor campaign

- **Source ID:** `R5C-2`.
- **Verdict:** valid, **high** (raised from medium).
- **Evidence:** Replan changes all outstanding findings to `carried` (`q86-controller-proof.py:493-495,866-867`), while `OUTSTANDING` excludes `carried` (`:12`) and `delivery_is_verified` checks only outstanding findings and untested obligations (`:1041-1049`). `check_b` always starts with an empty map (`:1417-1420`). I found 2,070 B `replan`/`scope_digest_changed` edges that turn an outstanding critical into `carried`, seeded a successor campaign with the resulting map, and reached 151 `complete` or `delivered_residual` states; `delivery_is_verified` returns `True` for them. The successor fixture itself accepts a carried critical (`:1368-1381`). This conflicts with the decision artifact saying carried findings keep delivery blocked (`Q-86-synthesis.md:78,99,153`).
- **Reasoning:** The chosen architecture promises that replan preserves unresolved finding identity rather than laundering the safety question. No successor-state semantics makes a carried serious finding live and blocking, and the checked predicate makes it invisible. A successor can therefore ship the carried critical despite the no-unresolved-critical delivery claim.
- **Correction:** Define and model the replan-to-successor boundary. A carried at-or-above-floor finding must enter the successor as a live blocking component, or successor delivery must quantify explicitly over its carried set until it is resolved or reaches a terminal non-delivery disposition. Add cross-family tests beginning with carried high and critical findings at both floors, and put this floor consequence in the Q-86 decision material rather than leaving it to an implementer.

### T4 — Scope re-check products are unenumerated and the reducer can escape `SeriousBlocked`

- **Source ID:** `Q86-R5-GPT-3`.
- **Verdict:** valid, **high**.
- **Evidence:** The synthesis claims arbitrary-finite composition over scope relation and disposition (`Q-86-synthesis.md:62`) and says either critical scope result is `SeriousBlocked` and cannot deliver (`:68,349`). Yet all singleton scope producers are separate from valid-plus-dismissed batch producers (`q86-controller-proof.py:223-240,373-389,602-614,655-665,800-815`), and all three canonical graphs contain zero states with both `AwaitingScopeRecheck` and `AwaitingDismissalRecheck`, and zero with two pending scope re-checks. The re-check reducers select one referral but rewrite every pending scope finding (`:206-218,356-368,761-786`). I seeded the documented legal product of a scope-expanded critical awaiting scope re-check and an in-scope high awaiting dismissal re-check. A takes `scope_recheck_upheld -> serious_blocked`, but then `dismissal_recheck_upheld -> repair -> verify -> complete`, resolving and delivering the scope-expanded critical.
- **Reasoning:** A `ReviewBatch` is explicitly atomic and entries carry both typed scope relation and triage disposition (`Q-86-synthesis.md:46-50`), so these are legal inputs to the specified controller, not an invented domain. The checker cannot establish the claimed critical-scope guarantee while it cannot construct the relevant product and its reducer violates the guarantee when seeded with it.
- **Correction:** Enumerate scope relation together with valid/dismissed dispositions and cardinality-two scope products. Process each scope re-check by its stable finding id, never by the first referral or a bulk rewrite. While a critical scope result is `SeriousBlocked`, remaining attached re-checks may settle only without opening repair, verification, completion, or delivery. Add scope-plus-dismissal and high-plus-critical scope controls for every controller and authority boundary.

### T5 — Successor freshness is only local, allowing sibling family-id reuse

- **Source ID:** `Q86-R5-GPT-2`.
- **Verdict:** valid, **high**.
- **Evidence:** `successor_authorised` builds freshness only from the candidate predecessor's ancestry plus its own id (`q86-controller-proof.py:945-954`). I constructed two different material successors, with obligation sets `O1,O2,O3` and `O1,O2,O4`, from terminal `F2`; both authorize as `F3`. The current fixture checks one candidate relation only (`:1368-1415`). The synthesis calls this a `TaskFamilyId` authority boundary and says the successor must be fresh against the predecessor and recorded ancestors (`Q-86-synthesis.md:64-79,363`), but the relation has no append-only family/receipt registry and no one-successor rule.
- **Reasoning:** Round-4 T1 closed reusing the direct predecessor or an ancestor. A sibling reuse is new evidence: two materially different campaigns can share the immutable identity to which authority, receipts, and spend are attached. That collision defeats unique family reconstruction and reopens authority laundering under a shared id.
- **Correction:** Authorize successors against ordered append-only family/receipt history, with a global no-reuse family-id registry and exactly one chosen successor for a terminal predecessor. Bind each later predecessor snapshot to the preceding authorized successor. Add controls for sibling reuse, unrelated existing-id reuse, a second successor for one predecessor, and omitted-ancestry reconstruction.

### T6 — `MateriallyNewEvidence` neither records nor requires new evidence

- **Source ID:** `Q86-R5-GPT-4`.
- **Verdict:** valid, **medium**.
- **Evidence:** The formal domain requires materially new evidence to mint a new `EvidenceId` for a named settled root (`Q-86-state-machine.md:118`); the synthesis says relitigation without it cannot take the reopen transition (`Q-86-synthesis.md:149,351`). The B reducer instead turns every resolved or dismissed finding owned by the selected obligation back to `open` without accepting or changing evidence (`q86-controller-proof.py:635-637`). I followed a normal initial-review/repair/verification path and then selected `material_new_evidence_existing`; the sole finding changes from `(1, 1, resolved)` to `(1, 1, open)`.
- **Reasoning:** The model cannot distinguish prohibited same-evidence relitigation from a valid reopen, and it loses the named root that the supposed new evidence defeated. Its finite reopen bound does not establish the evidence/relitigation control claimed for B.
- **Correction:** Make the transition accept a fresh `EvidenceId` tied to one or more explicit stable roots, preserve prior evidence, and reopen only those roots. Exercise a rejected unchanged-evidence case and a valid fresh-evidence case in the B proof.

### T7 — The replay drops a new fold identity when a record also repeats an older identity

- **Source ID:** `Q86-R5-GPT-5`.
- **Verdict:** valid, **low**.
- **Evidence:** `q86-q78-scope-replay.sh:20-31` chooses one `observed_fold` with an `if`/`elif` chain. On two selected synthetic records, first `Q-58/Q-82 scheduling fold`, then `Q-58/Q-82 scheduling fold plus Q-87 dynamic-selector decision`, it reports one observed fold and one replan. The repeated first match reaches the `continue` at `:35-38`, so the new Q-87 identity is never examined.
- **Reasoning:** The existing repeated-Q-87 self-test closes only repeated single identity mentions. A durable artifact description may name more than one stable fold, so the current extractor does not meet its stated first-observation accounting rule.
- **Correction:** Extract every known stable fold identity from a record, deduplicate each independently, and add a repeated-plus-new combined-record fixture. Specify deterministic ordering if more than one matched identity induces separate conditional replans.

### T8 — The state-machine proposal retains superseded exact graph counts

- **Source ID:** `Q86-R5-GPT-6`.
- **Verdict:** valid, **low**.
- **Evidence:** `Q-86-state-machine.md:229` still reports A counts `809/949` and `1386/1648`; `:327` still reports C counts `794/863` and `659/711`. The retained current command output at `:455-460` instead reports A `1547/1815` and `2351/2756`, and C `1365/1528` and `1107/1235`.
- **Reasoning:** Two incompatible exact proof summaries remain in one durable proposal. The later output is correct, but the earlier narrative is stale.
- **Correction:** Replace the stale narrative totals with the authoritative output, or remove duplicate totals and point readers to the one retained output block.

### T9 — `n_a` is undefined in the minimum-cost table

- **Source ID:** `R5C-4`.
- **Verdict:** valid, **low**.
- **Evidence:** `Q-86-synthesis.md:222` is the sole repository occurrence of `n_a`; the surrounding definitions define `n_q = |O_q|`, not `n_a` (`:160,220-223`).
- **Reasoning:** The acceptance minimum cannot be joined unambiguously to the table's defined vocabulary. This is the remaining sibling of the round-4 `r_q` documentation repair.
- **Correction:** Write `n_q + 1` with `q = acceptance`, or define `n_a = |O_acceptance|` beside `n_q` and use it consistently.

## Outcome, counts, cap, and backstop

**Round outcome: `new_valid`.** There are **9 deduplicated valid findings: 4 high, 2 medium, and 3 low**. No finding is dismissed and no residual risk is accepted.

This is the risky synthesis artifact's **fifth review round**. Its running consecutive-clean count is **0 of 2** because this round has valid findings; its total-round count is **5 of 5**. The ledger expressly records that round 5 must run and then route to the cap escalation (`docs/plans/agent-scaffold.ledger.md:551`). The convergence-first exception does not apply because this is not a converging clean round. Per the cap rule, the orchestrator must now escalate to the human under the human-input contract; it must not open a sixth ordinary review round. A later human decision may select a specific repair/closure path or resume with both round counters reset, as the workflow requires.

No high- or critical-severity finding was dismissed. Therefore **no independent dismissal backstop re-check is owed**. The high findings are valid, so they return for human-directed cap handling rather than triggering the dismissal backstop.

## Verification record

- Published `--mode all --floor high` checker command and the published SHA-256 — reproduced.
- Scope-return mutation, scope-edge reachability reduction, scope-plus-dismissal/multiple-scope state searches, and seeded scope-critical trace — reproduced.
- Settled-map cap traces, sibling-successor authorization, carried-critical successor delivery, and material-evidence identity trace — reproduced.
- Combined repeated-plus-new replay fixture and stale-count citations — reproduced.
