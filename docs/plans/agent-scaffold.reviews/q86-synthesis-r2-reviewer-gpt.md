# Q-86 synthesis round 2 review — proof verification and adversarial state

## Scope and reproduction

Reviewed product tip `66fb8dcf` against `main` (`af55e0fb`) as a risky artifact. I read the brief, both corrected proposals, the synthesis and plan fold, round-1 triage, and the planner repair. I did not re-raise a round-1 verdict without new evidence that the repair remains incomplete.

The documented proof commands reproduce exactly, including SHA-256 `db2874d8654957582f18592ece030f344b60ca9657c127715fcc78d6987ef9a7`. The A/B/C high- and critical-floor runs report the documented state/edge counts and zero reported violations. B's `n = 0..3` sweep reports bounds `1, 5, 9, 13`. The Q-78 replay prints ten passes, four replans, five families, four additional receipts, and four additional plan-review/freeze cycles. Strict render and workflow validation pass.

Those outputs do not settle the findings below because inspection and adversarial mutations show that some claimed properties are outside the model or oracle.

## Findings

### Q86-R2-GPT-1 — The repaired controllers still cannot represent all findings from one legal batch

- **Severity:** high
- **Evidence:** `docs/plans/workflow-calibration.explorations/q86-controller-proof.py:37-42` and `:109-112` give A and C one scalar `finding: str`. B also has one scalar campaign finding at `:178-183`, while each obligation slot is replaced by one scalar finding state at `:238-260` and `:263-283`. No transition accepts a set of triager-valid findings from one batch. This conflicts with the plural stable-finding domain in `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:51-53` and the claim at `:208-213` that the checker establishes the open-critical invariant. It is a reachable-input omission, not a hypothetical load shape: the live Q-78 acceptance records at `docs/metrics/workflow.jsonl:432-437` carry 5–10 valid findings per batch.
- **Reproduction:**

  ```sh
  jq -s '[.[] | select(.type == "round" and .task == "q78-design-pass" and .phase == "acceptance") | .valid_findings] | max' docs/metrics/workflow.jsonl
  PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3 -c 'import importlib.util; p="docs/plans/workflow-calibration.explorations/q86-controller-proof.py"; s=importlib.util.spec_from_file_location("q",p); q=importlib.util.module_from_spec(s); s.loader.exec_module(q); print(q.AState.__annotations__); print(q.CState.__annotations__); print(q.BState.__annotations__)'
  ```

  This prints `10`, followed by scalar `finding: str` fields for all three controllers. A batch containing a low and a critical, or two findings against one B obligation, has no reachable state. Thus an unrelated clean observation cannot erase the model's sole critical anymore, but the reduction into that sole slot can omit another critical before the oracle ever sees it. This is new evidence that round-1 T1's correction is incomplete.
- **Consequence:** The proof does not establish that completion quantifies over every open finding identity. The critical-safety claim and B's per-obligation repair accounting can both be satisfied by the model while a legal concurrent finding remains outside it.
- **Smallest safe correction:** Define the atomic triage reduction for a batch as a finite finding map/set, including multiple findings per obligation and blind closure. Make completion and terminal legality quantify over the full set, define whether one repair/verification batch groups all findings in an obligation attempt, then exhaust that controller or provide a compositional proof over set cardinality. Recompute the repair-call bound if repairs are not grouped.

### Q86-R2-GPT-2 — The “critical-clear” oracle accepts verification without repair and does not check phase immutability

- **Severity:** medium
- **Evidence:** `docs/plans/workflow-calibration.explorations/q86-controller-proof.py:370-372` decides that a critical clear is legal from the action's name alone. Any `verify_pass_*` is accepted without checking that its source disposition is repaired, and no assertion compares a B edge's source and target `phase`. This falls short of the claimed “named verification after repair” check in `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:208-213` and the immutable-phase claim at `:131`.
- **Reproduction:** Copy the checker to scratch and make either mutation below. Both illegal controllers remain green:

  ```sh
  tmp=$(mktemp -d); cp docs/plans/workflow-calibration.explorations/q86-controller-proof.py "$tmp/proof.py"
  TMP_PROOF="$tmp/proof.py" nix shell nixpkgs#python3 -c python3 -c 'import os; p=os.environ["TMP_PROOF"]; s=open(p).read(); old="candidate = AState(\"repair\", reviews, 0, serious_seen, finding)"; assert s.count(old)==1; open(p,"w").write(s.replace(old,"candidate = AState(\"verify\", reviews, 0, serious_seen, finding)"))'
  nix shell nixpkgs#python3 -c python3 "$tmp/proof.py" --mode A --phase acceptance --risk risky --floor high
  rm -rf "$tmp"
  ```

  The mutation sends every new finding directly to verification, skipping repair, but still reports `bad_critical_clear=0` and `bad_delivery=0`.

  A second scratch mutation changing B's `initial_clean` target from `state.phase` to `"transferred"` still reports `bad_critical_clear=0`, `bad_delivery=0`, and `bad_bound=0` for `--mode B --phase work:original --obligations 1`.
- **Consequence:** The green output is not an independent oracle for two decision-material invariants. A controller regression in repair ordering or phase ownership can preserve every advertised zero.
- **Smallest safe correction:** Track lifecycle provenance in the state/property check and allow a critical verification clear only when the source contains the same finding in `ResolvedPendingVerification`; assert source and target phase identity on every nonterminal B edge. Keep mutations that skip repair and transfer phase as red tests that must make the checker fail.

### Q86-R2-GPT-3 — The Q-78 script classifies prose tokens as scope digests, so four forced replans are not established

- **Severity:** high
- **Evidence:** `docs/plans/workflow-calibration.explorations/q86-q78-scope-replay.sh:9-26` reads only the free-text `artifact` field and maps four hard-coded substrings directly to `scope_digest_changed`. It never reads a scope id, digest, canonical obligation row, plan version, or commit. The synthesis itself concedes at `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:35` and `:158` that historical records have no obligation joins and cannot reconstruct obligation state, yet `:15`, `:173`, `:278`, and `:296` promote this classifier to four forced replans and exact extra-human cost.
- **Reproduction:** A record with no scope data is declared a digest change solely because its prose contains one token:

  ```sh
  tmp=$(mktemp)
  printf '%s\n' '{"type":"round","task":"q78-design-pass","phase":"acceptance","artifact":"synthetic text containing Q-87 dynamic-selector decision but no scope id or digest"}' > "$tmp"
  docs/plans/workflow-calibration.explorations/q86-q78-scope-replay.sh "$tmp"
  rm -f "$tmp"
  ```

  It emits `event=scope_digest_changed`, `terminal=Replanned`, and a successor freeze. The live records prove that named folds occurred, but they do not prove how absent prospective `[[obligation]]` rows would have changed B's digest. This is new evidence that round-1 T4's replay correction is a label-driven assumption rather than the requested controller replay.
- **Consequence:** B's largest stated measured cost and a central human-facing trade-off are presented as established when they depend on an unrecorded counterfactual mapping. That can materially bias the A/B/C choice.
- **Smallest safe correction:** Either reconstruct each event from exact historical commits into an explicit counterfactual obligation set and show the before/after digest, or label the four mappings as assumptions and remove “forced”, “measured”, and “establishes” claims. Keep the observed folds separate from the inferred B transitions and cost.

### Q86-R2-GPT-4 — `LegacyNoRubric` remains prose-only and has no replay/control

- **Severity:** medium
- **Evidence:** The repaired design specifies `LegacyNoRubric` at `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:152-154`, but `rg -n 'LegacyNoRubric' docs/plans/workflow-calibration.explorations/q86-controller-proof.py` returns no match. `check_b` at `q86-controller-proof.py:446-449` always starts an active prospective campaign with a tuple of `untested` obligations, including `--obligations 0`; that zero-obligation state is a valid prospective blind-closure campaign, not a legacy task with undefined rubric authority.
- **Consequence:** Round-1 T14's requested typed adoption state and replay control were not added. The proof cannot distinguish safe zero-obligation adoption from an active historical task that must neither mint B authority nor be declared complete.
- **Smallest safe correction:** Add an explicit legacy start variant and exhaust its only legal terminal/adoption paths: finish terminally under a pinned legacy disposition, or enter a new prospective plan-review/freeze before any B campaign. Add red controls proving that direct `LegacyNoRubric -> FrozenObligationCampaign`, old-round closure credit, and zero-obligation reinterpretation are rejected.

### Q86-R2-GPT-5 — Option A unlocks its reserve for a dismissal that the re-check upholds

- **Severity:** medium
- **Evidence:** Option A says only a **valid** high or critical unlocks reserve at `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:86` (also `Q-86-state-machine.md:157`). The checker instead sets `serious_seen=True` as soon as a high/critical dismissal is pending at `q86-controller-proof.py:72-76`, and `recheck_upheld` retains it at `:96-98`.
- **Reproduction:**

  ```sh
  PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3 -c 'import importlib.util; p="docs/plans/workflow-calibration.explorations/q86-controller-proof.py"; s=importlib.util.spec_from_file_location("q",p); q=importlib.util.module_from_spec(s); s.loader.exec_module(q); x=q.AState("active",4,0,False,"none"); y=dict(q.a_edges(x,2,5,2))["review_dismissed_high"]; z=dict(q.a_edges(y,2,5,2))["recheck_upheld_high"]; print(y); print(z); print("limit",q.a_limit(z,5,2))'
  ```

  The upheld dismissal leaves an active batch-five state with `serious_seen=True` and limit `7`, although no valid serious finding exists.
- **Consequence:** A can buy two extra review batches from an invalid serious allegation, so its terminal timing and reserve-eligibility semantics differ from the option presented to the human. The finite upper bound remains seven, but the five-plus-two policy being compared is not the implemented controller.
- **Smallest safe correction:** Set `serious_seen` only when triage/re-check confirms a valid high or critical (the overturned branch), or explicitly change the human-facing rule to say that any high-or-critical dismissal referral permanently unlocks reserve and price that behavior.

## Round-1 closure check

- **T1:** not fully closed; explicit lifecycle states replaced the old latest-observation scalar, but legal multi-finding batches remain outside all three controllers (Q86-R2-GPT-1).
- **T2:** the repaired B controller now distinguishes initial attempt, repair, verification, reopen, and blind closure and derives `4n_q + 1`; its plural-finding domain and oracle remain incomplete as above.
- **T4:** not closed; the replay now emits transitions, but scope-change classification is still inferred from prose substrings (Q86-R2-GPT-3).
- **T5:** closed; A pass seven / three later lows and C pass three / 23 later findings including highs follow from the live records.
- **T7:** the allocation formula, exact owner rule, and zero-obligation blind seat are now stated and the `n=0` sweep reaches bound one. Phase immutability is present in the current constructors but not checked by the oracle (Q86-R2-GPT-2).
- **T8:** closed; canonical finite `[[obligation]]` rows and the closed source-label enum now define `O`.
- **T14:** not closed; the prose state exists but no controller/replay control does (Q86-R2-GPT-4).
- **T16:** closed; the synthesis now gives the A/B/C/M3 source-label map.

## Other adversarial cases inspected

Final-batch high/critical dismissal re-checks remain reachable without consuming review authority; an overturned final re-check enters a serious terminal rather than repair. Repair without verification does not clear a tracked critical in the current source. Repeated resume has no authority-reset edge. B's phase allocation is `4n_q + 1`, including one blind batch at `n_q=0`, and the whole-family arithmetic `4|O| + m + 8` and `18|O| + 4m + 38` follows from the stated exact-owner and grouped-call assumptions. Scope change is terminal within the modeled family, relitigation has no reopen edge without materially new evidence, and blind-closure findings are terminal. The findings above identify where those current-source observations are not yet the exhaustive proof the human-facing text claims.

## Finding counts

- Critical: 0
- High: 2
- Medium: 3
- Low: 0
