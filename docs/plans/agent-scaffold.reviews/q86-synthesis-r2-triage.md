# Q-86 synthesis round 2 triage

## Scope and reproduction

I independently read `AGENTS.md`, the triager prompt, the Q-86 brief, both explorer proposals, the current synthesis and proof/replay artifacts, the Q-86 plan fold, the round-1 triage, the ledger anchor, and both round-2 reviewer reports. The reviewed artifact is `main..66fb8dcf` (`f82d8902..66fb8dcf`); it is risky.

I reproduced the published A/B/C proof commands for both floors, the B `n = 0..3` sweep, the checker SHA-256, the Q-78 replay, the Q-78 selector, strict render, and workflow validation. They return the documented outputs, including B bounds `1, 5, 9, 13`, ten Q-78 acceptance passes, and `[7,10,5,6,5,5,4,2,1,0]`. I also independently reproduced the reviewers' scratch-only mutations and state searches described below. `git diff --check main..HEAD`, strict render, and workflow validation pass.

Fifteen raw reports consolidate to thirteen findings. `Q86-R2-GPT-1` and `R2C-4` are one multi-finding-model defect; `Q86-R2-GPT-4` and `R2C-6` are one legacy-adoption-control defect. The round-1 ledger rule was observed: the three partial-closure items carry new evidence about the repaired controller or replay rather than repeating their prior evidence.

## Result

**Round outcome: `new_valid`.**

- Valid findings: **12** — **1 high**, **7 medium**, **4 low**.
- Invalid findings: **1**.
- Accepted residual findings: **0**.
- Dismissed high/critical findings: **0**. **No independent dismissal backstop re-check is owed.**

## Consolidated verdicts

### T1 — The controllers omit simultaneous valid findings

- **Source IDs:** `Q86-R2-GPT-1`, `R2C-4`.
- **Verdict:** valid, **high**.
- **Reproduced evidence:** `q86-controller-proof.py:37-42`, `:109-113`, and `:178-183` give A, C, and the campaign itself one scalar `finding: str`; B also serialises its obligation work with `permitted = {active[0]}` at `:228-232`. The Q-78 acceptance records at `docs/metrics/workflow.jsonl:432-441` contain as many as ten valid findings in one batch. Importing the checker confirms the scalar annotations, while the reported graph still passes.
- **Reasoning:** round-1 T1 correctly required persistent finding/disposition state, and the scalar replacement fixes the old latest-observation erasure. It does not model the legal input of a batch with multiple findings, including a low plus a critical or a still-open parent plus a fix-induced child. Therefore the enumerations cannot establish the synthesis claim that completion quantifies over every finding identity or that an unrelated observation cannot clear every open critical. This is new evidence that the round-1 repair is incomplete, not a relitigation of the withdrawn scalar proof.
- **Exact correction:** model a batch as a finite map of stable finding ids and dispositions, including multiple findings per obligation and blind closure. Define whether one repair/verification batch jointly verifies all findings attached to an obligation or whether each consumes separately; make completion and terminal legality quantify over the complete map; then exhaust a finite cardinality parameter or provide a compositional proof and recompute the repair/call bound.

### T2 — The Q-78 replay's four digest changes are inferred from prose tokens

- **Source IDs:** `Q86-R2-GPT-3`.
- **Verdict:** valid, **medium** (reduced from high).
- **Reproduced evidence:** `q86-q78-scope-replay.sh:9-26` reads only `artifact` text and assigns `scope_digest_changed` from four hard-coded substrings. Supplying a one-line synthetic log with only `Q-87 dynamic-selector decision` in its artifact text emits `event=scope_digest_changed` and a successor freeze despite containing no scope id, digest, obligation row, or plan version. The synthesis acknowledges that historical records cannot reconstruct obligation identity or closure at `Q-86-synthesis.md:35`, yet calls the resulting four replans a measured cost at `:173`.
- **Reasoning:** the named folds are observed, but the legacy log does not establish how their counterfactual canonical obligation sets would change. The replay is useful as a stated scenario, not evidence that those exact four `ScopeDigestChanged` transitions were forced. This weakens a central B trade-off but does not invalidate B's prospective controller or its finite per-family bound.
- **Exact correction:** either reconstruct each replay event from exact historical commits into an explicit counterfactual obligation set and before/after digest, or label each mapping an assumption. In the latter case, retain the observed four named folds but replace “forced”, “measured”, and “establishes” with conditional wording and present the four-replan cost as the result under those assumptions.

### T3 — `LegacyNoRubric` is specified but not controlled or replayed

- **Source IDs:** `Q86-R2-GPT-4`, `R2C-6`.
- **Verdict:** valid, **medium**.
- **Reproduced evidence:** `Q-86-synthesis.md:152-154` defines `LegacyNoRubric` and claims validation rejects a direct entry into a B campaign. Neither `q86-controller-proof.py` nor `q86-q78-scope-replay.sh` contains `LegacyNoRubric` or `legacy`; `check_b` always starts a prospective tuple of `untested` obligations at `q86-controller-proof.py:446-449`. A zero-obligation prospective campaign is not a legacy task that lacks authority to define `O`.
- **Reasoning:** this is new evidence on round-1 T14. The prose state is an improvement, but the required adoption control remains unexercised. Consequently B cannot yet demonstrate that an active pre-freeze task is neither granted a fresh campaign nor mistaken for a valid zero-obligation campaign.
- **Exact correction:** add an explicit legacy start variant to the controller or a separate adoption transition model. Its only legal paths must be terminal completion under a pinned legacy disposition, or a new prospective plan-review/freeze before any B campaign. Add red controls rejecting direct `LegacyNoRubric -> FrozenObligationCampaign`, historical-round closure credit, and reinterpretation as a zero-obligation campaign.

### T4 — A's reserve is unlocked by an upheld serious dismissal

- **Source IDs:** `Q86-R2-GPT-5`.
- **Verdict:** valid, **medium**.
- **Reproduced evidence:** the synthesis says a **valid** high or critical unlocks A's reserve at `Q-86-synthesis.md:86`. In the checker, a pending high dismissal sets `serious_seen=True` at `q86-controller-proof.py:76-79`; after `recheck_upheld` at `:95-98`, the state remains active at review five with an A limit of seven. The direct trace is `review_dismissed_high -> recheck_upheld_high`, with no valid serious finding.
- **Reasoning:** the controller's five-plus-two behavior differs from the option presented to the human. The finite maximum remains seven, but an invalid allegation can buy its reserve, so its terminal timing and ordinary review cost do not match the stated policy.
- **Exact correction:** preserve the prior `serious_seen` value on a dismissal referral and set it only when triage/re-check establishes a valid high or critical, including the recheck-overturned path. Add the upheld-dismissal trace as a red control. Alternatively change the human-facing policy to price permanent unlocking on every serious referral; do not leave the two definitions different.

### T5 — B's successor-scope rule is internally inconsistent

- **Source IDs:** `R2C-1`.
- **Verdict:** valid, **medium** (narrowed from high).
- **Reproduced evidence:** the synthesis makes a successor require “materially different scope” at `Q-86-synthesis.md:73` and `:127`, whereas the mapped M2 source requires it to be strictly narrower or disjoint at `Q-86-safety-process.md:273-279`. The same source and the synthesis admit the Q-78 expanded successors F2 through F5 at `Q-86-safety-process.md:369` and `Q-86-synthesis.md:162-171`. The repair diff deleted the synthesis's former stricter rule.
- **Reasoning:** the reviewer overstates the consequence: the brief permits a terminal, receipted materially different successor family, so it need not impose a finite bound across arbitrary new project work. B's per-family terminal rule is not disproved merely because users may start new scoped work. The valid defect is that the synthesis maps B to M2 while leaving its decisive successor rule and the Q-78 replay incompatible with the retained M2 source, so an implementer cannot tell which anti-laundering contract to enforce.
- **Exact correction:** state once which successor rule Option B selects. If it selects materially-different scope, mark the strict-narrower/disjoint rule as an unselected proposal alternative, remove its chain-bound claim from the selected M2 description, and state that the human receipt and immutable predecessor are the anti-laundering controls. If it selects stricter/disjoint, make the replay stop at the first expansion. In either case put the selected structured successor test and its terminal/replan red control in the enforcement inventory.

### T6 — B's minimum ordinary review cost is absent from the decision comparison

- **Source IDs:** `R2C-2`.
- **Verdict:** valid, **medium**.
- **Reproduced evidence:** B admits one `initial_clean` batch per untested obligation at `q86-controller-proof.py:237-241` and only permits blind closure when all are closed at `:304-311`. A breadth-first search over the published controller yields minimum batches `1,2,3,4,5,6` for B with zero through five obligations, while A requires one acceptance or two risky-work batches and C requires one low-risk or two risky batches. Thus each B phase costs at least `n_q + 1`, and the post-freeze family at least `|O| + p`, before the plan-review minimum.
- **Reasoning:** the synthesis provides B's maximum but not its unavoidable clean-case cost, despite recommending B while comparing the alternatives under Minimal by default. The current plan's count of prose bullets is not a valid substitute for `|O|`, which is prospective canonical data; the missing formula itself is enough.
- **Exact correction:** add the per-phase minimum `n_q + 1` and a whole-family minimum `r_plan + |O| + p`, where `r_plan` is the declared plan-review minimum, to B's cost section and Q-86 ask. Contrast it with A and C's `|O|`-independent phase minima and state that `|O|` is a future frozen-row count, not the current prose-bullet count.

### T7 — B's proof admits residual delivery before exhaustion with untested obligations

- **Source IDs:** `R2C-3`.
- **Verdict:** valid, **medium**.
- **Reproduced evidence:** `q86-controller-proof.py:312-316` adds `request_beyond_declared_authority` from every active state, without checking spend. From the resulting `exhausted` state, `:322-331` permits `accept_residual`. Breadth-first search from two `untested` obligations reaches `delivered_residual` via exactly `request_beyond_declared_authority`, `accept_residual`, with zero reviews and both obligations `accepted_untested`.
- **Reasoning:** the graph is broader than the documented “declared authority exhausted” terminal. Its current `bad_delivery` metric checks only critical/pending state, so it misses delivery without required obligation examination. That conflicts with B's claimed verified-closure completion model and makes the green proof insufficient for that claim.
- **Exact correction:** allow the exhaustion edge only when declared authority is genuinely exhausted or no legal automated action remains; schedule initial attempts so every obligation is attempted before discretionary reopen work can spend their authority; and prohibit `delivered_residual` with an `untested` obligation. Add a `bad_unverified_delivery` check and publish the rerun output.

### T8 — B's closed obligation source conflicts with the shared in-scope rule

- **Source IDs:** `R2C-5`.
- **Verdict:** valid, **medium**.
- **Reproduced evidence:** the shared package treats violations of a frozen obligation, invariant, boundary, or duty as in scope and makes every critical in scope at `Q-86-synthesis.md:49`. B's `O` accepts only `success_criterion`, `project_principle`, and `documentation_impact` rows at `:104-110`, expressly excludes unstructured invariants and trust-boundary prose, and its transition table at `:116-131` has no state for an in-scope finding with no owner.
- **Reasoning:** a genuine uncited invariant/boundary finding, including a critical, can be in scope under the common rule but cannot be opened, repaired, or block B's all-obligations-closed predicate. Sending “uncertainty” to a human in prose does not define a controller transition or validation rule. This is distinct from the stated general risk that the finite source might be incomplete.
- **Exact correction:** either encode every B in-scope category as a finite obligation row at freeze, or add an `UnownedInScopeFinding` transition that blocks phase completion and routes to the appropriate terminal human decision; retain the always-in-scope critical rule. State which option-specific scope rule supersedes the shared one and add a red control for an unowned in-scope critical.

### T9 — C's numerical protocol depth is omitted from the synthesis no-decision boundary

- **Source IDs:** `R2C-7`.
- **Verdict:** valid, **low**.
- **Reproduced evidence:** `Q-86-synthesis.md:298` lists A's five-plus-two value and B's one reopen as unapproved but omits C's four stages and two repairs, specified at `:183-187`. The plan TOML's broader no-decision sentence covers numeric constants, but the synthesis's own purportedly exhaustive list does not.
- **Reasoning:** the Q-86 ask correctly keeps all constants open, but the synthesis should not imply that choosing C also authorises its uncalibrated depth.
- **Exact correction:** add C's four-stage/two-repair values to the synthesis no-decision list, or replace the enumerated list with an explicit statement that every controller constant remains unapproved.

### T10 — The synthesis incorrectly says it changes no generated plan

- **Source IDs:** `R2C-8`.
- **Verdict:** valid, **low**.
- **Reproduced evidence:** `Q-86-synthesis.md:5` says the synthesis changes no “generated plan”, while `git diff --stat 62c6ddd9..66fb8dcf -- docs/plans/agent-scaffold.md` reports the required rendered-plan change. The change is a legitimate projection of the Q-86 source edits, not an unapproved workflow rule.
- **Reasoning:** the decision-boundary sentence is false against its own reviewed diff and confuses a generated projection update with a behavioral workflow change.
- **Exact correction:** say that it changes no generated-plan content beyond the required projection of the Q-86 source edits, or omit “generated plan” from the list.

### T11 — The proof presentation blurs per-phase enumeration with whole-family algebra

- **Source IDs:** `R2C-9`.
- **Verdict:** valid, **low**.
- **Reproduced evidence:** `check_b` starts one `BState` phase at `q86-controller-proof.py:446-449`, and `check_c` similarly starts one phase at `:428-430`. The synthesis derives the family formula by summing at `Q-86-synthesis.md:135-146`, but its proof summary at `:208-214` says the checker verifies review spend against “the stated bound” without distinguishing the phase-local graph from the no-transfer composition argument.
- **Reasoning:** the arithmetic is correct: exact ownership and no transfer let the per-phase maxima sum. The evidence claim needs to say that rather than imply a multi-phase enumeration, especially because the human is shown a whole-family bound.
- **Exact correction:** state in the proof section and Q-86 ask that the checker establishes each phase factor, and that `4|O| + m + 8` follows algebraically by summing exact phase owners with no transfer. Keep the no-transfer premise as an explicit enforced invariant.

### T12 — The proof silently omits `medium` from the project severity scale

- **Source IDs:** `R2C-10`.
- **Verdict:** valid, **low**.
- **Reproduced evidence:** `q86-controller-proof.py:6` sets `SEVERITIES = ("low", "high", "critical")`; `severity_of("open_medium")` returns `None`. The project's four-level scale includes medium, and Q-78's initial acceptance records contain medium findings (`docs/metrics/workflow.jsonl:432-438`).
- **Reasoning:** medium is behaviorally equivalent to low for the two currently offered floors, so this does not defeat the high/critical safety result. But the artifact calls its alphabet `SEVERITIES` and never declares the abstraction, making its model boundary unclear and unsafe if a later floor or rule distinguishes medium.
- **Exact correction:** model `medium` explicitly, update the rank map and published proof outputs/hash, or rename the modeled class to a documented below-floor quotient and state that it is valid only while `F` is `high` or `critical`.

### T13 — The mutation argument does not establish a defect in the current transition model

- **Source IDs:** `Q86-R2-GPT-2`.
- **Verdict:** invalid.
- **Reproduced evidence:** the reviewer's scratch mutations still print zero counters because `bad_critical_clear` does not serve as a mutation-test oracle. In the actual controller, an A critical reaches `verify` only through `active -> repair -> verify` at `q86-controller-proof.py:59-86`; B's actual constructors preserve `state.phase` on all transitions at `:238-331`. Thus repair ordering and phase immutability are already restrictions of the enumerated transition relation.
- **Reasoning:** an external mutation that deliberately changes the transition relation can expose a useful future regression test, but it does not show that the published graph cannot represent, or fails to enforce, the two properties in its unmutated state. Unlike T1 and T7, no legal source-state path violates the claimed property.
- **Exact correction:** none required. A future mutation test that fails on repair bypass or phase transfer would improve proof-regression coverage, but its absence is not a defect in this decision artifact.

## Verification record

- Published proof commands for A/B/C at both floors and B's `n = 0..3` sweep — reproduced.
- `q86-q78-scope-replay.sh docs/metrics/workflow.jsonl` and the Q-78 selector — reproduced.
- Scratch-only source mutations, graph searches, reserve trace, synthetic replay input, and severity probe — reproduced as cited above.
- `nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml` — passed.
- `nix develop -c cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` — passed.
- `git diff --check main..HEAD` — passed before this file was authored.
