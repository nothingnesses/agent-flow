# Q-86 synthesis round 5 review — GPT proof exhaustion

## Scope and result

Reviewed exact product tip `2bdd3213` against `main` (`55a58b5e`) as a `risky` artifact. I read `AGENTS.md`, the reviewer prompt, the Q-86 brief, both proposals, the synthesis, both executable proof artifacts, the Q-86 planning fold, the ledger's complete Q-86 round history, and every prior Q-86 review and triage. I did not re-raise a settled finding without new evidence from the round-4 repair.

**Result: six findings — zero critical, three high, one medium, and two low.**

Every published proof command reproduces exactly at checker SHA-256 `d0dabe6da04fde2009a2baf22d0a3d9fabdfbd6bc96d2859d26043531aff579a`. Both all-mode floors, every inherited A-controller run, low-risk C acceptance, the B `n = 0..3` sweep, the state-machine matrix at both floors, the live Q-78 replay, and its selected-length self-tests match the retained output. Strict render, workflow validation, and `git diff --check main...2bdd3213` pass. Those green outputs do not cover the states demonstrated below.

## Findings

### Q86-R5-GPT-1 — The global cardinality cap makes every later review incapable of finding anything after two settled findings

- **Severity:** high.
- **New evidence:** Prior rounds repaired scalar, same-owner, cross-owner, and mixed-disposition maps. The remaining defect is that the repaired checker counts settled historical identities against the interaction cap, so its transition relation is not extension-monotone and cannot support the claimed arbitrary-finite composition.
- **Exact evidence:** `q86-controller-proof.py:14` fixes `FINDING_CAP = 2`. A and C derive every new finding profile from `FINDING_CAP - len(state.findings)` at `:254`, `:261`, `:428`, and `:434`; their scope generators return nothing once the retained map reaches the cap at `:224` and `:374`. B does the same in `b_valid_batches` at `:510`, `b_mixed_batches` at `:521`, and its scope branches at `:644`, `:711`, and `:809`. Resolved and dismissed identities are never removed from the complete map. This directly contradicts the induction premise at `Q-86-synthesis.md:62` that adding a component cannot make release easier and the claimed arbitrary-finite result at `:242-244`.
- **Reproduction:**

  ```sh
  PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3 - <<'PY'
  import importlib.util
  p='docs/plans/workflow-calibration.explorations/q86-controller-proof.py'
  s=importlib.util.spec_from_file_location('q',p); q=importlib.util.module_from_spec(s); s.loader.exec_module(q)
  def take(state, edges, action): return next(t for a,t in edges(state) if a == action)
  a=q.AState('active',0,0,False,())
  a=take(a,lambda x:q.a_edges(x,2,5,2),'review_findings_low_medium')
  a=take(a,lambda x:q.a_edges(x,2,5,2),'repair_joint')
  a=take(a,lambda x:q.a_edges(x,2,5,2),'verify_pass_joint')
  print('A',a.control,a.reviews,a.streak,[x for x,_ in q.a_edges(a,2,5,2)])
  c=q.CState('acceptance','discovery',0,(),'none',False)
  c=take(c,lambda x:q.c_edges(x,'risky'),'review_findings_low_medium')
  c=take(c,lambda x:q.c_edges(x,'risky'),'repair1_joint')
  c=take(c,lambda x:q.c_edges(x,'risky'),'verify_pass_joint')
  print('C',c.control,c.reviews,[x for x,_ in q.c_edges(c,'risky')])
  b=q.BState('acceptance',('untested',),0,'active',())
  b=take(b,q.b_edges,'o1_initial_batch_o1-low-valid_o1-medium-valid')
  b=take(b,q.b_edges,'o1_repair0_joint')
  b=take(b,q.b_edges,'o1_verify0_pass_joint')
  print('B',b.control,b.reviews,b.obligations,[x for x,_ in q.b_blind_edges(b)])
  PY
  ```

  Output:

  ```text
  A active 2 1 ['review_settled']
  C blind_closure 2 ['review_settled']
  B active 2 ('closed0',) ['blind_closure_clean']
  ```

- **Consequence:** These are reachable ordinary paths. After jointly verifying exactly two findings, A's next risky clean round, C's mandatory blind closure, and B's blind closure are forced clean because all defect-producing edges have disappeared. `bad_delivery=0` then proves safety only over a graph that cannot express the next legal finding. The cardinality-two sweep therefore does not establish the recommendation-eligibility claim for arbitrary finite persistent maps.
- **Correction:** Separate the maximum findings in one enumerated batch from the number of identities retained in the persistent map. Permit fresh ids after any number of settled ids, or use a sound quotient that preserves fresh-discovery transitions. Add reachable controls for “two settled findings, then another valid, dismissed-serious, and scope-expanded batch” in A, B, and C, and restate the induction only after extension cannot remove edges or make completion easier.

### Q86-R5-GPT-2 — Successor freshness remains local to ancestry, so two different successors can reuse one family id

- **Severity:** high.
- **New evidence:** Round-4 T1 added same-family and direct-ancestor rejection. Its exact correction required freshness against “all recorded ancestors/family identities” or a no-reuse registry (`q86-synthesis-r4-triage.md:32`). The repaired relation still has no global no-reuse registry and does not record that a terminal predecessor has already issued its chosen successor.
- **Exact evidence:** `successor_authorised` builds only `predecessor_registry = predecessor.ancestor_ids + (predecessor.family_id,)` and defines freshness as `successor.family_id not in predecessor_registry` at `q86-controller-proof.py:945-954`. `check_successor` at `:1368` checks one candidate relation; it never checks a second successor or an id already used outside that candidate's ancestry. This is weaker than a unique `TaskFamilyId` and lets two different scope/budget states share the identity to which B's per-family bound is attached.
- **Reproduction:**

  ```sh
  PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3 - <<'PY'
  import importlib.util
  p='docs/plans/workflow-calibration.explorations/q86-controller-proof.py'
  s=importlib.util.spec_from_file_location('q',p); q=importlib.util.module_from_spec(s); s.loader.exec_module(q)
  carried=(q.Finding(1,'o1','critical','carried','pre_existing',0),)
  po=('O1','O2')
  pred=q.Predecessor('F2',('F0','F1'),po,(),q.scope_digest(po,()),True,7,carried)
  def candidate(obligations):
      succ=q.Successor('F3','F2',('F0','F1','F2'),obligations,(),q.scope_digest(obligations,()),7,carried,'new_human_receipt')
      rec=q.SuccessorReceipt('F2','F3',pred.ancestor_ids,succ.ancestor_ids,pred.scope_digest,succ.scope_digest,('F3','abandon'),'F3',7,carried,True)
      return q.successor_authorised(pred,succ,rec)
  print(candidate(('O1','O2','O3')))
  print(candidate(('O1','O2','O4')))
  PY
  ```

  Output is `True` twice. A second attack also succeeds if a later `Predecessor` omits its real ancestor: the pairwise predicate accepts reuse of that omitted id because it does not bind the predecessor snapshot to the preceding authorised successor record.
- **Consequence:** Two materially different campaigns can both be authorised as `F3`, or an omitted-ancestry reconstruction can cycle back to an older id. That makes authority and spend ambiguous under the same supposedly immutable family identity and reopens the laundering defect the round-4 repair was intended to close.
- **Correction:** Reconstruct successor authorization over the ordered append-only family/receipt history. Require the successor id to be absent from a global no-reuse registry, require exactly one chosen successor per terminal predecessor receipt, and bind each later predecessor snapshot to the previously authorised successor snapshot. Add sibling-id reuse, unrelated-existing-id reuse, and omitted-ancestry two-generation controls.

### Q86-R5-GPT-3 — Scope and re-check products are still unconstructible, and seeded legal products violate the critical route

- **Severity:** high.
- **New evidence:** Round-4 T2 added valid-plus-dismissed-serious products, and T5 integrated singleton scope routes. The new interaction is the product of `ScopeRelation` with dismissal/scope re-check dispositions, which the synthesis expressly includes in its arbitrary-finite proof at `Q-86-synthesis.md:62`.
- **Exact evidence:** A, B, and C generate a scope expansion only on a separate singleton edge (`q86-controller-proof.py:223-240`, `:373-389`, `:602-614`, `:655-665`, and `:800-815`). Their mixed-disposition generators create only in-scope valid plus dismissal entries. Exhausting all three shipped graphs yields zero states containing both `AwaitingScopeRecheck` and `AwaitingDismissalRecheck`, and zero states containing two pending scope re-checks. The scope reducers then choose the first referral but update **all** pending scope findings according to that first severity (`:207-218`, `:357-368`, `:762-786`). A's dismissal re-check can also call `a_open` regardless of an existing `SeriousBlocked` control (`:194-203`).
- **Reproduction, critical scope result escaped by a later dismissal re-check:**

  ```sh
  PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3 - <<'PY'
  import importlib.util
  p='docs/plans/workflow-calibration.explorations/q86-controller-proof.py'
  s=importlib.util.spec_from_file_location('q',p); q=importlib.util.module_from_spec(s); s.loader.exec_module(q)
  q.FLOOR='high'
  findings=(
    q.Finding(1,'phase','critical','awaiting_scope_recheck','pre_existing',0,q.SCOPE_EXPANDED,1),
    q.Finding(2,'phase','high','awaiting_recheck','pre_existing',0,q.IN_SCOPE,2),
  )
  state=q.AState('active',1,0,False,findings)
  for wanted in ('scope_recheck_upheld','dismissal_recheck_upheld','repair_joint','verify_pass_joint'):
      state=next(t for a,t in q.a_edges(state,1,5,2) if a == wanted)
      print(wanted,state.control,state.reviews,[(f.severity,f.disposition,f.scope_relation.kind) for f in state.findings])
  PY
  ```

  The trace enters `serious_blocked`, then leaves it for `repair`, and finishes `complete` after automatic verification. I also seeded a scope-expanded high followed by a scope-expanded critical; the high's overturned re-check sweeps both findings to `Open`, and direct A, B, and C traces all finish `complete` even though the critical never receives its mandatory independent scope ruling. Exhausting each canonical graph reports zero states with scope-plus-dismissal and zero with multiple pending scope findings, so neither construction contributes to the published counters.
- **Consequence:** The checker does not establish the stated rule at `Q-86-synthesis.md:68` that either result for a scope-expanded critical is `SeriousBlocked`, nor that a terminal serious state cannot emit another automatic action. Its eight singleton route counters do not observe re-check ordering or mixed scope/disposition maps.
- **Correction:** Make every batch entry carry both scope relation and triage disposition, enumerate the cardinality-two cross-products, and represent per-finding scope-recheck outcomes rather than applying the first referral's branch to all pending findings. Preserve a terminal `SeriousBlocked` state through every remaining attached re-check, and assert that it has no reviewer/repair successor. Add scope-plus-dismissal and high-plus-critical scope controls at normal and exhaustion boundaries for all three modes.

### Q86-R5-GPT-4 — B's materially-new-evidence transition does not carry new evidence

- **Severity:** medium.
- **Exact evidence:** The formal domain says materially new evidence creates a new `EvidenceId` and reopens the same root (`Q-86-state-machine.md:118`). `Finding` has `evidence_id` at `q86-controller-proof.py:36`, but B's `material_new_evidence_existing` transition merely changes every resolved/dismissed finding for the owner back to `open` at `:634-637`; it neither accepts nor mints an evidence id and it reopens all settled findings rather than a cited root.
- **Reproduction:**

  ```sh
  PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3 - <<'PY'
  import importlib.util
  p='docs/plans/workflow-calibration.explorations/q86-controller-proof.py'
  s=importlib.util.spec_from_file_location('q',p); q=importlib.util.module_from_spec(s); s.loader.exec_module(q)
  state=q.BState('work:evidence',('untested',),0,'active',())
  for wanted in ('o1_initial_batch_o1-low-valid','o1_repair0_joint','o1_verify0_pass_joint'):
      state=next(t for a,t in q.b_edges(state) if a == wanted)
  print('before',[(f.finding_id,f.evidence_id,f.disposition) for f in state.findings])
  state=next(t for a,t in q.b_edges(state) if a == 'o1_material_new_evidence_existing')
  print('after ',[(f.finding_id,f.evidence_id,f.disposition) for f in state.findings])
  PY
  ```

  Output changes `(1, 1, 'resolved')` to `(1, 1, 'open')`.
- **Consequence:** The proof cannot distinguish a relitigation with unchanged evidence from the event that is allowed to consume B's one reopen, and it loses which settled root the new evidence actually beat. This makes the relitigation control and stable-evidence replay claim unauditable, even though the one-reopen bound remains finite.
- **Correction:** Require a fresh `EvidenceId` tied to one or more named stable roots, preserve the prior evidence, and reopen only those roots. Add a negative same-evidence relitigation case and a positive new-evidence case to the B sweep.

### Q86-R5-GPT-5 — The replay deduplicates one identity but can miss a second identity in the same record

- **Severity:** low.
- **Exact evidence:** `q86-q78-scope-replay.sh:20-31` uses one `if`/`elif` chain and stores only one `observed_fold` per artifact. The round-4 fix correctly deduplicates a repeated Q-87 mention, but a record containing a repeated known fold and the first mention of another known fold selects the repeated one and `continue`s at `:35-39`, losing the second identity.
- **Reproduction:**

  ```sh
  tmp=$(mktemp)
  printf '%s\n' \
    '{"type":"round","task":"q78-design-pass","phase":"acceptance","artifact":"Q-58/Q-82 scheduling fold"}' \
    '{"type":"round","task":"q78-design-pass","phase":"acceptance","artifact":"Q-58/Q-82 scheduling fold plus Q-87 dynamic-selector decision"}' > "$tmp"
  docs/plans/workflow-calibration.explorations/q86-q78-scope-replay.sh "$tmp"
  rm "$tmp"
  ```

  The summary reports one fold/family change rather than two.
- **Consequence:** The live ten-record replay remains four because each current matching row names one selected fold, but the durable first-observation algorithm and selected-length controls do not correctly identify every fold in a legal artifact description.
- **Correction:** Extract all matching stable identities from each artifact, deduplicate and charge each independently, and add a combined repeated-plus-new fixture.

### Q86-R5-GPT-6 — The state-machine proposal retains obsolete exact proof counts

- **Severity:** low.
- **Exact evidence:** `Q-86-state-machine.md:229` says A acceptance reaches `809` states / `949` edges and risky work reaches `1386` / `1648`; `:327` says C risky reaches `794` / `863` and low-risk work `659` / `711`. The current exact outputs in the same file at `:455-460` are respectively `1547` / `1815`, `2351` / `2756`, `1365` / `1528`, and `1107` / `1235` after the round-4 repairs.
- **Consequence:** A reader encounters two incompatible exact proof summaries in one maintained proposal. The later command block is correct, so this is documentation staleness rather than a failed run.
- **Correction:** Update the two narrative summaries from the authoritative output or remove duplicated exact counts and point to the retained command block.

## Round-4 closure and attacks with no additional finding

- **T1 successor same-family/ancestor reuse:** direct same-family and recorded-ancestor cases are now rejected. Q86-R5-GPT-2 is new evidence about global/sibling reuse and cross-generation provenance, not the settled direct case.
- **T2 valid-plus-dismissed batches:** same-owner, cross-owner, owned/unowned, blind-closure, upheld, overturned, and seeded exhaustion paths are now reachable and preserve the open component. Q86-R5-GPT-3 concerns the separate scope-relation product.
- **T3 B initial-attempt priority:** the original early cross-owner reopen now enters `deferred1`; the three-obligation sweep reaches deferred states and reports zero active generation-one-before-initial violations. I found no remaining priority failure outside the scope-product omission.
- **T4 A streak and foreclosure:** the batch-five upheld-dismissal trace now completes with streak two; reserve remains locked after an upheld allegation unless already unlocked; risky impossible-suffix states foreclose before an automatic action. Published counters and direct traces agree.
- **T5 singleton scope routing:** all eight singleton routes are now inside each graph, preserve spend and identity, and do not reach delivery while pending. The missing products and terminal escape are Q86-R5-GPT-3.
- **B completion and cost:** for the enumerated graph, clean minima are `1,2,3,4`, maxima stay within `1,5,9,13`, owner state is bidirectional, no `Untested` obligation reaches residual delivery, and family arithmetic follows from exact ownership/no transfer. Q86-R5-GPT-1 invalidates the arbitrary-finding extension, not those finite arithmetic results.
- **C closure:** acceptance at both risks requires blind closure; low-risk work may complete at discovery; no enumerated completion carries an outstanding finding. The persistent-map cap and scope-product omissions are reported above.
- **Replay identity:** the live four identities and repeated-Q-87 eleven-pass fixture now deduplicate correctly. Q86-R5-GPT-5 is the remaining multi-identity-record case.
- **Brief and minimum-cost wording:** the brief now says Q-86 is `open`, and A's minimum uses `r_plan` / `r_work_q` consistently.

## Verification record

- Every exact controller command published in the synthesis, state-machine proposal, and safety proposal — reproduced, including both floors.
- Live Q-78 replay, `--self-test`, authoritative ten-pass selector, and parametric baseline replay — reproduced.
- `nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml` — passed.
- `nix develop -c cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` — passed with 482 metrics records, 114 steps, 87 questions, and workflow invariants holding.
- `git diff --check main...2bdd3213` — passed before this report was authored.
