# Option B proof work review round 3 — reviewer (Claude)

## Scope and method

Reviewed product: `main...fba79947` — the 13 files under `docs/plans/workflow-calibration.proofs/`. No other path changes, so the planning-only boundary (sidecar acceptance 15) holds: `git diff main...HEAD --name-status` lists only the proof directory, and `git diff --check main...HEAD` is clean.

I read `AGENTS.md`, `.agents/prompts/reviewer.md`, the sidecar `docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md`, `q86-option-b-spec.md`, the round-1 and round-2 triages, and the whole proof product. I did not read the other round-3 reviewer's file.

**Two passes over the five exact commands.** I ran each of the five exact sidecar commands twice (ten invocations) from the repository root, each invocation with a fresh external state directory (`TMPDIR`/`TEMP`/`TMP`/`XDG_CACHE_HOME`/`HOME`/`PYTHONPYCACHEPREFIX` pointed into it) and `PYTHONDONTWRITEBYTECODE=1`, never changing the working directory. All ten exited 0 and each command's two passes produced byte-identical stdout and stderr:

```text
architecture=FrozenObligationsWithSealedPhaseCampaigns selected_floor=high suite=all
safety_failures=0 transition_failures=0 authority_failures=0 delivery_failures=0 legacy_failures=0 identity_failures=0 evidence_failures=0 product_failures=0 bound_failures=0
architecture=FrozenObligationsWithSealedPhaseCampaigns comparison_floor=critical suite=all
formula L_q=n_q+1 / C_q=4n_q+1 / L_B=r_plan+|O|+m+1 / R_B=4|O|+m+8 / I_B=18|O|+4m+38
manifest=q86-option-b valid_findings=51 executable_rows=30 resolved_rows=30 exercised_rows=30 killed_rows=30 unresolved=0
manifest=q86-option-b discovered_tags=185 mutations=185 unexercised=0 survived=0
```

`git status --porcelain=v1 --untracked-files=all` and a full path/type/content manifest of the working tree (537 entries, including ignored paths, excluding the Git administrative path) were byte-identical before the first and after the tenth invocation. Sidecar acceptance 13 is met for the exact commands.

**Independent derivations.** All confirmed against the sources rather than the reported numbers:

- 51 valid round-qualified verdicts: r1 13 + r2 12 + r3 9 + r4 8 + r5 9; every `### T<n>` heading in each retained triage is an em-dash T section (17/13/9/10/9), with no unconsumed level-three heading and no duplicate id.
- 185 mutations = 167 unique `# MUTATION_TAG:` lines in `q86-option-b-proof.py` + 18 in `q86-option-b-traceability.py`.
- 51 matrix rows = 30 executable + 12 durable-text + 9 option-b-inapplicable, no duplicate row id; `executable_rows=30` matches.
- Bound witnesses: `derive_coefficients` differences zero- and one-obligation transition executions and cross-checks them against the independent `campaign_transition_account` token capacity (4 review tokens per obligation + 1 non-transferable closure token); `AlgebraCoefficients(1, 1, 4, 1, 18, 4, 7, 34)` reproduces `L_q=n_q+1`, `C_q=4n_q+1`, `R_B=4|O|+m+8`, `I_B=18|O|+4m+38`.
- Replay conservation: `replay.json` carries non-zero spend (5 of 19 authority), and `independent_event_authority` sums it separately from the reducer.

**Behavioural evidence.** Every behavioural claim below was produced in a fresh `git archive HEAD` extract under `/tmp`, with only the stated scratch edit applied, then re-running the applicable exact commands from that extract's root with the same isolated-state discipline. The repository working tree was never modified.

## Round-2 corrections: verification

All twelve round-2 corrections were checked by re-running the original attack or by breaking the repaired code and confirming an exact command now fails. Eleven are closed; one is partially closed (F5).

| r2 | Status | Evidence |
| --- | --- | --- |
| T1 receipt/state forgery | closed | `_campaign_is_legal` now replays receipts (`q86-option-b-proof.py:1359-1403`). The exact r2 attack — every phase campaign forged to `ClosedReopen` with receipts `blind-closure` then `initial-review` — is rejected, as are closure-first reordering, forged `ClosedReopen` over clean receipts, a dropped receipt, a duplicated receipt, a forged starting history, and an unsupported history append. |
| T2 shared reducer defect | closed | Removing the authority decrement (`:1788-1792`) now fails both all-suite commands with `identity_failures=1` via `independent_event_authority` (`:1972-1985`, asserted at `:3099-3105`). |
| T3 earlier-batch referrals | closed | New `earlier-batch-referrals` oracle (`:2549-2598`), `closure-rejects-earlier-referrals` (`:1101-1106`) and pre-closure re-check (`:1061-1064`). Forcing `no_earlier_pending = True`, `opens = False`, or `matching_stage = record.closure_discovery` each fails the all-suite command. |
| T4 unchanged replan | closed | The registry rejection is now a compared snapshot field (`:1854-1866`, `:3105`). Weakening `GlobalRegistry` freshness makes `unchanged_replan_rejected` (`:1926-1930`) raise inside `check_replay`, so the rule is load-bearing, not just present. |
| T5 CLI floor boundary | closed | `run_suite` now takes `ParsedCommand` and asserts the parsed floor reached model construction (`:3782-3785`). Substituting `Floor.HIGH` at `:3774` fails `--floor critical` with `AssertionError: parsed CLI floor did not reach suite model construction` and fails `--floor high` with `safety_failures=1`. |
| T6 arbitrary history semantics | closed | Flattening every `products.json` `history_extensions` row to low/in-scope/valid now fails the all-suite command with `product_failures=1`. |
| T7 algebra partition | closed | Setting `algebra.json` `finite_cases` to `[]` now fails the algebra command with `bound_failures=1`. |
| T8 hard-coded delivery bound | closed | The `4 * len(expected_keys) + 1` clauses are gone from `_campaign_is_legal`; `C_q` is derived from `campaign_transition_account` (`:1216-1251`) with duplicate-spend and capacity mutations. |
| T9 cross-credit witness | closed | `run_mutation("mut-algebra-cross-credit")` now returns `(True, True, 'AssertionError: L_q=2 < n_q+1=3')`; the witness at `:3117-3120` runs before the maximum driver. |
| T10 decorative fixture names | closed | `campaigns.json` now uses model transition names, joined per obligation to `transition.credited_owners` at `:2394-2412` with `campaign-fixture-lifecycle-join`. |
| T11 dead representation | closed | `owner_digest` asserted at `:2321`; `history_digest` load-bearing in receipts and replay (`:796`, `:1162`, `:1203`); `maximum_phase_witness` asserted at `:3190`; `phase_accounts` checked at `:1354-1358` and `:3348`; `SourceFinding.title` removed. |
| T12 caller-owned bytecode | **partial** | The unlink is gone and a pre-existing-cache regression exists, but the in-process contract now *writes* a repository artefact instead. See **F5**. |

## Findings

Five findings: 1 critical, 1 high, 2 medium, 1 low.

### F1 — The family delivery-block predicate is dead; removing it leaves all five exact commands green

- **Severity:** critical.
- **Location:** `docs/plans/workflow-calibration.proofs/q86-option-b-proof.py:1428-1455` (`FrozenFamily.complete` `blocks` / `allowed`), with `PhaseCampaign.completed:746-766` and `_campaign_is_legal:1320-1416`.
- **Reproduction.** In a fresh `git archive HEAD` extract, make one edit — replace `allowed = legal_campaigns and not any(blocks)` (`:1454`) with `allowed = legal_campaigns and not any(blocks[:0])` — and run all five exact commands. All five pass:

  ```text
  --- cmd1 rc=0  safety_failures=0 ... bound_failures=0
  --- cmd2 rc=0  comparison_floor=critical, all zero
  --- cmd3 rc=0  all five formulas, all zero
  --- cmd4 rc=0  valid_findings=51 executable_rows=30 resolved_rows=30 exercised_rows=30 killed_rows=30 unresolved=0
  --- cmd5 rc=0  discovered_tags=185 mutations=185 unexercised=0 survived=0
  ```

- **Failure scenario.** With that single conjunct removed, four families built entirely from legal receipts construct `Complete`. Baseline rejects each; the mutant accepts each, and no command notices:

  | Trace (all receipts legal, no forged state) | baseline | predicate removed |
  | --- | --- | --- |
  | live `UnownedInScopeFinding`, severity `high`, retained by a real `initial_batch` | rejected | **`Complete` constructed** |
  | live `CompletedPriorOwner`, severity `high`, discovered in `acceptance` for `work-build` | rejected | **`Complete` constructed** |
  | unsettled `TerminalScopeDecision` (medium scope expansion) | rejected | **`Complete` constructed** |
  | blind-closure-discovered `CurrentOwner` `high` (`closure_owner_effect == closure-current-owner-block`) | rejected | **`Complete` constructed** |

  For each, `finding_blocks_delivery(record, Floor.HIGH)` is `True`, so these are exactly the states sidecar §Selected state item 6 and acceptance 4/6/9 forbid.

- **Why the suite misses it.** The eight `check_complete_gate` blocker cases (`:3394-3425`) build their blockers by appending a `FindingRecord` to `clean_campaigns[-1].history`. That is an unsupported history change, so `_campaign_is_legal` already returns `False` at the T1 replay-history check. I confirmed this directly: for the `live-current` blocker case, `_campaign_is_legal = False` and `replayed.history == campaign.history` is `False`. The eight assertions therefore re-test the T1 repair, never the predicate they name.
- **Second gate, same hole.** `_campaign_is_legal` never consults `PhaseCampaign.completed`, and `completed`'s closure hard-effect clause (`:755-766`) is also unexercised in the negative direction: deleting `and not any(item.closure_discovery and closure_owner_effect(item) in hard_effects ...)` leaves all five exact commands green (`185/185`, `30/30`). Every use of `completed` in the suite asserts it is `True`; nothing asserts it is `False`. So the only two gates that stop delivery over an unsettled closure block are both untested.
- **Correction.** Drive the blockers through legal transitions rather than by appending to history: retain a live unowned in-scope high, a live completed-prior high, a medium scope expansion, and a valid current-owner blind-closure finding through real batches, then assert `complete` rejects each and name the rejecting conjunct. Make `_campaign_is_legal` consume `campaign.completed`, and add a positive/negative assertion pair for its closure hard-effect clause.

### F2 — `_campaign_is_legal` branches on the active mutation name, so ten manifest kills are self-certifying

- **Severity:** high.
- **Location:** `q86-option-b-proof.py:1363-1364`, `:1382-1383`, `:1385-1395`.
- **Evidence.** Outside `point()` and `run_mutation`, the reference model reads the global `ACTIVE_MUTATION` in three places and unconditionally satisfies a legality conjunct for ten named mutations:

  ```python
  if ACTIVE_MUTATION == "mut-family-exact-owner-keys":        replay_required = True
  if ACTIVE_MUTATION == "mut-family-legal-settled-attempts":  attempt_state   = True
  if ACTIVE_MUTATION in { ... eight family-*-block names ... }: replayed_history = True
  ```

- **Reproduction.** Delete only those three blocks in a scratch extract. The all-suite command still passes (`rc=0`, nine zero counters) but the manifest command fails:

  ```text
  AssertionError: mutation failure: unexercised=[] survived=['mut-family-carried-block',
  'mut-family-dismissal-pending-block', 'mut-family-exact-owner-keys', 'mut-family-legal-settled-attempts',
  'mut-family-live-current-block', 'mut-family-live-future-block', 'mut-family-live-prior-block',
  'mut-family-live-unowned-block', 'mut-family-scope-pending-block', 'mut-family-terminal-scope-block']
  ```

- **Failure scenario.** Ten of the 185 reported kills are produced by model code that recognises the mutation's name and stands down a sibling check, not by the property the row names. Combined with F1, the eight `family-*-block` kills are pure artefacts: under the F1 mutant (predicate neutralised) those eight mutations are *still* reported killed, because the escape hatch — not the block predicate — is what lets the illegal campaign construct `Complete`. So `survived=0` and the traceability join's `killed_rows=30` overstate what the manifest establishes, contrary to sidecar line 196 and acceptance 12.
- **Correction.** Remove every `ACTIVE_MUTATION` reference from the model. Where a redundant guard masks a mutation, isolate the property with a dedicated oracle input (a campaign whose receipts legitimately produce the state under test) instead of disabling the guard by name.

### F3 — A registered oracle has no failure category, so its failure crashes the suite and skips ten later oracles

- **Severity:** medium.
- **Location:** `q86-option-b-proof.py:3798-3814` (`categories`) versus `@oracle("earlier-batch-referrals")` at `:2549`; the handler is `:3818-3819`.
- **Evidence.** `ORACLES` has 16 entries; `categories` has 15. The missing key is `earlier-batch-referrals` — the oracle added by the round-2 T3 repair, and the named assertion for three manifest mutations (`earlier-recheck-before-closure`, `earlier-recheck-opens-attempt`, `closure-rejects-earlier-referrals`).
- **Failure scenario.** Break anything that oracle covers (I used `opens = False` at `:1037`) and run `--suite all --floor high`:

  ```text
  AssertionError                      # from check_earlier_batch_referrals
  During handling of the above exception, another exception occurred:
    File ".../q86-option-b-proof.py", line 3819, in run_suite
      failures[categories[name]] += 1
  KeyError: 'earlier-batch-referrals'
  rc=1
  ```

  The command prints neither the `architecture=... selected_floor=high` line nor any of the nine counters, and the ten oracles registered after `earlier-batch-referrals` (blind-closure products, arbitrary history, successor, fresh evidence, legacy, floors, replay, algebra, complete gate, CLI floor) never run. The command does exit non-zero, so this fails closed; it does not permit a false green. But the contract in sidecar line 210 — the all-suite runs identify the floor and report the nine counters — is unmet whenever this oracle fails, and one failure hides the rest of the suite's results.
- **Correction.** Add `"earlier-batch-referrals": "transition"` (or the intended category) and make the mapping total by construction — for example, fail fast at import if `set(ORACLES) != set(categories)`.

### F4 — The reopen continuation for an earlier-batch referral is unreachable in the suite, though it is a legal delivering product

- **Severity:** medium.
- **Location:** `q86-option-b-proof.py:1044-1049` (the second and third branches of `_open_attempt_after_earlier_recheck`).
- **Evidence.** Replace both branch bodies with `raise AssertionError("DEAD-BRANCH reached")` in a scratch extract: `--suite all --floor high` passes with nine zero counters and the manifest reports `185/185, unexercised=0 survived=0`. Neither branch is reached by any oracle, fixture, or mutation. `check_earlier_batch_referrals` (`:2550-2598`) only ever uses a one-owner phase where the referral belongs to the batch's own scheduled owner, so only the first branch (`initial_match`, `CLOSED_INITIAL -> OPEN_INITIAL`) executes.
- **Failure scenario.** The branch is reachable and delivering, so this is missing coverage of a required legal product, not defensive code. Building a two-owner phase where batch 1 (scheduled `O-0-0`) retains a serious dismissal against `O-0-1`, then batch 2 schedules `O-0-1`:

  ```text
  after batch2:            {'O-0-0': ClosedInitial, 'O-0-1': ClosedInitial}
  after overturn:          {'O-0-0': ClosedInitial, 'O-0-1': OpenReopen}   reopened: ('O-0-1',)
  after repair+verify:     {'O-0-0': ClosedInitial, 'O-0-1': ClosedReopen}
  complete: True  batches: 4
  ```

  This is exactly the cross-owner continuation the round-2 T3 correction required ("open the matching attempt on overturn") and that `q86-option-b-spec.md:90` asserts ("opens that finding's matching initial **or reopen** attempt"). Its rejection sibling — an overturned referral with no matching attempt authority — is equally untested, so a regression that silently fabricated authority there would pass every command.
- **Correction.** Add a fixture and oracle case for a cross-owner earlier-batch referral overturned after its owner's own scheduled batch, asserting the `OPEN_REOPEN` transition, the reopen-authority accounting, and the rejection when no attempt authority exists; tag both branches.

### F5 — The public in-process runner writes bytecode into the live planning tree (round-2 T12 only partly closed)

- **Severity:** low.
- **Location:** `q86-option-b-mutations.py:8` (`sys.dont_write_bytecode = True`) and `:101-105` (the before/after snapshot).
- **Evidence.** The suppression executes in the module body, which runs *after* the loader has already compiled and cached the module's own bytecode. In a fresh `git archive HEAD` extract with `PYTHONDONTWRITEBYTECODE` unset, importing the runner through the documented shared in-process contract:

  ```text
  before:              []
  after import:        ['docs/plans/workflow-calibration.proofs/__pycache__',
                        'docs/plans/workflow-calibration.proofs/__pycache__/q86-option-b-mutations.cpython-313.pyc']
  sys.dont_write_bytecode now: True
  after run_manifest:  (unchanged)   entries: 185
  ```

  `run_manifest`'s own guard cannot see this: `bytecode_before` is computed at `:101`, after the runner module was loaded, so `bytecode_after != bytecode_before` is never true for its own cache file. `__pycache__` is not in `.gitignore`, so the file is an untracked repository artefact in the live planning tree, contrary to sidecar lines 196 and 214. The round-2 finding was the mirror image (deleting a caller-owned cache file); the repair changed the direction but not the class.
- **Scope.** The five exact commands remain clean — they set `PYTHONDONTWRITEBYTECODE=1`, and I confirmed the working-tree manifest is unchanged after all ten invocations. I also confirmed that running each of the three scripts directly *without* the environment flag leaves no `__pycache__`, because `__main__` is never cached and the sibling loads happen after line 8. Only the exposed `run_manifest` import path leaks, which is why this is low rather than higher.
- **Correction.** Either load the runner through a wrapper that sets `sys.dont_write_bytecode` before `spec.loader.exec_module`, or document that callers must suppress bytecode before importing it and snapshot the tree before the runner module is loaded, not after. Extend the existing regression to cover the runner's own module file.

## Severities with no findings

- **No further critical findings** beyond F1.
- **No further high findings** beyond F2.
- I found **no** finding in these areas: the traceability source derivation and disposition partition (checker rejects a duplicate identity, an incomplete matrix, an overlapping partition, a wrong returned manifest, an unknown/surviving/unexercised row mutation, a dropped count assertion, and a suppressed report field, each through the shared in-process `run_manifest` join); the freeze fail-closed cases; the sealed plan-review account; the successor registry and fresh-evidence rules; legacy gating; terminal-floor tables; determinism and repository cleanliness of the exact commands; and the planning-only file boundary.
- **Hard-coded reports:** checked and clean. `report_fields`/`main` in the checker compute all four row counts in-invocation, and `print_algebra` renders the five formulas from `derive_coefficients` rather than from literals. The `assert coefficients == AlgebraCoefficients(1, 1, 4, 1, 18, 4, 7, 34)` at `:3189` compares derived values against the published constants, which is the intended direction.
- **One redundant-but-dead conjunct not counted as a finding:** dropping `and not campaign.deferred_reopens` at `:1404` leaves all five commands green, but `blind_closure` (`:1106`) already refuses while deferred reopens exist, so `closure_evidence` rejects the same campaigns. It is defensive duplication, not a hole.

## Outcome

- **Findings:** 5 — 1 critical, 1 high, 2 medium, 1 low.
- **Round-2 corrections closed:** 11 of 12; T12 partially closed (F5).
- F1 and F2 together mean the central Option B delivery gate is unproved and the manifest's `survived=0` overstates coverage, so this round is not clean.
