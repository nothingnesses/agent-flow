# Option B proof work review round 2 (reviewer: claude)

## Scope and reproduction

I reviewed `main...a167d71a` independently. I read `AGENTS.md`, `.agents/prompts/reviewer.md`, the `bounded-convergence-option-b-proof` sidecar, all 13 proof artefacts and eight fixtures, the five retained Q-86 synthesis triages, and the round-1 triage `agent-scaffold.reviews/option-b-proof-r1-triage.md`. I did not read any round-2 reviewer output.

The reviewed diff adds only the 13 files under `docs/plans/workflow-calibration.proofs/`. No production file, workflow rule, controller, pack source, generated copy, README, changelog, metrics schema, or ledger state changes (`git diff --name-only main...HEAD | grep -v '^docs/plans/workflow-calibration.proofs/'` is empty). All 13 files are pure ASCII. Criterion 15 holds.

I ran the five exact sidecar commands twice from the repository root, each of the ten invocations with a fresh external state directory (`TMPDIR`/`TMP`/`TEMP`/`XDG_CACHE_HOME`/`XDG_STATE_HOME`/`PYTHONPYCACHEPREFIX` pointed there), never changing the working directory, comparing each command's two passes and then removing both states. Results:

| Command | Pass 1 | Pass 2 | Summary |
| --- | --- | --- | --- |
| `--suite all --floor high` | 0 | 0 | `selected_floor=high`, all nine failure counters 0 |
| `--suite all --floor critical` | 0 | 0 | `comparison_floor=critical`, all nine failure counters 0 |
| `--suite algebra --floor high` | 0 | 0 | five derived formulas, domains, premises, early paths |
| traceability | 0 | 0 | `valid_findings=51 executable_rows=30 resolved_rows=30 exercised_rows=30 killed_rows=30 unresolved=0` |
| mutations `--all` | 0 | 0 | `discovered_tags=151 mutations=151 unexercised=0 survived=0` |

Every command's stdout, stderr, and exit status were byte-identical across the two passes. `git status --porcelain=v1 --untracked-files=all` and a complete non-Git path/type/content manifest of the working tree (534 entries, ignored paths included, `.git` excluded) were byte-identical before the first and after the tenth invocation. Criterion 13 holds and no repository artefact was created, removed, or changed.

Every demonstration below was run in a `git archive HEAD` extract outside the repository, using the same lock-bound Nix Python (3.13.13). All extracts were removed afterwards.

## Independent derivations

- **51 traceability ids.** I derived the round-qualified valid set from the five retained triages with an independent `awk` pass (58 `### T` sections total, 51 carrying a `valid` verdict). `diff` against the matrix identity set is empty. All 21 durable-text pointers resolve to a unique substring in a planning source that this branch does not modify, including R1-T12, which now cites the stable sidecar sentence rather than the mutable ledger anchor.
- **Bound witnesses.** I removed the batch/repair caps from `_campaign_is_legal` and ran an exhaustive DFS over the campaign transition API (initial batch with 0/1 findings per target owner, repair, verify, reopen, deferred reopen, closure) keeping only paths for which `FrozenFamily.complete` succeeds. Maximum delivering batch counts: `n_q=0 -> 1`, `n_q=1 -> 5`, `n_q=2 -> 9`, i.e. exactly `4n_q + 1`. `C_q` is therefore a genuine property of the transition relation and not only of the guard (see F6).
- **Derived, not printed, formulas.** Adding `"repair"` to `REVIEW_TRANSITIONS` and removing the caps changes the algebra output to `formula C_q=6n_q+1`, `formula R_B=6|O|+m+8`, `formula I_B=26|O|+4m+38`. Round-1 T3's "printed contract is not derived output" is fixed.
- **Cross-credit witness.** Under `mut-algebra-cross-credit`, `clean_delivering_phase(2)` returns `batches=2, delivering_domain=True, credited=('O-0-0','O-0-1')`: the mutant stays inside the independently observable ordinary-delivery domain and measures `L_q = 2 < n_q + 1 = 3`, exactly as the sidecar requires. It is not filtered out. See F7 for how it is actually killed.
- **Repository writes.** Importing `q86-option-b-mutations.py` by path without `PYTHONDONTWRITEBYTECODE` and calling `run_manifest("q86-option-b")` creates no `__pycache__` or `.pyc` anywhere (round-1 T10 fixed). Deleting the checker makes `--all` exit 1 with `required traceability checker is missing` (round-1 T11 fixed).

## Round-1 fix verification

Fixed and verified by mutation: T1, T2, T3, T5, T7, T8, T9, T10, T11. Notably T2 (`completed`/`blind_closure_spent` are now computed properties bound to family id, freeze digest, registry, owner keys, settled attempts, closure evidence, continuity and merged-history blocks; passing `completed=True` to the constructor raises `TypeError`) and T5 (emptying `campaigns.json` `obligations`, `products.json` `findings`, or `successors.json` `families` now turns the suites red, and removing a single `legacy.json` `forbidden` entry is caught by the mutation runner as unexercised-and-surviving).

Partially fixed: **T4** (views are now distinct reconstructions and degenerate streams fail, but the equality oracle remains blind to shared-reducer defects and all 50 replay mutations are injected after reconstruction, F1/F2), **T5** (residual decorative fixture fields, F4/F8), **T6** (`--floor` is still inert, F3).

## Findings

Severity counts: **0 critical, 1 high, 3 medium, 4 low.** I found nothing at critical severity: I could not construct a `Complete` carrying an unexamined obligation, a live current/prior/future/unowned route, a carried finding, a pending scope or dismissal re-check, or a terminal/serious scope block, and no unresolved critical reaches delivery under either floor.

### F1 - The replay equality oracle cannot see a defect in the shared reducer, and all 50 replay mutations are injected after reconstruction

- **Severity:** high.
- **Evidence.** In a scratch extract, delete `self.remaining_authority -= spend` from `ReplayState.apply` (`docs/plans/workflow-calibration.proofs/q86-option-b-proof.py:1452`), so replay authority is never consumed. All five exact commands still exit 0 with unchanged summaries, including `manifest=q86-option-b discovered_tags=151 mutations=151 unexercised=0 survived=0`.
- **Root cause.** `check_replay` (`:2589-2592`) compares each view's snapshot to `reduce_replay(events)`, which is `reconstruct_replay(events, "baseline")` (`:1616-1617`) - the same reducer every view uses. Any defect in `ReplayState.start`/`apply` shifts baseline and views equally, so equality still holds. The remaining assertion `snapshots[-1].remaining_authority == expected.remaining_authority` (`:2594`) is the same self-comparison and is already implied by `:2592`. Separately, `replay_view` (`:1620-1638`) applies every `replay-<view>-<field>` and `replay-<view>-replenishment` mutation to the snapshot *after* `reconstruct_replay` has returned, so no replay mutation perturbs a reconstruction rule. I mapped every mutation to its killing frame: 50 of 151 (33 percent) die at the single assertion `q86-option-b-proof.py:2592`.
- **Why this matters.** Criterion 4 requires the five views to compare equal on remaining authority "with no replenishment"; the sidecar's mandatory mutation set requires that mutations which "mint fresh authority without a material change, must be exercised and killed"; the spec asserts (`q86-option-b-spec.md:157`) that "Every compared field is derived from the start event and subsequent transitions". A model in which authority is never spent at all passes every command. The oracle does detect a per-view divergence (dropping the finding map in `ReplayState.resume` at `:1509` turns `identity_failures` to 1), so the fix is to add reconstruction-level mutations and at least one derivation that is independent of `replay_events`.

### F2 - The unchanged-replan view's only distinguishing rule is uncovered

- **Severity:** medium.
- **Evidence.** Replace the call `unchanged_replan_rejected(state)` at `q86-option-b-proof.py:1610` with `pass`. All five exact commands exit 0 with unchanged summaries, and the ten `mut-replay-unchanged-replan-*` entries are still reported exercised and killed.
- **Reasoning.** `unchanged_replan_rejected` (`:1551-1588`) is the whole substance of the fifth view: it is the only place the replay oracle exercises the sidecar rule that an unchanged replan "cannot mint a successor family, reset spend, reopen settled evidence, or replenish any review or closure authority". With it removed, the `unchanged-replan` view reduces to the baseline view plus a fixture-shape check. The ten mutations named for that view do not cover it, because they only corrupt the returned snapshot (F1). The spec claims (`q86-option-b-spec.md:159`) that the unchanged replan "is rejected by the actual global freshness rule"; nothing kills the removal of that invocation.

### F3 - The `--floor` argument is inert, so the second exact command adds no executable coverage

- **Severity:** medium.
- **Evidence.** Replace `EXECUTION_FLOOR = floor.value` with `EXECUTION_FLOOR = "high"` in `run_suite` (`q86-option-b-proof.py:3055`), so the parsed floor is discarded entirely. All five exact commands exit 0; the second command still prints `architecture=FrozenObligationsWithSealedPhaseCampaigns comparison_floor=critical suite=all` and nine zero counters. Separately, `finding_blocks_delivery(record, floor)` (`:608-626`) never reads its `floor` parameter: replacing its only call site `finding_blocks_delivery(item, complete.floor)` (`:1776`) with a constant `Floor.CRITICAL` also leaves all five commands green.
- **Reasoning.** `EXECUTION_FLOOR` has exactly one consumer, `check_complete_gate:2651`, and that oracle already constructs a hard-coded `Floor.CRITICAL` family unconditionally (`:2665-2671`), so the critical-floor family is built in the `high` run too and the parsed floor changes nothing observable. Round-1 T6's exact correction was to "thread the parsed floor through model construction and suite execution"; construction is threaded (`FreezePending.freeze:1001`) but no predicate or transition consumes it, so `--floor critical` is a relabelled duplicate of `--floor high`. The floor does matter in `terminal_choice` (`:1363-1379`) and `serious_delivery_blocked` (`:1383`), and `terminal-choices.json` covers both floors and all 14 `TerminalKind` values, so criterion 9 holds; what is unproved is the sidecar's separate requirement that the comparison invocation execute a distinct model. The spec's family-completion bullet "No terminal or serious scope block remains **under the selected floor**" (`q86-option-b-spec.md:122`) overclaims, since `FrozenFamily.complete` never consults the floor.

### F4 - The arbitrary-finite-history oracle does not execute the serious-dismissal or scope axes it claims

- **Severity:** medium.
- **Evidence.** In `docs/plans/workflow-calibration.proofs/fixtures/products.json`, set every `history_extensions` entry to `"severity": "low", "scope": "in-scope", "triage": "valid"`, so no fresh serious dismissal and no fresh scope referral exists at all. All five exact commands exit 0 with unchanged summaries.
- **Reasoning.** `check_arbitrary_history` (`q86-option-b-proof.py:2321-2329`) asserts only `len(extended.findings) == 260` and that the three ids are present; the severity, scope, and triage fields have no executable effect. The extension is also performed as `history.extend(records)` at the `HistoryQuotient` level, so no campaign transition (`initial_batch`, `blind_closure`, `scope_recheck`, `dismissal_recheck`, `reopen`) is exercised after the settled history. The sidecar requires "The oracle must include settled history followed by fresh valid, serious-dismissal, and scope batches" and criterion 5 requires executable interaction controls covering fresh events after settled history; matrix row R5-T1 cites this oracle for "persistent arbitrary history". The spec statement "Every field is parsed and executed" (`q86-option-b-spec.md:202`) is false for `products.json`.

### F5 - Dead state and no-op APIs in the reference model

- **Severity:** low.
- **Evidence.** In a scratch extract, delete `history_digest` (`q86-option-b-proof.py:671-691`) and `maximum_phase_witness` (`:1855-1857`), replace `owner_digest = digest(owner_projection)` (`:324`) with a constant string, and replace `phase_accounts=tuple((phase, 0) for phase in result.phases)` (`:1007`) with `(("DEAD", -999),)`. All five exact commands exit 0 with unchanged summaries. `grep -n` confirms `history_digest` and `maximum_phase_witness` have no call site, and `owner_digest` and `phase_accounts` are written once and never read. `SourceFinding.title` (`q86-option-b-traceability.py:51`) is parsed at `:117` and never used.
- **Reasoning.** The sidecar makes the freeze produce "exact post-freeze phase ownership for every obligation ... and their canonical digests" and gives `FrozenFamily` "phase accounts"; both are present as fields but neither participates in any equality, reconstruction, or authority check, so those two claims are unproved rather than false. This is the same class as round-1 T7's write-only `deferred_reopens`, whose exact correction was applied to that one field only. Either drive these through an assertion and a tagged mutation, or remove them.

### F6 - The published maximum is hard-coded inside the delivery legality predicate

- **Severity:** low.
- **Evidence.** `_campaign_is_legal` rejects any campaign with `campaign.batches > 4 * len(expected_keys) + 1` or `campaign.repair_count > 2 * len(expected_keys)` (`q86-option-b-proof.py:1077-1078`). Removing both clauses leaves all five exact commands green, so they are currently dead and carry no mutation tag. The mechanism is visible when the transition accounting changes: adding `"repair"` to `REVIEW_TRANSITIONS` (`:667`) makes the maximum witness 6 batches for `n_q=1`, and the shipped model then fails with `ValueError: family cannot construct Complete` raised from `_campaign_is_legal` via `drive_maximum_family` (`:1768` -> `:1125`); with the two clauses removed, the identical edit instead correctly reports `formula C_q=6n_q+1`.
- **Reasoning.** I verified by exhaustive search (see Independent derivations) that `4n_q + 1` really is the transition relation's maximum for `n_q` in 0, 1, 2, so no published coefficient is currently wrong. The defect is structural: the sidecar requires the proof to "derive rather than repeat these selected Option B bounds" and warns that "Hard-coding the published formula without deriving every coefficient is a proof failure". Embedding `4n_q + 1` in the predicate that decides whether a family may deliver means any future transition change that admits a longer delivering path is silently reclassified as an illegal campaign instead of falsifying `C_q`. Remove the clauses, or derive the limit from `derive_coefficients()` and give it a tagged mutation.

### F7 - The mandated cross-credit witness kills nothing; the mutation dies on an unrelated driver crash

- **Severity:** low.
- **Evidence.** Activating `mut-algebra-cross-credit` and running the `algebraic-bounds` oracle raises `ValueError: scheduled owner is not untested` with the frames `q86-option-b-proof.py:2618` -> `:1757` -> `:770`: `drive_maximum_family` (`:1740-1757`) iterates every owner and re-schedules one the mutation has already credited. That happens at `check_algebra:2618`, before the mandated witness at `:2639-2642` is reached. I mapped all 151 mutations to their killing frame; no mutation is killed at `:2642`.
- **Reasoning.** The witness itself is correct - I called `clean_delivering_phase(2)` directly under the mutation and got `batches=2, delivering_domain=True`, that is `L_q < n_q + 1`, with the mutant still in domain - so the property holds and this is an evidence-quality defect, not an unsound bound. But the sidecar names this witness as "The required cross-credit killing witness" (sidecar line 180) and criterion 10 requires the mutant to "report `L_q < n_q + 1`", while matrix rows R1-T2, R1-T7 and R2-T6 cite `mut-algebra-cross-credit` as the evidence that the model "derives the Option B campaign minimum and kills cross-credit". The reported kill demonstrates something weaker. Make `drive_maximum_family` skip already-credited owners (or move the witness before the finite-case loop) so `:2642` is the killing assertion.

### F8 - `campaigns.json` attempt names are a decorative field checked against a duplicated literal

- **Severity:** low.
- **Evidence.** `check_owner_routing` consumes `maximum_attempts` and `closure` only at `q86-option-b-proof.py:2007-2013`, asserting them equal to a literal list repeated in the source. One of the four names, `fresh-evidence-reopen`, is not a transition kind the model can emit: `REVIEW_TRANSITIONS` (`:667`) and `PhaseCampaign.reopen` (`:906`) use `reopen-review`. `grep -n "fresh-evidence-reopen" docs/plans/workflow-calibration.proofs/q86-option-b-proof.py` returns exactly one hit, `:2011`, which is the duplicated literal inside the assertion itself; no `CampaignTransition` in the model ever carries that kind.
- **Reasoning.** The assertion can only detect an edit to the fixture, never a change to the model's per-obligation attempt lifecycle, so the field is presented as proof input while carrying none. Round-1 T5's exact correction was to "Remove any fixture field that deliberately has no semantic role instead of presenting it as proof input", and the spec advertises these as "attempt names" supplied by the fixture (`q86-option-b-spec.md:201`). Either join the list to `REVIEW_TRANSITIONS` and the campaign's actual transition kinds, or drop the two fields.

## Documentation currency

`q86-option-b-spec.md:157` ("Every compared field is derived from the start event and subsequent transitions"), `:159` (unchanged replan "rejected by the actual global freshness rule"), `:202` ("Every field is parsed and executed") and `:122` ("under the selected floor") are stale relative to the shipped model; they are cited inside F1, F2, F4 and F3 rather than raised separately. The sidecar and the traceability matrix are otherwise accurate, and no shipped product documentation is made stale by this planning-only unit.

## Notes on things I checked and did not raise

- Repository formatter: `nix fmt` rewraps 7 of the 8 new fixture JSON files, but `main` is already formatter-dirty in 65 files, so the project does not enforce this gate, and formatter-owned wrapping is excluded from findings by `.agents/prompts/reviewer.md`.
- The ledger's `RESUME HERE` anchor still names round 1 and commit `e76367cb`. Advancing it is an explicit orchestrator duty under the sidecar, the ledger is outside the reviewed diff, and its "All five exact commands pass" sentence is now true at this tip.
- `_campaign_is_legal` reading public dataclass fields is inherent to a Python reference model and is acknowledged in `q86-option-b-spec.md:227`; the completion gate rejects every forged product I constructed.
