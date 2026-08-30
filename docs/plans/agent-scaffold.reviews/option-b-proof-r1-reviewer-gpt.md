# Option B proof round 1 formal-model review

## Scope and result

I reviewed `main...1ef6ad97` against `AGENTS.md`, the reviewer prompt, `bounded-convergence-option-b-proof`, the proof specification, all model/runner/checker/matrix files, all eight fixtures, and the five retained Q-86 triages. I treated the artifact as risky and inspected the implementation rather than accepting its summaries.

I found **five findings: four high and one medium**. There are no critical or low findings.

The two-pass ten-invocation repeatability check used a fresh external `HOME`, `TMPDIR`, and XDG cache/state/config tree for every invocation. Commands 1, 2, 3, and 5 produced byte-identical semantic output in both passes; command 4 failed identically in both passes. Repository status and a complete non-Git path/type/content manifest were byte-identical before and after. The standalone mutation command reported `discovered_tags=129 mutations=129 unexercised=0 survived=0`, but the adversarial mutations below show that this declared-manifest result is not an adequate oracle for the required transition/product space.

## Findings

### F1 - The required traceability command fails against the live retained source

- **Severity:** medium.
- **Evidence:** Run the fourth exact command at `docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md:206`. It exits 1 in both clean passes with:

  ```text
  ValueError: unresolved durable pointer: R1-T12
  ```

  The mismatch is directly reproducible with:

  ```sh
  rg -n 'R1-T12|OPTION B PROOF (IMPLEMENTATION IN PROGRESS|WORK REVIEW ROUND 1 READY)' \
    docs/plans/workflow-calibration.proofs/q86-option-b-traceability.md \
    docs/plans/agent-scaffold.ledger.md
  ```

  This reports the matrix's stale pointer at `docs/plans/workflow-calibration.proofs/q86-option-b-traceability.md:19` as `OPTION B PROOF IMPLEMENTATION IN PROGRESS`, while the live ledger anchor at `docs/plans/agent-scaffold.ledger.md:535` is `OPTION B PROOF WORK REVIEW ROUND 1 READY`. The ledger's same line claims that all five exact commands pass.

  As a control, copying the matrix to `/tmp`, changing only that needle to the current ledger phrase, and rerunning the command reports the source-derived in-process join correctly:

  ```text
  manifest=q86-option-b valid_findings=51 executable_rows=30 resolved_rows=30 exercised_rows=30 killed_rows=30 unresolved=0
  ```

- **Consequence:** Acceptance criteria 11 and 13 are not met, the retained-triage gate cannot pass at the reviewed tip, and the durable ledger contains a false green summary. Pointing a durable trace row at a moving resume-heading phrase also means ordinary progress updates can repeatedly break the gate.
- **Correction:** Replace R1-T12's moving textual needle with a stable durable resolution or a semantic ledger-currency check, and make the ledger summary truthful. Then rerun all five commands twice with the required repository snapshots.

### F2 - The published bounds are disconnected from transitions that admit arbitrarily long delivering executions

- **Severity:** high.
- **Evidence:** `PhaseCampaign.verify` at `q86-option-b-proof.py:721-739` accepts an empty or unknown selection and increments `batches`; `PhaseCampaign.repair` at `:701-719` can be repeated on the same `REPAIR_PENDING` finding; and `reopen` at `:741-753` does not increment the batch count. In contrast, `derive_bounds` assigns the formula coefficients directly at `:1221-1243`, `maximum_phase_witness` only constructs action-name strings at `:1246-1260`, and the algebra oracle checks the detached `clean_delivering_phase` helper at `:1262-1277` and `:1873-1907`.

  Run this from the repository root:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 - <<'PY'
  import importlib.util, sys
  from pathlib import Path
  p = Path('docs/plans/workflow-calibration.proofs/q86-option-b-proof.py')
  s = importlib.util.spec_from_file_location('q86_bounds_attack', p)
  m = importlib.util.module_from_spec(s); sys.modules[s.name] = m; s.loader.exec_module(m)
  raw = {
      'work_loops': [], 'acceptance_phase': 'acceptance', 'exclusions': [],
      'sources': [{'id':'A','kind':'success_criterion','locator':'synthetic#A','text':'A','owner':'acceptance'}],
  }
  family = m.SealedPlanReview(m.PlanReviewAccount('low_risk').review()).to_freeze_pending().freeze(raw, 'family-unbounded')
  campaign = family.campaign('acceptance')
  finding = m.FindingInput('F','F',None,m.Severity.LOW,m.ScopeRelation.IN_SCOPE,m.TriageDisposition.VALID,'E','R','acceptance','acceptance','A')
  campaign = campaign.initial_batch(m.ReviewBatch('A',(finding,))).repair(('F',))
  for _ in range(100): campaign = campaign.repair(('F',))
  for _ in range(100): campaign = campaign.verify(())
  campaign = campaign.verify(('F',)).blind_closure(m.ReviewBatch(None,()))
  complete = family.complete((campaign,))
  print(type(complete).__name__, 'batches=', campaign.batches, 'C_q=', m.derive_bounds(1,1,0,'low').c_q, 'extra_repairs=100')

  m.ACTIVE_MUTATION = 'mut-algebra-cross-credit'; m.EXERCISED_TAGS.clear()
  helper = m.clean_delivering_phase(2)
  actual = m.PhaseCampaign('work-build', (('A',m.ObligationAttempt.UNTESTED),('B',m.ObligationAttempt.UNTESTED)))
  actual = actual.initial_batch(m.ReviewBatch('A',()))
  m.ACTIVE_MUTATION = None
  print('cross-credit-helper=', helper, 'actual-states=', actual.obligation_states, 'exercised=', sorted(m.EXERCISED_TAGS))
  PY
  ```

  Output:

  ```text
  Complete batches= 103 C_q= 5 extra_repairs=100
  cross-credit-helper= (2, True, ('O-0', 'O-1')) actual-states= (('A', <ObligationAttempt.CLOSED_INITIAL: 'ClosedInitial'>), ('B', <ObligationAttempt.UNTESTED: 'Untested'>)) exercised= ['algebra-cross-credit']
  ```

  The first path is an ordinary `Complete` execution with one obligation and 103 phase batches despite `C_q = 5`; the extra repair calls independently exceed `I_B`. The second result shows that `mut-algebra-cross-credit` changes only the synthetic witness helper, not the actual `PhaseCampaign` transition. It is killed by assertions that repeat the expected helper count, not by the required in-domain path through blind closure and family `Complete` described at `bounded-convergence-option-b-proof.md:178,227`.

- **Consequence:** `C_q`, `R_B`, and `I_B` are not upper bounds of the executable transition system, and the lower-bound cross-credit control is not joined to that system. A green algebra suite and a killed named mutation therefore do not prove the load-bearing coefficients that would authorize bounded convergence.
- **Correction:** Make repair and verification parse exact legal non-empty sets, consume typed per-obligation authority once, reject calls after completion, count the reopen review batch, and enforce the phase/account maximum in transitions. Derive minima and maxima by induction over or exploration of those same transitions. Move the cross-credit mutation into scheduled-owner credit and require the mutated campaign to reach actual blind closure and `FrozenFamily.complete` before measuring the shorter witness.

### F3 - The public delivery constructor accepts fabricated completion with no frozen obligation examined

- **Severity:** high.
- **Evidence:** `FrozenFamily.complete` at `q86-option-b-proof.py:831-851` checks phase names and trusts each campaign's `completed` and `blind_closure_spent` booleans. It never checks that a campaign's owner keys equal `freeze.by_owner[phase]`, that every frozen obligation has a closed state, or that the campaign was derived from the family. Run:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 - <<'PY'
  import importlib.util, sys
  from pathlib import Path
  p=Path('docs/plans/workflow-calibration.proofs/q86-option-b-proof.py')
  s=importlib.util.spec_from_file_location('q86_complete_attack',p)
  m=importlib.util.module_from_spec(s); sys.modules[s.name]=m; s.loader.exec_module(m)
  family=m.SealedPlanReview(m.PlanReviewAccount('low_risk').review()).to_freeze_pending().freeze(m.load_fixture('freeze.json'),'family-forged')
  campaigns=tuple(m.PhaseCampaign(phase,(),blind_closure_spent=True,completed=True) for phase in family.freeze.phases)
  result=family.complete(campaigns)
  print(type(result).__name__, 'frozen_obligations=',len(family.freeze.obligations),'campaign_owner_keys=',sum(len(c.obligation_states) for c in campaigns))
  PY
  ```

  Output:

  ```text
  Complete frozen_obligations= 3 campaign_owner_keys= 0
  ```

  This is specifically inside the specification's stated boundary: `q86-option-b-spec.md:226` concedes that raw Python allocation can bypass factories but promises that “all delivery constructors reject illegal products.” The `family-completion-predicate` mutation does not exercise this case.

- **Consequence:** The executable delivery gate does not establish that all frozen obligations were scheduled, examined, and closed. The core illegal state that Option B is intended to prevent remains constructible through the advertised delivery API.
- **Correction:** Give campaigns an unforgeable family/freeze identity in the reference transition model and have `FrozenFamily.complete` recompute exact owner-key equality, legal terminal attempt state for every `O_q`, closure spend, campaign order, and merged history from transition receipts rather than trusting summary booleans. Add an independently killed mutation for dropping each of those joins.

### F4 - The freeze claims arbitrary finite phase composition but routing is hard-coded to one three-phase fixture

- **Severity:** high.
- **Evidence:** `freeze_sources` accepts any finite `work_loops` and acceptance identity, but routing uses the module constant `PHASE_ORDER = ("work-build", "work-check", "acceptance")` at `q86-option-b-proof.py:472-482`. It also does not reject duplicate work-loop/acceptance identities. Run:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 - <<'PY'
  import importlib.util, sys
  from pathlib import Path
  p=Path('docs/plans/workflow-calibration.proofs/q86-option-b-proof.py')
  s=importlib.util.spec_from_file_location('q86_phase_attack',p)
  m=importlib.util.module_from_spec(s); sys.modules[s.name]=m; s.loader.exec_module(m)
  raw={'work_loops':['design','build','verify'],'acceptance_phase':'ship','exclusions':[],
       'sources':[{'id':'X','kind':'success_criterion','locator':'synthetic#X','text':'X','owner':'ship'}]}
  frozen=m.freeze_sources(raw)
  try:
      m.finding_from_input(m.FindingInput('F','F',None,m.Severity.LOW,m.ScopeRelation.IN_SCOPE,m.TriageDisposition.VALID,'E','R','design','ship','X'),'design')
  except Exception as e:
      print('phases=',frozen.phases,'routing=',type(e).__name__,str(e))
  duplicate=m.freeze_sources({'work_loops':['same','same'],'acceptance_phase':'same','exclusions':[],
      'sources':[{'id':'D','kind':'success_criterion','locator':'D','text':'D','owner':'same'}]})
  print('duplicate_phases=',duplicate.phases,'owner_projection_sum=',sum(len(v) for v in duplicate.by_owner.values()))
  PY
  ```

  Output:

  ```text
  phases= ('design', 'build', 'verify', 'ship') routing= ValueError tuple.index(x): x not in tuple
  duplicate_phases= ('same', 'same', 'same') owner_projection_sum= 1
  ```

  `derive_owner_route` also ignores its `discovery` argument, so a `FindingInput` whose recorded discovery phase disagrees with the current campaign is accepted instead of rejected at the boundary. The algebra fixture claims cases through `m = 3`, but no such named phase registry can execute owner routing in the reference model.

- **Consequence:** The proof covers only the fixture's two work loops plus acceptance, not arbitrary finite `m`, and malformed duplicate registries can freeze. Cross-phase routing, exact ownership, replay, and the phase-to-family algebra are therefore unproved for the advertised domain.
- **Correction:** Carry the canonical `FreezeResult.phases` registry into every route reducer; validate that discovery equals the active campaign, owner is absent or occurs exactly once in that registry, and every phase identity is unique. Parameterize transition/product tests over zero, one, and several arbitrary phase names and connect the algebra cases to those executable families.

### F5 - Blind-closure re-checks are not campaign transitions, and a serious product defect survives the complete 129-mutation campaign

- **Severity:** high.
- **Evidence:** `PhaseCampaign.blind_closure` computes `completed` once at `q86-option-b-proof.py:755-784`. The per-id re-check functions at `:548-575` return only a `HistoryQuotient`; no campaign transition recomputes closure after either axis settles. A legal upheld serious dismissal therefore remains permanently incomplete and can even be sent through the unrelated repair API:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 - <<'PY'
  import importlib.util, sys
  from dataclasses import replace
  from pathlib import Path
  p=Path('docs/plans/workflow-calibration.proofs/q86-option-b-proof.py')
  s=importlib.util.spec_from_file_location('q86_closure_attack',p)
  m=importlib.util.module_from_spec(s); sys.modules[s.name]=m; s.loader.exec_module(m)
  i=m.FindingInput('dismissed-high','dismissed-high',None,m.Severity.HIGH,m.ScopeRelation.IN_SCOPE,m.TriageDisposition.DISMISSED,'E','R','work-build','work-build')
  c=m.PhaseCampaign('work-build',()).blind_closure(m.ReviewBatch(None,(i,)))
  settled=m.resolve_dismissal_in_history(c.history,'dismissed-high',False)
  c=replace(c,history=settled)
  print('spent=',c.blind_closure_spent,'completed=',c.completed,'effect=',m.closure_owner_effect(settled.findings[0]))
  for name,call in [('blind-again',lambda:c.blind_closure(m.ReviewBatch(None,()))),('repair-upheld',lambda:c.repair(('dismissed-high',))),('verify-upheld',lambda:c.verify(('dismissed-high',)))]:
      try: print(name,'completed=',call().completed)
      except Exception as e: print(name,type(e).__name__,str(e))
  PY
  ```

  Output:

  ```text
  spent= True completed= False effect= dismissal-settled
  blind-again ValueError blind closure is non-transferable and single-use
  repair-upheld completed= False
  verify-upheld completed= False
  ```

  The product oracle is also not exhaustive. Its critical-scope loop at `q86-option-b-proof.py:1589-1598` uses only current owner `work-build`; it does not compose critical scope with all four owner routes. I made one scratch-only semantic mutation: critical scope remains `SeriousBlocked` for `CurrentOwner` but incorrectly becomes `InScope` for every other route. No tag was removed or changed. Both the all-suite command and all 129 declared mutations still passed:

  ```text
  architecture=FrozenObligationsWithSealedPhaseCampaigns selected_floor=high suite=all
  safety_failures=0 transition_failures=0 authority_failures=0 delivery_failures=0 legacy_failures=0 identity_failures=0 evidence_failures=0 product_failures=0 bound_failures=0
  manifest=q86-option-b discovered_tags=129 mutations=129 unexercised=0 survived=0
  ```

  Under that surviving mutation, a future-owner critical scope referral followed by scope overturn and dismissal uphold produces:

  ```text
  future_critical_scope=InScope dismissal=dismissal-upheld effect=dismissal-settled blocks=False
  ```

  Exact reproduction: copy `docs/plans/workflow-calibration.proofs/` to a nested `/tmp/.../a/b/c/` directory; in the copy replace the good `ScopeDisposition.SERIOUS_BLOCKED` argument in the critical branch of `resolve_scope` with `ScopeDisposition.SERIOUS_BLOCKED if record.owner_route == OwnerRoute.CURRENT else ScopeDisposition.IN_SCOPE`; then run the copied proof's all suite and copied mutation runner `--all`. This is a load-bearing mutation required by `bounded-convergence-option-b-proof.md:128,132,221`, but it is absent from the manifest and invisible to its independent oracle. The named fixture rows are not substitutes: `check_finite_products` only checks fixture batch names, and the blind-closure oracle directly constructs selected singleton records.

- **Consequence:** The executable stage sum omits legal post-closure continuations, while the green mutation count can miss a future/prior/unowned critical-scope escape that clears the selected serious block. Thus the claimed exhaustive `OwnerRoute x ScopeDisposition x TriageDisposition x phase` closure proof and “one mutation per load-bearing property” contract are false.
- **Correction:** Integrate scope and dismissal re-checks as typed `PhaseCampaign` transitions keyed by finding id, recompute closure settlement after each axis, disallow repair of upheld dismissals, and propagate future components through the actual family scheduler. Generate and execute the full legal owner/scope/triage/phase product, including all critical owner routes and same-id dual-axis orderings. Add mutations conditioned on each product coordinate and require family delivery/non-delivery oracles, not direct expected-value assertions, to kill them.

## Other checks

- The corrected-in-scratch traceability run derived 51 valid round-qualified source verdicts and joined all 30 executable rows to the same in-process `run_manifest("q86-option-b")` result. Inspection and the checker's self-tests confirmed fail-closed handling for duplicate/malformed triages, exact row sets, wrong manifests, unknown/surviving/unexercised entries, and count reporting. The live command still fails as F1 records.
- All 111 model tags and 18 checker tags are unique and declared; the standalone runner exercised and killed all 129. F2 and F5 show why declaration/execution counts alone do not establish adequate or independent mutation coverage.
- Selected architecture output and selected/comparison floor labels are correct; terminal-choice checks represent both floor restrictions, legacy adoption controls, global successor identities/carry, and fresh-evidence identity checks passed their shipped cases. The findings above prevent those component greens from composing into the claimed proof.
- Post-freeze replay's five shipped views and all declared field/replenishment mutations passed. The replay remains synthetic and does not cure the disconnected campaign/delivery defects above.
- Ordinary gates passed: strict render check; workflow validation (`505` records, `115` steps, `93` questions); `cargo test --all-targets` (`470` total tests); Clippy with warnings denied; `git diff --check`.
- The changed file set stays within the 13 authorized proof artifacts. No production code, pack, README, changelog, metrics history, or ledger content changed in `main...1ef6ad97`.
