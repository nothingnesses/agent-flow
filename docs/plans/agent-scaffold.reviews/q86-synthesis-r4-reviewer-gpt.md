# Q-86 synthesis round 4 review — GPT proof adversary

## Result

Six findings: **0 critical, 2 high, 3 medium, 1 low**.

The published commands reproduce exactly at checker SHA-256 `b00662359b70139bb1ea670d8ed511caf8a727e6b773b385ab1a31ffd8f8f73c`. Strict render and workflow validation pass. The round-3 C acceptance correction works at low risk under both floors (`min_reviews=2`, `bad_acceptance_blind_bypass=0`), the B phase/family arithmetic is internally consistent, the live and selected-length replay summaries run, and the cross-owner low-plus-critical counters are nonzero. The findings below are new evidence about paths that those green counters do not cover.

## Q86-R4-GPT-1 — B authorizes a successor with the predecessor's same supposedly immutable family id

- **Severity:** high.
- **Evidence:** The design requires scope additions to create “new receipted families” and applies the finite bound to each immutable family (`docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:64-78`). `successor_authorised` checks the predecessor link and receipt bindings but never checks `successor.family_id != predecessor.family_id` (`docs/plans/workflow-calibration.explorations/q86-controller-proof.py:622-647`). Its advertised wrong-family control changes the receipt's *predecessor* id; it never attacks reuse of the predecessor as the successor id (`q86-controller-proof.py:887-921`). Reproduce:

```sh
PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3 - <<'PY'
import importlib.util
p='docs/plans/workflow-calibration.explorations/q86-controller-proof.py'
s=importlib.util.spec_from_file_location('q86',p); q=importlib.util.module_from_spec(s); s.loader.exec_module(q)
carried=(q.Finding(1,'o1','critical','carried','pre_existing',0),)
po=('O1',); so=('O1','O2')
pred=q.Predecessor('F1',po,(),q.scope_digest(po,()),True,7,carried)
succ=q.Successor('F1','F1',so,(),q.scope_digest(so,()),7,carried,'new_human_receipt')
receipt=q.SuccessorReceipt('F1','F1',pred.scope_digest,succ.scope_digest,('F1','abandon'),'F1',7,carried,True)
print('same_family_successor_authorised=',q.successor_authorised(pred,succ,receipt))
PY
```

Output: `same_family_successor_authorised= True`.

- **Consequence:** Repeated material scope changes can grant fresh receipt-origin authority while retaining `TaskFamilyId = F1`. That is a reset edge inside the identity to which the synthesis assigns `4|O| + m + 8`; therefore the claimed finite per-immutable-family bound and anti-laundering property do not hold for the accepted relation.
- **Correction:** Require a fresh successor family id distinct from every predecessor/ancestor id, bind that inequality into validation, and add negative same-family and ancestor-cycle cases. Replace the vacuous `predecessor == unchanged` check with an anchored predecessor snapshot/reconstruction test, then re-establish the per-family claim.

## Q86-R4-GPT-2 — The “complete-map” oracle cannot represent one batch containing a valid finding and a serious dismissal

- **Severity:** high.
- **Evidence:** The synthesis defines one atomic batch whose whole finding map is triaged and says dismissed criticals remain `AwaitingDismissalRecheck` (`Q-86-synthesis.md:46-60,99`). A real triage may confirm one report and dismiss another from the same batch. The checker instead offers mutually exclusive transitions: A's valid profiles versus dismissal profiles (`q86-controller-proof.py:163-169`), C's valid profiles versus dismissal profiles (`:267-272`), and B's all-valid `ReviewBatch` versus a primary-owner dismissal (`:345-362,419-424`). This command exhausts the shipped A/B/C edge sets and finds no edge that atomically adds both an `open` finding and an `awaiting_recheck` finding:

```sh
PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3 - <<'PY'
import importlib.util
p='docs/plans/workflow-calibration.explorations/q86-controller-proof.py'
s=importlib.util.spec_from_file_location('q86',p); q=importlib.util.module_from_spec(s); s.loader.exec_module(q)
def mixed_added(result):
  total=0
  for source,action,target in result['edges_data']:
    old={f.finding_id for f in q.findings_of(source)}
    ds={f.disposition for f in q.findings_of(target) if f.finding_id not in old}
    total += {'open','awaiting_recheck'} <= ds
  return total
cases=(
 ('A',q.walk(q.AState('active',0,0,False,()),lambda x:q.a_edges(x,2,5,2),('complete','delivered_residual'),7)),
 ('B',q.walk(q.BState('acceptance',('untested','untested'),0,'active',()),q.b_edges,('complete','delivered_residual'),9)),
 ('C',q.walk(q.CState('acceptance','discovery',0,(),'none',False),lambda x:q.c_edges(x,'risky'),('complete','delivered_residual'),4)))
for name,result in cases: print(name,mixed_added(result))
PY
```

Output: `A 0`, `B 0`, `C 0`.

- **Consequence:** The cardinality-two sweep is not exhaustive over complete triage-backed maps. In particular, it does not prove the ordering of A reserve/foreclosure when a valid low and a dismissed critical arrive at the normal boundary, B's owner product when one owner is open and another awaits re-check, C's stage return after that combination, or the promise that one attached re-check remains available for all serious dismissals at exhaustion. An implementation that drops the dismissed component of such a batch could retain all published zero counters while concealing a critical awaiting adjudication.
- **Correction:** Give each batch entry its triage disposition and exhaust mixed valid/dismissed owner maps. Atomically retain both components, attach one batch-level re-check, and model upheld and overturned continuations alongside the valid-finding repair path for A, B, and C at both floors and at exhaustion. Extend the arbitrary-finite composition argument to disposition products, not severity/owner products alone.

## Q86-R4-GPT-3 — A cross-owner initial batch spends reopen authority before all initial attempts

- **Severity:** medium.
- **Evidence:** B promises that every obligation receives initial authority before any closed obligation can spend reopen authority (`Q-86-synthesis.md:141-153`). During an initial attempt, however, `b_valid_batches` targets every owner, including already `closed0` owners (`q86-controller-proof.py:345-362,419-424`), and the reducer changes such an owner to `open1` (`:371-403`). Reproduce the legal three-obligation trace:

```sh
PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3 - <<'PY'
import importlib.util
p='docs/plans/workflow-calibration.explorations/q86-controller-proof.py'
s=importlib.util.spec_from_file_location('q86',p); q=importlib.util.module_from_spec(s); s.loader.exec_module(q)
state=q.BState('work:x',('untested',)*3,0,'active',())
a,state=next((a,t) for a,t in q.b_edges(state) if a=='o1_initial_clean')
print(a,state.obligations)
a,state=next((a,t) for a,t in q.b_edges(state) if a=='o2_initial_batch_owned_o1-low_unowned_none')
print(a,state.obligations,[(f.owner,f.disposition) for f in state.findings])
PY
```

Output ends with `('open1', 'closed0', 'untested')`: o1's reopen is active while o3 is untested. The published `bad_reopen_before_initial=0` misses this because it searches action-name substrings (`q86-controller-proof.py:952-960`); the violating action is named `initial_batch`.

- **Consequence:** B may process and even terminally fail a reopened obligation before another frozen obligation receives any initial attempt. This defeats a round-3 correction and makes the green priority control and the human-facing structured-completion claim false, even though the controller still fails closed against residual delivery with an `Untested` row.
- **Correction:** Define a typed response to incidental findings against closed owners while initial work remains—queue the reopen finding while preserving its identity, or terminally route it—without discarding it or processing reopen work first. Test the state transition directly: no source containing `Untested` may produce/process `open1`, `pending1`, or `closed1`, regardless of action label.

## Q86-R4-GPT-4 — An upheld dismissal erases A's prior clean streak and can falsely foreclose at batch five

- **Severity:** medium.
- **Evidence:** A is supposed to retain the risk-scaled consecutive-clean predicate over the complete triage-backed map (`Q-86-synthesis.md:109-117`), and a round whose findings are all dismissed after required re-check is a clean round under the project convergence rule. `review_dismissed_*` and `verify_dismissed_*` nevertheless construct `recheck` with `streak = 0` (`q86-controller-proof.py:167-169,192-196`), after which upheld re-check adds only one (`:197-201`). Reproduce a reachable risky trace:

```sh
PYTHONDONTWRITEBYTECODE=1 nix shell nixpkgs#python3 -c python3 - <<'PY'
import importlib.util
p='docs/plans/workflow-calibration.explorations/q86-controller-proof.py'
spec=importlib.util.spec_from_file_location('q86',p); q=importlib.util.module_from_spec(spec); spec.loader.exec_module(q)
s=q.AState('active',0,0,False,())
for wanted in ('review_settled','review_findings_low','repair_joint','verify_fail_joint','repair_joint','verify_pass_joint','review_dismissed_high','recheck_upheld'):
    s=next(t for a,t in q.a_edges(s,2,5,2) if a==wanted)
    print(wanted,s.control,s.reviews,s.streak)
PY
```

The last two lines are `review_dismissed_high recheck 5 0` and `recheck_upheld terminal 5 1`. Batch four was already the first clean batch; an upheld batch-five dismissal should be the second consecutive clean batch and complete, not terminally foreclose.

- **Consequence:** A and B's inherited plan controller can force an unnecessary terminal human decision on an artifact that met its declared risky clean suffix. The published `bad_foreclosure_state=0` verifies consistency with the already-reset streak, not correctness of streak reconstruction, so A's terminal timing and B's `r_plan` behavior remain misstated on this path.
- **Correction:** Preserve the incoming streak in re-check state (or retain its return state) and reset only on an overturned/valid result. Add the reachable batch-five trace as a regression requiring `Complete`, then rerun A and inherited B plan review under both floors.

## Q86-R4-GPT-5 — Scope routing is a detached lookup, not a red-control path through any controller

- **Severity:** medium.
- **Evidence:** The synthesis says the checker explicitly models scope routing and claims the low/medium/high/critical terminal and delivery outcomes for A, B, and C (`Q-86-synthesis.md:66-68,335-354`). In the checker, `scope_expanded_route` returns only a string (`q86-controller-proof.py:650-659`). `rg -n 'scope_expanded_route|check_scope_controls' docs/plans/workflow-calibration.explorations/q86-controller-proof.py` shows it is called only by `check_scope_controls` at lines 924-937; no A, B, or C edge invokes it. The test compares eight strings with eight expected strings and never carries a finding id, evidence, phase spend, owner state, re-check state, or delivery predicate.
- **Consequence:** The proof does not establish that low consumes the opened batch without growing scope, that medium terminally stops the relevant controller, that an overturned high re-enters its in-scope repair state without new authority, or that either critical result is connected to a non-delivering `SeriousBlocked` state. These are required red controls, not merely labels.
- **Correction:** Put `ScopeRelation`/`AwaitingScopeRecheck` into the shared finding and controller states, connect every route to A/B/C spend and terminal transitions, preserve stable identity/evidence through re-check, and run the existing delivery/bound oracles on each low/medium/high/critical path at both floors.

## Q86-R4-GPT-6 — The dynamic replay counts a repeated mention of one named fold as another family

- **Severity:** low.
- **Evidence:** `replay_rows` increments the family on every row containing a recognized substring and keeps no set of already-observed fold identities (`q86-q78-scope-replay.sh:18-43`). Its own eleven-pass fixture puts the same single `Q-87 dynamic-selector decision` at both passes 8 and 11 (`:62-64`) and then asserts five “observed named folds” and five replans (`:113-114`). Running the published `q86-q78-scope-replay.sh --self-test` reproduces that five-fold summary even though the fixture contains only four distinct named folds.
- **Consequence:** If a later append-only acceptance record repeats contextual prose naming Q-87, the conditional human-facing B cost grows by a spurious replan, receipt, family, and plan-review/freeze cycle. The current ten-pass result remains four; the selected-length regression encodes the future error.
- **Correction:** Track a stable fold/event identity and count its first occurrence only; treat later mentions as unchanged unless a distinct structured fold identity is present. Change the eleven-pass regression so a repeated Q-87 mention leaves the fold/replan count at four, and use a genuinely distinct event if testing a fifth scope change.

## Verification and attacks run

- Re-ran every exact published A/B/C command, both floors, inherited B plan-controller cases, low-risk C acceptance, B `n = 0..3`, and SHA-256: outputs match the synthesis.
- Additionally ran low-risk C acceptance at `critical`: `min_reviews=2`, `bad_acceptance_blind_bypass=0`.
- Re-ran live Q-78 replay, 9/11 self-tests, and the authoritative selector: ten passes and `[7,10,5,6,5,5,4,2,1,0]`.
- Re-ran strict render, workflow validation, and `git diff --check`: passed.
- Attacked cross-owner atomic reduction, arbitrary composition boundaries, initial/reopen priority, successor identity/spend binding, B plan arithmetic, scope routing, C closure under both floors, A foreclosure, replay growth, terminal floors, and all published human-facing minima/maxima.
