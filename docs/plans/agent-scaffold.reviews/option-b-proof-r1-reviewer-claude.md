# `bounded-convergence-option-b-proof-inc1` round 1: REVIEWER, executability and mutation-adequacy lens

Independent reviewer. I did not write this change. I read `AGENTS.md`, `.agents/prompts/reviewer.md`, the step sidecar `docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md`, all 13 new proof artefacts, and all five retained triages, and I re-derived every number below myself. I did not consult any other reviewer's work.

My lenses are executability, traceability, mutation adequacy and boundary. The governing question is the one the step sets in acceptance criterion 14: whether the green output distinguishes this model from an unsound one. On four points it does not.

## Artefact, commands, and how I ran them

- Worktree `.agents/worktrees/option-b-proof-r1-claude`, branch `review/option-b-proof-r1-claude`, tip `1ef6ad97` ("test: prove bounded convergence Option B"), against `main` at `3a285aac`.
- `git diff --name-only main...HEAD` is exactly the 13 named proof artefacts under `docs/plans/workflow-calibration.proofs/`. No production file, pack source, generated copy, README, changelog, metrics schema, ledger line or historical event is touched (criterion 15 holds).
- `grep -nE "^\s*(import|from)\s" docs/plans/workflow-calibration.proofs/*.py` resolves to the standard library only; no production controller is imported.

I ran all five exact commands from the repository root twice, ten invocations. Before each individual invocation I created a fresh temporary directory outside the repository with `mktemp -d` and pointed `TMPDIR`, `TEMP`, `TMP`, `PYTHONPYCACHEPREFIX`, `XDG_CACHE_HOME`, `XDG_STATE_HOME`, `XDG_DATA_HOME` and `XDG_RUNTIME_DIR` at it; the working directory stayed at the repository root throughout (`env -C`, never `cd`). I captured each invocation's stdout, stderr and exit status into that state, compared each command's two passes, and removed both states afterwards.

| command | pass 1 | pass 2 | passes identical |
| --- | --- | --- | --- |
| `--suite all --floor high` | exit 0 | exit 0 | yes, byte-identical stdout and stderr |
| `--suite all --floor critical` | exit 0 | exit 0 | yes |
| `--suite algebra --floor high` | exit 0 | exit 0 | yes |
| traceability | **exit 1** | **exit 1** | yes, identical traceback |
| mutations `--all` | exit 0 | exit 0 | yes |

Before the first invocation I captured `git status --porcelain=v1 --untracked-files=all` and a path/type/content manifest of the complete working tree, 530 entries, including ignored paths and excluding only `.git`, with a SHA-256 per regular file and the target of each symlink. After the tenth invocation both snapshots were byte-identical: `diff` on the status output and on the manifest both returned empty. **No tracked, untracked or ignored repository artefact was created, removed or changed by the ten invocations.** That half of criterion 13 holds. The other half does not, because command four fails.

Every demonstration below was run against a `git archive HEAD | tar -x` extract in `/tmp`, never against the repository tree, which I re-verified byte-identical to its baseline manifest after all of it.

## Findings

One critical, three high, three medium, three low. By severity: **critical** F2; **high** F1, F3, F4; **medium** F5, F6, F7; **low** F8, F9, F10. They are numbered in reading order rather than severity order because the later ones cite the earlier ones.

### F1 — The traceability command fails at the reviewed tip, because a gate row cites a transient orchestrator-owned ledger anchor

- **Severity:** high.
- **Evidence.** The fourth exact command exits 1 on both passes with an identical traceback:

  ```
  File ".../q86-option-b-traceability.py", line 278, in validate_non_executable_rows
    raise ValueError(f"unresolved durable pointer: {row.identity}")
  ValueError: unresolved durable pointer: R1-T12
  ```

  `q86-option-b-traceability.md:19` gives R1-T12 the evidence pointer `docs/plans/agent-scaffold.ledger.md#OPTION B PROOF IMPLEMENTATION IN PROGRESS`. `grep -c "OPTION B PROOF IMPLEMENTATION IN PROGRESS" docs/plans/agent-scaffold.ledger.md` returns 0 at this tip; the live anchor now reads `RESUME HERE (2026-08-30, OPTION B PROOF WORK REVIEW ROUND 1 READY)`. `git log -S` on that string shows it was introduced by `cca17cab` and removed by `3a285aac`, and `git diff --stat e76367cb 1ef6ad97` shows the proof commit was rebased from `cca17cab` onto `3a285aac` with the 13 artefacts unchanged and only the ledger differing. So the proof was authored while the anchor happened to hold the cited phrase, and the orchestrator's own anchor advance broke the gate.

  I resolved all twelve `durable-text` pointers independently with `grep -F`: eleven resolve, R1-T12 is the only failure. Patching only that one pointer in the scratch extract makes the command pass and print the contracted summary `manifest=q86-option-b valid_findings=51 executable_rows=30 resolved_rows=30 exercised_rows=30 killed_rows=30 unresolved=0`, so R1-T12 is the sole blocker.

- **Consequence.** Acceptance criteria 11 and 13 are unmet at the reviewed tip, and the ledger's claim that "All five exact commands pass" is false here. The deeper defect is structural: R1-T12's own required correction (`q86-synthesis-r1-triage.md:113`) says the fix is an orchestrator integration action, and the step sidecar says "Advancing the ledger's authoritative resume anchor is an orchestrator integration duty; the planner neither asserts that anchor is current nor edits the ledger". Binding a proof gate to a phrase in the live RESUME paragraph guarantees the gate breaks again on the next anchor move, and it makes the proof's reproducibility depend on transient state the proof does not own.
- **Correction.** Re-point R1-T12 at a durable planning source that records the anchor duty rather than at the anchor's current text: the step sidecar's own sentence about the resume anchor being an orchestrator integration duty is a stable target in a file this unit already cites. Do not merely update the phrase to the current anchor, which reproduces the defect. Separately, consider constraining `durable_pointer_resolves` to reject `agent-scaffold.ledger.md` as a durable-text target, since the ledger is by contract transient and deleted at task close.

### F2 — The family-completion delivery predicate is unexercised: the model's central safety claim can be deleted and every oracle still reports zero failures

- **Severity:** critical.
- **Evidence.** `FrozenFamily.complete` (`q86-option-b-proof.py:831-849`) is the only constructor of `Complete`, and it is only ever called from `check_complete_gate` (`:1912-1940`), which builds a family whose every campaign batch has **no findings at all** (`ReviewBatch(obligation_id, ())`, `ReviewBatch(None, ())`). Consequently the `delivery_blocks`, `route_blocks` and `pending_axes` conjuncts are only ever evaluated over an empty finding map. I confirmed this with three source mutations against the scratch extract, each re-running the full `--suite all` oracle set:

  | mutation applied to `q86-option-b-proof.py` | full suite result |
  | --- | --- |
  | `allowed = exact and all_closed and not delivery_blocks` (drop `route_blocks` and `pending_axes`) | still passes, zero failures |
  | `allowed = exact and all_closed` (drop the whole finding map from the predicate) | still passes, zero failures |
  | `finding_blocks_delivery` returns `False` for `COMPLETED_PRIOR`, `FUTURE` and `UNOWNED` routes | still passes, zero failures |

  The third is the decisive one. `finding_blocks_delivery` (`:596-615`) never inspects `owner_route` at all: an out-of-phase finding blocks only incidentally, through the final `return record.live`. The tests call it three times (`:1522`, `:1536`, `:1538`). Two of those pass `CurrentOwner` records; the third, `:1522`, does pass completed-prior, future-owner and unowned records, but only as *upheld dismissals*, which return `False` at `:610` before any of the route or liveness logic runs, so the assertion `assert not finding_blocks_delivery(upheld_record, Floor.HIGH)` holds identically under my mutation. No test ever passes it a live, triage-valid out-of-phase record, and no test ever runs a family carrying one through `complete()`. The single `mut-family-completion-predicate` tag is killed only by the coarse `family.complete((incomplete,))` case at `:1936`, whose `exact` and `all_closed` conjuncts already fail on their own. `route_blocks` is in any case dead: it is by construction a subset of `delivery_blocks`. `pending_axes` can differ from `delivery_blocks` only for a record already `RESOLVED` or `NON_DELIVERY`, which `:597-598` excludes first, and no test constructs that case either.

  The same gap covers serious carry. `serious_delivery_blocked` (`:1099-1102`) is asserted only as a standalone boolean in `check_successor` (`:1689`); no successor family is ever driven through campaigns to `complete()`, so the `CARRIED` branch of `finding_blocks_delivery` (`:612-614`) is never reached from the delivery gate.

- **Consequence.** This is exactly the "unsafe delivery path" the step's failure clause names. The proof's whole purpose is to establish that Option B cannot construct `Complete` while a completed-prior-owner, future-owner or unowned in-scope route is live, or while a scope or dismissal re-check is pending. A model that permits all of those produces identical green output. Acceptance criteria 4 and 6 ("Family `Complete` remains impossible until every prior- and future-owner route and every closure re-check settles", "no live in-scope or carried finding remains") are asserted in the spec prose and in `q86-option-b-spec.md:113-121` but not established by any executable assertion or mutation.
- **Correction.** Add oracles that construct a `FrozenFamily`, run its campaigns to the point where every phase is closed, and then assert `complete()` raises, once per blocking condition: a live `UnownedInScopeFinding`; a live `CompletedPriorOwner` finding; a live `FutureOwnerPending` component whose canonical campaign has not settled it; an identity in `AwaitingScopeRecheck`; an identity in `AwaitingDismissalRecheck`; and a successor family carrying a live high at floor `high`. Give each its own manifest tag so the predicate is decomposed rather than covered by one coarse mutation. Replace or delete the dead `route_blocks` and `pending_axes` conjuncts once the real assertions exist.

### F3 — `L_q` and `C_q` are asserted, not derived from the transition relation, and the sidecar's required in-domain cross-credit witness is absent

- **Severity:** high.
- **Evidence.** The sidecar requires the bound to be a conclusion of the transition relation, and names the exact witness: for `O_q = {A, B}`, mutate A's scheduled clean initial batch so it also credits B, "then run the explicit clean blind-closure discovery and continue to family `Complete`", and the mutant's measured `L_q` must satisfy `L_q < n_q + 1`.

  The implementation does not do this. `clean_delivering_phase` (`:1262-1277`) is a standalone counting loop over owner-name strings that never constructs a `PhaseCampaign`, never calls `initial_batch` or `blind_closure`, and never constructs `Complete`; its closure batch is the literal `batches += 1` at `:1275`. `delivering_domain` (`:1280-1282`) is called only with hand-written literals: `delivering_domain(complete, True, False, 0)` at `:1885`, `:1892`, `:1907` and `delivering_domain(True, False, True, 1)` at `:1902`. Nothing measures a real execution's state. `derive_bounds` then assigns the published formulas directly:

  ```
  1233:    l_q = n_q + 1
  1234:    c_q = 4 * n_q + 1
  1237:    r_b = normal + reserve + 4 * total_obligations + phases
  1238:    per_obligation_agents = 4 * review_batch_agents + repairs_per_obligation
  ```

  I traced which assertion kills each relevant mutation by activating it and capturing the traceback:

  | mutation | killed by |
  | --- | --- |
  | `mut-algebra-cross-credit` | `assert phase_batches == owner_count + 1` (`:1888`), on the standalone counter |
  | `mut-scheduled-owner-only-credit` | `assert states["B"] == ObligationAttempt.UNTESTED` (`:1411`), a direct observation of the credit rule |
  | `mut-minimum-domain-independent` | `assert not delivering_domain(True, False, True, 1)` (`:1902`), on literals |
  | `mut-cost-per-obligation-coefficient` | `assert bounds.i_b == 18 * total + 4 * work_loops + 38` (`:1900`), against the same published literal |

  So the coefficient is checked against itself, and the credit rule is checked by looking at it rather than by measuring the cost of a delivering execution.

  The model does support the required witness; the proof simply does not contain it. I built it in about twenty lines against the real transition model, freezing two obligations into `work-build` and one into `acceptance`, driving each phase through `initial_batch` per untested owner and then `blind_closure`, and calling `FrozenFamily.complete`:

  ```
  unmutated                       : {'work-build': 3, 'acceptance': 2} -> Complete
  mut-scheduled-owner-only-credit : {'work-build': 2, 'acceptance': 2} -> Complete
  ```

  Both reach the independently observable complete domain; the mutant does it in two phase batches against an unmutated minimum of three, that is `L_q = 2 < n_q + 1 = 3`. That is the sidecar's witness, and it is missing.

  `C_q` is worse than undeclared: it disagrees with the model. Driving one obligation through its full published lifecycle on the transition model, initial review, repair, initial verification, fresh-evidence reopen, reopen repair, reopen verification, then blind closure, the campaign's own `batches` counter reads 4, because `reopen` (`:741-753`) attaches evidence and moves the state to `OPEN_REOPEN` without incrementing `batches`, so the model has no "reopen review" batch transition at all. The published `C_q = 4n_q + 1` gives 5. The only cross-check on the literal is `assert len(maximum_phase_witness(owner_count)) == 4 * owner_count + 1` (`:1889`) against `maximum_phase_witness` (`:1246-1259`), a generator that emits exactly four label strings per owner. That is a tautology, not a derivation, and the model contains two mutually inconsistent notions of "batch".

- **Consequence.** The published bound is not violated, 4 is below 5, but acceptance criterion 10 requires the command to *derive* `L_q`, `C_q`, `L_B`, `R_B` and `I_B`, and the sidecar states that "Hard-coding the published formula without deriving every coefficient is a proof failure" and that a coefficient the transition model does not establish must be withdrawn. The unbacked literal `4` propagates into `C_q`, `R_B` and `I_B`, so the entire cost side rests on it. Because the derivation is what a future implementation's controller constants would be taken from, this is decision-material.
- **Correction.** Replace `clean_delivering_phase` with a measurement over real `PhaseCampaign` executions: count `batches` on phases driven to `blind_closure` inside families driven to `Complete`, and derive `delivering_domain` membership from the resulting objects rather than from literal arguments. Add the two-owner cross-credit witness above as a named oracle so `mut-scheduled-owner-only-credit` is killed by an `L_q` measurement, not by inspecting the credit set. Either give `reopen` its own counted review batch so the model's per-obligation maximum is genuinely 4, or withdraw the `4` and re-derive `C_q`, `R_B` and `I_B` from the measured maximum and the typed costs in `algebra.json`.

### F4 — The replay oracle compares one computation against itself; the five views and the event fixture are inert

- **Severity:** high.
- **Evidence.** `replay_view` (`:1172-1193`) calls `reduce_replay(events)` with the same events for every view; the `view` argument selects only which mutation tags are applied to the result. `check_replay` (`:1861-1869`) then sets `expected = reduce_replay(events)` and asserts `all(snapshot == expected for snapshot in snapshots)`, which is `f(x) == f(x)` by construction. There is no resume, rename, rebuild or unchanged-replan reconstruction to compare; the `unchanged_replan` event kind is `continue` at `:1141-1142`.

  Five of the nine compared fields are constants that never read the event stream: `predecessor_spend = 7` (`:1121`), `remaining = 19` (`:1123`), `"family-proof-1"` (`:1148`), and architecture and floor from module constants (`:1146-1147`). Line `:1868` then asserts the hard-coded family id against itself.

  Demonstration, against the scratch extract, editing only `fixtures/replay.json`:

  | `replay.json` events | `check_replay` |
  | --- | --- |
  | shipped 10-event stream | passes |
  | `[]` (empty) | **passes** |
  | one event repeated three times | **passes** |

  The 50 replay mutation tags (`grep -c '^# MUTATION_TAG: replay-'` returns 50 of the 111 proof tags, 50 of 129 including the checker) are killed only because `replay_view` deliberately perturbs its own output at `:1180-1186` and `:1188-1192`: adding 1 to an integer or appending `("drift","drift")` to a tuple makes an equality against the unperturbed copy fail. That is a test that arithmetic works, not that a reconstruction preserves authority.

- **Consequence.** Acceptance criterion 4's replay clause and the sidecar's replay-oracle paragraph are not established. The specific claim the step cares about, that an unchanged replan "cannot mint a successor family, reset spend, reopen settled evidence, or replenish any review or closure authority", has no executable content: the unchanged-replan view is the baseline function under a different tag prefix. 39% of the manifest is self-certifying, so the `survived=0` headline overstates mutation adequacy by a large margin.
- **Correction.** Give each view a genuinely distinct reconstruction path and compare across paths, not against a copy of one path. At minimum: derive `predecessor_spend`, `remaining_authority` and `family_id` from the event stream and the `PlanReviewAccount`/`FrozenFamily` objects rather than from constants; make `resume` reconstruct from a serialised snapshot; make `rename` and `rebuild` change presentation or artefact identity and assert authority identity is unchanged; and make `unchanged_replan` attempt an actual successor mint through `GlobalRegistry.authorise_successor` and assert it is rejected. Then the 50 drift and replenishment mutations acquire meaning.

### F5 — Named product, campaign, successor and legacy fixture bodies are dead data

- **Severity:** medium.
- **Evidence.** I corrupted individual fixture keys in the scratch extract and re-ran the full suite:

  | fixture, key corrupted | full suite |
  | --- | --- |
  | `products.json`, every batch's `scheduled_owner` and `findings` removed, `name` kept | **still passes** |
  | `products.json`, one batch renamed | fails (`finite-products`) |
  | `campaigns.json`, every phase's `obligations` emptied | **still passes** |
  | `campaigns.json`, one `maximum_attempts` entry dropped | fails (`owner-routing`) |
  | `successors.json`, `families` emptied | **still passes** |
  | `successors.json`, `receipt.predecessor_spend` corrupted | fails (`successor-registry`) |
  | `legacy.json`, `forbidden` emptied | **still passes** |
  | `terminal-choices.json`, an extra floor added | fails (`terminal-floors`) |

  The reads confirm it. `check_finite_products` (`:1428-1436`) consumes only `{item["name"] for item in fixture["batches"]}`; the `owners`, `phases`, `scheduled_owner` and `findings` values in `products.json` are never read, and every record it exercises is hand-built in Python at `:1438-1451`. `check_owner_routing` (`:1391-1393`) reads only each phase's `id`, its `closure` string and the *length* of `maximum_attempts`; `obligations` is unread. `check_terminal_floors` (`:1809-1811`) asserts three fixture lists equal the corresponding enum member sets, which restates the enums rather than constraining them.

- **Consequence.** The sidecar's "Named product fixtures cover at least these cases in every authority state where they are legal" is satisfied in name only: `products.json` is a list of six labels, and the sidecar's enumerated cases (low plus critical, high plus critical, valid plus serious dismissal in one batch, separate scope-referral and dismissal-referral ids, dual pending re-checks, and the rest) are neither present in the fixture nor driven from it. A future reader auditing coverage by reading the fixtures would be badly misled, and a fixture edit intended to add a case would have no executable effect.
- **Correction.** Drive the product oracles from `products.json`: parse each batch into `FindingInput` values using the fixture's `owners` map and `scheduled_owner`, run them through `PhaseCampaign.initial_batch`, and assert the credit and route outcomes per batch. Extend the fixture to the cases the sidecar enumerates. Delete `terminal-choices.json`'s enum mirrors or replace them with the receipt/floor matrix the spec's table describes, and either consume `campaigns.json`'s `obligations` and `successors.json`'s `families` or remove them.

### F6 — `--floor` selects only an output label, and no family or `Complete` is ever constructed at `critical`

- **Severity:** medium.
- **Evidence.** `main` (`:2227-2239`) passes only `args.suite` to `run_suite`; `args.floor` is used at `:2233-2235` to choose between the strings `selected_floor` and `comparison_floor`. The two all-suite commands therefore execute identical code and differ in exactly one printed token, which the two captured stdout files confirm.

  `FreezePending.freeze` hard-codes `selected_floor=Floor.HIGH` (`:805`), so a `FrozenFamily`, and therefore a `Complete`, can only ever exist at floor `high`. The floor argument threaded into `FrozenFamily.complete` (`:837`, `:842`) reaches `finding_blocks_delivery`, which is floor-insensitive: its `CARRIED` branch is `record.severity.rank >= threshold or record.live` (`:613-614`), and `CARRIED` is a member of the `live` set (`:391-395`), so the disjunction is always `True` and `threshold` is dead. Measured directly: a carried `low` finding blocks at `Floor.HIGH` and at `Floor.CRITICAL` alike.

- **Consequence.** Acceptance criterion 1 requires that "both floors pass the complete model". The complete model is never run at `critical`, and cannot be. Criterion 9's terminal-choice coverage is met, but by `check_terminal_floors`'s internal `for floor in Floor` loop rather than by the command, so the second exact command adds one bit of coverage over the first. No mutation covers the `selected_floor`/`comparison_floor` label mapping, so swapping it would pass.
- **Correction.** Thread the parsed floor into `run_suite` and into `FreezePending.freeze` so a `critical` family is constructible, and add a `Complete` case per floor with an open high, asserting it is blocked at `high` and permitted at `critical`. Remove the dead `or record.live` from the `CARRIED` branch so the floor threshold is load-bearing, and add a mutation tag for it.

### F7 — Deferred reopen retention is dead state, and the one-reopen-per-obligation guard is unexercised

- **Severity:** medium.
- **Evidence.** `PhaseCampaign.deferred_reopens` is declared at `:653`, computed at `:688-693` and stored at `:697`, and is read by nothing: no transition consults it, no assertion inspects it, and it carries no `MUTATION_TAG`. `blind_closure` (`:755-784`) gates on `closed_states` and `current_live` only. Replacing `deferred = set(self.deferred_reopens)` with `deferred = set()` leaves the full suite passing.

  Likewise the guard `raise ValueError("each obligation has at most one reopen")` at `:751` has no tag and no test: replacing the `raise` with `pass` leaves the full suite passing. I verified the guard itself is correct by driving a second reopen against the real model, which is rejected; the defect is coverage, not behaviour.

- **Consequence.** The sidecar requires that "An incidental finding against a closed current-phase owner is retained immediately as a live deferred reopen, but its reopen work waits until every obligation in that phase has received its scheduled initial attempt", and acceptance criterion 4 requires "one fresh-evidence reopen per obligation". The first is modelled as a write-only field, and the second is an unexercised branch. Both are load-bearing transitions with no mutation, which the sidecar's mutation-control clause says must fail ("A load-bearing tag without a mutation fails"); they escape because the tag census is driven by `# MUTATION_TAG:` comments, so an untagged guard is invisible to the census rather than reported.
- **Correction.** Assert `deferred_reopens` after a cross-owner batch that hits a closed owner, and make `reopen` require the finding's obligation to be in that set, so the field becomes load-bearing; add a tag for it. Add a tag and an oracle for the second-reopen rejection. Consider making the census also enumerate `point(` call sites so an untagged guard is reported rather than silently uncounted.

### F8 — `print_algebra` reports hard-coded strings, not model output

- **Severity:** low.
- **Evidence.** `print_algebra` (`:2205-2224`) prints the five formulas as string literals (`print("formula L_q=n_q+1")` and so on), and prints the minimum-domain line, the premise list `premises exact-ownership scheduled-owner-only-credit blind-closure no-transfer checked` and `early-paths terminal=constructible non-delivery=constructible delivery=false` as fixed strings. Only the `typed-costs sample_...` line is computed, from `derive_bounds(3, 7, 2, "risky")`. `check_algebra` builds exactly one early path, `early_terminal_path()` (`:1285-1287`, an `ABANDON` receipt), although the printed line claims both a terminal and a non-delivery path are constructible.
- **Consequence.** The sidecar says the algebra run "prints the five formulas above from the model" and "reports every premise checked". A reader of the command output cannot distinguish a model that derives these from one that does not, which is what made F3 hard to see from the green output.
- **Correction.** Render the formula strings from the same expressions `derive_bounds` evaluates, or from a symbolic form the oracle checks, and emit the premise and early-path lines from the set of checks that actually ran rather than from literals. Construct a distinct non-delivery path if the line is to claim one.

### F9 — The shared in-process `run_manifest` contract writes `__pycache__` into the planning tree for any caller that does not set `PYTHONDONTWRITEBYTECODE`

- **Severity:** low.
- **Evidence.** The step exposes `run_manifest(manifest_name) -> MutationRunResult` as the shared in-process contract a future validator or scheduler is expected to call. In a scratch extract, importing `q86-option-b-mutations.py` by path and calling `run_manifest("q86-option-b")` without `PYTHONDONTWRITEBYTECODE=1` creates `docs/plans/workflow-calibration.proofs/__pycache__/` containing three `.pyc` files, because `modules()` (`:47-53`) and `load_module` (`:37-44`) execute the sibling sources from disk. `.gitignore` does not list `__pycache__`, so those would be untracked repository artefacts. The five exact commands set the variable, so criterion 13 is unaffected; the exposure is to the in-process contract the sidecar itself anticipates.
- **Correction.** Set `sys.dont_write_bytecode = True` at the top of `q86-option-b-mutations.py` and `q86-option-b-traceability.py`, so the property holds for any caller rather than only for callers that remember the environment variable.

### F10 — `modules()` silently drops all eighteen checker mutation classes when the traceability file is absent

- **Severity:** low.
- **Evidence.** `q86-option-b-mutations.py:47-53` loads the checker only `if checker_path.exists()`, and otherwise returns `(proof,)`. `run_manifest` then compares discovered against declared tags within whatever set was loaded, so a run without `q86-option-b-traceability.py` reports `discovered_tags=111 mutations=111 survived=0` and exits 0, with all eighteen mandatory checker controls (the in-process load, the `run_manifest` call, the fabricated result, the manifest selection, the row join, the four count reports, and the rest) silently absent.
- **Consequence.** The sidecar makes those classes mandatory. A passing `survived=0` line is not evidence that they ran, and the counts it reports give no way to tell 111 from 129 without knowing the expected total.
- **Correction.** Make the checker module required rather than optional, and fail loudly if it is missing.

## Checks that came back clean

Stated explicitly so the triager can see what was covered and did not yield a finding.

- **The 51 valid identities.** I derived them independently of the checker, by listing every `^### T<n>` heading and every `^- \*\*Verdict` line in the five retained triages and pairing them by section. R1 has 17 sections of which T9, T13, T15 and T17 are invalid, giving 13; R2 has 13 of which T13 is invalid, giving 12; R3 has 9, all valid; R4 has 10 of which T7 and T9 are invalid, giving 8; R5 has 9, all valid. 13 + 12 + 9 + 8 + 9 = **51**, matching the contracted `valid_findings=51`. Every heading is a T section, so the checker's "unconsumed section" guard has nothing to trip on here, and its `len(headings) != len(all_level_three)` check is a genuine fail-closed guard.
- **Matrix identity set.** The 51 matrix rows are exactly my derived set, row by row, with no duplicate, no extra and no omission. The disposition partition is 30 executable, 12 durable-text, 9 Option-B-inapplicable; applicable and inapplicable are disjoint and their union is the source set. The checker computes this rather than comparing against a stored list, and `partition_is_valid`, `validate_source_matrix` and the count-equality assertion each carry a mutation that its self-test kills.
- **Option-B-inapplicable rows.** I read each of the nine underlying triage findings. R1-T1, R1-T5, R2-T9, R3-T5 and R3-T7 concern the A or C controllers; R3-T9, R4-T6, R5-T7 concern the retained Q-78 replay prototype, which the sidecar excludes as a proof input; R5-T8 concerns superseded graph counts in the state-machine proposal. Each row names a shared invariant (`terminal-floors`, `algebraic-bounds`, `blind-closure-products`, `post-freeze-replay`, `selected-state`) that is a real oracle name, and the checker enforces `row.assertion in properties` against the returned manifest's property names. I found no row that should have been applicable.
- **Matrix topic coverage.** All thirty topics the sidecar requires the matrix to close map onto at least one row.
- **The traceability join is real, not embedded.** `load_and_run_mutations` (`traceability.py:186-196`) loads the module named by `--mutation-runner` and calls `run_manifest` with the name from `--mutation-manifest` in the same process; `evaluate_executable_rows` resolves row mutations only against the returned entries and raises on an unknown name; `validate_manifest` rejects a wrong returned manifest and mismatched counts. There is no result file, cache or embedded expected map anywhere in the checker, and no hard-coded identity list or count. The eighteen checker tags cover omission of the load, the wrong manifest name, a fabricated result, a dropped row join, a suppressed count and each of the unknown, surviving and unexercised acceptances.
- **Row-to-mutation binding.** Every executable row's named mutations resolve to entries whose registered `property_name` equals the row's assertion (`evaluate_executable_rows:237`), and a multi-mutation row counts only when every name qualifies, which the self-test verifies with a mixed killed/surviving pair.
- **Tag census integrity.** `discovered == declared` holds in both modules (111 and 18), and every `point("literal", ...)` tag in the proof source is declared; I diffed the two sets and the difference is empty. Unexercised and surviving mutations both fail closed in `run_manifest`.
- **Freeze fail-closed.** `check_freeze` rejects all five malformed cases (missing locator, duplicate id, owner outside the registry, free-form kind, empty id), the partition over owners is exact, and the digest is stable across two freezes of the same input.
- **Sealed plan review.** The seven-batch maximum witness is real: five normal batches, a valid high unlocking reserve, then two reserve batches, ending converged at `spent == 7`. Upheld-dismissal streak preservation, overturned-dismissal reserve unlock, repair-before-verification, the six-repair cap, resume without replenishment and clean-suffix foreclosure each have a distinct assertion and a killed mutation.
- **Successor registry and fresh evidence.** Reuse of predecessor, ancestor, sibling and unrelated ids is rejected; a second successor is rejected; a misbound receipt is rejected; ancestry reconstructs in full; predecessor spend and the complete carried map are preserved. Same-evidence relitigation and an unknown reopen root are rejected, siblings are preserved, and reopen before every initial attempt is rejected. These are the best-grounded parts of the model.
- **Legacy adoption.** All five forbidden paths (direct campaign, zero-obligation reinterpretation, inferred stage, historical clean credit, successor receipt presented as adoption) are rejected, and both legal paths are constructible.
- **Blind-closure scope and dismissal product.** The full table is exercised per stable id: low to backlog, medium to terminal, high pending then upheld to terminal or overturned through each of the four owner routes, critical to `SeriousBlocked` on both results, dual pending axes requiring both results, and per-id re-check reducers that leave siblings pending. This is the most thoroughly covered area of the proof.
- **Command reproducibility and repository cleanliness.** Covered in the section above: ten invocations, per-invocation fresh external state, identical stdout, stderr and exit status across passes for all five commands, and byte-identical `git status` and 530-entry working-tree manifest before and after.
- **Planning-only boundary.** The diff is 13 planning artefacts; no runtime dependency is added; the scripts import the standard library only; nothing writes into the repository tree under the specified commands. Criterion 15 holds, and no production step for bounded convergence is authored.

## What I did not do

I did not edit any product file, and I did not run the repository's own gates (`render --check`, `validate --workflow`), which are the implementation review's ordinary-gate step and are unaffected by a diff that touches no plan source. Every demonstration ran against a `/tmp` extract of `HEAD`.
