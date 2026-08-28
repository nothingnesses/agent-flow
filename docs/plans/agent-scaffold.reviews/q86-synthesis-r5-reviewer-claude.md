# Q-86 synthesis round 5 — reviewer (claude)

Reviewed tip `2bdd3213` against `main` (`55a58b5e`), lens: final decision-executability and safety. I read `AGENTS.md`, `.agents/prompts/reviewer.md`, the Q-86 brief, `Q-86-state-machine.md`, `Q-86-safety-process.md`, `Q-86-synthesis.md`, `q86-controller-proof.py`, `q86-q78-scope-replay.sh`, the `[[question]] Q-86` TOML entry, `agent-scaffold.questions/Q-86.md`, `agent-scaffold.steps/workflow-calibration.md`, `agent-scaffold.success-criteria.md`, the generated `agent-scaffold.md`, and the round-1 through round-4 triages. I did not inspect the other round-5 reviewer.

**Result: four valid findings — zero critical, zero high, two medium, two low.** I found nothing at critical or high severity: every published number, formula, command, and output in the change set reproduces exactly, and all eight round-4 corrections landed (see *Round-4 correction verification* below).

Every demonstration below runs from this worktree with `nix shell nixpkgs#python3 -c python3`. Two are mutations, per the reviewer prompt's strongest-evidence rule.

---

## R5C-1 (medium). `scope_routes=8` is a false green for two of its eight labelled routes

**Evidence.** `Q-86-synthesis.md:314` states: "`scope_routes=8` means that low, medium, high referral, high upheld, **high overturned**, critical referral, critical upheld, and **critical overturned** are all reachable inside that controller." The red-control table makes the same two claims: "overturned returns in scope" (`:348`) and "either result is `SeriousBlocked`" (`:349`).

Two of the eight route predicates in `scope_control_metrics` do not mention scope expansion at all:

- `q86-controller-proof.py:1188` — `f.scope_relation.kind == "in_scope" and f.severity == "high" and f.disposition == "open"`
- `q86-controller-proof.py:1191` — `state.control == "serious_blocked" and ... f.scope_relation.kind == "in_scope" and f.severity == "critical"`

Both are satisfied by an ordinary in-scope finding minted by `review_findings_high` / `review_findings_critical`, with no scope-expansion transition involved.

*Mutation 1 — delete the "overturned returns in scope" behaviour and the counter does not move.* `update_scope` (`:63-64`) is the only writer of `IN_SCOPE` on an overturned scope re-check (`:212`, `:218`, `:362`, `:368`, `:769`, `:786`). Neutering it removes that behaviour entirely, yet every published counter is unchanged:

```sh
cat > /tmp/probe3.py <<'PY'
import importlib.util
spec = importlib.util.spec_from_file_location("chk","docs/plans/workflow-calibration.explorations/q86-controller-proof.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.FLOOR="high"; m.FINDING_CAP=2
m.update_scope = lambda findings, predicate, scope_relation: findings   # overturn no longer returns in scope
m.check_a("acceptance","risky"); m.check_b("acceptance",2); m.check_c("acceptance","risky")
PY
nix shell nixpkgs#python3 -c python3 /tmp/probe3.py
```

Prints `scope_routes=8 ... bad_scope_spend=0 bad_scope_identity=0 bad_scope_delivery=0` for A, B, and C, with every assertion still passing.

*Mutation 2 — remove every scope-expansion edge and the two routes are still "reachable".* Filtering all `scope_*` actions out of `a_edges`, `b_edges`, and `c_edges` so no `ScopeExpanded` finding is ever minted leaves routes 5 and 8 true in all three controllers:

```text
A with ALL scope edges removed: scope_routes = 2
    {'low backlogged': False, 'medium terminal': False, 'high referral': False, 'high upheld': False,
     'high OVERTURNED': True, 'critical referral': False, 'critical upheld': False, 'critical OVERTURNED': True}
B with ALL scope edges removed: scope_routes = 2   (same map)
C with ALL scope edges removed: scope_routes = 2   (same map)
```

**Consequence.** The overturn half of the selected scope policy is the abuse control the firewall exists for: it is what stops a triager parking a genuine high or critical behind an out-of-scope label (`Q-86-synthesis.md:68`; `Q-86-safety-process.md:255-257`). The behaviour is correctly implemented in `a_scope_recheck_edges`, `c_scope_recheck_edges`, and `b_scope_recheck_edges`, but the published counter the human is shown as its evidence cannot detect its removal, so `scope_routes=8` overstates what the proof establishes. This is distinct from round-4 T5, which was that scope routing sat outside the controllers entirely; that repair landed, and this is new evidence that two of the repair's own counters do not measure it.

**Correction.** Make routes 5 and 8 scope-specific: require `f.scope_relation.kind == "in_scope"` **and** an `evidence_id`/`finding_id` that entered the state through a `scope_recheck_overturned` edge, or measure them over `result["edges_data"]` filtered to `action == "scope_recheck_overturned"` (the source carries `awaiting_scope_recheck` and `scope_expanded`, the target carries `in_scope`). Re-run both mutations as regressions: with `update_scope` neutered, `scope_routes` must fall to 6. Then republish the outputs and the checker SHA-256.

---

## R5C-2 (medium). The serious floor `F` has no stated reach across the replan boundary, and the shipped predicate lets a carried at-or-above-floor finding be delivered

**Evidence.** `Q-86-synthesis.md:90` claims "Both values retain the invariant that no unresolved critical can be delivered", and the floor is one of the two decisions the human is being asked to make (`:397`). `Replan` is legal at any severity, including from `SeriousBlocked`, and converts every outstanding finding to `CarriedToSuccessor` (`:99`, `:153`). In the model, `carried` is a *terminal* disposition (`q86-controller-proof.py:11`), is not `OUTSTANDING` (`:12`), and so is invisible to `delivery_is_verified` (`:1041-1049`) and to `bad_delivery`/`bad_unverified_delivery`.

The selected successor rule permits **additive** scope deltas — "Scope additions are therefore permitted" (`Q-86-synthesis.md:80`) — so the successor can deliver the same artefact plus more, and nothing in the synthesis, `Q-86-safety-process.md:261-283`, or the checker requires it to keep a carried at-or-above-floor finding blocking. `check_successor`'s own fixture authorises a successor whose carry set contains an unresolved `critical` (`q86-controller-proof.py:1371`, `accepted_different=true`), and `check_b` always starts a campaign with `findings=()` (`:1418`), so no successor campaign carrying such a finding is ever enumerated.

```sh
cat > /tmp/probe2.py <<'PY'
import importlib.util
from collections import deque
spec = importlib.util.spec_from_file_location("chk","docs/plans/workflow-calibration.explorations/q86-controller-proof.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.FLOOR="high"; m.FINDING_CAP=2
def reach(start, ef):
    q=deque([start]); seen={start}; edges=[]
    while q:
        s=q.popleft()
        for a,t in ef(s):
            edges.append((s,a,t))
            if t not in seen: seen.add(t); q.append(t)
    return seen, edges
seen, edges = reach(m.BState("acceptance",("untested","untested"),0,"active",()), m.b_edges)
hits = [(s,a,t) for s,a,t in edges if a in ("replan","scope_digest_changed")
        and any(f.severity=="critical" and m.is_outstanding(f) for f in s.findings)
        and any(f.severity=="critical" and f.disposition=="carried" for f in t.findings)]
print("B edges turning an outstanding critical into `carried`:", len(hits))
succ, _ = reach(m.BState("acceptance",("untested","untested"),0,"active",hits[0][2].findings), m.b_edges)
d = [x for x in succ if x.control in ("complete","delivered_residual")]
print("successor campaign seeded with that carried critical: delivering states =", len(d),
      "delivery_is_verified =", m.delivery_is_verified(d[0]))
PY
nix shell nixpkgs#python3 -c python3 /tmp/probe2.py
```

```text
B edges turning an outstanding critical into `carried`: 2070
successor campaign seeded with that carried critical: delivering states = 151 delivery_is_verified = True
```

A and C have the same edge (63 and 70 `replan` edges respectively from a state holding an outstanding critical).

**Consequence.** The floor deliberately removes human discretion at the top of the scale: `Narrow scope` is illegal with an open finding at or above `F` and may only remove the affected output as terminal `RemovedFromDelivery` (`Q-86-synthesis.md:97`). `Replan` carries no such restriction, so replan → receipted additive-scope successor is a route that reaches delivery of the same artefact with the finding recorded but no longer blocking. `Q-86-safety-process.md:277` asserts the opposite ground — "A replan cannot change any finding's disposition, so it cannot launder the safety question" — which the reducer contradicts: `b_dispose` (`:493-495`) maps every outstanding finding to `carried`. The human is being asked to pick `high` or `critical` without being told whether the floor survives a replan, and an implementer reading this artifact has no rule to encode. This is not covered by round-2 T5 (successor-rule consistency), round-3 T2 (receipt binding and carry modelling), or round-4 T1 (successor id freshness); none of those asks whether a carried at-or-above-floor finding still blocks the successor.

**Correction.** State the cross-family rule once in the shared safety package and in the terminal-choices section: a `CarriedToSuccessor` finding at or above `F` re-enters the successor's live map as `Open` (or its own blocking variant) at freeze, and the successor's completion and residual-delivery predicates quantify over it exactly as over its own findings; `RemovedFromDelivery` with an exact exclusion remains the only way to stop carrying it. Then either model it — seed `check_b` with a carried at-or-above-floor finding and assert no delivering state exists — or say explicitly in `Q-86-synthesis.md:90` that the no-unresolved-critical invariant is proved per family only and that cross-family carry is an unproved design requirement. Add the rule to the human-facing floor co-decision in `agent-scaffold.plan.toml` and `agent-scaffold.questions/Q-86.md`, since it changes what choosing `high` actually buys.

---

## R5C-3 (low). The synthesis describes the sweep as bounded by the *live* map; the checker bounds the *complete* map

**Evidence.** `Q-86-synthesis.md:60` — "The durable checker exhausts every severity multiset whose complete **live** map has cardinality at most two" — and `:242` — "with a complete **live** finding-map cardinality of two". `FINDING_CAP` (`q86-controller-proof.py:14`) bounds `len(state.findings)`, which includes `resolved`, `dismissed`, `backlogged`, and `carried` entries: `severity_profiles(FINDING_CAP - len(state.findings))` (`:71-75`, called at `:254`, `:428`) and `mixed_disposition_profiles(FINDING_CAP - len(state.findings))` (`:78-81`) both subtract settled findings. The source proposal states the boundary correctly: "The finite sweep exhausts a **complete-map** cardinality of two" (`Q-86-safety-process.md:401`), as does the Success Criterion ("phase-local complete-map bounds at cardinality two").

```sh
cat > /tmp/probe5.py <<'PY'
import importlib.util
from collections import deque
spec = importlib.util.spec_from_file_location("chk","docs/plans/workflow-calibration.explorations/q86-controller-proof.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.FLOOR="high"; m.FINDING_CAP=2
def reach(start, ef):
    q=deque([start]); seen={start}
    while q:
        s=q.popleft()
        for a,t in ef(s):
            if t not in seen: seen.add(t); q.append(t)
    return seen
for lbl, seen in (("A", reach(m.AState("active",0,0,False,()), lambda s: m.a_edges(s,1,5,2))),
                  ("B", reach(m.BState("acceptance",("untested","untested"),0,"active",()), m.b_edges)),
                  ("C", reach(m.CState("acceptance","discovery",0,(),"none",False), lambda s: m.c_edges(s,"risky")))):
    live2 = sum(1 for s in seen if sum(1 for f in m.findings_of(s) if m.is_outstanding(f))==2 and any(not m.is_outstanding(f) for f in m.findings_of(s)))
    capped = sum(1 for s in seen if sum(1 for f in m.findings_of(s) if m.is_outstanding(f))<=1 and len(m.findings_of(s))==2)
    print(lbl, "live-map-2 states that also hold a settled finding =", live2, "| capped states with <=1 live finding =", capped)
print("profiles available with one settled + one live finding:", m.severity_profiles(0), m.mixed_disposition_profiles(0))
PY
nix shell nixpkgs#python3 -c python3 /tmp/probe5.py
```

```text
A live-map-2 states that also hold a settled finding = 0 | capped states with <=1 live finding = 1102
B live-map-2 states that also hold a settled finding = 0 | capped states with <=1 live finding = 30999
C live-map-2 states that also hold a settled finding = 0 | capped states with <=1 live finding = 1101
profiles available with one settled + one live finding: () ()
```

**Consequence.** Under the sentence as written, "every valid-severity by serious-dismissal product" and "all ten two-finding severity multisets" would be exhausted from any state with a live map below the cap. They are exhausted only from a state whose *whole* map is below the cap: in 1102/30999/1101 states no further finding can be minted at all. The substantive claim is unaffected — the interactions the sweep is designed to expose (scalar erasure, cross-owner mismatch, mixed floor, mixed disposition, parent-child) all arise from an empty start, and arbitrary finite maps rest on the compositional argument, not the sweep — but the decision artifact overstates its own proof boundary relative to both the code and its source proposal.

**Correction.** Change "complete live map" to "complete map (including settled entries)" at `Q-86-synthesis.md:60` and `:242`, matching `Q-86-safety-process.md:401`, and say explicitly that a state already holding a settled finding cannot receive a further two-finding batch in the sweep.

---

## R5C-4 (low). `n_a` is used in the minimum-cost table without definition

**Evidence.** `rg -n 'n_a' docs/plans/workflow-calibration.explorations/Q-86-synthesis.md` returns exactly one hit, `:222`: "| Acceptance phase | ... | `n_a + 1` batches and `2(n_a + 1)` reviewer calls. | ... |". The two rows immediately above it use `n_q`, defined at `:160` as `n_q = |O_q|`; `r_plan`, `r_work_q`, `c_plan`, `c_work_q`, `p`, `m`, and `|O|` are all defined in prose (`:120`, `:140`, `:162`, `:210`). `n_a` is defined nowhere in the synthesis, the question sidecar, the step sidecar, or `agent-scaffold.plan.toml`.

**Consequence.** This is the same defect class the round-4 triage validated as T10 for `r_q`; that repair replaced `r_q` but left `n_a` standing. In the one table the human uses to compare ordinary costs, the acceptance row's parameter cannot be joined unambiguously to its own definition — a reader cannot tell whether `n_a` is `n_q` instantiated at the acceptance phase or a separate quantity.

**Correction.** Write the acceptance row as `n_q + 1` with `q` = acceptance, or define `n_a = |O_acceptance|` once where `n_q` is defined at `:160`, and keep the table and the `L_B`/`R_B` formulas on one vocabulary.

---

## Round-4 correction verification

All eight valid round-4 findings are repaired; each check reproduces in this worktree.

| Round-4 finding | Verdict | Evidence |
| --- | --- | --- |
| T1 successor reuses predecessor family id | Fixed | `successor_authorised` now requires `predecessor_ancestry_valid`, `fresh_successor_id`, `exact_successor_ancestry` (`:951-954`); negative cases `same_family`, `ancestor_reuse`, `wrong_ancestry`, `wrong_receipt_ancestry` added (`:1388-1394`); output `structured_cases=14 ... bad_same_family=0 bad_ancestor_reuse=0 bad_ancestry_binding=0 bad_receipt_ancestry=0`. Synthesis `:75`, `:81` and the ask carry the strengthened rule. |
| T2 mixed valid-plus-dismissed batch absent | Fixed | `mixed_disposition_profiles` (`:78`), `mint_mixed_disposition` (`:97`), `b_mixed_batches` (`:520`) added; A/B/C report `mixed_disposition` 48/580/32, `mixed_upheld`/`mixed_overturned` equal, `bad_mixed_preservation=0`, and `mixed_exhaustion_cases` 16/144/8 with `bad_mixed_exhaustion=0`. |
| T3 early cross-owner reopen breaks initial priority | Fixed | Replaced by the state predicate `b_has_generation_one_work_before_initial` (`:824-827`); `deferred1`/`deferred_recheck1` added to the reducer (`:586-588`); `bad_reopen_before_initial=0`, `bad_deferred_identity=0`, and `deferred_early_findings=530` in the three-obligation sweep. Note the deferral machinery is structurally unreachable at `n <= 2`, so the headline `--obligations 2` run exercises it vacuously; the published `n = 3` sweep is what carries it. |
| T4 upheld A dismissal loses the prior streak | Fixed | `review_dismissed_*` preserves `state.streak` (`:260`); `a_dismissal_recheck_edges` routes a settled upheld batch through `a_settled` (`:199`), advancing the streak; `a_upheld_streak_trace` (`:1208-1224`) is asserted at `need == 2`. Risky plan and work runs report `upheld_prior_streak_complete=43 upheld_batch5_complete=1 bad_upheld_streak=0`. |
| T5 detached scope routing | Partly fixed — see **R5C-1** | Typed `ScopeRelation` (`:17-24`) and `awaiting_scope_recheck` are now inside `a_edges`, `b_edges`, and `c_edges`, and `bad_scope_spend`/`bad_scope_identity`/`bad_scope_delivery` are evaluated over real controller edges. Two of the eight `scope_routes` predicates remain scope-independent. |
| T6 replay counts a repeated fold mention | Fixed | `seen_folds` dedup (`q86-q78-scope-replay.sh:14`, `:35-40`); the eleven-pass control now expects four folds (`:121`); live and both self-tests reproduce the published summaries. |
| T8 brief states superseded `exploring` status | Fixed | `Q-86-convergence-mechanism-brief.md:5` now records the completed design pass and `open` status against the synthesis. Per the round-4 triage the absent plan pointer is not an independent violation, so I do not re-raise it. |
| T10 undefined `r_q` | Fixed for `r_q` — see **R5C-4** | `rg -n 'r_q' Q-86-synthesis.md` returns nothing; `:120` now uses `r_plan`/`r_work_q`. The sibling symbol `n_a` at `:222` remains undefined. |

## Checks that produced no finding

- **Every published command reproduces byte-for-byte.** Both all-mode runs at `--floor high` and `--floor critical`, the three inherited A-controller runs (`plan_review low_risk`, `plan_review risky`, `work_review risky`), the low-risk C acceptance run, and the `n = 0..3` B sweep all match `Q-86-synthesis.md:284-312`. `sha256sum` returns `d0dabe6da04fde2009a2baf22d0a3d9fabdfbd6bc96d2859d26043531aff579a`, matching `:314`.
- **Replay and selector.** `q86-q78-scope-replay.sh docs/metrics/workflow.jsonl` and `--self-test` return the published summaries at `:326` and `:332-333`. The `jq` selector at `:24` returns ten passes and `[7,10,5,6,5,5,4,2,1,0]`.
- **Arithmetic.** A: `14 + 7 + 7 + 6 = 34(m + 2)`; C: `5 + 4 + 4 + 2 = 15(m + 2)`; B: `R_B = 7 + 4|O| + p = 4|O| + m + 8` with `p = m + 1`, and `4R_B + 6 + 2|O| = 18|O| + 4m + 38`. `C_q = 4n_q + 1` matches the checker's `bound` (1, 5, 9, 13) and the observed maxima (1, 5, 9, 11) with the stated cardinality-two caveat; clean minima 1, 2, 3, 4 match `n_q + 1`. Whole-family minima `r_plan + sum(r_work_q) + 1`, `r_plan + |O| + m + 1`, `c_plan + sum(c_work_q) + 2` are consistent with the per-phase rows.
- **Q-78 evidence claims.** Pass 7 severities are `["medium","medium","low","low"]`; passes 8-10 carry `2 + 1 + 0 = 3` valid shortfalls, all `low`; passes 4-10 carry `6+5+5+4+2+1+0 = 23`; pass 3 carries a `high`. The retained triages `q78-acceptance-r3..r6-triage.md` each record a valid `high`, supporting `:87`. `jq` confirms 19 rounds with `outcome: "clean"` and `valid_findings > 0`, all advancing `consecutive_clean` (`:33`), and exactly one critical-bearing round (`:37`); `agent-scaffold.ledger.md:941` records the project's only `dismissal_recheck` and that it overturned.
- **Baseline non-admissibility** matches `AGENTS.md:51,56,57` (cap 5, streak 1/2, counter reset on resume) and `AGENTS.md:33` (acceptance runs no round loop or cap).
- **Source-to-projection currency.** `git diff main...HEAD -- docs/plans/agent-scaffold.md` touches exactly four hunks (the question list, the `workflow-calibration` narrative, the Q-86 question body, the Success Criterion), each matching its sidecar. `docs/metrics/workflow.jsonl` is unchanged, so `:5`'s decision-boundary sentence holds.
- **Migration inventory is executable.** Every surface named at `:359-365` exists (`pack/AGENTS.md`, `pack/instrument.md`, `pack/workflow.toml`, `.agents/workflow.toml`, `.agents/AGENTS.reference.md`, `.agents/LEDGER.template.md`, `AGENTS.md`, `README.md`, `CHANGELOG.md`), and `ReviewProcess`/`WorkflowSpec` exist in `src/`. The "shared typed review reconstruction" the chosen work must follow is the scheduled `review-loop-foreclosure-enforcement` step.
- **No-decision boundary is complete.** `:401` covers the five-plus-two slice, B's one reopen, C's four-stage/two-repair depth, the floor, and "every other controller constant"; the plan ask and both sidecars agree. Option-to-source mapping at `:13` matches the proposals' Candidate A/B and M1/M2/M3 headings, and M3's exclusion matches `Q-86-safety-process.md:344-354`.
- **Controller behaviour I could not break.** Foreclosure (`bad_foreclosure_state=0`, and every `active`/`repair`/`verify` state that cannot attain its suffix is unconstructible rather than merely unvisited); reserve unlock only on triage-valid serious evidence or an overturned dismissal; `accept_residual` blocked by any pending re-check, any at-or-above-floor outstanding finding, or any `untested` obligation; blind closure never authoring a repair; `LegacyNoRubric` unable to enter a campaign, claim historical credit, or become a zero-obligation campaign; C's acceptance blind-closure requirement at both risks; the bidirectional owner invariant including `deferred1`; and `open_exhausted`/`recheck_exhausted` terminality. Dropping a case from `check_successor`'s `rejected` tuple fails loudly with a `TypeError` rather than silently keeping `structured_cases=14`, so that literal is not a vacuous counter.
- **Not raised.** I checked whether a batch carrying both a serious dismissal and a proposed high/critical out-of-scope ruling would need two re-check calls and so exceed the "at most one re-check call" per-batch accounting behind `34(m + 2)`, `18|O| + 4m + 38`, and `15(m + 2)`. No reachable state in any controller holds both re-check kinds, but `Q-86-safety-process.md:255` settles the design question — an out-of-scope ruling on a high "is treated exactly like a dismissal and takes the same independent backstop re-check" — so one attached call covers both and the accounting stands.
