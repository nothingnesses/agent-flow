# Q-86 synthesis round 3 review — compositional proof and transition coverage

## Scope and result

Reviewed exact product tip `bc680ebe` against `main` (`7151b7b4`) as a `risky` artifact. I read `AGENTS.md`, the reviewer prompt, the Q-86 brief, both current proposals, the synthesis, the controller and Q-78 replay, the round-1 and round-2 reviewer reports and triages, and the round-2 repair. I did not edit reviewed product or prior findings.

**Result: four findings — one high, two medium, one low; zero critical.**

The published controller runs reproduce byte for byte at both terminal floors. The B sweep reproduces declared bounds `1, 5, 9, 13`, observed cardinality-two maxima `1, 5, 9, 11`, and zero advertised counters. The documented SHA-256 is correct: `937c714a483b583eaa66222adf4fc2e50e4764924568a5d435cbbf3078349260`. The conditional Q-78 replay returns ten passes, four observed named folds, four explicitly assumed digest changes, four conditional replans, and five conditional families. Strict render, workflow validation, and `git diff --check main...bc680ebe` pass.

## Findings

### Q86-R3-GPT-1 — B's composition proof omits one legal batch spanning multiple obligation owners

- **Severity:** high
- **New evidence relative to round-2 T1:** The round-2 repair now models several findings for one obligation and blind closure, but the new product still cannot reduce one legal review batch containing findings owned by two different obligations. This is a distinct owner-product interaction, not the settled scalar-map evidence.
- **Exact evidence:** The shared semantics permit “any finite set of findings” at `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:50`, but B assigns every profile in one attempt to the single active `owner` at `docs/plans/workflow-calibration.explorations/q86-controller-proof.py:317-324` and serially selects one special or untested obligation at `:435-460`. Exhausting the shipped `n=2` graph shows zero states with two outstanding owned owners:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3 - <<'PY'
  import importlib.util
  p='docs/plans/workflow-calibration.explorations/q86-controller-proof.py'
  sp=importlib.util.spec_from_file_location('q',p); q=importlib.util.module_from_spec(sp); sp.loader.exec_module(q)
  r=q.walk(q.BState('work:owners',('untested','untested'),0,'active',()),q.b_edges,('complete','delivered_residual'),9)
  print(sum(1 for s in r['seen'] if len({f.owner for f in s.findings if q.is_outstanding(f) and f.owner.startswith('o')}) >= 2))
  PY
  ```

  It prints `0`.

  I then changed only the scratch controller's `b_valid_from_attempt` constructor so an `o1` initial batch containing a low also contains a critical owned by `o2`. This is the smallest legal cross-owner input missing from the shipped enumerator. The shipped oracle correctly rejects the added path (`AssertionError` at `bad_delivery == 0`). A BFS over the mutated graph produces:

  ```text
  path=o1_initial_findings_low -> o1_repair0_joint -> o1_verify0_pass_joint -> o2_initial_clean -> blind_closure_clean
  terminal_control=complete reviews=4 obligations=('closed0', 'closed0')
  outstanding=((2, 'o2', 'critical', 'open'),)
  bad_delivery=7 bad_unverified_delivery=7
  ```

  Reproduce the mutation in scratch:

  ```sh
  scratch=$(mktemp -d)
  cp docs/plans/workflow-calibration.explorations/q86-controller-proof.py "$scratch/proof.py"
  PROOF="$scratch/proof.py" nix shell nixpkgs#python3 -c python3 - <<'PY'
  import os
  p=os.environ['PROOF']; s=open(p).read()
  old='''    findings = mint_profile(state.findings, profile, owner, origin)
      obligations = replace(state.obligations, index, stage)
  '''.replace('      obligations', '    obligations')
  new='''    findings = mint_profile(state.findings, profile, owner, origin)
      if index == 0 and len(state.obligations) > 1 and not state.findings and profile == ("low",):
          findings = mint_profile(findings, ("critical",), b_owner(1), origin)
      obligations = replace(state.obligations, index, stage)
  '''.replace('      if', '    if').replace('          findings', '        findings').replace('      obligations', '    obligations')
  assert s.count(old) == 1
  open(p,'w').write(s.replace(old,new))
  PY
  set +e
  PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3 "$scratch/proof.py" --mode B --phase work:cross-owner --obligations 2 --floor high
  rc=$?
  set -e
  echo "rc=$rc"
  rm -rf "$scratch"
  ```

  It exits `1` at `assert result["bad_delivery"] == 0`.
- **Consequence:** The cardinality-two sweep does not cover the non-pointwise owner interaction required for B. The induction at `Q-86-synthesis.md:60` composes finding dispositions only; it does not compose the separate obligation-state tuple. Adding the second-owner finding leaves `o2` as `Untested`, after which `o2_initial_clean` and blind closure can close the obligation controls while its critical remains open. Therefore the current per-phase enumeration plus arbitrary-finite argument does not establish B's complete-map delivery invariant for all legal batches, and B has not yet met the brief's recommendation-eligibility proof requirement.
- **Smallest correction:** Let a batch carry profiles keyed by arbitrary owner, and atomically update every affected obligation state, including mixed owned/unowned batches. Add the `o1 low + o2 critical` cardinality-two case to the shipped sweep. Then extend the composition proof over the product of `FindingMap` and obligation states, showing that every finding owner has a matching open/pending obligation state and that blind completion checks both structures. Recompute minima if one batch can count as the initial attempt for more than one obligation; the existing maxima can remain upper bounds only after that accounting is stated.

### Q86-R3-GPT-2 — The successor proof accepts an unbound receipt and cannot preserve predecessor findings or spend

- **Severity:** medium
- **New evidence relative to round-2 T5:** The round-2 repair consistently selects the materially-different successor rule in prose. The new defect is in the proof added to claim that selected rule is controlled: its receipt and predecessor types cannot represent the required joins or carry state.
- **Exact evidence:** The selected contract requires the receipt to name the predecessor, proposed obligations and exclusions, options, and chosen successor, and requires unresolved findings to remain carried (`Q-86-synthesis.md:70-77`). In the checker, `Predecessor` has only family, obligation/exclusion tuples, and a terminal bit, while `SuccessorReceipt` has only `present` and `materially_different` booleans (`q86-controller-proof.py:504-520`). Neither type contains predecessor findings, predecessor spend, the receipt's family/scope bindings, options, or choice. Consequently a value described as an unrelated receipt authorises a successor:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3 - <<'PY'
  import importlib.util
  p='docs/plans/workflow-calibration.explorations/q86-controller-proof.py'
  sp=importlib.util.spec_from_file_location('q',p); q=importlib.util.module_from_spec(sp); sp.loader.exec_module(q)
  predecessor=q.Predecessor('F1',('O1',),(),True)
  unrelated_receipt=q.SuccessorReceipt(True,True)
  print(q.SuccessorReceipt.__annotations__)
  print(q.successor_authorised(predecessor,('O1','O2'),(),unrelated_receipt))
  PY
  ```

  It prints only the two boolean fields and then `True`. `check_successor` at `q86-controller-proof.py:711-726` tests same scope, reordered scope, and a missing receipt, but cannot test a receipt for another family/scope, a missing carried critical, or copied unspent authority. Its `predecessor_immutable` check only compares the same frozen dataclass before and after a pure predicate call.
- **Consequence:** The executable `B successor structured_cases=4` result does not establish the anti-laundering and critical-lineage control the synthesis attributes to it at `Q-86-synthesis.md:238,253`. A stale receipt can satisfy the model, and predecessor findings/spend can disappear because they are absent from the successor relation. This weakens the proof at the exact boundary that is allowed to mint new family authority.
- **Smallest correction:** Give `SuccessorReceipt` exact predecessor id, proposed obligation/exclusion digest, options, and chosen successor fields; include spent authority and the complete carried finding map in the predecessor/successor relation. Reject wrong-family/wrong-scope receipts, a missing carried finding, and copied predecessor spend as fresh authority. Publish those negative cases alongside the current same-scope and missing-receipt controls.

### Q86-R3-GPT-3 — C permits low-risk acceptance to bypass its required blind closure

- **Severity:** medium
- **Exact evidence:** The synthesis says only low-risk **plan or work** phases can complete in one discovery batch, while acceptance requires discovery plus blind closure (`Q-86-synthesis.md:202-206,216-219`). The checker accepts `--phase acceptance --risk low_risk`, but `check_c` discards `phase` when constructing transitions (`q86-controller-proof.py:666-669`), and `c_settled` completes every low-risk discovery without an acceptance exception (`:209-215`). Reproduce:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3 docs/plans/workflow-calibration.explorations/q86-controller-proof.py --mode C --phase acceptance --risk low_risk --floor high
  ```

  It reports:

  ```text
  C phase=acceptance risk=low_risk ... min_reviews=1 ... bad_delivery=0 ...
  ```

- **Consequence:** The executable controller contradicts C's cost comparison and its reserved blind-closure safety control. If an acceptance caller supplies the CLI's legal `low_risk` value, the phase can deliver after one discovery batch without the independent closure sample on which C's anchoring trade-off relies.
- **Smallest correction:** Carry phase into `CState` or `c_settled` and permit the one-batch route only when `phase != acceptance` and risk is low. Add `--mode C --phase acceptance --risk low_risk` to the published matrix with `min_reviews=2`, plus an assertion that every completing acceptance path visited `BlindClosure`.

### Q86-R3-GPT-4 — A does not implement its stated foreclosure transition

- **Severity:** low
- **Exact evidence:** A says foreclosure fires when fewer batches remain than the required clean streak (`Q-86-synthesis.md:112`). `a_open` checks only whether reviews have reached the absolute limit (`q86-controller-proof.py:138-143`); it does not compare remaining authority with the now-reset streak. In a risky work phase, the shipped graph reaches a repair state at review six with streak zero and one batch remaining, then emits another implementer repair even though two clean rounds are required:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3 - <<'PY'
  import importlib.util
  from collections import deque
  p='docs/plans/workflow-calibration.explorations/q86-controller-proof.py'
  sp=importlib.util.spec_from_file_location('q',p); q=importlib.util.module_from_spec(sp); sp.loader.exec_module(q)
  start=q.AState('active',0,0,False,())
  todo=deque([start]); previous={start:None}; end=None
  while todo:
      state=todo.popleft()
      if state.control=='repair' and state.reviews==6 and state.streak==0 and q.a_limit(state,5,2)==7:
          end=state; break
      for action,target in q.a_edges(state,2,5,2):
          if target not in previous:
              previous[target]=(state,action); todo.append(target)
  path=[]; current=end
  while previous[current] is not None:
      source,action=previous[current]; path.append(action); current=source
  print(' -> '.join(reversed(path)))
  print('remaining',q.a_limit(end,5,2)-end.reviews,'clean_needed',2-end.streak)
  print([(a,t.control,t.reviews,t.streak) for a,t in q.a_edges(end,2,5,2)])
  PY
  ```

  The tail is `verify_fail_joint -> repair_joint -> verify_fail_joint`; the final state prints `remaining 1 clean_needed 2` and its only next edge is `repair_joint` to verification.
- **Consequence:** A can spend an implementer repair and final verification batch after convergence has become mathematically impossible. The seven-batch upper bound remains safe, but the transition timing and cost behavior do not match the option shown to the human or the planned foreclosure rule.
- **Smallest correction:** Centralise `clean_needed = need - streak` and foreclose before any review or repair whose remaining authorised verification path cannot supply it. Add a risky-work assertion that no active/repair/verify state has fewer remaining review batches than its required clean suffix, except a state whose next review can complete.

## Round-2 finding closure

- **T1, simultaneous findings:** partial; same-owner and blind batches are fixed, but the cross-owner batch in `Q86-R3-GPT-1` is new uncovered evidence.
- **T2, conditional Q-78 mapping:** closed. The script, synthesis, question, step, Success Criterion, and generated plan consistently distinguish observed named folds from assumed digest changes and label all resulting costs conditional.
- **T3, `LegacyNoRubric`:** closed for the stated controls. The controller has separate legacy states; direct campaign, historical credit, and zero-obligation reinterpretation counters are zero.
- **T4, A reserve unlock:** closed. An upheld serious dismissal preserves the prior reserve state, and `bad_upheld_unlock=0` reproduces at both floors.
- **T5, selected successor rule:** the prose contradiction is closed; `Q86-R3-GPT-2` is new proof evidence that receipt binding and carry preservation remain outside the corrected oracle.
- **T6, B minimum cost:** closed. The `n_q + 1` phase minimum and `r_plan + |O| + m + 1` family minimum are present in every human-facing plan source and reproduce for `n=0..3`.
- **T7, untested residual delivery:** closed for `Untested`; `bad_unverified_delivery=0` reproduces and residual acceptance is unavailable while an obligation remains `Untested`.
- **T8, unowned in-scope finding:** closed for the modeled singleton path. Unowned critical states are reachable for zero, one, and multiple obligations and none deliver.
- **T9, C constant boundary:** closed. Four stages and two repairs are explicitly unapproved.
- **T10, generated-plan wording:** closed. The synthesis now allows the required generated projection.
- **T11, phase enumeration versus family algebra:** closed as presentation. The files explicitly say the checker proves one phase and the family formulas use exact-owner/no-transfer summation. The arbitrary-finding composition premise remains incomplete for mixed owners under `Q86-R3-GPT-1`.
- **T12, medium severity:** closed. `medium` is explicit in the alphabet, rank map, profiles, and reproduced state graph.
- **T13, invalid mutation claim:** not re-raised.

## Verification and attacks run

- Exact all-mode A/B/C runs at `floor=high` and `floor=critical`: reproduced every published state, edge, terminal, minimum, maximum, interaction, and zero-counter value.
- B `n=0..3` sweep: reproduced. I also constructed maximal finite traces with finding caps `2n` for `n=1..4`; they reach exactly `5, 9, 13, 17 = 4n+1`, with all findings settled. This supports the arithmetic when findings remain within one owner at a time.
- A risky work, C low-risk work, and C risky work published runs: reproduced. The additional C low-risk acceptance attack exposes `Q86-R3-GPT-3`.
- Multiple same-owner findings, grouped repair and verification, all four severities, low plus critical, and parent plus fix-induced child: reachable and caught by the advertised counters. Mixed-owner composition fails as in `Q86-R3-GPT-1`.
- B initial-attempt priority and reopen order: no reopen edge has an `Untested` source; `bad_reopen_before_initial=0`. Zero- and one-obligation phases complete in minima one and two and stay within bounds one and five.
- Unowned findings, blind-closure findings, serious dismissal/upheld and overturned re-checks, residual delivery at both floors, final-batch re-checks, and non-delivery terminal dispositions: inspected in each graph; no additional safety violation found.
- Legacy adoption: five states/four edges reproduce with zero direct-campaign, historical-credit, and zero-obligation violations.
- Successor scope equality/reordering/missing-receipt controls reproduce; receipt binding and carry state are missing as in `Q86-R3-GPT-2`.
- Conditional Q-78 replay and authoritative selector: ten passes and `[7,10,5,6,5,5,4,2,1,0]`; every named-fold mapping is labelled assumed and every derived result conditional. No inconsistent `forced`, `measured`, or unconditional digest claim remains in the Q-86 fold.
- Baseline repeated-resume and later-acceptance parametric commands reproduce active states at `n=1,2,10,100`.
- Q-78 reviewer attribution, representative convergence histories, the 19 clean-with-findings records, 17 escalations with two resumes, and one overturned dismissal re-check reproduce the proposal's evidence.
- `nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml`: passed.
- `nix develop -c cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow`: passed with 480 metrics records, 114 steps, 87 questions, and workflow invariants holding.
- `git diff --check main...bc680ebe`: passed before this report was authored.
